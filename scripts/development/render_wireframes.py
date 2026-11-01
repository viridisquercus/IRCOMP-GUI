"""Render S4 design artifacts as editable SVG and matching PNG previews."""

from __future__ import annotations

from html import escape
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs/design/wireframes"
FONT = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
BOLD = FONT.with_name("DejaVuSans-Bold.ttf")
INK = "#18333b"
MUTED = "#526b72"
TEAL = "#126b65"
BORDER = "#d8e2e4"


class Frame:
    """Draw the same bounded primitives into vector and raster artifacts."""

    def __init__(
        self, section: str, title: str, subtitle: str, *, unsaved: bool = False
    ) -> None:
        self.image = Image.new("RGB", (1440, 960), "#f3f6f6")
        self.draw = ImageDraw.Draw(self.image)
        self.svg = [
            (
                '<svg xmlns="http://www.w3.org/2000/svg" width="1440" height='
                '"960" viewBox="0 0 1440 960">'
            ),
            f"<title>{escape(title)}</title>",
        ]
        self.box(0, 0, 1440, 960, "#f3f6f6", radius=0)
        self.box(0, 0, 1440, 76, "#18333b", radius=0)
        self.text(32, 23, "IRCOMP / Study workspace", 21, "#ffffff", bold=True)
        self.text(600, 27, "Study: Review demonstration  ▾", 16, "#ffffff")
        self.text(
            1030,
            27,
            "Unsaved draft · r3" if unsaved else "Saved · request r3",
            15,
            "#c9e6e2",
        )
        self.button(1230, 17, 178, "Save study", primary=True)
        for x, label in [(32, "Prepare"), (170, "Review"), (308, "Export")]:
            self.box(x, 91, 122, 42, TEAL if section == label else "#ffffff")
            self.text(
                x + 20,
                102,
                label,
                16,
                "#ffffff" if section == label else INK,
                bold=True,
            )
        self.text(1000, 102, "DESIGN ONLY · SYNTHETIC EXAMPLE", 13, MUTED)
        self.text(32, 151, title, 27, bold=True)
        self.text(32, 191, subtitle, 15, MUTED)
        self.text(
            32,
            921,
            ("S4 / 2026-11-01 · Initial design — primary-research validation pending"),
            13,
            MUTED,
        )

    def box(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        fill: str = "#ffffff",
        radius: int = 10,
        stroke: str = BORDER,
    ) -> None:
        """Draw a rounded surface."""
        self.draw.rounded_rectangle(
            (x, y, x + w, y + h), radius, fill=fill, outline=stroke
        )
        self.svg.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'rx="{radius}" fill="{fill}" stroke="{stroke}"/>'
        )

    def text(
        self,
        x: int,
        y: int,
        value: str,
        size: int = 16,
        color: str = INK,
        *,
        bold: bool = False,
    ) -> None:
        """Draw escaped text and reject horizontal overflow."""
        font = ImageFont.truetype(str(BOLD if bold else FONT), size)
        if x + font.getlength(value) > 1430:
            raise ValueError(f"Text exceeds frame: {value}")
        self.draw.text((x, y), value, font=font, fill=color)
        self.svg.append(
            f'<text x="{x}" y="{y + size}" '
            f'font-family="DejaVu Sans,sans-serif" font-size="{size}" '
            f'font-weight="{700 if bold else 400}" fill="{color}">'
            f"{escape(value)}</text>"
        )

    def paragraph(
        self, x: int, y: int, value: str, width: int, color: str = MUTED, size: int = 15
    ) -> None:
        """Wrap text within the available width."""
        font = ImageFont.truetype(str(FONT), size)
        line = ""
        for word in value.split():
            candidate = f"{line} {word}".strip()
            if font.getlength(candidate) > width and line:
                self.text(x, y, line, size, color)
                y += size + 9
                line = word
            else:
                line = candidate
        if line:
            self.text(x, y, line, size, color)

    def button(
        self,
        x: int,
        y: int,
        width: int,
        label: str,
        *,
        primary: bool = False,
        disabled: bool = False,
    ) -> None:
        """Draw an action with an explicit enabled state."""
        fill = "#e4e9eb" if disabled else TEAL if primary else "#ffffff"
        color = MUTED if disabled else "#ffffff" if primary else INK
        self.box(x, y, width, 42, fill)
        self.text(x + 16, y + 11, label, 15, color, bold=True)

    def field(
        self,
        x: int,
        y: int,
        width: int,
        label: str,
        value: str,
        *,
        invalid: bool = False,
    ) -> None:
        """Draw a labelled input and optional error boundary."""
        self.text(x, y, label, 14, MUTED)
        self.box(
            x,
            y + 27,
            width,
            47,
            "#fff5f3" if invalid else "#ffffff",
            stroke="#b44035" if invalid else BORDER,
        )
        self.text(x + 13, y + 40, value, 16)

    def save(self, name: str) -> None:
        """Write the editable SVG and raster preview."""
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / f"{name}.svg").write_text(
            "\n".join([*self.svg, "</svg>\n"]), encoding="utf-8"
        )
        self.image.save(OUT / f"{name}.png")


def prepare(*, invalid: bool) -> None:
    """Render request editing and a recoverable invalid draft."""
    f = Frame(
        "Prepare",
        "Prepare a request",
        (
            "Request r3 · demo-reference-v1 · Example profile · No scient"
            "ific checks performed"
        ),
        unsaved=invalid,
    )
    for x, w in [(32, 270), (322, 680), (1022, 386)]:
        f.box(x, 230, w, 650)
    f.text(52, 253, "Targets", 20, bold=True)
    f.button(52, 296, 230, "+ Add target")
    f.box(48, 359, 238, 94, "#e7f3f0")
    f.text(64, 375, "Region A", 17, bold=True)
    f.text(64, 408, "demo_contig: 100-240", 14, MUTED)
    f.text(64, 483, "Region B", 17, bold=True)
    f.text(64, 516, "demo_contig: 400-560", 14, MUTED)
    f.text(52, 600, "Remove selected target", 14, TEAL)
    f.paragraph(
        52,
        736,
        (
            "2 accepted targets. Selecting a target opens its editor with"
            "out changing request identity."
        ),
        220,
    )
    f.text(346, 253, "Region A", 20, bold=True)
    f.text(
        346,
        285,
        "Draft edits" if invalid else "Accepted target · no pending edits",
        14,
        MUTED,
    )
    f.field(346, 332, 630, "Target label", "Region A")
    f.field(346, 430, 630, "Contig", "demo_contig  ▾")
    f.field(346, 532, 296, "Start · 0-based", "100")
    f.field(
        676, 532, 300, "End · exclusive", "80" if invalid else "240", invalid=invalid
    )
    if invalid:
        f.text(676, 614, "End must be greater than 100.", 14, "#a32d25")
    else:
        f.text(346, 614, "Interval length: 140 bases", 14, MUTED)
    f.field(346, 666, 296, "Strand", "Unspecified  ▾")
    f.text(676, 677, "Coordinate convention", 14, MUTED)
    f.paragraph(676, 706, "0-based, end-exclusive. No automatic conversion.", 280)
    f.button(346, 797, 174, "Apply target", primary=True, disabled=invalid)
    f.button(536, 797, 170, "Discard edits")
    f.text(1044, 253, "Input checks", 20, bold=True)
    f.box(1042, 301, 344, 123, "#fff0ec" if invalid else "#e7f3f0")
    f.text(
        1058,
        317,
        "1 blocking problem" if invalid else "Structural checks passed",
        16,
        "#a32d25" if invalid else TEAL,
        bold=True,
    )
    f.paragraph(
        1058,
        354,
        "Region A → End. Correct the interval before applying this target."
        if invalid
        else "Both accepted targets satisfy the supported structural checks.",
        310,
    )
    f.button(1044, 448, 200, "Focus End" if invalid else "Check request")
    f.text(1044, 532, "Not checked", 17, bold=True)
    f.paragraph(
        1044,
        568,
        (
            "Biological suitability, external reference contents and scie"
            "ntific model validity."
        ),
        318,
    )
    f.text(1044, 685, "Drafts can be saved", 17, bold=True)
    f.paragraph(
        1044,
        721,
        "Saving work does not make an invalid request ready for analysis.",
        318,
    )
    f.save("02-prepare-error" if invalid else "01-prepare")


def review() -> None:
    """Render evidence and an independently editable review decision."""
    f = Frame(
        "Review",
        "Review evidence",
        (
            "Request r3 · demo-reference-v1 · Attached bundle: example-00"
            "1 · Synthetic evidence"
        ),
    )
    for x, w in [(32, 270), (322, 650), (992, 416)]:
        f.box(x, 230, w, 650)
    f.text(52, 253, "Candidates", 20, bold=True)
    f.button(52, 296, 230, "Import evidence")
    f.box(48, 359, 238, 94, "#e7f3f0")
    f.text(64, 375, "Candidate A", 17, bold=True)
    f.text(64, 408, "Needs clarification", 14, "#855710")
    f.text(64, 483, "Candidate B", 17, bold=True)
    f.text(64, 516, "Undecided", 14, MUTED)
    f.paragraph(
        52,
        738,
        "2 candidates. Filtering changes the view, not collection membership.",
        220,
    )
    f.text(346, 253, "Candidate A / Region A", 20, bold=True)
    f.text(346, 288, "Imported observations · read-only", 14, MUTED)
    f.box(346, 333, 602, 176, "#f6f8f8")
    f.text(364, 351, "SOURCE A · DEMO METRIC", 14, TEAL, bold=True)
    f.text(364, 389, "72", 34, bold=True)
    f.paragraph(
        446,
        393,
        (
            "Synthetic value. Scale: 0-100. Interpretation supplied by th"
            "is example only."
        ),
        470,
    )
    f.text(364, 470, "Record: source-a / item-01", 14, MUTED)
    f.box(346, 530, 602, 140, "#fff8e9")
    f.text(364, 548, "SOURCE B · DEMO METRIC", 14, "#855710", bold=True)
    f.text(364, 585, "Not supplied", 24, bold=True)
    f.text(364, 631, "Absence is not a numeric zero.", 15, MUTED)
    f.button(346, 699, 218, "View source records")
    f.paragraph(
        346,
        772,
        (
            "Values remain source-specific. No combined confidence or bio"
            "logical recommendation is calculated."
        ),
        580,
    )
    f.text(1014, 253, "Review decision", 20, bold=True)
    f.field(1014, 304, 368, "Collection", "Initial review  ▾")
    f.text(1014, 394, "✓ Candidate is in this collection", 14, TEAL)
    f.field(1014, 441, 368, "Disposition", "Needs clarification  ▾")
    f.text(1014, 542, "Reason", 14, MUTED)
    f.box(1014, 568, 368, 130)
    f.paragraph(
        1030,
        585,
        (
            "Source B does not provide the metric. Check source metadata "
            "before further review."
        ),
        330,
        INK,
    )
    f.text(1014, 720, "Evidence link: source-b / item-01", 14, MUTED)
    f.button(1014, 766, 208, "Apply decision", primary=True)
    f.text(1014, 837, "Remove from collection · Undo", 14, TEAL)
    f.save("03-review")


def mismatch() -> None:
    """Render a transactional import preview with incompatible identity."""
    f = Frame(
        "Review",
        "Check evidence before attaching",
        ("Current study remains unchanged until a compatible bundle is attached."),
    )
    f.box(160, 238, 1120, 640)
    f.text(192, 268, "Import preview / example-mismatch.json", 22, bold=True)
    f.text(
        192,
        308,
        "Synthetic evidence · format preview-v1 · bundle example-002",
        15,
        MUTED,
    )
    f.box(192, 358, 1056, 82, "#fff0ec")
    f.text(
        212, 375, "Cannot attach: reference identity differs", 19, "#a32d25", bold=True
    )
    f.text(
        212,
        407,
        "Changing the display label does not establish compatibility.",
        15,
        "#a32d25",
    )
    f.text(212, 484, "EXPECTED BY REQUEST r3", 14, MUTED, bold=True)
    f.text(752, 484, "DECLARED BY BUNDLE", 14, MUTED, bold=True)
    f.text(212, 529, "demo-reference-v1", 24, bold=True)
    f.text(752, 529, "demo-reference-v2", 24, bold=True)
    f.paragraph(
        212,
        599,
        (
            "Choose a bundle for the current request, or open the exact r"
            "equest context that produced this evidence. The original fil"
            "e is not modified."
        ),
        950,
    )
    f.button(192, 748, 224, "Choose another file")
    f.button(436, 748, 130, "Cancel")
    f.button(1004, 748, 244, "Attach unavailable", disabled=True)
    f.save("04-import-mismatch")


def export() -> None:
    """Render a handover preview with explicit unresolved decisions."""
    f = Frame(
        "Export",
        "Preview the handover",
        (
            "Last saved snapshot · request r3 · Synthetic evidence · Revi"
            "ew remains a draft"
        ),
    )
    f.box(32, 230, 858, 650)
    f.box(910, 230, 498, 650)
    f.text(56, 254, "Review package", 22, bold=True)
    f.text(56, 290, "Package type: Review package  ▾", 16, MUTED)
    f.box(56, 339, 810, 80, "#fff8e9")
    f.text(
        76, 354, "2 unresolved decisions — export as draft", 18, "#855710", bold=True
    )
    f.text(
        76, 386, "Unresolved items stay visible in the exported summary.", 15, "#855710"
    )
    rows = [
        ("Request snapshot", "r3 · 2 targets"),
        ("Evidence", "example-001 · synthetic"),
        ("Selected collection", "Initial review · 2 candidates"),
        ("Decisions", "1 needs clarification · 1 undecided"),
        ("Included source records", "2 referenced example records"),
        ("External dependencies", "None in this synthetic fixture"),
    ]
    for i, (label, value) in enumerate(rows):
        y = 461 + i * 53
        f.text(56, y, label, 15, MUTED)
        f.text(330, y, value, 16, bold=True)
    f.text(56, 824, "Exported context remains attached to request r3.", 15, TEAL)
    f.text(934, 254, "Before downloading", 22, bold=True)
    f.text(934, 318, "✓ Saved snapshot selected", 17, TEAL)
    f.text(934, 361, "✓ Source records included", 17, TEAL)
    f.text(934, 404, "! Review is incomplete", 17, "#855710")
    f.paragraph(
        934,
        468,
        (
            "This package records the current review state. It does not c"
            "ertify scientific validity or reproduce an external computat"
            "ion."
        ),
        444,
    )
    f.paragraph(
        934,
        602,
        "Synthetic example labels are retained in the manifest and summary.",
        444,
    )
    f.button(934, 720, 300, "Download draft", primary=True)
    f.button(934, 782, 230, "Return to review")
    f.save("05-export")


if __name__ == "__main__":
    prepare(invalid=False)
    prepare(invalid=True)
    review()
    mismatch()
    export()
