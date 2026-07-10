# Exhibit planning

Every slide must have a page brief before production. A page brief is not only a layout instruction; it is the analytical contract for the page.

Use `references/content-density.md` as the default quality bar. Unless the user explicitly asks for a short executive brief, analytical decks should use research-heavy consulting mode.

## Page brief template

| Field | Description |
|---|---|
| Page role | Core argument, supporting analysis, recommendation, decision or appendix |
| Key question | The business question this page answers |
| Action title | The evidence-backed conclusion placed at the top of the slide |
| Evidence IDs | Facts and calculations already registered in `evidence.json` |
| Required data points | Specific numbers, definitions, quotes or facts that must appear on the page |
| Comparison basis | Peer, historical period, segment, geography, scenario or benchmark |
| Analysis method | Trend, bridge, benchmark, decomposition, scoring, sensitivity, scenario or synthesis |
| Primary exhibit | The chart, table or analytical visual that proves the title |
| Insight annotations | Two to four implications to call out directly on the exhibit |
| Decision implication | What this means for the audience's decision or next action |
| Data source | Source, retrieval date, calculation basis or explicit `team assumption` |
| Caveat | Limitations, assumptions, counter-evidence or uncertainty |
| Appendix link | Backup page containing methodology, detail or source table |
| Density target | Executive, standard or research-heavy |
| Unresolved gaps | Missing evidence that must be researched, assumed visibly or removed |

## Recommended YAML structure

```yaml
page: 5
page_role: core_argument
key_question: What is driving the margin gap versus peers?
action_title: Product mix and service-delivery cost explain most of the 6.2-point margin gap
content_density_target: research-heavy
evidence_ids: [F018, F019, F020, F021, C006]
required_data_points:
  - company gross margin for the last five years
  - peer median and interquartile range
  - revenue mix by segment
  - delivery-cost bridge by major driver
comparison_basis:
  type: peer_and_historical
  peers: [Peer A, Peer B, Peer C]
  periods: [FY2022, FY2023, FY2024, FY2025, LTM]
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

## Quality bar

- No evidence, no page.
- No comparison or analytical method, no analytical page.
- The exhibit must prove the action title, not merely decorate the page.
- Core analytical pages normally require 4–8 evidence items; two is the minimum floor.
- A single statistic without history, peer, segment or scenario context is usually insufficient.
- If the evidence is complex, retain the conclusion in the core deck and move methodology, source tables and sensitivities into a linked appendix page.
- If a data point is illustrative, label it clearly and register it as an assumption.
- Generic frameworks, icon rows and architecture boxes must be supplemented with quantified baselines, targets, design decisions, trade-offs or implementation detail.
- If the action title is stronger than the available evidence, weaken the title or continue research.

## Research task derivation

Convert every unresolved field into a research task before production. Tasks should be granular enough that a researcher can return a usable fact rather than a general summary.

Bad task:

```text
Research the cloud market.
```

Good task:

```text
For page 4, retrieve 2022–2026 public-cloud revenue or market-size estimates from at least one primary or recognized institutional source, identify the included service categories, calculate CAGR, compare the top three providers, and find one credible source that challenges the base forecast.
```

## Completion test

A page brief is ready for production only when:

1. the action title is supported by registered evidence;
2. the required data points are available or visibly marked as assumptions;
3. a comparison basis and analysis method are defined;
4. the page has two to four planned insight annotations;
5. the decision implication is explicit;
6. detailed backup has an appendix destination where needed;
7. unresolved gaps are empty or approved as visible assumptions.

Covers, section dividers and explicitly requested conceptual framework pages are exempt from data-point minimums, but not from storyline relevance.