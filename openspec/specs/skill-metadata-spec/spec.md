# Purpose
定义 SKILL.md 的 YAML front matter 元数据规范。

## Requirements

### Requirement: SKILL.md 必须包含 YAML front matter 元数据
SKILL.md SHALL 以 YAML front matter 开头，包含 `name`、`description` 和 `metadata` 字段。`metadata` SHALL 包含 `author` 和 `version`。SHALL 不包含 `license`、`compatibility`、`generatedBy` 字段。

#### Scenario: 标准元数据格式
- **WHEN** 打开 SKILL.md
- **THEN** 文件首行 SHALL 为 `---`，其后包含 `name: android-performance-cr`、`description`、`metadata:` 块（含 `author: 廖兵` 和 `version: 0.0.1`），以 `---` 闭合

#### Scenario: 无多余字段
- **WHEN** 解析 SKILL.md 的 front matter
- **THEN** SHALL 不包含 `license`、`compatibility`、`generatedBy` 字段
