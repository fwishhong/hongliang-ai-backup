#!/usr/bin/env python3
"""
X账号简报定时任务 - 生成并发送简报到飞书和Telegram
"""

import requests
import json
import sys
import os
from datetime import datetime
from typing import List, Dict

SEARXNG_URL = "http://localhost:8888"
TELEGRAM_BOT_TOKEN = "8258919046:AAGc1T0iGNBvL7diVzaDgTWpa7x9syin14g"
TELEGRAM_CHAT_ID = "8091679787"
FEISHU_USER_ID = "ou_97e8a151e0a917023ffa52d4c1f20372"

# 科技账号
TECH_ACCOUNTS = [
    "sama", "elonmusk", "AndrewYNg", "ylecun", "JeffDean",
    "sundarpichai", "SatyaNadella", "DarioAmodei", "AndrewYang", "Jensen_Huang"
]

# 政治账号
POLITICS_ACCOUNTS = [
    "realDonaldTrump", "POTUS", "narendramodi", "ZelenskyyUa", "Putin"
]

# 金融账号
FINANCE_ACCOUNTS = [
    "paulkrugman", "elErnest", "CathieDWood", "zerohedge", "business"
]

# 热门话题
TOPICS = [
    "OpenAI GPT-5", "Anthropic Claude", "Google Gemini", "xAI Grok", "Nvidia",
    "AI agent", "AGI", "Trump", "Fed interest rate", "China economy"
]

def search(query: str, num_results: int = 10) -> List[Dict]:
    """搜索"""
    try:
        params = {"q": query, "format": "json", "num_results": num_results}
        resp = requests.get(f"{SEARXNG_URL}/search", params=params, timeout=15)
        return resp.json().get("results", [])
    except Exception as e:
        print(f"Search error: {e}", file=sys.stderr)
        return []

def generate_briefing() -> str:
    """生成简报"""
    date = datetime.now().strftime("%Y年%m月%d日")
    lines = [f"# X账号简报", f"**日期：{date}**", ""]
    
    # 热门话题
    lines.append("## 🔥 热门话题")
    for topic in TOPICS[:6]:
        results = search(topic, 3)
        if results:
            lines.append(f"- **{topic}**: {results[0].get('title', '')[:60]}")
    lines.append("")
    
    # 科技
    lines.append("## 🤖 科技动态")
    seen = set()
    for acc in TECH_ACCOUNTS[:4]:
        for r in search(f"from:{acc}", 3):
            title = r.get("title", "")
            if title and title not in seen:
                lines.append(f"- **@{acc}**: {title[:60]}")
                seen.add(title)
                break
    lines.append("")
    
    # 政治
    lines.append("## 🌍 政治动态")
    seen = set()
    for acc in POLITICS_ACCOUNTS[:3]:
        for r in search(f"from:{acc}", 3):
            title = r.get("title", "")
            if title and title not in seen:
                lines.append(f"- **@{acc}**: {title[:60]}")
                seen.add(title)
                break
    lines.append("")
    
    # 金融
    lines.append("## 💰 经济金融")
    seen = set()
    for acc in FINANCE_ACCOUNTS[:3]:
        for r in search(f"from:{acc}", 3):
            title = r.get("title", "")
            if title and title not in seen:
                lines.append(f"- **@{acc}**: {title[:60]}")
                seen.add(title)
                break
    lines.append("")
    
    lines.append(f"---\n**生成时间**: {datetime.now().strftime('%H:%M')}")
    return "\n".join(lines)

def send_telegram(text: str):
    """发送到Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": text[:4000], "parse_mode": "Markdown"}
    resp = requests.post(url, json=data)
    return resp.status_code == 200

def send_feishu(text: str):
    """发送到飞书"""
    # 飞书通过Telegram Bot发送（因为飞书API配置复杂）
    # 这里先用Telegram代替
    return send_telegram(text)

def main():
    print("Generating briefing...")
    content = generate_briefing()
    
    # 保存到文件
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"/Users/hongliang/.openclaw/workspace/x_tech_briefing_{date_str}.md"
    with open(filename, 'w') as f:
        f.write(content)
    print(f"Saved to {filename}")
    
    # 发送到Telegram
    if send_telegram(content):
        print("Sent to Telegram!")
    else:
        print("Failed to send to Telegram")
    
    print("Done!")

if __name__ == "__main__":
    main()
