# Android 性能 AI Code Review

本 Skill 对 Android 代码变更（Java/Kotlin）进行静态性能审查，覆盖主线程、启动、UI 渲染、内存、网络、磁盘 I/O、后台电量、协程线程、包体依赖、可观测性、WebView、架构共 12 个维度，81 条规则。

## 触发方式

- **自动模式**：直接调用 Skill，未 @ 文件时自动获取 `git diff`（已暂存 + 未暂存）
- **手动模式**：@ 指定文件或目录，仅审查指定范围

## 审查流程

### 第一步：确定输入范围并预扫描

1. 若用户 @ 了文件 → 审查指定文件；否则执行 `git diff` 获取变更集
2. 若 `git diff` 为空 → 提示"无代码变更可审查"，终止
3. 对每个变更文件执行**关键字预扫描**，识别：
   - **语言体系标记**（仅决定是否加载 UI 专项规则）：含 `@Composable` / `Composable` → Compose；含 `RecyclerView` / `findViewById` / `onCreateViewHolder` → View。两者都不含 → 不加载 UI 专项规则；两者都含 → 同时加载
   - **路径特征**：匹配 §6.1 路径启发式规则（决定加载哪些维度规则，独立于语言体系标记）
   - **影响半径**：匹配 §6.2 影响半径规则（扩展维度）
   > 注意：路由表中的 Compose 相关关键字（如 `LazyColumn`、`LaunchedEffect`）属于维度路由触发条件，独立于语言体系标记
4. 判断文件是否为纯资源文件（路径在 `res/values*/`、`res/drawable*/` 等，仅含 strings/colors/dimens 类）

### 第二步：动态路由加载规则文件

**第一层 — 粗筛**：根据预扫描结果，从 `rules/` 目录加载对应的维度规则文件：

| 路径/关键字特征 | 加载规则文件 |
|-----------------|-------------|
| 含 `Application`, `ContentProvider`, `Startup` | `startup.md` |
| 含 `Activity`, `Fragment` + `onCreate`/`onResume`/`LaunchedEffect` | `main-thread.md`, `startup.md` |
| 含 `RecyclerView`, `Adapter`, `onCreateViewHolder` | `ui-view.md`, `memory.md` |
| 含 `@Composable`, `LazyColumn`, `LaunchedEffect`, `derivedStateOf` | `ui-compose.md`, `memory.md` |
| 含 `OkHttp`, `Retrofit`, `suspend` + 网络层 | `network.md`, `main-thread.md` |
| 含 `SharedPreferences`, `DataStore`, `Room`, `File` IO | `disk-io.md`, `main-thread.md` |
| 含 `WorkManager`, `Service`, `AlarmManager`, `BroadcastReceiver` | `background.md` |
| 含 `Dispatchers`, `CoroutineScope`, `Flow`, `runBlocking`, `async` | `threading.md` |
| 含 `build.gradle`, `build.gradle.kts` | `package.md`, `startup.md` |
| 含 `proguard-rules.pro`, R8 配置变更 | `package.md` |
| 含 JNI, `.cpp`, `.c`, `System.loadLibrary` | `main-thread.md`, `memory.md`, `threading.md` |
| 含 `WebView`, `WebViewClient`, `@JavascriptInterface` | `webview.md` |
| 含 `minSdk`, `targetSdk`, `compileSdk` 变更 | `background.md`, `package.md` |
| 含 AIDL, `ContentProvider`（跨进程）, `SharedMemory`, `SplitInstallManager` | `architecture.md`, `background.md` |
| 含 `implementation`, `api` project 依赖变更 | `architecture.md`, `package.md`, `startup.md` |
| 含 `AndroidManifest.xml` 新增组件 | `background.md`, `startup.md` |
| ViewModel/Presenter 基类变更 | `memory.md`, `threading.md` |
| 自定义 View 基类变更 | `ui-view.md`（onDraw 分配、布局层级） |
| Compose Design System 基础组件变更 | `ui-compose.md`（CP-04 Modifier, CP-05 CompositionLocal, CP-06 Lambda） |

**第二层 — P0 必查兜底**：无论路由结果，始终加载 `rules/_must-check.md`：
- **L0（永远注入）**：MEM-01, MEM-02, TH-05
- **L1（按文件语言注入）**：MT-01, MT-02, MT-03, MT-06, BG-01, BG-05, ST-01, IO-01（仅在非资源文件变更时注入）

### 第三步：加载外置规则

按以下顺序检查并加载（后加载的同 ID 规则覆盖内置）：
1. `<项目根>/.android-performance-cr/overrides.md`
2. `<项目根>/.android-performance-cr/custom-rules.md`

overrides.md 支持：`disable`（禁用规则）、`override`（仅改变等级，不改判定条件，P0↔P1↔P2）、`add`（追加新规则）

### 第四步：逐规则审查

按已加载的规则文件逐条审查。使用**三重判定逻辑**：

| 匹配度 | 代码位置明确 | 行为 |
|--------|-------------|------|
| **精确匹配反例** | 是 | 按规则原等级报告（P0/P1/P2） |
| **模式可疑但不确定** | 是 | 降一级报告（P0→P1，P1→P2），在说明中标注"需人工确认" |
| **架构担忧无代码证据** | 否 | 写入「未覆盖/需人工」，不报告等级 |

**盲区处理**：遇到以下类型时不得臆造 P0，必须写入「未覆盖/需人工」：
- Native 内存分配（JNI malloc/new）、JNI 调用耗时、反射调用
- 动态代理/AOP、运行时配置变化、第三方 SDK 内部行为
- 线程调度实际分布、硬件相关性能、ProGuard/R8 实际效果

### 第五步：P0 清零与 OBS-01

- **P0 清零**：要求开发者修复后重跑 Skill 才能清 P0，不接受纯人工备注声明
- **OBS-01**：发现项为空时，自动在报告末尾追加提示"若改动涉及主线程/启动/内存/IO 路径，建议补充验证方式"

### 第六步：输出报告

严格按以下模板输出，不得增减字段。报告写入 `./android-performance-cr-report.md`，每次覆盖。

---

## 输出模板（强制）

```markdown
## Android 性能 CR 摘要

- **改动类型**：（AI 根据变更文件推断）
- **触发通道**：`local-agent`
- **AI 模型/版本**：（由调用方注入）
- **扫描范围**：full / reduced（注明依据）
- **已查维度**：（列出本次加载的维度文件）
- **审查耗时**：（秒）
- **合入建议**：通过 / 修复后合入 / 阻塞（存在未解决 P0）

### 发现项

| 规则 ID | 等级 | 文件:行 | 说明 | 建议 |
|---------|------|---------|------|------|
| MT-01 | P0 | FooActivity.kt:42 | 主线程同步读 SP | 改为 apply/DataStore |

### 未覆盖/需人工

- （如：仅改 ProGuard 规则，无法静态判断启动影响。建议 APK Analyzer 比对包体）

### 验证建议（OBS-01）

- （若 PR 未说明性能验证方式，AI 自动提示）
```

**格式校验规则**：
- `合入建议` 字段必须存在，值为"通过"/"修复后合入"/"阻塞（存在未解决 P0）"
- 发现项表格必须含表头行 `| 规则 ID | 等级 | 文件:行 | 说明 | 建议 |` + 分隔行
- 每条 P0 发现项的文件:行列必须包含具体文件名和行号（如 `FooActivity.kt:42`）

## 规则等级说明

| 等级 | 代号 | 含义 | CR 行为 |
|------|------|------|---------|
| P0 | Blocker | 高概率导致 ANR、崩溃、严重卡顿或内存失控 | **必须修复**方可合入 |
| P1 | Should Fix | 明显性能劣化或坏味道 | 修复或建 Issue 约定时间 |
| P2 | Nice to Have | 优化建议 | 建议采纳，不阻塞合入 |
