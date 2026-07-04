"""Automated QA for consulting-style PPTX files."""
from __future__ import annotations
import argparse
import json
import re
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from pptx import Presentation

SLIDE_W_CM = 33.87
SLIDE_H_CM = 19.05
EMU_PER_CM = 360000
ACTION_TERMS = ["will", "can", "should", "must", "reduce", "increase", "improve", "enable", "deliver", "requires", "offers", "prevents", "降低", "提升", "实现", "建议", "需要", "应", "将", "可"]
BANNED_TERMS = {"organization": "组织", "strategy": "战略", "stakeholder": "相关方", "alignment": "对齐", "capability": "能力", "initiative": "举措"}

@dataclass
class Finding:
    severity: str
    slide: int | None
    check: str
    message: str


def cm(value):
    return value / EMU_PER_CM


def shape_text(shape):
    if not getattr(shape, "has_text_frame", False):
        return ""
    return "\n".join(p.text for p in shape.text_frame.paragraphs).strip()


def first_top_text(slide):
    candidates = []
    for shape in slide.shapes:
        text = shape_text(shape)
        if text and cm(shape.top) <= 2.8 and cm(shape.left) <= 22:
            candidates.append((cm(shape.top), cm(shape.left), text))
    return sorted(candidates)[0][2] if candidates else None


def is_action_title(title):
    low = title.lower()
    return len(title.strip()) > 8 and (re.search(r"\d", title) or any(term in low or term in title for term in ACTION_TERMS))


def has_font_xml(path, font):
    marker = 'typeface="' + font + '"'
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if name.startswith("ppt/slides/slide") and name.endswith(".xml"):
                if marker in zf.read(name).decode("utf-8", errors="ignore"):
                    return True
    return False


def run_qa(path: Path):
    prs = Presentation(str(path))
    findings = []
    if not has_font_xml(path, "Arial"):
        findings.append(Finding("error", None, "font_xml", "Missing Arial font in slide XML"))
    if not has_font_xml(path, "Microsoft YaHei"):
        findings.append(Finding("error", None, "font_xml", "Missing Microsoft YaHei font in slide XML"))
    for idx, slide in enumerate(prs.slides, start=1):
        texts = [shape_text(shape) for shape in slide.shapes if shape_text(shape)]
        all_text = "\n".join(texts)
        cover_like = idx == 1 or any(re.fullmatch(r"\d{2}", text.strip()) for text in texts)
        if not cover_like:
            title = first_top_text(slide)
            if not title:
                findings.append(Finding("error", idx, "action_title", "Missing top action title"))
            else:
                if len(title) > 95:
                    findings.append(Finding("warning", idx, "action_title", "Title may exceed two lines"))
                if not is_action_title(title):
                    findings.append(Finding("warning", idx, "action_title", "Title may be a topic label"))
        if len(re.findall(r"\d", all_text)) >= 8 and not re.search(r"(来源[:：]|Source:)\s*\S+", all_text):
            findings.append(Finding("warning", idx, "source_line", "Numeric-heavy slide may need a source line"))
        for term, zh in BANNED_TERMS.items():
            if re.search(r"\b" + re.escape(term) + r"\b", all_text.lower()):
                findings.append(Finding("warning", idx, "terminology", f"Consider Chinese term for {term}: {zh}"))
        for shape in slide.shapes:
            x1, y1 = cm(shape.left), cm(shape.top)
            x2, y2 = x1 + cm(shape.width), y1 + cm(shape.height)
            if x1 < -0.05 or y1 < -0.05 or x2 > SLIDE_W_CM + 0.05 or y2 > SLIDE_H_CM + 0.05:
                findings.append(Finding("error", idx, "bounds", "Shape out of bounds"))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    findings = run_qa(args.pptx)
    if args.json:
        print(json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2))
    else:
        for finding in findings:
            where = f"slide {finding.slide}" if finding.slide else "deck"
            print(f"[{finding.severity.upper()}] {where} | {finding.check}: {finding.message}")
        if not findings:
            print("QA passed")
    return 1 if any(finding.severity == "error" for finding in findings) else 0

if __name__ == "__main__":
    raise SystemExit(main())
