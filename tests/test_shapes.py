from pathlib import Path
import sys
import zipfile
from pptx import Presentation
from pptx.util import Cm

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.consulting_layouts import SLIDE_W, SLIDE_H, add_action_title
from scripts.consulting_shapes import add_textbox, waterfall, native_chart


def blank_deck():
    prs = Presentation()
    prs.slide_width = Cm(SLIDE_W)
    prs.slide_height = Cm(SLIDE_H)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    return prs, slide


def test_font_xml_contains_latin_and_ea(tmp_path):
    prs, slide = blank_deck()
    add_action_title(slide, "分三波迁移可在 18 个月内降低 TCO")
    add_textbox(slide, "中文 English 123", 1, 3, 10, 1)
    out = tmp_path / "font.pptx"
    prs.save(out)
    with zipfile.ZipFile(out) as zf:
        xml = "\n".join(zf.read(name).decode("utf-8", errors="ignore") for name in zf.namelist() if name.startswith("ppt/slides/slide"))
    assert 'typeface="Arial"' in xml
    assert 'typeface="Microsoft YaHei"' in xml


def test_waterfall_math_validation():
    _, slide = blank_deck()
    waterfall(slide, [("Base", 100, "start"), ("Saving", -20, "delta"), ("Target", 80, "end")], 1, 3, 10, 6)


def test_native_chart_validates_series_length():
    _, slide = blank_deck()
    try:
        native_chart(slide, "bar", ["A", "B"], [("x", [1])], 1, 3, 10, 5)
    except ValueError:
        return
    raise AssertionError("Expected ValueError")
