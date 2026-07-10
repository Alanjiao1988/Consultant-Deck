# Consultant Deck Skill

A research-heavy consulting-style PowerPoint skill for generating executive-ready decks with storyline discipline, data-rich page briefs, mandatory evidence research, support and counter-evidence checks, analytical content-density gates, appendix depth, private project-state persistence, fact-table QA, subagent orchestration rules, revision loop, Chinese-English typography rules, and reusable PowerPoint-native data exhibits.

## What this version fixes

Earlier versions could produce a structurally correct but analytically thin deck: action titles and consulting layouts were present, yet pages could still contain only frameworks, icons, generic architecture boxes or a small number of uncontextualized facts.

This version makes **research-heavy consulting mode** the default unless the user explicitly requests a short executive brief.

Key changes:

1. Added `references/content-density.md` with hard numeric-density gates and minimum analytical depth by page type.
2. Added page-level contracts for required data points, quantification, concrete benchmarks, evidence IDs, comparison basis, analysis method, insight annotations, decision implication and appendix link.
3. Research-heavy analytical page bodies normally require at least 3 visible, unique numeric facts already registered in `evidence.json`, with 4–8 evidence items supporting the full page.
4. Explicit conceptual-framework pages are exceptions, but should normally remain below 25% of eligible pages.
5. Strong qualitative wording such as `显著提升` or `rapidly growing` is flagged when no number, range or evidence basis appears in the statement.
6. Non-numeric analytical titles require a dedicated quantification research task or documented justification after reasonable searches.
7. Added default deck-level evidence floors: for a typical 10-page core deck, 25–50 registered facts/calculations, 8–15 relevant sources, at least 5 data-bearing exhibits and at least 3 appendix pages.
8. Expanded strategy, IT/cloud, AI, sales proposal, investment and vendor archetypes into detailed analytical blueprints with minimum evidence packs.
9. Expanded `evidence.json` to capture period, entity, source tier, calculation formula, input fact IDs, caveat, confidence and page usage.
10. Added `research-log.md` to retain query decisions, rejected evidence and unresolved conflicts.
11. Added executable brief QA and table/chart-aware PPTX QA.
12. Replaced the concept-heavy demo with a data-rich example containing dense tables, a combo chart and CAGR, peer benchmark, quantified driver tree, sensitivity and quantified roadmap.
13. Added editable data-exhibit helpers: `dense_table`, `driver_tree`, `benchmark_bar`, `bar_h`, `area_stacked`, `combo_chart`, `cagr_annotation` and `chart_with_data_table`.

The repository also retains the consulting delivery workflow: storyline → exhibit plan → evidence research → page production → consulting QA → rendering QA, with private project-state security, fact consistency checks, subagent orchestration and revision-mode support.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/create_template.py
python scripts/demo_generate_deck.py

python scripts/qa_briefs.py examples/demo_ai_transformation.briefs.yaml \
  --facts examples/demo_ai_transformation.evidence.json \
  --json

python scripts/qa_pptx.py examples/demo_ai_transformation.pptx \
  --facts examples/demo_ai_transformation.evidence.json \
  --briefs examples/demo_ai_transformation.briefs.yaml \
  --json

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
  → Step 7 咨询、量化与内容深度 QA
  → Step 8 渲染 QA
```

Evidence Research must create a research task list from all page briefs. Each key claim needs one support query and one counter-evidence query. Quantitative tasks should normally return a core metric, at least 2–3 comparable time points and one to two comparable entities/scenarios, with findings written back as value, unit, period, entity, definition, source, source tier, retrieval date, calculation basis, caveat and confidence.

Having a source is not enough. Every analytical page also needs a central quantification, a concrete benchmark, a comparison or analytical method and enough evidence to support executive challenge.

## Research-heavy default

Unless the user explicitly asks for a concise executive brief, strategy, market, investment, vendor, cloud, AI, transformation and pre-sales decks should use research-heavy consulting mode.

Every core page should normally include:

- one evidence-backed action title;
- one primary analytical exhibit;
- at least 3 visible registered numeric facts in the body;
- 4–8 evidence items supporting the full page;
- a baseline, target, gap, range or decomposition;
- a concrete peer, threshold, scenario or historical benchmark;
- at least one comparison, trend, bridge, scenario or sensitivity;
- two to four insight annotations;
- a decision implication;
- caveat and source line;
- appendix backup for detailed methodology or data.

Concept-only pages are not allowed by default. Covers, section dividers and explicitly requested conceptual frameworks are exceptions. Missing data must trigger more research, a weaker conclusion or page removal—never invented numbers.

## Data-exhibit helpers

The main PowerPoint-native helpers in `scripts/consulting_shapes.py` include:

- `dense_table()` for detailed editable business tables;
- `benchmark_bar()` for peer and threshold comparisons;
- `driver_tree()` for quantified value, revenue or TCO decomposition;
- `native_chart()` with `column`, `bar_h`, `stacked_bar`, `line`, `area_stacked` and `combo` modes;
- `cagr_annotation()` for calculated trend labels;
- `chart_with_data_table()` for visual trend plus exact values;
- existing waterfall, 2x2, option-evaluation, risk and RACI helpers.

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
- Do not accept an isolated number when comparable periods or entities are reasonably available.
- Do not invent data to pass density QA.
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
  qa_briefs.py
  qa_pptx.py
tests/
  test_shapes.py
  test_qa_briefs.py
  test_data_exhibits.py
```

## CI validation

The pull-request workflow:

1. installs dependencies;
2. generates the template;
3. generates the data-rich demo PPTX, evidence table and briefs;
4. requires zero page-brief QA warnings/errors;
5. requires zero PPTX QA findings using both facts and briefs;
6. runs the full pytest suite.

## Behavioral validation

1. A request for a strategy, market, investment, vendor, IT/cloud or AI deck defaults to research-heavy mode unless the user explicitly requests a brief.
2. Page briefs without quantification, benchmark, required data points, comparison basis or analysis method fail the production gate.
3. Research-heavy analytical pages with fewer than 3 visible registered numeric facts produce a density warning.
4. Generic concept pages without quantified baselines, targets, trade-offs or implementation details fail content-depth QA.
5. Unsupported strong qualitative claims produce a warning.
6. The demo must return zero brief and PPTX QA findings.
7. If a demo slide number is manually changed to conflict with `evidence.json`, fact QA reports a consistency error.
8. A mixed-language cover such as `某银行数字化转型 strategy` produces a terminology warning.
9. If a user asks to modify a page after a frozen baseline exists, the agent enters revision mode and reruns scoped QA.
10. Publicly accessible paths contain no real project-state files.

Generated binary PPTX files are intentionally not stored in the repository by default. Run `scripts/create_template.py` and `scripts/demo_generate_deck.py` to create demo outputs locally. Store real delivery references only in the selected private state root.
