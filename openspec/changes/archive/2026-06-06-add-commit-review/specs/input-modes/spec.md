## ADDED Requirements

### Requirement: commit hash 输入模式
Skill SHALL 支持通过 commit hash 作为审查输入。当用户输入匹配 7-40 位 hex 字符串（`[0-9a-f]`）且非 @ 文件路径时，SHALL 执行 `git show <hash>` 获取该 commit 的变更集进行审查。

#### Scenario: 有效 hash 审查
- **WHEN** 用户输入 `/android-performance-cr a1b2c3d`
- **THEN** Skill SHALL 执行 `git show a1b2c3d`，将输出作为 diff 输入，走标准审查流程

#### Scenario: 无效 hash
- **WHEN** 用户输入的 hex 字符串对应无效 commit
- **THEN** Skill SHALL 提示"无效的 commit hash: <hash>"并终止

#### Scenario: hash 与 @ 文件共存
- **WHEN** 用户同时输入 hash 和 @ 文件
- **THEN** @ 文件优先级更高，Skill SHALL 审查 @ 的文件，忽略 hash

### Requirement: commit 模式报告标注
commit 审查模式下，报告 SHALL 在摘要中标注 commit hash、commit message 摘要和 author。

#### Scenario: 报告含 commit 信息
- **WHEN** 审查一个有效 commit
- **THEN** 报告摘要 SHALL 包含「Commit: `<hash>` — `<message>` (author)」行
