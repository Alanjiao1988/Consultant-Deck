# Categorical jurisdiction map

Use `scripts/jurisdiction_map` when geography is part of the analytical conclusion and the page classifies a small number of jurisdictions into one well-defined operating model. The helper uses a PowerPoint-compatible PNG primary image plus an Office SVG extension for the landmass, while markers, labels, leader lines and the legend/insight rail remain native editable shapes.

## When to use

Use the map when all of the following are true:

1. Geography materially affects the conclusion or implementation choice.
2. The classification dimension is explicitly named and consistent across all jurisdictions.
3. The core page contains no more than 12 representative markers and no more than 6 categories.
4. Every jurisdiction has a note, one or more evidence IDs and an as-of date.
5. The map is supported by a coverage statement and a detailed appendix table.

Do not use the map for numeric magnitude comparison. Use `benchmark_bar()`, a small-multiple chart or a table when the core question is which jurisdiction has a larger value. Do not use a single-colour categorical map when categories can coexist. Use a jurisdiction-by-dimension heatmap or multi-tag matrix instead.

## Rendering architecture

The supported rendering mode remains:

```text
svg_base_native_overlay
```

The implementation packages two representations in one picture shape:

1. `assets/maps/world_equal_earth.png` is the primary `a:blip` fallback understood by legacy Office clients and non-SVG consumers.
2. `assets/maps/world_equal_earth.svg` is referenced through the Office 2016 `asvg:svgBlip` extension using URI `{96DAC541-7B7A-43D3-8B79-37D633B846F1}`.

Desktop PowerPoint can select the vector representation, while clients that do not understand the extension display the PNG instead of a broken-image placeholder. Markers, leader lines, labels and the insight rail remain editable PowerPoint shapes. Both map assets are derived from Natural Earth public-domain data; see `assets/maps/LICENSE.md`.

Runtime theme recolouring is applied to the SVG text before packaging. The committed PNG fallback deliberately uses the default light-theme land and border colours, so an older client may show the default map colours when a project supplies a custom map theme. This limitation affects only the neutral base layer, not category markers or labels.

LibreOffice rendering proves that a PPTX can be opened and rendered, but it does not prove compatibility with Office's SVG extension. CI therefore also inspects the package and requires a PNG relationship, an SVG relationship, the SVG extension namespace and the extension URI.

This approach replaces low-polygon continent freeforms as the default. A future fully native-editable map may be added only as an explicit option and must not reduce default visual quality.

## Deterministic anchors

`assets/maps/jurisdiction_anchors.json` contains normalized 0–1 anchor positions for common countries, markets, regulatory blocs and approved groups. The registry uses the same Equal Earth projection as the SVG.

The caller normally supplies only a registered jurisdiction ID. Unregistered IDs fail fast. A one-off custom anchor is allowed only when `allow_custom_anchor=True` and the jurisdiction includes both:

```yaml
anchor: {x: 0.52, y: 0.31}
custom_anchor_rationale: Newly created regulatory group used only for this page
```

Custom anchors are recorded in the exhibit manifest and produce a semantic QA warning. Reused anchors should be promoted into the registry.

## Data contract

### Categories

```python
categories = [
    {
        "id": "sector_localization",
        "label": "Sector-specific localization",
        "description": "Government, finance, health or critical infrastructure",
        # optional; otherwise assigned from assets/theme.json
        "color": "#FF7F0E",
    }
]
```

Category IDs must be unique. Every legend category must be used by at least one jurisdiction. The default palette is defined under `map.category_palette` in `assets/theme.json`, not hard-coded in the page script.

### Jurisdictions

```python
jurisdictions = [
    {
        "id": "UAE_SA",
        "label": "UAE / Saudi Arabia",
        "category_id": "sector_localization",
        "note": "Regulated sectors drive local deployment",
        "evidence_ids": ["F103", "F108"],
        "entity_type": "custom_group",
        "members": ["UAE", "SA"],
    }
]
```

Supported `entity_type` values are normally `country_or_market`, `regulatory_bloc` and `custom_group`. A custom group must list its members. Do not group markets merely to save space when their rules or implications differ.

### Page call

```python
manifest = categorical_jurisdiction_map(
    slide,
    jurisdictions,
    categories,
    x=1.2,
    y=3.0,
    w=31.2,
    h=14.5,
    classification_dimension=(
        "Dominant regulatory operating model for enterprise data localization "
        "and cross-border transfer"
    ),
    as_of="2026-07-14",
    caveat=(
        "Validate the current entity, workload, sector and data-type requirements "
        "before implementation."
    ),
    coverage={"reviewed": 24, "shown": 6, "selection_basis": "Representative patterns"},
    insight_annotations=[
        "Localization decisions are workload-specific rather than country-wide defaults",
        "Grouping markets supports triage but does not replace legal review",
    ],
    decision_implication="Prioritize detailed assessments for regulated workloads.",
    page=4,
)
```

A custom SVG may also supply `map_fallback="path/to/matching.png"`. Without it, the default Equal Earth PNG is used as the compatibility fallback.

`classification_dimension`, `as_of` and `caveat` are mandatory. The helper returns a semantic exhibit manifest. Store every returned manifest in the deck sidecar:

```python
write_exhibit_manifest("output/deck.exhibits.json", [manifest])
```

Discarding the returned manifest is a workflow failure even when the PPTX renders correctly.

## Qualitative-exhibit density contract

A jurisdiction map is normally a qualitative analytical exhibit rather than a numeric comparison page. Its page brief must use:

```yaml
content_density_target: qualitative-exhibit
min_registered_numbers: 0
exhibit_manifest: output/deck.exhibits.json
appendix_link: A6
coverage:
  reviewed: 24
  shown: 6
  selection_basis: Representative operating patterns
as_of: 2026-07-14
```

The explicit zero overrides the generic research-heavy three-number floor already supported by `qa_pptx.py`. It does not waive evidence requirements. The page must still:

- show and register the reviewed/shown coverage counts where available;
- state the as-of date and sampling/selection basis;
- register every jurisdiction classification as qualitative evidence;
- use one classification dimension consistently;
- include a visible caveat and decision implication;
- link to an appendix table listing the full reviewed universe, classification, definition and source.

Do not manufacture three numbers from dates, jurisdiction codes or repeated coverage values. If numeric magnitude is the argument, use a quantitative exhibit instead.

## Semantic QA

Run the manifest gate before PPTX QA:

```bash
python scripts/qa_exhibits.py output/deck.exhibits.json \
  --facts <private-draft-dir>/evidence.json \
  --fail-on-warning \
  --json
```

The map QA validates:

- a named classification dimension and ISO as-of date;
- mandatory caveat and coverage statement;
- unique categories and jurisdictions;
- every marker category exists in and is used by the legend;
- every jurisdiction has a note and resolvable evidence IDs;
- custom groups list members;
- anchors are registered or explicitly justified;
- the core page remains within the 6-category / 12-marker limit;
- coverage reviewed is not lower than coverage shown;
- evidence usage agrees with page assignments where supplied.

Semantic QA uses the manifest because a PPTX scanner cannot reliably infer that a marker colour represents a category or evidence record. Shape names also contain `MAP_MARKER`, `MAP_LABEL`, `MAP_LEADER` and `MAP_LEGEND` metadata for geometry and debugging, but the manifest is the source of truth.

## Label placement

The helper starts with the registered preferred direction and tests right, left, top and bottom alternatives. It keeps labels inside the map region and minimizes bounding-box overlap deterministically. Leader lines are native PowerPoint connectors. Dense clusters that still overlap should be split into a regional small multiple or moved to an appendix rather than solved by reducing font size.

## Render and compatibility QA

The demo and CI use LibreOffice plus `pdftoppm` to create a rendered PNG and run `scripts/qa_map_render.py`. The structural render gate checks resolution, non-blank title/map/insight-rail regions, contrast and palette diversity. The package-level pytest separately verifies the PNG primary blip and Office SVG extension.

Before release of a change to picture packaging, open at least one generated deck in current Windows or Mac desktop PowerPoint. LibreOffice cannot validate an Office-specific extension path by itself.

Render smoke QA is not a substitute for an executive visual review. Before delivery, inspect the rendered page for geopolitical neutrality, label clarity, intentional grouping, source/caveat visibility and whether the map actually proves the action title.

## Demo

```bash
python scripts/demo_generate_jurisdiction_map.py
python scripts/qa_exhibits.py examples/demo_regulatory_map.exhibits.json \
  --facts examples/demo_regulatory_map.evidence.json \
  --fail-on-warning
python scripts/qa_map_render.py examples/demo_regulatory_map.pptx
```

The demo evidence is explicitly illustrative and must not be reused as legal or regulatory advice.
