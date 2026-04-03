#!/usr/bin/env python3
"""正常新闻自动汇报 - 直接发送到飞书"""

import subprocess
import json
import os
import requests

# 配置
NEWS_DIR = os.path.expanduser("~/.openclaw/workspace/skills/news-aggregator-skill-3")
PROXY = {"http": "http://127.0.0.1:7897", "https": "http://127.0.0.1:7897"}
FEISHU_USER_ID = "ou_97e8a151e0a917023ffa52d4c1f20372"

# 获取新闻
result = subprocess.run(
    ["python3", "scripts/fetch_news.py", "--source", "hn,36kr,weibo,wallstreetcn", "--limit", "15"],
    cwd=NEWS_DIR,
    capture_output=True,
    text=True,
    env={**os.environ, "https_proxy": "http://127.0.0.1:7897", "http_proxy": "http://127.0.0.1:7897"}
)

if result.returncode != 0 or not result.stdout.strip():
    print("Failed to fetch news")
    exit(1)

try:
    items = json.loads(result.stdout)
except:
    print("Failed to parse news")
    exit(1)

# 分类
geo, econ, tech = [], [], []
geo_kw = ['伊朗', '以色列', '美国', '中国', '俄罗斯', '欧洲', '中东', '导弹', '战争', '特朗普', '普京', '两会']
econ_kw = ['GDP', '股市', '美元', '油价', '关税', '美联储', '经济', '金融', '通胀', '非农', '央行', '石油']
tech_kw = ['AI', 'OpenAI', '苹果', '谷歌', '微软', '小鹏', '汽车', '芯片', '科技']

for item in items:
    title = item.get('title', '')
    src = item.get('source', '')
    t = item.get('time', '')
    heat = item.get('heat', '')
    url = item.get('url', '')
    
    if any(k in title for k in geo_kw):
        geo.append((title, src, t, heat, url))
    elif any(k in title for k in econ_kw):
        econ.append((title, src, t, heat, url))
    elif any(k in title for k in tech_kw):
        tech.append((title, src, t, heat, url))
    else:
        econ.append((title, src, t, heat, url))

# 构建报告
from datetime import datetime
ts = datetime.now().strftime("%Y-%m-%d %H:%M")

report = f"""## 📰 今日新闻汇总

### 🌍 地缘政治
"""
for i, (title, src, t, heat, url) in enumerate(geo[:5], 1):
    h = f"**热度**: {heat}" if heat else ""
    report += f"""**{i}. {title}**
- **来源**: {src} | **时间**: {t} {h}

"""

report += """### 💰 经济金融
"""
for i, (title, src, t, heat, url) in enumerate(econ[:5], 1):
    h = f"**热度**: {heat}" if heat else ""
    report += f"""**{i}. {title}**
- **来源**: {src} | **时间**: {t} {h}

"""

report += """### 🤖 科技动态
"""
for i, (title, src, t, heat, url) in enumerate(tech[:5], 1):
    h = f"**热度**: {heat}" if heat else ""
    report += f"""**{i}. {title}**
- **来源**: {src} | **时间**: {t} {h}

"""

report += f"""---
*新闻自动汇报 | {ts}*"""

# 发送到飞书 - 用 OpenClaw message
subprocess.run([
    "openclaw", "message", "send",
    "--channel", "feishu",
    "--target", FEISHU_USER_ID,
    "--message", report
], timeout=30)

print("Done!")
