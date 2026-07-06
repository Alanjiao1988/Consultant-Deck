# Consultant Deck Skill

A consulting-style PowerPoint skill for generating executive-ready decks with storyline discipline, action titles, exhibit planning, mandatory evidence research, support and counter-evidence checks, private project-state persistence, fact-table QA, subagent orchestration rules, revision loop, Chinese-English typography rules, and reusable PowerPoint-native layout/chart helpers.

## What was fixed

This version addresses the earlier review gaps:

1. Added a full consulting delivery workflow: storyline → exhibit plan → evidence research → page production → consulting QA → rendering QA.
2. Added mandatory Evidence Research before confirmation or automatic execution. Every key claim requires support and counter-evidence searches.
3. Added private project-state persistence under `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/`; real client state must not be stored in this public skill repo.
4. Added `evidence.json` as a fact table and `qa_pptx.py --facts` for numeric consistency checks.
5. Added reusable deck archetypes for strategy, IT/cloud transformation, sales proposal, investment analysis, vendor evaluation, executive decision meetings and workshops.
6. Added stronger evidence discipline and QA checks so the skill does not invent data.
7. Added IT consulting patterns for cloud migration, AI transformation, application modernization, data platform, security, business case and adoption.
8. Added orchestration rules for subagent parallelism, page-module assembly, failure degradation and serial fallback.
9. Added revision-loop rules for frozen-baseline changes.
10. Added CI to run template generation, demo generation, `--facts` QA and pytest.
11. Added `AGENTS.md` and `.github/copilot-instructions.md` so GitHub Copilot/Codex-style agents can use the repo directly.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

python scripts/create_template.py
python scripts/demo_generate_deck.py
python scripts/qa_pptx.py examples/demo_ai_transformation.pptx --facts examples/demo_ai_transformation.evidence.json
pytest tests/ -q
```

## Required workflow

```text
Step 1 需求澄清 → Step 2 Storyline → Step 3 Exhibit Plan → Step 4 Evidence Research → Step 5 确认/自动执行 → Step 6 逐页生成 → Step 7 咨询 QA → Step 8 渲染 QA
```

Evidence Research must create a research task list from all page briefs. Each key claim needs one support query and one counter-evidence query, with findings written back as number, unit, definition, source, retrieval date and caveat.

## Private state layer

Real project process artifacts must be stored outside this public skill repo. Preferred target:

```text
<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/
```

The private draft directory should contain `storyline.md`, `briefs.yaml`, `evidence.json`, `assumptions.md`, `pages/`, `output/`, `baseline/`, and `changelog.md`. See `references/project-state.md`.

If `baseline/` exists for a project, follow `references/revision-loop.md` instead of regenerating the full deck.

Security rule: customer names, internal numbers, project code names, non-public architecture details, source documents, draft storylines, `briefs.yaml`, `evidence.json` and assumptions must never be written to public storage.

## Parallel execution rules

See `references/orchestration.md`.

Hard prohibitions:

- Do not let multiple agents write to the same `.pptx` concurrently.
- Do not parallelize storyline writing.
- Do not skip Evidence Research in environments without subagents; execute the same task list serially.
- Do not store real client project state in this public skill repo.
- Do not put NDA information in public search queries, commit messages, branch names or file paths.

## Repository layout

```text
SKILL.md
AGENTS.md
.github/
  copilot-instructions.md
  workflows/ci.yml
references/
  deck-archetypes.md
  exhibit-planning.md
  project-state.md
  revision-loop.md
  orchestration.md
  it-consulting-patterns.md
  page-patterns.md
  qa-checklist.md
  terminology.md
assets/
  theme.json
scripts/
  consulting_layouts.py
  consulting_shapes.py
  business_case.py
  architecture_helpers.py
  create_template.py
  demo_generate_deck.py
  qa_pptx.py
tests/
  test_shapes.py
```

## Validation command

```bash
python scripts/create_template.py
python scripts/demo_generate_deck.py
python scripts/qa_pptx.py examples/demo_ai_transformation.pptx --facts examples/demo_ai_transformation.evidence.json --json
pytest tests/ -q
```

## Behavioral validation

1. Demo with `--facts` should return zero QA findings.
2. If a demo slide number is manually changed to conflict with `evidence.json`, `qa_pptx.py --facts` should report a `fact_consistency` error.
3. A mixed-language cover such as `某银行数字化转型 strategy` should produce a terminology warning.
4. If a user asks to modify page 3 after a frozen baseline exists, the agent should enter revision mode: diff the baseline, list impacted pages, update only affected artifacts, rerun scoped QA, and write a versioned changelog entry.
5. Publicly accessible paths must contain no real project state files.

Generated binary PPTX files are intentionally not stored in the repository by default. Run `scripts/create_template.py` and `scripts/demo_generate_deck.py` to create demo outputs locally. Store real delivery references only in the selected private state root.
