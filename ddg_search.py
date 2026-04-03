#!/usr/bin/env python3
"""简单搜索脚本 - 使用 DuckDuckGo"""

import sys
from ddgs import DDGS

def search(query, max_results=5):
    ddgs = DDGS()
    results = ddgs.text(query, max_results=max_results)
    return results

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "hello"
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    results = search(query, max_results)
    
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   {r['href']}")
        print(f"   {r['body'][:150]}...")
        print()
