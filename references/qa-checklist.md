# Consulting QA checklist

Use this checklist together with `references/content-density.md`. A visually correct deck can still fail consulting QA if it lacks evidence, comparison, analytical depth or implementation detail.

## Storyline QA

- Horizontal logic: reading only action titles tells a complete story.
- Pyramid test: the deck leads with the answer, then supports it.
- SCQA: context, complication, question and answer are clear.
- Decision test: the requested decision or action is explicit.
- Coverage test: the storyline covers diagnosis, quantified impact, recommendation, implementation, risk and decision.
- Redundancy test: no page exists only because it is common in a consulting template.
- Quantified-title test: analytical titles contain a defensible number/range where available, or have a completed `title_quantification` task and documented rationale.

## Page QA

- One page, one message.
- Action title is a conclusion, not a topic label.
- Evidence on the page supports the title directly.
- So-what and now-what are explicit where needed.
- The page contains a comparison, trend, benchmark, decomposition, scenario or other defined analytical method.
- The page brief contains both a central `quantification` and a concrete `benchmark`.
- Core analytical pages contain at least 2 registered evidence IDs and normally 4–8 in research-heavy mode.
- Research-heavy analytical page bodies expose at least 3 unique registered numeric facts unless explicitly exempt.
- The exhibit includes two to four insight annotations, not only raw numbers.
- A single statistic is not presented without period, definition and comparison context.
- Complex backup analysis is moved to a linked appendix page rather than omitted.
- Conceptual frameworks and architecture diagrams include quantified baselines or targets, design decisions, trade-offs and dependencies.
- Roadmaps include owners, deliverables, decision gates, measurable exit criteria, critical dependencies and quantified wave scope.
- Strong qualitative statements such as `显著提升` or `rapidly growing` include a number, range, threshold or visible evidence basis.
- A categorical jurisdiction map names one classification dimension, shows reviewed/displayed coverage and as-of date, uses no more than 12 markers and 6 categories, and links to an appendix table.
- A map is not used as a decorative substitute for a benchmark bar, small multiple, heatmap or detailed jurisdiction matrix.

## Quantification test

For every non-exempt analytical page, ask three mandatory questions:

1. **Number:** Is the conclusion supported by visible, registered numeric facts or calculations?
2. **Benchmark:** Is the number compared with history, peers, a scenario, a threshold or a target using a consistent definition?
3. **Definition and source:** Are the unit, period, entity, calculation basis and source traceable?

If any answer is `no`, return the page to Step 4 Evidence Research. Do not repair the page by adding unsupported numbers, generic prose or smaller text.

Also verify:

- baseline, target and gap reconcile where applicable;
- time series contains enough comparable periods to establish direction;
- peer or scenario comparisons use the same definition;
- derived metrics identify formulas and input evidence IDs;
- chart labels, table values and evidence.json agree;
- a non-numeric title has a justified rationale after reasonable searches.

## Content-depth QA

For each core page, answer yes or no:

1. Does the page contain the specific facts promised in the page brief?
2. Is there enough evidence to challenge the conclusion rather than merely illustrate it?
3. Is there at least one meaningful comparison basis and concrete benchmark?
4. Are calculations reproducible from the stated inputs?
5. Does the page explain why the finding matters?
6. Does it identify a decision, action or implication?
7. Is the main caveat visible or available in the notes/appendix?
8. Would removing the page weaken the decision logic?

Any core page with two or more `no` answers must be revised or removed. A failed Quantification test is independently sufficient to return the page to Step 4.

## Deck-level density QA

For a typical 10-page core deck in research-heavy mode, verify that the deck contains approximately:

- 25–50 non-duplicative facts or calculations in `evidence.json`;
- 8–15 distinct, relevant sources;
- at least 5 data-bearing analytical exhibits;
- at least 3 appendix pages covering source detail, methodology, sensitivities or backup analysis;
- one primary source for each major conclusion when available;
- two independent source families for high-impact market, financial or regulatory claims;
- no more than approximately 25% explicitly requested conceptual-framework pages.

These are quality floors, not reasons to split facts artificially. If the topic genuinely has less evidence, record the limitation and weaken the conclusions.

## Evidence QA

- Every non-obvious factual claim is sourced or explicitly marked as an assumption.
- Estimates include calculation basis and formula.
- Demonstration data is visibly labelled as illustrative.
- Units, time periods, currencies and definitions are consistent.
- Major conclusions have both support and counter-evidence research.
- Source hierarchy favors primary and authoritative sources.
- Retrieval dates are recorded for current or changeable information.
- Management claims are distinguished from independently verified evidence.
- Derived metrics can be traced to registered source facts.
- Evidence IDs used on slides exist in `evidence.json` and are assigned to the correct pages.
- Data-density requirements never justify fabrication or unsupported extrapolation.
- Every jurisdiction classification has its own evidence coverage; a source for one group member is not silently generalized to the whole group.

## Executive summary QA

- The executive summary synthesizes 3–5 conclusions rather than repeating section names.
- Each conclusion links to supporting pages and evidence IDs.
- Expected impact is quantified.
- The decision required is explicit.
- The primary risk or success condition is visible.
- The recommendation is consistent with the detailed analysis and scenarios.

## Appendix QA

- Every appendix page has a clear purpose and source line.
- Core pages reference appendix backup where needed.
- Full peer tables, formulas, assumptions and sensitivity outputs are retained.
- Counter-evidence and rejected alternatives are not silently discarded.
- Appendix content is readable at approved font sizes.
- The appendix does not contain unexplained raw-data dumps.
- Map appendix tables retain jurisdiction, entity type, members, category, note, evidence IDs, as-of date, source and caveat.

## Visual QA

- Fonts include both Arial and Microsoft YaHei in XML.
- Layout stays within margins; automated QA uses conservative text-overflow and independent-textbox-overlap heuristics.
- Exact alignment, page-number continuity and complex intentional layering still require rendered-image or manual review.
- Palette uses approved theme tokens; categorical maps may use the bounded `map.category_palette` in `assets/theme.json`.
- Charts are PowerPoint-native when possible.
- Categorical maps use a vector SVG base plus native PowerPoint markers, labels, leader lines and insight rail; low-polygon continent shapes are not the default.
- Source line and page number are present where required.
- No font is reduced below the approved minimum to force excess content onto a page.
- Dense analysis uses tables, chart-plus-table combinations, benchmark bars, driver trees, small multiples, annotated charts, bridges and insight rails rather than paragraphs.
- If a page is unreadable, split it into two pages instead of shrinking text.
- Rendered map review confirms recognizable geography, readable labels, no material collisions, neutral political treatment and a visible caveat.

## Automated QA

Run page-brief and evidence-budget QA before production:

```bash
python scripts/qa_briefs.py <private-draft-dir>/briefs.yaml \
  --facts <private-draft-dir>/evidence.json \
  --json
```

Resolve all errors before freezing the baseline. Review warnings explicitly; research-heavy evidence-budget and appendix-depth warnings should normally be fixed rather than ignored.

For data-driven exhibits such as categorical jurisdiction maps, also run semantic manifest QA:

```bash
python scripts/qa_exhibits.py <output>/deck.exhibits.json \
  --facts <private-draft-dir>/evidence.json \
  --fail-on-warning \
  --json
```

This validates classification dimensions, legend/category consistency, jurisdiction notes, anchor registration, group membership, coverage, caveats, dates and evidence references. The manifest is the source of truth because a PPTX scanner cannot reliably infer business meaning from marker colours.

After PPTX generation, run:

```bash
python scripts/qa_pptx.py path/to/deck.pptx \
  --facts path/to/evidence.json \
  --briefs path/to/briefs.yaml
```

For map pages, run the render smoke check and inspect the generated PNG:

```bash
python scripts/qa_map_render.py path/to/deck.pptx --json
```

`qa_pptx.py` checks registered-number density, unsupported strong qualitative claims, fact consistency, source-line signals, terminology, fonts and bounds. `qa_exhibits.py` checks semantic exhibit contracts. `qa_map_render.py` catches blank SVG output, gross clipping and structural render failures. Warnings should be reviewed manually; errors should be fixed before delivery. Automated QA does not replace source validation, calculation review, geopolitical review or executive skim testing.
