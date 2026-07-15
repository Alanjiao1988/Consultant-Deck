# Research-heavy content density standard

This reference defines the minimum analytical depth for a consulting deck. The objective is not to fill slides with text. The objective is to make every core page decision-useful, evidence-backed and sufficiently detailed that an executive can challenge the logic without asking for a separate research memo.

## Default output mode

Unless the user explicitly requests a short executive brief, use **research-heavy consulting mode** for strategy, market, investment, vendor, transformation, cloud, AI and pre-sales decks.

| Mode | Typical core pages | Appendix | Evidence expectation |
|---|---:|---:|---|
| Executive brief | 6–10 | 3–8 | 2–4 evidence items per core page |
| Standard consulting | 10–18 | 4–10 | 3–5 evidence items per analytical page |
| Research-heavy consulting — default | 12–25 | 6–20 | 4–8 evidence items per analytical page, plus benchmark or comparison |
| Qualitative exhibit | Used only for evidence-backed classification exhibits | Required detailed backup | Coverage, as-of date, classification evidence, sidecar manifest and appendix universe |

The page count is not a target by itself. Add pages when evidence requires separate analysis, and remove pages that do not contribute to the decision.

## Hard data-density gates

Data density means **verified and registered quantitative evidence**, not decorative numbers or fabricated precision.

For the body of each ordinary non-exempt page:

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
5. If an ordinary analytical page cannot meet the floor, return it to Evidence Research, weaken or delete the claim, or split the page.
6. Do not create multiple evidence IDs for one fact merely to pass the gate.
7. Never fabricate or extrapolate unsupported numbers to increase density. Density pressure strengthens research; it never relaxes Evidence Discipline.

### Qualitative-exhibit alternative contract

Some pages prove a decision through a structured, evidence-backed qualitative classification rather than numeric magnitude. The canonical example is `categorical_jurisdiction_map`. These pages are not conceptual-framework exemptions and must not silently inherit the research-heavy three-number floor.

A qualifying page brief must explicitly contain:

```yaml
content_density_target: qualitative-exhibit
min_registered_numbers: 0
exhibit_manifest: output/<deck-name>.exhibits.json
appendix_link: A6
as_of: 2026-07-14
coverage:
  reviewed: 24
  shown: 6
  selection_basis: Representative operating patterns
```

The explicit `min_registered_numbers: 0` uses the existing page-specific override in `qa_pptx.py`. It is mandatory; merely naming the density mode is not enough. This keeps the final-file QA deterministic and avoids special-casing one visual type inside the generic numeric scanner.

The zero threshold is permitted only when all of the following are true:

1. The primary exhibit is a structured qualitative classification with a named and consistent dimension.
2. Every classified entity is backed by one or more registered qualitative evidence IDs.
3. The page displays and registers `coverage.reviewed` and `coverage.shown` where those counts are available.
4. The page states an ISO as-of date and a non-empty selection basis.
5. The page includes two to four evidence-based observations, a decision implication and a visible caveat.
6. A semantic exhibit manifest is written and passes `qa_exhibits.py`.
7. A linked appendix table lists the full reviewed universe, definitions, category assignment, sources, retrieval dates and limitations.
8. The conclusion is about pattern, operating model or classification—not numeric magnitude.

This is a **substitute evidence contract**, not an evidence waiver. Dates, jurisdiction IDs, duplicated coverage counts or arbitrary scores must not be introduced merely to reach three numbers. If the conclusion is fundamentally quantitative, use a benchmark bar, table, small multiple or other numeric exhibit instead.

The deck-level evidence budget still applies. Qualitative-exhibit pages contribute registered qualitative facts and sources, but they do not reduce the evidence expected on unrelated research-heavy pages.

### Numeric and qualitative evidence records

`evidence.json` may contain both numeric and qualitative records. Numeric records have a finite numeric `value` and may participate in fact-consistency and data-density checks. Qualitative records may omit `value`, use a text `value`, or use `text_value`/`qualitative_value`; they remain registered and traceable but never count toward numeric-density thresholds. Malformed rows and invalid `used_on_pages` entries must not crash QA.

Run final density checks with:

```bash
python scripts/qa_pptx.py <deck.pptx> \
  --facts <private-draft-dir>/evidence.json \
  --briefs <private-draft-dir>/briefs.yaml
```

For data-driven qualitative exhibits, run semantic QA first:

```bash
python scripts/qa_exhibits.py <private-draft-dir>/output/<deck-name>.exhibits.json \
  --facts <private-draft-dir>/evidence.json \
  --fail-on-warning
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
4. the body still meets its ordinary or qualitative-exhibit evidence contract.

Do not force a misleading number into a title merely to satisfy this preference.

## Core principle: no decorative concept pages

A page is not complete merely because it has an action title and a diagram. Concept-only pages are allowed only when the user explicitly asks for a conceptual framework or when the page is navigation/section divider.

Every core page must contain:

1. One conclusion expressed as an action title.
2. One primary analytical exhibit that proves the conclusion.
3. At least 2 evidence IDs; analytical pages should normally contain 4–8.
4. At least one comparison, trend, benchmark, segmentation, decomposition, scenario or defined qualitative classification universe.
5. Two to four insight annotations that explain why the exhibit matters.
6. A decision implication, recommendation or next action.
7. A caveat, assumption or boundary condition where material.
8. A source line with source names, dates and calculation basis.
9. A defined `quantification` and benchmark, or an approved qualitative-exhibit contract.

A page with only icons, generic arrows, a five-box framework or unquantified maturity labels fails the standard.

## Minimum analytical content by page type

### Market or industry page

Include, where available:

- historical market size for at least 3 periods;
- current market size and growth rate;
- forecast range and horizon;
- segment, geography or customer breakdown;
- at least one independent benchmark or alternative estimate;
- explicit definitions explaining included and excluded scope.

Do not present a single CAGR or market-size number without the underlying period, source definition and comparison.

### Company or financial page

Include, where relevant:

- at least 3–5 years of history or all available periods;
- revenue, growth, margin, cash flow and capital intensity rather than revenue alone;
- segment or product decomposition;
- peer median or closest comparable companies;
- guidance versus actual performance;
- capital allocation implications;
- calculation basis for derived metrics.

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

Architecture pages should normally show 3–5 design decisions, 2–4 quantified baselines or targets, key interfaces, control points and implications.

### Qualitative jurisdiction or regulatory classification page

Include:

- a named classification dimension and whether categories are mutually exclusive;
- reviewed and shown coverage counts plus selection basis;
- a current as-of date;
- evidence-backed notes for every displayed jurisdiction;
- a complete legend with no unused categories;
- two to four implications and one decision statement;
- a visible legal/comparability caveat;
- a sidecar manifest;
- an appendix table covering the full reviewed universe.

Do not use this page type when categories overlap materially or when the intended conclusion is a numeric ranking.

### Option evaluation page

Include feasible options, weighted criteria, evidence behind scores, sensitivity, implementation consequences and the reason for rejecting the second-best option.

### Business case page

Include a full assumption table, one-off and recurring costs, benefit categories and timing, base/upside/downside scenarios, payback/NPV/IRR where appropriate, sensitivity and benefit ownership.

### Roadmap page

Include workstreams, owners, timing, deliverables, measurable exit criteria, dependencies, decision gates, resources, target KPIs, critical path and quantified scope by wave.

### Risk page

Include probability, impact, evidence/trigger, leading indicator, mitigation, owner, residual risk, time horizon and escalation threshold.

### Executive summary

Synthesize 3–5 evidence-backed conclusions linked to supporting pages and evidence IDs. At least one block states the decision, one quantifies expected impact, and one states the primary risk or success condition.

## Deck-level evidence budget

For a 10-page core deck, use the following default floor unless the topic has little available evidence:

- 25–50 registered facts or calculations, including material qualitative assertions;
- 8–15 distinct sources;
- at least 5 primary exhibits containing data, comparison or auditable classification;
- at least 3 appendix pages with supporting tables, methodology, source definitions or sensitivities;
- at least one primary source for each major conclusion when one exists;
- at least two independent source families for high-impact market, financial or regulatory conclusions.

Scale these floors proportionally. Do not split one fact into multiple IDs merely to meet a count.

## Source depth and hierarchy

Prefer sources in this order:

1. Company filings, earnings materials, official product documentation, government and regulator publications.
2. International organizations, standards bodies and recognized industry associations.
3. Reputable data providers and research institutions.
4. Reuters, Financial Times, Bloomberg and other high-quality reporting.
5. Vendor blogs, specialist publications and secondary summaries, used with caveats.

For each major conclusion, capture supporting and limiting or contradictory evidence. A large source list is not a substitute for source quality.

## Page brief content budget

Every page brief should include:

- `page_role`;
- `evidence_ids`;
- `required_data_points`;
- `quantification` or approved qualitative coverage contract;
- `comparison_basis`;
- `benchmark` or reviewed universe;
- `analysis_method`;
- `title_quantification`;
- `insight_annotations`;
- `decision_implication`;
- `appendix_link`;
- `content_density_target`;
- `min_registered_numbers` when using a page-specific override;
- `exhibit_manifest` for data-driven semantic exhibits;
- `unresolved_gaps`.

No page should enter production while its required evidence contract is incomplete, except covers, section dividers and explicitly requested conceptual pages.

## Appendix standard

Use the appendix for source tables and definitions, detailed statements and calculations, full peer or jurisdiction tables, methodology, sensitivities, technical detail, workplans, counter-evidence and assumptions. Every appendix page should be referenced from a core page or explicitly labeled general backup.

## Density without clutter

Do not solve content gaps by shrinking fonts or pasting long paragraphs. Increase analytical density through readable tables, small multiples, chart-plus-table combinations, benchmark bars, bridges, annotated charts, side-by-side comparisons, driver trees, scenario tables, audited maps, insight rails and appendix links.

If a page cannot remain readable at approved font sizes, split it rather than reducing the font below the design minimum.

## Completion gate

Before production, the main agent must confirm:

- every core page has a defined comparison or analytical method;
- every analytical page has a concrete quantification/benchmark or approved qualitative-exhibit contract;
- every major conclusion has enough evidence to survive challenge;
- data-driven exhibits have planned manifest outputs and semantic QA;
- the deck contains quantified impact, implementation detail and risk conditions;
- appendix coverage is planned;
- no page exists solely because it is common in a consulting template;
- density pressure has not led to invented or weakly supported numbers.

A visually polished deck that fails these checks is incomplete.
