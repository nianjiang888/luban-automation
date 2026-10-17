#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁班·PDF  OCR：把扫描件/图片型 PDF 识别成文字（需本机装 Tesseract）
# 依赖：①pip install pytesseract pdf2image pillow ②另装 Tesseract OCR 引擎并配中文包
#       Windows：下载 Tesseract 安装，勾选中文；macOS：brew install tesseract tesseract-lang
# 用法：改下方"配置区"后 python pdf_ocr.py
import os, glob

# ===== 配置区（只改这里）=====
IN = r"./pdf_in"           # ← 文件夹（批量）或单文件
OUT_DIR = r"./pdf_ocr"     # ← 输出
LANG = "chi_sim+eng"       # 中文+英文；只英文改 "eng"


def preflight():
    try:
        import pytesseract
        from pdf2image import convert_from_path
    except ImportError:
        print("❌ 缺依赖：先 pip install pytesseract pdf2image pillow，并安装 Tesseract 引擎。")
        return False
    if not os.path.isdir(IN) and not os.path.isfile(IN):
        print("❌ 找不到：%s" % IN)
        return False
    os.makedirs(OUT_DIR, exist_ok=True)
    print("🔍 预检通过（依赖齐全）：准备 OCR 识别。")
    return True


def main():
    if not preflight():
        return
    try:
        import pytesseract
        from pdf2image import convert_from_path
    except Exception as e:
        print("❌ 依赖未就绪：%s" % e)
        return
    try:
        paths = [IN] if os.path.isfile(IN) else sorted(glob.glob(os.path.join(IN, "*.pdf")))
        for p in paths:
            print("识别中：%s" % os.path.basename(p))
            imgs = convert_from_path(p, dpi=200)
            text = []
            for i, img in enumerate(imgs, 1):
                text.append("--- 第 %d 页 ---\n%s" % (i, pytesseract.image_to_string(img, lang=LANG)))
            out = os.path.join(OUT_DIR, os.path.splitext(os.path.basename(p))[0] + ".txt")
            with open(out, "w", encoding="utf-8") as f:
                f.write("\n".join(text))
            print("✅ OCR -> %s" % out)
        print("全部完成。识别率取决于扫描清晰度，模糊图请提高 dpi。")
    except Exception as e:
        print("❌ OCR 出错：%s\n   多数情况是没装 Tesseract 引擎或没装中文语言包。" % e)


if __name__ == "__main__":
    main()
