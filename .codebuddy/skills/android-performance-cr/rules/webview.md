# WebView 性能

> §9.11 WebView 性能。规则 ID 前缀 `WV-`。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| WV-01 | P1 | WebView 初始化异步完成 | ```kotlin
// ❌ 主线程创建 WebView
override fun onCreate(savedInstanceState: Bundle?) {
    setContentView(R.layout.webview)
    webView.loadUrl("https://example.com")
}
``` | ```kotlin
// ✅ 提前预热
class MyApp : Application() {
    override fun onCreate() {
        WebView.startWebView(this) // 后台预热内核
    }
}
``` | 冷启动延迟 | Systrace |
| WV-02 | P1 | JS Bridge 调用避免频繁序列化 | ```kotlin
// ❌ 高频大 JSON Bridge
@JavascriptInterface
fun onEvent(json: String) { // 每 100ms 传 50KB JSON
    val data = Gson().fromJson(json, BigData::class.java)
}
``` | ```kotlin
// ✅ 批量传输 + 核心数据优先
private val buffer = StringBuilder()
@JavascriptInterface
fun onBatch(events: String) { processBatch(events) } // 500ms 合并一次
``` | Bridge > 10/s | Systrace |
| WV-03 | P1 | WebView 页面正确销毁 | ```kotlin
// ❌ 未 destroy
override fun onDestroy() {
    super.onDestroy() // webView 未清理!
}
``` | ```kotlin
// ✅ 完整清理
override fun onDestroy() {
    webView.stopLoading()
    webView.loadUrl("about:blank")
    webView.removeAllViews()
    webView.destroy()
    super.onDestroy()
}
``` | Native 内存未降 | Memory Profiler |
| WV-04 | P2 | 离线缓存策略 | ```kotlin
// ❌ 每次走网络
webView.loadUrl("https://example.com/page")
``` | ```kotlin
// ✅ 离线包拦截
webView.webViewClient = object : WebViewClient() {
    override fun shouldInterceptRequest(view: WebView, request: WebResourceRequest): WebResourceResponse? {
        return offlineCache.get(request.url.toString())
    }
}
``` | 重复流量 | Network Profiler |
