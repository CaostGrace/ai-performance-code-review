## 1. §11 兜底规则转正

- [x] 1.1 ST-07：创建 Baseline Profile 检查规则（P0→降为P1），包含反例（启动路径改动但缺少 baseline-prof.txt）、正例、判定标准
- [x] 1.2 PKG-06：创建 16KB 页大小对齐规则（P1），检测 Native .so ELF 对齐，引用 Google Play 合规文档
- [x] 1.3 UI-09：创建 RecyclerView DiffUtil/预取规则（P1），反例为 `notifyDataSetChanged` 全局刷新，正例为 `ListAdapter` + `DiffUtil`
- [x] 1.4 MEM-08：创建大图与硬件位图规则（P1），反例为全分辨率解码、未使用 `Bitmap.Config.HARDWARE`
- [x] 1.5 将 CP-02（@Stable/@Immutable）和 ARCH-01（组件化通信开销）分别归入 Compose 子维度和架构维度任务中
- [x] 1.6 移除 PRD §11「后续可选规则」章节内容

## 2. Compose 专项子维度（10.3.A）

- [x] 2.1 CP-01：创建 LazyColumn key 稳定性规则（P1），反例为 `items(list)` 无 key，正例为 `items(list, key = { it.id })`
- [x] 2.2 CP-02：创建 @Stable/@Immutable 注解规则（P1），反例为未标注的 data class 被频繁重组
- [x] 2.3 CP-03：创建 LaunchedEffect key 稳定性规则（P1），反例为 `LaunchedEffect(Unit)` 包裹依赖外部变量的逻辑
- [x] 2.4 CP-04：创建 Modifier lambda 版本选择规则（P1），反例为 `Modifier.offset(state.value)` 在组合阶段读状态
- [x] 2.5 CP-05：创建 CompositionLocal 范围限制规则（P1），反例为全树 Provider
- [x] 2.6 CP-06：创建 Lambda 缓存规则（P1），反例为每次重组分配新 lambda 对象
- [x] 2.7 CP-07：创建 SubcomposeLayout 谨慎使用规则（P2），反例为 LazyColumn 中使用 SubcomposeLayout
- [x] 2.8 CP-08：创建 derivedStateOf 正确使用规则（P1），反例为 Composable 中直接 filter 计算

## 3. §10.12 架构与模块化维度

- [x] 3.1 ARCH-01：创建模块间大对象序列化风险规则（P2），反例为跨模块 Parcelable 大对象传递
- [x] 3.2 ARCH-02：创建模块循环依赖检测规则（P2），反例为 A→B→A 依赖链
- [x] 3.3 ARCH-03：创建 Dynamic Feature 加载时机规则（P1），反例为 Application.onCreate 中 startInstall
- [x] 3.4 ARCH-04：创建多进程 Binder 通信开销规则（P1），反例为高频/大体积 Binder 调用

## 4. §7.4 工具使用速查卡

- [x] 4.1 创建 StrictMode 速查卡：`ThreadPolicy`/`VmPolicy` 启用代码、Logcat 输出解读、常见违规类型与解决方案
- [x] 4.2 创建 Systrace/Perfetto 速查卡：命令行抓取（`adb shell perfetto`）、`ui.perfetto.dev` 打开、Choreographer 帧耗时解读
- [x] 4.3 创建 LeakCanary 速查卡：Gradle 依赖声明、自动触发机制、引用路径图解读
- [x] 4.4 创建 Memory Profiler 速查卡：Android Studio 入口、Heap Dump 抓取与对比、常见泄漏模式
- [x] 4.5 创建 Battery Historian 速查卡：Bugreport 提交方式、耗电排名解读、WakeLock 占用分析
- [x] 4.6 创建 APK Analyzer 速查卡：拖入 APK、DEX/资源/Native 库大小分析、前后版本对比
- [x] 4.7 创建 Database Inspector 速查卡：Android Studio 入口、查询性能分析、表结构检查
- [x] 4.8 创建 Network Profiler 速查卡：请求时间线、连接复用检测、响应体大小分析
- [x] 4.9 创建 Compose Layout Inspector 速查卡：重组计数查看、跳过次数解读、不稳定参数识别

## 5. 真实错误案例补充

- [x] 5.1 补充 TH-05 协程 ANR 案例：`runBlocking { performTask() }` 在 hot path 的生产事故反例代码
- [x] 5.2 补充 MEM-02 GlobalScope 泄漏案例：`GlobalScope.launch` 在 Activity 销毁后仍持有 UI 引用的泄漏反例
- [x] 5.3 补充 MEM-06 Handler 泄漏案例：非静态内部类 Handler 隐式持有 Activity 的反例与 WeakReference 正例
- [x] 5.4 补充 WV-03 WebView 未销毁案例：未调用 destroy() 导致 Native 内存残留数十 MB 的反例
- [x] 5.5 补充 UI-01/UI-09 DiffUtil 案例：`notifyDataSetChanged` vs `ListAdapter` + `DiffUtil` 的对比代码

## 6. 文档结构重组

- [x] 6.1 将 §7.2 Phase 2-4（CI 门禁拦截、指标看板、AI 模型微调）从「自动化路线图」移至 §11「后期处理」
- [x] 6.2 将 §7.3「流水线与本地集成」移至 §11「后期处理」
- [x] 6.3 在 §7 新增明确的「后期处理引用链接」指向 §11
- [x] 6.4 更新 §6 改动类型→规则维度速查映射表（增加 Compose/模块化行）
- [x] 6.5 更新 §6.1 路径启发式映射表（增加 Compose注解、模块依赖关键字）
- [x] 6.6 更新 §8.3 修订记录：增加 v2.0 版本记录

## 7. 最终校验

- [x] 7.1 统计总规则数达成 ≈ 83 条（原 64 + 新增 19）
- [x] 7.2 确认所有 CP- 规则在 §10.3.A 子维度中正确编号
- [x] 7.3 确认所有 ARCH- 规则在 §10.12 中正确编号
- [x] 7.4 确认 §11 已改为「后期处理：流水线与 CI」且不包含规则内容
- [x] 7.5 确认 §7.4 工具速查卡包含全部 9 个工具
