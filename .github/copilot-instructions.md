Follow `SKILL.md` for PowerPoint consulting deck generation. Preserve consulting discipline: action titles, storyline, exhibit plan, Evidence Research with support and counter-evidence searches, evidence discipline, Chinese-English typography with Arial + Microsoft YaHei, and automated QA with `scripts/qa_pptx.py`.

Use the 8-step flow from `SKILL.md`:

1. Clarify demand.
2. Write storyline as action titles.
3. Build exhibit plan / page briefs.
4. Run Evidence Research and write findings back to briefs.
5. Confirm or automatically proceed.
6. Generate pages.
7. Run consulting QA.
8. Run rendering QA.

Use `scripts/consulting_layouts.py` for consistent page skeletons and `scripts/consulting_shapes.py` for editable PowerPoint-native charts and consulting exhibits. Use `scripts/business_case.py` for TCO/ROI/payback pages and `scripts/architecture_helpers.py` for cloud/AI/IT consulting pages.

Parallelization guidance is in `references/orchestration.md`. If subagents are unavailable, execute the same task list serially. Do not skip Evidence Research.

Hard prohibitions:

- Do not let multiple agents write to the same `.pptx` concurrently.
- Do not parallelize storyline writing.
- Do not generate page modules until storyline, page briefs and evidence findings are frozen.
- Do not introduce new colors, fonts or sizing outside the repository helpers and theme tokens.
