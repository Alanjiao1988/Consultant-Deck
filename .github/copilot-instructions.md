Follow `SKILL.md` for PowerPoint consulting deck generation. Preserve consulting discipline: action titles, storyline, exhibit plan, Evidence Research with support and counter-evidence searches, research-heavy content density, private project-state persistence, fact-table QA, appendix depth, Chinese-English typography with Arial + Microsoft YaHei, and automated QA with `scripts/qa_pptx.py`.

The default is a **data-rich, research-heavy consulting deck**, not a sparse conceptual presentation. Read `references/content-density.md` before generation. Use executive-brief mode only when the user explicitly asks for a short or highly concise deck.

Before generation, identify a private state root. Preferred: a separate private GitHub repository or enterprise-internal repository. Fallback: a local encrypted workspace. Do not store real client project state in this public skill repository.

Persist all intermediate artifacts under:

```text
<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/
```

Required artifacts: `storyline.md`, `briefs.yaml`, `evidence.json`, `assumptions.md`, `pages/`, `output/`, `baseline/`, and `changelog.md`.

Use the 8-step flow from `SKILL.md`:

1. Clarify demand, set content-density mode and create the private draft directory.
2. Write storyline as action titles plus a coverage map and persist `storyline.md`.
3. Build exhibit plan / page briefs with required data points, comparison basis, analysis method, evidence IDs, insight annotations, decision implication and appendix link; persist `briefs.yaml`.
4. Run Evidence Research, including support and counter-evidence, write findings back to briefs, and persist `evidence.json`.
5. Confirm or automatically proceed only after content-completeness gates pass, then freeze `baseline/`.
6. Generate core pages and appendix pages.
7. Run consulting QA, content-depth QA and deck-density QA.
8. Run rendering QA with `python scripts/qa_pptx.py <deck.pptx> --facts <private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/evidence.json`.

If `baseline/` exists for the project, follow `references/revision-loop.md` instead of regenerating the full deck.

Use `scripts/consulting_layouts.py` for consistent page skeletons and `scripts/consulting_shapes.py` for editable PowerPoint-native charts and consulting exhibits. Use `scripts/business_case.py` for TCO/ROI/payback pages and `scripts/architecture_helpers.py` for cloud/AI/IT consulting pages.

## Required content depth

- Core analytical pages require at least 2 evidence IDs and normally 4–8 in research-heavy mode.
- Every analytical page needs a comparison, trend, benchmark, decomposition, bridge, scenario, sensitivity or other explicit method.
- Each page needs two to four insight annotations and a decision implication.
- A source footer does not make a sparse page complete.
- Avoid generic five-box frameworks, icon rows, unquantified maturity models and architecture diagrams without baselines, targets, trade-offs or dependencies.
- Use appendix pages for full tables, formulas, source definitions, sensitivities, architecture details and rejected alternatives.
- Do not shrink fonts below repository tokens to fit more text; split the page.

For a typical 10-page core deck, target 25–50 non-duplicative facts/calculations, 8–15 relevant sources, at least 5 data-bearing exhibits and at least 3 appendix pages, unless the topic genuinely lacks evidence.

Parallelization guidance is in `references/orchestration.md`. If subagents are unavailable, execute the same task list serially. Do not skip Evidence Research. Research subagents must return structured facts suitable for `evidence.json`, not general prose.

Hard prohibitions:

- Do not let multiple agents write to the same `.pptx` concurrently.
- Do not parallelize storyline writing.
- Do not generate page modules until storyline, page briefs and evidence findings are frozen.
- Do not generate concept-only pages unless explicitly requested or used as cover/section divider.
- Do not introduce new colors, fonts or sizing outside the repository helpers and theme tokens.
- Do not store customer-identifiable information in this public skill repository.
- Do not keep intermediate process files only locally unless using a deliberately chosen local encrypted fallback.