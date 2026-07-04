# Consultant Deck Skill

A consulting-style PowerPoint skill for generating executive-ready decks with storyline discipline, action titles, exhibit planning, mandatory evidence research, support and counter-evidence checks, subagent orchestration rules, Chinese-English typography rules, and reusable PowerPoint-native layout/chart helpers.

## What was fixed

This version addresses the earlier review gaps:

1. Added a full consulting delivery workflow: storyline → exhibit plan → evidence research → page production → consulting QA → rendering QA.
2. Added mandatory Evidence Research before confirmation or automatic execution. Every key claim requires support and counter-evidence searches.
3. Added reusable deck archetypes for strategy, IT/cloud transformation, sales proposal, investment analysis, vendor evaluation, executive decision meetings and workshops.
4. Added stronger evidence discipline and QA checks so the skill does not invent data.
5. Added IT consulting patterns for cloud migration, AI transformation, application modernization, data platform, security, business case and adoption.
6. Added orchestration rules for subagent parallelism, page-module assembly, failure degradation and serial fallback.
7. Added reusable scripts for layouts, consulting exhibits, business-case pages, architecture pages, template generation, demo generation and automated QA.
8. Added `AGENTS.md` and `.github/copilot-instructions.md` so GitHub Copilot/Codex-style agents can use the repo directly.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

python scripts/create_template.py
python scripts/demo_generate_deck.py
python scripts/qa_pptx.py examples/demo_ai_transformation.pptx
pytest
```

## Required workflow

```text
Step 1 需求澄清 → Step 2 Storyline → Step 3 Exhibit Plan → Step 4 Evidence Research → Step 5 确认/自动执行 → Step 6 逐页生成 → Step 7 咨询 QA → Step 8 渲染 QA
```

Evidence Research must create a research task list from all page briefs. Each key claim needs one support query and one counter-evidence query, with findings written back as number, unit, definition, source, retrieval date and caveat.

## Parallel execution rules

See `references/orchestration.md`.

Hard prohibitions:

- Do not let multiple agents write to the same `.pptx` concurrently.
- Do not parallelize storyline writing.
- Do not skip Evidence Research in environments without subagents; execute the same task list serially.

## Repository layout

```text
SKILL.md
AGENTS.md
.github/copilot-instructions.md
references/
  deck-archetypes.md
  exhibit-planning.md
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
python scripts/qa_pptx.py examples/demo_ai_transformation.pptx --json
pytest -q
```

Generated binary PPTX files are intentionally not stored in the repository. Run `scripts/create_template.py` and `scripts/demo_generate_deck.py` to create them locally.
