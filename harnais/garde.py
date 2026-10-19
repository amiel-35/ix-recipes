"""La garde : le compteur de tours et le plafond, tenus au scellé et appliqués par les hooks de Claude Code.

Ce qui compte les tours et bloque au plafond n'est plus un outil que la session de production lance, c'est un hook
`Stop` (à chaque fin de tour, que la boucle `/goal` relance ou non) ; un hook `UserPromptSubmit` et un hook
`PreToolUse` refusent la suite quand le plafond est atteint. Les trois lisent la garde, `garde.json` au scellé du sujet :
le compteur, les plafonds, ce que le pilote y a ajouté (`suite`), la phase (production ou correction), les fichiers figés.
Les outils du pilote la changent, jamais l'état du sujet (`.harnais/etat.json`), que la production peut écrire :
l'état n'est plus qu'un affichage, recopié de la garde (`harnais.synchroniser`).

Deux témoins se contrôlent : la garde (au scellé, que le hook refuse à la production) et `.harnais/temoin.json` (dans le sujet,
lisible). Chaque écriture de la garde récrit le témoin avec le même numéro de séquence et la même tête (sha256 du contenu).
Un compteur remis à zéro dans la garde seule, ou un témoin récrit seul, se voit au tour suivant : le hook refuse alors tout
outil et arrête la boucle. Remettre à zéro les deux d'un même geste demande de trouver la garde et de l'écrire par une forme
d'appel que le hook ne reconnaît pas : c'est le résidu écrit dans docs/harnais/architecture-harnais.md §8.
"""

import fcntl
import json
import os
import re
from contextlib import contextmanager
from pathlib import Path

import commun as C
from commun import HarnaisError

GARDE_FILE = "garde.json"        # au scellé : le compteur, les plafonds, la phase, les fichiers figés, la référence du jeton
TEMOIN_FILE = "temoin.json"      # dans .harnais/ du sujet : la séquence et la tête de la garde, pour voir une remise à zéro
VERROU_FILE = ".verrou"          # au scellé : un seul écrivain à la fois (les hooks de fin de tour et les outils du pilote)
PHASES_COMPTEES = {"goal": "goal", "correction": "correction"}   # phase -> compteur ; les autres phases ne comptent pas
COMPTEURS = ("goal", "correction")


def chemin(scelle):
    return Path(scelle) / GARDE_FILE


def chemin_temoin(sujet):
    return Path(sujet) / C.ETAT_DIR / TEMOIN_FILE


def neuve(sujet, jeton_sha256, plafonds):
    """La garde d'un sujet qu'on lance : avant le gel, rien n'est compté."""
    return {"version": 1, "sujet": Path(sujet).name, "pilote_sha256": jeton_sha256, "phase": "avant-gel",
            "plafonds": {k: int(plafonds[f"tours_{k}_max"]) for k in COMPTEURS},
            "extra": {k: 0 for k in COMPTEURS}, "tours": {k: 0 for k in COMPTEURS},
            "abandonne": False, "livre_avec_reserve": False, "gel": None, "journal": [], "seq": 0}


def tete_de(garde):
    corps = {k: v for k, v in garde.items() if k != "tete"}
    return C.sha256_text(json.dumps(corps, sort_keys=True, ensure_ascii=False))


def limite(garde, nom):
    return garde["plafonds"][nom] + garde["extra"][nom]


def sauver(scelle, sujet, garde):
    """Écrit la garde (séquence suivante, tête recalculée) puis le témoin du sujet, dans cet ordre."""
    garde["seq"] = int(garde.get("seq", 0)) + 1
    garde["tete"] = tete_de(garde)
    C.write_atomic(chemin(scelle), json.dumps(garde, indent=2, ensure_ascii=False, sort_keys=True) + "\n", mode=0o600)
    C.write_atomic(chemin_temoin(sujet), json.dumps({"seq": garde["seq"], "tete": garde["tete"], "tours": garde["tours"]},
                                                    indent=2, sort_keys=True) + "\n")


def lire_brut(scelle):
    try:
        garde = json.loads(chemin(scelle).read_text(encoding="utf-8"))
    except OSError:
        raise HarnaisError("la garde (compteur de tours) a disparu du scellé") from None
    except ValueError:
        raise HarnaisError("la garde (compteur de tours) est illisible au scellé") from None
    if not isinstance(garde, dict) or "tours" not in garde or "plafonds" not in garde:
        raise HarnaisError("la garde (compteur de tours) n'a pas la forme attendue")
    return garde


def controle(sujet, garde):
    """None si la garde est intacte et concorde avec le témoin du sujet, sinon la cause (un compteur remis à zéro, une garde ou un
    témoin récrit seul, un témoin disparu)."""
    if garde.get("tete") != tete_de(garde):
        return "la garde a été modifiée hors des commandes du harnais (sa tête ne correspond plus à son contenu)"
    try:
        temoin = json.loads(chemin_temoin(sujet).read_text(encoding="utf-8"))
    except OSError:
        return f"le témoin {C.ETAT_DIR}/{TEMOIN_FILE} a disparu"
    except ValueError:
        return f"le témoin {C.ETAT_DIR}/{TEMOIN_FILE} est illisible"
    if temoin.get("seq") != garde.get("seq") or temoin.get("tete") != garde.get("tete"):
        return (f"le témoin {C.ETAT_DIR}/{TEMOIN_FILE} (séquence {temoin.get('seq')}, tours {temoin.get('tours')}) ne correspond pas à la garde "
                f"(séquence {garde.get('seq')}, tours {garde.get('tours')}) : un compteur a été remis en arrière ou l'un des deux récrit")
    return None


def charger(scelle, sujet, verifier=True):
    garde = lire_brut(scelle)
    if verifier:
        cause = controle(sujet, garde)
        if cause:
            raise HarnaisError(f"écart de compteur : {cause}")
    return garde


@contextmanager
def verrou(scelle):
    """Un seul écrivain à la fois : le hook de fin de tour et les commandes du pilote ne se marchent pas dessus."""
    chemin_verrou = Path(scelle) / VERROU_FILE
    handle = open(chemin_verrou, "a+")
    try:
        fcntl.flock(handle, fcntl.LOCK_EX)
        yield
    finally:
        try:
            fcntl.flock(handle, fcntl.LOCK_UN)
        finally:
            handle.close()


def modifier(scelle, sujet, fonction, verifier=True):
    """Charge la garde sous verrou, appelle `fonction(garde)` (qui peut lever un refus : rien n'est alors écrit), l'écrit, rend le
    résultat de la fonction."""
    with verrou(scelle):
        garde = charger(scelle, sujet, verifier=verifier)
        resultat = fonction(garde)
        sauver(scelle, sujet, garde)
        return resultat


def compte_actif(garde):
    """Le nom du compteur que la phase fait avancer (`goal`, `correction`), ou None."""
    return PHASES_COMPTEES.get(garde.get("phase"))


def compter(garde, nom, t):
    """Compte un tour dans le compteur `nom` ; rend l'événement du journal. Ne vérifie rien : voir `refus_plafond`."""
    garde["tours"][nom] += 1
    n = garde["tours"][nom]
    evenement = {"seq": len(garde["journal"]) + 1, "nom": nom, "n": n, "t": t,
                 "limite": limite(garde, nom), "atteint": n >= limite(garde, nom), "regel": (garde.get("gel") or {}).get("regels", 0)}
    garde["journal"].append(evenement)
    return evenement


def refus_plafond(garde, nom):
    """La cause du refus d'un tour au plafond (aucune suite n'ajoute de tour), ou None."""
    cle, n = f"tours_{nom}_max", garde["tours"][nom]
    if n >= limite(garde, nom):
        return (f"le plafond {cle} est atteint ({n} tour(s) sur {limite(garde, nom)}) et aucune suite n'est consignée qui ajoute des tours : "
                "la main revient au pilote, qui seul en choisit une")
    return None


def refus_drapeaux(garde):
    if garde.get("abandonne"):
        return "le sujet est abandonné (suite consignée)"
    if garde.get("livre_avec_reserve"):
        return "la livraison avec réserve est consignée"
    return None

# ---------------------------------------------------------------------------
# Ce qui se contrôle avant un tour : les commandes du pilote et les hooks font les mêmes contrôles
# ---------------------------------------------------------------------------
GOAL_FILE = "goal.md"                    # le goal du sujet, quand il est posé à la racine ; sinon la sortie de l'étape du goal
SLOT = re.compile(r"<[A-Z][A-Z0-9_]+>")


def lire_empreintes(chemin):
    attendu = {}
    for ligne in Path(chemin).read_text(encoding="utf-8").splitlines():
        if not ligne.strip():
            continue
        empreinte, _, nom = ligne.partition("  ")
        attendu[nom] = empreinte
    return attendu


def verifier_empreintes(sujet, fichiers, scelle):
    """Le premier écart, en nommant le fichier, ou None. Les empreintes du sujet sont comparées aux fichiers et à la copie que
    le scellé en garde : un producteur qui récrit le fichier d'empreintes du sujet ne rattrape pas la copie qu'il ne voit pas.
    Le scellé est toujours là : les hooks le trouvent par le pointeur déclaré au gel, les commandes du pilote par IX_SCELLE_DIR."""
    chez_sujet = Path(sujet) / C.ETAT_DIR / C.EMPREINTES_FILE
    if not chez_sujet.is_file():
        return f"le fichier d'empreintes {C.ETAT_DIR}/{C.EMPREINTES_FILE} a disparu"
    chez_scelle = Path(scelle) / C.EMPREINTES_FILE
    if not chez_scelle.is_file():
        return "la copie des empreintes gardée au scellé a disparu"
    if chez_sujet.read_bytes() != chez_scelle.read_bytes():
        return f"le fichier d'empreintes {C.ETAT_DIR}/{C.EMPREINTES_FILE} ne correspond plus à la copie du scellé"
    attendu = lire_empreintes(chez_scelle)
    if sorted(attendu) != sorted(fichiers):
        return "la liste des fichiers figés a changé"
    for fichier in fichiers:
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


def controle_avant_tour(sujet, scelle, garde, nom, goal=True):
    """Ce qui se vérifie avant un tour de production ou de correction : refuse (HarnaisError) ou ne dit rien. Les mêmes contrôles
    sont faits par `tour` (le pilote), par le hook de début de tour et par celui de fin de tour (sans le goal)."""
    if not garde.get("gel"):
        raise HarnaisError("tour refusé : le sujet n'est pas gelé")
    ecart = verifier_empreintes(sujet, garde["gel"]["fichiers"], scelle)
    if ecart:
        raise HarnaisError(f"tour refusé, écart d'empreinte : {ecart}")
    if goal:
        texte = trouver_goal(sujet)
        if texte is None:
            raise HarnaisError(f"tour refusé : aucun goal ({GOAL_FILE} à la racine du sujet, ou la sortie de l'étape du goal de l'amont)")
        vides = emplacements_vides(texte)
        if vides:
            raise HarnaisError(f"tour refusé : le goal contient encore des emplacements réservés non remplis : {', '.join(vides)}")
    cause = refus_drapeaux(garde)
    if cause:
        raise HarnaisError(f"tour refusé : {cause}")
    cause = refus_plafond(garde, nom)
    if cause:
        raise HarnaisError(f"tour refusé : {cause}")


