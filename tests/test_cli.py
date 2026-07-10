from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.create_template import main as template_main
from scripts.demo_generate_deck import main as demo_main


def test_create_template_cli_honors_output(tmp_path):
    output = tmp_path / "custom_template.pptx"
    assert template_main(["--output", str(output)]) == 0
    assert output.exists() and output.stat().st_size > 0


def test_demo_cli_honors_all_output_paths(tmp_path):
    output = tmp_path / "custom_demo.pptx"
    evidence = tmp_path / "custom_evidence.json"
    briefs = tmp_path / "custom_briefs.yaml"
    assert demo_main(
        [
            "--output", str(output),
            "--evidence-output", str(evidence),
            "--briefs-output", str(briefs),
        ]
    ) == 0
    assert output.exists() and output.stat().st_size > 0
    assert evidence.exists() and evidence.stat().st_size > 0
    assert briefs.exists() and briefs.stat().st_size > 0
