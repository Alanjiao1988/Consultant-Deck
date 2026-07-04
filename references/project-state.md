# Project state layer

Every deck project must persist intermediate state to disk. Do not keep storyline, briefs, evidence or assumptions only in the conversation history.

## Work directory structure

Create one independent project directory at the start of deck generation:

```text
<project>/
  storyline.md        # Ordered action titles, with page pattern / exhibit markers
  briefs.yaml         # All page briefs with the seven required fields
  evidence.json       # Fact table used by the deck
  pages/              # page_NN.py modules for page-module assembly mode
  output/             # Versioned PPTX outputs
  assumptions.md      # Team assumptions used for automatic execution or unresolved evidence
  changelog.md        # Version history and revision notes
  baseline/           # Frozen baseline snapshot after Step 5 confirmation
```

## Persist timing

| Workflow point | Required state action |
|---|---|
| Step 2 Storyline complete | Write `storyline.md` |
| Step 3 Exhibit Plan complete | Write `briefs.yaml` |
| Step 4 Evidence Research complete | Write or update `evidence.json` and `assumptions.md` |
| Step 5 confirmation / automatic execution gate | Freeze a baseline snapshot, preferably via git commit or by copying current state into `baseline/` |
| Step 6 page generation | Write page modules into `pages/page_NN.py`; write generated PPTX into `output/` |
| Step 7 / Step 8 QA complete | Record QA result and relevant notes in `changelog.md` or delivery notes |

## Freeze semantics

A brief is considered frozen only when a baseline snapshot exists. In page-module assembly mode, subagents may read the frozen baseline but must not mutate it. Any change after baseline freeze must go through `references/revision-loop.md`.

## Evidence fact table schema

`evidence.json` is the fact table. Every number that enters the deck should be registered as a fact before it appears on a slide.

```json
{
  "facts": [
    {
      "id": "F001",
      "claim": "判断原文",
      "value": 30,
      "unit": "%",
      "definition": "口径说明",
      "source_type": "client | external | assumption",
      "source": "来源描述或文件名",
      "retrieved": "2026-07-05",
      "counter_evidence": "反证检索结论",
      "used_on_pages": [2, 5, 12]
    }
  ]
}
```

## Fact table rules

1. All numeric claims that enter the deck should be registered in `evidence.json` before page generation.
2. `source_type=assumption` numbers must be visibly labelled as team assumptions on the page or in the source line.
3. `used_on_pages` should be maintained by the assembler or by the main agent during page generation.
4. Customer or internal challenges to any number must be answerable from `evidence.json` alone: value, unit, definition, source and retrieval date.
5. If a number cannot be parsed or matched reliably, downgrade the automated check to warning rather than blocking delivery with a false error.

## Audit requirement

`evidence.json` must independently answer five questions for every material number:

1. What is the value?
2. What is the unit?
3. What is the definition / calculation basis?
4. What is the source?
5. What was the retrieval date?
