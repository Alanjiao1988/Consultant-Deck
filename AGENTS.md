# Agent instructions

When generating or editing decks in this repository, follow `SKILL.md` first. Use PowerPoint/PPTX tooling only as the file-generation layer; consulting logic is controlled by this repository.

The default output standard is **research-heavy consulting**, not a sparse conceptual deck. Use `references/content-density.md` as a hard quality gate. Unless the user explicitly asks for a short executive brief, every core analytical page should contain enough registered data, comparison, calculation and implementation detail to withstand executive challenge.

Before starting generation, identify a private project-state root. Preferred: a separate private GitHub repository or enterprise-internal repository. Fallback: a local encrypted workspace. Do not store real client project state in this public skill repository.

## Required order

1. Select a deck archetype from `references/deck-archetypes.md` and set the content-density mode. Default to `research-heavy`.
2. Create `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/`.
3. Write the storyline as action titles and a coverage map. Do not parallelize storyline writing. Persist it to `storyline.md`.
4. Build an exhibit plan/page brief for each page using `references/exhibit-planning.md`. Persist it to `briefs.yaml`.
5. For every non-exempt analytical page, define `required_data_points`, `quantification`, `comparison_basis`, `benchmark`, `analysis_method`, `evidence_ids`, `insight_annotations`, `decision_implication` and `appendix_link`.
6. If an analytical action title has no number, range or threshold, create `title_quantification`. After three reasonable searches, a justified non-numeric title is allowed only with the failed-search rationale recorded.
7. Build and execute the Evidence Research list. For each quantitative task, normally return a core metric, at least 2–3 comparable time points and one to two comparable entities/scenarios, plus support and counter-evidence.
8. Persist values, units, periods, entities, definitions, sources, retrieval dates, formulas, input fact IDs, caveats and confidence to `evidence.json`; persist search decisions to `research-log.md` and assumptions to `assumptions.md`.
9. Run `scripts/qa_briefs.py` and resolve errors before freezing `baseline/`.
10. Generate pages using `scripts/consulting_layouts.py` and `scripts/consulting_shapes.py`. Use `scripts/business_case.py` for ROI/TCO/payback pages and `scripts/architecture_helpers.py` for IT/AI/cloud architecture pages.
11. Run consulting, quantification and content-depth QA. Vertical review may be parallel; horizontal logic, coverage, executive-summary synthesis and deck-wide numeric consistency remain serial.
12. Run final PPTX QA with both facts and briefs before delivery.

```bash
python scripts/qa_briefs.py <private-draft-dir>/briefs.yaml \
  --facts <private-draft-dir>/evidence.json \
  --json

python scripts/qa_pptx.py <deck.pptx> \
  --facts <private-draft-dir>/evidence.json \
  --briefs <private-draft-dir>/briefs.yaml \
  --json
```

If a frozen baseline exists, follow `references/revision-loop.md` instead of regenerating the full deck.

Parallelization rules are defined in `references/orchestration.md`.

## Research-heavy page rules

- Research-heavy analytical page bodies normally expose at least 3 unique numeric facts registered in `evidence.json`; standard pages normally expose at least 2.
- The title alone does not satisfy body density.
- Core analytical pages require at least 2 evidence IDs and normally 4–8.
- Every analytical page needs a central quantification and a concrete benchmark, not only a generic comparison label.
- Include two to four insight annotations and a clear decision implication.
- Strong qualitative language such as `显著提升`, `大幅降低`, `rapidly growing` or `materially better` requires a number, range, threshold or visible evidence basis.
- Explicitly requested conceptual-framework pages may be exempt from numeric floors, but should normally remain below 25% of eligible pages.
- Market pages need historical periods, current value, growth, segmentation and an alternative benchmark where available.
- Financial pages need 3–5 years or all available periods, segment drivers, peer comparison and cash-flow/capital-allocation implications.
- Architecture pages need quantified baselines or targets, 3–5 design decisions, trade-offs, interfaces, controls and dependencies.
- Roadmaps need owners, deliverables, measurable exit criteria, gates, dependencies, resource implications, target KPIs and quantified scope by wave.
- Business cases need complete assumptions, costs, benefits, base/upside/downside scenarios and sensitivity.
- Risk pages need triggers, owners, mitigations and residual risk.
- Detailed methods, source tables, full peer sets and sensitivity outputs belong in linked appendix pages rather than being omitted.

For a typical 10-page core deck in research-heavy mode, target 25–50 non-duplicative registered facts or calculations, 8–15 relevant sources, at least 5 data-bearing analytical exhibits and at least 3 appendix pages. These are quality floors, not a reason to split facts artificially.

## Preferred data-exhibit helpers

Use editable PowerPoint-native helpers where suitable:

- `dense_table()` for detailed business data;
- `benchmark_bar()` for peer and threshold comparisons;
- `driver_tree()` for quantified value/TCO decomposition;
- `native_chart()` with `bar_h`, `area_stacked` and `combo` support;
- `cagr_annotation()` for calculated trend labels;
- `chart_with_data_table()` for visual trend plus exact values.

Do not default to a 2x2, architecture boxes or icon rows when the page question is quantitative.

## Hard prohibitions

- Do not let multiple agents write to the same `.pptx` concurrently.
- Do not parallelize storyline writing.
- Do not fabricate data, unsupported estimates or false precision to satisfy density gates.
- Do not create duplicate evidence IDs for one fact merely to increase counts.
- Do not treat a source footer as proof that the page is analytically complete.
- Do not accept an isolated number when comparable periods or entities are reasonably available.
- Do not generate concept-only pages unless the user explicitly requests a framework or the page is a cover/section divider.
- Do not shrink text below the design-token minimum to force excessive content onto one page; split the page or use appendix.
- If subagents are unavailable, execute the same task lists serially; do not skip Evidence Research or QA.
- Do not store customer-identifiable information in this public skill repository.
- Do not keep process state only in local scratch files; persist it under the private state root.

## Page-module mode for parallel page generation

- Subagents may produce `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/pages/page_NN.py` only after storyline, page briefs and evidence findings are frozen.
- Each module must expose `def render(slide, ctx)`.
- Modules may only import existing repository helpers and may not create or save a `Presentation` object.
- Page modules must render the frozen evidence IDs, quantification, benchmark, insight annotations, implication and appendix link.
- The main agent assembles the final PPTX in a single process and in storyline order.
- Research subagents must return structured facts ready for `evidence.json`, not generic narrative summaries.
