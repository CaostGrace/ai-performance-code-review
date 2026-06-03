## ADDED Requirements

### Requirement: 误报反馈标记
Reviewer SHALL 能够通过 `#false-positive` 标签标记 AI 审查的误报项，标签后跟规则 ID。

#### Scenario: 标记误报
- **WHEN** Reviewer 在 PR 讨论中输入 `#false-positive MT-03`
- **THEN** 该反馈被记录，关联到规则 MT-03 的误报统计

### Requirement: 误报自动聚合
系统 SHALL 每周自动聚合各规则 ID 的误报率。单规则误报率连续 2 周超过 20% SHALL 触发规则修订流程。

#### Scenario: 误报率超过阈值
- **WHEN** 规则 MT-03 连续 2 周误报率 > 20%
- **THEN** 自动通知性能组，触发规则反例/正例描述调整或等级降级

### Requirement: 双周审查校准
Team Leader SHALL 每两周组织审查校准：抽取 5-10 个已合入 PR，AI 重审 + Reviewer 独立审查，对比差异并输出校准报告。

#### Scenario: 校准发现系统性差异
- **WHEN** 校准中发现某规则 AI 与人工结论系统性分歧
- **THEN** 记录差异，更新规则描述或判定条件

### Requirement: 漏报回注
合入后发现的性能问题（线上 ANR、卡顿归因、内存泄漏）SHALL 由性能组判断是否可用静态规则覆盖，并回注规则集。

#### Scenario: 线上 ANR 可归因为静态规则
- **WHEN** 线上 ANR 被判定为"主线程同步 SP 写入"且无对应发现项
- **THEN** 反查审查报告，若 AI 遗漏则作为漏报记录，优化规则判定描述
