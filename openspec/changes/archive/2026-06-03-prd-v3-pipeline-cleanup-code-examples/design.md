## Context

PRD v2.0 已建立了完整的规则体系（81 条规则、12 维度）。但因历史原因，PRD 中充斥了大量「通道 A（流水线）」相关的描述——双通道流程图、CI 门禁、自动化路线图 Phase 2-4、合入阻塞策略等，占比约全文 15%。这些内容在 Skill 仅用于「本地 AI Code Review」时严重干扰阅读和 Skill 实现。同时，规则表中约 76 条规则的「反例/正例」列仅使用概念描述而非可编译代码，AI 模型的模式匹配效率大打折扣。

## Goals / Non-Goals

**Goals:**
- 所有流水线/CI/通道 A 描述从 §1-11 中清理完毕，统一移至 §13「后期展望」
- §3.1 改为纯本地 Agent 视角，移除双通道 Mermaid 图
- §5 CR 流程图重绘为 Developer → 本地 Skill → Markdown 输出
- 81 条规则的「反例」和「正例」列全部替换为可编译 Kotlin 代码片段（每段 ≥ 2 行）
- 代码片段来自联网搜索的真实生产案例或 Android 官方最佳实践

**Non-Goals:**
- 不修改任何规则 ID 或等级
- 不新增或删除规则
- 不实现 CI 流水线脚本
- 不修改 §7.4 工具速查卡内容（仅补充 Compose Compiler Metrics）

## Decisions

### D1: 流水线内容清理策略 → 激进清理

| 章节 | 当前 | 变更 |
|------|------|------|
| §1.2 目标 | "双触发通道（PR 流水线全量扫描/本地 Agent）" | 改为 "开发者本地 AI Code Review" |
| §1.4 成功指标 | 「流水线制品」度量 | 改为「审查报告文件」度量 |
| §3.1 | 双通道 Mermaid 图 + 表格 | 仅保留本地 Agent 说明 |
| §3.2 输入表 | 通道 A/通道 B 双列 | 单列（本地 Agent） |
| §3.3 投递方式 | 「流水线制品库」第一选项 | 「本地 Markdown 文件」 |
| §3.4 Skill路径 | 「Skill/流水线均引用同一规则集」 | 「Skill 引用规则集」 |
| §3.6 SLA | 「通道 A（流水线全量扫描）」 | 移入 §13 |
| §5 流程图 | 以流水线为核心 | 重绘为纯本地流程 |
| §6 映射表 | 通道 A/通道 B 列 | 删除双通道列 |
| §7.2 路线图 | Phase 1-4 全表 | 仅保留 Phase 0 当前阶段 |

### D2: 代码片段来源策略

每条规则的代码片段按以下优先级选取：
1. **Android 官方文档** (developer.android.com) 中的最佳实践示例
2. **真实生产事故** (掘金/CSDN/proandroiddev/StackOverflow 中的故障复盘)
3. **Kotlin/Java 编码规范** 中的推荐写法

### D3: 代码片段格式

每条规则的反例/正例列使用以下格式：

```
反例: ```kotlin
// ❌ 反例原因简述
val handler = Handler(Looper.getMainLooper()) { msg ->
    textView.text = "Hello"  // Activity 销毁后 crash
}
```

正例: ```kotlin
// ✅ 弱引用 + 生命周期管理
private class SafeHandler(activity: MyActivity) : Handler(Looper.getMainLooper()) {
    private val ref = WeakReference(activity)
    override fun handleMessage(msg: Message) {
        ref.get()?.updateUI(msg)
    }
}
```

## Risks / Trade-offs

| 风险 | 缓解 |
|------|------|
| 大范围清理可能误删有效引用 | 每章清理后 grep 验证无残留流水线关键词 |
| 81 条规则全部改写代码片段，PRD 文件变大 3-5x | 接受——代码示例是 AI Skill 准确性的核心要素 |
| 联网搜索的代码案例版权 | 仅使用 URL 可公开访问的社区文章中的代码模式（非一字不差复制） |
| 部分 P2 规则（如 OBS-02 埋点）无标准 Kotlin 代码反例 | 提供配置/注解层面代码替代（如 BuildConfig 配置示例） |
