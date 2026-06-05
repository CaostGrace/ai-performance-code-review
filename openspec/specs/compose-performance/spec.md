# compose-performance Specification

## Purpose
定义 Compose 专项性能审查规则，覆盖重组范围、稳定性注解、Effect key、Modifier 优化、derivedStateOf 等核心 Compose 性能场景。

## Requirements

### Requirement: Compose 规则覆盖基本性能场景
Compose 专项规则 SHALL 覆盖至少 8 个独立性能检查场景，使用独立 `CP-` 前缀 ID，归入 §9.3.A 子维度。规则 SHALL 包含完整的七列定义（ID、等级、检查项、反例、正例、判定、参考工具）。

#### Scenario: LazyColumn key 稳定性检查
- **WHEN** 审查涉及 `LazyColumn` 或 `LazyRow` 的 `items()` 调用
- **THEN** CP-01 规则 SHALL 检测是否传入稳定的 key 参数（非 index），确保增删项时 Diff 算法高效

#### Scenario: 数据类稳定性注解检查
- **WHEN** 审查 Compose 中作为 State 的数据类定义
- **THEN** CP-02 规则 SHALL 检测是否标注 `@Stable` 或 `@Immutable` 注解，避免不必要的全树重组

#### Scenario: LaunchedEffect key 稳定性检查
- **WHEN** 审查 `LaunchedEffect(key)` 调用
- **THEN** CP-03 规则 SHALL 检测 key 参数是否与内部使用的变量一致，防止协程遗漏重启或不必要重启

#### Scenario: Modifier lambda 版本检查
- **WHEN** 审查 Modifier 中读取可变状态（如 `scrollState.value`）的代码
- **THEN** CP-04 规则 SHALL 建议使用 lambda 版 Modifier（如 `Modifier.offset { ... }`），使状态读取延迟到布局阶段

#### Scenario: CompositionLocal 范围检查
- **WHEN** 审查 `CompositionLocalProvider` 的使用
- **THEN** CP-05 规则 SHALL 检测是否将 Provider 范围限制在最小必要子树，避免全树重组

#### Scenario: Lambda 缓存检查
- **WHEN** 审查 Composable 函数中传递给子组件的 lambda 表达式
- **THEN** CP-06 规则 SHALL 建议使用 `remember` 缓存 lambda，避免每次重组分配新对象

#### Scenario: SubcomposeLayout 使用检查
- **WHEN** 审查 `SubcomposeLayout` 的使用
- **THEN** CP-07 规则 SHALL 检测是否滥用或在频繁重组场景中使用，提示性能风险

#### Scenario: derivedStateOf 使用检查
- **WHEN** 审查基于其他 State 的计算逻辑
- **THEN** CP-08 规则 SHALL 建议使用 `derivedStateOf` 替代在 Composable 中直接计算，避免不必要的重组

### Requirement: Compose 规则与 UI 通用规则共存
Compose 规则（CP-前缀）SHALL 与 View 体系 UI 通用规则（UI-前缀）在 §9.3 维度的同一表中展示，通过 ID 前缀区分。AI 审查时 SHALL 按 §6 路径启发式同时激活 `Composable`/`@Composable` 关键字映射到 Compose 规则子集。

#### Scenario: Compose 代码同时触发 UI 和 CP 规则
- **WHEN** 审查包含 `@Composable` 注解和 `RecyclerView` 的混合代码
- **THEN** 审查引擎 SHALL 同时激活 CP- 规则（检测 Compose 性能）和 UI- 规则（检测 View 性能）

### Requirement: Compose 规则包含真实错误案例
CP-01 至 CP-08 每条规则 SHALL 在反例/正例中提供可编译的 Kotlin 代码片段（至少 2 行），来源 SHALL 包含官方文档最佳实践和社区真实事故案例。

#### Scenario: 反例代码可识别
- **WHEN** AI 审查器读取 CP 规则的正例/反例代码
- **THEN** 代码片段 SHALL 包含足够上下文使 AI 能通过模式匹配在 diff 中识别相似模式
