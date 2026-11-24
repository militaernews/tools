# tools

Small tools for militaernews projects.

## brand: logos in the radar look

`brand/brand.py` draws a project's logo (512×512, also as a 640 px PNG) and its social preview image
(1280×640) in the Militär-News radar style: a dark navy radar screen with a cyan sweep, a glowing
line-art icon, and the name as thin uppercase stroke lettering.

```
pip install resvg-py          # for the PNGs; the SVGs need nothing
python brand/brand.py path/to/brand.json
```

`brand.json`, with paths relative to it:

```json
{
  "name": "PTB-KIT",
  "icon": "kit",
  "tagline": ["Shared pieces for", "python-telegram-bot bots."],
  "tags": "TRANSLATIONS · SAFE LOGS · ERROR REPORTS",
  "out": "."
}
```

- `name`: the wordmark (A–Z, 0–9, `-`, spaces; Ä/Ö/Ü are drawn without dots). Long names shrink to fit.
- `icon`: a built-in icon from `brand/icons/` (`pillar`, `kit`) or a path to your own SVG fragment,
  drawn in a 512×512 box. Fragments may use the gradients and filters `#col`, `#glow`, `#screen` and
  `#sweep`.
- `tagline`: up to two lines under the name; `tags`: one cyan line of keywords.

The text uses Noto Sans (looked up in `~/.local/share/fonts` and `/usr/share/fonts`).

Used by [litfass](https://github.com/militaernews/litfass) and [ptb-kit](https://github.com/militaernews/ptb-kit).

## Development

```
pip install pytest
cd brand && pytest
```

MIT licensed.
