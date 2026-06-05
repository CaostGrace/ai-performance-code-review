## Context

PRD v3.0 定义了 81 条 Android 性能 CR 规则，但 Skill 的具体实现架构尚未确定。通过 grill-me 会话，确认了 15 个关键设计决策，涵盖文件结构、动态路由、P0 兜底、判定逻辑、交互模型、输出控制等。

## Goals / Non-Goals

**Goals:**
- 将 PRD §9 的 81 条规则落地为可工作的多文件 Skill
- 通过动态路由控制上下文窗口消耗
- 保证 P0 致命问题不因路由漏报
- 正反例代码可直接作为冒烟测试用例
- 平台无关的 Markdown 输出，可被脚本解析

**Non-Goals:**
- 不实现 Lint 规则或 CI 流水线（Phase 1+）
- 不做规则自动去重（Phase 0）
- 不支持 override 修改判定条件（仅改等级）
- 不做 OBS-01 自动阻塞判定（Phase 0 仅提示）

## Decisions

### D1: 多文件结构 + SKILL.md 做路由器

Skill 拆分为 1 个入口文件 + 14 个维度规则文件 + 1 个工具速查卡：

```
android-performance-cr/
├── SKILL.md                  # 总入口：触发说明 + 输出模板 + 路由逻辑
├── rules/
│   ├── _must-check.md        # P0 必查规则集（L0 + L1）
│   ├── main-thread.md        # §9.1 MT-01~MT-07
│   ├── startup.md            # §9.2 ST-01~ST-07
│   ├── ui-view.md            # §9.3 UI-01~UI-09
│   ├── ui-compose.md         # §9.3.A CP-01~CP-08
│   ├── memory.md             # §9.4 MEM-01~MEM-08
│   ├── network.md            # §9.5 NET-01~NET-06
│   ├── disk-io.md            # §9.6 IO-01~IO-05
│   ├── background.md         # §9.7 BG-01~BG-06
│   ├── threading.md          # §9.8 TH-01~TH-06
│   ├── package.md            # §9.9 PKG-01~PKG-06
│   ├── observability.md      # §9.10 OBS-01~OBS-04
│   ├── webview.md            # §9.11 WV-01~WV-04
│   └── architecture.md       # §9.12 ARCH-01~ARCH-04
└── tools.md                  # §7 工具速查卡（按需引用）
```

- `_must-check.md` 用 `_` 前缀排在文件列表第一位，加载顺序自然优先
- 路由逻辑控制在 SKILL.md 内 40 行以内
- tools.md 不每次加载，仅在建议引用工具时按需读取

### D2: 两层动态路由

**第一层 — 路径/关键字粗筛**：按 §6.1 路径启发式 + §6.2 影响半径，对每个变更文件做关键字扫描（grep），确定加载哪些维度规则文件。

**第二层 — P0 必查兜底**：无论路由结果，始终注入 `_must-check.md`，分两级：
- **L0（永远注入）**：MEM-01, MEM-02, TH-05 — 无论改什么代码都可能引入的致命问题
- **L1（按文件语言注入）**：MT-01/02/03/06, BG-01/05, ST-01, IO-01 — 仅在非资源文件变更时注入

**Trade-off: MEM-06（P0 Handler 泄漏）不在兜底集**：MEM-06 仅随 `memory.md` 被路由加载时审查。若审查纯网络/包体 diff 且路由不触发 `memory.md`，该 P0 可能漏报。理由：保持 L0 精简（3 条）+ L1 覆盖高发主线程/启动违规，Handler 泄漏模式通常伴随 Activity/Fragment 关键字触发 `memory.md` 路由。Phase 1+ 可根据线上漏报数据决定是否纳入 L1。

### D3: 文件级语言体系识别

对每个变更文件做极轻量关键字扫描：
- 含 `@Composable` / `Composable` → 标记为 Compose 文件，加载 `ui-compose.md`
- 含 `RecyclerView` / `findViewById` / `<LinearLayout` 等 → 标记为 View 文件，加载 `ui-view.md`
- 两者都不含 → 不加载 UI 专项规则
- 两者都含 → 同时加载两个文件

避免 View 文件被喂 Compose 规则、Compose 文件被喂 View 规则。

### D4: 三重判定逻辑

AI 发现可疑代码后的定级规则：

| 匹配度 | 代码位置明确 | 行为 |
|--------|-------------|------|
| 精确匹配反例 | 是 | 按规则原等级报告（P0/P1/P2） |
| 模式可疑但不确定 | 是 | 降一级报告（P0→P1，P1→P2），注明"需人工确认" |
| 架构担忧无代码证据 | 否 | 写入"未覆盖/需人工"，不报告等级 |

### D5: 双输入模式（C 模式）

- 用户 @ 了文件 → 审查指定文件范围
- 用户未 @ 任何文件 → 自动取 `git diff`（已暂存 + 未暂存）
- 行号使用 diff 生成时的文件绝对行号

### D6: 输出格式控制

- 报告固定路径 `./android-performance-cr-report.md`（项目根），每次覆盖
- Phase 0 用纯 Markdown 表格 + 简单正则做 CI 解析
- SKILL.md 用强约束 prompt + 输出示例控制格式
- Phase 0 开发时写 Markdown 格式校验脚本（检查合入建议行、表格结构、P0 行含文件:行号）

### D7: 外置规则热加载

- 外置规则随工作区切换自动热加载，无需手动 reload
- Phase 0 不做自动去重（双报通过人工 `#false-positive` 标记回注）
- overrides.md 仅支持改等级（disable/override），不支持修改判定条件
- 阈值定制需求走 custom-rules.md 的 add 新规则

### D8: P0 清零策略

- 强制要求重跑 Skill 才能清 P0，不接受纯人工备注声明
- 例外合入 P0 须 Team Leader 批准，PR 记录原因 + 偿还计划 + 监控项

### D9: OBS-01 策略（Phase 0）

Phase 0 不把 OBS-01 作为阻塞项。AI 在"发现项"为空的报告中自动追加提示：
"若改动涉及主线程/启动/内存/IO 路径，建议补充验证方式。"

### D10: 实现策略

- 全量一次性实现 81 条规则，不分批
- 正反例代码直接作为冒烟测试用例
- 规则文件保留反例/正例 Kotlin 代码块（few-shot 示例价值）
- 工具速查卡独立文件，按需引用

### D11: 平台无关

按通用 Skill 规范实现，不绑定 Cursor/CodeBuddy 特定平台机制。

## Risks / Trade-offs

- [R1] **全量 81 条一次性实现工作量大** → 按维度文件拆分，每个规则文件独立可测试；正反例直接来自 PRD，无需从零编写
- [R2] **路由可能漏报 P0** → L0 永远注入 + L1 按文件语言注入，双重兜底
- [R3] **格式不稳定导致 CI 解析失败** → Phase 0 开发格式校验脚本，Phase 2 若不稳定率 > 5% 引入 JSON 中间格式
- [R4] **外置规则热加载覆盖冲突** → Phase 0 不做自动去重，通过 `#false-positive` 反馈回注，Phase 2 再考虑规则指纹去重
- [R5] **三重判定"模式可疑"边界模糊** → 以精确反例匹配为第一优先，只有明显不符合反例但近似时走降级路径
