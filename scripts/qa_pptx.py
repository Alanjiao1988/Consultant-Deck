"""Automated QA for consulting-style PPTX files."""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml
from pptx import Presentation

SLIDE_W_CM = 33.87
SLIDE_H_CM = 19.05
EMU_PER_CM = 360000

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
CN_ACTION_SIGNALS = [
    "降低", "提升", "实现", "建议", "需要", "应", "将", "可", "必须", "能够",
    "优先", "集中", "更", "最佳", "风险", "收益", "回收", "减少", "增加",
]
BANNED_TERMS = {
    "organization": "组织",
    "strategy": "战略",
    "stakeholder": "相关方",
    "alignment": "对齐",
    "capability": "能力",
    "initiative": "举措",
}
EXEMPT_ROLES = {"cover", "section_divider", "divider", "navigation", "agenda"}
CONCEPT_ROLES = {"conceptual_framework", "concept", "framework"}
QUALITATIVE_PATTERNS = {
    "显著": re.compile(r"显著(?:提升|降低|增长|下降|改善|增加|减少)"),
    "大幅": re.compile(r"大幅(?:提升|降低|增长|下降|改善|增加|减少)"),
    "明显": re.compile(r"明显(?:高于|低于|提升|降低|增长|下降|改善)"),
    "快速": re.compile(r"快速(?:增长|提升|下降|扩张|收缩)"),
    "领先": re.compile(r"领先(?:于|同业|行业|市场)"),
    "大量": re.compile(r"大量(?:节省|减少|增加|增长)"),
    "significantly": re.compile(r"\bsignificantly\b", re.IGNORECASE),
    "substantially": re.compile(r"\bsubstantially\b", re.IGNORECASE),
    "rapidly": re.compile(r"\brapidly\b", re.IGNORECASE),
    "materially": re.compile(r"\bmaterially\b", re.IGNORECASE),
    "leading": re.compile(r"\bleading\s+(?:peers?|the industry|the market)\b", re.IGNORECASE),
}


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
    if getattr(shape, "has_text_frame", False):
        return "\n".join(p.text for p in shape.text_frame.paragraphs).strip()
    if getattr(shape, "has_table", False):
        return "\n".join(
            cell.text
            for row in shape.table.rows
            for cell in row.cells
            if cell.text
        ).strip()
    return ""


def has_cjk(text):
    return re.search(r"[\u3400-\u9fff]", text) is not None


def first_top_shape(slide):
    candidates = []
    for shape in slide.shapes:
        text = shape_text(shape)
        if text and cm(shape.top) <= 2.8 and cm(shape.left) <= 22:
            candidates.append((cm(shape.top), cm(shape.left), shape))
    return sorted(candidates, key=lambda item: (item[0], item[1]))[0][2] if candidates else None


def first_top_text(slide):
    shape = first_top_shape(slide)
    return shape_text(shape) if shape is not None else None


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
    for section in ("facts", "calculations"):
        for item in data.get(section, []):
            try:
                value = float(item.get("value"))
            except (TypeError, ValueError):
                continue
            facts.append({
                "id": item.get("id", "UNKNOWN"),
                "claim": item.get("claim", ""),
                "value": value,
                "unit": canonical_unit(item.get("unit", "plain")),
                "source_type": item.get("source_type", ""),
                "used_on_pages": set(int(p) for p in item.get("used_on_pages", [])),
            })
    return facts


def load_briefs(path: Path | None):
    if path is None:
        return {}, {}
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, list):
        pages = data
        meta = {}
    elif isinstance(data, dict):
        pages = data.get("pages", [])
        meta = data
    else:
        return {}, {}
    mapping = {}
    for index, page in enumerate(pages, start=1):
        if not isinstance(page, dict):
            continue
        page_num = page.get("page", page.get("page_num", index))
        try:
            mapping[int(page_num)] = page
        except (TypeError, ValueError):
            continue
    return meta, mapping


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
            value = float(match.group("value").replace(",", ""))
            unit = canonical_unit(unit_func(match))
            if min_value is None or abs(value) >= min_value:
                tokens.append(NumberToken(slide_num, value, unit, match.group(0)))
            for i in range(match.start(), match.end()):
                chars[i] = " "
        working = "".join(chars)

    consume(r"\$\s*(?P<value>-?\d[\d,]*(?:\.\d+)?)\s*(?P<suffix>m|bn|k)?\b", lambda m: "$" + (m.group("suffix") or ""))
    consume(r"(?P<value>-?\d[\d,]*(?:\.\d+)?)\s*%", lambda m: "%")
    consume(r"(?P<value>-?\d[\d,]*(?:\.\d+)?)\s*(?P<unit>个月|月|months?|mo|mos)(?![A-Za-z])", lambda m: m.group("unit"))
    consume(r"(?P<value>-?\d[\d,]*(?:\.\d+)?)\s*(?P<unit>年|years?|yrs?)(?![A-Za-z])", lambda m: m.group("unit"), min_value=6)

    for match in re.finditer(r"\b(?P<value>-?\d[\d,]*(?:\.\d+)?)\b", working):
        value = float(match.group("value").replace(",", ""))
        if abs(value) <= 12:
            continue
        tokens.append(NumberToken(slide_num, value, "plain", match.group(0)))
    return tokens


def text_shapes_for_fact_scan(slide, slide_num, exclude_shape=None):
    for shape in slide.shapes:
        if exclude_shape is not None and shape == exclude_shape:
            continue
        text = shape_text(shape)
        if not text:
            continue
        left, top = cm(shape.left), cm(shape.top)
        if left > 30 and top > 17:
            continue
        if top > 16.2:
            continue
        yield text


def chart_values(slide):
    values = []
    for shape in slide.shapes:
        if not getattr(shape, "has_chart", False):
            continue
        for series in shape.chart.series:
            for value in series.values:
                if value is not None:
                    values.append(float(value))
    return values


def token_matches_fact(token, fact):
    return unit_compatible(token.unit, fact["unit"]) and values_equal(token.value, fact["value"])


def fact_applies_to_page(fact, page):
    return not fact["used_on_pages"] or page in fact["used_on_pages"]


def run_fact_consistency(prs, facts):
    if not facts:
        return []
    findings = []
    tokens = []
    slide_chart_values = {}
    slide_text = {}
    for idx, slide in enumerate(prs.slides, start=1):
        texts = [shape_text(shape) for shape in slide.shapes if shape_text(shape)]
        if is_cover_or_divider(idx, texts):
            continue
        body_parts = list(text_shapes_for_fact_scan(slide, idx))
        slide_text[idx] = "\n".join(body_parts)
        slide_chart_values[idx] = chart_values(slide)
        for text in body_parts:
            tokens.extend(extract_number_tokens(text, idx))

    for token in tokens:
        matching_facts = [fact for fact in facts if token_matches_fact(token, fact)]
        if not matching_facts:
            findings.append(Finding("warning", token.slide, "fact_consistency", f"Unregistered number: {token.text}"))
            continue
        if not any(fact_applies_to_page(fact, token.slide) for fact in matching_facts):
            findings.append(Finding("warning", token.slide, "fact_consistency", f"Registered number appears on unlisted page: {token.text}"))

    for fact in facts:
        for page in fact["used_on_pages"]:
            page_tokens = [token for token in tokens if token.slide == page and unit_compatible(token.unit, fact["unit"])]
            if any(values_equal(token.value, fact["value"]) for token in page_tokens):
                continue
            if any(values_equal(value, fact["value"]) for value in slide_chart_values.get(page, [])):
                continue
            raw_pattern = re.compile(rf"(?<![\d.]){re.escape(f'{fact['value']:g}')}(?![\d.])")
            if raw_pattern.search(slide_text.get(page, "")):
                continue
            if page_tokens:
                seen = ", ".join(token.text for token in page_tokens[:5])
                findings.append(Finding(
                    "error", page, "fact_consistency",
                    f"Fact {fact['id']} expected {fact['value']:g}{fact['unit']} but page shows {seen}",
                ))
    return findings


def registered_fact_ids_on_slide(slide, slide_num, facts):
    if not facts:
        return set()
    title_shape = first_top_shape(slide)
    tokens = []
    for text in text_shapes_for_fact_scan(slide, slide_num, exclude_shape=title_shape):
        tokens.extend(extract_number_tokens(text, slide_num))
    chart_nums = chart_values(slide)
    matched = set()
    for fact in facts:
        if not fact_applies_to_page(fact, slide_num):
            continue
        if any(token_matches_fact(token, fact) for token in tokens):
            matched.add(fact["id"])
            continue
        if any(values_equal(value, fact["value"]) for value in chart_nums):
            matched.add(fact["id"])
    return matched


def brief_role(brief):
    return str(brief.get("page_role", brief.get("role", "core_argument"))).strip().lower()


def brief_density(brief, meta):
    value = brief.get("content_density_target", meta.get("content_density_target", "research-heavy"))
    return str(value).strip().lower().replace("_", "-")


def density_threshold(brief, meta):
    explicit = brief.get("min_registered_numbers")
    if explicit is not None:
        try:
            return max(0, int(explicit))
        except (TypeError, ValueError):
            pass
    density = brief_density(brief, meta)
    return {"executive": 1, "executive-brief": 1, "standard": 2, "research-heavy": 3}.get(density, 3)


def is_density_exempt(brief):
    role = brief_role(brief)
    if role in EXEMPT_ROLES:
        return True
    return role in CONCEPT_ROLES and bool(brief.get("explicitly_requested"))


def run_data_density(prs, facts, briefs_meta, briefs):
    if not facts:
        return []
    findings = []
    concept_count = 0
    eligible_count = 0

    for idx, slide in enumerate(prs.slides, start=1):
        texts = [shape_text(shape) for shape in slide.shapes if shape_text(shape)]
        if is_cover_or_divider(idx, texts):
            continue
        brief = briefs.get(idx, {})
        role = brief_role(brief)
        if role in CONCEPT_ROLES and bool(brief.get("explicitly_requested")):
            concept_count += 1
        if role not in EXEMPT_ROLES:
            eligible_count += 1
        if is_density_exempt(brief):
            continue

        threshold = density_threshold(brief, briefs_meta)
        matched = registered_fact_ids_on_slide(slide, idx, facts)
        if len(matched) < threshold:
            findings.append(Finding(
                "warning", idx, "data_density",
                f"Only {len(matched)} registered numeric facts are visible in the slide body; expected at least {threshold}",
            ))

    if briefs and eligible_count:
        max_share = briefs_meta.get("max_framework_share", 0.25)
        try:
            max_share = float(max_share)
        except (TypeError, ValueError):
            max_share = 0.25
        share = concept_count / eligible_count
        if share > max_share:
            findings.append(Finding(
                "warning", None, "data_density",
                f"Explicit conceptual-framework pages are {share:.0%} of eligible pages; maximum is {max_share:.0%}",
            ))
    return findings


def run_qualitative_claim_scan(slide, slide_num):
    findings = []
    title_shape = first_top_shape(slide)
    body = "\n".join(text_shapes_for_fact_scan(slide, slide_num, exclude_shape=title_shape))
    units_pattern = re.compile(r"\d|%|\$|€|£|倍|点|bps?\b", re.IGNORECASE)
    seen = set()
    for sentence in re.split(r"[\n。！？!?;；]+", body):
        sentence = sentence.strip()
        if not sentence or units_pattern.search(sentence):
            continue
        for label, pattern in QUALITATIVE_PATTERNS.items():
            if pattern.search(sentence) and label not in seen:
                findings.append(Finding(
                    "warning", slide_num, "qualitative_claim",
                    f"Qualitative claim '{label}' has no number or range in the same statement",
                ))
                seen.add(label)
    return findings


def run_qa(path: Path, facts_path: Path | None = None, briefs_path: Path | None = None):
    prs = Presentation(str(path))
    facts = load_facts(facts_path)
    briefs_meta, briefs = load_briefs(briefs_path)
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
            findings.extend(run_qualitative_claim_scan(slide, idx))

        if has_cjk(all_text):
            for term, zh in BANNED_TERMS.items():
                if re.search(r"\b" + re.escape(term) + r"\b", all_text.lower()):
                    findings.append(Finding("warning", idx, "terminology", f"Consider Chinese term for {term}: {zh}"))

        for shape in slide.shapes:
            x1, y1 = cm(shape.left), cm(shape.top)
            x2, y2 = x1 + cm(shape.width), y1 + cm(shape.height)
            if x1 < -0.05 or y1 < -0.05 or x2 > SLIDE_W_CM + 0.05 or y2 > SLIDE_H_CM + 0.05:
                findings.append(Finding("error", idx, "bounds", "Shape out of bounds"))

    findings.extend(run_fact_consistency(prs, facts))
    findings.extend(run_data_density(prs, facts, briefs_meta, briefs))
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("pptx", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--facts", type=Path, default=None, help="Optional evidence.json fact table for numeric consistency checks")
    parser.add_argument("--briefs", type=Path, default=None, help="Optional briefs.yaml for page-role and density thresholds")
    args = parser.parse_args(argv)
    findings = run_qa(args.pptx, args.facts, args.briefs)
    if args.json:
        print(json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2))
    else:
        for finding in findings:
            where = f"slide {finding.slide}" if finding.slide is not None else "deck"
            print(f"[{finding.severity}] {where} {finding.check}: {finding.message}")
    return 1 if any(finding.severity == "error" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
