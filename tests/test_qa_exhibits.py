from __future__ import annotations

import json
from pathlib import Path

from scripts.demo_generate_jurisdiction_map import generate
from scripts.qa_exhibits import run_qa

ROOT = Path(__file__).resolve().parents[1]


def test_demo_exhibit_manifest_passes_semantic_qa(tmp_path):
    _, manifest = generate(tmp_path / "map.pptx", tmp_path / "map.exhibits.json")
    findings = run_qa(manifest, ROOT / "examples" / "demo_regulatory_map.evidence.json")
    assert findings == []


def test_semantic_qa_catches_legend_and_evidence_failures(tmp_path):
    _, manifest_path = generate(tmp_path / "map.pptx", tmp_path / "map.exhibits.json")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    exhibit = payload["exhibits"][0]
    exhibit["categories"].append({"id": "unused", "label": "Unused", "color": "123456"})
    exhibit["jurisdictions"][0]["evidence_ids"] = ["MISSING"]
    broken = tmp_path / "broken.exhibits.json"
    broken.write_text(json.dumps(payload), encoding="utf-8")

    findings = run_qa(broken, ROOT / "examples" / "demo_regulatory_map.evidence.json")
    assert any(item.check == "legend_usage" and item.severity == "error" for item in findings)
    assert any(item.check == "evidence_reference" and "MISSING" in item.message for item in findings)


def test_semantic_qa_rejects_missing_caveat(tmp_path):
    _, manifest_path = generate(tmp_path / "map.pptx", tmp_path / "map.exhibits.json")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    payload["exhibits"][0]["caveat"] = ""
    broken = tmp_path / "missing-caveat.exhibits.json"
    broken.write_text(json.dumps(payload), encoding="utf-8")
    findings = run_qa(broken, ROOT / "examples" / "demo_regulatory_map.evidence.json")
    assert any(item.check == "caveat" and item.severity == "error" for item in findings)
