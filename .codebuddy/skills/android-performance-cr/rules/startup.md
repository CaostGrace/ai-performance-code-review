# 启动与初始化

> §9.2 启动与初始化。规则 ID 前缀 `ST-`。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| ST-01 | P0 | Application 中禁止非必要同步重初始化 | ```kotlin
// ❌ Application 同步初始化所有 SDK
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        Firebase.initializeApp(this)
        Analytics.init(this)
        ImageLoader.init(this)  // 阻塞数百 ms
    }
}
``` | ```kotlin
// ✅ 延迟 + Startup 库
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        // 仅初始化必需项，其他延迟到空闲或首次使用
        Looper.myQueue().addIdleHandler {
            FireAndForget.init()
            false
        }
    }
}
``` | 冷启动主线程耗时骤增 | Macrobenchmark、Systrace |
| ST-02 | P1 | ContentProvider 滥用初始化 | ```kotlin
// ❌ 每个 SDK 单独一个 Provider 自动拉起
class SdkAProvider : ContentProvider() {
    override fun onCreate(): Boolean {
        SdkA.init(context!!) // 启动时自动执行
        return true
    }
}
``` | ```kotlin
// ✅ 合并或使用 Startup
class AppInitializer : Initializer<Unit> {
    override fun create(context: Context) {
        // 集中初始化，可控顺序
    }
}
``` | 启动前多余进程工作 | App Startup 指南 |
| ST-03 | P1 | 首屏避免阻塞绘制 | ```kotlin
// ❌ onCreate 同步加载后 setContent
override fun onCreate(savedInstanceState: Bundle?) {
    val data = apiService.fetchHome() // 同线程阻塞
    setContent { HomeScreen(data) }
}
``` | ```kotlin
// ✅ 骨架屏 + 异步
override fun onCreate(savedInstanceState: Bundle?) {
    setContent {
        var data by remember { mutableStateOf<HomeData?>(null) }
        if (data == null) ShimmerScreen() else HomeScreen(data!!)
    }
    lifecycleScope.launch { data = apiService.fetchHome() }
}
``` | TTFD 变差 | Profiler |
| ST-04 | P2 | 启动任务可度量 | ```kotlin
// ❌ 无埋点
override fun onCreate() { init1(); init2(); init3() }
``` | ```kotlin
// ✅ 分阶段打点
val startTime = SystemClock.elapsedRealtime()
initSdk()
val sdkDone = SystemClock.elapsedRealtime()
reportTrace("app_start", startTime, sdkDone)
reportFullyDrawn() // Android 上报首屏完整
``` | 无法回归对比 | 内部埋点规范 |
| ST-05 | P1 | ContentProvider.onCreate 禁止同步重初始化 | ```kotlin
// ❌ Provider.onCreate 同步网络预热
class MyProvider : ContentProvider() {
    override fun onCreate(): Boolean {
        val config = httpGet("https://api/config") // 阻塞
        return true
    }
}
``` | ```kotlin
// ✅ 异步初始化 + 标记
class MyProvider : ContentProvider() {
    override fun onCreate(): Boolean {
        CoroutineScope(Dispatchers.IO).launch {
            config = prefetch()
            isReady = true
        }
        return true
    }
}
``` | 冷启动 provider 耗时 > 50ms | Systrace |
| ST-06 | P1 | 避免 Application 静态字段初始化重对象 | ```kotlin
// ❌ companion object 中 lazy 但首次访问仍在主线程
class MyApp : Application() {
    companion object {
        val gson by lazy { GsonBuilder().create() } // 主线程首次触发
    }
}
``` | ```kotlin
// ✅ IdleHandler 预加载
Looper.myQueue().addIdleHandler {
    backgroundThread { HeavyObject.init() }
    false
}
``` | 首次使用卡顿明显 | Systrace |
| ST-07 | P1 | 启动路径改动需检查 Baseline Profile | ```kotlin
// ❌ 关键路径改动无 baseline-prof.txt
fun navigateToHome() {
    startActivity(Intent(this, HomeActivity::class.java))
}
// src/main/baseline-prof.txt 缺失
``` | ```kotlin
// ✅ Macrobenchmark 生成 profile
// app/src/main/baseline-prof.txt
HSPLandroidx/compose/runtime/ComposerImpl;->apply
PLkotlin/collections/CollectionsKt___CollectionsKt
``` | 冷启动时间无 AOT 优化 | Macrobenchmark |
