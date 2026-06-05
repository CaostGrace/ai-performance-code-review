# Purpose
定义 AI 审查的三重判定逻辑：精确匹配、模式可疑、架构担忧。

## Requirements

### Requirement: 精确匹配 — 按原等级报告
当代码精确匹配规则反例模式且可定位到具体代码行时，AI SHALL 按规则定义的原等级报告发现项。

#### Scenario: 精确匹配 P0
- **WHEN** 代码中包含 `sp.getString("key", "")` 在主线程调用
- **THEN** SHALL 报告 MT-01 P0，标注文件:行号

#### Scenario: 精确匹配 P1
- **WHEN** 代码中使用 `Dispatchers.Default` 执行磁盘 IO
- **THEN** SHALL 报告 TH-01 P1

### Requirement: 模式可疑 — 降一级报告
当代码模式与反例相似但无法确定是否真正触发性能问题时，AI SHALL 降一级报告，标注"需人工确认"。

#### Scenario: 可疑的主线程 IO
- **WHEN** 代码在主线程调用 `File("cache.json").readText()`，文件大小未知
- **THEN** SHALL 报告 IO-01 P1（降级），标注"需人工确认"

### Requirement: 架构担忧 — 写入需人工
当仅架构层面担心但无具体代码证据时，AI SHALL 写入"未覆盖/需人工"章节，不报告等级。

#### Scenario: 仅架构担忧
- **WHEN** 新增大型模块依赖但未见具体初始化代码
- **THEN** SHALL 写入"未覆盖/需人工"

#### Scenario: 盲区声明
- **WHEN** 变更涉及 JNI 调用
- **THEN** SHALL 写入"未覆盖/需人工"，建议 Perfetto 验证
