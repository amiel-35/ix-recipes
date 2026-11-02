"""
Tests of the format 4 of the recipes (docs/format-recette.md §2quinquies, docs/executeur.md §8): bounded loops,
a hidden field, a step played outside the runner, and the refusals of the minimal format.

Run:  cd ~/Projets/ix-recipes && python3 -m unittest tests.test_format4 -v

No engine is ever called: the `fake` engine plays canned outputs (written here per step), the `simulation` engine
builds well-formed ones. The recipe under test is the real one (skills/amont-sujet.md) with its settings
(docs/harnais/A4-reglages.yaml), copied with stub skills into a temporary layout.
"""

import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

import parcours  # noqa: E402

REQUEST = "Écrire un module qui compte les mots d'un texte, parce que l'appelant a déjà retiré la ponctuation.\n"
CANARY = "CANARI-PART-CACHEE-4242"
SKILLS = ["cadrage", "questioning", "decomposer", "controle-qualite", "goal-writing", "critique", "criteres-reussite"]


def output(defn, verdict=None, hidden_text=None):
    """A well-formed output of a step of the recipe; `verdict` starts its verdict field, `hidden_text` its hidden field."""
    parts = [f"Output of {defn['id']}.\n"]
    if defn["produces_context_sheet"]:
        sheet = {f: f"CTX-{f}" for f in ("subject", "objective", "constraints", "readers", "deliverables", "named_solutions", "deadlines")}
        parts.append("## CONTEXT SHEET\n```json\n" + json.dumps(sheet) + "\n```\n")
    parts.append("## HANDOFF\n")
    for field in defn["transmits"]:
        if field == defn.get("output_field"):
            continue
        if field == defn.get("verdict_field"):
            parts.append(f"### {field}\n{verdict or 'OK'}\nLine about {defn['id']}.\n")
        elif field in defn.get("hidden", ()):
            parts.append(f"### {field}\n{hidden_text or 'hidden material of ' + defn['id']}\n")
        else:
            parts.append(f"### {field}\nVALUE[{defn['id']}.{field}]\n")
    parts.append(f"## SUMMARY\nSummary of {defn['id']}.\n")
    return "\n".join(parts)


class Format4TestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test-format4-")).resolve()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.root = self.tmp / "ix-recipes"
        self.subject = self.tmp / "sujet"
        self.pdir = self.subject / "parcours"
        self.seal = self.tmp / "seal"
        self.fake = self.tmp / "fake"
        for folder in (self.subject, self.seal, self.fake):
            folder.mkdir()
        (self.root / "skills").mkdir(parents=True)
        shutil.copy(REPO / "skills" / "amont-sujet.md", self.root / "skills")
        (self.root / "docs" / "harnais").mkdir(parents=True)
        for name in ("A4-reglages.yaml", "A5-grille-cadrage.md"):
            shutil.copy(REPO / "docs" / "harnais" / name, self.root / "docs" / "harnais")
        for skill in SKILLS:
            folder = self.tmp / "ix-skills" / "dist" / "skills" / skill
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(f"---\nname: {skill}\n---\n# Method of {skill}\nSTUB-{skill}\n", encoding="utf-8")
        env = {"PARCOURS_FAKE_DIR": str(self.fake), "HOME": str(self.tmp / "home"), "IX_SCELLE_DIR": str(self.seal),
               "IX_SKILLS_PATH": str(self.tmp / "ix-skills" / "dist" / "skills")}
        patcher = mock.patch.dict(os.environ, env)
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop("IX_REGLAGES", None)
        os.environ.pop("L", None)
        patcher = mock.patch.object(parcours, "ROOT", self.root)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.request = self.subject / "demande.md"
        self.request.write_text(REQUEST, encoding="utf-8")
        self.recipe = parcours.load_recipe("amont-sujet")
        self.defns = {d["id"]: d for d in self.recipe["steps"]}

    # -- helpers ----------------------------------------------------------
    def cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = parcours.main(list(argv) + ["--parcours-dir", str(self.pdir)])
        return code, out.getvalue(), err.getvalue()

    def ok(self, *argv):
        code, out, err = self.cli(*argv)
        self.assertEqual(code, 0, f"{argv} -> {code}\n{out}\n{err}")
        return out

    def new(self, engine="fake", extra=()):
        corpus = [str(self.root / "docs" / "harnais" / n) for n in ("A4-reglages.yaml", "A5-grille-cadrage.md")]
        return self.cli("new", "amont-sujet", "--input", str(self.request), "--slug", "amont", "--engine", engine,
                        "--corpus", *corpus, *extra)

    def canned(self, step_id, text, retry=False):
        (self.fake / f"{step_id}{'.retry' if retry else ''}.md").write_text(text, encoding="utf-8")

    def write_fakes(self, verdicts=None, hidden_text=None):
        """Canned outputs for every step; `verdicts` maps a step to the verdict it gives (default OK)."""
        verdicts = verdicts or {}
        for defn in self.recipe["steps"]:
            self.canned(defn["id"], output(defn, verdicts.get(defn["id"]), hidden_text))

    def state(self):
        return json.loads((self.pdir / "amont" / "state.json").read_text(encoding="utf-8"))

    def pending(self):
        return self.state()["pending"]

    def drive(self, max_rounds=40, stop_at=None):
        """Play the parcours up to a stop that only the pilot can lift (external, ceiling) or its end;
        `stop_at`: a step whose pause is not lifted."""
        for _ in range(max_rounds):
            state = self.state()
            pending = state["pending"]
            if state["status"] != "active":
                return state
            if pending and pending["step"] == stop_at:
                return state
            if pending is None:
                self.ok("next", "amont", "--yes")
            elif pending["type"] == "validate":
                self.ok("validate", "amont")
            elif pending["type"] == "answers":
                self.ok("answer", "amont", "--none")
            else:
                return state
        self.fail("the parcours does not settle")

    def supply(self, text):
        path = self.tmp / "externe.md"
        path.write_text(text, encoding="utf-8")
        return self.cli("supply", "amont", "contre_verif", "--file", str(path))

    def external_output(self, verdict="OK"):
        return f"Counter-check.\n\n## HANDOFF\n### verdict\n{verdict}\nA line.\n## SUMMARY\nDone.\n"

    def files_under(self, folder):
        return [p for p in Path(folder).rglob("*") if p.is_file()]

    def grep(self, folder, needle):
        return [p for p in self.files_under(folder) if needle.encode() in p.read_bytes()]


class RecipeChecksTests(Format4TestCase):
    """The minimal format refuses what it does not have, naming the cause."""

    def check(self, change):
        fm, body = parcours.parse_recipe_text((self.root / "skills" / "amont-sujet.md").read_text(encoding="utf-8"))
        change(fm["workflow"])
        return parcours.workflow_errors(fm, body, lambda ref: True)

    def test_the_recipe_of_the_repository_is_valid(self):
        self.assertEqual(self.check(lambda wf: None), [])

    def test_a_parallel_step_is_refused(self):
        errors = self.check(lambda wf: wf["steps"][0].update(parallel=True))
        self.assertTrue(any("parallèle" in e and "format 4" in e for e in errors), errors)

    def test_a_step_that_writes_is_refused(self):
        errors = self.check(lambda wf: wf["steps"][0].update(writes=True))
        self.assertTrue(any("écrit ou lance des commandes" in e for e in errors), errors)

    def test_the_fable_model_is_refused(self):
        errors = self.check(lambda wf: wf["steps"][1].update(model="fable"))
        self.assertTrue(any("fable" in e and "external" in e for e in errors), errors)

    def test_a_loop_goes_back_to_an_earlier_step_from_a_step_with_a_verdict(self):
        errors = self.check(lambda wf: wf["steps"][3].update(loop={"to": "goal", "ceiling": "passes_verification_max"}))
        self.assertTrue(any("antérieure" in e for e in errors), errors)
        errors = self.check(lambda wf: wf["steps"][3].pop("verdict_field"))
        self.assertTrue(any("verdict_field" in e for e in errors), errors)

    def test_loops_may_not_overlap(self):
        errors = self.check(lambda wf: wf["steps"][4 + 3].update(loop={"to": "fusion", "ceiling": "passes_verification_max"}))
        self.assertTrue(any("se recouvrent" in e for e in errors), errors)

    def test_only_an_external_step_receives_a_hidden_field(self):
        errors = self.check(lambda wf: wf["steps"].__getitem__(10).update(receives=["criteres.part_cachee"]))
        self.assertTrue(any("champ caché" in e and "external" in e for e in errors), errors)

    def test_the_ceiling_and_the_model_of_a_role_come_from_the_settings(self):
        errors = self.check(lambda wf: wf["steps"][3]["loop"].update(ceiling="passes_inconnues_max"))
        self.assertTrue(any("passes_inconnues_max" in e for e in errors), errors)
        errors = self.check(lambda wf: wf["steps"][5].update(model="opus"))   # verif_livrables is a haiku role
        self.assertTrue(any("verification_mecanique" in e for e in errors), errors)

    def test_the_format_4_keys_ask_for_format_4(self):
        errors = self.check(lambda wf: wf.update(format=3))
        for key in ("loop", "hidden", "external", "verdict_field"):
            self.assertTrue(any(f" {key} demande « format: 4 »" in e for e in errors), (key, errors))

    def test_the_runner_refuses_to_load_a_broken_recipe(self):
        path = self.root / "skills" / "amont-sujet.md"
        path.write_text(path.read_text(encoding="utf-8").replace("      skill: ix-skills:cadrage\n", "      skill: ix-skills:cadrage\n      parallel: true\n", 1),
                        encoding="utf-8")
        with self.assertRaises(parcours.ParcoursError) as ctx:
            parcours.load_recipe("amont-sujet")
        self.assertIn("parallèle", str(ctx.exception))

    def test_the_page_does_not_play_format_4(self):
        self.assertEqual(parcours.PAGE_FORMATS, (1, 2, 3))
        self.assertIn("format 4", parcours.format_error({"format": 4}, parcours.PAGE_FORMATS))
        self.assertIsNone(parcours.format_error({"format": 4}))


class LoopTests(Format4TestCase):
    def start(self, **kw):
        code, out, err = self.new()
        self.assertEqual(code, 0, err)
        self.write_fakes(**kw)

    def test_a_chain_without_reproach_runs_to_the_external_stop_then_to_the_end(self):
        self.start()
        state = self.drive()
        self.assertEqual(state["pending"]["type"], "external")
        self.assertEqual(state["pending"]["step"], "contre_verif")
        self.assertEqual(self.supply(self.external_output())[0], 0)
        state = self.drive()
        self.assertEqual(state["status"], "completed")
        self.assertEqual(state["loops"]["contre_verif"]["passes"], 1)

    def test_the_ceiling_is_read_from_the_settings(self):
        self.start(verdicts={"evaluation": "REPRENDRE"})
        state = self.drive()
        self.assertEqual(state["pending"]["type"], "ceiling")
        self.assertEqual(state["loops"]["evaluation"]["passes"], 2)   # plafonds.passes_verification_max in the settings
        self.assertEqual(state["pending"]["suites"], ["relancer", "livrer_avec_reserve", "abandonner"])
        self.assertNotIn("contourner", state["pending"]["suites"])

    def test_changing_the_setting_changes_the_ceiling_with_no_other_edit(self):
        settings = self.root / "docs" / "harnais" / "A4-reglages.yaml"
        settings.write_text(settings.read_text(encoding="utf-8").replace("passes_verification_max: 2", "passes_verification_max: 3"),
                            encoding="utf-8")
        self.start(verdicts={"verif_goal": "REPRENDRE"})
        state = self.drive()
        self.assertEqual((state["pending"]["type"], state["loops"]["verif_goal"]["passes"]), ("ceiling", 3))

    def test_a_verdict_goes_back_with_the_verdict_as_an_extra_input(self):
        self.start()
        self.canned("verif_goal", output(self.defns["verif_goal"], "REPRENDRE"))
        self.ok("validate", "amont") if self.pending() and self.pending()["type"] == "validate" else None
        for _ in range(12):
            state = self.state()
            if state["loops"].get("verif_goal", {}).get("passes"):
                break
            self.drive_one()
        self.canned("verif_goal", output(self.defns["verif_goal"], "OK"))
        self.ok("next", "amont", "--yes")
        goal = [s for s in self.state()["steps"] if s["id"] == "goal"][0]
        self.assertEqual(len(goal["runs"]), 2)   # the goal was written twice
        received = (self.fake / "received" / "goal.md").read_text(encoding="utf-8")
        self.assertIn("=== INPUT: verif_goal.verdict ===", received)

    def drive_one(self):
        state = self.state()
        pending = state["pending"]
        if pending is None:
            self.ok("next", "amont", "--yes")
        elif pending["type"] == "validate":
            self.ok("validate", "amont")
        elif pending["type"] == "answers":
            self.ok("answer", "amont", "--none")

    def test_the_session_never_chooses_the_suite(self):
        self.start(verdicts={"evaluation": "REPRENDRE"})
        self.drive()
        code, _, err = self.cli("next", "amont", "--yes")
        self.assertEqual(self.pending()["type"], "ceiling")
        calls_before = self.state()["calls"]
        self.cli("next", "amont", "--yes")
        self.assertEqual(self.state()["calls"], calls_before)   # nothing is played above the ceiling

    def test_a_suite_outside_the_offered_ones_is_refused(self):
        self.start(verdicts={"evaluation": "REPRENDRE"})
        self.drive()
        code, _, err = self.cli("suite", "amont", "--suite", "contourner")
        self.assertEqual(code, 1)
        self.assertIn("non offerte", err)
        self.assertEqual(self.pending()["type"], "ceiling")

    def test_relancer_adds_the_passes_the_pilot_fixes(self):
        self.start(verdicts={"evaluation": "REPRENDRE"})
        self.drive()
        code, _, err = self.cli("suite", "amont", "--suite", "relancer")
        self.assertEqual(code, 1)
        self.assertIn("--n", err)
        self.ok("suite", "amont", "--suite", "relancer", "--n", "1")
        state = self.drive()
        self.assertEqual(state["pending"]["type"], "ceiling")
        self.assertEqual(state["loops"]["evaluation"]["passes"], 3)
        self.assertEqual(state["suites"][0]["passes_ajoutees"], 1)

    def test_livrer_avec_reserve_goes_on_with_the_reserve_written(self):
        self.start(verdicts={"evaluation": "REPRENDRE"})
        self.drive()
        self.assertEqual(self.cli("suite", "amont", "--suite", "livrer_avec_reserve")[0], 1)
        self.ok("suite", "amont", "--suite", "livrer_avec_reserve", "--text", "le cadrage garde un défaut mineur", "--by", "Amiel")
        state = self.state()
        self.assertEqual(state["suites"][0]["reserve"], "le cadrage garde un défaut mineur")
        self.assertEqual(state["steps"][3]["status"], "done")

    def test_abandonner_stops_the_parcours(self):
        self.start(verdicts={"evaluation": "REPRENDRE"})
        self.drive()
        self.ok("suite", "amont", "--suite", "abandonner")
        self.assertEqual(self.state()["status"], "stopped")

    def test_an_unreadable_verdict_fails_the_step(self):
        self.start()
        self.canned("evaluation", output(self.defns["evaluation"], "peut-être"))
        code = 0
        for _ in range(10):
            code, _, err = self.cli("next", "amont", "--yes")
            if code:
                break
            self.drive_one()
        self.assertEqual(code, 1)
        self.assertIn("verdict illisible", err)

    def test_a_verdict_without_a_loop_waits_for_the_human(self):
        self.start(verdicts={"verif_livrables": "REPRENDRE"})
        state = self.drive(stop_at="verif_livrables")
        self.assertEqual((state["pending"]["type"], state["pending"]["step"]), ("verdict", "verif_livrables"))
        self.assertIn("REPRENDRE", state["pending"]["message"])
        self.assertEqual(self.cli("validate", "amont")[0], 1)   # a verdict is not a pause to lift
        calls = self.state()["calls"]
        self.cli("next", "amont", "--yes")
        self.assertEqual(self.state()["calls"], calls)           # the goal is not played
        self.assertEqual(self.state()["steps"][6]["status"], "pending")
        self.ok("validate", "amont", "--stop")
        self.assertEqual(self.state()["status"], "stopped")

    def test_the_form_check_goes_back_when_the_closing_is_redone(self):
        self.start(verdicts={"verif_livrables": "REPRENDRE"})
        self.drive(stop_at="verif_livrables")
        self.canned("verif_livrables", output(self.defns["verif_livrables"], "OK"))
        self.ok("rerun", "amont", "cloture")
        state = self.drive()
        self.assertEqual(state["pending"]["type"], "external")
        self.assertEqual(len(self.state()["steps"][5]["runs"]), 2)

    def test_the_simulation_engine_writes_the_accepting_value_first(self):
        code, out, err = self.new("simulation")
        self.assertEqual(code, 0, err)
        state = self.drive()
        self.assertEqual(state["pending"]["step"], "contre_verif")
        text = (self.pdir / "amont" / "04-evaluation.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"### verdict\nOK\n")


class ModelsTests(Format4TestCase):
    def test_each_call_takes_the_model_of_its_role_in_the_settings_read_at_creation(self):
        settings = self.root / "docs" / "harnais" / "A4-reglages.yaml"
        text = settings.read_text(encoding="utf-8")
        text = re.sub(r"(?m)^(\s+redaction_goal:)\s*\S+", r"\1 haiku", text)
        text = re.sub(r"(?m)^(\s+cadrage_et_criteres:)\s*\S+", r"\1 sonnet", text)
        settings.write_text(text, encoding="utf-8")
        code, _, err = self.new("simulation")
        self.assertEqual(code, 0, err)
        self.drive()
        models = {s["id"]: s.get("model") for s in self.state()["steps"]}
        self.assertEqual((models["goal"], models["criteres"], models["cadrage"]), ("haiku", "sonnet", "sonnet"))
        self.assertEqual(models["evaluation"], "opus")
        settings.write_text(text.replace("redaction_goal: haiku", "redaction_goal: opus"), encoding="utf-8")   # a later edit changes nothing in a created parcours
        self.assertEqual(json.loads(self.ok("status", "amont", "--json"))["steps"][6]["model"], "haiku")
        self.assertEqual(self.state()["models"]["goal"], "haiku")

    def test_the_external_step_has_no_model(self):
        self.new("simulation")
        self.drive()
        step = [s for s in self.state()["steps"] if s["id"] == "contre_verif"][0]
        self.assertIsNone(step.get("model"))
        self.assertEqual(step["engine"], "externe")


class HiddenFieldTests(Format4TestCase):
    def test_the_hidden_field_leaves_the_dossier_and_lives_in_the_sealed_place(self):
        code, _, err = self.new()
        self.assertEqual(code, 0, err)
        self.write_fakes(hidden_text=f"critère caché {CANARY}")
        self.drive()
        self.assertEqual(self.grep(self.subject, CANARY), [], "the hidden part is in a file of the dossier")
        sealed = self.grep(self.seal, CANARY)
        self.assertTrue(sealed)
        self.assertIn("amont", str(sealed[0]))
        criteria = self.state()["steps"][8]
        self.assertEqual(criteria["handoff"]["part_cachee"], parcours.HIDDEN_MARK)
        self.assertIn("part_cachee", criteria["hidden"])
        self.assertIn(parcours.HIDDEN_MARK, (self.pdir / "amont" / "09-criteres.md").read_text(encoding="utf-8"))

    def test_the_hidden_field_survives_a_retry_without_a_trace_in_the_dossier(self):
        self.new()
        self.write_fakes()
        broken = output(self.defns["criteres"], hidden_text=f"caché {CANARY}").replace("### grille_visible", "### visible")
        self.canned("criteres", broken)
        self.canned("criteres", output(self.defns["criteres"], hidden_text=f"caché {CANARY}"), retry=True)
        self.drive()
        self.assertEqual(self.grep(self.subject, CANARY), [])
        self.assertTrue((self.pdir / "amont" / "09-criteres.retry.in.md").is_file())

    def test_no_message_of_a_step_played_by_the_runner_carries_the_hidden_field(self):
        self.new()
        self.write_fakes(hidden_text=f"caché {CANARY}")
        self.drive()
        received = self.fake / "received"
        self.assertEqual(self.grep(received, CANARY), [])

    def test_the_external_step_receives_it_and_its_message_stays_in_the_sealed_place(self):
        self.new()
        self.write_fakes(hidden_text=f"caché {CANARY}")
        self.drive()
        self.assertEqual(self.grep(self.subject, CANARY), [])
        messages = [p for p in self.grep(self.seal, CANARY) if p.name.endswith("contre_verif.in.md")]
        self.assertTrue(messages)

    def test_the_sealed_place_is_required_and_checked(self):
        with mock.patch.dict(os.environ, {"IX_SCELLE_DIR": ""}):
            code, _, err = self.new()
        self.assertEqual(code, 1)
        self.assertIn("IX_SCELLE_DIR manque", err)
        self.assertFalse(self.pdir.exists())
        for bad, why in ((self.subject / "scelle", "lié à un chemin"), (self.root / "scelle", "lié à un chemin")):
            with mock.patch.dict(os.environ, {"IX_SCELLE_DIR": str(bad)}):
                code, _, err = self.new()
            self.assertEqual(code, 1, bad)
            self.assertIn(why, err)
        repo = self.tmp / "depot"
        repo.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        with mock.patch.dict(os.environ, {"IX_SCELLE_DIR": str(repo / "scelle")}):
            code, _, err = self.new()
        self.assertEqual(code, 1)
        self.assertIn("dépôt git", err)

    def test_redaction_keeps_the_rest_of_the_output(self):
        text = "Doc.\n\n## HANDOFF\n### a\nvisible\n### part_cachee\nsecret\n```\ncode\n```\n### b\nautre\n## SUMMARY\nfin\n"
        redacted = parcours.redact_fields(text, ["part_cachee"])
        self.assertNotIn("secret", redacted)
        self.assertNotIn("code", redacted)
        self.assertIn("visible", redacted)
        self.assertIn("autre", redacted)
        self.assertIn("fin", redacted)


class ExternalStepTests(Format4TestCase):
    def test_the_recipe_stops_before_the_counter_check_and_the_pending_names_the_step(self):
        self.new()
        self.write_fakes()
        self.drive()
        report = json.loads(self.ok("status", "amont", "--json"))
        self.assertEqual(report["pending"]["step"], "contre_verif")
        self.assertEqual(report["pending"]["type"], "external")
        self.assertEqual(report["status"], "active")
        step = [s for s in report["steps"] if s["id"] == "contre_verif"][0]
        self.assertTrue(step["external"])
        self.assertEqual(step["status"], "paused")

    def test_nothing_runs_past_the_stop_until_the_output_is_supplied(self):
        self.new()
        self.write_fakes()
        self.drive()
        before = self.state()["calls"]
        self.cli("next", "amont", "--yes")
        self.assertEqual(self.state()["calls"], before)
        self.assertEqual(self.state()["steps"][-1]["status"], "pending")   # reconciliation

    def test_a_supplied_output_that_asks_to_redo_sends_the_parcours_back_and_counts_a_pass(self):
        self.new()
        self.write_fakes()
        self.drive()
        self.assertEqual(self.supply(self.external_output("REPRENDRE"))[0], 0)
        state = self.state()
        self.assertEqual(state["loops"]["contre_verif"]["passes"], 1)
        self.assertEqual(state["steps"][8]["status"], "pending")   # criteres, to be played again
        state = self.drive()
        self.assertEqual(state["pending"]["step"], "contre_verif")
        self.supply(self.external_output("REPRENDRE"))
        state = self.state()
        self.assertEqual(state["pending"]["type"], "ceiling")   # the second pass reaches the ceiling

    def test_supply_refuses_another_step_or_a_missing_stop(self):
        self.new()
        self.write_fakes()
        code, _, err = self.cli("supply", "amont", "contre_verif", "--file", str(self.request))
        self.assertEqual(code, 1)
        self.drive()
        path = self.tmp / "x.md"
        path.write_text(self.external_output(), encoding="utf-8")
        code, _, err = self.cli("supply", "amont", "criteres", "--file", str(path))
        self.assertEqual(code, 1)
        self.assertIn("contre_verif", err)

    def test_the_cost_and_model_of_the_pilots_call_are_kept_for_the_trace(self):
        self.new()
        self.write_fakes()
        self.drive()
        path = self.tmp / "x.md"
        path.write_text(self.external_output(), encoding="utf-8")
        self.ok("supply", "amont", "contre_verif", "--file", str(path), "--model", "fable", "--cost-usd", "1.25")
        run = self.state()["steps"][9]["runs"][0]
        self.assertEqual((run["engine"], run["model"], run["cost_usd"], run["external"]), ("externe", "fable", 1.25, True))


class FormatsTests(Format4TestCase):
    def test_the_runner_plays_four_formats_and_the_page_three(self):
        self.assertEqual(parcours.RECIPE_FORMATS, (1, 2, 3, 4))
        self.assertEqual(json.loads(self.ok("formats", "--json"))["formats"], [1, 2, 3, 4])

    def test_a_format_1_to_3_recipe_keeps_its_state_free_of_format_4_keys(self):
        state = parcours.new_state({"id": "x", "version": "1", "format": 1, "steps": []}, "x", "fake", {}, {})
        for key in ("loops", "ceilings", "pauses", "suites"):
            self.assertNotIn(key, state)


if __name__ == "__main__":
    unittest.main()
