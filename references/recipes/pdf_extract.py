#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁班·PDF 提取文本：把一个（或文件夹下所有）PDF 的文字提取成 .txt
# 依赖：pip install pypdf
# 用法：改下方"配置区"后 python pdf_extract.py
import os, glob
from pypdf import PdfReader

# ===== 配置区（只改这里）=====
IN = r"./pdf_in"          # ← 文件夹（批量）或单个 .pdf 路径
OUT_DIR = r"./pdf_text"    # ← 输出文件夹


def preflight():
    if os.path.isfile(IN):
        print("🔍 预检通过：单文件模式 %s" % IN)
        return True
    if not os.path.isdir(IN):
        print("❌ 找不到：%s\n   可填单个 pdf 路径，或放 pdf 的文件夹。" % IN)
        return False
    if not glob.glob(os.path.join(IN, "*.pdf")):
        print("❌ 文件夹里没有 pdf：%s" % IN)
        return False
    print("🔍 预检通过：批量模式 %s" % IN)
    return True


def extract_one(path):
    texts = []
    for i, page in enumerate(PdfReader(path).pages, 1):
        try:
            texts.append("--- 第 %d 页 ---\n%s" % (i, page.extract_text() or ""))
        except Exception as e:
            texts.append("--- 第 %d 页 提取失败：%s ---" % (i, e))
    return "\n".join(texts)


def main():
    if not preflight():
        return
    try:
        os.makedirs(OUT_DIR, exist_ok=True)
        paths = [IN] if os.path.isfile(IN) else sorted(glob.glob(os.path.join(IN, "*.pdf")))
        for p in paths:
            txt = extract_one(p)
            out = os.path.join(OUT_DIR, os.path.splitext(os.path.basename(p))[0] + ".txt")
            with open(out, "w", encoding="utf-8") as f:
                f.write(txt)
            print("✅ 提取 -> %s" % out)
        print("全部完成。注：扫描件图片型 PDF 文字层为空，需改用 pdf_ocr.py。")
    except Exception as e:
        print("❌ 提取出错：%s" % e)


if __name__ == "__main__":
    main()
