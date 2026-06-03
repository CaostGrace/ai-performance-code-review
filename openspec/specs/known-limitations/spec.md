# known-limitations Specification

## Purpose
TBD - created by archiving change prd-v13-optimization. Update Purpose after archive.
## Requirements
### Requirement: 静态审查盲区声明
审查报告 SHALL 在「未覆盖/需人工」部分注明已知的限制类型，当代码变更涉及 Native 内存、JNI、反射、动态代理、第三方 SDK 内部等 9 类盲区时。

#### Scenario: 代码变更涉及 JNI
- **WHEN** 变更包含 `System.loadLibrary` 或 `.cpp/.c` 文件
- **THEN** 在「未覆盖/需人工」中标注"JNI 调用耗时不可静态评估"，建议使用 Perfetto 验证

### Requirement: 盲区不臆造 P0
当 AI 遇到静态审查盲区时 SHALL NOT 臆造 P0 发现项；SHALL 仅输出「需人工」提示 + 建议验证工具。

#### Scenario: 遇到 Native 内存操作
- **WHEN** 代码涉及 JNI malloc/new 但无可观测证据
- **THEN** 不报告任何 P0/P1/P2；在「需人工」中标注限制类型和建议工具

