"""
Tests of the personal recipes (scripts/recettes.py, and what parcours.py does for them).

Run:  cd ~/Projets/ix-recipes && python3 -m unittest tests.test_recettes -v

No real engine is ever called (the `fake` engine for the design call, `simulation`
for the test dossiers), and no real remote is ever touched: the proposal to the
repository runs against a throwaway bare repository in a temporary folder, and the
GitHub path against a fake `gh` placed first in PATH.

The parity tests compare the standard-library YAML reader with pyyaml, and the
French port of the workflow checks with build.py's validate_workflow; they are
skipped when pyyaml is not installed.
"""

import contextlib
import copy
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import types
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "tests"))

import parcours  # noqa: E402
import recettes  # noqa: E402
import test_parcours as tp  # noqa: E402

try:
    import yaml
except ImportError:  # the parity tests need pyyaml
    yaml = None


def frontmatter_text(path):
    match = parcours.FRONTMATTER_RE.match(Path(path).read_text(encoding="utf-8"))
    return match.group(1) if match else None


def personal_recipe(recipe_id="ma-recette", **changes):
    """The blank model under another id, with optional textual replacements (old -> new)."""
    text = recettes.TEMPLATE.replace("id: ma-recette", f"id: {recipe_id}", 1)
    for old, new in changes.items():
        text = text.replace(old.replace("__", " "), new)
    return text


DESIGN_OUTPUT = """## A. Verdict

Une recette se justifie : les réponses du manager changent la suite.

````markdown
{recipe}````

## Rationale

Le cadrage d'abord, puis le livrable.

## VERDICT
recipe
"""

SINGLE_SKILL_OUTPUT = """## A. Verdict

Un skill seul suffit : utilisez `ix-skills:brief` avec le mail du manager.

## VERDICT
single_skill
"""


# ---------------------------------------------------------------------------
# The YAML subset, against pyyaml
# ---------------------------------------------------------------------------
@unittest.skipUnless(yaml, "pyyaml is not installed")
class YamlSubsetParityTests(unittest.TestCase):
    def test_every_front_matter_of_both_repositories_reads_the_same(self):
        files = sorted((REPO / "skills").glob("*.md"))
        sibling = REPO.parent / "ix-skills" / "skills"
        files += sorted(sibling.glob("*.md")) if sibling.is_dir() else []
        checked = 0
        for path in files:
            text = frontmatter_text(path)
            if text is None:
                continue
            with self.subTest(path=path.name):
                self.assertEqual(parcours.load_yaml_subset(text), yaml.safe_load(text))
                checked += 1
        self.assertGreater(checked, 50)

    def test_the_constructs_of_a_recipe(self):
        cases = [
            "a: [x, 'y, z', \"q\\u00e9\"]\nb:\n  - k: 1\n    l: [1, 2]\n  - - n\n    - m\n",
            "c: |\n  line1\n   line2\n\n  line3\nd: >-\n  fold\n  this\n\n  para\n",
            "e: 'it''s'\nf: \"multi\n  line\"\ng: plain\n  continued\nh: {a: 1, b: [x]}\n",
            "i: ~\nj: yes\nk: 2026-10-15\nl: 1.4.0\nm: 1.5\n# comment\nn: value # trailing\no:\np: -5\nq: \"\"\n",
            "r: |+\n  keep\n\ns: x\n",
            "steps:\n- id: a\n  receives: [brief]\n- id: b\n",
            "k: >\n  a\n  b\n\n    indented\n  c\n",
            "requires: [ix-skills:cadrage,\n  ix-skills:brief]\nempty: []\n",
            "description: \"Triggers on \\\"x\\\", — see `y`.\"\nicon: ⇢\n",
            "key:\n  some text\n  more\nother:\n  'quoted'\nlist:\n  - a\n",
        ]
        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(parcours.load_yaml_subset(text), yaml.safe_load(text))

    def test_what_pyyaml_refuses_is_refused_with_its_line(self):
        for text, line in (("a: 1\nb: c: d\n", 2), ("a: [1, 2\n", 2), ("a: 'x\n", 1), ("a: 1\n  b: 2\n", 2)):
            with self.subTest(text=text):
                with self.assertRaises(yaml.YAMLError):
                    yaml.safe_load(text)
                with self.assertRaises(parcours.YamlSubsetError) as raised:
                    parcours.load_yaml_subset(text)
                self.assertIn("ligne", str(raised.exception))
        with self.assertRaises(parcours.YamlSubsetError) as raised:
            parcours.load_yaml_subset("a: 1\nb: &anchor 2\n")
        self.assertIn("ligne 2", str(raised.exception))

    def test_without_pyyaml_the_runner_reads_the_recipes_of_the_repository(self):
        with mock.patch.object(parcours, "yaml", None):
            recipe = parcours.load_recipe("brief-client")
        self.assertEqual([s["id"] for s in recipe["steps"]], ["cadrage", "questioning", "explorer", "decision", "brief"])
        self.assertEqual(recipe["context_labels"]["named_solutions"], "Solutions déjà nommées")


# ---------------------------------------------------------------------------
# The workflow checks, against build.py
# ---------------------------------------------------------------------------
def import_build():
    """build.py as a module; its jsonschema import is stubbed when absent (validate_workflow does not use it)."""
    if "jsonschema" not in sys.modules:
        try:
            import jsonschema  # noqa: F401
        except ImportError:
            sys.modules["jsonschema"] = types.ModuleType("jsonschema")
    sys.path.insert(0, str(REPO))
    try:
        import build
    finally:
        sys.path.remove(str(REPO))
    return build


def mutations(fm):
    """Broken variants of a workflow recipe, one rule each."""
    steps = fm["workflow"]["steps"]
    second = steps[1]["id"]
    out = []

    def variant(change):
        clone = copy.deepcopy(fm)
        change(clone)
        out.append(clone)

    variant(lambda f: f["workflow"]["steps"][1].update(id=f["workflow"]["steps"][0]["id"]))
    variant(lambda f: f["workflow"]["steps"][1].update(skill="ix-skills:not-required"))
    variant(lambda f: f["workflow"]["steps"][1].pop("mission"))
    variant(lambda f: f["workflow"]["steps"][1].update(label=""))
    variant(lambda f: f["workflow"]["steps"][1].update(model="gpt"))
    variant(lambda f: f["workflow"]["steps"][1].update(pause="later"))
    variant(lambda f: f["workflow"]["steps"][1].update(output_field="nope"))
    variant(lambda f: f["workflow"]["steps"][1].update(verbatim=[f["workflow"]["steps"][1]["transmits"][0]]))
    variant(lambda f: f["workflow"]["steps"][0].update(verbatim=["not_transmitted"]))
    variant(lambda f: f["workflow"]["steps"][1].update(produces_context_sheet=True))
    variant(lambda f: f["workflow"]["steps"][1]["receives"].append("brief"))
    variant(lambda f: f["workflow"]["steps"][0]["receives"].append("context_sheet"))
    variant(lambda f: f["workflow"]["steps"][0]["receives"].append("answers"))
    variant(lambda f: f["workflow"]["steps"][1]["receives"].append(f"{second}.later"))
    variant(lambda f: f["workflow"]["steps"][1]["receives"].append("whatever"))
    variant(lambda f: f["workflow"].update(context_labels={"not_a_key": "x"}))
    variant(lambda f: f.update(summary_fr=""))
    variant(lambda f: f["workflow"]["steps"][0].pop("produces_context_sheet"))
    variant(lambda f: f["workflow"].update(steps=[]))
    variant(lambda f: f.update(requires=f["requires"] + ["ix-skills:does-not-exist"]))
    variant(lambda f: f["workflow"].pop("format"))
    variant(lambda f: f["workflow"].update(format=2))
    variant(lambda f: f["workflow"].update(format="un"))
    return out


@unittest.skipUnless(yaml, "pyyaml is not installed")
class WorkflowCheckParityTests(unittest.TestCase):
    def setUp(self):
        self.build = import_build()

    def compare(self, fm, body):
        def exists(ref):
            return "does-not-exist" not in ref

        with mock.patch.object(self.build, "_skill_exists", exists):
            theirs = self.build.validate_workflow(fm, body)
        mine = parcours.workflow_errors(fm, body, exists, require_format=True)
        self.assertEqual(len(mine), len(theirs), f"build.py: {theirs}\nparcours.py: {mine}")
        return mine

    def test_same_verdict_as_build_py_on_every_recipe_and_its_broken_variants(self):
        recipes = 0
        for path in sorted((REPO / "skills").glob("*.md")):
            fm, body = self.build.parse_skill(path)
            if not fm.get("workflow"):
                continue
            recipes += 1
            with self.subTest(recipe=path.stem):
                self.assertEqual(self.compare(fm, body), [])
            for n, broken in enumerate(mutations(fm)):
                with self.subTest(recipe=path.stem, mutation=n):
                    self.assertTrue(self.compare(broken, body))
        self.assertGreaterEqual(recipes, 2)

    def test_a_skill_missing_from_the_body_is_an_error_for_both(self):
        fm, body = self.build.parse_skill(REPO / "skills" / "brief-client.md")
        self.assertTrue(self.compare(fm, body.replace("`ix-skills:brief`", "brief")))

    def test_build_py_wants_format_1(self):
        fm, body = self.build.parse_skill(REPO / "skills" / "brief-client.md")
        self.assertEqual(fm["workflow"]["format"], 1)
        self.assertEqual(self.compare(fm, body), [])
        missing = copy.deepcopy(fm)
        missing["workflow"].pop("format")
        self.assertEqual(self.compare(missing, body), ["pas de champ format dans le bloc workflow : la recette est lue comme "
                                                       "format 1 (ajoutez « format: 1 » en tête du bloc workflow)"])
        with mock.patch.object(self.build, "_skill_exists", lambda ref: True):
            self.assertIn("ajoutez « format: 1 »", self.build.validate_workflow(missing, body)[0])
            for value in (2, "deux"):
                newer = copy.deepcopy(fm)
                newer["workflow"]["format"] = value
                newer["workflow"]["steps"][1]["pause"] = "later"   # format 1's rules say nothing of another format
                errors = self.build.validate_workflow(newer, body)
                self.assertEqual(len(errors), 1, errors)
                self.assertIn("mettez à jour build.py et la page de suivi", errors[0])
        # a personal recipe without format is valid for the page (read as format 1)
        self.assertEqual(parcours.workflow_errors(missing, body, lambda ref: True), [])

    def test_the_blank_model_passes_build_py(self):
        fm, body = parcours.parse_recipe_text(recettes.TEMPLATE)
        self.assertEqual(self.compare(fm, body), [])


# ---------------------------------------------------------------------------
# Checking a personal recipe file
# ---------------------------------------------------------------------------
class RecipeCheckTests(tp.ParcoursTestCase):
    def check(self, text):
        return parcours.check_recipe_text(text)

    def test_the_blank_model_is_valid_and_ready_for_the_repository(self):
        result = self.check(recettes.TEMPLATE)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["contribution"], [])
        self.assertEqual(result["id"], "ma-recette")
        view = result["recipe"]
        self.assertEqual([s["id"] for s in view["steps"]], ["cadrage", "livrable"])
        self.assertEqual(view["steps"][0]["pause"], "validate")
        self.assertEqual(view["context_sheet"][0], {"key": "objective", "label": "Objectif",
                                                    "definition": "What the requester wants to obtain, in one sentence."})

    def test_errors_are_reported_in_french_with_the_line(self):
        self.assertIn("en-tête manquant", self.check("# no front matter\n")["errors"][0])
        bad = self.check(recettes.TEMPLATE.replace("label: Ma recette", "label: Ma: recette"))
        self.assertRegex(bad["errors"][0], r"^ligne 3 du fichier : « : »")
        self.assertIsNone(bad["recipe"])

    def test_an_id_already_taken_by_the_catalogue_is_refused(self):
        for taken in ("brief-client", "cadrage", "analyse-cdc"):
            with self.subTest(taken=taken):
                errors = self.check(personal_recipe(taken))["errors"]
                self.assertTrue(any("déjà pris" in e for e in errors), errors)
        for wrong in ("Ma-Recette", "ma_recette", "réponse"):
            errors = self.check(personal_recipe(wrong))["errors"]
            self.assertTrue(any("id manquant ou invalide" in e for e in errors), errors)

    def test_a_skill_outside_the_catalogue_is_an_error(self):
        text = (recettes.TEMPLATE.replace("ix-skills:brief]", "ix-skills:invented-skill]")
                .replace("skill: ix-skills:brief", "skill: ix-skills:invented-skill")
                .replace("`ix-skills:brief`", "`ix-skills:invented-skill`"))
        errors = self.check(text)["errors"]
        self.assertEqual(errors, ["requires : le skill 'ix-skills:invented-skill' n'existe pas dans le catalogue"])

    def test_workflow_and_runner_errors(self):
        text = recettes.TEMPLATE.replace("cadrage.open_points]", "cadrage.open_points, livrable.deliverable]")
        errors = self.check(text)["errors"]
        self.assertTrue(any("'livrable.deliverable' n'est transmis par aucune étape antérieure" in e for e in errors), errors)
        text = recettes.TEMPLATE.replace("receives: [brief]", "receives: [meeting_reports]")
        errors = self.check(text)["errors"]
        self.assertTrue(any("« meeting_reports » n'est pas une entrée possible" in e and "remplacez sans doute « meeting_reports » par brief" in e
                            for e in errors), errors)
        text = recettes.TEMPLATE.replace("    - id: livrable", "    - id: Livrable_Final")
        errors = self.check(text)["errors"]
        self.assertTrue(any("minuscules sans accents, chiffres, tirets et soulignés" in e for e in errors), errors)
        text = recettes.TEMPLATE.replace("      transmits: [deliverable]\n", "      transmits: []\n")
        errors = self.check(text)["errors"]
        self.assertTrue(any("transmits doit lister au moins un champ" in e for e in errors), errors)
        self.assertTrue(self.check(recettes.TEMPLATE.replace("workflow:", "flow:"))["errors"])
        weird = self.check(recettes.TEMPLATE.replace("context_labels:", "context_labels: 3\n  ignored:"))
        self.assertTrue(weird["errors"])

    def test_what_the_repository_asks_more(self):
        text = (recettes.TEMPLATE.replace("description_en:", "description_xx:")
                .replace("domain: ops", "domain: marketing").replace("version: 0.1.0", "version: 1"))
        result = self.check(text)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["contribution"], ["champ 'description_en' manquant", "version doit être de la forme 1.0.0",
                                                  "domain doit valoir rh, sales, finance, legal, ops, data, fondateur"])


# ---------------------------------------------------------------------------
# The runner and the recueil
# ---------------------------------------------------------------------------
class RecueilTests(tp.ParcoursTestCase):
    def setUp(self):
        super().setUp()
        self.recueil = parcours.recueil_dir(self.pdir)
        self.recueil.mkdir(parents=True)

    def recipes_json(self, pdir=None):
        code, out, err = self.cli_at(pdir or self.pdir, "recipes", "--json")
        self.assertEqual(code, 0, err)
        return json.loads(out)

    def cli_at(self, pdir, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = parcours.main(list(argv) + ["--parcours-dir", str(pdir)])
        return code, out.getvalue(), err.getvalue()

    def test_a_personal_recipe_is_listed_marked_and_played(self):
        (self.recueil / "ma-recette.md").write_text(recettes.TEMPLATE, encoding="utf-8")
        data = self.recipes_json()
        mine = next(r for r in data["recipes"] if r["id"] == "ma-recette")
        self.assertTrue(mine["personal"])
        self.assertEqual(mine["origin"], "personal")
        self.assertFalse(next(r for r in data["recipes"] if r["id"] == "brief-client")["personal"])
        self.assertEqual(data["recueil"], str(self.recueil.resolve()))
        code, out, _ = self.cli("recipes")
        self.assertIn("ma-recette — Ma recette (2 étapes) [personnelle]", out)
        self.ok("new", "ma-recette", "--input", str(self.input_file), "--slug", "demo", "--engine", "simulation")
        state = self.drive()
        self.assertEqual(state["status"], "completed")
        self.assertEqual(state["recipe_origin"], "personal")
        self.assertEqual(state["recipe_sha256"], hashlib.sha256(recettes.TEMPLATE.encode("utf-8")).hexdigest())
        report = json.loads(self.ok("status", "demo", "--json"))
        self.assertTrue(report["recipe_current"])
        self.assertEqual(report["recipe_origin"], "personal")

    def test_the_plugin_wins_over_a_personal_recipe_of_the_same_id(self):
        text = recettes.TEMPLATE.replace("id: ma-recette", "id: brief-client").replace("label: Ma recette", "label: Imposteur")
        (self.recueil / "brief-client.md").write_text(text, encoding="utf-8")
        data = self.recipes_json()
        theirs = [r for r in data["recipes"] if r["id"] == "brief-client"]
        self.assertEqual(len(theirs), 1)
        self.assertEqual(theirs[0]["label"], "Brief client")
        self.assertEqual(data["personal_problems"][0]["id"], "brief-client")
        self.assertIn("masquée", data["personal_problems"][0]["message"])

    def test_a_broken_personal_recipe_is_not_offered_and_says_why(self):
        (self.recueil / "cassee.md").write_text(personal_recipe("cassee").replace("pause: validate", "pause: later"), encoding="utf-8")
        (self.recueil / "illisible.md").write_text("---\nid: [\n---\n", encoding="utf-8")
        (self.recueil / "autre-id.md").write_text(personal_recipe("pas-le-meme"), encoding="utf-8")
        data = self.recipes_json()
        self.assertNotIn("cassee", [r["id"] for r in data["recipes"]])
        problems = {p["id"]: p["message"] for p in data["personal_problems"]}
        self.assertIn("pause", problems["cassee"])
        self.assertIn("illisible", problems)
        self.assertIn("son en-tête porte l'id", problems["autre-id"])

    def test_where_the_recueil_is(self):
        self.assertEqual(self.recueil, self.tmp / "recettes")   # next to a folder named parcours
        home = self.tmp / "home"
        self.assertEqual(parcours.recueil_dir(home / ".ix-recipes" / "parcours"), (home / ".ix-recipes" / "recettes").resolve())
        self.assertEqual(parcours.recueil_dir(home / "Parcours"), (home / "Parcours" / "recettes").resolve())   # an older folder
        self.assertEqual(parcours.recipe_places(self.pdir)["recueil"], self.recueil)

    def test_the_recueil_folder_is_never_a_dossier(self):
        self.ok("new", "brief-client", "--input", str(self.input_file), "--slug", "recettes", "--engine", "fake")
        self.assertTrue((self.pdir / "recettes-dossier" / "state.json").is_file())
        self.assertFalse((self.recueil / "state.json").exists())

    def test_a_draft_is_seen_only_from_its_test_folder(self):
        draft = self.recueil / parcours.DRAFTS_DIR / "essai-x"
        (draft / parcours.ESSAIS_DIR).mkdir(parents=True)
        (draft / parcours.DRAFT_FILE).write_text(personal_recipe("brouillon-x"), encoding="utf-8")
        essais = draft / parcours.ESSAIS_DIR
        self.assertEqual(parcours.recipe_places(essais), {"recueil": self.recueil.resolve(), "draft": (draft / parcours.DRAFT_FILE).resolve()})
        self.assertIn("brouillon-x", [r["id"] for r in self.recipes_json(essais)["recipes"]])
        self.assertNotIn("brouillon-x", [r["id"] for r in self.recipes_json()["recipes"]])
        code, out, _ = self.cli_at(essais, "new", "brouillon-x", "--input", str(self.input_file), "--engine", "simulation", "--json")
        self.assertEqual(code, 0, out)
        slug = json.loads(out)["slug"]
        self.assertEqual(json.loads((essais / slug / "state.json").read_text())["recipe_origin"], "draft")
        # the draft changes: the test dossier knows it ran an older version
        (draft / parcours.DRAFT_FILE).write_text(personal_recipe("brouillon-x").replace("Ma recette", "Ma recette v2"), encoding="utf-8")
        code, out, _ = self.cli_at(essais, "status", slug, "--json")
        self.assertFalse(json.loads(out)["recipe_current"])

    def test_the_simulation_engine_spends_nothing_and_keeps_the_isolation(self):
        (self.recueil / "ma-recette.md").write_text(recettes.TEMPLATE, encoding="utf-8")
        self.ok("new", "ma-recette", "--input", str(self.input_file), "--slug", "demo", "--engine", "simulation")
        self.ok("next", "demo", "--yes")
        first = (self.pdir / "demo" / "01-cadrage.md").read_text(encoding="utf-8")
        self.assertIn("aucun modèle", first.lower())
        self.assertIn("- `brief`", first)
        self.assertEqual(self.state()["context_sheet"]["objective"], "(simulé) objective")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        second = (self.pdir / "demo" / "02-livrable.md").read_text(encoding="utf-8")
        for name in ("context_sheet", "cadrage.need", "cadrage.constraints", "cadrage.open_points"):
            self.assertIn(f"- `{name}`", second)
        self.assertNotIn("Dupuis", second)   # inputs are named, never quoted
        state = self.state()
        self.assertEqual(state["status"], "completed")
        self.assertEqual(state["cost_usd"], 0.0)
        self.assertEqual(state["calls"], {"simulation": 2})
        self.assertIn("Ce document serait transmis", state["steps"][1]["handoff"]["deliverable"])
        plan = json.loads(self.ok("plan", "demo", "--json"))
        self.assertEqual(plan["subscription_calls"], 0)


# ---------------------------------------------------------------------------
# recettes.py: drafts, design, editing, the recueil
# ---------------------------------------------------------------------------
class RecettesTestCase(tp.ParcoursTestCase):
    def setUp(self):
        super().setUp()
        self.write_skill(self.root / "dist" / "skills", "concepteur-recette")
        self.recueil = parcours.recueil_dir(self.pdir)

    def rcli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = recettes.main(list(argv) + ["--parcours-dir", str(self.pdir)])
        return code, out.getvalue(), err.getvalue()

    def rok(self, *argv):
        code, out, err = self.rcli(*argv, "--json")
        self.assertEqual(code, 0, f"{argv} -> {code}\n{out}\n{err}")
        return json.loads(out.strip().splitlines()[-1])

    def rfail(self, *argv):
        code, out, err = self.rcli(*argv, "--json")
        self.assertEqual(code, 1, f"{argv} -> {code}\n{out}\n{err}")
        return json.loads(out.strip().splitlines()[-1])

    def need_file(self, text="Chaque mois, un manager m'envoie un besoin de recrutement flou ; je fais la fiche de poste."):
        path = self.tmp / "besoin.md"
        path.write_text(text, encoding="utf-8")
        return str(path)

    def recipe_file(self, text):
        path = self.tmp / "recette.md"
        path.write_text(text, encoding="utf-8")
        return str(path)

    def draft_with(self, text=None, title="Ouverture de poste"):
        slug = self.rok("draft-new", "--input", self.need_file(), "--title", title)["slug"]
        if text is not None:
            self.rok("save", slug, "--file", self.recipe_file(text))
        return slug

    def draft_path(self, slug):
        return self.recueil / parcours.DRAFTS_DIR / slug


class DraftTests(RecettesTestCase):
    def test_a_draft_needs_a_need_or_the_model(self):
        empty = self.tmp / "vide.md"
        empty.write_text("  \n", encoding="utf-8")
        self.assertEqual(self.rfail("draft-new", "--input", str(empty))["error"], "error")
        self.assertIn("le besoin est vide", self.rfail("draft-new")["message"])
        slug = self.rok("draft-new", "--template", "--title", "Modèle")["slug"]
        self.assertEqual(slug, "modele")
        shown = self.rok("show", slug)
        self.assertEqual(shown["check"]["errors"], [])
        self.assertIsNone(shown["need"])

    def test_saving_checks_every_time_and_keeps_the_previous_version(self):
        slug = self.draft_with()
        result = self.rok("save", slug, "--file", self.recipe_file(recettes.TEMPLATE.replace("pause: validate", "pause: later")))
        self.assertTrue(result["saved"])
        self.assertTrue(any("pause" in e for e in result["check"]["errors"]))
        result = self.rok("save", slug, "--file", self.recipe_file(recettes.TEMPLATE))
        self.assertEqual(result["check"]["errors"], [])
        self.assertTrue((self.draft_path(slug) / "recipe.v1.md").is_file())
        same = self.rok("save", slug, "--file", self.recipe_file(recettes.TEMPLATE))
        self.assertFalse(same["saved"])
        stale = self.rfail("save", slug, "--file", self.recipe_file(recettes.TEMPLATE + "\n"), "--if-sha", "0" * 64)
        self.assertEqual(stale["error"], "state_changed")
        self.rok("save", slug, "--file", self.recipe_file(recettes.TEMPLATE + "\n"), "--if-sha", result["sha256"])

    def test_check_command(self):
        code, out, _ = self.rcli("check", "--file", self.recipe_file(recettes.TEMPLATE))
        self.assertEqual(code, 0)
        self.assertIn("Recette valide", out)
        code, out, _ = self.rcli("check", "--file", self.recipe_file("nothing"))
        self.assertEqual(code, 1)

    def test_list_show_and_the_test_dossiers(self):
        slug = self.draft_with(recettes.TEMPLATE)
        listed = self.rok("list")
        self.assertEqual(listed["drafts"][0]["slug"], slug)
        self.assertFalse(listed["drafts"][0]["tested"])
        essais = self.draft_path(slug) / parcours.ESSAIS_DIR
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(parcours.main(["new", "ma-recette", "--input", str(self.input_file), "--engine", "simulation",
                                            "--parcours-dir", str(essais), "--slug", "essai", "--json"]), 0)
            for command in (["next", "essai", "--yes"], ["validate", "essai"], ["next", "essai", "--yes"]):
                self.assertEqual(parcours.main(command + ["--parcours-dir", str(essais)]), 0)
        shown = self.rok("show", slug)
        self.assertTrue(shown["tested"])
        self.assertEqual(shown["essais"][0]["status"], "completed")
        self.assertTrue(shown["essais"][0]["current"])
        self.assertFalse((self.pdir / "essai").exists())   # apart from the real dossiers
        self.rok("save", slug, "--file", self.recipe_file(recettes.TEMPLATE.replace("Ma recette", "Ma recette 2")))
        self.assertFalse(self.rok("show", slug)["tested"])   # tested with an older version
        self.rok("essai-delete", slug, "essai")
        self.assertFalse((essais / "essai").exists())
        self.assertEqual(self.rfail("essai-delete", slug, "essai")["error"], "not_found")
        self.assertEqual(self.rfail("essai-delete", slug, "../x")["error"], "error")

    def test_names_are_checked(self):
        self.assertEqual(self.rfail("show", "../etc")["error"], "error")
        self.assertEqual(self.rfail("show", "absent")["error"], "not_found")
        self.assertEqual(self.rfail("personal", "Absent")["error"], "error")
        self.assertEqual(self.rfail("personal", "absent")["error"], "not_found")

    def test_template_and_delete(self):
        slug = self.draft_with()
        self.rok("template", slug)
        self.assertEqual((self.draft_path(slug) / "recipe.md").read_text(encoding="utf-8"), recettes.TEMPLATE)
        with parcours.parcours_lock(self.draft_path(slug)):
            self.assertEqual(self.rfail("delete-draft", slug)["error"], "locked")
        self.rok("delete-draft", slug)
        self.assertFalse(self.draft_path(slug).exists())


PROPOSAL = {
    "title": "Ouverture de poste", "summary": "D'un mail de manager à un brief.",
    "context_sheet": ["Objectif", "Contraintes"],
    "steps": [
        {"id": "cadrage", "label": "Cadrage", "skill": "ix-skills:cadrage", "role": "Clarifie le besoin.",
         "receives": ["brief"], "produces": ["need", "constraints", "open_points"], "pause": "validate"},
        {"id": "livrable", "label": "Livrable", "skill": "ix-skills:brief", "role": "Écrit le brief.",
         "receives": ["context_sheet", "cadrage.need"], "produces": ["deliverable"], "pause": "none"},
    ],
}


def proposal_output(proposal=PROPOSAL, verdict="recipe"):
    return (f"## A. Verdict\n\nUne chaîne se justifie.\n\n```json\n{json.dumps(proposal, ensure_ascii=False, indent=1)}\n```\n\n"
            f"## Rationale\n\nLe cadrage d'abord.\n\n## VERDICT\n{verdict}\n")


WRITTEN = "Voici le fichier.\n\n````markdown\n{recipe}````\n\n## VERDICT\nrecipe\n"


class DesignTests(RecettesTestCase):
    def design(self, slug, output, *extra):
        (self.fake / "concepteur-recette.md").write_text(output, encoding="utf-8")
        return self.rok("design", slug, "--engine", "fake", *extra)

    def received(self):
        return (self.fake / "received" / "concepteur-recette.md").read_text(encoding="utf-8")

    def comments(self, slug, data):
        path = self.tmp / "commentaires.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return self.rcli("comments", slug, "--file", str(path), "--json")

    def test_the_designer_first_proposes_a_chain_from_the_real_catalogue_and_writes_no_file(self):
        slug = self.draft_with()
        result = self.design(slug, proposal_output())
        self.assertEqual((result["mode"], result["verdict"], result["has_recipe"], result["proposal_steps"]), ("propose", "recipe", False, 2))
        message = self.received()
        self.assertIn("STUB-METHOD-concepteur-recette", message)
        self.assertIn("- `ix-skills:cadrage` — stub", message)
        self.assertIn("- `ix-recipes:analyse-cdc` — stub", message)
        self.assertNotIn("`ix-recipes:concepteur-recette`", message)   # a tool, not a step
        self.assertIn("besoin de recrutement flou", message)
        self.assertIn("DO NOT write the recipe file", message)
        self.assertIn("step 1 receives `[brief]`, never names of documents", message)
        self.assertIn("## VERDICT", message)
        self.assertEqual(message, (self.draft_path(slug) / "conception.in.md").read_text(encoding="utf-8"))
        self.assertFalse((self.draft_path(slug) / "recipe.md").exists())
        shown = self.rok("show", slug)
        self.assertEqual(shown["stage"], "proposal")
        self.assertEqual([s["id"] for s in shown["proposal"]["steps"]], ["cadrage", "livrable"])
        self.assertEqual((shown["proposal"]["version"], shown["proposal"]["validated"], shown["proposal"]["problems"]), (1, False, []))
        self.assertIn("Le cadrage d'abord", shown["concept"])
        self.assertIn("onglet « Proposition »", shown["concept"])
        self.assertNotIn('"steps"', shown["concept"])   # the proposal is shown as steps, not as JSON
        self.assertEqual((shown["design"]["engine"], shown["design"]["model"]), ("fake", "opus"))
        self.assertEqual(self.rok("list")["drafts"][0]["stage"], "proposal")

    def test_comments_go_with_the_revision_and_are_kept(self):
        slug = self.draft_with()
        self.design(slug, proposal_output())
        self.assertIn("aucun commentaire", self.rfail("design", slug, "--mode", "revise", "--engine", "fake")["message"])
        code, out, _ = self.comments(slug, {"steps": {"absente": "x"}})
        self.assertEqual(code, 1)
        self.assertIn("absentes de la proposition", out)
        code, _, _ = self.comments(slug, {"general": "Ajoute une pause pour les réponses du manager",
                                          "steps": {"livrable": "Plus court", "cadrage": "  "}})
        self.assertEqual(code, 0)
        self.assertEqual(self.rok("show", slug)["comments"], {"general": "Ajoute une pause pour les réponses du manager",
                                                             "steps": {"livrable": "Plus court"}})
        revised = dict(PROPOSAL, steps=[dict(PROPOSAL["steps"][0], pause="answers"), PROPOSAL["steps"][1]])
        result = self.design(slug, proposal_output(revised), "--mode", "revise")
        self.assertEqual(result["mode"], "revise")
        message = self.received()
        self.assertIn("=== YOUR PREVIOUS PROPOSAL ===", message)
        self.assertIn("On the whole chain: Ajoute une pause pour les réponses du manager", message)
        self.assertIn("On step `livrable`: Plus court", message)
        shown = self.rok("show", slug)
        self.assertEqual(shown["proposal"]["version"], 2)
        self.assertEqual(shown["proposal"]["steps"][0]["pause"], "answers")
        self.assertEqual(shown["proposal"]["after_comments"]["steps"], {"livrable": "Plus court"})
        self.assertEqual(shown["comments"], {"general": "", "steps": {}})   # sent, so cleared
        self.assertTrue((self.draft_path(slug) / "commentaires.v1.json").is_file())
        self.assertTrue((self.draft_path(slug) / "proposition.v1.json").is_file())

    def test_writing_follows_the_validated_proposal(self):
        slug = self.draft_with()
        self.assertIn("aucune proposition", self.rfail("design", slug, "--mode", "write", "--engine", "fake")["message"])
        self.design(slug, proposal_output())
        result = self.design(slug, WRITTEN.format(recipe=recettes.TEMPLATE), "--mode", "write")
        self.assertEqual((result["mode"], result["has_recipe"], result["errors"], result["drift"]), ("write", True, [], []))
        message = self.received()
        self.assertIn("=== THE PROPOSAL THE USER VALIDATED ===", message)
        self.assertIn('"skill": "ix-skills:brief"', message)
        self.assertNotIn("THE USER'S COMMENTS", message)
        shown = self.rok("show", slug)
        self.assertEqual(shown["stage"], "recipe")
        self.assertTrue(shown["proposal"]["validated"])
        self.assertEqual(shown["text"], recettes.TEMPLATE)
        self.assertIn("onglet « Fichier de la recette »", shown["concept"])
        # a file that departs from the proposal says so
        other = recettes.TEMPLATE.replace("pause: validate", "pause: answers")
        result = self.design(slug, WRITTEN.format(recipe=other), "--mode", "write")
        self.assertEqual(result["drift"], ["« Cadrage » : pause answers au lieu de validate"])
        self.assertTrue((self.draft_path(slug) / "recipe.v1.md").is_file())
        # a new proposal puts the file aside: one starts again from the chain
        self.design(slug, proposal_output())
        shown = self.rok("show", slug)
        self.assertEqual((shown["stage"], shown["proposal"]["version"]), ("proposal", 2))
        self.assertTrue((self.draft_path(slug) / "recipe.v2.md").is_file())

    def test_a_proposal_that_cannot_become_a_recipe_is_not_written(self):
        slug = self.draft_with()
        bad = dict(PROPOSAL, steps=[dict(PROPOSAL["steps"][0], receives=["meeting_reports"]),
                                    dict(PROPOSAL["steps"][1], skill="ix-skills:invented", receives=["cadrage.absent"])])
        self.design(slug, proposal_output(bad))
        problems = self.rok("show", slug)["proposal"]["problems"]
        self.assertEqual(problems, [
            "« Cadrage » : « meeting_reports » n'est pas une entrée possible (la première étape reçoit brief)",
            "« Livrable » : le skill « ix-skills:invented » n'existe pas dans le catalogue",
            "« Livrable » : « cadrage.absent » n'est produit par aucune étape antérieure",
            "la première étape doit recevoir brief (la demande brute)"])
        refused = self.rfail("design", slug, "--mode", "write", "--engine", "fake")
        self.assertIn("Demandez une révision", refused["message"])
        self.assertFalse((self.draft_path(slug) / "recipe.md").exists())

    def test_a_single_skill_verdict_writes_nothing_and_insisting_asks_again(self):
        slug = self.draft_with()
        result = self.design(slug, SINGLE_SKILL_OUTPUT)
        self.assertEqual((result["verdict"], result["has_recipe"], result["proposal_steps"]), ("single_skill", False, 0))
        shown = self.rok("show", slug)
        self.assertEqual((shown["stage"], shown["proposal"]), ("start", None))
        self.assertIn("Un skill seul suffit", shown["concept"])
        result = self.design(slug, proposal_output(), "--insist")
        self.assertEqual((result["verdict"], result["proposal_steps"]), ("recipe", 2))
        message = self.received()
        self.assertIn("THE USER INSISTS", message)
        self.assertIn("Un skill seul suffit", message)   # the previous answer, for reference
        self.assertTrue((self.draft_path(slug) / "conception.v1.md").is_file())

    def test_a_failed_call_is_recorded_and_simulation_cannot_design(self):
        slug = self.draft_with()
        code, out, _ = self.rcli("design", slug, "--engine", "fake", "--json")   # no canned output
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out.strip().splitlines()[-1])["error"], "engine")
        self.assertIn("n'existe pas", self.rok("show", slug)["design"]["error"])
        unreadable = self.design(slug, "Une recette se justifie.\n\n## VERDICT\nrecipe\n")
        self.assertIn("pas rendu de proposition lisible", unreadable["error"])
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                recettes.main(["design", slug, "--engine", "simulation", "--parcours-dir", str(self.pdir)])
        template = self.rok("draft-new", "--template")["slug"]
        self.assertIn("pas de besoin", self.rfail("design", template, "--engine", "fake")["message"])

    def test_reading_the_designer_answer(self):
        verdict, recipe, document = recettes.parse_design(DESIGN_OUTPUT.format(recipe=recettes.TEMPLATE))
        self.assertEqual((verdict, recipe), ("recipe", recettes.TEMPLATE))
        self.assertIn("dans l'éditeur", document)
        nested = "Intro\n\n````markdown\n---\nid: x\nworkflow:\n---\n\n```text\ninner\n```\n\nend\n````\n\n## VERDICT\nRecipe\n"
        verdict, recipe, _ = recettes.parse_design(nested)
        self.assertEqual(verdict, "recipe")
        self.assertIn("```text\ninner\n```", recipe)
        self.assertEqual(recettes.parse_design("Use `ix-skills:brief`.\n\n## VERDICT\nmanual_sequence\n")[:2], ("manual_sequence", None))
        self.assertEqual(recettes.parse_design("No block, no verdict")[:2], (None, None))
        lenient = '```\n{"steps": [{"id": "Étape Un", "skill": "ix-skills:cadrage", "receives": "brief", "pause": "later",},],}\n```'
        step = recettes.proposal_block(lenient)[2]["steps"][0]
        self.assertEqual((step["id"], step["receives"], step["pause"], step["optional"]), ("etape-un", ["brief"], "none", False))


class ProvidedRecipeTests(RecettesTestCase):
    def test_a_provided_recipe_is_read_and_copied_under_a_free_id(self):
        shown = self.rok("provided", "brief-client")
        steps = shown["recipe"]["steps"]
        self.assertEqual([s["id"] for s in steps], ["cadrage", "questioning", "explorer", "decision", "brief"])
        self.assertTrue(steps[0]["produces_context_sheet"])
        self.assertEqual([s["optional"] for s in steps], [False, False, True, True, False])
        self.assertEqual(self.rfail("provided", "absente")["error"], "not_found")
        self.assertEqual(self.rfail("provided", "Bad_Id")["error"], "error")
        first = self.rok("fork", "brief-client")
        self.assertEqual((first["id"], first["forked_from"]), ("brief-client-perso", "brief-client"))
        draft = self.rok("show", first["slug"])
        self.assertEqual(draft["check"]["errors"], [])
        self.assertEqual(draft["recipe_label"], "Brief client (ma version)")
        self.assertIn("version: 0.1.0", draft["text"])
        self.assertEqual(self.rok("fork", "brief-client")["id"], "brief-client-perso-2")   # the first copy holds the id
        self.assertIn("Brief client", (parcours.ROOT / "skills" / "brief-client.md").read_text(encoding="utf-8"))   # untouched

    def test_in_the_plugin_the_file_is_rebuilt_from_recipe_json(self):
        folder = self.tmp / "plugin" / "skills"
        (folder / "suivi-parcours").mkdir(parents=True)
        (folder / "suivi-parcours" / "SKILL.md").write_text("---\nname: suivi-parcours\n---\n", encoding="utf-8")
        fm, body = parcours.parse_recipe_text((REPO / "skills" / "brief-client.md").read_text(encoding="utf-8"))
        (folder / "brief-client").mkdir()
        (folder / "brief-client" / "recipe.json").write_text(json.dumps(
            {k: fm[k] for k in ("id", "label", "version", "summary_fr", "description_fr", "icon", "workflow")}), encoding="utf-8")
        (folder / "brief-client" / "SKILL.md").write_text("---\nname: brief-client\ndescription: x\n---\n" + body, encoding="utf-8")
        with mock.patch.object(parcours, "ROOT", folder / "suivi-parcours"):
            text = recettes.provided_text("brief-client")
        rebuilt, rebuilt_body = parcours.parse_recipe_text(text)
        self.assertEqual(rebuilt["workflow"], fm["workflow"])
        self.assertEqual(rebuilt["requires"], ["ix-skills:cadrage", "ix-skills:questioning", "ix-skills:explorer",
                                               "ix-skills:decision", "ix-skills:brief"])
        self.assertEqual(rebuilt["description_fr"], fm["description_fr"])
        self.assertEqual(parcours.workflow_errors(rebuilt, rebuilt_body, lambda ref: True), [])


BUILT = {"title": "Bilan mensuel", "summary": "Des CR au tableau de bord.", "context_sheet": ["Période", "Projets", "Période"],
         "steps": [
             {"id": "synthese", "label": "Synthèse", "skill": "ix-skills:cadrage", "role": "Condense les CR.",
              "receives": ["brief"], "produces": ["resultat"], "pause": "none"},
             {"id": "questions", "label": "Questions", "skill": "ix-skills:questioning", "receives": ["context_sheet", "synthese.resultat"],
              "produces": ["resultat"], "pause": "answers"},
             {"id": "pistes", "label": "Pistes", "skill": "ix-skills:explorer", "optional": True,
              "receives": ["context_sheet", "synthese.resultat", "questions.resultat", "answers"], "produces": ["resultat"]},
             {"id": "tableau", "label": "Tableau de bord", "skill": "ix-skills:brief",
              "receives": ["context_sheet", "synthese.resultat", "questions.resultat", "answers", "pistes.resultat"], "produces": ["resultat"]}]}


class BlocksTests(RecettesTestCase):
    def save_proposal(self, slug, data, *extra):
        path = self.tmp / "proposition.json"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return self.rcli("proposal", slug, "--file", str(path), "--json", *extra)

    def test_from_blocks_to_a_valid_recipe_without_any_call(self):
        slug = self.rok("draft-new", "--blocks", "--title", "Bilan mensuel")["slug"]
        shown = self.rok("show", slug)
        self.assertEqual((shown["stage"], shown["proposal"]["source"], shown["proposal"]["steps"]), ("proposal", "blocks", []))
        self.assertIn("aucune proposition à écrire", self.rfail("write-file", slug)["message"])
        code, out, _ = self.save_proposal(slug, BUILT)
        self.assertEqual(code, 0, out)
        saved = json.loads(out.strip().splitlines()[-1])
        self.assertEqual(saved["problems"], [])
        self.assertTrue(all(s["auto"] for s in saved["steps"]))
        written = self.rok("write-file", slug)
        self.assertEqual((written["id"], written["errors"]), ("bilan-mensuel", []))
        shown = self.rok("show", slug)
        self.assertEqual(shown["stage"], "recipe")
        fm, body = parcours.parse_recipe_text(shown["text"])
        steps = fm["workflow"]["steps"]
        self.assertEqual([s["pause"] for s in steps], ["validate", "answers", "none", "none"])   # step 1 always stops
        self.assertTrue(steps[0]["produces_context_sheet"])
        self.assertTrue(steps[2]["optional"])
        self.assertEqual(steps[3]["output_field"], "resultat")
        self.assertEqual(fm["workflow"]["context_sheet"], ["periode", "projets", "periode_2"])
        self.assertEqual(fm["workflow"]["context_labels"]["periode"], "Période")
        self.assertEqual(steps[1]["mission"], "Apply the skill to the case, within the step « Questions ».")
        if yaml:   # the same file passes build.py's own check
            build = import_build()
            with mock.patch.object(build, "_skill_exists", lambda ref: True):
                self.assertEqual(build.validate_workflow(yaml.safe_load(shown["text"].split("---")[1]), body), [])
        # the recipe is then tested like any draft: the simulation runs it to the end
        essais = self.draft_path(slug) / parcours.ESSAIS_DIR
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(parcours.main(["new", "bilan-mensuel", "--input", str(self.input_file), "--engine", "simulation",
                                            "--parcours-dir", str(essais), "--slug", "essai", "--json"]), 0)
            for command in (["next", "essai", "--yes"], ["validate", "essai"], ["next", "essai", "--yes"],
                            ["answer", "essai", "--none"], ["next", "essai", "--yes"], ["choose", "essai", "--run", "pistes"],
                            ["next", "essai", "--yes"]):
                self.assertEqual(parcours.main(command + ["--parcours-dir", str(essais)]), 0, command)
        self.assertEqual(json.loads((essais / "essai" / "state.json").read_text())["status"], "completed")

    def test_a_file_goes_back_to_blocks_and_blocks_do_not_overwrite_a_file_silently(self):
        slug = self.draft_with(recettes.TEMPLATE)
        code, out, _ = self.save_proposal(slug, BUILT)
        self.assertEqual(json.loads(out.strip().splitlines()[-1])["error"], "exists")
        back = self.rok("to-blocks", slug)
        self.assertEqual([s["skill"] for s in back["steps"]], ["ix-skills:cadrage", "ix-skills:brief"])
        self.assertEqual(back["recipe_id"], "ma-recette")
        self.assertEqual(back["context_sheet"], ["Objectif", "Contraintes", "Destinataire", "Échéances"])
        self.assertFalse(any(s["auto"] for s in back["steps"]))   # the file's own wiring is kept
        self.assertTrue((self.draft_path(slug) / "recipe.v1.md").is_file())
        self.assertEqual(self.rok("write-file", slug)["id"], "ma-recette")   # the recipe keeps its id
        code, _, _ = self.save_proposal(slug, BUILT, "--replace-file")
        self.assertEqual(code, 0)
        self.assertEqual(self.rok("show", slug)["stage"], "proposal")

    def test_the_palette_is_the_catalogue(self):
        skills = self.rok("catalogue")["skills"]
        refs = [s["ref"] for s in skills]
        self.assertIn("ix-skills:cadrage", refs)
        self.assertIn("ix-recipes:analyse-cdc", refs)
        self.assertNotIn("ix-recipes:concepteur-recette", refs)
        self.assertNotIn("path", skills[0])


class RecueilCommandTests(RecettesTestCase):
    def test_promote_edit_retire(self):
        slug = self.draft_with(recettes.TEMPLATE.replace("pause: validate", "pause: later"))
        self.assertIn("encore des erreurs", self.rfail("promote", slug)["message"])
        self.rok("save", slug, "--file", self.recipe_file(recettes.TEMPLATE))
        result = self.rok("promote", slug)
        self.assertEqual(result["id"], "ma-recette")
        path = self.recueil / "ma-recette.md"
        self.assertEqual(path.read_text(encoding="utf-8"), recettes.TEMPLATE)
        shown = self.rok("show", slug)
        self.assertTrue(shown["in_recueil"])
        self.assertEqual(shown["origin"], "ma-recette")
        # a second draft with the same id: refused unless replacing, the old version kept
        other = self.draft_with(recettes.TEMPLATE.replace("Ma recette", "Autre"), title="Autre")
        refused = self.rfail("promote", other)
        self.assertEqual(refused["error"], "exists")
        self.rok("promote", other, "--replace")
        self.assertIn("label: Autre", path.read_text(encoding="utf-8"))
        self.assertEqual(len(list((self.recueil / ".versions").glob("ma-recette.*.md"))), 1)
        # the draft it came from updates it without asking
        self.rok("save", slug, "--file", self.recipe_file(recettes.TEMPLATE.replace("Ma recette", "Encore")))
        self.rok("promote", slug)
        # edit: an unchanged draft is reused, else a new one
        self.assertEqual(self.rok("edit", "ma-recette"), {"slug": slug, "reused": True})
        path.write_text(recettes.TEMPLATE.replace("Ma recette", "Changée à la main"), encoding="utf-8")
        fresh = self.rok("edit", "ma-recette")
        self.assertFalse(fresh["reused"])
        self.assertIn("Changée à la main", (self.draft_path(fresh["slug"]) / "recipe.md").read_text(encoding="utf-8"))
        personal = self.rok("personal", "ma-recette")
        self.assertEqual(personal["errors"], [])
        self.assertEqual(personal["default_source"], recettes.UPSTREAM)
        listed = self.rok("list")
        self.assertEqual([r["id"] for r in listed["personal"]], ["ma-recette"])
        self.rok("retire", "ma-recette")
        self.assertFalse(path.exists())
        self.assertEqual(len(list((self.recueil / ".versions").glob("ma-recette.*.md"))), 3)   # two replaced, one retired


# ---------------------------------------------------------------------------
# Proposing a recipe to the repository, against a throwaway repository
# ---------------------------------------------------------------------------
JSONSCHEMA_STUB = "class ValidationError(Exception):\n    message = ''\n\n\ndef validate(instance, schema):\n    return None\n"


@unittest.skipUnless(shutil.which("git") and yaml, "git and pyyaml are needed")
class ContributionTests(RecettesTestCase):
    def setUp(self):
        super().setUp()
        self.git_env = {"GIT_CONFIG_GLOBAL": str(self.tmp / "gitconfig"), "GIT_CONFIG_NOSYSTEM": "1"}
        (self.tmp / "gitconfig").write_text("[init]\n\tdefaultBranch = main\n", encoding="utf-8")
        stubs = self.tmp / "pystubs"
        stubs.mkdir()
        try:
            import jsonschema  # noqa: F401
        except ImportError:
            (stubs / "jsonschema.py").write_text(JSONSCHEMA_STUB, encoding="utf-8")
        paths = [str(stubs), str(Path(yaml.__file__).resolve().parent.parent)]
        env = dict(self.git_env, PYTHONPATH=os.pathsep.join(paths), PATH=f"{self.tmp / 'bin'}{os.pathsep}{os.environ['PATH']}")
        patcher = mock.patch.dict(os.environ, env)
        patcher.start()
        self.addCleanup(patcher.stop)
        (self.tmp / "bin").mkdir()
        self.upstream = self.make_upstream()
        self.clone = self.tmp / "clone"
        self.git("clone", "--quiet", str(self.upstream), str(self.clone))
        self.git("-C", str(self.clone), "config", "user.name", "Test")
        self.git("-C", str(self.clone), "config", "user.email", "test@example.invalid")
        self.recueil.mkdir(parents=True)
        (self.recueil / "ma-recette.md").write_text(recettes.TEMPLATE, encoding="utf-8")

    def git(self, *argv, cwd=None):
        done = subprocess.run(["git", *argv], cwd=cwd, capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        return done.stdout.strip()

    def make_upstream(self):
        work = self.tmp / "upstream-work"
        (work / "skills").mkdir(parents=True)
        (work / "partials").mkdir()
        (work / "dist" / ".claude-plugin").mkdir(parents=True)
        shutil.copy(REPO / "build.py", work / "build.py")
        shutil.copy(REPO / "dist" / ".claude-plugin" / "plugin.json", work / "dist" / ".claude-plugin" / "plugin.json")
        shutil.copy(REPO / ".gitignore", work / ".gitignore")
        shutil.copy(REPO / "skills" / "brief-client.md", work / "skills" / "brief-client.md")
        self.git("init", "--quiet", "-b", "main", cwd=work)
        self.git("add", "-A", cwd=work)
        self.git("-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "--quiet", "-m", "init", cwd=work)
        bare = self.tmp / "upstream.git"
        self.git("clone", "--quiet", "--bare", str(work), str(bare))
        return bare

    def contribute(self, action, *extra):
        return self.rok("contribute", "ma-recette", action, *extra)

    def test_prepare_shows_the_diff_and_pushes_nothing_then_push(self):
        report = self.contribute("prepare", "--source", str(self.clone))
        self.assertEqual(report["status"], "prepared")
        self.assertEqual(report["branch"], "recette/ma-recette")
        self.assertEqual(report["base"], "main")
        for name in ("skills/ma-recette.md", "skills/ma-recette.mystaffy.json", "dist/skills/ma-recette/SKILL.md",
                     "dist/skills/ma-recette/recipe.json"):
            self.assertIn(name, report["diff"])
        self.assertIn("Validation passed.", report["build_log"])
        self.assertEqual(self.git("branch", "--list", "recette/*", cwd=self.upstream), "")   # nothing pushed
        self.assertIn("recette/ma-recette", self.git("branch", "--list", cwd=self.clone))
        self.assertEqual(self.git("status", "--porcelain", cwd=self.clone), "")   # the user's checkout untouched
        status = self.contribute("status")
        self.assertEqual(status["status"], "prepared")
        self.assertEqual(status["diff"], report["diff"])
        pushed = self.contribute("push")
        self.assertEqual(pushed["status"], "pushed")
        self.assertIn("recette/ma-recette", self.git("branch", "--list", "recette/*", cwd=self.upstream))
        self.assertIn("n'est pas sur GitHub", pushed["message"])
        self.assertIsNone(pushed["pr_url"])
        self.assertIn("déjà proposée", self.rfail("contribute", "ma-recette", "prepare")["message"])
        done = self.contribute("cancel")
        self.assertTrue(done["pushed"])
        self.assertNotIn("recette/ma-recette", self.git("branch", "--list", cwd=self.clone))
        self.assertIn("recette/ma-recette", self.git("branch", "--list", "recette/*", cwd=self.upstream))

    def test_on_github_the_pull_request_is_opened_with_gh(self):
        fake_url = "https://github.com/test-owner/ix-recipes.git"
        self.git("-C", str(self.clone), "config", "remote.origin.url", fake_url)
        self.git("-C", str(self.clone), "config", f"url.{self.upstream}.insteadOf", fake_url)
        gh_log = self.tmp / "gh-args.json"
        gh = self.tmp / "bin" / "gh"
        gh.write_text(f"#!{sys.executable}\nimport json, sys\njson.dump(sys.argv[1:], open({str(gh_log)!r}, 'w'))\n"
                      "print('https://github.com/test-owner/ix-recipes/pull/7')\n", encoding="utf-8")
        gh.chmod(0o755)
        report = self.contribute("prepare", "--source", str(self.clone))
        self.assertEqual(report["github"], "test-owner/ix-recipes")
        pushed = self.contribute("push")
        self.assertEqual(pushed["pr_url"], "https://github.com/test-owner/ix-recipes/pull/7")
        self.assertIn("compare/main...recette/ma-recette", pushed["compare_url"])
        args = json.loads(gh_log.read_text())
        self.assertEqual(args[:2], ["pr", "create"])
        self.assertEqual(args[args.index("--repo") + 1], "test-owner/ix-recipes")
        self.assertEqual(args[args.index("--head") + 1], "recette/ma-recette")
        self.assertEqual(args[args.index("--base") + 1], "main")
        self.assertIn("recette/ma-recette", self.git("branch", "--list", "recette/*", cwd=self.upstream))

    def test_a_url_source_is_cloned_once_and_remembered(self):
        source = f"file://{self.upstream}"
        self.git("config", "--global", "user.name", "Test")
        self.git("config", "--global", "user.email", "test@example.invalid")
        report = self.contribute("prepare", "--source", source)
        self.assertEqual(report["source"], source)
        self.assertEqual(self.rok("personal", "ma-recette")["default_source"], source)
        self.contribute("cancel")
        again = self.contribute("prepare")   # the remembered source
        self.assertEqual(again["source"], source)
        self.assertEqual(len(list((self.recueil / ".contribution" / "clones").iterdir())), 1)

    def test_what_stops_a_proposal_is_said_plainly(self):
        (self.recueil / "ma-recette.md").write_text(recettes.TEMPLATE.replace("description_en:", "description_xx:"), encoding="utf-8")
        self.assertIn("complétez l'en-tête", self.rfail("contribute", "ma-recette", "prepare", "--source", str(self.clone))["message"])
        (self.recueil / "ma-recette.md").write_text(recettes.TEMPLATE, encoding="utf-8")
        self.assertIn("rien de préparé", self.rfail("contribute", "ma-recette", "push")["message"])
        self.assertIn("clone introuvable", self.rfail("contribute", "ma-recette", "prepare", "--source", "relative/path")["message"])
        self.assertIn("pas un dépôt git", self.rfail("contribute", "ma-recette", "prepare", "--source", str(self.tmp))["message"])
        # no identity: the commit is refused with the two commands to type
        self.git("-C", str(self.clone), "config", "--unset", "user.name")
        self.git("-C", str(self.clone), "config", "--unset", "user.email")
        with mock.patch.dict(os.environ, {"GIT_AUTHOR_NAME": "", "GIT_COMMITTER_NAME": "", "EMAIL": ""}):
            message = self.rfail("contribute", "ma-recette", "prepare", "--source", str(self.clone))["message"]
        self.assertIn("git config --global user.name", message)
        self.assertNotIn("recette/ma-recette", self.git("branch", "--list", cwd=self.clone))   # rolled back
        self.git("-C", str(self.clone), "config", "user.name", "Test")
        self.git("-C", str(self.clone), "config", "user.email", "test@example.invalid")
        # a push refused by the remote: the branch stays ready, the message says why
        self.contribute("prepare", "--source", str(self.clone))
        self.git("-C", str(self.clone), "remote", "set-url", "origin", str(self.tmp / "nowhere.git"))
        failed = self.rfail("contribute", "ma-recette", "push")
        self.assertEqual(failed["error"], "git")
        self.assertIn("La branche recette/ma-recette reste prête", failed["message"]) if "droits" in failed["message"] else \
            self.assertIn("git push a échoué", failed["message"])
        self.assertEqual(self.contribute("status")["status"], "prepared")

    def test_a_recipe_the_repository_already_has_is_refused(self):
        upstream_work = self.tmp / "upstream-work"
        shutil.copy(self.recueil / "ma-recette.md", upstream_work / "skills" / "ma-recette.md")
        self.git("add", "-A", cwd=upstream_work)
        self.git("-c", "user.name=T", "-c", "user.email=t@example.invalid", "commit", "--quiet", "-m", "x", cwd=upstream_work)
        self.git("push", "--quiet", str(self.upstream), "main", cwd=upstream_work)
        refused = self.rfail("contribute", "ma-recette", "prepare", "--source", str(self.clone))
        self.assertEqual(refused["error"], "exists")

    def test_without_git_or_build_dependencies(self):
        with mock.patch.object(recettes.shutil, "which", lambda name: None):
            message = self.rfail("contribute", "ma-recette", "prepare", "--source", str(self.clone))["message"]
        self.assertIn("git n'est pas installé", message)
        with mock.patch.object(recettes, "build_python", lambda: None):
            message = self.rfail("contribute", "ma-recette", "prepare", "--source", str(self.clone))["message"]
        self.assertIn("pip install -r", message)
        self.assertNotIn("recette/ma-recette", self.git("branch", "--list", cwd=self.clone))

    def test_github_addresses(self):
        for url in ("https://github.com/amiel-35/ix-recipes.git", "git@github.com:amiel-35/ix-recipes.git",
                    "https://github.com/amiel-35/ix-recipes", "ssh://git@github.com/amiel-35/ix-recipes.git"):
            self.assertEqual(recettes.github_slug(url), "amiel-35/ix-recipes")
        for url in ("/tmp/x.git", "https://gitlab.com/a/b.git", "https://github.com.evil.io/a/b"):
            self.assertIsNone(recettes.github_slug(url))


# ---------------------------------------------------------------------------
# Recipe format (docs/format-recette.md §2bis): personal recipes
# ---------------------------------------------------------------------------
class PersonalRecipeFormatTests(RecettesTestCase):
    def format_of(self, text):
        fm, _ = parcours.parse_recipe_text(text)
        return fm["workflow"].get("format", "absent")

    def test_every_recipe_created_from_the_page_declares_format_1(self):
        self.assertEqual(self.format_of(recettes.TEMPLATE), 1)
        slug = self.rok("draft-new", "--template", "--title", "Modèle")["slug"]
        self.assertEqual(self.format_of((self.draft_path(slug) / "recipe.md").read_text(encoding="utf-8")), 1)
        forked = self.rok("fork", "brief-client")
        self.assertEqual(self.format_of(self.rok("show", forked["slug"])["text"]), 1)
        built = recettes.proposal_to_recipe(recettes.normalize_proposal(PROPOSAL), "par-blocs")
        self.assertEqual(self.format_of(built), 1)
        self.assertNotIn(parcours.FORMAT_MISSING, parcours.check_recipe_text(built)["contribution"])

    def test_a_file_written_by_the_designer_without_format_gets_it(self):
        without = recettes.TEMPLATE.replace("\n  format: 1\n", "\n", 1)
        self.assertEqual(self.format_of(without), "absent")
        self.assertEqual(recettes.with_format(without), recettes.TEMPLATE)
        self.assertEqual(recettes.with_format(recettes.TEMPLATE), recettes.TEMPLATE)   # already there: unchanged
        deeper = without.replace("\n  ", "\n    ")
        self.assertEqual(self.format_of(recettes.with_format(deeper)), 1)
        self.assertEqual(recettes.with_format("pas d'en-tête"), "pas d'en-tête")
        slug = self.draft_with()
        (self.fake / "concepteur-recette.md").write_text(proposal_output(), encoding="utf-8")
        self.rok("design", slug, "--engine", "fake")
        (self.fake / "concepteur-recette.md").write_text(WRITTEN.format(recipe=without), encoding="utf-8")
        self.rok("design", slug, "--mode", "write", "--engine", "fake")
        self.assertEqual((self.draft_path(slug) / "recipe.md").read_text(encoding="utf-8"), recettes.TEMPLATE)

    def test_the_check_of_a_personal_recipe(self):
        good = parcours.check_recipe_text(recettes.TEMPLATE)
        self.assertEqual((good["errors"], good["format_error"], good["recipe"]["format"]), ([], None, 1))
        without = parcours.check_recipe_text(recettes.TEMPLATE.replace("\n  format: 1\n", "\n", 1))
        self.assertEqual(without["errors"], [])   # read as format 1: it can be tested and kept
        self.assertEqual((without["recipe"]["format"], without["recipe"]["format_declared"]), (1, False))
        self.assertIn(parcours.FORMAT_MISSING, without["contribution"])   # the repository wants it written
        newer = parcours.check_recipe_text(recettes.TEMPLATE.replace("\n  format: 1\n", "\n  format: 2\n", 1)
                                           .replace("pause: validate", "pause: later"))
        self.assertEqual(newer["errors"], [newer["format_error"]])   # only the format: the rest is format 1's rules
        self.assertIn("mettez la page à jour", newer["format_error"])
        self.assertIsNone(newer["recipe"])


if __name__ == "__main__":
    unittest.main()
