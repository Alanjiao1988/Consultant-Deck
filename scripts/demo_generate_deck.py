"""Generate a small end-to-end demo consulting deck."""
from pathlib import Path
import sys
from datetime import date
from pptx import Presentation
from pptx.util import Cm

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.consulting_layouts import SLIDE_W, SLIDE_H, cover_page, add_action_title, add_footer, exec_summary_block
from scripts.consulting_shapes import matrix_2x2_with_insights, native_chart, risk_matrix, option_evaluation_table, add_textbox
from scripts.architecture_helpers import layered_architecture
from scripts.business_case import business_case_summary


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def generate(output=ROOT / "examples" / "demo_ai_transformation.pptx"):
    prs = Presentation()
    prs.slide_width = Cm(SLIDE_W)
    prs.slide_height = Cm(SLIDE_H)

    slide = blank(prs)
    cover_page(slide, "AI transformation strategy for a banking client", "Consulting-style demo deck", "Illustrative client", str(date.today()))

    slide = blank(prs)
    add_action_title(slide, "The bank can unlock AI value faster by sequencing use cases around readiness and risk")
    exec_summary_block(slide, [("Where to play", "Prioritize internal knowledge workflows before external chatbots.", ["High-value use cases cluster in risk and productivity workflows.", "External-facing AI requires stronger control maturity."]), ("How to win", "Build reusable platform and governance assets before scaling domain copilots.", ["Reusable RAG and evaluation patterns avoid pilot sprawl.", "Hub-and-spoke ownership balances control and adoption."])])
    add_footer(slide, 2, "Illustrative analysis;示意数据")

    slide = blank(prs)
    add_action_title(slide, "Internal knowledge workflows offer the best first-wave balance of value and execution readiness")
    matrix_2x2_with_insights(slide, 1.4, 3.0, 10.8, "Execution readiness", "Business value", points=[("RM copilot", .72, .74), ("Call summary", .84, .62), ("Credit memo", .58, .78), ("Customer chatbot", .35, .68)], quadrant_labels=["Defer", "Quick wins", "Strategic bets", "Scale first"], quadrant_implications=[("Scale first", "Reusable data patterns and low external exposure make these candidates ideal for Wave 1."), ("Strategic bets", "High value but stronger controls are required before broad rollout.")])
    add_footer(slide, 3, "Illustrative scoring;示意数据")

    slide = blank(prs)
    add_action_title(slide, "A shared AI platform prevents pilot sprawl and shortens delivery cycles for future use cases")
    layered_architecture(slide, [("Experience", ["RM copilot", "Ops assistant", "Employee search"]), ("Orchestration", ["Prompt flow", "Tool calling", "Policy routing"]), ("Knowledge", ["Vector index", "Document store", "Entitlements"]), ("Model", ["GPT models", "Embedding", "Evaluation"]), ("Control", ["Audit log", "DLP", "Monitoring"])], 1.4, 3.2, 30.5, 10.6)
    add_footer(slide, 4, "Illustrative architecture;示意数据")

    slide = blank(prs)
    add_action_title(slide, "The roadmap can reach payback within 18 months if platform reuse lifts delivery productivity")
    business_case_summary(slide, [("3-year net benefit", "$18m", "before tax", "good"), ("Payback", "18 mo", "base case", "good"), ("Run-rate saving", "22%", "target process scope", "good"), ("One-off investment", "$7m", "platform + change", "neutral")], [("Y0", 0, -7, -7), ("Y1", 8, -3, 5), ("Y2", 12, -2, 10), ("Y3", 15, -2, 13)], 1.4, 3.0, 30.5, 10.5)
    add_footer(slide, 5, "Illustrative business case;示意数据")

    slide = blank(prs)
    add_action_title(slide, "The highest risks concentrate in data leakage and uncontrolled external-facing deployment")
    risk_matrix(slide, [("Data leakage", 4, 5, "security"), ("Wrong answer", 3, 4, "quality"), ("Low adoption", 3, 3, "change")], 1.4, 3.2, 11.5, 9.2)
    add_textbox(slide, "Mitigation priorities", 14.2, 3.2, 10, .5, 11, True)
    add_textbox(slide, "– Mandate evaluation gates before production\n– Enforce entitlement-aware retrieval and DLP\n– Separate internal assistant rollout from external chatbot path", 14.2, 4.0, 16.5, 2.4, 10.3)
    add_footer(slide, 6, "Illustrative risk assessment;示意数据")

    slide = blank(prs)
    add_action_title(slide, "A platform-first path is preferable because it maximizes reuse without delaying first value")
    option_evaluation_table(slide, ["Pilot-only", "Platform-first", "Big-bang"], ["Time", "Reuse", "Risk", "Cost", "Scale"], [[5, 2, 2, 4, 2], [4, 5, 5, 4, 5], [2, 5, 4, 2, 4]], 1.4, 3.1, 30.5, 8.0)
    add_footer(slide, 7, "Illustrative option scoring;示意数据")

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(output)
    print(output)


if __name__ == "__main__":
    generate()
