# Purpose
定义外置规则的发现、加载、覆盖机制。

## Requirements

### Requirement: 项目级外置规则发现与加载
Skill 启动时 SHALL 按优先级顺序发现并加载外置规则文件：`overrides.md`（覆盖内置规则等级/行为）和 `custom-rules.md`（追加项目专用规则）。外置规则 SHALL 随 IDE 工作区切换自动热加载，无需手动 reload。

#### Scenario: 项目存在 `overrides.md` 时，解析其中的覆盖规则，覆盖对应内置规则的等级或行为。
- **WHEN** 项目根存在 `overrides.md`
- **THEN** Skill SHALL 解析并应用覆盖规则

#### Scenario: 项目不存在任何外置规则文件时，仅使用内置规则集，审查正常执行。
- **WHEN** 项目无 `.android-performance-cr/` 目录
- **THEN** Skill SHALL 仅使用内置规则集

#### Scenario: 切换工作区触发热加载
- **WHEN** IDE 工作区从项目 A 切换到项目 B
- **THEN** Skill SHALL 自动检测项目 B 的外置规则并重新加载

### Requirement: 内置规则覆盖操作
`overrides.md` SHALL 支持三种覆盖操作：`disable`（禁用规则）、`override`（仅改变等级，不改判定条件）、`add`（追加新规则）。

#### Scenario: override ST-01
- **WHEN** overrides.md override ST-01 为 P1
- **THEN** ST-01 SHALL 按 P1 审查，检查项和判定条件保持不变

#### Scenario: custom-rules.md 追加新规则
- **WHEN** custom-rules.md 中 add CUSTOM-01
- **THEN** CUSTOM-01 SHALL 与内置规则同权重参与审查

### Requirement: Phase 0 不做自动去重
Phase 0 阶段，外置规则与内置规则之间的重叠 SHALL 不做自动去重处理。

#### Scenario: 规则重叠不自动合并
- **WHEN** 内置 MT-01 和外置 CUSTOM-01 对同一段代码同时报告
- **THEN** 报告中 SHALL 出现两条独立发现项

### Requirement: override 仅支持改等级
`override` 操作 SHALL 仅改变规则等级，不支持修改判定条件。阈值定制需求 SHALL 走 `custom-rules.md` 的 `add` 操作。

#### Scenario: 阈值定制
- **WHEN** 团队需要自定义判定条件
- **THEN** SHALL 通过 `custom-rules.md` 新增 CUSTOM 规则
