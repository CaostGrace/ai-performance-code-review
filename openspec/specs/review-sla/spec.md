# Purpose
定义流水线审查的 SLA 参数：超时保护、大 PR 降级、文件分段、并发限制。

## Requirements

### Requirement: 审查超时保护
流水线审查 SHALL 设置 300 秒超时。超时后 SHALL 立即产出已完成的 P0 发现项，并在报告中标注 `partial`。

#### Scenario: 超时前完成
- **WHEN** 审查在 300 秒内完成
- **THEN** 产出完整报告，无 partial 标记

#### Scenario: 超时
- **WHEN** 审查超过 300 秒
- **THEN** 产出部分报告，标注 `partial` 及遗漏维度

### Requirement: 大 PR 降级模式
变更文件超过 50 个时，审查 SHALL 进入大文件模式：核心文件全量审查，非核心文件 P1/P2 抽样审查，P0 仍全覆盖。

#### Scenario: PR 变更 60 个文件
- **WHEN** PR 变更文件数为 60
- **THEN** 报告标注 `large-pr`，列出跳过的非核心文件清单

### Requirement: 单文件分段审查
超过 2000 行的单文件 SHALL 按方法/类边界分段审查。

#### Scenario: 大文件分段
- **WHEN** 文件超过 2000 行
- **THEN** 按方法边界拆分独立审查，发现项合并至同一报告

### Requirement: 并发审查限制
流水线同时审查的 PR 数 SHALL 不超过 3 个。

#### Scenario: 5 个 PR 同时触发
- **WHEN** 5 个 PR 同时触发审查
- **THEN** 3 个立即执行，其余 2 个排队等待

### Requirement: 文件级预扫描
Skill SHALL 在路由阶段对每个变更文件执行轻量关键字预扫描（grep），根据扫描结果确定加载哪些维度规则文件。

#### Scenario: 关键字扫描
- **WHEN** 变更文件内容包含 `RecyclerView` 关键字
- **THEN** SHALL 标记为 View 体系文件，加载 `ui-view.md`

#### Scenario: 路径特征扫描
- **WHEN** 变更文件路径匹配 `build.gradle.kts`
- **THEN** SHALL 加载 `package.md`、`startup.md`
