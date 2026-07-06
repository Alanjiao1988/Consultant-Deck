Follow `SKILL.md` for PowerPoint consulting deck generation. Preserve consulting discipline: action titles, storyline, exhibit plan, Evidence Research with support and counter-evidence searches, evidence discipline, private project-state persistence, fact-table QA, Chinese-English typography with Arial + Microsoft YaHei, and automated QA with `scripts/qa_pptx.py`.

Before generation, identify a private state root. Preferred: a separate private GitHub repository or enterprise-internal repository. Fallback: a local encrypted workspace. Do not store real client project state in this public skill repository.

Persist all intermediate artifacts under:

```text
<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/
```

Required artifacts: `storyline.md`, `briefs.yaml`, `evidence.json`, `assumptions.md`, `pages/`, `output/`, `baseline/`, and `changelog.md`.

Use the 8-step flow from `SKILL.md`:

1. Clarify demand and create the private draft directory.
2. Write storyline as action titles and persist `storyline.md`.
3. Build exhibit plan / page briefs and persist `briefs.yaml`.
4. Run Evidence Research, write findings back to briefs, and persist `evidence.json`.
5. Confirm or automatically proceed and freeze `baseline/`.
6. Generate pages and outputs.
7. Run consulting QA.
8. Run rendering QA with `python scripts/qa_pptx.py <deck.pptx> --facts <private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/evidence.json`.

If `baseline/` exists for the project, follow `references/revision-loop.md` instead of regenerating the full deck.

Use `scripts/consulting_layouts.py` for consistent page skeletons and `scripts/consulting_shapes.py` for editable PowerPoint-native charts and consulting exhibits. Use `scripts/business_case.py` for TCO/ROI/payback pages and `scripts/architecture_helpers.py` for cloud/AI/IT consulting pages.

Parallelization guidance is in `references/orchestration.md`. If subagents are unavailable, execute the same task list serially. Do not skip Evidence Research.

Hard prohibitions:

- Do not let multiple agents write to the same `.pptx` concurrently.
- Do not parallelize storyline writing.
- Do not generate page modules until storyline, page briefs and evidence findings are frozen.
- Do not introduce new colors, fonts or sizing outside the repository helpers and theme tokens.
- Do not store customer-identifiable information in this public skill repository.
- Do not keep intermediate process files only locally unless using a deliberately chosen local encrypted fallback.
