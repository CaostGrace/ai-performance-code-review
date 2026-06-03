# architecture-modularization Specification

## Purpose
定义架构与模块化维度的性能审查规则，覆盖跨模块通信开销、循环依赖检测、Dynamic Feature 加载时机、多进程 Binder 通信等场景。

## Requirements

### Requirement: 模块间通信开销检测
ARCH-01 规则 SHALL 检测跨模块传递大对象（> 100KB Parcelable/Serializable）的场景，提示序列化开销风险。

#### Scenario: 跨模块大对象传递检测
- **WHEN** 审查涉及跨模块的接口方法调用，且参数为 Parcelable 或 Serializable 类型
- **THEN** ARCH-01 规则 SHALL 评估参数对象规模，若可能 > 100KB 则报告 P2 风险

### Requirement: 模块间循环依赖检测
ARCH-02 规则 SHALL 检测 `build.gradle(.kts)` 中的模块循环依赖（A→B→A）。AI 审查时在 diff 触及 `implementation/api project()` 声明时激活。

#### Scenario: 循环依赖检测触发
- **WHEN** 审查 `build.gradle.kts` 中的 `implementation(project(":feature-b"))` 变更
- **THEN** ARCH-02 SHALL 分析目标模块是否已依赖当前模块，若构成环则报告 P2

### Requirement: Dynamic Feature 加载时机检测
ARCH-03 规则 SHALL 检测 Dynamic Feature Module 是否在启动时被立即加载，提示启动性能风险。

#### Scenario: 启动时加载 Dynamic Feature
- **WHEN** 审查 `SplitInstallManager` 在 `Application.onCreate` 中调用
- **THEN** ARCH-03 SHALL 报告 P1，建议延迟到功能使用时按需加载

### Requirement: 多进程 Binder 通信开销检测
ARCH-04 规则 SHALL 检测多进程场景下的高频/大体积 Binder 通信模式，包括同一帧内多次 Binder 调用、未使用 SharedMemory 的大数据共享。

#### Scenario: 高频 Binder 调用检测
- **WHEN** 审查 AIDL 接口实现，且代码模式显示循环/高频调用
- **THEN** ARCH-04 SHALL 报告 P1，建议批量 RPC 或使用 MMKV/SharedMemory

### Requirement: 架构规则覆盖基本场景
§10.12 架构与模块化维度 SHALL 包含至少 4 条规则（ARCH-01 至 ARCH-04），每条规则使用独立 `ARCH-` 前缀 ID，包含完整的七列定义。

#### Scenario: 架构维度规则数量验证
- **WHEN** 统计 §10.12 中 ARCH- 前缀规则数量
- **THEN** SHALL ≥ 4 条
