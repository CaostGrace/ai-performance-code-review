# 冒烟测试用例

> 本文件记录 Skill 的冒烟测试用例。每条反例输入 Skill 后应触发对应规则 ID；每条正例不应触发。

## P0 规则反例测试（13 条）

### MT-01: 主线程同步磁盘 IO
```kotlin
// 输入 diff：
val sp = getSharedPreferences("app", MODE_PRIVATE)
val value = sp.getString("key", "")
sp.edit().putString("key", "data").commit()
```
**期望**：报告 MT-01 P0

### MT-02: 主线程同步网络
```kotlin
val client = OkHttpClient()
val resp = client.newCall(request).execute()
```
**期望**：报告 MT-02 P0

### MT-03: 主线程大计算
```kotlin
val json = File("cache/large.json").readText()
val obj = Gson().fromJson(json, BigData::class.java)
```
**期望**：报告 MT-03 P0

### MT-04: BroadcastReceiver 内长任务
```kotlin
class MyReceiver : BroadcastReceiver() {
    override fun onReceive(ctx: Context, intent: Intent) {
        val data = fetchFromNetwork()
    }
}
```
**期望**：报告 MT-04 P0

### MT-06: WebView 主线程重操作
```kotlin
webView.loadUrl("https://example.com")
val result = webView.evaluateJavascript(js) { }
```
**期望**：报告 MT-06 P0

### MEM-01: Activity/Context 泄漏
```kotlin
companion object { var activity: Activity? = null }
fun onCreate() { activity = this }
```
**期望**：报告 MEM-01 P0

### MEM-02: 协程随生命周期取消
```kotlin
fun loadData() {
    GlobalScope.launch {
        val data = networkCall()
        textView.text = data
    }
}
```
**期望**：报告 MEM-02 P0

### MEM-06: Handler 持有 Activity
```kotlin
class MyActivity : Activity() {
    val handler = Handler { msg -> textView.text = "" }
}
```
**期望**：报告 MEM-06 P0

### TH-05: runBlocking 主线程
```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    val data = runBlocking { apiService.fetchData() }
}
```
**期望**：报告 TH-05 P0

### ST-01: Application 同步重初始化
```kotlin
class MyApp : Application() {
    override fun onCreate() {
        super.onCreate()
        Firebase.initializeApp(this)
        Analytics.init(this)
        ImageLoader.init(this)
    }
}
```
**期望**：报告 ST-01 P0

### BG-01: 后台任务不合规 API
```kotlin
class MyReceiver : BroadcastReceiver() { /* ... */ }
// Manifest: <receiver android:exported="true">
//     <intent-filter>
//         <action android:name="android.intent.action.TIME_TICK"/>
```
**期望**：报告 BG-01 P0

### BG-05: Android 14+ 前台服务未声明类型
```kotlin
startForeground(NOTIFICATION_ID, notification)
```
**期望**：报告 BG-05 P0

### IO-01: 主线程同步读文件
```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    val json = File(cacheDir, "big.json").readText()
}
```
**期望**：报告 IO-01 P0

## P0 正例测试（不应触发）

### MT-01 正例
```kotlin
viewModelScope.launch(Dispatchers.IO) {
    val value = dataStore.data.first()[stringPreferencesKey("key")]
    withContext(Dispatchers.Main) { updateUI(value) }
}
sp.edit().putString("key", "data").apply()
```
**期望**：不报告 MT-01

### MEM-01 正例
```kotlin
private var activityRef: WeakReference<Activity>? = null
override fun onDestroy() { activityRef?.clear() }
```
**期望**：不报告 MEM-01

### TH-05 正例
```kotlin
lifecycleScope.launch {
    val data = apiService.fetchData()
    updateUI(data)
}
```
**期望**：不报告 TH-05

## 三重判定逻辑测试

### 可疑模式（应触发降级）
```kotlin
// 主线程读文件，但文件大小未知 → 应触发 IO-01 P1（降级）
fun loadConfig() {
    val config = File(filesDir, "config.json").readText()
    parseConfig(config)
}
```
**期望**：报告 IO-01 P1（降级），标注"需人工确认"

### 架构担忧（应写入需人工）
```kotlin
// 新增大型依赖但无具体代码变更
// build.gradle.kts:
implementation("com.squareup.retrofit2:converter-moshi:2.9.0")
// 仅新增依赖声明，无使用代码
```
**期望**：写入「未覆盖/需人工」而非 P0
