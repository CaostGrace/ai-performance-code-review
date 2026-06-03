# rule-checklist Specification (Delta)

## MODIFIED Requirements

### Requirement: 规则清单覆盖维度
规则清单 SHALL 覆盖主线程、启动、UI 渲染、内存、网络、磁盘 IO、后台电量、协程线程、包体依赖、可观测性、WebView 性能、架构与模块化共 12 个维度。每维度规则数 SHALL 不少于原始基线。§10.3 下 SHALL 包含 Compose 专项子维度（10.3.A），使用 `CP-` 前缀 ID。

#### Scenario: 主线程维度包含 WebView 检查
- **WHEN** 审查涉及 WebView 代码
- **THEN** MT-06 规则 SHALL 检测 WebView/JS Bridge 主线程重操作

#### Scenario: 协程维度包含 runBlocking 检查
- **WHEN** 审查涉及 Kotlin 协程代码
- **THEN** TH-05 规则 SHALL 检测 runBlocking 在主线程路径的调用

#### Scenario: 架构维度存在
- **WHEN** 统计 §10 主维度数量
- **THEN** SHALL = 12（含 §10.12 架构与模块化）

#### Scenario: Compose 子维度规则数
- **WHEN** 统计 10.3.A Compose 专项中 `CP-` 前缀规则
- **THEN** SHALL = 8 条

### Requirement: 真实错误案例嵌入
规则反例/正例代码片段 SHALL 使用可编译的 Kotlin 代码（≥ 2 行反例 + ≥ 2 行正例），来源 SHALL 优先为 Android 官方文档、真实生产事故复盘或 Kotlin 编码规范。

#### Scenario: 协程案例来源一致
- **WHEN** 验证 TH-05 / MEM-02 的反例代码
- **THEN** SHALL 展示可编译的 Kotlin 代码片段，且模式与生产环境中导致 ANR/泄漏的实际代码一致

#### Scenario: P2 规则代码片段
- **WHEN** P2 级别规则无标准 Kotlin 代码反例（如 ST-04 启动埋点）
- **THEN** SHALL 提供 BuildConfig/注解/配置文件等层面的代码示例作为替代

## ADDED Requirements

### Requirement: 代码片段格式统一
反例列 SHALL 以 ````kotlin` 代码块开头，正例列 SHALL 以 ````kotlin` 代码块开头。代码块前 SHALL 用 `// ❌` 和 `// ✅` 注释说明反例/正例的意图。

#### Scenario: 代码块可被 Markdown 解析器正确渲染
- **WHEN** 在 Markdown 编辑器中查看规则表
- **THEN** 反例/正例列 SHALL 显示为语法高亮的 Kotlin 代码块
