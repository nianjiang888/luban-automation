#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁班·PDF 合并：把文件夹下所有 .pdf 按文件名顺序合并成一个
# 依赖：pip install pypdf
# 用法：改下方"配置区"后 python pdf_merge.py
import os, glob
from pypdf import PdfReader, PdfWriter

# ===== 配置区（只改这里）=====
FOLDER = r"./pdf_in"        # ← 改成你的文件夹（放待合并的 pdf）
OUT = r"./pdf_out/合并.pdf"  # ← 输出路径


def preflight():
    if not os.path.isdir(FOLDER):
        print("❌ 找不到文件夹：%s\n   检查路径；./ 指脚本运行所在目录。" % FOLDER)
        return False
    files = sorted(glob.glob(os.path.join(FOLDER, "*.pdf")))
    if not files:
        print("❌ 文件夹里没有 .pdf 文件：%s" % FOLDER)
        return False
    print("🔍 预检通过：找到 %d 个 pdf。" % len(files))
    return True


def main():
    if not preflight():
        return
    try:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        w = PdfWriter()
        ok = 0
        for f in sorted(glob.glob(os.path.join(FOLDER, "*.pdf"))):
            try:
                for page in PdfReader(f).pages:
                    w.add_page(page)
                ok += 1
            except Exception as e:
                print("⚠️ 跳过损坏的 PDF %s：%s" % (os.path.basename(f), e))
        if ok == 0:
            print("❌ 没有任何可读的 PDF，未生成文件。")
            return
        with open(OUT, "wb") as fp:
            w.write(fp)
        print("✅ 已合并 %d 个 PDF -> %s" % (ok, OUT))
    except PermissionError:
        print("❌ 输出被占用：%s\n   关掉已打开的 PDF 再跑。" % OUT)
    except Exception as e:
        print("❌ 合并出错：%s" % e)


if __name__ == "__main__":
    main()
