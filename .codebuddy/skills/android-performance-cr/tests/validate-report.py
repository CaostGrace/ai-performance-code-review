#!/usr/bin/env python3
"""
Android 性能 CR 报告格式校验脚本
用法: python validate-report.py [report_path]
默认检查 ./android-performance-cr-report.md
"""

import sys
import re
from pathlib import Path


def validate(report_path: str) -> list[str]:
    """校验报告格式，返回错误列表。空列表表示通过。"""
    errors = []

    path = Path(report_path)
    if not path.exists():
        errors.append(f"报告文件不存在: {report_path}")
        return errors

    content = path.read_text(encoding="utf-8")

    # 1. 检查「合入建议」字段
    merge_advice = re.search(r"\*\*合入建议\*\*[：:]\s*(.+)", content)
    if not merge_advice:
        errors.append("缺少「合入建议」字段")
    else:
        value = merge_advice.group(1).strip()
        valid_values = ["通过", "修复后合入", "阻塞", "阻塞（存在未解决 P0）"]
        if not any(v in value for v in valid_values):
            errors.append(f"「合入建议」值无效: {value}（期望: 通过 / 修复后合入 / 阻塞）")

    # 2. 检查发现项表格表头
    header_pattern = r"\|\s*规则\s*ID\s*\|\s*等级\s*\|\s*文件:行\s*\|\s*说明\s*\|\s*建议\s*\|"
    if not re.search(header_pattern, content):
        errors.append("缺少发现项表格表头（| 规则 ID | 等级 | 文件:行 | 说明 | 建议 |）")

    # 检查表头后的分隔行
    separator_pattern = r"\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|\s*-+\s*\|"
    if not re.search(separator_pattern, content):
        errors.append("缺少发现项表格分隔行")

    # 3. 检查每条 P0 发现项是否含文件:行号
    p0_lines = re.findall(r"\|\s*(\w+-\d+)\s*\|\s*P0\s*\|", content)
    if p0_lines:
        # 找到所有 P0 行，检查是否包含 文件名.kt:数字 模式
        for line in content.split("\n"):
            if "| P0 |" in line:
                file_line_match = re.search(r"(\w+\.\w+):(\d+)", line)
                if not file_line_match:
                    errors.append(f"P0 行缺少文件:行号: {line.strip()[:80]}...")

    # 4. 检查摘要章节
    if "## Android 性能 CR 摘要" not in content:
        errors.append("缺少「## Android 性能 CR 摘要」章节")

    # 5. 检查必要章节
    required_sections = ["### 发现项", "### 未覆盖/需人工"]
    for section in required_sections:
        if section not in content:
            errors.append(f"缺少章节: {section}")

    return errors


def main():
    report_path = sys.argv[1] if len(sys.argv) > 1 else "./android-performance-cr-report.md"
    print(f"校验报告: {report_path}")
    print("-" * 50)

    errors = validate(report_path)

    if errors:
        print(f"❌ 校验未通过 ({len(errors)} 个错误):")
        for i, err in enumerate(errors, 1):
            print(f"  {i}. {err}")
        sys.exit(1)
    else:
        print("✓ 校验通过")
        sys.exit(0)


if __name__ == "__main__":
    main()
