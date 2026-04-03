#!/usr/bin/env python3
"""
ddgs-search - DuckDuckGo 搜索封装
用法:
  python ddgs_search.py "搜索关键词" [--count N] [--format json|text]
"""

import sys
import json
import argparse
from ddgs import DDGS

def main():
    parser = argparse.ArgumentParser(description='DuckDuckGo 搜索')
    parser.add_argument('query', help='搜索关键词')
    parser.add_argument('--count', '-n', type=int, default=5, help='返回结果数量')
    parser.add_argument('--format', choices=['json', 'text'], default='text', help='输出格式')
    args = parser.parse_args()
    
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(args.query, max_results=args.count))
            
            if args.format == 'json':
                print(json.dumps(results, ensure_ascii=False, indent=2))
            else:
                for i, r in enumerate(results, 1):
                    print(f"{i}. {r.get('title', '')}")
                    print(f"   {r.get('href', '')}")
                    print(f"   {r.get('body', '')[:100]}...")
                    print()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
