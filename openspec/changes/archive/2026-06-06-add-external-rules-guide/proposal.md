## Why

Skill 支持通过 `.android-performance-cr/overrides.md` 和 `custom-rules.md` 定制审查行为，但缺少编写教程和交互引导。新手面对七列格式和三种操作（disable/override/add）门槛高，容易写出格式错误或判定条件不合理的规则。

## What Changes

- 新增 `references/external-rules-guide.md`：外置规则编写教程，含正反例（"禁用 MEM-03"、"override ST-01 为 P1"、"新增一条自定义规则"）
- SKILL.md 新增伪命令 `/custom-rules-help`，三级响应（快速参考 / 完整教程 / 交互生成）
- PRD §3.5 引用教程文档；PRD 修订记录更新

## Capabilities

### New Capabilities
- `external-rules-tutorial`: 外置规则编写教程文档规范（存放于 `references/`，含正反例和常见错误）

### Modified Capabilities
- `skill-references-convention`: references/ 目录增加 `external-rules-guide.md`
- `output-format`: SKILL.md 新增伪命令 `/custom-rules-help` 及三级响应行为

## Impact

- **Skill 文件**: 新增 `references/external-rules-guide.md`，修改 `SKILL.md`
- **PRD**: §3.5 增加教程引用
- **Specs**: 新增 1 个，修改 2 个
