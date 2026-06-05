# APK、资源与依赖

> §9.9 APK、资源与依赖。规则 ID 前缀 `PKG-`。

| ID | 等级 | 检查项 | 反例 | 正例 | 判定 | 参考工具 |
|----|------|--------|------|------|------|----------|
| PKG-01 | P1 | 新增依赖评估包体与启动 | ```kotlin
// ❌ 无说明引入大 SDK
implementation("com.example:heavy-sdk:3.0")
``` | ```kotlin
// ✅ 按需引入，附启动评估注释
// 包体 +1.2MB, 启动 +80ms
implementation("com.example:heavy-sdk:3.0")
implementation("com.google.android.play:feature-delivery:2.1")
``` | APK 明显增大 | APK Analyzer |
| PKG-02 | P2 | 资源优化 | ```kotlin
// ❌ 未压缩 PNG 大图
res/drawable/bg.png (2MB)
``` | ```kotlin
// ✅ WebP/Vector
res/drawable/bg.webp (200KB)
res/drawable/ic_arrow.xml // Vector, 几 KB
``` | 包体与内存占用 | APK Analyzer |
| PKG-03 | P2 | ABI 与分包策略 | ```kotlin
// ❌ 全 ABI 打一个包
ndk { abiFilters += listOf("x86", "x86_64", "armeabi-v7a", "arm64-v8a") }
``` | ```kotlin
// ✅ splits / App Bundle
android { bundle { abi { enableSplit = true } } }
// 或 ndk { abiFilters += listOf("arm64-v8a") } 仅主 ABI
``` | 下载体积大 | Bundle Tool |
| PKG-04 | P1 | R8/ProGuard keep 规则有效性 | ```kotlin
// ❌ 过度 keep
-keep class com.example.** { *; }
``` | ```kotlin
// ✅ 精细化 keep
-keep class com.example.model.** { <fields>; }
-keepclassmembers class * { @com.example.Serialize <fields>; }
``` | 包体膨胀 | APK Analyzer |
| PKG-05 | P2 | Native 库剥离（strip） | ```kotlin
// ❌ 含调试符号
cmake { arguments "-DCMAKE_BUILD_TYPE=Debug" }
``` | ```kotlin
// ✅ strip + ABI 控制
cmake { arguments "-DCMAKE_BUILD_TYPE=Release" }
ndk { abiFilters += listOf("arm64-v8a") }
``` | 包体 +10-30% | APK Analyzer |
| PKG-06 | P1 | Native 库 16 KB 页对齐 | ```kotlin
// ❌ 未设置对齐
cmake { arguments "-DANDROID_SUPPORT_FLEXIBLE_PAGE_SIZES=OFF" }
``` | ```kotlin
// ✅ NDK r27+ 默认对齐
android { defaultConfig { ndk { abiFilters += listOf("arm64-v8a") } } }
// CMake: set(CMAKE_SHARED_LINKER_FLAGS "-Wl,-z,max-page-size=16384")
``` | Google Play 拒绝上架 | APK Analyzer |
