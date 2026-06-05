# Purpose
定义 P0 必查规则集的分级兜底机制。

## Requirements

### Requirement: L0 必查规则 — 永远注入
P0 必查规则集 SHALL 包含 L0 级别规则，无论变更类型如何均参与审查。L0 SHALL 覆盖 MEM-01、MEM-02、TH-05。

#### Scenario: 纯文案变更仍查 L0
- **WHEN** 变更仅涉及 strings.xml 翻译文本
- **THEN** MEM-01、MEM-02、TH-05 SHALL 仍然参与审查

#### Scenario: L0 规则触发
- **WHEN** 代码中存在 Activity 静态持有
- **THEN** SHALL 报告 MEM-01 P0

### Requirement: L1 必查规则 — 按文件语言注入
L1 级别 SHALL 包含 MT-01/02/03/06、BG-01/05、ST-01、IO-01，仅在非资源文件变更时注入。

#### Scenario: Kotlin 文件触发 L1
- **WHEN** 变更文件为 `.kt` 文件
- **THEN** L1 全部规则 SHALL 注入

#### Scenario: 纯资源文件不触发 L1
- **WHEN** 变更文件仅为资源文件
- **THEN** L1 规则 SHALL 不注入

### Requirement: 必查规则集独立可加载
`_must-check.md` SHALL 包含 L0 和 L1 规则的完整定义，可独立被加载和审查。

#### Scenario: 必查规则集完整性
- **WHEN** 仅加载 `_must-check.md`
- **THEN** SHALL 能独立完成 L0+L1 全部规则的审查
