# Revision loop

Use this flow whenever a frozen baseline already exists in `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/baseline/`. Do not regenerate the full deck by default.

## Trigger condition

If the private project draft directory contains a frozen baseline snapshot, any change request enters revision mode. Revision mode applies even when the user asks for a small wording, chart, fact or page-order change.

## Local revision rules

1. Diff against the frozen baseline before editing and state the intended change scope.
2. Modify only the target page brief and target page module unless dependencies require additional updates.
3. List impacted pages before execution. Impacted pages include shared-number pages, executive summary pages, appendix pages, tracker pages and page-number changes.
4. Do not silently propagate changes. Every dependent update must be explicit.
5. When adding, deleting or reordering pages, update `storyline.md`, page numbers, trackers, executive summary references and appendix references.
6. Persist every changed process artifact back to the same private draft path.
7. Do not copy real customer revision state into the public skill repository.

## Revision QA routing

| Change type | Required QA rerun |
|---|---|
| Action title / conclusion change | Read-only title test and horizontal logic |
| Number change | Update `evidence.json` and rerun deck-wide numeric consistency checks |
| Page add/delete/reorder | Horizontal logic, tracker and page-number checks |
| Wording / layout only | Rendering QA for the changed page only |

After any revision, affected pages must rerun `scripts/qa_pptx.py --facts <private-draft-dir>/evidence.json` and rendering checks.

## Version discipline

Output file naming:

```text
<deck-name>_v<major>.<minor>.pptx
```

- `minor` increments for local revisions.
- `major` increments for structural storyline changes or renewed confirmation.
- Every version must add one line to `changelog.md`: date, changed pages, reason, evidence impact and QA performed.
- Client-delivery versions must come from a frozen baseline plus recorded revisions. Do not deliver ad hoc outputs that bypass this loop.

## Evidence relationship

If a revision introduces a new factual or numerical claim, that claim must run through Step 4 Evidence Research with both support and counter-evidence checks. New numbers must be registered in `evidence.json` before appearing on slides.

## Recommended revision prompt shape

When a user asks for a revision, the agent should respond internally with:

1. Baseline detected or not.
2. Private draft path.
3. Target pages.
4. Dependent pages.
5. Required evidence updates.
6. QA rerun scope.
7. New output version name.
