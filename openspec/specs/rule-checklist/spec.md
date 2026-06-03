# rule-checklist Specification

## Purpose
TBD - created by archiving change prd-v13-optimization. Update Purpose after archive.
## Requirements
### Requirement: 规则清单覆盖维度
规则清单 SHALL 覆盖主线程、启动、UI 渲染、内存、网络、磁盘 IO、后台电量、协程线程、包体依赖、可观测性、WebView 性能共 11 个维度。每维度规则数 SHALL 不少于原始基线。

#### Scenario: 主线程维度包含 WebView 检查
- **WHEN** 审查涉及 WebView 代码
- **THEN** MT-06 规则 SHALL 检测 WebView/JS Bridge 主线程重操作

#### Scenario: 协程维度包含 runBlocking 检查
- **WHEN** 审查涉及 Kotlin 协程代码
- **THEN** TH-05 规则 SHALL 检测 runBlocking 在主线程路径的调用

### Requirement: P0 规则覆盖率
P0 级别规则 SHALL 覆盖以下高危场景：主线程 IO/网络/计算/Broadcast/WebView、Activity/Context 泄漏、Handler 泄漏、监听未取消、前台服务类型缺失、runBlocking 滥用。

#### Scenario: P0 规则总数
- **WHEN** 统计 §10 中 P0 规则数量
- **THEN** SHALL ≥ 10 条，覆盖 ANR、崩溃、内存严重泄漏、系统拒绝服务等场景

