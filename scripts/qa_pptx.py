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

@dataclass
class NumberToken:
    slide: int
    value: float
    unit: str
    text: str


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
        cjk_chars = len(re.findall(r"[\u3400-\u9fff]", cleaned))
        return cjk_chars <= 14 and len(cleaned) <= 28
    words = re.findall(r"[A-Za-z][A-Za-z\-]*", cleaned.lower())
    if any(word in EN_ACTION_SIGNALS for word in words):
        return False
    if re.search(r"[:;—–]|\b(to|by|because|through|within|without)\b", cleaned, re.IGNORECASE):
        return False
    return len(words) <= 7


def has_font_xml(path, font):
    marker = 'typeface="' + font + '"'
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if name.startswith("ppt/slides/slide") and name.endswith(".xml"):
                if marker in zf.read(name).decode("utf-8", errors="ignore"):
                    return True
    return False


def canonical_unit(unit):
    u = (unit or "").strip().lower()
    if u in {"%", "percent", "percentage"}:
        return "%"
    if u in {"$m", "usd m", "usd million", "million usd"}:
        return "$m"
    if u in {"$bn", "usd bn", "usd billion", "billion usd"}:
        return "$bn"
    if u in {"$k", "usd k", "usd thousand"}:
        return "$k"
    if u in {"$", "usd"}:
        return "$"
    if u in {"个月", "月", "mo", "mos", "month", "months"}:
        return "months"
    if u in {"年", "yr", "yrs", "year", "years"}:
        return "years"
    return u or "plain"


def load_facts(path: Path | None):
    if path is None:
        return []
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    facts = []
    for item in data.get("facts", []):
        facts.append({
            "id": item.get("id", "UNKNOWN"),
            "claim": item.get("claim", ""),
            "value": float(item.get("value")),
            "unit": canonical_unit(item.get("unit", "plain")),
            "source_type": item.get("source_type", ""),
            "used_on_pages": set(int(p) for p in item.get("used_on_pages", [])),
        })
    return facts


def values_equal(a, b):
    return abs(float(a) - float(b)) < 1e-6


def unit_compatible(a, b):
    return canonical_unit(a) == canonical_unit(b)


def strip_dates(text):
    text = re.sub(r"\b20\d{2}[-/]\d{1,2}[-/]\d{1,2}\b", " ", text)
    text = re.sub(r"20\d{2}年\d{1,2}月\d{1,2}日", " ", text)
    return text


def extract_number_tokens(text, slide_num):
    """Extract basic Arabic-numeral facts. Prefer low false positives over full recall."""
    working = strip_dates(text)
    tokens = []

    def consume(pattern, unit_func, min_value=None):
        nonlocal working, tokens
        matches = list(re.finditer(pattern, working, flags=re.IGNORECASE))
        if not matches:
            return
        chars = list(working)
        for match in matches:
            value = float(match.group("value"))
            unit = canonical_unit(unit_func(match))
            if min_value is None or value >= min_value:
                tokens.append(NumberToken(slide_num, value, unit, match.group(0)))
            for i in range(match.start(), match.end()):
                chars[i] = " "
        working = "".join(chars)

    consume(r"\$\s*(?P<value>\d+(?:\.\d+)?)\s*(?P<suffix>m|bn|k)?\b", lambda m: "$" + (m.group("suffix") or ""))
    consume(r"(?P<value>\d+(?:\.\d+)?)\s*%", lambda m: "%")
    consume(r"(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>个月|月|months?|mo|mos)\b?", lambda m: m.group("unit"))
    # Short year-period labels such as “3 年净收益” are usually metric labels, not facts.
    consume(r"(?P<value>\d+(?:\.\d+)?)\s*(?P<unit>年|years?|yrs?)\b?", lambda m: m.group("unit"), min_value=6)

    for match in re.finditer(r"\b(?P<value>\d+(?:\.\d+)?)\b", working):
        value = float(match.group("value"))
        if value <= 12:
            continue
        tokens.append(NumberToken(slide_num, value, "plain", match.group(0)))
    return tokens


def text_shapes_for_fact_scan(slide, slide_num):
    for shape in slide.shapes:
        text = shape_text(shape)
        if not text:
            continue
        left, top = cm(shape.left), cm(shape.top)
        # Ignore page-number footers and tiny bottom-right labels.
        if left > 30 and top > 17:
            continue
        yield text


def token_matches_fact(token, fact):
    return unit_compatible(token.unit, fact["unit"]) and values_equal(token.value, fact["value"])


def run_fact_consistency(prs, facts):
    if not facts:
        return []
    findings = []
    tokens = []
    for idx, slide in enumerate(prs.slides, start=1):
        texts = [shape_text(shape) for shape in slide.shapes if shape_text(shape)]
        if is_cover_or_divider(idx, texts):
            continue
        for text in text_shapes_for_fact_scan(slide, idx):
            tokens.extend(extract_number_tokens(text, idx))

    for token in tokens:
        matching_facts = [fact for fact in facts if token_matches_fact(token, fact)]
        if not matching_facts:
            findings.append(Finding("warning", token.slide, "fact_consistency", f"Unregistered number: {token.text}"))
            continue
        if not any((not fact["used_on_pages"] or token.slide in fact["used_on_pages"]) for fact in matching_facts):
            findings.append(Finding("warning", token.slide, "fact_consistency", f"Registered number appears on unlisted page: {token.text}"))

    for fact in facts:
        for page in fact["used_on_pages"]:
            page_tokens = [token for token in tokens if token.slide == page and unit_compatible(token.unit, fact["unit"])]
            if not page_tokens:
                continue
            if not any(values_equal(token.value, fact["value"]) for token in page_tokens):
                seen = ", ".join(token.text for token in page_tokens[:5])
                findings.append(Finding("error", page, "fact_consistency", f"Fact {fact['id']} expected {fact['value']:g}{fact['unit']} but page shows {seen}"))
    return findings


def run_qa(path: Path, facts_path: Path | None = None):
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

        if not cover_or_divider:
            if len(re.findall(r"\d", all_text)) >= 8 and not re.search(r"(来源[:：]|Source:)\s*\S+", all_text):
                findings.append(Finding("warning", idx, "source_line", "Numeric-heavy slide may need a source line"))

        # Terminology applies to any Chinese or mixed-language slide, including cover/divider pages.
        if has_cjk(all_text):
            for term, zh in BANNED_TERMS.items():
                if re.search(r"\b" + re.escape(term) + r"\b", all_text.lower()):
                    findings.append(Finding("warning", idx, "terminology", f"Consider Chinese term for {term}: {zh}"))

        for shape in slide.shapes:
            x1, y1 = cm(shape.left), cm(shape.top)
            x2, y2 = x1 + cm(shape.width), y1 + cm(shape.height)
            if x1 < -0.05 or y1 < -0.05 or x2 > SLIDE_W_CM + 0.05 or y2 > SLIDE_H_CM + 0.05:
                findings.append(Finding("error", idx, "bounds", "Shape out of bounds"))

    findings.extend(run_fact_consistency(prs, load_facts(facts_path)))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--facts", type=Path, default=None, help="Optional evidence.json fact table for numeric consistency checks")
    args = parser.parse_args(argv)
    findings = run_qa(args.pptx, args.facts)
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
