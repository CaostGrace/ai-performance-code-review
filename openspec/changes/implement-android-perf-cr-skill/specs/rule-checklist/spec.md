## MODIFIED Requirements

### Requirement: 规则清单覆盖维度
规则清单 SHALL 覆盖主线程、启动、UI 渲染、内存、网络、磁盘 IO、后台电量、协程线程、包体依赖、可观测性、WebView 性能、架构与模块化共 12 个维度。§9.3 下 SHALL 包含 Compose 专项子维度（9.3.A），使用 `CP-` 前缀 ID。规则 SHALL 从单体 PRD 文档拆分为 14 个独立维度文件 + 1 个 P0 必查规则文件。

#### Scenario: 涉及 WebView 代码时，MT-06 规则 SHALL 检测 WebView/JS Bridge 主线程重操作。
- **WHEN** 变更包含 WebView 相关代码
- **THEN** MT-06 SHALL 被加载（通过路由或必查规则集）

#### Scenario: §9 主维度数量 SHALL = 12（含 §9.12 架构与模块化）。
- **WHEN** 统计 Skill 加载的维度规则文件
- **THEN** 维度文件 SHALL = 14 个（12 维度 + 1 Compose 子维度 + 1 必查规则集）

#### Scenario: 9.3.A Compose 专项中 `CP-` 前缀规则 SHALL = 8 条。
- **WHEN** 加载 `ui-compose.md`
- **THEN** CP-01 到 CP-08 SHALL 全部包含

### Requirement: P0 规则覆盖率
P0 级别规则 SHALL 覆盖以下高危场景：主线程 IO/网络/计算/Broadcast/WebView、Activity/Context 泄漏、Handler 泄漏、监听未取消、前台服务类型缺失、runBlocking 滥用。

#### Scenario: §9 中 P0 规则数量 SHALL ≥ 10 条。
- **WHEN** 统计全部规则文件中的 P0 规则
- **THEN** SHALL ≥ 10 条

## ADDED Requirements

### Requirement: P0 必查规则集
Skill SHALL 包含独立的 `_must-check.md` 文件，包含 L0（永远注入）和 L1（按文件语言注入）两级 P0 必查规则。L0 SHALL 包含 MEM-01、MEM-02、TH-05。L1 SHALL 包含 MT-01/02/03/06、BG-01/05、ST-01、IO-01。

#### Scenario: L0 永远参与审查
- **WHEN** 任何类型的代码变更触发审查
- **THEN** L0 规则（MEM-01/02、TH-05）SHALL 始终被加载

#### Scenario: L1 按文件类型注入
- **WHEN** 变更文件为 `.kt` 或 `.java` 文件
- **THEN** L1 规则 SHALL 被加载
- **WHEN** 变更文件仅为资源文件
- **THEN** L1 规则 SHALL 不被加载

### Requirement: 规则按维度拆分文件
81 条规则 SHALL 拆分为 14 个独立 `.md` 文件，按 §9 维度组织：`main-thread.md`、`startup.md`、`ui-view.md`、`ui-compose.md`、`memory.md`、`network.md`、`disk-io.md`、`background.md`、`threading.md`、`package.md`、`observability.md`、`webview.md`、`architecture.md`，加 `_must-check.md`。

#### Scenario: 规则文件映射
- **WHEN** 路由决策加载 `main-thread.md`
- **THEN** SHALL 包含 MT-01 到 MT-07 全部 7 条规则
