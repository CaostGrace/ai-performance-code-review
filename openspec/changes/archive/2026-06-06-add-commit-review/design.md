## Context

Skill 的输入模式仅支持 `git diff`（未提交变更）和 @ 文件。需新增 commit hash 输入模式，通过 `git show` 获取历史 commit 的 diff。

## Goals / Non-Goals

**Goals:**
- 支持通过 commit hash 审查已提交的变更
- Hash 检测与 @ 文件互不冲突
- 报告标注 commit 来源信息

**Non-Goals:**
- 不支持 commit 范围（e.g., `a1b2..e4f5`）
- 不支持多 commit 批量审查
- 不需要新的命令语法

## Decisions

### D1: 直接传 hash（方案 A）

用户直接输入 7-40 位 hex 字符串（如 `a1b2c3d`）。SKILL.md 第一步检测输入是否匹配 `^[0-9a-f]{7,40}$`，匹配则走 `git show <hash>` 路径。

**选择理由**：hex 特征明显，与文件路径（含 `.kt`、`/` 等分隔符）几乎不会误判。不需要 `commit` 前缀命令。

### D2: 检测优先级

```
用户输入 → 含 @文件/目录? ──是──→ 审查指定文件（已有逻辑，不变）
         → 匹配 hex hash?  ──是──→ git show <hash>（新增）
         → 默认           ──否──→ git diff（已有逻辑，不变）
```

> @ 文件优先级最高，因为它显式表达了用户意图。hash 检测次之，diff 作为兜底。

### D3: 报告标注

commit 模式下输出报告增加：

```markdown
- **改动类型**：commit review
- **Commit**: `a1b2c3d` — "fix: memory leak in HomeFragment" (Author Name)
- **扫描范围**：single commit
```

### D4: git show 失败处理

若 hash 无效（`git show` 返回错误），提示"无效的 commit hash"，终止审查。

## Risks / Trade-offs

- 极罕见的文件名纯 hex 会被误判为 hash → 概率极低，且即使误判 `git show` 会报错终止，不会产生错误审查结果
