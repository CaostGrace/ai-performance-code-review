## ADDED Requirements

### Requirement: references/ 目录包含外置规则教程
Skill 的 `references/` 目录 SHALL 包含 `external-rules-guide.md`，与 `tools.md` 并列。SHALL 在 Skill 需要输出外置规则指导时按需加载该文档。

#### Scenario: 教程文件存在
- **WHEN** 查看 Skill 的 `references/` 目录
- **THEN** SHALL 包含 `external-rules-guide.md` 文件
