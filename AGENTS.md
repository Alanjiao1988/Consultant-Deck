# Agent instructions

When generating or editing decks in this repository, follow `SKILL.md` first. Use PowerPoint/PPTX tooling only as the file-generation layer; consulting logic is controlled by this repository.

Required order:

1. Select a deck archetype from `references/deck-archetypes.md`.
2. Write the storyline as action titles.
3. Build an exhibit plan/page brief for each page using `references/exhibit-planning.md`.
4. Generate pages using `scripts/consulting_layouts.py` and `scripts/consulting_shapes.py`.
5. Use `scripts/business_case.py` for ROI/TCO/payback pages.
6. Use `scripts/architecture_helpers.py` for IT/AI/cloud architecture pages.
7. Run `python scripts/qa_pptx.py <deck.pptx>` before final delivery.

Do not fabricate data. Use sources or explicit assumptions. Label illustrative data clearly.
