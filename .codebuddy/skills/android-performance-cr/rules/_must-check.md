# P0 必查规则集

> 本文件包含 L0（永远注入）和 L1（按文件语言注入）两级 P0 必查规则。
> 无论路由结果如何，本文件始终首先被加载。

## L0（永远注入）

以下规则无论变更类型如何均参与审查。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| MEM-01 | P0 | 禁止 Activity/Context 泄漏 | ```kotlin
// ❌ 静态持有 Activity
companion object { var activity: Activity? = null }
fun onCreate() { activity = this }
``` | ```kotlin
// ✅ WeakReference
private var activityRef: WeakReference<Activity>? = null
override fun onDestroy() { activityRef?.clear() }
``` | LeakCanary 可复现 | LeakCanary |
| MEM-02 | P0 | 监听/订阅/协程必须随生命周期取消 | ```kotlin
// ❌ GlobalScope 泄漏
fun loadData() {
    GlobalScope.launch {
        val data = networkCall()
        textView.text = data // Activity 销毁后 crash
    }
}
``` | ```kotlin
// ✅ lifecycleScope 自动管理
lifecycleScope.launch {
    val data = networkCall()
    textView.text = data
} // Activity destroy 时自动 cancel
``` | 退出页面后仍回调 | LeakCanary、Lint |
| TH-05 | P0 | 禁止 `runBlocking` 在主线程 | ```kotlin
// ❌ runBlocking → ANR
override fun onCreate(savedInstanceState: Bundle?) {
    val data = runBlocking { apiService.fetchData() } // 主线程阻塞!
}
``` | ```kotlin
// ✅ launch + 挂起
lifecycleScope.launch {
    val data = apiService.fetchData()
    updateUI(data)
}
``` | 主线程阻塞 ANR | Lint |

## L1（按文件语言注入）

以下规则仅在非资源文件（.kt, .java, .xml 非纯资源）变更时注入。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| MT-01 | P0 | UI 线程禁止同步磁盘 IO | ```kotlin
// ❌ 主线程同步读 SP → ANR
val sp = getSharedPreferences("app", MODE_PRIVATE)
val value = sp.getString("key", "") // 主线程阻塞
sp.edit().putString("key", "data").commit() // 同步写
``` | ```kotlin
// ✅ 后台线程 + DataStore
viewModelScope.launch(Dispatchers.IO) {
    val value = dataStore.data.first()[stringPreferencesKey("key")]
    withContext(Dispatchers.Main) { updateUI(value) }
}
// ✅ SP 异步写
sp.edit().putString("key", "data").apply()
``` | 主线程栈出现阻塞 IO | StrictMode、Systrace |
| MT-02 | P0 | UI 线程禁止同步网络 | ```kotlin
// ❌ OkHttp 同步 → ANR
val client = OkHttpClient()
val resp = client.newCall(request).execute() // 阻塞主线程
``` | ```kotlin
// ✅ Retrofit suspend + IO Dispatcher
viewModelScope.launch(Dispatchers.IO) {
    val data = apiService.fetchData()
    withContext(Dispatchers.Main) { updateUI(data) }
}
``` | 网络调用在主线程 | StrictMode、Lint |
| MT-03 | P0 | 禁止主线程大计算 | ```kotlin
// ❌ 主线程解析大 JSON
val json = File("cache/large.json").readText()
val obj = Gson().fromJson(json, BigData::class.java)
``` | ```kotlin
// ✅ 后台线程解析
viewModelScope.launch(Dispatchers.Default) {
    val obj = Gson().fromJson(json, BigData::class.java)
    withContext(Dispatchers.Main) { display(obj) }
}
``` | 单次主线程占用明显可感知 | Systrace |
| MT-06 | P0 | WebView/JS Bridge 禁止主线程重操作 | ```kotlin
// ❌ 主线程阻塞等待 WebView
webView.loadUrl("https://example.com")
val result = webView.evaluateJavascript(js) { } // 同步等待
``` | ```kotlin
// ✅ 异步处理 + 回调
webView.evaluateJavascript(js) { result ->
    lifecycleScope.launch(Dispatchers.Main) {
        handleResult(result)
    }
}
``` | 主线程调用 WebView API 且有同步等待语义 | Systrace |
| BG-01 | P0 | 后台任务使用合规 API | ```kotlin
// ❌ 滥用隐式广播 + 常驻服务
class MyReceiver : BroadcastReceiver() { ... }
// Manifest: <receiver android:exported="true"> <intent-filter> <action android:name="android.intent.action.TIME_TICK"/>
``` | ```kotlin
// ✅ WorkManager
val request = PeriodicWorkRequestBuilder<SyncWorker>(15, TimeUnit.MINUTES).build()
WorkManager.getInstance(ctx).enqueue(request)
``` | 系统杀进程 | 官方后台限制文档 |
| BG-05 | P0 | Android 14+ 前台服务须声明类型 | ```kotlin
// ❌ 未声明 foregroundServiceType
startForeground(NOTIFICATION_ID, notification)
``` | ```kotlin
// ✅ Manifest 声明
<service android:foregroundServiceType="dataSync|location" />
startForeground(NOTIFICATION_ID, notification, FOREGROUND_SERVICE_TYPE_DATA_SYNC)
``` | 系统拒绝启动 | 官方前台服务文档 |
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
| IO-01 | P0 | 主线程禁止同步读大 SP/文件 | ```kotlin
// ❌ 主线程 readText
override fun onCreate(savedInstanceState: Bundle?) {
    val json = File(cacheDir, "big.json").readText()
}
``` | ```kotlin
// ✅ 后台读
lifecycleScope.launch(Dispatchers.IO) {
    val json = File(cacheDir, "big.json").readText()
    withContext(Dispatchers.Main) { show(json) }
}
``` | 同 MT-01（命中时任一报告即可） | StrictMode |
