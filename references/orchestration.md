# Orchestration and parallel execution

This file defines when consulting-deck work may be parallelized and when it must remain serial. The task-list structure is mandatory even in environments without subagents; parallelism is an acceleration mechanism, not a substitute for analytical quality.

All workers must follow `references/content-density.md`. Research workers return structured evidence, page workers render frozen analysis, exhibit helpers return semantic manifests where applicable, and QA workers check content depth as well as visual correctness.

## Execution modes

### Mode A — Serial execution

Use when the environment has no subagent support, such as many Copilot/Codex-style environments and interactive chat. Follow the same task lists, research queues, evidence schemas, page briefs and manifest gates, but execute them in order.

### Mode B — Research-parallel execution

Use when subagents or task workers are available. Evidence Research is the highest-value parallel section because each page brief or evidence cluster can usually be researched independently.

Parallelize by evidence domain or page cluster, not by asking multiple agents to research the same broad topic. Recommended clusters:

- market, regulation and industry structure;
- company financials and management guidance;
- competitors and peer benchmarks;
- product capability, architecture and pricing;
- customer evidence and implementation benchmarks;
- operating model, adoption and risk;
- counter-thesis and contradictory evidence.

### Mode C — Page-module execution

Use after storyline, page briefs and evidence findings are frozen in `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/baseline/`. Page workers produce page modules and optional exhibit-manifest records, not PPTX files.

## Parallelization decision table

| Work item | Parallelize? | Rationale |
|---|---|---|
| Step 1 demand clarification | No | Single owner preserves context, scope and assumptions |
| Step 2 Storyline and coverage map | No | Horizontal logic requires one author and one narrative spine |
| Step 3 Exhibit Plan | Limited | Page briefs may be drafted in parallel only after storyline is frozen; main agent reconciles content budgets, qualitative-exhibit contracts and appendix coverage |
| Step 4 Evidence Research | Yes | Claims and evidence clusters can be researched independently; include support and counter-evidence searches |
| Step 5 confirmation / automatic execution gate | No | Decision and completeness gates must be controlled by the main agent |
| Step 6 page generation | Yes, with constraints | Generate page modules in parallel, then assemble the PPTX and manifest in one process |
| Step 7 consulting and content-depth QA | Limited | Vertical page QA can be parallel; horizontal logic, coverage, executive-summary synthesis, manifest reconciliation and deck-wide consistency must be serial |
| Step 8 semantic/rendering QA | Yes | Semantic exhibit QA and visual checks can run independently; final fix and acceptance remain serial |

## Hard prohibitions

1. Do not write storyline in parallel. The storyline must have a single owner.
2. Do not let multiple agents write to the same `.pptx` file concurrently.
3. Do not let multiple agents append directly to the same `*.exhibits.json`; workers return manifest records to the main assembler.
4. Do not merge independently generated PPTX sections as the default approach; cross-file merging often causes style drift.
5. Do not define new colors, fonts or sizing in page modules. Use existing helpers and theme tokens.
6. Do not keep process state only in local scratch files or chat history. Persist state under a private project-state root.
7. Do not write customer-identifiable state, evidence or manifests into this public skill repository.
8. Do not let research workers return only narrative summaries when the page brief requires numbers, definitions, formulas or source metadata.
9. Do not let page workers invent facts, assumptions, comparison sets, classification dimensions or analytical methods absent from the frozen brief.
10. Do not discard a semantic manifest returned by a data-driven exhibit helper.
11. Do not lower Evidence Discipline to satisfy data-density targets. Missing numbers trigger deeper research, a weaker conclusion, an approved qualitative-exhibit contract or page removal—not fabrication.

## Page-module assembly pattern

When generating pages in parallel, use page modules under the private draft directory:

```text
<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/pages/page_01.py
<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/pages/page_02.py
<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/pages/page_03.py
```

Each page module must expose the same signature:

```python
def render(slide, ctx):
    ...
```

A module may return either `None` or one or more semantic exhibit records:

```python
def render(slide, ctx):
    manifest = categorical_jurisdiction_map(...)
    return [manifest]
```

Rules:

- The module receives a blank slide and a shared `ctx` object.
- The module may only import existing repository helpers: `scripts/consulting_layouts.py`, `scripts/consulting_shapes.py`, `scripts/jurisdiction_map`, `scripts/business_case.py`, and `scripts/architecture_helpers.py`.
- The module may not create or save a `Presentation` object.
- The module must read page state from the frozen baseline or assembler-provided `ctx`; it must not mutate `baseline/`.
- The module must render the required evidence IDs, quantification or approved qualitative contract, benchmark/comparison basis, insight annotations, implication and appendix reference defined in the page brief.
- The module must not introduce unregistered numbers or unsupported claims.
- The module must return every manifest produced by a data-driven exhibit helper.
- The main agent assembles the final deck in storyline order, validates manifest page numbers, and writes one sidecar file under `output/`.

### Minimum `ctx` schema

The main assembler must pass at least these fields to every page module:

| Field | Type | Purpose |
|---|---|---|
| `page_num` | `int` | Current slide number for footer, manifest and QA references |
| `sections` | `list[str]` | Ordered section names for tracker or divider pages |
| `current_section` | `int` or `str` | Current section index/name for tracker highlighting |
| `lang` | `str` | Output language, usually `zh`, `en`, or `mixed` |
| `source` | `str` or `None` | Source line or calculation basis for footer |
| `draft_dir` | `str` | Private path under `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/` |

Recommended optional fields:

| Field | Type | Purpose |
|---|---|---|
| `theme` | `dict` | Theme tokens from `assets/theme.json` |
| `page_brief` | `dict` | Frozen page brief read from `briefs.yaml` |
| `evidence` | `list[dict]` | Evidence findings and calculations read from `evidence.json` |
| `assumptions` | `list[str]` | Page-level assumptions or caveats from `assumptions.md` |
| `appendix_map` | `dict` | Core-page to appendix-page references |
| `source_map` | `dict` | Evidence ID to compact source-line representation |
| `manifest_records` | `list[dict]` | Assembler-owned collection; workers must not mutate it concurrently |

A page module must not invent additional required `ctx` fields without updating this schema.

## Manifest assembly gate

The main assembler owns this serial workflow:

1. collect returned records from every page module;
2. require an integer `page` matching the assembled slide;
3. reject duplicate exhibit IDs or contradictory records for the same page;
4. ensure every page brief that names `exhibit_manifest` produced at least one matching record;
5. write `<private-draft-dir>/output/<deck-name>.exhibits.json` once, after PPTX assembly;
6. run `qa_exhibits.py` against the sidecar and `evidence.json` before accepting PPTX/render QA.

A PPTX that renders correctly but has a missing, stale or failing semantic manifest is incomplete.

## Qualitative-exhibit pages

A page whose primary proof is a categorical map or similar evidence-backed qualitative classification must be explicitly planned as:

```yaml
content_density_target: qualitative-exhibit
min_registered_numbers: 0
exhibit_manifest: output/<deck-name>.exhibits.json
appendix_link: A6
```

The page worker must also render coverage reviewed/shown, as-of date, selection basis, caveat and decision implication. The research worker must register the classifications as qualitative evidence and coverage counts as numeric evidence where available. The appendix must show the full reviewed universe. This contract replaces the generic three-number floor but does not create a concept-page exemption.

## Evidence Research parallel pattern

For each page brief or evidence cluster, create a research task containing:

| Field | Description |
|---|---|
| Page / cluster | Slide number, section reference or evidence domain |
| Claim | Judgment, number or comparison to verify |
| Required data points | Exact metrics, periods, entities, definitions or documents needed |
| Quantification | Baseline, target, gap, range, decomposition, threshold or approved qualitative coverage contract |
| Comparison basis | Peer, historical period, segment, geography, scenario, benchmark or classification universe |
| Benchmark | Named comparable entity, value/range/threshold or reviewed universe and definition |
| Support query | Query designed to find supporting evidence |
| Counter query | Query designed to find contradictory evidence or limitations |
| Evidence type | Market, competitor, product capability, pricing, regulation, financial, customer proof, implementation, operations or risk |
| Preferred sources | Source priority, date requirement and source constraints |
| Output | Structured fact/calculation objects plus research notes |

### Minimum quantitative output specification

Unless the page brief explicitly uses the qualitative-exhibit contract, each quantitative research task should return:

1. the core current metric or conclusion value;
2. a time series with at least 2–3 comparable time points;
3. one to two comparable entities, scenarios or thresholds;
4. the unit, period, entity, definition and source for every value;
5. calculation formula and input evidence IDs;
6. at least one limitation, counter-evidence item or comparability caveat.

A task that returns one isolated number is incomplete when a time series or comparable is reasonably available. If the source exposes only one defensible number, report failed comparison searches and the limitation rather than inventing context.

### Required research-worker output

Research workers must return records compatible with `references/project-state.md`, including:

- proposed evidence ID;
- claim;
- value or qualitative assertion;
- unit, period, entity and definition;
- source type and source tier;
- source date, retrieval date and page/section;
- calculation basis and input fact IDs where applicable;
- supporting evidence and counter-evidence;
- caveat and comparability limitations;
- confidence;
- recommended pages;
- implication for the action title;
- unresolved gaps.

A response such as “the market is growing quickly and major vendors are investing” is not acceptable research output.

## Main-agent reconciliation

Before freezing evidence, the main agent must:

1. deduplicate facts and normalize units, periods and definitions;
2. resolve source conflicts using the source hierarchy;
3. distinguish management claims from independent evidence;
4. verify formulas and input fact IDs;
5. assess whether evidence supports the action-title strength;
6. verify non-numeric titles have completed quantification tasks or justified rationales;
7. update caveats and counter-thesis pages;
8. verify each core page meets its quantification or qualitative-exhibit contract;
9. plan appendix pages for detailed tables, definitions, calculations and rejected alternatives;
10. persist `evidence.json`, `research-log.md`, `briefs.yaml` and `assumptions.md` before generation.

## QA-worker pattern

Vertical QA workers may review one page or a small batch. Their output must include:

- conclusion-evidence alignment;
- missing promised data points;
- visible registered-number count or qualitative-exhibit contract compliance;
- quantification/benchmark or classification/coverage quality;
- comparison or analysis-method quality;
- calculation and evidence traceability;
- unsupported strong qualitative wording;
- insight annotation quality;
- implication and caveat completeness;
- appendix linkage;
- expected manifest record and evidence references;
- visual readability and source-line presence;
- specific remediation actions.

The main agent retains ownership of horizontal logic, cross-page consistency, manifest reconciliation, executive-summary synthesis and the final accept/reject decision.

## Failure degradation

- Research worker timeout: mark unresolved and downgrade to a clearly labelled assumption unless central to the recommendation.
- Three unsuccessful searches: downgrade to an assumption or remove/weaken the page.
- Broad but shallow output: reissue a narrower task specifying required data points, period, entity, comparison and source hierarchy.
- Isolated-number output: request time points and comparables, or record why they do not exist.
- Page worker failure twice: main agent takes back the page and generates serially.
- Missing manifest return: fail the page module; do not reconstruct semantic data from marker colours.
- Numeric conflict: apply source priority and document the definition gap.
- Visual QA disagreement: final judgment belongs to the main agent after rendering review.
- Content-density failure: return to the brief and research queue; do not repair with generic prose or unsupported numbers.

## Platform adaptation

- Claude Code with Task tool: use all three modes where useful.
- Codex environments with subagents: parallelize evidence clusters and page modules, but keep storyline, reconciliation, final assembly and manifest writing serial.
- GitHub Copilot environments: use agent/worktree features where available; otherwise execute serially while preserving the same state files and gates.
- Interactive chat without subagents: execute the research queue and page briefs serially.
- The absence of subagents must not skip Evidence Research, manifest persistence, semantic exhibit QA, content-density checks, page-brief reconciliation, consulting QA or rendering QA.
