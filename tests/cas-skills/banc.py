#!/usr/bin/env python3
"""
Banc avant / après des skills métier, à plusieurs passages.

Pour chaque skill, chaque cas de tests/cas-skills/<id>.md, chaque modèle et
chaque passage, le banc joue la version « avant » (dist/skills/<id>/ à un
commit de référence) et la version « après » (dist/skills/<id>/ du dépôt),
puis fait noter chaque sortie, seule et anonymisée, par un juge. Il agrège
les notes par version et par modèle : moyenne, minimum, maximum.

Usage :
    python3 tests/cas-skills/banc.py --skills cgv-checker,ticket-triage \
        --base cbe271c --models sonnet,haiku --passages 3 --out /tmp/banc

Ce qu'il faut : la CLI `claude` (connectée) et git. Rien d'autre que la
bibliothèque standard. Le banc n'écrit rien dans le dépôt : tout va dans --out.

Chaque passage lance `claude -p` depuis une copie du dossier du skill, avec le
skill pour seule invite système et l'outil Lecture pour seul outil (le modèle
peut lire references/). Le juge (`claude -p --model <juge>`) ne voit qu'une
sortie à la fois, sans savoir quelle version ni quel modèle l'a produite, et
rend un JSON : une note 0/1 par critère et la liste des erreurs.
"""

import argparse
import concurrent.futures as cf
import json
import random
import re
import shutil
import statistics
import subprocess
import sys
import tarfile
import io
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CASES = REPO / "tests" / "cas-skills"

PREAMBLE = (
    "You are running the agent skill below. Its folder is the current directory: "
    "any file it mentions under references/ is at ./references/. Follow the skill to "
    "answer the user's request. Answer in the user's language. Produce the full "
    "deliverable in one answer; do not ask questions back unless the skill tells you to stop."
)

JUDGE = """Tu notes une réponse produite par un assistant à partir d'une demande d'utilisateur. Tu ne sais pas quel assistant l'a produite et tu n'as pas à le deviner.

Voici le cas : la demande, éventuellement des valeurs de référence, et les critères d'une bonne sortie.

<cas>
{case}
</cas>

Voici la réponse à noter :

<reponse>
{answer}
</reponse>

Pour chaque critère numéroté : 1 si la réponse le remplit clairement, 0 sinon. Sois strict et constant : un critère à moitié rempli vaut 0 ; une phrase vague qui ne porte pas le fait attendu vaut 0. Vérifie les calculs contre les valeurs de référence et refais les additions. Relève les erreurs : chiffre faux, total faux, article de loi faux, inexistant ou abrogé, fait inventé sur les parties. Chacune compte, même si aucun critère ne la vise. Si tu n'es pas sûr qu'un point de droit soit faux, mets-le dans « douteux » et ne le compte pas comme erreur.

Réponds uniquement par un objet JSON, sans texte autour :
{{"criteres": [1, 0, ...], "erreurs": ["..."], "douteux": ["..."], "commentaire": "une phrase sur les 0 les plus importants"}}
"""


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def parse_cases(skill):
    """Return [(n, case_text, n_criteria)] from tests/cas-skills/<skill>.md."""
    text = (CASES / f"{skill}.md").read_text()
    parts = re.split(r"^# Cas (\d+)\b.*$", text, flags=re.M)
    cases = []
    for i in range(1, len(parts), 2):
        n, body = parts[i], parts[i + 1]
        body = body.split("\n## Résultats", 1)[0]
        body = body.split("\n## Une mauvaise sortie", 1)[0]
        crit = body.split("## Une bonne sortie contient", 1)
        if len(crit) < 2:
            continue
        n_crit = len(re.findall(r"^\d+\.\s", crit[1], flags=re.M))
        request = body.split("## Demande", 1)[1].split("\n## ", 1)[0]
        request = "\n".join(l[2:] if l.startswith("> ") else l.lstrip(">") for l in request.strip().splitlines())
        cases.append({"n": n, "case": body.strip(), "request": request.strip(), "n_crit": n_crit})
    return cases


def prepare(skill, base, out):
    """Copy the before / after skill folders into out/skills/."""
    dirs = {}
    for ver in ("avant", "apres"):
        d = out / "skills" / f"{skill}-{ver}"
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        if ver == "avant":
            r = subprocess.run(["git", "-C", str(REPO), "archive", base, f"dist/skills/{skill}"], capture_output=True)
            if r.returncode != 0:
                raise SystemExit(f"{skill} absent de {base}: {r.stderr.decode()}")
            with tarfile.open(fileobj=io.BytesIO(r.stdout)) as tar:
                for m in tar.getmembers():
                    if not m.isfile():
                        continue
                    rel = Path(m.name).relative_to(f"dist/skills/{skill}")
                    (d / rel).parent.mkdir(parents=True, exist_ok=True)
                    (d / rel).write_bytes(tar.extractfile(m).read())
        else:
            shutil.copytree(REPO / "dist" / "skills" / skill, d, dirs_exist_ok=True)
        sp = out / "skills" / f"{skill}-{ver}.prompt.txt"
        sp.write_text(f"{PREAMBLE}\n\n<skill>\n{(d / 'SKILL.md').read_text()}\n</skill>\n")
        dirs[ver] = (d, sp)
    return dirs


def run_one(job):
    d, sp, request, model, dest = job
    if dest.exists() and dest.stat().st_size > 200:
        return dest
    r = sh(["claude", "-p", "--model", model, "--no-session-persistence",
            "--system-prompt-file", str(sp), "--strict-mcp-config", "--setting-sources", "",
            "--disable-slash-commands", "--tools", "Read"],
           input=request, cwd=d, timeout=1800)
    dest.write_text(r.stdout if r.returncode == 0 else f"[ERREUR {r.returncode}]\n{r.stdout}\n{r.stderr}")
    return dest


def judge_one(job):
    case_text, answer_path, judge_model, dest = job
    if dest.exists():
        return dest
    prompt = JUDGE.format(case=case_text, answer=answer_path.read_text())
    for _ in range(2):
        r = sh(["claude", "-p", "--model", judge_model, "--no-session-persistence",
                "--strict-mcp-config", "--setting-sources", "", "--disable-slash-commands", "--tools", ""],
               input=prompt, timeout=1800)
        m = re.search(r"\{.*\}", r.stdout, flags=re.S)
        if m:
            try:
                data = json.loads(m.group(0))
                dest.write_text(json.dumps(data, ensure_ascii=False, indent=1))
                return dest
            except json.JSONDecodeError:
                pass
    dest.write_text(json.dumps({"echec": r.stdout[-2000:]}, ensure_ascii=False))
    return dest


def fmt(values):
    if not values:
        return "—"
    m = statistics.mean(values)
    return f"{m:.1f} ({min(values)}–{max(values)})" if len(values) > 1 else f"{m:.1f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skills", required=True, help="ids séparés par des virgules")
    ap.add_argument("--base", default="cbe271c", help="commit de la version « avant »")
    ap.add_argument("--models", default="sonnet,haiku")
    ap.add_argument("--passages", type=int, default=3)
    ap.add_argument("--cases", default="", help="numéros de cas (défaut : tous)")
    ap.add_argument("--judge", default="opus")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    out = Path(a.out).resolve()
    (out / "sorties").mkdir(parents=True, exist_ok=True)
    (out / "anonymes").mkdir(exist_ok=True)
    (out / "notes").mkdir(exist_ok=True)
    skills = [s.strip() for s in a.skills.split(",") if s.strip()]
    models = [m.strip() for m in a.models.split(",") if m.strip()]
    wanted = {c.strip() for c in a.cases.split(",") if c.strip()}

    jobs, meta = [], []
    for skill in skills:
        dirs = prepare(skill, a.base, out)
        for case in parse_cases(skill):
            if wanted and case["n"] not in wanted:
                continue
            for ver, (d, sp) in dirs.items():
                for model in models:
                    for p in range(1, a.passages + 1):
                        dest = out / "sorties" / f"{skill}__c{case['n']}__{ver}__{model}__p{p}.md"
                        jobs.append((d, sp, case["request"], model, dest))
                        meta.append({"skill": skill, "case": case, "ver": ver, "model": model, "p": p, "out": dest})

    print(f"{len(jobs)} passages à jouer…", flush=True)
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for i, _ in enumerate(ex.map(run_one, jobs), 1):
            if i % 10 == 0 or i == len(jobs):
                print(f"  {i}/{len(jobs)}", flush=True)

    # Anonymise: the judge sees a random label, never the file name.
    key_path = out / "cle.json"
    key = json.loads(key_path.read_text()) if key_path.exists() else {}
    rev = {v: k for k, v in key.items()}
    rng = random.Random()
    judge_jobs = []
    for m in meta:
        name = m["out"].name
        label = rev.get(name)
        if not label:
            label = f"R{rng.randrange(10**8):08d}"
            key[label] = name
        anon = out / "anonymes" / f"{label}.md"
        shutil.copy(m["out"], anon)
        m["label"] = label
        judge_jobs.append((m["case"]["case"], anon, a.judge, out / "notes" / f"{label}.json"))
    key_path.write_text(json.dumps(key, indent=1))
    rng.shuffle(judge_jobs)

    print(f"{len(judge_jobs)} notations…", flush=True)
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for i, _ in enumerate(ex.map(judge_one, judge_jobs), 1):
            if i % 10 == 0 or i == len(judge_jobs):
                print(f"  {i}/{len(judge_jobs)}", flush=True)

    # Aggregate.
    table = {}
    for m in meta:
        data = json.loads((out / "notes" / f"{m['label']}.json").read_text())
        if "criteres" not in data:
            continue
        k = (m["skill"], m["case"]["n"], m["case"]["n_crit"], m["model"], m["ver"])
        t = table.setdefault(k, {"score": [], "err": []})
        t["score"].append(sum(data["criteres"]))
        t["err"].append(len(data.get("erreurs", [])))

    lines = [f"# Banc avant / après — base {a.base}, {a.passages} passage(s), juge {a.judge}", "",
             "Moyenne (min–max) des critères tenus et du nombre d'erreurs relevées, sur les passages.",
             "Le juge note chaque sortie seule : une sortie plus longue, qui calcule ou affirme davantage, offre plus de prise aux erreurs. Lire les erreurs avec les critères, pas seules.", "",
             "| Skill | Cas | Modèle | Avant : critères | Après : critères | Avant : erreurs | Après : erreurs |",
             "|---|---|---|---|---|---|---|"]
    for skill in skills:
        for (s, n, nc, model, ver) in sorted({(k[0], k[1], k[2], k[3], None) for k in table if k[0] == skill}):
            av = table.get((s, n, nc, model, "avant"), {"score": [], "err": []})
            ap_ = table.get((s, n, nc, model, "apres"), {"score": [], "err": []})
            lines.append(f"| `{s}` | {n} (/{nc}) | {model} | {fmt(av['score'])} | {fmt(ap_['score'])} | {fmt(av['err'])} | {fmt(ap_['err'])} |")
    rapport = out / "rapport.md"
    rapport.write_text("\n".join(lines) + "\n")
    print(rapport)
    print("\n".join(lines))


if __name__ == "__main__":
    sys.exit(main())
