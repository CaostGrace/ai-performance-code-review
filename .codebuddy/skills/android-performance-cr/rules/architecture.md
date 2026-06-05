# 架构与模块化

> §9.12 架构与模块化。规则 ID 前缀 `ARCH-`。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| ARCH-01 | P2 | 跨模块避免大对象序列化开销 | ```kotlin
// ❌ 跨模块大 Parcelable
// :feature-a
data class BigData(val list: List<Item>) : Parcelable { ... }
// :feature-b 每次都解析完整对象
``` | ```kotlin
// ✅ 轻量对象 + 本地缓存
// :feature-a 传递 key
data class LightRef(val id: String, val status: Status)
// :feature-b 按需从本地 DB 加载完整对象
``` | Parcelable 字段 > 20 | APK Analyzer |
| ARCH-02 | P2 | 避免模块间循环依赖 | ```kotlin
// ❌ A→B→A
// :feature-a/build.gradle.kts
implementation(project(":feature-b"))
// :feature-b/build.gradle.kts
implementation(project(":feature-a")) // 循环!
``` | ```kotlin
// ✅ 依赖倒置
// :feature-a → :base-api (接口)
// :feature-b → :base-api (接口)
// 无直接依赖
``` | project() 构成环 | Gradle moduleDependencyReport |
| ARCH-03 | P1 | Dynamic Feature 按需加载 | ```kotlin
// ❌ Application.onCreate 中加载
class MyApp : Application() {
    override fun onCreate() {
        SplitInstallManager.startInstall(request) // 阻塞启动
    }
}
``` | ```kotlin
// ✅ 使用时按需加载
fun navigateToFeature() {
    val manager = SplitInstallManagerFactory.create(context)
    manager.startInstall(request)
        .addOnSuccessListener { startFeatureActivity() }
}
``` | 冷启动阻塞 | Systrace |
| ARCH-04 | P1 | 多进程避免高频 Binder 通信 | ```kotlin
// ❌ 每帧多次跨进程调用
contentResolver.query(uri, null, null, null, null)
contentResolver.insert(uri, values)
``` | ```kotlin
// ✅ 批量 RPC / SharedMemory
// 使用 MMKV 进程间共享
val mmkv = MMKV.mmkvWithID("shared", MMKV.MULTI_PROCESS_MODE)
mmkv.encode("key", value)
``` | Binder 耗时 > 5ms | Systrace |
