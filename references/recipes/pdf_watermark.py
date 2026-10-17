#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁班·PDF 加水印：给每页加半透明文字水印（如"机密/草稿/公司名"）
# 依赖：pip install pypdf reportlab
# 用法：改下方"配置区"后 python pdf_watermark.py
import os, glob
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


# ===== 配置区（只改这里）=====
IN = r"./pdf_in"            # ← 文件夹（批量）或单文件
OUT_DIR = r"./pdf_wm"       # ← 输出
TEXT = "机密·请勿外传"       # ← 水印文字
OPACITY = 0.25              # 透明度 0~1，越小越淡


def make_wm(text):
    from reportlab.lib.colors import Color
    w, h = A4
    buf = os.path.join(OUT_DIR, "_wm_tmp.pdf")
    c = canvas.Canvas(buf, pagesize=A4)
    c.setFillColor(Color(0, 0, 0, alpha=OPACITY))
    c.setFont("Helvetica", 36)
    c.saveState()
    c.translate(w / 2, h / 2)
    c.rotate(30)
    c.drawCentredString(0, 0, text)
    c.restoreState()
    c.save()
    return buf


def preflight():
    if not os.path.isdir(IN) and not os.path.isfile(IN):
        print("❌ 找不到：%s" % IN)
        return False
    os.makedirs(OUT_DIR, exist_ok=True)
    print("🔍 预检通过：准备加水印【%s】。" % TEXT)
    return True


def main():
    if not preflight():
        return
    try:
        wm = make_wm(TEXT)
        paths = [IN] if os.path.isfile(IN) else sorted(glob.glob(os.path.join(IN, "*.pdf")))
        for p in paths:
            r = PdfReader(p)
            w = PdfWriter()
            for page in r.pages:
                page.merge_page(PdfReader(wm).pages[0])
                w.add_page(page)
            out = os.path.join(OUT_DIR, os.path.basename(p))
            with open(out, "wb") as f:
                w.write(f)
            print("✅ 水印 -> %s" % out)
        os.remove(wm)
        print("全部完成。")
    except Exception as e:
        print("❌ 加水印出错：%s" % e)


if __name__ == "__main__":
    main()
