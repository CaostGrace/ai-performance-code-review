## ADDED Requirements

### Requirement: Compose 文件识别
Skill SHALL 通过扫描文件内容中的 `@Composable` 或 `Composable` 关键字识别 Compose 体系文件，为其加载 `ui-compose.md` 规则。

#### Scenario: 识别 @Composable 函数
- **WHEN** 文件包含 `@Composable fun Screen(` 声明
- **THEN** SHALL 标记为 Compose 文件

#### Scenario: 识别 Composable lambda
- **WHEN** 文件包含 `content: @Composable () -> Unit` 参数类型
- **THEN** SHALL 标记为 Compose 文件

### Requirement: View 文件识别
Skill SHALL 通过扫描文件内容中的 View 体系关键字（`RecyclerView`、`findViewById`、`<LinearLayout`、`ViewGroup`、`Adapter`、`onCreateViewHolder`）识别 View 体系文件。

#### Scenario: 识别 RecyclerView 使用
- **WHEN** 文件包含 `RecyclerView.Adapter` 或 `onCreateViewHolder` 方法
- **THEN** SHALL 标记为 View 文件

#### Scenario: 识别布局引用
- **WHEN** 文件包含 `findViewById` 或 `R.layout.` 引用
- **THEN** SHALL 标记为 View 文件

### Requirement: 规则文件选择性加载
对标记为 Compose 的文件 SHALL 不应用 View 专用规则（UI-01 ViewHolder、UI-02 布局层级、UI-08 notifyDataSetChanged 等）。对标记为 View 的文件 SHALL 不应用 Compose 专用规则（CP-01~CP-08）。

#### Scenario: Compose 文件不加载 View 规则
- **WHEN** 变更文件为纯 Compose 文件
- **THEN** `ui-view.md` SHALL 不加载，CP-01~CP-08 SHALL 加载

#### Scenario: View 文件不加载 Compose 规则
- **WHEN** 变更文件为纯 View 文件
- **THEN** `ui-compose.md` SHALL 不加载，UI-01~UI-09 SHALL 加载
