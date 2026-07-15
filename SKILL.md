---
name: consulting-deck
description: Trigger for consulting-style PPT, consulting deck, McKinsey/BCG/Bain-style slides, 麦肯锡风格 PPT, 咨询风格 PPT, action title, storyline, 金字塔原理, executive briefing, sales proposal, pre-sales deck, IT/cloud/AI transformation presentation, workshop material, investment analysis and client or board-level PowerPoint decks; generate research-heavy, data-rich decks with storyline, exhibit planning, quantified evidence research, hard data-density gates, private project state, fact-table QA, semantic exhibit manifests, subagent orchestration, revision loop, appendix depth and Chinese-English typography rules.
---

# Consulting Deck Skill

咨询风格 deck 的本质是信息架构纪律、量化分析与证据链，不是视觉装饰。目标：读者只读标题就能理解完整论证；打开任何一页，10 秒内抓住唯一信息；继续阅读 1–2 分钟后，能够看到足够的数据、比较、计算、边界条件和实施细节来检验结论。

默认目标不是“概念正确的简报”，而是“研究驱动、数据密集、可以经受高管追问的咨询交付物”。除非用户明确要求极简 executive brief，否则策略、市场、投资、厂商评估、售前、云、AI 和转型类 deck 默认采用 research-heavy consulting mode。

## 触发场景

当用户要求「咨询风格 PPT」「consulting deck」「McKinsey style」「麦肯锡风格」「BCG style」「Bain style」「action title」「金字塔原理做 PPT」「storyline」「给客户/高管的汇报 deck」「方案汇报 PPT」「售前 PPT」「workshop 材料」「投资分析 PPT」，或受众为企业高管/客户的专业商务演示文稿时，触发本技能。

## 数据安全红线

真实客户项目状态不得写入公开可访问的存储，包括当前 public skill repo。客户名称、内部数字、项目代号、非公开架构、storyline、briefs、evidence.json、exhibit manifest、research-log 和 assumptions 必须存放在独立 private project-state repo、企业内部 repo，或本地加密工作区。

## 默认内容模式

使用 `references/content-density.md` 定义内容密度。

| 模式 | 适用场景 | 核心页 | Appendix | 分析页证据预期 |
|---|---|---:|---:|---|
| Executive brief | 用户明确要求极简、高管速览 | 6–10 | 3–8 | 每页 2–4 条证据，body 通常至少 1 个登记数字 |
| Standard consulting | 时间或数据受限 | 10–18 | 4–10 | 每页 3–5 条证据，body 通常至少 2 个登记数字 |
| Research-heavy consulting | 默认 | 12–25 | 6–20 | 每页 4–8 条证据，body 通常至少 3 个登记数字，并有 benchmark |
| Qualitative exhibit | 地图、监管分类等以可审计定性分类为主的页面 | 不单独决定页数 | 必须有明细备份 | coverage + as-of + 分类证据 + manifest；不得伪造数字凑密度 |

页数不是目标。证据与分析需要独立展开时增加页面；不能支持决策的页面删除。

## Data Density 硬规则

1. Research-heavy 核心分析页的 body 通常至少出现 3 个**已登记入 `evidence.json` 的独立数字或计算**，正常目标为 3–5 个或更多。
2. 标题中的数字不单独满足 body 密度；主体图表、表格或注释必须展示证据。
3. Cover、section divider、navigation 和用户明确要求的 conceptual framework 可豁免。
4. 以 `categorical_jurisdiction_map` 等定性分类为核心的页面可使用 `content_density_target: qualitative-exhibit`，但必须同时设置 `min_registered_numbers: 0`，并展示、登记 coverage reviewed/shown，记录 `as_of`、`selection_basis`、每个分类的 evidence IDs、`exhibit_manifest` 和 `appendix_link`。这是替代性证据合同，不是无证据豁免。
5. Qualitative-exhibit 页不得为了满足 research-heavy 的 3 数字门槛，把生效日期、辖区编号或重复 coverage 拆成伪数字；详细辖区表、定义和来源必须进入 appendix。
6. 明确豁免的纯框架页通常不得超过 eligible pages 的 25%；项目可以在 20%–30% 范围内调整，但必须记录理由。
7. 一个数字重复展示不增加计数；不得拆分、复制 evidence IDs 来凑数。
8. 密度不足的正确处理是回到 Step 4 补检索、弱化结论、拆页或删除页面。
9. **严禁为了达到密度门槛而编造数字、伪造精度或进行无依据外推。** 数据密度永远服从 Evidence Discipline。
10. `显著提升`、`大幅降低`、`快速增长`、`领先`、`significantly`、`rapidly`、`materially` 等强定性词，正文中必须在同一陈述里带数字、区间、阈值或明确证据基础，否则 QA warning。

## 强制工作流

```text
Step 1 需求与深度确认
  → Step 2 Storyline 与 coverage map
  → Step 3 Exhibit Plan、Quantification 与 content budget
  → Step 4 Evidence Research
  → Step 5 确认/自动执行与 brief QA
  → Step 6 逐页生成 + exhibit manifest 落盘
  → Step 7 咨询、量化与内容深度 QA
  → Step 8 Semantic exhibit QA + PPTX/render QA
```

### Step 1 — 需求与深度确认

已知的不重复问，缺失的必须补齐：受众、场景、语言、页数、是否需要 appendix、风格基准、交付时点、可用内部数据、是否允许外部研究。

除非用户明确要求精简，设定 `content_density_target: research-heavy`。用户给定较少页数但要求详实时，优先增加 appendix，而不是把分析压缩成概念页。

落盘：建立 `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/`。

### Step 2 — Storyline 与 coverage map

从 `references/deck-archetypes.md` 选择骨架，再产出全部 action titles。只读标题列表必须构成完整、连贯、有结论的故事。

Coverage map 至少覆盖：

- 事实基础与趋势；
- 问题/机会的量化；
- 根因或价值驱动；
- 备选方案与取舍；
- 推荐方案；
- 财务或运营影响；
- 实施路径、资源与治理；
- 风险、反证与成功条件；
- 决策请求；
- appendix 备份。

不得并行写 storyline。由单一主 agent 保证 horizontal logic。写入 `storyline.md`。

### Step 3 — Exhibit Plan、Quantification 与 content budget

每页必须填写 page brief，字段见 `references/exhibit-planning.md`。非豁免分析页至少包含：

| 字段 | 内容 |
|---|---|
| Page role | 核心论证、支持分析、建议、决策或 appendix |
| Key question | 这页回答什么问题 |
| Action title | 证据化结论 |
| Title quantification | 标题中的量化锚点、待检索任务或无数字标题理由 |
| Evidence IDs | 将使用的事实与计算 ID |
| Required data points | 页面必须出现的数字、事实或定义 |
| Quantification | 基线、目标、差距、区间、阈值或拆解 |
| Comparison basis | 历史、同业、分部、地区、情景等比较方法 |
| Benchmark | 具体对标对象、数值/范围/阈值及来源 |
| Analysis method | 趋势、桥接、拆解、评分、敏感性、场景或综合 |
| Primary exhibit | 证明标题的主要图表/表格 |
| Insight annotations | 2–4 条直接标注的洞察 |
| Decision implication | 对受众决策意味着什么 |
| Data source | 来源、检索日期、计算基础或团队假设 |
| Caveat | 假设、不确定性和反证 |
| Appendix link | 方法、明细或备份所在页 |
| Density target | executive、standard、research-heavy 或 qualitative-exhibit |
| Exhibit manifest | 数据驱动 exhibit 的 sidecar manifest 路径；非数据驱动页可为空 |
| Unresolved gaps | 待检索、假设或删除的证据缺口 |

`Comparison basis` 是比较方法；`Benchmark` 是具体对象和数值。只写“peer comparison”而没有 peer/median/value 不合格。

Action title 没有数字、区间或阈值时，必须生成 `title_quantification` 检索任务。合理检索 3 次无果后，才可记录 `justified_non_numeric`，并保留检索日志和限制。不得为了标题好看硬塞误导性数字。

写入 `briefs.yaml`。

### Step 4 — Evidence Research

Evidence Research 是独立强制步骤。必须从全部 page briefs 汇总检索任务，再回填每页。

每条任务包含：页码/cluster、claim、required data points、quantification、comparison basis、benchmark、support query、counter query、证据类型、来源优先级和输出格式。

每个关键判断至少执行支持性查询和反证查询。反证成立时修改 storyline/title；部分成立时写入 caveat、风险或 notes；不能忽略反证。

#### 量化任务最低产出

除非页面结构有明确例外，每个量化研究任务通常至少返回：

1. 核心当前指标或结论值；
2. 至少 2–3 个同口径时间点，用于趋势或增长计算；
3. 1–2 个同口径可比对象、场景或阈值；
4. 每个数字的单位、期间、entity、定义和来源；
5. 派生指标的公式和 input evidence IDs；
6. 至少一个反证、限制或 comparability caveat。

只带回一个孤立数字，在可合理获得趋势或 comparables 时视为未完成。如果来源只能支持一个数字，必须记录失败的比较检索和限制，不能自行编造上下文。

#### 来源优先级

1. 公司年报/10-K/20-F/财报材料、官方产品文档、政府和监管机构；
2. 国际组织、标准机构和权威行业协会；
3. 可靠数据商、研究机构和学术来源；
4. Reuters、FT、Bloomberg 等高质量媒体；
5. 厂商博客、专业媒体与二手总结，仅作补充并标注 caveat。

重大市场、财务或监管结论，在可获得时至少包含一个 primary source，并使用两个独立来源族交叉验证。管理层陈述必须与独立证据区分。

所有进入 deck 的数字先登记到 `evidence.json`。派生指标登记公式和 input evidence IDs。查询、拒绝来源、定义冲突和 storyline 影响写入 `research-log.md`。

典型 10 页核心 research-heavy deck 的默认底线：

- 25–50 个不重复事实或计算；
- 8–15 个相关、高质量独立来源；
- 至少 5 个数据型 primary exhibits；
- 至少 3 页 appendix。

不得拆分同一事实凑数。主题缺乏数据时，记录限制并弱化结论。

### Step 5 — 确认 / 自动执行与 brief QA

默认协作模式先确认 storyline、exhibit plan 和 research findings。用户要求一次性执行时继续，但 assumptions、未解决证据和 caveats 必须进入 appendix 或 notes。

冻结 baseline 前运行：

```bash
python scripts/qa_briefs.py <private-draft-dir>/briefs.yaml \
  --facts <private-draft-dir>/evidence.json \
  --json
```

必须解决 errors。Research-heavy 模式下 evidence budget、appendix depth、framework share 等 warnings 通常也应修复。Qualitative-exhibit page brief 必须显式写入 `min_registered_numbers: 0`、coverage/as-of/selection basis、manifest 路径和 appendix link；不得依赖运行时猜测。

确认门检查：

- 每个核心页有 quantification 和 concrete benchmark；
- 非数字标题有完成的 title quantification 或合理说明；
- 每个重大结论有支持与反证处理；
- deck 包含量化影响、实施细节、风险条件与决策请求；
- appendix 已规划；
- 数据驱动 exhibit 已规划 manifest 输出；
- 没有仅因“咨询 PPT 通常有这一页”而存在的页面。

通过后冻结 `baseline/`。

### Step 6 — 逐页生成与 manifest 落盘

- 页面骨架：`scripts/consulting_layouts.py`；
- 通用图形与数据 exhibit：`scripts/consulting_shapes.py`；
- 定性地理分类：`scripts/jurisdiction_map`；
- TCO/ROI/payback：`scripts/business_case.py`；
- 云/AI/架构：`scripts/architecture_helpers.py`。

优先使用：

- `dense_table()`：详细业务数据表；
- `benchmark_bar()`：同业/阈值横向对标；
- `driver_tree()`：收入、价值、TCO 等量化拆解；
- `native_chart()` 的 `bar_h`、`area_stacked`、`combo`；
- `cagr_annotation()`：自动计算 CAGR；
- `chart_with_data_table()`：图形趋势 + 精确值；
- `categorical_jurisdiction_map()`：单一分类维度、少量代表性辖区的定性地理页。

页面生成硬规则：

1. 主体用 primary exhibit 证明 action title。
2. 核心页至少引用 2 个 evidence IDs；research-heavy 通常 4–8 个。
3. Research-heavy body 通常至少展示 3 个独立登记数字；qualitative-exhibit 按本文件的替代性证据合同执行。
4. 每页至少有趋势、同业、分部、情景、benchmark、桥接、拆解或有定义的定性分类之一。
5. 图表有 2–4 个 insight annotations。
6. 页面明确 implication/now-what，并链接 appendix。
7. 禁止只有图标、箭头、五框模型、未量化成熟度或空泛“现状—目标—路径”的装饰页。
8. 架构页包含基线/约束、3–5 个设计决策、2–4 个量化目标、控制点、取舍与依赖。
9. 路线图包含 deliverables、owners、exit criteria、decision gates、dependencies、target KPIs、critical path 和每 wave 的 scope/budget/benefit 数字。
10. 商业论证包含完整假设、成本收益、base/upside/downside、敏感性和收益责任。
11. 风险页包含概率、影响、trigger、owner 和 residual risk。
12. 信息过多时拆页或进 appendix，不得缩小字号硬塞。
13. 任何返回结构化语义数据的 exhibit helper 都必须将返回值交给主 assembler；assembler 必须汇总并写入 `<private-draft-dir>/output/<deck-name>.exhibits.json`，同时把路径写入相关 page brief 的 `exhibit_manifest`。不得只生成 PPTX 而丢弃 manifest。

有 subagent 时只并行生成 `pages/page_NN.py`，统一 `def render(slide, ctx)`；不得并发写同一 `.pptx`。主 agent 单进程装配、汇总 manifest 并写盘。

### Step 7 — 咨询、量化与内容深度 QA

执行 `references/qa-checklist.md`。

Quantification test 对每个非豁免分析页问：

1. 判断是否有可见、已登记数字支撑，或是否满足批准的 qualitative-exhibit 证据合同？
2. 数字或分类是否有历史、同业、情景、目标、阈值、coverage universe 或一致的分类维度对标？
3. 数字/分类的单位、期间、entity、口径、公式、来源和 retrieval date 是否可追踪？

任一为“否”，退回 Step 4。不得通过增加泛泛文字或无依据数字修补。

逐页还要确认：promised data points、计算可复现性、分类一致性、why it matters、decision implication、caveat、appendix link 和页面必要性。

逐页 vertical/quantification QA 可并行；horizontal logic、coverage map、全 deck 数字一致性、manifest 汇总和 executive summary 综合必须由主 agent 串行完成。

### Step 8 — Semantic exhibit、PPTX 与渲染 QA

存在数据驱动 exhibit manifest 时，先运行语义 QA：

```bash
python scripts/qa_exhibits.py <private-draft-dir>/output/<deck-name>.exhibits.json \
  --facts <private-draft-dir>/evidence.json \
  --fail-on-warning \
  --json
```

然后运行成品 PPTX QA：

```bash
python scripts/qa_pptx.py <deck.pptx> \
  --facts <private-draft-dir>/evidence.json \
  --briefs <private-draft-dir>/briefs.yaml \
  --json
```

Semantic exhibit QA 检查 category/legend 对应关系、coverage、as-of、anchor、evidence references、custom rationale 和 manifest 完整性。PPTX QA 检查：

- 注册数字密度；
- 未登记数字与 fact consistency；
- 无数字支撑的强定性表述；
- source line；
- action title；
- 字体 XML；
- 画布边界；
- 启发式文本溢出与独立文本框重叠。

地图等复杂图元还必须执行专用 render QA，并在 Windows 或 Mac 桌面版 PowerPoint 中做至少一次兼容性抽检。LibreOffice render QA 不能证明 Office 专有 SVG 扩展兼容性；PPTX package test 必须确认 PNG primary blip 与 `asvg:svgBlip` 同时存在。

启发式检查不能替代渲染器级 QA。精确对齐、视觉层级、页码连续性和复杂组合图层仍必须通过渲染切图或人工检查确认。

Demo 和 CI 要求零 findings。真实项目 warnings 必须逐项审阅、修复或记录批准理由。Semantic exhibit QA 的 error 不得通过 PPTX 看起来正常而豁免。

## 修订模式

如果 `baseline/` 已存在，任何变更请求都进入 `references/revision-loop.md`，不得默认整体重生成。

用户反馈“内容太少、太概念化、缺少数据”时，不得只增加文字。必须回到 briefs/evidence，补充 quantification、benchmark、required data points、research tasks 和 appendix backup，再重新生成受影响页面。

## Action Title 规则

- 完整陈述句，含结论/判断，不是主题短语。
- 错：「云迁移成本分析」。对：「分三波迁移可在 18 个月内将 TCO 降低约 30%」。
- 长度不超过两行。
- 有可靠数字时优先放入标题；无可靠数字时允许有据可查的定性标题。
- 标题强度不得超过证据强度。只能支持相关性时不得写成因果结论。

## Evidence Discipline

1. 所有非显而易见事实判断必须有来源，或明确标注团队假设。
2. 当前数据必须实际检索，不得凭记忆填数。
3. 来源冲突时采用更权威、决策相关的口径，并说明差异。
4. 严禁编造数字；示意数据显著标注并登记为 assumption。
5. 所有估算标注 calculation basis。
6. 关键判断有支持与反证查询。
7. 所有数字和 material qualitative assertions 先进入 `evidence.json` 再进入页面。
8. 数据驱动 exhibit 的语义结构必须进入 exhibit manifest。
9. 有来源不代表分析充分；仍须满足 density、quantification/approved qualitative contract、benchmark、method 和 implication。
10. 数据密度要求不能降低真实性门槛。

## 设计 Token

| 用途 | 中文 | 西文/数字 |
|---|---|---|
| 全部文本 | Microsoft YaHei | Arial |

必须同时写入 `<a:latin typeface="Arial"/>` 与 `<a:ea typeface="Microsoft YaHei"/>`。字号：action title 18–20pt；正文 10.5–12pt；密集表格 8.5–9.5pt；图表标注 9–10pt；来源 8pt；页码 9pt。

配色：主色 `#1F3864`，强调色 `#C00000`，灰阶 `#333333/#595959/#A6A6A6/#D9D9D9/#F2F2F2`，背景白色。地图分类可使用 `assets/theme.json` 中受控的 category palette，不得由页面模块自行定义新色。

## 资源索引

- `references/content-density.md`：硬数据密度、qualitative-exhibit 合同与页面类型要求；
- `references/exhibit-planning.md`：page brief、quantification 与 benchmark；
- `references/orchestration.md`：研究 worker、page module、manifest 汇总和并行编排；
- `references/page-patterns.md`：数据密集页型；
- `references/jurisdiction-map.md`：定性辖区地图的数据契约、Office 兼容和 QA；
- `references/qa-checklist.md`：Quantification test 与咨询 QA；
- `references/deck-archetypes.md`：deck 骨架；
- `references/it-consulting-patterns.md`：云/AI/IT 分析模式；
- `references/project-state.md`：事实表与私有状态；
- `references/revision-loop.md`：冻结基线后的修订；
- `scripts/qa_briefs.py`：生产前 brief QA；
- `scripts/qa_exhibits.py`：数据驱动 exhibit semantic QA；
- `scripts/qa_pptx.py`：成品数字、密度与 PPTX QA；
- `scripts/jurisdiction_map`：PowerPoint-compatible PNG fallback + SVG extension 地图；
- `scripts/consulting_shapes.py`：可编辑 PowerPoint-native exhibits。
