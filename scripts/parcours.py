#!/usr/bin/env python3
"""
parcours.py — step-by-step runner for workflow recipes (spec: docs/executeur.md).

Plays the `workflow` block of a recipe (skills/<id>.md), one fresh engine call
per step. The script builds each step's message itself, so each step receives
only the fields listed in its `receives` and nothing else.

Usage:
    python3 scripts/parcours.py new brief-client --input demande.md [--slug S] [--engine claude]
    python3 scripts/parcours.py next <slug> [--yes] [--if-state FINGERPRINT]
    python3 scripts/parcours.py plan <slug> --json
    python3 scripts/parcours.py status <slug> [--json]
    python3 scripts/parcours.py validate <slug> [--context fiche.json] [--stop]
    python3 scripts/parcours.py answer <slug> --file reponses.md | --none
    python3 scripts/parcours.py choose <slug> --run explorer,decision | --skip
    python3 scripts/parcours.py rerun <slug> <step> [--extra <step>.<field>]
    python3 scripts/parcours.py retry <slug>
    python3 scripts/parcours.py handoff <slug> <step> --file champs.md   (failed, done or paused step)

Common options: --engine claude|codex|agy|vibe|fake, --engine-step <step>=<engine>
(repeatable), --yes, --timeout SECONDS (default 900), --max-budget-usd (default 5,
claude only), --parcours-dir (default ./parcours), --json (machine output for plan and
status; errors become {"error": code, "message": ...} on stdout, exit code 1),
--json-errors (the JSON error format only, also accepted before the command).
Exit code 2 is an argument error (a bug for a caller that builds the command line).

The `fake` engine runs nothing: it reads canned outputs from the directory named
by the PARCOURS_FAKE_DIR environment variable (<step-id>.md, and
<step-id>.retry.md for the retry call) and logs each message it receives in
<PARCOURS_FAKE_DIR>/received/. Used by the tests.
"""

import argparse
import contextlib
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import unicodedata
from datetime import datetime
from pathlib import Path

import yaml

try:
    import fcntl
except ImportError:  # not available on Windows; the lock is then skipped
    fcntl = None

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
ENGINES = ("claude", "codex", "agy", "vibe", "fake")
DEFAULT_TIMEOUT = 900
DEFAULT_BUDGET = 5.0
ARGV_PROMPT_LIMIT = 200_000  # bytes; agy takes the prompt in argv only (visible in `ps`); macOS ARG_MAX is 1 MB
LEAK_WORDS = 40          # a copied paragraph of the raw request; short quotes stay allowed
MIN_LEAK_WORDS = 4       # below this, an input is too short to be checked
VERBATIM_SHINGLE = 8     # word runs used to measure how much of the request a verbatim field copies
VERBATIM_MAX_SHARE = 0.85  # a verbatim field may copy at most this share of the raw request
SKIPPED = "skipped"
NOT_STATED = "not stated"
NO_ANSWERS = "none — open points remain hypotheses"
PAUSES = ("none", "validate", "answers", "choose")


class ParcoursError(Exception):
    """Any expected failure: reported on one line, exit code 1.

    `code` is the machine-readable name printed by --json / --json-errors.
    """

    code = "error"


class LockedError(ParcoursError):
    code = "locked"


class StateChanged(ParcoursError):
    code = "state_changed"


class NotFound(ParcoursError):
    code = "not_found"


class EngineError(ParcoursError):
    """An engine call failed; `cost` is what it still cost (claude reports it even on failure)."""

    code = "engine"

    def __init__(self, message, cost=0.0):
        super().__init__(message)
        self.cost = float(cost or 0.0)


class EngineTimeout(EngineError):
    code = "timeout"


class ParseError(ParcoursError):
    code = "parse"


class LeakError(ParcoursError):
    code = "leak"


class MissingInput(ParcoursError):
    code = "missing_input"


# ---------------------------------------------------------------------------
# Files: atomic writes, lock, versioned copies
# ---------------------------------------------------------------------------
def now():
    return datetime.now().isoformat(timespec="seconds")


def write_atomic(path, text):
    """Write to a temporary file in the same folder, then rename over `path`."""
    path = Path(path)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


@contextlib.contextmanager
def parcours_lock(directory):
    """Exclusive non-blocking lock; released by the OS even if the process dies."""
    handle = open(Path(directory) / ".lock", "a")
    try:
        if fcntl is not None:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                raise LockedError("un autre processus travaille déjà sur ce parcours (verrou pris)")
        yield
    finally:
        handle.close()


def is_locked(directory):
    """True when another process holds the parcours lock. Non-blocking, writes nothing.

    The probe takes (and at once releases) a shared lock on an existing `.lock`; a missing
    file means nobody ever locked, and is not created here.
    """
    path = Path(directory) / ".lock"
    if fcntl is None or not path.exists():
        return False
    try:
        with open(path, "r") as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except OSError:
                return True
            fcntl.flock(handle, fcntl.LOCK_UN)
    except OSError:
        return False
    return False


@contextlib.contextmanager
def terminate_as_exit():
    """SIGTERM becomes SystemExit, so that run_process kills the engine's own process group.

    Without it, stopping a `next` from outside would orphan a (paid) engine call, since each
    engine runs in a session of its own. The step is then left 'running' (see `retry`).
    """
    import threading
    if threading.current_thread() is not threading.main_thread():
        yield
        return

    def handler(signum, frame):
        raise SystemExit(128 + signum)

    previous = signal.signal(signal.SIGTERM, handler)
    try:
        yield
    finally:
        signal.signal(signal.SIGTERM, previous)


def versioned_name(path):
    """First free `<stem>.vN<suffix>` next to `path`."""
    n = 1
    while True:
        candidate = path.with_name(f"{path.stem}.v{n}{path.suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def say(message=""):
    print(message)


def warn(message):
    print(f"Avertissement : {message}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Recipe
# ---------------------------------------------------------------------------
FRONTMATTER_RE = re.compile(r"\A---[ \t]*\n(.*?)\n---[ \t]*\n?", re.S)


def split_frontmatter(text):
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, text[match.end():]


def load_recipe(recipe_id):
    path = ROOT / "skills" / f"{recipe_id}.md"
    if not path.is_file():
        raise ParcoursError(f"recette introuvable : {path}")
    fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
    workflow = fm.get("workflow") or {}
    if not workflow.get("steps"):
        raise ParcoursError(f"'{recipe_id}' n'a pas de bloc workflow")
    steps = [normalize_step(raw, i) for i, raw in enumerate(workflow["steps"])]
    return {
        "id": recipe_id,
        "version": str(fm.get("version", "")),
        "context_sheet": list(workflow.get("context_sheet") or []),
        "context_definitions": context_definitions(body),
        "steps": steps,
    }


def context_definitions(body):
    """`field -> definition` from the rows of the recipe body's « Context sheet » table.

    Step 1 needs them: a key name alone (`named_solutions`) does not say what goes in it
    nor what stays out (items the request imposes).
    """
    found, inside = {}, False
    for line in (body or "").splitlines():
        heading = re.match(r"#+\s*(.*?)\s*$", line)
        if heading:
            inside = heading.group(1).casefold() == "context sheet"
            continue
        row = re.match(r"\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|\s*$", line) if inside else None
        if row:
            found[row.group(1)] = row.group(2)
    return found


def normalize_step(raw, index):
    for key in ("id", "skill", "mission", "transmits"):
        if not raw.get(key):
            raise ParcoursError(f"étape {index + 1} de la recette : champ '{key}' manquant")
    pause = raw.get("pause", "none")
    if pause not in PAUSES:
        raise ParcoursError(f"étape '{raw['id']}' : pause '{pause}' inconnue")
    return {
        "id": raw["id"],
        "skill": raw["skill"],
        "mission": str(raw["mission"]).strip(),
        "receives": list(raw.get("receives") or []),
        "transmits": list(raw["transmits"]),
        "pause": pause,
        "model": raw.get("model"),
        "optional": bool(raw.get("optional")),
        "produces_context_sheet": bool(raw.get("produces_context_sheet")),
        "verbatim": [f for f in (raw.get("verbatim") or []) if f in (raw.get("transmits") or [])],
        "output_field": raw.get("output_field") if raw.get("output_field") in (raw.get("transmits") or []) else None,
    }


def effective_pause(defn):
    """The step that produces the context sheet always waits for the human.

    Its pause may be `answers` (the questions go out with the sheet): the sheet is then
    validated by `answer`, and still correctable with `validate --context` before.
    """
    if defn["produces_context_sheet"] and defn["pause"] != "answers":
        return "validate"
    return defn["pause"]


# ---------------------------------------------------------------------------
# Skill resolution
# ---------------------------------------------------------------------------
def version_key(name):
    return tuple(int(p) if p.isdigit() else 0 for p in re.split(r"[.\-]", name))


def cache_skill_roots(plugin):
    """Claude Code plugin cache: highest version first."""
    base = Path.home() / ".claude" / "plugins" / "cache"
    found = base.glob(f"*/{plugin}/*/skills")
    return sorted(found, key=lambda p: version_key(p.parent.name), reverse=True)


def skill_search_roots(namespace):
    if namespace == "ix-skills":
        env = [Path(p) for p in os.environ.get("IX_SKILLS_PATH", "").split(os.pathsep) if p]
        return env + [ROOT.parent / "ix-skills" / "dist" / "skills"] + cache_skill_roots("ix-skills")
    if namespace == "ix-recipes":
        return [ROOT / "dist" / "skills"] + cache_skill_roots("ix-recipes")
    raise ParcoursError(f"espace de noms de skill inconnu : '{namespace}'")


def skill_version(fm, path):
    """(version, source) — best effort; `source` says where the number comes from."""
    if fm.get("version"):
        return str(fm["version"]), "frontmatter"
    skills_dir = path.parent.parent
    if skills_dir.name == "skills" and skills_dir.parent.name == "dist":
        source = skills_dir.parent.parent / "skills" / f"{path.parent.name}.md"
        if source.is_file():
            source_fm, _ = split_frontmatter(source.read_text(encoding="utf-8"))
            if source_fm.get("version"):
                return str(source_fm["version"]), "source file"
    for parent in path.parents:
        if re.fullmatch(r"\d+\.\d+\.\d+\S*", parent.name):
            return parent.name, "cache dir"
    return "unknown", "unknown"


def resolve_skill(ref):
    namespace, _, skill_id = ref.partition(":")
    if not skill_id:
        raise ParcoursError(f"skill '{ref}' : l'espace de noms est obligatoire (ex. ix-skills:cadrage)")
    roots = skill_search_roots(namespace)
    for root in roots:
        path = root / skill_id / "SKILL.md"
        if path.is_file():
            fm, body = split_frontmatter(path.read_text(encoding="utf-8"))
            text = body.strip()
            version, version_source = skill_version(fm, path)
            return {
                "ref": ref,
                "path": str(path),
                "version": version,
                "version_source": version_source,
                "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                "text": text,
                "references": path.parent / "references",
            }
    searched = ", ".join(str(r) for r in roots)
    raise ParcoursError(f"skill introuvable : {ref} (cherché dans : {searched})")


def skill_record(skill):
    """What state.json keeps of a skill: where it is, which text (sha256), which version."""
    return {k: skill[k] for k in ("ref", "path", "version", "version_source", "sha256")}


def resolve_recipe_skills(recipe):
    """Every skill of the recipe, or one error naming all the missing ones."""
    found, missing = {}, []
    for defn in recipe["steps"]:
        try:
            found[defn["id"]] = resolve_skill(defn["skill"])
        except ParcoursError as exc:
            missing.append(str(exc))
    if missing:
        raise ParcoursError("; ".join(missing))
    return found


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------
def parcours_path(args, slug=None):
    slug = slug or args.slug
    if not slug or "/" in slug or slug.startswith("."):
        raise ParcoursError(f"identifiant de parcours invalide : '{slug}'")
    directory = Path(args.parcours_dir) / slug
    if not (directory / "state.json").is_file():
        raise NotFound(f"parcours introuvable : {directory}")
    return directory


def load_state(directory):
    return json.loads((directory / "state.json").read_text(encoding="utf-8"))


def read_snapshot(directory):
    """(state, fingerprint) from one read of state.json.

    The fingerprint is sha256(state.json bytes + NUL + 00-context.md bytes, empty when the
    sheet does not exist): it changes whenever the state or the context sheet does.
    """
    directory = Path(directory)
    raw = (directory / "state.json").read_bytes()
    context = directory / "00-context.md"
    context_raw = context.read_bytes() if context.is_file() else b""
    return json.loads(raw.decode("utf-8")), hashlib.sha256(raw + b"\0" + context_raw).hexdigest()


def save_state(directory, state):
    write_atomic(directory / "state.json", json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def new_state(recipe, slug, engine, engine_steps, skills):
    return {
        "recipe": recipe["id"],
        "recipe_version": recipe["version"],
        "slug": slug,
        "created": now(),
        "status": "active",
        "engine": engine,
        "engine_steps": engine_steps,
        "context_sheet": None,
        "context_validated": False,
        "answers": None,
        "cost_usd": 0.0,
        "calls": {},
        "steps": [
            {"id": s["id"], "status": "pending", "transmits": list(s["transmits"]),
             "skill": skill_record(skills[s["id"]]), **({"optional": True} if s["optional"] else {})}
            for s in recipe["steps"]
        ],
        "pending": None,
    }


def slugify(text):
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", folded.lower()).strip("-")


def default_slug(recipe_id, input_text):
    words = re.findall(r"[a-z0-9]{3,}", slugify(input_text).replace("-", " "))
    slug = "-".join([recipe_id] + words[:3])
    return slug[:60].strip("-") or f"{recipe_id}-{datetime.now():%Y%m%d}"


def create_unique_dir(base, slug):
    """mkdir with a numeric suffix on collision (mkdir itself is the atomic test)."""
    n = 1
    while True:
        name = slug if n == 1 else f"{slug}-{n}"
        try:
            (base / name).mkdir()
            return base / name, name
        except FileExistsError:
            n += 1


def step_index(state, step_id):
    for i, step in enumerate(state["steps"]):
        if step["id"] == step_id:
            return i
    ids = ", ".join(s["id"] for s in state["steps"])
    raise ParcoursError(f"étape inconnue : '{step_id}' (étapes : {ids})")


def output_name(idx, step_id):
    return f"{idx + 1:02d}-{step_id}.md"


def recipe_drift(state, recipe):
    """Why the recipe no longer matches the parcours (steps or `transmits` changed), else None."""
    mine, theirs = [s["id"] for s in state["steps"]], [s["id"] for s in recipe["steps"]]
    if mine != theirs:
        return ("la recette a changé depuis la création du parcours : étapes "
                f"{', '.join(mine)} (parcours) au lieu de {', '.join(theirs)} (recette)")
    for step, defn in zip(state["steps"], recipe["steps"]):
        if "transmits" in step and list(step["transmits"]) != list(defn["transmits"]):
            return ("la recette a changé depuis la création du parcours : l'étape "
                    f"'{step['id']}' transmettait {', '.join(step['transmits'])} (parcours), "
                    f"elle transmet {', '.join(defn['transmits'])} (recette)")
    return None


def check_recipe_matches(state, recipe):
    problem = recipe_drift(state, recipe)
    if problem:
        raise ParcoursError(problem)
    if state["recipe_version"] != recipe["version"]:
        warn(f"recette en version {recipe['version']}, parcours créé avec {state['recipe_version']}")


def refresh_pending(state):
    """Set `pending` for a choice before optional steps, or close the parcours."""
    if state["status"] != "active":
        state["pending"] = None
        return
    if state["pending"] and state["pending"]["type"] in ("validate", "answers"):
        return
    state["pending"] = None
    steps = state["steps"]
    nxt = next((i for i, s in enumerate(steps) if s["status"] == "pending"), None)
    if nxt is None:
        if all(s["status"] in ("done", "skipped") for s in steps):
            state["status"] = "completed"
        return
    if steps[nxt].get("optional") and not steps[nxt].get("chosen"):
        group = optional_group(state, nxt)
        state["pending"] = {
            "type": "choose",
            "steps": group,
            "message": f"Étapes optionnelles : {', '.join(group)}. "
                       f"`choose --run <étapes>` ou `choose --skip`.",
        }


def optional_group(state, start):
    group = []
    for step in state["steps"][start:]:
        if step["status"] == "pending" and step.get("optional") and not step.get("chosen"):
            group.append(step["id"])
        else:
            break
    return group


def total_calls(state):
    return ", ".join(f"{e} ×{n}" for e, n in sorted(state["calls"].items())) or "aucun"


# ---------------------------------------------------------------------------
# Building the message of a step
# ---------------------------------------------------------------------------
def input_value(directory, state, idx, source):
    """Text of one `receives` source for step `idx`."""
    if source == "brief":
        if idx != 0:
            raise ParcoursError("seule la première étape reçoit la demande brute")
        return (directory / "input.md").read_text(encoding="utf-8")
    if source == "answers":
        if not state.get("answers"):
            raise MissingInput("answers : pas encore de réponses")
        return (directory / state["answers"]).read_text(encoding="utf-8")
    step_id, _, field = source.partition(".")
    if not field:
        raise ParcoursError(f"source inconnue : '{source}'")
    step = state["steps"][step_index(state, step_id)]
    if step["status"] == "skipped":
        return SKIPPED
    handoff = step.get("handoff") or {}
    if step["status"] not in ("done", "paused") or field not in handoff:
        raise MissingInput(f"{source} : pas encore produit")
    return handoff[field]


def collect_inputs(directory, state, defn, idx, lenient=False):
    """[(name, text)] for the `receives` fields (context sheet apart) and rerun extras."""
    step = state["steps"][idx]
    inputs, unknown = [], 0
    for source in defn["receives"]:
        if source == "context_sheet":
            continue
        try:
            inputs.append((source, input_value(directory, state, idx, source)))
        except MissingInput:
            if not lenient:
                raise
            unknown += 1
    inputs += list((step.get("extra_inputs") or {}).items())
    return inputs, unknown


def render_context_sheet(state):
    return json.dumps(state["context_sheet"], indent=2, ensure_ascii=False)


def output_instructions(defn, idx, context_fields, definitions=None):
    lines = [
        "Write your complete output first. Then end with exactly these blocks, nothing after them:",
        "",
        "## HANDOFF",
    ]
    lines += [f"### {field}\n(content for this field)\n" for field in defn["transmits"] if field != defn.get("output_field")]
    if defn.get("output_field"):
        lines += [f"(Your complete output above is passed on as `{defn['output_field']}`: do not repeat it in the HANDOFF.)\n"]
    lines += [
        "Optional, only if a later step cannot do its job with what you transmit: add a "
        "`### blocking` sub-section to the HANDOFF saying what blocks. Reservations and caveats "
        "go in your output, not there. Omit the sub-section otherwise.\n",
        "## SUMMARY", "(5 lines at most)",
    ]
    if idx == 0 and defn["produces_context_sheet"]:
        lines += [
            "",
            "Before the HANDOFF block, add a `## CONTEXT SHEET` block: one ```json code block "
            f"with the keys {', '.join(context_fields)}. Facts from the request only, "
            f"`{NOT_STATED}` when absent.",
        ]
        known = [(f, (definitions or {}).get(f)) for f in context_fields]
        if any(d for _, d in known):
            lines += ["What each key holds:"] + [f"- `{f}`: {d}" for f, d in known if d]
    return "\n".join(lines)


def references_note(skill):
    """Tell the model where the skill's reference files are: copied, but useless if unannounced."""
    refs = skill.get("references")
    if not refs or not Path(refs).is_dir():
        return []
    names = sorted(p.name for p in Path(refs).iterdir() if p.is_file())
    if not names:
        return []
    return [
        "The skill's reference files are in ./references/, in your current working directory: "
        + ", ".join(names)
        + ". Read only those the skill text tells you to read, when it tells you to."
    ]


def input_block(name, text):
    return f"=== INPUT: {name} ===\n{text}\n=== END INPUT ==="


def build_message(skill, defn, idx, state, inputs, context_fields, definitions=None):
    parts = [
        "You are running ONE step of a recipe workflow. This message is all you know: "
        "you have no other context.",
        f"=== SKILL: {skill['ref']} ===\n{skill['text']}\n=== END SKILL ===",
        *references_note(skill),
        "The skill text is your method. Where its own output format and the HANDOFF below "
        "disagree, the HANDOFF wins: map your sections to its fields.",
        f"=== MISSION ===\n{defn['mission']}\n"
        "Stay strictly within the mission: do not produce the deliverables of later steps, "
        "do not answer the request yourself.\n=== END MISSION ===",
        "Write in the language of the material you receive (the context sheet and the inputs), "
        "not in the language of these instructions.",
    ]
    if idx > 0:
        parts.append(f"=== CONTEXT SHEET ===\n{render_context_sheet(state)}\n=== END CONTEXT SHEET ===")
    for name, text in inputs:
        parts.append(input_block(name, text))
    parts.append(f"=== OUTPUT FORMAT ===\n{output_instructions(defn, idx, context_fields, definitions)}\n=== END OUTPUT FORMAT ===")
    return "\n\n".join(parts) + "\n"


def build_retry_message(defn, idx, context_fields, produced, problem, definitions=None):
    """Retry message: the produced output only, never the input."""
    return (
        "Your previous output could not be read "
        f"({problem}). Reply with only the HANDOFF and SUMMARY blocks"
        + (" and the CONTEXT SHEET block" if idx == 0 and defn["produces_context_sheet"] else "")
        + ", in this format, nothing else:\n\n"
        + output_instructions(defn, idx, context_fields, definitions)
        + f"\n\n=== PREVIOUS OUTPUT ===\n{produced}\n=== END PREVIOUS OUTPUT ===\n"
    )


# ---------------------------------------------------------------------------
# Isolation check
# ---------------------------------------------------------------------------
def words_of(text):
    return re.findall(r"\w+", text.casefold())


def shingles(words, size):
    return {tuple(words[i:i + size]) for i in range(len(words) - size + 1)}


def find_leak(message, raw_input, admitted=""):
    """First fragment of the raw request found in `message`, or None.

    Compares runs of LEAK_WORDS consecutive words (case and punctuation
    ignored), so renaming or reformatting the file does not hide a leak.
    `admitted`: text already admitted as a verbatim extraction (an upstream
    `verbatim` field): its passages may be quoted again downstream.
    """
    source = words_of(raw_input)
    if len(source) < MIN_LEAK_WORDS:
        return None
    size = min(LEAK_WORDS, len(source))
    covered = admitted_positions(source, admitted)
    wanted = {tuple(source[i:i + size]) for i in range(len(source) - size + 1)
              if not covered.issuperset(range(i, i + size))}
    target = words_of(message)
    for i in range(len(target) - size + 1):
        if tuple(target[i:i + size]) in wanted:
            return " ".join(target[i:i + size])
    return None


def admitted_positions(source, admitted):
    """Positions of the request's words that an admitted verbatim extraction quotes.

    Short runs (VERBATIM_SHINGLE words) are enough: imposed items are often short lines,
    reformatted downstream into a list, so whole LEAK_WORDS runs rarely survive intact.
    """
    covered = set()
    if not admitted:
        return covered
    found = shingles(words_of(admitted), VERBATIM_SHINGLE)
    for i in range(len(source) - VERBATIM_SHINGLE + 1):
        if tuple(source[i:i + VERBATIM_SHINGLE]) in found:
            covered.update(range(i, i + VERBATIM_SHINGLE))
    return covered


def copied_share(text, raw_input):
    """Share of the raw request's words covered by runs of VERBATIM_SHINGLE words found in `text`."""
    source = words_of(raw_input)
    if len(source) < VERBATIM_SHINGLE:
        return 0.0
    found = shingles(words_of(text), VERBATIM_SHINGLE)
    covered = set()
    for i in range(len(source) - VERBATIM_SHINGLE + 1):
        if tuple(source[i:i + VERBATIM_SHINGLE]) in found:
            covered.update(range(i, i + VERBATIM_SHINGLE))
    return len(covered) / len(source)


def admitted_text(state, recipe, before):
    """Contents of the verbatim fields recorded by the done steps before `before`: material
    the recipe admitted on purpose (never the old value of the step being replaced)."""
    parts = []
    for defn, step in list(zip(recipe["steps"], state["steps"]))[:before]:
        if step.get("status") != "done":
            continue
        for field in defn.get("verbatim", ()):
            value = (step.get("handoff") or {}).get(field)
            if value:
                parts.append(value)
    return "\n".join(parts)


def verbatim_sources(recipe):
    """`<step>.<field>` names a recipe declares as verbatim extractions of the raw request."""
    return {f"{d['id']}.{f}" for d in recipe["steps"] for f in d.get("verbatim", [])}


def excerpt(fragment, words=12):
    """The beginning of a leaked fragment, enough to find it."""
    parts = fragment.split()
    return repr(" ".join(parts[:words]) + (" ..." if len(parts) > words else ""))


def read_raw_input(directory):
    return (directory / "input.md").read_text(encoding="utf-8")


def ensure_isolated(message, directory, idx, sources=(), verbatim=(), admitted=""):
    """From step 2 on, the message must not contain any passage of input.md.

    `sources` ([(name, text)]: the inputs and the context sheet) only serve to name
    the upstream field at fault and the remedy that works. Inputs named in `verbatim`
    are extractions the recipe asks to copy word for word: they were bounded when
    their step completed (copied_share) and are left out of the passage check here.
    """
    if idx == 0:
        return
    raw = read_raw_input(directory)
    for name, text in sources:
        if name in verbatim and text:
            message = message.replace(input_block(name, text), "")
    leak = find_leak(message, raw, admitted)
    if not leak:
        return
    for name, text in sources:
        if name in verbatim:
            continue
        if find_leak(text, raw, admitted):
            step_id = name.partition(".")[0]
            if name == "context_sheet":
                remedy = "Corrige la fiche (`validate --context`) ou relance la première étape (`rerun`)."
            elif name == "answers":
                remedy = ("Les réponses fournies reprennent la demande : rejoue l'étape qui les a "
                          "demandées (`rerun`) puis réponds à nouveau (`answer`) sans recopier la demande.")
            else:
                remedy = (f"Corrige le champ : `handoff {directory.name} {step_id} --file champs.md` "
                          f"(champs expurgés), ou `rerun {directory.name} {step_id}`.")
            raise LeakError(
                f"isolation : un passage de la demande brute figure dans '{name}' ({excerpt(leak)}). {remedy}")
    raise LeakError(f"isolation : un passage de la demande brute figure dans le message de l'étape ({excerpt(leak)}).")


def leak_in_parsed(raw, parsed, verbatim=(), admitted=""):
    """(where, fragment) of the first raw-request passage in the fields or the sheet, else None.

    A field the recipe declares `verbatim` is a list copied on purpose: each of its lines
    is checked on its own (a list item passes, a copied paragraph does not), and the
    whole field may not cover more than VERBATIM_MAX_SHARE of the request.
    """
    fields = dict(parsed["handoff"])
    if parsed.get("blocking"):
        fields["blocking"] = parsed["blocking"]
    for name, text in fields.items():
        if name in verbatim:
            for line in text.splitlines():
                leak = find_leak(line, raw)
                if leak:
                    return f"le champ '{name}' (extraction mot pour mot, mais une ligne recopie un paragraphe)", leak
            share = copied_share(text, raw)
            if share > VERBATIM_MAX_SHARE:
                return (f"le champ '{name}' (extraction mot pour mot, mais {share:.0%} de la demande, "
                        f"plafond {VERBATIM_MAX_SHARE:.0%})", " ".join(words_of(text)[:40]))
            continue
        leak = find_leak(text, raw, admitted)
        if leak:
            return f"le champ '{name}'", leak
    if parsed.get("context_sheet") is not None:
        leak = find_leak(json.dumps(parsed["context_sheet"], ensure_ascii=False), raw)
        if leak:
            return "la fiche de contexte", leak
    return None


def check_parsed_leak(directory, step_id, parsed, verbatim=(), admitted=""):
    """Refuse fields or a sheet that copy the raw request, naming the fragment and a working remedy."""
    found = leak_in_parsed(read_raw_input(directory), parsed, verbatim, admitted)
    if found:
        where, leak = found
        raise LeakError(
            f"isolation : un passage de la demande brute figure dans {where} de l'étape '{step_id}' "
            f"({excerpt(leak)}). Reformule-le : `handoff {directory.name} {step_id} --file champs.md` "
            f"(champs expurgés), ou `rerun {directory.name} {step_id}` pour refaire l'appel.")


def check_sheet_leak(directory, sheet):
    leak = find_leak(json.dumps(sheet, ensure_ascii=False), read_raw_input(directory))
    if leak:
        raise LeakError(
            f"isolation : un passage de la demande brute figure dans la fiche de contexte ({excerpt(leak)}). "
            f"Retire-le du fichier puis relance `validate {directory.name} --context fiche.json`.")


# ---------------------------------------------------------------------------
# Parsing an engine output
# ---------------------------------------------------------------------------
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})")
H2_RE = re.compile(r"^##[ \t]+(.+?)[ \t]*#*[ \t]*$")
H3_RE = re.compile(r"^###[ \t]+(.+?)[ \t]*#*[ \t]*$")
CONTEXT_FENCE_RE = re.compile(r"^ {0,3}(?:`{3,}|~{3,})[^\n]*\n(.*?)\n[ \t]*(?:`{3,}|~{3,})[ \t]*$", re.S | re.M)
SECTION_ENDERS = {"handoff": ("summary", "context_sheet")}
NO_BLOCKING = {"", "none", "n a", "na", "no", "nil", "aucun", "aucune", "rien", "neant", "ras"}


def fold_text(text):
    """Lower case without accents."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).casefold()


def normalize_name(name):
    """Field-name key: accents, case, spaces/underscores/hyphens, markdown decoration and a
    final plural mark do not matter (hypotheses = hypothesis, constraint = constraints)."""
    name = name.replace("`", "").replace("*", "").strip().rstrip(":")
    name = re.sub(r"[\s_\-]+", "_", fold_text(name)).strip("_")
    return re.sub(r"(?<=\w{3})(?:es|is|s|e)$", "", name)


NO_BLOCKING_OPENINGS = ("aucun blocage", "pas de blocage", "no blocking", "nothing blocks", "rien ne bloque")
NO_BLOCKING_MAX_WORDS = 8


def is_blocking(text):
    """A `### blocking` section only counts when it says something: not « none », nor a short
    « Aucun blocage pour la suite. ». Anything longer counts, even if it opens with « aucun
    blocage » (« … n'est levé tant que X manque »): a needless pause costs less than a missed block."""
    flat = re.sub(r"[\W_]+", " ", fold_text(text)).strip()
    if flat in NO_BLOCKING:
        return False
    return not (flat.startswith(NO_BLOCKING_OPENINGS) and len(flat.split()) <= NO_BLOCKING_MAX_WORDS)


def walk_fences(text, ignore=False):
    """Yield (line, inside_code_fence, fence_still_open_after_the_line)."""
    fence = None
    for line in text.splitlines():
        if ignore:
            yield line, False, False
            continue
        match = FENCE_RE.match(line)
        if fence is None:
            if match:
                fence = (match.group(1)[0], len(match.group(1)))
            yield line, bool(match), fence is not None
        else:
            closes = match and match.group(1)[0] == fence[0] and len(match.group(1)) >= fence[1]
            if closes and line.strip() == match.group(1).strip():
                fence = None
            yield line, True, fence is not None


def fenced_lines(text, ignore=False):
    """Yield (line, inside_code_fence)."""
    for line, in_fence, _ in walk_fences(text, ignore):
        yield line, in_fence


def has_unclosed_fence(text):
    opened = False
    for _, _, opened in walk_fences(text):
        pass
    return opened


def unwrap_fence(text):
    """The text inside a code fence that wraps the whole output (```markdown ... ```), else None."""
    lines = text.strip().splitlines()
    if len(lines) < 3:
        return None
    first, last = FENCE_RE.match(lines[0]), FENCE_RE.match(lines[-1])
    if not first or not last or first.group(1)[0] != last.group(1)[0] or lines[-1].strip() != last.group(1):
        return None
    return "\n".join(lines[1:-1])


def parse_sections(text, ignore_fences=False):
    """Last occurrence of ## HANDOFF, ## SUMMARY, ## CONTEXT SHEET -> [(line, in_fence)].

    HANDOFF only ends at SUMMARY or CONTEXT SHEET, so a value may hold its own
    `##` headings; the other sections end at any `##` heading.
    """
    sections, current = {}, None
    for line, in_fence in fenced_lines(text, ignore_fences):
        match = None if in_fence else H2_RE.match(line)
        if match:
            name = normalize_name(match.group(1))
            if name in ("handoff", "summary", "context_sheet"):
                sections[name] = []
                current = name
                continue
            if current != "handoff":
                current = None
                continue
        if current:
            sections[current].append((line, in_fence))
    return sections


def find_sections(text):
    """(sections, notes): like parse_sections, tolerant of a fence wrapping the whole output
    and of a fence left unclosed (last resort: fences ignored)."""
    candidates = [text]
    inner = unwrap_fence(text)
    if inner is not None:
        candidates.append(inner)
    for i, candidate in enumerate(candidates):
        sections = parse_sections(candidate)
        if "handoff" in sections and not has_unclosed_fence(candidate):
            return sections, ["sortie encadrée par un bloc de code, extraite telle quelle"] if i else []
    for candidate in candidates:
        sections = parse_sections(candidate, ignore_fences=True)
        if "handoff" in sections:
            return sections, ["bloc de code non fermé : extraction sans tenir compte des blocs de code"]
    return {}, []


def join_value(lines):
    text = "\n".join(lines)
    return re.sub(r"\A(?:[ \t]*\n)+", "", text).rstrip()


def parse_fields(section_lines):
    """`### field` sub-sections of the HANDOFF -> ({normalized name: text}, warnings, {name: as written})."""
    fields, labels, current, label, buffer, warnings = {}, {}, None, "", [], []

    def flush():
        if current is not None:
            if current in fields:
                warnings.append(f"champ '{label}' présent plusieurs fois, le dernier est retenu")
            fields[current] = join_value(buffer)
            labels[current] = label

    for line, in_fence in section_lines:
        match = None if in_fence else H3_RE.match(line)
        if match:
            flush()
            current, buffer = normalize_name(match.group(1)), []
            label = match.group(1).replace("`", "").replace("*", "").strip().rstrip(":")
        elif current is not None:
            buffer.append(line)
    flush()
    return fields, warnings, labels


def strip_json_noise(text):
    """Remove // and /* */ comments, then trailing commas, outside of strings."""
    def scan(source, handle):
        out, i, in_str = [], 0, False
        while i < len(source):
            c = source[i]
            if in_str:
                out.append(c)
                if c == "\\" and i + 1 < len(source):
                    i += 1
                    out.append(source[i])
                elif c == '"':
                    in_str = False
            elif c == '"':
                in_str = True
                out.append(c)
            else:
                i = handle(source, i, out)
            i += 1
        return "".join(out)

    def comments(source, i, out):
        if source.startswith("//", i):
            end = source.find("\n", i)
            return (end if end != -1 else len(source)) - 1
        if source.startswith("/*", i):
            end = source.find("*/", i + 2)
            return (end + 1) if end != -1 else len(source)
        out.append(source[i])
        return i

    def commas(source, i, out):
        if source[i] == ",":
            j = i + 1
            while j < len(source) and source[j].isspace():
                j += 1
            if j < len(source) and source[j] in "}]":
                return i
        out.append(source[i])
        return i

    return scan(scan(text, comments), commas)


def load_json_lenient(text):
    """json.loads; failing that, the text from the first { to the last }, comments and trailing commas removed."""
    try:
        return json.loads(text)
    except ValueError as strict:
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end <= start:
            raise strict
        return json.loads(strip_json_noise(text[start:end + 1]))


def parse_context_sheet(section_lines, context_fields):
    text = "\n".join(line for line, _ in section_lines)
    match = CONTEXT_FENCE_RE.search(text)
    bodies = ([match.group(1)] if match else []) + [text.strip()]
    sheet, error = None, None
    for body in bodies:
        try:
            sheet = load_json_lenient(body)
            break
        except ValueError as exc:
            error = error or exc
    else:
        raise ParseError(f"CONTEXT SHEET : JSON illisible ({error})")
    if not isinstance(sheet, dict):
        raise ParseError("CONTEXT SHEET : un objet JSON est attendu")
    warnings = []
    for field in context_fields:
        if field not in sheet:
            sheet[field] = NOT_STATED
            warnings.append(f"fiche de contexte : champ '{field}' absent, mis à '{NOT_STATED}'")
    return sheet, warnings


RETRY_MARKER = "<!-- retry output -->"


def output_body(text):
    """The step's output before its closing CONTEXT SHEET / HANDOFF blocks (fences respected,
    a fence wrapping the whole output removed, a short SUMMARY written before the HANDOFF left out)."""
    text = text.split(RETRY_MARKER)[0]  # a retry only re-sends the closing blocks
    inner = unwrap_fence(text)
    if inner is not None:
        text = inner
    lines, heads = text.splitlines(), {}
    for i, (line, in_fence, _) in enumerate(walk_fences(text)):
        match = None if in_fence else H2_RE.match(line)
        if match and normalize_name(match.group(1)) in ("handoff", "summary", "context_sheet"):
            heads[normalize_name(match.group(1))] = i  # last occurrence, as parse_sections
    cut = min([heads[n] for n in ("handoff", "context_sheet") if n in heads], default=len(lines))
    summary = heads.get("summary")
    if summary is not None and summary < cut and sum(1 for l in lines[summary + 1:cut] if l.strip()) <= 8:
        cut = summary
    return "\n".join(lines[:cut]).strip()


def parse_step_output(text, transmits, context_fields=None, output_field=None):
    """Parse an engine output; raise ParseError when a transmitted field is missing.

    `output_field`: the field that carries the step's whole output (a document such as an
    offer), taken from the text before the HANDOFF rather than copied into it.
    """
    sections, notes = find_sections(text)
    if "handoff" not in sections:
        raise ParseError("bloc '## HANDOFF' introuvable")
    fields, warnings, labels = parse_fields(sections["handoff"])
    warnings = notes + warnings
    declared = {normalize_name(f): f for f in transmits if f != output_field}
    given = fields.pop(normalize_name(output_field), "") if output_field else ""  # a hand-written `handoff --file`
    blocking = ""
    if "blocking" not in declared and "blocking" in fields:
        blocking = fields.pop("blocking")
        if not is_blocking(blocking):
            if blocking.strip():
                warnings.append(f"section blocking sans blocage, ignorée : {excerpt(blocking)}")
            blocking = ""
    missing = [declared[n] for n in declared if not fields.get(n)]
    if missing:
        raise ParseError(f"champ(s) manquant(s) ou vide(s) dans le HANDOFF : {', '.join(missing)}")
    warnings += [f"champ '{labels[n]}' en trop dans le HANDOFF, ignoré" for n in fields if n not in declared]
    handoff = {declared[n]: fields[n] for n in declared}
    if output_field:
        body = output_body(text) or given
        if not body:
            raise ParseError(f"sortie vide : le champ '{output_field}' reprend la sortie complète de l'étape")
        handoff[output_field] = body
    result = {
        "handoff": handoff,
        "blocking": blocking,
        "summary": join_value(l for l, _ in sections.get("summary", [])),
        "context_sheet": None,
        "warnings": warnings,
    }
    if not result["summary"]:
        result["warnings"].append("bloc '## SUMMARY' absent ou vide")
    if context_fields is not None:
        if "context_sheet" not in sections:
            raise ParseError("bloc '## CONTEXT SHEET' introuvable")
        result["context_sheet"], more = parse_context_sheet(sections["context_sheet"], context_fields)
        result["warnings"] += more
    return result


# ---------------------------------------------------------------------------
# Engines
# ---------------------------------------------------------------------------
def engine_argv(engine, model, work, out_file, budget):
    """Command line of an engine; the prompt goes through stdin, except for agy (see argv_prompt)."""
    if engine == "claude":
        argv = ["claude", "-p"]
        if model:
            argv += ["--model", model]
        return argv + [
            "--output-format", "json", "--tools", "Read", "--setting-sources", "",
            "--no-session-persistence", "--disable-slash-commands",
            "--max-budget-usd", f"{budget:g}",
        ]
    if engine == "codex":
        return ["codex", "exec", "-s", "read-only", "--skip-git-repo-check", "--ephemeral",
                "-C", str(work), "-o", str(out_file)]
    if engine == "agy":
        return ["agy", "--disable-slash-commands"]
    if engine == "vibe":
        return ["vibe", "-p", "--output", "text"]
    raise ParcoursError(f"moteur inconnu : '{engine}'")


def kill_group(proc):
    with contextlib.suppress(ProcessLookupError, PermissionError):
        os.killpg(proc.pid, signal.SIGKILL)


def run_process(argv, stdin_text, cwd, timeout):
    """Run `argv` in its own process group; kill the whole group on timeout."""
    try:
        proc = subprocess.Popen(
            argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=str(cwd), text=True, encoding="utf-8", errors="replace", start_new_session=True,
        )
    except FileNotFoundError:
        raise EngineError(f"commande introuvable : {argv[0]}")
    try:
        out, err = proc.communicate(stdin_text, timeout=timeout)
    except subprocess.TimeoutExpired:
        kill_group(proc)
        with contextlib.suppress(subprocess.TimeoutExpired):
            proc.communicate(timeout=5)
        raise EngineTimeout(f"délai dépassé ({timeout}s) : {argv[0]}")
    except BaseException:
        kill_group(proc)
        raise
    return proc.returncode, out, err


def claude_payload(stdout):
    """The `result` object of `claude -p --output-format json`, or None when stdout is not that."""
    try:
        data = json.loads(stdout)
    except (ValueError, TypeError):
        return None
    if isinstance(data, list):
        data = next((d for d in reversed(data) if isinstance(d, dict) and d.get("type") == "result"), {})
    return data if isinstance(data, dict) else None


def claude_cost(stdout):
    """total_cost_usd, whatever the outcome (an error or a non-zero exit still cost something)."""
    try:
        return float((claude_payload(stdout) or {}).get("total_cost_usd") or 0.0)
    except (TypeError, ValueError):
        return 0.0


def parse_claude_json(stdout):
    """(text, cost) from `claude -p --output-format json`."""
    data = claude_payload(stdout)
    if data is None:
        raise EngineError("claude : sortie standard qui n'est pas du JSON")
    cost = claude_cost(stdout)
    if data.get("is_error") or not data.get("result"):
        raise EngineError(f"claude : échec ({data.get('subtype') or 'sans résultat'})", cost=cost)
    return data["result"], cost


def copy_references(skill, work):
    refs = skill.get("references")
    if refs and Path(refs).is_dir():
        shutil.copytree(refs, work / "references")


def fake_engine(step_id, kind, message):
    fixtures = os.environ.get("PARCOURS_FAKE_DIR")
    if not fixtures:
        raise EngineError("moteur fake : PARCOURS_FAKE_DIR n'est pas défini")
    fixtures = Path(fixtures)
    suffix = ".retry.md" if kind == "retry" else ".md"
    received = fixtures / "received"
    received.mkdir(exist_ok=True)
    (received / f"{step_id}{suffix}").write_text(message, encoding="utf-8")
    canned = fixtures / f"{step_id}{suffix}"
    if not canned.is_file():
        raise EngineError(f"moteur fake : {canned} n'existe pas")
    return canned.read_text(encoding="utf-8"), 0.0


def call_engine(engine, message, *, model, timeout, budget, skill, step_id, kind):
    """One engine call in a throwaway folder holding only the skill's references/."""
    if engine == "fake":
        return fake_engine(step_id, kind, message)
    tmp = Path(tempfile.mkdtemp(prefix="parcours-"))
    try:
        work, out_file = tmp / "work", tmp / "last-message.txt"
        work.mkdir()
        copy_references(skill, work)
        argv = engine_argv(engine, model, work, out_file, budget)
        stdin_text = message
        if engine == "agy":
            # agy reads no text prompt on stdin: `-p -` is taken literally, a bare -p prints help.
            size = len(message.encode("utf-8"))
            if size > ARGV_PROMPT_LIMIT:
                raise EngineError(f"message trop long pour agy ({size} octets, limite {ARGV_PROMPT_LIMIT})")
            argv, stdin_text = argv + [f"-p={message}"], ""
        code, stdout, stderr = run_process(argv, stdin_text, work, timeout)
        if code != 0:
            cost = claude_cost(stdout) if engine == "claude" else 0.0
            raise EngineError(f"{engine} a échoué (code {code}) : {(stderr or '').strip()[-300:]}", cost=cost)
        return read_engine_output(engine, stdout, out_file)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def read_engine_output(engine, stdout, out_file):
    """Only stdout or the engine's output file are parsed, never stderr."""
    if engine == "claude":
        return parse_claude_json(stdout)
    text = out_file.read_text(encoding="utf-8") if engine == "codex" and out_file.is_file() else stdout
    if not (text or "").strip():
        raise EngineError(f"{engine} : sortie vide")
    return text, 0.0


# ---------------------------------------------------------------------------
# Running a step
# ---------------------------------------------------------------------------
def engine_for(state, step_id):
    return state["engine_steps"].get(step_id, state["engine"])


def invoke(directory, state, step, engine, message, opts, kind, skill, model):
    """Engine call with its accounting (call count, cost), saved as soon as the call returns."""
    state["calls"][engine] = state["calls"].get(engine, 0) + 1
    text, cost = None, 0.0
    try:
        text, cost = call_engine(
            engine, message, model=model, timeout=opts.timeout, budget=opts.max_budget_usd,
            skill=skill, step_id=step["id"], kind=kind,
        )
    except EngineError as exc:
        cost = exc.cost  # a failed claude call still reports what it cost
        raise
    finally:
        state["cost_usd"] = round(state["cost_usd"] + cost, 6)
        step["cost_usd"] = round(step.get("cost_usd", 0.0) + cost, 6)
        save_state(directory, state)
    return text


def trace_name(idx, step_id, kind):
    return f"{idx + 1:02d}-{step_id}{'.retry' if kind == 'retry' else ''}.in.md"


def write_trace(directory, idx, step_id, kind, message):
    """Keep the exact message sent to the engine (an older trace is kept as .vN)."""
    path = directory / trace_name(idx, step_id, kind)
    if path.exists():
        path.rename(versioned_name(path))
    write_atomic(path, message)


def reuse_existing_output(out_path, defn, retried, context_fields):
    """An output already on disk (crash between the file and state.json): parse it, no engine call.

    Unusable, or not left by a crashed attempt: it is set aside as NN-<step>.vN.md.
    """
    if not out_path.is_file():
        return None
    if retried:
        try:
            parsed = parse_step_output(out_path.read_text(encoding="utf-8"), defn["transmits"], context_fields, defn.get("output_field"))
            warn(f"étape '{defn['id']}' : sortie déjà présente ({out_path.name}), reprise sans nouvel appel")
            return parsed
        except (ParseError, UnicodeDecodeError):
            pass
    out_path.rename(versioned_name(out_path))
    return None


def produce_output(directory, state, recipe, idx, skill, message, opts, retried=False):
    """First call, then at most one retry on the produced output only."""
    defn, step = recipe["steps"][idx], state["steps"][idx]
    engine, model = engine_for(state, defn["id"]), defn["model"]
    context_fields = recipe["context_sheet"] if defn["produces_context_sheet"] else None
    out_path = directory / output_name(idx, defn["id"])

    existing = reuse_existing_output(out_path, defn, retried, context_fields)
    if existing:
        return existing
    write_trace(directory, idx, defn["id"], "main", message)
    text = invoke(directory, state, step, engine, message, opts, "main", skill, model)
    write_atomic(out_path, text)
    try:
        return parse_step_output(text, defn["transmits"], context_fields, defn.get("output_field"))
    except ParseError as first:
        retry = build_retry_message(defn, idx, recipe["context_sheet"], text, first,
                                    recipe.get("context_definitions"))
        ensure_isolated(retry, directory, idx, admitted=admitted_text(state, recipe, idx))
        warn(f"étape '{defn['id']}' : {first} ; une relance sur la sortie produite")
        write_trace(directory, idx, defn["id"], "retry", retry)
        retry_text = invoke(directory, state, step, engine, retry, opts, "retry", skill, model)
        write_atomic(out_path, f"{text}\n\n{RETRY_MARKER}\n{retry_text}\n")
        if defn.get("output_field"):
            retry_text = f"{output_body(text)}\n\n{retry_text}"  # the document comes from the first answer
        try:
            return parse_step_output(retry_text, defn["transmits"], context_fields, defn.get("output_field"))
        except ParseError as second:
            raise ParseError(f"extraction impossible après relance : {second}")


def pause_message(defn, idx, blocking=""):
    out = output_name(idx, defn["id"])
    if defn["produces_context_sheet"] and effective_pause(defn) == "answers":
        message = (f"Fiche de contexte (00-context.md) et questions à envoyer dans {out}. "
                   "Corriger la fiche si besoin (`validate --context`), puis coller les réponses "
                   "(`answer --file`) ou `answer --none` : cela valide aussi la fiche.")
    elif defn["produces_context_sheet"]:
        message = f"Valider la fiche de contexte (00-context.md) et {out}."
    elif effective_pause(defn) == "answers":
        message = f"Questions à envoyer dans {out}. Coller les réponses (`answer --file`) ou `answer --none`."
    else:
        message = f"Valider {out}."
    if blocking:
        text = " ".join(blocking.split())
        message = (f"Blocage signalé par l'étape '{defn['id']}' : {text} — {message} "
                   "Ou `validate --stop` pour arrêter.")
    return message


def complete_step(directory, state, recipe, idx, parsed, keep_status=None, check=True):
    """Record a successful extraction and open the pause the recipe asks for.

    The fields and the context sheet are checked against the raw request first (nothing is
    recorded if they copy it). `keep_status="done"|"paused"`: a correction made by hand on a
    step already past its output keeps that status (and, for "done", the pending pause).
    """
    defn, step = recipe["steps"][idx], state["steps"][idx]
    if check:
        check_parsed_leak(directory, defn["id"], parsed, defn.get("verbatim", ()),
                          admitted_text(state, recipe, idx))
    pause = effective_pause(defn)
    blocking = parsed.get("blocking") or ""
    if blocking and pause == "none":
        pause = "validate"  # a blocking signal always waits for the human
    status = keep_status or ("paused" if pause in ("validate", "answers") else "done")
    step.update(
        status=status,
        output=output_name(idx, defn["id"]),
        handoff=parsed["handoff"],
        summary=parsed["summary"],
        ended=now(),
    )
    step.pop("error", None)
    step.pop("blocking", None)
    if blocking:
        step["blocking"] = blocking
    if parsed["context_sheet"] is not None:
        state["context_sheet"] = parsed["context_sheet"]
        state["context_validated"] = keep_status == "done"
        write_context_file(directory, state)
    if keep_status != "done":
        state["pending"] = None
        if status == "paused":
            state["pending"] = {"type": pause, "step": defn["id"], "message": pause_message(defn, idx, blocking)}
    for message in parsed["warnings"]:
        warn(f"étape '{defn['id']}' : {message}")


def write_context_file(directory, state):
    path = directory / "00-context.md"
    if path.exists():
        shutil.copyfile(path, versioned_name(path))
    body = "# Context sheet\n\n```json\n" + render_context_sheet(state) + "\n```\n"
    write_atomic(path, body)


def execute_step(directory, state, recipe, idx, opts):
    defn, step = recipe["steps"][idx], state["steps"][idx]
    if idx > 0 and not state["context_validated"]:
        raise ParcoursError("la fiche de contexte n'est pas validée (`validate`)")
    skill = resolve_skill(defn["skill"])
    inputs, _ = collect_inputs(directory, state, defn, idx)
    message = build_message(skill, defn, idx, state, inputs, recipe["context_sheet"],
                            recipe.get("context_definitions"))
    ensure_isolated(message, directory, idx,
                    inputs + [("context_sheet", render_context_sheet(state))] if idx else (),
                    verbatim_sources(recipe), admitted_text(state, recipe, idx))

    retried = bool(step.pop("retried", False))
    step.update(
        status="running", engine=engine_for(state, defn["id"]), model=defn["model"],
        skill=skill_record(skill), started=now(),
    )
    step.setdefault("cost_usd", 0.0)
    step.pop("ended", None)
    save_state(directory, state)
    try:
        parsed = produce_output(directory, state, recipe, idx, skill, message, opts, retried)
        complete_step(directory, state, recipe, idx, parsed)
    except ParcoursError as exc:
        step.update(status="failed", error=str(exc), ended=now())
        save_state(directory, state)
        raise
    except Exception as exc:  # never leave the step 'running' on a bug or an I/O error
        reason = " ".join(f"erreur inattendue : {type(exc).__name__}: {exc}".split())
        step.update(status="failed", error=reason, ended=now())
        with contextlib.suppress(OSError):
            save_state(directory, state)
        raise ParcoursError(f"étape '{defn['id']}' : {reason}") from exc
    refresh_pending(state)
    save_state(directory, state)
    say(f"  {defn['id']} : terminé ({step['output']}, coût ${step['cost_usd']:.4f})")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------
def parse_engine_steps(pairs, recipe):
    result = {}
    ids = {s["id"] for s in recipe["steps"]}
    for pair in pairs or []:
        step_id, _, engine = pair.partition("=")
        if step_id not in ids:
            raise ParcoursError(f"--engine-step : étape inconnue '{step_id}'")
        if engine not in ENGINES:
            raise ParcoursError(f"--engine-step : moteur inconnu '{engine}'")
        result[step_id] = engine
    return result


def read_text_arg(path):
    text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    if not text.strip():
        raise ParcoursError(f"fichier vide : {path}")
    return text


def cmd_new(args):
    recipe = load_recipe(args.recipe)
    text = read_text_arg(args.input)
    engine_steps = parse_engine_steps(args.engine_step, recipe)
    skills = resolve_recipe_skills(recipe)  # fail early, naming every missing skill
    base = Path(args.parcours_dir)
    base.mkdir(parents=True, exist_ok=True)
    wanted = slugify(args.slug) if args.slug else default_slug(recipe["id"], text)
    directory, slug = create_unique_dir(base, wanted)
    write_atomic(directory / "input.md", text)
    save_state(directory, new_state(recipe, slug, args.engine or "claude", engine_steps, skills))
    say(f"Parcours créé : {slug} ({directory})")
    say(f"Suite : parcours.py next {slug}")
    return 0


def apply_engine_overrides(state, args, recipe):
    if args.engine:
        state["engine"] = args.engine
    state["engine_steps"].update(parse_engine_steps(args.engine_step, recipe))


def guard_steps(state):
    """Refuse to go on over an interrupted or failed step."""
    for step in state["steps"]:
        if step["status"] == "running":
            raise ParcoursError(
                f"l'étape '{step['id']}' est restée 'running' (arrêt brutal ?) : `retry` pour la reprendre")
        if step["status"] == "failed":
            raise ParcoursError(
                f"l'étape '{step['id']}' a échoué ({step.get('error', '?')}) : "
                f"`retry`, `rerun {state['slug']} {step['id']}` (nouvel appel), "
                f"ou `handoff {state['slug']} {step['id']} --file champs.md`")


def plan_steps(state, recipe):
    """Indices of the steps the next run would play, up to the next pause."""
    plan = []
    for idx, step in enumerate(state["steps"]):
        if step["status"] != "pending":
            continue
        if step.get("optional") and not step.get("chosen"):
            break
        plan.append(idx)
        if effective_pause(recipe["steps"][idx]) in ("validate", "answers"):
            break
    return plan


def plan_rows(directory, state, recipe, plan):
    """For each step of the plan: engine, model and size of the message it would be sent."""
    rows = []
    for idx in plan:
        defn = recipe["steps"][idx]
        skill = resolve_skill(defn["skill"])
        inputs, unknown = collect_inputs(directory, state, defn, idx, lenient=True)
        message = build_message(skill, defn, idx, state, inputs, recipe["context_sheet"],
                            recipe.get("context_definitions"))
        rows.append({
            "index": idx + 1, "id": defn["id"], "skill": defn["skill"],
            "engine": engine_for(state, defn["id"]), "model": defn["model"],
            "chars": len(message), "bytes": len(message.encode("utf-8")),
            "unknown_fields": unknown, "pause": effective_pause(defn),
        })
    return rows


def print_plan(directory, state, recipe, plan):
    if not plan:
        say("Rien à jouer.")
        return
    say(f"Plan : {len(plan)} étape(s) jusqu'à la prochaine pause")
    per_engine = {}
    for row in plan_rows(directory, state, recipe, plan):
        per_engine[row["engine"]] = per_engine.get(row["engine"], 0) + 1
        more = f" + {row['unknown_fields']} champ(s) à venir" if row["unknown_fields"] else ""
        say(f"  {row['index']}. {row['id']} — moteur {row['engine']}, modèle {row['model'] or 'défaut'}, "
            f"entrée ≈ {row['chars']} caractères{more}")
    say("Appels : " + ", ".join(f"{e} ×{n}" for e, n in per_engine.items()))


def confirm(prompt):
    try:
        return input(prompt).strip().lower() in ("y", "yes", "o", "oui")
    except EOFError:
        return False


def describe_pending(directory, state):
    pending = state["pending"]
    say(f"En attente ({pending['type']}) : {pending['message']}")
    if pending["type"] in ("validate", "answers"):
        step = state["steps"][step_index(state, pending["step"])]
        if step.get("summary"):
            say(f"Résumé :\n{step['summary']}")
        if state["context_sheet"] is not None and not state["context_validated"]:
            say(f"Fiche de contexte :\n{render_context_sheet(state)}")


def skill_changes(state, recipe):
    """Messages for the skills still to play whose text changed since it was recorded."""
    messages = []
    for step, defn in zip(state["steps"], recipe["steps"]):
        recorded = (step.get("skill") or {}).get("sha256")
        if step["status"] not in ("pending", "failed", "running") or not recorded:
            continue
        try:
            current = resolve_skill(defn["skill"])["sha256"]
        except ParcoursError:
            continue  # reported by the plan, with the folders searched
        if current != recorded:
            messages.append(f"le skill '{defn['skill']}' (étape '{defn['id']}') a changé depuis la création "
                            f"du parcours (sha256 {recorded[:12]} → {current[:12]}) ; la version actuelle sera envoyée")
    return messages


def warn_skill_changes(state, recipe):
    """Warn (nothing more) when the text of a skill still to play changed since it was recorded."""
    for message in skill_changes(state, recipe):
        warn(message)


def cmd_next(args):
    directory = parcours_path(args)
    with parcours_lock(directory):
        state, fingerprint = read_snapshot(directory)
        if args.if_state and args.if_state.lower() != fingerprint:
            # checked under the lock, before anything is written: the plan that was confirmed is stale
            raise StateChanged("l'état du parcours a changé depuis le plan affiché : rien n'a été lancé, relire le plan")
        if state["status"] != "active":
            say(f"Parcours {state['status']}.")
            return 0
        recipe = load_recipe(state["recipe"])
        check_recipe_matches(state, recipe)
        apply_engine_overrides(state, args, recipe)
        guard_steps(state)
        refresh_pending(state)
        save_state(directory, state)
        if state["status"] != "active":
            say(f"Parcours {state['status']}.")
            return 0
        if state["pending"]:
            describe_pending(directory, state)
            return 0
        warn_skill_changes(state, recipe)
        print_plan(directory, state, recipe, plan_steps(state, recipe))
        if not args.yes and not confirm("Lancer ? [y/N] "):
            say("Annulé.")
            return 1
        with terminate_as_exit():
            return run_until_pause(directory, state, recipe, args)


def announce_end(state):
    """Say where the final output is once the parcours is completed."""
    if state["status"] == "completed":
        last = next((s for s in reversed(state["steps"]) if s["status"] == "done"), None)
        if last:
            say(f"Parcours terminé. Sortie finale : {last['output']}")


def run_until_pause(directory, state, recipe, opts):
    while state["status"] == "active" and not state["pending"]:
        plan = plan_steps(state, recipe)
        if not plan:
            break
        execute_step(directory, state, recipe, plan[0], opts)
    save_state(directory, state)
    if state["status"] == "completed":
        announce_end(state)
    elif state["pending"]:
        describe_pending(directory, state)
    return 0


def emit_json(data):
    """One line of ASCII JSON on stdout (no dependency on the terminal encoding)."""
    print(json.dumps(data))


def listed_files(directory):
    """Names of the regular files of a parcours folder, without hidden and temporary ones."""
    return sorted(p.name for p in Path(directory).iterdir()
                  if p.is_file() and not p.name.startswith(".") and not p.name.endswith(".tmp"))


def status_report(directory, state, fingerprint):
    """Everything a page needs to show a parcours, in one object (`status --json`)."""
    recipe, problem = None, None
    try:
        recipe = load_recipe(state["recipe"])
        problem = recipe_drift(state, recipe)
    except ParcoursError as exc:
        problem = str(exc)
    defns = {d["id"]: d for d in recipe["steps"]} if recipe else {}
    files = listed_files(directory)
    steps = []
    for idx, step in enumerate(state["steps"]):
        defn = defns.get(step["id"])
        item = {
            "index": idx + 1, "id": step["id"], "status": step["status"],
            "optional": bool(step.get("optional")), "chosen": bool(step.get("chosen")),
            "engine": step.get("engine") or engine_for(state, step["id"]),
            "model": step["model"] if "model" in step else (defn["model"] if defn else None),
            "pause": effective_pause(defn) if defn else None,
            "produces_context_sheet": bool(defn and defn["produces_context_sheet"]),
            "transmits": list(step.get("transmits") or (defn["transmits"] if defn else [])),
            "output": step.get("output"), "summary": step.get("summary"), "handoff": step.get("handoff"),
            "blocking": step.get("blocking"), "error": step.get("error"),
            "cost_usd": step.get("cost_usd", 0.0), "started": step.get("started"), "ended": step.get("ended"),
            "skill": {k: (step.get("skill") or {}).get(k) for k in ("ref", "version")},
        }
        for key, kind in (("trace", "main"), ("retry_trace", "retry")):
            name = trace_name(idx, step["id"], kind)
            item[key] = name if name in files else None
        steps.append(item)
    final = None
    if state["status"] == "completed":
        last = next((s for s in reversed(state["steps"]) if s["status"] == "done"), None)
        final = last["output"] if last else None
    return {
        "slug": state["slug"], "recipe": state["recipe"], "recipe_version": state["recipe_version"],
        "created": state.get("created"), "status": state["status"],
        "engine": state["engine"], "engine_steps": state["engine_steps"],
        "cost_usd": state["cost_usd"], "calls": state["calls"],
        "context_sheet": state["context_sheet"], "context_validated": state["context_validated"],
        "context_fields": list(recipe["context_sheet"]) if recipe else [],
        "answers": state.get("answers"), "pending": state["pending"], "steps": steps,
        "files": files, "final_output": final, "recipe_error": problem,
        "locked": is_locked(directory), "fingerprint": fingerprint,
        "updated": datetime.fromtimestamp((Path(directory) / "state.json").stat().st_mtime).isoformat(timespec="seconds"),
    }


def cmd_status(args):
    directory = parcours_path(args)
    state, fingerprint = read_snapshot(directory)
    if args.json:
        emit_json(status_report(directory, state, fingerprint))
        return 0
    say(f"Parcours {state['slug']} — recette {state['recipe']} {state['recipe_version']} — {state['status']}")
    say(f"Moteur : {state['engine']}" + "".join(f", {k}={v}" for k, v in state["engine_steps"].items()))
    say(f"Coût cumulé : ${state['cost_usd']:.4f} — appels : {total_calls(state)}")
    say(f"Fiche de contexte : {'validée' if state['context_validated'] else 'non validée'}")
    for i, step in enumerate(state["steps"]):
        extra = f" ({step['output']})" if step.get("output") else ""
        say(f"  {i + 1}. {step['id']} : {step['status']}{extra}")
    if state["pending"]:
        say(f"En attente ({state['pending']['type']}) : {state['pending']['message']}")
    return 0


def cmd_plan(args):
    """What `next` would play, without writing anything (no lock, no state change).

    Engine overrides (--engine, --engine-step) apply to the plan only, in memory.
    """
    directory = parcours_path(args)
    state, fingerprint = read_snapshot(directory)
    original_engine = state["engine"]
    report = {
        "slug": state["slug"], "fingerprint": fingerprint, "locked": is_locked(directory),
        "status": state["status"], "engine": state["engine"], "engine_steps": state["engine_steps"],
        "changes_default_engine": False, "runnable": False, "reason": None, "message": "",
        "pending": None, "steps": [], "calls": {}, "claude_steps": 0,
        "max_budget_usd": args.max_budget_usd, "ceiling_usd": 0.0, "subscription_calls": 0,
        "agy_argv_warning": False, "agy_over_limit": False, "warnings": [],
    }

    def finish(reason, message):
        report.update(reason=reason, message=message)
        if args.json:
            emit_json(report)
        else:
            say(message)
        return 0

    if state["status"] != "active":
        return finish(state["status"], f"Parcours {state['status']}.")
    recipe = load_recipe(state["recipe"])
    check_recipe_matches(state, recipe)
    apply_engine_overrides(state, args, recipe)
    report.update(engine=state["engine"], engine_steps=state["engine_steps"],
                  changes_default_engine=state["engine"] != original_engine)
    try:
        guard_steps(state)
    except ParcoursError as exc:
        stuck = next(s for s in state["steps"] if s["status"] in ("running", "failed"))
        return finish(stuck["status"], str(exc))
    refresh_pending(state)
    if state["status"] != "active":
        return finish(state["status"], f"Parcours {state['status']}.")
    if state["pending"]:
        report["pending"] = state["pending"]
        return finish("pending", f"En attente ({state['pending']['type']}) : {state['pending']['message']}")
    plan = plan_steps(state, recipe)
    if not plan:
        return finish("nothing", "Rien à jouer.")
    rows = plan_rows(directory, state, recipe, plan)
    calls = {}
    for row in rows:
        calls[row["engine"]] = calls.get(row["engine"], 0) + 1
    claude_steps = calls.get("claude", 0)
    report.update(
        runnable=True, steps=rows, calls=calls, claude_steps=claude_steps,
        # one claude call per step, plus the single retry on a failed extraction
        ceiling_usd=round(claude_steps * args.max_budget_usd * 2, 6),
        subscription_calls=sum(n for e, n in calls.items() if e not in ("claude", "fake")),
        agy_argv_warning=any(r["engine"] == "agy" for r in rows),
        agy_over_limit=any(r["engine"] == "agy" and r["bytes"] > ARGV_PROMPT_LIMIT for r in rows),
        warnings=skill_changes(state, recipe),
    )
    if args.json:
        emit_json(report)
    else:
        print_plan(directory, state, recipe, plan)
    return 0


def require_pending(state, kind):
    pending = state["pending"]
    if state["status"] != "active" or not pending or pending["type"] != kind:
        got = f"'{pending['type']}'" if pending else "rien"
        raise ParcoursError(f"cette commande attend une pause '{kind}' ; en attente : {got}")
    return pending


def close_pause(directory, state, pending):
    step = state["steps"][step_index(state, pending["step"])]
    step["status"] = "done"
    state["pending"] = None
    refresh_pending(state)
    save_state(directory, state)


def sheet_answers_pause(state, recipe, pending):
    """True at the `answers` pause of the step that produces the context sheet."""
    return bool(
        state["status"] == "active" and pending and pending["type"] == "answers"
        and recipe["steps"][step_index(state, pending["step"])]["produces_context_sheet"]
    )


def cmd_validate(args):
    directory = parcours_path(args)
    with parcours_lock(directory):
        state = load_state(directory)
        recipe = load_recipe(state["recipe"])
        check_recipe_matches(state, recipe)
        if args.stop and args.context:
            raise ParcoursError("--stop et --context ne se combinent pas")
        if args.context and sheet_answers_pause(state, recipe, state["pending"]):
            replace_context(directory, state, recipe, args.context)
            save_state(directory, state)
            say("Fiche de contexte corrigée. Suite : answer (valide aussi la fiche)")
            return 0
        pending = require_pending(state, "validate")
        idx = step_index(state, pending["step"])
        if args.context:
            replace_context(directory, state, recipe, args.context)
            if idx > 0:
                say("Fiche corrigée : les étapes déjà jouées ont reçu l'ancienne ; `rerun` pour les refaire.")
        if recipe["steps"][idx]["produces_context_sheet"]:
            state["context_validated"] = True
        if args.stop:
            state["status"] = "stopped"
            say("Parcours arrêté (No-go).")
        close_pause(directory, state, pending)
        if state["status"] == "active":
            say("Validé. Suite : next")
        announce_end(state)
        return 0


def replace_context(directory, state, recipe, path):
    try:
        sheet = load_json_lenient(Path(path).read_text(encoding="utf-8"))
    except ValueError as exc:
        raise ParcoursError(f"fiche de contexte : JSON illisible ({exc})")
    if not isinstance(sheet, dict):
        raise ParcoursError("fiche de contexte : un objet JSON est attendu")
    check_sheet_leak(directory, sheet)
    for field in recipe["context_sheet"]:
        if field not in sheet:
            warn(f"fiche de contexte : champ '{field}' absent")
    state["context_sheet"] = sheet
    write_context_file(directory, state)


def cmd_answer(args):
    directory = parcours_path(args)
    with parcours_lock(directory):
        state = load_state(directory)
        recipe = load_recipe(state["recipe"])
        check_recipe_matches(state, recipe)
        pending = require_pending(state, "answers")
        text = NO_ANSWERS if args.none else read_text_arg(args.file)
        write_atomic(directory / "answers.md", text.rstrip("\n") + "\n")
        state["answers"] = "answers.md"
        if recipe["steps"][step_index(state, pending["step"])]["produces_context_sheet"]:
            state["context_validated"] = True
        close_pause(directory, state, pending)
        say("Réponses enregistrées. Suite : next" if not args.none else "Sans réponses. Suite : next")
        announce_end(state)
        return 0


def cmd_choose(args):
    directory = parcours_path(args)
    with parcours_lock(directory):
        state = load_state(directory)
        recipe = load_recipe(state["recipe"])
        check_recipe_matches(state, recipe)
        pending = require_pending(state, "choose")
        group = pending["steps"]
        wanted = [] if args.skip else [s.strip() for s in args.run.split(",") if s.strip()]
        unknown = [s for s in wanted if s not in group]
        if unknown:
            raise ParcoursError(f"étape(s) hors embranchement : {', '.join(unknown)} (choix : {', '.join(group)})")
        for step_id in wanted:
            for source in recipe["steps"][step_index(state, step_id)]["receives"]:
                origin = source.partition(".")[0] if "." in source else None
                if origin in group and origin not in wanted:
                    raise ParcoursError(
                        f"l'étape '{step_id}' reçoit '{source}' de '{origin}', écartée par le même choix : "
                        f"jouer aussi '{origin}' (--run {','.join(g for g in group if g in wanted + [origin])}) "
                        f"ou écarter aussi '{step_id}'")
        for step_id in group:
            step = state["steps"][step_index(state, step_id)]
            if step_id in wanted:
                step["chosen"] = True
            else:
                step["status"] = SKIPPED
        state["pending"] = None
        refresh_pending(state)
        save_state(directory, state)
        say(f"Jouées : {', '.join(wanted) or 'aucune'} ; écartées : {', '.join(g for g in group if g not in wanted) or 'aucune'}")
        announce_end(state)
        return 0


def cmd_rerun(args):
    directory = parcours_path(args)
    with parcours_lock(directory):
        state = load_state(directory)
        recipe = load_recipe(state["recipe"])
        check_recipe_matches(state, recipe)
        if state["status"] == "stopped":
            raise ParcoursError("parcours arrêté : rien à relancer")
        idx = step_index(state, args.step)
        if state["steps"][idx]["status"] in ("pending", "running"):
            raise ParcoursError(f"l'étape '{args.step}' n'a pas encore tourné (`next`)")
        extras = collect_extras(state, idx, args.extra)
        downstream = reset_from(directory, state, recipe, idx)
        step = state["steps"][idx]
        step["extra_inputs"] = extras
        if step.get("optional"):
            step["chosen"] = True
        state["status"] = "active"
        refresh_pending(state)
        save_state(directory, state)
        say(f"Étape '{args.step}' remise en file ; en aval, remises en file : "
            f"{', '.join(downstream) or 'aucune'}. Suite : next")
        return 0


def collect_extras(state, idx, sources):
    """Snapshot of extra `<step>.<field>` inputs for a rerun."""
    extras = {}
    for source in sources or []:
        step_id, _, field = source.partition(".")
        other = step_index(state, step_id)
        value = (state["steps"][other].get("handoff") or {}).get(field)
        if other == idx or value is None:
            raise ParcoursError(f"--extra {source} : champ indisponible (étape non jouée, ou celle qu'on relance)")
        extras[source] = value
    return extras


RESET_KEYS = ("handoff", "summary", "output", "error", "ended", "started", "extra_inputs", "blocking", "retried")


def reset_step(directory, state, recipe, j):
    """One step back to pending; its output is kept as .vN."""
    step = state["steps"][j]
    old = directory / step["output"] if step.get("output") else None
    if old and old.is_file():
        old.rename(versioned_name(old))
    for key in RESET_KEYS:
        step.pop(key, None)
    step["status"] = "pending"
    if recipe["steps"][j]["pause"] == "answers":
        state["answers"] = None


def reset_from(directory, state, recipe, idx):
    """Step `idx` and the played steps after it go back to pending; old outputs are kept as .vN.

    Returns the ids of the downstream steps that were reset.
    """
    downstream = []
    for j in range(idx, len(state["steps"])):
        if j > idx and state["steps"][j]["status"] not in ("done", "paused", "failed"):
            continue
        reset_step(directory, state, recipe, j)
        if j > idx:
            downstream.append(state["steps"][j]["id"])
    if recipe["steps"][idx]["produces_context_sheet"]:
        state["context_validated"] = False
    state["pending"] = None
    return downstream


def consumers(state, recipe, idx):
    """Indices of the played steps after `idx` that consumed its fields (or its context sheet),
    directly or through another consumer."""
    edited = recipe["steps"][idx]
    consumed, found = {edited["id"]}, []
    for j in range(idx + 1, len(state["steps"])):
        step, defn = state["steps"][j], recipe["steps"][j]
        if step["status"] not in ("done", "paused", "failed"):
            continue
        sources = list(defn["receives"]) + list(step.get("extra_inputs") or {})
        if edited["produces_context_sheet"] or any(
                "." in src and src.partition(".")[0] in consumed for src in sources):
            consumed.add(defn["id"])
            found.append(j)
    return found


def cmd_retry(args):
    directory = parcours_path(args)
    with parcours_lock(directory):
        state = load_state(directory)
        stuck = [s for s in state["steps"] if s["status"] in ("running", "failed")]
        if not stuck:
            raise ParcoursError("aucune étape 'running' ou 'failed' à reprendre")
        for step in stuck:
            step["status"] = "pending"
            step["retried"] = True  # an output file left on disk is parsed before any new call
            step.pop("error", None)
        refresh_pending(state)
        save_state(directory, state)
        say(f"Remises en attente : {', '.join(s['id'] for s in stuck)}. Suite : next")
        return 0


def cmd_handoff(args):
    directory = parcours_path(args)
    with parcours_lock(directory):
        state = load_state(directory)
        recipe = load_recipe(state["recipe"])
        check_recipe_matches(state, recipe)
        idx = step_index(state, args.step)
        step, defn = state["steps"][idx], recipe["steps"][idx]
        previous = step["status"]
        if previous not in ("failed", "done", "paused"):
            raise ParcoursError(
                f"l'étape '{args.step}' n'est ni en échec, ni terminée, ni en pause ({previous}) ; voir `rerun`")
        if state["status"] == "stopped" and previous != "failed":
            raise ParcoursError("parcours arrêté : rien à corriger")
        text = read_text_arg(args.file)
        if "handoff" not in find_sections(text)[0]:
            text = "## HANDOFF\n" + text
        context_fields = recipe["context_sheet"] if defn["produces_context_sheet"] else None
        parsed = parse_step_output(text, defn["transmits"], context_fields, defn.get("output_field"))
        check_parsed_leak(directory, defn["id"], parsed, defn.get("verbatim", ()),
                          admitted_text(state, recipe, idx))  # refused before anything is touched
        out_path = directory / output_name(idx, defn["id"])
        if out_path.exists():
            out_path.rename(versioned_name(out_path))
        write_atomic(out_path, "(sortie fournie à la main)\n\n" + text)
        stale = consumers(state, recipe, idx)
        reset = [state["steps"][j]["id"] for j in stale]
        for j in stale:
            reset_step(directory, state, recipe, j)
        if (state["pending"] or {}).get("step") in reset:
            state["pending"] = None
        if reset and state["status"] == "completed":
            state["status"] = "active"
        complete_step(directory, state, recipe, idx, parsed,
                      keep_status=previous if previous in ("done", "paused") else None, check=False)
        refresh_pending(state)
        save_state(directory, state)
        say(f"Champs de '{args.step}' enregistrés"
            + (f" ; remises en file : {', '.join(reset)}" if reset else "")
            + ". Suite : " + ("`validate`/`answer`" if step["status"] == "paused" else "next"))
        return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--engine", choices=ENGINES, help="moteur de tout le parcours (défaut : claude)")
    common.add_argument("--engine-step", action="append", metavar="STEP=ENGINE",
                        help="moteur d'une étape (répétable)")
    common.add_argument("--yes", action="store_true", help="ne pas demander confirmation avant de lancer")
    common.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="délai maximal par appel, en secondes")
    common.add_argument("--max-budget-usd", type=float, default=DEFAULT_BUDGET, help="plafond par appel (claude)")
    common.add_argument("--parcours-dir", default="./parcours", help="dossier des parcours")
    common.add_argument("--json", action="store_true",
                        help="sortie lisible par un programme (plan, status) ; erreurs en JSON sur la sortie standard")
    common.add_argument("--json-errors", action="store_true", default=argparse.SUPPRESS,
                        help="erreurs en JSON {\"error\", \"message\"} sur la sortie standard, code de sortie 1")

    parser = argparse.ArgumentParser(description="Exécuteur de parcours (voir docs/executeur.md)")
    parser.add_argument("--json-errors", action="store_true", help="erreurs en JSON (accepté avant la commande)")
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name, func, help_text, *positionals):
        p = sub.add_parser(name, parents=[common], help=help_text)
        for positional in positionals:
            p.add_argument(positional)
        p.set_defaults(func=func)
        return p

    p = add("new", cmd_new, "créer un parcours", "recipe")
    p.add_argument("--input", required=True, help="demande brute (fichier, ou - pour stdin)")
    p.add_argument("--slug")
    p = add("next", cmd_next, "jouer jusqu'à la prochaine pause", "slug")
    p.add_argument("--if-state", metavar="FINGERPRINT",
                   help="empreinte de l'état (donnée par `plan --json`) ; refusé sous le verrou si l'état a changé")
    add("plan", cmd_plan, "le plan du prochain `next`, sans rien écrire", "slug")
    add("status", cmd_status, "état du parcours", "slug")
    p = add("validate", cmd_validate, "lever une pause validate", "slug")
    p.add_argument("--context", help="fiche de contexte corrigée (JSON), à toute pause validate")
    p.add_argument("--stop", action="store_true", help="No-go : arrêter le parcours")
    p = add("answer", cmd_answer, "lever une pause answers", "slug")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--file")
    group.add_argument("--none", action="store_true")
    p = add("choose", cmd_choose, "embranchement avant des étapes optionnelles", "slug")
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", help="étapes à jouer, séparées par des virgules")
    group.add_argument("--skip", action="store_true")
    p = add("rerun", cmd_rerun, "relancer une étape", "slug", "step")
    p.add_argument("--extra", action="append", metavar="STEP.FIELD", help="champ supplémentaire (répétable)")
    add("retry", cmd_retry, "reprendre une étape restée running ou failed", "slug")
    p = add("handoff", cmd_handoff, "fournir ou corriger les champs à la main (étape en échec, terminée ou en pause)", "slug", "step")
    p.add_argument("--file", required=True)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    as_json = args.json or args.json_errors
    try:
        return args.func(args)
    except ParcoursError as exc:
        if as_json:
            emit_json({"error": exc.code, "message": str(exc)})
        else:
            print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        if not as_json:
            raise
        emit_json({"error": "unexpected", "message": f"{type(exc).__name__}: {exc}"})
        return 1


if __name__ == "__main__":
    sys.exit(main())
