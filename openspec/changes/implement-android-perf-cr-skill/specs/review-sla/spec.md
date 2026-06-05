## ADDED Requirements

### Requirement: 文件级预扫描
Skill SHALL 在路由阶段对每个变更文件执行轻量关键字预扫描（grep），根据扫描结果确定加载哪些维度规则文件。预扫描 SHALL 在规则加载前完成，不产生额外审查耗时。

#### Scenario: 关键字扫描
- **WHEN** 变更文件内容包含 `RecyclerView` 关键字
- **THEN** SHALL 标记为 View 体系文件，加载 `ui-view.md`

#### Scenario: 路径特征扫描
- **WHEN** 变更文件路径匹配 `build.gradle.kts`
- **THEN** SHALL 加载 `package.md`、`startup.md`
