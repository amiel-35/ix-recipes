#!/usr/bin/env python3
"""harnais.py — les outils du pilote autour d'un sujet traité de bout en bout (docs/harnais/spec-harnais.md).

    harnais.py lancer TYPE [options de parcours.py new]   ouvre le sujet : T1, T2, étape 0, parcours de l'amont
    harnais.py trace                                       écrit ou met à jour la trace A3 du sujet
    harnais.py suite CLE SUITE [NOMBRE|TEXTE]              consigne la suite choisie par le pilote à un plafond atteint
    harnais.py contre-verif FICHIER                        rend à l'amont la sortie de la contre-vérification
    harnais.py geler DOSSIER_LIVRABLE FICHIER...           fige les fichiers, scelle la part cachée, déclare le hook
    harnais.py sceau                                       (pilote) le chemin du scellé du sujet
    harnais.py empreintes                                  vérifie les empreintes des fichiers figés
    harnais.py tour | tour-correction                      avant un tour de production | de correction
    harnais.py regeler                                     regel après un « contourner » (retour en 2B)
    harnais.py fin-production                              commite le livrable et pose l'étiquette
    harnais.py juge                                        lance le juge du sujet
    harnais.py ouvrir                                      fin du jugement : verse la part cachée et la trace du juge
    harnais.py hook                                        événement PreToolUse (JSON sur l'entrée standard)

Chaque commande tourne dans le dossier du sujet (variables S, R, L), avec IX_SCELLE_DIR donné par l'appelant.
Code de sortie 0 : accepté ; 1 : refusé, avec une ligne qui nomme la cause ; 2 : ligne de commande mal construite.
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import commun as C                      # noqa: E402
import trace_a3                         # noqa: E402
from commun import HarnaisError, P      # noqa: E402

GOAL_FILE = "goal.md"                    # le goal du sujet, quand il est posé à la racine ; sinon la sortie de l'étape du goal
CONSTAT_FILE = "constat-juge.md"         # le constat destiné au producteur : l'exigence de chaque ligne en échec
JUGEMENT_DIR = "jugement"                # là où le jugement s'ouvre, à la fin
SLOT = re.compile(r"<[A-Z][A-Z0-9_]+>")
LIGNE_VERDICT = re.compile(r"^\|(.+)\|\s*$")
SUITES_AVEC_NOMBRE = ("relancer",)
SUITES_AVEC_TEXTE = ("contourner", "livrer_avec_reserve")


# ---------------------------------------------------------------------------
# Petits outils
# ---------------------------------------------------------------------------
def ligne_etat(etat, cle, row, t=None):
    """Consigne un geste du harnais comme une ligne de T3 (la trace est reconstruite de l'état)."""
    etat.setdefault("lignes", []).append({"t": t or P.now_us(), "cle": cle, "row": row})


def reglages_du_sujet(etat):
    return etat["reglages"]


def plafond_valeur(etat, cle):
    plafonds = etat["reglages"]["plafonds"]
    if cle not in plafonds:
        raise HarnaisError(f"les réglages n'ont pas de plafond '{cle}'")
    return plafonds[cle]


def valider_chemin_relatif(sujet, valeur, quoi):
    chemin = Path(valeur)
    if chemin.is_absolute() or ".." in chemin.parts:
        raise HarnaisError(f"{quoi} '{valeur}' : un chemin relatif au dossier du sujet est attendu")
    return chemin


def dossier_livrable(sujet, valeur):
    """Le dossier du livrable : un chemin relatif au sujet, ou absolu (le livrable peut vivre dans un dépôt à côté)."""
    chemin = Path(valeur)
    return (chemin if chemin.is_absolute() else Path(sujet) / chemin).resolve()


def livrable_affiche(sujet, etat):
    """Le dossier du livrable tel que la trace le montre : relatif au sujet (`../sujet.livrable` quand il est à côté)."""
    return os.path.relpath(dossier_livrable(sujet, etat["gel"]["livrable"]), Path(sujet).resolve())


def aplatir(sujet, valeurs):
    """Les fichiers désignés (un dossier donne tous ses fichiers), chemins relatifs, dans l'ordre, sans doublon."""
    fichiers = []
    for valeur in valeurs:
        chemin = valider_chemin_relatif(sujet, valeur, "fichier figé")
        absolu = Path(sujet) / chemin
        if absolu.is_dir():
            trouves = sorted(p for p in absolu.rglob("*") if p.is_file())
            if not trouves:
                raise HarnaisError(f"dossier figé vide : {valeur}")
            candidats = [p.relative_to(sujet).as_posix() for p in trouves]
        elif absolu.is_file():
            candidats = [chemin.as_posix()]
        else:
            raise HarnaisError(f"fichier à figer introuvable : {valeur}")
        for c in candidats:
            if c not in fichiers:
                fichiers.append(c)
    return fichiers


def classer(chemin):
    """L'élément de T9 d'un fichier figé, d'après son nom (A3 : script de recette, grille visible, fixtures, ou autre)."""
    nom = chemin.lower()
    if "fixture" in nom:
        return "fixtures"
    if "grille" in nom:
        return "grille visible"
    if re.search(r"(accept|recette|script)", nom) or nom.endswith((".sh", ".py")):
        return "script de recette"
    return "autre élément figé"


def ecrire_empreintes(sujet, fichiers, scelle):
    lignes = []
    for f in fichiers:
        lignes.append(f"{C.sha256_file(Path(sujet) / f)}  {f}")
    texte = "\n".join(lignes) + "\n"
    C.write_atomic(Path(sujet) / C.ETAT_DIR / C.EMPREINTES_FILE, texte)
    C.write_atomic(scelle / C.EMPREINTES_FILE, texte, mode=0o600)
    return lignes


def lire_empreintes(chemin):
    attendu = {}
    for ligne in Path(chemin).read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        empreinte, _, nom = ligne.partition("  ")
        attendu[nom] = empreinte
    return attendu


def verifier_empreintes(sujet, etat, scelle):
    """Le premier écart, en nommant le fichier, ou None. Les empreintes du sujet sont comparées aux fichiers, et celles du
    sujet à la copie gardée au scellé : un producteur qui récrit les deux ne rattrape pas la copie qu'il ne voit pas."""
    if not etat.get("gel"):
        return "le sujet n'est pas gelé"
    chez_sujet = Path(sujet) / C.ETAT_DIR / C.EMPREINTES_FILE
    chez_scelle = scelle / C.EMPREINTES_FILE
    if not chez_sujet.is_file():
        return f"le fichier d'empreintes {C.ETAT_DIR}/{C.EMPREINTES_FILE} a disparu"
    if not chez_scelle.is_file():
        return "la copie des empreintes gardée au scellé a disparu"
    if chez_sujet.read_bytes() != chez_scelle.read_bytes():
        return f"le fichier d'empreintes {C.ETAT_DIR}/{C.EMPREINTES_FILE} ne correspond plus à la copie du scellé"
    attendu = lire_empreintes(chez_scelle)
    figes = etat["gel"]["fichiers"]
    if sorted(attendu) != sorted(figes):
        return "la liste des fichiers figés a changé"
    for fichier in figes:
        chemin = Path(sujet) / fichier
        if not chemin.is_file():
            return f"{fichier} : fichier figé disparu"
        if C.sha256_file(chemin) != attendu[fichier]:
            return f"{fichier} : l'empreinte a changé"
    return None


def trouver_goal(sujet):
    """Le goal du sujet : `goal.md` à la racine du sujet, sinon la sortie de l'étape du goal de l'amont."""
    direct = Path(sujet) / GOAL_FILE
    if direct.is_file():
        return direct.read_text(encoding="utf-8")
    amont = C.etat_amont(sujet)
    if amont:
        etape = C.manifeste().get("ETAPE_GOAL")
        for step in amont["steps"]:
            if step["id"] == etape and (step.get("handoff") or {}).get("goal"):
                return step["handoff"]["goal"]
    return None


def emplacements_vides(goal):
    """Les emplacements réservés encore en chevrons hors de la section « Valeurs fixées plus tard » du goal."""
    texte, dedans = [], False
    for ligne in goal.splitlines():
        titre = re.match(r"#{1,6}\s+(.*)", ligne)
        if titre:
            dedans = bool(re.match(r"(values fixed later|valeurs fixées)", titre.group(1).strip(), re.I))
        if not dedans:
            texte.append(ligne)
    return sorted(set(SLOT.findall("\n".join(texte))))


# ---------------------------------------------------------------------------
# lancer
# ---------------------------------------------------------------------------
def cmd_lancer(args):
    sujet = C.dossier_sujet()
    C.scelle(sujet)
    if C.charger_etat(sujet, requis=False):
        raise HarnaisError("ce sujet est déjà lancé (voir .harnais/etat.json)")
    demande = sujet / "demande.md"
    if not demande.is_file() or not demande.read_text(encoding="utf-8").strip():
        raise HarnaisError("demande.md manque ou est vide dans le dossier du sujet")
    donnees, chemin, empreinte = C.reglages()
    types = donnees.get("types_de_sujet") or {}
    if args.type not in types:
        raise HarnaisError(f"type de sujet '{args.type}' absent des réglages (types : {', '.join(types) or 'aucun'}) : rien n'est créé")
    if isinstance(types[args.type], dict) and "statut" in types[args.type]:
        raise HarnaisError(f"type de sujet '{args.type}' : {types[args.type]['statut']}, il n'a ni réglages, ni annexes, ni skills : "
                           "rien n'est créé")
    valeurs = C.manifeste()
    recette = valeurs["RECETTE"]
    pieces = [str(C.chemin_manifeste("A4")), str(C.chemin_manifeste("A5"))]
    options = list(args.options)
    if "--corpus" in options:   # les pièces du pilote s'ajoutent à celles du harnais (les réglages et la grille du cadrage)
        i = options.index("--corpus") + 1
        options[i:i] = pieces
    else:
        options += ["--corpus", *pieces]
    for interdit in ("--slug", "--input", "--parcours-dir"):
        if interdit in options:
            raise HarnaisError(f"l'option {interdit} est fixée par le harnais")
    debut = P.now_us()
    code = P.main(["new", recette, "--input", str(demande), "--slug", C.PARCOURS_SLUG, "--title", C.titre_de(sujet)[:120],
                   "--parcours-dir", str(sujet / "parcours"), *options])
    if code != 0:
        raise HarnaisError("l'exécuteur a refusé de créer le parcours de l'amont")
    etat = {
        "version": 1, "sujet": sujet.name, "titre": C.titre_de(sujet), "type": args.type, "pilote": C.pilote(),
        "debut": debut[:19], "debut_us": debut,
        "reglages": {
            "version": str(donnees.get("version")), "sha256": empreinte,
            "plafonds": {k: v for k, v in (donnees.get("plafonds") or {}).items() if type(v) is int},
            "production": {k: v for k, v in (donnees.get("production") or {}).items() if type(v) is int},
            "suites": {k: list(v) for k, v in (donnees.get("suites_au_plafond") or {}).items() if isinstance(v, list)},
            "modeles": {k: v for k, v in (donnees.get("modeles") or {}).items() if isinstance(v, str)},
            "contre_verification": dict(((donnees.get("modeles") or {}).get("contre_verification")) or {}),
        },
        "lignes": [], "tours": {"goal": 0, "correction": 0}, "extra": {"tours_goal": 0, "tours_correction": 0},
        "suites": [], "plafonds_atteints": [], "elements": [], "points": [], "juge": {"appels": []},
        "gel": None, "livrable": None, "ouvert": None,
    }
    C.sauver_etat(sujet, etat)
    trace_a3.ecrire(sujet)
    print(f"Sujet lancé : {sujet.name} (type {args.type}). Parcours de l'amont : parcours/{C.PARCOURS_SLUG}. Trace : {trace_a3.TRACE_FILE}.")
    return 0


# ---------------------------------------------------------------------------
# trace, suite, contre-vérification
# ---------------------------------------------------------------------------
def cmd_trace(args):
    sujet = C.dossier_sujet()
    C.scelle(sujet)
    chemin = trace_a3.ecrire(sujet)
    print(f"Trace A3 écrite : {chemin.relative_to(sujet)}")
    return 0


def cmd_suite(args):
    sujet = C.dossier_sujet()
    C.scelle(sujet)
    etat = C.charger_etat(sujet)
    suites = etat["reglages"]["suites"]
    cle = args.cle[:-4] if args.cle.endswith("_max") else args.cle   # `tours_goal_max` (le plafond) ou `tours_goal` (ses suites)
    if cle not in suites:
        raise HarnaisError(f"plafond '{args.cle}' inconnu des réglages (plafonds avec suites : "
                           f"{', '.join(k + '_max' for k in suites)})")
    if args.suite not in suites[cle]:
        raise HarnaisError(f"suite '{args.suite}' hors de suites_au_plafond.{cle} des réglages (suites offertes : "
                           f"{', '.join(suites[cle])})")
    nombre, texte = None, None
    if args.suite in SUITES_AVEC_NOMBRE:
        if args.valeur is None or not re.fullmatch(r"[1-9]\d*", args.valeur):
            raise HarnaisError(f"'{args.suite}' prend un nombre (le pilote fixe combien de tours ou de passes de plus)")
        nombre = int(args.valeur)
    elif args.suite in SUITES_AVEC_TEXTE:
        if not (args.valeur or "").strip():
            raise HarnaisError(f"'{args.suite}' prend un texte "
                               f"({'le critère revu et la raison' if args.suite == 'contourner' else 'la réserve'})")
        texte = args.valeur.strip()
    pilote = C.pilote()
    if cle == "passes_verification":
        amont = C.etat_amont(sujet)
        pending = (amont or {}).get("pending")
        if not pending or pending["type"] != "ceiling":
            raise HarnaisError("aucun plafond des passes de vérification n'est atteint dans l'amont")
        options = ["--suite", args.suite, "--by", pilote]
        if nombre:
            options += ["--n", str(nombre)]
        if texte:
            options += ["--text", texte]
        code = P.main(["suite", C.PARCOURS_SLUG, "--parcours-dir", str(sujet / "parcours"), *options])
        if code != 0:
            raise HarnaisError("l'exécuteur a refusé la suite")
        trace_a3.ecrire(sujet)
        return 0
    compteur = "goal" if cle == "tours_goal" else "correction"
    atteint = next((a for a in reversed(etat["plafonds_atteints"]) if a["plafond"] == f"{cle}_max"
                    and not any(s.get("atteint_id") == a["id"] for s in etat["suites"])), None)
    if not atteint:
        limite = plafond_valeur(etat, f"{cle}_max") + etat["extra"][cle]
        raise HarnaisError(f"le plafond {cle}_max n'est pas atteint ({etat['tours'][compteur]} tour(s) sur {limite}) : "
                           "une suite ne se consigne qu'à un plafond atteint")
    enregistrement = {"cle": cle, "suite": args.suite, "n": nombre, "texte": texte, "par": pilote, "at": P.now(),
                      "t": P.now_us(), "atteint_id": atteint["id"], "apres_gel": (etat["gel"] or {}).get("regels", 0), "utilise": False}
    if nombre:
        etat["extra"][cle] += nombre
    if args.suite == "abandonner":
        etat["abandonne"] = True
    if args.suite == "livrer_avec_reserve":
        etat["livre_avec_reserve"] = True
    etat["suites"].append(enregistrement)
    C.sauver_etat(sujet, etat)
    trace_a3.ecrire(sujet)
    print(f"Suite consignée à {cle}_max : {args.suite}" + (f" {nombre}" if nombre else ""))
    return 0


def cmd_contre_verif(args):
    sujet = C.dossier_sujet()
    C.scelle(sujet)
    C.charger_etat(sujet)
    etape = C.manifeste()["ETAPE_CONTRE_VERIF"]
    amont = C.etat_amont(sujet)
    pending = (amont or {}).get("pending")
    if not pending or pending["type"] != "external" or pending["step"] != etape:
        raise HarnaisError(f"la recette n'est pas arrêtée avant l'étape '{etape}' : rien à rendre")
    fichier = Path(args.fichier)
    if not fichier.is_file():
        raise HarnaisError(f"fichier introuvable : {fichier}")
    options = []
    if os.environ.get("IX_MODELE_EXTERNE"):
        options += ["--model", os.environ["IX_MODELE_EXTERNE"]]
    code = P.main(["supply", C.PARCOURS_SLUG, etape, "--file", str(fichier), "--parcours-dir", str(sujet / "parcours"), *options])
    if code != 0:
        raise HarnaisError("l'exécuteur a refusé la sortie de la contre-vérification")
    trace_a3.ecrire(sujet)
    return 0


# ---------------------------------------------------------------------------
# geler, empreintes, regeler
# ---------------------------------------------------------------------------
def part_cachee(sujet, etat, scelle):
    """[(nom, chemin)] des champs cachés que l'amont a scellés."""
    amont = C.etat_amont(sujet)
    if not amont:
        return []
    dossier = scelle / amont["slug"]
    trouves = []
    if dossier.is_dir():
        for step in amont["steps"]:
            for champ in (step.get("hidden") or {}):
                chemin = dossier / f"{step['id']}.{champ}.md"
                if chemin.is_file():
                    trouves.append((f"{step['id']}.{champ}", chemin))
    return trouves


def declarer_hook(sujet):
    """Déclare le hook de HOOKS_FICHIER dans les réglages de projet du sujet (`.claude/settings.json`), mot pour mot et sans
    toucher à ce qui s'y trouve déjà. La commande du hook cite `$R`, la racine d'ix-recipes : le pilote l'exporte dans
    l'environnement de la session de production, comme il le fait pour toutes les commandes du harnais."""
    source = C.chemin_manifeste("HOOKS_FICHIER")
    try:
        entrees = json.loads(source.read_text(encoding="utf-8"))["hooks"]["PreToolUse"]
    except (OSError, ValueError, KeyError) as exc:
        raise HarnaisError(f"fichier des hooks illisible : {source} ({exc})") from None
    cible = Path(sujet) / ".claude" / "settings.json"
    reglages = {}
    if cible.is_file():
        try:
            reglages = json.loads(cible.read_text(encoding="utf-8"))
        except ValueError:
            raise HarnaisError(f"{cible.relative_to(sujet)} n'est pas du JSON : je n'y touche pas") from None
    reglages.setdefault("hooks", {}).setdefault("PreToolUse", [])
    for entree in entrees:
        if entree not in reglages["hooks"]["PreToolUse"]:
            reglages["hooks"]["PreToolUse"].append(entree)
    C.write_atomic(cible, json.dumps(reglages, indent=2, ensure_ascii=False) + "\n")
    return cible


def pointer_sujet(livrable, sujet):
    """Si le livrable est un dépôt git, y noter (dans `.git/`, que le dépôt ne suit pas) le sujet auquel il appartient :
    le hook, lancé depuis le dossier du livrable, retrouve ainsi les fichiers figés de ce sujet."""
    git_dir = Path(livrable) / ".git"
    if git_dir.is_dir():
        C.write_atomic(git_dir / "ix-sujet", str(Path(sujet).resolve()) + "\n")


def elements_gel(sujet, fichiers, cle_ligne):
    rows = []
    for f in fichiers:
        rows.append({"élément": classer(f), "état": "figé", "empreinte_sha256": C.sha256_file(Path(sujet) / f),
                     "emplacement": f, "cle_ligne": cle_ligne, "ouvert_à": "sans objet"})
    return rows


def elements_caches(etat, cachees, cle_ligne):
    rows = []
    for nom, chemin in cachees:
        rows.append({"élément": "part cachée", "état": "scellé", "empreinte_sha256": C.sha256_file(chemin),
                     "emplacement": "non écrit", "cle_ligne": cle_ligne, "ouvert_à": "à venir", "source": nom})
    return rows


def cmd_geler(args):
    sujet = C.dossier_sujet()
    scelle = C.scelle(sujet)
    etat = C.charger_etat(sujet)
    if etat.get("gel"):
        raise HarnaisError("ce sujet est déjà gelé : après un « contourner », c'est `regeler`")
    if not args.fichiers:
        raise HarnaisError("aucun fichier à figer")
    livrable = dossier_livrable(sujet, args.livrable)
    if livrable == Path(sujet).resolve() or livrable in Path(sujet).resolve().parents:
        raise HarnaisError("le dossier du livrable ne peut pas contenir le dossier du sujet")
    fichiers = aplatir(sujet, args.fichiers)
    livrable.mkdir(parents=True, exist_ok=True)
    cachees = part_cachee(sujet, etat, scelle)
    t = P.now_us()
    cle = "gel"
    ecrire_empreintes(sujet, fichiers, scelle)
    declarer_hook(sujet)
    C.write_atomic(scelle / "gel.json", json.dumps({"fichiers": fichiers, "livrable": args.livrable, "t": t}, indent=2) + "\n", mode=0o600)
    pointer_sujet(livrable, sujet)
    etat["gel"] = {"at": t[:19], "t": t, "livrable": args.livrable, "fichiers": fichiers, "regels": 0}
    etat["elements"] = elements_gel(sujet, fichiers, cle) + elements_caches(etat, cachees, cle)
    ligne_etat(etat, cle, {
        "étape": "3", "occurrence": "gel", "entrée": " ; ".join(fichiers), "sortie": f"{C.ETAT_DIR}/{C.EMPREINTES_FILE}",
        "note": "empreintes relevées ; hook de gel déclaré dans .claude/settings.json ; part cachée "
                + ("scellée" if cachees else "absente : l'amont n'en a pas produit")}, t)
    C.sauver_etat(sujet, etat)
    trace_a3.ecrire(sujet)
    print(f"Gel : {len(fichiers)} fichier(s) figé(s), {len(cachees)} champ(s) caché(s) scellé(s), hook déclaré dans .claude/settings.json.")
    return 0


def cmd_empreintes(args):
    sujet = C.dossier_sujet()
    scelle = C.scelle(sujet)
    etat = C.charger_etat(sujet)
    ecart = verifier_empreintes(sujet, etat, scelle)
    if ecart:
        raise HarnaisError(f"écart d'empreinte : {ecart}")
    print(f"Empreintes intactes ({len(etat['gel']['fichiers'])} fichier(s)).")
    return 0


def cmd_regeler(args):
    sujet = C.dossier_sujet()
    scelle = C.scelle(sujet)
    etat = C.charger_etat(sujet)
    if not etat.get("gel"):
        raise HarnaisError("le sujet n'est pas gelé : `geler` d'abord")
    regels = etat["gel"]["regels"]
    derogation = next((s for s in etat["suites"] if s["suite"] == "contourner" and s["apres_gel"] == regels and not s["utilise"]), None)
    if not derogation:
        raise HarnaisError("aucun « contourner » n'est consigné depuis le dernier gel : un critère ne se revoit que par cette suite, "
                           "avec une dérogation tracée (`suite tours_goal|tours_correction contourner \"critère et raison\"`)")
    fichiers = etat["gel"]["fichiers"]
    for f in fichiers:
        if not (Path(sujet) / f).is_file():
            raise HarnaisError(f"{f} : fichier figé disparu, rien à regeler")
    cachees = part_cachee(sujet, etat, scelle)
    t = P.now_us()
    cle = f"regel:{regels + 1}"
    ecrire_empreintes(sujet, fichiers, scelle)
    derogation["utilise"] = True
    etat["gel"]["regels"] = regels + 1
    etat.setdefault("tours_historique", []).append({"regel": regels + 1, **etat["tours"]})
    etat["tours"] = {"goal": 0, "correction": 0}
    etat["extra"] = {"tours_goal": 0, "tours_correction": 0}
    etat["abandonne"] = False
    for e in etat["elements"]:
        if e["état"] == "figé" and e["emplacement"] in fichiers:
            e["empreinte_sha256"], e["cle_ligne"] = C.sha256_file(Path(sujet) / e["emplacement"]), cle
        if e["élément"] == "part cachée" and e["état"] == "scellé":
            nouveau = next((c for n, c in cachees if n == e.get("source")), None)
            if nouveau:
                e["empreinte_sha256"], e["cle_ligne"] = C.sha256_file(nouveau), cle
    ligne_etat(etat, cle, {
        "étape": "3", "occurrence": f"regel {regels + 1}", "entrée": " ; ".join(fichiers), "sortie": f"{C.ETAT_DIR}/{C.EMPREINTES_FILE}",
        "note": "retour en 2B puis nouveau gel, après la dérogation tracée en T7 ; les compteurs de tours repartent de zéro"}, t)
    C.sauver_etat(sujet, etat)
    trace_a3.ecrire(sujet)
    print(f"Regel {regels + 1} : nouvelles empreintes relevées pour {len(fichiers)} fichier(s).")
    return 0


# ---------------------------------------------------------------------------
# tour, tour-correction
# ---------------------------------------------------------------------------
def cmd_tour(args, nom="goal"):
    sujet = C.dossier_sujet()
    scelle = C.scelle(sujet)
    etat = C.charger_etat(sujet)
    cle = "tours_goal" if nom == "goal" else "tours_correction"
    if not etat.get("gel"):
        raise HarnaisError("tour refusé : le sujet n'est pas gelé")
    ecart = verifier_empreintes(sujet, etat, scelle)
    if ecart:
        raise HarnaisError(f"tour refusé, écart d'empreinte : {ecart}")
    goal = trouver_goal(sujet)
    if goal is None:
        raise HarnaisError(f"tour refusé : aucun goal ({GOAL_FILE} à la racine du sujet, ou la sortie de l'étape du goal de l'amont)")
    vides = emplacements_vides(goal)
    if vides:
        raise HarnaisError(f"tour refusé : le goal contient encore des emplacements réservés non remplis : {', '.join(vides)}")
    if etat.get("abandonne"):
        raise HarnaisError("tour refusé : le sujet est abandonné (suite consignée)")
    if etat.get("livre_avec_reserve"):
        raise HarnaisError("tour refusé : la livraison avec réserve est consignée")
    limite = plafond_valeur(etat, f"{cle}_max") + etat["extra"][cle]
    n = etat["tours"][nom]
    if n >= limite:
        atteint = next((a for a in etat["plafonds_atteints"] if a["plafond"] == f"{cle}_max"
                        and not any(s.get("atteint_id") == a["id"] for s in etat["suites"])), None)
        autre = next((s for s in reversed(etat["suites"]) if s["cle"] == cle and s["apres_gel"] == etat["gel"]["regels"]
                      and not s["utilise"]), None)
        if atteint or not autre:
            raise HarnaisError(f"tour refusé : le plafond {cle}_max est atteint ({n} tour(s) sur {limite}) et aucune suite n'est "
                               "consignée : la main revient au pilote, qui seul en choisit une")
        raise HarnaisError(f"tour refusé : le plafond {cle}_max est atteint ({n} tour(s) sur {limite}) et la suite consignée "
                           f"est « {autre['suite']} », qui n'ajoute pas de tour")
    t = P.now_us()
    n += 1
    etat["tours"][nom] = n
    ligne_cle = f"tour:{nom}:{n}"
    etape = "4" if nom == "goal" else "6"
    modele = etat["reglages"]["modeles"].get("production")
    ligne_etat(etat, ligne_cle, {
        "étape": etape, "occurrence": f"tour {n}", "granularité": "session",
        "entrée": f"{GOAL_FILE} ; " + " ; ".join(etat["gel"]["fichiers"]) if (Path(sujet) / GOAL_FILE).is_file()
        else " ; ".join(etat["gel"]["fichiers"]),
        "sortie": livrable_affiche(sujet, etat), "agent": "agent de production, contexte repris", "modèle": C.modele_nom(modele),
        "durée": "n.c.", "jetons": "n.c.", "portée_jetons": "session", "coût": "n.c.", "source_coût": "n.c.",
        "méthode_coût": "la session sous /goal n'expose au harnais ni jetons ni dollars : à relever dans la session",
        "note": "tour compté par le harnais, empreintes vérifiées avant le tour ; jetons non relevés"
                + (f" ; plafond {cle}_max atteint : la main revient au pilote, qui seul choisit la suite" if n >= limite else "")}, t)
    if n >= limite:
        etat["plafonds_atteints"].append({
            "id": f"{cle}:{len(etat['plafonds_atteints']) + 1}", "plafond": f"{cle}_max", "cle_ligne": ligne_cle, "at": t,
            "constat": (f"dernier résultat : {n} tour(s) comptés sur {limite}, plafond atteint ; reste en échec : la condition d'arrêt "
                        "du goal n'est pas établie (dernier lancement du script à lire dans la session) ; livré : "
                        f"{livrable_affiche(sujet, etat)}"),
            "suites_proposees": etat["reglages"]["suites"][cle]})
    C.sauver_etat(sujet, etat)
    trace_a3.ecrire(sujet)
    print(f"Tour {n} sur {limite} ({'production' if nom == 'goal' else 'correction'}).")
    return 0


def cmd_tour_correction(args):
    return cmd_tour(args, "correction")


# ---------------------------------------------------------------------------
# fin-production
# ---------------------------------------------------------------------------
GIT = ["git", "-c", "user.name=ix-harnais", "-c", "user.email=ix-harnais@localhost", "-c", "commit.gpgsign=false",
       "-c", "tag.gpgsign=false", "-c", "core.hooksPath=/dev/null"]


def git(args, cwd, check=True):
    sortie = subprocess.run(GIT + list(args), cwd=cwd, capture_output=True, text=True)
    if check and sortie.returncode != 0:
        raise HarnaisError(f"git {' '.join(args[:2])} a échoué : {(sortie.stderr or sortie.stdout).strip()[-300:]}")
    return sortie


def depot_de(dossier):
    sortie = git(["rev-parse", "--show-toplevel"], dossier, check=False)
    return Path(sortie.stdout.strip()).resolve() if sortie.returncode == 0 and sortie.stdout.strip() else None


def hors_livrable(sujet, livrable):
    """Quand le livrable est le dossier du sujet lui-même : ce que le harnais y écrit n'est pas le livrable."""
    if Path(sujet).resolve() != Path(livrable).resolve():
        return []
    return [f":(exclude){x}" for x in (C.ETAT_DIR, ".claude", "parcours", trace_a3.TRACE_FILE, CONSTAT_FILE, JUGEMENT_DIR)]


def manifeste_livrable(livrable, exclus=()):
    """L'empreinte du contenu du livrable : sha256 de la liste triée « empreinte  chemin »."""
    lignes = []
    livrable = Path(livrable)
    for chemin in sorted(p for p in livrable.rglob("*") if p.is_file() and ".git" not in p.relative_to(livrable).parts):
        relatif = chemin.relative_to(livrable).as_posix()
        if any(relatif == x or relatif.startswith(x + "/") for x in exclus):
            continue
        lignes.append(f"{C.sha256_file(chemin)}  {relatif}")
    return C.sha256_text("\n".join(lignes) + "\n")


def cmd_fin_production(args):
    sujet = C.dossier_sujet()
    C.scelle(sujet)
    etat = C.charger_etat(sujet)
    if not etat.get("gel"):
        raise HarnaisError("fin de production refusée : le sujet n'est pas gelé")
    livrable = dossier_livrable(sujet, etat["gel"]["livrable"])
    if not livrable.is_dir():
        raise HarnaisError(f"le dossier du livrable n'existe pas : {etat['gel']['livrable']}")
    depot = depot_de(livrable)
    if depot is None:
        git(["init", "-q"], livrable)
        depot = livrable
    pointer_sujet(depot, sujet)
    exclus = [Path(x[len(":(exclude)"):]) for x in hors_livrable(sujet, livrable)]
    if depot != livrable or not exclus:
        cible = livrable.relative_to(depot).as_posix() or "."
    else:
        cible = "."
    git(["add", "-A", "--", cible, *hors_livrable(sujet, livrable)], depot)
    n = len(etat.get("livrables") or []) + 1
    message = f"Livrable du sujet {etat['sujet']} : fin de la production {n}"
    git(["commit", "-q", "--allow-empty", "--no-verify", "-m", message], depot)
    commit = git(["rev-parse", "HEAD"], depot).stdout.strip()
    etiquette = f"livrable-{n}"
    while git(["rev-parse", "-q", "--verify", f"refs/tags/{etiquette}"], depot, check=False).returncode == 0:
        n += 1
        etiquette = f"livrable-{n}"
    git(["tag", etiquette, commit], depot)
    t = P.now_us()
    empreinte = manifeste_livrable(livrable, [x.as_posix() for x in exclus] if depot == livrable else [])
    enregistrement = {"etiquette": etiquette, "commit": commit, "depot": str(depot), "dossier": etat["gel"]["livrable"],
                      "empreinte": empreinte, "at": t[:19], "t": t}
    etat.setdefault("livrables", []).append(enregistrement)
    etat["livrable"] = enregistrement
    cle = f"fin:{n}"
    ligne_etat(etat, cle, {"étape": "4", "occurrence": f"gel du livrable {n}", "entrée": livrable_affiche(sujet, etat),
                           "sortie": f"étiquette {etiquette}", "note": f"livrable commité ({commit[:12]}) et étiqueté {etiquette}"}, t)
    etat["elements"] = [e for e in etat["elements"] if not e["élément"].startswith("livrable")] + [{
        "élément": f"livrable (étiquette {etiquette})", "état": "figé", "empreinte_sha256": empreinte,
        "emplacement": livrable_affiche(sujet, etat), "cle_ligne": cle, "ouvert_à": "sans objet"}]
    C.sauver_etat(sujet, etat)
    trace_a3.ecrire(sujet)
    print(f"Livrable commité ({commit[:12]}) et étiqueté {etiquette}.")
    return 0


def livrable_inchange(sujet, etat):
    """None si le livrable est tel qu'à son étiquette, sinon la cause."""
    courant = etat.get("livrable")
    if not courant:
        return "aucune étiquette : `fin-production` d'abord"
    depot, livrable = Path(courant["depot"]), dossier_livrable(sujet, courant["dossier"])
    if not livrable.is_dir():
        return "le dossier du livrable a disparu"
    exclus = [x[len(":(exclude)"):] for x in hors_livrable(sujet, livrable)]
    cible = livrable.relative_to(depot).as_posix() or "."
    differences = git(["diff", "--quiet", courant["etiquette"], "--", cible, *hors_livrable(sujet, livrable)], depot, check=False)
    if differences.returncode != 0:
        return f"le livrable a bougé depuis l'étiquette {courant['etiquette']} (fichiers modifiés)"
    nouveaux = git(["ls-files", "--others", "--exclude-standard", "--", cible, *hors_livrable(sujet, livrable)], depot).stdout.strip()
    if nouveaux:
        return f"le livrable a bougé depuis l'étiquette {courant['etiquette']} (fichiers ajoutés : {nouveaux.splitlines()[0]})"
    if manifeste_livrable(livrable, exclus if depot == livrable else []) != courant["empreinte"]:
        return f"le livrable a bougé depuis l'étiquette {courant['etiquette']}"
    return None


# ---------------------------------------------------------------------------
# juge
# ---------------------------------------------------------------------------
FORMAT_VERDICT = """\
# Verdict du juge

## Lignes

| exigence | part | verdict | preuve |
|---|---|---|---|
| <référence de l'exigence> | visible ou cachée | passe ou échec | <la preuve : sortie brute, extrait, constat> |

## Synthèse

<quelques lignes>
"""


def consigne_du_juge(sujet, etat, cachees):
    figes = "\n".join(f"- {f}" for f in etat["gel"]["fichiers"])
    cachee = "\n".join(f"- {c}" for _, c in cachees) or "- (aucune part cachée)"
    return f"""Tu es le juge de ce sujet. Tu travailles en contexte neuf, distinct du producteur.

Dossier du sujet : {sujet}
Livrable : {dossier_livrable(sujet, etat['gel']['livrable'])} (étiquette {etat['livrable']['etiquette']})
Fichiers figés (script de recette, grille visible, fixtures) :
{figes}
Part cachée de la grille (toi seul la lis) :
{cachee}

Ce que tu fais, dans l'ordre :
1. Relance le script de recette toi-même et montre sa sortie brute : tu ne crois pas le producteur sur parole.
2. Répartis la relecture de la part visible par thème entre des sous-agents ordinaires (outil Agent), chacun avec un modèle explicite
   (jamais fable ; sonnet pour lire, opus pour vérifier, haiku pour la forme). Aucun Workflow.
3. Juge la part cachée seul, sans la montrer à aucun sous-agent.
4. Fais le test du nouveau venu avec un sous-agent neuf (sonnet) qui n'utilise le livrable qu'avec sa documentation.
5. Tu n'écris dans aucun fichier du sujet ni du livrable. Tu rends ton verdict sur la sortie standard, rien d'autre.

Format du verdict (une ligne par exigence, une preuve pour chacune) :

{FORMAT_VERDICT}
Un verdict est « passe » ou « échec ». La part est « visible » ou « cachée ».
"""


def lire_verdict(texte):
    """[(exigence, part, verdict, preuve)] des lignes du tableau du verdict ; vide si le format n'est pas tenu."""
    lignes, entete = [], False
    for brut in texte.splitlines():
        trouve = LIGNE_VERDICT.match(brut.strip())
        if not trouve:
            continue
        cellules = [c.strip() for c in trouve.group(1).split("|")]
        if len(cellules) < 4:
            continue
        if re.fullmatch(r"[-: ]+", cellules[0]):
            continue
        if cellules[0].lower() == "exigence":
            entete = True
            continue
        if not entete:
            continue
        exigence, part, verdict, preuve = cellules[0], cellules[1].lower(), cellules[2].lower(), "|".join(cellules[3:])
        if exigence.startswith("<") and exigence.endswith(">"):
            continue
        lignes.append((exigence, "cachée" if part.startswith("cach") or part.startswith("hid") else "visible",
                       "échec" if re.match(r"(éch|ech|fail|ko|ko\b)", verdict) else "passe", preuve))
    return lignes


def nettoyer_session(dossier):
    """Supprime le dossier de travail du juge et, s'il existe, le dossier de projet que claude a pu créer pour lui."""
    dossier = Path(dossier)
    shutil.rmtree(dossier, ignore_errors=True)
    projets = Path.home() / ".claude" / "projects"
    if projets.is_dir():
        for variante in {re.sub(r"[^A-Za-z0-9]", "-", str(dossier)), re.sub(r"[^A-Za-z0-9]", "-", str(dossier.resolve()))}:
            cible = projets / variante
            if cible.is_dir() and dossier.name in cible.name:
                shutil.rmtree(cible, ignore_errors=True)


def cmd_juge(args):
    sujet = C.dossier_sujet()
    scelle = C.scelle(sujet)
    etat = C.charger_etat(sujet)
    if not etat.get("gel"):
        raise HarnaisError("jugement refusé : le sujet n'est pas gelé")
    ecart = verifier_empreintes(sujet, etat, scelle)
    if ecart:
        raise HarnaisError(f"jugement refusé, écart d'empreinte : {ecart}")
    cause = livrable_inchange(sujet, etat)
    if cause:
        raise HarnaisError(f"jugement refusé : {cause}")
    claude = shutil.which("claude")
    if not claude:
        raise HarnaisError("jugement refusé : la commande `claude` est introuvable dans le PATH")
    n = len(etat["juge"]["appels"]) + 1
    cachees = part_cachee(sujet, etat, scelle)
    modele = etat["reglages"]["modeles"].get("juge")
    if not modele:
        raise HarnaisError("les réglages n'ont pas de modèle pour le rôle 'juge'")
    neutre = C.temp_neutre("juge-")
    debut = P.now_us()
    try:
        sortie = subprocess.run(
            [claude, "-p", "--model", modele, "--output-format", "json", "--no-session-persistence",
             "--allowedTools", "Read,Glob,Grep,Bash,Agent", "--add-dir", str(sujet), "--add-dir", str(scelle)],
            input=consigne_du_juge(sujet, etat, cachees), cwd=neutre, capture_output=True, text=True,
            timeout=int(os.environ.get("IX_JUGE_DELAI", "3600")))
    except (OSError, subprocess.SubprocessError) as exc:
        nettoyer_session(neutre)
        raise HarnaisError(f"jugement refusé : le juge n'a pas pu tourner ({type(exc).__name__})") from None
    nettoyer_session(neutre)
    fin = P.now_us()
    brut = sortie.stdout
    texte, cout = brut, None
    try:
        charge = json.loads(brut)
        if isinstance(charge, dict) and "result" in charge:
            texte, cout = str(charge["result"]), charge.get("total_cost_usd")
    except ValueError:
        pass
    if sortie.returncode != 0:
        raise HarnaisError(f"le juge a échoué (code {sortie.returncode}) : {(sortie.stderr or '').strip()[-200:]}")
    lignes = lire_verdict(texte)
    dossier_juge = scelle / "juge"
    dossier_juge.mkdir(parents=True, exist_ok=True)
    chemin_sortie = dossier_juge / f"sortie-{n}.md"
    C.write_atomic(chemin_sortie, texte if texte.endswith("\n") else texte + "\n", mode=0o600)
    if not lignes:
        raise HarnaisError("le verdict du juge n'est pas au format du harnais (un tableau « exigence | part | verdict | preuve ») : "
                           f"sa sortie est gardée au scellé (appel {n}), le jugement est à refaire")
    echecs = [l for l in lignes if l[2] == "échec"]
    constat = ["# Constat du juge", "",
               f"Appel du juge {n} sur le livrable étiqueté {etat['livrable']['etiquette']}.", "",
               "Pour chaque exigence en échec, la référence de l'exigence ; la preuve d'une exigence visible est donnée, "
               "celle d'une exigence cachée ne l'est jamais.", ""]
    if not echecs:
        constat.append("Aucune exigence en échec.")
    for exigence, part, _v, preuve in echecs:
        if part == "cachée":
            constat.append(f"- {exigence} (part cachée) : en échec. Rien de plus n'est donné.")
        else:
            constat.append(f"- {exigence} (part visible) : en échec. Preuve : {preuve}")
    C.write_atomic(Path(sujet) / CONSTAT_FILE, "\n".join(constat) + "\n")
    C.write_atomic(dossier_juge / f"meta-{n}.json", json.dumps(
        {"n": n, "debut": debut, "fin": fin, "cout_usd": cout, "modele": modele, "lignes": [list(l[:3]) for l in lignes]},
        indent=2, ensure_ascii=False) + "\n", mode=0o600)
    cle = f"juge:{n}"
    if cout is not None:
        cout_t, source, methode = C.cout_texte(float(cout)), "mesuré", "total_cost_usd rendu par claude -p"
    else:
        cout_t, source, methode = "n.c.", "n.c.", "le juge n'a pas rendu de coût (sortie sans total_cost_usd)"
    ligne_etat(etat, cle, {
        "étape": "5", "occurrence": f"appel du juge {n}", "granularité": "étape",
        "entrée": f"{livrable_affiche(sujet, etat)} ; " + " ; ".join(etat["gel"]["fichiers"]), "sortie": "scellé, voir T9",
        "agent": "agent de jugement, contexte neuf (dossier de travail neutre, nettoyé)", "modèle": C.modele_nom(modele),
        "durée": C.duree_entre(debut, fin), "jetons": "n.c.", "portée_jetons": "appel", "coût": cout_t, "source_coût": source,
        "méthode_coût": methode, "note": "jetons non relevés ; sous-agents du juge non consignés ; le constat pour le producteur "
                                          f"est {CONSTAT_FILE}"}, debut)
    etat["juge"]["appels"].append({"n": n, "t": debut, "echecs": len(echecs), "echecs_caches": sum(1 for l in echecs if l[1] == "cachée"),
                                   "sortie_sha256": C.sha256_file(chemin_sortie)})
    etat["elements"] = [e for e in etat["elements"] if not (e["élément"] == "trace du juge" and e.get("appel") == n)] + [{
        "élément": "trace du juge", "état": "scellé", "empreinte_sha256": C.sha256_file(chemin_sortie), "emplacement": "non écrit",
        "cle_ligne": cle, "ouvert_à": "à venir", "appel": n}]
    C.sauver_etat(sujet, etat)
    trace_a3.ecrire(sujet)
    print(f"Jugement {n} : {len(lignes)} exigence(s), {len(echecs)} en échec dont {sum(1 for l in echecs if l[1] == 'cachée')} cachée(s). "
          f"Constat pour le producteur : {CONSTAT_FILE}.")
    return 0


# ---------------------------------------------------------------------------
# ouvrir, sceau
# ---------------------------------------------------------------------------
def cmd_ouvrir(args):
    sujet = C.dossier_sujet()
    scelle = C.scelle(sujet)
    etat = C.charger_etat(sujet)
    appels = etat["juge"]["appels"]
    if not appels:
        raise HarnaisError("ouverture refusée : aucun jugement n'a eu lieu")
    if etat.get("ouvert"):
        raise HarnaisError("le jugement est déjà ouvert")
    dernier = appels[-1]
    limite = plafond_valeur(etat, "tours_correction_max") + etat["extra"]["tours_correction"]
    fait = etat["tours"]["correction"]
    plafond_atteint = any(a["plafond"] == "tours_correction_max" for a in etat["plafonds_atteints"])
    termine = dernier["echecs"] == 0 or plafond_atteint or etat.get("abandonne") or etat.get("livre_avec_reserve")
    if not termine:
        raise HarnaisError(f"ouverture refusée : les tours de correction ne sont pas terminés ({fait} sur {limite}) et le dernier "
                           f"jugement a {dernier['echecs']} exigence(s) en échec")
    cachees = part_cachee(sujet, etat, scelle)
    dossier = Path(sujet) / JUGEMENT_DIR
    dossier.mkdir(exist_ok=True)
    t = P.now_us()
    verses = {}
    for nom, chemin in cachees:   # chaque champ caché est versé tel quel : octet pour octet, son empreinte reste celle du scellé
        cible = f"{JUGEMENT_DIR}/part-cachee.md" if len(cachees) == 1 else f"{JUGEMENT_DIR}/part-cachee-{nom}.md"
        shutil.copyfile(chemin, Path(sujet) / cible)
        verses[f"part cachée:{nom}"] = cible
    for appel in appels:
        source = scelle / "juge" / f"sortie-{appel['n']}.md"
        if source.is_file():
            C.write_atomic(dossier / f"trace-du-juge-{appel['n']}.md", source.read_text(encoding="utf-8"))
            verses[f"trace du juge:{appel['n']}"] = f"{JUGEMENT_DIR}/trace-du-juge-{appel['n']}.md"
    for e in etat["elements"]:
        if e["état"] != "scellé":
            continue
        cle = f"part cachée:{e.get('source')}" if e["élément"] == "part cachée" else f"trace du juge:{e.get('appel')}"
        if cle in verses:
            e["état"], e["emplacement"], e["ouvert_à"] = "ouvert", verses[cle], t[:19]
    etat["ouvert"] = {"at": t[:19], "fichiers": sorted(verses.values())}
    C.sauver_etat(sujet, etat)
    trace_a3.ecrire(sujet)
    print(f"Jugement ouvert : {', '.join(sorted(verses.values())) or 'rien à verser'}.")
    return 0


def cmd_sceau(args):
    sujet = C.dossier_sujet()
    print(C.scelle(sujet))
    return 0


def cmd_hook(args):
    import hook
    return hook.main()


# ---------------------------------------------------------------------------
# Ligne de commande
# ---------------------------------------------------------------------------
def construire_parseur():
    parser = argparse.ArgumentParser(prog="harnais.py", description="Outils du pilote autour d'un sujet (voir docs/harnais/)")
    sub = parser.add_subparsers(dest="commande", required=True)
    p = sub.add_parser("lancer", help="ouvrir un sujet")
    p.add_argument("type", help="le type de sujet (une clé de types_de_sujet des réglages)")
    p.add_argument("options", nargs=argparse.REMAINDER, help="options de parcours.py new")
    p.set_defaults(func=cmd_lancer)
    p = sub.add_parser("trace", help="écrire la trace A3")
    p.set_defaults(func=cmd_trace)
    p = sub.add_parser("suite", help="consigner la suite choisie à un plafond atteint")
    p.add_argument("cle", help="le plafond atteint : passes_verification_max | tours_correction_max | tours_goal_max")
    p.add_argument("suite", help="relancer | contourner | livrer_avec_reserve | abandonner")
    p.add_argument("valeur", nargs="?", help="un nombre (relancer) ou un texte (contourner, livrer_avec_reserve)")
    p.set_defaults(func=cmd_suite)
    p = sub.add_parser("contre-verif", help="rendre la sortie de la contre-vérification")
    p.add_argument("fichier")
    p.set_defaults(func=cmd_contre_verif)
    p = sub.add_parser("geler", help="figer les fichiers de jugement du sujet")
    p.add_argument("livrable", help="le dossier du livrable, relatif au sujet")
    p.add_argument("fichiers", nargs="*", help="les fichiers figés, relatifs au sujet")
    p.set_defaults(func=cmd_geler)
    for nom, fonction, aide in (("sceau", cmd_sceau, "le chemin du scellé du sujet (outil du pilote)"),
                                ("empreintes", cmd_empreintes, "vérifier les empreintes des fichiers figés"),
                                ("tour", cmd_tour, "avant un tour de production"),
                                ("tour-correction", cmd_tour_correction, "avant un tour de correction"),
                                ("regeler", cmd_regeler, "regel après un retour en 2B"),
                                ("fin-production", cmd_fin_production, "commiter le livrable et poser l'étiquette"),
                                ("juge", cmd_juge, "lancer le juge du sujet"),
                                ("ouvrir", cmd_ouvrir, "fin du jugement"),
                                ("hook", cmd_hook, "événement PreToolUse")):
        sub.add_parser(nom, help=aide).set_defaults(func=fonction)
    return parser


def main(argv=None):
    args = construire_parseur().parse_args(argv)
    try:
        return args.func(args)
    except HarnaisError as exc:
        print(f"Refusé : {exc}", file=sys.stderr)
        return 1
    except P.ParcoursError as exc:
        print(f"Refusé : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
