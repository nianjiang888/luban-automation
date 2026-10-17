#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁班·批量格式转换：Excel(.xlsx) 与 CSV 互转 / 图片格式互转
# 依赖：pip install pandas openpyxl pillow
# 用法：改下方"配置区"后 python batch_convert.py
import os, glob
import pandas as pd
from PIL import Image

# ===== 配置区（只改这里）=====
IN = r"./convert_in"     # ← 输入文件夹
OUT_DIR = r"./convert_out"
MODE = "xlsx2csv"         # 可选：xlsx2csv / csv2xlsx / img2jpg / img2png
IMG_EXT = (".png", ".jpg", ".jpeg", ".bmp", ".webp")


def preflight():
    if not os.path.isdir(IN):
        print("❌ 找不到文件夹：%s" % IN)
        return False
    os.makedirs(OUT_DIR, exist_ok=True)
    print("🔍 预检通过：模式=%s" % MODE)
    return True


def main():
    if not preflight():
        return
    try:
        if MODE == "xlsx2csv":
            for f in glob.glob(os.path.join(IN, "*.xlsx")):
                df = pd.read_excel(f)
                out = os.path.join(OUT_DIR, os.path.splitext(os.path.basename(f))[0] + ".csv")
                df.to_csv(out, index=False, encoding="utf-8-sig")
                print("✅", os.path.basename(f), "-> csv")
        elif MODE == "csv2xlsx":
            for f in glob.glob(os.path.join(IN, "*.csv")):
                df = pd.read_csv(f)
                out = os.path.join(OUT_DIR, os.path.splitext(os.path.basename(f))[0] + ".xlsx")
                df.to_excel(out, index=False)
                print("✅", os.path.basename(f), "-> xlsx")
        elif MODE in ("img2jpg", "img2png"):
            fmt = "JPEG" if MODE == "img2jpg" else "PNG"
            ext = ".jpg" if MODE == "img2jpg" else ".png"
            for f in [x for x in glob.glob(os.path.join(IN, "*")) if x.lower().endswith(IMG_EXT)]:
                im = Image.open(f).convert("RGB")
                out = os.path.join(OUT_DIR, os.path.splitext(os.path.basename(f))[0] + ext)
                im.save(out, fmt)
                print("✅", os.path.basename(f), "->", ext)
        else:
            print("❌ MODE 不支持：填 xlsx2csv / csv2xlsx / img2jpg / img2png")
            return
        print("全部完成 -> %s" % OUT_DIR)
    except Exception as e:
        print("❌ 转换出错：%s" % e)


if __name__ == "__main__":
    main()
