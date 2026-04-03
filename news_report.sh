#!/bin/bash
# 新闻汇报脚本 - 2026-03-04 修复版
# 正确的用法：清理缓存 + 指定源 + 不加keyword

cd ~/.openclaw/workspace/skills/news-aggregator-skill-3

# 清理缓存
rm -f scripts/reports/*.json scripts/reports/daily_*.md

# 抓新闻（4个有效源 × 10条 = 40条）
python3 scripts/fetch_news.py --source hn,36kr,weibo,wallstreetcn --limit 10

echo "新闻抓取完成"
