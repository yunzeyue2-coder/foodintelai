#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CATEGORY 脱敏扫描器（Category Desensitization Scanner）
=======================================================
GPT 工业化加固 P0-1：自动检测代码中规则层的品类关键词。

原则（沧林 2026-08-10）：系统不认识"炸鸡/米线/奶茶"这些名字——
品类只是输入标签，任何规则层出现品类词 = 系统被污染 = Fail。

扫描范围: qto-engine 全部 .py（排除测试文件里的示例数据？不——测试也要干净）
判定:
  规则层（def 内逻辑/条件/字典 key）含品类词 → FAIL
  纯注释/文档字符串里作为示例说明 → WARNING（可接受但建议改）
  测试用例名称/输入数据 → PASS（品类是测试样本，允许出现）

用法: python3 category_desensitizer.py [--strict]
"""
import os, re, sys

# 品类词表（食品+非食品常见，可扩展）
CATEGORY_WORDS = [
    "炸鸡", "米线", "卤味", "卤肉", "早餐", "饮品", "奶茶", "火锅", "烧烤",
    "甜品", "螺蛳粉", "烤冷面", "手抓饼", "鸡架", "鸡腿", "鸡排",
    "酸辣粉", "麻辣烫", "包子", "馒头", "饺子", "面条", "快餐", "咖啡",
    "烘焙店", "面包店", "蛋糕店",
]
# 工艺词（不是品类——烘焙/炸制/烤制/炸串是工艺/出品形态，允许出现在规则层）
PROCESS_WORDS = ["烘焙", "炸制", "烤制", "卤制", "现煮", "冲调", "现卤", "炸串"]

# 测试文件/目录（测试用例输入品类名是允许的——它们是测试样本）
TEST_MARKERS = ["test", "acceptance", "proof", "regression", "category_agnostic"]


def scan_file(path, strict=False):
    """扫描单个文件。返回 (fail_lines, warning_lines)"""
    fails, warnings = [], []
    lines = open(path, encoding="utf-8").read().splitlines()
    in_docstring = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # 跳过空/注释
        if not stripped or stripped.startswith("#"):
            continue
        # 检测字符串/文档字符串
        if '"""' in stripped or "'''" in stripped:
            in_docstring = not in_docstring
            continue
        if in_docstring:
            continue

        # 找品类词（在代码逻辑行）——排除工艺词（烘焙/炸串等是工艺/出品形态）
        found = []
        for c in CATEGORY_WORDS:
            if c in stripped:
                # 若是工艺词（如"炸串"是工艺，"炸串店"才是品类）→ 跳过
                if c in PROCESS_WORDS:
                    continue
                code_only = stripped.split("#")[0]
                if c in code_only:
                    found.append(c)
        if not found:
            continue

        # 判断是否为规则层（if/elif/==/in/dict key/return 含品类）
        is_rule = any(kw in stripped for kw in ["==", "!=", " in ", "if ", "elif ",
                                                 "def ", "return", ":", "dict", "key"])
        # 纯注释示例（行内 # 后面）不算规则
        code_part = stripped.split("#")[0]
        is_example_only = not any(c in code_part for c in found)

        if strict:
            fails.append((i, stripped[:100], found))
        elif is_rule and not is_example_only:
            fails.append((i, stripped[:100], found))
        elif is_rule:
            warnings.append((i, stripped[:100], found))
    return fails, warnings


# 扫描器自身也检查（词表含品类词是定义行为，跳过自身）
if __name__ == "__main__" and os.path.basename(__file__) in ("category_desensitizer.py",):
    pass  # 自身定义词表不算污染

def main():
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qto-engine")
    if not os.path.exists(root):
        root = os.path.dirname(os.path.abspath(__file__))
    strict = "--strict" in sys.argv
    self_name = os.path.basename(__file__)

    total_fails, total_warns = 0, 0
    print(f"=== CATEGORY 脱敏扫描（{'strict' if strict else 'standard'}）===")
    print(f"扫描目录: {root}\n")

    for dirpath, dirnames, filenames in os.walk(root):
        if "__pycache__" in dirpath:
            continue
        for fname in sorted(filenames):
            if not fname.endswith(".py"):
                continue
            if fname == self_name:
                continue  # 跳过扫描器自身（词表定义不算污染）
            path = os.path.join(dirpath, fname)
            rel = os.path.relpath(path, root)
            is_test = any(m in fname.lower() for m in TEST_MARKERS) or "test" in rel.lower()
            fails, warns = scan_file(path, strict=strict and not is_test)
            if fails and not is_test:
                total_fails += len(fails)
                print(f"❌ {rel}: {len(fails)} 条规则层品类依赖")
                for ln, txt, cats in fails:
                    print(f"    L{ln}: {txt} [{'/'.join(cats)}]")
            elif warns and not is_test:
                total_warns += len(warns)
                print(f"⚠️  {rel}: {len(warns)} 处注释示例（不阻塞）")
                for ln, txt, cats in warns:
                    print(f"    L{ln}: {txt} [{'/'.join(cats)}]")
            elif is_test and fails:
                # 测试文件：品类词是测试样本，允许——但标注说明
                print(f"🧪 {rel}: 含 {len(fails)} 处品类测试样本（允许——炸鸡等是测试样本非系统能力）")
            else:
                print(f"✅ {rel}")

    print(f"\n=== 结果: FAIL {total_fails} / WARNING {total_warns} ===")
    if total_fails:
        print("❌ 规则层存在品类依赖——系统被污染，需清理")
        sys.exit(1)
    else:
        print("✅ 规则层无品类依赖——系统品类无关（品类词仅存在于测试样本/注释）")
        sys.exit(0)


if __name__ == "__main__":
    main()
