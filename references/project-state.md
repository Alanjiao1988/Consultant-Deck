# Project state layer

Every deck project must persist intermediate state, but real client project state must not be written to a public skill repository. Keep this skill repository distributable; store project state in a separate private project-state repository, an enterprise-internal repository, or a local encrypted workspace when GitHub storage is unavailable.

## Security rule

Customer-identifiable information must never be written to public storage. This includes customer names, internal numbers, project code names, workshop notes, non-public architecture details, source documents, draft storylines and `evidence.json` facts.

When using GitHub for process persistence, the target must be a private repository or enterprise-internal repository with appropriate access controls. Do not use this public skill repo for real project drafts.

## Work directory structure

At the start of deck generation, create one independent project directory under a private state root:

```text
<private-state-root>/
  deck-drafts/
    <YYYY-MM-DD>/
      <deck-title-slug>/
        storyline.md        # Ordered action titles, coverage map and core/appendix plan
        briefs.yaml         # Page briefs with analytical content budgets
        evidence.json       # Fact and calculation table used by the deck
        research-log.md     # Queries, source decisions, rejected evidence and open gaps
        pages/              # page_NN.py modules for page-module assembly mode
        output/             # Versioned PPTX outputs or delivery references
        assumptions.md      # Team assumptions used for automatic execution or unresolved evidence
        changelog.md        # Version history and revision notes
        baseline/           # Frozen baseline snapshot after Step 5 confirmation
```

Directory naming rules:

- Use the request date in `YYYY-MM-DD` format.
- Use a concise, filesystem-safe deck title slug, for example `bank-ai-transformation-roadmap`.
- Use `deck-drafts` rather than a path with spaces so shell scripts and CI do not require special quoting.
- Keep all process artifacts for the same deck inside this private directory to avoid local resource sprawl and to make the work auditable.
- Generated binary PPTX files may be stored as versioned outputs if repository policy allows; otherwise store a delivery reference and keep all process state in the draft directory.

## Persist timing

| Workflow point | Required state action |
|---|---|
| Project start | Create `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/` |
| Step 2 Storyline complete | Write `storyline.md` including coverage map and appendix plan |
| Step 3 Exhibit Plan complete | Write `briefs.yaml` with content-density fields |
| Step 4 Evidence Research in progress | Maintain `research-log.md`, `evidence.json` and `assumptions.md` |
| Step 4 Evidence Research complete | Resolve or visibly classify all evidence gaps |
| Step 5 confirmation / automatic execution gate | Freeze a baseline snapshot, preferably via git commit in the private state repo or by copying current state into `baseline/` |
| Step 6 page generation | Write page modules into `pages/page_NN.py`; write generated PPTX or delivery reference into `output/` |
| Step 7 / Step 8 QA complete | Record QA result, density checks and relevant notes in `changelog.md` or delivery notes |

## Freeze semantics

A brief is considered frozen only when a baseline snapshot exists in the private draft directory. In page-module assembly mode, subagents may read the frozen baseline but must not mutate it. Any change after baseline freeze must go through `references/revision-loop.md`.

## Evidence fact table schema

`evidence.json` is the analytical fact table. Every material number, sourced qualitative assertion and derived calculation that enters the deck should be registered before it appears on a slide.

```json
{
  "facts": [
    {
      "id": "F001",
      "claim": "判断原文",
      "value": 30,
      "unit": "%",
      "period": "FY2025",
      "comparison_period": "FY2024",
      "entity": "Company or segment",
      "definition": "口径说明，包括 included / excluded scope",
      "source_type": "client | filing | regulator | official_doc | research | media | assumption",
      "source_tier": 1,
      "source": "来源描述、文件名或 canonical citation",
      "source_date": "2026-06-30",
      "retrieved": "2026-07-05",
      "page_or_section": "p. 42 / Note 7",
      "calculation_basis": null,
      "input_fact_ids": [],
      "counter_evidence": "反证检索结论",
      "caveat": "限制、定义差异或可比性问题",
      "confidence": "high | medium | low",
      "used_on_pages": [2, 5, 12]
    }
  ],
  "calculations": [
    {
      "id": "C001",
      "claim": "FY2022–FY2025 revenue CAGR",
      "value": 12.4,
      "unit": "%",
      "period": "FY2022–FY2025",
      "definition": "Compound annual growth rate",
      "formula": "(F014 / F011)^(1/3) - 1",
      "input_fact_ids": ["F011", "F014"],
      "calculation_basis": "Unrounded source values; constant reporting currency",
      "caveat": "Acquisition contribution not separated",
      "confidence": "high",
      "used_on_pages": [4]
    }
  ]
}
```

## Fact table rules

1. All material numeric claims that enter the deck should be registered in `evidence.json` before page generation.
2. Important qualitative claims such as regulatory requirements, product limitations, management commitments and customer-case outcomes should also be registered when they materially support a conclusion.
3. `source_type=assumption` numbers must be visibly labelled as team assumptions on the page or in the source line.
4. `source_tier` should follow the hierarchy in `references/content-density.md`: tier 1 primary/official, tier 2 institutional, tier 3 reputable research/data, tier 4 high-quality media, tier 5 secondary/vendor commentary.
5. `period`, `entity` and `definition` are required whenever the same metric could have multiple interpretations.
6. Derived metrics belong in `calculations`, with formula and `input_fact_ids`; do not cite a derived number as if it came directly from a source.
7. `used_on_pages` should be maintained by the assembler or by the main agent during page generation.
8. Customer or internal challenges to any number must be answerable from `evidence.json` alone: value, unit, period, entity, definition, source, calculation basis, caveat and retrieval date.
9. If a number cannot be parsed or matched reliably, downgrade the automated check to warning rather than blocking delivery with a false error.
10. Do not duplicate the same fact under multiple IDs simply to satisfy a content count.

## Evidence-set quality

For every major conclusion, the evidence set should record:

- at least one supporting item;
- at least one counter-evidence or limiting item;
- a primary source when one exists;
- an independent source family for high-impact market, financial or regulatory claims;
- definition and comparability caveats;
- confidence level.

The page brief should reference evidence IDs rather than free-text source descriptions wherever possible.

## Audit requirement

`evidence.json` must independently answer these questions for every material fact or calculation:

1. What is the value or assertion?
2. What is the unit, period, entity and definition?
3. Is it sourced or derived?
4. What is the source and source tier?
5. What was the source date and retrieval date?
6. What formula and input facts produced a derived value?
7. What counter-evidence or caveat limits the conclusion?
8. What is the confidence level?
9. Which pages use it?

## Research log

`research-log.md` should capture:

- page and claim being researched;
- support query and counter-evidence query;
- sources reviewed;
- source selected and why;
- sources rejected and why;
- unresolved definition conflicts;
- remaining evidence gaps;
- resulting changes to storyline, action title or caveat.

The research log should not be pasted into the deck, but it makes the evidence trail reproducible and prevents later agents from repeating low-value searches.

## Storage discipline

- Real process files belong under a private project-state root, not in this public skill repository.
- Subagents must write or return content for paths under the private draft directory.
- The main agent owns baseline freezes and final output versioning.
- Avoid excessive binary churn. Prefer storing process text artifacts and versioned final outputs; if large binaries are not desired in the private state repo, store a delivery reference in `output/README.md`.
- If only public storage is available, do not persist customer-identifiable project state there. Ask for a private target or use local encrypted storage instead.