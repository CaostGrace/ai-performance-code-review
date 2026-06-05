# 主线程与 ANR

> §9.1 主线程与 ANR（P0 高发区）。规则 ID 前缀 `MT-`。

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
| MT-04 | P0 | BroadcastReceiver 内长任务 | ```kotlin
// ❌ onReceive 中直接做 IO
class MyReceiver : BroadcastReceiver() {
    override fun onReceive(ctx: Context, intent: Intent) {
        val data = fetchFromNetwork() // ANR!
    }
}
``` | ```kotlin
// ✅ goAsync + 后台线程
class MyReceiver : BroadcastReceiver() {
    override fun onReceive(ctx: Context, intent: Intent) {
        val pending = goAsync()
        thread {
            val data = fetchFromNetwork()
            pending.finish()
        }
    }
}
``` | 10s 内无法完成 | — |
| MT-05 | P1 | 避免主线程锁等待 | ```kotlin
// ❌ 主线程等待后台持有的锁
val lock = Object()
synchronized(lock) {
    while (!ready) lock.wait() // UI 冻结
}
``` | ```kotlin
// ✅ 无锁结构 / CAS
val state = AtomicReference<State>(State.LOADING)
lifecycleScope.launch {
    stateFlow.collect { updateUI(it) }
}
``` | Systrace 见主线程阻塞 | Systrace |
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
| MT-07 | P1 | 主线程避免调用系统服务重操作 | ```kotlin
// ❌ 主线程查询 PackageManager
val pm = context.packageManager
val apps = pm.getInstalledApplications(0) // 耗时 > 50ms
``` | ```kotlin
// ✅ 后台获取 + 缓存
viewModelScope.launch(Dispatchers.IO) {
    val apps = pm.getInstalledApplications(0)
    appCache = apps
}
``` | 主线程调用系统服务耗时 > 5ms | Systrace |
