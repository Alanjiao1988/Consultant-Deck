# Terminology and Chinese-English typography

## Keep technical primitives in English

Keep terms such as API, token, RAG, SLA, TCO, LLM, embedding, prompt, landing zone, DevOps, FinOps, Zero Trust, data lakehouse and MLOps in English unless the user gives a project-specific glossary.

## Translate generic business terms into Chinese

- organization → 组织
- strategy → 战略
- stakeholder → 相关方 / 干系人
- alignment → 对齐 / 一致
- capability → 能力
- initiative → 举措
- roadmap → 路线图
- governance → 治理
- operating model → 运营模式 / 组织运作模式
- business case → 商业论证

## Spacing

- Put a half-width space between Chinese and English: 使用 Azure OpenAI 构建 RAG 应用。
- Put a half-width space between numbers and Chinese units: 18 个月、5 个系统。
- Do not add a space before percent sign or currency suffix: 30%、$5m。
- Chinese context uses Chinese punctuation: ，。；：。

## Font rule

All text runs should set both Latin and East Asian fonts: Arial + Microsoft YaHei. Use `set_font()` from `scripts/consulting_shapes.py`.
