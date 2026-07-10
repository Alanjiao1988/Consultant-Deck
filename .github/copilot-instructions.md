Follow `SKILL.md` for PowerPoint consulting deck generation. Preserve consulting discipline: action titles, storyline, quantified exhibit plan, Evidence Research with support and counter-evidence, hard data-density gates, private project-state persistence, fact-table QA, appendix depth, Chinese-English typography with Arial + Microsoft YaHei, and automated QA with both `scripts/qa_briefs.py` and `scripts/qa_pptx.py`.

The default is a **data-rich, research-heavy consulting deck**, not a sparse conceptual presentation. Read `references/content-density.md` before generation. Use executive-brief mode only when the user explicitly asks for a short or highly concise deck.

Before generation, identify a private state root. Preferred: a separate private GitHub repository or enterprise-internal repository. Fallback: a local encrypted workspace. Do not store real client project state in this public skill repository.

Persist all intermediate artifacts under:

```text
<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/
```

Required artifacts: `storyline.md`, `briefs.yaml`, `evidence.json`, `research-log.md`, `assumptions.md`, `pages/`, `output/`, `baseline/`, and `changelog.md`.

Use the 8-step flow from `SKILL.md`:

1. Clarify demand, set content-density mode and create the private draft directory.
2. Write storyline as action titles plus a coverage map and persist `storyline.md`.
3. Build page briefs with required data points, quantification, concrete benchmark, comparison basis, analysis method, evidence IDs, insight annotations, decision implication and appendix link; persist `briefs.yaml`.
4. If an analytical title lacks a number/range/threshold, create a `title_quantification` task. Keep a non-numeric title only after reasonable searches and a documented rationale.
5. Run Evidence Research. Quantitative tasks should normally return a core metric, 2–3 comparable time points, one to two comparable entities/scenarios, support evidence and counter-evidence. Persist findings to `evidence.json` and search decisions to `research-log.md`.
6. Run `qa_briefs.py`, resolve errors and normally fix research-heavy warnings before freezing `baseline/`.
7. Generate core and appendix pages, then run consulting, quantification and content-depth QA.
8. Run final PPTX QA with both facts and briefs.

```bash
python scripts/qa_briefs.py <private-draft-dir>/briefs.yaml \
  --facts <private-draft-dir>/evidence.json \
  --json

python scripts/qa_pptx.py <deck.pptx> \
  --facts <private-draft-dir>/evidence.json \
  --briefs <private-draft-dir>/briefs.yaml \
  --json
```

If `baseline/` exists, follow `references/revision-loop.md` instead of regenerating the full deck.

Use `scripts/consulting_layouts.py` for page skeletons and `scripts/consulting_shapes.py` for editable PowerPoint-native exhibits. Prefer `dense_table`, `benchmark_bar`, `driver_tree`, `native_chart` with `bar_h`/`area_stacked`/`combo`, `cagr_annotation` and `chart_with_data_table` for quantitative pages. Use `scripts/business_case.py` for TCO/ROI/payback pages and `scripts/architecture_helpers.py` for cloud/AI/IT architecture pages.

## Required content depth

- Research-heavy analytical page bodies normally expose at least 3 unique numeric facts registered in `evidence.json`; standard pages normally expose at least 2.
- The title alone does not satisfy body density.
- Core analytical pages require at least 2 evidence IDs and normally 4–8 in research-heavy mode.
- Every analytical page needs a central quantification and a concrete peer, historical, scenario, threshold or target benchmark.
- Each page needs two to four insight annotations and a decision implication.
- Strong qualitative claims such as `显著提升`, `大幅降低`, `rapidly growing` or `materially better` need a number, range, threshold or explicit evidence basis.
- Explicit conceptual-framework pages may be exempt, but should normally remain below 25% of eligible pages.
- Avoid generic five-box frameworks, icon rows, unquantified maturity models and architecture diagrams without baselines, targets, trade-offs or dependencies.
- Roadmaps require quantified scope, budget or KPI gates by wave.
- Use appendix pages for full tables, formulas, source definitions, sensitivities, architecture details and rejected alternatives.
- Do not shrink fonts below repository tokens; split the page.

For a typical 10-page core deck, target 25–50 non-duplicative facts/calculations, 8–15 relevant sources, at least 5 data-bearing exhibits and at least 3 appendix pages, unless the topic genuinely lacks evidence.

Parallelization guidance is in `references/orchestration.md`. If subagents are unavailable, execute the same task list serially. Research subagents must return structured facts suitable for `evidence.json`, not general prose or isolated numbers when time series/comparables are reasonably available.

Hard prohibitions:

- Do not let multiple agents write to the same `.pptx` concurrently.
- Do not parallelize storyline writing.
- Do not generate page modules until storyline, page briefs and evidence findings are frozen.
- Do not fabricate data, false precision or duplicate facts to satisfy density gates.
- Do not generate concept-only pages unless explicitly requested or used as cover/section divider.
- Do not introduce new colors, fonts or sizing outside repository helpers and theme tokens.
- Do not store customer-identifiable information in this public skill repository.
- Do not keep intermediate process files only locally unless using a deliberately chosen encrypted fallback.
