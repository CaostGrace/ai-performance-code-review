## Context

Skill 已支持外置规则加载，但用户需要编写指导。当前仅有 PRD §3.5 的格式定义，缺少实践教程、正反例和交互引导。

## Goals / Non-Goals

**Goals:**
- 提供完整的外置规则编写教程（正反例覆盖 3 个真实场景）
- SKILL.md 支持伪命令 `/custom-rules-help`，三级智能响应
- 教程嵌入在 `references/` 中，可按需加载

**Non-Goals:**
- 不改变外置规则的加载机制或文件格式
- 不改变 rules/ 内置规则

## Decisions

### D1: 三级响应模型

当用户输入 `/custom-rules-help` 或关键词（"写外置规则"/"添加外置规则"/"自定义规则"）时：

- **L1 快速参考**：仅问格式 → 内联输出 3 行模板
- **L2 完整教程**：问"怎么写" → 读取 `references/external-rules-guide.md` 输出全文
- **L3 交互生成**：说"帮我添加" → AI 逐步引导填写，生成到 `.android-performance-cr/`

### D2: 教程内容结构

```
1. 概述
2. 文件位置与加载顺序
3. overrides.md 三种操作
   - disable：正例（禁用 MEM-03）+ 反例（误禁用 ST-01）
   - override：正例（ST-01 P0→P1）+ 反例（试图改判定条件）
   - add：正例 + 反例（ID 重复、缺列）
4. custom-rules.md 七列详解
5. 真实场景完整示例（3 个）
6. 常见错误和 FAQ
```

### D3: 真实场景示例

- 场景 A：项目用 Glide 统一加载图片 → 禁用 MEM-03
- 场景 B：启动 SDK 已在基线计量 → ST-01 降为 P1
- 场景 C：新增规则 "禁止 ViewModel 直接持有 Context"

### D4: SKILL.md 伪命令检测

在触发方式区域增加伪命令 `custom-rules-help` 和关键词检测逻辑。

## Risks / Trade-offs

- 教程内容较重（含 Kotlin 代码示例）→ 仅按需加载，不常驻 prompt
- 交互生成依赖 AI 推理能力 → L3 为实验性功能，引导词强调"AI 辅助"
