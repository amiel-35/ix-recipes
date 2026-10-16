"""Rejoue l'étape persona du test de dérive (grille.md), avec ou sans corpus, sans toucher à l'exécuteur.

Script d'essai, pas du code de production. Le message est celui que l'exécuteur a construit pour l'étape
(capturé par le moteur `fake`, `02-personas.in.md`). Variante `avec` : le dossier jetable reçoit
`corpus/<pièces>` et le message les deux phrases que proposerait l'exécuteur (decision-corpus.md §5),
plus la section `### sources_read`. Options de l'exécuteur (engine_argv), sortie stream-json.
    python3 rejouer.py <message.in.md> <sans|avec> <dossier de sortie> [pièce…]
Écrit <sortie>/<variante>-<n>.jsonl, .md (la sortie) et .reads.txt (chaque Read et son résultat).
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ANNONCE = ("The dossier's pieces are in ./corpus/, in your current working directory: {names}. "
           "Consult them only for what your mission needs; cite them as `file:line` "
           "(or by the note id when the line carries one).")
SOURCES_READ = ("In the HANDOFF block, add a `### sources_read` sub-section: the corpus files you read "
                "(with the parts you used) and those you did not open.")


def message_for(text, variant, names):
    if variant == "sans":
        return text
    anchor = "=== MISSION ==="
    text = text.replace(anchor, ANNONCE.format(names=", ".join(names)) + "\n\n" + anchor, 1)
    return text.replace("## SUMMARY\n(5 lines at most)", SOURCES_READ + "\n\n## SUMMARY\n(5 lines at most)", 1)


def reads_of(events):
    results = {}
    for ev in events:
        if ev.get("type") == "user":
            for b in ev.get("message", {}).get("content", []):
                if isinstance(b, dict) and b.get("type") == "tool_result":
                    c = b.get("content")
                    if isinstance(c, list):
                        c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
                    results[b.get("tool_use_id")] = (b.get("is_error", False), str(c))
    out = []
    for ev in events:
        if ev.get("type") == "assistant":
            for b in ev.get("message", {}).get("content", []):
                if b.get("type") == "tool_use":
                    err, res = results.get(b["id"], (None, ""))
                    out.append(f"{json.dumps(b.get('input'), ensure_ascii=False)} -> "
                               f"{'ERREUR' if err else 'ok'} ({len(res)} car.) {res[:200]!r}")
    return out


def main():
    msg_file, variant, out_dir, *pieces = sys.argv[1:]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    n = 1 + len(list(out.glob(f"{variant}-*.md")))
    work = Path(tempfile.mkdtemp(prefix="parcours-"))
    try:
        if variant == "avec":
            (work / "corpus").mkdir()
            for p in pieces:
                shutil.copy(p, work / "corpus")
        message = message_for(Path(msg_file).read_text(encoding="utf-8"), variant, [Path(p).name for p in pieces])
        (out / f"{variant}-{n}.in.md").write_text(message, encoding="utf-8")
        argv = [shutil.which("claude") or "claude", "-p", "--model", "sonnet", "--output-format", "stream-json",
                "--verbose", "--tools", "Read", "--setting-sources", "", "--no-session-persistence",
                "--disable-slash-commands", "--max-budget-usd", "1"]
        proc = subprocess.run(argv, input=message, capture_output=True, text=True, cwd=work, timeout=900)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    (out / f"{variant}-{n}.jsonl").write_text(proc.stdout, encoding="utf-8")
    events = [json.loads(line) for line in proc.stdout.splitlines() if line.strip().startswith("{")]
    result = next((e for e in reversed(events) if e.get("type") == "result"), {})
    (out / f"{variant}-{n}.md").write_text(result.get("result", ""), encoding="utf-8")
    (out / f"{variant}-{n}.reads.txt").write_text("\n".join(reads_of(events)) + "\n", encoding="utf-8")
    print(f"{variant}-{n} : code {proc.returncode}, {len(reads_of(events))} lecture(s), "
          f"{result.get('total_cost_usd', 0):.4f} $")


if __name__ == "__main__":
    main()
