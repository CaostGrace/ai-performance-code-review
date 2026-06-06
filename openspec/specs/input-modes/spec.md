# Purpose
定义 Skill 的三种输入模式：自动 git diff、手动 @ 文件和 commit hash。

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

### Requirement: commit hash 输入模式
Skill SHALL 支持通过 commit hash 作为审查输入。当用户输入匹配 7-40 位 hex 字符串且非 @ 文件路径时，SHALL 执行 `git show <hash>` 获取该 commit 的变更集进行审查。

#### Scenario: 有效 hash 审查
- **WHEN** 用户输入 hex commit hash
- **THEN** Skill SHALL 执行 `git show <hash>`，走标准审查流程

#### Scenario: 无效 hash
- **WHEN** 输入的 hex 字符串对应无效 commit
- **THEN** Skill SHALL 提示"无效的 commit hash"并终止

#### Scenario: hash 与 @ 文件共存
- **WHEN** 用户同时输入 hash 和 @ 文件
- **THEN** @ 文件优先级更高，忽略 hash

### Requirement: commit 模式报告标注
commit 审查模式下，报告 SHALL 在摘要中标注 commit hash、message 和 author。

#### Scenario: 报告含 commit 信息
- **WHEN** 审查一个有效 commit
- **THEN** 报告摘要 SHALL 包含「Commit: `<hash>` — `<message>` (author)」行
