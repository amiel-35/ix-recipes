"""La trace d'un sujet au format A3 : son écriture, son contrôle, et la traduction de la trace de l'amont.

L'amont, joué par l'exécuteur, écrit son état (`parcours/amont/state.json`) : une exécution par passage d'une étape, avec
son modèle, sa durée, son coût quand l'outil le rend. Ce module en tire les tables T1 à T11 de `docs/harnais/A3-format-trace.md` ;
les gestes du harnais (gel, tours, suites, jugement, ouverture) viennent de `.harnais/etat.json`. La trace se reconstruit
entièrement de ces deux états : l'écrire deux fois donne le même fichier.
"""

import re
from pathlib import Path

from commun import (P, HarnaisError, PARCOURS_SLUG, cellule, cout_texte, charger_etat, dossier_amont, duree_entre,
                    etat_amont, modele_nom, relatif, write_atomic)

TRACE_FILE = "trace.md"      # le fichier de trace d'un sujet, à la racine de son dossier (réponse de L5 à Q8)

T1 = ["sujet", "titre", "type_de_sujet", "pilote", "début", "version_réglages", "empreinte_réglages", "sujet_parent"]
T2 = ["plafond", "valeur_appliquée", "atteint"]
T3 = ["ligne", "étape", "occurrence", "granularité", "entrée", "sortie", "agent", "modèle", "réglages", "durée", "jetons",
      "portée_jetons", "coût", "source_coût", "méthode_coût", "inclus_dans", "cumule_de", "note"]
T4 = ["ligne", "skill", "version", "empreinte_sha256", "fichier", "note"]
T5 = ["ligne", "rôle", "modèle", "objet", "résultat"]
T6 = ["pause", "question", "décision", "source", "décideur", "date", "à rappeler"]
T7 = ["ligne", "plafond", "constat", "suites_proposées", "suite_choisie", "tours_ajoutés", "dérogation", "réserve",
      "décideur", "date"]
T8 = ["enfant", "dossier", "ligne", "motif"]
T9 = ["élément", "état", "empreinte_sha256", "emplacement", "ligne", "ouvert_à"]
T10 = ["ligne", "tour", "commande", "code_sortie", "vérifications", "échecs", "durée_relevée", "jetons_relevés"]
T11 = ["ligne", "nature", "description", "raison", "confirmé_par"]

TITRES = {
    "T1": "Sujet", "T2": "Plafonds appliqués", "T3": "Étapes", "T4": "Skills", "T5": "Sous-agents",
    "T6": "Pauses et décisions", "T7": "Plafonds atteints et suites", "T8": "Sujets enfants",
    "T9": "Gel et scellés", "T10": "Lancements du script de recette", "T11": "Points à confirmer et écarts",
}
COLONNES = {"T1": T1, "T2": T2, "T3": T3, "T4": T4, "T5": T5, "T6": T6, "T7": T7, "T8": T8, "T9": T9, "T10": T10, "T11": T11}
VIDES = {"T5": "aucun sous-agent consigné", "T7": "aucun plafond atteint", "T8": "aucun sujet enfant",
         "T10": "aucun lancement du script de recette consigné", "T11": "aucun point à confirmer"}   # T9 vide : l'en-tête seul
ABSENT = ("n.c.", "inclus dans la session", "sans objet")


def ligne_humaine(**kw):
    base = {"granularité": "appel", "agent": "humain", "modèle": "humain", "durée": "sans objet", "jetons": "sans objet",
            "portée_jetons": "sans objet", "coût": "sans objet", "source_coût": "sans objet",
            "méthode_coût": "personne : aucun appel d'outil", "inclus_dans": "sans objet", "cumule_de": "sans objet",
            "note": "sans objet"}
    base.update(kw)
    return base


def sortie_amont(amont, step_id):
    for i, step in enumerate(amont["steps"]):
        if step["id"] == step_id:
            return f"parcours/{PARCOURS_SLUG}/{P.output_name(i, step_id)}"
    return None


def entrees(defn, amont):
    chemins = []
    for src in defn["receives"]:
        if src == "brief":
            chemin = "demande.md"
        elif src == "context_sheet":
            chemin = f"parcours/{PARCOURS_SLUG}/00-context.md"
        elif src == "answers":
            chemin = f"parcours/{PARCOURS_SLUG}/answers.md"
        elif src == "corpus":
            chemin = f"parcours/{PARCOURS_SLUG}/corpus/"
        elif "." in src:
            chemin = sortie_amont(amont, src.partition(".")[0])
        else:
            continue
        if chemin and chemin not in chemins:
            chemins.append(chemin)
    return " ; ".join(chemins) or "sans objet"


def agent_et_modele(run, defn):
    moteur, modele = run.get("engine") or "n.c.", run.get("model") or defn.get("model")
    if moteur == "externe":
        return ("appel du pilote hors de l'exécuteur, contexte neuf",
                modele_nom(modele) if modele else "n.c. (modèle du rôle contre_verification, non saisi)")
    if moteur in P.FREE_ENGINES:
        return (f"moteur simulé ({moteur}), aucun appel, contexte neuf", f"{modele_nom(modele)} (simulé : aucun appel)")
    return (f"agent {moteur}, contexte neuf", modele_nom(modele))


def cout_de(run):
    """(coût, source_coût, méthode_coût) : mesuré là où l'outil le rend, jamais présenté comme mesuré sinon."""
    moteur = run.get("engine")
    if moteur == "claude":
        return cout_texte(run["cost_usd"]), "mesuré", "total_cost_usd rendu par claude -p, relances comprises"
    if moteur == "externe":
        if run.get("cost_known"):
            return cout_texte(run["cost_usd"]), "mesuré", "coût de l'appel du pilote, saisi d'après la sortie de l'outil qui l'a rendu"
        return "n.c.", "n.c.", "appel du pilote hors de l'exécuteur : le coût n'a pas été saisi"
    if moteur in P.FREE_ENGINES:
        return "n.c.", "n.c.", "moteur simulé : aucun appel de modèle, donc aucun coût"
    return "n.c.", "n.c.", f"moteur {moteur} : abonnement, les appels sont comptés mais aucun montant n'est rendu"


def versions_skill(skill):
    version = skill.get("version")
    return "n.c." if not version or version == "unknown" else version


def lignes_amont(sujet, etat, amont, recette):
    """(lignes T3, lignes T4, lignes T6, rangées de T7) tirées de l'état de l'amont."""
    t3, t4, t6, t7 = [], [], [], []
    version = etat["reglages"]["version"]
    pauses_numero = 0
    for idx, step in enumerate(amont["steps"]):
        defn = recette["steps"][idx]
        etape = defn.get("stage") or defn["id"]
        runs = step.get("runs") or []
        verifie = bool(defn.get("verdict_field"))
        for n, run in enumerate(runs, 1):
            occurrence = f"passe {n}" if verifie else ("unique" if len(runs) == 1 else f"rédaction {n}")
            agent, modele = agent_et_modele(run, defn)
            cout, source, methode = cout_de(run)
            sortie = f"parcours/{PARCOURS_SLUG}/{run['output']}" if run.get("output") else "sans objet"
            if run.get("hidden"):
                sortie += " ; part cachée : scellé, voir T9"
            note = [f"jetons non relevés par l'exécuteur"]
            if verifie:
                verdicts = (amont.get("loops") or {}).get(defn["id"], {}).get("history") or []
                if n <= len(verdicts):
                    note.append(f"verdict {verdicts[n - 1]['verdict']}")
            if defn["id"] == "contre_verif" or defn.get("external"):
                note.append("passe comptée dans le plafond des passes de vérification")
            t3.append({"t": run["t"], "cle": f"run:{defn['id']}:{n}", "row": {
                "étape": etape, "occurrence": occurrence, "granularité": "appel", "entrée": entrees(defn, amont),
                "sortie": sortie, "agent": agent, "modèle": modele, "réglages": version,
                "durée": duree_entre(run.get("started"), run.get("ended")) if run.get("started") else "n.c.",
                "jetons": "n.c.", "portée_jetons": "appel", "coût": cout, "source_coût": source, "méthode_coût": methode,
                "inclus_dans": "sans objet", "cumule_de": "sans objet", "note": " ; ".join(note)}})
            skill = run.get("skill") or step.get("skill") or {}
            t4.append({"t": run["t"], "cle": f"run:{defn['id']}:{n}", "row": {
                "skill": skill.get("ref", defn["skill"]), "version": versions_skill(skill),
                "empreinte_sha256": skill.get("sha256", "n.c."), "fichier": "n.c.",
                "note": "texte lu hors du dossier du sujet : son chemin n'est pas consigné"}})
    for pause in amont.get("pauses") or []:
        idx = next(i for i, s in enumerate(amont["steps"]) if s["id"] == pause["step"])
        defn = recette["steps"][idx]
        if defn["produces_context_sheet"]:
            continue
        pauses_numero += 1
        nom = f"pause {pauses_numero}"
        sortie = f"parcours/{PARCOURS_SLUG}/answers.md" if pause["type"] == "answers" else sortie_amont(amont, pause["step"])
        t3.append({"t": pause["t"], "cle": f"pause:{pauses_numero}", "row": ligne_humaine(**{
            "étape": nom, "occurrence": "unique", "entrée": sortie_amont(amont, pause["step"]) or "sans objet",
            "sortie": sortie or "sans objet", "réglages": version,
            "note": f"pause après l'étape {pause['step']}"})})
        sans_reponse = False
        if pause["type"] == "answers":
            reponses = dossier_amont(sujet) / "answers.md"
            sans_reponse = reponses.is_file() and reponses.read_text(encoding="utf-8").strip() == P.NO_ANSWERS
        t6.append({"t": pause["t"], "row": {
            "pause": str(pauses_numero),
            "question": (f"P{pauses_numero} : réponses aux questions bloquantes du cadrage" if pause["type"] == "answers"
                         else f"P{pauses_numero} : validation de l'étape {pause['step']}"),
            "décision": ("aucune réponse : les défauts sont gardés, les points restent des hypothèses" if sans_reponse
                         else "réponses consignées dans parcours/amont/answers.md" if pause["type"] == "answers"
                         else "validée"),
            "source": "défaut accepté" if sans_reponse else "réponse", "décideur": etat["pilote"],
            "date": pause["at"][:10], "à rappeler": "oui" if sans_reponse else "non"}})
    for plafond in amont.get("ceilings") or []:
        choix = plafond.get("choice") or {}
        t7.append({"t": plafond["t"], "cle": f"run:{plafond['step']}:{len((amont['loops'] or {}).get(plafond['step'], {}).get('history', []))}",
                   "plafond": plafond["ceiling"], "constat": plafond["constat"],
                   "suites": plafond["suites_proposees"], "suite": choix.get("suite", "à venir"),
                   "tours": choix.get("passes_ajoutees"), "derogation": None, "reserve": choix.get("reserve"),
                   "par": choix.get("by", "à venir"), "date": (choix.get("at") or plafond["at"])[:10]})
    return t3, t4, t6, t7


def lignes_harnais(sujet, etat):
    """Les lignes de T3 des gestes du harnais, dans l'ordre où l'état les a consignées."""
    t3 = []
    version = etat["reglages"]["version"]
    for evt in etat.get("lignes") or []:
        row = ligne_humaine(**{"réglages": version, **evt["row"]})
        t3.append({"t": evt["t"], "cle": evt["cle"], "row": row})
    return t3


def table(nom, lignes, phrase=None, apres=None):
    """Une table de A3 : son titre, son en-tête, ses lignes ; une table vide est remplacée par sa phrase (`phrase` pour la
    changer), sauf T9 qui garde son en-tête. `apres` : une phrase sous la table."""
    colonnes = COLONNES[nom]
    sortie = [f"### {nom}. {TITRES[nom]}", ""]
    if not lignes and (nom in VIDES or phrase):
        sortie += [phrase or VIDES[nom], ""]
        return sortie
    sortie.append("| " + " | ".join(colonnes) + " |")
    sortie.append("|" + "|".join("---" for _ in colonnes) + "|")
    for ligne in lignes:
        sortie.append("| " + " | ".join(cellule(ligne.get(c)) for c in colonnes) + " |")
    sortie.append("")
    if apres:
        sortie += [apres, ""]
    return sortie


def construire(sujet):
    """Le texte de la trace du sujet, d'après l'état de l'amont et celui du harnais."""
    sujet = Path(sujet)
    etat = charger_etat(sujet)
    amont = etat_amont(sujet)
    recette = None
    t3, t4, t6, t7 = [], [], [], []
    if amont:
        try:
            recette = P.load_recipe(amont["recipe"])
        except P.ParcoursError as exc:
            raise HarnaisError(f"la recette de l'amont ne se lit plus : {exc}") from None
        t3, t4, t6, t7 = lignes_amont(sujet, etat, amont, recette)
    t3 += lignes_harnais(sujet, etat)
    t3.sort(key=lambda r: r["t"])
    zero = {"t": etat["debut_us"], "cle": "etape0", "row": ligne_humaine(**{
        "étape": "0", "occurrence": "unique", "entrée": "demande.md", "sortie": "demande.md",
        "réglages": etat["reglages"]["version"], "note": "la demande est séparée des pièces ; le sujet n'a pas de pièces"
        if not (sujet / "pieces").exists() else "la demande est séparée des pièces (pieces/)"})}
    t3.insert(0, zero)
    ids = {}
    lignes3 = []
    for i, item in enumerate(t3, 1):
        ident = f"L{i:02d}"
        ids[item["cle"]] = ident
        lignes3.append({"ligne": ident, **item["row"]})
    lignes4 = [{"ligne": ids.get(i["cle"], "n.c."), **i["row"]} for i in sorted(t4, key=lambda r: r["t"])]
    lignes6 = [r["row"] for r in sorted(t6, key=lambda r: r["t"])]
    # T7 : une ligne par plafond atteint dont le pilote a choisi la suite (A3 : suite_choisie est une des quatre suites) ;
    # un plafond atteint sans suite choisie figure en T2 (`oui`) et sous la table, jamais comme une suite inventée.
    lignes7, sans_suite, atteints = [], [], set()
    for item in sorted(t7, key=lambda r: r["t"]):
        atteints.add(item["plafond"])
        if item["suite"] == "à venir":
            sans_suite.append((item["plafond"], ids.get(item["cle"], "n.c.")))
            continue
        lignes7.append({"ligne": ids.get(item["cle"], "n.c."), "plafond": item["plafond"], "constat": item["constat"],
                        "suites_proposées": ", ".join(item["suites"]), "suite_choisie": item["suite"],
                        "tours_ajoutés": item["tours"] if item["tours"] else "sans objet", "dérogation": item["derogation"] or "sans objet",
                        "réserve": item["reserve"] or "sans objet", "décideur": item["par"], "date": item["date"]})
    for atteint in etat.get("plafonds_atteints") or []:
        atteints.add(atteint["plafond"])
        suite = next((s for s in etat.get("suites") or [] if s.get("atteint_id") == atteint["id"]), None)
        if not suite:
            sans_suite.append((atteint["plafond"], ids.get(atteint["cle_ligne"], "n.c.")))
            continue
        lignes7.append({
            "ligne": ids.get(atteint["cle_ligne"], "n.c."), "plafond": atteint["plafond"], "constat": atteint["constat"],
            "suites_proposées": ", ".join(atteint["suites_proposees"]), "suite_choisie": suite["suite"],
            "tours_ajoutés": suite.get("n") if suite.get("n") else "sans objet",
            "dérogation": suite["texte"] if suite["suite"] == "contourner" else "sans objet",
            "réserve": suite["texte"] if suite["suite"] == "livrer_avec_reserve" else "sans objet",
            "décideur": suite["par"], "date": suite["at"][:10]})
    lignes2 = []
    for cle, valeur in etat["reglages"]["plafonds"].items():
        lignes2.append({"plafond": cle, "valeur_appliquée": valeur, "atteint": "oui" if cle in atteints else "non"})
    for cle, valeur in (etat["reglages"].get("production") or {}).items():
        lignes2.append({"plafond": f"production.{cle}", "valeur_appliquée": valeur, "atteint": "non"})
    en_attente = ", ".join(f"{p} ({ligne})" for p, ligne in sans_suite)
    phrase7 = ("aucun plafond atteint n'a encore reçu de suite : la main est au pilote, qui seul en choisit une (plafonds atteints : "
               f"{en_attente})" if sans_suite and not lignes7 else None)
    apres7 = (f"Plafonds atteints dont le pilote n'a pas encore choisi la suite : {en_attente}." if sans_suite and lignes7 else None)
    lignes1 = [{"sujet": etat["sujet"], "titre": etat["titre"], "type_de_sujet": etat["type"], "pilote": etat["pilote"],
                "début": etat["debut"], "version_réglages": etat["reglages"]["version"],
                "empreinte_réglages": etat["reglages"]["sha256"], "sujet_parent": "sans objet"}]
    lignes9 = []
    for element in etat.get("elements") or []:
        lignes9.append({**element, "ligne": ids.get(element["cle_ligne"], "n.c.") if element.get("cle_ligne") else element.get("ligne", "n.c.")})
    lignes10 = []
    lignes11 = [{**p, "ligne": ids.get(p.get("cle_ligne"), "L01")} for p in etat.get("points") or []]
    texte = [f"# Trace du sujet {etat['sujet']}", "",
             "Trace au format A3 (`docs/harnais/A3-format-trace.md`), reconstruite par le harnais à partir de l'état de l'amont "
             "et de celui du harnais : l'écrire deux fois donne le même fichier.", ""]
    for nom, lignes in (("T1", lignes1), ("T2", lignes2), ("T3", lignes3), ("T4", lignes4), ("T5", []), ("T6", lignes6),
                        ("T7", lignes7), ("T8", []), ("T9", lignes9), ("T10", lignes10), ("T11", lignes11)):
        texte += table(nom, lignes, phrase7 if nom == "T7" else None, apres7 if nom == "T7" else None)
    return "\n".join(texte).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Lecture et contrôle
# ---------------------------------------------------------------------------
def lire_tables(texte):
    """{T1: [ {colonne: cellule} ], ...} : les titres de niveau 3 « Tn. », puis la ligne d'en-tête, puis les lignes (A3 §6).
    Une table absente (remplacée par sa phrase) vaut une liste vide."""
    tables, courant, colonnes = {}, None, None
    for ligne in texte.splitlines():
        titre = re.match(r"###\s+(T\d+)\.", ligne)
        if titre:
            courant, colonnes = titre.group(1), None
            tables[courant] = []
            continue
        if courant and ligne.startswith("|"):
            cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
            if colonnes is None:
                colonnes = cellules
            elif not all(re.fullmatch(r"-+", c) for c in cellules):
                tables[courant].append(dict(zip(colonnes, cellules)))
    return tables


def controler(texte):
    """Les écarts de la trace à A3 que le code sait contrôler : colonnes exactes, aucune cellule vide, ligne unique,
    première ligne = étape 0, (étape, occurrence) unique, coût mesuré ou estimé avec sa méthode, `n.c.` expliqué."""
    problemes = []
    tables = lire_tables(texte)
    for nom, colonnes in COLONNES.items():
        if nom not in tables:
            problemes.append(f"{nom} absente")
            continue
        entetes = [l for l in texte.splitlines() if l.startswith("|")]
        for ligne in tables[nom]:
            if list(ligne) != colonnes:
                problemes.append(f"{nom} : colonnes {list(ligne)} au lieu de {colonnes}")
                break
            for colonne, valeur in ligne.items():
                if not valeur.strip():
                    problemes.append(f"{nom} : cellule vide dans la colonne {colonne}")
    t3 = tables.get("T3") or []
    if not t3 or t3[0].get("étape") != "0":
        problemes.append("T3 : la première ligne n'est pas l'étape 0")
    ids = [l.get("ligne") for l in t3]
    if len(set(ids)) != len(ids):
        problemes.append("T3 : identifiant de ligne en double")
    couples = [(l.get("étape"), l.get("occurrence")) for l in t3]
    if len(set(couples)) != len(couples):
        problemes.append("T3 : un couple (étape, occurrence) désigne plus d'une ligne")
    for ligne in t3:
        source, methode = ligne.get("source_coût"), ligne.get("méthode_coût", "")
        if source == "mesuré" and not re.fullmatch(r"\d+,\d{2} \$", ligne.get("coût", "")):
            problemes.append(f"{ligne.get('ligne')} : coût mesuré qui n'est pas un montant en dollars")
        if source == "estimé" and not methode.strip():
            problemes.append(f"{ligne.get('ligne')} : coût estimé sans méthode")
        if source in ("mesuré", "estimé") and ligne.get("coût") in ABSENT:
            problemes.append(f"{ligne.get('ligne')} : coût {source} sans montant")
        if source == "n.c." and ligne.get("coût") != "n.c.":
            problemes.append(f"{ligne.get('ligne')} : coût présenté alors que sa source est n.c.")
        if ligne.get("jetons") == "n.c." and not ligne.get("note", "").strip():
            problemes.append(f"{ligne.get('ligne')} : jetons n.c. sans raison dans la note")
    for ligne in tables.get("T9") or []:
        if ligne.get("état") == "scellé" and ligne.get("emplacement") != "non écrit":
            problemes.append(f"T9 : l'élément scellé '{ligne.get('élément')}' a un emplacement écrit")
    return problemes


def ecrire(sujet):
    """Écrit (ou met à jour) la trace du sujet ; refuse, sans l'écrire, si elle ne tient pas A3."""
    texte = construire(sujet)
    problemes = controler(texte)
    if problemes:
        raise HarnaisError("trace refusée, elle ne tient pas A3 : " + " ; ".join(problemes))
    write_atomic(Path(sujet) / TRACE_FILE, texte)
    return Path(sujet) / TRACE_FILE
