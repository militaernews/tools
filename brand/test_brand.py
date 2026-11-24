import json
import xml.etree.ElementTree as ET

import pytest

import brand


def test_every_glyph_and_icon_builds(tmp_path):
    config = tmp_path / "brand.json"
    config.write_text(json.dumps({"name": "ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789-ÄÖÜ", "icon": "pillar", "tagline": ["a & b"], "tags": "X"}))
    written = brand.build(config)
    for path in written:
        if path.suffix == ".svg":
            ET.fromstring(path.read_text())  # valid XML
    assert "a &amp; b" in (tmp_path / "social.svg").read_text()


def test_own_icon_and_unknown_glyph(tmp_path):
    (tmp_path / "mine.svg").write_text('<!-- comment -->\n<circle cx="256" cy="256" r="40" fill="#fff"/>')
    (tmp_path / "brand.json").write_text(json.dumps({"name": "OK", "icon": "mine.svg"}))
    brand.build(tmp_path / "brand.json")
    assert '<circle cx="256" cy="256" r="40"' in (tmp_path / "logo.svg").read_text()
    with pytest.raises(ValueError):
        brand.wordmark("€", 0, 0, 10)


def test_long_names_shrink_to_fit():
    import re

    social = brand.social("", "MILITAERNEWS TOOLS", [], "")
    scale = float(re.search(r'translate\(660 [\d.]+\) scale\(([\d.]+)\)', social).group(1))
    assert scale < 0.96 and brand.wordmark_width("MILITAERNEWS TOOLS") * scale <= 561
