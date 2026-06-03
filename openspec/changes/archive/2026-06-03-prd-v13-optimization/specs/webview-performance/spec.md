## ADDED Requirements

### Requirement: WebView 初始化异步
审查 SHALL 检测 WebView 首次初始化是否在后台线程或预热阶段完成，避免主线程阻塞。

#### Scenario: 主线程首次创建 WebView
- **WHEN** 代码在 Activity.onCreate 或 Composable 中直接 `WebView(context)` 且无提前预热
- **THEN** 报告 WV-01 P1 发现项，建议使用 `WebView.startWebView()` 预热或异步初始化

### Requirement: JS Bridge 调用频率控制
审查 SHALL 关注 JS Bridge 的高频调用模式，避免频繁序列化大 JSON 导致卡顿。

#### Scenario: 高频 JS Bridge 调用
- **WHEN** JS Bridge 方法被高频调用（推测 > 10/s）且传递大对象
- **THEN** 报告 WV-02 P1，建议批量传输或降频

### Requirement: WebView 生命周期销毁
审查 SHALL 检测页面退出时 WebView 是否正确销毁（调 `destroy()` 或从父视图移除）。

#### Scenario: onDestroy 中遗漏 WebView 销毁
- **WHEN** Activity.onDestroy 中存在 WebView 引用但未调用 destroy()
- **THEN** 报告 WV-03 P1，提示 Native 内存泄漏风险

### Requirement: WebView 离线缓存策略
审查 SHALL 关注 WebView 加载是否每次走网络，建议离线缓存优化。

#### Scenario: WebView 无缓存配置
- **WHEN** WebView 设置中无缓存模式配置，且未启用离线包/Service Worker
- **THEN** 报告 WV-04 P2 建议
