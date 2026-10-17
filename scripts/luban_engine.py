#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""鲁班引擎：办公自动化。先校验输入 → 红线 → 智能选脚本 → 输出可运行代码 + 能力边界 + 预期效果。

用法：
    python luban_engine.py "帮我把这个文件夹的 Excel 都合并"
    python luban_engine.py "把总表按部门拆成多个文件"
    python luban_engine.py "把扫描件pdf识别成文字"
    python luban_engine.py --scene pdf "给这几个pdf加水印"

输出：输入澄清（如需） + 红线校验 + 场景判定 + 可运行脚本（含预检占位符） + 能力边界 + 预期效果 + 依赖 + 合规前提。
"""
import json
import os
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "resources", "luban.json")
RECIPE_DIR = os.path.join(HERE, "..", "references", "recipes")

# 动词同义词 → recipe 键
SYNONYMS = {
    "拆分": ["拆", "分开", "切分", "拆分"],
    "去重": ["去重", "重复", "剔重"],
    "提取": ["提取", "取文字", "转文本", "导出文字"],
    "水印": ["水印"],
    "ocr": ["ocr", "扫描", "识别文字", "扫描件"],
    "转csv": ["转csv", "转成csv", "导出csv"],
    "重命名": ["重命名", "改名", "统一命名"],
    "转换": ["转换", "转格式", "互转"],
}


def load_resources():
    try:
        with open(RES, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("❌ 技能资源加载失败：%s\n   请确认 luban.json 与脚本在同一包内、未损坏。" % e)
        raise SystemExit(1)


def check_red_flag(text, res):
    hits = []
    for kw in ["反爬", "付费墙", "破解", "绕过付费", "密码", "隐私", "批量抓取他人", "病毒", "勒索", "恶意", "一键搞定", "肯定能行"]:
        if kw in text:
            hits.append(kw)
    return hits


# 口语信号词 → 场景（keywords 没命中时的兜底，避免"拆成/总表"类说法锁不定场景）
SCENE_HINTS = {
    "excel": ["表", "xlsx", "csv", "拆", "总表", "单元格", "行列", "数据表", "sheet"],
    "pdf": ["pdf", "扫描", "页"],
    "batch": ["改名", "素材", "图片", "转格式", "重命名"],
    "crawler": ["网页", "网站", "抓", "采集"],
    "doc": ["word", "报告", "docx", "通知", "文书"],
    "schedule": ["定时", "每天", "周期", "自动跑", "计划"],
}


def score_scenes(text, res):
    scored = []
    for s in res.get("scenes", []):
        kw_hit = sum(1 for k in s.get("keywords", []) if k in text)
        hint_hit = sum(1 for h in SCENE_HINTS.get(s["id"], []) if h in text)
        sc = kw_hit + hint_hit * 0.5
        if sc > 0:
            scored.append((s["id"], sc, s))
    scored.sort(key=lambda x: -x[1])
    return scored


def select_recipe(scene, text):
    recipes = scene.get("recipes", {})
    for key, path in recipes.items():
        if key == "默认":
            continue
        for syn in SYNONYMS.get(key, [key]):
            if syn in text:
                return path, key
    return recipes.get("默认"), "默认"


def emit_scene(scene, recipe_path, recipe_name):
    out = []
    out.append("识别场景：【%s】——%s" % (scene["name"], scene["desc"]))
    out.append("选中脚本：%s（%s）" % (recipe_path, recipe_name))
    out.append("")
    out.append("✅ 能做的：")
    for x in scene.get("can_do", []):
        out.append("   · " + x)
    out.append("⚠️ 暂时做不到的：")
    for x in scene.get("cannot_do", []):
        out.append("   · " + x)
    if scene.get("large_file"):
        out.append("📦 大文件：%s" % scene["large_file"])
    if scene.get("special_format"):
        out.append("🧩 特殊格式：%s" % scene["special_format"])
    if scene.get("expected"):
        out.append("🎯 预期效果：%s" % scene["expected"])
    if scene.get("tips"):
        out.append("💡 提示：" + "；".join(scene["tips"]))
    out.append("")
    return "\n".join(out)


def run(text, scene=None, res=None):
    res = res or load_resources()
    lines = []
    persona = res.get("persona", "鲁班")
    lines.append("【%s】说吧，哪活儿要 automation——" % persona)
    lines.append("")

    # 输入校验：太短/无实质 → 澄清，不吐脚本
    if len(text.strip()) < 4:
        lines.append("没太听懂，先确认三件事（答完我直接给脚本）：")
        for q in res.get("clarify_questions", []):
            lines.append("  1. " + q if q == res["clarify_questions"][0] else "  2. " + q if q == res["clarify_questions"][1] else "  3. " + q)
        lines.append("")
        lines.append("免责：" + res.get("disclaimer", ""))
        return "\n".join(lines)

    flags = check_red_flag(text, res)
    if flags:
        lines.append("⛔ 红线提示：涉及%s，本技能只做合规自动化——不碰隐私、不破防护、不写恶意代码、不承诺一键搞定。" % "、".join(flags))
        lines.append("")
        return "\n".join(lines)

    target = None
    if scene:
        target = next((s for s in res["scenes"] if s["id"] == scene), None)
    if target is None:
        sc = score_scenes(text, res)
        target = sc[0][2] if sc else None

    if target is None:
        lines.append("没锁定场景，可选：Excel / PDF / 批量处理 / 轻量采集 / 文档生成 / 定时任务。")
        lines.append("先回答这 3 个我直接给脚本：")
        for i, q in enumerate(res.get("clarify_questions", []), 1):
            lines.append("  %d. %s" % (i, q))
        lines.append("")
        lines.append("免责：" + res.get("disclaimer", ""))
        return "\n".join(lines)

    recipe_path, recipe_name = select_recipe(target, text)
    lines.append(emit_scene(target, recipe_path, recipe_name))
    full = os.path.join(RECIPE_DIR, recipe_path)
    if os.path.exists(full):
        code = open(full, "r", encoding="utf-8").read()
        lines.append("```python")
        lines.append(code.rstrip("\n"))
        lines.append("```")
        lines.append("")
    else:
        lines.append("⚠️ 脚本文件 %s 未找到，请确认包完整。" % recipe_path)
        lines.append("")
    lines.append("依赖：" + res.get("deps", ""))
    lines.append("")
    lines.append("⚠️ 合规前提：仅处理您有权处理的文件/数据；采集须守 robots.txt 与合理频率，不破反爬、不侵版权隐私。")
    lines.append("")
    lines.append("免责：" + res.get("disclaimer", ""))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="鲁班引擎")
    ap.add_argument("text", nargs="?", default="", help="用户要自动化的活")
    ap.add_argument("--scene", choices=[s["id"] for s in load_resources()["scenes"]], default=None)
    args = ap.parse_args()
    print(run(args.text, scene=args.scene))


if __name__ == "__main__":
    main()
