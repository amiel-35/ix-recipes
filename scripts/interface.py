#!/usr/bin/env python3
"""
interface.py — local tracking page for parcours (spec: docs/interface.md).

A small HTTP server (standard library only) bound to 127.0.0.1 that serves one HTML
page and a JSON API on top of the runner. Nothing is reimplemented here: every
action calls scripts/parcours.py in a subprocess (argv list, `--` before the
positionals, absolute --parcours-dir, --json), so the page does what the command
line does, with the same checks and the same state.json.

Usage:
    python3 scripts/interface.py [--parcours-dir ./parcours] [--port 8765] [--dev] [--no-browser]

Access control (see docs/interface.md §1): a random token kept in
<parcours-dir>/.interface-token (mode 0600, stable across restarts) goes in the
URL fragment (#t=...) and must come back in the X-Parcours-Token header on every
/api route, reads included; the Host header must be 127.0.0.1:<port> or
localhost:<port>; no OPTIONS, no CORS; POST bodies are JSON only.

`--dev` also offers the `fake` engine (canned outputs, PARCOURS_FAKE_DIR) in the page.
"""

import argparse
import contextlib
import hmac
import json
import os
import re
import secrets
import signal
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit

import parcours  # reads only: is_locked() (the probe of `status --json`), load_recipe() labels, output_document()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
HERE = Path(__file__).resolve().parent
PARCOURS_SCRIPT = HERE / "parcours.py"
PAGE = HERE / "interface.html"
DEFAULT_PORT = 8765
TOKEN_FILE = ".interface-token"
TOKEN_HEADER = "X-Parcours-Token"
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,79}$")          # slugs are made by slugify(): letters, digits, hyphens
STEP_RE = SLUG_RE                                            # step ids are kebab-case in the recipes
FILE_RE = re.compile(r"^[a-z0-9][a-z0-9.-]{0,79}$")          # no leading dot: neither .lock nor temporary files
TOKEN_RE = re.compile(r"^[A-Za-z0-9_-]{32,}$")
FINGERPRINT_RE = re.compile(r"^[0-9a-f]{64}$")
REAL_ENGINES = ("claude", "codex", "agy", "vibe")
ACTIONS = ("next", "stop", "validate", "answer", "choose", "retry", "rerun")
MAX_BODY = 4_000_000        # bytes of a POST body (a pasted answer can be long)
MAX_FILE = 2_000_000        # bytes of a file sent to the page
MAX_TITLE = 120             # characters of a parcours title
LOG_TAIL = 100_000          # bytes of .next.log sent to the page
QUICK_WAIT = 2.5            # seconds `next` is watched after launch, to report a refusal at once
SYNC_TIMEOUT = 120          # seconds for the commands that do not call an engine
STOP_GRACE = 15             # seconds between SIGTERM and SIGKILL when stopping a `next`


class ApiError(Exception):
    """An error answered as {"error": code, "message": ...} with an HTTP status."""

    def __init__(self, status, code, message):
        super().__init__(message)
        self.status, self.code, self.message = status, code, message


def valid_file_name(name):
    """A file name the page may ask for: lowercase, no leading dot, no lock or temporary file."""
    return bool(FILE_RE.match(name)) and not name.endswith((".lock", ".tmp"))


# ---------------------------------------------------------------------------
# Token
# ---------------------------------------------------------------------------
def load_or_create_token(directory):
    """The token kept in <directory>/.interface-token (0600); created on first use."""
    path = Path(directory) / TOKEN_FILE
    if path.is_file():
        token = path.read_text(encoding="utf-8").strip()
        if TOKEN_RE.match(token):
            with contextlib.suppress(OSError):
                os.chmod(path, 0o600)
            return token
    token = secrets.token_urlsafe(32)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(token + "\n")
    os.chmod(path, 0o600)
    return token


# ---------------------------------------------------------------------------
# Application: what the handlers do
# ---------------------------------------------------------------------------
class App:
    def __init__(self, parcours_dir, dev=False):
        self.dir = Path(parcours_dir).resolve()
        self.dir.mkdir(parents=True, exist_ok=True)
        self.dev = dev
        self.token = load_or_create_token(self.dir)
        self.launches = {}              # slug -> Popen of the `next` this server started
        self.slug_locks = {}            # slug -> threading.Lock (one launch at a time)
        self.registry = threading.Lock()

    # -- helpers ----------------------------------------------------------
    @property
    def engines(self):
        return list(REAL_ENGINES) + (["fake"] if self.dev else [])

    def slug_lock(self, slug):
        with self.registry:
            return self.slug_locks.setdefault(slug, threading.Lock())

    def parcours_dir(self, slug):
        """Folder of an existing parcours; the slug is checked, the folder must hold state.json."""
        if not SLUG_RE.match(slug):
            raise ApiError(400, "bad_slug", "identifiant de parcours invalide")
        directory = self.dir / slug
        if directory.is_symlink() or not (directory / "state.json").is_file():
            raise ApiError(404, "not_found", f"parcours introuvable : {slug}")
        if directory.resolve().parent != self.dir:
            raise ApiError(400, "bad_slug", "identifiant de parcours invalide")
        return directory

    def check_engine(self, engine):
        if engine not in self.engines:
            raise ApiError(400, "bad_engine", f"moteur non proposé : {engine!r}")
        return engine

    def argv(self, command, flags=(), positionals=()):
        """Command line of the runner: absolute --parcours-dir, --json, `--` before the positionals."""
        return [sys.executable, str(PARCOURS_SCRIPT), command, *flags,
                "--parcours-dir", str(self.dir), "--json", *(["--", *positionals] if positionals else [])]

    @staticmethod
    def child_env():
        return dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")

    def run(self, command, flags=(), positionals=(), timeout=SYNC_TIMEOUT, input_text=None):
        """Run the runner to completion; returns (stdout, stderr) or raises ApiError.

        `input_text` goes to the runner's stdin (`new --input -`), never through a file."""
        stdin = {"input": input_text} if input_text is not None else {"stdin": subprocess.DEVNULL}
        try:
            done = subprocess.run(
                self.argv(command, flags, positionals), capture_output=True, **stdin,
                text=True, encoding="utf-8", errors="replace", timeout=timeout, env=self.child_env())
        except subprocess.TimeoutExpired:
            raise ApiError(504, "timeout", f"parcours.py n'a pas répondu en {timeout} s")
        interpret(done.returncode, done.stdout, done.stderr)
        return done.stdout, done.stderr

    def run_json(self, command, flags=(), positionals=(), input_text=None):
        out, _ = self.run(command, flags, positionals, input_text=input_text)
        try:
            return json.loads(out)
        except ValueError:
            raise ApiError(500, "unreadable", "réponse illisible de parcours.py")

    # -- reads ------------------------------------------------------------
    @staticmethod
    def recipe_labels(recipe_id, cache):
        """(recipe label, {step id: label}) for the list page; the ids if the recipe is unreadable."""
        if recipe_id not in cache:
            try:
                recipe = parcours.load_recipe(recipe_id)
                cache[recipe_id] = (recipe["label"], {s["id"]: s["label"] for s in recipe["steps"]})
            except Exception:  # a broken recipe must not break the list
                cache[recipe_id] = (recipe_id, {})
        return cache[recipe_id]

    def list_parcours(self):
        items, without_state, broken, labels = [], [], [], {}
        for entry in sorted(self.dir.iterdir()):
            if not entry.is_dir() or entry.is_symlink() or not SLUG_RE.match(entry.name):
                continue
            state_file = entry / "state.json"
            if not state_file.is_file():
                without_state.append(entry.name)  # creation interrupted: listed apart, not an error
                continue
            try:
                state = json.loads(state_file.read_text(encoding="utf-8"))
                steps = state["steps"]
                pending = state.get("pending")
                recipe_label, step_labels = self.recipe_labels(state["recipe"], labels)
                current = next((s for s in steps if s["status"] in ("running", "failed", "paused")), None) \
                    or next((s for s in steps if s["status"] == "pending"), None)
                items.append({
                    "slug": entry.name, "title": state.get("title"), "recipe_label": recipe_label,
                    "updated": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(state_file.stat().st_mtime)),
                    "current": {"id": current["id"], "label": step_labels.get(current["id"]),
                                "status": current["status"]} if current else None,
                    "recipe": state["recipe"], "recipe_version": state.get("recipe_version"),
                    "status": state["status"], "engine": state.get("engine"), "created": state.get("created"),
                    "pending": {"type": pending["type"], "step": pending.get("step"), "steps": pending.get("steps")}
                    if pending else None,
                    "cost_usd": state.get("cost_usd", 0.0), "calls": state.get("calls", {}),
                    "steps_total": len(steps),
                    "steps_done": sum(1 for s in steps if s["status"] in ("done", "skipped")),
                    "locked": parcours.is_locked(entry),
                })
            except (OSError, ValueError, KeyError, TypeError) as exc:
                broken.append({"slug": entry.name, "message": f"state.json illisible : {exc}"})
        items.sort(key=lambda i: i.get("created") or "", reverse=True)
        return {"parcours": items, "without_state": without_state, "broken": broken,
                "engines": self.engines, "dev": self.dev, "parcours_dir": str(self.dir)}

    def status(self, slug):
        self.parcours_dir(slug)
        data = self.run_json("status", positionals=[slug])
        data.update(engines=self.engines, dev=self.dev, parcours_dir=str(self.dir))
        return data

    def plan(self, slug, engine=None):
        self.parcours_dir(slug)
        flags = ["--engine", self.check_engine(engine)] if engine else []
        return self.run_json("plan", flags, [slug])

    def read_file(self, slug, name):
        directory = self.parcours_dir(slug)
        if not valid_file_name(name):
            raise ApiError(400, "bad_file", "nom de fichier invalide")
        path = directory / name
        if path.is_symlink() or not path.is_file() or path.resolve().parent != directory.resolve():
            raise ApiError(404, "not_found", f"fichier introuvable : {name}")
        raw = path.read_bytes()[:MAX_FILE + 1]
        return {"name": name, "text": raw[:MAX_FILE].decode("utf-8", errors="replace"), "truncated": len(raw) > MAX_FILE}

    def read_document(self, slug, name):
        """A step output as a reader sees it: the document before its HANDOFF / SUMMARY blocks,
        without its front matter (returned apart as `meta`)."""
        data = self.read_file(slug, name)
        document, meta = parcours.output_document(data["text"])
        return {"name": name, "document": document, "meta": meta, "truncated": data["truncated"]}

    def recipes(self):
        return self.run_json("recipes")

    def create(self, body):
        recipe, text = body.get("recipe"), body.get("text")
        title, engine = body.get("title") or "", body.get("engine")
        if not isinstance(recipe, str) or not SLUG_RE.match(recipe):
            raise ApiError(400, "bad_request", "recette invalide")
        if recipe not in {r["id"] for r in self.recipes()["recipes"]}:
            raise ApiError(404, "not_found", f"recette introuvable : {recipe}")
        if not isinstance(text, str) or not text.strip():
            raise ApiError(400, "bad_request", "la demande est vide : collez le texte ou déposez un fichier")
        if not isinstance(title, str) or len(title) > MAX_TITLE:
            raise ApiError(400, "bad_request", f"titre invalide ({MAX_TITLE} caractères au plus)")
        flags = ["--input", "-"]
        if title.strip():
            flags += [f"--title={title.strip()}", f"--slug={title.strip()}"]   # `=`: a title starting with "-" stays a value
        if engine:
            flags += ["--engine", self.check_engine(engine)]
        return self.run_json("new", flags, [recipe], input_text=text)

    def read_log(self, slug):
        path = self.parcours_dir(slug) / ".next.log"
        if not path.is_file():
            return {"exists": False, "log": "", "truncated": False}
        size = path.stat().st_size
        with open(path, "rb") as handle:
            handle.seek(max(0, size - LOG_TAIL))
            raw = handle.read()
        return {"exists": True, "log": raw.decode("utf-8", errors="replace"), "truncated": size > LOG_TAIL}

    # -- actions ----------------------------------------------------------
    def act(self, slug, action, body):
        self.parcours_dir(slug)
        if action == "next":
            return self.action_next(slug, body)
        if action == "stop":
            return self.action_stop(slug)
        if action == "validate":
            return self.action_validate(slug, body)
        if action == "answer":
            return self.action_answer(slug, body)
        if action == "choose":
            return self.action_choose(slug, body)
        if action == "retry":
            return self.done(*self.run("retry", positionals=[slug]))
        if action == "rerun":
            return self.action_rerun(slug, body)
        raise ApiError(404, "not_found", f"action inconnue : {action}")

    @staticmethod
    def done(out, err, notice=None):
        return {"ok": True, "output": out.strip(), "warnings": err.strip(), "notice": notice}

    def action_next(self, slug, body):
        fingerprint = body.get("fingerprint")
        if not isinstance(fingerprint, str) or not FINGERPRINT_RE.match(fingerprint):
            raise ApiError(400, "bad_fingerprint", "empreinte du plan manquante ou invalide")
        flags = ["--yes", "--if-state", fingerprint]
        if body.get("engine"):
            flags += ["--engine", self.check_engine(body["engine"])]
        directory = self.dir / slug
        with self.slug_lock(slug):
            previous = self.launches.get(slug)
            if (previous and previous.poll() is None) or parcours.is_locked(directory):
                raise ApiError(409, "running", "une étape est déjà en cours sur ce parcours")
            # Detached on purpose: output goes to a file, never to a pipe owned by this server,
            # so stopping the server does not break a paid call. "Running" is read from the lock.
            with open(directory / ".next.log", "wb") as log:
                proc = subprocess.Popen(
                    self.argv("next", flags, [slug]), stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                    cwd=str(directory), env=self.child_env(), start_new_session=True)
            (directory / ".next.pid").write_text(f"{proc.pid}\n", encoding="utf-8")
            self.launches[slug] = proc
            threading.Thread(target=proc.wait, daemon=True).start()  # reaps the child
            try:
                code = proc.wait(timeout=QUICK_WAIT)
            except subprocess.TimeoutExpired:
                return {"ok": True, "started": True, "finished": False, "pid": proc.pid}
        if code != 0:  # a refusal (stale plan, lock...) shows up at once: report it as such
            log_text = (directory / ".next.log").read_text(encoding="utf-8", errors="replace")
            interpret(code, log_text, log_text[-300:])
        return {"ok": True, "started": True, "finished": True, "pid": proc.pid}

    def action_stop(self, slug):
        directory = self.dir / slug
        if not parcours.is_locked(directory):
            raise ApiError(409, "not_running", "aucune étape en cours sur ce parcours")
        pgid = self.owned_group(directory, slug)
        os.killpg(pgid, signal.SIGTERM)  # the runner turns it into an exit that also kills the engine call
        forced = False
        if not self.wait_unlocked(directory, STOP_GRACE):
            forced = True
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(pgid, signal.SIGKILL)
            self.wait_unlocked(directory, 3)
        return {"ok": True, "stopped": True, "forced": forced, "still_locked": parcours.is_locked(directory)}

    @staticmethod
    def wait_unlocked(directory, seconds):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            if not parcours.is_locked(directory):
                return True
            time.sleep(0.1)
        return not parcours.is_locked(directory)

    @staticmethod
    def owned_group(directory, slug):
        """Process group of the `next` this interface started, checked before anything is killed.

        The lock is held (checked by the caller); the pid file must name a live process that leads
        its own group and whose command line is parcours.py next <slug>: a recycled pid is refused.
        """
        try:
            pid = int((directory / ".next.pid").read_text(encoding="utf-8").strip())
            os.kill(pid, 0)
            leads_group = os.getpgid(pid) == pid
            command = subprocess.run(["ps", "-o", "command=", "-p", str(pid)], capture_output=True,
                                     text=True, timeout=10).stdout
        except (OSError, ValueError, subprocess.SubprocessError):
            leads_group, command = False, ""
        if not leads_group or "parcours.py" not in command or slug not in command.split():
            raise ApiError(409, "not_owned", "le verrou est tenu par un processus que cette interface n'a pas "
                                             "lancé : l'arrêter depuis le terminal qui l'a démarré")
        return pid

    def action_validate(self, slug, body):
        stop, context = body.get("stop") is True, body.get("context")
        if stop and context is not None:
            raise ApiError(400, "bad_request", "'stop' et 'context' ne se combinent pas")
        if context is not None and not isinstance(context, dict):
            raise ApiError(400, "bad_request", "la fiche de contexte doit être un objet JSON")
        notice = None
        if context is not None:
            before = self.status(slug)
            pending = before["pending"] or {}
            idx = next((s["index"] - 1 for s in before["steps"] if s["id"] == pending.get("step")), None)
            if pending.get("type") == "validate" and idx:  # steps after the first already received the old sheet
                stale = [s["id"] for s in before["steps"][1:] if s["status"] in ("done", "paused", "failed")]
                notice = {"kind": "context_stale", "steps": stale} if stale else None
        with tempfile.TemporaryDirectory(prefix="parcours-ui-") as tmp:
            flags = ["--stop"] if stop else []
            if context is not None:
                path = write_private(tmp, "fiche.json", json.dumps(context, ensure_ascii=False, indent=2))
                flags += ["--context", path]
            return self.done(*self.run("validate", flags, [slug]), notice)

    def action_answer(self, slug, body):
        with tempfile.TemporaryDirectory(prefix="parcours-ui-") as tmp:
            if body.get("none") is True:
                flags = ["--none"]
            else:
                text = body.get("text")
                if not isinstance(text, str) or not text.strip():
                    raise ApiError(400, "bad_request", "réponses vides : coller le texte, ou « continuer sans réponses »")
                flags = ["--file", write_private(tmp, "reponses.md", text)]
            return self.done(*self.run("answer", flags, [slug]))

    def action_choose(self, slug, body):
        if body.get("skip") is True:
            return self.done(*self.run("choose", ["--skip"], [slug]))
        run = body.get("run")
        if not isinstance(run, list) or not run or not all(isinstance(s, str) and STEP_RE.match(s) for s in run):
            raise ApiError(400, "bad_request", "liste d'étapes à jouer invalide")
        return self.done(*self.run("choose", ["--run", ",".join(run)], [slug]))

    def action_rerun(self, slug, body):
        step = body.get("step")
        if not isinstance(step, str) or not STEP_RE.match(step):
            raise ApiError(400, "bad_request", "étape invalide")
        before = self.status(slug)
        out, err = self.run("rerun", positionals=[slug, step])
        after = self.status(slug)
        was = {s["id"]: s["status"] for s in before["steps"]}
        requeued = [s["id"] for s in after["steps"] if s["status"] == "pending" and was.get(s["id"]) != "pending"]
        return self.done(out, err, {"kind": "rerun", "steps": requeued})


def write_private(directory, name, text):
    """A file in a private temporary folder, for the commands that take a file argument."""
    path = Path(directory) / name
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)
    return str(path)


def interpret(code, stdout, stderr):
    """Turn the runner's exit code into nothing (0) or an ApiError.

    1: expected failure, {"error", "message"} is the last line of stdout. 2: the command line
    was refused by argparse, i.e. a bug of this interface. Anything else: unexpected.
    """
    if code == 0:
        return
    tail = (stderr or "").strip()[-400:]
    if code == 1:
        for line in reversed((stdout or "").strip().splitlines()):
            try:
                data = json.loads(line)
            except ValueError:
                continue
            if isinstance(data, dict) and "error" in data:
                status = {"not_found": 404, "locked": 409, "state_changed": 409}.get(data["error"], 422)
                raise ApiError(status, str(data["error"]), str(data.get("message", "")))
        raise ApiError(500, "unreadable", f"erreur sans message lisible de parcours.py : {tail or stdout[-300:]}")
    if code == 2:
        raise ApiError(500, "interface_bug", f"bug de l'interface : parcours.py a refusé la ligne de commande ({tail})")
    raise ApiError(500, "unexpected", f"parcours.py a quitté avec le code {code} : {tail}")


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
class Handler(BaseHTTPRequestHandler):
    server_version = "parcours-interface"
    sys_version = ""

    # -- entry points -----------------------------------------------------
    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def do_OPTIONS(self):
        self.handle_request("OPTIONS")

    do_HEAD = do_PUT = do_DELETE = do_PATCH = do_OPTIONS

    def log_message(self, format, *args):  # quiet: URLs never carry the token, but nothing needs logging
        pass

    @property
    def app(self):
        return self.server.app

    def handle_request(self, method):
        try:
            self.dispatch(method)
        except ApiError as exc:
            self.send_json(exc.status, {"error": exc.code, "message": exc.message})
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception:
            traceback.print_exc()
            with contextlib.suppress(Exception):
                self.send_json(500, {"error": "internal", "message": "erreur interne du serveur (voir sa sortie)"})

    # -- checks -----------------------------------------------------------
    def allowed_hosts(self):
        port = self.server.server_address[1]
        return {f"127.0.0.1:{port}", f"localhost:{port}"}

    def dispatch(self, method):
        if self.headers.get("Host", "") not in self.allowed_hosts():
            raise ApiError(403, "bad_host", "en-tête Host refusé")
        if method not in ("GET", "POST"):
            raise ApiError(405, "method_not_allowed", "méthode refusée")
        path = urlsplit(self.path).path
        if path == "/":
            if method != "GET":
                raise ApiError(405, "method_not_allowed", "méthode refusée")
            return self.send_page()
        if path != "/api" and not path.startswith("/api/"):
            raise ApiError(404, "not_found", "introuvable")
        self.check_token()
        origin = self.headers.get("Origin")
        if origin is not None and origin not in {f"http://{h}" for h in self.allowed_hosts()}:
            raise ApiError(403, "bad_origin", "en-tête Origin refusé")
        parts = [unquote(p) for p in path.split("/")[2:]]
        query = parse_qs(urlsplit(self.path).query)
        self.route(method, parts, query)

    def check_token(self):
        given = self.headers.get(TOKEN_HEADER, "")
        if not hmac.compare_digest(given.encode("utf-8", errors="replace"), self.app.token.encode("utf-8")):
            raise ApiError(403, "bad_token", "jeton manquant ou invalide")

    def read_json_body(self):
        if self.headers.get_content_type() != "application/json":
            raise ApiError(415, "unsupported_media_type", "Content-Type: application/json requis")
        try:
            length = int(self.headers.get("Content-Length", ""))
        except ValueError:
            raise ApiError(411, "length_required", "Content-Length requis")
        if length < 0 or length > MAX_BODY:
            raise ApiError(413, "too_large", "corps de requête trop gros")
        raw = self.rfile.read(length)
        try:
            body = json.loads(raw.decode("utf-8")) if raw.strip() else {}
        except ValueError:
            raise ApiError(400, "bad_json", "corps JSON illisible")
        if not isinstance(body, dict):
            raise ApiError(400, "bad_json", "un objet JSON est attendu")
        return body

    # -- routes -----------------------------------------------------------
    def route(self, method, parts, query):
        if parts == ["parcours"]:
            if method == "POST":
                return self.send_json(200, self.app.create(self.read_json_body()))
            self.only(method, "GET")
            return self.send_json(200, self.app.list_parcours())
        if parts == ["recipes"]:
            self.only(method, "GET")
            return self.send_json(200, self.app.recipes())
        if len(parts) >= 2 and parts[0] == "parcours":
            slug, rest = parts[1], parts[2:]
            if not rest:
                self.only(method, "GET")
                return self.send_json(200, self.app.status(slug))
            if rest[0] == "file" and len(rest) == 2:
                self.only(method, "GET")
                return self.send_json(200, self.app.read_file(slug, rest[1]))
            if rest[0] == "document" and len(rest) == 2:
                self.only(method, "GET")
                return self.send_json(200, self.app.read_document(slug, rest[1]))
            if rest == ["plan"]:
                self.only(method, "GET")
                return self.send_json(200, self.app.plan(slug, (query.get("engine") or [None])[0]))
            if rest == ["log"]:
                self.only(method, "GET")
                return self.send_json(200, self.app.read_log(slug))
            if len(rest) == 1 and rest[0] in ACTIONS:
                self.only(method, "POST")
                return self.send_json(200, self.app.act(slug, rest[0], self.read_json_body()))
        raise ApiError(404, "not_found", "introuvable")

    @staticmethod
    def only(method, allowed):
        if method != allowed:
            raise ApiError(405, "method_not_allowed", "méthode refusée")

    # -- responses --------------------------------------------------------
    def send_common_headers(self, content_type, length, csp):
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Security-Policy", csp)
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

    def send_json(self, status, data):
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_common_headers("application/json; charset=utf-8", len(payload), "default-src 'none'")
        if self.command != "HEAD":
            self.wfile.write(payload)

    def send_page(self):
        nonce = secrets.token_hex(16)
        html = PAGE.read_text(encoding="utf-8").replace("{{NONCE}}", nonce).encode("utf-8")
        csp = (f"default-src 'none'; script-src 'nonce-{nonce}'; style-src 'nonce-{nonce}'; "
               "connect-src 'self'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
        self.send_response(200)
        self.send_common_headers("text/html; charset=utf-8", len(html), csp)
        self.wfile.write(html)


class Server(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, app, port=0):
        super().__init__(("127.0.0.1", port), Handler)
        self.app = app


def make_server(parcours_dir, port=0, dev=False):
    return Server(App(parcours_dir, dev=dev), port)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv=None):
    parser = argparse.ArgumentParser(description="Page de suivi des parcours (voir docs/interface.md)")
    parser.add_argument("--parcours-dir", default="./parcours", help="dossier des parcours")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"port local (défaut {DEFAULT_PORT}, 0 = au hasard)")
    parser.add_argument("--dev", action="store_true", help="propose aussi le moteur fake (PARCOURS_FAKE_DIR)")
    parser.add_argument("--no-browser", action="store_true", help="ne pas ouvrir le navigateur")
    args = parser.parse_args(argv)
    try:
        server = make_server(args.parcours_dir, args.port, args.dev)
    except OSError as exc:
        print(f"Erreur : impossible de démarrer le serveur sur le port {args.port} ({exc})", file=sys.stderr)
        return 1
    url = f"http://127.0.0.1:{server.server_address[1]}/#t={server.app.token}"
    print(f"Dossier des parcours : {server.app.dir}", flush=True)
    print(f"Page de suivi : {url}", flush=True)
    print("Ctrl-C pour arrêter (une étape en cours continue sans le serveur).", flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
