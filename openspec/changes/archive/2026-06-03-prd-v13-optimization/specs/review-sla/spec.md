## ADDED Requirements

### Requirement: 审查超时保护
通道 A 流水线审查 SHALL 设置 300 秒超时。超时后 SHALL 立即产出已完成的 P0 发现项，并在报告中标注 `partial` 及遗漏维度清单。

#### Scenario: 审查在超时前完成
- **WHEN** 审查在 300 秒内完成所有维度
- **THEN** 产出完整报告，无 partial 标记

#### Scenario: 审查超时
- **WHEN** 审查超过 300 秒
- **THEN** 产出部分报告，标注 `partial` 及遗漏维度；门禁仅检验已完成的 P0

### Requirement: 大 PR 降级模式
变更文件超过 50 个时，审查 SHALL 进入大文件模式：核心文件（Application、Activity、协程密集代码）全量审查，非核心文件 P1/P2 抽样审查，P0 仍全覆盖。

#### Scenario: 大 PR 触发降级
- **WHEN** PR 变更文件数为 60
- **THEN** 报告标注 `large-pr`，列出跳过的非核心文件清单；P0 所有文件仍全覆盖

### Requirement: 单文件分段审查
超过 2000 行的单文件 SHALL 按方法/类边界分段审查，每段独立产出发现项。

#### Scenario: 超大文件分段审查
- **WHEN** 某文件超过 2000 行且新增了多个方法
- **THEN** 按方法边界拆分为 2+ 段独立审查，发现项合并至同一报告

### Requirement: 并发审查限制
流水线同时审查的 PR 数 SHALL 不超过 3 个，避免 API 速率限制。

#### Scenario: 并发超限
- **WHEN** 5 个 PR 同时触发审查
- **THEN** 3 个立即执行，其余 2 个排队等待，完成后顺次执行
