# output-format Specification

## Purpose
定义 AI Code Review 的 Markdown 报告格式，当前面向本地 Agent 使用。流水线触发通道内容已移入 §10 后期展望。

## Requirements

### Requirement: 审查报告摘要字段
审查报告 SHALL 包含改动类型、审查模型版本、扫描范围、已查维度、审查耗时、合入建议字段。触发通道 SHALL 固定为 `local-agent`。

#### Scenario: 摘要包含审查耗时
- **WHEN** 审查完成
- **THEN** 报告摘要 SHALL 包含审查耗时（秒）；若超时则标注 `partial` 及原因

#### Scenario: 触发通道固定为本地 Agent
- **WHEN** 审查报告生成
- **THEN**「触发通道」字段 SHALL 固定为 `local-agent`
