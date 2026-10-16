"""
Tests of scripts/parcours.py (the recipe runner of docs/executeur.md).

Run:  cd ~/Projets/ix-recipes && python3 -m unittest tests.test_parcours -v

No real engine is ever called. Two substitutes are used:
  - the `fake` engine: canned outputs per step, written by the tests into a
    temporary fixtures directory named by PARCOURS_FAKE_DIR (<step>.md and
    <step>.retry.md). The fake engine also logs every message it receives in
    <fixtures>/received/<step>.md, which is how the tests inspect what a step
    was sent;
  - a mock of `parcours.run_process` for the claude/codex/agy/vibe command
    lines (argv, cwd, stdin are captured, nothing is executed).

The recipes under test are the two real ones (skills/brief-client.md and
skills/reponse-appel-offres.md), copied into a temporary repo layout with stub
skills, so the tests do not depend on ../ix-skills or on the plugin cache.
"""

import contextlib
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import parcours  # noqa: E402

INPUT_TEXT = (
    "Bonjour, nous sommes la société Dupuis Menuiserie et nous voulons former nos vingt "
    "commerciaux à la vente consultative avant la fin du premier trimestre.\n\n"
    "Notre budget est d'environ trente mille euros hors taxes et nous préférons une formation "
    "en présentiel dans nos locaux de Lyon. Pouvez-vous nous dire ce que vous proposez ?\n"
)
ANSWERS_TEXT = "ANSWERS-FROM-CLIENT: le budget est confirmé, la date reste ouverte.\n"
STUB_SKILLS = {
    "ix-skills": ["cadrage", "questioning", "explorer", "decision", "brief", "controle-qualite", "deliver"],
    "ix-recipes": ["analyse-cdc", "offre-commerciale"],
}


def fake_output(defn, context_fields=None, retry=False):
    """A well-formed engine output for a step; every field value is a unique marker."""
    whole = defn.get("output_field")
    parts = [] if retry else [f"Complete analysis written by step {defn['id']}.\n"
                              + (f"VALUE[{defn['id']}.{whole}]\n" if whole else "")]
    if context_fields:
        sheet = {f: f"CTX-{f}" for f in context_fields}
        parts.append("## CONTEXT SHEET\n```json\n" + json.dumps(sheet) + "\n```\n")
    parts.append("## HANDOFF\n")
    for field in defn["transmits"]:
        if field != whole:
            parts.append(f"### {field}\nVALUE[{defn['id']}.{field}]\n")
    parts.append(f"## SUMMARY\nSummary of {defn['id']}.\n")
    return "\n".join(parts)


class ParcoursTestCase(unittest.TestCase):
    """Temporary repo layout, fake engine fixtures and a CLI helper."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test-parcours-")).resolve()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.root = self.tmp / "ix-recipes"
        self.pdir = self.tmp / "parcours"
        self.fake = self.tmp / "fake"
        self.fake.mkdir()
        self.build_layout()
        env = {"PARCOURS_FAKE_DIR": str(self.fake), "HOME": str(self.tmp / "home")}
        patcher = mock.patch.dict(os.environ, env)
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop("IX_SKILLS_PATH", None)
        patcher = mock.patch.object(parcours, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.input_file = self.tmp / "demande.md"
        self.input_file.write_text(INPUT_TEXT, encoding="utf-8")
        self.answers_file = self.tmp / "reponses.md"
        self.answers_file.write_text(ANSWERS_TEXT, encoding="utf-8")

    def build_layout(self):
        (self.root / "skills").mkdir(parents=True)
        for recipe in ("brief-client", "reponse-appel-offres"):
            shutil.copy(REPO / "skills" / f"{recipe}.md", self.root / "skills")
        for namespace, ids in STUB_SKILLS.items():
            base = self.root / "dist" / "skills" if namespace == "ix-recipes" else self.tmp / "ix-skills" / "dist" / "skills"
            for skill_id in ids:
                self.write_skill(base, skill_id)

    def write_skill(self, base, skill_id, extra=""):
        folder = base / skill_id
        folder.mkdir(parents=True, exist_ok=True)
        text = f"---\nname: {skill_id}\ndescription: stub\n{extra}---\n# Method of {skill_id}\nSTUB-METHOD-{skill_id}\n"
        (folder / "SKILL.md").write_text(text, encoding="utf-8")
        return folder

    # -- helpers ----------------------------------------------------------
    def cli(self, *argv):
        """Run the CLI; returns (exit code, stdout, stderr)."""
        out, err = io.StringIO(), io.StringIO()
        full = list(argv) + ["--parcours-dir", str(self.pdir)]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = parcours.main(full)
        return code, out.getvalue(), err.getvalue()

    def ok(self, *argv):
        code, out, err = self.cli(*argv)
        self.assertEqual(code, 0, f"{argv} -> {code}\n{out}\n{err}")
        return out

    def new(self, recipe="brief-client", slug="demo", *extra):
        self.ok("new", recipe, "--input", str(self.input_file), "--slug", slug, "--engine", "fake", *extra)
        return slug

    def state(self, slug="demo"):
        return json.loads((self.pdir / slug / "state.json").read_text(encoding="utf-8"))

    def step(self, step_id, slug="demo"):
        return next(s for s in self.state(slug)["steps"] if s["id"] == step_id)

    def recipe(self, recipe_id):
        return parcours.load_recipe(recipe_id)

    def write_fakes(self, recipe_id, **overrides):
        """Canned outputs for every step of a recipe; `overrides` maps '<step>' or '<step>.retry' to text."""
        recipe = self.recipe(recipe_id)
        for defn in recipe["steps"]:
            ctx = recipe["context_sheet"] if defn["produces_context_sheet"] else None
            (self.fake / f"{defn['id']}.md").write_text(fake_output(defn, ctx), encoding="utf-8")
            (self.fake / f"{defn['id']}.retry.md").write_text(fake_output(defn, ctx, retry=True), encoding="utf-8")
        for name, text in overrides.items():
            (self.fake / f"{name.replace('__', '.')}.md").write_text(text, encoding="utf-8")

    def received(self, step_id, kind=""):
        name = f"{step_id}.retry.md" if kind == "retry" else f"{step_id}.md"
        return (self.fake / "received" / name).read_text(encoding="utf-8")

    def was_called(self, step_id):
        return (self.fake / "received" / f"{step_id}.md").exists()

    def drive(self, slug="demo", run=None):
        """Play a parcours to the end, answering every pause. `run`: optional steps to play (None = skip)."""
        for _ in range(40):
            self.ok("next", slug, "--yes")
            state = self.state(slug)
            if state["status"] != "active":
                return state
            pending = state["pending"]
            if pending["type"] == "validate":
                self.ok("validate", slug)
            elif pending["type"] == "answers":
                self.ok("answer", slug, "--file", str(self.answers_file))
            elif pending["type"] == "choose" and run:
                self.ok("choose", slug, "--run", ",".join(run))
            else:
                self.ok("choose", slug, "--skip")
        self.fail("parcours did not finish")


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
class ParsingTests(unittest.TestCase):
    FIELDS = ["need", "constraints"]

    def parse(self, text, fields=None, **kw):
        return parcours.parse_step_output(text, fields or self.FIELDS, **kw)

    def test_sections_by_heading(self):
        text = "Long analysis.\n\n## HANDOFF\n### need\nA need.\n\n### constraints\nA limit.\n\n## SUMMARY\nShort.\n"
        result = self.parse(text)
        self.assertEqual(result["handoff"], {"need": "A need.", "constraints": "A limit."})
        self.assertEqual(result["summary"], "Short.")
        self.assertEqual(result["warnings"], [])

    def test_multi_paragraph_value(self):
        text = "## HANDOFF\n### need\nFirst paragraph.\n\nSecond paragraph.\n\n- a bullet\n- another\n\n### constraints\nx\n## SUMMARY\ns\n"
        value = self.parse(text)["handoff"]["need"]
        self.assertEqual(value, "First paragraph.\n\nSecond paragraph.\n\n- a bullet\n- another")

    def test_code_fences_and_quotes_inside_values(self):
        text = (
            "## HANDOFF\n### need\nSee:\n```md\n### constraints\nnot a field\n## SUMMARY\nnot a section\n```\n"
            "~~~~\n### fake\n~~~~\n> ### quoted\n> a quote\n\n### constraints\nreal\n## SUMMARY\nS\n"
        )
        result = self.parse(text)
        self.assertIn("### constraints\nnot a field", result["handoff"]["need"])
        self.assertIn("## SUMMARY\nnot a section", result["handoff"]["need"])
        self.assertIn("> ### quoted\n> a quote", result["handoff"]["need"])
        self.assertEqual(result["handoff"]["constraints"], "real")
        self.assertEqual(result["summary"], "S")
        self.assertEqual(result["warnings"], [])

    def test_longer_fence_is_not_closed_by_a_shorter_one(self):
        text = "## HANDOFF\n### need\n````\n```\n### constraints\n````\nafter\n### constraints\nreal\n## SUMMARY\nS\n"
        result = self.parse(text)
        self.assertIn("### constraints", result["handoff"]["need"])
        self.assertEqual(result["handoff"]["constraints"], "real")

    def test_value_may_hold_its_own_level_two_heading(self):
        text = "## HANDOFF\n### need\n## Option A\ntext\n### constraints\nc\n## SUMMARY\nS\n"
        self.assertEqual(self.parse(text)["handoff"]["need"], "## Option A\ntext")

    def test_field_names_ignore_case_spaces_and_decoration(self):
        text = "## HANDOFF\n### NEED\nn\n### **Open  Points**:\no\n### `Constraints`\nc\n## SUMMARY\nS\n"
        result = self.parse(text, ["need", "open_points", "constraints"])
        self.assertEqual(result["handoff"], {"need": "n", "open_points": "o", "constraints": "c"})

    def test_heading_names_ignore_case(self):
        text = "## handoff\n### need\nn\n### constraints\nc\n## Summary\nS\n"
        self.assertEqual(self.parse(text)["summary"], "S")

    def test_extra_field_is_ignored_with_a_warning(self):
        text = "## HANDOFF\n### need\nn\n### constraints\nc\n### bonus\nb\n## SUMMARY\nS\n"
        result = self.parse(text)
        self.assertNotIn("bonus", result["handoff"])
        self.assertTrue(any("bonus" in w for w in result["warnings"]))

    def test_missing_or_empty_field_raises(self):
        with self.assertRaisesRegex(parcours.ParseError, "constraints"):
            self.parse("## HANDOFF\n### need\nn\n## SUMMARY\nS\n")
        with self.assertRaisesRegex(parcours.ParseError, "constraints"):
            self.parse("## HANDOFF\n### need\nn\n### constraints\n\n\n## SUMMARY\nS\n")

    def test_missing_handoff_block_raises(self):
        with self.assertRaisesRegex(parcours.ParseError, "HANDOFF"):
            self.parse("Just prose, no blocks.")

    def test_last_handoff_block_wins(self):
        text = "I will end with:\n## HANDOFF\n### need\nDRAFT\n### constraints\nDRAFT\n## SUMMARY\nx\n\n" \
               "## HANDOFF\n### need\nFINAL\n### constraints\nFINAL\n## SUMMARY\ny\n"
        self.assertEqual(self.parse(text)["handoff"]["need"], "FINAL")

    def test_missing_summary_is_only_a_warning(self):
        result = self.parse("## HANDOFF\n### need\nn\n### constraints\nc\n")
        self.assertEqual(result["summary"], "")
        self.assertTrue(any("SUMMARY" in w for w in result["warnings"]))

    def test_context_sheet_before_or_after_handoff(self):
        sheet = '```json\n{"client": "ACME", "objective": "train"}\n```'
        fields = ["client", "objective"]
        before = f"## CONTEXT SHEET\n{sheet}\n## HANDOFF\n### need\nn\n### constraints\nc\n## SUMMARY\nS\n"
        after = f"## HANDOFF\n### need\nn\n### constraints\nc\n## SUMMARY\nS\n## CONTEXT SHEET\n{sheet}\n"
        for text in (before, after):
            result = self.parse(text, context_fields=fields)
            self.assertEqual(result["context_sheet"], {"client": "ACME", "objective": "train"})
            self.assertEqual(result["handoff"]["constraints"], "c")

    def test_context_sheet_missing_key_becomes_not_stated(self):
        text = '## CONTEXT SHEET\n```json\n{"client": "ACME"}\n```\n## HANDOFF\n### need\nn\n### constraints\nc\n## SUMMARY\nS\n'
        result = self.parse(text, context_fields=["client", "deadlines"])
        self.assertEqual(result["context_sheet"]["deadlines"], parcours.NOT_STATED)
        self.assertTrue(any("deadlines" in w for w in result["warnings"]))

    def test_context_sheet_errors(self):
        base = "## HANDOFF\n### need\nn\n### constraints\nc\n## SUMMARY\nS\n"
        with self.assertRaisesRegex(parcours.ParseError, "CONTEXT SHEET"):
            self.parse(base, context_fields=["client"])
        with self.assertRaisesRegex(parcours.ParseError, "JSON"):
            self.parse("## CONTEXT SHEET\n```json\n{oops\n```\n" + base, context_fields=["client"])


# ---------------------------------------------------------------------------
# Isolation of the raw request
# ---------------------------------------------------------------------------
class LeakCheckTests(unittest.TestCase):
    def test_detects_a_reformatted_passage(self):
        message = "intro\n" + INPUT_TEXT.replace("\n\n", " ").upper().replace(",", " ;") + "\noutro"
        self.assertIsNotNone(parcours.find_leak(message, INPUT_TEXT))

    def test_ignores_short_overlaps(self):
        message = "Le budget est d'environ trente mille euros, a-t-on dit."
        self.assertIsNone(parcours.find_leak(message, INPUT_TEXT))

    def test_file_name_is_not_content(self):
        self.assertIsNone(parcours.find_leak("see input.md and demande.md", INPUT_TEXT))

    def test_tiny_input_is_not_checked(self):
        self.assertIsNone(parcours.find_leak("Formation commerciale", "Formation"))


class IsolationTests(ParcoursTestCase):
    def test_no_step_after_the_first_contains_the_raw_request(self):
        for recipe_id in ("brief-client", "reponse-appel-offres"):
            slug = self.new(recipe_id, slug=recipe_id)
            self.write_fakes(recipe_id)
            self.drive(slug, run=["explorer", "decision"])
            recipe = self.recipe(recipe_id)
            for idx, defn in enumerate(recipe["steps"]):
                message = self.received(defn["id"])
                if idx == 0:
                    continue
                self.assertIsNone(parcours.find_leak(message, INPUT_TEXT), defn["id"])
                self.assertNotIn("Dupuis Menuiserie", message, defn["id"])
                self.assertNotIn("vente consultative", message, defn["id"])

    def test_first_step_receives_the_raw_input(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        message = self.received("cadrage")
        self.assertIn(INPUT_TEXT, message)
        self.assertEqual(re.findall(r"^=== INPUT: (.+?) ===$", message, re.M), ["brief"])
        self.assertNotIn("=== CONTEXT SHEET ===", message)

    def leaking_cadrage(self, field="need", sheet=False):
        """Canned cadrage output copying a paragraph of the raw request into a field (or the sheet)."""
        recipe = self.recipe("brief-client")
        text = fake_output(recipe["steps"][0], recipe["context_sheet"])
        paragraph = " ".join(INPUT_TEXT.split()[:45])
        if sheet:
            return text.replace("CTX-client", paragraph)
        return text.replace(f"VALUE[cadrage.{field}]", f"The client says: {paragraph}")

    def test_a_fragment_leaking_through_a_handoff_field_fails_the_step_at_once(self):
        self.new()
        self.write_fakes("brief-client", cadrage=self.leaking_cadrage())
        code, _, err = self.cli("next", "demo", "--yes")
        self.assertEqual(code, 1)
        self.assertIn("isolation", err)
        self.assertIn("le champ 'need'", err)
        self.assertIn("bonjour nous sommes", err)  # the fragment is named
        self.assertEqual(self.step("cadrage")["status"], "failed")
        self.assertIsNone(self.state()["pending"])
        self.assertFalse(self.was_called("questioning"))

    def test_the_remedy_named_in_the_leak_message_works(self):
        self.new()
        self.write_fakes("brief-client", cadrage=self.leaking_cadrage())
        _, _, err = self.cli("next", "demo", "--yes")
        self.assertIn("handoff demo cadrage --file", err)
        self.assertIn("rerun demo cadrage", err)
        # remedy 1: cleaned fields by hand
        fields = self.tmp / "champs.md"
        fields.write_text(
            "### need\nclean need\n### constraints\nc\n### hypotheses\nh\n### open_points\no\n"
            '## CONTEXT SHEET\n```json\n{"client": "x"}\n```\n## SUMMARY\nS\n', encoding="utf-8")
        self.ok("handoff", "demo", "cadrage", "--file", str(fields))
        self.assertEqual(self.step("cadrage")["status"], "paused")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        self.assertTrue(self.was_called("questioning"))

    def test_rerun_is_the_other_remedy_and_calls_the_engine_again(self):
        self.new()
        self.write_fakes("brief-client", cadrage=self.leaking_cadrage())
        self.cli("next", "demo", "--yes")
        self.write_fakes("brief-client")
        self.ok("rerun", "demo", "cadrage")
        self.ok("next", "demo", "--yes")
        self.assertEqual(self.step("cadrage")["status"], "paused")
        self.assertEqual(self.state()["calls"], {"fake": 2})
        self.assertTrue((self.pdir / "demo" / "01-cadrage.v1.md").is_file())

    def test_a_leak_in_the_context_sheet_fails_the_step(self):
        self.new()
        self.write_fakes("brief-client", cadrage=self.leaking_cadrage(sheet=True))
        code, _, err = self.cli("next", "demo", "--yes")
        self.assertEqual(code, 1)
        self.assertIn("la fiche de contexte", err)
        self.assertEqual(self.step("cadrage")["status"], "failed")
        self.assertIsNone(self.state()["context_sheet"])

    def test_validate_context_refuses_a_sheet_that_copies_the_request(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        sheet = self.tmp / "fiche.json"
        sheet.write_text(json.dumps({"client": " ".join(INPUT_TEXT.split()[:45])}), encoding="utf-8")
        code, _, err = self.cli("validate", "demo", "--context", str(sheet))
        self.assertEqual(code, 1)
        self.assertIn("isolation", err)
        self.assertIn("bonjour nous sommes", err)
        self.assertEqual(self.state()["context_sheet"]["client"], "CTX-client")  # unchanged
        self.assertFalse((self.pdir / "demo" / "00-context.v1.md").exists())
        self.assertEqual(self.state()["pending"]["type"], "validate")

    def test_an_old_state_with_a_leaking_field_is_still_refused_before_the_call(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo")
        path = self.pdir / "demo" / "state.json"
        state = json.loads(path.read_text())
        state["steps"][0]["handoff"]["need"] = " ".join(INPUT_TEXT.split()[:45])  # as if edited by hand
        path.write_text(json.dumps(state))
        code, _, err = self.cli("next", "demo", "--yes")
        self.assertEqual(code, 1)
        self.assertIn("isolation", err)
        self.assertIn("'cadrage.need'", err)
        self.assertIn("handoff demo cadrage --file", err)
        self.assertFalse(self.was_called("questioning"))
        self.assertFalse((self.pdir / "demo" / "02-questioning.in.md").exists())  # nothing sent, nothing traced
        self.assertEqual(self.step("questioning")["status"], "pending")

    def test_a_short_verbatim_quote_is_allowed(self):
        self.new()
        self.write_fakes("brief-client")
        quoting = fake_output(self.recipe("brief-client")["steps"][0], self.recipe("brief-client")["context_sheet"])
        sentence = "nous préférons une formation en présentiel dans nos locaux de Lyon"
        quoting = quoting.replace("VALUE[cadrage.need]", f"The client says: « {sentence} ».")
        (self.fake / "cadrage.md").write_text(quoting, encoding="utf-8")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        self.assertTrue(self.was_called("questioning"))

    def test_a_manual_handoff_that_leaks_is_refused_too(self):
        self.new()
        self.write_fakes("brief-client", cadrage="no handoff here")
        (self.fake / "cadrage.retry.md").write_text("still nothing", encoding="utf-8")
        code, _, _ = self.cli("next", "demo", "--yes")
        self.assertEqual(code, 1)
        fields = self.tmp / "champs.md"
        paragraph = " ".join(INPUT_TEXT.split()[:45])
        fields.write_text(
            f"### need\nThe client wrote: {paragraph}\n"
            "### constraints\nc\n### hypotheses\nh\n### open_points\no\n"
            '## CONTEXT SHEET\n```json\n{"client": "x"}\n```\n## SUMMARY\nS\n',
            encoding="utf-8",
        )
        code, _, err = self.cli("handoff", "demo", "cadrage", "--file", str(fields))
        self.assertEqual(code, 1)
        self.assertIn("isolation", err)
        self.assertEqual(self.step("cadrage")["status"], "failed")  # nothing recorded

    def test_a_manual_correction_that_leaks_is_refused_on_a_paused_step_too(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        fields = self.tmp / "champs.md"
        paragraph = " ".join(INPUT_TEXT.split()[:45])
        fields.write_text(
            f"### need\n{paragraph}\n### constraints\nc\n### hypotheses\nh\n### open_points\no\n"
            '## CONTEXT SHEET\n```json\n{"client": "x"}\n```\n', encoding="utf-8")
        code, _, err = self.cli("handoff", "demo", "cadrage", "--file", str(fields))
        self.assertEqual(code, 1)
        self.assertIn("isolation", err)
        self.assertEqual(self.step("cadrage")["handoff"]["need"], "VALUE[cadrage.need]")
        self.assertFalse((self.pdir / "demo" / "01-cadrage.v1.md").exists())


# ---------------------------------------------------------------------------
# What each step receives
# ---------------------------------------------------------------------------
class MessageContentTests(ParcoursTestCase):
    def check_recipe_messages(self, recipe_id, run=None):
        slug = self.new(recipe_id, slug=recipe_id)
        self.write_fakes(recipe_id)
        state = self.drive(slug, run=run)
        self.assertEqual(state["status"], "completed")
        recipe = self.recipe(recipe_id)
        for idx, defn in enumerate(recipe["steps"]):
            if state["steps"][idx]["status"] == "skipped":
                self.assertFalse(self.was_called(defn["id"]))
                continue
            message = self.received(defn["id"])
            expected = [r for r in defn["receives"] if r != "context_sheet"]
            self.assertEqual(re.findall(r"^=== INPUT: (.+?) ===$", message, re.M), expected, defn["id"])
            self.assertEqual("=== CONTEXT SHEET ===" in message, idx > 0, defn["id"])
            markers = set(re.findall(r"VALUE\[([^\]]+)\]", message))
            produced = {r for r in expected if "." in r and state["steps"][self.index(state, r)]["status"] != "skipped"}
            self.assertEqual(markers, produced, defn["id"])
            self.assertIn(f"=== SKILL: {defn['skill']} ===", message)
            self.assertIn(f"STUB-METHOD-{defn['skill'].split(':')[1]}", message)
            self.assertIn(defn["mission"], message)
            for field in defn["transmits"]:
                if field == defn.get("output_field"):
                    self.assertIn(f"passed on as `{field}`", message)
                else:
                    self.assertIn(f"### {field}", message)
            if "answers" in expected:
                self.assertIn(ANSWERS_TEXT.strip(), message)
            if idx > 0:
                self.assertIn("CTX-" + recipe["context_sheet"][0], message)
        return state

    @staticmethod
    def index(state, source):
        step_id = source.split(".")[0]
        return next(i for i, s in enumerate(state["steps"]) if s["id"] == step_id)

    def test_brief_client_all_steps_get_exactly_their_fields(self):
        self.check_recipe_messages("brief-client", run=["explorer", "decision"])

    def test_brief_client_with_skipped_steps(self):
        state = self.check_recipe_messages("brief-client", run=None)
        self.assertEqual([s["status"] for s in state["steps"]], ["done", "done", "skipped", "skipped", "done"])

    def test_reponse_appel_offres_all_steps_get_exactly_their_fields(self):
        state = self.check_recipe_messages("reponse-appel-offres")
        self.assertEqual(len(state["steps"]), 7)

    def test_step_without_context_sheet_in_receives_still_gets_it(self):
        # conformite lists no context_sheet but spec section 3 sends it from step 2 on
        self.new("reponse-appel-offres", slug="rao")
        self.write_fakes("reponse-appel-offres")
        self.drive("rao")
        self.assertNotIn("context_sheet", self.recipe("reponse-appel-offres")["steps"][5]["receives"])
        self.assertIn("=== CONTEXT SHEET ===", self.received("conformite"))

    def test_message_orders_instructions(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        message = self.received("cadrage")
        for needle in ("the HANDOFF wins", "Stay strictly within the mission", "## CONTEXT SHEET",
                       "do not answer the request yourself", "5 lines at most"):
            self.assertIn(needle, message)


# ---------------------------------------------------------------------------
# End to end: brief-client with the fake engine
# ---------------------------------------------------------------------------
class BriefClientFlowTests(ParcoursTestCase):
    def test_full_run_with_skipped_branch(self):
        self.new()
        self.write_fakes("brief-client")

        out = self.ok("next", "demo", "--yes")
        state = self.state()
        self.assertEqual(self.step("cadrage")["status"], "paused")
        self.assertEqual(state["pending"]["type"], "validate")
        self.assertEqual(self.step("questioning")["status"], "pending")
        self.assertEqual(state["context_sheet"]["client"], "CTX-client")
        self.assertFalse(state["context_validated"])
        self.assertIn("Fiche de contexte", out)
        self.assertTrue((self.pdir / "demo" / "00-context.md").is_file())
        self.assertTrue((self.pdir / "demo" / "01-cadrage.md").is_file())
        self.assertFalse(self.was_called("questioning"))

        self.ok("validate", "demo")
        self.assertTrue(self.state()["context_validated"])
        self.assertEqual(self.step("cadrage")["status"], "done")

        self.ok("next", "demo", "--yes")
        self.assertEqual(self.step("questioning")["status"], "paused")
        self.assertEqual(self.state()["pending"]["type"], "answers")

        self.ok("answer", "demo", "--file", str(self.answers_file))
        self.assertEqual((self.pdir / "demo" / "answers.md").read_text(), ANSWERS_TEXT)
        self.assertEqual(self.state()["pending"]["type"], "choose")
        self.assertEqual(self.state()["pending"]["steps"], ["explorer", "decision"])

        self.ok("choose", "demo", "--skip")
        self.assertEqual(self.step("explorer")["status"], "skipped")
        self.assertEqual(self.step("decision")["status"], "skipped")
        self.assertIsNone(self.state()["pending"])

        self.ok("next", "demo", "--yes")
        state = self.state()
        self.assertEqual(state["status"], "completed")
        self.assertEqual(self.step("brief")["status"], "done")
        brief_message = self.received("brief")
        self.assertRegex(brief_message, r"=== INPUT: decision\.chosen_direction ===\nskipped\n=== END INPUT ===")
        self.assertNotIn("VALUE[decision", brief_message)
        self.assertFalse(self.was_called("explorer"))
        self.assertFalse(self.was_called("decision"))

    def test_choose_run_plays_the_optional_steps(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        self.ok("answer", "demo", "--none")
        self.assertEqual((self.pdir / "demo" / "answers.md").read_text().strip(), parcours.NO_ANSWERS)
        self.ok("choose", "demo", "--run", "explorer,decision")
        self.ok("next", "demo", "--yes")
        self.assertEqual(self.step("explorer")["status"], "done")
        self.assertEqual(self.step("decision")["status"], "paused")
        self.assertIn(parcours.NO_ANSWERS, self.received("explorer"))
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        self.assertEqual(self.state()["status"], "completed")
        self.assertIn("VALUE[decision.chosen_direction]", self.received("brief"))

    def test_choose_a_single_optional_step(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        self.ok("answer", "demo", "--none")
        self.ok("choose", "demo", "--run", "explorer")
        self.assertEqual(self.step("decision")["status"], "skipped")
        self.ok("next", "demo", "--yes")
        self.assertEqual(self.step("explorer")["status"], "done")
        self.assertEqual(self.state()["status"], "completed")
        self.assertRegex(self.received("brief"), r"=== INPUT: decision\.chosen_direction ===\nskipped\n")

    def test_commands_refuse_the_wrong_pause(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        for argv in (("answer", "demo", "--none"), ("choose", "demo", "--skip")):
            code, _, err = self.cli(*argv)
            self.assertEqual(code, 1)
            self.assertIn("attend une pause", err)
        code, out, _ = self.cli("next", "demo", "--yes")
        self.assertEqual(code, 0)
        self.assertIn("En attente (validate)", out)

    def test_validate_stop_stops_the_parcours(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo", "--stop")
        self.assertEqual(self.state()["status"], "stopped")
        out = self.ok("next", "demo", "--yes")
        self.assertIn("stopped", out)
        self.assertFalse(self.was_called("questioning"))

    def test_context_edit_keeps_the_previous_version(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        original = (self.pdir / "demo" / "00-context.md").read_text()
        sheet = self.tmp / "fiche.json"
        sheet.write_text(json.dumps({"client": "EDITED-CLIENT", "objective": "o"}), encoding="utf-8")
        self.ok("validate", "demo", "--context", str(sheet))
        folder = self.pdir / "demo"
        self.assertEqual((folder / "00-context.v1.md").read_text(), original)
        self.assertIn("EDITED-CLIENT", (folder / "00-context.md").read_text())
        self.assertEqual(self.state()["context_sheet"]["client"], "EDITED-CLIENT")
        self.ok("next", "demo", "--yes")
        self.assertIn("EDITED-CLIENT", self.received("questioning"))

    def test_context_edit_twice_numbers_the_versions(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        sheet = self.tmp / "fiche.json"
        sheet.write_text(json.dumps({"client": "v2"}), encoding="utf-8")
        self.ok("validate", "demo", "--context", str(sheet))
        self.ok("rerun", "demo", "cadrage")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo")
        self.assertTrue((self.pdir / "demo" / "00-context.v2.md").exists())

    def test_rerun_with_extra_field(self):
        self.new()
        self.write_fakes("brief-client")
        self.drive()
        folder = self.pdir / "demo"
        first_output = (folder / "05-brief.md").read_text()
        self.ok("rerun", "demo", "brief", "--extra", "questioning.client_questions")
        self.assertEqual(self.step("brief")["status"], "pending")
        self.assertEqual(self.state()["status"], "active")
        self.assertEqual((folder / "05-brief.v1.md").read_text(), first_output)
        self.ok("next", "demo", "--yes")
        message = self.received("brief")
        self.assertRegex(message, r"=== INPUT: questioning\.client_questions ===\nVALUE\[questioning\.client_questions\]")
        self.assertEqual(self.state()["status"], "completed")

    def test_rerun_resets_the_downstream_steps(self):
        self.new("reponse-appel-offres", slug="rao")
        self.write_fakes("reponse-appel-offres")
        self.drive("rao")
        self.ok("rerun", "rao", "offre", "--extra", "conformite.compliance_verdicts")
        statuses = {s["id"]: s["status"] for s in self.state("rao")["steps"]}
        self.assertEqual(statuses["offre"], "pending")
        self.assertEqual(statuses["conformite"], "pending")
        self.assertEqual(statuses["mise-en-forme"], "pending")
        self.assertEqual(statuses["strategie"], "done")
        self.ok("next", "rao", "--yes")
        self.assertIn("=== INPUT: conformite.compliance_verdicts ===", self.received("offre"))
        self.assertEqual(self.state("rao")["pending"]["step"], "conformite")

    def test_rerun_extra_must_exist(self):
        self.new()
        self.write_fakes("brief-client")
        self.drive()
        code, _, err = self.cli("rerun", "demo", "brief", "--extra", "decision.chosen_direction")
        self.assertEqual(code, 1)
        self.assertIn("indisponible", err)


# ---------------------------------------------------------------------------
# Failures: retry, failed, handoff --file, orphan running
# ---------------------------------------------------------------------------
class FailureTests(ParcoursTestCase):
    def malformed(self):
        defn = self.recipe("brief-client")["steps"][0]
        text = fake_output(defn, self.recipe("brief-client")["context_sheet"])
        return text.replace("### constraints\nVALUE[cadrage.constraints]\n", "")

    def test_malformed_output_gets_one_retry_on_the_produced_output_only(self):
        self.new()
        self.write_fakes("brief-client", cadrage=self.malformed())
        self.ok("next", "demo", "--yes")
        step = self.step("cadrage")
        self.assertEqual(step["status"], "paused")
        self.assertEqual(step["handoff"]["constraints"], "VALUE[cadrage.constraints]")
        retry_message = self.received("cadrage", "retry")
        self.assertIn("Complete analysis written by step cadrage.", retry_message)  # the produced output
        self.assertIn("constraints", retry_message)
        self.assertIsNone(parcours.find_leak(retry_message, INPUT_TEXT))
        self.assertNotIn("STUB-METHOD", retry_message)  # no skill, no input
        self.assertNotIn("=== INPUT", retry_message)
        self.assertEqual(self.state()["calls"], {"fake": 2})
        self.assertIn("<!-- retry output -->", (self.pdir / "demo" / "01-cadrage.md").read_text())

    def test_second_failure_marks_the_step_failed_and_handoff_repairs_it(self):
        self.new()
        self.write_fakes("brief-client", cadrage=self.malformed(), cadrage__retry="## SUMMARY\nonly a summary\n")
        code, _, err = self.cli("next", "demo", "--yes")
        self.assertEqual(code, 1)
        self.assertIn("après relance", err)
        step = self.step("cadrage")
        self.assertEqual(step["status"], "failed")
        self.assertIn("HANDOFF", step["error"])
        self.assertEqual(self.state()["calls"], {"fake": 2})

        code, _, err = self.cli("next", "demo", "--yes")  # failed step blocks the run
        self.assertEqual(code, 1)
        self.assertIn("échoué", err)

        fields = self.tmp / "champs.md"
        fields.write_text(
            "### Need\nn\n### Constraints\nc\n### hypotheses\nh\n### open points\no\n"
            '## CONTEXT SHEET\n```json\n{"client": "by hand"}\n```\n## SUMMARY\nby hand\n',
            encoding="utf-8",
        )
        self.ok("handoff", "demo", "cadrage", "--file", str(fields))
        step = self.step("cadrage")
        self.assertEqual(step["status"], "paused")
        self.assertEqual(step["handoff"]["open_points"], "o")
        self.assertEqual(self.state()["context_sheet"]["client"], "by hand")
        self.assertEqual(self.state()["pending"]["type"], "validate")

    def test_handoff_refuses_a_step_that_has_not_run(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        fields = self.tmp / "champs.md"
        fields.write_text("### need\nn\n", encoding="utf-8")
        code, _, err = self.cli("handoff", "demo", "questioning", "--file", str(fields))  # still pending
        self.assertEqual(code, 1)
        self.assertIn("ni en échec", err)

    def test_handoff_file_with_a_missing_field_is_refused(self):
        self.new()
        self.write_fakes("brief-client", cadrage="nothing", cadrage__retry="nothing")
        self.cli("next", "demo", "--yes")
        fields = self.tmp / "champs.md"
        fields.write_text("### need\nn\n", encoding="utf-8")
        code, _, err = self.cli("handoff", "demo", "cadrage", "--file", str(fields))
        self.assertEqual(code, 1)
        self.assertEqual(self.step("cadrage")["status"], "failed")

    def test_orphan_running_step_is_detected_and_fixed_by_retry(self):
        self.new()
        self.write_fakes("brief-client")
        path = self.pdir / "demo" / "state.json"
        state = json.loads(path.read_text())
        state["steps"][0]["status"] = "running"  # what a killed process leaves behind
        path.write_text(json.dumps(state))
        code, _, err = self.cli("next", "demo", "--yes")
        self.assertEqual(code, 1)
        self.assertIn("running", err)
        self.assertIn("retry", err)
        self.ok("retry", "demo")
        self.assertEqual(self.step("cadrage")["status"], "pending")
        self.ok("next", "demo", "--yes")
        self.assertEqual(self.step("cadrage")["status"], "paused")

    def test_retry_with_nothing_to_retry(self):
        self.new()
        code, _, err = self.cli("retry", "demo")
        self.assertEqual(code, 1)

    def test_engine_error_marks_the_step_failed_then_retry(self):
        self.new()  # no canned file: the fake engine raises
        code, _, err = self.cli("next", "demo", "--yes")
        self.assertEqual(code, 1)
        self.assertEqual(self.step("cadrage")["status"], "failed")
        self.write_fakes("brief-client")
        self.ok("retry", "demo")
        self.ok("next", "demo", "--yes")
        self.assertEqual(self.step("cadrage")["status"], "paused")


# ---------------------------------------------------------------------------
# State machine robustness
# ---------------------------------------------------------------------------
class RobustnessTests(ParcoursTestCase):
    def test_atomic_write_keeps_the_old_file_on_failure(self):
        target = self.tmp / "state.json"
        target.write_text("OLD", encoding="utf-8")
        with mock.patch.object(parcours.os, "replace", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                parcours.write_atomic(target, "NEW")
        self.assertEqual(target.read_text(), "OLD")
        self.assertEqual([p.name for p in self.tmp.iterdir() if p.name.endswith(".tmp")], [])
        parcours.write_atomic(target, "NEW")
        self.assertEqual(target.read_text(), "NEW")

    def test_atomic_write_survives_a_failure_while_writing(self):
        target = self.tmp / "state.json"
        target.write_text("OLD", encoding="utf-8")
        with mock.patch.object(Path, "write_text", side_effect=OSError("boom")):
            with self.assertRaises(OSError):
                parcours.write_atomic(target, "NEW")
        self.assertEqual(target.read_text(), "OLD")

    def test_state_json_is_never_left_half_written(self):
        self.new()
        self.write_fakes("brief-client")
        with mock.patch.object(parcours.os, "replace", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                self.cli("next", "demo", "--yes")
        json.loads((self.pdir / "demo" / "state.json").read_text())  # still valid JSON

    def test_lock_prevents_concurrent_next(self):
        self.new()
        self.write_fakes("brief-client")
        with parcours.parcours_lock(self.pdir / "demo"):
            code, _, err = self.cli("next", "demo", "--yes")
            self.assertEqual(code, 1)
            self.assertIn("verrou", err)
            self.assertFalse(self.was_called("cadrage"))
        self.ok("next", "demo", "--yes")  # released

    def test_slug_collision_gets_a_suffix(self):
        self.assertEqual(self.new(slug="demo"), "demo")
        self.new(slug="demo")
        self.new(slug="demo")
        self.assertTrue((self.pdir / "demo-2" / "state.json").is_file())
        self.assertTrue((self.pdir / "demo-3" / "state.json").is_file())
        self.assertEqual(self.state("demo-2")["slug"], "demo-2")

    def test_default_slug_comes_from_the_recipe_and_the_request(self):
        self.ok("new", "brief-client", "--input", str(self.input_file), "--engine", "fake")
        self.assertEqual([p.name for p in self.pdir.iterdir()], ["brief-client-bonjour-nous-sommes"])

    def test_new_records_the_request_and_the_initial_state(self):
        self.new()
        folder = self.pdir / "demo"
        self.assertEqual((folder / "input.md").read_text(), INPUT_TEXT)
        state = self.state()
        self.assertEqual(state["recipe"], "brief-client")
        self.assertEqual(state["recipe_version"], self.recipe("brief-client")["version"])
        self.assertEqual([s["status"] for s in state["steps"]], ["pending"] * 5)
        self.assertEqual(state["status"], "active")

    def test_new_rejects_unknown_recipe_and_engine_step(self):
        code, _, err = self.cli("new", "nope", "--input", str(self.input_file))
        self.assertEqual(code, 1)
        code, _, err = self.cli("new", "brief-client", "--input", str(self.input_file), "--engine-step", "ghost=agy")
        self.assertEqual(code, 1)
        self.assertIn("ghost", err)

    def test_unknown_parcours(self):
        code, _, err = self.cli("status", "ghost")
        self.assertEqual(code, 1)
        self.assertIn("introuvable", err)

    def test_completed_parcours_does_nothing(self):
        self.new()
        self.write_fakes("brief-client")
        self.drive()
        calls = dict(self.state()["calls"])
        out = self.ok("next", "demo", "--yes")
        self.assertIn("completed", out)
        self.assertEqual(self.state()["calls"], calls)


# ---------------------------------------------------------------------------
# Skill resolution
# ---------------------------------------------------------------------------
class SkillResolutionTests(ParcoursTestCase):
    def test_ix_skills_resolves_to_the_sibling_checkout(self):
        skill = parcours.resolve_skill("ix-skills:cadrage")
        self.assertEqual(Path(skill["path"]), self.tmp / "ix-skills" / "dist" / "skills" / "cadrage" / "SKILL.md")

    def test_ix_recipes_resolves_to_local_dist(self):
        skill = parcours.resolve_skill("ix-recipes:analyse-cdc")
        self.assertEqual(Path(skill["path"]), self.root / "dist" / "skills" / "analyse-cdc" / "SKILL.md")

    def test_namespace_is_mandatory_and_known(self):
        with self.assertRaisesRegex(parcours.ParcoursError, "espace de noms"):
            parcours.resolve_skill("cadrage")
        with self.assertRaisesRegex(parcours.ParcoursError, "inconnu"):
            parcours.resolve_skill("other:cadrage")
        with self.assertRaisesRegex(parcours.ParcoursError, "introuvable"):
            parcours.resolve_skill("ix-skills:does-not-exist")

    def test_the_same_id_in_another_namespace_is_not_confused(self):
        with self.assertRaises(parcours.ParcoursError):
            parcours.resolve_skill("ix-recipes:cadrage")  # exists only under ix-skills

    def test_env_path_comes_first(self):
        other = self.tmp / "custom"
        self.write_skill(other, "cadrage")
        with mock.patch.dict(os.environ, {"IX_SKILLS_PATH": str(other)}):
            skill = parcours.resolve_skill("ix-skills:cadrage")
        self.assertEqual(Path(skill["path"]), other / "cadrage" / "SKILL.md")

    def test_plugin_cache_is_the_last_resort_and_highest_version_wins(self):
        shutil.rmtree(self.tmp / "ix-skills")
        cache = Path(os.environ["HOME"]) / ".claude" / "plugins" / "cache" / "market" / "ix-skills"
        for version in ("3.3.0", "4.1.0", "4.0.0", "10.0.0", "9.9.9"):
            self.write_skill(cache / version / "skills", "cadrage")
        skill = parcours.resolve_skill("ix-skills:cadrage")
        self.assertIn("/10.0.0/", skill["path"])
        self.assertEqual(skill["version"], "10.0.0")

    def test_ix_recipes_falls_back_to_the_cache(self):
        shutil.rmtree(self.root / "dist")
        cache = Path(os.environ["HOME"]) / ".claude" / "plugins" / "cache" / "market" / "ix-recipes" / "2.2.0" / "skills"
        self.write_skill(cache, "analyse-cdc")
        skill = parcours.resolve_skill("ix-recipes:analyse-cdc")
        self.assertIn("/2.2.0/", skill["path"])

    def test_frontmatter_is_stripped_and_version_read(self):
        self.write_skill(self.tmp / "ix-skills" / "dist" / "skills", "cadrage", extra="version: 7.1.2\n")
        skill = parcours.resolve_skill("ix-skills:cadrage")
        self.assertEqual(skill["version"], "7.1.2")
        self.assertNotIn("description: stub", skill["text"])
        self.assertTrue(skill["text"].startswith("# Method of cadrage"))

    def test_version_comes_from_the_source_skill_next_to_dist(self):
        source = self.tmp / "ix-skills" / "skills"
        source.mkdir()
        (source / "cadrage.md").write_text("---\nid: cadrage\nversion: 3.9.1\n---\nbody\n", encoding="utf-8")
        self.assertEqual(parcours.resolve_skill("ix-skills:cadrage")["version"], "3.9.1")

    def test_path_and_version_are_recorded_per_step(self):
        source = self.tmp / "ix-skills" / "skills"
        source.mkdir()
        (source / "cadrage.md").write_text("---\nid: cadrage\nversion: 3.9.1\n---\nbody\n", encoding="utf-8")
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        recorded = self.step("cadrage")["skill"]
        self.assertEqual(recorded["ref"], "ix-skills:cadrage")
        self.assertEqual(recorded["version"], "3.9.1")
        self.assertTrue(recorded["path"].endswith("ix-skills/dist/skills/cadrage/SKILL.md"))
        self.assertEqual(self.step("cadrage")["engine"], "fake")
        self.assertEqual(self.step("cadrage")["model"], "opus")

    def test_references_are_copied_into_the_scratch_dir(self):
        folder = self.write_skill(self.tmp / "ix-skills" / "dist" / "skills", "cadrage")
        (folder / "references").mkdir()
        (folder / "references" / "guide.md").write_text("REF-CONTENT", encoding="utf-8")
        seen = {}

        def fake_run(argv, stdin, cwd, timeout):
            seen["listing"] = sorted(str(p.relative_to(cwd)) for p in Path(cwd).rglob("*"))
            seen["ref"] = (Path(cwd) / "references" / "guide.md").read_text()
            return 0, json.dumps({"result": "x", "total_cost_usd": 0}), ""

        skill = parcours.resolve_skill("ix-skills:cadrage")
        with mock.patch.object(parcours, "run_process", fake_run):
            parcours.call_engine("claude", "msg", model="opus", timeout=5, budget=5.0,
                                 skill=skill, step_id="cadrage", kind="main")
        self.assertEqual(seen["listing"], ["references", "references/guide.md"])
        self.assertEqual(seen["ref"], "REF-CONTENT")

    def test_a_verbatim_field_may_copy_passages_within_its_share(self):
        raw = " ".join(f"mot{i}" for i in range(300))
        (self.tmp / "p").mkdir(exist_ok=True)
        (self.tmp / "p" / "input.md").write_text(raw, encoding="utf-8")
        copied = "\n".join("- " + " ".join(f"mot{i}" for i in range(k, k + 20)) for k in range(0, 60, 20))  # a 3-item list
        parsed = {"handoff": {"imposed_items": copied, "need": "short"}, "context_sheet": None}
        self.assertIsNone(parcours.leak_in_parsed(raw, parsed, verbatim=["imposed_items"]))
        joined = {"handoff": {"imposed_items": copied.replace("\n- ", " "), "need": "short"}, "context_sheet": None}
        self.assertIsNotNone(parcours.leak_in_parsed(raw, joined, verbatim=()))  # undeclared: blocked

    def test_a_verbatim_list_covering_much_of_a_list_heavy_request_passes(self):
        raw = "\n".join(" ".join(f"m{j}x{i}" for i in range(12)) for j in range(25))
        items = "\n".join("- " + " ".join(f"m{j}x{i}" for i in range(12)) for j in range(20))  # 80 %, as a list
        parsed = {"handoff": {"imposed_items": items}, "context_sheet": None}
        self.assertIsNone(parcours.leak_in_parsed(raw, parsed, verbatim=["imposed_items"]))

    def test_a_verbatim_field_with_a_copied_paragraph_line_is_refused(self):
        raw = " ".join(f"mot{i}" for i in range(300))
        paragraph = " ".join(f"mot{i}" for i in range(100, 150))  # one 50-word line
        parsed = {"handoff": {"imposed_items": "- court\n" + paragraph}, "context_sheet": None}
        found = parcours.leak_in_parsed(raw, parsed, verbatim=["imposed_items"])
        self.assertIsNotNone(found)
        self.assertIn("paragraphe", found[0])

    def test_a_verbatim_field_copying_most_of_the_request_is_refused(self):
        raw = "\n".join(" ".join(f"m{j}x{i}" for i in range(12)) for j in range(25))
        items = "\n".join("- " + " ".join(f"m{j}x{i}" for i in range(12)) for j in range(25))  # 100 %
        parsed = {"handoff": {"imposed_items": items}, "context_sheet": None}
        found = parcours.leak_in_parsed(raw, parsed, verbatim=["imposed_items"])
        self.assertIsNotNone(found)
        self.assertIn("plafond", found[0])

    def test_a_verbatim_input_does_not_trip_the_message_check_but_others_still_do(self):
        directory = self.tmp / "pv"
        directory.mkdir()
        raw = " ".join(f"mot{i}" for i in range(300))
        (directory / "input.md").write_text(raw, encoding="utf-8")
        copied = " ".join(f"mot{i}" for i in range(60))
        sources = [("analyse-cdc.imposed_items", copied)]
        message = "=== INPUT: analyse-cdc.imposed_items ===\n" + copied + "\n=== END INPUT ==="
        parcours.ensure_isolated(message, directory, 1, sources, verbatim={"analyse-cdc.imposed_items"})
        with self.assertRaises(parcours.LeakError):
            parcours.ensure_isolated(message, directory, 1, sources, verbatim=set())
        with self.assertRaises(parcours.LeakError):
            parcours.ensure_isolated(message + "\n" + copied[:400], directory, 1, [("other.field", copied)],
                                     verbatim={"analyse-cdc.imposed_items"})

    def test_output_field_takes_the_whole_output_before_the_handoff(self):
        text = ("# Offre\n\nCorps complet de l'offre.\n\n```\n## HANDOFF dans un bloc de code\n```\n\nFin.\n\n"
                "## HANDOFF\n### notes\nune note\n## SUMMARY\nS\n")
        parsed = parcours.parse_step_output(text, ["offer", "notes"], None, "offer")
        self.assertTrue(parsed["handoff"]["offer"].startswith("# Offre"))
        self.assertIn("Fin.", parsed["handoff"]["offer"])
        self.assertNotIn("une note", parsed["handoff"]["offer"])
        self.assertEqual(parsed["handoff"]["notes"], "une note")

    def test_output_field_survives_a_retry(self):
        first = "# Offre\n\nCorps.\n\n(pas de handoff)"
        stored = f"{first}\n\n{parcours.RETRY_MARKER}\n## HANDOFF\n### notes\nn\n## SUMMARY\nS\n"
        self.assertEqual(parcours.output_body(stored), first.strip())

    def test_the_message_asks_for_the_language_of_the_material(self):
        folder = self.write_skill(self.tmp / "ix-skills" / "dist" / "skills", "cadrage")
        skill = parcours.resolve_skill("ix-skills:cadrage")
        defn = {"id": "s", "mission": "m", "transmits": ["a"], "produces_context_sheet": False}
        message = parcours.build_message(skill, defn, 1, {"context_sheet": {}}, [], [])
        self.assertIn("language of the material", message)

    def test_admitted_verbatim_passages_may_be_quoted_downstream_but_not_others(self):
        raw = " ".join(f"mot{i}" for i in range(300))
        admitted = "- " + " ".join(f"mot{i}" for i in range(0, 50))
        quoting = {"handoff": {"offer": "Offre : " + " ".join(f"mot{i}" for i in range(0, 50))}, "context_sheet": None}
        self.assertIsNone(parcours.leak_in_parsed(raw, quoting, (), admitted))
        other = {"handoff": {"offer": "Offre : " + " ".join(f"mot{i}" for i in range(100, 150))}, "context_sheet": None}
        self.assertIsNotNone(parcours.leak_in_parsed(raw, other, (), admitted))

    def test_step_1_gets_the_context_sheet_definitions_of_the_recipe_body(self):
        definitions = parcours.load_recipe("reponse-appel-offres")["context_definitions"]
        self.assertIn("without imposing them", definitions["named_solutions"])
        defn = parcours.load_recipe("reponse-appel-offres")["steps"][0]
        text = parcours.output_instructions(defn, 0, ["buyer", "named_solutions"], definitions)
        self.assertIn("- `named_solutions`: means or methods the buyer mentions", text)
        self.assertNotIn("What each key holds", parcours.output_instructions(defn, 0, ["buyer"], {}))

    def test_admitted_short_lines_cover_a_reformatted_list(self):
        # imposed items are short lines: the admitted text holds them one per line,
        # the offer re-lists them; no single 40-word run exists in the admitted text
        items = [" ".join(f"item{k}w{j}" for j in range(9)) for k in range(12)]
        raw = "Préambule " + " ; ".join(items) + " " + " ".join(f"autre{i}" for i in range(80))
        admitted = "\n".join(f"- {line} ;" for line in items)
        offer = {"handoff": {"offer": "Programme : " + " ".join(items)}, "context_sheet": None}
        self.assertIsNone(parcours.leak_in_parsed(raw, offer, (), admitted))
        tail = {"handoff": {"offer": " ".join(f"autre{i}" for i in range(80))}, "context_sheet": None}
        self.assertIsNotNone(parcours.leak_in_parsed(raw, tail, (), admitted))

    def test_recipes_title_and_labels_for_a_page(self):
        listed = json.loads(self.ok("recipes", "--json"))["recipes"]
        self.assertEqual([r["id"] for r in listed], ["brief-client", "reponse-appel-offres"])
        brief = listed[0]
        self.assertEqual(brief["label"], "Brief client")
        self.assertEqual(brief["steps"][0], {"id": "cadrage", "label": "Cadrage de la demande", "pause": "validate", "optional": False})
        self.assertTrue(brief["description"])
        created = json.loads(self.ok("new", "brief-client", "--input", str(self.input_file), "--title", "  Offre   formation  ",
                                     "--slug", "Offre formation", "--engine", "fake", "--json"))
        self.assertEqual(created, {"slug": "offre-formation", "title": "Offre formation"})
        status = json.loads(self.ok("status", "offre-formation", "--json"))
        self.assertEqual((status["title"], status["recipe_label"]), ("Offre formation", "Brief client"))
        self.assertEqual(status["steps"][0]["label"], "Cadrage de la demande")
        self.assertTrue(status["steps"][0]["mission"])
        self.assertEqual(status["max_budget_usd"], parcours.DEFAULT_BUDGET)

    def test_the_plugin_bundles_the_current_scripts(self):
        bundle = REPO / "dist" / "skills" / "suivi-parcours" / "scripts"
        for name in ("parcours.py", "interface.py", "interface.html"):
            self.assertEqual((bundle / name).read_bytes(), (REPO / "scripts" / name).read_bytes(),
                             f"dist/…/scripts/{name} is stale: python3 build.py --target agentskills")

    def test_the_runner_bundled_in_the_plugin_works_without_the_repo_or_pyyaml(self):
        """dist/skills/suivi-parcours/scripts/parcours.py, recipes as <skills>/<id>/recipe.json + SKILL.md."""
        if not (REPO / "dist" / "skills" / "suivi-parcours" / "scripts" / "parcours.py").is_file():
            self.skipTest("dist not built")
        plugin = self.tmp / "plugin"
        shutil.copytree(REPO / "dist", plugin)
        script = plugin / "skills" / "suivi-parcours" / "scripts" / "parcours.py"
        guard = ("import runpy, sys; sys.modules['yaml'] = None; sys.argv = sys.argv[1:]; "
                 "runpy.run_path(sys.argv[0], run_name='__main__')")
        env = dict(os.environ, IX_SKILLS_PATH=str(self.tmp / "ix-skills" / "dist" / "skills"), PYTHONUTF8="1")

        def run(*argv):
            done = subprocess.run([sys.executable, "-c", guard, str(script), *argv, "--parcours-dir", str(self.tmp / "d")],
                                  capture_output=True, text=True, env=env, timeout=60)
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            return done.stdout

        ids = [r["id"] for r in json.loads(run("recipes", "--json"))["recipes"]]
        self.assertIn("brief-client", ids)
        self.assertIn("reponse-appel-offres", ids)
        self.assertEqual(json.loads(run("new", "brief-client", "--input", str(self.input_file), "--slug", "b", "--json"))["slug"], "b")
        status = json.loads(run("status", "b", "--json"))
        self.assertEqual(status["steps"][0]["label"], "Cadrage de la demande")
        self.assertTrue(json.loads(run("plan", "b", "--json"))["runnable"])

    def test_output_document_drops_closing_blocks_and_front_matter(self):
        text = ("---\nstatus: draft\nrecipient: comité\n---\n\n# Offre\nCorps.\n\n## CONTEXT SHEET\n```json\n{}\n```\n"
                "## HANDOFF\n### offer\nX\n## SUMMARY\nS\n")
        document, meta = parcours.output_document(text)
        self.assertEqual(document, "# Offre\nCorps.")
        self.assertEqual(meta, {"status": "draft", "recipient": "comité"})
        self.assertEqual(parcours.output_document("Pas de bloc.\n## HANDOFF\n### a\nA\n"), ("Pas de bloc.", {}))
        after_title = "# Questions\n\n---\nstatus: draft\nskill: questioning\n---\n\n## Scope\nX\n## HANDOFF\n### a\nA\n"
        self.assertEqual(parcours.output_document(after_title), ("# Questions\n\n## Scope\nX", {"status": "draft", "skill": "questioning"}))
        ruled = "---\n\nParagraphe un.\n\n---\n\nParagraphe deux.\n## HANDOFF\n### a\nA\n"
        self.assertEqual(parcours.output_document(ruled), ("---\n\nParagraphe un.\n\n---\n\nParagraphe deux.", {}))

    def test_archive_and_restore(self):
        self.new()
        self.new(slug="autre")
        self.assertEqual(json.loads(self.ok("archive", "demo", "--json")), {"archived": "demo"})
        self.assertFalse((self.pdir / "demo").exists())
        self.assertTrue((self.pdir / ".archives" / "demo" / "state.json").is_file())
        self.assertEqual([a["slug"] for a in json.loads(self.ok("archives", "--json"))["archives"]], ["demo"])
        self.new()                                                     # the slug is free again
        restored = json.loads(self.ok("unarchive", "demo", "--json"))["restored"]
        self.assertEqual(restored, "demo-2")                           # never over a parcours of the list
        self.assertEqual(self.state("demo-2")["slug"], "demo-2")
        self.assertEqual(json.loads(self.ok("archives", "--json"))["archives"], [])
        code, out, _ = self.cli("unarchive", "absent", "--json")
        self.assertEqual(code, 1)
        code, out, _ = self.cli("archive", ".archives", "--json")
        self.assertEqual(code, 1)

    def test_a_title_always_gives_a_usable_slug(self):
        long_title = "Réponse à la consultation de la Fédération nationale pour la formation gestion de projet 2026 et suite"
        for title in (long_title, "🚀", "—", "-"):
            created = json.loads(self.ok("new", "brief-client", "--input", str(self.input_file), f"--title={title}",
                                         f"--slug={title}", "--engine", "fake", "--json"))
            self.assertRegex(created["slug"], r"^[a-z0-9][a-z0-9-]{0,79}$", title)
        self.assertFalse(any(p.name.startswith("-") for p in self.pdir.iterdir()))

    def test_a_missing_or_binary_input_file_is_a_clean_error(self):
        with self.assertRaises(parcours.ParcoursError) as missing:
            parcours.read_text_arg(str(self.tmp / "absent.md"))
        self.assertIn("introuvable", str(missing.exception))
        binary = self.tmp / "cdc.pdf"
        binary.write_bytes(b"%PDF-1.7\xff\xfe\x00")
        with self.assertRaises(parcours.ParcoursError) as unreadable:
            parcours.read_text_arg(str(binary))
        self.assertIn("UTF-8", str(unreadable.exception))

    def test_only_a_short_no_blocking_opening_is_neutral(self):
        self.assertFalse(parcours.is_blocking("Aucun blocage pour la suite."))
        self.assertFalse(parcours.is_blocking("No blocking issue."))
        # longer texts count, whatever their opening: a needless pause beats a missed block
        self.assertTrue(parcours.is_blocking("Aucun blocage n'est levé tant que le module 4 manque à l'offre."))
        self.assertTrue(parcours.is_blocking("No blocking issue except that module 4 is absent from the offer."))
        self.assertTrue(parcours.is_blocking("Le texte de l'offre manque : impossible de mettre en forme."))

    def test_an_ignored_blocking_section_leaves_a_warning(self):
        parsed = parcours.parse_step_output("Doc\n## HANDOFF\n### a\nA\n### blocking\nAucun blocage.\n## SUMMARY\nS\n", ["a"])
        self.assertEqual(parsed["blocking"], "")
        self.assertTrue(any("blocking" in w for w in parsed["warnings"]))

    def test_output_body_of_a_fenced_or_summary_first_output(self):
        fenced = "```markdown\n# Offre\nTexte.\n## HANDOFF\n### x\nX\n## SUMMARY\nS\n```\n"
        self.assertEqual(parcours.output_body(fenced), "# Offre\nTexte.")
        tilde = "# Offre\n~~~\n## HANDOFF inside an example\n~~~\nSuite.\n## HANDOFF\n### x\nX\n"
        self.assertIn("Suite.", parcours.output_body(tilde))
        first = "# Offre\nTexte.\n## Summary\nCourt.\n## HANDOFF\n### x\nX\n"
        self.assertEqual(parcours.output_body(first), "# Offre\nTexte.")
        long_section = "# Offre\n## Summary\n" + "\n".join(f"l{i}" for i in range(20)) + "\n## HANDOFF\n### x\nX\n"
        self.assertIn("l19", parcours.output_body(long_section))  # a document section, not the closing summary

    def test_a_short_verbatim_value_does_not_mutilate_the_checked_message(self):
        raw = " ".join(f"de mot{i}" for i in range(60))
        self.pdir.mkdir(parents=True, exist_ok=True)
        directory = self.pdir / "court"
        directory.mkdir()
        (directory / "input.md").write_text(raw, encoding="utf-8")
        message = "=== INPUT: s.items ===\nde\n=== END INPUT ===\n" + raw
        with self.assertRaises(parcours.LeakError):
            parcours.ensure_isolated(message, directory, 1, [("s.items", "de")], {"s.items"})

    def test_the_message_announces_the_reference_files(self):
        folder = self.write_skill(self.tmp / "ix-skills" / "dist" / "skills", "cadrage")
        (folder / "references").mkdir()
        (folder / "references" / "guide.md").write_text("REF-CONTENT", encoding="utf-8")
        with_refs = parcours.references_note(parcours.resolve_skill("ix-skills:cadrage"))
        self.assertEqual(len(with_refs), 1)
        self.assertIn("./references/", with_refs[0])
        self.assertIn("guide.md", with_refs[0])
        self.assertNotIn("REF-CONTENT", with_refs[0])
        self.assertEqual(parcours.references_note({"references": self.tmp / "none"}), [])

    @unittest.skipUnless((REPO.parent / "ix-skills" / "dist" / "skills").is_dir(), "../ix-skills not checked out")
    def test_real_recipes_resolve_against_the_real_checkouts(self):
        with mock.patch.object(parcours, "ROOT", REPO):
            for recipe_id in ("brief-client", "reponse-appel-offres"):
                for defn in parcours.load_recipe(recipe_id)["steps"]:
                    skill = parcours.resolve_skill(defn["skill"])
                    self.assertTrue(skill["text"], defn["skill"])
                    self.assertFalse(skill["text"].startswith("---"))


# ---------------------------------------------------------------------------
# Engines: command lines, output reading, cost, timeout
# ---------------------------------------------------------------------------
class EngineTests(ParcoursTestCase):
    MESSAGE = "THE-WHOLE-MESSAGE " * 5000  # far beyond any argv limit

    def call(self, engine, run, model="opus", step_id="cadrage"):
        calls = []

        def spy(argv, stdin, cwd, timeout):
            calls.append({"argv": list(argv), "stdin": stdin, "cwd": Path(cwd), "timeout": timeout,
                          "cwd_listing": list(Path(cwd).iterdir())})
            return run(argv, stdin, cwd, timeout)

        skill = {"references": self.tmp / "no-references"}
        with mock.patch.object(parcours, "run_process", spy):
            result = parcours.call_engine(engine, self.MESSAGE, model=model, timeout=77, budget=5.0,
                                          skill=skill, step_id=step_id, kind="main")
        self.assertEqual(len(calls), 1)
        return calls[0], result

    def assert_safe_call(self, call):
        self.assertEqual(call["stdin"], self.MESSAGE)
        self.assertNotIn("THE-WHOLE-MESSAGE", " ".join(call["argv"]))
        self.assertEqual(call["timeout"], 77)
        cwd = call["cwd"]
        self.assertFalse(cwd.exists(), "scratch dir must be removed after the call")
        self.assertTrue(str(cwd).startswith(str(Path(tempfile.gettempdir()).resolve())) or
                        str(cwd).startswith(tempfile.gettempdir()))
        self.assertNotEqual(cwd, Path.cwd())
        self.assertNotIn(str(self.pdir), str(cwd))
        self.assertEqual(call["cwd_listing"], [])  # nothing in it: no input.md, no upstream output

    def test_claude_command_line_and_cost(self):
        payload = json.dumps({"type": "result", "is_error": False, "result": "OUT", "total_cost_usd": 0.4242})
        call, (text, cost) = self.call("claude", lambda *a: (0, payload, "A new version is available!"))
        self.assertEqual(call["argv"], [
            "claude", "-p", "--model", "opus", "--output-format", "json", "--tools", "Read",
            "--setting-sources", "", "--no-session-persistence", "--disable-slash-commands",
            "--max-budget-usd", "5",
        ])
        self.assertEqual((text, cost), ("OUT", 0.4242))
        self.assert_safe_call(call)

    def test_claude_model_comes_from_the_step(self):
        payload = json.dumps({"result": "x", "total_cost_usd": 0})
        call, _ = self.call("claude", lambda *a: (0, payload, ""), model="sonnet")
        self.assertEqual(call["argv"][call["argv"].index("--model") + 1], "sonnet")

    def test_claude_error_results(self):
        for payload in (json.dumps({"is_error": True, "subtype": "error_max_budget_usd", "total_cost_usd": 5}),
                        "not json at all"):
            with self.assertRaises(parcours.EngineError):
                self.call("claude", lambda *a: (0, payload, ""))

    def test_codex_command_line_reads_the_output_file_not_stdout(self):
        def run(argv, stdin, cwd, timeout):
            Path(argv[argv.index("-o") + 1]).write_text("CODEX-ANSWER", encoding="utf-8")
            return 0, "banner noise on stdout", "update notice"

        call, (text, cost) = self.call("codex", run)
        argv = call["argv"]
        self.assertEqual(argv[:7], ["codex", "exec", "-s", "read-only", "--skip-git-repo-check", "--ephemeral", "-C"])
        self.assertEqual(argv[7], str(call["cwd"]))
        self.assertEqual(argv[8], "-o")
        self.assertNotEqual(Path(argv[9]).parent, call["cwd"])
        self.assertEqual((text, cost), ("CODEX-ANSWER", 0.0))
        self.assert_safe_call(call)

    def test_agy_takes_the_prompt_attached_to_p_and_reads_stdout_only(self):
        # agy has no text-on-stdin mode: the prompt must be attached as -p=<message>.
        call, (text, _) = self.call("agy", lambda *a: (0, "AGY-ANSWER\n", "Update available: 9.9"))
        self.assertEqual(call["argv"], ["agy", "--disable-slash-commands", f"-p={self.MESSAGE}"])
        self.assertEqual(call["stdin"], "")
        self.assertEqual(text, "AGY-ANSWER\n")
        self.assertNotIn("Update", text)
        cwd = call["cwd"]
        self.assertFalse(cwd.exists())
        self.assertNotIn(str(self.pdir), str(cwd))
        self.assertEqual(call["cwd_listing"], [])

    def test_vibe_command_line(self):
        call, (text, _) = self.call("vibe", lambda *a: (0, "VIBE-ANSWER", ""))
        self.assertEqual(call["argv"], ["vibe", "-p", "--output", "text"])
        self.assertEqual(text, "VIBE-ANSWER")
        self.assert_safe_call(call)

    def test_failures_surface_as_engine_errors(self):
        with self.assertRaisesRegex(parcours.EngineError, "code 3"):
            self.call("agy", lambda *a: (3, "", "it broke"))
        with self.assertRaisesRegex(parcours.EngineError, "vide"):
            self.call("vibe", lambda *a: (0, "  \n", ""))

    def test_unknown_engine_is_refused(self):
        with self.assertRaises(parcours.ParcoursError):
            parcours.engine_argv("gpt", None, Path("."), Path("."), 5.0)

    def test_missing_binary_is_reported(self):
        with self.assertRaisesRegex(parcours.EngineError, "introuvable"):
            parcours.run_process(["definitely-not-a-command-xyz"], "", self.tmp, 5)

    def test_run_process_passes_stdin_and_separates_streams(self):
        code, out, err = parcours.run_process(
            ["sh", "-c", "cat; echo problem >&2"], "hello", self.tmp, 5)
        self.assertEqual((code, out, err.strip()), (0, "hello", "problem"))

    def test_timeout_kills_the_process(self):
        started = time.time()
        with self.assertRaises(parcours.EngineTimeout):
            parcours.run_process(["sleep", "30"], "", self.tmp, 1)
        self.assertLess(time.time() - started, 4)

    def test_timeout_kills_the_whole_process_group(self):
        pid_file = self.tmp / "child.pid"
        script = f"sleep 30 & echo $! > {pid_file}; wait"
        started = time.time()
        with self.assertRaises(parcours.EngineTimeout):
            parcours.run_process(["sh", "-c", script], "", self.tmp, 1)
        self.assertLess(time.time() - started, 4)
        child = int(pid_file.read_text())
        for _ in range(20):
            try:
                os.kill(child, 0)
            except ProcessLookupError:
                break
            time.sleep(0.1)
        else:
            os.kill(child, 9)
            self.fail("the grandchild survived the timeout")

    def test_timeout_during_a_step_fails_it_and_counts_the_call(self):
        self.new()
        with mock.patch.object(parcours, "run_process", side_effect=parcours.EngineTimeout("délai dépassé")):
            code, _, err = self.cli("next", "demo", "--yes", "--engine", "claude")
        self.assertEqual(code, 1)
        self.assertIn("délai", err)
        self.assertEqual(self.step("cadrage")["status"], "failed")
        self.assertEqual(self.state()["calls"], {"claude": 1})


class PlanAndAccountingTests(ParcoursTestCase):
    def claude_runner(self, cost=0.31):
        """Mock of run_process answering with the canned outputs, in step order."""
        outputs = []
        recipe = self.recipe("brief-client")
        for defn in recipe["steps"]:
            ctx = recipe["context_sheet"] if defn["produces_context_sheet"] else None
            outputs.append(fake_output(defn, ctx))
        queue = iter(outputs)
        calls = []

        def run(argv, stdin, cwd, timeout):
            calls.append({"argv": list(argv), "stdin": stdin})
            return 0, json.dumps({"result": next(queue), "total_cost_usd": cost}), ""

        return run, calls

    def test_plan_is_printed_and_declining_runs_nothing(self):
        self.new()
        run, calls = self.claude_runner()
        with mock.patch.object(parcours, "run_process", run), mock.patch("builtins.input", return_value="n"):
            code, out, _ = self.cli("next", "demo", "--engine", "claude")
        self.assertEqual(code, 1)
        self.assertEqual(calls, [])
        self.assertEqual(self.step("cadrage")["status"], "pending")
        self.assertIn("Plan", out)
        self.assertIn("cadrage", out)
        self.assertIn("moteur claude", out)
        self.assertIn("modèle opus", out)
        self.assertRegex(out, r"entrée ≈ \d+ caractères")
        self.assertIn("Annulé", out)

    def test_plan_size_is_the_size_of_the_message(self):
        self.new()
        run, calls = self.claude_runner()
        with mock.patch.object(parcours, "run_process", run), mock.patch("builtins.input", return_value="y"):
            code, out, _ = self.cli("next", "demo", "--engine", "claude")
        self.assertEqual(code, 0)
        announced = int(re.search(r"entrée ≈ (\d+) caractères", out).group(1))
        self.assertEqual(announced, len(calls[0]["stdin"]))

    def test_yes_skips_the_question(self):
        self.new()
        run, calls = self.claude_runner()
        with mock.patch.object(parcours, "run_process", run), mock.patch("builtins.input", side_effect=AssertionError):
            self.ok("next", "demo", "--yes", "--engine", "claude")
        self.assertEqual(len(calls), 1)

    def test_no_terminal_means_no(self):
        self.new()
        with mock.patch("builtins.input", side_effect=EOFError):
            code, _, _ = self.cli("next", "demo", "--engine", "fake")
        self.assertEqual(code, 1)

    def test_plan_covers_the_steps_up_to_the_next_pause(self):
        self.new("reponse-appel-offres", slug="rao")
        self.write_fakes("reponse-appel-offres")
        self.drive_until_pending("rao", "answers")
        self.ok("answer", "rao", "--file", str(self.answers_file))
        self.ok("next", "rao", "--yes")  # go-no-go, pause validate
        self.ok("validate", "rao")
        with mock.patch("builtins.input", return_value="n"):
            _, out, _ = self.cli("next", "rao")
        # strategie and offre have pause none, conformite validates: three steps in the plan
        self.assertIn("3 étape(s)", out)
        for step_id in ("strategie", "offre", "conformite"):
            self.assertIn(step_id, out)
        self.assertNotIn("mise-en-forme", out)
        self.assertIn("champ(s) à venir", out)  # offre depends on strategie, not yet produced

    def drive_until_pending(self, slug, kind):
        for _ in range(10):
            self.ok("next", slug, "--yes")
            pending = self.state(slug)["pending"]
            if pending["type"] == kind:
                return
            self.ok("validate", slug)
        self.fail("pause not reached")

    def test_claude_cost_and_calls_are_stored_and_shown(self):
        self.new()
        run, _ = self.claude_runner(cost=0.31)
        with mock.patch.object(parcours, "run_process", run):
            self.ok("next", "demo", "--yes", "--engine", "claude")
            self.ok("validate", "demo")
            self.ok("next", "demo", "--yes")
        self.assertEqual(self.step("cadrage")["cost_usd"], 0.31)
        state = self.state()
        self.assertAlmostEqual(state["cost_usd"], 0.62)
        self.assertEqual(state["calls"], {"claude": 2})
        out = self.ok("status", "demo")
        self.assertIn("$0.6200", out)
        self.assertIn("claude ×2", out)
        self.assertIn("cadrage : done", out)
        self.assertIn("questioning : paused", out)

    def test_engine_per_step(self):
        self.new()
        run, calls = self.claude_runner()
        self.write_fakes("brief-client")
        with mock.patch.object(parcours, "run_process", run):
            self.ok("next", "demo", "--yes", "--engine", "claude")
            self.ok("validate", "demo")
            self.ok("next", "demo", "--yes", "--engine-step", "questioning=fake")
        self.assertEqual(len(calls), 1)  # questioning went to the fake engine
        self.assertEqual(self.state()["calls"], {"claude": 1, "fake": 1})
        self.assertEqual(self.step("questioning")["engine"], "fake")

    def test_status_shows_calls_per_engine(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        out = self.ok("status", "demo")
        self.assertIn("fake ×1", out)
        self.assertIn("Fiche de contexte : non validée", out)


# ---------------------------------------------------------------------------
# Parsing: tolerance (fences, names, sheet JSON), blocking section
# ---------------------------------------------------------------------------
class ParsingToleranceTests(unittest.TestCase):
    FIELDS = ["need", "constraints"]
    BODY = "## HANDOFF\n### need\nn\n### constraints\nc\n## SUMMARY\nS\n"

    def parse(self, text, **kw):
        return parcours.parse_step_output(text, self.FIELDS, **kw)

    def test_output_wrapped_in_a_code_fence(self):
        result = self.parse("```markdown\nLong analysis.\n" + self.BODY + "```\n")
        self.assertEqual(result["handoff"], {"need": "n", "constraints": "c"})
        self.assertEqual(result["summary"], "S")
        self.assertTrue(any("encadrée" in w for w in result["warnings"]))

    def test_wrapped_output_holding_its_own_json_block(self):
        text = ("```markdown\nAnalysis.\n## CONTEXT SHEET\n```json\n{\"client\": \"ACME\"}\n```\n"
                + self.BODY + "```")
        result = self.parse(text, context_fields=["client"])
        self.assertEqual(result["context_sheet"], {"client": "ACME"})
        self.assertEqual(result["handoff"]["constraints"], "c")
        self.assertEqual(result["summary"], "S")

    def test_unclosed_fence_swallowing_the_handoff(self):
        result = self.parse("Intro\n```text\nnever closed\n" + self.BODY)
        self.assertEqual(result["handoff"], {"need": "n", "constraints": "c"})
        self.assertTrue(any("non fermé" in w for w in result["warnings"]))

    def test_unclosed_fence_after_the_summary(self):
        result = self.parse(self.BODY + "```\nstray")
        self.assertEqual(result["handoff"]["need"], "n")
        self.assertTrue(any("non fermé" in w for w in result["warnings"]))

    def test_a_closed_fence_inside_a_value_is_still_respected(self):
        text = "## HANDOFF\n### need\n```\n### constraints\nfake\n```\n### constraints\nc\n## SUMMARY\nS\n"
        result = self.parse(text)
        self.assertEqual(result["handoff"]["constraints"], "c")
        self.assertEqual(result["warnings"], [])

    def test_field_names_fold_accents_case_separators_and_plural(self):
        n = parcours.normalize_name
        self.assertEqual(n("Hypotheses"), n("hypothesis"))
        self.assertEqual(n("constraint"), n("Constraints"))
        self.assertEqual(n("Points ouverts"), n("points_ouvert"))
        self.assertEqual(n("Hypothèses"), n("HYPOTHESES"))
        self.assertEqual(n("open-points"), n("Open  Points"))
        self.assertEqual(n("grey zones"), n("grey_zone"))
        self.assertEqual(n("évaluation"), n("evaluation"))
        self.assertNotEqual(n("need"), n("constraint"))

    def test_plural_and_accented_headings_are_matched_to_declared_fields(self):
        text = "## HANDOFF\n### Constraint\nc\n### Needs\nn\n### Hypothèses\nh\n## SUMMARY\nS\n"
        result = parcours.parse_step_output(text, ["need", "constraints", "hypotheses"])
        self.assertEqual(result["handoff"], {"need": "n", "constraints": "c", "hypotheses": "h"})
        self.assertEqual(result["warnings"], [])

    def test_declared_field_names_of_the_real_recipes_stay_distinct(self):
        for recipe_id in ("brief-client", "reponse-appel-offres"):
            for defn in self.real_steps(recipe_id):
                keys = [parcours.normalize_name(f) for f in defn["transmits"]]
                self.assertEqual(len(keys), len(set(keys)), defn["id"])

    @staticmethod
    def real_steps(recipe_id):
        with mock.patch.object(parcours, "ROOT", REPO):
            return parcours.load_recipe(recipe_id)["steps"]

    def sheet(self, block, **kw):
        text = f"## CONTEXT SHEET\n{block}\n" + self.BODY
        return self.parse(text, context_fields=["client", "deadlines"], **kw)["context_sheet"]

    def test_sheet_fence_info_string_is_free(self):
        for info in ("json", "JSON", "jsonc", "", "json5 title=x"):
            sheet = self.sheet(f'```{info}\n{{"client": "ACME", "deadlines": "May"}}\n```')
            self.assertEqual(sheet["client"], "ACME", info)
        self.assertEqual(self.sheet('~~~json\n{"client": "T", "deadlines": "d"}\n~~~')["client"], "T")

    def test_sheet_comments_and_trailing_commas(self):
        block = ('```jsonc\n{\n  // who\n  "client": "ACME", /* inline */\n'
                 '  "deadlines": "see http://x.example/a//b", // note\n}\n```')
        sheet = self.sheet(block)
        self.assertEqual(sheet, {"client": "ACME", "deadlines": "see http://x.example/a//b"})

    def test_sheet_without_a_fence_and_with_prose_around(self):
        sheet = self.sheet('Here it is: {"client": "ACME", "deadlines": ["a", "b",],} hope it helps')
        self.assertEqual(sheet["deadlines"], ["a", "b"])

    def test_sheet_still_fails_when_unreadable(self):
        with self.assertRaisesRegex(parcours.ParseError, "JSON"):
            self.sheet("```json\n{oops\n```")
        with self.assertRaisesRegex(parcours.ParseError, "JSON"):
            self.sheet("no braces at all")

    def test_blocking_section_is_returned_apart_and_not_flagged_as_extra(self):
        result = self.parse("## HANDOFF\n### need\nn\n### constraints\nc\n### blocking\nThe budget is missing.\n## SUMMARY\nS\n")
        self.assertEqual(result["blocking"], "The budget is missing.")
        self.assertNotIn("blocking", result["handoff"])
        self.assertEqual(result["warnings"], [])

    def test_empty_or_trivial_blocking_is_ignored(self):
        for value in ("", "None", "n/a", "-", "Aucun.", "RAS"):
            text = f"## HANDOFF\n### need\nn\n### constraints\nc\n### blocking\n{value}\n## SUMMARY\nS\n"
            self.assertEqual(self.parse(text)["blocking"], "", value)
        self.assertEqual(self.parse(self.BODY)["blocking"], "")



# ---------------------------------------------------------------------------
# Review fixes: cost on failure, crash window, accounting, unexpected errors
# ---------------------------------------------------------------------------
class RecoveryTests(ParcoursTestCase):
    def cadrage_defn(self):
        recipe = self.recipe("brief-client")
        return recipe["steps"][0], recipe["context_sheet"]

    def test_claude_error_result_keeps_its_cost_on_the_exception(self):
        payload = json.dumps({"is_error": True, "subtype": "error_max_budget_usd", "total_cost_usd": 4.2})
        with mock.patch.object(parcours, "run_process", lambda *a: (0, payload, "")):
            with self.assertRaises(parcours.EngineError) as caught:
                parcours.call_engine("claude", "m", model="opus", timeout=5, budget=5.0,
                                     skill={"references": self.tmp / "none"}, step_id="cadrage", kind="main")
        self.assertEqual(caught.exception.cost, 4.2)

    def test_claude_non_zero_exit_keeps_the_cost_found_in_stdout(self):
        payload = json.dumps({"type": "result", "is_error": True, "total_cost_usd": 1.5})
        with mock.patch.object(parcours, "run_process", lambda *a: (2, payload, "boom")):
            with self.assertRaises(parcours.EngineError) as caught:
                parcours.call_engine("claude", "m", model="opus", timeout=5, budget=5.0,
                                     skill={"references": self.tmp / "none"}, step_id="cadrage", kind="main")
        self.assertEqual(caught.exception.cost, 1.5)

    def test_a_failed_claude_call_is_added_to_step_and_run_cost_and_counted(self):
        self.new()
        payload = json.dumps({"is_error": True, "subtype": "error_max_budget_usd", "total_cost_usd": 4.2})
        with mock.patch.object(parcours, "run_process", lambda *a: (0, payload, "")):
            code, _, _ = self.cli("next", "demo", "--yes", "--engine", "claude")
        self.assertEqual(code, 1)
        state = self.state()
        self.assertEqual(state["cost_usd"], 4.2)
        self.assertEqual(self.step("cadrage")["cost_usd"], 4.2)
        self.assertEqual(state["calls"], {"claude": 1})
        self.assertEqual(self.step("cadrage")["status"], "failed")
        # a retry adds to the same step cost instead of forgetting the failed call
        good = json.dumps({"result": fake_output(*self.cadrage_defn()), "total_cost_usd": 0.5})
        self.ok("retry", "demo")
        with mock.patch.object(parcours, "run_process", lambda *a: (0, good, "")):
            self.ok("next", "demo", "--yes")
        self.assertAlmostEqual(self.step("cadrage")["cost_usd"], 4.7)
        self.assertAlmostEqual(self.state()["cost_usd"], 4.7)

    def test_cost_and_calls_are_saved_as_soon_as_each_call_returns(self):
        self.new()
        defn, ctx = self.cadrage_defn()
        seen = []

        def run(argv, stdin, cwd, timeout):
            seen.append(json.loads((self.pdir / "demo" / "state.json").read_text()))
            text = "no handoff at all" if len(seen) == 1 else fake_output(defn, ctx, retry=True)
            return 0, json.dumps({"result": text, "total_cost_usd": 0.31}), ""

        with mock.patch.object(parcours, "run_process", run):
            self.ok("next", "demo", "--yes", "--engine", "claude")
        self.assertEqual(len(seen), 2)
        self.assertEqual(seen[0]["calls"], {})
        self.assertEqual(seen[1]["calls"], {"claude": 1})  # on disk before the retry started
        self.assertEqual(seen[1]["cost_usd"], 0.31)
        self.assertEqual(seen[1]["steps"][0]["status"], "running")
        self.assertAlmostEqual(self.state()["cost_usd"], 0.62)

    def crash_after_output(self, text):
        """What a killed process leaves: step running, output file on disk, no extraction recorded."""
        self.new()
        path = self.pdir / "demo" / "state.json"
        state = json.loads(path.read_text())
        state["steps"][0]["status"] = "running"
        path.write_text(json.dumps(state))
        (self.pdir / "demo" / "01-cadrage.md").write_text(text, encoding="utf-8")

    def test_output_left_by_a_crash_is_parsed_without_a_new_call(self):
        self.crash_after_output(fake_output(*self.cadrage_defn()))
        self.ok("retry", "demo")
        self.ok("next", "demo", "--yes")
        self.assertFalse(self.was_called("cadrage"))
        self.assertEqual(self.state()["calls"], {})
        self.assertEqual(self.step("cadrage")["status"], "paused")
        self.assertEqual(self.step("cadrage")["handoff"]["need"], "VALUE[cadrage.need]")
        self.assertEqual(self.state()["context_sheet"]["client"], "CTX-client")

    def test_unusable_output_left_by_a_crash_is_set_aside_then_the_engine_is_called(self):
        self.crash_after_output("half-written garbage")
        self.write_fakes("brief-client")
        self.ok("retry", "demo")
        self.ok("next", "demo", "--yes")
        folder = self.pdir / "demo"
        self.assertEqual((folder / "01-cadrage.v1.md").read_text(), "half-written garbage")
        self.assertTrue(self.was_called("cadrage"))
        self.assertIn("VALUE[cadrage.need]", (folder / "01-cadrage.md").read_text())
        self.assertEqual(self.step("cadrage")["status"], "paused")

    def test_a_stale_output_on_a_step_never_retried_is_not_reused(self):
        self.new()
        self.write_fakes("brief-client")
        (self.pdir / "demo" / "01-cadrage.md").write_text(fake_output(*self.cadrage_defn()), encoding="utf-8")
        self.ok("next", "demo", "--yes")
        self.assertTrue(self.was_called("cadrage"))
        self.assertTrue((self.pdir / "demo" / "01-cadrage.v1.md").is_file())

    def test_an_unexpected_error_leaves_the_step_failed_with_one_line(self):
        self.new()
        self.write_fakes("brief-client")
        with mock.patch.object(parcours, "parse_step_output", side_effect=RuntimeError("boom\nsecond line")):
            code, _, err = self.cli("next", "demo", "--yes")
        self.assertEqual(code, 1)
        self.assertEqual(err.strip().count("\n"), 0)
        self.assertIn("RuntimeError", err)
        self.assertIn("boom second line", err)
        step = self.step("cadrage")
        self.assertEqual(step["status"], "failed")
        self.assertIn("erreur inattendue", step["error"])
        self.ok("retry", "demo")  # and it can be taken up again
        self.ok("next", "demo", "--yes")
        self.assertEqual(self.step("cadrage")["status"], "paused")

    def test_engine_output_is_decoded_with_replacement(self):
        code, out, _ = parcours.run_process(["sh", "-c", "printf 'ok\\377ok'"], "", self.tmp, 5)
        self.assertEqual((code, out), (0, "ok�ok"))

    def test_agy_size_guard_counts_bytes_not_characters(self):
        message = "é" * 150_000  # 150 000 characters, 300 000 bytes
        spy = mock.Mock()
        with mock.patch.object(parcours, "run_process", spy):
            with self.assertRaisesRegex(parcours.EngineError, "octets"):
                parcours.call_engine("agy", message, model=None, timeout=5, budget=5.0,
                                     skill={"references": self.tmp / "none"}, step_id="cadrage", kind="main")
        spy.assert_not_called()

    def test_next_on_a_stopped_or_completed_parcours_ignores_failed_steps(self):
        self.new()
        self.write_fakes("brief-client")
        for status in ("stopped", "completed"):
            path = self.pdir / "demo" / "state.json"
            state = json.loads(path.read_text())
            state["status"] = status
            state["steps"][0]["status"] = "failed"
            state["steps"][0]["error"] = "x"
            path.write_text(json.dumps(state))
            out = self.ok("next", "demo", "--yes")
            self.assertIn(status, out)
            self.assertFalse(self.was_called("cadrage"))


class RecipeDriftTests(ParcoursTestCase):
    def edit_recipe(self, old, new, recipe_id="brief-client"):
        path = self.root / "skills" / f"{recipe_id}.md"
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text.count(old), 1, old)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def commands(self):
        fields = self.tmp / "champs.md"
        fields.write_text("### need\nn\n", encoding="utf-8")
        return [
            ("next", "demo", "--yes"), ("validate", "demo"), ("answer", "demo", "--none"),
            ("choose", "demo", "--skip"), ("rerun", "demo", "cadrage"),
            ("handoff", "demo", "cadrage", "--file", str(fields)),
        ]

    def test_every_command_that_indexes_steps_checks_the_recipe(self):
        for old, new in (("transmits: [client_questions]", "transmits: [client_questions, extra_field]"),
                         ("    - id: questioning\n", "    - id: questions\n")):
            with self.subTest(change=new):
                self.setUp()
                self.new()
                self.write_fakes("brief-client")
                self.ok("next", "demo", "--yes")
                self.edit_recipe(old, new)
                for argv in self.commands():
                    code, _, err = self.cli(*argv)
                    self.assertEqual(code, 1, argv)
                    self.assertIn("a changé", err, argv)

    def test_the_message_says_which_step_and_which_fields_changed(self):
        self.new()
        self.edit_recipe("transmits: [client_questions]", "transmits: [client_questions, extra_field]")
        code, _, err = self.cli("rerun", "demo", "cadrage")
        self.assertEqual(code, 1)
        self.assertIn("'questioning'", err)
        self.assertIn("client_questions, extra_field", err)
        self.assertIn("(parcours)", err)
        self.edit_recipe("transmits: [client_questions, extra_field]", "transmits: [client_questions]")
        self.edit_recipe("    - id: questioning\n", "    - id: questions\n")
        code, _, err = self.cli("validate", "demo")
        self.assertIn("questioning", err)
        self.assertIn("questions", err)


# ---------------------------------------------------------------------------
# Skills: resolution at `new`, recorded hash, drift warning
# ---------------------------------------------------------------------------
class SkillRecordTests(ParcoursTestCase):
    def test_new_fails_early_naming_every_missing_skill(self):
        shutil.rmtree(self.tmp / "ix-skills" / "dist" / "skills" / "decision")
        shutil.rmtree(self.tmp / "ix-skills" / "dist" / "skills" / "brief")
        code, _, err = self.cli("new", "brief-client", "--input", str(self.input_file), "--slug", "demo")
        self.assertEqual(code, 1)
        self.assertIn("ix-skills:decision", err)
        self.assertIn("ix-skills:brief", err)
        self.assertNotIn("ix-skills:cadrage", err)
        self.assertFalse(self.pdir.exists() and any(self.pdir.iterdir()))

    def test_new_records_path_sha256_and_version_for_every_step(self):
        self.new()
        text = (self.tmp / "ix-skills" / "dist" / "skills" / "cadrage" / "SKILL.md").read_text()
        body = text.split("---\n", 2)[2].strip()
        recorded = self.step("cadrage")["skill"]
        self.assertEqual(recorded["sha256"], hashlib.sha256(body.encode("utf-8")).hexdigest())
        self.assertTrue(recorded["path"].endswith("cadrage/SKILL.md"))
        self.assertEqual(recorded["ref"], "ix-skills:cadrage")
        for step in self.state()["steps"]:
            self.assertEqual(set(step["skill"]), {"ref", "path", "version", "version_source", "sha256"})

    def test_the_hash_recorded_after_a_run_is_that_of_the_text_sent(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        sent = self.received("cadrage").split("=== SKILL: ix-skills:cadrage ===\n")[1].split("\n=== END SKILL ===")[0]
        self.assertEqual(self.step("cadrage")["skill"]["sha256"], hashlib.sha256(sent.encode("utf-8")).hexdigest())

    def test_version_source_is_labelled(self):
        base = self.tmp / "ix-skills" / "dist" / "skills"
        self.write_skill(base, "cadrage", extra="version: 7.1.2\n")
        self.assertEqual(parcours.resolve_skill("ix-skills:cadrage")["version_source"], "frontmatter")
        self.write_skill(base, "cadrage")
        source = self.tmp / "ix-skills" / "skills"
        source.mkdir()
        (source / "cadrage.md").write_text("---\nid: cadrage\nversion: 3.9.1\n---\nbody\n", encoding="utf-8")
        skill = parcours.resolve_skill("ix-skills:cadrage")
        self.assertEqual((skill["version"], skill["version_source"]), ("3.9.1", "source file"))
        shutil.rmtree(self.tmp / "ix-skills")
        cache = Path(os.environ["HOME"]) / ".claude" / "plugins" / "cache" / "market" / "ix-skills" / "4.1.0" / "skills"
        self.write_skill(cache, "cadrage")
        skill = parcours.resolve_skill("ix-skills:cadrage")
        self.assertEqual((skill["version"], skill["version_source"]), ("4.1.0", "cache dir"))

    def test_next_warns_when_a_skill_text_changed_since_new_and_goes_on(self):
        self.new()
        self.write_fakes("brief-client")
        path = self.tmp / "ix-skills" / "dist" / "skills" / "questioning" / "SKILL.md"
        path.write_text(path.read_text() + "\nA NEW RULE\n", encoding="utf-8")
        code, _, err = self.cli("next", "demo", "--yes")
        self.assertEqual(code, 0)
        self.assertIn("Avertissement", err)
        self.assertIn("ix-skills:questioning", err)
        self.assertNotIn("ix-skills:cadrage", err)
        self.ok("validate", "demo")
        code, _, err = self.cli("next", "demo", "--yes")  # warns again until the step has run
        self.assertEqual(code, 0)
        self.assertIn("ix-skills:questioning", err)
        self.assertIn("A NEW RULE", self.received("questioning"))  # the current text is the one sent
        self.assertEqual(self.step("questioning")["status"], "paused")
        self.ok("answer", "demo", "--none")
        self.ok("choose", "demo", "--skip")
        code, _, err = self.cli("next", "demo", "--yes")
        self.assertNotIn("a changé depuis", err)  # recorded hash is now that of the text sent

    def test_no_warning_when_nothing_changed(self):
        self.new()
        self.write_fakes("brief-client")
        _, _, err = self.cli("next", "demo", "--yes")
        self.assertNotIn("a changé", err)


# ---------------------------------------------------------------------------
# Trace of the exact messages
# ---------------------------------------------------------------------------
class TraceTests(ParcoursTestCase):
    def test_the_message_of_each_step_is_written_before_the_call(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        folder = self.pdir / "demo"
        self.assertEqual((folder / "01-cadrage.in.md").read_text(), self.received("cadrage"))
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        self.assertEqual((folder / "02-questioning.in.md").read_text(), self.received("questioning"))
        self.assertEqual([p.name for p in folder.glob(".*.tmp")], [])

    def test_the_trace_exists_even_if_the_engine_fails(self):
        self.new()  # no canned file: the fake engine raises
        self.cli("next", "demo", "--yes")
        self.assertIn(INPUT_TEXT, (self.pdir / "demo" / "01-cadrage.in.md").read_text())

    def test_the_retry_message_has_its_own_trace(self):
        self.new()
        defn = self.recipe("brief-client")["steps"][0]
        bad = fake_output(defn, self.recipe("brief-client")["context_sheet"]).replace(
            "### constraints\nVALUE[cadrage.constraints]\n", "")
        self.write_fakes("brief-client", cadrage=bad)
        self.ok("next", "demo", "--yes")
        folder = self.pdir / "demo"
        self.assertEqual((folder / "01-cadrage.retry.in.md").read_text(), self.received("cadrage", "retry"))
        self.assertEqual((folder / "01-cadrage.in.md").read_text(), self.received("cadrage"))

    def test_a_rerun_keeps_the_previous_trace(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        first = (self.pdir / "demo" / "01-cadrage.in.md").read_text()
        self.ok("rerun", "demo", "cadrage")
        self.ok("next", "demo", "--yes")
        self.assertEqual((self.pdir / "demo" / "01-cadrage.in.v1.md").read_text(), first)


# ---------------------------------------------------------------------------
# End of the parcours, branching, human corrections, blocking, answers on step 1
# ---------------------------------------------------------------------------
class PauseAndCorrectionTests(ParcoursTestCase):
    def edit_recipe(self, old, new, recipe_id="brief-client"):
        path = self.root / "skills" / f"{recipe_id}.md"
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text.count(old), 1, old)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def sheet_file(self, **values):
        path = self.tmp / "fiche.json"
        path.write_text(json.dumps(values), encoding="utf-8")
        return path

    def fields_file(self, need="hand need"):
        path = self.tmp / "champs.md"
        path.write_text(
            f"### need\n{need}\n### constraints\nhand c\n### hypotheses\nhand h\n### open_points\nhand o\n"
            '## CONTEXT SHEET\n```json\n{"client": "HAND-CLIENT"}\n```\n## SUMMARY\nby hand\n', encoding="utf-8")
        return path

    def to_decision_pause(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        self.ok("answer", "demo", "--none")
        self.ok("choose", "demo", "--run", "explorer,decision")
        self.ok("next", "demo", "--yes")
        self.assertEqual(self.state()["pending"]["step"], "decision")

    # -- 8: end announced by validate -------------------------------------------
    def test_validating_the_last_step_announces_the_final_output(self):
        self.edit_recipe("      pause: none\n      model: sonnet\n---", "      pause: validate\n      model: sonnet\n---")
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        self.ok("answer", "demo", "--none")
        self.ok("choose", "demo", "--skip")
        out = self.ok("next", "demo", "--yes")
        self.assertNotIn("Parcours terminé", out)
        self.assertEqual(self.state()["status"], "active")
        out = self.ok("validate", "demo")
        self.assertEqual(self.state()["status"], "completed")
        self.assertIn("Parcours terminé. Sortie finale : 05-brief.md", out)

    def test_choose_that_ends_the_parcours_announces_the_final_output(self):
        self.edit_recipe("      skill: ix-skills:brief\n", "      skill: ix-skills:brief\n      optional: true\n")
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        self.ok("answer", "demo", "--none")
        out = self.ok("choose", "demo", "--skip")
        self.assertEqual(self.state()["status"], "completed")
        self.assertIn("Parcours terminé. Sortie finale : 02-questioning.md", out)

    # -- 9: choose with a subset -------------------------------------------------
    def test_choose_refuses_a_step_whose_input_comes_from_a_step_skipped_in_the_same_choice(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        self.ok("answer", "demo", "--none")
        code, _, err = self.cli("choose", "demo", "--run", "decision")
        self.assertEqual(code, 1)
        self.assertIn("'decision'", err)
        self.assertIn("explorer.options", err)
        self.assertIn("explorer", err)
        self.assertEqual(self.state()["pending"]["type"], "choose")  # nothing changed
        self.assertEqual(self.step("decision")["status"], "pending")
        self.ok("choose", "demo", "--run", "explorer")  # the other subset stays valid

    # -- 16a: validate --context at any validate pause -----------------------------
    def test_context_can_be_corrected_at_a_later_validate_pause(self):
        self.to_decision_pause()
        folder = self.pdir / "demo"
        before = (folder / "00-context.md").read_text()
        out = self.ok("validate", "demo", "--context", str(self.sheet_file(client="LATE-EDIT", objective="o")))
        self.assertIn("ancienne", out)
        self.assertEqual(self.state()["context_sheet"]["client"], "LATE-EDIT")
        self.assertEqual((folder / "00-context.v1.md").read_text(), before)
        self.assertTrue(self.state()["context_validated"])
        self.assertEqual(self.step("decision")["status"], "done")
        self.ok("next", "demo", "--yes")
        self.assertIn("LATE-EDIT", self.received("brief"))

    # -- 16b: handoff --file on a done or paused step -----------------------------
    def test_handoff_corrects_a_paused_step_and_versions_its_output(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        folder = self.pdir / "demo"
        old_output = (folder / "01-cadrage.md").read_text()
        self.ok("handoff", "demo", "cadrage", "--file", str(self.fields_file()))
        step = self.step("cadrage")
        self.assertEqual(step["status"], "paused")
        self.assertEqual(step["handoff"]["need"], "hand need")
        self.assertEqual((folder / "01-cadrage.v1.md").read_text(), old_output)
        self.assertIn("sortie fournie à la main", (folder / "01-cadrage.md").read_text())
        state = self.state()
        self.assertEqual(state["pending"]["type"], "validate")
        self.assertEqual(state["pending"]["step"], "cadrage")
        self.assertFalse(state["context_validated"])
        self.assertEqual(state["context_sheet"]["client"], "HAND-CLIENT")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        self.assertIn("hand need", self.received("questioning"))
        self.assertIn("HAND-CLIENT", self.received("questioning"))

    def test_handoff_on_a_done_step_resets_the_steps_that_consumed_its_fields(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")  # questioning played, waiting for answers
        self.assertEqual(self.step("questioning")["status"], "paused")
        out = self.ok("handoff", "demo", "cadrage", "--file", str(self.fields_file()))
        self.assertIn("questioning", out)
        state = self.state()
        self.assertEqual(self.step("cadrage")["status"], "done")
        self.assertEqual(self.step("questioning")["status"], "pending")
        self.assertIsNone(state["pending"])  # the pause of the reset step is gone
        self.assertTrue(state["context_validated"])  # the human gave the sheet: no pause to re-validate it
        self.assertTrue((self.pdir / "demo" / "02-questioning.v1.md").is_file())
        self.assertTrue((self.pdir / "demo" / "01-cadrage.v1.md").is_file())
        self.ok("next", "demo", "--yes")
        self.assertIn("hand need", self.received("questioning"))

    def test_handoff_on_a_done_step_leaves_unrelated_steps_and_pauses_alone(self):
        self.to_decision_pause()
        fields = self.tmp / "champs.md"
        fields.write_text("### options\nhand options\n## SUMMARY\nS\n", encoding="utf-8")
        self.ok("handoff", "demo", "explorer", "--file", str(fields))
        self.assertEqual(self.step("explorer")["handoff"]["options"], "hand options")
        self.assertEqual(self.step("explorer")["status"], "done")
        self.assertEqual(self.step("decision")["status"], "pending")  # consumed explorer.options
        self.assertEqual(self.step("questioning")["status"], "done")
        self.assertIsNone(self.state()["pending"])

    def test_handoff_reopens_a_completed_parcours_only_if_steps_are_reset(self):
        self.new()
        self.write_fakes("brief-client")
        self.drive()
        fields = self.tmp / "champs.md"
        fields.write_text("### final_brief\nhand brief\n", encoding="utf-8")
        self.ok("handoff", "demo", "brief", "--file", str(fields))
        self.assertEqual(self.state()["status"], "completed")
        self.assertEqual(self.step("brief")["handoff"]["final_brief"], "hand brief")
        self.ok("handoff", "demo", "cadrage", "--file", str(self.fields_file()))
        self.assertEqual(self.state()["status"], "active")
        self.assertEqual(self.step("brief")["status"], "pending")

    def test_handoff_refuses_a_stopped_parcours(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo", "--stop")
        code, _, err = self.cli("handoff", "demo", "cadrage", "--file", str(self.fields_file()))
        self.assertEqual(code, 1)
        self.assertIn("arrêté", err)

    # -- 17: blocking signal -----------------------------------------------------
    def blocking_brief(self, value):
        defn = self.recipe("brief-client")["steps"][4]
        text = fake_output(defn)
        return text.replace("## SUMMARY", f"### blocking\n{value}\n## SUMMARY")

    def to_last_step(self):
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        self.ok("answer", "demo", "--none")
        self.ok("choose", "demo", "--skip")

    def test_a_blocking_section_pauses_a_step_whose_pause_is_none(self):
        self.new()
        self.write_fakes("brief-client", brief=self.blocking_brief("The budget is unknown."))
        self.to_last_step()
        out = self.ok("next", "demo", "--yes")
        state = self.state()
        self.assertEqual(self.step("brief")["status"], "paused")
        self.assertEqual(state["status"], "active")  # the runner never stops the run by itself
        self.assertEqual(state["pending"]["type"], "validate")
        self.assertIn("Blocage signalé par l'étape 'brief'", state["pending"]["message"])
        self.assertIn("The budget is unknown.", state["pending"]["message"])
        self.assertIn("Blocage signalé par l'étape 'brief'", out)
        self.assertEqual(self.step("brief")["blocking"], "The budget is unknown.")
        out = self.ok("validate", "demo")
        self.assertEqual(self.state()["status"], "completed")
        self.assertIn("Parcours terminé", out)

    def test_a_blocking_pause_can_end_in_a_no_go(self):
        self.new()
        self.write_fakes("brief-client", brief=self.blocking_brief("Stop here."))
        self.to_last_step()
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo", "--stop")
        self.assertEqual(self.state()["status"], "stopped")

    def test_no_pause_without_a_blocking_text(self):
        self.new()
        self.write_fakes("brief-client", brief=self.blocking_brief("None"))
        self.to_last_step()
        self.ok("next", "demo", "--yes")
        self.assertEqual(self.step("brief")["status"], "done")
        self.assertEqual(self.state()["status"], "completed")
        self.assertNotIn("blocking", self.step("brief"))

    def test_the_blocking_section_is_asked_for_in_the_message(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.assertIn("### blocking", self.received("cadrage"))

    def test_a_blocking_text_that_copies_the_request_is_refused(self):
        self.new()
        leak = " ".join(INPUT_TEXT.split()[:45])
        self.write_fakes("brief-client", brief=self.blocking_brief(leak))
        self.to_last_step()
        code, _, err = self.cli("next", "demo", "--yes")
        self.assertEqual(code, 1)
        self.assertIn("blocking", err)
        self.assertEqual(self.step("brief")["status"], "failed")

    # -- 19: step 1 with an answers pause -----------------------------------------
    def test_the_context_step_may_pause_for_answers(self):
        self.edit_recipe("      produces_context_sheet: true\n      pause: validate\n",
                         "      produces_context_sheet: true\n      pause: answers\n")
        self.new()
        self.write_fakes("brief-client")
        out = self.ok("next", "demo", "--yes")
        state = self.state()
        self.assertEqual(self.step("cadrage")["status"], "paused")
        self.assertEqual(state["pending"]["type"], "answers")
        self.assertIn("01-cadrage.md", state["pending"]["message"])
        self.assertIn("Fiche de contexte", out)
        self.assertIn("CTX-client", out)  # the sheet is shown with the pause
        self.assertFalse(state["context_validated"])

        code, _, err = self.cli("validate", "demo")  # a plain validate is not this pause
        self.assertEqual(code, 1)
        self.assertIn("attend une pause", err)

        self.ok("validate", "demo", "--context", str(self.sheet_file(client="FIXED", objective="o")))
        state = self.state()
        self.assertEqual(state["context_sheet"]["client"], "FIXED")
        self.assertEqual(state["pending"]["type"], "answers")  # still waiting for the answers
        self.assertFalse(state["context_validated"])
        self.assertTrue((self.pdir / "demo" / "00-context.v1.md").is_file())

        self.ok("answer", "demo", "--file", str(self.answers_file))
        state = self.state()
        self.assertTrue(state["context_validated"])  # `answer` validates the sheet too
        self.assertEqual(self.step("cadrage")["status"], "done")
        self.ok("next", "demo", "--yes")
        self.assertIn("FIXED", self.received("questioning"))

    def test_context_option_is_refused_at_an_answers_pause_of_another_step(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo")
        self.ok("next", "demo", "--yes")
        code, _, err = self.cli("validate", "demo", "--context", str(self.sheet_file(client="x")))
        self.assertEqual(code, 1)
        self.assertIn("attend une pause", err)

    def test_rerun_of_a_step_one_with_answers_clears_the_answers(self):
        self.edit_recipe("      produces_context_sheet: true\n      pause: validate\n",
                         "      produces_context_sheet: true\n      pause: answers\n")
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.ok("answer", "demo", "--none")
        self.ok("rerun", "demo", "cadrage")
        state = self.state()
        self.assertIsNone(state["answers"])
        self.assertFalse(state["context_validated"])


# ---------------------------------------------------------------------------
# Support for the tracking interface (docs/interface.md §6): plan, status --json,
# next --if-state, JSON errors
# ---------------------------------------------------------------------------
class InterfaceSupportTests(ParcoursTestCase):
    def snapshot(self, slug="demo"):
        """{relative path: sha256} of every file of the parcours folder, hidden ones included."""
        base = self.pdir / slug
        return {str(p.relative_to(base)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(base.rglob("*")) if p.is_file() and p.name != ".lock"}

    def json_of(self, *argv):
        code, out, err = self.cli(*argv)
        self.assertEqual(code, 0, f"{argv} -> {code}\n{out}\n{err}")
        return json.loads(out)

    def fingerprint(self, slug="demo"):
        raw = (self.pdir / slug / "state.json").read_bytes()
        ctx = self.pdir / slug / "00-context.md"
        return hashlib.sha256(raw + b"\0" + (ctx.read_bytes() if ctx.is_file() else b"")).hexdigest()

    # -- plan --json -------------------------------------------------------
    def test_plan_writes_nothing(self):
        self.new()
        self.write_fakes("brief-client")
        before = self.snapshot()
        mtime = (self.pdir / "demo" / "state.json").stat().st_mtime_ns
        plan = self.json_of("plan", "demo", "--json")
        self.assertTrue(plan["runnable"])
        self.assertEqual(self.snapshot(), before)
        self.assertEqual((self.pdir / "demo" / "state.json").stat().st_mtime_ns, mtime)
        self.assertFalse((self.pdir / "demo" / ".lock").exists())  # no probe, no lock file created
        self.assertFalse(self.was_called("cadrage"))

    def test_plan_writes_nothing_at_a_pause_and_with_engine_overrides(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")  # pause validate
        before = self.snapshot()
        paused = self.json_of("plan", "demo", "--json", "--engine", "codex")
        self.assertFalse(paused["runnable"])
        self.assertEqual(paused["reason"], "pending")
        self.assertEqual(paused["pending"]["type"], "validate")
        self.ok("validate", "demo")
        before = self.snapshot()
        plan = self.json_of("plan", "demo", "--json", "--engine", "codex", "--engine-step", "questioning=agy")
        self.assertTrue(plan["runnable"])
        self.assertEqual(self.snapshot(), before)  # the override is not saved by the plan
        self.assertEqual(self.state()["engine"], "fake")

    def test_plan_content(self):
        self.new()
        self.write_fakes("brief-client")
        plan = self.json_of("plan", "demo", "--json", "--engine", "claude", "--max-budget-usd", "2")
        self.assertEqual([r["id"] for r in plan["steps"]], ["cadrage"])  # stops at the first pause
        row = plan["steps"][0]
        self.assertEqual((row["engine"], row["model"], row["pause"]), ("claude", "opus", "validate"))
        self.assertGreater(row["chars"], 0)
        self.assertGreaterEqual(row["bytes"], row["chars"])
        self.assertEqual(plan["claude_steps"], 1)
        self.assertEqual(plan["max_budget_usd"], 2.0)
        self.assertEqual(plan["ceiling_usd"], 4.0)  # 1 claude step x 2 $ x 2 (the retry)
        self.assertEqual(plan["calls"], {"claude": 1})
        self.assertEqual(plan["subscription_calls"], 0)
        self.assertFalse(plan["agy_argv_warning"])
        self.assertTrue(plan["changes_default_engine"])
        self.assertFalse(plan["locked"])
        self.assertEqual(plan["fingerprint"], self.fingerprint())

    def test_plan_counts_subscription_calls_and_flags_agy(self):
        self.new("reponse-appel-offres", slug="rao")
        self.write_fakes("reponse-appel-offres")
        plan = self.json_of("plan", "rao", "--json", "--engine", "agy")
        self.assertTrue(plan["agy_argv_warning"])
        self.assertFalse(plan["agy_over_limit"])
        self.assertEqual(plan["calls"], {"agy": len(plan["steps"])})
        self.assertEqual(plan["subscription_calls"], len(plan["steps"]))
        self.assertEqual(plan["claude_steps"], 0)
        self.assertEqual(plan["ceiling_usd"], 0.0)
        mixed = self.json_of("plan", "rao", "--json", "--engine", "codex", "--engine-step", "analyse-cdc=claude")
        self.assertEqual(mixed["claude_steps"], 1)
        self.assertEqual(mixed["ceiling_usd"], 10.0)  # default ceiling 5 $ x 1 x 2
        self.assertFalse(mixed["agy_argv_warning"])

    def test_plan_flags_a_message_too_long_for_agy(self):
        self.new()
        with mock.patch.object(parcours, "ARGV_PROMPT_LIMIT", 10):
            plan = self.json_of("plan", "demo", "--json", "--engine", "agy")
        self.assertTrue(plan["agy_over_limit"])

    def test_plan_says_why_nothing_runs(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        state = self.state()
        state["steps"][0]["status"] = "failed"
        state["steps"][0]["error"] = "boom"
        state["pending"] = None
        (self.pdir / "demo" / "state.json").write_text(json.dumps(state), encoding="utf-8")
        plan = self.json_of("plan", "demo", "--json")
        self.assertFalse(plan["runnable"])
        self.assertEqual(plan["reason"], "failed")
        self.assertIn("a échoué", plan["message"])
        self.ok("retry", "demo")
        self.ok("next", "demo", "--yes")
        self.ok("validate", "demo", "--stop")
        self.assertEqual(self.json_of("plan", "demo", "--json")["reason"], "stopped")

    def test_plan_without_json_prints_the_text_plan(self):
        self.new()
        out = self.ok("plan", "demo")
        self.assertIn("Plan : 1 étape(s)", out)

    def test_the_fingerprint_follows_the_state_and_the_context_sheet(self):
        self.new()
        self.write_fakes("brief-client")
        first = self.json_of("plan", "demo", "--json")["fingerprint"]
        self.assertEqual(first, self.json_of("plan", "demo", "--json")["fingerprint"])
        self.ok("next", "demo", "--yes")
        second = self.json_of("status", "demo", "--json")["fingerprint"]
        self.assertNotEqual(first, second)
        self.assertEqual(second, self.fingerprint())
        (self.pdir / "demo" / "00-context.md").write_text("changed\n", encoding="utf-8")
        self.assertNotEqual(second, self.json_of("status", "demo", "--json")["fingerprint"])

    # -- status --json -----------------------------------------------------
    def test_status_json_has_what_a_page_needs(self):
        self.new()
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        before = self.snapshot()
        status = self.json_of("status", "demo", "--json")
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(status["slug"], "demo")
        self.assertEqual(status["status"], "active")
        self.assertEqual(status["pending"]["type"], "validate")
        self.assertFalse(status["context_validated"])
        self.assertEqual(status["context_sheet"]["client"], "CTX-client")
        self.assertIn("client", status["context_fields"])
        self.assertEqual(status["calls"], {"fake": 1})
        self.assertEqual(status["cost_usd"], 0.0)
        self.assertFalse(status["locked"])
        self.assertIn("01-cadrage.md", status["files"])
        self.assertIn("01-cadrage.in.md", status["files"])
        self.assertIn("state.json", status["files"])
        self.assertNotIn(".lock", status["files"])
        steps = {s["id"]: s for s in status["steps"]}
        self.assertEqual(list(steps), ["cadrage", "questioning", "explorer", "decision", "brief"])
        self.assertEqual(steps["cadrage"]["status"], "paused")
        self.assertEqual(steps["cadrage"]["output"], "01-cadrage.md")
        self.assertEqual(steps["cadrage"]["trace"], "01-cadrage.in.md")
        self.assertEqual(steps["cadrage"]["summary"], "Summary of cadrage.")
        self.assertEqual(steps["cadrage"]["handoff"]["need"], "VALUE[cadrage.need]")
        self.assertEqual(steps["cadrage"]["model"], "opus")
        self.assertEqual(steps["questioning"]["model"], "sonnet")  # from the recipe before it runs
        self.assertEqual(steps["questioning"]["pause"], "answers")
        self.assertTrue(steps["explorer"]["optional"])
        self.assertIsNone(steps["questioning"]["trace"])

    def test_status_json_reports_the_lock(self):
        self.new()
        self.assertFalse(self.json_of("status", "demo", "--json")["locked"])
        with parcours.parcours_lock(self.pdir / "demo"):
            self.assertTrue(self.json_of("status", "demo", "--json")["locked"])
            self.assertTrue(self.json_of("plan", "demo", "--json")["locked"])
        self.assertFalse(self.json_of("status", "demo", "--json")["locked"])

    def test_status_json_survives_a_changed_recipe(self):
        self.new()
        path = self.root / "skills" / "brief-client.md"
        path.write_text(path.read_text(encoding="utf-8").replace("    - id: brief\n", "    - id: brief2\n"), encoding="utf-8")
        status = self.json_of("status", "demo", "--json")
        self.assertIn("a changé", status["recipe_error"])
        self.assertEqual(len(status["steps"]), 5)

    def test_status_json_gives_the_final_output(self):
        self.new()
        self.write_fakes("brief-client")
        self.drive()
        status = self.json_of("status", "demo", "--json")
        self.assertEqual(status["status"], "completed")
        self.assertEqual(status["final_output"], "05-brief.md")

    # -- next --if-state ---------------------------------------------------
    def test_next_with_the_right_fingerprint_runs(self):
        self.new()
        self.write_fakes("brief-client")
        fingerprint = self.json_of("plan", "demo", "--json")["fingerprint"]
        self.ok("next", "demo", "--yes", "--if-state", fingerprint)
        self.assertEqual(self.step("cadrage")["status"], "paused")

    def test_next_with_a_stale_fingerprint_runs_nothing(self):
        self.new()
        self.write_fakes("brief-client")
        fingerprint = self.json_of("plan", "demo", "--json")["fingerprint"]
        (self.pdir / "demo" / "00-context.md").write_text("edited meanwhile\n", encoding="utf-8")
        before = self.snapshot()
        code, out, err = self.cli("next", "demo", "--yes", "--if-state", fingerprint, "--engine", "codex", "--json")
        self.assertEqual(code, 1)
        error = json.loads(out)
        self.assertEqual(error["error"], "state_changed")
        self.assertIn("a changé", error["message"])
        self.assertFalse(self.was_called("cadrage"))
        self.assertEqual(self.snapshot(), before)  # not even the engine override was saved
        self.assertEqual(self.state()["engine"], "fake")

    def test_the_fingerprint_is_checked_under_the_lock(self):
        self.new()
        fingerprint = self.json_of("plan", "demo", "--json")["fingerprint"]
        with parcours.parcours_lock(self.pdir / "demo"):
            code, out, _ = self.cli("next", "demo", "--yes", "--if-state", fingerprint, "--json")
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)["error"], "locked")

    # -- JSON errors -------------------------------------------------------
    def test_json_errors(self):
        code, out, err = self.cli("status", "nope", "--json")
        self.assertEqual(code, 1)
        self.assertEqual(err, "")
        error = json.loads(out)
        self.assertEqual(error["error"], "not_found")
        self.assertIn("introuvable", error["message"])

    def test_json_errors_flag_works_before_and_after_the_command(self):
        for argv in (["--json-errors", "validate", "nope"], ["validate", "nope", "--json-errors"]):
            code, out, err = self.cli(*argv)
            self.assertEqual((code, err), (1, ""), argv)
            self.assertEqual(json.loads(out)["error"], "not_found")
        self.new()
        code, out, _ = self.cli("validate", "demo", "--json-errors")
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)["error"], "error")  # no validate pause open

    def test_errors_stay_text_without_the_flag(self):
        code, out, err = self.cli("status", "nope")
        self.assertEqual((code, out), (1, ""))
        self.assertTrue(err.startswith("Erreur : "))

    def test_error_codes_of_the_failures(self):
        self.new()
        self.write_fakes("brief-client", cadrage="no handoff here\n", cadrage__retry="still none\n")
        code, out, _ = self.cli("next", "demo", "--yes", "--json")
        self.assertEqual(code, 1)
        # the progress text of `next` comes first; the error is the last line of stdout
        self.assertEqual(json.loads(out.strip().splitlines()[-1])["error"], "parse")

    def test_argument_errors_exit_2(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
            parcours.main(["next", "--json"])  # no slug
        self.assertEqual(raised.exception.code, 2)

    def test_double_dash_precedes_positionals(self):
        self.new()
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = parcours.main(["status", "--json", "--parcours-dir", str(self.pdir), "--", "demo"])
        self.assertEqual(code, 0, err.getvalue())
        self.assertEqual(json.loads(out.getvalue())["slug"], "demo")

    # -- stopping ----------------------------------------------------------
    def test_sigterm_becomes_an_exit_inside_next(self):
        import signal
        before = signal.getsignal(signal.SIGTERM)
        with self.assertRaises(SystemExit) as raised:
            with parcours.terminate_as_exit():
                os.kill(os.getpid(), signal.SIGTERM)
                time.sleep(1)
        self.assertEqual(raised.exception.code, 128 + signal.SIGTERM)
        self.assertEqual(signal.getsignal(signal.SIGTERM), before)


# ---------------------------------------------------------------------------
# Recipe format (docs/format-recette.md §2bis)
# ---------------------------------------------------------------------------
class RecipeFormatTests(ParcoursTestCase):
    def set_format(self, line, recipe="brief-client"):
        """Rewrites the `format:` line of a recipe of the temporary repository (None: removes it)."""
        path = self.root / "skills" / f"{recipe}.md"
        text = path.read_text(encoding="utf-8")
        self.assertIn("\n  format: 1\n", text)
        path.write_text(text.replace("\n  format: 1\n", "\n" if line is None else f"\n  format: {line}\n", 1), encoding="utf-8")

    def test_every_recipe_of_the_repository_declares_format_1(self):
        recipes = [p for p in sorted((REPO / "skills").glob("*.md")) if "\nworkflow:" in p.read_text(encoding="utf-8")]
        self.assertGreaterEqual(len(recipes), 2)
        for path in recipes:
            with self.subTest(recipe=path.stem):
                fm, _ = parcours.split_frontmatter(path.read_text(encoding="utf-8"))
                self.assertEqual(fm["workflow"].get("format"), 1)
        for path in sorted((REPO / "dist" / "skills").glob("*/recipe.json")):
            with self.subTest(bundled=path.parent.name):
                self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["workflow"].get("format"), 1)

    def test_a_recipe_at_the_right_format_runs_without_warning(self):
        code, out, err = self.cli("new", "brief-client", "--input", str(self.input_file), "--slug", "demo", "--engine", "fake")
        self.assertEqual(code, 0, err)
        self.assertNotIn("format", err)
        self.assertEqual(self.state()["recipe_format"], 1)
        self.assertEqual(json.loads(self.ok("status", "demo", "--json"))["recipe_format"], 1)
        listed = json.loads(self.ok("recipes", "--json"))
        self.assertEqual(listed["formats"], [1])
        self.assertEqual({r["id"]: (r["format"], r["warnings"]) for r in listed["recipes"]},
                         {"brief-client": (1, []), "reponse-appel-offres": (1, [])})

    def test_a_recipe_without_format_is_read_as_format_1_with_a_warning(self):
        self.set_format(None)
        code, out, err = self.cli("new", "brief-client", "--input", str(self.input_file), "--slug", "demo", "--engine", "fake")
        self.assertEqual(code, 0, err)
        self.assertIn("pas de champ format", err)
        self.assertIn("lue comme format 1", err)
        self.assertEqual(self.state()["recipe_format"], 1)
        listed = {r["id"]: r for r in json.loads(self.ok("recipes", "--json"))["recipes"]}
        self.assertEqual(listed["brief-client"]["format"], 1)
        self.assertIn("ajoutez « format: 1 »", listed["brief-client"]["warnings"][0])
        self.assertIn("avertissement : pas de champ format", self.ok("recipes"))
        self.write_fakes("brief-client")
        self.ok("next", "demo", "--yes")
        self.assertEqual(self.step("cadrage")["status"], "paused")

    def test_a_recipe_of_a_newer_format_is_refused_with_a_clear_message(self):
        self.new()   # a dossier created while the recipe was still at format 1
        self.set_format(2)
        code, out, err = self.cli("new", "brief-client", "--input", str(self.input_file), "--slug", "autre", "--engine", "fake")
        self.assertEqual(code, 1)
        self.assertIn("au format 2", err)
        self.assertIn("mettez la page à jour", err)
        self.assertFalse((self.pdir / "autre").exists())
        code, out, _ = self.cli("new", "brief-client", "--input", str(self.input_file), "--json")
        self.assertEqual(json.loads(out.strip().splitlines()[-1])["error"], "error")
        self.assertNotIn("brief-client", [r["id"] for r in json.loads(self.ok("recipes", "--json"))["recipes"]])
        report = json.loads(self.ok("status", "demo", "--json"))   # the dossier still reads, and says why it cannot go on
        self.assertIn("mettez la page à jour", report["recipe_error"])
        self.assertEqual(report["recipe_format"], 1)
        code, out, _ = self.cli("next", "demo", "--yes", "--json")
        self.assertEqual(code, 1)
        self.assertIn("mettez la page à jour", json.loads(out.strip().splitlines()[-1])["message"])

    def test_an_unknown_format_is_refused(self):
        for value in ("deux", "1.0", "0", "true", "'1'"):
            with self.subTest(format=value):
                self.set_format(value)
                code, _, err = self.cli("new", "brief-client", "--input", str(self.input_file), "--engine", "fake")
                self.assertEqual(code, 1)
                self.assertIn("format de recette inconnu", err)
                self.assertIn("mettez la page à jour", err)
                self.set_format_back()

    def set_format_back(self):
        shutil.copy(REPO / "skills" / "brief-client.md", self.root / "skills")

    def test_the_runner_announces_the_formats_it_plays(self):
        self.assertEqual(json.loads(self.ok("formats", "--json")), {"formats": [1], "current": 1})
        self.assertIn("Formats de recette acceptés : 1", self.ok("formats"))


if __name__ == "__main__":
    unittest.main()
