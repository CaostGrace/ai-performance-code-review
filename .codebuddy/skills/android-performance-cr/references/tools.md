# 工具速查卡

> 本文件按需引用。AI 在审查发现中需要建议验证工具时，从此文件加载对应工具条目。

## 工具概览

| 场景 | 工具 |
|------|------|
| 主线程 IO/泄漏 | StrictMode、LeakCanary |
| 卡顿/启动 | Android Studio Profiler、Perfetto、Systrace |
| 内存 | Memory Profiler、Heap Dump |
| 电量 | Battery Historian |
| 静态检查 | Android Lint、Detekt 自定义规则 |
| Compose | Layout Inspector（重组）、Macrobenchmark（可选） |

## 详细速查

### StrictMode
- **启用**：代码内启用，无需额外依赖
- **命令**：`StrictMode.setThreadPolicy(ThreadPolicy.Builder().detectDiskReads().detectDiskWrites().detectNetwork().penaltyLog().build())` / `StrictMode.setVmPolicy(VmPolicy.Builder().detectActivityLeaks().detectLeakedClosableObjects().penaltyLog().build())`
- **解读**：Logcat `StrictMode policy violation` → 违规类型 + 调用栈；建议在 `Application.onCreate` 中 `BuildConfig.DEBUG` 下启用

### Perfetto
- **启用**：Android 10+ 系统内置；Web UI `ui.perfetto.dev`
- **命令**：`adb shell perfetto -o /data/misc/perfetto-traces/trace -t 10s gfx input view wm am`
- **解读**：MainThread 轨道 `doFrame` 耗时 > 16ms = 掉帧，> 32ms = 明显卡顿；支持 SQL 查询 `SELECT * FROM slice WHERE dur > 16000000`

### Systrace
- **启用**：SDK Platform Tools 自带
- **命令**：`python systrace.py -o trace.html gfx view wm am dalvik`（Android 9-）；Android 10+ 建议用 Perfetto
- **解读**：主线程 `running` > 16ms 连续出现 → 掉帧；`Choreographer#doFrame` 耗时超 16ms/32ms 为卡顿帧

### LeakCanary
- **启用**：`debugImplementation 'com.squareup.leakcanary:leakcanary-android:2.x'`
- **自动触发**，Activity/Fragment 销毁后检测
- **解读**：通知展示泄漏对象 + 引用路径图（蓝=强引用，虚线=弱引用）

### Memory Profiler
- **位置**：Android Studio → View → Tool Windows → Profiler
- **操作**：运行 → 点击 Memory 时间线 → 选择区间 → 右键 Export Heap Dump
- **解读**：Shallow Size vs Retained Size；两次 Heap Dump 对比找持续增长对象；Activity/Fragment 实例数 ≤ 预期存活页面数

### Battery Historian
- **启用**：Docker `docker run -p 9999:9999 gcr.io/android-battery-historian/stable:3.1`
- **操作**：`adb bugreport bugreport.zip` → 上传 `localhost:9999`
- **解读**：Device Power Estimates → 各 App 耗电占比；WakeLock 持有时间 → 电量杀手；Mobile Radio Active 时长 → 耗电警告

### APK Analyzer
- **位置**：Android Studio → Build → Analyze APK
- **操作**：拖入 `.apk` 或选择历史构建产物
- **解读**：classes.dex 大小 → 方法数估算；lib/ 各 ABI .so 大小 → 检查是否 strip；res/ 资源占用排名 → 找出未压缩大图

### Database Inspector
- **位置**：Android Studio → View → Tool Windows → App Inspection → Database Inspector
- **操作**：运行 → 选择进程 → 自动加载 Room/SQLite 数据库
- **解读**：Live Query 观察耗时；检查索引、字段类型；大表行数统计

### Network Profiler
- **位置**：Android Studio → View → Tool Windows → Profiler → Network
- **操作**：运行 → 触发网络请求 → 查看时间线
- **解读**：Request Timeline（排队+发送+等待+响应）；Connection View（复用情况）；Response Size（大 JSON 需分页）

### Compose Layout Inspector
- **位置**：Android Studio → View → Tool Windows → Layout Inspector
- **操作**：运行 Compose App → 选择进程 → 查看重组计数
- **解读**：重组次数异常高的 Composable → 优化目标；跳过次数 → skippable 效果

### Compose Compiler Metrics
- **启用**：`composeCompiler { reportsDestination = layout.buildDirectory.dir("compose_compiler") }`
- **操作**：`./gradlew assembleRelease` → 查看 `build/compose_compiler/<module>_classes.txt`
- **解读**：`unstable` 标记参数 → 需 @Stable 注解；`restartable but not skippable` → 添加 stable 参数后可跳过
