---
name: consulting-deck
description: Generate consulting-style PowerPoint decks with storyline, action titles, exhibit planning, evidence discipline, consulting page patterns, and Chinese-English typography rules.
---

# Consulting Deck Skill

咨询风格 deck 的本质是信息架构纪律与证据链，不是视觉装饰。目标：读者只读标题就能理解完整论证；打开任何一页，10 秒内抓住该页唯一信息；每个判断都能回答「证据是什么」。

## 触发场景

当用户要求「咨询风格 PPT」「consulting deck」「McKinsey style」「麦肯锡风格」「action title」「金字塔原理做 PPT」「storyline」「给客户/高管的汇报 deck」「方案汇报 PPT」「售前 PPT」「workshop 材料」，或任何受众为企业高管/客户的专业商务演示文稿时，触发本技能。

## 强制工作流

```text
Step 1 需求澄清 → Step 2 Storyline → Step 3 Exhibit Plan → Step 4 确认/自动执行 → Step 5 逐页生成 → Step 6 咨询 QA → Step 7 渲染 QA
```

### Step 1 — 需求澄清

已知的不重复问，缺失的必须补齐：受众、场景、语言、页数、是否需要 appendix、风格基准。

### Step 2 — Storyline

先从 `references/deck-archetypes.md` 选择骨架，再产出全部页面 action title。只读标题列表，必须构成完整、连贯、有结论的故事。

### Step 3 — Exhibit Plan

每页必须填写 page brief：

| 字段 | 内容 |
|---|---|
| Key question | 这页回答什么问题 |
| Action title | 这页的结论 |
| Evidence | 用什么数据/事实支撑 |
| Exhibit type | 用哪种图表/版式 |
| Data source | 来源，或标注「团队假设」 |
| Implication | 对受众决策意味着什么 |
| Caveat | 假设与不确定性 |

Evidence 为空且无法标注为合理假设的页面，要么补证据，要么删除。

### Step 4 — 确认 / 自动执行

默认协作模式下，先请用户确认 storyline + exhibit plan。用户要求「一次性生成」「不要反复确认」「直接给我文件」时，进入自动执行模式：继续生成，并将 assumptions 放入 appendix。

### Step 5 — 逐页生成

- 页面骨架调用 `scripts/consulting_layouts.py`。
- 咨询图形调用 `scripts/consulting_shapes.py`。
- TCO/ROI/payback 调用 `scripts/business_case.py`。
- 云/AI/架构/能力地图/operating model 调用 `scripts/architecture_helpers.py`。
- 模板由 `scripts/create_template.py` 生成；示例由 `scripts/demo_generate_deck.py` 生成。

### Step 6 — 咨询 QA

执行 `references/qa-checklist.md`：Pyramid test、Horizontal logic、Vertical logic、So-what、Now-what、Evidence test、Executive skim test、Appendix hygiene、术语与数字一致性。

### Step 7 — 渲染 QA

先运行：

```bash
python scripts/qa_pptx.py <deck.pptx>
```

再执行 PPT 渲染检查：文本溢出、元素重叠、对齐、页码、来源行和字体。

## Action Title 规则

- 完整陈述句，含结论/判断，不是主题短语。
- 错：「云迁移成本分析」。对：「分三波迁移可在 18 个月内将 TCO 降低约 30%」。
- 长度不超过两行。有具体数字时，优先放进标题。
- 标题和主体是「论点—论据」关系。

## Evidence Discipline

1. 所有非显而易见的事实判断必须有来源，或明确标注为「团队假设」。
2. 外部市场数据优先使用公司年报/10-K/IR、政府/监管机构、权威研究机构、Reuters/FT/Bloomberg 等来源。
3. 需要当前数据时必须实际检索，不得凭记忆填数。
4. 来源冲突时，正文采用更权威口径，并在 appendix 或 notes 说明差异。
5. 严禁为完成图表而编造数字；示意数据必须显著标注。
6. 所有估算必须标注 calculation basis。

## 设计 Token

| 用途 | 中文 | 西文/数字 |
|---|---|---|
| 全部文本 | Microsoft YaHei | Arial |

必须同时写入 `<a:latin typeface="Arial"/>` 与 `<a:ea typeface="Microsoft YaHei"/>`。只设置 `font.name` 不够。

字号：action title 18–20pt；正文 10.5–12pt；图表标注 9–10pt；来源 8pt；页码 9pt。

配色：主色 `#1F3864`，强调色 `#C00000`，灰阶 `#333333/#595959/#A6A6A6/#D9D9D9/#F2F2F2`，背景白色。

## 中英混排

详见 `references/terminology.md`。核心：技术原语保留英文，通用商务词中文化；中英文之间、数字与中文之间加半角空格；中文语境使用全角标点。

## 资源索引

| 文件 | 用途 |
|---|---|
| `references/deck-archetypes.md` | deck 骨架 |
| `references/exhibit-planning.md` | page brief |
| `references/page-patterns.md` | 页面模式 |
| `references/it-consulting-patterns.md` | 云/AI/IT 咨询模式 |
| `references/terminology.md` | 中英混排与术语 |
| `references/qa-checklist.md` | 咨询 QA |
| `assets/theme.json` | 设计 token |
| `scripts/consulting_layouts.py` | 页面骨架 |
| `scripts/consulting_shapes.py` | 咨询图形 |
| `scripts/business_case.py` | 商业论证 |
| `scripts/architecture_helpers.py` | 架构/能力图 |
| `scripts/qa_pptx.py` | 自动 QA |
| `scripts/create_template.py` | 生成模板 PPTX |
| `scripts/demo_generate_deck.py` | 生成 demo deck |
