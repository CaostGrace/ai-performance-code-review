## ADDED Requirements

### Requirement: 项目级外置规则发现与加载
Skill 启动时 SHALL 按优先级顺序发现并加载外置规则文件：
1. `<项目根>/.android-performance-cr/overrides.md`（覆盖内置规则等级/行为）
2. `<项目根>/.android-performance-cr/custom-rules.md`（追加项目专用规则）

#### Scenario: 项目存在 overrides.md
- **WHEN** Skill 启动且 `<项目根>/.android-performance-cr/overrides.md` 存在
- **THEN** 解析其中的覆盖规则，覆盖对应内置规则的等级或行为

#### Scenario: 项目不存在任何外置规则文件
- **WHEN** Skill 启动且 `.android-performance-cr/` 目录不存在或为空
- **THEN** 仅使用内置规则集，审查正常执行

### Requirement: 内置规则覆盖操作
overrides.md SHALL 支持三种覆盖操作：`disable`（禁用规则）、`override`（改变等级）、`add`（追加新规则）。

#### Scenario: 覆盖 P0 规则降级
- **WHEN** overrides.md 中包含 `| override | ST-01 | P1 | ...` 条目
- **THEN** ST-01 按 P1 等级审查，不再作为 P0 阻塞合入

#### Scenario: 追加自定义规则
- **WHEN** custom-rules.md 中包含完整七列新规则
- **THEN** 该规则与内置规则同权重参与审查，ID 冲突时以项目规则优先

### Requirement: 外置规则格式兼容
外置规则文件 SHALL 采用与 §10 同构的 Markdown 表格格式（七列：ID / 等级 / 检查项 / 反例 / 正例 / 判定 / 参考工具）。

#### Scenario: 格式不匹配的规则
- **WHEN** 外置规则表格缺少必填列
- **THEN** Skill 跳过该规则并输出警告，不中断审查
