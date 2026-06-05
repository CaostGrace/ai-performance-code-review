# 网络

> §9.5 网络。规则 ID 前缀 `NET-`。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| NET-01 | P1 | 避免重复请求与惊群 | ```kotlin
// ❌ 每次 bind 请求同一接口
override fun onBindViewHolder(holder: VH, pos: Int) {
    api.fetchUser(item.id).execute()
}
``` | ```kotlin
// ✅ 请求去重/缓存
private val inFlight = ConcurrentHashMap<String, Deferred<User>>()
suspend fun fetch(id: String) = inFlight.getOrPut(id) {
    coroutineScope { async { api.fetchUser(id) } }
}
``` | 流量与耗电异常 | Network Profiler |
| NET-02 | P1 | 响应体与解析可控 | ```kotlin
// ❌ 一次拉全部
@GET("users") suspend fun getAllUsers(): List<User>
``` | ```kotlin
// ✅ 分页 + 字段限制
@GET("users") suspend fun getUsers(
    @Query("page") page: Int,
    @Query("fields") fields: String
): Page<User>
``` | 解析阻塞后台过久 | — |
| NET-03 | P2 | 弱网与超时策略 | ```kotlin
// ❌ 无超时
val client = OkHttpClient()
``` | ```kotlin
// ✅ 超时 + 退避
val client = OkHttpClient.Builder()
    .connectTimeout(10, TimeUnit.SECONDS)
    .readTimeout(30, TimeUnit.SECONDS).build()
``` | 用户长期白屏 | Network Profiler |
| NET-04 | P2 | 连接复用与协议 | ```kotlin
// ❌ 每次 new client
fun req() { OkHttpClient().newCall(rq).execute() }
``` | ```kotlin
// ✅ 单例复用
object HttpClient { val client = OkHttpClient() }
``` | 连接建立开销大 | Network Profiler |
| NET-05 | P1 | 图片加载必须有磁盘缓存 | ```kotlin
// ❌ 禁用磁盘缓存
Glide.with(ctx).load(url).diskCacheStrategy(NONE).into(iv)
``` | ```kotlin
// ✅ 默认缓存
Glide.with(ctx).load(url).into(iv)
``` | 重复流量 | — |
| NET-06 | P2 | 计量网络检测与流量控制 | ```kotlin
// ❌ 无网络类型检测
fun sync() { api.syncAll() }
``` | ```kotlin
// ✅ 检测计量网络
val cm = ctx.getSystemService<ConnectivityManager>()
if (cm.isActiveNetworkMetered) syncEssential() else syncAll()
``` | 用户流量超额 | — |
