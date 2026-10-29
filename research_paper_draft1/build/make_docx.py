"""Write Draft 1 into a .docx derived from the official IST-Africa template.

Usage: python -I make_docx.py <template_derived.docx> <manuscript_source.txt> <out.docx>

The template-derived .docx (Word's conversion of IST-AfricaTemplate.dot) supplies
styles.xml, numbering.xml, theme, fonts and page setup. Only document.xml,
its relationships, the content types, the media and the document properties
are replaced. Standard library only.
"""
import re
import struct
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

template, source, out = map(Path, sys.argv[1:4])
lines = source.read_text(encoding="utf-8").splitlines()

STYLE = {"T": "Title", "AU": "AuthorName", "ABS": "Abstract", "H1": "Heading1", "H2": "Heading2",
         "LN": "ListNumber", "LB": "ListBullet", "N": "Normal", "CAP": "Caption"}
AQ = re.compile(r"(\[AQ\d+[^\]]*\])")


def runs(text, size=None):
    parts = []
    for chunk in AQ.split(text):
        if not chunk:
            continue
        rpr = ""
        if size:
            rpr += f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>'
        if AQ.fullmatch(chunk):
            rpr += '<w:highlight w:val="yellow"/>'
        rpr = f"<w:rPr>{rpr}</w:rPr>" if rpr else ""
        parts.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escape(chunk)}</w:t></w:r>')
    return "".join(parts)


def para(style, text, tab=False, size=None, extra_ppr=""):
    lead = '<w:r><w:tab/></w:r>' if tab else ""
    return f'<w:p><w:pPr><w:pStyle w:val="{style}"/>{extra_ppr}</w:pPr>{lead}{runs(text, size)}</w:p>'


def table(rows, cols):
    border = "".join(f'<w:{b} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                     for b in ("top", "left", "bottom", "right", "insideH", "insideV"))
    xml = [f'<w:tbl><w:tblPr><w:tblStyle w:val="TableNormal"/><w:tblW w:w="0" w:type="auto"/><w:jc w:val="center"/>'
           f'<w:tblBorders>{border}</w:tblBorders><w:tblLayout w:type="autofit"/>'
           f'<w:tblCellMar><w:left w:w="80" w:type="dxa"/><w:right w:w="80" w:type="dxa"/></w:tblCellMar></w:tblPr>'
           f'<w:tblGrid>{"<w:gridCol/>" * cols}</w:tblGrid>']
    for r, row in enumerate(rows):
        trpr = "<w:trPr><w:tblHeader/><w:cantSplit/></w:trPr>" if r == 0 else "<w:trPr><w:cantSplit/></w:trPr>"
        cells = "".join(
            '<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/></w:tcPr>'
            + para("Normal", cell, size=20, extra_ppr='<w:spacing w:before="20" w:after="20"/><w:jc w:val="left"/>')
            + "</w:tc>"
            for cell in (row + [""] * cols)[:cols])
        xml.append(f"<w:tr>{trpr}{cells}</w:tr>")
    xml.append("</w:tbl>")
    return "".join(xml)


def png_size(path):
    data = path.read_bytes()[:24]
    return struct.unpack(">II", data[16:24])


def figure(rid, path, width_emu=5400000):
    w, h = png_size(path)
    height_emu = int(width_emu * h / w)
    return ('<w:p><w:pPr><w:pStyle w:val="Normal"/><w:keepNext/><w:spacing w:before="120"/><w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
            f'<wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{width_emu}" cy="{height_emu}"/>'
            '<wp:docPr id="1" name="Figure 1"/><a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">'
            '<pic:nvPicPr><pic:cNvPr id="1" name="figure1.png"/><pic:cNvPicPr/></pic:nvPicPr>'
            f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
            f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{width_emu}" cy="{height_emu}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic>'
            '</wp:inline></w:drawing></w:r></w:p>')


body, media = [], []
prev_heading = True
i = 0
while i < len(lines):
    m = re.match(r"^@(\w+)\s?(.*)$", lines[i])
    i += 1
    if not m:
        continue
    tag, text = m.groups()
    if tag in ("H1", "H2"):
        body.append(para(STYLE[tag], text)); prev_heading = True
    elif tag == "P":
        body.append(para("Paragraph1", text) if prev_heading else para("Paragraph2", text, tab=True))
        prev_heading = False
    elif tag == "REF":
        body.append(para("Paragraph1", text, size=20))
    elif tag == "CAP":
        keep = '<w:keepNext/>' if text.startswith("Table") else ""
        body.append(para("Caption", text, extra_ppr=keep))
    elif tag == "TABLE":
        cols, rows = int(text), []
        while i < len(lines) and lines[i].startswith("@TR "):
            rows.append(lines[i][4:].split("|")); i += 1
        if i < len(lines) and lines[i].startswith("@ENDTABLE"):
            i += 1
        body.append(table(rows, cols)); prev_heading = True
    elif tag == "FIG":
        path = source.parent / text
        media.append(path)
        body.append(figure(f"rIdImg{len(media)}", path))
    elif tag in STYLE:
        body.append(para(STYLE[tag], text))
        if tag == "LN":
            prev_heading = False

with zipfile.ZipFile(template) as z:
    parts = {n: z.read(n) for n in z.namelist()}

doc = parts["word/document.xml"].decode("utf-8")
head = doc[: doc.index("<w:body>") + len("<w:body>")]
sect = re.findall(r"<w:sectPr.*?</w:sectPr>", doc, re.S)[-1]
parts["word/document.xml"] = (head + "".join(body) + sect + "</w:body></w:document>").encode("utf-8")

rels = parts["word/_rels/document.xml.rels"].decode("utf-8")
img_rels = "".join(f'<Relationship Id="rIdImg{k}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{k}.png"/>'
                   for k in range(1, len(media) + 1))
parts["word/_rels/document.xml.rels"] = rels.replace("</Relationships>", img_rels + "</Relationships>").encode("utf-8")
for k, path in enumerate(media, 1):
    parts[f"word/media/image{k}.png"] = path.read_bytes()

ct = parts["[Content_Types].xml"].decode("utf-8")
if 'Extension="png"' not in ct:
    ct = ct.replace("<Default Extension=", '<Default Extension="png" ContentType="image/png"/><Default Extension=', 1)
parts["[Content_Types].xml"] = ct.encode("utf-8")

# Double-blind: no personal names in document properties.
parts["docProps/core.xml"] = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
    'xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" '
    'xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<dc:title>Draft 1</dc:title><dc:creator></dc:creator><cp:lastModifiedBy></cp:lastModifiedBy><cp:revision>1</cp:revision>'
    '</cp:coreProperties>').encode("utf-8")
app = parts["docProps/app.xml"].decode("utf-8")
app = re.sub(r"<Company>.*?</Company>", "<Company></Company>", app)
app = re.sub(r"<Manager>.*?</Manager>", "<Manager></Manager>", app)
parts["docProps/app.xml"] = app.encode("utf-8")

out.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    order = ["[Content_Types].xml"] + [n for n in parts if n != "[Content_Types].xml"]
    for name in order:
        z.writestr(name, parts[name])
print(f"wrote {out} ({len(body)} blocks, {len(media)} image(s))")
