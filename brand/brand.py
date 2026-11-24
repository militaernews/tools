"""Logos and social images in the Militär-News radar look.

    python brand.py path/to/brand.json

brand.json (paths relative to it):
    {
      "name": "PTB-KIT",                       wordmark, letters A–Z, digits 0–9, "-" and spaces
      "icon": "kit",                           a built-in icon (icons/<name>.svg) or a path to your own fragment
      "tagline": ["Shared pieces for", "python-telegram-bot bots."],
      "tags": "TRANSLATIONS · SAFE LOGS · ERROR REPORTS",
      "out": "."                               where logo.svg/.png and social.svg/.png go
    }

An icon fragment is SVG drawn in a 512×512 box that may use the gradients and filters #col, #glow,
#screen and #sweep. PNGs need `pip install resvg-py` and the Noto Sans fonts.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Geometric stroke letters, 100 units high, like the Militär-News wordmark (A without crossbar)
O = "M10 0H50Q60 0 60 10V90Q60 100 50 100H10Q0 100 0 90V10Q0 0 10 0Z"
P = "M0 100V0H46Q60 0 60 14V36Q60 50 46 50H0"
GLYPHS: dict[str, tuple[str, float]] = {
    "A": ("M0 100L31 0L62 100", 62),
    "B": ("M0 100V0H44Q56 0 56 12V36Q56 48 44 48H0M44 48Q60 48 60 62V88Q60 100 48 100H0", 60),
    "C": ("M60 0H10Q0 0 0 10V90Q0 100 10 100H60", 60),
    "D": ("M0 0V100H40Q60 100 60 80V20Q60 0 40 0Z", 60),
    "E": ("M56 0H0V100H56M0 50H44", 56),
    "F": ("M0 100V0H56M0 48H44", 56),
    "G": ("M60 0H10Q0 0 0 10V90Q0 100 10 100H50Q60 100 60 90V55H32", 60),
    "H": ("M0 0V100M60 0V100M0 50H60", 60),
    "I": ("M0 0V100", 0),
    "J": ("M44 0V90Q44 100 34 100H0", 44),
    "K": ("M0 0V100M58 0L6 56M24 38L60 100", 60),
    "L": ("M0 0V100H56", 56),
    "M": ("M0 100V0L36 60L72 0V100", 72),
    "N": ("M0 100V0L60 100V0", 60),
    "O": (O, 60),
    "P": (P, 60),
    "Q": (O + "M38 78L64 104", 64),
    "R": (P + "M30 50L60 100", 60),
    "S": ("M60 0H10Q0 0 0 10V40Q0 50 10 50H50Q60 50 60 60V90Q60 100 50 100H0", 60),
    "T": ("M0 0H62M31 0V100", 62),
    "U": ("M0 0V90Q0 100 10 100H50Q60 100 60 90V0", 60),
    "V": ("M0 0L31 100L62 0", 62),
    "W": ("M0 0L20 100L42 30L64 100L84 0", 84),
    "X": ("M0 0L60 100M60 0L0 100", 60),
    "Y": ("M0 0L31 50L62 0M31 50V100", 62),
    "Z": ("M0 0H60L0 100H60", 60),
    "0": (O + "M60 0L0 100", 60),
    "1": ("M10 16L30 0V100", 30),
    "2": ("M0 0H50Q60 0 60 10V40Q60 50 50 50H10Q0 50 0 60V100H60", 60),
    "3": ("M0 0H60V100H0M14 50H60", 60),
    "4": ("M44 100V0L0 70H60", 60),
    "5": ("M60 0H0V50H50Q60 50 60 60V90Q60 100 50 100H0", 60),
    "6": ("M56 0H10Q0 0 0 10V90Q0 100 10 100H50Q60 100 60 90V60Q60 50 50 50H0", 60),
    "7": ("M0 0H60L20 100", 60),
    "8": ("M10 0H50Q60 0 60 10V100H0V0Z" + "M0 50H60", 60),
    "9": ("M60 50H10Q0 50 0 40V10Q0 0 10 0H50Q60 0 60 10V90Q60 100 50 100H4", 60),
    "-": ("M0 54H34", 34),
    " ": ("", 20),
}
UMLAUTS = str.maketrans({"Ä": "A", "Ö": "O", "Ü": "U", "ß": "S"})


def wordmark_width(text: str, gap: float = 22) -> float:
    widths = [GLYPHS[c][1] for c in text]
    return sum(widths) + gap * (len(widths) - 1)


def wordmark(text: str, x: float, y: float, height: float, gap: float = 22) -> str:
    text = text.upper().translate(UMLAUTS)
    unknown = sorted({c for c in text if c not in GLYPHS})
    if unknown:
        raise ValueError(f"no glyph for {''.join(unknown)!r}")
    scale = height / 100
    parts, cursor = [], 0.0
    for char in text:
        path, width = GLYPHS[char]
        if path:
            parts.append(f'<path transform="translate({cursor:.1f} 0)" d="{path}"/>')
        cursor += width + gap
    return (
        f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="#f2fbff" stroke-width="9" '
        f'stroke-linecap="square" stroke-linejoin="miter" filter="url(#glow)">{"".join(parts)}</g>'
    )


def radar(cx: float, cy: float, r: float) -> str:
    rings = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r * f:.1f}" fill="none" stroke="#5fd0ff" stroke-opacity=".28" stroke-width="2"/>' for f in (0.25, 0.5, 0.75))
    spokes = "".join(
        f'<line x1="{cx}" y1="{cy}" x2="{cx + r * math.cos(math.radians(a)):.1f}" y2="{cy + r * math.sin(math.radians(a)):.1f}" stroke="#5fd0ff" stroke-opacity="{0.3 if a % 90 == 0 else 0.13}" stroke-width="{2 if a % 90 == 0 else 1.5}"/>'
        for a in range(0, 360, 30)
    )
    ticks = f'<circle cx="{cx}" cy="{cy}" r="{r - 9:.1f}" fill="none" stroke="#7fdcff" stroke-opacity=".45" stroke-width="6" stroke-dasharray="1.5 {2 * math.pi * (r - 9) / 120 - 1.5:.2f}"/>'
    a0, a1 = math.radians(-100), math.radians(-40)
    sweep = (
        f'<path d="M{cx} {cy}L{cx + r * math.cos(a0):.1f} {cy + r * math.sin(a0):.1f}A{r} {r} 0 0 1 {cx + r * math.cos(a1):.1f} {cy + r * math.sin(a1):.1f}Z" fill="url(#sweep)"/>'
        f'<line x1="{cx}" y1="{cy}" x2="{cx + r * math.cos(a1):.1f}" y2="{cy + r * math.sin(a1):.1f}" stroke="#9be7ff" stroke-opacity=".8" stroke-width="2.5"/>'
    )
    blips = "".join(
        f'<circle cx="{cx + r * d * math.cos(math.radians(a)):.1f}" cy="{cy + r * d * math.sin(math.radians(a)):.1f}" r="{s}" fill="#8fe6ff" filter="url(#glow)"/>'
        for a, d, s in ((-60, 0.62, 5), (-75, 0.35, 3.5), (200, 0.7, 4), (150, 0.55, 3), (30, 0.8, 4.5), (100, 0.82, 3), (-20, 0.45, 3))
    )
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#screen)"/>{rings}{spokes}{sweep}{blips}{ticks}'
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#2ec5ff" stroke-opacity=".7" stroke-width="3"/>'
    )


DEFS = """<defs>
	<radialGradient id="screen" cx=".45" cy=".4" r=".7">
		<stop offset="0" stop-color="#1f6fae"/><stop offset=".55" stop-color="#0c3a6b"/><stop offset="1" stop-color="#061a36"/>
	</radialGradient>
	<linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
		<stop offset="0" stop-color="#2ec5ff" stop-opacity="0"/><stop offset="1" stop-color="#2ec5ff" stop-opacity=".35"/>
	</linearGradient>
	<linearGradient id="col" x1="0" x2="1">
		<stop offset="0" stop-color="#04122a" stop-opacity=".95"/><stop offset=".5" stop-color="#0d3768" stop-opacity=".9"/><stop offset="1" stop-color="#04122a" stop-opacity=".95"/>
	</linearGradient>
	<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
		<feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
	</filter>
</defs>"""

BACKGROUND = "#1b1029"


def svg(width: int, height: int, body: str) -> str:
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">{DEFS}{body}</svg>'


def load_icon(value: str, base: Path) -> str:
    path = HERE / "icons" / f"{value}.svg"
    if not path.exists():
        path = (base / value).resolve()
    text = path.read_text(encoding="utf-8")
    return "\n".join(line for line in text.splitlines() if not line.strip().startswith("<!--"))


def logo(icon: str) -> str:
    return svg(512, 512, f'<rect width="512" height="512" fill="{BACKGROUND}"/>{radar(256, 256, 240)}{icon}')


def social(icon: str, name: str, tagline: list[str], tags: str) -> str:
    # The wordmark fills at most 560 px next to the radar, at most 96 px high
    height = min(96.0, 560 / (wordmark_width(name.upper().translate(UMLAUTS)) / 100))
    lines = "".join(
        f'<text x="662" y="{400 + 46 * i}" font-family="Noto Sans" font-size="36" fill="#cfefff">{escape(line)}</text>'
        for i, line in enumerate(tagline[:2])
    )
    tag_y = 400 + 46 * max(1, len(tagline[:2])) + 20
    return svg(
        1280,
        640,
        f'<rect width="1280" height="640" fill="{BACKGROUND}"/>{radar(320, 320, 290)}'
        f'<g transform="translate(320 320) scale(1.12) translate(-256 -256)">{icon}</g>'
        + wordmark(name, 660, 301 - height, height)
        + lines
        + (f'<text x="662" y="{tag_y}" font-family="Noto Sans" font-weight="700" font-size="22" fill="#2ec5ff" letter-spacing="1">{escape(tags)}</text>' if tags else ""),
    )


def escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render(out: Path, name: str, width: int) -> bool:
    try:
        import resvg_py
    except ImportError:
        return False
    fonts = [str(p) for p in Path.home().glob(".local/share/fonts/**/NotoSans-*.ttf")]
    fonts += [str(p) for p in Path("/usr/share/fonts").glob("**/NotoSans-*.ttf")]
    png = resvg_py.svg_to_bytes(svg_path=str(out / f"{name}.svg"), width=width, font_files=fonts or None)
    (out / f"{name}.png").write_bytes(bytes(png))
    return True


def build(config_path: Path) -> list[Path]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    base = config_path.parent
    out = (base / config.get("out", ".")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    icon = load_icon(config["icon"], base)
    (out / "logo.svg").write_text(logo(icon), encoding="utf-8")
    (out / "social.svg").write_text(social(icon, config["name"], config.get("tagline", []), config.get("tags", "")), encoding="utf-8")
    written = [out / "logo.svg", out / "social.svg"]
    if render(out, "logo", 640) and render(out, "social", 1280):
        written += [out / "logo.png", out / "social.png"]
    else:
        print("resvg-py not installed: SVGs written, PNGs unchanged")
    return written


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    for path in build(Path(sys.argv[1])):
        print(path)
