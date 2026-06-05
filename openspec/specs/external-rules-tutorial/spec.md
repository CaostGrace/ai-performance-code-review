# Purpose
定义外置规则编写教程文档的规范，含正反例和交互引导。

## Requirements

### Requirement: 外置规则编写教程文档
Skill SHALL 在 `references/` 目录包含 `external-rules-guide.md` 教程文档。文档 SHALL 覆盖 overrides.md 三种操作和 custom-rules.md 七列写法，每种操作 SHALL 包含正例和反例。

#### Scenario: 教程完整性
- **WHEN** 用户打开 `references/external-rules-guide.md`
- **THEN** SHALL 包含以下章节：概述、文件位置、overrides.md 操作手册（含正反例）、custom-rules.md 七列详解、真实场景示例、常见错误和 FAQ

#### Scenario: 正反例覆盖
- **WHEN** 教程描述 overrides.md 的 disable 操作
- **THEN** SHALL 包含正例（如"禁用 MEM-03"）和反例（如"误禁用 ST-01"）

### Requirement: 真实场景示例
教程 SHALL 包含至少 3 个完整真实场景示例。

#### Scenario: 场景完整性
- **WHEN** 阅读场景示例
- **THEN** 每个场景 SHALL 包含：触发原因、文件路径、完整 Markdown 内容、加载后效果

### Requirement: 伪命令检测
SKILL.md SHALL 支持伪命令 `/custom-rules-help` 和关键词检测（"写外置规则"、"添加外置规则"、"自定义规则"、"怎么加规则"）。

#### Scenario: 伪命令触发
- **WHEN** 用户输入 `/custom-rules-help`
- **THEN** SKILL.md SHALL 识别为外置规则帮助请求，进入三级响应模式

#### Scenario: 关键词触发
- **WHEN** 用户输入包含"写外置规则"或"自定义规则"等关键词
- **THEN** SKILL.md SHALL 识别为帮助请求
