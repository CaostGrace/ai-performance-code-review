# 线程与协程

> §9.8 线程与协程。规则 ID 前缀 `TH-`。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| TH-01 | P1 | Dispatcher 使用正确 | ```kotlin
// ❌ IO 用 Default
viewModelScope.launch(Dispatchers.Default) {
    File("cache.txt").readText() // 阻塞 Default 线程池
}
``` | ```kotlin
// ✅ IO → IO, 计算 → Default
viewModelScope.launch(Dispatchers.IO) {
    val data = File("cache.txt").readText()
    withContext(Dispatchers.Default) { process(data) }
}
``` | 线程池饥饿 | Lint |
| TH-02 | P1 | 线程池可配置、可命名 | ```kotlin
// ❌ 随处 cachedThreadPool
val pool = Executors.newCachedThreadPool()
``` | ```kotlin
// ✅ 统一线程池
val pool = ThreadPoolExecutor(coreSize, maxSize, 30, TimeUnit.SECONDS,
    LinkedBlockingQueue(128), NamedThreadFactory("download"))
``` | 线程数爆炸 | Systrace |
| TH-03 | P1 | Flow 背压与 collect 上下文 | ```kotlin
// ❌ 热 Flow 无缓冲
hotFlow.collect { heavy(it) } // 阻塞生产者
``` | ```kotlin
// ✅ buffer + shareIn
hotFlow.buffer(Channel.BUFFERED)
    .flowOn(Dispatchers.Default)
    .collect { heavy(it) }
``` | 异常或卡顿 | — |
| TH-04 | P2 | 避免过度并行 | ```kotlin
// ❌ 大量 async
items.map { async { process(it) } }.awaitAll() // 10000 个 coroutine
``` | ```kotlin
// ✅ 限制并发度
items.chunked(10).forEach { batch ->
    coroutineScope { batch.map { async { process(it) } }.awaitAll() }
}
``` | 调度开销 > 收益 | — |
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
| TH-06 | P1 | 结构化并发：Scope 生命周期归属 | ```kotlin
// ❌ 无 cancel 管理
val scope = CoroutineScope(Job())
scope.launch { fetchData() }
``` | ```kotlin
// ✅ lifecycleScope
lifecycleScope.launch { fetchData() }
// Compose: rememberCoroutineScope()
``` | 泄漏或生命周期异常 | Lint |
