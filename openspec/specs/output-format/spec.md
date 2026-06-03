# output-format Specification

## Purpose
TBD - created by archiving change prd-v13-optimization. Update Purpose after archive.
## Requirements
### Requirement: 审查报告摘要字段
审查报告摘要 SHALL 包含以下字段：改动类型、触发通道、AI 模型/版本、扫描范围、已查维度、审查耗时、合入建议。

#### Scenario: 通道 A 报告包含完整摘要
- **WHEN** 通道 A 产出审查报告
- **THEN** 摘要 SHALL 包含 AI 模型/版本和审查耗时字段，用于一致性复盘

#### Scenario: 审查超时标注
- **WHEN** 审查超时
- **THEN** 审查耗时字段后 SHALL 标注 `partial` 及原因

