#!/bin/bash
cd ~/.openclaw/workspace/skills/news-aggregator-skill-3
rm -f scripts/reports/*.json scripts/reports/daily_*.md
python3 scripts/fetch_news.py --source hn,36kr,weibo,wallstreetcn --limit 10
echo "DONE:$?"