# Agent instructions

When generating or editing decks in this repository, follow `SKILL.md` first. Use PowerPoint/PPTX tooling only as the file-generation layer; consulting logic is controlled by this repository.

The default output standard is **research-heavy consulting**, not a sparse conceptual deck. Use `references/content-density.md` as a hard quality gate. Unless the user explicitly asks for a short executive brief, every core analytical page should contain enough data, comparison, calculation and implementation detail to withstand executive challenge.

Before starting generation, identify a private project-state root. Preferred: a separate private GitHub repository or enterprise-internal repository. Fallback: a local encrypted workspace. Do not store real client project state in this public skill repository.

Required order:

1. Select a deck archetype from `references/deck-archetypes.md` and set the content-density mode. Default to `research-heavy`.
2. Create `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/`.
3. Write the storyline as action titles and a coverage map. Do not parallelize storyline writing. Persist it to `storyline.md`.
4. Build an exhibit plan/page brief for each page using `references/exhibit-planning.md`. Persist it to `briefs.yaml`.
5. For every core page, define required data points, comparison basis, analysis method, evidence IDs, insight annotations, decision implication and appendix link before production.
6. Build and execute the Evidence Research list. For every key claim, run at least one support query and one counter-evidence query, then write back the number, unit, period, definition, source, retrieval date, calculation basis and caveat. Persist facts to `evidence.json` and assumptions to `assumptions.md`.
7. Confirm or automatically proceed with storyline, exhibit plan and evidence research findings. Unresolved research must be converted into a visible team assumption or removed. Freeze the baseline in `baseline/`.
8. Generate pages using `scripts/consulting_layouts.py` and `scripts/consulting_shapes.py`. Use `scripts/business_case.py` for ROI/TCO/payback pages and `scripts/architecture_helpers.py` for IT/AI/cloud architecture pages. Persist page modules in `pages/` and outputs in `output/`.
9. Run consulting QA and content-depth QA: vertical logic may be checked page by page, but horizontal logic, coverage, executive-summary synthesis and deck-wide numeric consistency must be checked serially by the main agent.
10. Run rendering QA with `python scripts/qa_pptx.py <deck.pptx> --facts <private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/evidence.json` before final delivery.

If a frozen baseline exists, follow `references/revision-loop.md` instead of regenerating the full deck.

Parallelization rules are defined in `references/orchestration.md`.

## Research-heavy page rules

- Core analytical pages require at least 2 evidence IDs and normally 4–8.
- Every analytical page needs a comparison, trend, benchmark, decomposition, bridge, scenario or other explicit analytical method.
- Include two to four insight annotations and a clear decision implication.
- A single metric, generic framework, icon row or unquantified diagram is not sufficient.
- Market pages need historical periods, current value, growth, segmentation and an alternative benchmark where available.
- Financial pages need 3–5 years or all available periods, segment drivers, peer comparison and cash-flow/capital-allocation implications.
- Architecture pages need quantified baselines or targets, 3–5 design decisions, trade-offs, interfaces, controls and dependencies.
- Roadmaps need owners, deliverables, measurable exit criteria, gates, dependencies, resource implications and target KPIs.
- Business cases need complete assumptions, costs, benefits, base/upside/downside scenarios and sensitivity.
- Risk pages need triggers, owners, mitigations and residual risk.
- Detailed methods, source tables, full peer sets and sensitivity outputs belong in linked appendix pages rather than being omitted.

For a typical 10-page core deck in research-heavy mode, target 25–50 non-duplicative registered facts or calculations, 8–15 relevant sources, at least 5 data-bearing analytical exhibits and at least 3 appendix pages. These are quality floors, not a reason to split facts artificially.

## Hard prohibitions

- Do not let multiple agents write to the same `.pptx` concurrently.
- Do not parallelize storyline writing.
- Do not fabricate data. Use sources or explicit assumptions. Label illustrative data clearly.
- Do not treat a source footer as proof that the page is analytically complete.
- Do not generate concept-only pages unless the user explicitly requests a conceptual framework or the page is a cover/section divider.
- Do not shrink text below the design-token minimum to force excessive content onto one page; split the page or use appendix.
- If subagents are unavailable, execute the same task lists serially; do not skip Evidence Research or QA.
- Do not store customer-identifiable information in this public skill repository.
- Do not keep process state only in local scratch files; persist it under the private state root.

## Page-module mode for parallel page generation

- Subagents may produce `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/pages/page_NN.py` modules only after storyline, page briefs and evidence findings are frozen.
- Each module must expose `def render(slide, ctx)`.
- Modules may only import existing repository helpers and may not create or save a `Presentation` object.
- The main agent assembles the final PPTX in a single process and in storyline order.
- Research subagents must return structured facts ready for `evidence.json`, not generic narrative summaries.