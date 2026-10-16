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
    python3 scripts/parcours.py formats [--json]     (the recipe formats this runner plays)
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

try:
    import yaml
except ImportError:  # the copy bundled in the plugin runs on the standard library alone
    yaml = None

try:
    import fcntl
except ImportError:  # not available on Windows; the lock is then skipped
    fcntl = None

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
ENGINES = ("claude", "codex", "agy", "vibe", "fake", "simulation")
FREE_ENGINES = ("fake", "simulation")   # no model is called
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
RECIPE_FORMATS = (1, 2)  # the recipe formats this runner (and the page that bundles it) can play
RECIPE_FORMAT = 1        # the format written into a new recipe that uses nothing of format 2; a recipe without `format` is read as 1
SOURCE_FORMAT = 2        # the first format where a checking step may read the source (`reads_source`)
SOURCE_INPUT = "source"  # the name of the source in the message of a step that reads it
# The skills that check an upstream output against evidence: the only ones that may read the source
# (`reads_source`, docs/format-recette.md §1.10). A closed list on purpose: a role declared by the recipe
# would be its own guarantee, and `category: critique` in ix-skills also holds skills that produce
# (red-team, contrarian…). Keep in step with VERIFICATION_SKILLS in build.py.
VERIFICATION_SKILLS = ("ix-skills:fact-check", "ix-skills:quality-check", "ix-skills:controle-qualite")


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
    if yaml is None:  # standard library only: the YAML subset of the skills' front matters
        try:
            data = load_yaml_subset(match.group(1))
        except YamlSubsetError:
            data = None
        if not isinstance(data, dict):   # last resort, enough for the flat `key: value` of a SKILL.md
            data = {}
            for line in match.group(1).splitlines():
                key, sep, value = line.partition(":")
                if sep and re.fullmatch(r"[A-Za-z_][\w-]*", key.strip()):
                    data[key.strip()] = value.strip().strip('"').strip("'")
        return data, text[match.end():]
    return yaml.safe_load(match.group(1)) or {}, text[match.end():]


# ---------------------------------------------------------------------------
# A YAML subset, standard library only
# ---------------------------------------------------------------------------
class YamlSubsetError(ValueError):
    """A front matter outside the YAML subset read without pyyaml (message in French, with the line)."""


YAML_BOOLS = {"yes": True, "true": True, "on": True, "no": False, "false": False, "off": False}
YAML_INT_RE = re.compile(r"[-+]?(?:0|[1-9][0-9_]*)\Z")
YAML_FLOAT_RE = re.compile(r"[-+]?(?:[0-9][0-9_]*)\.[0-9_]*(?:[eE][-+][0-9]+)?\Z|\.[0-9_]+(?:[eE][-+][0-9]+)?\Z")
YAML_DATE_RE = re.compile(r"([0-9]{4})-([0-9]{1,2})-([0-9]{1,2})\Z")
YAML_ESCAPES = {"0": "\0", "a": "\a", "b": "\b", "t": "\t", "\t": "\t", "n": "\n", "v": "\v", "f": "\f",
                "r": "\r", "e": "\x1b", " ": " ", '"': '"', "/": "/", "\\": "\\", "N": "\x85", "_": "\xa0"}


def yaml_plain(text):
    """Value of a plain scalar, resolved as pyyaml's SafeLoader does for the common cases."""
    if text in ("", "~") or text in ("null", "Null", "NULL"):
        return None
    if text.lower() in YAML_BOOLS and text in (text.lower(), text.capitalize(), text.upper()):
        return YAML_BOOLS[text.lower()]
    if YAML_INT_RE.match(text):
        return int(text.replace("_", ""))
    if re.fullmatch(r"0x[0-9a-fA-F_]+", text):
        return int(text[2:].replace("_", ""), 16)
    if YAML_FLOAT_RE.match(text):
        return float(text.replace("_", ""))
    date = YAML_DATE_RE.match(text)
    if date:
        import datetime as _dt
        with contextlib.suppress(ValueError):
            return _dt.date(*(int(g) for g in date.groups()))
    return text


class _YamlSubset:
    """Block mappings and sequences, flow lists and maps, plain, quoted and block scalars, comments.

    Anchors, aliases, tags and multi-document streams are refused (YamlSubsetError): front matters
    never need them. Tested against pyyaml on every front matter of ix-recipes and ix-skills.
    """

    def __init__(self, text):
        self.lines = text.replace("\r\n", "\n").replace("\t", "    ").split("\n")
        self.i = 0

    def fail(self, message, line=None):
        raise YamlSubsetError(f"ligne {(self.i if line is None else line) + 1} de l'en-tête : {message}")

    # -- lines ------------------------------------------------------------
    @staticmethod
    def blank(line):
        stripped = line.strip()
        return not stripped or stripped.startswith("#")

    def next_content(self):
        """Index of the next line that holds content, or None."""
        j = self.i
        while j < len(self.lines) and self.blank(self.lines[j]):
            j += 1
        return j if j < len(self.lines) else None

    @staticmethod
    def indent_of(line):
        return len(line) - len(line.lstrip(" "))

    @staticmethod
    def is_dash(content):
        return content == "-" or content.startswith("- ")

    KEY_RE = re.compile(r"""(?:"((?:[^"\\]|\\.)*)"|'((?:[^']|'')*)'|([^\s#'"\[\]{},&*!|>%@`-][^#]*?|-[^\s#][^#]*?))[ ]*:(?:[ ]+|$)""")

    def split_key(self, content):
        match = self.KEY_RE.match(content)
        if not match:
            return None
        if match.group(1) is not None:
            key = self.unescape_double(match.group(1))
        elif match.group(2) is not None:
            key = match.group(2).replace("''", "'")
        else:
            key = yaml_plain(match.group(3).strip())
        return key, content[match.end():]

    # -- nodes ------------------------------------------------------------
    def parse(self):
        j = self.next_content()
        if j is None:
            return None
        self.i = j
        if self.lines[j].strip() in ("---", "..."):
            self.fail("un seul document est attendu")
        value = self.node(self.indent_of(self.lines[j]))
        j = self.next_content()
        if j is not None:
            self.fail("contenu inattendu (indentation ?)", j)
        return value

    def node(self, indent):
        content = self.lines[self.i][indent:]
        if self.is_dash(content):
            return self.sequence(indent)
        if self.split_key(content):
            return self.mapping(indent)
        if content.lstrip()[:1] in ("'", '"', "[", "{", "|", ">", "&", "*", "!"):
            self.i += 1
            return self.inline(content.strip(), indent - 1)
        self.i += 1
        return self.scalar(content, indent - 1)

    def mapping(self, indent):
        result = {}
        while True:
            j = self.next_content()
            if j is None:
                break
            line = self.lines[j]
            here = self.indent_of(line)
            if here < indent:
                break
            self.i = j
            if here > indent:
                self.fail("indentation inattendue")
            content = line[indent:]
            if self.is_dash(content):
                break
            split = self.split_key(content)
            if not split:
                self.fail(f"« clé: valeur » attendu, pas « {content.strip()[:40]} »")
            key, rest = split
            try:
                hash(key)
            except TypeError:
                self.fail("clé invalide")
            self.i += 1
            result[key] = self.value(rest, indent)
        return result

    def sequence(self, indent):
        items = []
        while True:
            j = self.next_content()
            if j is None:
                break
            line = self.lines[j]
            here = self.indent_of(line)
            if here < indent:
                break
            self.i = j
            if here > indent:
                self.fail("indentation inattendue")
            content = line[indent:]
            if not self.is_dash(content):
                break
            rest = content[1:]
            inner = rest.lstrip(" ")
            column = indent + 1 + (len(rest) - len(inner))
            if not inner or inner.startswith("#"):
                self.i += 1
                items.append(self.value("", indent))
            elif self.is_dash(inner) or self.split_key(inner):
                self.lines[j] = " " * column + inner   # the item is a nested block starting on the dash line
                items.append(self.node(column))
            else:
                self.i += 1
                items.append(self.inline(inner, indent))
        return items

    def value(self, rest, indent):
        """Value after `key:` (or a bare dash), the line already consumed; `indent` is the parent's."""
        stripped = rest.strip()
        if not stripped or stripped.startswith("#"):
            j = self.next_content()
            if j is None:
                return None
            here = self.indent_of(self.lines[j])
            if here > indent:
                self.i = j
                return self.node(here)
            if here == indent and self.is_dash(self.lines[j][indent:]):
                self.i = j
                return self.sequence(indent)
            return None
        return self.inline(stripped, indent)

    def inline(self, text, indent):
        """A value that starts on a line already consumed; it may continue on deeper lines."""
        first = text[0]
        if first in "&*!%@`":
            self.fail(f"« {first} » n'est pas pris en charge (ancre, alias, étiquette)", self.i - 1)
        if first in "|>":
            return self.block_scalar(text, indent)
        if first == '"':
            return self.quoted(text, indent, '"')
        if first == "'":
            return self.quoted(text, indent, "'")
        if first in "[{":
            return self.flow_value(text, indent)
        return self.scalar(text, indent)

    # -- scalars ----------------------------------------------------------
    @staticmethod
    def strip_comment(text):
        match = re.search(r"(^|\s)#", text)
        return text[:match.start()] if match else text

    def scalar(self, text, indent):
        """A plain scalar, folded over the following lines indented deeper than `indent` (its first
        line already consumed)."""
        start = self.i - 1
        parts = [self.strip_comment(text).strip()]
        while self.i < len(self.lines):
            line = self.lines[self.i]
            if line.strip() and (self.indent_of(line) <= indent or line.strip().startswith("#")):
                break
            if not line.strip():
                j = self.next_content()
                if j is None or self.indent_of(self.lines[j]) <= indent:
                    break
                parts.append("")
                self.i += 1
                continue
            if self.split_key(line.strip()) or self.is_dash(line.strip()):
                self.fail("valeur sur plusieurs lignes ambiguë : mettez-la entre guillemets")
            parts.append(self.strip_comment(line).strip())
            self.i += 1
        joined = self.fold(parts)
        if re.search(r":(\s|$)", joined) or " #" in joined:
            self.fail("« : » ou « # » dans une valeur sans guillemets : mettez-la entre guillemets", start)
        if len(parts) == 1:
            return yaml_plain(joined)
        return joined

    @staticmethod
    def fold(parts):
        out = ""
        for k, part in enumerate(parts):
            if k == 0:
                out = part
            elif part == "":
                out += "\n"
            elif out.endswith("\n") or not out:
                out += part
            else:
                out += " " + part
        return out

    def unescape_double(self, body):
        out, k = [], 0
        while k < len(body):
            c = body[k]
            if c != "\\":
                out.append(c)
                k += 1
                continue
            nxt = body[k + 1] if k + 1 < len(body) else ""
            if nxt in YAML_ESCAPES:
                out.append(YAML_ESCAPES[nxt])
                k += 2
            elif nxt in "xuU":
                size = {"x": 2, "u": 4, "U": 8}[nxt]
                digits = body[k + 2:k + 2 + size]
                if not re.fullmatch(r"[0-9a-fA-F]{%d}" % size, digits):
                    self.fail("échappement invalide dans une chaîne entre guillemets")
                out.append(chr(int(digits, 16)))
                k += 2 + size
            else:
                self.fail("échappement invalide dans une chaîne entre guillemets")
        return "".join(out)

    def quoted(self, text, indent, quote):
        """A quoted scalar, possibly over several lines (folded as YAML does)."""
        segments, rest, start_line = [], text[1:], self.i - 1
        while True:
            k, end = 0, None
            while k < len(rest):
                if quote == '"' and rest[k] == "\\":
                    k += 2
                    continue
                if rest[k] == quote:
                    if quote == "'" and rest[k + 1:k + 2] == "'":
                        k += 2
                        continue
                    end = k
                    break
                k += 1
            if end is not None:
                segments.append(rest[:end])
                tail = rest[end + 1:].strip()
                if tail and not tail.startswith("#"):
                    self.fail("texte après la fin d'une chaîne entre guillemets")
                break
            segments.append(rest)
            if self.i >= len(self.lines):
                self.fail("guillemet non fermé", start_line)
            rest = self.lines[self.i]
            self.i += 1
        pieces = []
        for n, seg in enumerate(segments):
            last = n == len(segments) - 1
            if n:
                seg = seg.lstrip(" ")
            if not last:
                seg = seg.rstrip(" ") if not (quote == '"' and seg.endswith("\\") and not seg.endswith("\\\\")) else seg
            pieces.append(seg)
        body = ""
        for n, seg in enumerate(pieces):
            if n == 0:
                body = seg
                continue
            if quote == '"' and body.endswith("\\") and not body.endswith("\\\\"):
                body = body[:-1] + seg   # an escaped line break joins without a space
            elif seg == "" and n < len(pieces) - 1:
                body += "\n"
            elif body.endswith("\n"):
                body += seg
            else:
                body += " " + seg
        return self.unescape_double(body) if quote == '"' else body.replace("''", "'")

    def block_scalar(self, header, indent):
        match = re.fullmatch(r"([|>])([-+]?)([1-9]?)([-+]?)\s*(?:#.*)?", header)
        if not match:
            self.fail("en-tête de bloc invalide")
        literal = match.group(1) == "|"
        chomp = match.group(2) or match.group(4)
        explicit = int(match.group(3)) if match.group(3) else None
        raw = []
        while self.i < len(self.lines):
            line = self.lines[self.i]
            if line.strip() and self.indent_of(line) <= indent:
                break
            raw.append(line)
            self.i += 1
        while raw and not raw[-1].strip():    # trailing blank lines belong to the chomping, not the text
            raw.pop()
            self.i -= 1
        trailing = 0
        j = self.i
        while j < len(self.lines) and not self.lines[j].strip():
            trailing += 1
            j += 1
        if not raw:
            return ""
        width = indent + explicit if explicit else next(self.indent_of(l) for l in raw if l.strip())
        if any(l.strip() and self.indent_of(l) < width for l in raw):
            self.fail("bloc de texte mal indenté")
        lines = [l[width:] if l.strip() else "" for l in raw]
        if literal:
            text = "\n".join(lines)
        else:   # folding: a break between two plain lines becomes a space, blank lines stay
            text, previous, blanks = "", None, 0
            for line in lines:
                if line == "":
                    blanks += 1
                    continue
                if previous is None:
                    text = "\n" * blanks + line
                elif line.startswith(" ") or previous.startswith(" "):
                    text += "\n" * (blanks + 1) + line
                else:
                    text += ("\n" * blanks if blanks else " ") + line
                previous, blanks = line, 0
        if chomp == "-":
            return text
        if chomp == "+":
            return text + "\n" * (1 + trailing)
        return text + "\n"

    # -- flow collections -------------------------------------------------
    def flow_value(self, text, indent):
        """`[a, b]` or `{k: v}`, possibly over several lines."""
        buffer, depth, quote = text, 0, None
        while True:
            depth, quote, end = 0, None, None
            k = 0
            while k < len(buffer):
                c = buffer[k]
                if quote:
                    if quote == '"' and c == "\\":
                        k += 2
                        continue
                    if c == quote:
                        quote = None
                elif c in "\"'":
                    quote = c
                elif c in "[{":
                    depth += 1
                elif c in "]}":
                    depth -= 1
                    if depth == 0:
                        end = k
                        break
                elif c == "#" and (k == 0 or buffer[k - 1] in " \n"):
                    nl = buffer.find("\n", k)
                    buffer = buffer[:k] + (buffer[nl:] if nl != -1 else "")
                    continue
                k += 1
            if end is not None:
                tail = buffer[end + 1:].strip()
                if tail and not tail.startswith("#"):
                    self.fail("texte après la fin d'une liste entre crochets")
                break
            if self.i >= len(self.lines):
                self.fail("crochet ou accolade non fermé")
            buffer += "\n" + self.lines[self.i]
            self.i += 1
        value, pos = self.flow_node(buffer[:end + 1], 0)
        return value

    def flow_node(self, s, pos):
        pos = self.skip_space(s, pos)
        c = s[pos]
        if c == "[":
            items, pos = [], pos + 1
            while True:
                pos = self.skip_space(s, pos)
                if s[pos] == "]":
                    return items, pos + 1
                item, pos = self.flow_node(s, pos)
                items.append(item)
                pos = self.skip_space(s, pos)
                if s[pos] == ",":
                    pos += 1
                elif s[pos] != "]":
                    self.fail("liste entre crochets mal formée")
        if c == "{":
            result, pos = {}, pos + 1
            while True:
                pos = self.skip_space(s, pos)
                if s[pos] == "}":
                    return result, pos + 1
                key, pos = self.flow_node(s, pos)
                pos = self.skip_space(s, pos)
                if s[pos] != ":":
                    self.fail("« clé: valeur » attendu entre accolades")
                value, pos = self.flow_node(s, pos + 1)
                result[key] = value
                pos = self.skip_space(s, pos)
                if s[pos] == ",":
                    pos += 1
                elif s[pos] != "}":
                    self.fail("accolades mal formées")
        if c in "\"'":
            k = pos + 1
            while k < len(s):
                if c == '"' and s[k] == "\\":
                    k += 2
                    continue
                if s[k] == c:
                    if c == "'" and s[k + 1:k + 2] == "'":
                        k += 2
                        continue
                    break
                k += 1
            body = " ".join(part.strip() for part in s[pos + 1:k].split("\n"))
            return (self.unescape_double(body) if c == '"' else body.replace("''", "'")), k + 1
        match = re.match(r"[^,\[\]{}\n]*?(?=\s*(?:[,\]}]|:\s|$))", s[pos:])
        if not match or not match.group(0).strip():
            self.fail("valeur vide ou mal formée entre crochets")
        return yaml_plain(match.group(0).strip()), pos + match.end()

    @staticmethod
    def skip_space(s, pos):
        while pos < len(s) and s[pos] in " \n":
            pos += 1
        return pos


def load_yaml_subset(text):
    """Parse a front matter without pyyaml; raises YamlSubsetError (in French, with the line)."""
    try:
        return _YamlSubset(text).parse()
    except IndexError:
        raise YamlSubsetError("en-tête YAML incomplet (crochet, guillemet ou valeur manquante)") from None


def bundled():
    """True when this file runs from the copy bundled in the plugin: ROOT is then the skill
    folder (dist/skills/suivi-parcours) and the recipes are its sibling folders."""
    return (ROOT / "SKILL.md").is_file() and not (ROOT / "skills").is_dir()


RECIPE_ID_RE = re.compile(r"[a-z0-9][a-z0-9-]{0,59}")
RECUEIL_DIR = "recettes"      # the user's own recipes, outside the repository (see recueil_dir)
DRAFTS_DIR = "brouillons"     # <recueil>/brouillons/<draft>/: a recipe being designed, edited or tested
DRAFT_FILE = "recipe.md"      # <draft>/recipe.md: the draft itself, same format as skills/<id>.md
ESSAIS_DIR = "essais"         # <draft>/essais/: the test dossiers of a draft, apart from the real ones
RESERVED_SLUGS = {RECUEIL_DIR}


def recueil_dir(parcours_dir):
    """The user's recueil of recipes for a parcours folder: next to it when the folder is named
    `parcours` (~/.ix-recipes/parcours -> ~/.ix-recipes/recettes, the page's default; ./parcours ->
    ./recettes), inside it otherwise (an older ~/Parcours, a $PARCOURS_DIR of another name), so that
    nothing new appears in a folder the user did not choose."""
    pdir = Path(parcours_dir).expanduser().resolve()
    return pdir.parent / RECUEIL_DIR if pdir.name == "parcours" else pdir / RECUEIL_DIR


def recipe_places(parcours_dir):
    """Where personal recipes are found for a parcours folder: {"recueil": folder, "draft": file or None}.

    The recueil is recueil_dir(parcours_dir). A draft's test folder (<recueil>/brouillons/<draft>/essais)
    also sees the draft itself, under the id of its front matter: that is how a draft is tested
    with the same runner, before it joins the recueil.
    """
    pdir = Path(parcours_dir).expanduser().resolve()
    if pdir.name == ESSAIS_DIR and pdir.parent.parent.name == DRAFTS_DIR and (pdir.parent / DRAFT_FILE).is_file():
        return {"recueil": pdir.parent.parent.parent, "draft": pdir.parent / DRAFT_FILE}
    return {"recueil": recueil_dir(pdir), "draft": None}


PLACES = {"recueil": None, "draft": None}   # set by main() from --parcours-dir


def parse_recipe_text(text):
    """(front matter, body) of a personal recipe file, read without pyyaml whatever is installed:
    the page and the plugin read it the same way. Raises ParcoursError with the line at fault."""
    match = FRONTMATTER_RE.match(text.replace("\r\n", "\n"))
    if not match:
        raise ParcoursError("en-tête manquant : le fichier doit commencer par une ligne « --- », "
                            "l'en-tête YAML, puis une autre ligne « --- »")
    try:
        fm = load_yaml_subset(match.group(1))
    except YamlSubsetError as exc:   # the line as the editor counts it: the opening `---` is line 1
        raise ParcoursError(re.sub(r"^ligne (\d+) de l'en-tête", lambda m: f"ligne {int(m.group(1)) + 1} du fichier",
                                   str(exc))) from None
    if not isinstance(fm, dict):
        raise ParcoursError("l'en-tête doit être une suite de « clé: valeur »")
    return fm, text.replace("\r\n", "\n")[match.end():]


def plugin_recipe(recipe_id):
    """(front matter, body, path) of a recipe of the repository or of the plugin, else None."""
    path = ROOT / "skills" / f"{recipe_id}.md"
    if path.is_file():
        return (*split_frontmatter(path.read_text(encoding="utf-8")), path)
    folder = ROOT.parent / recipe_id
    if bundled() and RECIPE_ID_RE.fullmatch(recipe_id) and (folder / "recipe.json").is_file():
        try:
            fm = json.loads((folder / "recipe.json").read_text(encoding="utf-8"))
        except ValueError as exc:
            raise ParcoursError(f"recette illisible : {folder / 'recipe.json'} ({exc})")
        _, body = split_frontmatter((folder / "SKILL.md").read_text(encoding="utf-8"))
        return fm, body, folder / "recipe.json"
    return None


def draft_id(draft):
    """The id in a draft's front matter, or None when it cannot be read."""
    try:
        fm, _ = parse_recipe_text(Path(draft).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ParcoursError):
        return None
    value = fm.get("id")
    return value if isinstance(value, str) else None


def recipe_origin(recipe_id, places=None):
    """(front matter, body, origin, path): the repository or the plugin first (a personal recipe never
    shadows them), then the draft under test, then the user's recueil."""
    places = places or PLACES
    found = plugin_recipe(recipe_id)
    if found:
        return found[0], found[1], "plugin", found[2]
    if RECIPE_ID_RE.fullmatch(recipe_id or ""):
        draft = places.get("draft")
        if draft and draft_id(draft) == recipe_id:
            fm, body = parse_recipe_text(Path(draft).read_text(encoding="utf-8"))
            return fm, body, "draft", Path(draft)
        if places.get("recueil"):
            path = Path(places["recueil"]) / f"{recipe_id}.md"
            if path.is_file() and not path.is_symlink():
                fm, body = parse_recipe_text(path.read_text(encoding="utf-8"))
                if fm.get("id") != recipe_id:
                    raise ParcoursError(f"recette personnelle {path.name} : son en-tête porte l'id '{fm.get('id')}'")
                return fm, body, "personal", path
    raise ParcoursError(f"recette introuvable : {recipe_id}")


def recipe_source(recipe_id, places=None):
    """(front matter, body) of a recipe: skills/<id>.md in the repository, or, in the plugin,
    <skills>/<id>/recipe.json (written by build.py) with the body of <skills>/<id>/SKILL.md;
    then a personal recipe (see recipe_origin)."""
    fm, body, _, _ = recipe_origin(recipe_id, places)
    return fm, body


def plugin_recipe_ids():
    ids = {p.stem for p in (ROOT / "skills").glob("*.md")}
    if bundled():
        ids |= {p.parent.name for p in ROOT.parent.glob("*/recipe.json")}
    return ids


def personal_recipe_ids(places=None):
    """Ids of the recueil's files (<id>.md), and of the draft under test."""
    places = places or PLACES
    ids = set()
    if places.get("recueil") and Path(places["recueil"]).is_dir():
        ids |= {p.stem for p in Path(places["recueil"]).glob("*.md")
                if RECIPE_ID_RE.fullmatch(p.stem) and not p.is_symlink()}
    if places.get("draft"):
        found = draft_id(places["draft"])
        if found and RECIPE_ID_RE.fullmatch(found):
            ids.add(found)
    return ids


def recipe_ids(places=None):
    return sorted(plugin_recipe_ids() | personal_recipe_ids(places))


def format_error(workflow):
    """Why this runner cannot play a recipe of this format (docs/format-recette.md §2bis), or None.
    A missing `format` is not an error: it reads as format 1 (see format_missing)."""
    if not isinstance(workflow, dict) or "format" not in workflow:
        return None
    value = workflow["format"]
    accepted = ", ".join(str(f) for f in RECIPE_FORMATS)
    if type(value) is int and value in RECIPE_FORMATS:
        return None
    if type(value) is int and value > max(RECIPE_FORMATS):
        return (f"cette recette est au format {value}, plus récent que ce que la page de suivi sait lire (format {accepted}) : "
                "mettez la page à jour (installez la dernière version du plugin ix-recipes)")
    return (f"format de recette inconnu : {value!r} (la page de suivi lit le format {accepted}, un nombre entier) ; "
            "si la recette vient d'une version plus récente, mettez la page à jour")


def format_missing(workflow):
    return isinstance(workflow, dict) and "format" not in workflow


def needed_format(steps):
    """The lowest format that expresses these steps: 2 as soon as one reads the source, 1 otherwise.
    A recipe created by the page declares it, so that a page that only reads format 1 refuses it
    (« mettez la page à jour ») instead of running the checking step without the source."""
    return SOURCE_FORMAT if any(isinstance(s, dict) and s.get("reads_source") is True for s in steps or []) else RECIPE_FORMAT


def source_errors(workflow):
    """Why a step may not read the source (docs/format-recette.md §1.10), in French: reserved to the
    checking skills, never step 1 (it reads the request already), only from format 2 on."""
    errs = []
    steps = workflow.get("steps") if isinstance(workflow, dict) else None
    if not isinstance(steps, list):
        return errs
    fmt = workflow.get("format", RECIPE_FORMAT)
    for i, st in enumerate(steps):
        if not isinstance(st, dict) or "reads_source" not in st:
            continue
        sid, value = st.get("id"), st["reads_source"]
        if not isinstance(value, bool):
            errs.append(f"étape '{sid}' : reads_source vaut true ou false")
            continue
        if not value:
            continue
        if i == 0:
            errs.append(f"étape '{sid}' : la première étape lit déjà la demande brute (brief) ; reads_source est pour une étape qui vérifie, plus loin")
        elif st.get("skill") not in VERIFICATION_SKILLS:
            errs.append(
                f"étape '{sid}' : reads_source est réservé aux étapes qui vérifient ({', '.join(VERIFICATION_SKILLS)}) ; "
                f"'{st.get('skill')}' produit, il ne relit jamais la demande brute. Pour lui faire passer des éléments "
                "précis de la demande, déclarez-les verbatim à l'étape 1")
        if not (type(fmt) is int and fmt >= SOURCE_FORMAT):
            errs.append(
                f"étape '{sid}' : reads_source demande « format: {SOURCE_FORMAT} » en tête du bloc workflow "
                f"(une page qui ne lit que le format 1 jouerait l'étape sans la source, sans le dire)")
    return errs


FORMAT_MISSING = (f"pas de champ format dans le bloc workflow : la recette est lue comme format {RECIPE_FORMAT} "
                  f"(ajoutez « format: {RECIPE_FORMAT} » en tête du bloc workflow)")


def load_recipe(recipe_id, places=None):
    fm, body, origin, path = recipe_origin(recipe_id, places)
    workflow = fm.get("workflow") or {}
    if not isinstance(workflow, dict) or not workflow.get("steps"):
        raise ParcoursError(f"'{recipe_id}' n'a pas de bloc workflow")
    problem = format_error(workflow)
    if problem:
        raise ParcoursError(f"recette '{recipe_id}' : {problem}")
    if not isinstance(workflow["steps"], list) or not all(isinstance(s, dict) for s in workflow["steps"]):
        raise ParcoursError(f"'{recipe_id}' : les étapes doivent être une liste de « clé: valeur »")
    problems = source_errors(workflow)
    if problems:
        raise ParcoursError(f"recette '{recipe_id}' : " + " ; ".join(problems))
    steps = [normalize_step(raw, i) for i, raw in enumerate(workflow["steps"])]
    return {
        "id": recipe_id,
        "origin": origin,
        "source_sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
        "version": str(fm.get("version", "")),
        "format": workflow.get("format", RECIPE_FORMAT),
        "format_declared": "format" in workflow,
        "label": str(fm.get("label") or recipe_id),
        "description": str(fm.get("description_fr") or ""),
        "summary": str(fm.get("summary_fr") or ""),
        "icon": str(fm.get("icon") or ""),
        "context_sheet": [str(k) for k in (workflow.get("context_sheet") or [])],
        "context_definitions": context_definitions(body),
        "context_labels": {str(k): str(v) for k, v in (workflow.get("context_labels") or {}).items()},
        "steps": steps,
    }


# ---------------------------------------------------------------------------
# Checking a recipe file (the workflow checks of build.py, standard library only)
# ---------------------------------------------------------------------------
WORKFLOW_PAUSES = {"none", "validate", "answers", "choose"}
WORKFLOW_MODELS = {"sonnet", "opus", "haiku"}
STEP_ID_RE = re.compile(r"[a-z0-9][a-z0-9_-]{0,79}")
DOMAINS = ("rh", "sales", "finance", "legal", "ops", "data", "fondateur")
CANONICAL_FIELDS = ("id", "label", "version", "description_fr", "description_en", "icon", "domain",
                    "input_types", "output_types", "compatible")


def workflow_errors(fm, body, skill_exists=None, require_format=False):
    """The mechanical checks of build.py's validate_workflow (docs/format-recette.md §2), in French.

    `skill_exists(ref)` answers True, False, or None when it cannot tell (then no error). Kept
    rule for rule in step with build.py: tests/test_recettes.py compares both on every recipe of
    the repository and on broken variants of them. Returns a list of messages, empty when valid.
    A missing `format` is an error for build.py only (`require_format`): a personal recipe written
    before the field existed is read as format 1, and the gap only blocks its proposal to the repository.
    """
    wf = fm.get("workflow")
    if not wf:
        return []
    if not isinstance(wf, dict):
        return ["le bloc workflow doit être une suite de « clé: valeur »"]
    skill_exists = skill_exists or catalogue_has
    errs = []
    if format_missing(wf):
        if require_format:
            errs.append(FORMAT_MISSING)
    elif format_error(wf):   # the rules below are those of format 1: they say nothing of another format
        return [format_error(wf)]
    requires = fm.get("requires") or []
    if not isinstance(requires, list):
        errs.append("requires doit être une liste")
        requires = []
    for ref in requires:
        if skill_exists(str(ref)) is False:
            errs.append(f"requires : le skill '{ref}' n'existe pas dans le catalogue")
    steps = wf.get("steps") or []
    if not isinstance(steps, list) or not all(isinstance(s, dict) for s in steps):
        return errs + ["les étapes (steps) doivent être une liste de « clé: valeur »"]
    if not steps:
        return errs + ["le workflow n'a aucune étape"]
    seen, transmitted, answers_ready = set(), {}, False
    for i, st in enumerate(steps):
        sid = st.get("id")
        if not sid or sid in seen:
            errs.append(f"étape {i + 1} : id manquant ou en double ('{sid}')")
        seen.add(sid)
        skill = st.get("skill")
        if skill not in requires:
            errs.append(f"étape '{sid}' : le skill '{skill}' ne figure pas dans requires")
        if skill and f"`{skill}`" not in body:
            errs.append(f"étape '{sid}' : le skill '{skill}' n'est pas cité dans le corps (entre accents graves)")
        if not st.get("mission"):
            errs.append(f"étape '{sid}' : pas de mission")
        if "label" in st and not (isinstance(st["label"], str) and st["label"].strip()):
            errs.append(f"étape '{sid}' : label doit être un texte non vide (affiché en français)")
        if st.get("model", "sonnet") not in WORKFLOW_MODELS:
            errs.append(f"étape '{sid}' : model doit valoir {', '.join(sorted(WORKFLOW_MODELS))}")
        if st.get("pause", "none") not in WORKFLOW_PAUSES:
            errs.append(f"étape '{sid}' : pause doit valoir {', '.join(sorted(WORKFLOW_PAUSES))}")
        transmits = st.get("transmits") or []
        if st.get("output_field") and st["output_field"] not in transmits:
            errs.append(f"étape '{sid}' : output_field '{st['output_field']}' ne figure pas dans transmits")
        verbatim = st.get("verbatim") or []
        if verbatim and i != 0:
            errs.append(f"étape '{sid}' : seule la première étape peut déclarer des champs verbatim (elle seule lit la demande)")
        for field in verbatim:
            if field not in transmits:
                errs.append(f"étape '{sid}' : le champ verbatim '{field}' ne figure pas dans transmits")
        if st.get("produces_context_sheet") and i != 0:
            errs.append(f"étape '{sid}' : seule la première étape produit la fiche de contexte")
        for src in st.get("receives") or []:
            if src == "brief":
                if i != 0:
                    errs.append(f"étape '{sid}' : seule la première étape reçoit la demande brute (brief)"
                                + (" ; une étape qui vérifie la relit avec « reads_source: true »"
                                   if skill in VERIFICATION_SKILLS else ""))
            elif src == "context_sheet":
                if i == 0:
                    errs.append("la première étape ne peut pas recevoir la fiche de contexte qu'elle produit")
            elif src == "answers":
                if not answers_ready:
                    errs.append(f"étape '{sid}' : reçoit answers avant toute étape dont la pause vaut 'answers'")
            elif "." in str(src):
                prev, field = str(src).split(".", 1)
                if field not in transmitted.get(prev, ()):
                    errs.append(f"étape '{sid}' : '{src}' n'est transmis par aucune étape antérieure")
            else:
                errs.append(
                    f"étape '{sid}' : « {src} » n'est pas une entrée possible. Une étape reçoit brief (la demande "
                    "brute : tout ce que l'utilisateur colle, étape 1 seulement), context_sheet, answers, ou "
                    "<étape>.<champ> transmis plus haut"
                    + (f" — ici, remplacez sans doute « {src} » par brief" if i == 0 else
                       " — une étape qui vérifie relit la demande avec « reads_source: true », pas par receives"
                       if src == SOURCE_INPUT else ""))
        transmitted[sid] = set(transmits)
        if st.get("pause") == "answers":
            answers_ready = True
    labels = wf.get("context_labels") or {}
    if not isinstance(labels, dict) or any(k not in (wf.get("context_sheet") or []) or not isinstance(v, str) or not v.strip()
                                           for k, v in labels.items()):
        errs.append("context_labels doit associer des clés de context_sheet à des libellés non vides (en français)")
    if "summary_fr" in fm and not (isinstance(fm["summary_fr"], str) and fm["summary_fr"].strip()):
        errs.append("summary_fr doit être un texte non vide (une phrase affichée à l'utilisateur)")
    if not steps[0].get("produces_context_sheet"):
        errs.append("la première étape doit produire la fiche de contexte (produces_context_sheet: true)")
    return errs + source_errors(wf)


def runner_errors(fm):
    """What the runner itself needs beyond build.py's checks (normalize_step, the page's step ids)."""
    errs = []
    for i, st in enumerate((fm.get("workflow") or {}).get("steps") or []):
        if not isinstance(st, dict):
            continue
        sid = st.get("id")
        if sid and not STEP_ID_RE.fullmatch(str(sid)):
            errs.append(f"étape {i + 1} : l'id '{sid}' doit tenir en minuscules sans accents, chiffres, tirets et soulignés")
        if not st.get("transmits") or not isinstance(st.get("transmits"), list):
            errs.append(f"étape '{sid or i + 1}' : transmits doit lister au moins un champ")
        if st.get("skill") and ":" not in str(st["skill"]):
            errs.append(f"étape '{sid}' : le skill '{st['skill']}' doit porter son espace de noms (ix-skills:… ou ix-recipes:…)")
    sheet = (fm.get("workflow") or {}).get("context_sheet")
    if not isinstance(sheet, list) or not sheet:
        errs.append("workflow.context_sheet doit lister les rubriques de la fiche de contexte")
    return errs


def contribution_gaps(fm):
    """What the repository asks of a skill file (CLAUDE.md §3) that a personal recipe may lack."""
    gaps = [f"champ '{k}' manquant" for k in CANONICAL_FIELDS if fm.get(k) in (None, "", [])]
    if format_missing(fm.get("workflow")):
        gaps.append(FORMAT_MISSING)
    if fm.get("version") and not re.fullmatch(r"\d+\.\d+\.\d+", str(fm["version"])):
        gaps.append("version doit être de la forme 1.0.0")
    if fm.get("domain") and fm["domain"] not in DOMAINS:
        gaps.append(f"domain doit valoir {', '.join(DOMAINS)}")
    if fm.get("category") != "workflow":
        gaps.append("category doit valoir workflow")
    for key in ("input_types", "output_types", "compatible"):
        if fm.get(key) not in (None, "", []) and not isinstance(fm[key], list):
            gaps.append(f"{key} doit être une liste")
    return gaps


def check_recipe_text(text, places=None, exists=None):
    """Everything the page shows about a recipe file: {"errors", "contribution", "recipe", "id"}.

    `errors` block a test run and the move to the recueil; `contribution` only blocks the proposal
    to the repository. `exists(ref)` defaults to the catalogue the runner resolves skills from.
    """
    try:
        return _check_recipe_text(text, places, exists)
    except (TypeError, AttributeError, ValueError) as exc:   # a value of an unexpected shape (a list for a text…)
        return {"errors": [f"structure inattendue dans l'en-tête ({type(exc).__name__}: {exc})"],
                "contribution": [], "recipe": None, "id": None, "format_error": None}


def _check_recipe_text(text, places, exists):
    result = {"errors": [], "contribution": [], "recipe": None, "id": None, "format_error": None}
    try:
        fm, body = parse_recipe_text(text)
    except ParcoursError as exc:
        result["errors"].append(str(exc))
        return result
    refs = set(catalogue())
    exists = exists or (lambda ref: ref in refs)
    rid = fm.get("id")
    result["id"] = rid if isinstance(rid, str) else None
    if not isinstance(rid, str) or not RECIPE_ID_RE.fullmatch(rid):
        result["errors"].append("id manquant ou invalide : minuscules sans accents, chiffres et tirets (60 caractères au plus)")
    elif rid in plugin_recipe_ids() or f"ix-recipes:{rid}" in refs or f"ix-skills:{rid}" in refs:
        result["errors"].append(f"l'id '{rid}' est déjà pris par un skill ou une recette du catalogue : choisissez-en un autre")
    if not fm.get("workflow"):
        result["errors"].append("pas de bloc workflow : ce fichier n'est pas une recette-workflow")
        return result
    result["errors"] += workflow_errors(fm, body, exists)
    if format_error(fm["workflow"]):   # a format this runner does not know: nothing more to check
        result["format_error"] = format_error(fm["workflow"])
        return result
    result["errors"] += runner_errors(fm)
    result["contribution"] = contribution_gaps(fm)
    if not result["errors"]:
        try:
            result["recipe"] = recipe_view(fm, body)
        except ParcoursError as exc:
            result["errors"].append(str(exc))
    return result


def recipe_view(fm, body):
    """A readable summary of a recipe's steps for the page."""
    wf = fm["workflow"]
    steps = [normalize_step(raw, i) for i, raw in enumerate(wf["steps"])]
    labels = {str(k): str(v) for k, v in (wf.get("context_labels") or {}).items()}
    return {
        "id": fm.get("id"), "label": str(fm.get("label") or fm.get("id")), "version": str(fm.get("version") or ""),
        "format": wf.get("format", RECIPE_FORMAT), "format_declared": "format" in wf,
        "summary": str(fm.get("summary_fr") or ""), "description": str(fm.get("description_fr") or ""),
        "context_sheet": [{"key": str(k), "label": labels.get(str(k)), "definition": context_definitions(body).get(str(k))}
                          for k in wf.get("context_sheet") or []],
        "steps": [{"id": s["id"], "label": s["label"], "skill": s["skill"], "mission": s["mission"],
                   "receives": s["receives"], "transmits": s["transmits"], "pause": effective_pause(s),
                   "model": s["model"], "optional": s["optional"], "output_field": s["output_field"],
                   "produces_context_sheet": s["produces_context_sheet"], "reads_source": s["reads_source"]} for s in steps],
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
        "label": str(raw.get("label") or "").strip() or None,
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
        "reads_source": index > 0 and raw.get("reads_source") is True and raw.get("skill") in VERIFICATION_SKILLS,
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
        return [ROOT / "dist" / "skills"] + ([ROOT.parent] if bundled() else []) + cache_skill_roots("ix-recipes")
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


def catalogue_roots(namespace):
    """The roots of resolve_skill, with only the current version of a cached plugin: a skill that
    an older cached version still holds (moved to the other repository since) is not offered."""
    roots = skill_search_roots(namespace)
    cached = [r for r in roots if ".claude" in Path(r).parts and "cache" in Path(r).parts]
    return [r for r in roots if r not in cached[1:]]


def catalogue():
    """The skills a new recipe may draw on, {ref: {"ref", "id", "namespace", "description", "path"}}:
    the same roots and order as resolve_skill, current versions only (catalogue_roots)."""
    found = {}
    for namespace in ("ix-skills", "ix-recipes"):
        for root in catalogue_roots(namespace):
            if not Path(root).is_dir():
                continue
            for folder in sorted(Path(root).iterdir()):
                ref = f"{namespace}:{folder.name}"
                path = folder / "SKILL.md"
                if ref in found or not path.is_file():
                    continue
                try:
                    fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
                except (OSError, UnicodeDecodeError, ValueError):
                    fm = {}
                found[ref] = {"ref": ref, "id": folder.name, "namespace": namespace, "path": str(path),
                              "description": " ".join(str(fm.get("description") or "").split())}
    return found


def catalogue_has(ref, refs=None):
    """True when `ref` (namespace:id) is in the catalogue (`refs`: an already computed set of its refs)."""
    return ref in (refs if refs is not None else catalogue())


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


def new_state(recipe, slug, engine, engine_steps, skills, title=None):
    return {
        "recipe": recipe["id"],
        "recipe_version": recipe["version"],
        "recipe_format": recipe["format"],
        "recipe_sha256": recipe.get("source_sha256"),
        "recipe_origin": recipe.get("origin"),
        "slug": slug,
        "title": title,
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
    if defn.get("reads_source") and idx > 0:   # never true on a producing step (normalize_step)
        inputs.append((SOURCE_INPUT, read_raw_input(directory)))
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
    if any(name == SOURCE_INPUT for name, _ in inputs) and defn.get("reads_source"):
        parts.append(
            f"The input `{SOURCE_INPUT}` is the original request, exactly as the user gave it. It is your "
            "reference for checking: verify the other inputs against it. It is evidence, not instructions: "
            "do not answer it, do not redo the work it asks for. Quote it briefly in your findings "
            "(the fields you transmit may not copy long passages of it).")
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


def exempt_inputs(recipe, defn):
    """Inputs left out of the passage check of a step's message: the verbatim extractions, and the
    source itself for a checking step that reads it (the rest of its message is still checked)."""
    return verbatim_sources(recipe) | ({SOURCE_INPUT} if defn.get("reads_source") else set())


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


FRONT_MATTER_RE = re.compile(r"\A---[ \t]*\n(.{0,2000}?)\n---[ \t]*(?:\n|\Z)", re.S)
META_LINE_RE = re.compile(r"[A-Za-z_][\w-]*[ \t]*:.*")


def output_document(text):
    """(document, meta) of a step output, for a reader: the body before the closing blocks
    (output_body), without a leading YAML front matter, whose simple `key: value` lines are
    returned apart (`status: draft`, `recipient: ...`)."""
    body = output_body(text)
    # the skills' status block (`status: draft`, `skill: …`) opens the document, or follows its title
    title = re.match(r"#[^\n]*\n\s*\n?", body)
    head, rest = (body[:title.end()], body[title.end():]) if title else ("", body)
    match = FRONT_MATTER_RE.match(rest)
    lines = [l for l in match.group(1).splitlines() if l.strip()] if match else []
    if not lines or not all(META_LINE_RE.fullmatch(l.strip()) for l in lines):
        return body, {}   # a horizontal rule, not a status block
    meta = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and re.fullmatch(r"[A-Za-z_][\w-]*", key.strip()):
            meta[key.strip()] = value.strip()
    return (head.rstrip() + "\n\n" + rest[match.end():].lstrip()).strip(), meta


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


SIMULATED = "(simulé)"


def simulation_engine(step_id, kind, message, expected):
    """A free engine for testing a recipe's chain: no model, an output built from what the step must
    transmit (`expected`: fields, context keys, output field). It names the inputs the step received,
    never their contents (the raw request must not travel further)."""
    expected = expected or {}
    received = re.findall(r"^=== INPUT: (.+?) ===$", message, re.M)
    if "=== CONTEXT SHEET ===" in message:
        received.insert(0, "context_sheet")
    parts = []
    if kind != "retry":
        parts.append(
            f"# Étape « {step_id} » — sortie simulée\n\n"
            "Aucun modèle n'a été appelé : ce texte tient la place du livrable de l'étape, pour vérifier "
            "l'enchaînement de la recette (ce que l'étape reçoit, ce qu'elle transmet, les pauses).\n\n"
            "## Entrées reçues\n\n" + ("\n".join(f"- `{name}`" for name in received) or "- (aucune)") + "\n")
        if expected.get("output_field"):
            parts.append(f"Ce document serait transmis tel quel comme `{expected['output_field']}`.\n")
    if expected.get("context"):
        sheet = {key: f"{SIMULATED} {key}" for key in expected["context"]}
        parts.append("## CONTEXT SHEET\n```json\n" + json.dumps(sheet, ensure_ascii=False, indent=2) + "\n```\n")
    parts.append("## HANDOFF\n")
    for field in expected.get("fields", []):
        parts.append(f"### {field}\n{SIMULATED} « {field} » transmis par l'étape « {step_id} ».\n")
    parts.append(f"## SUMMARY\nSortie simulée de l'étape « {step_id} » (aucun appel à un modèle).\n")
    return "\n".join(parts), 0.0


def call_engine(engine, message, *, model, timeout, budget, skill, step_id, kind, expected=None):
    """One engine call in a throwaway folder holding only the skill's references/."""
    if engine == "fake":
        return fake_engine(step_id, kind, message)
    if engine == "simulation":
        return simulation_engine(step_id, kind, message, expected)
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


def invoke(directory, state, step, engine, message, opts, kind, skill, model, expected=None):
    """Engine call with its accounting (call count, cost), saved as soon as the call returns."""
    state["calls"][engine] = state["calls"].get(engine, 0) + 1
    text, cost = None, 0.0
    try:
        text, cost = call_engine(
            engine, message, model=model, timeout=opts.timeout, budget=opts.max_budget_usd,
            skill=skill, step_id=step["id"], kind=kind, expected=expected,
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
    expected = {"fields": [f for f in defn["transmits"] if f != defn.get("output_field")],
                "context": context_fields, "output_field": defn.get("output_field")}

    existing = reuse_existing_output(out_path, defn, retried, context_fields)
    if existing:
        return existing
    write_trace(directory, idx, defn["id"], "main", message)
    text = invoke(directory, state, step, engine, message, opts, "main", skill, model, expected)
    write_atomic(out_path, text)
    try:
        return parse_step_output(text, defn["transmits"], context_fields, defn.get("output_field"))
    except ParseError as first:
        retry = build_retry_message(defn, idx, recipe["context_sheet"], text, first,
                                    recipe.get("context_definitions"))
        if not defn["reads_source"]:   # the retry goes back to the same step: one that reads the source may see it
            ensure_isolated(retry, directory, idx, admitted=admitted_text(state, recipe, idx))
        warn(f"étape '{defn['id']}' : {first} ; une relance sur la sortie produite")
        write_trace(directory, idx, defn["id"], "retry", retry)
        retry_text = invoke(directory, state, step, engine, retry, opts, "retry", skill, model, expected)
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
                    exempt_inputs(recipe, defn), admitted_text(state, recipe, idx))

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
    if path == "-":
        text = sys.stdin.read()
    else:
        try:
            text = Path(path).read_text(encoding="utf-8")
        except FileNotFoundError:
            raise ParcoursError(f"fichier introuvable : {Path(path).resolve()}") from None
        except IsADirectoryError:
            raise ParcoursError(f"c'est un dossier, pas un fichier : {path}") from None
        except UnicodeDecodeError:
            raise ParcoursError(f"fichier illisible en UTF-8 (texte attendu, pas un PDF ni un .docx) : {path}") from None
    if not text.strip():
        raise ParcoursError(f"fichier vide : {path}")
    return text


def cmd_new(args):
    recipe = load_recipe(args.recipe)
    if not recipe["format_declared"]:
        warn(f"recette '{recipe['id']}' : {FORMAT_MISSING}")
    text = read_text_arg(args.input)
    engine_steps = parse_engine_steps(args.engine_step, recipe)
    skills = resolve_recipe_skills(recipe)  # fail early, naming every missing skill
    base = Path(args.parcours_dir)
    base.mkdir(parents=True, exist_ok=True)
    # a slug stays within the page's whitelist (^[a-z0-9][a-z0-9-]{0,79}$): truncated, and the
    # default one when nothing ASCII is left (a title such as « 🚀 » or « — »)
    wanted = (slugify(args.slug)[:60].strip("-") if args.slug else "") or default_slug(recipe["id"], text)
    if wanted in RESERVED_SLUGS:   # <parcours-dir>/recettes may be the user's recueil, never a dossier
        wanted += "-dossier"
    directory, slug = create_unique_dir(base, wanted)
    title = " ".join((args.title or "").split())[:120] or None
    write_atomic(directory / "input.md", text)
    save_state(directory, new_state(recipe, slug, args.engine or "claude", engine_steps, skills, title))
    if args.json:
        emit_json({"slug": slug, "title": title})
        return 0
    say(f"Parcours créé : {slug} ({directory})")
    say(f"Suite : parcours.py next {slug}")
    return 0


def list_recipes(places=None, problems=None):
    """The workflow recipes of this repo, then the user's own (`personal`: true), for a page that
    creates parcours (`recipes --json`). A personal recipe that the runner cannot play, or that a
    recipe of the plugin shadows, is not offered: it goes to `problems` ([{id, message}]) instead."""
    found = []
    unreadable = (ParcoursError, OSError, ValueError) + ((yaml.YAMLError,) if yaml else ())
    plugin_ids, personal_ids = plugin_recipe_ids(), personal_recipe_ids(places)
    for recipe_id in sorted(plugin_ids | personal_ids):
        try:
            recipe = load_recipe(recipe_id, places)
            if recipe["origin"] != "plugin":
                fm, body, _, _ = recipe_origin(recipe_id, places)
                errors = workflow_errors(fm, body) + runner_errors(fm)
                if errors:
                    raise ParcoursError("; ".join(errors))
        except unreadable as exc:
            if recipe_id in personal_ids and recipe_id not in plugin_ids and problems is not None:
                problems.append({"id": recipe_id, "message": str(exc)})
            continue  # not a workflow recipe, or unreadable: not offered
        if recipe_id in personal_ids and recipe["origin"] == "plugin" and problems is not None:
            problems.append({"id": recipe_id, "message": "une recette du plugin porte le même id : "
                                                         "la vôtre est masquée, renommez-la"})
        found.append({
            "id": recipe["id"], "label": recipe["label"], "description": recipe["description"],
            "icon": recipe["icon"], "version": recipe["version"], "summary": recipe["summary"],
            "origin": recipe["origin"], "personal": recipe["origin"] != "plugin",
            "format": recipe["format"], "warnings": [] if recipe["format_declared"] else [FORMAT_MISSING],
            "steps": [{"id": s["id"], "label": s["label"], "pause": effective_pause(s),
                       "optional": s["optional"], "reads_source": s["reads_source"]} for s in recipe["steps"]],
        })
    return found


def cmd_formats(args):
    """The recipe formats this runner plays (docs/format-recette.md §2bis)."""
    if args.json:
        emit_json({"formats": list(RECIPE_FORMATS), "current": RECIPE_FORMAT, "source_format": SOURCE_FORMAT})
        return 0
    say(f"Formats de recette acceptés : {', '.join(str(f) for f in RECIPE_FORMATS)} "
        f"(une recette nouvelle est écrite au format {RECIPE_FORMAT}, au format {SOURCE_FORMAT} si une étape relit la source ; "
        f"sans champ format, elle est lue comme format {RECIPE_FORMAT})")
    return 0


def cmd_recipes(args):
    problems = []
    recipes = list_recipes(problems=problems)
    if args.json:
        emit_json({"recipes": recipes, "personal_problems": problems, "formats": list(RECIPE_FORMATS),
                   "recueil": str(PLACES["recueil"]) if PLACES.get("recueil") else None})
        return 0
    for r in recipes:
        mark = " [personnelle]" if r["personal"] else ""
        say(f"{r['id']} — {r['label']} ({len(r['steps'])} étapes){mark}")
        for warning in r["warnings"]:
            say(f"    avertissement : {warning}")
    for problem in problems:
        say(f"{problem['id']} — écartée : {problem['message']}")
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
            "unknown_fields": unknown, "pause": effective_pause(defn), "reads_source": defn["reads_source"],
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
            f"entrée ≈ {row['chars']} caractères{more}" + (" — relit la demande brute pour vérifier" if row["reads_source"] else ""))
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
            "reads_source": bool(defn and defn["reads_source"]),
            "transmits": list(step.get("transmits") or (defn["transmits"] if defn else [])),
            "output": step.get("output"), "summary": step.get("summary"), "handoff": step.get("handoff"),
            "blocking": step.get("blocking"), "error": step.get("error"),
            "cost_usd": step.get("cost_usd", 0.0), "started": step.get("started"), "ended": step.get("ended"),
            "skill": {k: (step.get("skill") or {}).get(k) for k in ("ref", "version")},
            "label": defn["label"] if defn else None, "mission": defn["mission"] if defn else None,
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
        "slug": state["slug"], "title": state.get("title"), "recipe": state["recipe"],
        "recipe_version": state["recipe_version"], "recipe_label": recipe["label"] if recipe else state["recipe"],
        "recipe_format": recipe["format"] if recipe else state.get("recipe_format"),
        "recipe_origin": recipe["origin"] if recipe else state.get("recipe_origin"),
        "recipe_sha256": state.get("recipe_sha256"),
        "recipe_current": bool(recipe and state.get("recipe_sha256") == recipe.get("source_sha256")),
        "created": state.get("created"), "status": state["status"],
        "engine": state["engine"], "engine_steps": state["engine_steps"],
        "cost_usd": state["cost_usd"], "calls": state["calls"],
        "context_sheet": state["context_sheet"], "context_validated": state["context_validated"],
        "context_fields": list(recipe["context_sheet"]) if recipe else [],
        "context_labels": dict(recipe["context_labels"]) if recipe else {}, "not_stated": NOT_STATED,
        "answers": state.get("answers"), "pending": state["pending"], "steps": steps,
        "files": files, "final_output": final, "recipe_error": problem,
        "locked": is_locked(directory), "fingerprint": fingerprint, "max_budget_usd": DEFAULT_BUDGET,
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
        subscription_calls=sum(n for e, n in calls.items() if e not in ("claude",) + FREE_ENGINES),
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


ARCHIVES = ".archives"   # hidden: never listed as a parcours, never a valid slug


def cmd_archive(args):
    """Move a parcours out of the list (<dir>/.archives/<slug>), not while a step runs."""
    directory = parcours_path(args)
    target_dir = Path(args.parcours_dir) / ARCHIVES
    target_dir.mkdir(exist_ok=True)
    with parcours_lock(directory):
        target, slug = create_unique_dir(target_dir, directory.name)
        target.rmdir()
        directory.rename(target)
    if args.json:
        emit_json({"archived": slug})
    else:
        say(f"Parcours archivé : {slug} ({target})")
    return 0


def cmd_unarchive(args):
    """Bring an archived parcours back into the list, under a free slug."""
    slug = args.slug
    if not slug or "/" in slug or slug.startswith("."):
        raise ParcoursError(f"identifiant de parcours invalide : '{slug}'")
    source = Path(args.parcours_dir) / ARCHIVES / slug
    if not (source / "state.json").is_file():
        raise NotFound(f"archive introuvable : {source}")
    target, restored = create_unique_dir(Path(args.parcours_dir), slug)
    target.rmdir()
    source.rename(target)
    if restored != slug:   # the parcours keeps the slug of its folder
        state = load_state(target)
        state["slug"] = restored
        save_state(target, state)
    if args.json:
        emit_json({"restored": restored})
    else:
        say(f"Parcours restauré : {restored}")
    return 0


def cmd_archives(args):
    """The archived parcours, most recent first (title, recipe, status, dates)."""
    base = Path(args.parcours_dir) / ARCHIVES
    items = []
    for entry in sorted(base.iterdir()) if base.is_dir() else []:
        try:
            state = json.loads((entry / "state.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        items.append({"slug": entry.name, "title": state.get("title"), "recipe": state.get("recipe"),
                      "status": state.get("status"), "created": state.get("created"),
                      "archived": datetime.fromtimestamp(entry.stat().st_mtime).isoformat(timespec="seconds")})
    items.sort(key=lambda i: i["archived"], reverse=True)
    if args.json:
        emit_json({"archives": items})
    else:
        for i in items:
            say(f"{i['slug']} — {i['title'] or i['recipe']} ({i['status']})")
    return 0


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
    common.add_argument("--parcours-dir", default=os.environ.get("PARCOURS_DIR") or "./parcours",
                        help="dossier des parcours (défaut : $PARCOURS_DIR, sinon ./parcours)")
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
    p.add_argument("--title", help="titre lisible du parcours (affiché par la page de suivi)")
    add("recipes", cmd_recipes, "les recettes-workflows disponibles")
    add("formats", cmd_formats, "les formats de recette que cet exécuteur sait jouer")
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
    add("archive", cmd_archive, "sortir un parcours de la liste (dossier .archives/)", "slug")
    add("unarchive", cmd_unarchive, "remettre un parcours archivé dans la liste", "slug")
    add("archives", cmd_archives, "les parcours archivés")
    p = add("handoff", cmd_handoff, "fournir ou corriger les champs à la main (étape en échec, terminée ou en pause)", "slug", "step")
    p.add_argument("--file", required=True)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    PLACES.update(recipe_places(args.parcours_dir))
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
