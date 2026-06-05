# Purpose
定义 AI Code Review 的 Markdown 报告格式，面向本地 Agent 使用。含固定报告路径和格式校验。

## Requirements

### Requirement: 审查报告摘要字段
审查报告 SHALL 包含改动类型、审查模型版本、扫描范围、已查维度、审查耗时、合入建议字段。触发通道 SHALL 固定为 `local-agent`。

#### Scenario: 审查完成时，报告摘要 SHALL 包含审查耗时（秒）；若超时则标注 `partial` 及原因。
- **WHEN** 审查在超时前完成
- **THEN** 摘要 SHALL 包含审查耗时（秒）

#### Scenario: 审查报告生成时，「触发通道」字段 SHALL 固定为 `local-agent`。
- **WHEN** 任何触发方式
- **THEN** 触发通道字段 SHALL 为 `local-agent`

### Requirement: 固定报告路径
审查报告 SHALL 固定输出到项目根目录 `./android-performance-cr-report.md`，每次审查 SHALL 覆盖前次报告。

#### Scenario: 报告位置
- **WHEN** Skill 完成审查
- **THEN** 报告 SHALL 写入 `<项目根>/android-performance-cr-report.md`

### Requirement: Phase 0 格式校验
Phase 0 SHALL 提供 Markdown 格式校验脚本，检查报告是否包含必要字段。

#### Scenario: 校验报告完整性
- **WHEN** 报告生成后
- **THEN** 校验脚本 SHALL 检查合入建议行、发现项表格表头+分隔线、P0 行含文件:行号

### Requirement: 强约束 Prompt 控制格式
SKILL.md SHALL 包含严格的输出格式指令，要求 AI 必须完全按照 §3.3 模板输出，不得增减字段。

#### Scenario: 模板约束
- **WHEN** AI 生成审查报告
- **THEN** SHALL 包含「摘要」「发现项」「未覆盖/需人工」「验证建议（OBS-01）」四个章节
