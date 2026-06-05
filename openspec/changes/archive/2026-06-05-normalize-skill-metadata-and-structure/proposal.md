## Why

SKILL.md 缺少 Skills 规范要求的 YAML front matter 元数据（name、description、metadata），且辅助文档 `tools.md` 直接放在 Skill 根目录而非规范的 `references/` 子目录，不符合项目中已有 Openspec Skills 的目录约定。

## What Changes

- SKILL.md 新增 YAML front matter：`name: android-performance-cr`、`description`、`metadata.author: 廖兵`、`metadata.version: 0.0.1`
- `tools.md` 从根目录移至 `references/tools.md`
- SKILL.md 新增对 `references/tools.md` 的按需加载引用指令
- 同步更新 PRD §3.4、design.md、proposal.md、specs/skill-file-structure/spec.md、tasks.md 中的路径引用

## Capabilities

### New Capabilities
- `skill-metadata-spec`: 定义 SKILL.md 的 YAML front matter 元数据规范（name、description、metadata.author、metadata.version）
- `skill-references-convention`: 定义 Skill 辅助文档存放于 `references/` 目录的约定

### Modified Capabilities
- `skill-file-structure`: 目录结构从 `tools.md`（根目录）变更为 `references/tools.md`；SKILL.md 增加元数据头

## Impact

- **SKILL.md**: 新增 YAML front matter + references 引用指令
- **tools.md**: 移动至 `references/tools.md`
- **PRD §3.4**: 目录结构图更新
- **design.md D1**: 目录结构图更新
- **proposal.md**: 3 处 `tools.md` 路径 → `references/tools.md`
- **specs/skill-file-structure/spec.md**: 文件名约束更新
- **tasks.md**: 任务描述更新
