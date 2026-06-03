# rule-checklist Specification

## Purpose
定义 Android 性能 AI Code Review 的规则清单覆盖维度、P0 规则覆盖率、规则数量基准和代码案例质量标准。规则清单由 PRD §10 维护，共 12 维度 81 条规则，每条规则包含可编译 Kotlin 反例/正例代码。

## Requirements

### Requirement: 规则清单覆盖维度
规则清单 SHALL 覆盖主线程、启动、UI 渲染、内存、网络、磁盘 IO、后台电量、协程线程、包体依赖、可观测性、WebView 性能、架构与模块化共 12 个维度。§10.3 下 SHALL 包含 Compose 专项子维度（10.3.A），使用 `CP-` 前缀 ID。

#### Scenario: 主线程维度包含 WebView 检查
- **WHEN** 审查涉及 WebView 代码
- **THEN** MT-06 规则 SHALL 检测 WebView/JS Bridge 主线程重操作

#### Scenario: 架构维度存在
- **WHEN** 统计 §10 主维度数量
- **THEN** SHALL = 12（含 §10.12 架构与模块化）

#### Scenario: Compose 子维度规则数
- **WHEN** 统计 10.3.A Compose 专项中 `CP-` 前缀规则
- **THEN** SHALL = 8 条

### Requirement: P0 规则覆盖率
P0 级别规则 SHALL 覆盖以下高危场景：主线程 IO/网络/计算/Broadcast/WebView、Activity/Context 泄漏、Handler 泄漏、监听未取消、前台服务类型缺失、runBlocking 滥用。

#### Scenario: P0 规则总数
- **WHEN** 统计 §10 中 P0 规则数量
- **THEN** SHALL ≥ 10 条

### Requirement: 真实错误案例嵌入
规则反例/正例代码片段 SHALL 使用可编译的 Kotlin 代码（≥ 2 行反例 + ≥ 2 行正例），来源 SHALL 优先为 Android 官方文档、真实生产事故复盘或 Kotlin 编码规范。反例列 SHALL 以 ` ```kotlin ` 代码块开头。

#### Scenario: 协程案例来源一致
- **WHEN** 验证 TH-05 / MEM-02 的反例代码
- **THEN** SHALL 展示可编译的 Kotlin 代码片段，且模式与生产环境中导致 ANR/泄漏的实际代码一致

#### Scenario: P2 规则代码片段
- **WHEN** P2 级别规则无标准 Kotlin 代码反例（如 ST-04 启动埋点）
- **THEN** SHALL 提供 BuildConfig/注解/配置文件等层面的代码示例作为替代
