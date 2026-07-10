"""Validate consulting deck page briefs before PowerPoint production.

This QA complements ``qa_pptx.py``. It checks whether the analytical plan is
complete enough to produce a research-heavy deck, rather than trying to infer
content quality from a rendered PPTX.
"""
from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml


EXEMPT_ROLES = {"cover", "section_divider", "divider", "navigation"}
CONCEPT_ROLES = {"conceptual_framework", "concept", "framework"}
REQUIRED_FIELDS = {
    "action_title": "Missing action title",
    "required_data_points": "Missing required data points",
    "comparison_basis": "Missing comparison basis",
    "analysis_method": "Missing analysis method",
    "primary_exhibit": "Missing primary exhibit",
    "insight_annotations": "Missing insight annotations",
    "decision_implication": "Missing decision implication",
}


@dataclass
class Finding:
    severity: str
    page: int | str | None
    check: str
    message: str


def _nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, set, dict)):
        return bool(value)
    return True


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def _load_yaml(path: Path) -> tuple[dict[str, Any], list[Any]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return {}, data
    if not isinstance(data, dict):
        raise ValueError("briefs YAML must be a list or a mapping with a 'pages' list")
    pages = data.get("pages")
    if not isinstance(pages, list):
        raise ValueError("briefs YAML mapping must contain a 'pages' list")
    return data, pages


def _load_evidence(path: Path | None) -> tuple[dict[str, dict[str, Any]], int, set[str]]:
    if path is None:
        return {}, 0, set()
    data = json.loads(path.read_text(encoding="utf-8"))
    records: dict[str, dict[str, Any]] = {}
    sources: set[str] = set()
    count = 0
    for section in ("facts", "calculations"):
        for item in data.get(section, []):
            if not isinstance(item, dict):
                continue
            item_id = str(item.get("id", "")).strip()
            if not item_id:
                continue
            records[item_id] = item
            count += 1
            source = str(item.get("source", "")).strip()
            if source:
                sources.add(source)
    return records, count, sources


def _page_number(page: dict[str, Any], index: int) -> int | str:
    return page.get("page", page.get("page_num", index + 1))


def _page_role(page: dict[str, Any]) -> str:
    return str(page.get("page_role", page.get("role", "core_argument"))).strip().lower()


def _density(page: dict[str, Any], deck_meta: dict[str, Any]) -> str:
    value = page.get("content_density_target", deck_meta.get("content_density_target", "research-heavy"))
    return str(value).strip().lower().replace("_", "-")


def _is_exempt(page: dict[str, Any]) -> bool:
    role = _page_role(page)
    if role in EXEMPT_ROLES:
        return True
    if role in CONCEPT_ROLES and bool(page.get("explicitly_requested")):
        return True
    return False


def run_qa(briefs_path: Path, evidence_path: Path | None = None) -> list[Finding]:
    deck_meta, pages = _load_yaml(briefs_path)
    evidence, evidence_count, sources = _load_evidence(evidence_path)
    findings: list[Finding] = []
    core_pages: list[dict[str, Any]] = []
    appendix_pages = 0

    if not pages:
        return [Finding("error", None, "briefs", "No pages found in briefs YAML")]

    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            findings.append(Finding("error", index + 1, "briefs", "Page brief must be a mapping"))
            continue

        page_num = _page_number(page, index)
        role = _page_role(page)
        exempt = _is_exempt(page)
        if role == "appendix":
            appendix_pages += 1
        elif not exempt:
            core_pages.append(page)

        if exempt:
            continue

        for field, message in REQUIRED_FIELDS.items():
            if not _nonempty(page.get(field)):
                findings.append(Finding("error", page_num, field, message))

        data_points = _as_list(page.get("required_data_points"))
        insights = _as_list(page.get("insight_annotations"))
        evidence_ids = [str(item).strip() for item in _as_list(page.get("evidence_ids")) if str(item).strip()]
        density = _density(page, deck_meta)

        if len(data_points) < 1:
            findings.append(Finding("error", page_num, "content_depth", "At least one required data point is needed"))
        elif density == "research-heavy" and len(data_points) < 3:
            findings.append(Finding("warning", page_num, "content_depth", "Research-heavy pages should normally define at least three required data points"))

        if len(insights) < 2:
            findings.append(Finding("error", page_num, "content_depth", "At least two insight annotations are required"))

        if len(evidence_ids) < 2:
            findings.append(Finding("error", page_num, "evidence_budget", "Core analytical pages require at least two evidence IDs"))
        elif density == "research-heavy" and len(evidence_ids) < 4:
            findings.append(Finding("warning", page_num, "evidence_budget", "Research-heavy pages should normally use four to eight evidence items"))

        for evidence_id in evidence_ids:
            if evidence_path is not None and evidence_id not in evidence:
                findings.append(Finding("error", page_num, "evidence_reference", f"Unknown evidence ID: {evidence_id}"))
                continue
            item = evidence.get(evidence_id)
            if item:
                used_pages = {str(value) for value in _as_list(item.get("used_on_pages"))}
                if used_pages and str(page_num) not in used_pages:
                    findings.append(Finding("warning", page_num, "evidence_reference", f"Evidence {evidence_id} does not list this page in used_on_pages"))

        gaps = [str(item).strip() for item in _as_list(page.get("unresolved_gaps")) if str(item).strip()]
        if gaps:
            findings.append(Finding("error", page_num, "unresolved_gaps", f"Unresolved evidence gaps remain: {', '.join(gaps)}"))

        caveat = page.get("caveat")
        if not _nonempty(caveat):
            findings.append(Finding("warning", page_num, "caveat", "No caveat or boundary condition is recorded"))

        if density == "research-heavy" and not _nonempty(page.get("appendix_link")):
            findings.append(Finding("warning", page_num, "appendix_link", "Research-heavy core pages should link to backup where detail or methodology is material"))

    mode = str(deck_meta.get("content_density_target", "research-heavy")).strip().lower().replace("_", "-")
    core_count = len(core_pages)
    if mode == "research-heavy" and core_count:
        if evidence_path is None:
            findings.append(Finding("warning", None, "deck_density", "No evidence.json supplied for deck-level density checks"))
        else:
            evidence_floor = max(2 * core_count, 12 if core_count >= 6 else 0)
            if evidence_count < evidence_floor:
                findings.append(Finding("warning", None, "deck_density", f"Only {evidence_count} facts/calculations for {core_count} core pages; expected at least about {evidence_floor}"))
            source_floor = max(4, math.ceil(core_count * 0.6))
            if len(sources) < source_floor:
                findings.append(Finding("warning", None, "deck_density", f"Only {len(sources)} distinct sources for {core_count} core pages; expected at least about {source_floor}"))

        appendix_floor = max(1, math.ceil(core_count * 0.25)) if core_count >= 4 else 0
        if appendix_pages < appendix_floor:
            findings.append(Finding("warning", None, "appendix_depth", f"Only {appendix_pages} appendix pages for {core_count} core pages; expected at least about {appendix_floor}"))

    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate consulting deck page briefs and content budgets")
    parser.add_argument("briefs", type=Path, help="Path to briefs.yaml")
    parser.add_argument("--facts", type=Path, default=None, help="Optional evidence.json for evidence-reference and deck-density checks")
    parser.add_argument("--json", action="store_true", help="Print findings as JSON")
    parser.add_argument("--fail-on-warning", action="store_true", help="Return a non-zero exit code for warnings as well as errors")
    args = parser.parse_args(argv)

    findings = run_qa(args.briefs, args.facts)
    if args.json:
        print(json.dumps([asdict(item) for item in findings], ensure_ascii=False, indent=2))
    else:
        for item in findings:
            where = f"page {item.page}" if item.page is not None else "deck"
            print(f"[{item.severity}] {where} {item.check}: {item.message}")

    if any(item.severity == "error" for item in findings):
        return 1
    if args.fail_on_warning and findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
