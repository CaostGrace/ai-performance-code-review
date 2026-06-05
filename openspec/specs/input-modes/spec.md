# Purpose
定义 Skill 的双输入模式：自动 git diff 和手动 @ 文件。

## Requirements

### Requirement: 自动 git diff 模式
当用户触发 Skill 但未通过 @ 指定任何文件时，Skill SHALL 自动获取当前 `git diff` 作为审查输入范围。

#### Scenario: 无 @ 文件时使用 git diff
- **WHEN** 用户调用 Skill 但未 @ 任何文件
- **THEN** Skill SHALL 执行 `git diff` 获取变更集

#### Scenario: git diff 为空时提示
- **WHEN** `git diff` 返回空
- **THEN** Skill SHALL 提示"无代码变更可审查"

### Requirement: 手动 @ 文件模式
当用户通过 @ 指定文件或目录时，Skill SHALL 仅审查指定范围内的文件。

#### Scenario: @ 指定文件
- **WHEN** 用户 @ 指定文件
- **THEN** Skill SHALL 仅审查指定文件

### Requirement: 行号使用文件绝对行号
发现项中的行号 SHALL 使用审查时文件的绝对行号。

#### Scenario: 行号格式
- **WHEN** 发现项在 `FooActivity.kt` 第 42 行
- **THEN** 报告中 SHALL 标注 `FooActivity.kt:42`
