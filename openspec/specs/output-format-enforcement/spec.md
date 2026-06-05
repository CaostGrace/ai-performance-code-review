# Purpose
定义审查报告的固定路径输出和格式校验。

## Requirements

### Requirement: 固定报告路径
审查报告 SHALL 固定输出到项目根目录 `./android-performance-cr-report.md`，每次审查 SHALL 覆盖前次报告。

#### Scenario: 报告固定位置
- **WHEN** Skill 完成审查
- **THEN** 报告 SHALL 写入 `<项目根>/android-performance-cr-report.md`

#### Scenario: 报告覆盖
- **WHEN** 同一项目第二次触发审查
- **THEN** 新报告 SHALL 覆盖旧报告

### Requirement: Phase 0 格式校验脚本
Phase 0 开发阶段 SHALL 提供 Markdown 格式校验脚本。

#### Scenario: 校验通过
- **WHEN** 报告包含必要字段
- **THEN** 校验脚本 SHALL 返回通过

#### Scenario: 校验失败
- **WHEN** 报告缺少必要字段
- **THEN** 校验脚本 SHALL 返回失败并提示

### Requirement: 强约束 Prompt 控制格式
SKILL.md SHALL 包含严格的输出格式指令。

#### Scenario: 输出模板约束
- **WHEN** AI 生成审查报告
- **THEN** SHALL 包含「摘要」「发现项」「未覆盖/需人工」「验证建议」四个章节
