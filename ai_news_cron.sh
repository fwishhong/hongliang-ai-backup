#!/bin/bash
# AI Signal Board 新闻汇报 - 每半小时版本
# 8:00 发夜间汇总，其他时间发这半小时新增的新闻

# ===== 修复 cron 环境变量问题 =====
# 强制加载用户环境变量
if [ -f ~/.zshrc ]; then
    source ~/.zshrc
elif [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# 如果代理仍未生效，强制设置
if [ -z "$http_proxy" ]; then
    export http_proxy=http://127.0.0.1:7897
    export https_proxy=http://127.0.0.1:7897
    export HTTP_PROXY=http://127.0.0.1:7897
    export HTTPS_PROXY=http://127.0.0.1:7897
fi

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

NEWS_DIR="/Users/hongliang/.openclaw/workspace/ai-news-radar"
LAST_RUN_FILE="/tmp/ai_news_last_run.txt"
LOCK_FILE="/tmp/ai_news_cron.lock"
TIMESTAMP=$(date +%Y-%m-%d\ %H:%M:%S)
HOUR=$(date +%H)

# 8:00 场次特殊处理：不管之前有没有运行过，都必须执行
if [ "$HOUR" = "8" ]; then
    rm -f "$LOCK_FILE"
fi

# 防止其他时段重复运行（5分钟内只运行一次）
if [ -f "$LOCK_FILE" ]; then
    LOCK_TIME=$(stat -f %m "$LOCK_FILE" 2>/dev/null || stat -c %Y "$LOCK_FILE" 2>/dev/null)
    CURRENT_TIME=$(date +%s)
    if [ $((CURRENT_TIME - LOCK_TIME)) -lt 300 ]; then
        echo "=== 5分钟内已运行过，跳过 ==="
        exit 0
    fi
fi
touch "$LOCK_FILE"

echo "=== [$(date '+%Y-%m-%d %H:%M')] AI Signal Board 新闻汇报 ==="

# 1. 更新新闻数据
cd "$NEWS_DIR"
.venv/bin/python scripts/update_news.py --output-dir data --window-hours 24 2>&1

# 2. 根据时间生成不同报告
python3 << ENDPY
import json
from datetime import datetime, timedelta
import os

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
hour = int("$HOUR")
news_dir = "$NEWS_DIR"
last_run_file = "$LAST_RUN_FILE"

with open(f"{news_dir}/data/latest-24h.json", "r") as f:
    data = json.load(f)

total = data["total_items"]

# 8:00 发夜间汇总，其他时间发这半小时新增的
if hour == 8:
    # 夜间汇总：筛选0点-8点发布的新闻
    night_items = []
    for item in data["items"]:
        pub_time = item.get("published_at", "")
        if pub_time:
            try:
                dt = datetime.fromisoformat(pub_time.replace("Z", "+00:00"))
                if 16 <= dt.hour or dt.hour <= 23:
                    night_items.append(item)
            except:
                pass
    
    items = night_items[:30] if night_items else data["items"][:15]
    
    report = f"""# 🌙 夜间要闻回顾

**{timestamp}** | **夜间({len(night_items)}条)**

---
"""
    if len(night_items) > 30:
        report += f"*仅显示前30条，共{len(night_items)}条*\n\n"

else:
    # 读取上次发送时间
    last_run = None
    if os.path.exists(last_run_file):
        with open(last_run_file, "r") as f:
            last_run = datetime.fromisoformat(f.read().strip())
    
    # 筛选这半小时新增的新闻
    new_items = []
    for item in data["items"]:
        pub_time = item.get("published_at", "")
        if pub_time:
            try:
                dt = datetime.fromisoformat(pub_time.replace("Z", "+00:00"))
                if last_run and dt > last_run:
                    new_items.append(item)
                elif not last_run:
                    # 首次运行，取最新15条
                    new_items.append(item)
            except:
                pass
    
    items = new_items[:30]  # 最多30条
    
    # 保存本次时间
    with open(last_run_file, "w") as f:
        f.write(datetime.now().isoformat())
    
    # 如果没有新新闻，取最新的15条，确保每半小时都发送
    if not items:
        print("没有新新闻，取最新15条发送")
        items = data["items"][:15]
    
    report = f"""# 📰 AI 新闻速报

**{timestamp}** | **最新{len(items)}条** | **24h共{total}条**

---
"""

for i, item in enumerate(items, 1):
    title = item.get("title_zh") or item.get("title") or "无标题"
    url = item.get("url", "#")
    source = item.get("site_name", "未知")
    pub_time = (item.get("published_at") or "")[:16].replace("T", " ")
    
    report += f"""**{i}. {title}**
> {source} | {pub_time}

"""

report += f"""---
数据来源: AI Signal Board ({data.get('site_count', 10)}个源聚合)"""

print(report)

# 发送到 Telegram (已禁用，只发飞书)
# import requests
# token = "8258919046:AAGc1T0iGNBvL7diVzaDgTWpa7x9syin14g"
# chat_id = "8091679787"
# url = f"https://api.telegram.org/bot{token}/sendMessage"
# payload = {"chat_id": chat_id, "text": report, "parse_mode": "Markdown"}
# try:
#     r = requests.post(url, json=payload, timeout=10)
#     print(f"✅ 发送到Telegram: {r.status_code}")
# except Exception as e:
#     print(f"❌ Telegram发送失败: {e}")

# 发送到微信 - 使用 openclaw-weixin CLI
try:
    import subprocess
    wechat_user = "o9cq807HpYgjyGEiwS4skQyWez-o@im.wechat"
    cmd = [
        "openclaw", "message", "send",
        "--channel", "openclaw-weixin",
        "--target", wechat_user,
        "--message", report[:4000]
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode == 0:
        print(f"✅ 发送到微信: 成功")
    else:
        print(f"❌ 微信发送失败: {result.stderr}")
except Exception as e:
    print(f"❌ 微信发送失败: {e}")

ENDPY

echo "=== 完成 ==="
