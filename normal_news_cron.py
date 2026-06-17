#!/usr/bin/env python3
# 正常新闻自动汇报 - 每天 8:30 和 19:30 自动执行

import subprocess
import json
import os
import sys
from datetime import datetime

PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
LOCK_FILE = "/tmp/normal_news_cron.lock"
USER_ID = "ou_97e8a151e0a917023ffa52d4c1f20372"

# 防止重复运行（10分钟内只运行一次）
if os.path.exists(LOCK_FILE):
    lock_time = os.path.getmtime(LOCK_FILE)
    if (datetime.now().timestamp() - lock_time) < 600:
        print("=== 10分钟内已运行过，跳过 ===")
        sys.exit(0)
open(LOCK_FILE, 'w').close()

print(f"=== [{datetime.now().strftime('%Y-%m-%d %H:%M')}] 正常新闻汇报 ===")

# 获取新闻
try:
    result = subprocess.run(
        ["python3", "scripts/fetch_news.py", "--source", "hn,36kr,weibo,wallstreetcn", "--limit", "15"],
        cwd=os.path.expanduser("~/.openclaw/workspace/skills/news-aggregator-skill-3"),
        capture_output=True, text=True, timeout=60
    )
    items = json.loads(result.stdout)
except Exception as e:
    print(f"获取新闻失败: {e}")
    sys.exit(1)

# 分类新闻
geo, econ, tech = [], [], []
kw_geo = ['伊朗','以色列','美国','中国','俄罗斯','欧洲','中东','导弹','战争','特朗普','普京','乌克兰']
kw_econ = ['GDP','股市','美元','油价','关税','美联储','经济','金融','通胀','非农','人民币','出口']
kw_tech = ['AI','OpenAI','苹果','谷歌','微软','小鹏','汽车','芯片','科技','特斯拉','小米']

for item in items:
    t, s, u = item.get('title',''), item.get('source',''), item.get('url','')
    ti, h = item.get('time',''), item.get('heat','')
    
    if any(k in t for k in kw_geo):
        geo.append((t,s,ti,h,u))
    elif any(k in t for k in kw_econ):
        econ.append((t,s,ti,h,u))
    elif any(k in t for kw in kw_tech for k in [kw]):
        tech.append((t,s,ti,h,u))
    else:
        econ.append((t,s,ti,h,u))

# 生成报告
report = "## 📰 过去24小时重大新闻汇总\n\n"
report += "### 🌍 地缘政治\n"
for i,(t,s,ti,h,u) in enumerate(geo[:5],1):
    heat_str = f" | 热度: {h}" if h else ""
    report += f"**{i}. {t}**\n- 来源: {s} | 时间: {ti}{heat_str}\n\n"

report += "### 💰 经济金融\n"
for i,(t,s,ti,h,u) in enumerate(econ[:5],1):
    heat_str = f" | 热度: {h}" if h else ""
    report += f"**{i}. {t}**\n- 来源: {s} | 时间: {ti}{heat_str}\n\n"

report += "### 🤖 科技动态\n"
for i,(t,s,ti,h,u) in enumerate(tech[:5],1):
    heat_str = f" | 热度: {h}" if h else ""
    report += f"**{i}. {t}**\n- 来源: {s} | 时间: {ti}{heat_str}\n\n"

report += f"### 📊 数据\n- 来源: HN、36Kr、微博、华尔街见闻\n- 时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}"

# 发送飞书
feishu_user = "ou_97e8a151e0a917023ffa52d4c1f20372"
try:
    result = subprocess.run(
        ["openclaw", "message", "send",
         "--channel", "feishu",
         "--target", feishu_user,
         "--message", report[:4000]],
        capture_output=True, text=True, timeout=60
    )
    print(result.stdout)
    if result.returncode == 0:
        print("=== 飞书发送成功 ===")
    else:
        print(f"发送失败: {result.stderr}")
except Exception as e:
    print(f"发送失败: {e}")
