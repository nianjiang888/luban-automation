#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁班·批量重命名：把文件夹下文件按 "前缀_序号.扩展名" 统一重命名
# 安全：先 DRY_RUN=True 预览，确认无误再改 False 执行（防改错）
# 用法：改下方"配置区"后 python batch_rename.py
import os

# ===== 配置区（只改这里）=====
FOLDER = r"./files"   # ← 改成你的文件夹
PREFIX = "物料"        # ← 新文件名前缀
DRY_RUN = True        # ← True 只预览；确认无误改 False 才真改名


def preflight():
    if not os.path.isdir(FOLDER):
        print("❌ 找不到文件夹：%s\n   检查路径。" % FOLDER)
        return False
    files = [f for f in os.listdir(FOLDER) if os.path.isfile(os.path.join(FOLDER, f))]
    if not files:
        print("❌ 文件夹是空的：%s" % FOLDER)
        return False
    print("🔍 预检通过：%d 个文件，预览模式=%s。" % (len(files), DRY_RUN))
    return True


def main():
    if not preflight():
        return
    try:
        files = [f for f in os.listdir(FOLDER) if os.path.isfile(os.path.join(FOLDER, f))]
        for i, f in enumerate(files, 1):
            ext = os.path.splitext(f)[1]
            new = "%s_%03d%s" % (PREFIX, i, ext)
            src = os.path.join(FOLDER, f)
            dst = os.path.join(FOLDER, new)
            if DRY_RUN:
                print("%s -> %s" % (f, new))
            else:
                if os.path.exists(dst):
                    print("⚠️ 跳过（已存在）%s" % new)
                    continue
                os.rename(src, dst)
        print("✅ 预览完成，确认无误请把 DRY_RUN 改 False 再跑" if DRY_RUN else "✅ 重命名完成")
    except Exception as e:
        print("❌ 出错：%s\n   可能原因：文件被占用。关掉占用程序再试。" % e)


if __name__ == "__main__":
    main()
