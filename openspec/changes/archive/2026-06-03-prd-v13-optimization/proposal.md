## Why

v1.2 PRD 已建立 Android 性能 CR Skill 的核心骨架（10 维度、40+ 条规则、双通道触发），但在探索审查中发现以下关键缺口：

1. **规则覆盖盲区**：主线程 WebView、协程 `runBlocking`、Handler 泄漏、Android 14+ 前台服务合规等高频性能问题无对应规则
2. **缺乏质量闭环**：AI 审查的误报/漏报无回注机制，无法持续优化规则准确性
3. **缺少运营保障**：无审查超时 / 大 PR 策略 / 模型版本记录，流水线规模化时不可控
4. **缺少外置规则机制**：各项目无法定制/覆盖内置规则，落地灵活性不足
5. **缺少能力边界声明**：未明确静态审查固有盲区（Native 内存、JNI、反射等）

**Why now**：Phase 0（Skill 生成）即将启动，须在实现前补齐规则完整性和运营机制。

## What Changes

- 新增 **20 条规则**（其中 4 条 P0），覆盖主线程、启动、内存、网络、协程、后台合规、包体、可观测性等维度
- 新增 **§10.11 WebView 性能**独立维度（4 条规则）
- 新增 **§3.5 外置规则加载机制**：项目级 `custom-rules.md` 和 `overrides.md`，支持 `disable`/`override`/`add` 操作
- 新增 **§3.6 审查规模与 SLA**：超时 5 分钟、大 PR 模式、并发策略
- 新增 **§3.7 质量保障反馈机制**：`#false-positive` 闭环、双周校准、一致性度量
- 新增 **§6.2 影响半径启发式**：高影响改动点（Application、核心网络基类等）的连带维度触发规则
- 新增 **§8.4 已知限制**：9 类静态审查盲区 + 兜底建议
- **§3.3 输出模板**新增 `AI 模型/版本` 和 `审查耗时` 字段
- **§6.1 路径启发式**扩充 Gradle/JNI/WebView/minSdk 映射
- **§7.2** 增加各阶段完成标准、升级条件、回滚策略
- **§9 开放问题**修复编号顺序，新增多模块、热更新、成本监控问题
- 修复 NET-03/04 缺失的参考工具列

## Capabilities

### New Capabilities
- `external-rules`: 项目级外置规则加载与覆盖机制
- `review-quality-feedback`: AI 审查误报/漏报闭环与校准流程
- `review-sla`: 审查规模控制、超时策略、大 PR 降级
- `webview-performance`: WebView 性能审查规则维度
- `known-limitations`: 静态审查能力边界声明

### Modified Capabilities
- `rule-checklist`: 规则清单从 ~40 条扩展至 ~60 条，新增 P0 4 条、P1 11 条、P2 5 条
- `output-format`: 审查报告增加 AI 模型版本和耗时字段

## Impact

- 影响文件：`Android 性能 CR AI Code Review 技能 prd文档.md`（v1.2 → v1.3）
- Skill 实现（`.cursor/skills/android-performance-cr/SKILL.md`）需按 v1.3 规则集实现
- 流水线 Job 模板需支持外置规则发现
- 无代码依赖变更，纯文档产品
