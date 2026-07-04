from pathlib import Path
import json
import sys
import zipfile
from pptx import Presentation
from pptx.util import Cm

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.consulting_layouts import SLIDE_W, SLIDE_H, add_action_title
from scripts import consulting_shapes as shapes
from scripts.consulting_shapes import add_textbox, waterfall, native_chart
from scripts.demo_generate_deck import generate as generate_demo
from scripts.qa_pptx import run_qa


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


def test_theme_json_matches_shape_constants():
    theme = json.loads((ROOT / "assets" / "theme.json").read_text(encoding="utf-8"))
    assert theme["fonts"]["latin"] == shapes.FONT_LATIN
    assert theme["fonts"]["east_asian"] == shapes.FONT_EA
    assert theme["colors"]["primary"].lstrip("#") == shapes.PRIMARY
    assert theme["colors"]["accent"].lstrip("#") == shapes.ACCENT
    assert theme["colors"]["text"].lstrip("#") == shapes.GRAY_TEXT
    assert theme["colors"]["secondary_text"].lstrip("#") == shapes.GRAY_2
    assert theme["colors"]["light_text"].lstrip("#") == shapes.GRAY_3
    assert theme["colors"]["line"].lstrip("#") == shapes.GRAY_LINE
    assert theme["colors"]["fill"].lstrip("#") == shapes.GRAY_FILL


def test_demo_deck_has_no_qa_false_positive_findings(tmp_path):
    out = tmp_path / "demo_ai_transformation.pptx"
    generate_demo(out)
    findings = run_qa(out)
    assert findings == []
