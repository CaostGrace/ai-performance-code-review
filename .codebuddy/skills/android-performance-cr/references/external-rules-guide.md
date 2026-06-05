# 外置规则编写指南

> 本指南教你如何通过 `.android-performance-cr/` 定制审查行为，无需修改 Skill 内置规则。

## 1. 概述

### 什么时候用外置规则

- ✅ 团队有特殊场景，内置规则的 P0/P1 等级不适用
- ✅ 需要添加项目特有的性能规范
- ✅ 内置规则判定条件太严或太松
- ❌ 需要修改判定条件（如"耗时 < 200ms 不算违规"）→ 走 custom-rules.md 的 `add`
- ❌ 想要永久修改内置规则 → 应提交 PR 到 Skill 仓库

### 两种文件

| 文件 | 用途 | 格式 |
|------|------|------|
| `overrides.md` | 覆盖内置规则（改等级/禁用） | 4 列：操作 \| 规则ID \| 新等级 \| 说明 |
| `custom-rules.md` | 追加项目专用规则 | 7 列：ID \| 等级 \| 检查项 \| 反例 \| 正例 \| 判定 \| 参考工具 |

### 加载顺序

```
Skill 启动
  → 1. 加载 overrides.md（覆盖内置规则等级）
  → 2. 加载 custom-rules.md（追加新规则）
  → 3. 加载内置规则集（作为兜底）

后加载的同 ID 规则覆盖先加载的。即：custom-rules.md 中的规则 > 内置规则
```

---

## 2. overrides.md 操作手册

### 2.1 格式

```markdown
| 操作 | 规则 ID | 新等级 | 说明 |
|------|--------|--------|------|
```

### 2.2 disable — 禁用某条规则

**用途**：当内置规则对项目不适用时，完全跳过该规则的检查。

> ✅ **正例：禁用 MEM-03（大图按采样加载）**

如果项目使用 Glide/Coil 等图片加载框架，框架已内置自动降采样，MEM-03 每次都会误报：

```markdown
| 操作 | 规则 ID | 新等级 | 说明 |
|------|--------|--------|------|
| disable | MEM-03 | — | 项目使用 Glide 统一图片加载，框架已自动降采样，MEM-03 误报率高 |
```

> ❌ **反例：误禁用 ST-01**

ST-01 是 P0 规则（Application 同步初始化），即使团队认为"启动性能不是重点"，直接禁用会导致严重的启动劣化：

```markdown
| 操作 | 规则 ID | 新等级 | 说明 |
|------|--------|--------|------|
| disable | ST-01 | — | <!-- ❌ P0 规则不应轻率禁用 --> |
```

**建议**：P0 规则慎用 disable，优先考虑 override 降级为 P1。

### 2.3 override — 改变规则等级

**用途**：调整内置规则的等级（P0 ↔ P1 ↔ P2），但不改变检查项和判定条件。

> ✅ **正例：ST-01 P0 降为 P1**

如果项目的启动 SDK 初始化已在 CI 基线中计量，且不允许退步：

```markdown
| 操作 | 规则 ID | 新等级 | 说明 |
|------|--------|--------|------|
| override | ST-01 | P1 | 启动初始化已在 CI 基线中计量，P0 过严；改为 P1 建 Issue 跟进 |
```

> ❌ **反例：试图 override 改判定条件**

有的团队想"ST-01 中如果初始化 < 200ms 就不报"，但 override 只能改等级，不能改判定条件。这种情况应该用 `custom-rules.md` 的 `add` 新增一条规则：

```markdown
| 操作 | 规则 ID | 新等级 | 说明 |
|------|--------|--------|------|
| override | ST-01 | P1 | <!-- ❌ 想改成"耗时 < 200ms 不报"，但 override 不支持改判定 --> |
```

> ❌ **反例：override 到无效等级**

```markdown
| 操作 | 规则 ID | 新等级 | 说明 |
|------|--------|--------|------|
| override | MT-01 | P10 | <!-- ❌ 不存在 P10 等级 --> |
```

### 2.4 add — 追加新规则（在 overrides.md 中）

**用途**：在 overrides.md 中用 `add` 追加一条新规则。与 custom-rules.md 的 add 等价，但加载优先级更高。

```markdown
| 操作 | 规则 ID | 新等级 | 说明 |
|------|--------|--------|------|
| add | CUSTOM-01 | P0 | （须包含完整七列 ↑ 本列值为占位） |
```

> **注意**：overrides.md 的 `add` 操作仅 4 列，**不包含完整规则定义**。如果需要完整七列的新规则，请使用 `custom-rules.md`。

---

## 3. custom-rules.md — 完整七列新规则

### 3.1 格式

```markdown
| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
```

### 3.2 每一列详解

| 列 | 说明 | 要求 |
|----|------|------|
| **ID** | 规则唯一标识 | 格式 `CUSTOM-NN`（如 CUSTOM-01），避免与内置 ID 冲突 |
| **等级** | P0 / P1 / P2 | P0 = 阻塞合入，P1 = 应修复，P2 = 建议 |
| **检查项** | 一句话描述检查什么 | 简洁明确，说清楚禁止什么或要求什么 |
| **反例** | 违反规则的 Kotlin 代码 | 至少 2 行可编译代码，以 ` ```kotlin ` 开头 |
| **正例** | 符合规则的 Kotlin 代码 | 至少 2 行可编译代码，展示推荐做法 |
| **判定** | 如何判断违规 | 具体条件，如"主线程中调用 xxx()" |
| **参考工具** | 验证工具 | 如 StrictMode、LeakCanary 等，无则填 `—` |

### 3.3 正例：新增一条完整的自定义规则

```markdown
| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| CUSTOM-01 | P1 | ViewModel 禁止直接持有 Context 引用 | ```kotlin
// ❌ ViewModel 直接持有 Activity Context
class MyViewModel : ViewModel() {
    val context: Context = ApplicationContextProvider.get()
    fun loadData() {
        context.getSharedPreferences("app", MODE_PRIVATE)
    }
}
``` | ```kotlin
// ✅ 使用 AndroidViewModel 或 DI 注入
class MyViewModel(
    private val repository: DataRepository
) : ViewModel() {
    fun loadData() {
        repository.loadFromDataStore()
    }
}
``` | ViewModel 构造函数或成员变量直接引用 Context | LeakCanary |
```

### 3.4 反例：常见错误

> ❌ **ID 与内置规则冲突**

```markdown
| MT-01 | P0 | ... | <!-- ❌ MT-01 已被内置规则占用 -->
```

> ❌ **缺少必填列**

```markdown
| CUSTOM-01 | P1 | 检查项描述 | ```kotlin
反例代码
``` | <!-- ❌ 缺少正例、判定、参考工具列 -->
```

> ❌ **反例代码不可编译**

```markdown
| CUSTOM-02 | P1 | 检查项 | ```kotlin
val x = someUnknownFunction() // ❌ 引用了不存在的函数
``` | ...
```

> ❌ **判定条件模糊**

```markdown
| CUSTOM-03 | P1 | ... | ... | ... | 性能不好时触发 | <!-- ❌ "性能不好"太模糊，无法自动判断 --> | — |
```

---

## 4. 真实场景完整示例

### 场景 A：禁用 MEM-03（项目用 Glide）

**背景**：项目统一使用 Glide 加载图片，Glide 自带降采样和内存管理。MEM-03 每次审查都误报。

**文件**：`.android-performance-cr/overrides.md`

```markdown
| 操作 | 规则 ID | 新等级 | 说明 |
|------|--------|--------|------|
| disable | MEM-03 | — | 项目使用 Glide 统一图片加载，框架已自动降采样，MEM-03 误报率 > 80% |
```

**效果**：审查报告中不再出现 MEM-03 发现项。

---

### 场景 B：override ST-01 为 P1

**背景**：项目启动阶段 SDK 初始化耗时已在 CI 中用 Macrobenchmark 监控，不允许退步。ST-01 报 P0 过于严格，每次都要 Team Leader 签字例外。

**文件**：`.android-performance-cr/overrides.md`

```markdown
| 操作 | 规则 ID | 新等级 | 说明 |
|------|--------|--------|------|
| override | ST-01 | P1 | 启动 SDK 初始化耗时已在 CI Macrobenchmark 中计量，P0 严格模式改为 P1 建 Issue 跟进 |
| override | ST-05 | P2 | Provider 初始化已有异步框架，P1 降为 P2 建议 |
```

**效果**：ST-01 不再阻塞合入，但仍会在报告中提示建 Issue。

---

### 场景 C：新增一条自定义规则

**背景**：项目发现多次线上事故是由于开发者在协程中吞掉了异常，导致静默失败。需要新增一条规则检查。

**文件**：`.android-performance-cr/custom-rules.md`

```markdown
| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| CUSTOM-01 | P0 | 协程中禁止空 catch 吞异常 | ```kotlin
// ❌ 空 catch 吞掉异常
viewModelScope.launch {
    try {
        val data = apiService.fetchData()
    } catch (e: Exception) {
        // 静默失败，用户看到空白页
    }
}
``` | ```kotlin
// ✅ 记录日志 + 通知用户
viewModelScope.launch {
    try {
        val data = apiService.fetchData()
    } catch (e: Exception) {
        Log.e(TAG, "Failed to fetch data", e)
        _uiState.emit(UiState.Error(e.message))
    }
}
``` | catch 块为空或仅含注释，未处理异常 | — |
| CUSTOM-02 | P2 | 大列表数据类应实现 equals/hashCode | ```kotlin
// ❌ data class 但用于 RecyclerView DiffUtil
data class User(
    val id: String,
    val name: String,
    val avatar: String,
    val bio: String,
    val followers: Int
)
``` | ```kotlin
// ✅ 简单 data class 即可正确生成 equals/hashCode
// Kotlin data class 自动生成 equals, hashCode, toString, copy
// 确保 DiffUtil 正常比较
data class User(
    val id: String,
    val name: String
)
``` | DiffUtil 中使用了 data class 的 equals 比较 | — |
```

**效果**：审查时，CUSTOM-01 和 CUSTOM-02 与内置规则同权重参与审查，CUSTOM-01 为 P0 会阻塞合入。

---

## 5. 常见错误和 FAQ

### Q: custom-rules.md 可以改内置规则的等级吗？
**A**: 不可以。改等级用 `overrides.md` 的 `override`，追加新规则用 `custom-rules.md`。

### Q: overrides.md 和 custom-rules.md 的 add 有什么区别？
**A**: overrides.md 的 add 仅 4 列，用于简单追加（不包含代码示例）。custom-rules.md 的规则需完整七列（含反例正例），推荐用 custom-rules.md。

### Q: 多个项目共用一个 Skill，外置规则怎么隔离？
**A**: 外置规则文件放在**各项目仓库根目录**的 `.android-performance-cr/` 下。切换项目时 Skill 会自动加载对应项目的外置规则。

### Q: 外置规则 ID 和内置规则 ID 冲突会怎样？
**A**: custom-rules.md 中的规则加载在内置规则之后，同 ID 会覆盖内置规则。建议使用 `CUSTOM-NN` 前缀避免冲突。

### Q: 如何验证我写的外置规则是否生效？
**A**: 运行一次 Skill 审查，检查报告中的合入建议是否体现了规则变更。例如：disable 了 MEM-03 后，相关代码不应再触发 MEM-03。
