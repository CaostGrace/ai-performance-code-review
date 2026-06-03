# rule-checklist Specification (Delta)

## ADDED Requirements

### Requirement: 规则清单扩展覆盖维度
规则清单 SHALL 从 11 个维度扩展到 12 个维度（新增 §10.12 架构与模块化），并在 §10.3 下新增 Compose 专项子维度（10.3.A），包含 8 条 `CP-` 前缀规则。

#### Scenario: 架构维度存在
- **WHEN** 统计 §10 主维度数量
- **THEN** SHALL = 12（含 §10.12 架构与模块化）

#### Scenario: Compose 子维度规则数
- **WHEN** 统计 10.3.A Compose 专项中 `CP-` 前缀规则
- **THEN** SHALL = 8 条

### Requirement: §11 兜底规则全部转正
§11 后续可选规则中的所有 6 条主题 SHALL 转正为正式规则（补全七列定义），分布到以下维度：ST-07（Baseline Profile）、PKG-06（16KB 页大小）、UI-09（DiffUtil）、MEM-08（大图硬件位图）、CP-02（Compose @Stable）、ARCH-01（组件化通信开销）。原 §11 位置 SHALL 改为「后期处理：流水线与 CI」。

#### Scenario: 兜底规则归零
- **WHEN** 检查 §11 是否仍存在「后续可选规则」标题
- **THEN** SHALL 不存在，所有主题已转为正式规则

### Requirement: 规则总数扩展
规则清单总数 SHALL 从约 64 条扩展到约 83 条（新增约 19 条规则）。

#### Scenario: 规则总数达到预期
- **WHEN** 统计 §10 中全部规则条目
- **THEN** SHALL ≈ 83 条（含原有 64 + 新增 19）

### Requirement: 真实错误案例嵌入
规则反例/正例代码片段 SHALL 优先使用从真实生产事故中提取的代码模式，来源包括但不限于：Android 官方文档、掘金、CSDN、proandroiddev.com 等社区的真实问题分析。

#### Scenario: 协程案例来源一致
- **WHEN** 验证 TH-05 / MEM-02 的反例代码
- **THEN** SHALL 与生产环境中导致 ANR/泄漏的实际代码模式一致（如 `runBlocking { performTask() }` 在 hot path 导致 ANR）

## REMOVED Requirements

### Requirement: §11 后续可选规则
**Reason**: 全部主题已转正为正式规则，归入 §10 各维度。
**Migration**: 查找原 §11 内容时，在 §10 对应维度的新规则 ID 中获取（如 Baseline Profile → ST-07, 16KB 页大小 → PKG-06）。
