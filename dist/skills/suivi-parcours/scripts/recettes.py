#!/usr/bin/env python3
"""
recettes.py — the user's own workflow recipes (spec: docs/interface.md §9).

A personal recipe lives outside the repository, in the user's recueil
(~/.ix-recipes/recettes/<id>.md next to the page's ~/.ix-recipes/parcours, see
parcours.recueil_dir; same format as skills/<id>.md). It is born as a
draft (<recueil>/brouillons/<draft>/): a need pasted by the user, a fresh engine call
playing the `concepteur-recette` skill over the real catalogue, a recipe file the
user edits (every save is checked like build.py checks a workflow), test dossiers
played apart from the real ones (<draft>/essais/, free `simulation` engine by
default), then the move to the recueil and, if wanted, a proposal to the
repository through git (branch, build, commit; push and pull request only once
confirmed).

Usage:
    python3 scripts/recettes.py list [--json]
    python3 scripts/recettes.py draft-new --input besoin.md [--title T] [--template]
    python3 scripts/recettes.py design <draft> [--mode propose|revise|write] [--insist] [--engine claude] [--model opus]
    python3 scripts/recettes.py comments <draft> --file commentaires.json   (sent with the next revision)
    python3 scripts/recettes.py show <draft> [--json]
    python3 scripts/recettes.py save <draft> --file recette.md [--if-sha SHA]
    python3 scripts/recettes.py check --file recette.md [--json]
    python3 scripts/recettes.py promote <draft> [--replace]
    python3 scripts/recettes.py template <draft>          (the blank model as the draft's file)
    python3 scripts/recettes.py edit <id>                 (a personal recipe back to a draft)
    python3 scripts/recettes.py personal <id> [--json]
    python3 scripts/recettes.py retire <id>               (out of the recueil, kept in .versions/)
    python3 scripts/recettes.py delete-draft <draft>
    python3 scripts/recettes.py essai-delete <draft> <slug>
    python3 scripts/recettes.py contribute <id> prepare [--source PATH|URL] | push | cancel | status

Common options: --parcours-dir (default $PARCOURS_DIR, else ./parcours), --json (machine
output; errors become {"error": code, "message": ...} on stdout, exit code 1).
Standard library only, like parcours.py, which it imports.
"""

import argparse
import contextlib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import parcours as P  # noqa: E402

UPSTREAM = "https://github.com/amiel-35/ix-recipes.git"
DRAFT_STATE = "brouillon.json"
NEED_FILE = "besoin.md"
DESIGN_OUT = "conception.md"
DESIGN_TRACE = "conception.in.md"
VERSIONS = ".versions"
CONTRIB = ".contribution"
SLUG_RE = re.compile(r"[a-z0-9][a-z0-9-]{0,79}")
VERDICTS = ("recipe", "single_skill", "manual_sequence", "catalogue_gap")
DESIGN_ENGINES = ("claude", "codex", "agy", "vibe", "fake")   # not `simulation`: it has nothing to design
DESIGN_MODEL = "opus"            # a judgement on the whole job: the rule of step 1 (docs/format-recette.md §1.8)
NOT_IN_CATALOGUE = {"concepteur-recette", "suivi-parcours", "configuration-ix"}   # tools, not steps
DIFF_LIMIT = 300_000
GIT_TIMEOUT = 300


class ExistsError(P.ParcoursError):
    code = "exists"


class GitError(P.ParcoursError):
    code = "git"


# ---------------------------------------------------------------------------
# Folders
# ---------------------------------------------------------------------------
def recueil(args):
    return P.recueil_dir(args.parcours_dir)


def drafts_dir(args):
    return recueil(args) / P.DRAFTS_DIR


def draft_dir(args, slug, must_exist=True):
    if not slug or not SLUG_RE.fullmatch(slug):
        raise P.ParcoursError(f"identifiant de brouillon invalide : '{slug}'")
    directory = drafts_dir(args) / slug
    if must_exist and (directory.is_symlink() or not (directory / DRAFT_STATE).is_file()):
        raise P.NotFound(f"brouillon introuvable : {slug}")
    return directory


def personal_path(args, recipe_id):
    if not recipe_id or not P.RECIPE_ID_RE.fullmatch(recipe_id):
        raise P.ParcoursError(f"identifiant de recette invalide : '{recipe_id}'")
    path = recueil(args) / f"{recipe_id}.md"
    if path.is_symlink() or not path.is_file():
        raise P.NotFound(f"recette personnelle introuvable : {recipe_id}")
    return path


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(path, data):
    P.write_atomic(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest() if Path(path).is_file() else None


def stamp():
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def keep_version(path, folder=None):
    """Copy `path` into `folder` (default: next to it, as .vN) before it is replaced."""
    path = Path(path)
    if not path.is_file():
        return None
    if folder is None:
        target = P.versioned_name(path)
    else:
        folder.mkdir(parents=True, exist_ok=True)
        target = folder / f"{path.stem}.{stamp()}{path.suffix}"
        n = 2
        while target.exists():
            target = folder / f"{path.stem}.{stamp()}-{n}{path.suffix}"
            n += 1
    shutil.copyfile(path, target)
    return target


# ---------------------------------------------------------------------------
# The blank model (also the format reference sent to the designer)
# ---------------------------------------------------------------------------
TEMPLATE = """---
id: ma-recette
label: Ma recette
version: 0.1.0
description_fr: "Décrit en une ou deux phrases ce que fait la recette, quand l'utiliser (déclenche sur « … ») et ce qu'elle ne fait pas (voir `autre-skill`)."
description_en: "One or two sentences on what the recipe does, when to use it (triggers on \\"…\\") and what it does not do (see `other-skill`)."
summary_fr: "D'une demande à un livrable : cadrage, relecture, puis livrable."
icon: ⇢
domain: ops
category: workflow
input_types:
- brief
output_types:
- brief
compatible:
- claude-ai
- claude-code
- cowork
- gpt
- gemini
- mystaffy
requires: [ix-skills:cadrage, ix-skills:brief]
workflow:
  context_sheet: [objective, constraints, recipient, deadlines]
  context_labels:
    objective: "Objectif"
    constraints: "Contraintes"
    recipient: "Destinataire"
    deadlines: "Échéances"
  steps:
    - id: cadrage
      label: "Cadrage de la demande"
      skill: ix-skills:cadrage
      mission: Clarify the need from the raw request — goal, constraints, hypotheses, named solutions — and stop at clarification.
      receives: [brief]
      transmits: [need, constraints, open_points]
      produces_context_sheet: true
      pause: validate
      model: opus
    - id: livrable
      label: "Livrable"
      skill: ix-skills:brief
      mission: Write the actionable brief from the scoped need — objective, scope, constraints, acceptance criteria, remaining hypotheses.
      receives: [context_sheet, cadrage.need, cadrage.constraints, cadrage.open_points]
      transmits: [deliverable]
      output_field: deliverable
      pause: none
      model: sonnet
---

# Role

You orchestrate this recipe: you chain its steps, stop at its pauses and never do the work of a step yourself.

# Absolute rules

- Each step runs isolated and receives only what its `receives` line lists.
- The raw request reaches step 1 only; the validated context sheet replaces it for the later steps.
- Steps hand over named fields only; the human decides at the pauses.

# Context sheet

| field | definition |
|---|---|
| `objective` | What the requester wants to obtain, in one sentence. |
| `constraints` | Imposed constraints (budget, format, scope), facts only. |
| `recipient` | Who reads the deliverable. |
| `deadlines` | Dates stated in the request. |

# Steps

| # | Step | Skill | Mission | Receives | Transmits | Pause |
|---|---|---|---|---|---|---|
| 1 | cadrage | `ix-skills:cadrage` | Clarify the need | brief | need, constraints, open_points | validate |
| 2 | livrable | `ix-skills:brief` | Write the deliverable | context_sheet, cadrage.* | deliverable | none |

# Running a step

Send the sub-agent: the skill to use, its model, its mission, the context sheet (from step 2), the received fields only, the trace file to write its full output to; it answers with its `## HANDOFF` block and a five-line summary, and never goes beyond its mission.

# Pauses

After step 1: show the output and the context sheet; wait for the human to validate or correct.

# Trace

Each full output in `./parcours/<slug>/NN-<step>.md`, the context sheet in `00-context.md`.

# Without sub-agents

Chain the steps in the conversation, opening each with a block holding only its inputs, and say at the top of the output that isolation was not possible.

# Output

The output of the last step, plus a short trace (steps played, pauses, what stayed a hypothesis).

# Definition of done

- Every step ran with its inputs only; the human validated the context sheet.
- The deliverable answers the objective of the context sheet.
"""


# ---------------------------------------------------------------------------
# Drafts
# ---------------------------------------------------------------------------
def new_draft(args, title, need=None, text=None, origin=None, slug_hint=None):
    """Create <recueil>/brouillons/<slug>/ with its state, its need and, if given, a recipe file."""
    base = drafts_dir(args)
    base.mkdir(parents=True, exist_ok=True)
    wanted = P.slugify(slug_hint or title or "")[:50].strip("-")
    if not wanted and need:
        words = re.findall(r"[a-z0-9]{3,}", P.slugify(need).replace("-", " "))
        wanted = "-".join(["recette"] + words[:3])[:50].strip("-")
    directory, slug = P.create_unique_dir(base, wanted or f"recette-{datetime.now():%Y%m%d}")
    state = {"slug": slug, "title": title or None, "created": P.now(), "updated": P.now(), "origin": origin,
             "verdict": None, "design": None, "promoted": None}
    if need is not None:
        P.write_atomic(directory / NEED_FILE, need)
    if text is not None:
        P.write_atomic(directory / P.DRAFT_FILE, text)
    write_json(directory / DRAFT_STATE, state)
    return directory, slug


def touch(directory, state, **changes):
    state.update(changes, updated=P.now())
    write_json(directory / DRAFT_STATE, state)


def cmd_draft_new(args):
    title = " ".join((args.title or "").split())[:120] or None
    need = P.read_text_arg(args.input) if args.input else None
    if not need and not args.template:
        raise P.ParcoursError("le besoin est vide : décrivez le travail récurrent, ou partez du modèle (--template)")
    if not title and need:   # a readable name until the recipe has one: the need's first words
        words = " ".join(need.split()).split(" ")
        title = " ".join(words[:8]) + (" …" if len(words) > 8 else "")
    _, slug = new_draft(args, title, need=need, text=TEMPLATE if args.template else None)
    return emit(args, {"slug": slug, "title": title}, f"Brouillon créé : {slug}")


def essais_summary(directory, current_sha):
    """The test dossiers of a draft: title, status, steps, whether they ran the current recipe."""
    folder = directory / P.ESSAIS_DIR
    items = []
    for entry in sorted(folder.iterdir()) if folder.is_dir() else []:
        state = read_json(entry / "state.json") if entry.is_dir() and not entry.is_symlink() else None
        if not isinstance(state, dict) or not SLUG_RE.fullmatch(entry.name):
            continue
        steps = state.get("steps") or []
        items.append({
            "slug": entry.name, "title": state.get("title"), "status": state.get("status"),
            "engine": state.get("engine"), "created": state.get("created"), "cost_usd": state.get("cost_usd", 0.0),
            "steps_total": len(steps), "steps_done": sum(1 for s in steps if s.get("status") in ("done", "skipped")),
            "pending": (state.get("pending") or {}).get("type"),
            "current": bool(current_sha and state.get("recipe_sha256") == current_sha),
            "locked": P.is_locked(entry),
            "updated": datetime.fromtimestamp((entry / "state.json").stat().st_mtime).isoformat(timespec="seconds"),
        })
    items.sort(key=lambda i: i["updated"], reverse=True)
    return items


def draft_summary(args, directory, full=False):
    state = read_json(directory / DRAFT_STATE, {}) or {}
    recipe_file = directory / P.DRAFT_FILE
    text = recipe_file.read_text(encoding="utf-8", errors="replace") if recipe_file.is_file() else None
    sha = sha256_file(recipe_file)
    check = P.check_recipe_text(text) if text is not None else None
    essais = essais_summary(directory, sha)
    promoted = state.get("promoted") or None
    summary = {
        "slug": directory.name, "title": state.get("title"), "created": state.get("created"),
        "updated": state.get("updated"), "origin": state.get("origin"), "verdict": state.get("verdict"),
        "design": state.get("design"), "promoted": promoted, "locked": P.is_locked(directory),
        "has_recipe": text is not None, "sha256": sha,
        "recipe_id": check["id"] if check else None,
        "recipe_label": (check["recipe"] or {}).get("label") if check and check["recipe"] else None,
        "errors": len(check["errors"]) if check else 0,
        "tested": any(e["current"] and e["status"] == "completed" for e in essais),
        "in_recueil": bool(promoted and promoted.get("sha256") == sha),
        "essais_count": len(essais),
    }
    proposal = read_json(directory / PROPOSAL_FILE)
    summary["stage"] = "recipe" if text is not None else "proposal" if proposal else "start"
    summary["proposal_steps"] = len((proposal or {}).get("steps") or [])
    if full:
        concept = directory / DESIGN_OUT
        summary.update(
            need=(directory / NEED_FILE).read_text(encoding="utf-8", errors="replace") if (directory / NEED_FILE).is_file() else None,
            text=text, check=check, essais=essais,
            proposal=dict(proposal, problems=proposal_problems(proposal)) if proposal else None,
            comments=read_comments(directory),
            concept=design_document(concept.read_text(encoding="utf-8", errors="replace")) if concept.is_file() else None,
            files=P.listed_files(directory),
            recueil=str(recueil(args)),
            exists_in_recueil=bool(check and check["id"] and P.RECIPE_ID_RE.fullmatch(check["id"])
                                   and (recueil(args) / f"{check['id']}.md").is_file()),
        )
    return summary


def cmd_show(args):
    directory = draft_dir(args, args.draft)
    data = draft_summary(args, directory, full=True)
    if args.json:
        P.emit_json(data)
        return 0
    P.say(f"Brouillon {data['slug']} — {data['title'] or data['recipe_id'] or ''}")
    P.say(f"Verdict du concepteur : {data['verdict'] or '—'} ; recette : {'oui' if data['has_recipe'] else 'non'}")
    for error in (data["check"] or {}).get("errors", []):
        P.say(f"  erreur : {error}")
    for essai in data["essais"]:
        P.say(f"  essai {essai['slug']} : {essai['status']}")
    return 0


def cmd_save(args):
    directory = draft_dir(args, args.draft)
    text = P.read_text_arg(args.file).replace("\r\n", "\n")
    with P.parcours_lock(directory):
        path = directory / P.DRAFT_FILE
        current = sha256_file(path)
        if args.if_sha and current and args.if_sha.lower() != current:
            raise P.StateChanged("le fichier a changé depuis son ouverture (nouvelle conception ?) : rien n'a été "
                                 "enregistré, rechargez-le")
        if path.is_file() and path.read_text(encoding="utf-8", errors="replace") == text:
            changed = False
        else:
            keep_version(path)
            P.write_atomic(path, text)
            changed = True
        state = read_json(directory / DRAFT_STATE, {})
        touch(directory, state)
    check = P.check_recipe_text(text)
    return emit(args, {"saved": changed, "sha256": sha256_file(path), "check": check},
                "Enregistré." + (f" {len(check['errors'])} erreur(s)." if check["errors"] else " Recette valide."))


def cmd_check(args):
    text = P.read_text_arg(args.file)
    check = P.check_recipe_text(text)
    if args.json:
        P.emit_json(check)
        return 0
    for error in check["errors"]:
        P.say(f"erreur : {error}")
    for gap in check["contribution"]:
        P.say(f"pour le dépôt : {gap}")
    P.say("Recette valide." if not check["errors"] else f"{len(check['errors'])} erreur(s).")
    return 0 if not check["errors"] else 1


def cmd_promote(args):
    """The draft joins the recueil (<recueil>/<id>.md); a replaced version is kept in .versions/."""
    directory = draft_dir(args, args.draft)
    with P.parcours_lock(directory):
        path = directory / P.DRAFT_FILE
        if not path.is_file():
            raise P.ParcoursError("ce brouillon n'a pas encore de fichier de recette")
        text = path.read_text(encoding="utf-8")
        check = P.check_recipe_text(text)
        if check["errors"]:
            raise P.ParcoursError("la recette a encore des erreurs : " + " ; ".join(check["errors"][:5]))
        recipe_id = check["id"]
        state = read_json(directory / DRAFT_STATE, {})
        target = recueil(args) / f"{recipe_id}.md"
        if target.is_symlink():
            raise P.ParcoursError(f"{target} est un lien symbolique : refusé")
        if target.is_file() and state.get("origin") != recipe_id and not args.replace:
            raise ExistsError(f"votre recueil contient déjà une recette '{recipe_id}' : la remplacer, ou changer l'id")
        recueil(args).mkdir(parents=True, exist_ok=True)
        replaced = keep_version(target, recueil(args) / VERSIONS)
        P.write_atomic(target, text)
        touch(directory, state, origin=recipe_id,
              promoted={"id": recipe_id, "at": P.now(), "sha256": sha256_file(path)})
    return emit(args, {"id": recipe_id, "path": str(target), "replaced": bool(replaced)},
                f"Recette '{recipe_id}' enregistrée dans votre recueil ({target}).")


def cmd_edit(args):
    """A personal recipe back to a draft (the draft it came from if it is unchanged since)."""
    path = personal_path(args, args.recipe)
    text = path.read_text(encoding="utf-8")
    base = drafts_dir(args)
    for directory in sorted(base.iterdir()) if base.is_dir() else []:
        state = read_json(directory / DRAFT_STATE)
        if isinstance(state, dict) and state.get("origin") == args.recipe and not P.is_locked(directory):
            current = directory / P.DRAFT_FILE
            if current.is_file() and current.read_text(encoding="utf-8", errors="replace") == text:
                return emit(args, {"slug": directory.name, "reused": True}, f"Brouillon : {directory.name}")
    fm, _ = P.parse_recipe_text(text)
    _, slug = new_draft(args, str(fm.get("label") or args.recipe), text=text, origin=args.recipe, slug_hint=args.recipe)
    directory = draft_dir(args, slug)
    state = read_json(directory / DRAFT_STATE, {})
    touch(directory, state, promoted={"id": args.recipe, "at": None, "sha256": sha256_file(directory / P.DRAFT_FILE)})
    return emit(args, {"slug": slug, "reused": False}, f"Brouillon créé : {slug}")


def cmd_template(args):
    """The blank model as the draft's recipe file (the current one kept as recipe.vN.md)."""
    directory = draft_dir(args, args.draft)
    with P.parcours_lock(directory):
        keep_version(directory / P.DRAFT_FILE)
        P.write_atomic(directory / P.DRAFT_FILE, TEMPLATE)
        touch(directory, read_json(directory / DRAFT_STATE, {}))
    return emit(args, {"slug": args.draft, "sha256": sha256_file(directory / P.DRAFT_FILE)}, "Modèle copié dans le brouillon.")


def cmd_delete_draft(args):
    directory = draft_dir(args, args.draft)
    if P.is_locked(directory) or any(P.is_locked(e) for e in (directory / P.ESSAIS_DIR).glob("*") if e.is_dir()):
        raise P.LockedError("une conception ou un essai tourne sur ce brouillon")
    shutil.rmtree(directory)
    return emit(args, {"deleted": args.draft}, f"Brouillon supprimé : {args.draft}")


def cmd_essai_delete(args):
    directory = draft_dir(args, args.draft)
    if not SLUG_RE.fullmatch(args.slug or ""):
        raise P.ParcoursError(f"identifiant d'essai invalide : '{args.slug}'")
    essai = directory / P.ESSAIS_DIR / args.slug
    if essai.is_symlink() or not (essai / "state.json").is_file() or essai.resolve().parent != (directory / P.ESSAIS_DIR).resolve():
        raise P.NotFound(f"essai introuvable : {args.slug}")
    if P.is_locked(essai):
        raise P.LockedError("une étape tourne sur cet essai")
    shutil.rmtree(essai)
    return emit(args, {"deleted": args.slug}, f"Essai supprimé : {args.slug}")


# ---------------------------------------------------------------------------
# Personal recipes
# ---------------------------------------------------------------------------
def personal_summary(args, path, full=False):
    text = path.read_text(encoding="utf-8", errors="replace")
    check = P.check_recipe_text(text)
    recipe = check["recipe"] or {}
    contribution = read_json(recueil(args) / CONTRIB / f"{path.stem}.json")
    data = {
        "id": path.stem, "label": recipe.get("label") or path.stem, "version": recipe.get("version"),
        "summary": recipe.get("summary") or recipe.get("description") or "",
        "steps": len(recipe.get("steps") or []), "errors": check["errors"],
        "shadowed": path.stem in P.plugin_recipe_ids(),
        "updated": datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
        "contribution": public_contribution(contribution),
    }
    if full:
        versions = recueil(args) / VERSIONS
        data.update(text=text, check=check, sha256=sha256_file(path), path=str(path),
                    versions=sorted(p.name for p in versions.glob(f"{path.stem}.*.md")) if versions.is_dir() else [],
                    default_source=default_source(args))
    return data


def cmd_list(args):
    base = recueil(args)
    personal = [personal_summary(args, p) for p in sorted(base.glob("*.md"))
                if P.RECIPE_ID_RE.fullmatch(p.stem) and not p.is_symlink()] if base.is_dir() else []
    drafts = []
    folder = drafts_dir(args)
    for directory in sorted(folder.iterdir()) if folder.is_dir() else []:
        if directory.is_dir() and not directory.is_symlink() and SLUG_RE.fullmatch(directory.name) \
                and (directory / DRAFT_STATE).is_file():
            drafts.append(draft_summary(args, directory))
    drafts.sort(key=lambda d: d.get("updated") or "", reverse=True)
    data = {"recueil": str(base), "personal": personal, "drafts": drafts}
    if args.json:
        P.emit_json(data)
        return 0
    P.say(f"Recueil : {base}")
    for r in personal:
        P.say(f"  {r['id']} — {r['label']}" + (" (erreurs)" if r["errors"] else ""))
    for d in drafts:
        P.say(f"  brouillon {d['slug']} — {d['title'] or d['recipe_id'] or ''}")
    return 0


def cmd_personal(args):
    path = personal_path(args, args.recipe)
    data = personal_summary(args, path, full=True)
    if args.json:
        P.emit_json(data)
        return 0
    P.say(data["text"])
    return 0


def cmd_retire(args):
    path = personal_path(args, args.recipe)
    target = keep_version(path, recueil(args) / VERSIONS)
    path.unlink()
    return emit(args, {"retired": args.recipe, "kept": str(target)}, f"Recette retirée du recueil (copie : {target})")


# ---------------------------------------------------------------------------
# Design: one fresh engine call playing concepteur-recette over the real catalogue
# ---------------------------------------------------------------------------
def catalogue_block():
    lines = []
    for ref, item in sorted(P.catalogue().items()):
        if item["id"] in NOT_IN_CATALOGUE:
            continue
        description = item["description"]
        if len(description) > 600:
            description = description[:600].rsplit(" ", 1)[0] + " …"
        lines.append(f"- `{ref}` — {description or '(no description)'}")
    return "\n".join(lines)


PROPOSAL_FILE = "proposition.json"   # the chain proposed by the designer, commented before any file is written
COMMENTS_FILE = "commentaires.json"  # the user's comments, sent with the next revision
DESIGN_MODES = ("propose", "revise", "write")
MAX_STEPS = 6
SOURCES_RULE = (
    "`receives` takes ONLY these sources: `brief` (the raw input, all of it, whatever it holds — "
    "reports, tables, emails: step 1 receives `[brief]`, never names of documents), `context_sheet` "
    "(from step 2 on), `answers` (after a step with `pause: answers`), or `<step>.<field>` transmitted "
    "by an earlier step. Any other name is refused.")
PROPOSAL_SHAPE = (
    '{"title": "<short French name of the recipe>", "summary": "<one French sentence: from what to what>",\n'
    ' "context_sheet": ["<French rubric of the context sheet>", "..."],\n'
    ' "steps": [{"id": "<lower-case id>", "label": "<French name>", "skill": "<namespace:id from the catalogue>",\n'
    '            "role": "<what the step does, one French sentence>", "receives": ["brief"],\n'
    '            "produces": ["<field>", "..."], "pause": "none | validate | answers | choose", "optional": false}]}')


def design_message(skill, need, mode="propose", insist=False, previous=None, proposal=None, comments=None):
    """The message of one designer call. `propose` and `revise` ask for the chain only (a JSON
    proposal the user comments on), `write` for the recipe file implementing a validated proposal."""
    parts = [
        "You are running ONE call of the recipe designer. This message is all you know: you have no "
        "other context, and you need no file and no tool.",
        f"=== SKILL: {skill['ref']} ===\n{skill['text']}\n=== END SKILL ===",
        "The skill text is your method. Where its output format and the OUTPUT FORMAT below disagree, "
        "the OUTPUT FORMAT wins.",
        "=== CATALOGUE ===\nThe real catalogue, complete: these skills exist and no other. Write their "
        "namespaced ids exactly as below; never invent one, never use a label or a translation in place "
        "of an id. Recipes cannot run other workflow recipes (`category: workflow`).\n"
        f"{catalogue_block()}\n=== END CATALOGUE ===",
        "=== FORMAT REFERENCE ===\nA complete recipe file in the ix-recipes format (docs/format-recette.md), "
        "given as a model of the FORMAT only — not of the steps, which depend on the job. Keep every "
        "frontmatter key it has; a `workflow` step may also use `optional: true` (run only if the human "
        "chooses it at the pause before), `verbatim` (step 1 only) and `pause: answers` / `choose`.\n"
        f"{SOURCES_RULE}\n"
        f"````markdown\n{TEMPLATE}````\n=== END FORMAT REFERENCE ===",
        f"=== JOB ===\n{need}\n=== END JOB ===",
    ]
    if insist:
        parts.append(
            "=== THE USER INSISTS ===\nThe user has read a verdict saying that no recipe was needed and "
            "still wants one. Give verdict `recipe` and the shortest defensible chain, from the catalogue "
            "only. Say in the rationale what a single skill would have done instead."
            + (f"\n\nYour previous answer, for reference:\n{previous}" if previous else "")
            + "\n=== END THE USER INSISTS ===")
    if proposal is not None and mode in ("revise", "write"):
        shown = {k: proposal.get(k) for k in ("title", "summary", "context_sheet", "steps")}
        name = "THE PROPOSAL THE USER VALIDATED" if mode == "write" else "YOUR PREVIOUS PROPOSAL"
        parts.append(f"=== {name} ===\n```json\n{json.dumps(shown, ensure_ascii=False, indent=2)}\n```\n=== END {name} ===")
    if comments and mode == "revise":
        lines = []
        if comments.get("general"):
            lines.append(f"On the whole chain: {comments['general']}")
        for step_id, text in (comments.get("steps") or {}).items():
            lines.append(f"On step `{step_id}`: {text}")
        parts.append("=== THE USER'S COMMENTS ===\n" + "\n".join(lines) + "\n=== END THE USER'S COMMENTS ===")
    language = ("Write for the user in French (verdict, rationale, questions). Step ids and field names: lower "
                "case without accents, digits, hyphens or underscores.\n")
    verdict_block = ("End with exactly this block, nothing after it, holding one of the four words alone:\n\n"
                     "## VERDICT\nrecipe | single_skill | manual_sequence | catalogue_gap\n")
    if mode == "write":
        parts.append(
            "=== OUTPUT FORMAT ===\n" + language +
            "Write the complete recipe file implementing EXACTLY the validated proposal: the same steps in "
            "the same order, the same skills, pauses and optional steps, the context sheet rubrics as keys "
            "(with French `context_labels`), each step's `produces` as its `transmits`. Fill in what the "
            "proposal leaves out (missions in English, models, the body). The file follows the skill's "
            "language rules: `label`, `summary_fr` and `description_fr` in French, `description_en` and the "
            "body in English, step `label` in French.\n"
            "Give the recipe file in ONE fenced code block opened with four backticks (````markdown) whose "
            "first line is `---`, then, if anything in the proposal could not be kept as is, say so in one "
            "short paragraph. No rationale, no questions.\n" + verdict_block + "=== END OUTPUT FORMAT ===")
    else:
        parts.append(
            "=== OUTPUT FORMAT ===\n" + language +
            "Give the skill's part A (verdict). When a recipe is justified, DO NOT write the recipe file: "
            "the user first comments on the chain. Give instead the PROPOSAL, in ONE ```json code block of "
            f"exactly this shape:\n{PROPOSAL_SHAPE}\n"
            f"Sources in `receives` follow the rule above: {SOURCES_RULE} At most {MAX_STEPS} steps.\n"
            + ("Take every comment into account; when you do not follow one, say why in the rationale.\n"
               if mode == "revise" else "")
            + "Then the rationale and the questions to settle (the skill's part B, without the file). Leave "
            "out part C. When no recipe is justified, give no JSON block.\n" + verdict_block
            + "=== END OUTPUT FORMAT ===")
    return "\n\n".join(parts) + "\n"


def fenced_blocks(text):
    """[(start line, end line, info, content)] of the top-level fenced code blocks."""
    lines, found, i = text.splitlines(), [], 0
    while i < len(lines):
        match = P.FENCE_RE.match(lines[i])
        if not match:
            i += 1
            continue
        char, size = match.group(1)[0], len(match.group(1))
        info = lines[i].strip()[size:].strip()
        body, j = [], i + 1
        while j < len(lines):
            close = P.FENCE_RE.match(lines[j])
            if close and close.group(1)[0] == char and len(close.group(1)) >= size and lines[j].strip() == close.group(1):
                break
            body.append(lines[j])
            j += 1
        found.append((i, j, info, "\n".join(body).strip("\n")))
        i = j + 1
    return found


def recipe_block(text):
    """(start line, end line, content) of the first fenced block whose content opens with `---`, else None."""
    for start, end, _, content in fenced_blocks(text):
        if content.lstrip().startswith("---") and "workflow" in content:
            return start, end, content.strip() + "\n"
    return None


def proposal_block(text):
    """(start line, end line, normalized proposal) of the first JSON block holding `steps`, else None."""
    for start, end, _, content in fenced_blocks(text):
        if "{" not in content or '"steps"' not in content:
            continue
        try:
            data = P.load_json_lenient(content)
        except ValueError:
            continue
        if isinstance(data, dict) and isinstance(data.get("steps"), list):
            return start, end, normalize_proposal(data)
    return None


def as_strings(value):
    if isinstance(value, str):
        value = [value]
    return [str(v).strip() for v in (value or []) if str(v).strip()] if isinstance(value, list) else []


def normalize_proposal(data):
    steps = []
    for raw in data.get("steps") or []:
        if not isinstance(raw, dict):
            continue
        sid = re.sub(r"[^a-z0-9_-]+", "-", P.fold_text(str(raw.get("id") or raw.get("label") or "")).strip()).strip("-_")
        pause = str(raw.get("pause") or "none").strip()
        steps.append({
            "id": sid or f"etape-{len(steps) + 1}", "label": str(raw.get("label") or "").strip(),
            "skill": str(raw.get("skill") or "").strip(), "role": str(raw.get("role") or "").strip(),
            "receives": as_strings(raw.get("receives")), "produces": as_strings(raw.get("produces")),
            "pause": pause if pause in P.PAUSES else "none", "optional": raw.get("optional") is True,
        })
    return {"title": str(data.get("title") or "").strip(), "summary": str(data.get("summary") or "").strip(),
            "context_sheet": as_strings(data.get("context_sheet")), "steps": steps}


def proposal_problems(proposal, refs=None):
    """What would make the validated chain an invalid recipe, in French (the rules of workflow_errors
    that a proposal can already break): unknown skills, sources, step count."""
    refs = set(P.catalogue()) if refs is None else refs
    problems, produced, answers_ready, seen = [], {}, False, set()
    steps = proposal.get("steps") or []
    if not steps:
        return ["la proposition n'a aucune étape"]
    if len(steps) > MAX_STEPS:
        problems.append(f"{len(steps)} étapes : {MAX_STEPS} au plus")
    for i, step in enumerate(steps):
        name = step["label"] or step["id"]
        if step["id"] in seen:
            problems.append(f"« {name} » : identifiant en double ({step['id']})")
        seen.add(step["id"])
        if step["skill"] not in refs:
            problems.append(f"« {name} » : le skill « {step['skill'] or '?'} » n'existe pas dans le catalogue")
        if not step["produces"]:
            problems.append(f"« {name} » : ne produit rien pour la suite")
        for source in step["receives"]:
            if source == "brief":
                if i:
                    problems.append(f"« {name} » : seule la première étape lit la demande brute (brief)")
            elif source == "context_sheet":
                if not i:
                    problems.append("la première étape ne peut pas recevoir la fiche de contexte qu'elle produit")
            elif source == "answers":
                if not answers_ready:
                    problems.append(f"« {name} » : reçoit les réponses avant toute pause « answers »")
            elif "." in source:
                origin, field = source.split(".", 1)
                if field not in produced.get(origin, ()):
                    problems.append(f"« {name} » : « {source} » n'est produit par aucune étape antérieure")
            else:
                problems.append(f"« {name} » : « {source} » n'est pas une entrée possible"
                                + (" (la première étape reçoit brief)" if not i else ""))
        produced[step["id"]] = set(step["produces"])
        answers_ready = answers_ready or step["pause"] == "answers"
    if "brief" not in steps[0]["receives"]:
        problems.append("la première étape doit recevoir brief (la demande brute)")
    return problems


def verdict_of(text):
    lines = text.splitlines()
    cut = next((k for k in range(len(lines) - 1, -1, -1) if re.match(r"^##\s+VERDICT\s*$", lines[k].strip(), re.I)), None)
    if cut is None:
        return None, text
    words = re.findall(r"[a-z_]+", " ".join(lines[cut + 1:]).lower())
    return next((w for w in words if w in VERDICTS), None), "\n".join(lines[:cut])


def parse_design(text):
    """(verdict, recipe text or None, document for the reader)."""
    verdict, body = verdict_of(text)
    block = recipe_block(body)
    recipe = block[2] if block else None
    if verdict is None:
        verdict = "recipe" if recipe or proposal_block(body) else None
    return verdict, recipe, design_document(text)


def design_document(text):
    """The designer's answer as the page shows it: the recipe file and the JSON proposal replaced by
    pointers to where the page shows them."""
    _, body = verdict_of(text)
    for finder, note in ((recipe_block, "*(Le fichier de la recette est dans l'éditeur, onglet « Fichier de la recette ».)*"),
                         (proposal_block, "*(La proposition est affichée étape par étape, onglet « Proposition ».)*")):
        block = finder(body)
        if block:
            kept = body.splitlines()
            body = "\n".join(kept[:block[0]] + [note] + kept[block[1] + 1:])
    return body.strip()


def read_comments(directory):
    data = read_json(directory / COMMENTS_FILE, {}) or {}
    steps = {k: v for k, v in (data.get("steps") or {}).items() if isinstance(v, str) and v.strip()}
    return {"general": str(data.get("general") or "").strip(), "steps": steps}


def cmd_comments(args):
    """Record the user's comments on the current proposal (sent with the next `design --mode revise`)."""
    directory = draft_dir(args, args.draft)
    try:
        data = json.loads(P.read_text_arg(args.file))
    except ValueError as exc:
        raise P.ParcoursError(f"commentaires illisibles ({exc})")
    if not isinstance(data, dict):
        raise P.ParcoursError("commentaires : un objet JSON est attendu")
    proposal = read_json(directory / PROPOSAL_FILE)
    ids = {s["id"] for s in (proposal or {}).get("steps", [])}
    steps = data.get("steps") or {}
    if not isinstance(steps, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in steps.items()):
        raise P.ParcoursError("commentaires : « steps » associe un id d'étape à un texte")
    unknown = [k for k, v in steps.items() if v.strip() and k not in ids]
    if unknown:
        raise P.ParcoursError(f"commentaires sur des étapes absentes de la proposition : {', '.join(unknown)}")
    clean = {"general": str(data.get("general") or "").strip(),
             "steps": {k: v.strip() for k, v in steps.items() if v.strip()}}
    with P.parcours_lock(directory):
        write_json(directory / COMMENTS_FILE, clean)
    return emit(args, clean, "Commentaires enregistrés.")


def step_drift(proposal, recipe_text):
    """How the written file departs from the validated proposal (steps, order, skills, pauses)."""
    try:
        fm, _ = P.parse_recipe_text(recipe_text)
        written = [s for s in (fm.get("workflow") or {}).get("steps") or [] if isinstance(s, dict)]
    except P.ParcoursError:
        return []
    wanted = proposal.get("steps") or []
    drift = []
    if [s.get("skill") for s in written] != [s["skill"] for s in wanted]:
        drift.append("les étapes ou leurs skills ne suivent pas la proposition : "
                     + " → ".join(str(s.get("skill")) for s in written))
    for want, got in zip(wanted, written):
        pause = got.get("pause", "none")
        if want["skill"] == got.get("skill") and want["pause"] != pause and not (got.get("produces_context_sheet") and want["pause"] == "none"):
            drift.append(f"« {want['label'] or want['id']} » : pause {pause} au lieu de {want['pause']}")
    return drift


def cmd_design(args):
    directory = draft_dir(args, args.draft)
    engine = args.engine or "claude"
    mode = args.mode or "propose"
    if engine not in DESIGN_ENGINES:
        raise P.ParcoursError(f"moteur '{engine}' : la conception se fait avec {', '.join(DESIGN_ENGINES)}")
    need_file = directory / NEED_FILE
    if not need_file.is_file():
        raise P.ParcoursError("ce brouillon n'a pas de besoin décrit : la conception n'a rien à lire")
    with P.parcours_lock(directory):
        state = read_json(directory / DRAFT_STATE, {})
        proposal = read_json(directory / PROPOSAL_FILE)
        comments = read_comments(directory)
        if mode in ("revise", "write") and not (proposal and proposal.get("steps")):
            raise P.ParcoursError("aucune proposition à reprendre : lancez d'abord la conception")
        if mode == "revise" and not (comments["general"] or comments["steps"] or args.insist):
            raise P.ParcoursError("aucun commentaire : écrivez ce qu'il faut changer, sur une étape ou sur l'ensemble")
        if mode == "write":
            problems = proposal_problems(proposal)
            if problems:
                raise P.ParcoursError("la proposition ne peut pas devenir une recette valide : " + " ; ".join(problems[:4])
                                      + ". Demandez une révision.")
        skill = P.resolve_skill("ix-recipes:concepteur-recette")
        previous = None
        if args.insist and (directory / DESIGN_OUT).is_file():
            previous = design_document((directory / DESIGN_OUT).read_text(encoding="utf-8", errors="replace"))[:8000]
        message = design_message(skill, need_file.read_text(encoding="utf-8"), mode, args.insist, previous,
                                 proposal, comments)
        model = args.model or DESIGN_MODEL
        design = {"engine": engine, "model": model, "mode": mode, "insist": bool(args.insist), "started": P.now(),
                  "ended": None, "error": None, "cost_usd": 0.0, "drift": [],
                  "skill": {k: skill[k] for k in ("ref", "version", "sha256")}}
        touch(directory, state, design=design)
        for name in (DESIGN_OUT, DESIGN_TRACE):
            if (directory / name).is_file():
                (directory / name).rename(P.versioned_name(directory / name))
        P.write_atomic(directory / DESIGN_TRACE, message)
        P.say(f"Conception ({mode}) : moteur {engine}, modèle {model}, message ≈ {len(message)} caractères")
        try:
            with P.terminate_as_exit():
                text, cost = P.call_engine(engine, message, model=model, timeout=args.timeout,
                                           budget=args.max_budget_usd, skill=skill,
                                           step_id="concepteur-recette", kind="main")
        except P.EngineError as exc:
            design.update(error=str(exc), ended=P.now(), cost_usd=round(exc.cost, 6))
            touch(directory, state, design=design)
            raise
        P.write_atomic(directory / DESIGN_OUT, text)
        verdict, body = verdict_of(text)
        design.update(ended=P.now(), cost_usd=round(cost, 6))
        recipe, new_proposal = None, None
        if mode == "write":
            block = recipe_block(body)
            recipe = block[2] if block else None
            if recipe:
                keep_version(directory / P.DRAFT_FILE)
                P.write_atomic(directory / P.DRAFT_FILE, recipe)
                design["drift"] = step_drift(proposal, recipe)
                proposal.update(validated=True, validated_at=P.now())
                write_json(directory / PROPOSAL_FILE, proposal)
            else:
                design["error"] = "le concepteur n'a pas rendu de fichier de recette lisible : relancez l'écriture"
            verdict = verdict or ("recipe" if recipe else None)
        else:
            block = proposal_block(body)
            if block:
                new_proposal = dict(block[2], version=int((proposal or {}).get("version") or 0) + 1,
                                    created=P.now(), validated=False, after_comments=comments if mode == "revise" else None)
                if (directory / PROPOSAL_FILE).is_file():
                    (directory / PROPOSAL_FILE).rename(P.versioned_name(directory / PROPOSAL_FILE))
                write_json(directory / PROPOSAL_FILE, new_proposal)
                if (directory / P.DRAFT_FILE).is_file():   # back to the proposal: the old file is kept as recipe.vN.md
                    (directory / P.DRAFT_FILE).rename(P.versioned_name(directory / P.DRAFT_FILE))
                verdict = verdict or "recipe"
            elif verdict == "recipe" or verdict is None:
                design["error"] = "le concepteur n'a pas rendu de proposition lisible : relancez la conception"
            if mode == "revise" and (directory / COMMENTS_FILE).is_file():   # sent: kept with the history
                (directory / COMMENTS_FILE).rename(P.versioned_name(directory / COMMENTS_FILE))
        touch(directory, state, design=design, verdict=verdict)
    check = P.check_recipe_text(recipe) if recipe else None
    return emit(args, {"mode": mode, "verdict": verdict, "has_recipe": bool(recipe),
                       "proposal_steps": len((new_proposal or {}).get("steps") or []),
                       "cost_usd": design["cost_usd"], "errors": check["errors"] if check else [],
                       "drift": design["drift"], "error": design["error"]},
                f"Conception ({mode}) — verdict : {verdict or 'non lu'} ; coût ${design['cost_usd']:.4f}")


# ---------------------------------------------------------------------------
# Proposing a personal recipe to the repository (git, then gh)
# ---------------------------------------------------------------------------
def git_env():
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", LC_ALL="C", LANG="C")
    env.setdefault("GIT_SSH_COMMAND", "ssh -o BatchMode=yes")   # never wait for a password nobody types
    return env


def run_cmd(argv, cwd=None, timeout=GIT_TIMEOUT, env=None):
    try:
        done = subprocess.run(argv, cwd=str(cwd) if cwd else None, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout, env=env or git_env(),
                              stdin=subprocess.DEVNULL)
    except FileNotFoundError:
        raise GitError(f"commande introuvable : {argv[0]}") from None
    except subprocess.TimeoutExpired:
        raise GitError(f"{argv[0]} n'a pas répondu en {timeout} s ({' '.join(argv[1:3])})") from None
    return done.returncode, done.stdout, done.stderr


def git(*argv, cwd=None, timeout=GIT_TIMEOUT, check=True):
    code, out, err = run_cmd(["git", *argv], cwd=cwd, timeout=timeout)
    if check and code != 0:
        raise GitError(f"git {argv[0]} a échoué : {(err or out).strip()[-600:]}")
    return code, out.strip(), err.strip()


def github_slug(url):
    match = re.match(r"(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)([\w.-]+)/([\w.-]+?)(?:\.git)?/?$", url or "")
    return f"{match.group(1)}/{match.group(2)}" if match else None


def contrib_dir(args):
    return recueil(args) / CONTRIB


def contrib_state_path(args, recipe_id):
    return contrib_dir(args) / f"{recipe_id}.json"


def public_contribution(state):
    if not isinstance(state, dict):
        return None
    return {k: state.get(k) for k in ("status", "branch", "source", "remote_url", "github", "pr_url",
                                      "compare_url", "prepared_at", "pushed_at", "worktree", "base")}


def default_source(args):
    config = read_json(contrib_dir(args) / "config.json", {}) or {}
    return config.get("source") or UPSTREAM


def is_url(source):
    return bool(re.match(r"(https?|ssh|file)://|git@[\w.-]+:", source or ""))


def repo_clone(args, source):
    """The clone the contribution branches off: the user's own (a path), or one kept for a URL."""
    if not source or source.startswith("-"):
        raise P.ParcoursError("source invalide : un chemin de clone local ou une adresse git")
    if is_url(source):
        clones = contrib_dir(args) / "clones"
        clone = clones / hashlib.sha1(source.encode("utf-8")).hexdigest()[:12]
        if (clone / ".git").exists():
            git("fetch", "--quiet", "origin", cwd=clone, check=False)
        else:
            clones.mkdir(parents=True, exist_ok=True)
            git("clone", "--quiet", "--", source, str(clone), timeout=GIT_TIMEOUT)
        return clone
    path = Path(source).expanduser()
    if not path.is_absolute() or not path.is_dir():
        raise P.ParcoursError(f"clone introuvable : {source} (chemin absolu d'un clone d'ix-recipes attendu)")
    code, top, _ = git("rev-parse", "--show-toplevel", cwd=path, check=False)
    if code != 0:
        raise P.ParcoursError(f"{path} n'est pas un dépôt git")
    git("fetch", "--quiet", "origin", cwd=path, check=False)   # best effort: offline, the local branch serves
    return Path(top)


def check_clone(clone):
    missing = [name for name in ("build.py", "skills", "dist/.claude-plugin/plugin.json") if not (Path(clone) / name).exists()]
    if missing:
        raise P.ParcoursError(f"{clone} ne ressemble pas à un clone d'ix-recipes (manque : {', '.join(missing)})")


def base_ref(clone):
    """(ref to branch off, name of the target branch for the pull request)."""
    code, out, _ = git("symbolic-ref", "--quiet", "refs/remotes/origin/HEAD", cwd=clone, check=False)
    candidates = ([out.replace("refs/remotes/", "", 1)] if code == 0 and out else []) + ["origin/main", "main", "HEAD"]
    for ref in candidates:
        if git("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}", cwd=clone, check=False)[0] == 0:
            name = ref.split("/", 1)[1] if ref.startswith("origin/") else ("main" if ref == "HEAD" else ref)
            return ref, name
    raise P.ParcoursError(f"{clone} : aucune branche de départ (origin/main, main)")


def build_python():
    """An interpreter that has build.py's two dependencies (pyyaml, jsonschema), or None."""
    candidates = [os.environ.get("IX_RECIPES_PYTHON"), sys.executable, shutil.which("python3")]
    for python in dict.fromkeys(c for c in candidates if c):
        code, _, _ = run_cmd([python, "-c", "import yaml, jsonschema"], timeout=60, env=dict(os.environ))
        if code == 0:
            return python
    return None


MYSTAFFY = {"category": "workflow", "params": {}, "ui": {"simple_fields": [], "advanced_fields": []},
            "kind": "llm", "launch_mode": "run", "transport": "json", "output_format": "markdown",
            "enabled": True, "visibility": "public"}


def remove_worktree(clone, worktree, branch=None, drop_branch=True):
    if worktree and Path(worktree).exists():
        git("worktree", "remove", "--force", str(worktree), cwd=clone, check=False)
        shutil.rmtree(worktree, ignore_errors=True)
    git("worktree", "prune", cwd=clone, check=False)
    if branch and drop_branch:
        git("branch", "-D", branch, cwd=clone, check=False)


def contribute_prepare(args, recipe_id):
    if not shutil.which("git"):
        raise GitError("git n'est pas installé : installez-le (sur Mac : xcode-select --install), puis recommencez. "
                       "Sans git, proposez la recette à la main : envoyez le fichier "
                       f"{recueil(args) / (recipe_id + '.md')} au mainteneur du dépôt.")
    path = personal_path(args, recipe_id)
    text = path.read_text(encoding="utf-8")
    check = P.check_recipe_text(text)
    if check["errors"]:
        raise P.ParcoursError("la recette a des erreurs : " + " ; ".join(check["errors"][:5]))
    if check["contribution"]:
        raise P.ParcoursError("avant de la proposer, complétez l'en-tête : " + " ; ".join(check["contribution"]))
    state_path = contrib_state_path(args, recipe_id)
    old = read_json(state_path)
    if isinstance(old, dict) and old.get("status") == "pushed":
        raise P.ParcoursError(f"déjà proposée (branche {old.get('branch')}) : annulez d'abord pour en préparer une nouvelle")
    source = args.source or default_source(args)
    if isinstance(old, dict) and old.get("status") == "prepared":   # prepared again: the old local branch goes
        remove_worktree(old["clone"], old.get("worktree"), old.get("branch"))
        state_path.unlink(missing_ok=True)
    clone = repo_clone(args, source)
    check_clone(clone)
    ref, base_name = base_ref(clone)
    if git("cat-file", "-e", f"{ref}:skills/{recipe_id}.md", cwd=clone, check=False)[0] == 0:
        raise ExistsError(f"le dépôt contient déjà une recette '{recipe_id}' : changez l'id de la vôtre")
    branch, n = f"recette/{recipe_id}", 2
    while git("rev-parse", "--verify", "--quiet", f"refs/heads/{branch}", cwd=clone, check=False)[0] == 0:
        branch, n = f"recette/{recipe_id}-{n}", n + 1
    worktree = contrib_dir(args) / recipe_id / "ix-recipes"   # named ix-recipes: build.py reads its namespace there
    remove_worktree(clone, worktree, drop_branch=False)
    worktree.parent.mkdir(parents=True, exist_ok=True)
    git("worktree", "add", "--quiet", "-b", branch, str(worktree), ref, cwd=clone)
    state = {"id": recipe_id, "status": "preparing", "source": source, "clone": str(clone), "worktree": str(worktree),
             "branch": branch, "base": base_name, "base_ref": ref, "prepared_at": P.now()}
    write_json(state_path, state)
    try:
        (worktree / "skills" / f"{recipe_id}.md").write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")
        mystaffy = worktree / "skills" / f"{recipe_id}.mystaffy.json"
        mystaffy.write_text(json.dumps(MYSTAFFY, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        python = build_python()
        if not python:
            raise GitError("build.py demande pyyaml et jsonschema, absents de ce Python : installez-les "
                           f"(python3 -m pip install -r {clone}/requirements.txt), ou indiquez un Python qui les a "
                           "dans la variable IX_RECIPES_PYTHON, puis recommencez.")
        logs = []
        for argv in ([python, "build.py", recipe_id, "--validate"], [python, "build.py", recipe_id]):
            code, out, err = run_cmd(argv, cwd=worktree, timeout=300, env=dict(os.environ))
            logs.append(f"$ {' '.join(['python3'] + argv[1:])}\n{out}{err}")
            if code != 0:
                raise GitError(f"build.py refuse la recette :\n{(out + err).strip()[-1500:]}")
        targets = [f"skills/{recipe_id}.md", f"skills/{recipe_id}.mystaffy.json", f"dist/skills/{recipe_id}"]
        git("add", "--", *targets, cwd=worktree)
        _, porcelain, _ = git("status", "--porcelain", cwd=worktree)
        others = [line[3:] for line in porcelain.splitlines() if line[:2].strip() and not any(line[3:].startswith(t) for t in targets)]
        fm, _ = P.parse_recipe_text(text)
        message = (f"Recette personnelle {recipe_id} : {fm.get('label')}\n\n"
                   f"Proposée depuis la page de suivi des parcours (recueil personnel, version {fm.get('version')}) :\n"
                   f"skills/{recipe_id}.md, skills/{recipe_id}.mystaffy.json et dist/skills/{recipe_id}/ "
                   f"(python3 build.py {recipe_id}).\n")
        code, out, err = run_cmd(["git", "commit", "--quiet", "-m", message], cwd=worktree)
        if code != 0:
            if any(k in (out + err).lower() for k in ("tell me who you are", "user.email", "empty ident", "auto-detect")):
                raise GitError("git ne connaît pas votre nom : git config --global user.name \"Prénom Nom\" et "
                               "git config --global user.email vous@exemple.fr, puis recommencez.")
            raise GitError(f"git commit a échoué : {(err or out).strip()[-600:]}")
        _, commit, _ = git("rev-parse", "HEAD", cwd=worktree)
        _, url, _ = git("config", "--get", "remote.origin.url", cwd=worktree, check=False)
        state.update(status="prepared", commit=commit, remote_url=url or None, github=github_slug(url),
                     others=others, build_log="\n".join(logs)[-20000:])
        write_json(state_path, state)
        config = read_json(contrib_dir(args) / "config.json", {}) or {}
        write_json(contrib_dir(args) / "config.json", dict(config, source=source))
    except BaseException:
        remove_worktree(clone, worktree, branch)
        state_path.unlink(missing_ok=True)
        raise
    return contribution_report(state)


def contribution_report(state):
    worktree = Path(state["worktree"])
    diff = ""
    if worktree.is_dir():
        _, diff, _ = git("show", "--stat", "--patch", "--format=commit %H%nAuthor: %an <%ae>%n%n    %s%n", "HEAD",
                         cwd=worktree, check=False)
    report = public_contribution(state)
    report.update(commit=state.get("commit"), others=state.get("others") or [], build_log=state.get("build_log", ""),
                  diff=diff[:DIFF_LIMIT], diff_truncated=len(diff) > DIFF_LIMIT,
                  gh=bool(shutil.which("gh")), message=state.get("message"))
    return report


def contribute_push(args, recipe_id):
    state_path = contrib_state_path(args, recipe_id)
    state = read_json(state_path)
    if not isinstance(state, dict) or state.get("status") != "prepared":
        raise P.ParcoursError("rien de préparé à pousser : « Préparer » d'abord")
    worktree = Path(state["worktree"])
    if not worktree.is_dir():
        raise P.ParcoursError("la copie de travail préparée a disparu : préparez à nouveau")
    _, head, _ = git("rev-parse", "HEAD", cwd=worktree)
    if head != state.get("commit"):
        raise P.StateChanged("la branche a changé depuis le diff affiché : rien n'a été poussé, préparez à nouveau")
    code, out, err = run_cmd(["git", "push", "--quiet", "-u", "origin", state["branch"]], cwd=worktree)
    if code != 0:
        raise GitError(push_failure(state, (err or out).strip()))
    state.update(status="pushed", pushed_at=P.now())
    slug = state.get("github")
    if slug:
        state["compare_url"] = f"https://github.com/{slug}/compare/{state['base']}...{state['branch']}?expand=1"
    message = None
    if slug and shutil.which("gh"):
        fm, _ = P.parse_recipe_text((worktree / "skills" / f"{recipe_id}.md").read_text(encoding="utf-8"))
        body = (f"Recette personnelle `{recipe_id}` ({fm.get('label')}, version {fm.get('version')}), conçue, "
                "testée et validée dans la page de suivi des parcours, proposée depuis le recueil de l'utilisateur.\n\n"
                f"- `skills/{recipe_id}.md`, `skills/{recipe_id}.mystaffy.json`\n"
                f"- `dist/skills/{recipe_id}/` régénéré par `python3 build.py {recipe_id}`\n\n"
                "À vérifier par le mainteneur : la version du plugin (`dist/.claude-plugin/plugin.json`), "
                "le CHANGELOG et les README (FR + EN) ne sont pas modifiés par cette proposition.\n")
        code, out, err = run_cmd(["gh", "pr", "create", "--repo", slug, "--base", state["base"], "--head", state["branch"],
                                  "--title", f"Recette {recipe_id} : {fm.get('label')}", "--body", body],
                                 cwd=worktree, env=dict(os.environ, GH_PROMPT_DISABLED="1"))
        urls = re.findall(r"https://github\.com/\S+/pull/\d+", out + err)
        if code == 0 and urls:
            state["pr_url"] = urls[-1]
        else:
            message = ("Branche poussée, mais gh n'a pas pu ouvrir la demande de fusion "
                       f"({(err or out).strip()[-300:]}). Ouvrez-la depuis l'adresse ci-dessous.")
    elif slug:
        message = "Branche poussée. gh n'est pas installé : ouvrez la demande de fusion depuis l'adresse ci-dessous."
    else:
        message = (f"Branche {state['branch']} poussée vers {state.get('remote_url')}, qui n'est pas sur GitHub : "
                   "ouvrez la demande de fusion depuis l'outil de ce dépôt.")
    state["message"] = message
    write_json(state_path, state)
    return contribution_report(state)


def push_failure(state, stderr):
    low = stderr.lower()
    where = state.get("remote_url") or "origin"
    if any(k in low for k in ("permission", "403", "denied", "authentication failed", "could not read username",
                              "not allowed", "write access")):
        fork = (f" Sans droits d'écriture sur {state['github']}, forkez le dépôt (gh repo fork {state['github']} "
                "--remote), puis poussez la branche sur votre fork et ouvrez la demande de fusion depuis GitHub."
                if state.get("github") else "")
        return (f"Envoi refusé par {where} : pas de droits d'écriture, ou pas d'identifiants.{fork} "
                f"La branche {state['branch']} reste prête dans {state['worktree']}. Détail : {stderr[-300:]}")
    if "could not resolve host" in low or "unable to access" in low or "network" in low:
        return f"Envoi impossible : réseau ou adresse injoignable ({where}). Réessayez plus tard. Détail : {stderr[-300:]}"
    return f"git push a échoué ({where}) : {stderr[-600:]}"


def contribute_cancel(args, recipe_id):
    state_path = contrib_state_path(args, recipe_id)
    state = read_json(state_path)
    if not isinstance(state, dict):
        raise P.NotFound("aucune proposition en cours pour cette recette")
    remove_worktree(state["clone"], state.get("worktree"), state.get("branch"))
    with contextlib.suppress(OSError):
        Path(state["worktree"]).parent.rmdir()
    state_path.unlink(missing_ok=True)
    pushed = state.get("status") == "pushed"
    return {"cancelled": recipe_id, "pushed": pushed,
            "note": f"La branche {state.get('branch')} déjà poussée reste sur le dépôt distant." if pushed else None}


def cmd_contribute(args):
    personal_path(args, args.recipe)
    if args.action == "prepare":
        data = contribute_prepare(args, args.recipe)
    elif args.action == "push":
        data = contribute_push(args, args.recipe)
    elif args.action == "cancel":
        data = contribute_cancel(args, args.recipe)
    else:
        state = read_json(contrib_state_path(args, args.recipe))
        data = contribution_report(state) if isinstance(state, dict) else {"status": None,
                                                                          "default_source": default_source(args)}
    if args.json:
        P.emit_json(data)
    else:
        P.say(json.dumps({k: v for k, v in data.items() if k not in ("diff", "build_log")}, ensure_ascii=False, indent=2))
        if data.get("diff"):
            P.say(data["diff"])
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def emit(args, data, text):
    if args.json:
        P.emit_json(data)
    else:
        P.say(text)
    return 0


def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--parcours-dir", default=os.environ.get("PARCOURS_DIR") or "./parcours",
                        help="dossier des parcours ; le recueil est le dossier recettes/ à côté s'il s'appelle parcours, dedans sinon")
    common.add_argument("--json", action="store_true", help="sortie JSON ; erreurs en {\"error\", \"message\"}")
    parser = argparse.ArgumentParser(description="Recettes personnelles (voir docs/interface.md §9)")
    sub = parser.add_subparsers(dest="command", required=True)

    def add(name, func, help_text, *positionals):
        p = sub.add_parser(name, parents=[common], help=help_text)
        for positional in positionals:
            p.add_argument(positional)
        p.set_defaults(func=func)
        return p

    add("list", cmd_list, "recettes personnelles et brouillons")
    p = add("draft-new", cmd_draft_new, "nouveau brouillon à partir d'un besoin")
    p.add_argument("--input", help="le besoin (fichier, ou - pour l'entrée standard)")
    p.add_argument("--title")
    p.add_argument("--template", action="store_true", help="partir du modèle de recette, sans conception")
    p = add("design", cmd_design, "concevoir la recette (un appel moteur, skill concepteur-recette)", "draft")
    p.add_argument("--mode", choices=DESIGN_MODES, default="propose",
                   help="propose : la chaîne à commenter (défaut) ; revise : avec les commentaires ; write : le fichier, "
                        "d'après la proposition validée")
    p.add_argument("--insist", action="store_true", help="demander une recette même si un skill seul suffit")
    p.add_argument("--engine", choices=DESIGN_ENGINES)
    p.add_argument("--model", choices=sorted(P.WORKFLOW_MODELS))
    p.add_argument("--timeout", type=int, default=P.DEFAULT_TIMEOUT)
    p.add_argument("--max-budget-usd", type=float, default=P.DEFAULT_BUDGET)
    add("show", cmd_show, "un brouillon", "draft")
    p = add("comments", cmd_comments, "enregistrer les commentaires sur la proposition", "draft")
    p.add_argument("--file", required=True, help="JSON {\"general\": texte, \"steps\": {id: texte}}")
    p = add("save", cmd_save, "enregistrer le fichier d'un brouillon (vérifié à chaque fois)", "draft")
    p.add_argument("--file", required=True)
    p.add_argument("--if-sha", help="empreinte du fichier ouvert ; refus s'il a changé depuis")
    p = add("check", cmd_check, "vérifier un fichier de recette")
    p.add_argument("--file", required=True)
    p = add("promote", cmd_promote, "passer le brouillon dans le recueil", "draft")
    p.add_argument("--replace", action="store_true", help="remplacer une recette du recueil qui porte le même id")
    add("edit", cmd_edit, "rouvrir une recette du recueil en brouillon", "recipe")
    add("personal", cmd_personal, "une recette du recueil", "recipe")
    add("retire", cmd_retire, "retirer une recette du recueil (copie gardée)", "recipe")
    add("template", cmd_template, "remplacer le fichier d'un brouillon par le modèle", "draft")
    add("delete-draft", cmd_delete_draft, "supprimer un brouillon et ses essais", "draft")
    add("essai-delete", cmd_essai_delete, "supprimer un dossier de test", "draft", "slug")
    p = add("contribute", cmd_contribute, "proposer une recette au dépôt", "recipe")
    p.add_argument("action", choices=("prepare", "push", "cancel", "status"))
    p.add_argument("--source", help="clone local d'ix-recipes (chemin absolu) ou adresse git ; défaut : le dernier utilisé, sinon GitHub")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    P.PLACES.update(P.recipe_places(args.parcours_dir))
    try:
        return args.func(args)
    except P.ParcoursError as exc:
        if args.json:
            P.emit_json({"error": exc.code, "message": str(exc)})
        else:
            print(f"Erreur : {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        if not args.json:
            raise
        P.emit_json({"error": "unexpected", "message": f"{type(exc).__name__}: {exc}"})
        return 1


if __name__ == "__main__":
    sys.exit(main())
