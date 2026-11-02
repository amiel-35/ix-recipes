"""
Tests of the tools of the harness (harnais/, docs/harnais/spec-harnais.md): launching a subject, the trace of format A3,
the freeze, the ceilings counted by the harness, the sealed part, the judge, and the hook.

Run:  cd ~/Projets/ix-recipes && python3 -m unittest tests.test_harnais -v

No model is ever called: the amont runs on the `simulation` engine, the judge is a fake `claude` found by PATH, the
hook is called with test events. Every mechanism that must refuse is tried on a case that passes and on a case that is refused.
"""

import contextlib
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "harnais"))

import parcours  # noqa: E402
import commun  # noqa: E402
import garde  # noqa: E402
import harnais  # noqa: E402
import hook  # noqa: E402
import trace_a3  # noqa: E402

SKILLS = ["cadrage", "questioning", "decomposer", "controle-qualite", "goal-writing", "critique", "criteres-reussite"]
CANARY = "CANARI-JUGE-9917"
GOAL = "# Goal\n\n## Values fixed later\n\n`<ACCEPTANCE_SCRIPT>` is `acceptation.sh`.\n\n## Intent\n\nWrite the module.\n"
VERDICT = (REPO / "harnais" / "modele-verdict.md").read_text(encoding="utf-8")


class HarnaisTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="test-harnais-")).resolve()
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.subject = self.tmp / "sujet"
        self.seal = self.tmp / "seal"
        self.bin = self.tmp / "bin"
        for folder in (self.subject, self.seal, self.bin):
            folder.mkdir()
        for skill in SKILLS:
            folder = self.tmp / "ix-skills" / "dist" / "skills" / skill
            folder.mkdir(parents=True)
            (folder / "SKILL.md").write_text(f"---\nname: {skill}\n---\n# Method of {skill}\nSTUB-{skill}\n", encoding="utf-8")
        env = {"S": str(self.subject), "R": str(REPO), "IX_SCELLE_DIR": str(self.seal), "HOME": str(self.tmp / "home"),
               "IX_SKILLS_PATH": str(self.tmp / "ix-skills" / "dist" / "skills"), "IX_PILOTE": "Amiel",
               "PATH": f"{self.bin}{os.pathsep}{os.environ['PATH']}"}
        patcher = mock.patch.dict(os.environ, env)
        patcher.start()
        self.addCleanup(patcher.stop)
        os.environ.pop("L", None)
        (self.subject / "demande.md").write_text("# Compter les mots\n\nÉcrire un module qui compte les mots d'un texte.\n", encoding="utf-8")
        (self.subject / "acceptation.sh").write_text("#!/bin/sh\necho 'OK 1'\n", encoding="utf-8")
        (self.subject / "grille.md").write_text("# Grille\n\nR1 le module existe.\n", encoding="utf-8")
        (self.subject / "fixtures").mkdir()
        (self.subject / "fixtures" / "exemples.txt").write_text("un deux trois\n", encoding="utf-8")

    # -- helpers ----------------------------------------------------------
    def run_h(self, *argv):
        """Run a command of the harness in the subject's folder; (code, stdout, stderr)."""
        out, err = io.StringIO(), io.StringIO()
        old = os.getcwd()
        os.chdir(self.subject)
        try:
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = harnais.main(list(argv))
        finally:
            os.chdir(old)
        return code, out.getvalue(), err.getvalue()

    def ok(self, *argv):
        code, out, err = self.run_h(*argv)
        self.assertEqual(code, 0, f"{argv} -> {code}\n{out}\n{err}")
        return out

    def refused(self, *argv):
        code, out, err = self.run_h(*argv)
        self.assertEqual(code, 1, f"{argv} should be refused\n{out}\n{err}")
        return err

    def launch(self):
        self.ok("lancer", "code", "--engine", "simulation")

    def amont(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = parcours.main(list(argv) + ["--parcours-dir", str(self.subject / "parcours")])
        self.assertEqual(code, 0, err.getvalue())

    def play_amont(self, external_output=None):
        for _ in range(60):
            state = commun.etat_amont(self.subject)
            pending = state["pending"]
            if state["status"] != "active":
                return
            if pending is None:
                self.amont("next", "amont", "--yes")
            elif pending["type"] == "validate":
                self.amont("validate", "amont")
            elif pending["type"] == "answers":
                self.amont("answer", "amont", "--none")
            elif pending["type"] == "external":
                path = self.tmp / "externe.md"
                path.write_text("Counter-check.\n\n## HANDOFF\n### verdict\nOK\nrien\n## SUMMARY\nok\n", encoding="utf-8")
                self.ok("contre-verif", str(path))
            else:
                self.fail(f"unexpected stop {pending}")
        self.fail("the amont does not settle")

    def freeze(self):
        self.launch()
        self.play_amont()
        self.ok("geler", "livrable", "acceptation.sh", "grille.md", "fixtures")

    def etat(self):
        return commun.charger_etat(self.subject)

    def scelle(self):
        return commun.scelle(self.subject)

    def garde(self):
        return garde.lire_brut(self.scelle())

    def set_tours(self, nom, n):
        """Test helper: put the guard's counter at `n`, as `n` end-of-turn hooks would have (through the guard's own writer)."""
        def fixer(g):
            g["tours"][nom] = n
        garde.modifier(self.scelle(), self.subject, fixer)

    def prod_env(self):
        """The environment of the production session: the pilot's variable is not in it; Claude Code gives the project folder."""
        env = {k: v for k, v in os.environ.items() if k != "IX_SCELLE_DIR"}
        env["CLAUDE_PROJECT_DIR"] = str(self.subject)
        return env

    def declared(self, event):
        """The command the settings of the subject declare for a hook event (what Claude Code runs)."""
        settings = json.loads((self.subject / ".claude" / "settings.json").read_text(encoding="utf-8"))
        return settings["hooks"][event][0]["hooks"][0]["command"]

    def fire(self, event, payload=None, env=None):
        """Run the declared hook command the way Claude Code does: `sh -c`, the event as JSON on stdin, in the production env."""
        payload = dict({"session_id": "essai", "transcript_path": "/dev/null", "cwd": str(self.subject), "hook_event_name": event}, **(payload or {}))
        return subprocess.run(["sh", "-c", self.declared(event)], input=json.dumps(payload), capture_output=True, text=True,
                              cwd=self.subject, env=env or self.prod_env())

    def stop_turn(self):
        done = self.fire("Stop")
        self.assertEqual(done.returncode, 0, done.stderr)
        return json.loads(done.stdout) if done.stdout.strip() else {}

    def fake_judge(self, text=None):
        script = self.bin / "claude"
        verdict = (text or VERDICT).replace("@@EXIGENCE@@", "H7").replace("@@CANARI@@", CANARY)
        script.write_text("#!/bin/sh\ncat <<'EOF_VERDICT'\n" + verdict + "\nEOF_VERDICT\n", encoding="utf-8")
        script.chmod(script.stat().st_mode | stat.S_IEXEC)

    def deliverable(self):
        (self.subject / "livrable").mkdir(exist_ok=True)
        (self.subject / "livrable" / "compte_mots.py").write_text("def compter(texte):\n    return len(texte.split())\n", encoding="utf-8")

    def tables(self):
        return trace_a3.lire_tables((self.subject / "trace.md").read_text(encoding="utf-8"))

    def grep(self, folder, needle):
        return [p for p in Path(folder).rglob("*") if p.is_file() and needle.encode() in p.read_bytes()]


class LaunchTests(HarnaisTestCase):
    def test_a_subject_of_a_known_type_opens_with_t1_t2_and_step_0(self):
        self.launch()
        tables = self.tables()
        self.assertEqual(tables["T1"][0]["type_de_sujet"], "code")
        self.assertEqual(tables["T1"][0]["version_réglages"], "1.0.0")
        self.assertEqual({r["plafond"] for r in tables["T2"]},
                         {"passes_verification_max", "tours_correction_max", "tours_goal_max",
                          "production.sous_agents_niveaux_max", "production.sous_agents_parallele_max"})
        self.assertEqual(tables["T3"][0]["étape"], "0")
        self.assertTrue((self.subject / "parcours" / "amont" / "state.json").is_file())

    def test_a_missing_type_and_a_part_c_type_are_refused_and_nothing_is_created(self):
        for argv in (("lancer", "inconnu"), ("lancer", "formation"), ("lancer", "audit_ux"), ("lancer", "reponse_commerciale")):
            with self.subTest(argv=argv):
                err = self.refused(*argv, "--engine", "simulation")
                self.assertRegex(err, r"absent des réglages|partie C")
                self.assertEqual(sorted(p.name for p in self.subject.iterdir()), ["acceptation.sh", "demande.md", "fixtures", "grille.md"])
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                harnais.main(["lancer"])

    def test_the_sealed_place_is_required_at_launch(self):
        with mock.patch.dict(os.environ, {"IX_SCELLE_DIR": ""}):
            self.assertIn("IX_SCELLE_DIR manque", self.refused("lancer", "code", "--engine", "simulation"))
        repo = self.tmp / "depot"
        repo.mkdir()
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        with mock.patch.dict(os.environ, {"IX_SCELLE_DIR": str(repo / "s")}):
            self.assertIn("dépôt git", self.refused("lancer", "code", "--engine", "simulation"))
        with mock.patch.dict(os.environ, {"IX_SCELLE_DIR": str(self.subject / "s")}):
            self.assertIn("lié à un chemin", self.refused("lancer", "code", "--engine", "simulation"))
        self.assertFalse((self.subject / ".harnais").exists())

    def test_a_subject_is_launched_once(self):
        self.launch()
        self.assertIn("déjà lancé", self.refused("lancer", "code", "--engine", "simulation"))

    def test_the_trace_is_idempotent_and_holds_a3(self):
        self.launch()
        self.play_amont()
        self.ok("trace")
        first = (self.subject / "trace.md").read_text(encoding="utf-8")
        self.ok("trace")
        self.assertEqual(first, (self.subject / "trace.md").read_text(encoding="utf-8"))
        self.assertEqual(trace_a3.controler(first), [])

    def test_the_trace_marks_a_simulated_cost_n_c_and_never_as_measured(self):
        self.launch()
        self.play_amont()
        for ligne in self.tables()["T3"][1:]:
            if "simulé" in ligne["agent"]:
                self.assertEqual((ligne["coût"], ligne["source_coût"]), ("n.c.", "n.c."), ligne["ligne"])
                self.assertIn("simulé", ligne["méthode_coût"])

    def test_a_claude_cost_is_measured_and_a_pass_has_its_occurrence(self):
        self.launch()
        self.play_amont()
        state_path = self.subject / "parcours" / "amont" / "state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        run = state["steps"][0]["runs"][0]
        run.update(engine="claude", cost_usd=0.4321)
        state_path.write_text(json.dumps(state), encoding="utf-8")
        self.ok("trace")
        t3 = {(r["étape"], r["occurrence"]): r for r in self.tables()["T3"]}
        self.assertEqual((t3[("1a", "unique")]["coût"], t3[("1a", "unique")]["source_coût"]), ("0,43 $", "mesuré"))
        for etape in ("1d", "2A", "2B"):
            self.assertIn((etape, "passe 1"), t3)

    def test_the_trace_check_catches_what_a3_forbids(self):
        self.launch()
        text = (self.subject / "trace.md").read_text(encoding="utf-8")
        self.assertEqual(trace_a3.controler(text), [])
        broken = text.replace("| sujet | Compter", "|  | Compter")
        self.assertTrue(any("cellule vide" in p or "colonnes" in p for p in trace_a3.controler(broken)))
        estimated = text.replace("| personne : aucun appel d'outil |", "| personne : aucun appel d'outil |", 1)
        row = "| L02 | 1a | unique | appel | demande.md | x | humain | humain | 1.0.0 | 1 s | n.c. | appel | 1,00 $ | estimé | | sans objet | sans objet | n.c. |"
        problems = trace_a3.controler(text.replace("### T4.", row + "\n\n### T4.", 1))
        self.assertTrue(any("estimé sans méthode" in p or "cellule vide" in p for p in problems), problems)


class SuiteAndCeilingTests(HarnaisTestCase):
    def write_goal(self, text=GOAL):
        (self.subject / "goal.md").write_text(text, encoding="utf-8")

    def test_a_suite_is_consigned_only_at_a_ceiling_reached_and_among_the_offered_ones(self):
        self.freeze()
        self.write_goal()
        self.assertIn("pas atteint", self.refused("suite", "tours_goal", "relancer", "3"))
        self.assertIn("inconnu des réglages", self.refused("suite", "tours_inconnus", "relancer", "3"))
        self.assertIn("hors de suites_au_plafond.passes_verification", self.refused("suite", "passes_verification", "contourner", "x"))
        self.assertIn("aucun plafond des passes", self.refused("suite", "passes_verification", "relancer", "1"))

    def test_the_production_ceiling_is_counted_by_the_harness_and_a_refused_call_counts_nothing(self):
        self.freeze()
        self.write_goal()
        limit = self.etat()["reglages"]["plafonds"]["tours_goal_max"]
        for n in range(limit):
            self.ok("tour")
        self.assertEqual(self.etat()["tours"]["goal"], limit)
        err = self.refused("tour")
        self.assertIn("le plafond tours_goal_max est atteint", err)
        self.assertIn("aucune suite", err)
        for suite in ("relancer", "contourner", "livrer_avec_reserve", "abandonner"):
            self.assertNotIn(suite, err)   # the production is never offered a suite (P3)
        self.assertEqual(self.etat()["tours"]["goal"], limit)   # the refused call counted no turn
        # the ceiling is reached (T2) and nobody has chosen yet: T7 holds no invented suite, its sentence says so
        tables = self.tables()
        self.assertEqual({r["plafond"]: r["atteint"] for r in tables["T2"]}["tours_goal_max"], "oui")
        self.assertEqual(tables["T7"], [])
        text = (self.subject / "trace.md").read_text(encoding="utf-8")
        self.assertIn("aucun plafond atteint n'a encore reçu de suite", text)
        self.assertIn("tours_goal_max", text.split("### T7.")[1].split("### T8.")[0])
        note = [r for r in tables["T3"] if r["occurrence"] == f"tour {limit}"][0]["note"]
        self.assertIn("la main revient au pilote", note)

    def test_relancer_gives_the_turns_the_pilot_fixes_and_is_traced(self):
        self.freeze()
        self.write_goal()
        self.set_tours("goal", self.etat()["reglages"]["plafonds"]["tours_goal_max"] - 1)
        self.ok("tour")
        self.refused("tour")
        self.assertIn("un nombre", self.refused("suite", "tours_goal", "relancer", "beaucoup"))
        self.ok("suite", "tours_goal", "relancer", "2")
        self.ok("tour")
        self.ok("tour")
        self.refused("tour")
        row = [r for r in self.tables()["T7"] if r["plafond"] == "tours_goal_max"][0]
        self.assertEqual((row["suite_choisie"], row["tours_ajoutés"], row["décideur"]), ("relancer", "2", "Amiel"))
        # the 2 turns are used: a new ceiling is reached, with no suite yet, and the trace says it under the table
        self.assertIn("Plafonds atteints dont le pilote n'a pas encore choisi la suite", (self.subject / "trace.md").read_text(encoding="utf-8"))

    def test_the_other_suites_end_the_production_or_wait_for_a_new_freeze(self):
        for suite, argument in (("abandonner", None), ("livrer_avec_reserve", "reste un défaut mineur"), ("contourner", "R3 revu, ambigu")):
            with self.subTest(suite=suite):
                shutil.rmtree(self.subject / ".harnais", ignore_errors=True)
                for name in ("parcours", "trace.md", ".claude", "livrable"):
                    p = self.subject / name
                    shutil.rmtree(p, ignore_errors=True) if p.is_dir() else p.unlink(missing_ok=True)
                shutil.rmtree(self.seal, ignore_errors=True)
                self.seal.mkdir()
                self.freeze()
                self.write_goal()
                self.set_tours("goal", self.etat()["reglages"]["plafonds"]["tours_goal_max"] - 1)
                self.ok("tour")
                self.ok(*(["suite", "tours_goal", suite] + ([argument] if argument else [])))
                self.assertIn("tour refusé", self.refused("tour"))

    def test_the_correction_has_its_own_counter_and_ceiling(self):
        self.freeze()
        self.write_goal()
        self.ok("tour")
        limit = self.etat()["reglages"]["plafonds"]["tours_correction_max"]
        for _ in range(limit):
            self.ok("tour-correction")
        self.assertIn("tours_correction_max", self.refused("tour-correction"))
        self.assertEqual(self.etat()["tours"], {"goal": 1, "correction": limit})

    def test_a_turn_is_refused_without_freeze_on_a_gap_and_with_an_unfilled_slot(self):
        self.launch()
        self.write_goal()
        self.assertIn("pas gelé", self.refused("tour"))
        self.play_amont()
        self.ok("geler", "livrable", "acceptation.sh", "grille.md", "fixtures")
        self.write_goal("# Goal\n\n## Values fixed later\n\n`<ACCEPTANCE_SCRIPT>`\n\n## Stopping condition\n\nRun `<ACCEPTANCE_SCRIPT>` and `<TRACE_FILE>`.\n")
        err = self.refused("tour")
        self.assertIn("<ACCEPTANCE_SCRIPT>", err)
        self.assertIn("<TRACE_FILE>", err)
        self.assertEqual(self.etat()["tours"]["goal"], 0)
        self.write_goal()
        self.ok("tour")
        (self.subject / "grille.md").write_text("changée\n", encoding="utf-8")
        self.assertIn("grille.md", self.refused("tour"))

    def test_the_amont_ceiling_takes_its_suite_through_the_harness(self):
        self.launch()
        fakes = self.tmp / "fakes"
        fakes.mkdir()
        self.assertIn("aucun plafond", self.refused("suite", "passes_verification", "relancer", "1"))


class FreezeTests(HarnaisTestCase):
    def test_the_freeze_takes_the_fingerprints_seals_the_hidden_part_and_declares_the_hook(self):
        self.freeze()
        tables = self.tables()
        elements = {(r["élément"], r["emplacement"]): r for r in tables["T9"]}
        self.assertIn(("script de recette", "acceptation.sh"), elements)
        self.assertIn(("grille visible", "grille.md"), elements)
        self.assertIn(("fixtures", "fixtures/exemples.txt"), elements)
        hidden = elements[("part cachée", "non écrit")]
        self.assertEqual(hidden["état"], "scellé")
        self.assertEqual(hidden["ouvert_à"], "à venir")
        settings = json.loads((self.subject / ".claude" / "settings.json").read_text(encoding="utf-8"))
        command = settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        self.assertEqual(command, commun.manifeste()["CMD_HOOK"])   # the declared command is the manifest's, word for word
        self.assertIn("$R", command)
        self.ok("empreintes")

    def test_the_freeze_keeps_the_hooks_already_declared(self):
        (self.subject / ".claude").mkdir()
        (self.subject / ".claude" / "settings.json").write_text(json.dumps(
            {"permissions": {"allow": ["Bash(ls)"]}, "hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [{"type": "command", "command": "true"}]}]}}), encoding="utf-8")
        self.freeze()
        settings = json.loads((self.subject / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertEqual(settings["permissions"], {"allow": ["Bash(ls)"]})
        self.assertEqual(len(settings["hooks"]["PreToolUse"]), 2)

    def test_the_first_changed_file_is_named(self):
        self.freeze()
        self.ok("empreintes")
        (self.subject / "fixtures" / "exemples.txt").write_text("autre\n", encoding="utf-8")
        err = self.refused("empreintes")
        self.assertIn("fixtures/exemples.txt", err)
        (self.subject / "fixtures" / "exemples.txt").write_text("un deux trois\n", encoding="utf-8")
        (self.subject / "acceptation.sh").unlink()
        self.assertIn("acceptation.sh", self.refused("empreintes"))

    def test_rewriting_the_fingerprints_in_the_subject_does_not_fool_the_check(self):
        self.freeze()
        (self.subject / "grille.md").write_text("critère affaibli\n", encoding="utf-8")
        files = self.etat()["gel"]["fichiers"]
        lines = [f"{commun.sha256_file(self.subject / f)}  {f}" for f in files]
        (self.subject / ".harnais" / "empreintes.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")
        self.assertIn("copie du scellé", self.refused("empreintes"))

    def test_a_subject_is_frozen_once_and_its_files_must_exist_inside_it(self):
        self.launch()
        self.assertIn("introuvable", self.refused("geler", "livrable", "n-existe-pas.sh"))
        self.assertIn("relatif", self.refused("geler", "livrable", "../hors.sh"))
        self.assertIn("ne peut pas contenir", self.refused("geler", str(self.tmp), "grille.md"))
        self.ok("geler", "livrable", "grille.md")
        self.assertIn("regeler", self.refused("geler", "livrable", "grille.md"))

    def test_the_freeze_opens_again_only_by_a_traced_contourner(self):
        self.freeze()
        (self.subject / "goal.md").write_text(GOAL, encoding="utf-8")
        self.assertIn("contourner", self.refused("regeler"))
        self.set_tours("goal", self.etat()["reglages"]["plafonds"]["tours_goal_max"] - 1)
        self.ok("tour")
        self.ok("suite", "tours_goal", "contourner", "R3 est ambigu : on le précise en 2B")
        (self.subject / "grille.md").write_text("# Grille\n\nR1 précisée.\n", encoding="utf-8")
        self.assertIn("grille.md", self.refused("empreintes"))
        self.ok("regeler")
        self.ok("empreintes")
        self.assertEqual(self.etat()["tours"], {"goal": 0, "correction": 0})
        self.assertEqual(self.etat()["gel"]["regels"], 1)
        self.assertIn("contourner", self.refused("regeler"))   # a derogation opens the freeze once
        row = [r for r in self.tables()["T3"] if r["occurrence"] == "regel 1"]
        self.assertTrue(row)
        derogation = [r for r in self.tables()["T7"] if r["suite_choisie"] == "contourner"][0]
        self.assertIn("R3 est ambigu", derogation["dérogation"])


class JudgeTests(HarnaisTestCase):
    def finish_production(self):
        self.freeze()
        (self.subject / "goal.md").write_text(GOAL, encoding="utf-8")
        self.ok("tour")
        self.deliverable()
        self.ok("fin-production")

    def test_the_end_of_production_commits_the_deliverable_and_tags_it(self):
        self.finish_production()
        livrable = self.subject / "livrable"
        tags = subprocess.run(["git", "tag"], cwd=livrable, capture_output=True, text=True).stdout.split()
        self.assertEqual(tags, ["livrable-1"])
        log = subprocess.run(["git", "log", "--oneline"], cwd=livrable, capture_output=True, text=True).stdout
        self.assertEqual(len(log.splitlines()), 1)
        self.assertEqual(subprocess.run(["git", "status", "--porcelain"], cwd=livrable, capture_output=True, text=True).stdout, "")
        self.assertTrue([r for r in self.tables()["T9"] if r["élément"].startswith("livrable (étiquette livrable-1)")])

    def test_the_judge_is_refused_when_the_deliverable_moved_since_its_tag(self):
        self.finish_production()
        self.fake_judge()
        (self.subject / "livrable" / "compte_mots.py").write_text("def compter(t):\n    return 0\n", encoding="utf-8")
        self.assertIn("a bougé depuis l'étiquette livrable-1", self.refused("juge"))
        subprocess.run(["git", "checkout", "-q", "--", "."], cwd=self.subject / "livrable", check=True)
        (self.subject / "livrable" / "nouveau.py").write_text("x = 1\n", encoding="utf-8")
        self.assertIn("a bougé depuis l'étiquette", self.refused("juge"))
        (self.subject / "livrable" / "nouveau.py").unlink()
        self.ok("juge")

    def test_the_judge_needs_a_frozen_unchanged_subject_and_a_claude_command(self):
        self.finish_production()
        with mock.patch.dict(os.environ, {"PATH": "/usr/bin:/bin"}):
            if shutil.which("claude"):
                self.skipTest("a real claude is installed in the minimal PATH")
            self.assertIn("introuvable dans le PATH", self.refused("juge"))
        self.fake_judge()
        (self.subject / "grille.md").write_text("changée\n", encoding="utf-8")
        self.assertIn("grille.md", self.refused("juge"))

    def test_the_finding_for_the_producer_names_the_hidden_requirement_without_its_content(self):
        self.finish_production()
        self.fake_judge()
        self.ok("juge")
        finding = (self.subject / "constat-juge.md").read_text(encoding="utf-8")
        self.assertIn("H7", finding)
        self.assertNotIn(CANARY, finding)
        self.assertEqual(self.grep(self.subject, CANARY), [])   # nothing in the subject's folder holds the proof
        sealed = self.grep(self.seal, CANARY)
        self.assertTrue(sealed)
        self.assertEqual(self.etat()["juge"]["appels"][0]["echecs_caches"], 1)
        t3 = [r for r in self.tables()["T3"] if r["étape"] == "5"][0]
        self.assertEqual((t3["occurrence"], t3["granularité"], t3["sortie"]), ("appel du juge 1", "étape", "scellé, voir T9"))
        judge_row = [r for r in self.tables()["T9"] if r["élément"] == "trace du juge"][0]
        self.assertEqual((judge_row["état"], judge_row["emplacement"]), ("scellé", "non écrit"))

    def test_a_visible_failure_gives_its_proof_to_the_producer(self):
        self.finish_production()
        self.fake_judge(VERDICT.replace("| V1 | visible | passe |", "| V1 | visible | échec |"))
        self.ok("juge")
        finding = (self.subject / "constat-juge.md").read_text(encoding="utf-8")
        self.assertIn("V1", finding)
        self.assertIn("script de recette relancé", finding)

    def test_the_judge_runs_from_a_neutral_folder_that_is_removed(self):
        self.finish_production()
        marker = self.tmp / "cwd.txt"
        script = self.bin / "claude"
        script.write_text("#!/bin/sh\npwd > " + str(marker) + "\ncat <<'EOF_V'\n" + VERDICT.replace("@@EXIGENCE@@", "H7").replace("@@CANARI@@", CANARY) + "\nEOF_V\n", encoding="utf-8")
        script.chmod(script.stat().st_mode | stat.S_IEXEC)
        self.ok("juge")
        cwd = Path(marker.read_text(encoding="utf-8").strip())
        self.assertNotIn(self.subject, [cwd, *cwd.parents])
        self.assertTrue(cwd.name.startswith("juge-"))
        self.assertFalse(cwd.exists())

    def test_an_unreadable_verdict_is_refused_but_kept_in_the_sealed_place(self):
        self.finish_production()
        self.fake_judge("Tout va bien.\n")
        self.assertIn("pas au format du harnais", self.refused("juge"))
        sealed = sorted(p for p in self.seal.iterdir() if p.is_dir())   # `index.json` est un fichier : un seul dossier, celui du sujet
        self.assertEqual(len(sealed), 1)
        self.assertTrue((sealed[0] / "juge" / "sortie-1.md").is_file())
        self.assertFalse((self.subject / "constat-juge.md").exists())

    def test_the_hidden_part_and_the_judge_trace_open_only_at_the_end_of_the_corrections(self):
        self.finish_production()
        self.assertIn("aucun jugement", self.refused("ouvrir"))
        self.fake_judge()
        self.ok("juge")
        err = self.refused("ouvrir")
        self.assertIn("tours de correction ne sont pas terminés", err)
        self.assertFalse((self.subject / "jugement").exists())
        for _ in range(self.etat()["reglages"]["plafonds"]["tours_correction_max"]):
            self.ok("tour-correction")
        self.ok("ouvrir")
        self.assertTrue((self.subject / "jugement" / "part-cachee.md").is_file())
        self.assertTrue((self.subject / "jugement" / "trace-du-juge-1.md").is_file())
        states = {r["élément"]: (r["état"], r["emplacement"]) for r in self.tables()["T9"] if r["élément"] in ("part cachée", "trace du juge")}
        self.assertEqual(states["part cachée"], ("ouvert", "jugement/part-cachee.md"))
        self.assertEqual(states["trace du juge"], ("ouvert", "jugement/trace-du-juge-1.md"))
        self.assertIn("déjà ouvert", self.refused("ouvrir"))

    def test_the_judgement_opens_at_once_when_nothing_fails(self):
        self.finish_production()
        self.fake_judge("| exigence | part | verdict | preuve |\n|---|---|---|---|\n| V1 | visible | passe | ok |\n| H1 | cachée | passe | ok |\n")
        self.ok("juge")
        self.assertIn("Aucune exigence en échec", (self.subject / "constat-juge.md").read_text(encoding="utf-8"))
        self.ok("ouvrir")

    def test_the_sealed_path_is_given_to_the_pilot_tool_alone(self):
        self.launch()
        path = self.ok("sceau").strip()
        self.assertTrue(path.startswith(str(self.seal.resolve())))
        self.assertEqual(self.grep(self.subject, path), [])


class HookTests(HarnaisTestCase):
    def event(self, tool, **tool_input):
        return {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": tool_input, "cwd": str(self.subject)}

    def decide(self, event):
        try:
            hook.decider(event)
        except hook.Refus as refus:
            return str(refus)
        return None

    def test_writes_to_frozen_files_and_to_the_state_are_refused_after_the_freeze(self):
        self.freeze()
        for tool in ("Write", "Edit", "MultiEdit"):
            for target in ("acceptation.sh", "grille.md", "fixtures/exemples.txt", ".harnais/etat.json", ".harnais/empreintes.sha256"):
                with self.subTest(tool=tool, target=target):
                    self.assertIsNotNone(self.decide(self.event(tool, file_path=str(self.subject / target))))
        self.assertIsNotNone(self.decide(self.event("Write", file_path="grille.md")))   # relative to the event's folder
        self.assertIsNone(self.decide(self.event("Write", file_path=str(self.subject / "livrable" / "compte_mots.py"))))
        self.assertIsNone(self.decide(self.event("Write", file_path=str(self.subject / "notes.md"))))
        self.assertIsNone(self.decide(self.event("Read", file_path=str(self.subject / "grille.md"))))

    def test_before_the_freeze_only_the_unconditional_refusals_apply(self):
        self.launch()
        self.assertIsNone(self.decide(self.event("Write", file_path=str(self.subject / "grille.md"))))
        self.assertIsNotNone(self.decide(self.event("Write", file_path=str(self.subject / ".claude" / "settings.json"))))

    def test_the_settings_that_declare_hooks_cannot_be_written(self):
        self.freeze()
        for target in (self.subject / ".claude" / "settings.json", self.subject / ".claude" / "settings.local.json",
                       self.subject / "livrable" / ".claude" / "settings.json", self.tmp / "ailleurs" / ".claude" / "settings.local.json",
                       REPO / "harnais" / "hooks.json"):
            with self.subTest(target=target):
                self.assertIsNotNone(self.decide(self.event("Write", file_path=str(target))))
        for command in ("echo '{}' > .claude/settings.json", "sed -i '' s/a/b/ .claude/settings.local.json", "rm -f livrable/.claude/settings.json",
                        f"cp x {REPO}/harnais/hooks.json"):
            with self.subTest(command=command):
                self.assertIsNotNone(self.decide(self.event("Bash", command=command)))

    def test_the_pilots_seal_command_is_refused_to_the_production(self):
        self.freeze()
        sceau = commun.manifeste()["CMD_SCEAU"].replace('"$R"', str(REPO))
        for command in (commun.manifeste()["CMD_SCEAU"], sceau, f"x=$({sceau})", "python3 harnais/harnais.py sceau", "cd /x && python3 'h/harnais.py' sceau"):
            with self.subTest(command=command):
                self.assertIn("commande du pilote", self.decide(self.event("Bash", command=command)) or "")

    def test_no_command_that_chooses_or_reopens_is_the_productions(self):
        self.freeze()
        for name in ("suite", "regeler", "ouvrir", "juge", "geler", "lancer", "contre-verif"):
            command = commun.manifeste()[f"CMD_{name.upper().replace('-', '_')}"].replace("$R", str(REPO))
            with self.subTest(command=name):
                self.assertIsNotNone(self.decide(self.event("Bash", command=f"{command} tours_goal_max relancer 5")))
        for name in ("tour", "tour-correction", "empreintes", "trace", "fin-production"):
            command = commun.manifeste()[f"CMD_{name.upper().replace('-', '_')}"].replace("$R", str(REPO))
            with self.subTest(command=name):
                self.assertIsNone(self.decide(self.event("Bash", command=command)))

    def test_the_sealed_place_and_its_variable_are_closed_to_the_production(self):
        self.freeze()
        sealed = self.ok("sceau").strip()
        self.assertIsNotNone(self.decide(self.event("Read", file_path=sealed + "/amont/criteres.part_cachee.md")))
        self.assertIsNotNone(self.decide(self.event("Bash", command=f"cat {sealed}/juge/sortie-1.md")))
        self.assertIsNotNone(self.decide(self.event("Bash", command="echo $IX_SCELLE_DIR")))
        self.assertIsNotNone(self.decide(self.event("Grep", pattern="x", path=sealed)))
        self.assertIsNone(self.decide(self.event("Read", file_path=str(self.subject / "livrable" / "x.py"))))

    def test_shell_writes_to_frozen_files_are_refused_and_reads_and_runs_are_not(self):
        self.freeze()
        refused = ["echo x > grille.md", "echo x >> fixtures/exemples.txt", "sed -i '' 's/a/b/' grille.md", "rm acceptation.sh",
                   "mv grille.md /tmp/g", "tee grille.md < /dev/null", "git checkout -- grille.md", "rm -rf fixtures",
                   "python3 -c \"open('fixtures/exemples.txt','w').write('x')\"", "chmod 777 acceptation.sh", "rm -r .harnais",
                   "echo x > .harnais/etat.json", f"cp /dev/null {self.subject}/grille.md"]
        for command in refused:
            with self.subTest(command=command):
                self.assertIsNotNone(self.decide(self.event("Bash", command=command)), command)
        allowed = ["bash acceptation.sh .", "cat grille.md", "bash acceptation.sh . > sortie.txt 2>&1", "sha256sum grille.md acceptation.sh",
                   "python3 -m unittest", "ls fixtures", "echo x > livrable/notes.txt", "diff grille.md /tmp/x", "cd livrable && git status",
                   "python3 livrable/compte_mots.py fixtures/exemples.txt"]
        for command in allowed:
            with self.subTest(command=command):
                self.assertIsNone(self.decide(self.event("Bash", command=command)), command)

    def test_the_hook_reads_the_form_of_a_call_not_only_the_manifest_string(self):
        self.freeze()
        for command in ("python3 \"$R/harnais/harnais.py\" 'su''ite' tours_goal_max relancer 3", "cd harnais && ./harnais.py regeler",
                        "python3 -m harnais juge", "python3 /somewhere/harnais.py \"ouvrir\"", "sh -c 'python3 harnais/harnais.py geler x'",
                        "python3 -c 'import harnais; harnais.cmd_juge(None)'", "python3 harnais/harnais.py contre-verif x.md"):
            with self.subTest(command=command):
                self.assertIn("commande du pilote", self.decide(self.event("Bash", command=command)) or "")
        for command in ("grep -n juge docs/harnais/spec-harnais.md", "cat harnais/harnais.py", "python3 -m unittest tests.test_harnais",
                        "sed -n '1,20p' harnais/hook.py", "python3 harnais/harnais.py tour", "python3 harnais/harnais.py fin-production"):
            with self.subTest(command=command):
                self.assertIsNone(self.decide(self.event("Bash", command=command)), command)

    def test_the_hook_refuses_to_empty_the_environment_but_this_is_not_what_keeps_the_seal_out(self):
        self.freeze()
        for command in ("printenv", "env | grep SCELLE", "python3 -c 'import os; print(os.environ)'", "cat /proc/self/environ", "export -p"):
            with self.subTest(command=command):
                self.assertIsNotNone(self.decide(self.event("Bash", command=command)))
        self.assertIsNone(self.decide(self.event("Bash", command="env FOO=1 python3 x.py")))

    def test_the_hook_command_has_the_exit_codes_of_the_interface(self):
        self.freeze()
        env = dict(os.environ)
        command = commun.manifeste()["CMD_HOOK"]
        refused = subprocess.run(["sh", "-c", command], input=json.dumps(self.event("Write", file_path=str(self.subject / "grille.md"))),
                                 capture_output=True, text=True, cwd=self.subject, env=env)
        self.assertEqual(refused.returncode, 2)
        self.assertIn("figé", refused.stderr)
        accepted = subprocess.run(["sh", "-c", command], input=json.dumps(self.event("Write", file_path=str(self.subject / "notes.md"))),
                                  capture_output=True, text=True, cwd=self.subject, env=env)
        self.assertEqual((accepted.returncode, accepted.stdout, accepted.stderr), (0, "", ""))
        garbage = subprocess.run(["sh", "-c", command], input="pas du json", capture_output=True, text=True, cwd=self.subject, env=env)
        self.assertEqual(garbage.returncode, 2)

    def test_the_hook_of_the_settings_is_the_manifest_command(self):
        declared = json.loads((REPO / "harnais" / "hooks.json").read_text(encoding="utf-8"))
        commands = [h["command"] for e in declared["hooks"]["PreToolUse"] for h in e["hooks"]]
        self.assertIn(commun.manifeste()["CMD_HOOK"], commands)


class PilotProofTests(HarnaisTestCase):
    """O11, P3 and the pilot's token: the pilot's commands refuse by themselves, whatever the form of the call, unless the caller
    holds the sealed place of the subject. What a pilot command changes lives in the sealed place (the guard), where the hooks read it."""

    PILOT = [("sceau",), ("suite", "tours_goal_max", "relancer", "3"), ("regeler",), ("ouvrir",), ("juge",),
             ("geler", "livrable", "grille.md"), ("lancer", "code"), ("contre-verif", "x.md"), ("empreintes",), ("trace",)]

    def goal(self):
        (self.subject / "goal.md").write_text(GOAL, encoding="utf-8")

    def reach_the_ceiling(self):
        self.freeze()
        self.goal()
        for _ in range(self.etat()["reglages"]["plafonds"]["tours_goal_max"]):
            self.ok("tour")

    def fake_root(self, name="faux-scelle"):
        forged = self.tmp / name
        forged.mkdir()
        return forged

    def test_without_the_sealed_place_no_harness_command_runs_but_the_end_of_production(self):
        self.freeze()
        self.goal()
        with mock.patch.dict(os.environ):
            os.environ.pop("IX_SCELLE_DIR")
            for argv in self.PILOT + [("tour",), ("tour-correction",)]:
                with self.subTest(command=argv[0]):
                    self.assertIn("IX_SCELLE_DIR", self.refused(*argv))
            self.deliverable()
            self.ok("fin-production")
        self.assertEqual(self.garde()["tours"], {"goal": 0, "correction": 0})   # nothing was counted by those calls

    def test_the_forgery_of_the_reviewer_fails(self):
        """A fake sealed folder at the name the old code computed from the subject's path, a token of its own, and the reference of the
        token rewritten in the state: the pilot's commands refuse, the real guard keeps its ceiling."""
        self.reach_the_ceiling()
        forged = self.fake_root()
        slug = commun.P.slugify(self.subject.name)
        old_name = f"{slug}-{commun.sha256_text(str(self.subject))[:8]}"   # what the old code computed
        (forged / old_name).mkdir()
        (forged / old_name / commun.JETON_FILE).write_text("faux\n", encoding="utf-8")
        state = self.etat()
        state["pilote_sha256"] = commun.sha256_text("faux")   # the reference was in the state; it is not read there any more
        commun.sauver_etat(self.subject, state)
        with mock.patch.dict(os.environ, {"IX_SCELLE_DIR": str(forged)}):
            err = self.refused("suite", "tours_goal_max", "relancer", "9")
            self.assertIn("n'est pas celui de ce sujet", err)
        self.assertEqual(self.etat()["suites"], [])
        self.assertEqual(self.garde()["extra"]["goal"], 0)
        self.assertIn("plafond", self.refused("tour"))   # `tour` still stops at the real ceiling

    def test_a_complete_fake_sealed_place_is_not_the_one_the_hooks_declare(self):
        """The fake carries an index, a guard and a token that agree with each other: the pilot's commands still refuse, because the
        hooks declared at the freeze point at the real sealed place."""
        self.reach_the_ceiling()
        forged = self.fake_root()
        key = str(self.subject.resolve())
        (forged / "index.json").write_text(json.dumps({key: "aa"}), encoding="utf-8")
        (forged / "aa").mkdir()
        (forged / "aa" / commun.JETON_FILE).write_text("faux\n", encoding="utf-8")
        (forged / "aa" / "garde.json").write_text(json.dumps({"pilote_sha256": commun.sha256_text("faux")}), encoding="utf-8")
        with mock.patch.dict(os.environ, {"IX_SCELLE_DIR": str(forged)}):
            err = self.refused("suite", "tours_goal_max", "relancer", "9")
        self.assertIn("hooks du gel", err)
        self.assertEqual(self.etat()["suites"], [])

    def test_the_refusal_holds_for_any_form_of_call(self):
        """A string match cannot see these; the tool refuses them all, with the variable absent or forged."""
        self.reach_the_ceiling()
        forged = self.fake_root()
        script = REPO / "harnais" / "harnais.py"
        copie = self.tmp / "copie"   # a whole copy of the tool, under another name and another place
        (copie / "harnais").mkdir(parents=True)
        for source in (REPO / "harnais").glob("*.py"):
            shutil.copy(source, copie / "harnais" / ("h.py" if source.name == "harnais.py" else source.name))
        shutil.copy(REPO / "harnais" / "points-d-entree.env", copie / "harnais" / "points-d-entree.env")
        for name in ("scripts", "docs"):
            (copie / name).symlink_to(REPO / name)
        suite = "['suite','tours_goal_max','relancer','9']"
        forms = [
            ["python3", str(script), "suite", "tours_goal_max", "relancer", "9"],
            ["sh", "-c", f'V=su; python3 "{REPO}/harnais/./harnais.py" "$V"ite tours_goal_max relancer 9'],
            ["python3", "-c", f"import sys; sys.path.insert(0, '{REPO}/harnais'); import harnais; sys.exit(harnais.main({suite}))"],
            ["python3", "-c", f"import runpy, sys; sys.argv=['x', 'suite', 'tours_goal_max', 'relancer', '9']; runpy.run_path('{script}', run_name='__main__')"],
            ["python3", "-c", f"import sys; sys.path.insert(0, '{copie}/harnais'); import h; sys.exit(h.main({suite}))"],
        ]
        for place in (None, str(forged)):
            env = {k: v for k, v in os.environ.items() if k != "IX_SCELLE_DIR"}
            if place:
                env["IX_SCELLE_DIR"] = place
            for form in forms:
                with self.subTest(place=place, form=form[-1][:60]):
                    done = subprocess.run(form, capture_output=True, text=True, cwd=self.subject, env=env)
                    self.assertNotEqual(done.returncode, 0, done.stdout + done.stderr)
                    self.assertIn("commande du pilote", done.stderr)
        self.assertEqual(self.etat()["suites"], [])
        self.assertEqual(self.etat()["extra"]["tours_goal"], 0)
        self.assertEqual(self.garde()["extra"]["goal"], 0)

    def test_a_copy_of_the_tool_without_its_own_guard_changes_nothing_the_hooks_apply(self):
        """The refusal does not rest on the form of the call, nor on the check inside the script: the copy below has the check
        removed, and without the sealed place it has nothing to write to."""
        self.reach_the_ceiling()
        code = ("import sys, pathlib; sys.path.insert(0, %r); import commun, harnais; "
                "commun.exiger_pilote = lambda sujet, commande: pathlib.Path(%r); sys.exit(harnais.main(['suite','tours_goal_max','relancer','9']))"
                % (str(REPO / "harnais"), str(self.tmp / "nulle-part")))
        done = subprocess.run(["python3", "-c", code], capture_output=True, text=True, cwd=self.subject, env=self.prod_env())
        self.assertNotEqual(done.returncode, 0, done.stdout)
        self.assertEqual(self.garde()["extra"]["goal"], 0)
        self.assertTrue(self.hook_denies(self.event("Write", file_path=str(self.subject / "notes.md"))))   # the ceiling still holds

    def test_the_pilot_holding_the_seal_chooses_a_suite_by_the_same_forms(self):
        self.reach_the_ceiling()
        script = REPO / "harnais" / "harnais.py"
        done = subprocess.run(["python3", str(script), "suite", "tours_goal_max", "relancer", "2"], capture_output=True, text=True,
                              cwd=self.subject, env=dict(os.environ))
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.etat()["extra"]["tours_goal"], 2)
        self.assertEqual(self.garde()["extra"]["goal"], 2)

    def test_a_suite_or_extra_turns_written_into_the_state_by_other_hands_are_refused_and_change_no_ceiling(self):
        self.reach_the_ceiling()
        etat = self.etat()
        etat["suites"].append({"cle": "tours_goal", "suite": "relancer", "n": 50, "texte": None, "par": "Amiel", "at": "x", "t": "x",
                               "atteint_id": "tours_goal:1", "apres_gel": 0, "utilise": False})
        etat["extra"]["tours_goal"] = 50
        commun.sauver_etat(self.subject, etat)
        for argv in (("suite", "tours_goal_max", "relancer", "1"), ("empreintes",), ("juge",), ("regeler",), ("ouvrir",)):
            with self.subTest(command=argv[0]):
                err = self.refused(*argv)
                self.assertIn("ne correspond pas à ce que le pilote a scellé", err)
        self.assertEqual(self.garde()["extra"]["goal"], 0)   # the ceiling the hooks apply did not move
        self.assertTrue(self.hook_denies(self.event("Write", file_path=str(self.subject / "notes.md"))))

    def test_the_reference_of_the_token_is_in_the_guard_alone(self):
        self.launch()
        token = (self.scelle() / commun.JETON_FILE).read_text(encoding="utf-8").strip()
        reference = commun.sha256_text(token)
        self.assertEqual(self.grep(self.subject, token), [])
        self.assertEqual(self.grep(self.subject, reference), [])   # not in the state, nor in any file of the subject
        self.assertNotIn("pilote_sha256", self.etat())
        self.assertEqual(self.garde()["pilote_sha256"], reference)

    def test_the_rewritten_state_and_fingerprint_file_are_seen_by_tour_by_the_pilots_commands_and_by_the_hooks(self):
        self.freeze()
        self.goal()
        (self.subject / "grille.md").write_text("# Grille\n\nR1 changé.\n", encoding="utf-8")
        empreintes = self.subject / ".harnais" / "empreintes.sha256"
        empreintes.write_text("\n".join(f"{commun.sha256_file(self.subject / f)}  {f}" for f in self.etat()["gel"]["fichiers"]) + "\n",
                              encoding="utf-8")
        etat = self.etat()
        etat["gel"]["empreintes_sha256"] = commun.sha256_file(empreintes)
        commun.sauver_etat(self.subject, etat)
        for argv in (("tour",), ("empreintes",), ("juge",)):
            with self.subTest(command=argv[0]):
                err = self.refused(*argv)
                self.assertTrue("copie du scellé" in err or "écart d'état" in err, err)
        out = self.fire("Stop")
        self.assertIn('"continue": false', out.stdout)
        self.assertIn("copie du scellé", out.stdout)
        self.assertEqual(self.garde()["tours"]["goal"], 1)   # the end of that turn was counted all the same
        self.assertTrue(self.hook_denies(self.event("Write", file_path=str(self.subject / "notes.md"))))

    def event(self, tool, **tool_input):
        return {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": tool_input, "cwd": str(self.subject)}

    def hook_denies(self, event):
        with mock.patch.dict(os.environ, self.prod_env(), clear=True):
            try:
                hook.decider(event)
            except hook.Refus:
                return True
        return False


class CounterHookTests(HarnaisTestCase):
    """O5: the ceiling is counted by the hooks of Claude Code, at each end of turn, whatever the production runs; the state, which the
    production can write, is only a display of the guard."""

    def setUp(self):
        super().setUp()
        self.freeze()
        (self.subject / "goal.md").write_text(GOAL, encoding="utf-8")

    def limit(self):
        return self.etat()["reglages"]["plafonds"]["tours_goal_max"]

    def denies(self, tool="Write", **tool_input):
        tool_input = tool_input or {"file_path": str(self.subject / "notes.md")}
        event = {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": tool_input, "cwd": str(self.subject)}
        with mock.patch.dict(os.environ, self.prod_env(), clear=True):
            try:
                hook.decider(event)
            except hook.Refus as refus:
                return str(refus)
        return None

    def prompt(self):
        done = self.fire("UserPromptSubmit")
        self.assertEqual(done.returncode, 0, done.stderr)
        return json.loads(done.stdout) if done.stdout.strip() else {}

    def test_the_declared_hooks_are_the_manifest_ones_and_the_others_point_at_the_sealed_place(self):
        settings = json.loads((self.subject / ".claude" / "settings.json").read_text(encoding="utf-8"))
        self.assertEqual(settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"], commun.manifeste()["CMD_HOOK"])
        for event, name in (("Stop", "hook-stop"), ("UserPromptSubmit", "hook-prompt")):
            command = settings["hooks"][event][0]["hooks"][0]["command"]
            self.assertIn(name, command)
            self.assertIn(f'--garde "{commun.coder_pointeur(self.scelle())}"', command)
            self.assertNotIn(str(self.scelle()), command)   # the place is not written in the clear
        self.assertEqual(commun.pointeur_declare(self.subject), self.scelle())

    def test_every_end_of_turn_is_counted_without_the_production_running_anything(self):
        for n in range(1, 4):
            out = self.stop_turn()
            self.assertEqual(out["systemMessage"], f"Tour {n} sur {self.limit()} (production).")
        self.assertEqual(self.garde()["tours"]["goal"], 3)
        self.assertEqual(self.etat()["tours"]["goal"], 0)   # the state is a display: it follows at the pilot's next command
        self.ok("trace")
        self.assertEqual(self.etat()["tours"]["goal"], 3)
        self.assertIn("tour 3", [r["occurrence"] for r in self.tables()["T3"]])

    def test_at_the_ceiling_the_loop_stops_the_next_turn_cannot_start_and_no_tool_runs(self):
        for _ in range(self.limit() - 1):
            self.assertNotIn("continue", self.stop_turn())
        self.assertIsNone(self.denies())
        self.assertEqual(self.prompt(), {})
        last = self.stop_turn()
        self.assertIs(last["continue"], False)
        self.assertIn(f"plafond tours_goal_max atteint ({self.limit()} tour(s)", last["stopReason"])
        for suite in ("relancer", "contourner", "livrer_avec_reserve", "abandonner"):
            self.assertNotIn(suite, last["stopReason"])   # the production is never offered a suite (P3)
        self.assertEqual(self.prompt()["decision"], "block")
        self.assertIn("plafond", self.prompt()["reason"])
        self.assertIn("la main revient au pilote", self.denies() or "")
        self.assertIn("la main revient au pilote", self.denies("Read", file_path=str(self.subject / "grille.md")) or "")
        # the production calling the pilot's tool changes nothing: no turn is left to it
        self.assertEqual(self.garde()["tours"]["goal"], self.limit())

    def test_a_suite_that_adds_turns_lifts_the_ceiling_by_exactly_those_turns(self):
        for _ in range(self.limit()):
            self.stop_turn()
        self.ok("suite", "tours_goal", "relancer", "2")
        self.assertIsNone(self.denies())
        self.assertEqual(self.prompt(), {})
        self.assertNotIn("continue", self.stop_turn())
        self.assertIs(self.stop_turn()["continue"], False)
        self.assertEqual(self.garde()["tours"]["goal"], self.limit() + 2)
        self.assertIsNotNone(self.denies())

    def test_the_other_suites_keep_the_hooks_closed(self):
        for _ in range(self.limit()):
            self.stop_turn()
        self.ok("suite", "tours_goal", "abandonner")
        self.assertIn("abandonné", self.denies() or "")
        self.assertEqual(self.prompt()["decision"], "block")

    def test_a_counter_reset_in_the_guard_alone_is_seen_before_the_next_tool_and_the_next_turn(self):
        for _ in range(5):
            self.stop_turn()
        guard_file = self.scelle() / garde.GARDE_FILE
        data = json.loads(guard_file.read_text(encoding="utf-8"))
        data["tours"]["goal"] = 0
        guard_file.write_text(json.dumps(data), encoding="utf-8")   # a naive edit: the head no longer matches
        self.assertIn("écart de compteur", self.denies() or "")
        self.assertEqual(self.prompt()["decision"], "block")
        self.assertIs(self.stop_turn()["continue"], False)
        self.assertIn("écart de compteur", self.refused("tour"))
        self.assertIn("écart de compteur", self.refused("empreintes"))

    def test_a_guard_rewritten_in_step_but_not_its_witness_is_seen(self):
        for _ in range(5):
            self.stop_turn()
        data = self.garde()
        data["tours"]["goal"] = 0
        data["seq"] -= 1
        data["tete"] = garde.tete_de(data)   # the head recomputed: a careful forger
        (self.scelle() / garde.GARDE_FILE).write_text(json.dumps(data), encoding="utf-8")
        self.assertIn("témoin", self.denies() or "")
        self.assertIs(self.stop_turn()["continue"], False)

    def test_a_witness_rewritten_alone_or_removed_is_seen(self):
        for _ in range(5):
            self.stop_turn()
        witness = self.subject / ".harnais" / garde.TEMOIN_FILE
        data = json.loads(witness.read_text(encoding="utf-8"))
        data["seq"] = 1
        witness.write_text(json.dumps(data), encoding="utf-8")
        self.assertIn("témoin", self.denies() or "")
        witness.unlink()
        self.assertIn("a disparu", self.denies() or "")
        self.assertEqual(self.prompt()["decision"], "block")

    def test_the_one_residual_a_guard_and_its_witness_rewritten_together_by_a_form_the_hook_does_not_know(self):
        """Written down on purpose: nothing in the harness sees this. A process of the same user that finds the guard and rewrites it and its
        witness in one gesture, by a form no pattern of the hook recognises, resets the counter (architecture §8)."""
        for _ in range(5):
            self.stop_turn()
        data = self.garde()
        data["tours"]["goal"] = 0
        data["journal"] = []
        garde.sauver(self.scelle(), self.subject, data)   # the same writer the hooks use, here called directly
        self.assertIsNone(self.denies())
        self.assertEqual(self.prompt(), {})

    def test_a_counter_reset_in_the_state_is_overwritten_and_a_raised_one_is_refused(self):
        for _ in range(3):
            self.stop_turn()
        state = self.etat()
        state["tours"]["goal"] = 0
        commun.sauver_etat(self.subject, state)
        self.ok("trace")
        self.assertEqual(self.etat()["tours"]["goal"], 3)   # the guard overwrote it
        state = self.etat()
        state["tours"]["goal"] = 39
        commun.sauver_etat(self.subject, state)
        self.assertIn("écart de compteur", self.refused("tour"))
        self.assertIn("écart de compteur", self.refused("trace"))

    def test_the_pilot_can_still_count_a_turn_and_a_double_count_only_brings_the_ceiling_nearer(self):
        self.ok("tour")
        self.stop_turn()
        self.assertEqual(self.garde()["tours"]["goal"], 2)

    def test_a_changed_frozen_file_stops_the_loop_and_closes_the_tools_until_it_is_restored(self):
        original = (self.subject / "grille.md").read_text(encoding="utf-8")
        (self.subject / "grille.md").write_text("critère affaibli\n", encoding="utf-8")
        self.assertIn("grille.md", self.denies() or "")
        self.assertIn("grille.md", self.prompt()["reason"])
        out = self.stop_turn()
        self.assertIs(out["continue"], False)
        self.assertIn("grille.md", out["stopReason"])
        (self.subject / "grille.md").write_text(original, encoding="utf-8")
        self.assertIsNone(self.denies())
        self.assertEqual(self.prompt(), {})

    def test_an_unfilled_slot_of_the_goal_refuses_the_turn_start(self):
        (self.subject / "goal.md").write_text("# Goal\n\nRun `<ACCEPTANCE_SCRIPT>`.\n", encoding="utf-8")
        self.assertIn("<ACCEPTANCE_SCRIPT>", self.prompt()["reason"])

    def test_after_the_judgement_the_hooks_count_the_corrections_apart(self):
        self.deliverable()
        self.ok("fin-production")
        self.fake_judge("| exigence | part | verdict | preuve |\n|---|---|---|---|\n| V1 | visible | échec | non |\n")
        self.ok("juge")
        self.assertEqual(self.garde()["phase"], "correction")
        self.stop_turn()
        self.assertEqual(self.garde()["tours"], {"goal": 0, "correction": 1})
        limit = self.etat()["reglages"]["plafonds"]["tours_correction_max"]
        for _ in range(limit - 1):
            self.stop_turn()
        self.assertIsNotNone(self.denies())
        self.assertIn("tours_correction_max", self.prompt()["reason"])

    def test_the_freeze_opening_again_gives_back_the_turns(self):
        for _ in range(self.limit()):
            self.stop_turn()
        self.ok("suite", "tours_goal", "contourner", "R3 est ambigu")
        (self.subject / "grille.md").write_text("# Grille\n\nR1 précisée.\n", encoding="utf-8")
        self.ok("regeler")
        self.assertEqual(self.garde()["tours"], {"goal": 0, "correction": 0})
        self.assertIsNone(self.denies())
        self.assertNotIn("continue", self.stop_turn())

    def test_nothing_is_counted_before_the_freeze_and_after_the_opening(self):
        self.assertEqual(self.garde()["phase"], "goal")
        shutil.rmtree(self.seal)
        self.seal.mkdir()
        for name in ("parcours", "trace.md", ".claude", ".harnais"):
            p = self.subject / name
            shutil.rmtree(p, ignore_errors=True) if p.is_dir() else p.unlink(missing_ok=True)
        self.launch()
        self.assertEqual(self.garde()["phase"], "avant-gel")
        guard = self.garde()
        self.assertIsNone(garde.compte_actif(guard))


class SealClosedTests(HarnaisTestCase):
    """O11: the sealed place is shut to the production by its path, not by the form of a call: Read, Glob, Grep and the shell forms."""

    def setUp(self):
        super().setUp()
        self.freeze()
        self.sealed = self.scelle()
        self.hidden = next(self.sealed.rglob("*.part_cachee.md"), None) or (self.sealed / commun.JETON_FILE)
        self.env = self.prod_env()
        self.env["TMPDIR"] = str(self.tmp)
        self.env["HOME"] = str(self.tmp)

    def decide(self, tool, **tool_input):
        event = {"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": tool_input, "cwd": str(self.subject)}
        with mock.patch.dict(os.environ, self.env, clear=True):
            try:
                hook.decider(event)
            except hook.Refus as refus:
                return str(refus)
        return None

    def test_read_glob_and_grep_cannot_open_list_or_search_the_sealed_place(self):
        for name, args in [("Read file", ("Read", {"file_path": str(self.hidden)})),
                           ("Read token", ("Read", {"file_path": str(self.sealed / commun.JETON_FILE)})),
                           ("Read index", ("Read", {"file_path": str(self.seal / "index.json")})),
                           ("Glob inside", ("Glob", {"path": str(self.sealed), "pattern": "*"})),
                           ("Glob parent", ("Glob", {"path": str(self.tmp), "pattern": "**/jeton"})),
                           ("Glob absolute wildcards", ("Glob", {"pattern": f"{self.tmp}/s*/*/{commun.JETON_FILE}"})),
                           ("Glob absolute star", ("Glob", {"pattern": f"{self.seal}/*"})),
                           ("Grep inside", ("Grep", {"pattern": "x", "path": str(self.sealed)})),
                           ("Grep parent", ("Grep", {"pattern": "x", "path": str(self.tmp)})),
                           ("Grep root", ("Grep", {"pattern": "x", "path": "/"})),
                           ("Grep glob", ("Grep", {"pattern": "x", "path": str(self.tmp), "glob": "seal/**"})),
                           ("Write", ("Write", {"file_path": str(self.sealed / "garde.json")}))]:
            with self.subTest(name):
                self.assertIsNotNone(self.decide(args[0], **args[1]), name)

    def test_the_legitimate_reads_of_the_production_pass(self):
        for tool, args in [("Read", {"file_path": str(self.subject / "grille.md")}),
                           ("Glob", {"path": str(self.subject), "pattern": "**/*.md"}),
                           ("Glob", {"pattern": "fixtures/*.txt"}),
                           ("Grep", {"pattern": "R1", "path": str(self.subject)}),
                           ("Grep", {"pattern": "R1"}),
                           ("Read", {"file_path": str(REPO / "harnais" / "harnais.py")})]:
            with self.subTest(tool=tool, args=args):
                self.assertIsNone(self.decide(tool, **args))

    def test_the_settings_that_hold_the_pointer_are_not_read(self):
        for tool, args in [("Read", {"file_path": str(self.subject / ".claude" / "settings.json")}),
                           ("Read", {"file_path": ".claude/settings.local.json"}),
                           ("Glob", {"pattern": ".claude/*.json"}),
                           ("Glob", {"pattern": "**/settings.json"}),
                           ("Grep", {"pattern": "garde", "path": str(self.subject), "glob": ".claude/settings.json"})]:
            with self.subTest(tool=tool, args=args):
                self.assertIsNotNone(self.decide(tool, **args))

    def test_the_shell_forms_that_find_list_or_read_the_sealed_place_are_refused(self):
        sealed = str(self.sealed)
        for command in ['find "$TMPDIR" -name jeton', "find / -name jeton", f"find {self.tmp} -type f -exec cat {{}} +", "find ~ -name garde.json",
                        'grep -r CANARI "$TMPDIR"', "grep -rl x /", "grep -R x ~", 'rg -l x "$TMPDIR"', "rg x /", "fd jeton /", "ag x ~",
                        'ls -R "$TMPDIR"', 'ls "$TMPDIR"/seal', f"ls {sealed}", f"cat {sealed}/jeton", 'cat "$TMPDIR"/seal/*/jeton',
                        "cat /" + "/".join(Path(self.seal).parts[1:-2] + ("t*", "s*")) + "/*/jeton", "cat $TMPDIR/s*/*/garde.json", 'du -a "$TMPDIR"', 'tar czf /tmp/x.tgz "$TMPDIR"',
                        'cp -r "$TMPDIR" /tmp/x', 'rsync -a "$TMPDIR"/ /tmp/y/', "tree ~", "mdfind -name jeton", "locate jeton",
                        f"cd {self.seal} && ls", f"sh -c 'find / -name jeton'", f"echo $(find / -name jeton)", f"bash -c \"cat {sealed}/jeton\"",
                        "X=1 find ~ -name jeton", "time find / -name jeton", "find $UNKNOWN_DIR -name jeton", "cat .claude/settings.json",
                        "cat .cla*/set*", "grep garde .claude/settings.local.json", f"cat {self.subject}/.claude/settings.json",
                        "echo $IX_SCELLE_DIR", "printenv"]:
            with self.subTest(command=command):
                self.assertIsNotNone(self.decide("Bash", command=command), command)

    def test_the_shell_forms_a_production_legitimately_uses_pass(self):
        for command in ["find . -name '*.py'", "find fixtures livrable -type f", "grep -rn R1 .", "grep -n R1 grille.md", "ls -la", "ls fixtures",
                        "rg R1 livrable", "cat grille.md", f"cat {self.subject}/grille.md", "du -sh livrable", "tar czf /dev/null livrable",
                        "python3 -m unittest", "sh acceptation.sh .", "cd livrable && ls -R", "echo $HOME",
                        f"find {self.subject} -name '*.md'", "grep -r R1 fixtures", "git status", "tree livrable", 'ls "$HOME"']:
            with self.subTest(command=command):
                self.assertIsNone(self.decide("Bash", command=command), command)

    def test_the_name_of_the_place_is_drawn_at_random_and_written_nowhere_the_production_reads(self):
        name = self.sealed.name
        self.assertRegex(name, r"^[0-9a-f]{32}$")
        slug = commun.P.slugify(self.subject.name)
        self.assertNotIn(slug, name)
        self.assertNotEqual(name, f"{slug}-{commun.sha256_text(str(self.subject))[:8]}")   # not what the old code computed from the path
        for read in (REPO / "harnais", REPO / "docs"):
            self.assertEqual(self.grep(read, name), [], read)
        self.assertEqual(self.grep(self.subject, name), [])   # the pointer in the settings is hexadecimal, not the place in the clear
        self.assertEqual(self.grep(self.subject, str(self.seal)), [])
        state = json.loads((self.subject / "parcours" / "amont" / "state.json").read_text(encoding="utf-8"))
        self.assertNotIn("seal_key", state)
        # two subjects, two names; the same subject keeps its own
        other = self.tmp / "autre-sujet"
        other.mkdir()
        self.assertNotEqual(commun.P.seal_dir(self.seal, other).name, name)
        self.assertEqual(commun.P.seal_dir(self.seal, self.subject).name, name)

    def test_no_file_of_the_harness_suggests_a_default_place(self):
        for folder in (REPO / "docs" / "harnais", REPO / "harnais"):
            self.assertEqual(self.grep(folder, ".ix-scelles"), [], folder)
        text = (REPO / "docs" / "harnais" / "A7-guide-usage.md").read_text(encoding="utf-8")
        self.assertNotRegex(text, r"~/\.[a-z-]*scelle|export IX_SCELLE_DIR=~|IX_SCELLE_DIR=\$HOME")

    def test_the_hook_files_cannot_be_read_back_through_the_error_messages(self):
        message = self.decide("Read", file_path=str(self.hidden)) or ""
        self.assertNotIn(self.sealed.name, message)
        self.assertNotIn(str(self.seal), message)


class ManifestTests(unittest.TestCase):
    PATHS = ["A3", "A4", "A5", "A6_ARCHI", "A6_SPEC", "A7_GUIDE", "A7_TRACE", "A8", "SPEC", "ARCHI", "HOOKS_FICHIER", "MODELE_VERDICT"]
    VALUES = ["RECETTE", "TRACE", "ETAPE_EVAL_CADRAGE", "ETAPE_CADRAGE", "ETAPE_CLOTURE", "ETAPE_VERIF_LIVRABLES", "ETAPE_GOAL",
              "ETAPE_VERIF_GOAL", "ETAPE_CRITERES", "ETAPE_CONTRE_VERIF", "CHAMP_VERDICT", "VERDICT_OK", "VERDICT_REPRENDRE", "CHAMP_CACHE"]
    COMMANDS = ["CMD_LANCER", "CMD_TRACE", "CMD_SUITE", "CMD_CONTRE_VERIF", "CMD_GELER", "CMD_SCEAU", "CMD_EMPREINTES", "CMD_TOUR",
                "CMD_TOUR_CORRECTION", "CMD_REGELER", "CMD_FIN_PRODUCTION", "CMD_JUGE", "CMD_OUVRIR", "CMD_HOOK"]

    def setUp(self):
        self.values = commun.manifeste()

    def test_the_manifest_has_exactly_the_forty_keys(self):
        self.assertEqual(sorted(self.values), sorted(self.PATHS + self.VALUES + self.COMMANDS))
        self.assertEqual((len(self.PATHS), len(self.VALUES), len(self.COMMANDS)), (12, 14, 14))

    def test_every_path_exists_and_the_recipe_is_in_skills(self):
        for key in self.PATHS:
            with self.subTest(key=key):
                self.assertTrue((REPO / self.values[key]).is_file(), self.values[key])
        self.assertTrue((REPO / "skills" / f"{self.values['RECETTE']}.md").is_file())

    def test_the_step_ids_are_the_recipe_steps_and_the_verdict_values_are_the_runner_ones(self):
        recipe = parcours.load_recipe(self.values["RECETTE"])
        ids = [s["id"] for s in recipe["steps"]]
        for key in self.VALUES:
            if key.startswith("ETAPE_"):
                self.assertIn(self.values[key], ids, key)
        self.assertEqual((self.values["VERDICT_OK"], self.values["VERDICT_REPRENDRE"]), (parcours.VERDICT_OK, parcours.VERDICT_REPRENDRE))
        steps = {s["id"]: s for s in recipe["steps"]}
        self.assertEqual(steps[self.values["ETAPE_CRITERES"]]["hidden"], [self.values["CHAMP_CACHE"]])
        self.assertTrue(all(steps[self.values[k]]["verdict_field"] == self.values["CHAMP_VERDICT"]
                            for k in ("ETAPE_EVAL_CADRAGE", "ETAPE_VERIF_LIVRABLES", "ETAPE_VERIF_GOAL", "ETAPE_CONTRE_VERIF")))
        self.assertTrue(steps[self.values["ETAPE_CONTRE_VERIF"]]["external"])

    def test_the_order_of_the_steps_follows_the_procedure(self):
        ids = [s["id"] for s in parcours.load_recipe(self.values["RECETTE"])["steps"]]
        order = [self.values[k] for k in ("ETAPE_CADRAGE", "ETAPE_EVAL_CADRAGE", "ETAPE_CLOTURE", "ETAPE_VERIF_LIVRABLES", "ETAPE_GOAL",
                                          "ETAPE_VERIF_GOAL", "ETAPE_CRITERES", "ETAPE_CONTRE_VERIF")]
        self.assertEqual([ids.index(i) for i in order], sorted(ids.index(i) for i in order))

    def test_the_goal_never_receives_the_criteria_nor_the_criteria_the_goal(self):
        recipe = parcours.load_recipe(self.values["RECETTE"])
        steps = {s["id"]: s for s in recipe["steps"]}
        self.assertFalse([r for r in steps[self.values["ETAPE_GOAL"]]["receives"] + steps[self.values["ETAPE_VERIF_GOAL"]]["receives"]
                          if r.startswith(self.values["ETAPE_CRITERES"] + ".")])
        self.assertFalse([r for r in steps[self.values["ETAPE_CRITERES"]]["receives"] if r.startswith(self.values["ETAPE_GOAL"] + ".")])

    def test_no_step_of_the_recipe_has_the_fable_model_and_every_model_is_the_one_of_its_role(self):
        settings = parcours.load_reglages()[0]
        for step in parcours.load_recipe(self.values["RECETTE"])["steps"]:
            if step["external"]:
                continue
            self.assertNotEqual(step["model"], "fable")
            self.assertEqual(step["model"], settings["modeles"][step["role"]], step["id"])

    def test_the_migrated_pieces_are_the_originals(self):
        pilote = Path("/Users/amiellavon/Projets/ix-pilote/partie-a")
        if not pilote.is_dir():
            self.skipTest("ix-pilote is not next to this repository")
        for key, name in (("A3", "A3-format-trace.md"), ("A4", "A4-reglages.yaml"), ("A5", "A5-grille-cadrage.md"),
                          ("A6_ARCHI", "A6-architecture.md"), ("A6_SPEC", "A6-spec.md")):
            with self.subTest(piece=name):
                self.assertEqual((REPO / self.values[key]).read_bytes(), (pilote / name).read_bytes())


if __name__ == "__main__":
    unittest.main()
