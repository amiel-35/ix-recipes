"""Joue les essais « pièces non textuelles » : un appel `claude -p` par pièce, dans un dossier jetable
qui ne contient que la pièce, avec les options de l'exécuteur (scripts/parcours.py, engine_argv),
sauf la sortie : stream-json, pour garder chaque Read et ce que l'outil a répondu.

Script d'essai, pas du code de production.
    python3 lancer.py [essai…]      # sans argument : tous les essais
Écrit traces/<essai>.jsonl (flux complet) et traces/<essai>.md (lectures, réponse, coût).
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
CONSIGNE = ("Le dossier courant contient la ou les pièces d'un dossier : {pieces}. Lis-les avec l'outil Read. "
            "Si une lecture échoue, dis exactement ce que l'outil a répondu et n'invente rien. ")
ESSAIS = {
    "contrat-pdf": (["pieces/contrat.pdf"],
                    "Réponds : (a) le prix HT du noyer (NO-40) ; (b) le préavis de résiliation ; (c) le plafond "
                    "des pénalités de retard. Pour chaque réponse, donne la page et une citation courte. "
                    "(d) Comment citerais-tu ces passages pour qu'un lecteur les retrouve (fichier, page, ligne) ?"),
    "pdf-25-pages": (["pieces/annexe-25-pages.pdf"],
                     "Quel est le délai de garantie des ouvrages, et à quelle page figure-t-il ? "
                     "Dis combien de lectures il t'a fallu et ce que l'outil a répondu à chacune."),
    "pdf-scanne": (["pieces/avenant-scanne.pdf"],
                   "Quel nouveau prix fixe ce document, pour quelle référence, et à partir de quand ? "
                   "Cite le passage."),
    # le même PDF long, sans poppler (pdftoppm) dans le PATH : cas d'un poste sans Homebrew
    "pdf-25-pages-sans-poppler": (["pieces/annexe-25-pages.pdf"],
                                  "Quel est le délai de garantie des ouvrages, et à quelle page figure-t-il ? "
                                  "Dis combien de lectures il t'a fallu et ce que l'outil a répondu à chacune.",
                                  {"PATH": "/usr/bin:/bin:/usr/sbin:/sbin"}),
    "xlsx": (["pieces/budget-t3.xlsx"],
             "Réponds : (a) l'écart marketing ; (b) le total des charges, budget et réel ; (c) la date d'arrêté ; "
             "(d) la cause de l'écart marketing, si le classeur la donne."),
    "csv-converti": (["converti/budget-t3.T3.csv", "converti/budget-t3.Commentaires.csv"],
                     "Réponds : (a) l'écart marketing ; (b) le total des charges, budget et réel ; (c) la date "
                     "d'arrêté ; (d) la cause de l'écart marketing. Cite chaque valeur par fichier:ligne."),
}


def argv():
    return [shutil.which("claude") or "claude", "-p", "--model", "sonnet", "--output-format", "stream-json", "--verbose",
            "--tools", "Read", "--setting-sources", "", "--no-session-persistence",
            "--disable-slash-commands", "--max-budget-usd", "0.5"]


def summarize(events):
    reads, answer, cost = [], "", 0.0
    results = {}
    for ev in events:
        if ev.get("type") == "user":
            for block in ev.get("message", {}).get("content", []):
                if isinstance(block, dict) and block.get("type") == "tool_result":
                    content = block.get("content")
                    if isinstance(content, list):
                        content = " ".join(c.get("text", f"[{c.get('type')}]") for c in content if isinstance(c, dict))
                    results[block.get("tool_use_id")] = (block.get("is_error", False), str(content)[:400])
    for ev in events:
        if ev.get("type") == "assistant":
            for block in ev.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    err, res = results.get(block["id"], (None, "(pas de résultat)"))
                    reads.append((json.dumps(block.get("input"), ensure_ascii=False), err, res))
        if ev.get("type") == "result":
            answer, cost = ev.get("result", ""), ev.get("total_cost_usd", 0.0)
    return reads, answer, cost


def run(name):
    pieces, question, *env = ESSAIS[name]
    env = {**os.environ, **env[0]} if env else None
    work = Path(tempfile.mkdtemp(prefix="corpus-essai-"))
    try:
        for p in pieces:
            shutil.copy(HERE / p, work)
        names = ", ".join(Path(p).name for p in pieces)
        prompt = CONSIGNE.format(pieces=names) + question
        proc = subprocess.run(argv(), input=prompt, capture_output=True, text=True, cwd=work, timeout=600, env=env)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    traces = HERE / "traces"
    traces.mkdir(exist_ok=True)
    (traces / f"{name}.jsonl").write_text(proc.stdout, encoding="utf-8")
    events = [json.loads(line) for line in proc.stdout.splitlines() if line.strip().startswith("{")]
    reads, answer, cost = summarize(events)
    lines = [f"# Essai {name}", "", f"Pièces : {names}  ", f"Code de sortie : {proc.returncode} ; coût : {cost:.4f} $",
             "", "## Consigne", "", prompt, "", "## Lectures (flux stream-json)", ""]
    for inp, err, res in reads:
        lines.append(f"- `Read {inp}` → {'ERREUR' if err else 'ok'} : {res!r}")
    lines += ["", "## Réponse", "", answer, ""]
    if proc.stderr.strip():
        lines += ["## stderr", "", "```", proc.stderr.strip()[-1500:], "```", ""]
    (traces / f"{name}.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"{name} : code {proc.returncode}, {len(reads)} lecture(s), {cost:.4f} $")


if __name__ == "__main__":
    for essai in sys.argv[1:] or ESSAIS:
        run(essai)
