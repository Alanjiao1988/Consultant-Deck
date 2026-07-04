# Agent instructions

When generating or editing decks in this repository, follow `SKILL.md` first. Use PowerPoint/PPTX tooling only as the file-generation layer; consulting logic is controlled by this repository.

Before starting generation, create a GitHub repo draft directory under `Deck draft/<YYYY-MM-DD>/<deck-title-slug>/`. Intermediate artifacts must be written there; do not keep storyline, briefs, evidence, assumptions or page modules only in local scratch files or conversation history.

Required order:

1. Select a deck archetype from `references/deck-archetypes.md`.
2. Write the storyline as action titles. Do not parallelize storyline writing. Persist it to `storyline.md`.
3. Build an exhibit plan/page brief for each page using `references/exhibit-planning.md`. Persist it to `briefs.yaml`.
4. Build and execute the Evidence Research list. For every key claim, run at least one support query and one counter-evidence query, then write back the number, unit, definition, source, retrieval date and caveat to the page brief. Persist facts to `evidence.json` and assumptions to `assumptions.md`.
5. Confirm or automatically proceed with storyline, exhibit plan and evidence research findings. Unresolved research must be converted into a visible team assumption or removed. Freeze the baseline in `baseline/`.
6. Generate pages using `scripts/consulting_layouts.py` and `scripts/consulting_shapes.py`. Use `scripts/business_case.py` for ROI/TCO/payback pages and `scripts/architecture_helpers.py` for IT/AI/cloud architecture pages. Persist page modules in `pages/` and outputs in `output/`.
7. Run consulting QA: vertical logic may be checked page by page, but horizontal logic and deck-wide numeric consistency must be checked serially by the main agent.
8. Run rendering QA with `python scripts/qa_pptx.py <deck.pptx> --facts <draft-dir>/evidence.json` before final delivery.

If a frozen baseline exists, follow `references/revision-loop.md` instead of regenerating the full deck.

Parallelization rules are defined in `references/orchestration.md`.

Hard prohibitions:

- Do not let multiple agents write to the same `.pptx` concurrently.
- Do not parallelize storyline writing.
- Do not fabricate data. Use sources or explicit assumptions. Label illustrative data clearly.
- If subagents are unavailable, execute the same task lists serially; do not skip Evidence Research or QA.
- Do not keep process state only in local scratch files; persist it under `Deck draft/` in the repository.

Page-module mode for parallel page generation:

- Subagents may produce `Deck draft/<YYYY-MM-DD>/<deck-title-slug>/pages/page_NN.py` modules only after storyline, page briefs and evidence findings are frozen.
- Each module must expose `def render(slide, ctx)`.
- Modules may only import existing repository helpers and may not create or save a `Presentation` object.
- The main agent assembles the final PPTX in a single process and in storyline order.
