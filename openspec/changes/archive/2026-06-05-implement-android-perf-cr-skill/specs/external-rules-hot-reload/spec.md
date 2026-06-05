## ADDED Requirements

### Requirement: 工作区切换自动热加载
当 IDE 工作区切换到不同项目时，Skill SHALL 自动检测新项目的 `.android-performance-cr/` 目录，重新加载外置规则文件。SHALL 不需要开发者手动执行 reload 命令。

#### Scenario: 切换工作区触发重新加载
- **WHEN** 开发者在 IDE 中从项目 A 切换到项目 B
- **THEN** Skill SHALL 检测项目 B 的 `.android-performance-cr/` 目录，若存在则加载其外置规则

#### Scenario: 同工作区无需重新加载
- **WHEN** 开发者在同一项目内多次触发审查
- **THEN** Skill SHALL 复用已加载的外置规则，不重复读取文件

### Requirement: Phase 0 不做自动去重
Phase 0 阶段，外置规则与内置规则之间的重叠 SHALL 不做自动去重处理。同段代码被多个规则 ID 报告时，SHALL 通过 Reviewer 人工标记 `#false-positive` 回注。

#### Scenario: 双报不自动去重
- **WHEN** 内置 MT-01 和外置 CUSTOM-01 对同一段代码同时报告
- **THEN** 报告中 SHALL 出现两条独立发现项，由 Reviewer 手动判断

### Requirement: overrides.md 仅支持等级修改
`overrides.md` 的 `override` 操作 SHALL 仅改变规则等级（P0↔P1↔P2），SHALL 不修改规则的判定条件、检查项描述或其他属性。

#### Scenario: override 只改等级
- **WHEN** `overrides.md` 包含 `| override | ST-01 | P1 | 启动 SDK 初始化已在基线中计量 |`
- **THEN** ST-01 SHALL 按 P1 审查，其他属性（检查项、反例、正例、判定）保持不变

#### Scenario: 阈值定制走 custom-rules
- **WHEN** 团队需要自定义判定条件（如"启动初始化耗时 < 200ms 不算 P0"）
- **THEN** SHALL 通过 `custom-rules.md` 的 `add` 操作新增独立规则，而非 override
