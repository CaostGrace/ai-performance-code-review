# Compose 专项

> §9.3.A Compose 专项规则。规则 ID 前缀 `CP-`。仅在识别到 Compose 关键字（`@Composable`）时加载。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| CP-01 | P1 | LazyColumn/LazyRow key 必须稳定唯一 | ```kotlin
// ❌ 用 index 做隐式 key
LazyColumn { items(list) { Text(it.name) } } // 增删时全量重组
``` | ```kotlin
// ✅ 稳定唯一 key
LazyColumn { items(list, key = { it.id }) { Text(it.name) } }
``` | key 不唯一导致 Diff 低效 | Compose Layout Inspector |
| CP-02 | P1 | 数据类标注 @Stable / @Immutable 注解 | ```kotlin
// ❌ 未标注，Compose 认为不稳定
data class User(val name: String)
``` | ```kotlin
// ✅ 声明稳定性契约
@Immutable data class User(val name: String)
``` | 数据类被频繁重组 | Compose Compiler Metrics |
| CP-03 | P1 | LaunchedEffect key 必须稳定且与内部依赖一致 | ```kotlin
// ❌ key 不随 userId 变
LaunchedEffect(Unit) { loadData(userId) } // 不会重启
``` | ```kotlin
// ✅ key 与内部使用变量一致
LaunchedEffect(userId) { loadData(userId) }
``` | 协程未重启或每次重组都重启 | Compose Layout Inspector |
| CP-04 | P1 | 频繁变化的状态用 lambda 版 Modifier | ```kotlin
// ❌ 组合阶段读滚动状态
Modifier.offset(scrollState.value.dp)
``` | ```kotlin
// ✅ 延迟到布局阶段
Modifier.offset { IntOffset(0, scrollState.value) }
``` | Systrace 显示频繁重组帧 | Systrace |
| CP-05 | P1 | CompositionLocal 提供范围限制在最小子树 | ```kotlin
// ❌ 全屏提供
CompositionLocalProvider(LocalX provides val) {
    EntireScreen() // 全树重组
}
``` | ```kotlin
// ✅ 限制到需要的子树
Column {
    CompositionLocalProvider(LocalX provides val) {
        ChildComposable()
    }
}
``` | CompositionLocal 变更时重组范围过大 | Compose Layout Inspector |
| CP-06 | P1 | Composable lambda 参数使用 remember 缓存 | ```kotlin
// ❌ 每次重组分配新 lambda
Button(onClick = { doSomething(item) }) { Text("Go") }
``` | ```kotlin
// ✅ remember 缓存 lambda
val onClick = remember(item) { { doSomething(item) } }
Button(onClick = onClick) { Text("Go") }
``` | 子组件因 lambda 引用变化频繁重组 | Compose Compiler Metrics |
| CP-07 | P2 | 避免在频繁重组区域使用 SubcomposeLayout | ```kotlin
// ❌ LazyColumn 中 SubcomposeLayout
LazyColumn {
    item { SubcomposeLayout { ... } } // 每项触发子组合
}
``` | ```kotlin
// ✅ 用标准布局替代
LazyColumn {
    item { Column { ... } }
}
``` | 每次重组触发子组合 | Compose Layout Inspector |
| CP-08 | P1 | 派生状态使用 derivedStateOf 而非直接计算 | ```kotlin
// ❌ 直接 filter 计算
@Composable fun List(items: List<Item>) {
    val active = items.filter { it.active } // 每次重组全算
}
``` | ```kotlin
// ✅ derivedStateOf
@Composable fun List(items: List<Item>) {
    val active by remember { derivedStateOf { items.filter { it.active } } }
}
``` | 基于 State 的计算触发多余重组 | Compose Layout Inspector |
