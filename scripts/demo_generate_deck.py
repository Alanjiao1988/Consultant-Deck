"""Generate a small end-to-end mixed Chinese-English consulting deck and evidence table."""
from pathlib import Path
import json
import sys
from datetime import date
from pptx import Presentation
from pptx.util import Cm

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.consulting_layouts import SLIDE_W, SLIDE_H, cover_page, add_action_title, add_footer, exec_summary_block
from scripts.consulting_shapes import matrix_2x2_with_insights, risk_matrix, option_evaluation_table, add_textbox
from scripts.architecture_helpers import layered_architecture
from scripts.business_case import business_case_summary


def blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def write_demo_evidence(path):
    evidence = {
        "facts": [
            {
                "id": "F001",
                "claim": "AI platform reuse can reach payback within 18 months in the illustrative base case.",
                "value": 18,
                "unit": "months",
                "definition": "Payback period under illustrative base-case assumptions.",
                "source_type": "assumption",
                "source": "Illustrative demo assumption",
                "retrieved": str(date.today()),
                "counter_evidence": "Actual payback may be longer if platform reuse or adoption is lower than assumed.",
                "used_on_pages": [2, 5]
            },
            {
                "id": "F002",
                "claim": "Three-year net benefit is $18m in the illustrative base case.",
                "value": 18,
                "unit": "$m",
                "definition": "Cumulative illustrative pre-tax net benefit over three years.",
                "source_type": "assumption",
                "source": "Illustrative demo assumption",
                "retrieved": str(date.today()),
                "counter_evidence": "Benefit depends on realised automation and productivity capture.",
                "used_on_pages": [5]
            },
            {
                "id": "F003",
                "claim": "Run-rate saving reaches 22% for the target process scope.",
                "value": 22,
                "unit": "%",
                "definition": "Illustrative run-rate saving for target process scope.",
                "source_type": "assumption",
                "source": "Illustrative demo assumption",
                "retrieved": str(date.today()),
                "counter_evidence": "Savings may be lower if process standardisation is limited.",
                "used_on_pages": [5]
            },
            {
                "id": "F004",
                "claim": "One-off investment is $7m for platform and change work.",
                "value": 7,
                "unit": "$m",
                "definition": "Illustrative one-off investment for platform build and change management.",
                "source_type": "assumption",
                "source": "Illustrative demo assumption",
                "retrieved": str(date.today()),
                "counter_evidence": "Investment may be higher with stricter security, data remediation or integration scope.",
                "used_on_pages": [5]
            }
        ]
    }
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def generate(output=ROOT / "examples" / "demo_ai_transformation.pptx", evidence_output=None):
    prs = Presentation()
    prs.slide_width = Cm(SLIDE_W)
    prs.slide_height = Cm(SLIDE_H)

    slide = blank(prs)
    cover_page(slide, "银行 AI 转型路线图", "Mixed Chinese-English consulting demo deck", "Illustrative client", str(date.today()))

    slide = blank(prs)
    add_action_title(slide, "银行可通过先内后外的 AI 用例排序，在 18 个月内更快释放价值")
    exec_summary_block(slide, [("优先方向", "先扩展内部知识工作流，再推进外部客户 chatbot。", ["高价值用例集中在风险控制与员工效率场景。", "外部 AI 触点需要更成熟的权限、审计与模型评估机制。"]), ("落地方式", "先建设可复用平台与治理资产，再规模化 domain copilot。", ["复用 RAG（检索增强生成）和 evaluation 模式，可减少试点蔓延。", "Hub-and-spoke 运营模式兼顾集中治理与业务采用。"])])
    add_footer(slide, 2, "Illustrative analysis；团队假设", lang="zh")

    slide = blank(prs)
    add_action_title(slide, "内部知识工作流在价值与就绪度之间提供最佳 Wave 1 平衡")
    matrix_2x2_with_insights(slide, 1.4, 3.0, 10.8, "Execution readiness", "Business value", points=[("RM copilot", .72, .74), ("Call summary", .84, .62), ("Credit memo", .58, .78), ("Customer chatbot", .35, .68)], quadrant_labels=["Defer", "Quick wins", "Strategic bets", "Scale first"], quadrant_implications=[("Scale first", "低外部暴露与可复用数据模式，使其适合作为 Wave 1。"), ("Strategic bets", "价值较高，但大规模上线前需要更强控制机制。")])
    add_footer(slide, 3, "Illustrative scoring；示意数据", lang="zh")

    slide = blank(prs)
    add_action_title(slide, "共享 AI 平台可避免试点蔓延，并缩短后续 use case 交付周期")
    layered_architecture(slide, [("体验层", ["RM copilot", "Ops assistant", "Employee search"]), ("编排层", ["Prompt flow", "Tool calling", "Policy routing"]), ("知识层", ["Vector index", "Document store", "Entitlements"]), ("模型层", ["GPT models", "Embedding", "Evaluation"]), ("控制层", ["Audit log", "DLP", "Monitoring"])], 1.4, 3.2, 30.5, 10.6)
    add_footer(slide, 4, "Illustrative architecture；示意数据", lang="zh")

    slide = blank(prs)
    add_action_title(slide, "如平台复用提升交付效率，路线图可在 18 个月内达到 payback")
    business_case_summary(slide, [("3 年净收益", "$18m", "税前口径", "good"), ("Payback", "18 mo", "base case", "good"), ("Run-rate saving", "22%", "目标流程范围", "good"), ("一次性投入", "$7m", "平台 + 变革", "neutral")], [("Y0", 0, -7, -7), ("Y1", 8, -3, 5), ("Y2", 12, -2, 10), ("Y3", 15, -2, 13)], 1.4, 3.0, 30.5, 10.5)
    add_footer(slide, 5, "Illustrative business case；团队假设", lang="zh")

    slide = blank(prs)
    add_action_title(slide, "最高风险集中在数据泄露与外部触点失控，应优先建设上线门禁")
    risk_matrix(slide, [("Data leakage", 4, 5, "security"), ("Wrong answer", 3, 4, "quality"), ("Low adoption", 3, 3, "change")], 1.4, 3.2, 11.5, 9.2)
    add_textbox(slide, "Mitigation priorities", 14.2, 3.2, 10, .5, 11, True)
    add_textbox(slide, "– 生产上线前强制 evaluation gate\n– 启用 entitlement-aware retrieval 与 DLP\n– 内部 assistant 与外部 chatbot 分阶段推进", 14.2, 4.0, 16.5, 2.4, 10.3)
    add_footer(slide, 6, "Illustrative risk assessment；示意数据", lang="zh")

    slide = blank(prs)
    add_action_title(slide, "Platform-first 路径更优，因为它最大化复用且不延迟首批价值")
    option_evaluation_table(slide, ["Pilot-only", "Platform-first", "Big-bang"], ["Time", "Reuse", "Risk", "Cost", "Scale"], [[5, 2, 2, 4, 2], [4, 5, 5, 4, 5], [2, 5, 4, 2, 4]], 1.4, 3.1, 30.5, 8.0)
    add_footer(slide, 7, "Illustrative option scoring；示意数据", lang="zh")

    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(output)
    evidence_path = Path(evidence_output) if evidence_output else output.with_suffix(".evidence.json")
    write_demo_evidence(evidence_path)
    print(output)
    print(evidence_path)


if __name__ == "__main__":
    generate()
