#!/usr/bin/env python3
"""
ClawFeed RSS 抓取脚本
每天自动抓取 RSS 源，调用 ClawFeed API 生成每日简报
"""

import json
import sqlite3
import time
import os
from datetime import datetime, timedelta
from urllib.request import urlopen, Request
from urllib.error import URLError
import ssl
import re

# 配置
CLAWFEED_API_URL = "http://127.0.0.1:8767/api/digests"
CLAWFEED_API_KEY = "clayfeed2026"
DB_PATH = os.path.expanduser("~/.openclaw/workspace/skills/clawfeed/data/digest.db")

# RSS 源列表（政治 + 金融 + 科技）
RSS_SOURCES = [
    # 科技
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/"},
    {"name": "HackerNews", "url": "https://news.ycombinator.com/rss"},
    {"name": "The Verge", "url": "https://www.theverge.com/rss/index.xml"},
    {"name": "Wired", "url": "https://www.wired.com/feed/rss"},
    {"name": "Ars Technica", "url": "https://feeds.arstechnica.com/arstechnica/index"},
    
    # 金融
    {"name": "Bloomberg", "url": "https://feeds.bloomberg.com/markets/news.rss"},
    {"name": "WSJ", "url": "https://feeds.aol.com/aol/rss/topstories"},
    {"name": "Financial Times", "url": "https://www.ft.com/rss/home"},
    {"name": "CNBC", "url": "https://www.cnbc.com/id/100003114/device/rss/rss.html"},
    
    # 政治/国际
    {"name": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml"},
    {"name": "Reuters World", "url": "https://www.reuters.com/world/rssfeed/"},
    {"name": "NYT World", "url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"},
    {"name": "AP News", "url": "https://feeds.apnews.com/apnews/topnews"},
    
    # 中文
    {"name": "华尔街见闻", "url": "https://api.tuofeng.net/v1/wallstreetcn/rss"},
    {"name": "少数派", "url": "https://sspai.com/feed"},
]

def fetch_rss(url, timeout=15):
    """抓取 RSS 源"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = Request(url, headers=headers)
        with urlopen(req, timeout=timeout, context=ctx) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"  ❌ {url}: {e}")
        return None

def parse_rss(xml_content):
    """解析 RSS 内容"""
    items = []
    
    # 匹配 item 或 entry
    item_pattern = r'<item>(.*?)</item>'
    entry_pattern = r'<entry>(.*?)</entry>'
    
    for pattern in [item_pattern, entry_pattern]:
        matches = re.findall(pattern, xml_content, re.DOTALL)
        for match in matches:
            title = re.search(r'<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>', match, re.DOTALL)
            link = re.search(r'<link>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</link>', match, re.DOTALL)
            desc = re.search(r'<description>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>', match, re.DOTALL)
            
            if title:
                item = {
                    "title": title.group(1).strip(),
                    "url": link.group(1).strip() if link else "",
                    "desc": desc.group(1).strip()[:200] if desc else ""
                }
                items.append(item)
    
    return items[:15]  # 每个源最多15条

def create_digest(title, content):
    """调用 ClawFeed API 创建 digest"""
    import urllib.request
    
    data = json.dumps({
        "type": "daily",
        "content": content,
        "metadata": json.dumps({
            "generated_at": datetime.now().isoformat(),
            "source": "auto-rss-fetcher"
        })
    }).encode('utf-8')
    
    req = Request(
        CLAWFEED_API_URL,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {CLAWFEED_API_KEY}'
        },
        method='POST'
    )
    
    try:
        with urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"  ✅ Digest created: {result.get('id')}")
            return result
    except Exception as e:
        print(f"  ❌ Failed to create digest: {e}")
        return None

def main():
    print(f"\n📡 ClawFeed RSS Fetcher - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    all_items = []
    sources_count = 0
    
    for source in RSS_SOURCES:
        print(f"\n📥 Fetching: {source['name']}...")
        xml = fetch_rss(source['url'])
        
        if xml:
            items = parse_rss(xml)
            print(f"  📰 Got {len(items)} items")
            
            for item in items:
                item['source'] = source['name']
                all_items.append(item)
            sources_count += 1
        else:
            print(f"  ⚠️ Failed to fetch")
    
    print(f"\n📊 Total: {len(all_items)} items from {sources_count} sources")
    
    if not all_items:
        print("❌ No items fetched, skipping digest creation")
        return
    
    # 构建 digest 内容
    content_lines = [f"### 📰 Daily Digest - {datetime.now().strftime('%Y-%m-%d')}", ""]
    content_lines.append(f"**来源**: RSS 自动聚合 ({sources_count} 个源)")
    content_lines.append("")
    
    # 按来源分组
    by_source = {}
    for item in all_items:
        src = item.get('source', 'Unknown')
        if src not in by_source:
            by_source[src] = []
        by_source[src].append(item)
    
    for src, items in by_source.items():
        content_lines.append(f"#### {src}")
        for item in items[:5]:  # 每个源最多5条
            title = item['title'][:80] + ('...' if len(item['title']) > 80 else '')
            url = item['url']
            content_lines.append(f"- [{title}]({url})")
        content_lines.append("")
    
    content_lines.append(f"*由 RSS Fetcher 自动生成 | {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    
    content = "\n".join(content_lines)
    
    print(f"\n📝 Creating digest...")
    result = create_digest("Daily Digest", content)
    
    if result:
        print(f"\n🎉 Done! Digest ID: {result.get('id')}")
    else:
        print(f"\n❌ Failed to create digest")

if __name__ == "__main__":
    main()
