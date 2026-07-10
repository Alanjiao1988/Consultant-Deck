# Research-heavy content density standard

This reference defines the minimum analytical depth for a consulting deck. The objective is not to fill slides with text. The objective is to make every core page decision-useful, evidence-backed and sufficiently detailed that an executive can challenge the logic without asking for a separate research memo.

## Default output mode

Unless the user explicitly requests a short executive brief, use **research-heavy consulting mode** for strategy, market, investment, vendor, transformation, cloud, AI and pre-sales decks.

| Mode | Typical core pages | Appendix | Evidence expectation |
|---|---:|---:|---|
| Executive brief | 6–10 | 3–8 | 2–4 evidence items per core page |
| Standard consulting | 10–18 | 4–10 | 3–5 evidence items per analytical page |
| Research-heavy consulting — default | 12–25 | 6–20 | 4–8 evidence items per analytical page, plus benchmark or comparison |

The page count is not a target by itself. Add pages when the available evidence requires separate analysis, and remove pages that do not contribute to the decision.

## Hard data-density gates

Data density means **verified and registered quantitative evidence**, not decorative numbers or fabricated precision.

For the body of each non-exempt page:

| Density mode | Minimum visible registered numeric facts | Normal target |
|---|---:|---:|
| Executive brief | 1 | 1–3 |
| Standard consulting | 2 | 2–4 |
| Research-heavy consulting | 3 | 3–5 or more when the exhibit requires it |

Rules:

1. Count unique facts or calculations already registered in `evidence.json`; repeated display of the same number does not increase the count.
2. The action title does not by itself satisfy the body-density gate. The body exhibit must carry the proof.
3. Covers, section dividers, navigation pages and explicitly requested conceptual-framework pages are exempt.
4. Explicit conceptual-framework pages should normally be no more than 25% of eligible pages. A project may set a limit between 20% and 30%, but must record the reason.
5. If a page cannot meet the floor, return it to Evidence Research, weaken or delete the claim, or mark it as an explicitly requested framework page with a documented rationale.
6. Do not create multiple evidence IDs for one fact merely to pass the gate.
7. Never fabricate or extrapolate unsupported numbers to increase density. Density pressure always strengthens Step 4 research; it never relaxes Evidence Discipline.

### Numeric and qualitative evidence records

`evidence.json` may contain both numeric and qualitative records. Numeric records have a finite numeric `value` and may participate in fact-consistency and data-density checks. Qualitative records may omit `value`, use a text `value`, or use `text_value`/`qualitative_value`; they remain registered and traceable but never count toward numeric-density thresholds. Malformed rows and invalid `used_on_pages` entries must not crash QA.

Run final density checks with:

```bash
python scripts/qa_pptx.py <deck.pptx> \
  --facts <private-draft-dir>/evidence.json \
  --briefs <private-draft-dir>/briefs.yaml
```

### Qualitative-claim rule

Strong qualitative wording in the body must be quantified or bounded. Terms such as `显著`, `大幅`, `明显`, `快速`, `领先`, `大量`, `significantly`, `substantially`, `rapidly` and `materially` should normally be accompanied in the same statement by a number, range, threshold or explicitly stated qualitative basis.

Examples:

- Weak: `自动化将显著降低成本。`
- Better: `自动化可将目标流程成本降低约 18%–24%。`
- Acceptable when numbers are unavailable: `访谈显示控制复杂度是首要障碍；由于缺乏可比成本数据，本页不量化影响。`

`qa_pptx.py` flags unsupported strong qualitative claims as warnings.

### Action-title quantification rule

If an analytical action title contains no number, range or threshold, Step 4 must create a `title_quantification` task to find a defensible quantitative anchor.

A non-numeric title is allowed only when:

1. the title describes a genuinely qualitative decision or design principle; or
2. three reasonable searches found no defensible number;
3. the failed search and rationale are recorded; and
4. the body still meets its evidence and comparison requirements.

Do not force a misleading number into a title merely to satisfy this preference.

## Core principle: no decorative concept pages

A page is not complete merely because it has an action title and a diagram. Concept-only pages are allowed only when the user explicitly asks for a conceptual framework or when the page is a navigation/section divider.

Every core page must contain:

1. One conclusion expressed as an action title.
2. One primary analytical exhibit that proves the conclusion.
3. At least 2 evidence IDs; analytical pages should normally contain 4–8.
4. At least one comparison, trend, benchmark, segmentation, decomposition or scenario.
5. Two to four insight annotations that explain why the exhibit matters.
6. A decision implication, recommendation or next action.
7. A caveat, assumption or boundary condition where material.
8. A source line with source names, dates and calculation basis.
9. A defined `quantification` statement and a concrete `benchmark` object or threshold.

A page with only icons, generic arrows, a five-box framework or unquantified maturity labels fails the content-density standard.

## Minimum analytical content by page type

### Market or industry page

Include, where available:

- historical market size for at least 3 periods;
- current market size and growth rate;
- forecast range and forecast horizon;
- segment, geography or customer breakdown;
- at least one independent benchmark or alternative estimate;
- explicit definitions explaining what is included and excluded.

Do not present a single CAGR or market-size number without the underlying time period, source definition and comparison.

### Company or financial page

Include, where relevant:

- at least 3–5 years of history or all available reporting periods;
- revenue, growth, margin, cash flow and capital intensity rather than revenue alone;
- segment or product decomposition;
- peer median or closest comparable companies;
- management guidance versus actual performance;
- capital allocation, dividend, buyback and balance-sheet implications;
- calculation basis for derived metrics.

A company page with only profile facts, logos or management quotes is insufficient.

### Investment or valuation page

Include:

- base, bull and bear cases;
- explicit operating assumptions;
- valuation method and formula;
- sensitivity to the two most important drivers;
- current valuation versus historical range and peers;
- catalysts, downside triggers and invalidation conditions;
- total shareholder return components where applicable.

### Technology, cloud, AI or vendor page

Include:

- current-state baseline and quantified pain points;
- target-state KPIs and service levels;
- product or architecture capability evidence;
- price, TCO or resource consumption where decision-relevant;
- independent benchmark, customer case or implementation evidence;
- limitations, lock-in, regulatory constraints and operational dependencies;
- design trade-offs, not only target-state boxes.

Architecture pages should normally show 3–5 design decisions, 2–4 quantified baselines or targets, key interfaces, control points and the implications of the chosen design.

### Option evaluation page

Include:

- options that are genuinely feasible;
- weighted criteria and rationale for weights;
- evidence behind each score;
- sensitivity if the recommendation changes under different weights;
- implementation consequences and switching costs;
- explicit reason for rejecting the second-best option.

### Business case page

Include:

- full assumption table;
- one-off and recurring costs;
- benefit categories and realization timing;
- base, upside and downside scenarios;
- payback, NPV or IRR where appropriate;
- sensitivity to the two largest assumptions;
- ownership for benefit realization;
- non-financial benefits stated separately from financial benefits.

### Roadmap page

Include:

- workstreams, owners and timing;
- deliverables and measurable exit criteria;
- dependencies and decision gates;
- resource or budget implications;
- target KPIs by wave;
- critical path and what can run in parallel;
- risks that could delay each wave;
- quantified scope for each wave, such as system count, user count, budget, workload or benefit milestone.

A roadmap with generic phases such as Discover, Design, Build and Run is insufficient unless each phase contains specific outputs and gates.

### Risk page

Include:

- probability and impact;
- evidence or trigger for the rating;
- leading indicator;
- mitigation action;
- accountable owner;
- residual risk after mitigation;
- time horizon and escalation threshold.

### Executive summary

The executive summary must be a synthesis of the analysis, not a table of contents. It should include 3–5 evidence-backed conclusions, each linked to the supporting pages and evidence IDs. At least one block should state the decision required, one should quantify expected impact, and one should state the primary risk or condition for success.

## Deck-level evidence budget

For a 10-page core deck, use the following default floor unless the topic has little available evidence:

- 25–50 registered facts or calculations in `evidence.json`;
- 8–15 distinct sources;
- at least 5 primary exhibits containing data, comparison or quantified analysis;
- at least 3 appendix pages with supporting tables, methodology, source definitions or sensitivities;
- at least one primary source for each major conclusion when a primary source exists;
- at least two independent source families for high-impact market, financial or regulatory conclusions.

Scale these floors proportionally for larger decks. Do not split one fact into multiple IDs merely to meet a count.

## Source depth and hierarchy

Prefer sources in this order:

1. Company filings, earnings materials, official product documentation, government and regulator publications.
2. International organizations, standards bodies and recognized industry associations.
3. Reputable data providers and research institutions.
4. Reuters, Financial Times, Bloomberg and other high-quality reporting.
5. Vendor blogs, specialist publications and secondary summaries, used with clear caveats.

For each major conclusion, capture both supporting evidence and limiting or contradictory evidence. A large source list is not a substitute for source quality.

## Page brief content budget

Every page brief should include these fields in addition to the standard key question and action title:

- `page_role`: core argument, supporting analysis, recommendation, decision or appendix;
- `evidence_ids`: IDs already registered in `evidence.json`;
- `required_data_points`: the specific numbers or facts that must appear;
- `quantification`: the principal baseline, target, gap, range or metric;
- `comparison_basis`: peer, period, scenario, segment or analytical comparison type;
- `benchmark`: the actual comparison entity, value, range or threshold and its source;
- `analysis_method`: trend, bridge, benchmark, decomposition, scoring, sensitivity, scenario or synthesis;
- `title_quantification`: quantitative title anchor, research task or justified non-numeric rationale;
- `insight_annotations`: two to four implications to call out on the exhibit;
- `decision_implication`: what the audience should decide or do;
- `appendix_link`: backup page containing methodology or detailed data;
- `content_density_target`: executive, standard or research-heavy;
- `unresolved_gaps`: missing evidence that must be researched, assumed or removed.

No page should enter production while `required_data_points`, `quantification`, `comparison_basis` or `benchmark` is empty, except covers, section dividers and explicitly requested conceptual pages.

## Appendix standard

The appendix is part of the analytical product, not a dumping ground. Use it for:

- source tables and definitions;
- detailed financial statements and calculations;
- full peer-comparison tables;
- methodology and scoring rationale;
- sensitivity and scenario outputs;
- technical architecture detail;
- implementation workplan and RACI;
- counter-evidence and rejected alternatives;
- data limitations and assumptions.

Every appendix page should be referenced from at least one core page or explicitly labeled as general backup.

## Density without clutter

Do not solve content gaps by shrinking fonts or pasting long paragraphs. Increase analytical density through:

- dense but readable summary tables;
- small multiples;
- chart-plus-data-table combinations;
- benchmark bars;
- variance bridges;
- annotated charts;
- side-by-side comparisons;
- quantified driver trees;
- scenario tables;
- insight rails;
- appendix links.

If a page cannot remain readable at the design-token font sizes, split the analysis across two pages rather than reducing the font below the approved minimum.

## Completion gate

Before page production, the main agent must confirm:

- every core page has a defined comparison or analytical method;
- every analytical page has a concrete quantification and benchmark;
- every major conclusion has enough evidence to survive challenge;
- the deck contains quantified impact, implementation detail and risk conditions;
- appendix coverage is planned rather than added at the end;
- no page exists solely because it is common in a consulting template;
- data-density pressure has not led to invented or weakly supported numbers.

A deck that is visually polished but fails these checks is incomplete.
