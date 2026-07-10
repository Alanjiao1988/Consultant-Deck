# Revision loop

Use this flow whenever a frozen baseline already exists in `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/baseline/`. Do not regenerate the full deck by default.

## Trigger condition

If the private project draft directory contains a frozen baseline snapshot, any change request enters revision mode. Revision mode applies even when the user asks for a small wording, chart, fact or page-order change.

A user complaint such as “内容太少”“太概念化”“缺乏数据”“没有细节”“像提纲而不像咨询报告” is a **content-depth revision**, not a wording or visual revision.

## Local revision rules

1. Diff against the frozen baseline before editing and state the intended change scope.
2. Modify only the target page brief and target page module unless dependencies require additional updates.
3. List impacted pages before execution. Impacted pages include shared-number pages, executive summary pages, appendix pages, tracker pages and page-number changes.
4. Do not silently propagate changes. Every dependent update must be explicit.
5. When adding, deleting or reordering pages, update `storyline.md`, page numbers, trackers, executive summary references and appendix references.
6. Persist every changed process artifact back to the same private draft path.
7. Do not copy real customer revision state into the public skill repository.
8. Do not repair a content-depth problem by merely adding paragraphs, icons or smaller text.
9. When a page is too dense after adding valid analysis, split it or move detail into a linked appendix page.

## Content-depth revision flow

When the feedback is that the deck is sparse or conceptual:

1. Re-open `references/content-density.md` and assess the affected pages against the page-type minimums.
2. Inspect `briefs.yaml` for missing `required_data_points`, `comparison_basis`, `analysis_method`, `evidence_ids`, `insight_annotations`, `decision_implication` and `appendix_link`.
3. Inspect `evidence.json` for insufficient facts, weak source tiers, missing periods/definitions, untraceable calculations or absent counter-evidence.
4. Create targeted research tasks for the missing content; do not issue broad “research more” instructions.
5. Reconcile new findings into `evidence.json`, `research-log.md`, `briefs.yaml` and `assumptions.md`.
6. Decide whether the page should be enriched, split into two core pages, or supported with new appendix pages.
7. Update the executive summary if new analysis changes the quantified impact, recommendation, risk or decision request.
8. Rerun content-depth, deck-density, evidence, horizontal-logic and rendering QA for all impacted pages.

Examples:

- A market page with one CAGR becomes a historical trend + segment breakdown page, supported by a forecast-methodology appendix.
- An architecture page with five layers gains current-state constraints, target SLAs, design decisions, control points, trade-offs and an implementation-sequence appendix.
- A roadmap with three generic phases gains scoped assets, owners, deliverables, exit criteria, dependencies, target KPIs and critical-path markers.
- A vendor comparison with unsupported scores gains requirements traceability, evidence behind scores, TCO assumptions, risk/lock-in analysis and sensitivity.

## Revision QA routing

| Change type | Required QA rerun |
|---|---|
| Action title / conclusion change | Read-only title test, horizontal logic and evidence-strength check |
| Number or calculation change | Update `evidence.json`, verify formula/input IDs and rerun deck-wide numeric consistency checks |
| Source or definition change | Evidence reconciliation, comparability review and all pages using the fact |
| Page add/delete/reorder | Horizontal logic, coverage map, tracker, page-number and appendix-reference checks |
| Content-depth expansion | Page brief gate, targeted Evidence Research, content-depth QA, deck-density QA, affected executive-summary/appendix checks and rendering QA |
| New appendix page | Core-page reference, source/methodology QA and page-number checks |
| Wording / layout only | Rendering QA for the changed page only, unless wording changes claim strength |

After any revision, affected pages must rerun `scripts/qa_pptx.py --facts <private-draft-dir>/evidence.json` and rendering checks.

## Version discipline

Output file naming:

```text
<deck-name>_v<major>.<minor>.pptx
```

- `minor` increments for local revisions.
- `major` increments for structural storyline changes, material new research, new core pages or renewed confirmation.
- Every version must add one line to `changelog.md`: date, changed pages, reason, evidence impact, density impact and QA performed.
- Client-delivery versions must come from a frozen baseline plus recorded revisions. Do not deliver ad hoc outputs that bypass this loop.

## Evidence relationship

If a revision introduces a new factual, qualitative or numerical claim, that claim must run through Step 4 Evidence Research with both support and counter-evidence checks. New numbers must be registered in `evidence.json` before appearing on slides.

Derived calculations require a formula and input fact IDs. If new evidence weakens the old action title, revise the title rather than hiding the limitation in notes.

## Recommended revision prompt shape

When a user asks for a revision, the agent should respond internally with:

1. Baseline detected or not.
2. Private draft path.
3. Feedback classification: wording, visual, evidence, content depth or structural.
4. Target pages.
5. Dependent pages.
6. Missing page-brief fields.
7. Required evidence and research updates.
8. Core-page split or appendix additions.
9. QA rerun scope.
10. New output version name.