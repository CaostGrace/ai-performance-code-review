## ADDED Requirements

### Requirement: 正反例作为测试用例
PRD §9 中每条规则的反例和正例 Kotlin 代码 SHALL 可直接作为 Skill 的冒烟测试用例。测试 SHALL 验证：将反例代码输入 Skill 后能正确识别对应规则 ID。

#### Scenario: 反例触发规则
- **WHEN** 将 MT-01 的反例代码片段（`sp.getString("key", "")` 在主线程）作为 diff 输入
- **THEN** Skill SHALL 输出 MT-01 P0 发现项

#### Scenario: 正例不触发规则
- **WHEN** 将 MT-01 的正例代码片段（`viewModelScope.launch(Dispatchers.IO)`）作为 diff 输入
- **THEN** Skill SHALL 不输出 MT-01 发现项

### Requirement: 冒烟测试覆盖所有 P0 规则
冒烟测试集 SHALL 覆盖全部 P0 规则（MT-01/02/03/04/06、ST-01、MEM-01/02/06、IO-01、BG-01/05、TH-05），每个 P0 规则的反例代码 SHALL 能触发对应规则 ID。

#### Scenario: P0 冒烟测试全通过
- **WHEN** 依次输入全部 P0 规则的反例代码
- **THEN** 每个 P0 规则 SHALL 被正确识别，无漏报
