## Why

PRD v1.3 的规则清单存在三个关键缺口：
1. **Compose 性能覆盖严重不足**（仅 2 条规则），现代 Android 应用中 Compose 性能问题已成为 ANR 和卡顿的高频来源
2. **§11「后续可选规则」6 条主题长期悬置**，包括 Google Play 强制要求的 16KB 页对齐和 Baseline Profile 等关键检查项，却未纳入正式规则流程
3. **架构/模块化维度完全缺失**，多模块项目中的跨模块通信开销、循环依赖、Dynamic Feature 加载时机等性能风险无法审查

同时，当前 PRD 的工具链描述仅列工具名称，缺少具体安装方式、核心命令和输出解读，导致 AI Skill 在遇到静态审查盲区时无法给出可操作的工具使用建议。流水线/CI 配置（§7.2 Phase 2-4、§7.3）与当前聚焦的「Skill AI Code Review 流程」目标不一致，需后移到专门章节。

## What Changes

- **§11 6 条兜底规则全部转正**为正式规则，补全 ID/等级/反例/正例/判定/参考工具七列
- **新增 Compose 性能专项子维度**（10.3.A），从 2 条扩展到 8 条规则，覆盖 LazyColumn key、@Stable 注解、LaunchedEffect、Modifier lambda、derivedStateOf 等核心性能场景
- **新建 §10.12 架构与模块化维度**，含 4 条规则（跨模块序列化开销、循环依赖、Dynamic Feature 加载、多进程通信）
- **新增 §7.4 工具使用速查卡**，覆盖 StrictMode / Systrace / Perfetto / LeakCanary / Memory Profiler / Battery Historian / APK Analyzer / Database Inspector / Network Profiler，每工具提供安装方式、核心命令、关键输出解读
- **重构流水线内容**：将 §7.2 Phase 2-4 与 §7.3「流水线与本地集成」移至新增的「§11 后期处理：流水线与 CI」章节
- **补充真实错误案例**：联网搜集的 runBlocking ANR、GlobalScope 泄漏、Handler 泄漏、WebView 未销毁等生产环境典型案例写入规则的反例/正例

## Capabilities

### New Capabilities
- `compose-performance`: Compose 专项性能审查规则（8 条），覆盖重组范围、稳定性注解、Effect key、Modifier 优化、derivedStateOf 等
- `architecture-modularization`: 架构与模块化性能审查规则（4 条），覆盖跨模块通信、循环依赖、Dynamic Feature、多进程 Binder 开销
- `tool-reference`: 工具使用速查卡（9 个工具），提供安装方式、核心命令、关键输出解读

### Modified Capabilities
- `rule-checklist`: 新增约 19 条规则（ST-07 Baseline Profile、PKG-06 16KB 页对齐、UI-09 RecyclerView DiffUtil、MEM-08 大图硬件位图、CP-01~08 Compose 专项、ARCH-01~04 架构模块化）；§11 后续可选规则移除（已转正）；流水线内容移至 §11 后期处理

## Impact

- **影响文件**：`Android 性能 CR AI Code Review 技能 prd文档.md`（主 PRD 文档）
- **影响章节**：§7（工具与路线图）、§10（规则清单）、§11（内容重组）
- **受影响规范**：`rule-checklist`（规则数量从 ~64 增至 ~83 条）、`output-format`（无变更，但工具引用增强）
- **向后兼容**：所有现有规则 ID 保持不变，仅追加新规则；Compose 规则使用 CP- 前缀与 UI- 前缀区分
