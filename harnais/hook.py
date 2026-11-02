"""Les hooks de Claude Code du harnais : ce que la session de production ne doit pas faire, et le compte des tours.

`PreToolUse` (`hook`, la commande de `CMD_HOOK`) refuse, sans condition : l'écriture d'un fichier de réglages qui déclare ou
désactive des hooks (`.claude/settings.json` et `.claude/settings.local.json`, ceux du dossier du sujet et du livrable compris) et
celle du fichier qui déclare le hook ; tout appel qui a la **forme** d'une commande du pilote ; tout accès au scellé (voir plus bas)
et à la variable qui le désigne ; la lecture des réglages qui déclarent les hooks (ils portent l'emplacement de la garde). Il
refuse **tout outil**, une fois le sujet gelé, quand la garde n'est plus intacte (compteur remis en arrière, témoin récrit seul),
quand le plafond de tours est atteint sans suite qui en ajoute, ou quand un fichier figé a changé. Il refuse, une fois le sujet
gelé : l'écriture des fichiers figés, de l'état du harnais (`.harnais/`) et du code du harnais.

Le scellé est fermé à la production par **chemin**, non par forme d'appel : le hook connaît l'emplacement (le pointeur déclaré au gel,
ou `IX_SCELLE_DIR` quand il est donné) et refuse tout outil (`Read`, `Glob`, `Grep`, les outils d'écriture) et toute commande shell
dont un mot, une fois les `~`, les variables d'environnement et les jokers résolus, tombe dans le dossier des scellés, ou en est un
parent sur lequel la commande cherche ou liste en profondeur (`find`, `grep -r`, `rg`, `ls -R`, `du`, `tar`…).

`Stop` (`hook-stop`) compte un tour à **chaque fin de tour** de la session, que la boucle `/goal` la relance ou non, et arrête la
boucle (`continue: false`) quand le plafond est atteint, quand la garde n'est plus intacte ou quand un fichier figé a changé.
`UserPromptSubmit` (`hook-prompt`) refuse de commencer un tour dans ces mêmes cas. Ils lisent la garde au scellé, que la
production ne lance ni ne compte : voir `garde.py`.

Ce que le hook reconnaît d'une commande shell est une **chaîne** : le shell peut écrire, lire et chercher de mille façons que nul motif
ne reconnaît toutes (un interpréteur qui construit son chemin, une variable inconnue du hook, une substitution). Les commandes du
pilote se refusent d'elles-mêmes, quelle que soit la forme de l'appel (elles exigent de tenir le scellé, `commun.exiger_pilote`, et
ce qu'elles changent vit au scellé) ; le scellé n'est pas dans l'environnement de la session de production. Ce qui reste est le seul
résidu, écrit dans `docs/harnais/architecture-harnais.md` §8, avec ce qui le détecte.

Refus : code 2 et la cause sur la sortie d'erreur. Acceptation : code 0, rien sur la sortie. Une entrée illisible, ou une erreur du
hook, est refusée (code 2) : un hook qui laisse tout passer quand il ne comprend pas ne garde rien. Les hooks `Stop` et
`UserPromptSubmit` rendent leur décision en JSON sur la sortie standard, code 0 (`continue: false`, `decision: block`).
"""

import fnmatch
import json
import os
import re
import shlex
import sys
from pathlib import Path

import commun as C
import garde as G
from commun import (ETAT_DIR, ETAT_FILE, EMPREINTES_FILE, ROOT, HarnaisError, manifeste)

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


def scelle_de(dossier):
    """Le scellé du sujet `dossier` tel que le hook le connaît : le pointeur déclaré au gel dans les réglages du sujet (le hook de la
    session de production ne reçoit pas IX_SCELLE_DIR), sinon l'index de `IX_SCELLE_DIR` quand l'appelant le donne (le pilote, les
    essais). None si le sujet n'a pas de scellé connu."""
    declare = C.pointeur_declare(dossier)
    if declare is not None:
        return declare
    brut = os.environ.get("IX_SCELLE_DIR", "").strip()
    if brut:
        racine = Path(brut).expanduser()
        try:
            nom = json.loads((racine / "index.json").read_text(encoding="utf-8")).get(str(Path(dossier).resolve()))
        except (OSError, ValueError):
            nom = None
        if nom:
            return (racine / nom).resolve()
    return None


def projets_geles(cwd):
    """[(dossier du sujet, fichiers figés absolus, scellé ou None)] des sujets que la session touche : celui du dossier de
    l'événement, du dossier de projet, et ceux que l'environnement du pilote désigne (S et L) quand il est présent. Les fichiers figés
    sont ceux de la garde quand elle se lit (l'état du sujet, que la production peut écrire, n'en est que le repli)."""
    vus, trouves = set(), []
    for depart in (cwd, os.environ.get("CLAUDE_PROJECT_DIR"), os.environ.get("S"), os.environ.get("L")):
        if not depart:
            continue
        dossier = sujet_de(depart)
        if dossier is None or dossier in vus:
            continue
        vus.add(dossier)
        scelle = scelle_de(dossier)
        fichiers = None
        if scelle is not None:
            try:
                fichiers = (G.lire_brut(scelle).get("gel") or {}).get("fichiers")
            except HarnaisError:
                fichiers = None
        if fichiers is None:
            try:
                donnees = json.loads((dossier / ETAT_DIR / ETAT_FILE).read_text(encoding="utf-8"))
            except (OSError, ValueError):
                donnees = {}
            fichiers = (donnees.get("gel") or {}).get("fichiers", [])
        trouves.append((dossier, [(dossier / f).resolve() for f in fichiers], scelle))
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


def refuser_ecriture(chemin, projets):
    chemin = Path(chemin)
    if fichier_reglages(chemin):
        raise Refus(f"écriture refusée : {chemin} déclare ou désactive les hooks de la session (réglages interdits à la production)")
    declare = hooks_declares()
    if declare and chemin == declare:
        raise Refus(f"écriture refusée : {chemin} est le fichier qui déclare le hook")
    for projet, figes, _scelle in projets:
        if chemin in figes:
            raise Refus(f"écriture refusée : {chemin} est figé (script de recette, grille ou fixtures) ; seul « contourner » le rouvre, par un retour en 2B")
        if sous(chemin, projet / ETAT_DIR):
            raise Refus(f"écriture refusée : {chemin} fait partie de l'état du harnais (gel, empreintes, tours)")
        if sous(chemin, ROOT / "harnais"):
            raise Refus(f"écriture refusée : {chemin} fait partie du code du harnais")


# ---------------------------------------------------------------------------
# Le scellé : fermé par chemin
# ---------------------------------------------------------------------------
def racines_scelles(projets):
    """Les dossiers des scellés que le hook connaît : le parent de chaque scellé déclaré (le dossier qui les tient tous, donc leurs
    noms aussi) et `IX_SCELLE_DIR` quand il est donné. Chacun sous ses deux formes (donnée, résolue)."""
    racines = []
    for _dossier, _figes, scelle in projets:
        if scelle is not None:
            racines.append(Path(scelle).parent)
    brut = os.environ.get("IX_SCELLE_DIR", "").strip()
    if brut:
        racines.append(Path(brut).expanduser())
    uniques, vus = [], set()
    for racine in racines:
        for forme in (racine, racine.resolve()):
            if str(forme) not in vus:
                vus.add(str(forme))
                uniques.append(forme)
    return uniques


def reglages_proteges(projets):
    """Les réglages de projet qui portent l'emplacement de la garde : la production ne les lit pas."""
    return [dossier / ".claude" / nom for dossier, _f, _s in projets for nom in SETTINGS]


def situation(chemin, cible):
    """Où est `chemin` par rapport à `cible` : "dedans" (égal ou dessous), "ancetre", ou None."""
    chemin, cible = Path(chemin), Path(cible)
    if chemin == cible or cible in chemin.parents:
        return "dedans"
    if chemin in cible.parents:
        return "ancetre"
    return None


def motif_atteint(motif, cible, dossier=True):
    """Un chemin absolu qui contient des jokers (`*?[`, `**`) peut-il désigner `cible`, ce qu'elle contient ou l'un de ses parents ? Sans
    toucher au disque : les composantes du motif sont comparées une à une à celles de la cible. "egal", "dedans" (si `cible` est un
    dossier : le motif descend dessous), "ancetre" ou None."""
    morceaux = [m for m in str(motif).split("/") if m]
    voulus = list(Path(cible).parts[1:])

    def aller(i, j):
        if j == len(voulus):
            if i == len(morceaux) or all(m == "**" for m in morceaux[i:]):
                return "egal"
            return "dedans" if dossier else None
        if i == len(morceaux):
            return "ancetre"
        if morceaux[i] == "**":
            return aller(i, j + 1) or aller(i + 1, j)
        if fnmatch.fnmatchcase(voulus[j], morceaux[i]):
            return aller(i + 1, j + 1)
        return None
    return aller(0, 0)


def refuser_texte_scelle(texte, racines):
    """Le nom de l'emplacement, dans un texte (une commande, un motif, un chemin) : refusé."""
    if "IX_SCELLE_DIR" in texte:
        raise Refus("accès refusé : l'emplacement des scellés est une entrée du pilote, la production ne la lit pas")
    for racine in racines:
        if re.search(re.escape(str(racine)) + r"(?![\w.-])", texte):
            raise Refus("accès refusé : ce chemin est un scellé (part cachée du jugement)")


def refuser_chemin_scelle(chemin, racines, profondeur=False):
    """`chemin` (absolu) est dans un scellé, ou, quand l'outil descend dans l'arbre (`profondeur` : Glob, Grep), en est un parent."""
    for racine in racines:
        place = situation(chemin, racine)
        if place == "dedans" or (profondeur and place == "ancetre"):
            raise Refus("accès refusé : ce chemin est un scellé (part cachée du jugement)" if place == "dedans" else
                        "accès refusé : cette recherche descendrait dans les scellés (part cachée du jugement)")


def refuser_motif_scelle(motif, racines, protegees=()):
    """Un motif de Glob ou de Grep, absolu : refusé s'il peut atteindre un scellé ou un de ses parents, ou un réglage protégé."""
    for racine in racines:
        if motif_atteint(motif, racine):
            raise Refus("accès refusé : ce motif atteindrait les scellés (part cachée du jugement)")
    for reglage in protegees:
        if motif_atteint(motif, reglage, dossier=False) == "egal":
            raise Refus("accès refusé : les réglages qui déclarent les hooks portent l'emplacement de la garde, la production ne les lit pas")


def refuser_lecture_reglages(chemin, protegees):
    chemin = Path(chemin)
    if chemin in [Path(r) for r in protegees] or fichier_reglages(chemin):
        raise Refus("accès refusé : les réglages qui déclarent les hooks portent l'emplacement de la garde, la production ne les lit pas")


# les commandes qui descendent dans l'arbre d'un dossier qu'on leur donne, sans qu'il y faille un drapeau, et celles qui le font avec
RECURSIVES = {"find", "rg", "ag", "ack", "fd", "fdfind", "tree", "du", "rsync", "tar", "zip", "ditto", "ncdu", "gfind", "bsdtar", "7z"}
RECURSIVES_AVEC_DRAPEAU = {"grep": r"-[A-Za-z]*[rR][A-Za-z]*|--recursive|--dereference-recursive", "egrep": r"-[A-Za-z]*[rR][A-Za-z]*",
                           "fgrep": r"-[A-Za-z]*[rR][A-Za-z]*", "zgrep": r"-[A-Za-z]*[rR][A-Za-z]*",
                           "ls": r"-[A-Za-z]*R[A-Za-z]*|--recursive", "cp": r"-[A-Za-z]*[rRa][A-Za-z]*|--recursive|--archive",
                           "scp": r"-[A-Za-z]*r[A-Za-z]*", "chmod": r"-[A-Za-z]*R[A-Za-z]*", "chown": r"-[A-Za-z]*R[A-Za-z]*"}
INTERDITES = {"mdfind", "locate", "mlocate", "plocate", "updatedb"}   # cherchent partout, sans chemin à vérifier
ENVELOPPES = {"sudo", "env", "command", "time", "nohup", "nice", "exec", "xargs", "builtin"}


def mots_de(commande):
    """[(mots, texte)] de chaque commande simple d'une ligne shell, y compris celles que `$( )`, les accents graves, les parenthèses et
    `sh -c '…'` enferment."""
    plat = re.sub(r"\$\(|`|\(|\)|\{|\}", ";", commande)
    for texte in re.split(r"\|\||&&|[;|&\n]", plat):
        try:
            mots = shlex.split(texte)
        except ValueError:
            mots = texte.split()
        if not mots:
            continue
        yield mots, texte
        if os.path.basename(mots[0]) in ("sh", "bash", "zsh", "dash", "ksh", "eval") and len(mots) > 1:
            interne = " ".join(mots[2:] if mots[1] in ("-c", "-lc", "-ic", "-xc") and len(mots) > 2 else mots[1:])
            if interne and interne != texte.strip():
                yield from mots_de(interne)


def candidat_chemin(mot, cwd):
    """(chemin absolu, a des jokers, variable non résolue) de ce qu'un mot de commande peut désigner, ou None si ce n'est pas un chemin."""
    brut = mot.split("=", 1)[1] if mot.startswith("-") and "=" in mot else mot
    if not brut or (brut.startswith("-") and len(brut) > 1):
        return None
    etendu = os.path.expanduser(os.path.expandvars(brut))
    inconnu = "$" in etendu or "`" in etendu
    absolu_ = etendu if os.path.isabs(etendu) else os.path.join(cwd, etendu)
    absolu_ = os.path.normpath(absolu_)
    return absolu_, bool(re.search(r"[*?\[]", absolu_)), inconnu


def refuser_scelle_shell(commande, cwd, racines, protegees):
    """Le scellé et les réglages protégés, dans une commande shell : le nom de l'emplacement, un mot qui désigne (jokers, `~` et
    variables d'environnement résolus) un scellé, une commande qui descend dans l'arbre d'un parent du scellé, une recherche
    qui ne dit pas où (`mdfind`, `locate`)."""
    refuser_texte_scelle(commande, racines)
    plat = sans_decor(commande)
    if re.search(r"\.claude/settings", plat):
        raise Refus("accès refusé : les réglages qui déclarent les hooks portent l'emplacement de la garde, la production ne les lit pas")
    courant = str(cwd)
    for mots, texte in mots_de(commande):
        nus = list(mots)
        while nus and (re.fullmatch(r"\w+=\S*", nus[0]) or os.path.basename(nus[0]) in ENVELOPPES):
            nus = nus[1:]
        if not nus:
            continue
        verbe = os.path.basename(nus[0])
        arguments = nus[1:]
        if verbe in INTERDITES:
            raise Refus(f"commande refusée : « {verbe} » cherche partout, scellés compris ; la production cherche par un chemin qu'elle donne")
        profond = verbe in RECURSIVES or (verbe in RECURSIVES_AVEC_DRAPEAU and any(
            re.fullmatch(RECURSIVES_AVEC_DRAPEAU[verbe], m) for m in arguments if m.startswith("-")))
        if verbe in RECURSIVES and not [m for m in arguments if not m.startswith("-")]:
            profond_ici = [courant]   # sans chemin donné, la commande part du dossier courant
        else:
            profond_ici = []
        for chemin_ in profond_ici:
            for racine in racines:
                if situation(chemin_, racine) in ("dedans", "ancetre"):
                    raise Refus("commande refusée : cette recherche partirait d'un dossier qui contient les scellés")
        for mot in arguments:
            trouve = candidat_chemin(mot, courant)
            if trouve is None:
                continue
            chemin_, joker, inconnu = trouve
            if inconnu and verbe in RECURSIVES and verbe not in ("rg", "ag", "ack", "fd", "fdfind"):
                raise Refus(f"commande refusée : « {verbe} » reçoit un chemin que le hook ne sait pas résoudre ({mot}) ; "
                            "la production donne le chemin en clair")
            for racine in racines:
                place = motif_atteint(chemin_, racine) if joker else situation(Path(chemin_).resolve(), racine)
                if place in ("egal", "dedans") or (place == "ancetre" and profond):
                    raise Refus("commande refusée : elle touche un scellé (part cachée du jugement)" if place != "ancetre" else
                                "commande refusée : elle descendrait dans un dossier qui contient les scellés")
            for reglage in protegees:
                place = motif_atteint(chemin_, reglage, dossier=False) if joker else situation(Path(chemin_).resolve(), reglage)
                if place in ("egal", "dedans"):
                    raise Refus("commande refusée : les réglages qui déclarent les hooks portent l'emplacement de la garde, "
                                "la production ne les lit pas")
        if verbe == "cd" and arguments:
            trouve = candidat_chemin(arguments[0], courant)
            if trouve and not trouve[1] and not trouve[2]:
                courant = trouve[0]


def refuser_si_bloque(projets):
    """Une fois le sujet gelé, tout outil est refusé tant que la garde n'est pas intacte, que le plafond n'est pas levé par une suite qui
    ajoute des tours, et qu'aucun fichier figé n'a changé : la boucle peut avoir été relancée par un autre chemin que `/goal`, et la
    production n'a rien à faire d'un outil qu'on lui refuse pour une de ces causes."""
    for dossier, _figes, scelle in projets:
        if scelle is None:
            continue
        try:
            with G.verrou(scelle):
                garde = G.lire_brut(scelle)
                cause = G.controle(dossier, garde)
                if cause:
                    raise HarnaisError(f"écart de compteur : {cause}")
                nom = G.compte_actif(garde)
                if nom is not None:
                    G.controle_avant_tour(dossier, scelle, garde, nom, goal=False)
        except HarnaisError as exc:
            raise Refus(f"outils refusés, la main revient au pilote : {exc}") from None
        except OSError as exc:
            raise Refus(f"outils refusés : la garde du sujet n'est pas lisible ({type(exc).__name__})") from None


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


def refuser_shell(commande, projets, cwd):
    refuser_pilote(commande)
    refuser_scelle_shell(commande, cwd, racines_scelles(projets), reglages_proteges(projets))
    if VIDE_ENVIRONNEMENT.search(sans_decor(commande)):
        raise Refus("commande refusée : la production ne vide pas son environnement (l'emplacement des scellés n'y est pas, "
                    "et ne doit pas y être)")
    declare = hooks_declares()
    candidats = set()
    for projet, figes, _scelle in projets:
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
    refuser_si_bloque(projets)
    racines = racines_scelles(projets)
    protegees = reglages_proteges(projets)
    if outil in OUTILS_ECRITURE:
        for cle in OUTILS_ECRITURE[outil]:
            if entree.get(cle):
                cible = absolu(entree[cle], cwd)
                refuser_ecriture(cible, projets)
                refuser_texte_scelle(str(cible), racines)
                refuser_chemin_scelle(cible, racines)
        return
    if outil in OUTILS_LECTURE:
        for cle in OUTILS_LECTURE[outil]:
            valeur = entree.get(cle)
            if not valeur:
                continue
            refuser_texte_scelle(str(valeur), racines)
            if outil == "Glob" and cle == "pattern" or outil == "Grep" and cle == "glob":
                base = absolu(entree.get("path") or cwd, cwd)
                motif = str(valeur) if os.path.isabs(str(valeur)) else os.path.normpath(os.path.join(str(base), str(valeur)))
                refuser_motif_scelle(motif, racines, protegees)
            else:
                chemin = absolu(valeur, cwd)
                refuser_chemin_scelle(chemin, racines, profondeur=outil in ("Glob", "Grep"))
                refuser_lecture_reglages(chemin, protegees)
        if outil in ("Glob", "Grep") and not entree.get("path"):   # sans dossier donné, la recherche part du dossier de l'événement
            refuser_chemin_scelle(absolu(cwd, cwd), racines, profondeur=True)
        return
    if outil == "Bash":
        refuser_shell(str(entree.get("command") or ""), projets, cwd)


# ---------------------------------------------------------------------------
# Stop et UserPromptSubmit : le compte des tours, l'arrêt de la boucle
# ---------------------------------------------------------------------------
def lire_evenement():
    try:
        evenement = json.loads(sys.stdin.read() or "{}")
    except ValueError:
        return None
    return evenement if isinstance(evenement, dict) else None


def sujet_de_session(evenement):
    for depart in (os.environ.get("CLAUDE_PROJECT_DIR"), (evenement or {}).get("cwd"), os.getcwd()):
        if depart:
            dossier = sujet_de(depart)
            if dossier is not None:
                return dossier
    return None


def arreter(raison, code=0):
    """Fin de tour : la boucle s'arrête (`continue: false`), la main revient au pilote."""
    print(json.dumps({"continue": False, "stopReason": f"Arrêt par le harnais : {raison}"}, ensure_ascii=False))
    return code


def main_stop(garde_arg):
    """Événement `Stop` : un tour s'achève. Il est compté, dans la garde, dans le compteur de la phase en cours ; la boucle s'arrête au
    plafond, quand la garde n'est plus intacte et quand un fichier figé a changé. Sans suite qui ajoute des tours, le prochain tour ne
    peut pas commencer (`hook-prompt`, `hook`)."""
    evenement = lire_evenement()
    try:
        scelle = Path(garde_arg)
        sujet = sujet_de_session(evenement)
        if sujet is None:
            return arreter("le dossier du sujet est introuvable depuis la session : le tour ne peut pas être contrôlé")
        with G.verrou(scelle):
            garde = G.lire_brut(scelle)
            cause = G.controle(sujet, garde)
            if cause:
                return arreter(f"écart de compteur : {cause}")
            nom = G.compte_actif(garde)
            if nom is None:
                return 0
            ev = G.compter(garde, nom, C.P.now_us())
            G.sauver(scelle, sujet, garde)
            try:
                G.controle_avant_tour(sujet, scelle, garde, nom, goal=False)
            except HarnaisError as exc:
                if ev["atteint"] and not G.refus_drapeaux(garde):
                    return arreter(f"plafond tours_{nom}_max atteint ({ev['n']} tour(s) comptés sur {ev['limite']}) : la main revient au "
                                   "pilote, qui seul choisit la suite")
                return arreter(str(exc))
            print(json.dumps({"systemMessage": f"Tour {ev['n']} sur {ev['limite']} ({'production' if nom == 'goal' else 'correction'})."},
                             ensure_ascii=False))
            return 0
    except (HarnaisError, OSError) as exc:
        return arreter(str(exc))
    except Exception as exc:   # un hook qui plante ne doit pas laisser la boucle continuer
        return arreter(f"erreur du hook de fin de tour ({type(exc).__name__}: {exc})")


def main_prompt(garde_arg):
    """Événement `UserPromptSubmit` : un tour va commencer. Il est refusé (`decision: block`) au plafond, sur un écart de compteur,
    d'empreinte ou de goal."""
    evenement = lire_evenement()
    try:
        scelle = Path(garde_arg)
        sujet = sujet_de_session(evenement)
        if sujet is None:
            raise HarnaisError("le dossier du sujet est introuvable depuis la session : le tour ne peut pas être contrôlé")
        with G.verrou(scelle):
            garde = G.lire_brut(scelle)
            cause = G.controle(sujet, garde)
            if cause:
                raise HarnaisError(f"écart de compteur : {cause}")
            nom = G.compte_actif(garde)
            if nom is not None:
                G.controle_avant_tour(sujet, scelle, garde, nom, goal=True)
    except (HarnaisError, OSError) as exc:
        print(json.dumps({"decision": "block", "reason": f"Refusé par le harnais : {exc}"}, ensure_ascii=False))
    except Exception as exc:
        print(json.dumps({"decision": "block", "reason": f"Refusé par le harnais : erreur du hook ({type(exc).__name__}: {exc})"},
                         ensure_ascii=False))
    return 0


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
    except Exception as exc:   # un hook qui plante (code 1) laisserait l'outil passer : on refuse
        print(f"Refusé par le harnais : erreur du hook ({type(exc).__name__}: {exc})", file=sys.stderr)
        return 2
    return 0
