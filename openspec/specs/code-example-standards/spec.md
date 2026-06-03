# code-example-standards Specification

## Purpose
定义规则表中反例/正例代码片段的格式、质量标准和来源要求，确保 81 条规则都有可编译的 Kotlin 代码示例供 AI 模型进行模式匹配。

## Requirements

### Requirement: 每条规则必须包含完整代码片段
规则表中的反例列和正例列 SHALL 分别包含至少 2 行可编译的 Kotlin 代码片段。反例代码 SHALL 展示明确的性能问题模式，正例代码 SHALL 展示业界推荐的最佳实践。

#### Scenario: 反例代码可独立识别问题
- **WHEN** AI 审查器读取某规则的反例代码
- **THEN** 代码 SHALL 包含至少 2 行 Kotlin 语句，展示可独立理解的性能反模式

#### Scenario: 正例代码可直接作为修复参考
- **WHEN** Reviewer 查看某规则的正例代码
- **THEN** 代码 SHALL 是可编译的 Kotlin 片段，可作为修复方向的参考

### Requirement: 代码来源必须可追溯
代码片段 SHALL 来源于 Android 官方文档、真实生产事故复盘或 Kotlin 编码规范。优先级：① Android 官方文档 → ② 真实生产事故（掘金/CSDN/proandroiddev）→ ③ 编码规范推荐写法。

#### Scenario: 官方文档优先
- **WHEN** Android 官方文档中存在对应反模式/最佳实践示例
- **THEN** SHALL 优先使用官方文档中的代码模式

#### Scenario: 生产事故案例补充
- **WHEN** 官方文档未覆盖某性能场景
- **THEN** SHALL 使用社区真实事故复盘中的代码模式（需可公开访问）

### Requirement: 代码片段保持 Kotlin 语法正确性
所有代码片段 SHALL 使用标准 Kotlin 语法。代码片段 SHALL 可独立阅读，不依赖外部类定义。

#### Scenario: Kotlin 语法检查
- **WHEN** 审查代码片段是否可用于 AI 模式匹配
- **THEN** 代码 SHALL 不包含未定义变量的引用、不包含截断的方法体

### Requirement: 代码片段覆盖所有 12 维度
全部 12 个维度（10.1 到 10.12）的 81 条规则 SHALL 均完成代码片段增强。

#### Scenario: 全维度覆盖
- **WHEN** 统计已增强代码的规则数
- **THEN** SHALL = 81 条
