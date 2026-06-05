## ADDED Requirements

### Requirement: 伪命令响应行为
当用户输入 `/custom-rules-help` 或外置规则相关关键词时，Skill SHALL 按三级响应：

- **L1**（格式询问）：内联输出快速参考格式
- **L2**（教程请求）：读取 `references/external-rules-guide.md` 输出完整教程
- **L3**（交互生成）：逐步引导用户填写规则 ID、等级、说明等字段，生成到 `.android-performance-cr/`

#### Scenario: L1 快速参考
- **WHEN** 用户问"overrides.md 格式是什么"
- **THEN** SHALL 输出 3 行模板示例，不读取教程文件

#### Scenario: L2 完整教程
- **WHEN** 用户输入 `/custom-rules-help` 或"怎么写外置规则"
- **THEN** SHALL 读取 `references/external-rules-guide.md` 并输出全文

#### Scenario: L3 交互生成
- **WHEN** 用户说"帮我添加一条外置规则"或"禁用 MEM-03"
- **THEN** SHALL 逐步引导用户完成规则编写，最终生成文件到目标路径
