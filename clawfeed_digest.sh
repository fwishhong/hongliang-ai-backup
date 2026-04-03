#!/bin/bash
# ClawFeed Digest Generator - 每天自动生成新闻摘要
# 使用 news-aggregator 获取新闻，发送到 ClawFeed

API_URL="http://127.0.0.1:8767"
API_KEY="clayfeed2026"
NEWS_DIR="$HOME/.openclaw/workspace/skills/news-aggregator-skill-3"

echo "===== ClawFeed Digest Generator $(date) ====="

# 获取综合新闻
echo "Fetching news..."
NEWS_JSON=$(cd "$NEWS_DIR" && python3 scripts/fetch_news.py --source hackernews,36kr,wallstreetcn --limit 15 2>/dev/null)

if [ -z "$NEWS_JSON" ] || [ "$NEWS_JSON" = "[]" ]; then
    echo "No news fetched, using fallback content"
    NEWS_JSON='[{"source":"System","title":"Daily digest generated","content":"News fetch failed, using backup"}]'
fi

# 构建 digest 内容
CONTENT="# 📰 每日新闻摘要 $(date '+%Y-%m-%d')

来源：HackerNews, 36Kr, WallStreetCN

---

## 今日热门

"

# 解析 JSON 并构建 markdown
echo "$NEWS_JSON" | python3 -c "
import json, sys

try:
    items = json.load(sys.stdin)
    for i, item in enumerate(items[:15], 1):
        title = item.get('title', 'No title')
        source = item.get('source', 'Unknown')
        url = item.get('url', '')
        time = item.get('time', '')
        
        print(f'### {i}. {title}')
        print(f'**来源**: {source}' + (f' | {time}' if time else ''))
        if url:
            print(f'**链接**: {url}')
        print()
except:
    print('Failed to parse news')
" >> /tmp/clawfeed_content.md

# 添加总结
cat >> /tmp/clawfeed_content.md << 'EOF'

---

*由 ClawFeed 自动生成 | $(date)*
EOF

# 读取内容
DIGEST_CONTENT=$(cat /tmp/clawfeed_content.md)

# 发送到 ClawFeed API
echo "Creating digest..."
RESPONSE=$(curl -s -X POST "$API_URL/api/digests" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d "{
    \"type\": \"daily\",
    \"content\": $(echo "$DIGEST_CONTENT" | jq -Rs .)
  }")

echo "Response: $RESPONSE"

# 清理
rm -f /tmp/clawfeed_content.md

echo "Done!"
