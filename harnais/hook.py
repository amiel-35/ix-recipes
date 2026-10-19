"""Le hook `PreToolUse` du harnais : il refuse ce que la session de production ne doit pas faire.

Il refuse, sans condition : l'écriture d'un fichier de réglages qui déclare ou désactive des hooks (`.claude/settings.json`
et `.claude/settings.local.json`, ceux du dossier du sujet et du livrable compris) et celle du fichier qui déclare le hook ;
tout appel qui a la **forme** d'une commande du pilote (l'emplacement du scellé, le choix d'une suite, le regel, le juge…) ;
tout accès au scellé et à la variable qui le désigne, et les commandes qui vident l'environnement.
Il refuse, une fois le sujet gelé : l'écriture des fichiers figés, de l'état du harnais (`.harnais/`) et du code du harnais.

Ce que le hook reconnaît d'un appel est une **chaîne** : il ne tient donc pas seul les commandes du pilote ni le scellé.
Les commandes du pilote se refusent d'elles-mêmes, quelle que soit la forme de l'appel (elles exigent le jeton du scellé,
`commun.exiger_pilote`) ; le scellé n'est pas dans l'environnement de la session de production. Ce que le hook ne voit pas est
dit dans `docs/harnais/architecture-harnais.md` §8 : une commande shell peut écrire de mille façons que nul motif ne
reconnaît toutes ; les empreintes vérifiées par `tour` (si la production le lance) et par `empreintes` et `juge` (le pilote)
rattrapent l'écart.

Refus : code 2 et la cause sur la sortie d'erreur. Acceptation : code 0, rien sur la sortie. Une entrée illisible est refusée
(code 2) : un hook qui laisse tout passer quand il ne comprend pas ne garde rien.
"""

import json
import os
import re
import shlex
import sys
from pathlib import Path

from commun import (ETAT_DIR, ETAT_FILE, EMPREINTES_FILE, ROOT, manifeste)

OUTILS_ECRITURE = {"Write": ("file_path",), "Edit": ("file_path",), "MultiEdit": ("file_path",),
                   "NotebookEdit": ("notebook_path", "file_path")}
OUTILS_LECTURE = {"Read": ("file_path",), "Glob": ("path", "pattern"), "Grep": ("path", "glob"), "NotebookRead": ("notebook_path",)}
SETTINGS = ("settings.json", "settings.local.json")
COMMANDES_ECRITURE = {"tee", "mv", "cp", "rm", "rmdir", "chmod", "chown", "truncate", "dd", "install", "patch", "ln", "unlink",
                      "shred", "sponge", "touch", "ed", "ex", "vi", "vim", "nano"}
GIT_ECRITURE = {"checkout", "restore", "reset", "clean", "rm", "mv", "apply", "stash", "switch"}
INTERPRETES = {"python", "python3", "perl", "ruby", "node", "bash", "sh", "zsh", "php"}
ECRITURE_INTERPRETE = re.compile(r"\bopen\([^)]*['\"][wax]|\.write\(|\bwrite_text\b|\bwrite_bytes\b|\bos\.(?:remove|unlink|rename|replace)\b"
                                 r"|\bshutil\.|\bfs\.(?:write|unlink|rename|rm)|\bFile\.(?:write|delete)|\bunlink\b|\bsysopen\b")
REDIRECTION = re.compile(r"^(?:[0-9]*|&)>>?(?!&)(.*)$")


class Refus(Exception):
    pass


def sujet_de(dossier):
    """Le dossier du sujet gelé que désigne `dossier` ou l'un de ses parents : celui qui porte `.harnais/etat.json`, ou
    celui qu'un livrable désigne dans `.git/ix-sujet`. None sinon."""
    dossier = Path(dossier).resolve()
    for place in (dossier, *dossier.parents):
        if (place / ETAT_DIR / ETAT_FILE).is_file():
            return place
        pointeur = place / ".git" / "ix-sujet"
        if pointeur.is_file():
            try:
                cible = Path(pointeur.read_text(encoding="utf-8").strip()).resolve()
            except OSError:
                continue
            if (cible / ETAT_DIR / ETAT_FILE).is_file():
                return cible
    return None


def projets_geles(cwd):
    """[(dossier du sujet, fichiers figés absolus)] des sujets que la session touche : celui du dossier de l'événement, du
    dossier de projet, et ceux que l'environnement du pilote désigne (S et L) quand il est présent."""
    vus, trouves = set(), []
    for depart in (cwd, os.environ.get("CLAUDE_PROJECT_DIR"), os.environ.get("S"), os.environ.get("L")):
        if not depart:
            continue
        dossier = sujet_de(depart)
        if dossier is None or dossier in vus:
            continue
        vus.add(dossier)
        try:
            donnees = json.loads((dossier / ETAT_DIR / ETAT_FILE).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            donnees = {}
        gel = donnees.get("gel") or {}
        trouves.append((dossier, [(dossier / f).resolve() for f in gel.get("fichiers", [])]))
    return trouves


def absolu(valeur, base):
    chemin = Path(str(valeur)).expanduser()
    return (chemin if chemin.is_absolute() else Path(base) / chemin).resolve()


def sous(chemin, parent):
    chemin, parent = Path(chemin), Path(parent)
    return chemin == parent or parent in chemin.parents


def fichier_reglages(chemin):
    return chemin.name in SETTINGS and chemin.parent.name == ".claude"


def hooks_declares():
    """Le fichier qui déclare le hook (HOOKS_FICHIER du manifeste), absolu."""
    try:
        return (ROOT / manifeste()["HOOKS_FICHIER"]).resolve()
    except (KeyError, OSError):
        return None


def scelle_env():
    brut = os.environ.get("IX_SCELLE_DIR", "").strip()
    return Path(brut).expanduser().resolve() if brut else None


def refuser_ecriture(chemin, projets):
    chemin = Path(chemin)
    if fichier_reglages(chemin):
        raise Refus(f"écriture refusée : {chemin} déclare ou désactive les hooks de la session (réglages interdits à la production)")
    declare = hooks_declares()
    if declare and chemin == declare:
        raise Refus(f"écriture refusée : {chemin} est le fichier qui déclare le hook")
    for projet, figes in projets:
        if chemin in figes:
            raise Refus(f"écriture refusée : {chemin} est figé (script de recette, grille ou fixtures) ; seul « contourner » le rouvre, par un retour en 2B")
        if sous(chemin, projet / ETAT_DIR):
            raise Refus(f"écriture refusée : {chemin} fait partie de l'état du harnais (gel, empreintes, tours)")
        if sous(chemin, ROOT / "harnais"):
            raise Refus(f"écriture refusée : {chemin} fait partie du code du harnais")


def refuser_acces_scelle(texte, chemin_scelle):
    if "IX_SCELLE_DIR" in texte:
        raise Refus("accès refusé : l'emplacement des scellés est une entrée du pilote, la production ne la lit pas")
    if chemin_scelle and (str(chemin_scelle) in texte):
        raise Refus("accès refusé : ce chemin est un scellé (part cachée du jugement)")


POUR_LE_PILOTE = ("sceau", "suite", "regeler", "ouvrir", "juge", "geler", "lancer", "contre-verif", "contre_verif")
CLES_PILOTE = ("CMD_SCEAU", "CMD_SUITE", "CMD_REGELER", "CMD_OUVRIR", "CMD_JUGE", "CMD_GELER", "CMD_LANCER", "CMD_CONTRE_VERIF")
# ce qui désigne l'outil du harnais, quelle que soit la façon de l'appeler : le script, le module, une fonction de commande
APPEL_HARNAIS = re.compile(r"harnais\.py|\bimport\s+harnais\b|\bfrom\s+harnais\b|-m\s+harnais\b|runpy|"
                           r"\bcmd_(?:sceau|suite|regeler|ouvrir|juge|geler|lancer|contre_verif)\b")
VERBE_PILOTE = re.compile(r"(?<![\w-])(?:" + "|".join(re.escape(v) for v in POUR_LE_PILOTE) + r")(?![\w-])")
# ce qui vide l'environnement d'une session (au mieux : l'environnement de la production ne porte pas le scellé)
VIDE_ENVIRONNEMENT = re.compile(r"\bprintenv\b|(?:^|[\s;|&(])env\s*(?:$|[|;&>)])|\bexport\s+-p\b|\bdeclare\s+-[a-zA-Z]*[xp]\b|"
                                r"\bcompgen\s+-[ev]\b|\bos\.environ\b|/proc/[^\s]*/environ|\bset\s*(?:$|[|;&>)])")


def sans_decor(texte):
    """Le texte sans guillemets ni antislash, espaces réunis : `su''ite` et `"suite"` valent `suite`."""
    return " ".join(re.sub(r"[\"'\\]", "", texte).split())


def refuser_pilote(commande):
    """Ce que la session de production ne lance jamais : donner l'emplacement du scellé, choisir une suite à un plafond,
    rouvrir le gel, lancer le juge, ouvrir le jugement, geler, lancer un sujet, rendre une contre-vérification.

    Le hook ne reconnaît que la **forme** d'un appel : la chaîne de la commande du manifeste, ou le nom du script (ou du
    module) suivi, dans la même commande simple, d'un mot du pilote, guillemets et antislash ôtés. Une autre forme (un
    chemin construit, une variable, un script copié) lui échappe, et c'est l'outil qui refuse alors (`exiger_pilote`)."""
    valeurs = manifeste()
    plat = sans_decor(commande)
    for cle in CLES_PILOTE:
        brut = sans_decor(valeurs.get(cle, ""))
        if brut and (brut in plat or brut.replace("$R", str(ROOT)) in plat):
            raise Refus(f"appel refusé : « {cle.removeprefix('CMD_').lower().replace('_', '-')} » est une commande du pilote, "
                        "la session de production ne la lance pas")
    for texte in re.split(r"\|\||&&|[;|&\n]", commande):
        segment = sans_decor(texte)
        appel = APPEL_HARNAIS.search(segment)
        if not appel:
            continue
        if appel.group(0).startswith("cmd_"):
            raise Refus(f"appel refusé : « {appel.group(0)} » est une commande du pilote, la session de production ne la lance pas")
        verbe = VERBE_PILOTE.search(segment, appel.end())
        if verbe:
            raise Refus(f"appel refusé : « {verbe.group(0)} » est une commande du pilote, la session de production ne la lance pas")


def candidats_figes(figes, projet):
    """Les chaînes dont la présence dans une commande shell désigne un fichier figé : chemin absolu, chemin relatif au
    sujet, nom du fichier, dossier qui le contient (sous le sujet)."""
    candidats = set()
    for chemin in figes:
        candidats.add(str(chemin))
        try:
            relatif = chemin.relative_to(projet)
        except ValueError:
            continue
        candidats.add(str(relatif))
        candidats.add(chemin.name)
        if relatif.parent != Path("."):
            candidats.add(str(relatif.parent))
    candidats.add(ETAT_DIR)
    return {c for c in candidats if c}


def segments(commande):
    """Les commandes simples d'une ligne shell : (mots, texte), séparées par ; && || | et les fins de ligne."""
    for texte in re.split(r"\|\||&&|[;|\n]", commande):
        try:
            mots = shlex.split(texte)
        except ValueError:
            mots = texte.split()
        if mots:
            yield mots, texte


def cibles_ecriture(mots, texte):
    """Les mots qui désignent ce qu'une commande simple écrit, déplace ou supprime ; None si elle n'écrit pas.
    Un `>` désigne le mot qui le suit ; une commande d'écriture désigne tous ses arguments ; un interpréteur qui
    écrit dans son code désigne tout le texte (on ne sait pas où)."""
    cibles, ecrit = [], False
    i = 0
    while i < len(mots):
        redirection = REDIRECTION.match(mots[i])
        if redirection:
            ecrit = True
            cible = redirection.group(1) or (mots[i + 1] if i + 1 < len(mots) else "")
            cibles.append(cible)
            i += 1 if redirection.group(1) else 2
            continue
        i += 1
    mots_nus = [m for m in mots if not REDIRECTION.match(m)]
    while mots_nus and (re.fullmatch(r"\w+=\S*", mots_nus[0]) or mots_nus[0] in ("sudo", "env", "command", "time", "nohup")):
        mots_nus = mots_nus[1:]
    if not mots_nus:
        return cibles if ecrit else None
    commande = os.path.basename(mots_nus[0])
    arguments = [m.split("=", 1)[-1] for m in mots_nus[1:]]
    if commande in COMMANDES_ECRITURE:
        return cibles + arguments
    if commande in ("sed", "perl", "awk", "gawk") and any(re.fullmatch(r"-[A-Za-z]*i[A-Za-z]*(?:=.*)?|-i.*|--in-place.*|inplace", m)
                                                         for m in mots_nus[1:]):
        return cibles + arguments
    if commande == "git" and len(mots_nus) > 1 and mots_nus[1] in GIT_ECRITURE:
        return cibles + arguments
    if commande in INTERPRETES and ECRITURE_INTERPRETE.search(texte):
        return cibles + [texte]
    return cibles if ecrit else None


def designe(mot, candidat):
    mot, candidat = mot.strip("\"'").rstrip("/"), candidat.rstrip("/")
    return bool(mot) and (mot == candidat or mot.endswith("/" + candidat) or mot.startswith(candidat + "/")
                          or f"/{candidat}/" in mot or candidat in mot and len(mot) > 200)


def refuser_shell(commande, projets):
    refuser_pilote(commande)
    refuser_acces_scelle(commande, scelle_env())
    if VIDE_ENVIRONNEMENT.search(sans_decor(commande)):
        raise Refus("commande refusée : la production ne vide pas son environnement (l'emplacement des scellés n'y est pas, "
                    "et ne doit pas y être)")
    declare = hooks_declares()
    candidats = set()
    for projet, figes in projets:
        candidats |= candidats_figes(figes, projet)
    for mots, texte in segments(commande):
        cibles = cibles_ecriture(mots, texte)
        if cibles is None:
            continue
        for cible in cibles:
            if re.search(r"\.claude/(?:hooks(?:/|$)|settings(?:\.local)?\.json)", cible) or fichier_reglages(Path(cible)):
                raise Refus("commande refusée : elle écrit dans les réglages qui déclarent les hooks de la session")
            if declare and (cible == str(declare) or cible.endswith("/" + declare.name) and "harnais" in cible):
                raise Refus(f"commande refusée : elle écrit dans {declare.name}, qui déclare le hook")
            if projets and (str(ROOT / "harnais") in cible):
                raise Refus("commande refusée : elle écrit dans le code du harnais")
            for candidat in sorted(candidats, key=len, reverse=True):
                if designe(cible, candidat) or (cible == texte and candidat in texte):
                    raise Refus(f"commande refusée : elle écrit là où est figé « {candidat} » (script de recette, grille, fixtures "
                                "ou état du harnais)")


def decider(evenement):
    """Lève Refus avec la cause, ou rend None. `evenement` : l'objet JSON d'un événement PreToolUse."""
    outil = evenement.get("tool_name") or ""
    entree = evenement.get("tool_input") or {}
    cwd = evenement.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    projets = projets_geles(cwd)
    if outil in OUTILS_ECRITURE:
        for cle in OUTILS_ECRITURE[outil]:
            if entree.get(cle):
                refuser_ecriture(absolu(entree[cle], cwd), projets)
                refuser_acces_scelle(str(absolu(entree[cle], cwd)), scelle_env())
        return
    if outil in OUTILS_LECTURE:
        for cle in OUTILS_LECTURE[outil]:
            if entree.get(cle):
                refuser_acces_scelle(str(entree[cle]), scelle_env())
                if scelle_env() and sous(absolu(entree[cle], cwd), scelle_env()):
                    raise Refus("accès refusé : ce chemin est un scellé (part cachée du jugement)")
        return
    if outil == "Bash":
        refuser_shell(str(entree.get("command") or ""), projets)


def main():
    try:
        evenement = json.loads(sys.stdin.read() or "{}")
        if not isinstance(evenement, dict):
            raise ValueError("l'événement n'est pas un objet JSON")
    except ValueError as exc:
        print(f"refusé : entrée illisible ({exc})", file=sys.stderr)
        return 2
    try:
        decider(evenement)
    except Refus as refus:
        print(f"Refusé par le harnais : {refus}", file=sys.stderr)
        return 2
    return 0
