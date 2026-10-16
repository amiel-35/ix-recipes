import re, sys, unicodedata
from pathlib import Path
W = Path(sys.argv[1])
notes = (W / "notes.md").read_text()
norm = lambda s: re.sub(r"\s+", " ", unicodedata.normalize("NFC", s).replace("’", "'")).strip().lower()
NOTES = norm(notes)
groups_txt = (W / "parcours/bf4/01-regroupement.md").read_text().split("## HANDOFF")[1]
gids = {}
for m in re.finditer(r"\*\*G(\d) :(.*?)(?=\*\*G\d :|\*\*Non placés|## SUMMARY)", groups_txt, re.S):
    gids[m.group(1)] = set(re.findall(r"N\d{3}", m.group(2)))
received = set().union(*gids.values())
for run in ["s1/sans-1", "s2/sans-1", "a1/avec-1", "a2/avec-1"]:
    out = (W / "out" / f"{run}.md").read_text()
    quotes = [q.strip() for q in re.findall(r"«\s*(.+?)\s*»", out, re.S)]
    bad = [q for q in quotes if norm(q).replace("[…]", "") not in NOTES and not all(norm(p) in NOTES for p in re.split(r"\s*\[…\]\s*", q) if p)]
    ids = set(re.findall(r"N\d{3}", out))
    outside = sorted(ids - received)
    print(f"== {run}: {len(out.split())} mots, personas (titres ###/##): {len(re.findall(r'^#{2,3} .*(?:Persona|P\d|G\d)', out, re.M))}")
    print(f"   citations {len(quotes)}, absentes des notes {len(bad)} : {bad[:6]}")
    print(f"   identifiants cités {len(ids)}, hors des groupes reçus : {outside}")
    print(f"   'requalifi' : {out.lower().count('requalifi')} ; 'sources_read' : {'sources_read' in out}")
