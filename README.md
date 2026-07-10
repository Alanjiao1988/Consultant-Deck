# Consultant Deck Skill

A research-heavy consulting-style PowerPoint skill for generating executive-ready decks with storyline discipline, data-rich page briefs, mandatory evidence research, support and counter-evidence checks, analytical content-density gates, appendix depth, private project-state persistence, fact-table QA, subagent orchestration rules, revision loop, Chinese-English typography rules, and reusable PowerPoint-native layout/chart helpers.

## What this version fixes

Earlier versions could produce a structurally correct but analytically thin deck: action titles and consulting layouts were present, yet pages could still contain only frameworks, icons, generic architecture boxes or a small number of uncontextualized facts.

This version makes **research-heavy consulting mode** the default unless the user explicitly requests a short executive brief.

Key changes:

1. Added `references/content-density.md` with minimum analytical depth by page type.
2. Added hard page-level requirements: required data points, evidence IDs, comparison basis, analysis method, insight annotations, decision implication and appendix link.
3. Core analytical pages now require at least 2 registered evidence items and normally 4–8 in research-heavy mode.
4. Added default deck-level evidence floors: for a typical 10-page core deck, 25–50 registered facts/calculations, 8–15 relevant sources, at least 5 data-bearing exhibits and at least 3 appendix pages.
5. Expanded strategy, IT/cloud, AI, sales proposal, investment and vendor archetypes into detailed analytical blueprints with minimum evidence packs.
6. Expanded page patterns so charts, roadmaps, architecture, option evaluation, risk and business-case pages include the analysis needed to support decisions.
7. Added content-depth and deck-density QA. A polished but sparse deck now fails QA.
8. Expanded `evidence.json` to capture period, entity, source tier, calculation formula, input fact IDs, caveat, confidence and page usage.
9. Added `research-log.md` to retain query decisions, rejected evidence and unresolved conflicts.
10. Updated `SKILL.md`, `AGENTS.md` and Copilot instructions so Codex/Copilot execute these rules rather than treating them as optional references.

The repository also retains the earlier consulting delivery workflow: storyline → exhibit plan → evidence research → page production → consulting QA → rendering QA, with private project-state security, fact consistency checks, subagent orchestration and revision-mode support.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/create_template.py
python scripts/demo_generate_deck.py
python scripts/qa_pptx.py examples/demo_ai_transformation.pptx --facts examples/demo_ai_transformation.evidence.json
pytest tests/ -q
```

## Required workflow

```text
Step 1 需求与深度确认
  → Step 2 Storyline 与 coverage map
  → Step 3 Exhibit Plan 与 content budget
  → Step 4 Evidence Research
  → Step 5 确认/自动执行
  → Step 6 逐页生成
  → Step 7 咨询与内容深度 QA
  → Step 8 渲染 QA
```

Evidence Research must create a research task list from all page briefs. Each key claim needs one support query and one counter-evidence query, with findings written back as value, unit, period, entity, definition, source, source tier, retrieval date, calculation basis, caveat and confidence.

Having a source is not enough. Every analytical page also needs a comparison or analytical method and enough evidence to support executive challenge.

## Research-heavy default

Unless the user explicitly asks for a concise executive brief, strategy, market, investment, vendor, cloud, AI, transformation and pre-sales decks should use research-heavy consulting mode.

Every core page should normally include:

- one evidence-backed action title;
- one primary analytical exhibit;
- 4–8 evidence items in research-heavy mode;
- at least one comparison, trend, benchmark, decomposition, bridge, scenario or sensitivity;
- two to four insight annotations;
- a decision implication;
- caveat and source line;
- appendix backup for detailed methodology or data.

Concept-only pages are not allowed by default. Covers, section dividers and explicitly requested conceptual frameworks are exceptions.

## Private state layer

Real project process artifacts must be stored outside this public skill repo. Preferred target:

```text
<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/
```

The private draft directory should contain `storyline.md`, `briefs.yaml`, `evidence.json`, `research-log.md`, `assumptions.md`, `pages/`, `output/`, `baseline/`, and `changelog.md`. See `references/project-state.md`.

If `baseline/` exists for a project, follow `references/revision-loop.md` instead of regenerating the full deck.

Security rule: customer names, internal numbers, project code names, non-public architecture details, source documents, draft storylines, `briefs.yaml`, `evidence.json` and assumptions must never be written to public storage.

## Parallel execution rules

See `references/orchestration.md`.

Hard prohibitions:

- Do not let multiple agents write to the same `.pptx` concurrently.
- Do not parallelize storyline writing.
- Do not skip Evidence Research in environments without subagents; execute the same task list serially.
- Do not generate generic narrative summaries when structured facts are required.
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
  content-density.md
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

1. A request for a strategy, market, investment, vendor, IT/cloud or AI deck should default to research-heavy mode unless the user explicitly requests a brief.
2. Page briefs without required data points, comparison basis or analysis method should fail the production gate.
3. Generic concept pages without quantified baselines, targets, trade-offs or implementation details should fail content-depth QA.
4. Demo with `--facts` should return zero automated QA findings.
5. If a demo slide number is manually changed to conflict with `evidence.json`, `qa_pptx.py --facts` should report a `fact_consistency` error.
6. A mixed-language cover such as `某银行数字化转型 strategy` should produce a terminology warning.
7. If a user asks to modify page 3 after a frozen baseline exists, the agent should enter revision mode: diff the baseline, list impacted pages, update only affected artifacts, rerun scoped QA, and write a versioned changelog entry.
8. Publicly accessible paths must contain no real project state files.

Generated binary PPTX files are intentionally not stored in the repository by default. Run `scripts/create_template.py` and `scripts/demo_generate_deck.py` to create demo outputs locally. Store real delivery references only in the selected private state root.