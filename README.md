# Consultant Deck Skill

A consulting-style PowerPoint skill for generating executive-ready decks with storyline discipline, action titles, exhibit planning, evidence discipline, Chinese-English typography rules, and reusable PowerPoint-native layout/chart helpers.

## What was fixed

This version addresses the earlier review gaps:

1. Added a full consulting delivery workflow: storyline → exhibit plan → page production → consulting QA → rendering QA.
2. Added reusable deck archetypes for strategy, IT/cloud transformation, sales proposal, investment analysis, vendor evaluation, executive decision meetings and workshops.
3. Added stronger evidence discipline and QA checks so the skill does not invent data.
4. Added IT consulting patterns for cloud migration, AI transformation, application modernization, data platform, security, business case and adoption.
5. Added reusable scripts for layouts, consulting exhibits, business-case pages, architecture pages, template generation, demo generation and automated QA.
6. Added `AGENTS.md` and `.github/copilot-instructions.md` so GitHub Copilot/Codex-style agents can use the repo directly.

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

## Repository layout

```text
SKILL.md
AGENTS.md
.github/copilot-instructions.md
references/
  deck-archetypes.md
  exhibit-planning.md
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

## Validation performed locally

```bash
python scripts/create_template.py
python scripts/demo_generate_deck.py
python scripts/qa_pptx.py examples/demo_ai_transformation.pptx --json
pytest -q
```

Result: tests passed; QA returned no errors.

Note: generated binary PPTX files are intentionally not stored in the repository. Run `scripts/create_template.py` and `scripts/demo_generate_deck.py` to create them locally.
