#!/usr/bin/env python3
"""
SearXNG 搜索工具 - 免费无限搜索
"""

import requests
import json
import sys
from typing import List, Dict, Optional

SEARXNG_URL = "http://localhost:8888"

def search(query: str, num_results: int = 10, category: str = "general") -> List[Dict]:
    """搜索网页"""
    params = {
        "q": query,
        "format": "json",
        "num_results": num_results,
        "categories": category
    }
    resp = requests.get(f"{SEARXNG_URL}/search", params=params, timeout=15)
    data = resp.json()
    return data.get("results", [])

def search_news(query: str, num_results: int = 10) -> List[Dict]:
    """搜索新闻"""
    return search(query, num_results, "news")

def format_result(result: Dict, idx: int) -> str:
    """格式化单条结果"""
    title = result.get("title", "无标题")
    url = result.get("url", "")
    content = result.get("content", "")[:200]
    return f"{idx+1}. **{title}**\n   {url}\n   {content[:100]}..."

def main():
    if len(sys.argv) < 2:
        print("Usage: searxng_search.py <query> [--news] [--limit N]")
        sys.exit(1)
    
    query = sys.argv[1]
    is_news = "--news" in sys.argv
    limit = 10
    
    for arg in sys.argv:
        if arg.startswith("--limit="):
            limit = int(arg.split("=")[1])
    
    category = "news" if is_news else "general"
    results = search(query, limit, category)
    
    print(f"Found {len(results)} results for '{query}':\n")
    for i, r in enumerate(results[:limit]):
        print(format_result(r, i))
        print()

if __name__ == "__main__":
    main()
