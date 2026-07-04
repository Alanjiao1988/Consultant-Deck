# Orchestration and parallel execution

This file defines when consulting-deck work may be parallelized and when it must remain serial. The task list structure is mandatory even in environments without subagents; parallelism is an acceleration mechanism, not a required capability.

## Execution modes

### Mode A — Serial execution

Use when the environment has no subagent support, such as many Copilot/Codex-style environments and interactive chat. Follow the same task lists, research queues and page briefs, but execute them in order.

### Mode B — Research-parallel execution

Use when subagents or task workers are available. Evidence Research is the highest-value parallel section because each page brief can usually be researched independently.

### Mode C — Page-module execution

Use after storyline, page briefs and evidence findings are frozen. Page workers produce page modules, not PPTX files.

## Parallelization decision table

| Work item | Parallelize? | Rationale |
|---|---|---|
| Step 1 demand clarification | No | Single owner preserves context and assumptions |
| Step 2 Storyline | No | Horizontal logic requires one author and one narrative spine |
| Step 3 Exhibit Plan | Limited | Page briefs may be drafted in parallel only after storyline is frozen; main agent reconciles |
| Step 4 Evidence Research | Yes | Each key claim can be researched independently; include support and counter-evidence searches |
| Step 5 confirmation / automatic execution gate | No | Decision gate must be controlled by the main agent |
| Step 6 page generation | Yes, with constraints | Generate page modules in parallel, then assemble in one process |
| Step 7 consulting QA | Limited | Vertical page QA can be parallel; horizontal logic and deck-wide numeric consistency must be serial |
| Step 8 rendering QA | Yes | Visual checks can be assigned in batches of 3–5 slides; final fix pass remains serial |

## Hard prohibitions

1. Do not write storyline in parallel. The storyline must have a single owner.
2. Do not let multiple agents write to the same `.pptx` file concurrently.
3. Do not merge independently generated PPTX sections as the default approach; cross-file merging often causes style drift.
4. Do not define new colors, fonts or sizing in page modules. Use existing helpers and theme tokens.

## Page-module assembly pattern

When generating pages in parallel, use page modules:

```text
pages/page_01.py
pages/page_02.py
pages/page_03.py
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
- The main agent assembles the final deck in a single process and in storyline order.

## Evidence Research parallel pattern

For each page brief, create a research task containing:

| Field | Description |
|---|---|
| Page | Slide number or section reference |
| Claim | Judgment or number to verify |
| Support query | Query designed to find supporting evidence |
| Counter query | Query designed to find contradictory evidence or limitations |
| Evidence type | Market data, competitor, product capability, pricing, regulation, financial, customer proof |
| Preferred sources | Source priority or source constraints |
| Output | Number, unit, definition, source, retrieval date, caveat |

Research findings must be reconciled by the main agent before page generation.

## Failure degradation

- Research worker timeout: mark the item as unresolved and downgrade to a clearly labelled team assumption, unless the claim is central to the recommendation.
- Three unsuccessful searches: downgrade to a team assumption or remove the page.
- Page worker failure twice: the main agent takes back the page and generates it serially.
- Numeric conflict across research workers: apply source priority, document the definition gap, and record the difference in appendix or speaker notes.
- Visual QA worker disagreement: final judgment belongs to the main agent after rendering review.

## Platform adaptation

- Claude Code with Task tool: use all three modes where useful.
- claude.ai, many Codex environments and many Copilot environments: subagents may not exist; execute serially while preserving the same task lists.
- The absence of subagents must not skip Evidence Research, page brief reconciliation, consulting QA or rendering QA.
