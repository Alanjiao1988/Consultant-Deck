# Agent instructions

When generating or editing decks in this repository, follow `SKILL.md` first. Use PowerPoint/PPTX tooling only as the file-generation layer; consulting logic is controlled by this repository.

Required order:

1. Select a deck archetype from `references/deck-archetypes.md`.
2. Write the storyline as action titles. Do not parallelize storyline writing.
3. Build an exhibit plan/page brief for each page using `references/exhibit-planning.md`.
4. Build and execute the Evidence Research list. For every key claim, run at least one support query and one counter-evidence query, then write back the number, unit, definition, source, retrieval date and caveat to the page brief.
5. Confirm or automatically proceed with storyline, exhibit plan and evidence research findings. Unresolved research must be converted into a visible team assumption or removed.
6. Generate pages using `scripts/consulting_layouts.py` and `scripts/consulting_shapes.py`. Use `scripts/business_case.py` for ROI/TCO/payback pages and `scripts/architecture_helpers.py` for IT/AI/cloud architecture pages.
7. Run consulting QA: vertical logic may be checked page by page, but horizontal logic and deck-wide numeric consistency must be checked serially by the main agent.
8. Run rendering QA with `python scripts/qa_pptx.py <deck.pptx>` before final delivery.

Parallelization rules are defined in `references/orchestration.md`.

Hard prohibitions:

- Do not let multiple agents write to the same `.pptx` concurrently.
- Do not parallelize storyline writing.
- Do not fabricate data. Use sources or explicit assumptions. Label illustrative data clearly.
- If subagents are unavailable, execute the same task lists serially; do not skip Evidence Research or QA.

Page-module mode for parallel page generation:

- Subagents may produce `pages/page_NN.py` modules only after storyline, page briefs and evidence findings are frozen.
- Each module must expose `def render(slide, ctx)`.
- Modules may only import existing repository helpers and may not create or save a `Presentation` object.
- The main agent assembles the final PPTX in a single process and in storyline order.
