"""Build the Phase I report. Project owner: Lukáš Dubšík; review pending.

Report tooling is optional and separate from application dependencies.
Requires python-docx and Pillow. The supplied institutional template is external.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from copy import deepcopy
from pathlib import Path
from zipfile import ZipFile

from docx import Document
from docx.document import Document as DocumentType
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from docx.text.paragraph import Paragraph
from PIL import Image, ImageDraw, ImageFont

TEMPLATE_SHA256 = "35bbd6d62d18fbc8a4985b5302694f2fe6e6105f3a42150b5cd9f02a0d87e00d"
PRESERVED_PARTS = (
    "word/numbering.xml",
    "word/styles.xml",
    "word/fontTable.xml",
    "word/theme/theme1.xml",
    "word/settings.xml",
    "_rels/.rels",
)


def paragraph_text(
    paragraph: Paragraph, text: str, *, size: float | None = None
) -> None:
    """Add text with safe wrapping of long source paths and URLs."""
    chunks = re.split(r"(`[^`]+`)", text)
    for chunk in chunks:
        code = chunk.startswith("`") and chunk.endswith("`")
        value = chunk[1:-1] if code else chunk
        value = re.sub(r"(?<=[/_.-])(?=\S)", "\u200b", value)
        run = paragraph.add_run(value)
        run.font.color.rgb = RGBColor(0, 0, 0)
        if size is not None:
            run.font.size = Pt(size)
        if code:
            run.font.name = "Liberation Mono"


def diagram(path: Path, kind: str, font_path: Path) -> None:
    """Draw a readable native diagram, keeping labels larger than UI text."""
    width = 1560
    height = 620 if kind == "navigation" else 900
    im = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(str(font_path), 31)
    small = ImageFont.truetype(str(font_path), 27)

    def box(
        rect: tuple[int, int, int, int],
        lines: list[str],
        fill: str = "#edf6f7",
    ) -> None:
        draw.rounded_rectangle(rect, radius=12, fill=fill, outline="#40565c", width=3)
        x0, y0, x1, y1 = rect
        y = (y0 + y1 - len(lines) * 40) / 2
        for line in lines:
            draw.text(((x0 + x1) / 2, y), line, font=font, fill="#142f38", anchor="mt")
            y += 40

    def arrow(
        points: list[tuple[int, int]],
        label: str | None = None,
        label_xy: tuple[int, int] | None = None,
    ) -> None:
        draw.line(points, fill="#40565c", width=4)
        x, y = points[-1]
        px, py = points[-2]
        if x != px:
            sign = 1 if x > px else -1
            draw.polygon(
                [(x, y), (x - sign * 17, y - 10), (x - sign * 17, y + 10)],
                fill="#40565c",
            )
        else:
            sign = 1 if y > py else -1
            draw.polygon(
                [(x, y), (x - 10, y - sign * 17), (x + 10, y - sign * 17)],
                fill="#40565c",
            )
        if label and label_xy is not None:
            draw.text(label_xy, label, font=small, fill="#142f38", anchor="mm")

    if kind == "navigation":
        box((25, 35, 475, 195), ["Prepare", "Požadavek a cíle"])
        box((555, 35, 1005, 195), ["Review", "Podklady a rozhodnutí"])
        box((1085, 35, 1535, 195), ["Export", "Uložený výběr"])
        arrow([(475, 115), (555, 115)])
        arrow([(1005, 115), (1085, 115)])
        box((25, 365, 475, 540), ["Výpočet mimo GUI", "Není implementován"], "#f4f4f4")
        box((555, 365, 1005, 540), ["Import evidence", "Náhled a shoda revize"])
        arrow([(475, 445), (555, 445)])
        arrow([(780, 365), (780, 195)], "připojení", (900, 280))
        draw.text(
            (780, 580),
            "Save a otevření zachovávají společnou studii",
            font=small,
            fill="#142f38",
            anchor="mm",
        )
    else:
        box((40, 25, 670, 155), ["React Views", "Prepare / Review / Export"])
        box(
            (890, 25, 1520, 155),
            ["Sdílený reducer a selectors", "zrcadlo, buffery, navigace"],
        )
        arrow([(890, 90), (670, 90)], "render", (780, 60))
        box((40, 245, 670, 365), ["Kontrolér a fetch JSON"])
        arrow([(350, 155), (350, 245)], "záměr", (440, 200))
        arrow([(670, 305), (1205, 305), (1205, 155)], "stav odpovědi", (1220, 345))
        box((40, 445, 670, 565), ["FastAPI transport"])
        arrow([(350, 365), (350, 445)], "HTTP", (435, 405))
        box(
            (40, 645, 670, 805),
            ["Aplikační služby", "Workspace / Prepare / Review / Export"],
        )
        arrow([(350, 565), (350, 645)])
        box((890, 445, 1520, 565), ["Doména", "modely, identity a pravidla"])
        arrow([(670, 690), (800, 690), (800, 505), (890, 505)])
        box((890, 665, 1520, 825), ["Aplikační porty", "SQLite a JSON adaptéry"])
        arrow([(670, 760), (890, 760)])
        draw.text(
            (780, 870),
            "IRCOMP kompilátor není součástí této běhové cesty",
            font=small,
            fill="#142f38",
            anchor="mm",
        )
    im.save(path)


def assets(root: Path, out: Path, font: Path) -> dict[str, Path]:
    """Prepare explicitly labelled figure excerpts and diagrams."""
    result = {}
    crops = {
        "prepare-wire": (
            "docs/design/wireframes/01-prepare.png",
            (322, 315, 1002, 665),
        ),
        "review-wire": ("docs/design/wireframes/03-review.png", (1015, 435, 1382, 815)),
        "export-wire": ("docs/design/wireframes/05-export.png", (32, 230, 890, 700)),
        "runtime-review": (
            "docs/development/screenshots/s6-review.png",
            (285, 690, 1035, 970),
        ),
    }
    for name, (relative, bounds) in crops.items():
        target = out / f"{name}.png"
        with Image.open(root / relative) as source:
            source.crop(bounds).save(target)
        result[name] = target
    for name in ("navigation", "architecture"):
        result[name] = out / f"{name}.png"
        diagram(result[name], name, font)
    return result


def table(document: DocumentType, rows: list[list[str]]) -> None:
    """Render compact comparable records with visible borders and wrapping."""
    count = len(rows[0])
    widths = {2: (1.8, 4.7), 3: (0.85, 4.45, 1.2)}[count]
    if count == 3 and rows[0][0] in ("ID", "Příkaz či služba", "Příkaz"):
        widths = (0.55, 4.1, 1.85) if rows[0][0] == "ID" else (1.65, 2.05, 2.8)
    item = document.add_table(rows=0, cols=count)
    item.autofit = False
    for column, width in zip(item.columns, widths, strict=True):
        column.width = Inches(width)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = OxmlElement(f"w:{edge}")
        for key, value in {"val": "single", "sz": "4", "color": "D9D9D9"}.items():
            node.set(qn(f"w:{key}"), value)
        borders.append(node)
    item._tbl.tblPr.append(borders)
    for index, values in enumerate(rows):
        row = item.add_row()
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        if index == 0:
            row._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
        for cell, value, width in zip(row.cells, values, widths, strict=True):
            cell.width = Inches(width)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
            props = cell._tc.get_or_add_tcPr()
            margins = OxmlElement("w:tcMar")
            for edge in ("top", "bottom", "left", "right"):
                margin = OxmlElement(f"w:{edge}")
                margin.set(qn("w:w"), "65" if edge in ("top", "bottom") else "90")
                margin.set(qn("w:type"), "dxa")
                margins.append(margin)
            props.append(margins)
            if index == 0:
                shading = OxmlElement("w:shd")
                shading.set(qn("w:fill"), "EBF7FF")
                props.append(shading)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            paragraph_text(p, value, size=9.5)
            if index == 0:
                for run in p.runs:
                    run.bold = True


def main() -> None:
    """Build from the external template and verify preserved package parts."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[2]
    )
    parser.add_argument("--source", type=Path)
    parser.add_argument("--metadata", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--font",
        type=Path,
        default=Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    )
    parser.add_argument(
        "--strict", action="store_true", help="Reject unresolved report TODOs."
    )
    args = parser.parse_args()
    template_hash = hashlib.sha256(args.template.read_bytes()).hexdigest()
    if template_hash != TEMPLATE_SHA256:
        raise SystemExit(
            "Template hash differs; inspect and update the template contract first."
        )
    source = args.source or args.root / "docs/report/phase-i.md"
    metadata = json.loads(
        (args.metadata or args.root / "docs/report/metadata.json").read_text()
    )
    text = source.read_text()
    metadata["implementation_commit_short"] = metadata["implementation_commit"][:7]
    metadata["login_filename"] = (
        metadata["login"]
        if re.fullmatch(r"[a-z][a-z0-9]{2,15}", metadata["login"])
        else "DOPLNIT_LOGIN"
    )
    for name, value in metadata.items():
        text = text.replace("{{" + name + "}}", value)
    if args.strict and "TODO" in text + json.dumps(metadata):
        raise SystemExit(
            "Unresolved TODOs remain. Complete primary research "
            "and metadata before final output."
        )
    args.output.mkdir(parents=True, exist_ok=True)
    pages = text.split("<!-- page -->")
    with tempfile.TemporaryDirectory(prefix="ircomp-report-") as temporary:
        temp = Path(temporary)
        images = assets(args.root, temp, args.font)
        doc = Document(args.template)
        identity = deepcopy(doc.tables[0]._tbl)
        for child in list(doc._element.body):
            if child.tag != qn("w:sectPr"):
                doc._element.body.remove(child)
        footer = doc.sections[0].footer.paragraphs[0]
        footer.paragraph_format.space_before = Pt(0)
        footer.alignment = 2
        footer.add_run("CRISPR Study Workspace  |  ").font.size = Pt(8)
        field = OxmlElement("w:fldSimple")
        field.set(qn("w:instr"), "PAGE")
        footer._p.append(field)
        pending_break = False
        figure_number = 0
        for page_number, page in enumerate(pages, 1):
            lines = page.strip().splitlines()
            index = 0
            if page_number > 1:
                pending_break = True
            while index < len(lines):
                line = lines[index].strip()
                index += 1
                if not line:
                    continue
                before = len(doc.paragraphs)
                if line == "{{identification}}":
                    original = deepcopy(identity)
                    doc._element.body.insert(len(doc._element.body) - 1, original)
                    cells = original.findall(".//" + qn("w:tc"))
                    values = [
                        "Identifikace projektu",
                        "\n".join(
                            (
                                "Název projektu: CRISPR Study Workspace",
                                f"Kapitán a jediný člen: {metadata['author']}",
                                f"Login: {metadata['login']}",
                                f"Cvičení: {metadata['lab']}",
                                "Rozdělení: Prepare, Review a společná infrastruktura",
                                "Samostatná účast dohodnuta; rozsah pro dva členy",
                                f"Verze zprávy: {metadata['date']}",
                            )
                        ),
                    ]
                    for cell, value in zip(cells, values, strict=True):
                        for child in list(cell):
                            if child.tag != qn("w:tcPr"):
                                cell.remove(child)
                        for content in value.splitlines():
                            p = OxmlElement("w:p")
                            r = OxmlElement("w:r")
                            t = OxmlElement("w:t")
                            t.text = content
                            r.append(t)
                            p.append(r)
                            cell.append(p)
                    continue
                if line == "{{contents}}":
                    p = doc.add_paragraph()
                    p.paragraph_format.page_break_before = True
                    p.add_run("Obsah  /  " + metadata["author"]).bold = True
                    for n, item in enumerate(pages, 1):
                        for marks, title in re.findall(r"^(#{2,4}) (.+)$", item, re.M):
                            if not title[0].isdigit():
                                continue
                            p = doc.add_paragraph()
                            p.paragraph_format.space_before = Pt(2)
                            p.paragraph_format.left_indent = Inches(
                                (len(marks) - 2) * 0.15
                            )
                            paragraph_text(p, f"{title}  /  {n + 1}", size=10)
                    continue
                heading = re.match(r"^(#{1,4}) (.+)$", line)
                if heading:
                    level = len(heading[1])
                    p = doc.add_paragraph(
                        style="Title" if level == 1 else f"Heading {level - 1}"
                    )
                    p.paragraph_format.keep_with_next = True
                    paragraph_text(p, heading[2])
                    author = p.add_run("  /  " + metadata["author"])
                    author.font.size = Pt(8.5)
                    author.font.color.rgb = RGBColor(0, 0, 0)
                    if pending_break:
                        p.paragraph_format.space_before = Pt(0)
                elif line.startswith("!["):
                    match = re.fullmatch(r"!\[(.+)\]\(asset:([a-z-]+)\)", line)
                    if match is None:
                        raise ValueError(f"Unsupported figure: {line}")
                    figure_number += 1
                    p = doc.add_paragraph()
                    p.paragraph_format.keep_with_next = True
                    width = 4.0 if match[2] == "review-wire" else 6.5
                    p.add_run().add_picture(str(images[match[2]]), width=Inches(width))
                    picture = p._p.find(".//" + qn("wp:docPr"))
                    picture.set("descr", match[1])
                    p = doc.add_paragraph()
                    p.paragraph_format.space_before = Pt(3)
                    paragraph_text(p, match[1], size=9)
                elif line.startswith("|"):
                    rows = [[part.strip() for part in line.strip("|").split("|")]]
                    while index < len(lines) and lines[index].strip().startswith("|"):
                        value = lines[index].strip()
                        index += 1
                        if re.fullmatch(r"[| :\-]+", value):
                            continue
                        rows.append(
                            [part.strip() for part in value.strip("|").split("|")]
                        )
                    table(doc, rows)
                elif line.startswith("```"):
                    while index < len(lines) and not lines[index].startswith("```"):
                        p = doc.add_paragraph()
                        p.paragraph_format.space_before = Pt(0)
                        paragraph_text(p, "`" + lines[index] + "`", size=9)
                        index += 1
                    index += 1
                else:
                    p = doc.add_paragraph()
                    paragraph_text(p, line)
                if pending_break and len(doc.paragraphs) > before:
                    doc.paragraphs[before].paragraph_format.page_break_before = True
                    pending_break = False
        stem = f"00_{metadata['login_filename']}_navrh"
        intermediate = temp / "authored.docx"
        doc.save(intermediate)
        output = args.output / f"{stem}.docx"
        editable = {
            "word/document.xml",
            "word/_rels/document.xml.rels",
            "[Content_Types].xml",
        }
        with (
            ZipFile(args.template) as reference,
            ZipFile(intermediate) as authored,
            ZipFile(output, "w") as final,
        ):
            original_names = set(reference.namelist())
            for name in reference.namelist():
                final.writestr(
                    name,
                    authored.read(name) if name in editable else reference.read(name),
                )
            for name in authored.namelist():
                if name not in original_names:
                    final.writestr(name, authored.read(name))
        with ZipFile(args.template) as reference, ZipFile(output) as final:
            for name in PRESERVED_PARTS:
                if reference.read(name) != final.read(name):
                    raise ValueError(f"Unexpected template change: {name}")
        (args.output / "build-record.json").write_text(
            json.dumps(
                {
                    "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                    "metadata_sha256": hashlib.sha256(
                        (
                            args.metadata or args.root / "docs/report/metadata.json"
                        ).read_bytes()
                    ).hexdigest(),
                    "template_sha256": template_hash,
                    "implementation_commit": metadata["implementation_commit"],
                    "planned_pages": len(pages) + 1,
                    "figures": figure_number,
                    "unresolved_todo_lines": [
                        line for line in text.splitlines() if "TODO" in line
                    ],
                    "preserved_template_parts": list(PRESERVED_PARTS),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
        print(output)


if __name__ == "__main__":
    main()
