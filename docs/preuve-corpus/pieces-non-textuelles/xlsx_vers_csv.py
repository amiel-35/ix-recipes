"""Essai de conversion .xlsx -> un .csv par onglet, bibliothèque standard seule (decision-corpus.md §8).

Script d'essai, pas du code de production : il montre ce que la création du dossier aurait à faire.
    python3 xlsx_vers_csv.py classeur.xlsx <dossier de sortie>
Écrit <classeur>.<onglet>.csv et affiche les avertissements (formule sans valeur calculée, etc.).
"""
import csv
import datetime
import posixpath
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}
BUILTIN_DATE_FORMATS = set(range(14, 23)) | {45, 46, 47}


def col_index(ref):
    letters = re.match(r"[A-Z]+", ref).group()
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def text_of(si):
    return "".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t"))


def date_styles(z):
    """Indices de cellXfs dont le format est une date."""
    if "xl/styles.xml" not in z.namelist():
        return set()
    root = ET.fromstring(z.read("xl/styles.xml"))
    custom = {int(f.get("numFmtId")): f.get("formatCode", "")
              for f in root.iterfind("m:numFmts/m:numFmt", NS)}
    dates = set()
    for i, xf in enumerate(root.iterfind("m:cellXfs/m:xf", NS)):
        fid = int(xf.get("numFmtId", 0))
        code = re.sub(r'"[^"]*"|\[[^\]]*\]', "", custom.get(fid, "")).lower()
        if fid in BUILTIN_DATE_FORMATS or (fid in custom and re.search(r"[dy]|m{3,}", code)):
            dates.add(i)
    return dates


def convert(path, out_dir):
    warnings = []
    out_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            shared = [text_of(si) for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iterfind("m:si", NS)]
        dates = date_styles(z)
        rels = {r.get("Id"): r.get("Target")
                for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).iterfind("pr:Relationship", NS)}
        workbook = ET.fromstring(z.read("xl/workbook.xml"))
        epoch = datetime.date(1904, 1, 1) if workbook.find("m:workbookPr[@date1904='1']", NS) is not None \
            else datetime.date(1899, 12, 30)
        written = []
        for sheet in workbook.iterfind("m:sheets/m:sheet", NS):
            name = sheet.get("name")
            target = rels[sheet.get(f"{{{NS['r']}}}id")]
            part = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))
            root = ET.fromstring(z.read(part))
            rows = []
            for row in root.iterfind("m:sheetData/m:row", NS):
                values = {}
                for c in row.iterfind("m:c", NS):
                    ref, kind, style = c.get("r"), c.get("t", "n"), int(c.get("s", 0))
                    v, f = c.find("m:v", NS), c.find("m:f", NS)
                    if kind == "s":
                        val = shared[int(v.text)]
                    elif kind == "inlineStr":
                        val = text_of(c.find("m:is", NS))
                    elif v is None:
                        val = ""
                        if f is not None:
                            warnings.append(f"{name}!{ref} : formule ={f.text} sans valeur calculée (fichier "
                                            "jamais ouvert dans un tableur ?) ; cellule laissée vide")
                    elif kind == "b":
                        val = "VRAI" if v.text == "1" else "FAUX"
                    elif kind in ("str", "e"):
                        val = v.text or ""
                    elif style in dates:
                        val = (epoch + datetime.timedelta(days=float(v.text))).isoformat()
                    else:
                        num = float(v.text)
                        val = str(int(num)) if num.is_integer() else v.text
                    values[col_index(ref)] = val
                r = int(row.get("r")) - 1
                while len(rows) < r:
                    rows.append([])
                rows.append([values.get(i, "") for i in range(max(values) + 1)] if values else [])
            merged = [m.get("ref") for m in root.iterfind("m:mergeCells/m:mergeCell", NS)]
            if merged:
                warnings.append(f"{name} : cellules fusionnées {', '.join(merged)} — valeur dans la première "
                                "cellule seulement")
            dest = out_dir / f"{Path(path).stem}.{name}.csv"
            with dest.open("w", newline="", encoding="utf-8") as fh:
                csv.writer(fh).writerows(rows)
            written.append(dest)
    return written, warnings


if __name__ == "__main__":
    files, warns = convert(sys.argv[1], Path(sys.argv[2]))
    for f in files:
        print(f"écrit : {f}")
    for w in warns:
        print(f"avertissement : {w}")
