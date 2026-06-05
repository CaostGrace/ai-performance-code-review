## Context

SKILL.md 缺少 Agent Skill 规范的 YAML front matter 元数据，且 `tools.md` 放于根目录而非 `references/` 子目录。需对齐项目中已有 Skills（如 openspec-* 系列）的目录约定。

## Goals / Non-Goals

**Goals:**
- SKILL.md 增补 YAML front matter（name、description、metadata）
- tools.md 迁入 `references/` 目录
- SKILL.md 新增对 references 按需加载的显式指令
- 同步更新所有引用路径的文档

**Non-Goals:**
- 不改变规则文件（rules/*.md）的内容或结构
- 不改变 tests/ 目录
- 不引入新字段（如 license、compatibility、generatedBy）

## Decisions

### D1: YAML front matter 字段裁剪

```yaml
---
name: android-performance-cr
description: 对 Android 代码变更进行静态性能审查，覆盖 12 个维度、81 条规则。...
metadata:
  author: 廖兵
  version: 0.0.1
---
```

移除 `license`、`compatibility`、`generatedBy`，保留 `name`、`description`、`metadata`（author + version）。

### D2: tools.md 移至 references/

```
android-performance-cr/
├── SKILL.md              (新增 YAML front matter)
├── references/
│   └── tools.md          ← 从根目录移入
├── rules/                (不变)
└── tests/                (不变)
```

### D3: SKILL.md 增加按需加载指令

在审查流程中增加：当需要建议验证工具时，读取 `references/tools.md`。

## Risks / Trade-offs

- **路径变更影响**: PRD、design.md、proposal.md、specs、tasks.md 中的路径引用需同步更新。风险低，所有引用均为纯文本路径。
