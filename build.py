#!/usr/bin/env python3
"""
build.py — Multi-target skill builder for ix-recipes.

Usage:
    python build.py                              # all targets, all skills
    python build.py <id>                         # specific skill id, all targets
    python build.py --target agentskills         # dist/skills/<id>/SKILL.md — Claude Cowork + ChatGPT Skills
    python build.py --target cowork              # cowork validation only
    python build.py --target mystaffy            # all skills, mystaffy only
    python build.py --target mystaffy --domain cognitif  # filter by domain
    python build.py <id> --target mystaffy       # specific skill, mystaffy only
    python build.py --target codex               # codex-dist/<id>/SKILL.md
    python build.py <id> --target codex          # specific skill, codex only
    python build.py --validate                   # validate without writing files
"""

import argparse
import json
import shutil
import re
import sys
from pathlib import Path

import yaml
import jsonschema

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SKILLS_DIR = Path("skills")
DIST_DIR = Path("dist")
DIST_SKILLS_DIR = DIST_DIR / "skills"
MYSTAFFY_DIST_DIR = Path("mystaffy-dist")
CODEX_DIST_DIR = Path("codex-dist")
PARTIALS_DIR = Path("partials")
PLUGIN_JSON = DIST_DIR / ".claude-plugin" / "plugin.json"

# ---------------------------------------------------------------------------
# Domain → métier mapping
# ---------------------------------------------------------------------------
DOMAIN_TO_METIER = {
    "cognitif":  ["transverse"],
    "rh":        ["rh"],
    "sales":     ["commercial"],
    "finance":   ["finance"],
    "legal":     ["juridique"],
    "ops":       ["transverse"],
    "data":      ["analyste_data"],
    "strategy":  ["intelligence_strategique"],
    "fondateur": ["fondateur_ceo"],
}

# Reverse mapping — used by --target ix-memory
METIER_TO_DOMAIN = {v[0]: k for k, v in DOMAIN_TO_METIER.items()}
# Extended entries not covered by DOMAIN_TO_METIER values
METIER_TO_DOMAIN.update({
    "achats":                   "ops",
    "commercial":               "sales",
    "intelligence_strategique": "strategy",
    "it_projet":                "ops",
    "fondateur_ceo":            "fondateur",
    "analyste_data":            "data",
})

# ---------------------------------------------------------------------------
# Mystaffy JSON Schema
# ---------------------------------------------------------------------------
MYSTAFFY_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "IX Skill Manifest",
    "type": "object",
    "additionalProperties": False,
    "required": ["id", "label", "version", "description", "kind", "category",
                 "input_types", "output_format", "params", "ui"],
    "properties": {
        "artifact_kind": {"type": "string", "enum": ["skill", "workflow"]},
        "id": {"type": "string", "pattern": "^[a-z0-9_\\-]+$"},
        "label": {"type": "string", "minLength": 1},
        "aliases": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
        "description": {"type": "string", "minLength": 1},
        "icon": {"type": "string"},
        "color": {"type": "string"},
        "enabled": {"type": "boolean"},
        "visibility": {"type": "string", "enum": ["public", "internal"]},
        "metier": {
            "type": "array",
            "items": {"type": "string", "enum": [
                "transverse", "achats", "commercial", "intelligence_strategique",
                "finance", "juridique", "it_projet", "fondateur_ceo", "rh", "analyste_data"
            ]}
        },
        "kind": {"type": "string", "enum": ["local", "llm", "hybrid"]},
        "category": {"type": "string", "enum": [
            "atome", "research", "critique", "decision", "production",
            "import", "pipeline", "internal", "workflow"
        ]},
        "input_types": {"type": "array", "items": {"type": "string"}, "minItems": 1, "uniqueItems": True},
        "output_type": {"type": "string"},
        "output_types": {"type": "array", "items": {"type": "string"}, "minItems": 1, "uniqueItems": True},
        "output_format": {"type": "string", "enum": ["markdown", "json", "html", "pdf", "docx", "pptx", "mixed"]},
        "output_format_dynamic": {
            "type": "object",
            "required": ["param", "map"],
            "properties": {
                "param": {"type": "string"},
                "map": {"type": "object"}
            }
        },
        "params": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "required": ["label", "type", "required"],
                "properties": {
                    "label": {"type": "string"},
                    "type": {"type": "string", "enum": ["string", "text", "boolean", "number", "enum", "multiselect", "file"]},
                    "required": {"type": "boolean"},
                    "default": {},
                    "help": {"type": "string"},
                    "values": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
                    "placeholder": {"type": "string"},
                    "min": {"type": "number"},
                    "max": {"type": "number"}
                }
            }
        },
        "ui": {
            "type": "object",
            "required": ["simple_fields", "advanced_fields"],
            "properties": {
                "simple_fields": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
                "advanced_fields": {"type": "array", "items": {"type": "string"}, "uniqueItems": True}
            }
        },
        "execution": {
            "type": "object",
            "properties": {
                "supports_async": {"type": "boolean"},
                "supports_review_gate": {"type": "boolean"},
                "max_input_artifacts": {"type": "integer"},
                "max_estimated_tokens": {"type": "integer"}
            }
        },
        "launch_mode": {"type": "string", "enum": ["run", "direct_api"]},
        "transport": {"type": "string", "enum": ["json", "multipart"]},
        "endpoint": {"type": "string", "pattern": "^/"},
        "uses_partials": {"type": "array", "items": {"type": "string"}, "uniqueItems": True},
        "tools": {"type": "array", "items": {"type": "string"}, "uniqueItems": True}
    },
    "allOf": [
        {
            "oneOf": [
                {"required": ["output_type"], "not": {"required": ["output_types"]}},
                {"required": ["output_types"], "not": {"required": ["output_type"]}}
            ]
        },
        {
            "if": {"properties": {"launch_mode": {"const": "direct_api"}}, "required": ["launch_mode"]},
            "then": {"required": ["endpoint"]}
        }
    ]
}

# ---------------------------------------------------------------------------
# Skill parsing
# ---------------------------------------------------------------------------

def parse_skill(path: Path):
    """Parse a skill .md file, returning (frontmatter_dict, body_str).
    Raises ValueError on parse errors.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"No YAML frontmatter found in {path}")
    # Find closing ---
    end = text.find("\n---\n", 3)
    if end == -1:
        raise ValueError(f"Unclosed frontmatter in {path}")
    fm_text = text[3:end]
    body = text[end + 5:]  # skip \n---\n
    body = body.lstrip("\n")
    fm = yaml.safe_load(fm_text)
    if not isinstance(fm, dict):
        raise ValueError(f"Frontmatter is not a mapping in {path}")
    return fm, body


def load_skills(skill_id=None, domain=None):
    """Return list of (path, frontmatter, body) for selected skills.
    Returns (skills_list, errors_count).
    """
    if skill_id:
        paths = [SKILLS_DIR / f"{skill_id}.md"]
    else:
        paths = sorted(p for p in SKILLS_DIR.glob("*.md") if p.name != "README.md")

    skills = []
    errors = 0
    for path in paths:
        if not path.exists():
            print(f"  Error: skill '{path.stem}' not found at {path}")
            errors += 1
            continue
        if path.name == "README.md":
            continue
        try:
            fm, body = parse_skill(path)
        except Exception as e:
            print(f"  Error parsing {path}: {e}")
            errors += 1
            continue
        if domain and fm.get("domain") != domain:
            continue
        wf_errors = validate_workflow(fm, body)
        if wf_errors:
            for msg in wf_errors:
                print(f"  Error in workflow of {path.stem}: {msg}")
            errors += len(wf_errors)
            continue
        skills.append((path, fm, body))
    return skills, errors


# ---------------------------------------------------------------------------
# Workflow recipes (docs/format-recette.md in ix-recipes)
# ---------------------------------------------------------------------------
SIBLING_SKILL_DIRS = {
    "ix-skills": Path("../ix-skills/skills"),
    "ix-recipes": Path("../ix-recipes/skills"),
}
PAUSES = {"none", "validate", "answers", "choose"}
MODELS = {"sonnet", "opus", "haiku"}


def _skill_exists(ref: str):
    """True / False if checkable, None if the sibling repo is not present."""
    if ":" not in ref:
        return False
    ns, sid = ref.split(":", 1)
    local_ns = Path.cwd().name
    if ns == local_ns:
        return (SKILLS_DIR / f"{sid}.md").is_file()
    d = SIBLING_SKILL_DIRS.get(ns)
    if d is None:
        return False
    if not d.is_dir():
        return None
    return (d / f"{sid}.md").is_file()


def validate_workflow(fm: dict, body: str) -> list:
    """Mechanical checks of a workflow recipe; returns a list of error messages."""
    wf = fm.get("workflow")
    if not wf:
        return []
    errs = []
    requires = fm.get("requires") or []
    for ref in requires:
        ok = _skill_exists(ref)
        if ok is False:
            errs.append(f"requires '{ref}' does not exist")
        elif ok is None:
            print(f"  Warning: cannot check '{ref}' (sibling repo not found next to this one)")
    steps = wf.get("steps") or []
    if not steps:
        return errs + ["workflow has no steps"]
    seen, transmitted, answers_ready = set(), {}, False
    for i, st in enumerate(steps):
        sid = st.get("id")
        if not sid or sid in seen:
            errs.append(f"step {i + 1}: missing or duplicate id '{sid}'")
        seen.add(sid)
        skill = st.get("skill")
        if skill not in requires:
            errs.append(f"step '{sid}': skill '{skill}' is not listed in requires")
        if skill and f"`{skill}`" not in body:
            errs.append(f"step '{sid}': skill '{skill}' is not cited in the body")
        if not st.get("mission"):
            errs.append(f"step '{sid}': no mission")
        if "label" in st and not (isinstance(st["label"], str) and st["label"].strip()):
            errs.append(f"step '{sid}': label must be a non-empty string (shown to the user, in French)")
        if st.get("model", "sonnet") not in MODELS:
            errs.append(f"step '{sid}': model must be one of {sorted(MODELS)}")
        if st.get("pause", "none") not in PAUSES:
            errs.append(f"step '{sid}': pause must be one of {sorted(PAUSES)}")
        if st.get("output_field") and st["output_field"] not in (st.get("transmits") or []):
            errs.append(f"step '{sid}': output_field '{st['output_field']}' is not in transmits")
        verbatim = st.get("verbatim") or []
        if verbatim and i != 0:
            errs.append(f"step '{sid}': only the first step may declare verbatim fields (it alone reads the raw input)")
        for field in verbatim:
            if field not in (st.get("transmits") or []):
                errs.append(f"step '{sid}': verbatim field '{field}' is not in transmits")
        if st.get("produces_context_sheet") and i != 0:
            errs.append(f"step '{sid}': only the first step produces the context sheet")
        for src in st.get("receives") or []:
            if src == "brief":
                if i != 0:
                    errs.append(f"step '{sid}': only the first step may receive the raw brief")
            elif src == "context_sheet":
                if i == 0:
                    errs.append("the first step cannot receive the context sheet it produces")
            elif src == "answers":
                if not answers_ready:
                    errs.append(f"step '{sid}': receives answers before any step with pause 'answers'")
            elif "." in src:
                prev, field = src.split(".", 1)
                if field not in transmitted.get(prev, ()):
                    errs.append(f"step '{sid}': '{src}' is not transmitted by an earlier step")
            else:
                errs.append(f"step '{sid}': unknown source '{src}'")
        transmitted[sid] = set(st.get("transmits") or [])
        if st.get("pause") == "answers":
            answers_ready = True
    labels = wf.get("context_labels") or {}
    if not isinstance(labels, dict) or any(k not in (wf.get("context_sheet") or []) or not isinstance(v, str) or not v.strip()
                                           for k, v in labels.items()):
        errs.append("context_labels must map context_sheet keys to non-empty labels (shown to the user, in French)")
    if "summary_fr" in fm and not (isinstance(fm["summary_fr"], str) and fm["summary_fr"].strip()):
        errs.append("summary_fr must be a non-empty string (one sentence shown to the user)")
    if not steps[0].get("produces_context_sheet"):
        errs.append("the first step must produce the context sheet (produces_context_sheet: true)")
    return errs


# ---------------------------------------------------------------------------
# Target: agentskills (Claude Cowork + ChatGPT Skills \u2014 shared Agent Skills format)
# ---------------------------------------------------------------------------
# Replaces the old `claude-ai` target (zipped .skill with untransformed
# frontmatter \u2014 invalid). Emits open dist/skills/<id>/SKILL.md directories,
# serving both Cowork and ChatGPT Skills.
_AGENTSKILL_NAME_RE = re.compile(r"^[a-z0-9-]+$")


def _agentskill_md(fm: dict, body: str) -> str:
    """Render an Agent Skills-compatible SKILL.md (name + description frontmatter, unchanged body)."""
    name = fm["id"]
    if not _AGENTSKILL_NAME_RE.match(name):
        raise ValueError(f"id '{name}' does not match Agent Skills name pattern ^[a-z0-9-]+$")
    # Full description, not just the first sentence: in this repo's frontmatter,
    # description_en carries its trigger phrases ("Triggers when\u2026") after the
    # first sentence, and Agent Skills has no separate `triggers:` field \u2014
    # `description` is the only surface Claude matches against.
    description = fm.get("description_en", fm.get("description_fr", ""))
    if not description:
        raise ValueError(f"skill '{name}' has no description_en/description_fr")
    description = json.dumps(description)  # safe JSON string = valid YAML scalar

    lines = ["---", f"name: {name}", f"description: {description}", "---", ""]
    return "\n".join(lines) + body


def build_agentskills(skills: list, dry_run: bool = False) -> int:
    """Build Agent Skills-compatible SKILL.md files into dist/skills/<id>/SKILL.md.

    dist/ is the plugin root (dist/.claude-plugin/plugin.json); skills live in
    the default skills/<id>/SKILL.md layout so Cowork/claude.ai auto-discover
    them \u2014 the web validator does not reliably support custom `skills` paths.
    Serves both Claude Cowork and ChatGPT Skills (same Agent Skills format).
    """
    print(f"\nTarget: agentskills ({len(skills)} skill(s))")
    errors = 0
    for path, fm, body in skills:
        dry_tag = " [dry-run]" if dry_run else ""
        skill_id = fm.get("id", path.stem)
        try:
            skill_id = fm["id"]
            out_dir = DIST_SKILLS_DIR / skill_id
            out_file = out_dir / "SKILL.md"
            content = _agentskill_md(fm, body)
            if not dry_run:
                out_dir.mkdir(parents=True, exist_ok=True)
                out_file.write_text(content, encoding="utf-8")
            _write_references(fm, out_dir, dry_run)
            _write_recipe_json(fm, out_dir, dry_run)
            _write_bundled_scripts(fm, out_dir, dry_run)
            print(f"  \u2713 agentskills {skill_id:<20} \u2192 dist/skills/{skill_id}/SKILL.md{dry_tag}")
        except Exception as e:
            print(f"  \u2717 agentskills {skill_id:<20} \u2192 {e}")
            errors += 1
    return errors


RECIPE_JSON_KEYS = ("id", "label", "version", "summary_fr", "description_fr", "icon", "workflow")


def _write_recipe_json(fm: dict, out_dir: Path, dry_run: bool) -> None:
    """A workflow recipe ships its `workflow` block next to its SKILL.md, as recipe.json.

    SKILL.md keeps the Agent Skills front matter (name, description) that the Cowork
    validator accepts; the runner bundled in the plugin (scripts/parcours.py, see
    `scripts` below) reads the steps from recipe.json and the body from SKILL.md.
    """
    target = out_dir / "recipe.json"
    if dry_run:
        return
    if not fm.get("workflow"):
        if target.is_file():
            target.unlink()
        return
    data = {k: fm[k] for k in RECIPE_JSON_KEYS if k in fm}
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _write_bundled_scripts(fm: dict, out_dir: Path, dry_run: bool) -> None:
    """Copy the repository files a skill lists in `scripts` into <out_dir>/scripts/ (rebuilt
    from scratch): an Agent Skill may bundle the code it runs. A file lands under its own
    name; a folder (a theme, say `themes/inflexion`) keeps its path below scripts/."""
    names = fm.get("scripts") or []
    for name in names:
        if not Path(name).exists():
            raise FileNotFoundError(f"script '{name}' not found")
    if dry_run:
        return
    folder = out_dir / "scripts"
    if folder.is_dir():
        shutil.rmtree(folder)
    if names:
        folder.mkdir(parents=True)
        for name in names:
            if Path(name).is_dir():
                shutil.copytree(name, folder / name)
            else:
                shutil.copy2(name, folder / Path(name).name)


def _write_references(fm: dict, out_dir: Path, dry_run: bool) -> list:
    """Copy the partials listed in `references` next to the SKILL.md.

    Progressive disclosure: partials/<name>.md lands in <out_dir>/references/,
    and the skill body tells the model which one to read when — so a skill can
    ship eight domain annexes while the model loads only the one it needs.
    The references/ folder is rebuilt from scratch on every build.
    """
    names = fm.get("references") or []
    for name in names:
        if not (PARTIALS_DIR / f"{name}.md").is_file():
            raise FileNotFoundError(f"reference '{name}' not found in {PARTIALS_DIR}/")
    if dry_run:
        return names
    ref_dir = out_dir / "references"
    if ref_dir.is_dir():
        shutil.rmtree(ref_dir)
    if names:
        ref_dir.mkdir(parents=True)
        for name in names:
            shutil.copyfile(PARTIALS_DIR / f"{name}.md", ref_dir / f"{name}.md")
    return names


# ---------------------------------------------------------------------------
# Target: cowork
# ---------------------------------------------------------------------------

def build_cowork(dry_run=False):
    print("\nTarget: cowork")
    errors = 0
    dry_tag = " [dry-run]" if dry_run else ""
    if not PLUGIN_JSON.exists():
        print(f"  \u2717 cowork: {PLUGIN_JSON} not found{dry_tag}")
        return 1
    try:
        data = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"  \u2717 cowork: {PLUGIN_JSON} invalid JSON — {e}{dry_tag}")
        return 1
    missing = [f for f in ("name", "version") if f not in data]
    # No `skills` field required: the plugin root is dist/, so skills are
    # auto-discovered from the default dist/skills/<id>/SKILL.md layout.
    if "skills" in data:
        print(f"  ✗ cowork: {PLUGIN_JSON} has a custom 'skills' field — remove it, "
              f"the Cowork web validator only supports default skills/ discovery{dry_tag}")
        errors += 1
    if missing:
        print(f"  \u2717 cowork: {PLUGIN_JSON} missing fields: {', '.join(missing)}{dry_tag}")
        errors += 1
    else:
        print(f"  \u2713 cowork: {PLUGIN_JSON} valid{dry_tag}")
    return errors


# ---------------------------------------------------------------------------
# Target: mystaffy
# ---------------------------------------------------------------------------

def build_mystaffy_manifest(fm):
    """Build a mystaffy manifest dict from frontmatter (steps 1–3)."""
    manifest = {
        "enabled": True,
        "visibility": "public",
        "launch_mode": "run",
        "transport": "json",
        "kind": "llm",
        "output_format": "markdown",
        "params": {},
        "ui": {"simple_fields": [], "advanced_fields": []},
    }

    # Step 2: map from frontmatter
    manifest["id"] = fm["id"]
    manifest["label"] = fm["label"]
    manifest["version"] = fm["version"]
    manifest["description"] = fm["description_fr"]
    if "icon" in fm:
        manifest["icon"] = fm["icon"]
    manifest["metier"] = DOMAIN_TO_METIER.get(fm.get("domain", ""), ["transverse"])
    manifest["input_types"] = fm["input_types"]
    output_types = fm.get("output_types", [])
    if len(output_types) == 1:
        manifest["output_type"] = output_types[0]
    else:
        manifest["output_types"] = output_types
    if "category" in fm:
        manifest["category"] = fm["category"]

    # Step 3: override from skills/<id>.mystaffy.json if present
    override_path = SKILLS_DIR / f"{fm['id']}.mystaffy.json"
    if override_path.exists():
        override = json.loads(override_path.read_text(encoding="utf-8"))
        manifest.update(override)

    return manifest


def build_mystaffy(skills, dry_run=False):
    print(f"\nTarget: mystaffy ({len(skills)} skill(s))")
    errors = 0
    for path, fm, body in skills:
        skill_id = fm["id"]
        out_dir = MYSTAFFY_DIST_DIR / skill_id
        dry_tag = " [dry-run]" if dry_run else ""
        try:
            manifest = build_mystaffy_manifest(fm)
            # Validate
            jsonschema.validate(manifest, MYSTAFFY_SCHEMA)
            if not dry_run:
                MYSTAFFY_DIST_DIR.mkdir(exist_ok=True)
                out_dir.mkdir(exist_ok=True)
                (out_dir / "manifest.json").write_text(
                    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8"
                )
                (out_dir / "skill.md").write_text(body, encoding="utf-8")
            print(f"  \u2713 mystaffy   {skill_id:<12} \u2192 mystaffy-dist/{skill_id}/{dry_tag}")
        except jsonschema.ValidationError as e:
            print(f"  \u2717 mystaffy   {skill_id:<12} \u2192 schema error: {e.message}")
            errors += 1
        except Exception as e:
            print(f"  \u2717 mystaffy   {skill_id:<12} \u2192 {e}")
            errors += 1
    return errors


# ---------------------------------------------------------------------------
# Target: ix-memory
# ---------------------------------------------------------------------------

def build_ix_memory(skills: list, dry_run: bool = False) -> None:
    """Reconstruct ix-memory format (manifest.json + skill.md) from ix-recipes canonical source."""
    for _path, frontmatter, body in skills:
        skill_id = frontmatter["id"]

        mystaffy_path = SKILLS_DIR / f"{skill_id}.mystaffy.json"
        if not mystaffy_path.exists():
            print(f"  WARN: no .mystaffy.json for {skill_id}, skipping ix-memory build")
            continue

        mystaffy_data = json.loads(mystaffy_path.read_text(encoding="utf-8"))

        # Reconstruct manifest
        manifest: dict = {
            "id": frontmatter["id"],
            "label": frontmatter["label"],
            "version": frontmatter.get("version", "1.0.0"),
            "description": frontmatter.get("description_fr", ""),
            "icon": frontmatter.get("icon", "○"),
            "kind": mystaffy_data.get("kind", "llm"),
            "category": mystaffy_data.get("category", frontmatter.get("category", "atome")),
            "input_types": frontmatter.get("input_types", []),
            "output_format": mystaffy_data.get("output_format", "markdown"),
            "params": mystaffy_data.get("params", {}),
            "ui": mystaffy_data.get("ui", {"simple_fields": [], "advanced_fields": []}),
        }

        # Preserve bilingual descriptions if present
        if frontmatter.get("description_fr"):
            manifest["description_fr"] = frontmatter["description_fr"]
        if frontmatter.get("description_en"):
            manifest["description_en"] = frontmatter["description_en"]

        # output_type vs output_types
        output_types = frontmatter.get("output_types", [])
        if len(output_types) == 1:
            manifest["output_type"] = output_types[0]
        elif len(output_types) > 1:
            manifest["output_types"] = output_types

        # Optional fields from .mystaffy.json
        for field in ["metier", "uses_partials", "execution", "color", "launch_mode",
                      "transport", "enabled", "visibility", "aliases"]:
            if field in mystaffy_data:
                manifest[field] = mystaffy_data[field]

        # aliases from frontmatter override
        if frontmatter.get("aliases"):
            manifest["aliases"] = frontmatter["aliases"]

        if dry_run:
            print(f"  [dry-run] ix-memory: mystaffy-dist/{skill_id}/")
            continue

        out_dir = MYSTAFFY_DIST_DIR / skill_id
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "manifest.json").write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_dir / "skill.md").write_text(body, encoding="utf-8")
        print(f"  OK ix-memory: {skill_id}")


# ---------------------------------------------------------------------------
# Target: codex
# ---------------------------------------------------------------------------

# Words too generic to be useful as triggers
_CODEX_STOPWORDS = {
    "and", "the", "for", "from", "with", "into", "that", "does", "not", "any",
    "all", "this", "your", "before", "after", "when", "what", "how", "its",
    "without", "produce", "build", "create", "generate", "make", "structured",
    "clear", "based", "using", "used", "will", "than", "more", "less", "each",
    "have", "been", "also", "only", "then", "them", "their", "they", "turn",
    "into", "over", "under", "about", "across",
}


def _first_sentence(text: str) -> str:
    """Return the first sentence of text, capped at 120 chars."""
    if not text:
        return ""
    for sep in (". ", ".\n", "? ", "! "):
        idx = text.find(sep)
        if idx != -1:
            return text[: idx + 1].strip()
    return text[:120].strip()


def _codex_triggers(fm: dict) -> list:
    """Generate Codex trigger strings from ix-recipes frontmatter.

    Strategy:
      1. The skill id (always first).
      2. Meaningful parts of the id (split on '-').
      3. Words from the label.
      4. Key words from the first sentence of description_en.
    Capped at 8 triggers.
    """
    triggers: list = []

    skill_id = fm["id"]
    triggers.append(skill_id)

    for part in skill_id.split("-"):
        if len(part) > 3 and part not in triggers:
            triggers.append(part)

    label = fm.get("label", "").lower()
    for word in re.findall(r"[a-z]+", label):
        if len(word) > 3 and word not in _CODEX_STOPWORDS and word not in triggers:
            triggers.append(word)

    desc_en = fm.get("description_en", fm.get("description_fr", ""))
    first = _first_sentence(desc_en).lower()
    for word in re.findall(r"[a-z]+", first):
        if len(word) > 4 and word not in _CODEX_STOPWORDS and word not in triggers:
            triggers.append(word)
        if len(triggers) >= 8:
            break

    return triggers[:8]


def _codex_skill_md(fm: dict, body: str) -> str:
    """Render a Codex-compatible SKILL.md (Codex frontmatter + ix-recipes body)."""
    name = fm["id"]
    description = _first_sentence(
        fm.get("description_en", fm.get("description_fr", ""))
    )
    description = json.dumps(description)  # safe JSON string = valid YAML scalar

    triggers = _codex_triggers(fm)
    lines = ["---", f"name: {name}", f"description: {description}", "triggers:"]
    for t in triggers:
        lines.append(f"  - {t}")
    lines += ["---", ""]
    return "\n".join(lines) + body


def build_codex(skills: list, dry_run: bool = False) -> int:
    """Build Codex-compatible SKILL.md files into codex-dist/<id>/SKILL.md."""
    print(f"\nTarget: codex ({len(skills)} skill(s))")
    errors = 0
    for _path, fm, body in skills:
        skill_id = fm["id"]
        out_dir = CODEX_DIST_DIR / skill_id
        out_file = out_dir / "SKILL.md"
        dry_tag = " [dry-run]" if dry_run else ""
        try:
            content = _codex_skill_md(fm, body)
            if not dry_run:
                CODEX_DIST_DIR.mkdir(exist_ok=True)
                out_dir.mkdir(exist_ok=True)
                out_file.write_text(content, encoding="utf-8")
            _write_references(fm, out_dir, dry_run)
            print(f"  \u2713 codex      {skill_id:<20} \u2192 codex-dist/{skill_id}/SKILL.md{dry_tag}")
        except Exception as e:
            print(f"  \u2717 codex      {skill_id:<20} \u2192 {e}")
            errors += 1
    return errors


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Multi-target skill builder for ix-recipes.",
        add_help=True,
    )
    parser.add_argument(
        "skill_id",
        nargs="?",
        default=None,
        help="Specific skill id to build (optional)",
    )
    parser.add_argument(
        "--target",
        choices=["agentskills", "cowork", "mystaffy", "ix-memory", "codex"],
        default=None,
        help="Build target (default: all)",
    )
    parser.add_argument(
        "--domain",
        default=None,
        help="Filter skills by domain (mystaffy only)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate without writing files (dry-run)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    dry_run = args.validate
    total_errors = 0

    targets = [args.target] if args.target else ["cowork", "agentskills", "mystaffy", "ix-memory", "codex"]

    # --- cowork (repo-level, not per-skill) ---
    if "cowork" in targets:
        total_errors += build_cowork(dry_run=dry_run)

    # --- skill-based targets ---
    skill_targets = [t for t in targets if t != "cowork"]
    if skill_targets:
        # If skill_id given and not found, exit 1
        if args.skill_id:
            skill_path = SKILLS_DIR / f"{args.skill_id}.md"
            if not skill_path.exists():
                print(f"Error: skill '{args.skill_id}' not found at {skill_path}")
                sys.exit(1)

        skills, parse_errors = load_skills(skill_id=args.skill_id, domain=args.domain)
        total_errors += parse_errors

        if "agentskills" in skill_targets:
            total_errors += build_agentskills(skills, dry_run=dry_run)

        if "mystaffy" in skill_targets:
            total_errors += build_mystaffy(skills, dry_run=dry_run)

        if "ix-memory" in skill_targets:
            build_ix_memory(skills, dry_run=dry_run)

        if "codex" in skill_targets:
            total_errors += build_codex(skills, dry_run=dry_run)

    print()
    if total_errors > 0:
        print(f"{total_errors} error(s) found.")
        sys.exit(1)
    else:
        if dry_run:
            print("Validation passed.")
        else:
            print("Done.")


if __name__ == "__main__":
    main()
