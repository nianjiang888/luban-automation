#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁班·Excel 合并：把某文件夹下所有 .xlsx 合并成一个总表（按文件名分 sheet）
# 依赖：pip install pandas openpyxl
# 用法：改下方"配置区"后 python excel_merge.py
import os, glob
import pandas as pd

# ===== 配置区（只改这里）=====
FOLDER = r"./excel_in"            # ← 改成你的文件夹路径（放待合并的 xlsx）
OUT = r"./excel_out/合并总表.xlsx"  # ← 输出路径
SHEET_INDEX = 0                   # 0 = 每个文件第一个 sheet；改数字取第 N 个


def preflight():
    if not os.path.isdir(FOLDER):
        print("❌ 找不到文件夹：%s\n   请检查路径是否写对、是否用了相对路径（脚本在哪运行，./ 就指哪）。" % FOLDER)
        return False
    files = glob.glob(os.path.join(FOLDER, "*.xlsx"))
    if not files:
        print("❌ 文件夹里没有 .xlsx 文件：%s\n   确认后缀是 .xlsx（不是 .xls/.csv），且文件没被 Excel 占用。" % FOLDER)
        return False
    print("🔍 预检通过：找到 %d 个 xlsx，准备合并。" % len(files))
    return True


def main():
    if not preflight():
        return
    try:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with pd.ExcelWriter(OUT) as writer:
            for f in sorted(glob.glob(os.path.join(FOLDER, "*.xlsx"))):
                name = os.path.splitext(os.path.basename(f))[0][:31]
                try:
                    df = pd.read_excel(f, sheet_name=SHEET_INDEX)
                except Exception as e:
                    print("⚠️ 跳过损坏/打不开的文件 %s：%s" % (os.path.basename(f), e))
                    continue
                df.to_excel(writer, sheet_name=name, index=False)
        print("✅ 已合并 -> %s" % OUT)
    except PermissionError:
        print("❌ 输出文件被占用：%s\n   关掉已打开的 Excel/目标文件，再跑一次。" % OUT)
    except Exception as e:
        print("❌ 合并出错：%s\n   常见原因：①某个表列数差异过大 ②文件被占用。先单文件试，再批量。" % e)


if __name__ == "__main__":
    main()
