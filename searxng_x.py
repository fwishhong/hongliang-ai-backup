#!/usr/bin/env python3
"""
X账号科技简报生成器 - 使用SearXNG
"""

import requests
import json
import sys
from datetime import datetime
from typing import List, Dict

SEARXNG_URL = "http://localhost:8888"

# 科技与AI领域的关键账号和话题
TECH_ACCOUNTS = [
    "sama",       # Sam Altman (OpenAI)
    "elonmusk",   # Elon Musk (xAI/Tesla)
    "AndrewYNg",  # 吴恩达
    "ylecun",     # Yann LeCun (Meta)
    "JeffDean",   # Jeff Dean (Google)
    "sundarpichai", # Sundar Pichai (Google)
    "SatyaNadella", # Satya Nadella (Microsoft)
    "DarioAmodei", # Dario Amodei (Anthropic)
    "AndrewYang", # 杨安泽
    "Jensen_Huang", # 黄仁勋 (Nvidia)
    "hwchase17",  # AI
    "sama",       # AI
]

# 政治账号
POLITICS_ACCOUNTS = [
    "realDonaldTrump",  # Trump
    "POTUS",          # 美国总统
    "narendramodi",   # 印度总理
    "ZelenskyyUa",    # 泽连斯基
    "Putin",          # 普京
    "BorisJohnson",   # 英国
    "Pontifex",      # 教皇
]

# 经济金融账号
FINANCE_ACCOUNTS = [
    "paulkrugman",    # 诺贝尔经济学奖
    "elErnest",       # Michael Burry
    "CathieDWood",    # Ark Invest
    "zerohedge",      # 金融博客
    "business",       # Bloomberg
    "WSJ",            # 华尔街日报
    "FT",             # 金融时报
]

# 热门话题
TOPICS = [
    "OpenAI GPT-5",
    "Anthropic Claude",
    "Google Gemini",
    "xAI Grok",
    "Nvidia",
    "AI agent",
    "AGI",
    "Trump",
    "Fed interest rate",
    "China economy",
]

def search(query: str, num_results: int = 10) -> List[Dict]:
    """搜索"""
    params = {
        "q": query,
        "format": "json",
        "num_results": num_results,
    }
    try:
        resp = requests.get(f"{SEARXNG_URL}/search", params=params, timeout=15)
        data = resp.json()
        return data.get("results", [])
    except Exception as e:
        print(f"Search error: {e}", file=sys.stderr)
        return []

def search_account(account: str) -> List[Dict]:
    """搜索特定账号的最近动态"""
    return search(f"from:{account}", 10)

def generate_briefing() -> str:
    """生成简报"""
    date = datetime.now().strftime("%Y年%m月%d日")
    lines = [f"# X账号简报", f"**日期：{date}**", ""]
    
    # 搜索热门话题
    lines.append("## 🔥 热门话题")
    for topic in TOPICS[:8]:
        results = search(topic, 3)
        if results:
            r = results[0]
            lines.append(f"- **{topic}**: {r.get('title', '')[:80]}")
    lines.append("")
    
    # 搜索科技账号
    lines.append("## 🤖 科技动态")
    seen = set()
    for acc in TECH_ACCOUNTS[:6]:
        results = search(f"from:{acc}", 3)
        if results:
            for r in results:
                title = r.get("title", "")
                if title and title not in seen:
                    lines.append(f"- **@{acc}**: {title[:60]}")
                    seen.add(title)
                    break
    lines.append("")
    
    # 搜索政治账号
    lines.append("## 🌍 政治动态")
    seen = set()
    for acc in POLITICS_ACCOUNTS[:4]:
        results = search(f"from:{acc}", 3)
        if results:
            for r in results:
                title = r.get("title", "")
                if title and title not in seen:
                    lines.append(f"- **@{acc}**: {title[:60]}")
                    seen.add(title)
                    break
    lines.append("")
    
    # 搜索金融账号
    lines.append("## 💰 经济金融")
    seen = set()
    for acc in FINANCE_ACCOUNTS[:4]:
        results = search(f"from:{acc}", 3)
        if results:
            for r in results:
                title = r.get("title", "")
                if title and title not in seen:
                    lines.append(f"- **@{acc}**: {title[:60]}")
                    seen.add(title)
                    break
    lines.append("")
    
    lines.append(f"---\n**生成时间**: {datetime.now().strftime('%H:%M')}")
    return "\n".join(lines)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--briefing":
        print(generate_briefing())
    elif len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        results = search(query, 10)
        for i, r in enumerate(results):
            print(f"{i+1}. {r.get('title','')}")
            print(f"   {r.get('url','')}")
            print()
    else:
        print("Usage:")
        print("  searxng_x.py <query>           # 搜索")
        print("  searxng_x.py --briefing      # 生成简报")

if __name__ == "__main__":
    main()
