"""
Render a text note into a synthetic "scanned" image (PNG).

Used to demonstrate the multimodal / LMM step: instead of plain text, the note
arrives as an image (as a faxed or scanned chart would), and Claude reads it
directly via vision — no separate OCR engine required.

We add a slight rotation and a faint speckle to imitate a real scan.
"""

import random
import textwrap

from PIL import Image, ImageDraw, ImageFont

LINES_PER_PAGE = 38  # what fits on one 850x1100 "page" at 26px line height
WRAP_COLS = 68       # chars that fit the printable width in 18pt Courier


def _load_font():
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New.ttf", 18)
    except OSError:
        return ImageFont.load_default()


def _render_page(lines: list[str], out_path: str, rnd: random.Random) -> str:
    W, H = 850, 1100
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    font = _load_font()

    y = 50
    for line in lines:
        draw.text((55, y), line, fill=(20, 20, 20), font=font)
        y += 26

    # Faint scan speckle.
    for _ in range(1500):
        x, yy = rnd.randint(0, W - 1), rnd.randint(0, H - 1)
        shade = rnd.randint(200, 240)
        img.putpixel((x, yy), (shade, shade, shade))

    # Slight skew, like a page fed crooked.
    img = img.rotate(rnd.uniform(-1.2, 1.2), expand=False, fillcolor="white")
    img.save(out_path)
    return out_path


def render(note_text: str, out_path: str, seed: int = 7) -> str:
    """Render the first page only (kept for back-compat; see render_pages)."""
    return render_pages(note_text, out_path, seed=seed)[0]


def render_pages(note_text: str, out_path: str, seed: int = 7) -> list[str]:
    """Render the whole note as one PNG per page, wrapping long lines.

    Returns the page paths: ["...note.png"] for one page, otherwise
    ["...note_p1.png", "...note_p2.png", ...].
    """
    rnd = random.Random(seed)
    lines: list[str] = []
    for raw in note_text.splitlines():
        lines.extend(textwrap.wrap(raw, WRAP_COLS) or [""])

    pages = [lines[i:i + LINES_PER_PAGE] for i in range(0, len(lines), LINES_PER_PAGE)] or [[]]
    if len(pages) == 1:
        return [_render_page(pages[0], out_path, rnd)]

    stem, dot, ext = out_path.rpartition(".")
    return [
        _render_page(page, f"{stem}_p{n}{dot}{ext}" if dot else f"{out_path}_p{n}", rnd)
        for n, page in enumerate(pages, start=1)
    ]


if __name__ == "__main__":
    import os

    here = os.path.dirname(__file__)
    notes = os.path.join(here, "..", "data", "notes")
    with open(os.path.join(notes, "note1.txt")) as f:
        text = f.read()
    out = os.path.join(notes, "scanned_note.png")
    render(text, out)
    print("wrote", out)
