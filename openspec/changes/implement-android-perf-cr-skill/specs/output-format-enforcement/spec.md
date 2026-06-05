## ADDED Requirements

### Requirement: 固定报告路径
审查报告 SHALL 固定输出到项目根目录 `./android-performance-cr-report.md`，每次审查 SHALL 覆盖前次报告。

#### Scenario: 报告固定位置
- **WHEN** Skill 完成审查
- **THEN** 报告 SHALL 写入 `<项目根>/android-performance-cr-report.md`

#### Scenario: 报告覆盖
- **WHEN** 同一项目第二次触发审查
- **THEN** 新报告 SHALL 覆盖旧的 `android-performance-cr-report.md`

### Requirement: Phase 0 格式校验脚本
Phase 0 开发阶段 SHALL 提供 Markdown 格式校验脚本，检查报告是否包含必要字段（合入建议行、发现项表格表头+分隔线、P0 行含文件:行号）。

#### Scenario: 校验通过
- **WHEN** 报告包含"合入建议"行、发现项表格表头和分隔线
- **THEN** 校验脚本 SHALL 返回通过

#### Scenario: 校验失败
- **WHEN** 报告缺少"合入建议"字段
- **THEN** 校验脚本 SHALL 返回失败并提示缺失字段

### Requirement: 强约束 Prompt 控制格式
SKILL.md SHALL 包含严格的输出格式指令，要求 AI 必须完全按照 §3.3 模板输出，不得增减字段。

#### Scenario: 输出模板约束
- **WHEN** AI 生成审查报告
- **THEN** SHALL 包含「摘要」「发现项」「未覆盖/需人工」「验证建议（OBS-01）」四个章节，不得缺失
