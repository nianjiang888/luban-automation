#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁班·Excel 去重：按"某列"或"整行"删除重复行，保留首次出现
# 依赖：pip install pandas openpyxl
# 用法：改下方"配置区"后 python excel_dedupe.py
import os
import pandas as pd

# ===== 配置区（只改这里）=====
SRC = r"./待去重.xlsx"        # ← 源文件
OUT = r"./去重后.xlsx"         # ← 输出
KEY_COL = None                 # ← 填列名则按该列去重；留 None 按整行去重
SHEET = 0
KEEP_FIRST = True              # True=保留首次；False=保留末次


def preflight():
    if not os.path.isfile(SRC):
        print("❌ 找不到源文件：%s" % SRC)
        return False
    print("🔍 预检通过：准备去重（按%s）。" % ("整行" if KEY_COL is None else "列【%s】" % KEY_COL))
    return True


def main():
    if not preflight():
        return
    try:
        df = pd.read_excel(SRC, sheet_name=SHEET)
        before = len(df)
        df = df.drop_duplicates(subset=KEY_COL, keep="first" if KEEP_FIRST else "last")
        after = len(df)
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        df.to_excel(OUT, index=False)
        print("✅ 去重完成：%d 行 -> %d 行，删掉 %d 条重复 -> %s" % (before, after, before - after, OUT))
    except KeyError:
        print("❌ 指定的列名不存在。\n   现有列名：%s" % list(df.columns))
    except Exception as e:
        print("❌ 去重出错：%s" % e)


if __name__ == "__main__":
    main()
