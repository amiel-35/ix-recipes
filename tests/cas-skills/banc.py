#!/usr/bin/env python3
"""
Banc des skills métier : sans skill / avant / après, sur plusieurs réglages de modèle.

Pour chaque skill, chaque cas de tests/cas-skills/<id>.md, chaque version, chaque
réglage de modèle et chaque passage, le banc joue la demande du cas, puis fait noter
chaque sortie, seule et anonymisée, par un ou plusieurs juges. Il agrège par skill,
cas, réglage et version :

- le fond : critères de « Une bonne sortie contient » tenus ;
- la forme : critères de « Forme attendue » tenus, si le cas en a ;
- les erreurs relevées par le juge ;
- la stabilité de structure entre passages (mêmes titres et mêmes tableaux d'un
  passage à l'autre, de 0 à 1) : c'est souvent là qu'un skill gagne sur « pas de skill » ;
- le coût et la durée de chaque passage.

Versions :
    sans  : le même modèle, sans skill, avec une invite neutre
    avant : dist/skills/<id>/ au commit --base
    apres : dist/skills/<id>/ du dépôt

Réglages : `modèle[:effort]`, par exemple `sonnet:medium,sonnet:high,opus`.

Juges : `opus`, `sonnet` (CLI claude), `codex[:modèle]` (CLI Codex d'OpenAI), `agy[:modèle]` (CLI
Antigravity, Gemini par défaut). Des juges de plusieurs fournisseurs limitent le biais d'un juge
pour les sorties de son propre modèle.

Usage :
    python3 tests/cas-skills/banc.py --skills cgv-checker,ticket-triage \
        --versions sans,avant,apres --configs sonnet:medium,sonnet:high,opus \
        --cases 3 --passages 3 --judges opus,sonnet,codex,agy --out /tmp/banc

Ce qu'il faut : la CLI `claude` connectée et git ; bibliothèque standard seulement.
Le banc n'écrit rien dans le dépôt. Un passage ou une notation déjà présents dans
--out sont réutilisés : relancer la même commande reprend là où elle s'est arrêtée.

Idées reprises de l'exécuteur d'évaluations de romainsimon/paperasse (MIT) : comparer
avec et sans skill, réutiliser les passages déjà faits. Voir THIRD_PARTY.md.
"""

import argparse
import concurrent.futures as cf
import io
import itertools
import json
import random
import re
import shutil
import statistics
import subprocess
import sys
import tarfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CASES = REPO / "tests" / "cas-skills"

PREAMBLE = (
    "You are running the agent skill below. Its folder is the current directory: "
    "any file it mentions under references/ is at ./references/. Follow the skill to "
    "answer the user's request. Answer in the user's language. Produce the full "
    "deliverable in one answer; do not ask questions back unless the skill tells you to stop."
)
NEUTRAL = (
    "Answer the user's request in the user's language. Produce the full deliverable "
    "in one answer; do not ask questions back."
)

JUDGE = """Tu notes une réponse produite par un assistant à partir d'une demande d'utilisateur. Tu ne sais pas quel assistant l'a produite et tu n'as pas à le deviner.

Voici le cas : la demande, éventuellement des valeurs de référence, les critères de fond (« Une bonne sortie contient ») et, s'il y en a, les critères de forme (« Forme attendue »).

<cas>
{case}
</cas>

Voici la réponse à noter :

<reponse>
{answer}
</reponse>

Pour chaque critère numéroté : 1 si la réponse le remplit clairement, 0 sinon. Sois strict et constant : un critère à moitié rempli vaut 0 ; une phrase vague qui ne porte pas le fait attendu vaut 0. Vérifie les calculs contre les valeurs de référence et refais les additions. Relève les erreurs : chiffre faux, total faux, article de loi faux, inexistant ou abrogé, fait inventé sur les parties. Chacune compte, même si aucun critère ne la vise. Si tu n'es pas sûr qu'un point de droit soit faux, mets-le dans « douteux » et ne le compte pas comme erreur.

Réponds uniquement par un objet JSON, sans texte autour. « criteres » suit la liste « Une bonne sortie contient » ({n_crit} notes) ; « forme » suit la liste « Forme attendue » ({n_form} notes, liste vide s'il n'y en a pas) :
{{"criteres": [1, 0, ...], "forme": [1, 0, ...], "erreurs": ["..."], "douteux": ["..."], "commentaire": "une phrase sur les 0 les plus importants"}}
"""


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def numbered(block):
    return len(re.findall(r"^\d+\.\s", block, flags=re.M))


def parse_cases(skill):
    """Return [{n, case, request, n_crit, n_form}] from tests/cas-skills/<skill>.md."""
    text = (CASES / f"{skill}.md").read_text()
    parts = re.split(r"^# Cas (\d+)\b.*$", text, flags=re.M)
    cases = []
    for i in range(1, len(parts), 2):
        n, body = parts[i], parts[i + 1]
        body = body.split("\n## Résultats", 1)[0]
        body = body.split("\n## Une mauvaise sortie", 1)[0]
        if "## Une bonne sortie contient" not in body:
            continue
        good = body.split("## Une bonne sortie contient", 1)[1].split("\n## ", 1)[0]
        form = body.split("## Forme attendue", 1)[1].split("\n## ", 1)[0] if "## Forme attendue" in body else ""
        request = body.split("## Demande", 1)[1].split("\n## ", 1)[0]
        request = "\n".join(l[2:] if l.startswith("> ") else l.lstrip(">") for l in request.strip().splitlines())
        cases.append({"n": n, "case": body.strip(), "request": request.strip(),
                      "n_crit": numbered(good), "n_form": numbered(form)})
    return cases


def prepare(skill, base, versions, out):
    """Copy each version's skill folder into out/skills/ and write its system prompt."""
    dirs = {}
    for ver in versions:
        d = out / "skills" / f"{skill}-{ver}"
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        sp = out / "skills" / f"{skill}-{ver}.prompt.txt"
        if ver == "sans":
            sp.write_text(NEUTRAL + "\n")
        else:
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
            sp.write_text(f"{PREAMBLE}\n\n<skill>\n{(d / 'SKILL.md').read_text()}\n</skill>\n")
        dirs[ver] = (d, sp)
    return dirs


def cfg_args(cfg):
    model, _, effort = cfg.partition(":")
    return ["--model", model] + (["--effort", effort] if effort else [])


def cfg_name(cfg):
    return cfg.replace(":", "-")


def run_one(job):
    d, sp, request, cfg, dest = job
    meta = dest.with_suffix(".meta.json")
    if dest.exists() and dest.stat().st_size > 200 and meta.exists():
        return dest
    r = sh(["claude", "-p", *cfg_args(cfg), "--no-session-persistence",
            "--system-prompt-file", str(sp), "--strict-mcp-config", "--setting-sources", "",
            "--disable-slash-commands", "--tools", "Read", "--output-format", "json"],
           input=request, cwd=d, timeout=2400)
    try:
        data = json.loads(r.stdout)
        dest.write_text(data.get("result") or "")
        meta.write_text(json.dumps({"cout_usd": data.get("total_cost_usd"), "duree_ms": data.get("duration_ms"),
                                    "erreur": data.get("is_error")}, indent=1))
    except json.JSONDecodeError:
        dest.write_text(f"[ERREUR {r.returncode}]\n{r.stdout}\n{r.stderr}")
        meta.write_text(json.dumps({"erreur": True}))
    return dest


EMPTY = None


def ask_judge(judge, prompt, workdir):
    """Send the grading prompt to one judge and return its text answer.

    `opus`, `sonnet`, `haiku` (or any Claude model id): the claude CLI.
    `codex[:model]`: OpenAI Codex CLI, read-only sandbox, user config ignored, reasoning medium.
    `agy[:model]`: Antigravity CLI (default model gemini-3.8-flash-high).
    Codex and agy run from an empty folder so that no project file leaks into the prompt.
    """
    global EMPTY
    if EMPTY is None:
        EMPTY = workdir / "_vide"
        EMPTY.mkdir(exist_ok=True)
    kind, _, model = judge.partition(":")
    if kind == "codex":
        last = EMPTY / f"codex-{random.randrange(10**9)}.txt"
        cmd = ["codex", "exec", "--ephemeral", "--skip-git-repo-check", "--ignore-user-config", "-s", "read-only",
               "-c", 'model_reasoning_effort="medium"', "-o", str(last)] + (["-m", model] if model else []) + ["-"]
        r = sh(cmd, input=prompt, cwd=EMPTY, timeout=2400)
        text = last.read_text() if last.exists() else ""
        last.unlink(missing_ok=True)
        return text or r.stdout[-500:] + r.stderr[-500:]
    if kind == "agy":
        r = sh(["agy", "-p", prompt, "--model", model or "gemini-3.8-flash-high", "--output-format", "text",
                "--disable-slash-commands"], cwd=EMPTY, timeout=2400)
        return r.stdout or r.stderr[-800:]
    r = sh(["claude", "-p", "--model", judge, "--no-session-persistence",
            "--strict-mcp-config", "--setting-sources", "", "--disable-slash-commands", "--tools", ""],
           input=prompt, timeout=2400)
    return r.stdout


def judge_one(job):
    case, answer_path, judge_model, dest = job
    if dest.exists() and '"echec"' not in dest.read_text():
        return dest  # a failed grading (quota, timeout) is retried on the next run
    prompt = JUDGE.format(case=case["case"], answer=answer_path.read_text(),
                          n_crit=case["n_crit"], n_form=case["n_form"])
    out = ""
    for _ in range(2):
        out = ask_judge(judge_model, prompt, dest.parent)
        m = re.search(r"\{.*\}", out, flags=re.S)
        if m:
            try:
                data = json.loads(m.group(0))
                dest.write_text(json.dumps(data, ensure_ascii=False, indent=1))
                return dest
            except json.JSONDecodeError:
                pass
    dest.write_text(json.dumps({"echec": out[-2000:]}, ensure_ascii=False))
    return dest


def structure(text):
    """The skeleton of an answer: its headings, bold labels and the header rows of its tables."""
    sig = set()
    lines = text.splitlines()
    for i, l in enumerate(lines):
        s = l.strip()
        if s.startswith("#"):
            sig.add("h:" + re.sub(r"[^a-z0-9àâçéèêëîïôûùüÿœ ]", "", s.lstrip("#").strip().lower())[:40])
        elif re.fullmatch(r"\*\*[^*]{2,60}\*\*:?", s):
            sig.add("b:" + s.strip("*: ").lower()[:40])
        elif s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*:?-{2,}", lines[i + 1].strip()):
            sig.add("t:" + "|".join(c.strip().lower()[:20] for c in s.strip("|").split("|")))
    return sig


def stability(texts):
    sigs = [structure(t) for t in texts if t.strip()]
    if len(sigs) < 2:
        return None
    vals = [len(a & b) / len(a | b) if (a | b) else 1.0 for a, b in itertools.combinations(sigs, 2)]
    return statistics.mean(vals)


def fmt(values, digits=1):
    values = [v for v in values if v is not None]
    if not values:
        return "—"
    m = statistics.mean(values)
    return f"{m:.{digits}f} ({min(values):.{digits}f}–{max(values):.{digits}f})" if len(values) > 1 else f"{m:.{digits}f}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skills", required=True, help="ids séparés par des virgules")
    ap.add_argument("--base", default="cbe271c", help="commit de la version « avant »")
    ap.add_argument("--versions", default="avant,apres", help="parmi sans, avant, apres")
    ap.add_argument("--configs", "--models", dest="configs", default="sonnet,haiku", help="modèle[:effort], séparés par des virgules")
    ap.add_argument("--passages", type=int, default=3)
    ap.add_argument("--cases", default="", help="numéros de cas (défaut : tous)")
    ap.add_argument("--judges", "--judge", dest="judges", default="opus", help="modèles juges, séparés par des virgules")
    ap.add_argument("--jobs", type=int, default=6)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    out = Path(a.out).resolve()
    for sub in ("sorties", "anonymes", "notes"):
        (out / sub).mkdir(parents=True, exist_ok=True)
    skills = [s.strip() for s in a.skills.split(",") if s.strip()]
    versions = [v.strip() for v in a.versions.split(",") if v.strip()]
    configs = [c.strip() for c in a.configs.split(",") if c.strip()]
    judges = [j.strip() for j in a.judges.split(",") if j.strip()]
    wanted = {c.strip() for c in a.cases.split(",") if c.strip()}

    jobs, meta = [], []
    for skill in skills:
        dirs = prepare(skill, a.base, versions, out)
        for case in parse_cases(skill):
            if wanted and case["n"] not in wanted:
                continue
            for ver, (d, sp) in dirs.items():
                for cfg in configs:
                    for p in range(1, a.passages + 1):
                        dest = out / "sorties" / f"{skill}__c{case['n']}__{ver}__{cfg_name(cfg)}__p{p}.md"
                        jobs.append((d, sp, case["request"], cfg, dest))
                        meta.append({"skill": skill, "case": case, "ver": ver, "cfg": cfg_name(cfg), "p": p, "out": dest})

    print(f"{len(jobs)} passages à jouer…", flush=True)
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for i, _ in enumerate(ex.map(run_one, jobs), 1):
            if i % 10 == 0 or i == len(jobs):
                print(f"  {i}/{len(jobs)}", flush=True)

    # Anonymise: a judge sees a random label, never the file name.
    key_path = out / "cle.json"
    key = json.loads(key_path.read_text()) if key_path.exists() else {}
    rev = {v: k for k, v in key.items()}
    rng = random.Random()
    judge_jobs = []
    for m in meta:
        name = m["out"].name
        label = rev.get(name) or f"R{rng.randrange(10**8):08d}"
        key[label] = name
        anon = out / "anonymes" / f"{label}.md"
        shutil.copy(m["out"], anon)
        m["label"] = label
        for j in judges:
            judge_jobs.append((m["case"], anon, j, out / "notes" / f"{label}__{j.replace(':', '-')}.json"))
    key_path.write_text(json.dumps(key, indent=1))
    rng.shuffle(judge_jobs)

    print(f"{len(judge_jobs)} notations…", flush=True)
    with cf.ThreadPoolExecutor(a.jobs) as ex:
        for i, _ in enumerate(ex.map(judge_one, judge_jobs), 1):
            if i % 10 == 0 or i == len(judge_jobs):
                print(f"  {i}/{len(judge_jobs)}", flush=True)

    # Aggregate: one value per passage = mean over judges.
    groups = {}
    disagreement = []
    for m in meta:
        k = (m["skill"], m["case"]["n"], m["cfg"], m["ver"])
        g = groups.setdefault(k, {"fond": [], "forme": [], "err": [], "cout": [], "duree": [], "texts": [],
                                  "n_crit": m["case"]["n_crit"], "n_form": m["case"]["n_form"]})
        notes = []
        for j in judges:
            p = out / "notes" / f"{m['label']}__{j.replace(':', '-')}.json"
            data = json.loads(p.read_text()) if p.exists() else {}
            if "criteres" in data:
                notes.append(data)
        if notes:
            fond = [sum(n["criteres"]) for n in notes]
            g["fond"].append(statistics.mean(fond))
            if m["case"]["n_form"]:
                g["forme"].append(statistics.mean(sum(n.get("forme", [])) for n in notes))
            g["err"].append(statistics.mean(len(n.get("erreurs", [])) for n in notes))
            if len(fond) > 1:
                disagreement.append(max(fond) - min(fond))
        mp = m["out"].with_suffix(".meta.json")
        md = json.loads(mp.read_text()) if mp.exists() else {}
        g["cout"].append(md.get("cout_usd"))
        g["duree"].append((md.get("duree_ms") or 0) / 1000 or None)
        g["texts"].append(m["out"].read_text())

    lines = [f"# Banc — base {a.base}, {a.passages} passage(s), juge(s) {', '.join(judges)}", "",
             "Moyenne (min–max) sur les passages ; chaque passage est la moyenne des juges. Stabilité : ressemblance "
             "de la structure (titres, tableaux) entre passages, de 0 à 1. Une sortie plus longue offre plus de prise "
             "aux erreurs : lire les erreurs avec les critères.", "",
             "| Skill | Cas | Réglage | Version | Fond | Forme | Erreurs | Stabilité | Coût ($) | Durée (s) |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    order = {v: i for i, v in enumerate(["sans", "avant", "apres"])}
    for k in sorted(groups, key=lambda k: (skills.index(k[0]), k[1], k[2], order.get(k[3], 9))):
        g = groups[k]
        forme = f"{fmt(g['forme'])} /{g['n_form']}" if g["n_form"] else "—"
        lines.append(f"| `{k[0]}` | {k[1]} | {k[2]} | {k[3]} | {fmt(g['fond'])} /{g['n_crit']} | {forme} | "
                     f"{fmt(g['err'])} | {fmt([stability(g['texts'])], 2)} | {fmt(g['cout'], 3)} | {fmt(g['duree'], 0)} |")
    per_judge = {}
    for m in meta:
        for j in judges:
            p = out / "notes" / f"{m['label']}__{j.replace(':', '-')}.json"
            data = json.loads(p.read_text()) if p.exists() else {}
            if "criteres" in data:
                per_judge.setdefault(j, {}).setdefault(m["ver"], []).append(sum(data["criteres"]) / max(1, m["case"]["n_crit"]))
    if len(judges) > 1 and per_judge:
        lines += ["", "Note moyenne de fond par juge (part des critères tenus, toutes sorties) :", "",
                  "| Juge | " + " | ".join(versions) + " |", "|---|" + "---|" * len(versions)]
        for j in judges:
            row = per_judge.get(j, {})
            lines.append(f"| {j} | " + " | ".join(f"{statistics.mean(row[v]):.2f}" if row.get(v) else "—" for v in versions) + " |")
    if disagreement:
        lines += ["", f"Écart entre juges sur le fond, par sortie : moyenne {statistics.mean(disagreement):.2f} critère, "
                      f"maximum {max(disagreement):.1f}."]
    rapport = out / "rapport.md"
    rapport.write_text("\n".join(lines) + "\n")
    print(rapport)
    print("\n".join(lines))


if __name__ == "__main__":
    sys.exit(main())
