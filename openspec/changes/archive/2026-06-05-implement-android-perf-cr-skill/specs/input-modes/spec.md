## ADDED Requirements

### Requirement: 自动 git diff 模式
当用户触发 Skill 但未通过 @ 指定任何文件时，Skill SHALL 自动获取当前 `git diff`（已暂存 + 未暂存的变更）作为审查输入范围。

#### Scenario: 无 @ 文件时使用 git diff
- **WHEN** 用户输入 `/ @android-performance-cr` 但未 @ 任何文件
- **THEN** Skill SHALL 执行 `git diff` 获取变更集，作为审查输入

#### Scenario: git diff 为空时提示
- **WHEN** `git diff` 返回空（无任何变更）
- **THEN** Skill SHALL 提示开发者"无代码变更可审查"，不产出报告

### Requirement: 手动 @ 文件模式
当用户通过 @ 指定文件或目录时，Skill SHALL 仅审查指定范围内的文件。

#### Scenario: @ 指定文件
- **WHEN** 用户输入 `/ @android-performance-cr @MainActivity.kt @NetworkModule.kt`
- **THEN** Skill SHALL 仅审查 MainActivity.kt 和 NetworkModule.kt

#### Scenario: @ 指定目录
- **WHEN** 用户输入 `/ @android-performance-cr @src/main/kotlin/ui/`
- **THEN** Skill SHALL 审查该目录下所有代码文件

### Requirement: 行号使用文件绝对行号
发现项中的行号 SHALL 使用审查时文件的绝对行号（非 diff hunk 内的相对偏移）。

#### Scenario: 行号格式
- **WHEN** 发现项在 `FooActivity.kt` 第 42 行
- **THEN** 报告中 SHALL 标注 `FooActivity.kt:42`
