#!/bin/bash
# 发送AI新闻到两个平台

cd ~/.openclaw/workspace/ai-news-radar
python3 scripts/update_news.py --window-hours 24 2>/dev/null

# 获取前10条
DATA=$(python3 -c "
import json
with open('data/latest-24h.json') as f:
    d = json.load(f)
for i, item in enumerate(d['items'][:10], 1):
    t = item.get('title_zh','')[:55]
    s = item.get('site_name','')
    print(f'{i}. {t} | {s}')
")

MSG="📰 AI新闻速报 2026-03-04

$DATA

来源: AI Signal Board"

# 发飞书
openclaw message send --channel feishu \
  --target "ou_97e8a151e0a917023ffa52d4c1f20372" \
  --message "$MSG" > /dev/null 2>&1

echo "Done: $(date)"
