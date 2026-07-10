---
name: consulting-deck
description: Trigger for consulting-style PPT, consulting deck, McKinsey/BCG/Bain-style slides, 麦肯锡风格 PPT, 咨询风格 PPT, action title, storyline, 金字塔原理, executive briefing, sales proposal, pre-sales deck, IT/cloud/AI transformation presentation, workshop material, investment analysis and client or board-level PowerPoint decks; generate research-heavy, data-rich decks with storyline, exhibit planning, evidence research with support and counter-evidence, content-density gates, private repo-backed project state, fact-table QA, subagent orchestration, revision loop, consulting QA, appendix depth and Chinese-English typography rules.
---

# Consulting Deck Skill

咨询风格 deck 的本质是信息架构纪律、分析深度与证据链，不是视觉装饰。目标：读者只读标题就能理解完整论证；打开任何一页，10 秒内抓住该页唯一信息；继续阅读 1–2 分钟后，能够看到足够的数据、比较、计算、边界条件和实施细节来检验该结论。

默认目标不是“概念正确的简报”，而是“研究驱动、数据密集、可以经受高管追问的咨询交付物”。除非用户明确要求极简 executive brief，否则策略、市场、投资、厂商评估、售前、云、AI 和转型类 deck 默认采用 research-heavy consulting mode。

## 触发场景

当用户要求「咨询风格 PPT」「consulting deck」「McKinsey style」「麦肯锡风格」「BCG style」「Bain style」「action title」「金字塔原理做 PPT」「storyline」「给客户/高管的汇报 deck」「方案汇报 PPT」「售前 PPT」「workshop 材料」「投资分析 PPT」，或任何受众为企业高管/客户的专业商务演示文稿时，触发本技能。

## 数据安全红线

真实客户项目状态不得写入公开可访问的存储，包括当前 public skill repo。客户名称、内部数字、项目代号、非公开架构、storyline、briefs、evidence.json 和 assumptions 必须存放在独立 private project-state repo、企业内部 repo，或本地加密工作区。

## 默认内容模式

使用 `references/content-density.md` 定义内容密度。默认模式：

| 模式 | 适用场景 | 核心页 | Appendix | 分析页证据预期 |
|---|---|---:|---:|---|
| Executive brief | 用户明确要求极简、高管速览 | 6–10 | 3–8 | 每页 2–4 条证据 |
| Standard consulting | 时间或数据受限 | 10–18 | 4–10 | 每页 3–5 条证据 |
| Research-heavy consulting | 默认 | 12–25 | 6–20 | 每页 4–8 条证据，并有比较或 benchmark |

页数不是目标。证据与分析需要独立展开时增加页面；不能支持决策的页面删除。

## 强制工作流

```text
Step 1 需求与深度确认 → Step 2 Storyline 与 coverage map → Step 3 Exhibit Plan 与 content budget → Step 4 Evidence Research → Step 5 确认/自动执行 → Step 6 逐页生成 → Step 7 咨询与内容深度 QA → Step 8 渲染 QA
```

### Step 1 — 需求与深度确认

已知的不重复问，缺失的必须补齐：受众、场景、语言、页数、是否需要 appendix、风格基准、交付时点、可用内部数据、是否允许外部研究。

除非用户明确要求精简，设定 `content_density_target: research-heavy`。用户给定较少页数但要求详实内容时，优先增加 appendix，而不是把所有分析压缩成概念页。

落盘动作：生成开始前，确认 private state root，并建立 `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/`。所有中间过程文件都写入该私有目录，不只保存在本地临时文件或对话中，也不得写入 public skill repo。

### Step 2 — Storyline 与 coverage map

先从 `references/deck-archetypes.md` 选择骨架，再产出全部页面 action title。只读标题列表，必须构成完整、连贯、有结论的故事。

Storyline 之外必须建立 coverage map，检查是否覆盖：

- 事实基础与趋势；
- 问题/机会的量化；
- 根因或价值驱动；
- 备选方案和取舍；
- 推荐方案；
- 财务或运营影响；
- 实施路径、资源与治理；
- 风险、反证与成功条件；
- 决策请求；
- appendix 备份。

硬禁令：不得并行写 storyline。Storyline 必须由单一主 agent 负责，以保证 horizontal logic 和叙事主线一致。

落盘动作：写入 `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/storyline.md`，并包含 core deck 与 appendix 的页面规划。

### Step 3 — Exhibit Plan 与 content budget

每页必须填写 page brief。字段见 `references/exhibit-planning.md`，至少包含：

| 字段 | 内容 |
|---|---|
| Page role | 核心论证、支持分析、建议、决策或 appendix |
| Key question | 这页回答什么问题 |
| Action title | 这页的证据化结论 |
| Evidence IDs | 将使用的事实与计算 ID |
| Required data points | 页面必须出现的具体数字、事实或定义 |
| Comparison basis | 历史、同业、分部、地区、情景或 benchmark |
| Analysis method | 趋势、桥接、拆解、评分、敏感性、场景或综合 |
| Primary exhibit | 证明标题的主要图表/表格 |
| Insight annotations | 2–4 条需要直接标注的洞察 |
| Decision implication | 对受众决策意味着什么 |
| Data source | 来源、检索日期、计算基础或团队假设 |
| Caveat | 假设、不确定性和反证 |
| Appendix link | 方法、明细或备份所在页 |
| Density target | executive、standard 或 research-heavy |
| Unresolved gaps | 尚待检索、假设或删除的证据缺口 |

Evidence 为空、没有比较基准、没有分析方法且无法标注为合理概念页的页面，要么补证据，要么删除。

Research-heavy 模式下，核心分析页通常需要 4–8 个 evidence items；2 个是最低下限，不是推荐值。市场、财务、投资、厂商、TCO、路线图、风险和架构页面必须满足 `references/content-density.md` 中对应页面类型的内容要求。

落盘动作：写入 `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/briefs.yaml`。

### Step 4 — Evidence Research

Evidence Research 是独立强制步骤，不得只作为 Evidence Discipline 的原则存在。必须从全部 page brief 汇总检索任务清单，再回填每页 brief。

每条检索任务必须包含：页码、待验证判断、所需数据点、建议查询词、比较口径、证据类型、来源优先级、输出格式和反证方向。

证据类型至少包括：市场数据、竞品、产品能力与价格、监管、财务、客户案例、技术可行性、实施成本、运营基线、组织能力和风险。

#### 双向检索规则

每个关键判断至少执行：

1. 支持性查询：寻找能证明该判断的证据。
2. 反证查询：寻找能推翻、限制或弱化该判断的证据。

处理规则：

- 反证成立：修改 storyline 或 action title，不得硬撑原结论。
- 反证部分成立：写入该页 Caveat、风险页或 speaker notes。
- 反证不成立：在 speaker notes 预置客户 Q&A 应答。

凡 Evidence Research 导致 action title、核心结论、页面顺序或推荐方案变更，进入 Step 5 前必须重新执行只读标题测试和 coverage test。

#### 来源深度规则

优先级：

1. 公司年报/10-K/20-F/财报材料、官方产品文档、政府和监管机构；
2. 国际组织、标准机构和权威行业协会；
3. 可靠数据商、研究机构和学术来源；
4. Reuters、FT、Bloomberg 等高质量媒体；
5. 厂商博客、专业媒体与二手总结，仅作为补充并标注 caveat。

重大市场、财务或监管结论，在可获得的情况下应包含至少一个 primary source，并使用两个独立来源族进行交叉验证。管理层陈述必须与独立证据区分。

#### 回填规则

检索结果必须回填到 page brief：数字、单位、期间、定义、来源、检索日期、计算基础、counter-evidence 和 caveat。

所有进入 deck 的数字必须先登记到 `evidence.json`，再进入页面。派生指标必须登记公式和 input evidence IDs。

检索 3 次无果的判断，必须降级为显著标注的「团队假设」，或删除对应页面。需要当前数据时必须实际检索，不得凭记忆填数。

Research-heavy 模式下，典型 10 页核心 deck 的默认质量底线为：

- 25–50 个不重复的事实或计算；
- 8–15 个相关且高质量的独立来源；
- 至少 5 个带数据、对比或量化分析的 primary exhibits；
- 至少 3 页 appendix，用于来源、方法、完整表格、敏感性或备份分析。

这些是质量门槛，不得通过拆分同一事实来凑数。主题本身缺乏数据时，应显著记录限制并弱化结论。

落盘动作：写入或更新 `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/evidence.json` 和 `assumptions.md`。

### Step 5 — 确认 / 自动执行

默认协作模式下，先请用户确认 storyline + exhibit plan + evidence research findings。用户要求「一次性生成」「不要反复确认」「直接给我文件」时，进入自动执行模式：继续生成，并将 assumptions、未解决证据项和关键 caveats 放入 appendix 或 speaker notes。

确认门除了故事线外，还必须检查：

- 每个核心页有明确的比较基准或分析方法；
- 每个重大结论有足够证据和反证处理；
- deck 包含量化影响、实施细节、风险条件和决策请求；
- appendix 已经规划，而不是最后补齐；
- 没有只因为“咨询 PPT 通常有这一页”而存在的页面。

落盘动作：确认通过或自动执行门通过后，冻结 `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/baseline/` 基线快照。冻结 = 基线快照存在。

### Step 6 — 逐页生成

- 页面骨架调用 `scripts/consulting_layouts.py`。
- 咨询图形调用 `scripts/consulting_shapes.py`。
- TCO/ROI/payback 调用 `scripts/business_case.py`。
- 云/AI/架构/能力地图/operating model 调用 `scripts/architecture_helpers.py`。
- 模板由 `scripts/create_template.py` 生成；示例由 `scripts/demo_generate_deck.py` 生成。

页面生成硬规则：

1. 主体必须用一个 primary exhibit 证明 action title。
2. 每个核心分析页至少引用 2 个 evidence IDs，research-heavy 模式通常为 4–8 个。
3. 每页至少有一个趋势、同业、分部、情景、benchmark、桥接或拆解；单独一个数字通常不够。
4. 图表需有 2–4 个 insight annotations，不能把解释全部留给口头汇报。
5. 页面必须明确 implication/now-what；复杂方法与完整表格通过 appendix link 保留。
6. 禁止使用只有图标、箭头、五框模型、未量化成熟度或空泛“现状—目标—路径”的装饰性概念页。
7. 架构页必须包括基线/约束、3–5 个设计决策、2–4 个量化目标、控制点、取舍与依赖。
8. 路线图必须包含 deliverables、owners、exit criteria、decision gates、dependencies、target KPIs 和 critical path。
9. 商业论证必须包含完整假设、成本与收益、base/upside/downside、敏感性和收益实现责任。
10. 风险页必须包含概率、影响、触发/领先指标、mitigation owner 和 residual risk。
11. 信息过多时拆成两页或放入 appendix，不得通过把正文缩到设计 token 以下来硬塞。

如使用 subagent 并行生成页面，必须遵守 `references/orchestration.md`：不得多个 agent 并发写同一个 `.pptx`；采用页面模块化装配模式，subagent 只产出 `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/pages/page_NN.py`，统一签名为 `def render(slide, ctx)`，主 agent 单进程按 storyline 顺序装配。`ctx` 的最小 schema 由 `references/orchestration.md` 定义，页面 worker 不得自行发明新的必填字段。

落盘动作：页面模块写入 `pages/`，输出写入 `output/<deck-name>_v<major>.<minor>.pptx` 或保存交付引用。

### Step 7 — 咨询与内容深度 QA

执行 `references/qa-checklist.md`：Pyramid test、Horizontal logic、Vertical logic、So-what、Now-what、Evidence test、Content-depth test、Deck-density test、Executive skim test、Appendix hygiene、术语与数字一致性。

逐页必须回答：

- promised data points 是否全部出现；
- evidence 是否足够支持追问，而不是仅用于装饰；
- 是否存在有意义的 comparison basis；
- 计算是否可复现；
- 是否解释了 why it matters；
- 是否有 decision implication；
- caveat 是否可见或有 appendix/notes 备份；
- 删除该页是否会削弱决策逻辑。

任何核心页有两个或以上答案为“否”，必须修订或删除。

并行规则：逐页 vertical logic 与 content-depth QA 可并行；horizontal logic、coverage map、全 deck 数字一致性和 executive summary 综合核对不得并行，必须由主 agent 串行完成。

落盘动作：将 QA 结果或修复摘要写入 `changelog.md`。

### Step 8 — 渲染 QA

先运行：

```bash
python scripts/qa_pptx.py <deck.pptx> --facts <private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/evidence.json
```

再执行 PPT 渲染检查：文本溢出、元素重叠、对齐、页码、来源行和字体。渲染切图检查可以按 3–5 页一组并行分派；最终修订必须由主 agent 串行完成。

密度检查：不得用低于设计 token 的字号来掩盖页面过载。无法保持可读性时，拆页或转移到 appendix。

落盘动作：将最终 QA 结论、输出版本和交付说明写入 `changelog.md`。

## 修订模式

如果 `<private-state-root>/deck-drafts/<YYYY-MM-DD>/<deck-title-slug>/baseline/` 已存在，任何变更请求都进入修订模式，不得默认整体重新生成。修订前先 diff 基线，列出目标页和牵连页；修订后按变更类型分级重跑 QA。详见 `references/revision-loop.md`。

如果用户反馈“内容太少、太概念化、缺少数据”，不得只增加文字。必须回到 briefs 与 evidence 层，补充 required data points、comparison basis、analysis method、research tasks 和 appendix backup，然后重新生成受影响页面。

## Orchestration 规则

详见 `references/orchestration.md`。核心硬规则：

1. 不得并行写 storyline。
2. 不得并发写同一个 `.pptx`。
3. 不推荐分段生成多个 `.pptx` 再合并；默认采用页面模块化装配模式。
4. 有 subagent 时优先并行 Evidence Research、页面模块生成、逐页 vertical/content-depth QA 和分批渲染检查。
5. 无 subagent 环境下按相同步骤串行执行；任务清单本身是质量工具，并行只是加速手段。
6. 中间过程文件必须写入 private state root，不得写入当前 public skill repo。
7. Research subagent 必须返回可进入 `evidence.json` 的结构化事实、定义、来源、反证与 caveat，而不是泛泛的行业总结。

## Action Title 规则

- 完整陈述句，含结论/判断，不是主题短语。
- 错：「云迁移成本分析」。对：「分三波迁移可在 18 个月内将 TCO 降低约 30%」。
- 长度不超过两行。有具体数字时，优先放进标题。
- 标题和主体是「论点—论据」关系。
- 标题强度不得超过证据强度。证据只能支持相关性时，不得写成因果结论。

## Evidence Discipline

1. 所有非显而易见的事实判断必须有来源，或明确标注为「团队假设」。
2. 外部市场数据优先使用公司年报/10-K/IR、政府/监管机构、权威研究机构、Reuters/FT/Bloomberg 等来源。
3. 需要当前数据时必须实际检索，不得凭记忆填数。
4. 来源冲突时，正文采用更权威口径，并在 appendix 或 notes 说明差异。
5. 严禁为完成图表而编造数字；示意数据必须显著标注。
6. 所有估算必须标注 calculation basis。
7. 每个关键判断必须有支持性查询与反证查询，反证结果必须影响 storyline、caveat 或 Q&A notes。
8. 所有进入 deck 的数字必须先登记事实表 `evidence.json`，再进入页面；QA 必须使用 `qa_pptx.py --facts <evidence.json>` 模式检查数字一致性。
9. 有来源不代表分析充分；还必须满足 content-density、comparison、method 和 implication 要求。
10. 一个来源列表不能替代 source quality。重大结论优先使用 primary sources 并进行独立交叉验证。

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
| `references/content-density.md` | research-heavy 默认模式、每页与全 deck 内容门槛 |
| `references/deck-archetypes.md` | 各类 deck 的研究型分析骨架与 minimum evidence pack |
| `references/exhibit-planning.md` | page brief、content budget 与研究任务模板 |
| `references/project-state.md` | 私有状态层与事实表 |
| `references/revision-loop.md` | 冻结基线后的修订流程 |
| `references/orchestration.md` | subagent 并行编排与失败降级 |
| `references/page-patterns.md` | 数据密集型页面模式 |
| `references/it-consulting-patterns.md` | 云/AI/IT 咨询模式 |
| `references/terminology.md` | 中英混排与术语 |
| `references/qa-checklist.md` | 咨询、内容深度、证据与渲染 QA |
| `assets/theme.json` | 设计 token |
| `scripts/consulting_layouts.py` | 页面骨架 |
| `scripts/consulting_shapes.py` | 咨询图形 |
| `scripts/business_case.py` | 商业论证 |
| `scripts/architecture_helpers.py` | 架构/能力图 |
| `scripts/qa_pptx.py` | 自动 QA |
| `scripts/create_template.py` | 生成模板 PPTX |
| `scripts/demo_generate_deck.py` | 生成 demo deck |