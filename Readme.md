# Android 性能 CR Skill 介绍与使用

# android-performance-cr — Android 性能代码审查 Skill，支持自动识别 Java/Kotlin 代码变更，覆盖主线程、启动、UI 渲染、内存、网络、磁盘 I/O、后台电量、协程线程、包体依赖、可观测性、WebView、架构模块化共 12 个维度，81 条检查规则。

---

## 1. 背景

### 1.1 人工性能 Code Review 的工作方式

Android 性能 CR 主要依赖人工完成：

| 阶段 | 工作内容 | 工具/方式 |
|---|---|---|
| **变更识别** | 阅读 diff，判断涉及哪些性能维度 | git diff、IDE diff 视图 |
| **规则检索** | 查阅性能规范文档，逐条比对 | 内部 Wiki、规范文档 |
| **问题定位** | 阅读代码上下文，确认是否触发反模式 | IDE 代码阅读 |
| **报告撰写** | 填写 CR 评论，标注严重等级 | PR 平台评论、Markdown |
| **工具建议** | 凭经验推荐验证工具 | 个人经验积累 |

### 1.2 人工审查的局限

| 问题 | 具体表现 | 影响 |
|---|---|---|
| **覆盖不全** | 依赖个人经验，易遗漏不熟悉的维度 | 性能问题漏审入库 |
| **一致性差** | 不同 Reviewer 审查深度和标准不一 | 规则执行标准不统一 |
| **规则老化** | 文档更新滞后，新 API 反模式未收录 | 审查规则与实际脱节 |
| **门槛较高** | 需熟悉 12 个维度的全部规则 | 新人 Reviewer 上手困难 |
| **盲区不透明** | 不清楚哪些场景静态分析无法覆盖 | 误报或漏报风险 |

### 1.3 痛点总结

Android 性能 CR 依赖资深工程师的个人经验。Reviewer 变动或团队扩张时，审查质量难以保持稳定，性能问题往往在合入后才发现，修复成本较高。

---

## 2. 目标

### 2.1 版本目标

覆盖 Android 代码变更的 12 个性能维度，共 81 条规则，通过 Skill 自动化审查流程。

| 目标维度 | 具体指标 | 完成状态 |
|---|---|---|
| **规则覆盖** | 12 个维度 + 1 个 Compose 子维度，共 81 条规则 | ✅ |
| **P0 识别** | 主线程 IO、内存泄漏等 13 条 P0 规则可触发 | ✅ |
| **动态路由** | 两层路由（路径粗筛 + P0 兜底） | ✅ |
| **多输入模式** | 支持 git diff、@ 文件、commit hash 三种输入 | ✅ |
| **外置规则** | 支持项目级 overrides.md / custom-rules.md 覆盖 | ✅ |
| **盲区声明** | 9 类静态盲区明确标注，不臆造 P0 | ✅ |

### 2.2 当前版本（v0.0.1）

| 属性 | 说明 |
|---|---|
| **版本号** | v0.0.1 |
| **适用范围** | Android 客户端（Java/Kotlin），含 View 体系与 Jetpack Compose |
| **规则维度数** | 12 个维度 + Compose 专项子维度（§9.3.A） |
| **规则总数** | 81 条（含 13 条 P0 / 28 条 P1 / 40 条 P2） |
| **规则文件数** | 14 个按维度拆分的 `.md` 文件 + 1 个 P0 必查规则文件 |

#### 已实现功能

- 两层动态规则路由（路径/关键字粗筛 + P0 分级兜底）
- 12 维度 81 条性能检查规则，含完整反例/正例 Kotlin 代码
- Compose 专项规则（CP-01 ~ CP-08，使用 `CP-` 前缀 ID）
- 三重判定逻辑（精确匹配 / 模式可疑 / 架构担忧）
- 外置规则支持（项目级 overrides.md + custom-rules.md）
- 9 类静态盲区声明，遇到盲区输出"需人工"而非臆造 P0
- 审查超时保护（300 秒超时 + 大 PR 降级模式）
- 工具速查卡（9 个核心性能分析工具）


### 2.3 Skill 项目结构

#### 目录结构

```
android-performance-cr/
├── SKILL.md                         # 核心 Skill 定义（含 YAML front matter）
├── rules/                           # 按维度拆分的规则文件（14 个）
│   ├── main-thread.md               # 主线程安全
│   ├── startup.md                   # 启动性能
│   ├── ui-view.md                   # UI 渲染（View 体系）
│   ├── ui-compose.md                # UI 渲染（Compose 专项，CP- 前缀）
│   ├── memory.md                    # 内存管理
│   ├── network.md                   # 网络性能
│   ├── disk-io.md                   # 磁盘 I/O
│   ├── background.md                # 后台电量
│   ├── threading.md                 # 协程与线程
│   ├── package.md                   # 包体与依赖
│   ├── observability.md             # 可观测性
│   ├── webview.md                   # WebView 性能
│   ├── architecture.md              # 架构与模块化
│   └── p0-safety-net.md             # P0 必查规则集（L0/L1 分级兜底）
└── references/                      # 辅助参考文档
    ├── tools.md                     # 工具速查卡（9 个核心性能分析工具）
    └── external-rules-guide.md      # 外置规则编写教程
```

#### 核心文件

| 文件 | 用途 |
|---|---|
| **SKILL.md** | Skill 定义，包含输入解析、路由、规则调度、输出格式化、超时控制 |
| **rules/p0-safety-net.md** | P0 必查规则集：L0（永远注入：MEM-01/MEM-02/TH-05）+ L1（按文件语言注入：MT-01～06 等） |

#### rules/ 规则文件分类

| 文件 | 维度 | 代表规则 |
|---|---|---|
| **main-thread.md** | 主线程安全 | MT-01（主线程 SharedPreferences 读写）、MT-05（主线程 Binder 调用）|
| **startup.md** | 启动性能 | ST-01（Application.onCreate 主线程初始化）、ST-03（ContentProvider 重量级初始化）|
| **ui-view.md** | UI 渲染 View 体系 | UI-01（onDraw 对象分配）、UI-03（过度绘制）|
| **ui-compose.md** | UI 渲染 Compose 专项 | CP-01（LazyColumn key 稳定性）、CP-02（@Stable/@Immutable 注解）|
| **memory.md** | 内存管理 | MEM-01（Activity 静态持有）、MEM-04（Bitmap 未释放）|
| **network.md** | 网络性能 | NET-01（主线程网络请求）、NET-03（无效缓存策略）|
| **disk-io.md** | 磁盘 I/O | IO-01（主线程文件读写）、IO-03（未使用批量写入）|
| **background.md** | 后台电量 | BG-01（Foreground Service 滥用）、BG-05（高频 AlarmManager）|
| **threading.md** | 协程与线程 | TH-01（IO 操作在 Default 调度器）、TH-05（GlobalScope 滥用）|
| **package.md** | 包体与依赖 | PKG-01（引入大体积第三方库）、PKG-03（重复依赖）|
| **observability.md** | 可观测性 | OBS-01（关键路径缺少日志/埋点）、OBS-02（异常无 log 吞掉）|
| **webview.md** | WebView 性能 | WV-01（主线程首次初始化 WebView）、WV-03（JS Bridge 高频大对象）|
| **architecture.md** | 架构与模块化 | ARCH-01（跨模块大对象传递）、ARCH-02（模块循环依赖）|

#### references/ 辅助文档

| 文件 | 说明 |
|---|---|
| **tools.md** | 工具速查卡，覆盖 StrictMode、Systrace、Perfetto、LeakCanary、Memory Profiler、Battery Historian、APK Analyzer、Database Inspector、Network Profiler 共 9 个工具，每项含安装/启用方式、核心命令/操作步骤、关键输出解读 |
| **external-rules-guide.md** | 外置规则编写教程，含 overrides.md 三种操作（disable/demote/promote）和 custom-rules.md 七列写法，每种操作含正反例 |

#### 核心组件

**1. 两层动态路由**

- **第一层（粗筛）**：基于文件路径（如 `Application`、`ContentProvider`）和代码关键字（如 `@Composable`）确定应加载的维度规则文件
- **第二层（P0 兜底）**：L0 规则（MEM-01/02、TH-05）永远注入；L1 规则在非资源文件变更时注入
- 支持影响半径扩展（如变更 `Application.onCreate` 时联动加载 startup/main-thread/memory 三个维度）

**2. 三重判定逻辑**

- **精确匹配**：代码精确命中反例模式 + 可定位具体行 → 按规则原等级报告
- **模式可疑**：模式相似但无法确定 → 降一级报告，标注"需人工确认"
- **架构担忧**：结构性风险，无法精确定位 → 报告 P2 架构担忧，提供重构建议

**3. 外置规则系统**

- 项目级规则目录：`<项目根>/.android-performance-cr/`
- `overrides.md`：覆盖内置规则等级/行为（disable / demote / promote）
- `custom-rules.md`：追加项目专用规则（七列格式与内置规则一致）
- 工作区切换时自动重新加载

**4. 审查超时保护与大 PR 降级**

- 300 秒超时保护：超时后立即产出已完成的 P0 发现项，报告标注 `partial`
- 大 PR 降级（> 50 个变更文件）：核心文件全量审查，非核心文件 P1/P2 抽样，P0 仍全覆盖

#### 支持的输入类型

| 输入模式 | 触发条件 | 说明 |
|---|---|---|
| **自动 git diff** | 未 @ 任何文件时 | 自动执行 `git diff` 获取未提交变更 |
| **手动 @ 文件** | @ 指定文件或目录 | 仅审查指定范围内的文件 |
| **commit hash** | 输入 7-40 位 hex | 通过 `git show <hash>` 审查已提交变更 |


### 2.4 用法示例

#### 触发方式

在对话中使用以下关键词即可触发，或在 Skills 面板中手动调用：

| 触发词 | 说明 |
|---|---|
| **分析性能问题** | 对当前 diff 进行性能审查 |
| **性能 CR** / **性能代码审查** | 全量执行 12 维度审查 |
| **Android 性能审查** | 指定 Android 性能维度 |
| **检查内存泄漏** | 重点审查内存维度（自动叠加 P0 兜底）|
| **审查这段代码** + @ 文件 | 审查指定文件 |
| **commit 性能审查** + hash | 审查指定 commit 的性能问题 |

#### 使用场景示例

**场景一：提交前自检**

```plaintext
用户："帮我做一下性能 CR"
响应：
  1. 执行 git diff，获取未提交变更集
  2. 路由分析：检测到 ViewModel 变更 → 加载 memory.md / threading.md
  3. P0 兜底：L0 规则（MEM-01/02、TH-05）永远注入
  4. 三重判定：MEM-01 精确匹配 → 报告 P0
  5. 输出报告到 ./android-performance-cr-report.md
  6. 摘要："发现 2 个 P0 / 1 个 P1 / 3 个 P2，建议合入前修复 P0"
```

**场景二：Compose 页面审查**

```plaintext
用户："审查一下这个 Compose 页面" @ui/HomeScreen.kt
响应：
  1. 检测到 @Composable 关键字 → 加载 ui-compose.md (CP-01~CP-08)
  2. 检测到 LazyColumn → CP-01 检查 key 稳定性
  3. 检测到数据类 → CP-02 检查 @Stable/@Immutable 注解
  4. 报告：CP-02 P1 — HomeUiState 未标注 @Stable，可能导致不必要的全树重组
  5. 输出报告，附 Compose Compiler 验证命令
```

**场景三：外置规则定制**

```plaintext
用户："我们项目禁用了 MEM-03，另外新增了一条业务规则"
配置：
  .android-performance-cr/
  ├── overrides.md     # disable: MEM-03
  └── custom-rules.md  # BIZ-01: 禁止在 Payment 模块使用 Handler
响应：
  1. 加载项目外置规则
  2. MEM-03 已禁用，审查时跳过
  3. BIZ-01 追加到规则集，Payment 相关变更触发检测
```

**场景四：静态盲区处理**

```plaintext
用户："帮我检查这个 JNI 接口的性能问题" @jni/NativeProcessor.cpp
响应：
  1. 检测到 System.loadLibrary → 识别 JNI 盲区
  2. 不臆造 P0 发现项
  3. 在「未覆盖/需人工」中标注：
     "JNI 调用耗时不可静态评估，建议使用 Perfetto systrace 验证 native 执行时间"
  4. 附 Perfetto 抓取命令和关键输出解读
```

---

## 3. 开发计划

### 3.1 已完成阶段

| 阶段 | 名称 | 主要成果 | 完成时间 |
|---|---|---|---|
| **Phase 1** | 核心规则建设 | 12 维度规则框架，P0/P1/P2 分级体系 | 2026 年 6 月 |
| **Phase 2** | Skill 工程化 | 多文件目录结构、YAML front matter、rules/ + references/ 分层 | 2026 年 6 月 |
| **Phase 3** | 智能路由 | 两层动态路由（路径粗筛 + P0 分级兜底）、三重判定逻辑 | 2026 年 6 月 |
| **Phase 4** | 扩展能力 | Compose 专项规则（CP-01~08）、外置规则系统、超时保护 | 2026 年 6 月 |
| **Phase 5** | 质量规范 | 代码示例标准、工具速查卡、外置规则教程、盲区声明 | 2026 年 6 月 |

### 3.2 阶段能力演进

| 阶段 | 能力方向 | 演进关系 |
|---|---|---|
| **Phase 1** | 规则定义 | 基础，支撑后续所有功能 |
| **Phase 2** | Skill 工程化 | 将规则封装为可执行的 Agent Skill |
| **Phase 3** | 智能路由 | 提升审查效率，避免无关规则干扰 |
| **Phase 4** | 扩展能力 | 覆盖更多场景（Compose、外置规则） |
| **Phase 5** | 质量保障 | 提升报告可信度和使用体验 |

**演进路径**：规则定义 → Skill 工程化 → 智能路由 → 扩展能力 → 质量保障

### 3.3 执行流程

| 检查点 | 名称 | 说明 | 是否必须 |
|---|---|---|---|
| **CP1** | 输入解析 | 确定输入模式（git diff / @ 文件 / commit hash），获取变更集 | 是 |
| **CP2** | 路由分析 | 第一层路径/关键字粗筛，确定应加载的维度规则文件 | 是 |
| **CP3** | P0 兜底 | L0 永远注入，L1 按文件语言注入 | 是 |
| **CP4** | 规则审查 | 加载规则文件，三重判定，外置规则合并 | 是 |
| **CP5** | 报告生成 | 按格式规范输出 Markdown 报告到固定路径 | 是 |
| **CP6** | 盲区标注 | 识别静态盲区，在「需人工」部分标注，不臆造 P0 | 是 |

**执行顺序**：CP1 → CP2 → CP3 → CP4 → CP5 → CP6

---

## 4. 阶段点汇报

### 4.1 已完成阶段

| 阶段 | 完成时间 | 成果 | 关键指标 |
|---|---|---|---|
| **规则框架** | 2026 年 6 月 | 12 维度规则框架，81 条规则（13 P0 / 28 P1 / 40 P2）| P0 识别准确率目标 > 95% |
| **Skill 工程化** | 2026 年 6 月 | 多文件目录结构，YAML front matter，14 个规则文件 | 目录结构符合通用 Skill 规范 |
| **智能路由** | 2026 年 6 月 | 两层动态路由 + 三重判定逻辑 | 规则加载精准率目标 > 90% |
| **扩展能力** | 2026 年 6 月 | Compose 专项 8 条规则，外置规则系统，超时保护 | 支持项目级规则自定义 |
| **质量规范** | 2026 年 6 月 | 代码示例全覆盖，9 个工具速查卡，9 类盲区声明 | 每条 P0 规则含正反例代码 |

### 4.2 阶段成果对比

| 指标 | 人工审查 | Skill 辅助 |
|---|---|---|
| **审查时间** | 10-20 分钟 / PR | 约 5-10 分钟 / PR（含人工复核）|
| **规则覆盖率** | 依赖 Reviewer 个人经验 | 12 维度 81 条规则系统性覆盖 |
| **P0 识别可靠性** | 易因经验不足漏审 | 13 条 P0 规则强制兜底（L0/L1）|
| **Compose 专项** | 需 Compose 专家参与 | 8 条 CP- 规则自动检测 |
| **一致性** | Reviewer 间差异大 | 规则标准化，判定逻辑透明 |
| **工具建议** | 凭经验推荐，不成体系 | 9 个工具速查卡，含具体命令 |

---

## 5. 预期收益

> 以下收益基于当前 v0.0.1 版本。Skill 已具备 12 维度 81 条规则的系统化覆盖、P0 强制兜底、动态路由和三重判定能力，接入后即可体现。

### 5.1 核心收益对比

| 收益维度 | 人工审查 | Skill 辅助（v0.0.1） | 变化 |
|---|---|---|---|
| **审查时间** | 10-20 分钟 / PR | 约 5-10 分钟 / PR（含人工复核） | 缩短约一半 |
| **规则覆盖率** | 依赖个人经验，覆盖率有限 | 12 维度 81 条规则系统性覆盖 | 覆盖面更全 |
| **P0 漏审率** | 新人 Reviewer 容易遗漏 P0 问题 | 13 条 P0 规则强制兜底（L0 + L1） | 遗漏减少 |
| **Reviewer 门槛** | 需熟悉全部 12 维度规则才能审查 | 自动路由匹配维度，Reviewer 聚焦判断 | 门槛降低 |
| **审查一致性** | 不同 Reviewer 审查标准差异大 | 规则标准化 + 三重判定逻辑 | 一致性改善 |
| **工具建议** | 凭经验推荐，不成体系 | 9 个工具速查卡，含安装/命令/解读 | 建议可操作 |
| **Compose 专项** | 需 Compose 专家参与 | 8 条 CP- 规则自动检测 | 降低对专家的依赖 |
| **盲区透明度** | 不清楚哪些场景无法静态覆盖 | 9 类盲区声明，遇到输出"需人工" | 减少误报 |

### 5.2 典型收益场景

| 场景 | 人工方式 | Skill 辅助后 | 关键收益 |
|---|---|---|---|
| **新人提交 PR** | Reviewer 逐项检查性能问题，耗时较长 | Skill 产出审查报告，Reviewer 复核 P0 项即可 | 新人不因经验不足漏审 |
| **Compose 页面开发** | 团队缺 Compose 性能专家，重组/稳定性问题难发现 | CP-01~08 自动检测 LazyColumn key、@Stable 注解等 | 补上 Compose 性能审查短板 |
| **跨模块重构** | 架构维度规则多，人工容易遗漏循环依赖等 | ARCH-01/02 自动检测跨模块大对象传递、循环依赖 | 架构风险提前发现 |
| **外置规则定制** | 团队特有规则无标准化管理方式 | overrides.md 禁用/降级规则 + custom-rules.md 追加规则 | 规则随项目演进，热加载生效 |

### 5.3 投入与回报

| 项目 | 说明 |
|---|---|
| **接入成本** | 安装 Skill 即可使用，无需额外配置 |
| **定制成本** | 按需添加 `.android-performance-cr/` 目录，编写 overrides.md / custom-rules.md |
| **学习成本** | 12 维度规则由 Skill 自动路由，Reviewer 无需逐条学习 |
| **回报** | 首次使用即可产出结构化审查报告，P0 问题直接可见 |

---

## 6. 后续优化

### 可优化项（规划中）

| 优化项 | 描述 | 收益 |
|---|---|---|
| **Lint 规则映射** | 将高频 P0 规则转化为 Android Lint 规则 | CR 前置到编译阶段 |
| **CI 流水线集成** | 在 CI 中自动触发性能审查，结果写入 PR 评论 | 无需人工触发 |
| **架构健康度评分** | 基于审查历史数据，输出模块级架构健康度评分 | 辅助架构演进决策 |
| **智能重构建议** | 基于审查结果生成具体重构方案（含代码示例） | 直接辅助开发者修复 |
| **跨项目规则共享** | 外置规则支持团队级共享仓库 | 组织内规则标准统一 |

---

## 7. 版本列表

### v0.0.1（当前版本）

| 属性 | 说明 |
|---|---|
| **版本** | v0.0.1 |
| **特性** | 12 维度 81 条规则，两层动态路由，三重判定，外置规则，超时保护 |
| **OpenSpec changes** | 7 个已归档 change（2026-06-03 ~ 2026-06-06） |

**已归档的变更（openspec/changes/archive/）**：

| 变更目录 | 内容 |
|---|---|
| `2026-06-03-prd-v13-optimization` | PRD v1.3 规则优化 |
| `2026-06-03-prd-v2-comprehensive-coverage` | PRD v2 全面覆盖 |
| `2026-06-03-prd-v3-pipeline-cleanup-code-examples` | 流水线清理与代码示例补全 |
| `2026-06-05-implement-android-perf-cr-skill` | Skill 主体实现 |
| `2026-06-05-normalize-skill-metadata-and-structure` | Skill 元数据与目录结构规范化 |
| `2026-06-06-add-commit-review` | 新增 commit hash 输入模式 |
| `2026-06-06-add-external-rules-guide` | 新增外置规则编写教程 |

---

## 8. 附录：9 类静态审查盲区说明

本 Skill 以下场景因静态分析的固有限制无法可靠评估，遇到时只会输出「需人工」提示，**不会臆造 P0 发现项**：

| 盲区类型 | 触发场景 | 建议工具 |
|---|---|---|
| **Native 内存** | JNI malloc/new 操作 | Perfetto / Address Sanitizer |
| **JNI 调用耗时** | `System.loadLibrary` / `.cpp` 文件 | Perfetto systrace |
| **反射调用** | `Class.forName` / `Method.invoke` | Android Profiler |
| **动态代理** | `Proxy.newProxyInstance` 等 | Android Studio Debugger |
| **第三方 SDK 内部** | 闭源 SDK 初始化链 | Battery Historian / Perfetto |
| **运行时 UI 帧率** | 仅静态代码，无实际渲染数据 | Systrace / Choreographer 日志 |
| **实际内存占用** | 无 heap dump 数据 | Memory Profiler / LeakCanary |
| **网络实际延迟** | 无网络抓包数据 | Network Profiler / Charles |
| **电量实际消耗** | 无设备实测数据 | Battery Historian |
