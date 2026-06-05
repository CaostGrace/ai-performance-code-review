# 可观测性

> §9.10 可观测性（CR 流程要求）。规则 ID 前缀 `OBS-`。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| OBS-01 | P1 | 性能敏感改动需说明验证方式 | ```kotlin
// ❌ PR 无性能验证说明
// 提交了 RecyclerView 优化，但未说明如何验证
``` | ```kotlin
// ✅ PR 附带性能验证
// 验证: Systrace 抓取 100 条列表滑动, doFrame 从 avg 25ms → 12ms
``` | Reviewer 无法评估 | — |
| OBS-02 | P2 | 关键路径有埋点 | ```kotlin
// ❌ 无打点
fun startApp() { init1(); init2(); init3() }
``` | ```kotlin
// ✅ APM SDK 打点
val trace = FirebasePerformance.startTrace("cold_start")
initSdk()
trace.putMetric("sdk_init_ms", elapsed)
trace.stop()
``` | 线上无法回归 | 内部 APM |
| OBS-03 | P1 | 性能敏感改动须关联线上监控 | ```kotlin
// ❌ 新功能无性能监控
fun newFeature() { ... }
``` | ```kotlin
// ✅ 与 APM 对齐
// ANR 看板: feature_anr_rate
// 卡顿看板: feature_fps_p50
val monitor = PerformanceMonitor("new_feature")
monitor.recordFrameTime(duration)
``` | 上线后无数据验证 | 内部 APM |
| OBS-04 | P2 | 调试/测试代码与 release 隔离 | ```kotlin
// ❌ LeakCanary 打进 release
implementation("com.squareup.leakcanary:leakcanary-android:2.x")
``` | ```kotlin
// ✅ debug 依赖
debugImplementation("com.squareup.leakcanary:leakcanary-android:2.x")
if (BuildConfig.DEBUG) { Log.d(TAG, "debug only") }
``` | 包体膨胀 | — |
