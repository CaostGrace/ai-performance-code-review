# 内存

> §9.4 内存。规则 ID 前缀 `MEM-`。

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
| MEM-03 | P1 | 大图按采样加载 | ```kotlin
// ❌ 原图解码 → OOM
val bm = BitmapFactory.decodeFile("/sdcard/img.jpg")
imageView.setImageBitmap(bm)
``` | ```kotlin
// ✅ 降采样
val opts = BitmapFactory.Options().apply {
    inJustDecodeBounds = true
    decodeFile(path, this)
    inSampleSize = calculateScale(outWidth, outHeight, 300, 300)
    inJustDecodeBounds = false
}
val bm = BitmapFactory.decodeFile(path, opts)
``` | OOM 或内存峰值异常 | Memory Profiler |
| MEM-04 | P1 | 缓存必须有界 | ```kotlin
// ❌ 无界 HashMap
private val cache = HashMap<String, Bitmap>()
``` | ```kotlin
// ✅ LruCache
val cache = LruCache<String, Bitmap>(4 * 1024 * 1024) { value -> value.byteCount }
``` | 长时间后内存单调涨 | Memory Profiler |
| MEM-05 | P1 | 及时释放大对象与 Native 资源 | ```kotlin
// ❌ 未 recycle/close
var bitmap: Bitmap? = loadBitmap()
cursor.moveToFirst() // 未 close
``` | ```kotlin
// ✅ use/try-finally
cursor.use { while (it.moveToNext()) { process(it) } }
bitmap?.let { if (!it.isRecycled) it.recycle() }
``` | 内存 Profiler 残留 | Memory Profiler |
| MEM-06 | P0 | 禁止 Handler / 匿名内部类持有 Activity | ```kotlin
// ❌ 匿名 Handler 持有 Activity
class MyActivity : Activity() {
    val handler = Handler { msg -> textView.text = "" }
}
``` | ```kotlin
// ✅ 静态内部类 + WeakReference
class SafeHandler(activity: MyActivity) : Handler(Looper.getMainLooper()) {
    private val ref = WeakReference(activity)
    override fun handleMessage(msg: Message) {
        ref.get()?.handle(msg)
    }
}
``` | 退出 Activity 后仍可回调 | LeakCanary |
| MEM-07 | P1 | WebView 建议独立进程 | ```kotlin
// ❌ WebView 与主进程共用
<activity android:name=".WebViewActivity" />
``` | ```kotlin
// ✅ 独立进程
<activity android:name=".WebViewActivity" android:process=":webview" />
override fun onDestroy() {
    webView.stopLoading()
    webView.loadUrl("about:blank")
    webView.destroy()
}
``` | WebView 内存持续增长 | Memory Profiler |
| MEM-08 | P1 | 大图按需降采样，优先硬件位图 | ```kotlin
// ❌ ARGB_8888 全分辨率
val bm = BitmapFactory.decodeStream(input)
``` | ```kotlin
// ✅ 硬件位图 (Android O+)
val opts = BitmapFactory.Options().apply {
    inPreferredConfig = Bitmap.Config.HARDWARE
}
val bm = BitmapFactory.decodeStream(input, null, opts)
``` | 内存峰值、OOM | Memory Profiler |
