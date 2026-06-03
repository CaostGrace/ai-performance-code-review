## 1. 激进清理流水线内容

- [x] 1.1 清理 §1.2 目标 → 移除「双触发通道」描述，改为纯本地 Agent
- [x] 1.2 清理 §1.4 成功指标 → 将「流水线制品」度量改为「审查报告文件」
- [x] 1.3 重写 §3.1 → 移除双通道 Mermaid 图和相关表格，改为纯本地 Agent 说明
- [x] 1.4 清理 §3.2 输入 → 删除「通道 A（流水线）」列，仅保留本地 Agent 输入
- [x] 1.5 清理 §3.3 输出 → 投递方式从「流水线制品库」改为「本地 Markdown 文件」；触发通道固定为 `local-agent`
- [x] 1.6 清理 §3.4 Skill 文件结构 → 移除「流水线均引用同一规则集」描述
- [x] 1.7 清理 §3.6 审查规模与 SLA → 整个章节移入 §13（流水线相关）
- [x] 1.8 重绘 §5 CR 流程图 → 改为 Developer → 本地 Skill → Markdown 输出
- [x] 1.9 清理 §5.1 审查步骤 → 移除通道 A 超时保护和大文件模式引用
- [x] 1.10 清理 §6 映射表 → 删除「通道 A/通道 B」双列
- [x] 1.11 清理 §7.2 → 删除 Phase 1-4 表，仅保留 Phase 0
- [x] 1.12 清理 §9 开放问题 → 移除流水线 Job 调用方式等流水线相关问题
- [x] 1.13 将 §11 重命名为 §13「后期展望」→ 汇集所有清理出的流水线内容

## 2. §10.1 主线程规则代码增强

- [x] 2.1 MT-01：补全同步磁盘 IO 反例/正例代码（`File.readText` → `Dispatchers.IO`）
- [x] 2.2 MT-02：补全同步网络反例/正例代码（`OkHttp.execute()` → Retrofit suspend）
- [x] 2.3 MT-03：补全主线程大计算反例/正例代码（JSON 解析 → `withContext`）
- [x] 2.4 MT-04：补全 BroadcastReceiver 长任务反例/正例代码（`goAsync()`）
- [x] 2.5 MT-05：补全主线程锁等待反例/正例代码（synchronized → 无锁/CAS）
- [x] 2.6 MT-06：补全 WebView 主线程重操作反例/正例代码
- [x] 2.7 MT-07：补全系统服务主线程重操作反例/正例代码

## 3. §10.2 启动规则代码增强

- [x] 3.1 ST-01：补全 Application onCreate 同步初始化反例/正例代码
- [x] 3.2 ST-02：补全 ContentProvider 滥用反例/正例代码
- [x] 3.3 ST-03：补全首屏阻塞绘制反例/正例代码（骨架屏 + 异步加载）
- [x] 3.4 ST-04：补全启动埋点反例/正例代码（BuildConfig/注解示例）
- [x] 3.5 ST-05：补全 ContentProvider.onCreate 同步初始化反例/正例代码
- [x] 3.6 ST-06：补全静态字段重对象反例/正例代码（companion object → IdleHandler）
- [x] 3.7 ST-07：补全 Baseline Profile 检查反例/正例代码

## 4. §10.3 UI 渲染规则代码增强

- [x] 4.1 UI-01：补全 ViewHolder 不复用反例/正例代码（RecyclerView Adapter）
- [x] 4.2 UI-02：补全布局层级过深反例/正例代码（LinearLayout → ConstraintLayout）
- [x] 4.3 UI-03：补全 onDraw 分配对象反例/正例代码（new Paint → 成员复用）
- [x] 4.4 UI-04：补全过度 invalidate 反例/正例代码（全屏 → 局部刷新）
- [x] 4.5 UI-05：补全 Compose 重组范围过大反例/正例代码
- [x] 4.6 UI-06：补全动画硬件加速反例/正例代码（clipChildren）
- [x] 4.7 UI-07：补全 remember 无 key 反例/正例代码
- [x] 4.8 UI-08：补全 notifyDataSetChanged 反例/正例代码
- [x] 4.9 UI-09：补全 DiffUtil 缺失反例/正例代码

## 5. §10.3.A Compose 规则代码增强

- [x] 5.1 CP-01：补全 LazyColumn key 不稳定反例/正例代码
- [x] 5.2 CP-02：补全 @Stable/@Immutable 缺失反例/正例代码
- [x] 5.3 CP-03：补全 LaunchedEffect key 错误反例/正例代码
- [x] 5.4 CP-04：补全 Modifier 非 lambda 版反例/正例代码
- [x] 5.5 CP-05：补全 CompositionLocal 全树提供反例/正例代码
- [x] 5.6 CP-06：补全 lambda 未缓存反例/正例代码
- [x] 5.7 CP-07：补全 SubcomposeLayout 滥用反例/正例代码
- [x] 5.8 CP-08：补全 derivedStateOf 未用反例/正例代码

## 6. §10.4 内存规则代码增强

- [x] 6.1 MEM-01：补全 Activity/Context 泄漏反例/正例代码（静态持有）
- [x] 6.2 MEM-03：补全大图未采样反例/正例代码（BitmapFactory.Options）
- [x] 6.3 MEM-04：补全缓存无界反例/正例代码（HashMap → LruCache）
- [x] 6.4 MEM-05：补全大对象未释放反例/正例代码（Bitmap.recycle/Cursor.close）
- [x] 6.5 MEM-07：补全 WebView 独立进程配置反例/正例代码
- [x] 6.6 MEM-08：补全硬件位图使用反例/正例代码（Bitmap.Config.HARDWARE）

## 7. §10.5 网络规则代码增强

- [x] 7.1 NET-01：补全重复请求反例/正例代码（去重/合并）
- [x] 7.2 NET-02：补全超大响应无反例/正例代码（分页/字段裁剪）
- [x] 7.3 NET-03：补全弱网超时反例/正例代码（退避重试）
- [x] 7.4 NET-04：补全 OkHttpClient 实例化反例/正例代码（单例）
- [x] 7.5 NET-05：补全图片无磁盘缓存反例/正例代码（Glide diskCache）
- [x] 7.6 NET-06：补全无流量检测反例/正例代码（ConnectivityManager）

## 8. §10.6 磁盘 IO 规则代码增强

- [x] 8.1 IO-01：补全主线程同步读大文件反例/正例代码
- [x] 8.2 IO-02：补全数据库批量操作反例/正例代码（Room @Transaction）
- [x] 8.3 IO-03：补全日志同步写反例/正例代码（异步队列）
- [x] 8.4 IO-04：补全频繁小文件读写反例/正例代码
- [x] 8.5 IO-05：补全 commit vs apply 反例/正例代码

## 9. §10.7 后台电量规则代码增强

- [x] 9.1 BG-01：补全后台滥用隐式广播反例/正例代码
- [x] 9.2 BG-02：补全 WakeLock 未释放反例/正例代码
- [x] 9.3 BG-03：补全高频 AlarmManager 反例/正例代码
- [x] 9.4 BG-04：补全无条件全量拉取反例/正例代码
- [x] 9.5 BG-05：补全前台服务类型缺失反例/正例代码（AndroidManifest）
- [x] 9.6 BG-06：补全精确闹钟无权限检查反例/正例代码

## 10. §10.8 协程规则代码增强

- [x] 10.1 TH-01：补全 Dispatcher 误用反例/正例代码
- [x] 10.2 TH-02：补全线程池无配置反例/正例代码（newCachedThreadPool → 统一池）
- [x] 10.3 TH-03：补全 Flow 背压反例/正例代码（buffer/shareIn）
- [x] 10.4 TH-04：补全过度并行反例/正例代码（批量/限制并发）
- [x] 10.5 TH-06：补全结构化并发反例/正例代码（CoroutineScope → lifecycleScope）

## 11. §10.9 包体规则代码增强

- [x] 11.1 PKG-01：补全新增大依赖反例/正例代码（gradle 配置）
- [x] 11.2 PKG-02：补全资源未优化反例/正例代码（WebP/Vector）
- [x] 11.3 PKG-03：补全 ABI 全打包反例/正例代码（splits/App Bundle）
- [x] 11.4 PKG-04：补全 R8 keep 规则过度反例/正例代码
- [x] 11.5 PKG-05：补全 Native 库未 strip 反例/正例代码（CMakeLists）
- [x] 11.6 PKG-06：补全 16KB 页对齐配置反例/正例代码

## 12. §10.10 可观测性规则代码增强

- [x] 12.1 OBS-01：补全性能敏感改动无验证说明反例/正例（PR 描述模板）
- [x] 12.2 OBS-02：补全无埋点反例/正例代码（APM SDK 调用）
- [x] 12.3 OBS-03：补全无线上监控反例/正例代码
- [x] 12.4 OBS-04：补全调试代码未隔离反例/正例代码（BuildConfig.DEBUG）

## 13. §10.11 WebView 规则代码增强

- [x] 13.1 WV-01：补全 WebView 未异步初始化反例/正例代码
- [x] 13.2 WV-02：补全 JS Bridge 高频调用反例/正例代码
- [x] 13.3 WV-04：补全无离线缓存反例/正例代码（shouldInterceptRequest）

## 14. §10.12 架构规则代码增强

- [x] 14.1 ARCH-01：补全跨模块大对象序列化反例/正例代码
- [x] 14.2 ARCH-02：补全模块循环依赖反例/正例代码（build.gradle.kts）
- [x] 14.3 ARCH-03：补全 Dynamic Feature 启动加载反例/正例代码
- [x] 14.4 ARCH-04：补全高频 Binder 调用反例/正例代码

## 15. 文档结构重组

- [x] 15.1 创建 §13「后期展望：流水线集成与 CI 自动化」→ 汇集所有清理出的流水线内容
- [x] 15.2 §7.2 简化为仅 Phase 0 说明，增加指向 §13 的引用链接
- [x] 15.3 §7.4 工具速查卡新增 Compose Compiler Metrics 条目
- [x] 15.4 更新 §8.3 修订记录：v3.0 流水线激进清理 + 81 条规则代码增强
- [x] 15.5 全局搜索验证无残留流水线关键词（pipeline/通道 A/CI 门禁）

## 16. 最终校验

- [x] 16.1 确认 81 条规则全部有 ≥ 2 行 Kotlin 反例代码
- [x] 16.2 确认 81 条规则全部有 ≥ 2 行 Kotlin 正例代码
- [x] 16.3 确认 §1-12 中无流水线相关残留描述
- [x] 16.4 确认 §13「后期展望」包含完整的流水线/CI/自动化路线图内容
