## Why

Skill 目前仅支持审查未提交的 `git diff` 或 @ 指定文件，无法审查已合入或历史 commit。开发者在复盘线上问题时需要审视历史提交的性能风险，或在 code review 时快速检查某个 commit 的变更。

## What Changes

- SKILL.md 第一步增加 commit hash 检测：用户输入匹配 7-40 位 hex 字符串时，执行 `git show <hash>` 获取变更集
- 输出报告的「改动类型」和「扫描范围」标注 commit hash 及 author 信息
- Phase 0 仅支持单 commit，不支持范围

## Capabilities

### Modified Capabilities
- `input-modes`: 输入模式从 2 种（git diff / @ 文件）扩展为 3 种（增加 commit hash）

## Impact

- **SKILL.md**: 第一步增加 hex hash 检测分支
- **PRD §3.1**: 触发方式增加 commit hash 模式
- **PRD §3.2**: 输入来源增加 `git show`
- **PRD 修订记录**: v3.3
- **specs/input-modes**: 新增 commit hash 相关要求
