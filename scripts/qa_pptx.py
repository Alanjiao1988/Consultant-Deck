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

# These signals are used only to avoid false positives. The QA rule should not try
# to prove that a title is an action title; it should only flag likely topic labels.
EN_ACTION_SIGNALS = {
    "can", "will", "should", "must", "need", "needs", "require", "requires",
    "enable", "enables", "enabled", "offer", "offers", "offered", "provide",
    "provides", "prioritize", "prioritizes", "reduce", "reduces", "increase",
    "increases", "improve", "improves", "deliver", "delivers", "prevent",
    "prevents", "concentrate", "concentrates", "prefer", "preferable", "maximize",
    "maximizes", "unlock", "unlocks", "shorten", "shortens", "reach", "reaches",
    "drive", "drives", "create", "creates", "balance", "balances", "outperform",
    "outperforms", "mitigate", "mitigates", "because", "within", "while",
    "before", "after", "therefore", "best", "better", "highest", "lowest", "faster",
    "slower", "more", "less", "first-wave", "platform-first",
}
CN_ACTION_SIGNALS = ["降低", "提升", "实现", "建议", "需要", "应", "将", "可", "必须", "能够", "优先", "集中", "更", "最佳", "风险", "收益", "回收", "减少", "增加"]
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


def has_cjk(text):
    return re.search(r"[\u3400-\u9fff]", text) is not None


def first_top_text(slide):
    candidates = []
    for shape in slide.shapes:
        text = shape_text(shape)
        if text and cm(shape.top) <= 2.8 and cm(shape.left) <= 22:
            candidates.append((cm(shape.top), cm(shape.left), text))
    return sorted(candidates)[0][2] if candidates else None


def is_cover_or_divider(idx, texts):
    if idx == 1:
        return True
    # Section dividers commonly carry a large two-digit section number.
    return any(re.fullmatch(r"\d{2}", text.strip()) for text in texts)


def looks_like_topic_label(title):
    """Return True only for likely topic labels; avoid judging full titles."""
    cleaned = re.sub(r"\s+", " ", title.strip())
    if not cleaned:
        return True
    if re.search(r"\d", cleaned):
        return False
    if has_cjk(cleaned):
        if any(signal in cleaned for signal in CN_ACTION_SIGNALS):
            return False
        # Short Chinese noun phrases such as “云迁移成本分析” are suspicious.
        cjk_chars = len(re.findall(r"[\u3400-\u9fff]", cleaned))
        return cjk_chars <= 14 and len(cleaned) <= 28
    words = re.findall(r"[A-Za-z][A-Za-z\-]*", cleaned.lower())
    if any(word in EN_ACTION_SIGNALS for word in words):
        return False
    if re.search(r"[:;—–]|\b(to|by|because|through|within|without)\b", cleaned, re.IGNORECASE):
        return False
    # Only short English noun phrases are flagged. Longer statements are left to human review.
    return len(words) <= 7


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
        cover_or_divider = is_cover_or_divider(idx, texts)

        if not cover_or_divider:
            title = first_top_text(slide)
            if not title:
                findings.append(Finding("error", idx, "action_title", "Missing top action title"))
            else:
                if len(title) > 95:
                    findings.append(Finding("warning", idx, "action_title", "Title may exceed two lines"))
                if looks_like_topic_label(title):
                    findings.append(Finding("warning", idx, "action_title", "Title may be a topic label"))

        # Cover and section divider pages are exempt from content-evidence checks.
        if not cover_or_divider:
            if len(re.findall(r"\d", all_text)) >= 8 and not re.search(r"(来源[:：]|Source:)\s*\S+", all_text):
                findings.append(Finding("warning", idx, "source_line", "Numeric-heavy slide may need a source line"))
            # The terminology blacklist applies only to Chinese or mixed Chinese-English pages.
            if has_cjk(all_text):
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
