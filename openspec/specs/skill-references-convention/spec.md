# Purpose
定义 Skill 辅助文档存放于 `references/` 目录的约定。

## Requirements

### Requirement: 辅助文档存放于 references/ 目录
Skill 的辅助参考文档（工具速查卡等）SHALL 存放于 `references/` 子目录，SHALL 不直接放在 Skill 根目录。

#### Scenario: tools.md 位置
- **WHEN** 查看 Skill 目录结构
- **THEN** `tools.md` SHALL 位于 `references/tools.md`，SHALL 不在根目录

### Requirement: SKILL.md 显式引用 references/ 文档
SKILL.md SHALL 在审查流程中包含对 `references/tools.md` 的按需加载指令：当 AI 需要在建议中引用验证工具时，读取 `references/tools.md`。

#### Scenario: 按需加载 tools
- **WHEN** AI 审查发现需要建议验证工具
- **THEN** SKILL.md 中的流程指令 SHALL 引导读取 `references/tools.md`

### Requirement: references/ 目录包含外置规则教程
Skill 的 `references/` 目录 SHALL 包含 `external-rules-guide.md`，与 `tools.md` 并列。

#### Scenario: 教程文件存在
- **WHEN** 查看 Skill 的 `references/` 目录
- **THEN** SHALL 包含 `external-rules-guide.md` 文件
