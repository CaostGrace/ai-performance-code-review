## ADDED Requirements

### Requirement: 第一层路由 — 路径/关键字粗筛
Skill 启动后 SHALL 对每个变更文件执行关键字扫描（grep），基于 §6.1 路径启发式和 §6.2 影响半径确定应加载的维度规则文件。匹配逻辑 SHALL 包含文件路径匹配和代码内容关键字匹配两个维度。

#### Scenario: 路径匹配触发
- **WHEN** 变更文件路径包含 `Application`、`ContentProvider` 关键字
- **THEN** SHALL 加载 `startup.md` 规则文件

#### Scenario: 代码关键字匹配触发
- **WHEN** 变更文件内容包含 `@Composable` 关键字
- **THEN** SHALL 加载 `ui-compose.md` 规则文件

#### Scenario: 影响半径扩展
- **WHEN** 变更涉及 `Application.onCreate`
- **THEN** SHALL 联动加载 `startup.md`、`main-thread.md`、`memory.md`

### Requirement: 第二层路由 — P0 必查兜底
无论第一层路由结果如何，Skill SHALL 始终加载 `_must-check.md` 中的 P0 必查规则集。必查规则集 SHALL 分为两级：L0（永远注入）和 L1（按文件语言注入）。

#### Scenario: L0 永远注入
- **WHEN** 任何类型的代码变更触发审查
- **THEN** MEM-01（Activity/Context 泄漏）、MEM-02（生命周期取消）、TH-05（runBlocking 主线程）SHALL 始终参与审查

#### Scenario: L1 按文件语言注入
- **WHEN** 变更文件为非资源文件（.kt/.java/.xml 非纯资源）
- **THEN** MT-01/02/03/06、BG-01/05、ST-01、IO-01 SHALL 参与审查
- **WHEN** 变更文件仅为纯资源文件（strings.xml、colors.xml、图片资源等）
- **THEN** L1 规则 SHALL 不注入

### Requirement: 文件级语言体系识别
路由 SHALL 对每个变更文件执行语言体系识别，根据关键字区分 View 体系和 Compose 体系，按文件分别加载对应规则子集。

#### Scenario: Compose 文件识别
- **WHEN** 文件内容包含 `@Composable` 或 `Composable` 关键字
- **THEN** 该文件 SHALL 标记为 Compose 体系，加载 `ui-compose.md`

#### Scenario: View 文件识别
- **WHEN** 文件内容包含 `RecyclerView`、`findViewById`、`<LinearLayout` 等 View 体系关键字
- **THEN** 该文件 SHALL 标记为 View 体系，加载 `ui-view.md`

#### Scenario: 混合体系
- **WHEN** 同一文件同时包含 View 和 Compose 关键字
- **THEN** SHALL 同时加载 `ui-view.md` 和 `ui-compose.md`

#### Scenario: 非 UI 文件
- **WHEN** 文件既不包含 View 也不包含 Compose 关键字
- **THEN** SHALL 不加载 UI 体系专用规则（`ui-view.md`、`ui-compose.md`）
