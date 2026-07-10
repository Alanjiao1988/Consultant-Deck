from pathlib import Path
import json
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.qa_briefs import run_qa


def write_yaml(path, data):
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return path


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def evidence_records(page=2):
    return {
        "facts": [
            {
                "id": f"F00{i}",
                "claim": f"Fact {i}",
                "value": i * 10,
                "unit": "%",
                "period": "FY2025",
                "definition": "Test fact",
                "source_type": "filing",
                "source_tier": 1,
                "source": f"Source {i}",
                "retrieved": "2026-07-10",
                "used_on_pages": [page],
            }
            for i in range(1, 5)
        ],
        "calculations": [],
    }


def valid_page():
    return {
        "page": 2,
        "page_role": "core_argument",
        "key_question": "What drives the performance gap?",
        "action_title": "Three operating drivers explain most of the performance gap",
        "content_density_target": "research-heavy",
        "evidence_ids": ["F001", "F002", "F003", "F004"],
        "required_data_points": [
            "five-year company trend",
            "peer median",
            "segment decomposition",
        ],
        "comparison_basis": {"type": "peer_and_historical", "periods": ["FY2024", "FY2025"]},
        "analysis_method": "variance_bridge",
        "primary_exhibit": "driver bridge plus peer benchmark",
        "insight_annotations": ["Driver A explains half the gap", "Driver B remains above peer median"],
        "decision_implication": "Prioritize operating redesign before pricing changes",
        "data_source": ["Source 1", "Source 2", "Source 3", "Source 4"],
        "caveat": "Peer definitions are not perfectly comparable",
        "appendix_link": "A2",
        "unresolved_gaps": [],
    }


def test_valid_research_heavy_page_passes(tmp_path):
    briefs = write_yaml(
        tmp_path / "briefs.yaml",
        {"content_density_target": "research-heavy", "pages": [valid_page()]},
    )
    facts = write_json(tmp_path / "evidence.json", evidence_records())
    assert run_qa(briefs, facts) == []


def test_missing_analytical_fields_fail(tmp_path):
    page = valid_page()
    page["comparison_basis"] = None
    page["analysis_method"] = ""
    page["insight_annotations"] = ["Only one insight"]
    page["evidence_ids"] = ["F001"]
    briefs = write_yaml(tmp_path / "briefs.yaml", {"pages": [page]})
    facts = write_json(tmp_path / "evidence.json", evidence_records())
    findings = run_qa(briefs, facts)
    checks = {(finding.severity, finding.check) for finding in findings}
    assert ("error", "comparison_basis") in checks
    assert ("error", "analysis_method") in checks
    assert ("error", "content_depth") in checks
    assert ("error", "evidence_budget") in checks


def test_unknown_evidence_id_fails(tmp_path):
    page = valid_page()
    page["evidence_ids"] = ["F001", "F002", "F003", "F999"]
    briefs = write_yaml(tmp_path / "briefs.yaml", {"pages": [page]})
    facts = write_json(tmp_path / "evidence.json", evidence_records())
    findings = run_qa(briefs, facts)
    assert any(finding.severity == "error" and finding.check == "evidence_reference" and "F999" in finding.message for finding in findings)


def test_unresolved_gaps_fail(tmp_path):
    page = valid_page()
    page["unresolved_gaps"] = ["Missing peer capex definition"]
    briefs = write_yaml(tmp_path / "briefs.yaml", {"pages": [page]})
    facts = write_json(tmp_path / "evidence.json", evidence_records())
    findings = run_qa(briefs, facts)
    assert any(finding.severity == "error" and finding.check == "unresolved_gaps" for finding in findings)


def test_explicit_conceptual_framework_is_exempt(tmp_path):
    briefs = write_yaml(
        tmp_path / "briefs.yaml",
        {
            "content_density_target": "research-heavy",
            "pages": [
                {
                    "page": 2,
                    "page_role": "conceptual_framework",
                    "explicitly_requested": True,
                    "action_title": "The requested framework organizes the discussion into four domains",
                }
            ],
        },
    )
    findings = run_qa(briefs)
    assert not any(finding.severity == "error" for finding in findings)
