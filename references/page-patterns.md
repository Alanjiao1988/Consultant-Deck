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

## Chart plus data table

Use when the audience needs both the visual pattern and exact values. Place the chart above the table or use a left-chart/right-table layout.

Requirements:

- the chart and table use the same categories, periods, units and definitions;
- the table contains exact values, while the chart highlights trend or comparison;
- decisive rows or columns are highlighted;
- the insight rail explains the implication rather than repeating the table;
- use `chart_with_data_table()` and `dense_table()` where practical.

This is the preferred pattern for financial trends, market development, utilization, adoption, capacity and KPI reviews.

## Benchmark bar

Use a horizontal bar when entity names are long or the primary question is relative position.

Include:

- the company or recommended option highlighted in primary color;
- peers in gray;
- a peer median, industry average, best-in-class or threshold line;
- exact values and consistent definitions;
- one annotation explaining the size and practical meaning of the gap.

Use `benchmark_bar()` or `native_chart(..., chart_type="bar_h")`.

## Benchmark small multiples

Use 3–6 aligned charts or mini-tables to compare periods, peers, segments or geographies. Keep axes and definitions consistent. Highlight the outlier or decision-relevant gap and include the peer median or relevant threshold.

## Market-size page: TAM / SAM / SOM

Do not use a decorative funnel with labels only. Show:

- TAM, SAM and SOM values with units and forecast year;
- the explicit filtering logic from TAM to SAM and SOM;
- historical or forecast growth for at least 2–3 periods;
- a source definition for each market boundary;
- an alternative estimate or sensitivity where market definitions vary;
- the revenue-share or penetration assumption connecting SOM to the business case.

Use a quantified funnel, driver tree or chart-plus-table pattern.

## KPI baseline–target–gap page

Use a four-column structure:

| KPI | Current baseline | Target / benchmark | Gap and action |
|---|---:|---:|---|

Include owner, target date and measurement definition where the page supports execution. A target without a baseline and external or internal benchmark is insufficient.

## Unit-economics page

Use for cost per transaction, margin per customer, CAC/LTV, cloud unit cost, model inference cost, service-delivery economics or similar questions.

Include:

- the unit definition and volume denominator;
- revenue or benefit per unit;
- variable and allocated cost components;
- contribution margin or net value per unit;
- current versus target or peer benchmark;
- sensitivity to volume, utilization or price;
- a detailed input table or appendix link.

Preferred exhibits are a waterfall plus dense input table, or a quantified driver tree.

## Variance or driver bridge

Use for revenue, margin, cost, capacity, adoption or performance gaps. Show starting value, driver contributions and ending value. Register both source values and derived calculations in `evidence.json`.

## Quantified driver tree

Use when a result must be decomposed into controllable drivers, for example:

- revenue = customers × ARPU;
- TCO = infrastructure + license + labor + migration;
- benefit = volume × adoption × time saved × loaded labor cost;
- capacity = resources × utilization × productivity.

Every node should carry a value and unit where possible. Child nodes must reconcile to the parent or clearly state that they are non-additive drivers. Use `driver_tree()`.

## 2x2 matrix

Use for prioritization or portfolio choices only when the two axes have clear definitions and evidence-backed scores. Preferred pattern: left 2x2 plus right insight rail containing:

- scoring method and evidence IDs;
- implications for each decision-relevant quadrant;
- sensitivity or caveat;
- recommended action.

Do not place items based only on intuition without visibly marking the scores as assumptions.

## Quantified roadmap

Use workstreams as rows and periods as columns. Show:

- named deliverables;
- owners;
- measurable exit criteria;
- decision gates;
- dependencies;
- target KPIs;
- critical-path markers;
- quantified scope per wave, such as `12 systems`, `2,000 users`, `$2.4m`, `70% adoption` or `99.9% availability`.

Avoid generic phase labels without specific outputs. If the roadmap requires more than 4–5 periods, use a high-level roadmap in the core deck and a detailed appendix workplan. A dense roadmap table is often more useful than decorative arrows.

## Waterfall

Use for TCO, savings, revenue bridge and margin bridge. Validate that start plus deltas equals end. Include definitions, period, currency, calculation basis and at least one explanatory annotation for the largest drivers.

## Combo trend chart and CAGR

Use a column-plus-line chart when one metric explains the scale and a second metric explains rate or quality, for example revenue plus growth, workload plus automation, or capacity plus utilization.

Requirements:

- both series use the same periods;
- units are clear and scales are not misleading;
- the start and end values are registered facts;
- CAGR is calculated from the correct number of intervals and visibly annotated;
- use `native_chart(..., chart_type="combo")` and `cagr_annotation()`.

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

## Dense data table

Use when decision-making requires more exact values than a chart can carry. `dense_table()` supports 6–8 columns and approximately 8–10 body rows at approved font sizes.

Requirements:

- numeric columns are right-aligned and consistently formatted;
- totals and decisive rows are highlighted;
- positive and negative deltas are visually differentiated;
- the title states the conclusion so the audience does not need to inspect every cell;
- a full source table moves to appendix if the core page becomes unreadable.

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

## Source and methodology appendix

Use a structured table with fact ID, metric, definition, period, value, source, retrieval date, calculation basis and pages used. For derived calculations, show formulas and input fact IDs. This page should make the core analysis auditable.
