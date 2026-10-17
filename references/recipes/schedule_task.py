#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 鲁班·定时任务：每天定时跑一段活（演示：每天 09:00 执行 job()）
# 说明：脚本内循环适合临时用；长期稳定运行建议用系统定时：
#   Windows：任务计划程序 拉起 python schedule_task.py
#   macOS/Linux：crontab -e 加 0 9 * * * /usr/bin/python3 绝对路径/schedule_task.py
# 用法：把要定时做的逻辑写进 job() 后 python schedule_task.py
import time, datetime


def job():
    # ← 把要定时做的事放这里（可调用别的脚本/发通知）
    print("执行于", datetime.datetime.now())


def preflight():
    print("ℹ️ 定时任务说明：脚本循环方式会一直占着一个窗口；"
          "想开机自启/后台跑，请用系统定时（Windows 任务计划 / macOS launchd / Linux crontab）。")
    return True


def main():
    if not preflight():
        return
    target_hour, target_min = 9, 0
    print("定时任务已启动，每天 %02d:%02d 执行（Ctrl+C 停止）" % (target_hour, target_min))
    try:
        while True:
            now = datetime.datetime.now()
            if now.hour == target_hour and now.minute == target_min and now.second < 10:
                try:
                    job()
                except Exception as e:
                    print("⚠️ 本次 job 出错：%s" % e)
                time.sleep(60)
            time.sleep(20)
    except KeyboardInterrupt:
        print("\n⏹ 已停止定时任务。")


if __name__ == "__main__":
    main()
