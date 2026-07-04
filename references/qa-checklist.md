# Consulting QA checklist

## Storyline QA

- Horizontal logic: reading only action titles tells a complete story.
- Pyramid test: the deck leads with the answer, then supports it.
- SCQA: context, complication, question and answer are clear.
- Decision test: the requested decision or action is explicit.

## Page QA

- One page, one message.
- Action title is a conclusion, not a topic label.
- Evidence on the page supports the title directly.
- So-what and now-what are explicit where needed.
- Complex backup analysis is moved to appendix.

## Evidence QA

- Every non-obvious factual claim is sourced or explicitly marked as an assumption.
- Estimates include calculation basis.
- Demonstration data is visibly labelled as illustrative.
- Units, time periods and currency are consistent.

## Visual QA

- Fonts include both Arial and Microsoft YaHei in XML.
- Layout stays within margins and no text boxes overlap.
- Palette uses primary, accent and gray scale only.
- Charts are PowerPoint-native when possible.
- Source line and page number are present where required.

## Automated QA

Run:

```bash
python scripts/qa_pptx.py path/to/deck.pptx
```

Warnings should be reviewed manually; errors should be fixed before delivery.
