## 1. 项目骨架搭建

- [x] 1.1 创建 `android-performance-cr/` 目录及所有子目录
- [x] 1.2 创建 `SKILL.md` 入口文件（触发说明 + 输出模板 + 路由逻辑框架）
- [x] 1.3 创建 `tools.md` 工具速查卡文件（§7 内容迁移）

## 2. P0 必查规则集

- [x] 2.1 创建 `rules/_must-check.md`，包含 L0 规则（MEM-01, MEM-02, TH-05）完整定义
- [x] 2.2 在 `_must-check.md` 中补充 L1 规则（MT-01/02/03/06, BG-01/05, ST-01, IO-01）完整定义
- [x] 2.3 标记每条规则的 L0/L1 分级

## 3. 维度规则文件（12 维度 + Compose 子维度）

- [x] 3.1 创建 `rules/main-thread.md`（MT-01~MT-07）
- [x] 3.2 创建 `rules/startup.md`（ST-01~ST-07）
- [x] 3.3 创建 `rules/ui-view.md`（UI-01~UI-09）
- [x] 3.4 创建 `rules/ui-compose.md`（CP-01~CP-08）
- [x] 3.5 创建 `rules/memory.md`（MEM-01~MEM-08）
- [x] 3.6 创建 `rules/network.md`（NET-01~NET-06）
- [x] 3.7 创建 `rules/disk-io.md`（IO-01~IO-05）
- [x] 3.8 创建 `rules/background.md`（BG-01~BG-06）
- [x] 3.9 创建 `rules/threading.md`（TH-01~TH-06）
- [x] 3.10 创建 `rules/package.md`（PKG-01~PKG-06）
- [x] 3.11 创建 `rules/observability.md`（OBS-01~OBS-04）
- [x] 3.12 创建 `rules/webview.md`（WV-01~WV-04）
- [x] 3.13 创建 `rules/architecture.md`（ARCH-01~ARCH-04）

## 4. 路由逻辑实现

- [x] 4.1 在 SKILL.md 中实现第一层路由：路径/关键字映射表（§6.1 路径启发式 + §6.2 影响半径）
- [x] 4.2 实现文件级语言体系识别（@Composable → Compose, RecyclerView/findViewById → View）
- [x] 4.3 实现第二层路由：P0 必查兜底加载（L0 永远注入 + L1 按文件语言注入）
- [x] 4.4 实现双输入模式（自动 git diff + 手动 @ 文件）

## 5. 审查执行逻辑

- [x] 5.1 在 SKILL.md 中实现三重判定逻辑（精确匹配/可疑降级/架构担忧写需人工）
- [x] 5.2 实现 §3.7 盲区检测（遇到盲区类型时不臆造 P0，写入需人工）
- [x] 5.3 实现 OBS-01 Phase 0 策略（发现项为空时自动追加验证建议提示）
- [x] 5.4 实现外置规则热加载逻辑（读取 `.android-performance-cr/overrides.md` 和 `custom-rules.md`）

## 6. 输出格式控制

- [x] 6.1 在 SKILL.md 中编写强约束输出 prompt（严格按 §3.3 模板，不得增减字段）
- [x] 6.2 实现报告固定路径输出 `./android-performance-cr-report.md`（每次覆盖）
- [x] 6.3 编写 Markdown 格式校验脚本（检查合入建议行、表格结构、P0 行含文件:行号）

## 7. 冒烟测试

- [x] 7.1 从 §9 规则反例中提取 P0 规则（13 条）的代码片段作为测试输入
- [x] 7.2 验证每个 P0 反例能触发对应规则 ID
- [x] 7.3 验证 P0 正例不触发误报
- [x] 7.4 验证三重判定逻辑（构造一个可疑模式、一个架构担忧场景）

## 8. PRD 文档更新

- [x] 8.1 更新 PRD 至 v3.1，回写 grill-me 确认的全部设计决策
- [x] 8.2 更新 §3.4 Skill 文件结构（替换为实际多文件结构）
- [x] 8.3 更新 §3.5 规则加载机制（补充路由逻辑和必查规则集）
- [x] 8.4 更新 §4 规则分级（补充三重判定逻辑）
- [x] 8.5 更新 §5 CR 流程（补充双输入模式、P0 清零策略）
- [x] 8.6 更新 §10.4 待决策开放项（标记已决议项）
