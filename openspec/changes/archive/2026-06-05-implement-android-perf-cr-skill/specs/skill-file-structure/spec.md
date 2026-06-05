## ADDED Requirements

### Requirement: Skill 文件组织结构
Skill SHALL 采用多文件结构：1 个 SKILL.md 入口文件 + 14 个按维度拆分的规则文件 + 1 个工具速查卡文件。SKILL.md SHALL 包含触发说明、输出模板、路由逻辑，不包含规则清单内容。

#### Scenario: Skill 目录结构
- **WHEN** Skill 部署到 IDE 中
- **THEN** 目录结构 SHALL 为 `android-performance-cr/` 根目录下包含 `SKILL.md`、`rules/`（含 14 个 `.md` 文件）、`tools.md`

#### Scenario: SKILL.md 职责边界
- **WHEN** 开发者触发 Skill 审查
- **THEN** SKILL.md SHALL 负责输入解析、路由决策、规则文件加载调度、输出格式化；规则文件 SHALL 仅包含检查项定义（含反例/正例）

### Requirement: 规则文件按维度命名
每个规则文件 SHALL 对应 PRD §9 的一个维度，命名 SHALL 与维度语义一致：`main-thread.md`、`startup.md`、`ui-view.md`、`ui-compose.md`、`memory.md`、`network.md`、`disk-io.md`、`background.md`、`threading.md`、`package.md`、`observability.md`、`webview.md`、`architecture.md`。

#### Scenario: 规则文件命名一致性
- **WHEN** 审查加载某维度规则
- **THEN** 文件名 SHALL 可直接映射到 §9 的子章节编号（如 `main-thread.md` → §9.1）

### Requirement: P0 必查规则文件优先加载
P0 必查规则集文件 `_must-check.md` SHALL 使用 `_` 前缀命名，确保在文件列表中排在第一位。路由逻辑 SHALL 在加载任何维度规则前优先加载该文件。

#### Scenario: _must-check.md 加载优先级
- **WHEN** 审查启动，读取 `rules/` 目录
- **THEN** `_must-check.md` SHALL 在文件列表中排在首位，并被第一个加载
