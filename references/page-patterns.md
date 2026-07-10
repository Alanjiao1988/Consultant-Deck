# Page patterns

Use these patterns as analytical structures, not decorative layouts. Every core page must also satisfy `references/content-density.md`.

## Executive summary

Use 3–5 blocks. Each block contains:

- an evidence-backed conclusion sentence;
- one quantified impact or proof point;
- one supporting implication;
- links to the supporting pages and evidence IDs.

At least one block should state the decision required, one should quantify expected impact, and one should state the primary risk or success condition.

## SCQA page

Use four columns or stacked blocks: Situation, Complication, Question and Answer. Keep the language concise, but include at least one quantified fact in Situation or Complication. The Answer must point to the recommendation and supporting analysis.

## Annotated one-chart page

Use a primary chart in the left or center area and a right insight rail containing:

- two to four evidence-based observations;
- one implication;
- one caveat or definition;
- an appendix reference where methodology is detailed.

The chart must prove the action title. Avoid a chart with no benchmark, no annotations or no stated implication.

## Benchmark small multiples

Use 3–6 aligned charts or mini-tables to compare periods, peers, segments or geographies. Keep axes and definitions consistent. Highlight the outlier or decision-relevant gap and include the peer median or relevant threshold.

## Variance or driver bridge

Use for revenue, margin, cost, capacity, adoption or performance gaps. Show starting value, driver contributions and ending value. Register both source values and derived calculations in `evidence.json`.

## 2x2 matrix

Use for prioritization or portfolio choices only when the two axes have clear definitions and evidence-backed scores. Preferred pattern: left 2x2 plus right insight rail containing:

- scoring method and evidence IDs;
- implications for each decision-relevant quadrant;
- sensitivity or caveat;
- recommended action.

Do not place items based only on intuition without visibly marking the scores as assumptions.

## Roadmap

Use workstreams as rows and periods as columns. Show:

- named deliverables;
- owners;
- measurable exit criteria;
- decision gates;
- dependencies;
- target KPIs;
- critical-path markers.

Avoid generic phase labels without specific outputs. If the roadmap requires more than 4–5 periods, use a high-level roadmap in the core deck and a detailed appendix workplan.

## Waterfall

Use for TCO, savings, revenue bridge and margin bridge. Validate that start plus deltas equals end. Include definitions, period, currency, calculation basis and at least one explanatory annotation for the largest drivers.

## Heatmap

Use for maturity, controls, risk, capability readiness or requirement fit. Explain the scoring scale and evidence behind the ratings. Add row or column totals, benchmarks or priority flags so the heatmap leads to a decision.

## Option evaluation table

Rows are options and columns are criteria. Include:

- criteria weights and rationale;
- evidence behind each score;
- weighted total;
- sensitivity to material weight changes;
- key trade-offs and implementation consequences;
- reason for rejecting the second-best option.

## Scenario table

Use base, upside and downside columns with explicit assumptions, operating outputs, financial impact and trigger conditions. Keep scenario definitions internally consistent and trace every derived metric to registered facts.

## RACI matrix

Use for governance, operating model and implementation roles. Keep roles to 4–6 and activities to 5–8 where possible. Add decision rights, escalation rules and cadence where the RACI alone would be ambiguous.

## Risk matrix

Use likelihood × impact, but do not stop at the dots. Add a mitigation table with trigger, owner, timing, residual risk and escalation threshold. Ratings should have an evidence basis or be marked as team judgment.

## Architecture page

Use layers such as experience, orchestration, knowledge/data, model/platform and control/governance. Add:

- current-state pain points or constraints;
- 3–5 explicit design decisions;
- 2–4 quantified service, cost, security or performance targets;
- key interfaces and control points;
- trade-offs and dependencies;
- implication for implementation sequence.

Avoid mixing business process and infrastructure on the same visual plane unless the relationship is the analytical point.

## Detailed table page

Use when decision-making requires more detail than a chart can carry. Limit the main table to the rows and columns needed for the conclusion, highlight the decisive cells, and place the full table in the appendix. Add an insight rail rather than forcing the audience to interpret the table unaided.

## Source and methodology appendix

Use a structured table with fact ID, metric, definition, period, value, source, retrieval date, calculation basis and pages used. For derived calculations, show formulas and input fact IDs. This page should make the core analysis auditable.