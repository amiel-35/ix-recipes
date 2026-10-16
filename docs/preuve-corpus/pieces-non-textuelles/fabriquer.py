"""Fabrique les pièces jetables de l'essai « pièces non textuelles » (decision-corpus.md §8).

Script d'essai, pas du code de production. Bibliothèque standard, plus Pillow pour le PDF scanné.
    python3 fabriquer.py <dossier de sortie>
"""
import datetime
import sys
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


# --- PDF texte, écrit à la main (Helvetica, WinAnsiEncoding) -------------------------------------
def pdf_text(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)").encode("cp1252")


def make_pdf(pages, path):
    """pages : liste de pages, chaque page une liste de (x, y, taille, texte)."""
    objs = []
    font_id = 3
    page_ids = []
    contents = []
    for lines in pages:
        stream = b"".join(
            b"BT /F1 %d Tf %d %d Td (" % (size, x, y) + pdf_text(t) + b") Tj ET\n" for x, y, size, t in lines)
        contents.append(stream)
    n = len(pages)
    # 1 catalogue, 2 pages, 3 police, puis (page, contenu) par page
    for i in range(n):
        page_ids.append(4 + 2 * i)
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(b"<< /Type /Pages /Kids [" + b" ".join(b"%d 0 R" % p for p in page_ids) + b"] /Count %d >>" % n)
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
    for i, stream in enumerate(contents):
        objs.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                    b"/Resources << /Font << /F1 %d 0 R >> >> /Contents %d 0 R >>" % (font_id, page_ids[i] + 1))
        objs.append(b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"endstream")
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for k, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % k + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += b"".join(b"%010d 00000 n \n" % o for o in offsets)
    out += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objs) + 1, xref)
    Path(path).write_bytes(bytes(out))


def contrat_pages():
    p1 = [
        (60, 780, 16, "Contrat de fourniture n° CF-2026-114"),
        (60, 750, 10, "Entre Atelier Morvan (le Client) et Scierie du Blavet SAS (le Fournisseur)."),
        (60, 720, 12, "Article 3 - Prix"),
        (60, 700, 10, "Les prix unitaires sont fixés comme suit, en euros hors taxes :"),
        (80, 675, 10, "Référence"), (220, 675, 10, "Essence"), (340, 675, 10, "Unité"), (440, 675, 10, "Prix HT"),
        (80, 655, 10, "CH-27"), (220, 655, 10, "Chêne massif"), (340, 655, 10, "m3"), (440, 655, 10, "1 180 €"),
        (80, 635, 10, "HE-27"), (220, 635, 10, "Hêtre"), (340, 635, 10, "m3"), (440, 635, 10, "640 €"),
        (80, 615, 10, "NO-40"), (220, 615, 10, "Noyer"), (340, 615, 10, "m3"), (440, 615, 10, "2 350 €"),
        (60, 585, 10, "Les prix sont révisables une fois par an, au 1er janvier, dans la limite de 4 %."),
        (60, 555, 12, "Article 4 - Livraison"),
        (60, 535, 10, "Livraison sous 15 jours ouvrés à compter de la commande, franco à partir de 3 000 € HT."),
    ]
    p2 = [
        (60, 780, 12, "Article 7 - Durée et résiliation"),
        (60, 760, 10, "Le contrat est conclu pour deux ans à compter du 1er mars 2026."),
        (60, 745, 10, "Chaque partie peut le résilier par lettre recommandée avec un préavis de trois mois."),
        (60, 715, 12, "Article 9 - Pénalités"),
        (60, 695, 10, "Tout retard de livraison donne lieu à une pénalité de 1 % du montant de la commande"),
        (60, 680, 10, "par jour ouvré de retard, plafonnée à 10 %."),
        (60, 650, 12, "Article 11 - Loi applicable"),
        (60, 630, 10, "Le présent contrat est soumis au droit français. Tribunal de commerce de Lorient."),
    ]
    return [p1, p2]


def long_pages():
    pages = []
    for n in range(1, 26):
        lines = [(60, 780, 14, f"Annexe technique - section {n}"),
                 (60, 750, 10, f"Spécifications de la section {n} : tolérances d'usinage et d'humidité du bois.")]
        if n == 23:
            lines.append((60, 720, 10, "Le délai de garantie des ouvrages est de 36 mois à compter de la réception."))
        pages.append(lines)
    return pages


# --- PDF scanné : une image, aucun texte ---------------------------------------------------------
def make_scan(path):
    img = Image.new("RGB", (1240, 1754), "white")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 34)
    except OSError:
        font = ImageFont.load_default()
    y = 160
    for line in ["Avenant n° 2 au contrat CF-2026-114",
                 "",
                 "À compter du 1er janvier 2027, le prix unitaire",
                 "du chêne massif (réf. CH-27) passe à 1 225 € HT le m3.",
                 "",
                 "Fait à Lorient, le 2 octobre 2026."]:
        d.text((140, y), line, fill="black", font=font)
        y += 60
    img = img.rotate(0.8, fillcolor="white").convert("L")  # légèrement de travers, comme un scan
    img.save(path, "PDF", resolution=150)


# --- Tableur .xlsx écrit à la main, comme Excel l'enregistre --------------------------------------
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def make_xlsx(path):
    strings = ["Suivi budgétaire T3 2026 - k€ HT", "Poste", "Budget T3", "Réel T3", "Écart",
               "Chiffre d'affaires", "Achats matières", "Masse salariale", "Marketing", "Déplacements",
               "Loyers et charges", "Total charges", "Arrêté au",
               "Cause", "Salon Maison&Objet de septembre, décidé en juin, hors budget.",
               "Prix du chêne +6 % depuis juillet."]
    sid = {s: i for i, s in enumerate(strings)}
    rows = [("Chiffre d'affaires", 2400, 2310), ("Achats matières", 960, 1010), ("Masse salariale", 720, 705),
            ("Marketing", 120, 138), ("Déplacements", 30, 41), ("Loyers et charges", 90, 90)]
    serial = (datetime.date(2026, 9, 30) - datetime.date(1899, 12, 30)).days

    def s_cell(ref, text, style=0):
        return f'<c r="{ref}" t="s"{f" s=\"{style}\"" if style else ""}><v>{sid[text]}</v></c>'

    def n_cell(ref, val, formula=None, style=0):
        f = f"<f>{esc(formula)}</f>" if formula else ""
        return f'<c r="{ref}"{f" s=\"{style}\"" if style else ""}>{f}<v>{val}</v></c>'

    xml_rows = [f'<row r="1">{s_cell("A1", strings[0], 1)}</row>',
                '<row r="2">' + "".join(s_cell(f"{c}2", t, 1) for c, t in zip("ABCD", strings[1:5])) + "</row>"]
    r = 3
    for name, b, a in rows:
        xml_rows.append(f'<row r="{r}">{s_cell(f"A{r}", name)}{n_cell(f"B{r}", b)}{n_cell(f"C{r}", a)}'
                        f'{n_cell(f"D{r}", a - b, f"C{r}-B{r}")}</row>')
        r += 1
    tb, ta = sum(b for _, b, _ in rows[1:]), sum(a for _, _, a in rows[1:])
    xml_rows.append(f'<row r="{r}">{s_cell(f"A{r}", "Total charges", 1)}{n_cell(f"B{r}", tb, "SUM(B4:B8)")}'
                    f'{n_cell(f"C{r}", ta, "SUM(C4:C8)")}{n_cell(f"D{r}", ta - tb, f"C{r}-B{r}")}</row>')
    r += 2
    xml_rows.append(f'<row r="{r}">{s_cell(f"A{r}", "Arrêté au")}{n_cell(f"B{r}", serial, style=2)}</row>')
    sheet1 = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              f'<sheetData>{"".join(xml_rows)}</sheetData>'
              '<mergeCells count="1"><mergeCell ref="A1:D1"/></mergeCells></worksheet>')
    sheet2 = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>'
              f'<row r="1">{s_cell("A1", "Poste", 1)}{s_cell("B1", "Cause", 1)}</row>'
              f'<row r="2">{s_cell("A2", "Marketing")}{s_cell("B2", strings[14])}</row>'
              f'<row r="3">{s_cell("A3", "Achats matières")}{s_cell("B3", strings[15])}</row>'
              '</sheetData></worksheet>')
    shared = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              f'<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" count="{len(strings)}" '
              f'uniqueCount="{len(strings)}">' + "".join(f"<si><t>{esc(s)}</t></si>" for s in strings) + "</sst>")
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font>'
              '<font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="1"><fill><patternFill patternType="none"/></fill></fills>'
              '<borders count="1"><border/></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
              '<xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/>'
              '<xf numFmtId="14" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/></cellXfs>'
              '</styleSheet>')
    workbook = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>'
                '<sheet name="T3" sheetId="1" r:id="rId1"/><sheet name="Commentaires" sheetId="2" r:id="rId2"/>'
                '</sheets></workbook>')
    rel = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    wb_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
               '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
               f'<Relationship Id="rId1" Type="{rel}/worksheet" Target="worksheets/sheet1.xml"/>'
               f'<Relationship Id="rId2" Type="{rel}/worksheet" Target="worksheets/sheet2.xml"/>'
               f'<Relationship Id="rId3" Type="{rel}/sharedStrings" Target="sharedStrings.xml"/>'
               f'<Relationship Id="rId4" Type="{rel}/styles" Target="styles.xml"/></Relationships>')
    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 f'<Relationship Id="rId1" Type="{rel}/officeDocument" Target="xl/workbook.xml"/></Relationships>')
    ct = "application/vnd.openxmlformats-officedocument.spreadsheetml"
    types = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
             '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
             '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
             '<Default Extension="xml" ContentType="application/xml"/>'
             f'<Override PartName="/xl/workbook.xml" ContentType="{ct}.sheet.main+xml"/>'
             f'<Override PartName="/xl/worksheets/sheet1.xml" ContentType="{ct}.worksheet+xml"/>'
             f'<Override PartName="/xl/worksheets/sheet2.xml" ContentType="{ct}.worksheet+xml"/>'
             f'<Override PartName="/xl/sharedStrings.xml" ContentType="{ct}.sharedStrings+xml"/>'
             f'<Override PartName="/xl/styles.xml" ContentType="{ct}.styles+xml"/></Types>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        z.writestr("xl/worksheets/sheet1.xml", sheet1)
        z.writestr("xl/worksheets/sheet2.xml", sheet2)
        z.writestr("xl/sharedStrings.xml", shared)
        z.writestr("xl/styles.xml", styles)


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    make_pdf(contrat_pages(), out / "contrat.pdf")
    make_pdf(long_pages(), out / "annexe-25-pages.pdf")
    make_scan(out / "avenant-scanne.pdf")
    make_xlsx(out / "budget-t3.xlsx")
