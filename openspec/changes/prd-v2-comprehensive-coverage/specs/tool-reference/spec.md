# tool-reference Specification

## Purpose
为 AI Skill 在执行性能审查时提供可操作的工具使用参考，使 Skill 在遇到静态审查盲区时能给出具体的工具安装、运行和输出解读建议。

## Requirements

### Requirement: 工具速查卡覆盖核心性能工具
§7.4 工具使用速查卡 SHALL 覆盖以下 9 个核心性能分析工具：StrictMode、Systrace、Perfetto、LeakCanary、Memory Profiler（Android Studio）、Battery Historian、APK Analyzer、Database Inspector、Network Profiler。

#### Scenario: 工具数量覆盖
- **WHEN** Skill 需要引用工具使用说明
- **THEN** 速查卡 SHALL 包含 9 个工具的完整条目

### Requirement: 每个工具至少包含三要素
每个工具条目 SHALL 包含：安装/启用方式、核心命令/操作步骤、关键输出解读（至少 3 条可操作解读）。

#### Scenario: Perfetto 工具条目完整性
- **WHEN** 审查依赖 Perfetto 检测运行时性能（如 MT-05、ST-01、UI-04）
- **THEN** 速查卡 SHALL 提供：`adb shell perfetto` 命令行抓取、`ui.perfetto.dev` 打开方式、主线程 Choreographer 帧耗时解读

#### Scenario: LeakCanary 工具条目完整性
- **WHEN** 审查依赖 LeakCanary 检测内存泄漏（如 MEM-01、MEM-02、MEM-06）
- **THEN** 速查卡 SHALL 提供：Gradle 依赖声明方式、自动触发说明、泄漏引用路径图解读方法

### Requirement: 工具与规则的映射关系
每条规则的「参考工具」列 SHALL 引用 §7.4 中的工具条目。AI Skill 在报告中遇到「需人工/未覆盖」场景时，SHALL 引用对应工具的速查卡建议。

#### Scenario: 盲区场景的工具引用
- **WHEN** 审查遇到 Native 内存分配（JNI 场景）
- **THEN** Skill SHALL 在报告中引用 Perfetto Heap Profile 和 MAT Native 堆分析条目
