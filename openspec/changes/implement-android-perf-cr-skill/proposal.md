## Why

PRD v3.0 定义了 81 条 Android 性能 CR 规则和 AI Skill 的宏观设计，但缺少 Skill 的**具体实现设计**——包括文件结构、动态路由机制、规则加载策略、P0 兜底模型、判定逻辑、交互模型、输出格式控制等关键架构决策。需要通过一次系统的设计澄清（grill-me 会话）产出所有实现决策，并落地为可执行的 Skill 文件。

## What Changes

- 将 Skill 落地为**多文件结构**：1 个 SKILL.md 入口 + 14 个按维度拆分的规则文件 + 1 个工具速查卡文件
- 实现**两层动态路由**：第一层路径/关键字粗筛 + 第二层 P0 必查兜底
- P0 兜底分 **L0（永远注入）+ L1（按文件语言注入）**
- 引入**三重判定逻辑**：精确匹配 → 按原等级报告 / 模式可疑 → 降级报告 / 架构担忧 → 写入需人工
- 支持**文件级语言体系识别**（View vs Compose），按文件加载对应规则子集
- 支持**外置规则热加载**：随工作区切换自动读取 `.android-performance-cr/overrides.md` 和 `custom-rules.md`
- 支持**双输入模式**：自动 `git diff` + 手动 @ 文件
- 输出固定路径 `./android-performance-cr-report.md`，格式校验脚本兜底
- 正反例代码直接作为冒烟测试用例
- OBS-01 Phase 0 不阻塞，改为 AI 自动追加提示

## Capabilities

### New Capabilities
- `skill-file-structure`: Skill 多文件组织与路由入口（SKILL.md + rules/*.md + tools.md）
- `dynamic-rule-routing`: 两层路由机制（粗筛 + P0 兜底），按 diff 特征动态加载规则子集
- `p0-safety-net`: P0 必查规则集，分 L0/L1 两级，确保致命问题不遗漏
- `triple-judgment`: 三重判定逻辑（精确匹配/可疑降级/架构担忧写需人工）
- `file-type-detection`: 文件级语言体系识别，按 View/Compose 分派规则
- `external-rules-hot-reload`: 外置规则随工作区切换自动热加载
- `input-modes`: 双输入模式（自动 git diff + 手动 @ 文件）
- `output-format-enforcement`: 固定路径报告 + 格式校验脚本
- `test-from-examples`: 正反例代码直接作为冒烟测试用例

### Modified Capabilities
- `output-format`: 触发通道固定 `local-agent`；报告路径固定为 `./android-performance-cr-report.md`（每次覆盖）；增加格式校验要求
- `rule-checklist`: 规则从单体文档拆分为 14 个维度文件；引入必查规则集（`_must-check.md`）
- `external-rules`: 外置规则加载从"Skill 启动时一次性加载"改为"随工作区切换自动热加载"；Phase 0 不做自动去重
- `review-sla`: 新增文件级预扫描（grep 关键字）机制，路由阶段消费
- `code-example-standards`: 正反例代码从 PRD 文档中的示例升级为可独立运行于审查流程的测试用例

## Impact

- **Skill 文件**: 新建 `android-performance-cr/` 目录，包含 SKILL.md + 14 个 rules/*.md + tools.md
- **PRD 文档**: 更新至 v3.1，回写 grill-me 确认的全部设计决策
- **OpenSpec specs**: 新增 9 个 spec，修改 5 个已有 spec（delta）
- **无外部依赖变更**：不涉及 CI 流水线、Lint 规则、APM 系统
