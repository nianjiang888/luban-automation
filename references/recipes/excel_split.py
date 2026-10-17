#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁班·Excel 拆分：把一个总表按"某列的值"拆成多个文件（如按"部门"列拆成各部门表）
# 依赖：pip install pandas openpyxl
# 用法：改下方"配置区"后 python excel_split.py
import os
import pandas as pd

# ===== 配置区（只改这里）=====
SRC = r"./总表.xlsx"        # ← 要拆分的源文件
OUT_DIR = r"./split_out"    # ← 输出文件夹
KEY_COL = "部门"             # ← 按哪一列拆分（列名要和实际表头一致）
SHEET = 0                   # 第几个 sheet


def preflight():
    if not os.path.isfile(SRC):
        print("❌ 找不到源文件：%s\n   检查路径；./ 指脚本运行目录。" % SRC)
        return False
    print("🔍 预检通过：准备按列【%s】拆分。" % KEY_COL)
    return True


def main():
    if not preflight():
        return
    try:
        df = pd.read_excel(SRC, sheet_name=SHEET)
        if KEY_COL not in df.columns:
            print("❌ 表里没有【%s】这一列。\n   现有列名：%s\n   把 KEY_COL 改成其中任意一个。" % (KEY_COL, list(df.columns)))
            return
        os.makedirs(OUT_DIR, exist_ok=True)
        n = 0
        for val, g in df.groupby(KEY_COL):
            safe = str(val).replace("/", "_").replace("\\", "_")[:50]
            out = os.path.join(OUT_DIR, "%s.xlsx" % safe)
            g.to_excel(out, index=False)
            n += 1
        print("✅ 已拆成 %d 个文件 -> %s" % (n, OUT_DIR))
    except Exception as e:
        print("❌ 拆分出错：%s" % e)


if __name__ == "__main__":
    main()
