# Consulting QA checklist

Use this checklist together with `references/content-density.md`. A visually correct deck can still fail consulting QA if it lacks evidence, comparison, analytical depth or implementation detail.

## Storyline QA

- Horizontal logic: reading only action titles tells a complete story.
- Pyramid test: the deck leads with the answer, then supports it.
- SCQA: context, complication, question and answer are clear.
- Decision test: the requested decision or action is explicit.
- Coverage test: the storyline covers diagnosis, quantified impact, recommendation, implementation, risk and decision.
- Redundancy test: no page exists only because it is common in a consulting template.

## Page QA

- One page, one message.
- Action title is a conclusion, not a topic label.
- Evidence on the page supports the title directly.
- So-what and now-what are explicit where needed.
- The page contains a comparison, trend, benchmark, decomposition, scenario or other defined analytical method.
- Core analytical pages contain at least 2 registered evidence IDs and normally 4–8 in research-heavy mode.
- The exhibit includes two to four insight annotations, not only raw numbers.
- A single statistic is not presented without period, definition and comparison context.
- Complex backup analysis is moved to a linked appendix page rather than omitted.
- Conceptual frameworks and architecture diagrams include quantified baselines or targets, design decisions, trade-offs and dependencies.
- Roadmaps include owners, deliverables, decision gates, measurable exit criteria and critical dependencies.

## Content-depth QA

For each core page, answer yes or no:

1. Does the page contain the specific facts promised in the page brief?
2. Is there enough evidence to challenge the conclusion rather than merely illustrate it?
3. Is there at least one meaningful comparison basis?
4. Are calculations reproducible from the stated inputs?
5. Does the page explain why the finding matters?
6. Does it identify a decision, action or implication?
7. Is the main caveat visible or available in the notes/appendix?
8. Would removing the page weaken the decision logic?

Any core page with two or more `no` answers must be revised or removed.

## Deck-level density QA

For a typical 10-page core deck in research-heavy mode, verify that the deck contains approximately:

- 25–50 non-duplicative facts or calculations in `evidence.json`;
- 8–15 distinct, relevant sources;
- at least 5 data-bearing analytical exhibits;
- at least 3 appendix pages covering source detail, methodology, sensitivities or backup analysis;
- one primary source for each major conclusion when available;
- two independent source families for high-impact market, financial or regulatory claims.

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

## Visual QA

- Fonts include both Arial and Microsoft YaHei in XML.
- Layout stays within margins and no text boxes overlap.
- Palette uses primary, accent and gray scale only.
- Charts are PowerPoint-native when possible.
- Source line and page number are present where required.
- No font is reduced below the approved minimum to force excess content onto a page.
- Dense analysis uses small multiples, summary tables, annotated charts, bridges and insight rails rather than paragraphs.
- If a page is unreadable, split it into two pages instead of shrinking text.

## Automated QA

Run:

```bash
python scripts/qa_pptx.py path/to/deck.pptx --facts path/to/evidence.json
```

Warnings should be reviewed manually; errors should be fixed before delivery. Automated QA does not replace content-depth review, source validation or executive skim testing.