#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁班·轻量采集：抓取一个公开网页里的所有表格，存成 Excel
# 合规前提：仅采集公开数据；遵守目标站 robots.txt；加延迟不高频；不破反爬、不侵版权。
# 依赖：pip install pandas requests beautifulsoup4 lxml
# 用法：把 URL 改成合规公开网页后 python crawler_table.py
import os
import pandas as pd
import requests, time

# ===== 配置区（只改这里）=====
URL = "在此填入公开网页地址"     # ← 改成合规公开网页（先自查该站 robots.txt 是否允许采集）
OUT = r"./采集结果.xlsx"         # ← 输出路径
DELAY = 1                        # 请求间隔秒数，礼貌采集不要调太小


def preflight():
    if "在此填入" in URL or not URL.startswith("http"):
        print("❌ 还没填网页地址：请先把 URL 改成你要采集的合规公开网页。")
        return False
    print("🔍 预检通过：准备采集 %s（请确认你已查看该站 robots.txt 允许采集）。" % URL)
    return True


def main():
    if not preflight():
        return
    try:
        HEADERS = {"User-Agent": "Mozilla/5.0 (合规教学采集)"}
        r = requests.get(URL, headers=HEADERS, timeout=15)
        r.raise_for_status()
        time.sleep(DELAY)
        tables = pd.read_html(r.text)
        if not tables:
            print("❌ 该页没解析到 <table> 表格。\n   换思路：①页面可能是 JS 动态渲染，需用 Playwright ②或表格是图片需 OCR。")
            return
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        with pd.ExcelWriter(OUT) as w:
            for i, t in enumerate(tables):
                t.to_excel(w, sheet_name="table_%d" % i, index=False)
        print("✅ 已抓取 %d 个表格 -> %s" % (len(tables), OUT))
    except requests.exceptions.HTTPError as e:
        print("❌ 网页返回错误（404/403 等）：%s\n   403 多为反爬，请换数据源或放弃。" % e)
    except requests.exceptions.ConnectionError:
        print("❌ 连不上网页：检查网络，或网址拼写。")
    except Exception as e:
        print("❌ 采集出错：%s" % e)


if __name__ == "__main__":
    main()
