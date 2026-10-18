"""Ce que partagent les outils du harnais : le manifeste, le sujet courant, les réglages (A4), l'état du harnais
dans le dossier du sujet, et le scellé.

Le harnais lit ses valeurs dans le manifeste `harnais/points-d-entree.env` (chemins, identifiants d'étapes, valeurs de
verdict) et dans les réglages A4 (plafonds, suites, modèles). Il n'en porte aucune dans son code, sauf les noms des
clés qu'il lit.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import parcours as P   # noqa: E402  (l'exécuteur : isolation, état, scellé, lecture des réglages)

MANIFEST = ROOT / "harnais" / "points-d-entree.env"
ETAT_DIR = ".harnais"            # dans le dossier du sujet : l'état du harnais et les empreintes des fichiers figés
ETAT_FILE = "etat.json"
EMPREINTES_FILE = "empreintes.sha256"
PARCOURS_SLUG = "amont"          # le parcours de l'amont, dans ./parcours/ du sujet
TRACE_SCHEMA = 1


class HarnaisError(Exception):
    """Un refus : une ligne qui nomme la cause, code de sortie 1."""


def now():
    return datetime.now().isoformat(timespec="seconds")


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_atomic(path, text, mode=None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        if mode is not None:
            os.chmod(tmp, mode)
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


# ---------------------------------------------------------------------------
# Le manifeste
# ---------------------------------------------------------------------------
def manifeste():
    """{clé: valeur} du manifeste `harnais/points-d-entree.env` (une ligne `CLE=valeur`, `#` pour un commentaire)."""
    try:
        text = MANIFEST.read_text(encoding="utf-8")
    except OSError:
        raise HarnaisError(f"manifeste introuvable : {MANIFEST}") from None
    values = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip()
    return values


def chemin_manifeste(cle):
    """Un chemin du manifeste, absolu (il est relatif à la racine d'ix-recipes)."""
    valeurs = manifeste()
    if cle not in valeurs:
        raise HarnaisError(f"le manifeste ne porte pas la clé {cle}")
    return ROOT / valeurs[cle]


# ---------------------------------------------------------------------------
# Le sujet courant
# ---------------------------------------------------------------------------
def dossier_sujet():
    return Path(os.environ.get("S") or os.getcwd()).resolve()


def dossier_livrable_env():
    return Path(os.environ["L"]).resolve() if os.environ.get("L") else None


def reglages():
    """(réglages, chemin, sha256) : le fichier A4 du manifeste."""
    try:
        return P.load_reglages(chemin_manifeste("A4"))
    except P.ParcoursError as exc:
        raise HarnaisError(str(exc)) from None


def scelle(sujet):
    """Le dossier scellé de ce sujet : `$IX_SCELLE_DIR/<clé du sujet>`. Refusé comme le refuse l'exécuteur : variable
    absente, dossier dans un dépôt git, ou lié à un chemin que lit le producteur."""
    try:
        racine = P.seal_root(sujet)
    except P.ParcoursError as exc:
        raise HarnaisError(str(exc)) from None
    dossier = racine / P.seal_key(sujet)
    dossier.mkdir(parents=True, exist_ok=True)
    os.chmod(dossier, 0o700)
    return dossier


def chemin_etat(sujet):
    return Path(sujet) / ETAT_DIR / ETAT_FILE


def charger_etat(sujet, requis=True):
    chemin = chemin_etat(sujet)
    if not chemin.is_file():
        if requis:
            raise HarnaisError("ce dossier n'est pas un sujet lancé (pas de .harnais/etat.json) : lancer d'abord le sujet")
        return None
    return json.loads(chemin.read_text(encoding="utf-8"))


def sauver_etat(sujet, etat):
    write_atomic(chemin_etat(sujet), json.dumps(etat, indent=2, ensure_ascii=False) + "\n")


def relatif(chemin, base):
    try:
        return str(Path(chemin).resolve().relative_to(Path(base).resolve()))
    except ValueError:
        return str(chemin)


def pilote():
    """La personne qui pilote : $IX_PILOTE, sinon l'utilisateur git, sinon `n.c.`."""
    if os.environ.get("IX_PILOTE", "").strip():
        return os.environ["IX_PILOTE"].strip()
    try:
        out = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True, timeout=10)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return "n.c."


def titre_de(sujet):
    """Le premier titre de demande.md, sinon le nom du dossier."""
    try:
        for line in (Path(sujet) / "demande.md").read_text(encoding="utf-8").splitlines():
            if line.startswith("#"):
                return line.lstrip("#").strip() or Path(sujet).name
    except OSError:
        pass
    return Path(sujet).name


def etat_amont(sujet):
    """L'état du parcours de l'amont (state.json), ou None."""
    chemin = Path(sujet) / "parcours" / PARCOURS_SLUG / "state.json"
    if not chemin.is_file():
        return None
    return json.loads(chemin.read_text(encoding="utf-8"))


def dossier_amont(sujet):
    return Path(sujet) / "parcours" / PARCOURS_SLUG


def modele_nom(valeur):
    """Un modèle d'après sa clé de réglage (`opus` -> `Opus`) : la version n'est connue d'aucun outil."""
    return str(valeur).capitalize() if valeur else "n.c."


def minuteur(secondes):
    """`2 min 28 s` (A3, colonne durée)."""
    secondes = int(round(secondes))
    if secondes < 60:
        return f"{secondes} s"
    if secondes < 3600:
        return f"{secondes // 60} min {secondes % 60} s"
    return f"{secondes // 3600} h {(secondes % 3600) // 60} min"


def duree_entre(debut, fin):
    try:
        delta = datetime.fromisoformat(fin) - datetime.fromisoformat(debut)
        return minuteur(max(delta.total_seconds(), 0))
    except (TypeError, ValueError):
        return "n.c."


def cout_texte(valeur):
    """`9,40 $` (A3, colonne coût)."""
    return f"{valeur:.2f}".replace(".", ",") + " $"


def cellule(valeur):
    """Une cellule de tableau Markdown : jamais vide, une seule ligne, sans barre verticale."""
    texte = " ".join(str(valeur if valeur is not None else "").split()).replace("|", "¦")
    return texte or "n.c."


def temp_neutre(prefixe):
    """Un dossier de travail neuf sous $TMPDIR, à défaut sous /private/var/tmp (jamais sous /tmp, que Codex peut lire)."""
    base = os.environ.get("TMPDIR") or "/private/var/tmp"
    Path(base).mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=prefixe, dir=base)).resolve()
