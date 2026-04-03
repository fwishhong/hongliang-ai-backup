#!/usr/bin/env python3
"""
ddgs_news_fallback.py - 当官方源失败时用 ddgs 补充新闻
用法:
  python3 ddgs_news_fallback.py --category tech --count 5
"""

import sys
import json
import argparse
from ddgs import DDGS
from datetime import datetime

CATEGORIES = {
    'tech': ['AI', 'OpenAI', 'DeepSeek', 'Google', 'Microsoft', 'Nvidia', 'GPT-5', 'Agent'],
    'finance': ['stock', 'market', 'Bitcoin', 'Fed', 'interest rate', 'economy'],
    'politics': ['Trump', 'Biden', 'Putin', 'Zelensky', 'Ukraine', 'China US'],
    'all': ['AI', 'tech', 'stock market', 'Bitcoin', 'Trump', 'Russia Ukraine']
}

def search_news(category='tech', count=5):
    keywords = CATEGORIES.get(category, CATEGORIES['all'])
    
    results = []
    seen_titles = set()
    
    with DDGS() as ddgs:
        for kw in keywords[:3]:  # 最多搜3个关键词
            try:
                for r in ddgs.text(f"{kw} news 2026", max_results=count):
                    title = r.get('title', '')
                    if title and title not in seen_titles:
                        seen_titles.add(title)
                        results.append({
                            "source": f"DDGS ({kw})",
                            "title": title,
                            "url": r.get('href', ''),
                            "heat": "",
                            "time": datetime.now().strftime("%Y-%m-%d"),
                            "body": r.get('body', '')[:150]
                        })
                        if len(results) >= count:
                            break
            except Exception as e:
                print(f"Error searching {kw}: {e}", file=sys.stderr)
            
            if len(results) >= count:
                break
    
    return results[:count]

def main():
    parser = argparse.ArgumentParser(description='DDGS 新闻补充')
    parser.add_argument('--category', '-c', default='all', 
                        choices=['tech', 'finance', 'politics', 'all'],
                        help='新闻类别')
    parser.add_argument('--count', '-n', type=int, default=5, help='结果数量')
    parser.add_argument('--format', '-f', choices=['json', 'text'], default='json', help='输出格式')
    args = parser.parse_args()
    
    results = search_news(args.category, args.count)
    
    if args.format == 'json':
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['title']}")
            print(f"   {r['url']}")
            print()

if __name__ == "__main__":
    main()
