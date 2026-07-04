---
name: consulting-deck
description: Trigger for consulting-style PPT, consulting deck, McKinsey/BCG/Bain-style slides, 麦肯锡风格 PPT, 咨询风格 PPT, action title, storyline, 金字塔原理, executive briefing, sales proposal, pre-sales deck, IT/cloud/AI transformation presentation, workshop material, and client or board-level PowerPoint decks; generate decks with storyline, exhibit planning, evidence research with support and counter-evidence, subagent orchestration, consulting QA, and Chinese-English typography rules.
---

# Consulting Deck Skill

咨询风格 deck 的本质是信息架构纪律与证据链，不是视觉装饰。目标：读者只读标题就能理解完整论证；打开任何一页，10 秒内抓住该页唯一信息；每个判断都能回答「证据是什么」。

## 触发场景

当用户要求「咨询风格 PPT」「consulting deck」「McKinsey style」「麦肯锡风格」「BCG style」「Bain style」「action title」「金字塔原理做 PPT」「storyline」「给客户/高管的汇报 deck」「方案汇报 PPT」「售前 PPT」「workshop 材料」，或任何受众为企业高管/客户的专业商务演示文稿时，触发本技能。

## 强制工作流

```text
Step 1 需求澄清 → Step 2 Storyline → Step 3 Exhibit Plan → Step 4 Evidence Research → Step 5 确认/自动执行 → Step 6 逐页生成 → Step 7 咨询 QA → Step 8 渲染 QA
```

### Step 1 — 需求澄清

已知的不重复问，缺失的必须补齐：受众、场景、语言、页数、是否需要 appendix、风格基准。

### Step 2 — Storyline

先从 `references/deck-archetypes.md` 选择骨架，再产出全部页面 action title。只读标题列表，必须构成完整、连贯、有结论的故事。

硬禁令：不得并行写 storyline。Storyline 必须由单一主 agent 负责，以保证 horizontal logic 和叙事主线一致。

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

### Step 4 — Evidence Research

Evidence Research 是独立强制步骤，不得只作为 Evidence Discipline 的原则存在。必须从全部 page brief 汇总检索任务清单，再回填每页 brief。

每条检索任务必须包含：页码、待验证判断、建议查询词、证据类型、来源优先级、输出格式。

证据类型至少包括：市场数据、竞品、产品能力与价格、监管、财务、客户案例、技术可行性。

#### 双向检索规则

每个关键判断至少执行：

1. 支持性查询：寻找能证明该判断的证据。
2. 反证查询：寻找能推翻、限制或弱化该判断的证据。

处理规则：

- 反证成立：修改 storyline 或 action title，不得硬撑原结论。
- 反证部分成立：写入该页 Caveat、风险页或 speaker notes。
- 反证不成立：在 speaker notes 预置客户 Q&A 应答。

凡 Evidence Research 导致 action title、核心结论、页面顺序或推荐方案变更，进入 Step 5 前必须重新执行只读标题测试，确认 horizontal logic 仍然成立。

#### 回填规则

检索结果必须回填到 page brief：数字、单位、口径、来源、检索日期、caveat。

检索 3 次无果的判断，必须降级为显著标注的「团队假设」，或删除对应页面。

需要当前数据时必须实际检索，不得凭记忆填数。

### Step 5 — 确认 / 自动执行

默认协作模式下，先请用户确认 storyline + exhibit plan + evidence research list。用户要求「一次性生成」「不要反复确认」「直接给我文件」时，进入自动执行模式：继续生成，并将 assumptions、未解决证据项和关键 caveats 放入 appendix 或 speaker notes。

### Step 6 — 逐页生成

- 页面骨架调用 `scripts/consulting_layouts.py`。
- 咨询图形调用 `scripts/consulting_shapes.py`。
- TCO/ROI/payback 调用 `scripts/business_case.py`。
- 云/AI/架构/能力地图/operating model 调用 `scripts/architecture_helpers.py`。
- 模板由 `scripts/create_template.py` 生成；示例由 `scripts/demo_generate_deck.py` 生成。

如使用 subagent 并行生成页面，必须遵守 `references/orchestration.md`：不得多个 agent 并发写同一个 `.pptx`；采用页面模块化装配模式，subagent 只产出 `pages/page_NN.py`，统一签名为 `def render(slide, ctx)`，主 agent 单进程按 storyline 顺序装配。`ctx` 的最小 schema 由 `references/orchestration.md` 定义，页面 worker 不得自行发明新的必填字段。

### Step 7 — 咨询 QA

执行 `references/qa-checklist.md`：Pyramid test、Horizontal logic、Vertical logic、So-what、Now-what、Evidence test、Executive skim test、Appendix hygiene、术语与数字一致性。

并行规则：逐页 vertical logic QA 可并行；horizontal logic 检查与全 deck 数字一致性核对不得并行，必须由主 agent 串行完成。

### Step 8 — 渲染 QA

先运行：

```bash
python scripts/qa_pptx.py <deck.pptx>
```

再执行 PPT 渲染检查：文本溢出、元素重叠、对齐、页码、来源行和字体。渲染切图检查可以按 3–5 页一组并行分派；最终修订必须由主 agent 串行完成。

## Orchestration 规则

详见 `references/orchestration.md`。核心硬规则：

1. 不得并行写 storyline。
2. 不得并发写同一个 `.pptx`。
3. 不推荐分段生成多个 `.pptx` 再合并；默认采用页面模块化装配模式。
4. 有 subagent 时优先并行 Evidence Research、页面模块生成、逐页 vertical QA 和分批渲染检查。
5. 无 subagent 环境下按相同步骤串行执行；任务清单本身是质量工具，并行只是加速手段。

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
7. 每个关键判断必须有支持性查询与反证查询，反证结果必须影响 storyline、caveat 或 Q&A notes。

## 设计 Token

| 用途 | 中文 | 西文/数字 |
|---|---|---|
| 全部文本 | Microsoft YaHei | Arial |

必须同时写入 `<a:latin typeface="Arial"/>` 与 `<a:ea typeface="Microsoft YaHei"/>`。只设置 `font.name` 不够。

字号：action title 18–20pt；正文 10.5–12pt；图表标注 9–10pt；来源 8pt；页码 9pt。

配色：主色 `#1F3864`，强调色 `#C00000`，灰阶 `#333333/#595959/#A6A6A6/#D9D9D9/#F2F2F2`，背景白色。

## 中英混排

详见 `references/terminology.md`。核心：技术原语保留英文，通用商务词中文化；缩写首次出现加中文注释；未列出的通用商务词默认中文化；同一概念全 deck 使用单一表述；中英文之间、数字与中文之间加半角空格；中文语境使用全角标点。

## 资源索引

| 文件 | 用途 |
|---|---|
| `references/deck-archetypes.md` | deck 骨架 |
| `references/exhibit-planning.md` | page brief |
| `references/orchestration.md` | subagent 并行编排与失败降级 |
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
