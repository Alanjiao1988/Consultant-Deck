Follow `SKILL.md` for PowerPoint consulting deck generation. Preserve consulting discipline: action titles, storyline, exhibit plan, Evidence Research with support and counter-evidence searches, evidence discipline, repo-backed Deck draft state, fact-table QA, Chinese-English typography with Arial + Microsoft YaHei, and automated QA with `scripts/qa_pptx.py`.

Before generation, create a repository draft directory under `Deck draft/<YYYY-MM-DD>/<deck-title-slug>/`. Persist all intermediate artifacts there: `storyline.md`, `briefs.yaml`, `evidence.json`, `assumptions.md`, `pages/`, `output/`, `baseline/`, and `changelog.md`. Do not keep process state only in local scratch files or chat context.

Use the 8-step flow from `SKILL.md`:

1. Clarify demand and create the draft directory.
2. Write storyline as action titles and persist `storyline.md`.
3. Build exhibit plan / page briefs and persist `briefs.yaml`.
4. Run Evidence Research, write findings back to briefs, and persist `evidence.json`.
5. Confirm or automatically proceed and freeze `baseline/`.
6. Generate pages and outputs.
7. Run consulting QA.
8. Run rendering QA with `python scripts/qa_pptx.py <deck.pptx> --facts <draft-dir>/evidence.json`.

If `baseline/` exists for the project, follow `references/revision-loop.md` instead of regenerating the full deck.

Use `scripts/consulting_layouts.py` for consistent page skeletons and `scripts/consulting_shapes.py` for editable PowerPoint-native charts and consulting exhibits. Use `scripts/business_case.py` for TCO/ROI/payback pages and `scripts/architecture_helpers.py` for cloud/AI/IT consulting pages.

Parallelization guidance is in `references/orchestration.md`. If subagents are unavailable, execute the same task list serially. Do not skip Evidence Research.

Hard prohibitions:

- Do not let multiple agents write to the same `.pptx` concurrently.
- Do not parallelize storyline writing.
- Do not generate page modules until storyline, page briefs and evidence findings are frozen.
- Do not introduce new colors, fonts or sizing outside the repository helpers and theme tokens.
- Do not keep intermediate process files only locally; use the repo `Deck draft/` path.
