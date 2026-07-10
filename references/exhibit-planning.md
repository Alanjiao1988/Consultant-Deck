# Exhibit planning

Every slide must have a page brief before production. A page brief is not only a layout instruction; it is the analytical contract for the page.

Use `references/content-density.md` as the default quality bar. Unless the user explicitly asks for a short executive brief, analytical decks should use research-heavy consulting mode.

## Page brief template

| Field | Description |
|---|---|
| Page role | Core argument, supporting analysis, recommendation, decision or appendix |
| Key question | The business question this page answers |
| Action title | The evidence-backed conclusion placed at the top of the slide |
| Title quantification | Numeric anchor for the title, a dedicated research task, or a justified non-numeric rationale |
| Evidence IDs | Facts and calculations already registered in `evidence.json` |
| Required data points | Specific numbers, definitions, quotes or facts that must appear on the page |
| Quantification | The core baseline, target, gap, range or metric the page will establish |
| Comparison basis | The analytical comparison type: peer, historical period, segment, geography or scenario |
| Benchmark | The actual comparable entity, value, range or threshold, including its source |
| Analysis method | Trend, bridge, benchmark, decomposition, scoring, sensitivity, scenario or synthesis |
| Primary exhibit | The chart, table or analytical visual that proves the title |
| Insight annotations | Two to four implications to call out directly on the exhibit |
| Decision implication | What this means for the audience's decision or next action |
| Data source | Source, retrieval date, calculation basis or explicit `team assumption` |
| Caveat | Limitations, assumptions, counter-evidence or uncertainty |
| Appendix link | Backup page containing methodology, detail or source table |
| Density target | Executive, standard or research-heavy |
| Minimum registered numbers | Optional page-specific override for final PPTX density QA |
| Unresolved gaps | Missing evidence that must be researched, assumed visibly or removed |

`Comparison basis` and `Benchmark` are deliberately separate. `Comparison basis` describes the method, such as peer comparison. `Benchmark` identifies the actual comparator and value, such as `peer median = 35%, derived from Peer A/B/C FY2025 filings`.

## Recommended YAML structure

```yaml
page: 5
page_role: core_argument
key_question: What is driving the margin gap versus peers?
action_title: Product mix and service-delivery cost explain most of the 6.2-point margin gap
title_quantification:
  status: resolved
  metric: margin gap
  value: 6.2
  unit: percentage_points
content_density_target: research-heavy
min_registered_numbers: 3
evidence_ids: [F018, F019, F020, F021, C006]
required_data_points:
  - company gross margin for the last five years
  - peer median and interquartile range
  - revenue mix by segment
  - delivery-cost bridge by major driver
quantification:
  baseline: company margin 24.8%
  target: peer median 31.0%
  gap: 6.2 percentage points
comparison_basis:
  type: peer_and_historical
  periods: [FY2022, FY2023, FY2024, FY2025, LTM]
benchmark:
  type: peer_median
  entities: [Peer A, Peer B, Peer C]
  value: 31.0%
  source: peer filings and team calculation
analysis_method: variance_bridge
primary_exhibit: margin bridge plus five-year peer benchmark
insight_annotations:
  - mix shift explains roughly half of the gap
  - delivery cost remains structurally above peer median
  - pricing is a secondary rather than primary driver
decision_implication: prioritize service-delivery redesign before broad price increases
data_source:
  - company filings
  - peer filings
  - team calculation
caveat: segment disclosures are not perfectly comparable
appendix_link: A7
unresolved_gaps: []
```

## Action-title quantification workflow

If the proposed action title has no number, range or threshold, create a dedicated `title_quantification` research task before production.

Example:

```yaml
title_quantification:
  status: research_task
  task: Find a defensible quantified delivery-cycle reduction versus the current baseline
  required_output:
    - current median cycle time
    - target or observed cycle time
    - sample and period
    - source and caveat
  attempts: 0
```

After three reasonable searches with no defensible result, the task may become:

```yaml
title_quantification:
  status: justified_non_numeric
  rationale: No comparable cycle-time disclosures were found; the page instead uses client interview evidence and explicitly limits the conclusion
  search_log: research-log.md#page-5-title
```

Do not insert an unsupported number merely to make the title look stronger.

## Quantification quality

A valid `quantification` field should identify at least one of:

- baseline → target → gap;
- current value versus benchmark;
- historical start and end values plus growth;
- downside/base/upside range;
- component values that reconcile to a total;
- threshold and actual performance;
- scope, budget and exit gate by implementation wave.

A label such as `cost improvement` is not quantification.

## Benchmark quality

A valid benchmark should identify the comparator, number and definition. Useful benchmark types include:

- own historical performance;
- named peers or peer median;
- industry average or best-in-class threshold;
- contractual SLA or regulatory threshold;
- management guidance;
- base case versus upside/downside;
- approved budget, hurdle rate or target KPI.

When no external benchmark is available, use a clearly labeled internal threshold or scenario and explain the limitation.

## Quality bar

- No evidence, no page.
- No quantification, no analytical page.
- No comparison method and concrete benchmark, no analytical page.
- The exhibit must prove the action title, not merely decorate the page.
- Core analytical pages normally require 4–8 evidence items; two is the minimum floor.
- Research-heavy page bodies must normally expose at least 3 unique registered numeric facts.
- A single statistic without history, peer, segment or scenario context is usually insufficient.
- If the evidence is complex, retain the conclusion in the core deck and move methodology, source tables and sensitivities into a linked appendix page.
- If a data point is illustrative, label it clearly and register it as an assumption.
- Generic frameworks, icon rows and architecture boxes must be supplemented with quantified baselines, targets, design decisions, trade-offs or implementation detail.
- If the action title is stronger than the available evidence, weaken the title or continue research.

## Research task derivation

Convert every unresolved field into a research task before production. Tasks should be granular enough that a researcher can return usable facts rather than a general summary.

Bad task:

```text
Research the cloud market.
```

Good task:

```text
For page 4, retrieve 2022–2026 public-cloud revenue or market-size estimates from at least one primary or recognized institutional source; return at least three time points, calculate CAGR, compare one to two relevant providers or an industry benchmark, define included service categories, and find one credible source that challenges the base forecast.
```

A research task that returns only one isolated number is incomplete unless the source itself exposes no time series or comparables and the limitation is recorded.

## Completion test

A page brief is ready for production only when:

1. the action title is supported by registered evidence;
2. a non-numeric title has a completed quantification task or justified rationale;
3. the required data points are available or visibly marked as assumptions;
4. `quantification` identifies the central metric, gap, range or decomposition;
5. a comparison basis and concrete benchmark are defined;
6. the page has two to four planned insight annotations;
7. the decision implication is explicit;
8. detailed backup has an appendix destination where needed;
9. unresolved gaps are empty or approved as visible assumptions.

Covers, section dividers and explicitly requested conceptual-framework pages are exempt from numeric minimums, but not from storyline relevance. Explicit framework pages should remain within the deck-level limit defined in `references/content-density.md`.
