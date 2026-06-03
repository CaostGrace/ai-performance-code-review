# tool-reference Specification (Delta)

## ADDED Requirements

### Requirement: 工具速查卡覆盖 Compose Compiler Metrics
§7.4 工具使用速查卡 SHALL 新增 Compose Compiler Metrics（`composeCompiler`）工具条目，帮助定位 Compose 规则中的不稳定性参数和重组统计。

#### Scenario: Compose Compiler Metrics 条目完整性
- **WHEN** Skill 审查 Compose 代码遇到 @Stable/@Immutable 检查
- **THEN** 速查卡 SHALL 提供 Compose Compiler Metrics 的 Gradle 配置、输出文件位置、不稳定参数识别方法
