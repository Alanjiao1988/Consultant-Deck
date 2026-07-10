from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.qa_pptx import load_facts, numeric_facts


def test_nonfinite_values_remain_qualitative_and_do_not_count_for_density(tmp_path):
    evidence = tmp_path / "evidence.json"
    evidence.write_text(
        json.dumps(
            {
                "facts": [
                    {"id": "Q_NAN", "claim": "NaN is not a usable metric", "value": "NaN"},
                    {"id": "Q_INF", "claim": "Infinity is not a usable metric", "value": "Infinity"},
                    {"id": "Q_NINF", "claim": "Negative infinity is not a usable metric", "value": "-Infinity"},
                ],
                "calculations": [],
            }
        ),
        encoding="utf-8",
    )

    records = load_facts(evidence)
    assert len(records) == 3
    assert all(record["evidence_type"] == "qualitative" for record in records)
    assert all(record["value"] is None for record in records)
    assert numeric_facts(records) == []
