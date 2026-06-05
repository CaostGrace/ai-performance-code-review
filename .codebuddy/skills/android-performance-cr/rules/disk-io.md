# 磁盘与 I/O

> §9.6 磁盘与 I/O。规则 ID 前缀 `IO-`。
> IO-01 与 MT-01 主线程磁盘 IO 重叠；IO-01 强调存储介质与体量，命中时任一报告即可。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
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
``` | 同 MT-01 | StrictMode |
| IO-02 | P1 | 数据库批量与索引 | ```kotlin
// ❌ 循环单条 insert
users.forEach { dao.insert(it) }
``` | ```kotlin
// ✅ 事务批量
@Transaction suspend fun insertAll(users: List<User>) { dao.insertAll(users) }
// Room DAO: @Entity(indices = [Index("name")])
``` | 后台耗时过长 | Database Inspector |
| IO-03 | P1 | 日志与埋点异步 | ```kotlin
// ❌ 主线程同步写
File("log.txt").appendText("event\n")
``` | ```kotlin
// ✅ 异步 Channel
scope.launch(Dispatchers.IO) { logChannel.consumeEach { file.appendText(it) } }
``` | IO 影响流畅度 | — |
| IO-04 | P2 | 避免频繁小文件读写 | ```kotlin
// ❌ 每次写完整文件
fun save(token: String) { File(filesDir, "t.txt").writeText(token) }
``` | ```kotlin
// ✅ 批量存储
fun save(token: String) { sp.edit().putString("token", token).apply() }
``` | I/O 次数过多 | — |
| IO-05 | P1 | SharedPreferences 避免同步 commit | ```kotlin
// ❌ commit 同步
sp.edit().putString("k", "v").commit()
``` | ```kotlin
// ✅ apply 异步
sp.edit().putString("k", "v").apply()
// 或迁移 DataStore
``` | 主线程 commit ANR | StrictMode |
