#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁班·批量文档：用一份数据，按模板生成多份 Word 报告
# 依赖：pip install python-docx
# 用法：改 ROWS 数据后 python doc_gen.py
from docx import Document
import os

# ===== 配置区（只改这里）=====
ROWS = [  # ← 每行一份报告；字段随意增减，下面 make_one 同步改
    {"name": "张三", "title": "季度复盘", "point": "营收环比+12%"},
    {"name": "李四", "title": "季度复盘", "point": "新客成本-8%"},
]
OUT_DIR = r"./doc_out"   # ← 输出文件夹


def preflight():
    if not ROWS:
        print("❌ ROWS 是空的：先在脚本里填好要生成的数据。")
        return False
    print("🔍 预检通过：%d 条数据，准备生成。" % len(ROWS))
    return True


def make_one(row):
    d = Document()
    d.add_heading("%s · %s" % (row.get("name", ""), row.get("title", "")), level=1)
    d.add_paragraph("核心结论：%s" % row.get("point", ""))
    return d


def main():
    if not preflight():
        return
    try:
        os.makedirs(OUT_DIR, exist_ok=True)
        for row in ROWS:
            d = make_one(row)
            path = os.path.join(OUT_DIR, "%s_%s.docx" % (row.get("name", "x"), row.get("title", "x")))
            d.save(path)
            print("生成 ->", path)
        print("✅ 共 %d 份 -> %s" % (len(ROWS), OUT_DIR))
    except Exception as e:
        print("❌ 生成出错：%s\n   常见原因：模板字段名和 make_one 里对不上。" % e)


if __name__ == "__main__":
    main()
