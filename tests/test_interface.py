"""
Tests of scripts/interface.py (the local tracking page of docs/interface.md).

Run:  cd ~/Projets/ix-recipes && python3 -m unittest tests.test_interface -v

No real engine is ever called: the server runs in a thread on a free port, over a
temporary parcours folder, and drives scripts/parcours.py (a copy placed in a temporary
repo layout with stub skills) with the `fake` engine, as test_parcours.py does. The
copy of parcours.py only differs by a test hook that makes the fake engine sleep when
PARCOURS_TEST_SLEEP is set (to have a `next` that runs long enough to be stopped).

The Markdown renderer lives in interface.html and cannot be tested from Python; one
optional test runs it under node when node is installed (skipped otherwise).
"""

import http.client
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "tests"))

import interface  # noqa: E402
import test_parcours as tp  # noqa: E402


def wait_for(condition, timeout=20, step=0.05):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        value = condition()
        if value:
            return value
        time.sleep(step)
    raise AssertionError("condition not met in time")


class InterfaceTestCase(tp.ParcoursTestCase):
    """The server on a free port over the temporary layout of ParcoursTestCase."""

    def setUp(self):
        super().setUp()
        scripts = self.root / "scripts"
        scripts.mkdir()
        source = (REPO / "scripts" / "parcours.py").read_text(encoding="utf-8")
        hook = '    time.sleep(float(os.environ.get("PARCOURS_TEST_SLEEP", "0")))\n    canned = fixtures /'
        self.assertIn("    canned = fixtures /", source)
        source = source.replace("    canned = fixtures /", hook, 1).replace("import tempfile\n", "import tempfile\nimport time\n", 1)
        (scripts / "parcours.py").write_text(source, encoding="utf-8")
        for target, value in (("PARCOURS_SCRIPT", scripts / "parcours.py"), ("QUICK_WAIT", 0.5), ("STOP_GRACE", 8)):
            patcher = mock.patch.object(interface, target, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.write_fakes("brief-client")
        self.start_server()

    def start_server(self, dev=True):
        self.server = interface.make_server(self.pdir, 0, dev=dev)
        self.port = self.server.server_address[1]
        self.token = self.server.app.token
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(self.stop_server, self.server, thread)

    @staticmethod
    def stop_server(server, thread):
        for proc in list(server.app.launches.values()):
            if proc.poll() is None:
                proc.kill()
        server.shutdown()
        server.server_close()
        thread.join(5)

    # -- HTTP -------------------------------------------------------------
    def request(self, method, path, body=None, token=True, host=None, content_type="application/json",
                raw=None, extra=None):
        """(status, headers, parsed body) — JSON when the answer is JSON, text otherwise."""
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=90)
        try:
            conn.putrequest(method, path, skip_host=True, skip_accept_encoding=True)
            conn.putheader("Host", host if host is not None else f"127.0.0.1:{self.port}")
            if token is True:
                conn.putheader(interface.TOKEN_HEADER, self.token)
            elif token:
                conn.putheader(interface.TOKEN_HEADER, token)
            data = raw if raw is not None else (json.dumps(body).encode("utf-8") if body is not None else None)
            if method == "POST":
                if content_type:
                    conn.putheader("Content-Type", content_type)
                conn.putheader("Content-Length", str(len(data or b"")))
            for key, value in (extra or {}).items():
                conn.putheader(key, value)
            conn.endheaders(data if method == "POST" else None)
            response = conn.getresponse()
            payload = response.read().decode("utf-8")
            headers = {k.lower(): v for k, v in response.getheaders()}
            if "json" in headers.get("content-type", "") and payload:
                payload = json.loads(payload)
            return response.status, headers, payload
        finally:
            conn.close()

    def get(self, path, **kw):
        return self.request("GET", path, **kw)

    def post(self, path, body=None, **kw):
        return self.request("POST", path, body if body is not None else {}, **kw)

    def api(self, method, path, body=None, expect=200):
        status, _, data = self.request(method, path, body)
        self.assertEqual(status, expect, f"{method} {path} -> {status} {data}")
        return data

    # -- driving a parcours through the API ---------------------------------
    def status_of(self, slug="demo"):
        return self.api("GET", f"/api/parcours/{slug}")

    def idle_status(self, slug="demo"):
        """Status once nothing runs any more (running state comes from the lock)."""
        return wait_for(lambda: (lambda s: s if not s["locked"] else None)(self.status_of(slug)))

    def run_next(self, slug="demo", **extra):
        plan = self.api("GET", f"/api/parcours/{slug}/plan")
        self.assertTrue(plan["runnable"], plan)
        answer = self.api("POST", f"/api/parcours/{slug}/next", {"fingerprint": plan["fingerprint"], **extra})
        self.assertTrue(answer["started"])
        return self.idle_status(slug)


# ---------------------------------------------------------------------------
# Access control
# ---------------------------------------------------------------------------
class AccessTests(InterfaceTestCase):
    def test_every_api_route_needs_the_token_reads_included(self):
        self.new()
        for path in ("/api/parcours", "/api/parcours/demo", "/api/parcours/demo/plan",
                     "/api/parcours/demo/log", "/api/parcours/demo/file/state.json"):
            for token in (False, "wrong-token", self.token[:-1], self.token + "x"):
                status, _, data = self.get(path, token=token)
                self.assertEqual(status, 403, f"{path} {token!r}")
                self.assertEqual(data["error"], "bad_token")

    def test_posts_need_the_token_too(self):
        self.new()
        for action in ("next", "stop", "validate", "answer", "choose", "retry", "rerun"):
            for token in (False, "wrong-token"):
                status, _, _ = self.post(f"/api/parcours/demo/{action}", token=token)
                self.assertEqual(status, 403, action)
        self.assertEqual(self.step("cadrage")["status"], "pending")

    def test_the_token_is_a_0600_file_and_survives_a_restart(self):
        path = self.pdir / interface.TOKEN_FILE
        self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o600)
        self.assertEqual(path.read_text(encoding="utf-8").strip(), self.token)
        self.assertGreaterEqual(len(self.token), 32)
        again = interface.App(self.pdir)
        self.assertEqual(again.token, self.token)

    def test_a_bad_host_is_refused_everywhere(self):
        self.new()
        for host in ("evil.example", f"evil.example:{self.port}", "127.0.0.1", "127.0.0.1:1", f"127.0.0.1.evil.example:{self.port}", ""):
            for path in ("/", "/api/parcours"):
                status, _, _ = self.get(path, host=host)
                self.assertEqual(status, 403, f"{path} Host={host!r}")
        status, _, _ = self.get("/api/parcours", host=f"localhost:{self.port}")
        self.assertEqual(status, 200)

    def test_a_foreign_origin_is_refused(self):
        status, _, _ = self.get("/api/parcours", extra={"Origin": "http://evil.example"})
        self.assertEqual(status, 403)
        status, _, _ = self.get("/api/parcours", extra={"Origin": f"http://127.0.0.1:{self.port}"})
        self.assertEqual(status, 200)

    def test_options_and_other_methods_are_refused_and_no_cors_header_is_sent(self):
        for method in ("OPTIONS", "PUT", "DELETE", "HEAD", "PATCH"):
            status, headers, _ = self.request(method, "/api/parcours")
            self.assertEqual(status, 405, method)
            self.assertFalse([h for h in headers if h.startswith("access-control")], method)
        status, headers, _ = self.get("/api/parcours")
        self.assertEqual(status, 200)
        self.assertFalse([h for h in headers if h.startswith("access-control")])

    def test_a_post_must_be_json(self):
        self.new()
        for content_type in ("text/plain", "application/x-www-form-urlencoded", "multipart/form-data", None):
            status, _, data = self.post("/api/parcours/demo/retry", content_type=content_type)
            self.assertEqual(status, 415, content_type)
        status, _, _ = self.post("/api/parcours/demo/choose", raw=b"not json", content_type="application/json")
        self.assertEqual(status, 400)
        status, _, _ = self.post("/api/parcours/demo/choose", raw=b"[1]", content_type="application/json")
        self.assertEqual(status, 400)
        status, _, _ = self.post("/api/parcours/demo/retry", raw=b"{}", content_type="application/json; charset=utf-8")
        self.assertEqual(status, 422)  # accepted as JSON; the runner finds nothing to retry
        with mock.patch.object(interface, "MAX_BODY", 100):
            status, _, _ = self.post("/api/parcours/demo/answer", raw=b'{"text": "' + b"x" * 500 + b'"}', content_type="application/json")
        self.assertEqual(status, 413)

    def test_the_page_carries_a_csp_with_a_fresh_nonce_and_no_external_url(self):
        status, headers, html = self.get("/", token=False)
        self.assertEqual(status, 200)
        csp = headers["content-security-policy"]
        self.assertIn("default-src 'none'", csp)
        self.assertIn("connect-src 'self'", csp)
        nonce = re.search(r"script-src 'nonce-([0-9a-f]+)'", csp).group(1)
        self.assertIn(f"style-src 'nonce-{nonce}'", csp)
        self.assertEqual(headers["referrer-policy"], "no-referrer")
        self.assertIn(f'<script nonce="{nonce}">', html)
        self.assertIn(f'<style nonce="{nonce}">', html)
        self.assertNotIn("{{NONCE}}", html)
        _, headers2, _ = self.get("/", token=False)
        self.assertNotEqual(headers2["content-security-policy"], csp)
        code = html.replace("var SVG_NS = 'http://www.w3.org/2000/svg';", "")   # an XML namespace name, never fetched
        self.assertIsNone(re.search(r"(?i)https?://|\bsrc\s*=|<link\b|@import|\bwss?://", code))
        self.assertIsNone(re.search(r"\bon[a-z]+\s*=\s*[\"']", html), "inline event handler (blocked by the CSP anyway)")
        self.assertIsNone(re.search(r"<[^>]+\bstyle\s*=", html), "inline style attribute (blocked by the CSP)")
        self.assertEqual(html.count("</script"), 1, "a stray closing tag inside the script would cut it short")
        self.assertEqual(html.count("innerHTML"), 2)  # its comment + the single use, in mdBox()
        self.assertIn("box.innerHTML = safeRender(text);", html)

    def test_unknown_routes_and_wrong_methods(self):
        self.new()
        self.assertEqual(self.get("/nope", token=False)[0], 404)
        self.assertEqual(self.get("/api/nope")[0], 404)
        self.assertEqual(self.get("/api/parcours/demo/next")[0], 405)       # an action is a POST
        self.assertEqual(self.post("/api/recipes")[0], 405)
        self.assertEqual(self.post("/api/parcours/demo/plan")[0], 405)
        self.assertEqual(self.post("/api/parcours/demo/frobnicate")[0], 404)
        self.assertEqual(self.post("/")[0], 405)


# ---------------------------------------------------------------------------
# Names, paths, whitelists
# ---------------------------------------------------------------------------
class PathTests(InterfaceTestCase):
    def test_bad_slugs_are_refused(self):
        self.new()
        for slug in ("-x", "--help", "../demo", "..", ".hidden", "Demo", "a%2Fb", "a%2fb", "demo%00", "d" * 90, "x%20y", "%2e%2e"):
            for path in (f"/api/parcours/{slug}", f"/api/parcours/{slug}/plan", f"/api/parcours/{slug}/log",
                         f"/api/parcours/{slug}/file/state.json"):
                status, _, _ = self.get(path)
                self.assertIn(status, (400, 404), path)
            self.assertIn(self.post(f"/api/parcours/{slug}/retry")[0], (400, 404), slug)
        self.assertEqual(self.get("/api/parcours/nope")[0], 404)

    def test_bad_step_names_and_engines_are_refused(self):
        self.new()
        self.write_fakes("brief-client")
        self.run_next()
        self.api("POST", "/api/parcours/demo/validate", {})
        self.run_next()  # questioning, pause answers
        self.api("POST", "/api/parcours/demo/answer", {"none": True})
        for step in ("-x", "--help", "../x", "a,b", "Cadrage", "", None, 3, ["explorer"]):
            self.assertEqual(self.post("/api/parcours/demo/rerun", {"step": step})[0], 400, step)
        for run in (["-x"], [], "explorer", ["explorer", "-rf"], [1]):
            self.assertEqual(self.post("/api/parcours/demo/choose", {"run": run})[0], 400, run)
        for engine in ("--yes", "bogus", "Claude", 3):
            status, _, _ = self.post("/api/parcours/demo/next", {"fingerprint": "0" * 64, "engine": engine})
            self.assertEqual(status, 400, engine)
            self.assertEqual(self.get("/api/parcours/demo/plan?engine=" + str(engine))[0], 400, engine)

    def test_the_fake_engine_exists_only_with_dev(self):
        self.new()
        self.assertEqual(self.get("/api/parcours/demo/plan?engine=fake")[0], 200)
        self.assertIn("fake", self.get("/api/parcours")[2]["engines"])
        self.server.app.dev = False
        self.assertEqual(self.get("/api/parcours/demo/plan?engine=fake")[0], 400)
        self.assertNotIn("fake", self.get("/api/parcours")[2]["engines"])
        self.assertEqual(self.post("/api/parcours/demo/next", {"fingerprint": "0" * 64, "engine": "fake"})[0], 400)

    def test_file_names_are_checked_and_stay_inside_the_folder(self):
        self.new()
        self.write_fakes("brief-client")
        self.run_next()
        bad = ("../state.json", "%2e%2e%2fstate.json", "..%2f..%2fetc%2fpasswd", ".lock", ".next.log", ".next.pid", "x.lock",
               "x.tmp", "-rf", "STATE.JSON", "a" * 90 + ".md", "state.json%00.md", "..", ".", "sub/state.json", "inexistant.md")
        for name in bad:
            status, _, _ = self.get(f"/api/parcours/demo/file/{name}")
            self.assertIn(status, (400, 404), name)
        status, _, data = self.get("/api/parcours/demo/file/01-cadrage.md")
        self.assertEqual(status, 200)
        self.assertIn("VALUE[cadrage.need]", data["text"])
        self.assertEqual(self.get("/api/parcours/demo/file/01-cadrage.in.md")[0], 200)
        # the token file lives beside the parcours, not inside one
        self.assertEqual(self.get(f"/api/parcours/demo/file/{interface.TOKEN_FILE}")[0], 400)

    def test_symlinks_cannot_lead_out_of_the_parcours_folder(self):
        self.new()
        self.write_fakes("brief-client")
        self.run_next()
        secret = self.tmp / "secret.md"
        secret.write_text("outside", encoding="utf-8")
        (self.pdir / "demo" / "leak.md").symlink_to(secret)
        self.assertEqual(self.get("/api/parcours/demo/file/leak.md")[0], 404)
        outside = self.tmp / "elsewhere"
        outside.mkdir()
        shutil.copy(self.pdir / "demo" / "state.json", outside / "state.json")
        (self.pdir / "linked").symlink_to(outside)
        self.assertEqual(self.get("/api/parcours/linked")[0], 404)
        self.assertNotIn("linked", [p["slug"] for p in self.get("/api/parcours")[2]["parcours"]])


# ---------------------------------------------------------------------------
# Reads
# ---------------------------------------------------------------------------
class ReadTests(InterfaceTestCase):
    def test_list(self):
        self.new()
        self.new("reponse-appel-offres", "rao")
        (self.pdir / "interrupted").mkdir()          # no state.json: creation interrupted
        (self.pdir / "BadName").mkdir()               # not a slug: ignored
        (self.pdir / "broken").mkdir()
        (self.pdir / "broken" / "state.json").write_text("{not json", encoding="utf-8")
        data = self.api("GET", "/api/parcours")
        self.assertEqual(sorted(p["slug"] for p in data["parcours"]), ["demo", "rao"])
        self.assertEqual(data["without_state"], ["interrupted"])
        self.assertEqual([b["slug"] for b in data["broken"]], ["broken"])
        self.assertEqual(data["parcours_dir"], str(self.pdir.resolve()))
        demo = next(p for p in data["parcours"] if p["slug"] == "demo")
        self.assertEqual((demo["recipe"], demo["status"], demo["locked"], demo["steps_done"], demo["steps_total"]),
                         ("brief-client", "active", False, 0, 5))
        self.assertIsNone(demo["pending"])
        self.write_fakes("brief-client")
        self.run_next()
        demo = next(p for p in self.api("GET", "/api/parcours")["parcours"] if p["slug"] == "demo")
        self.assertEqual(demo["pending"]["type"], "validate")
        self.assertEqual(demo["calls"], {"fake": 1})

    def test_status_plan_and_log(self):
        self.new()
        status = self.status_of()
        self.assertEqual(status["slug"], "demo")
        self.assertFalse(status["locked"])
        self.assertEqual(status["engines"], ["claude", "codex", "agy", "vibe", "fake"])
        self.assertEqual(status["parcours_dir"], str(self.pdir.resolve()))
        self.assertEqual([s["id"] for s in status["steps"]], ["cadrage", "questioning", "explorer", "decision", "brief"])
        plan = self.api("GET", "/api/parcours/demo/plan?engine=claude")
        self.assertTrue(plan["runnable"])
        self.assertEqual((plan["ceiling_usd"], plan["claude_steps"], plan["changes_default_engine"]), (10.0, 1, True))
        self.assertEqual(plan["fingerprint"], status["fingerprint"])
        self.assertEqual(self.state()["engine"], "fake")  # a plan changes nothing
        self.assertEqual(self.api("GET", "/api/parcours/demo/log")["exists"], False)

    def test_reading_writes_nothing(self):
        self.new()
        before = sorted((p.name, p.read_bytes()) for p in (self.pdir / "demo").iterdir())
        for path in ("/api/parcours", "/api/parcours/demo", "/api/parcours/demo/plan", "/api/parcours/demo/log",
                     "/api/parcours/demo/file/input.md"):
            self.api("GET", path)
        self.assertEqual(sorted((p.name, p.read_bytes()) for p in (self.pdir / "demo").iterdir()), before)


class CreateAndReadTests(InterfaceTestCase):
    def test_recipes_and_creation_from_the_page(self):
        recipes = self.api("GET", "/api/recipes")["recipes"]
        self.assertEqual([r["id"] for r in recipes], ["brief-client", "reponse-appel-offres"])
        created = self.api("POST", "/api/parcours", {"recipe": "brief-client", "title": "Offre formation",
                                                     "text": "Une demande\nsur deux lignes.", "engine": "fake"})
        self.assertEqual(created["slug"], "offre-formation")
        self.assertEqual((self.pdir / "offre-formation" / "input.md").read_text(encoding="utf-8"), "Une demande\nsur deux lignes.")
        status = self.status_of("offre-formation")
        self.assertEqual((status["title"], status["recipe_label"], status["engine"]), ("Offre formation", "Brief client", "fake"))
        listed = next(p for p in self.api("GET", "/api/parcours")["parcours"] if p["slug"] == "offre-formation")
        self.assertEqual((listed["title"], listed["recipe_label"]), ("Offre formation", "Brief client"))
        self.assertEqual(listed["current"], {"id": "cadrage", "label": "Cadrage de la demande", "status": "pending"})
        dashed = self.api("POST", "/api/parcours", {"recipe": "brief-client", "title": "--engine claude", "text": "x"})
        self.assertEqual((dashed["slug"], dashed["title"]), ("engine-claude", "--engine claude"))
        untitled = self.api("POST", "/api/parcours", {"recipe": "brief-client", "text": "autre demande"})
        self.assertTrue(untitled["slug"].startswith("brief-client"))
        self.assertIsNone(untitled["title"])

    def test_a_lone_surrogate_is_a_clean_refusal(self):
        status, _, data = self.request("POST", "/api/parcours", None, raw=b'{"recipe": "brief-client", "text": "\\ud800"}')
        self.assertEqual((status, data["error"]), (400, "bad_json"))

    def test_creation_refusals(self):
        for body, status in (({"recipe": "inconnue", "text": "x"}, 404), ({"recipe": "../x", "text": "x"}, 400),
                             ({"recipe": "brief-client", "text": "  "}, 400), ({"recipe": "brief-client", "text": "x", "title": "t" * 121}, 400),
                             ({"recipe": "brief-client", "text": "x", "engine": "rm"}, 400), ({"recipe": "brief-client", "text": 3}, 400)):
            self.assertEqual(self.request("POST", "/api/parcours", body)[0], status, body)
        self.assertEqual(sorted(p.name for p in self.pdir.iterdir() if not p.name.startswith(".")), [])

    def test_document_of_a_step(self):
        self.new()
        self.run_next()
        doc = self.api("GET", "/api/parcours/demo/document/01-cadrage.md")
        self.assertEqual(doc["document"], "Complete analysis written by step cadrage.")
        self.assertNotIn("HANDOFF", doc["document"])
        self.assertEqual(self.request("GET", "/api/parcours/demo/document/..%2Fstate.json")[0], 400)
        self.assertEqual(self.request("GET", "/api/parcours/demo/document/absent.md")[0], 404)


class ManyDossiersTests(InterfaceTestCase):
    def test_archive_from_the_page_and_restore(self):
        self.new()
        self.new(slug="autre")
        self.api("POST", "/api/parcours/demo/archive", {})
        listed = self.api("GET", "/api/parcours")
        self.assertEqual(([p["slug"] for p in listed["parcours"]], listed["archived"]), (["autre"], 1))
        self.assertEqual([a["slug"] for a in self.api("GET", "/api/archives")["archives"]], ["demo"])
        self.assertEqual(self.api("POST", "/api/archives/demo/restore", {})["restored"], "demo")
        self.assertEqual(self.api("GET", "/api/parcours")["archived"], 0)
        self.assertEqual(self.request("POST", "/api/archives/..%2Fx/restore", {})[0], 400)

    def test_the_list_cache_follows_every_change(self):
        self.new()
        first = self.api("GET", "/api/parcours")["parcours"][0]
        self.assertEqual(first["steps_done"], 0)
        self.run_next()
        again = self.api("GET", "/api/parcours")["parcours"][0]
        self.assertEqual((again["pending"]["type"], again["calls"]), ("validate", {"fake": 1}))


class ThemeTests(InterfaceTestCase):
    def themed(self):
        theme = self.tmp / "theme"
        theme.mkdir()
        (theme / "theme.css").write_text(":root { --primary: #295294; } /* </style><script>x</script> */", encoding="utf-8")
        (theme / "Font.ttf").write_bytes(b"\x00\x01fake font")
        (self.tmp / "secret.ttf").write_bytes(b"outside")
        server = interface.make_server(self.pdir, 0, dev=True, theme=theme)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)
        return server.server_address[1]

    def test_a_theme_adds_its_styles_and_serves_its_fonts(self):
        port = self.themed()
        self.port = port
        status, headers, html = self.get("/", token=False)
        self.assertEqual(status, 200)
        self.assertIn("--primary: #295294", html)
        theme_block = html[html.index("--primary: #295294"):]
        self.assertNotIn("</", theme_block[:theme_block.index("</style>")])   # the theme cannot close its style element
        self.assertEqual(html.count("</style>"), 2)
        self.assertIn("font-src 'self'", headers["content-security-policy"])
        status, headers, body = self.get("/theme/Font.ttf", token=False)
        self.assertEqual((status, headers["content-type"]), (200, "font/ttf"))
        for bad in ("/theme/..%2Fsecret.ttf", "/theme/theme.css", "/theme/absent.ttf", "/theme/.hidden.ttf"):
            self.assertEqual(self.get(bad, token=False)[0], 404, bad)

    def test_without_a_theme_nothing_changes(self):
        status, headers, html = self.get("/", token=False)
        self.assertNotIn("{{THEME}}", html)
        self.assertNotIn("font-src", headers["content-security-policy"])
        self.assertEqual(self.get("/theme/Font.ttf", token=False)[0], 404)

    def test_the_inflexion_theme_is_the_default_and_none_is_neutral(self):
        self.assertTrue((interface.theme_folder("inflexion") / "theme.css").is_file())
        self.assertIsNone(interface.theme_folder("none"))
        self.assertEqual(interface.theme_folder("~/x"), Path.home() / "x")
        bundled = REPO / "dist" / "skills" / "suivi-parcours" / "scripts" / "themes" / "inflexion"
        for name in ("theme.css", "Archivo.ttf", "SourceSans3.ttf", "OFL-Archivo.txt"):
            self.assertTrue((bundled / name).is_file(), name)

    def test_a_theme_folder_needs_its_stylesheet(self):
        with self.assertRaises(OSError):
            interface.make_server(self.pdir, 0, theme=self.tmp)


class UnknownRecipeTests(InterfaceTestCase):
    """The page knows no recipe: everything it shows comes from the recipe file."""

    RECIPE = """---
id: recette-inventee
label: "Recette inventée"
version: 0.1.0
summary_fr: "Une phrase écrite pour un humain."
description_fr: "Déclenche sur des mots-clés qu'un humain n'a pas à lire."
description_en: "Invented."
icon: "*"
domain: ops
category: production
input_types: [brief]
output_types: [markdown]
compatible: [claude-ai, claude-code, cowork, gpt, gemini, mystaffy]
requires: [ix-skills:cadrage, ix-skills:deliver]
workflow:
  context_sheet: [mandant, enjeu_principal, horizon]
  context_labels:
    mandant: "Commanditaire"
    enjeu_principal: "Enjeu principal"
  steps:
    - id: lecture-initiale
      label: "Lecture initiale"
      skill: ix-skills:cadrage
      mission: Read it.
      receives: [brief]
      transmits: [points]
      produces_context_sheet: true
      pause: validate
    - id: livrable
      skill: ix-skills:deliver
      mission: Write it.
      receives: [context_sheet, lecture-initiale.points]
      transmits: [texte]
      output_field: texte
      pause: none
---

# Role

Orchestrates `ix-skills:cadrage` then `ix-skills:deliver`.
"""

    def test_an_unknown_recipe_is_listed_created_and_read_like_the_others(self):
        (self.root / "skills" / "recette-inventee.md").write_text(self.RECIPE, encoding="utf-8")
        listed = next(r for r in self.api("GET", "/api/recipes")["recipes"] if r["id"] == "recette-inventee")
        self.assertEqual((listed["label"], listed["summary"]), ("Recette inventée", "Une phrase écrite pour un humain."))
        self.assertEqual([s["label"] for s in listed["steps"]], ["Lecture initiale", None])
        recipe = tp.parcours.load_recipe("recette-inventee")
        self.write_fakes("recette-inventee")
        (self.fake / "lecture-initiale.md").write_text(tp.fake_output(recipe["steps"][0], recipe["context_sheet"]).replace(
            '"CTX-horizon"', '"not stated"'), encoding="utf-8")
        slug = self.api("POST", "/api/parcours", {"recipe": "recette-inventee", "text": "une demande", "engine": "fake"})["slug"]
        self.run_next(slug)
        status = self.status_of(slug)
        self.assertEqual(status["recipe_label"], "Recette inventée")
        self.assertEqual(status["context_labels"], {"mandant": "Commanditaire", "enjeu_principal": "Enjeu principal"})
        self.assertEqual(status["not_stated"], "not stated")
        self.assertEqual(status["context_sheet"]["horizon"], "not stated")
        self.assertEqual(status["pending"]["type"], "validate")
        self.api("POST", f"/api/parcours/{slug}/validate", {})
        status = self.run_next(slug)
        self.assertEqual(status["status"], "completed")
        doc = self.api("GET", f"/api/parcours/{slug}/document/{status['final_output']}")
        self.assertIn("Complete analysis written by step livrable.", doc["document"])
        self.assertNotIn("HANDOFF", doc["document"])


# ---------------------------------------------------------------------------
# A whole brief-client run, through the API only
# ---------------------------------------------------------------------------
class FullRunTests(InterfaceTestCase):
    def test_brief_client_from_start_to_completion(self):
        self.new()
        base = "/api/parcours/demo"

        # step 1 (cadrage): the plan carries a fingerprint, next is launched with it
        status = self.run_next()
        self.assertEqual(status["pending"]["type"], "validate")
        self.assertEqual(status["steps"][0]["status"], "paused")
        self.assertEqual(status["context_sheet"]["client"], "CTX-client")
        self.assertFalse(status["context_validated"])
        self.assertIn("Context sheet", self.api("GET", f"{base}/file/00-context.md")["text"])
        self.assertIn("exists", self.api("GET", f"{base}/log"))

        # the sheet is corrected while validating
        sheet = dict(status["context_sheet"], client="Dupuis Menuiserie SA")
        answer = self.api("POST", f"{base}/validate", {"context": sheet})
        self.assertTrue(answer["ok"])
        self.assertIsNone(answer["notice"])  # nothing had received the old sheet yet
        status = self.status_of()
        self.assertTrue(status["context_validated"])
        self.assertEqual(status["context_sheet"]["client"], "Dupuis Menuiserie SA")
        self.assertIn("00-context.v1.md", status["files"])
        self.assertIsNone(status["pending"])

        # step 2 (questioning): pause answers
        status = self.run_next()
        self.assertEqual(status["pending"]["type"], "answers")
        self.assertIn("Dupuis Menuiserie SA", self.received("questioning"))
        self.assertEqual(self.post(f"{base}/answer", {"text": "  "})[0], 400)
        self.assertEqual(self.post(f"{base}/validate", {})[0], 422)           # wrong kind of pause
        self.api("POST", f"{base}/answer", {"text": tp.ANSWERS_TEXT})
        self.assertIn("ANSWERS-FROM-CLIENT", self.api("GET", f"{base}/file/answers.md")["text"])

        # branch point: skip the optional steps
        status = self.status_of()
        self.assertEqual(status["pending"]["type"], "choose")
        self.assertEqual(status["pending"]["steps"], ["explorer", "decision"])
        self.api("POST", f"{base}/choose", {"skip": True})

        # last step, and the parcours completes
        status = self.run_next()
        self.assertEqual(status["status"], "completed")
        self.assertEqual(status["final_output"], "05-brief.md")
        self.assertEqual([s["status"] for s in status["steps"]], ["done", "done", "skipped", "skipped", "done"])
        self.assertFalse(self.was_called("explorer"))
        self.assertFalse(self.was_called("decision"))
        self.assertEqual(status["calls"], {"fake": 3})
        self.assertIn("VALUE[brief.final_brief]", self.api("GET", f"{base}/file/05-brief.md")["text"])
        self.assertFalse(self.get(f"{base}/plan")[2]["runnable"])
        self.assertEqual(self.get(f"{base}/plan")[2]["reason"], "completed")

    def test_the_optional_steps_a_stale_sheet_notice_and_a_rerun_notice(self):
        self.new()
        base = "/api/parcours/demo"
        self.run_next()
        self.api("POST", f"{base}/validate", {})
        self.run_next()
        self.api("POST", f"{base}/answer", {"none": True})
        self.api("POST", f"{base}/choose", {"run": ["explorer", "decision"]})
        status = self.run_next()
        self.assertEqual(status["pending"], {"type": "validate", "step": "decision", "message": status["pending"]["message"]})
        sheet = dict(status["context_sheet"], objective="Nouvel objectif")
        notice = self.api("POST", f"{base}/validate", {"context": sheet})["notice"]
        self.assertEqual(notice["kind"], "context_stale")
        self.assertEqual(notice["steps"], ["questioning", "explorer", "decision"])
        self.assertEqual(self.post(f"{base}/validate", {"context": sheet, "stop": True})[0], 400)
        self.assertEqual(self.post(f"{base}/validate", {"context": ["no"]})[0], 400)
        status = self.run_next()
        self.assertEqual(status["pending"]["step"], "decision") if status["pending"] else None
        notice = self.api("POST", f"{base}/rerun", {"step": "questioning"})["notice"]
        self.assertEqual(notice["kind"], "rerun")
        self.assertEqual(notice["steps"][0], "questioning")
        self.assertIn("explorer", notice["steps"])
        status = self.status_of()
        self.assertEqual(status["steps"][1]["status"], "pending")
        self.assertIn("01-cadrage.md", status["files"])

    def test_a_no_go_stops_the_parcours(self):
        self.new()
        self.run_next()
        self.api("POST", "/api/parcours/demo/validate", {"stop": True})
        status = self.status_of()
        self.assertEqual(status["status"], "stopped")
        plan = self.api("GET", "/api/parcours/demo/plan")
        self.assertEqual((plan["runnable"], plan["reason"]), (False, "stopped"))

    def test_a_failed_step_is_reported_and_retried(self):
        self.write_fakes("brief-client", cadrage="no handoff\n", cadrage__retry="none either\n")
        self.new()
        plan = self.api("GET", "/api/parcours/demo/plan")
        # the step fails within the first seconds: the refusal is reported at once, with the runner's message
        status, _, data = self.post("/api/parcours/demo/next", {"fingerprint": plan["fingerprint"]})
        self.assertEqual((status, data["error"]), (422, "parse"))
        status = self.idle_status()
        self.assertEqual(status["steps"][0]["status"], "failed")
        self.assertIn("extraction impossible", status["steps"][0]["error"])
        plan = self.api("GET", "/api/parcours/demo/plan")
        self.assertEqual((plan["runnable"], plan["reason"]), (False, "failed"))
        self.write_fakes("brief-client")
        self.api("POST", "/api/parcours/demo/retry")
        status = self.run_next()
        self.assertEqual(status["steps"][0]["status"], "paused")

    def test_a_fingerprint_that_no_longer_matches_runs_nothing(self):
        self.new()
        plan = self.api("GET", "/api/parcours/demo/plan")
        # the state moves between the plan and the confirmation
        (self.pdir / "demo" / "00-context.md").write_text("edited meanwhile\n", encoding="utf-8")
        status, _, data = self.post("/api/parcours/demo/next", {"fingerprint": plan["fingerprint"]})
        self.assertEqual(status, 409)
        self.assertEqual(data["error"], "state_changed")
        self.assertFalse(self.was_called("cadrage"))
        self.assertEqual(self.step("cadrage")["status"], "pending")
        for body in ({}, {"fingerprint": "abc"}, {"fingerprint": 5}, {"fingerprint": "G" * 64}):
            self.assertEqual(self.post("/api/parcours/demo/next", body)[0], 400, body)
        # a fresh plan works
        self.assertEqual(self.run_next()["steps"][0]["status"], "paused")

    def test_the_engine_chosen_in_the_page_becomes_the_default(self):
        self.new()
        status = self.run_next(engine="fake")
        self.assertEqual(status["engine"], "fake")
        plan = self.api("GET", "/api/parcours/demo/plan?engine=codex")
        self.assertTrue(plan["changes_default_engine"])
        self.assertEqual(self.state()["engine"], "fake")


# ---------------------------------------------------------------------------
# Long calls, the lock, stopping
# ---------------------------------------------------------------------------
class RunningTests(InterfaceTestCase):
    def test_a_long_next_is_seen_through_the_lock_and_can_be_stopped(self):
        self.new()
        base = "/api/parcours/demo"
        with mock.patch.dict(os.environ, {"PARCOURS_TEST_SLEEP": "60"}):
            plan = self.api("GET", f"{base}/plan")
            started = self.api("POST", f"{base}/next", {"fingerprint": plan["fingerprint"]})
        self.assertTrue(started["started"])
        self.assertFalse(started["finished"])
        status = wait_for(lambda: (lambda s: s if s["locked"] else None)(self.status_of()))
        self.assertEqual(self.step("cadrage")["status"], "running")
        self.assertTrue(self.get("/api/parcours")[2]["parcours"][0]["locked"])
        # the lock, not the server's memory, says it runs: the runner itself refuses other commands
        status_code, _, data = self.post(f"{base}/validate", {})
        self.assertEqual((status_code, data["error"]), (409, "locked"))
        self.assertEqual(self.post(f"{base}/next", {"fingerprint": status["fingerprint"]})[0], 409)
        self.assertEqual(self.get(f"{base}/log")[2]["exists"], True)
        self.assertTrue((self.pdir / "demo" / ".next.pid").is_file())

        pid = int((self.pdir / "demo" / ".next.pid").read_text(encoding="utf-8"))
        stopped = self.api("POST", f"{base}/stop")
        self.assertTrue(stopped["stopped"])
        self.assertFalse(stopped["still_locked"])
        self.assertFalse(stopped["forced"])
        with self.assertRaises(OSError):
            os.kill(pid, 0)
        status = self.status_of()
        self.assertFalse(status["locked"])
        self.assertEqual(status["steps"][0]["status"], "running")  # left as is: `retry` takes it back
        self.assertEqual(self.post(f"{base}/stop")[0], 409)         # nothing runs any more

        self.api("POST", f"{base}/retry")
        status = self.run_next()
        self.assertEqual(status["steps"][0]["status"], "paused")

    def test_stop_refuses_a_lock_it_does_not_own(self):
        self.new()
        base = "/api/parcours/demo"
        import parcours as runner
        with runner.parcours_lock(self.pdir / "demo"):   # held by the test process, not launched by the page
            status, _, data = self.post(f"{base}/stop")
            self.assertEqual((status, data["error"]), (409, "not_owned"))
            (self.pdir / "demo" / ".next.pid").write_text(f"{os.getpid()}\n", encoding="utf-8")   # a live pid that is not a runner
            self.assertEqual(self.post(f"{base}/stop")[2]["error"], "not_owned")
            (self.pdir / "demo" / ".next.pid").write_text("999999\n", encoding="utf-8")
            self.assertEqual(self.post(f"{base}/stop")[2]["error"], "not_owned")
        self.assertEqual(os.kill(os.getpid(), 0), None)   # the test process is still here

    def test_the_log_is_written_by_a_detached_process(self):
        self.new()
        self.run_next()
        log = self.api("GET", "/api/parcours/demo/log")
        self.assertTrue(log["exists"])
        self.assertIn("cadrage", log["log"])
        proc_args = (self.pdir / "demo" / ".next.log").read_text(encoding="utf-8")
        self.assertIn("Plan :", proc_args)


# ---------------------------------------------------------------------------
# How the runner is called
# ---------------------------------------------------------------------------
class CommandLineTests(InterfaceTestCase):
    def capture(self, body):
        """argv of the runner call(s) made while `body` runs (subprocess.run is mocked)."""
        calls = []

        def fake_run(argv, **kwargs):
            calls.append(list(argv))
            return subprocess.CompletedProcess(argv, 0, stdout=json.dumps({"steps": [], "pending": None}), stderr="")

        with mock.patch.object(interface.subprocess, "run", fake_run):
            body()
        return calls

    def test_argv_lists_with_double_dash_and_absolute_directory(self):
        self.new()
        base = "/api/parcours/demo"
        cases = [
            (f"{base}/retry", {}, ["demo"]),
            (f"{base}/choose", {"run": ["explorer", "decision"]}, ["demo"]),
            (f"{base}/choose", {"skip": True}, ["demo"]),
            (f"{base}/answer", {"none": True}, ["demo"]),
            (f"{base}/validate", {"stop": True}, ["demo"]),
        ]
        for path, body, positionals in cases:
            calls = self.capture(lambda: self.post(path, body))
            self.assertEqual(len(calls), 1, path)
            argv = calls[0]
            self.assertEqual(argv[0], sys.executable)
            self.assertEqual(Path(argv[1]), interface.PARCOURS_SCRIPT)
            self.assertIn("--", argv)
            cut = argv.index("--")
            self.assertEqual(argv[cut + 1:], positionals, argv)
            options = argv[2:cut]
            self.assertIn("--json", options)
            self.assertTrue(Path(options[options.index("--parcours-dir") + 1]).is_absolute())
            self.assertEqual(options[options.index("--parcours-dir") + 1], str(self.pdir.resolve()))
        calls = self.capture(lambda: self.post(f"{base}/rerun", {"step": "cadrage"}))
        self.assertEqual(calls[1][calls[1].index("--") + 1:], ["demo", "cadrage"])   # status, rerun, status
        self.assertIn("rerun", calls[1])

    def test_values_travel_as_arguments_never_through_a_shell(self):
        self.new()
        with mock.patch.object(interface.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, stdout="{}", stderr="")
            self.post("/api/parcours/demo/choose", {"run": ["explorer", "decision"]})
        argv = run.call_args[0][0]
        self.assertIsInstance(argv, list)
        self.assertEqual(argv[argv.index("--run") + 1], "explorer,decision")
        self.assertNotIn("shell", run.call_args[1])

    def test_exit_codes_of_the_runner_are_interpreted(self):
        with self.assertRaises(interface.ApiError) as raised:
            interface.interpret(2, "", "usage: parcours.py ...\nerror: bad")
        self.assertEqual((raised.exception.status, raised.exception.code), (500, "interface_bug"))
        self.assertIn("bug de l'interface", raised.exception.message)
        with self.assertRaises(interface.ApiError) as raised:
            interface.interpret(1, 'Plan : …\n{"error": "locked", "message": "verrou pris"}\n', "")
        self.assertEqual((raised.exception.status, raised.exception.code, raised.exception.message), (409, "locked", "verrou pris"))
        with self.assertRaises(interface.ApiError) as raised:
            interface.interpret(1, '{"error": "leak", "message": "x"}', "")
        self.assertEqual(raised.exception.status, 422)
        with self.assertRaises(interface.ApiError) as raised:
            interface.interpret(1, "garbage", "")
        self.assertEqual(raised.exception.status, 500)
        with self.assertRaises(interface.ApiError) as raised:
            interface.interpret(-9, "", "")
        self.assertEqual(raised.exception.status, 500)
        interface.interpret(0, "", "")

    def test_an_argument_error_of_the_runner_is_a_500_with_a_clear_message(self):
        self.new()
        real = interface.App.argv

        def broken(self_, command, flags=(), positionals=()):
            return real(self_, command, ["--no-such-flag", *flags], positionals)

        with mock.patch.object(interface.App, "argv", broken):
            status, _, data = self.get("/api/parcours/demo")
        self.assertEqual(status, 500)
        self.assertEqual(data["error"], "interface_bug")
        self.assertIn("bug de l'interface", data["message"])


# ---------------------------------------------------------------------------
# The Markdown renderer of the page (optional: needs node)
# ---------------------------------------------------------------------------
@unittest.skipUnless(shutil.which("node"), "node is not installed")
class RendererTests(unittest.TestCase):
    def render(self, text):
        html = (REPO / "scripts" / "interface.html").read_text(encoding="utf-8")
        code = re.search(r"// <markdown-renderer>(.*?)// </markdown-renderer>", html, re.S).group(1)
        script = code + "\nprocess.stdout.write(renderMarkdown(JSON.parse(process.argv[1])));"
        done = subprocess.run(["node", "-e", script, json.dumps(text)], capture_output=True, text=True, timeout=30)
        self.assertEqual(done.returncode, 0, done.stderr)
        return done.stdout

    def test_every_special_character_is_escaped(self):
        self.assertEqual(self.render("<b>&\"'"), "<p>&lt;b&gt;&amp;&quot;&#39;</p>")

    ALLOWED = r"<(?!/?(p|br|h[2-6]|ul|ol|li|strong|em|del|code|pre|table|thead|tbody|tr|th|td|blockquote|hr|div|span|a)\b)"

    def test_no_raw_html_no_image_no_script_link(self):
        for hostile in ("<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "[x](javascript:alert(1))",
                        "[x](data:text/html,<script>)", "[x](https://a.b/\" onmouseover=\"alert(1))", "![y](http://evil/a.png)",
                        "```\n<script>x</script>\n```", "| <i> |\n|---|\n| <u> |", "# <h1>", "- <li>", "> <q>", "**<b>**",
                        "`<code>`", "<!-- x --><b>", "- [x] <i>", "~~<s>~~", "_<u>_"):
            html = self.render(hostile)
            self.assertIsNone(re.search(self.ALLOWED, html), html)
            for link in re.findall(r"<a [^>]*>", html):
                self.assertRegex(link, r'^<a href="https?://[^"<>]*" target="_blank" rel="noopener noreferrer">$')
            self.assertEqual(set(re.findall(r"<div[^>]*>", html)) - {'<div class="tbl">'}, set(), html)
            self.assertEqual(set(re.findall(r"<span[^>]*>", html)) - {'<span class="task">'}, set(), html)
            self.assertNotIn("<img", html)
            self.assertNotIn("<script", html)
            self.assertNotRegex(html, r"<[a-z0-9]+ [^>]*\son\w+=")

    def test_basic_structures(self):
        html = self.render("# Titre\n\n- a **b**\n  - c\n\n3. trois\n\n| x | y |\n|---|---|\n| 1 | 2 |\n\n```\ncode\n```\n")
        for expected in ("<h2>Titre</h2>", "<strong>b</strong>", "<ul>", '<ol start="3">', '<div class="tbl"><table>', "<th>x</th>",
                         "<td>2</td>", "<pre class=\"code\">"):
            self.assertIn(expected, html)

    def test_hostile_inputs_render_in_linear_time(self):
        html = (REPO / "scripts" / "interface.html").read_text(encoding="utf-8")
        code = re.search(r"// <markdown-renderer>(.*?)// </markdown-renderer>", html, re.S).group(1)
        script = code + """
var cases = ['[a](https://b'.repeat(50000), '<!--'.repeat(40000) + 'x', '[' .repeat(100000) + '](https://a',
             '*a'.repeat(50000), ('| a |\\n').repeat(20000)];
var worst = 0;
cases.forEach(function (c) { var t = Date.now(); renderMarkdown(c); worst = Math.max(worst, Date.now() - t); });
process.stdout.write(String(worst));"""
        done = subprocess.run(["node", "-e", script], capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertLess(int(done.stdout), 1500, "a hostile output freezes the page")

    def test_comments_and_size_limit(self):
        self.assertEqual(self.render("a <!-- x --> b"), "<p>a  b</p>")
        self.assertIn("&lt;!-- jamais fermé", self.render("<!-- jamais fermé"))
        self.assertTrue(self.render("x" * 300001).startswith('<pre class="raw">'))
        self.assertIn("&lt;!-- gardé --&gt;", self.render("```html\n<!-- gardé -->\n```\n<!-- ôté -->après"))
        self.assertNotIn("ôté", self.render("```html\n<!-- gardé -->\n```\n<!-- ôté -->après"))

    def test_document_niceties(self):
        html = self.render("**Destinataire :** X\n**Prestataire :** Y\n\n- [ ] à faire\n- [x] fait\n\n~~barré~~ et _penché_ "
                           "[lien](https://example.org/a?b=1&c=2)\n<!-- retry output -->")
        self.assertIn("<strong>Destinataire :</strong> X<br><strong>Prestataire :</strong> Y", html)
        self.assertIn('<span class="task">\u2610</span>à faire', html)
        self.assertIn("<del>barré</del>", html)
        self.assertIn("<em>penché</em>", html)
        self.assertIn('<a href="https://example.org/a?b=1&amp;c=2" target="_blank" rel="noopener noreferrer">lien</a>', html)
        self.assertNotIn("retry", html)
        self.assertNotIn("<em>", self.render("snake_case_name et mot_composé"))


if __name__ == "__main__":
    unittest.main()
