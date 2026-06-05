## MODIFIED Requirements

### Requirement: 每条规则必须包含完整代码片段
规则表中的反例列和正例列 SHALL 分别包含至少 2 行可编译的 Kotlin 代码片段。反例代码 SHALL 展示明确的性能问题模式，正例代码 SHALL 展示业界推荐的最佳实践。代码片段 SHALL 可直接作为 Skill 的冒烟测试用例。

#### Scenario: AI 审查器读取某规则的反例代码时，代码 SHALL 包含至少 2 行 Kotlin 语句，展示可独立理解的性能反模式。
- **WHEN** Skill 加载规则文件中的反例代码
- **THEN** 代码 SHALL 为至少 2 行可编译 Kotlin

#### Scenario: Reviewer 查看某规则的正例代码时，代码 SHALL 是可编译的 Kotlin 片段，可作为修复方向的参考。
- **WHEN** 报告引用规则正例
- **THEN** 正例代码 SHALL 为可编译 Kotlin

### Requirement: 代码来源必须可追溯
代码片段 SHALL 来源于 Android 官方文档、真实生产事故复盘或 Kotlin 编码规范。优先级：① Android 官方文档 → ② 真实生产事故（掘金/CSDN/proandroiddev）→ ③ 编码规范推荐写法。

#### Scenario: Android 官方文档中存在对应反模式/最佳实践示例时，SHALL 优先使用官方文档中的代码模式。
- **WHEN** 官方文档存在对应示例
- **THEN** SHALL 优先使用官方文档模式

#### Scenario: 官方文档未覆盖某性能场景时，SHALL 使用社区真实事故复盘中的代码模式（需可公开访问）。
- **WHEN** 官方文档无对应示例
- **THEN** SHALL 使用社区可公开访问的真实事故代码

### Requirement: 代码片段保持 Kotlin 语法正确性
所有代码片段 SHALL 使用标准 Kotlin 语法。代码片段 SHALL 可独立阅读，不依赖外部类定义。

#### Scenario: 审查代码片段是否可用于 AI 模式匹配时，代码 SHALL 不包含未定义变量的引用、不包含截断的方法体。
- **WHEN** Skill 读取规则代码片段
- **THEN** 代码 SHALL 不包含未定义变量、截断方法体

### Requirement: 代码片段覆盖所有 12 维度
全部 12 个维度（10.1 到 10.12）的 81 条规则 SHALL 均完成代码片段增强。

#### Scenario: 统计已增强代码的规则数时，SHALL = 81 条。
- **WHEN** 统计全部规则文件中的代码片段
- **THEN** 每条规则 SHALL 含反例+正例代码

## ADDED Requirements

### Requirement: 正反例代码作为冒烟测试用例
规则中的反例和正例 Kotlin 代码 SHALL 可直接作为 Skill 的冒烟测试用例。将反例代码作为 diff 输入 Skill 后，SHALL 能正确识别对应规则 ID。

#### Scenario: P0 冒烟测试
- **WHEN** 将 MT-01 反例代码输入 Skill
- **THEN** Skill SHALL 输出 MT-01 P0 发现项

#### Scenario: 正例不触发
- **WHEN** 将 MT-01 正例代码输入 Skill
- **THEN** Skill SHALL 不输出 MT-01 发现项
