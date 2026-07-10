# Orchestration and parallel execution

This file defines when consulting-deck work may be parallelized and when it must remain serial. The task-list structure is mandatory even in environments without subagents; parallelism is an acceleration mechanism, not a substitute for analytical quality.

All workers must follow `references/content-density.md`. Research workers return structured evidence, page workers render frozen analysis, and QA workers check content depth as well as visual correctness.

## Execution modes

### Mode A — Serial execution

Use when the environment has no subagent support, such as many Copilot/Codex-style environments and interactive chat. Follow the same task lists, research queues, evidence schemas and page briefs, but execute them in order.

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

Use after storyline, page briefs and evidence findings are frozen in `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/baseline/`. Page workers produce page modules, not PPTX files.

## Parallelization decision table

| Work item | Parallelize? | Rationale |
|---|---|---|
| Step 1 demand clarification | No | Single owner preserves context, scope and assumptions |
| Step 2 Storyline and coverage map | No | Horizontal logic requires one author and one narrative spine |
| Step 3 Exhibit Plan | Limited | Page briefs may be drafted in parallel only after storyline is frozen; main agent reconciles content budgets and appendix coverage |
| Step 4 Evidence Research | Yes | Claims and evidence clusters can be researched independently; include support and counter-evidence searches |
| Step 5 confirmation / automatic execution gate | No | Decision and completeness gates must be controlled by the main agent |
| Step 6 page generation | Yes, with constraints | Generate page modules in parallel, then assemble in one process |
| Step 7 consulting and content-depth QA | Limited | Vertical page QA can be parallel; horizontal logic, coverage, executive-summary synthesis and deck-wide numeric consistency must be serial |
| Step 8 rendering QA | Yes | Visual checks can be assigned in batches of 3–5 slides; final fix pass remains serial |

## Hard prohibitions

1. Do not write storyline in parallel. The storyline must have a single owner.
2. Do not let multiple agents write to the same `.pptx` file concurrently.
3. Do not merge independently generated PPTX sections as the default approach; cross-file merging often causes style drift.
4. Do not define new colors, fonts or sizing in page modules. Use existing helpers and theme tokens.
5. Do not keep process state only in local scratch files or chat history. Persist state under a private project-state root.
6. Do not write customer-identifiable state into this public skill repository.
7. Do not let research workers return only narrative summaries when the page brief requires numbers, definitions, formulas or source metadata.
8. Do not let page workers invent facts, assumptions, comparison sets or analytical methods that are absent from the frozen brief.
9. Do not split one broad research task among many agents without assigning non-overlapping source or evidence scopes; duplicated shallow research does not improve quality.

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

Rules:

- The module receives a blank slide and a shared `ctx` object.
- The module may only import existing repository helpers: `scripts/consulting_layouts.py`, `scripts/consulting_shapes.py`, `scripts/business_case.py`, and `scripts/architecture_helpers.py`.
- The module may not create or save a `Presentation` object.
- The module must read page state from the frozen baseline or from assembler-provided `ctx`; it must not mutate `baseline/`.
- The module must render the required evidence IDs, comparison basis, insight annotations, implication and appendix reference defined in the page brief.
- The module must not introduce unregistered numbers or unsupported claims.
- The main agent assembles the final deck in a single process and in storyline order.

### Minimum `ctx` schema

The main assembler must pass at least these fields to every page module:

| Field | Type | Purpose |
|---|---|---|
| `page_num` | `int` | Current slide number for footer and QA references |
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

A page module must not invent additional required `ctx` fields without updating this schema.

## Evidence Research parallel pattern

For each page brief or evidence cluster, create a research task containing:

| Field | Description |
|---|---|
| Page / cluster | Slide number, section reference or evidence domain |
| Claim | Judgment, number or comparison to verify |
| Required data points | Exact metrics, periods, entities, definitions or documents needed |
| Comparison basis | Peer, historical period, segment, geography, scenario or benchmark |
| Support query | Query designed to find supporting evidence |
| Counter query | Query designed to find contradictory evidence or limitations |
| Evidence type | Market, competitor, product capability, pricing, regulation, financial, customer proof, implementation, operations or risk |
| Preferred sources | Source priority, date requirement and source constraints |
| Output | Structured fact/calculation objects plus research notes |

### Required research-worker output

Research workers must return records compatible with `references/project-state.md`, including:

- proposed evidence ID;
- claim;
- value or qualitative assertion;
- unit, period, entity and definition;
- source type and source tier;
- source date, retrieval date and page/section;
- calculation basis and input fact IDs where applicable;
- supporting evidence;
- counter-evidence;
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
5. assess whether the evidence supports the strength of the action title;
6. update caveats and counter-thesis pages;
7. verify that each core page meets its content budget;
8. plan appendix pages for detailed tables, definitions, calculations and rejected alternatives;
9. persist the reconciled result to `evidence.json`, `research-log.md`, `briefs.yaml` and `assumptions.md`.

Research findings must be reconciled by the main agent and persisted before page generation.

## QA-worker pattern

Vertical QA workers may review one page or a small page batch. Their output must include:

- conclusion-evidence alignment;
- missing promised data points;
- comparison or analysis-method quality;
- calculation traceability;
- insight annotation quality;
- implication and caveat completeness;
- appendix linkage;
- visual readability and source-line presence;
- specific remediation actions.

The main agent retains ownership of horizontal logic, cross-page consistency, executive-summary synthesis and the final accept/reject decision.

## Failure degradation

- Research worker timeout: mark the item as unresolved and downgrade to a clearly labelled team assumption, unless the claim is central to the recommendation.
- Three unsuccessful searches: downgrade to a team assumption or remove/weaken the page.
- Broad but shallow output: reissue a narrower task specifying required data points, period, entity, comparison and source hierarchy.
- Page worker failure twice: the main agent takes back the page and generates it serially.
- Numeric conflict across research workers: apply source priority, document the definition gap, and record the difference in appendix or speaker notes.
- Source-definition conflict: retain both definitions, choose the most decision-relevant one for the core deck and document reconciliation.
- Visual QA worker disagreement: final judgment belongs to the main agent after rendering review.
- Content-density failure: return to the page brief and research queue; do not repair it by adding generic prose.

## Platform adaptation

- Claude Code with Task tool: use all three modes where useful.
- Codex environments with subagents: parallelize evidence clusters and page modules, but keep storyline, evidence reconciliation and final assembly serial.
- GitHub Copilot environments: use agent/worktree features where available; otherwise execute serially while preserving the same task lists and state files.
- Interactive chat without subagents: execute the research queue and page briefs serially.
- The absence of subagents must not skip Evidence Research, content-density checks, page-brief reconciliation, consulting QA or rendering QA.