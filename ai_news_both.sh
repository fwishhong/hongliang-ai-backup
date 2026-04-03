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

# 发微信
openclaw message send --channel openclaw-weixin \
  --target "o9cq807HpYgjyGEiwS4skQyWez-o@im.wechat" \
  --message "$MSG" > /dev/null 2>&1

# 发Telegram (备用)
curl -s -X POST "https://api.telegram.org/bot8258919046:AAGc1T0iGNBvL7diVzaDgTWpa7x9syin14g/sendMessage" \
  -d "chat_id=8091679787" -d "text=$MSG" > /dev/null

# 发飞书 - 需要tenant_access_token
# 先获取token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"cli_a90adbc0b278dcda","app_secret":"__OPENCLAW_REDACTED__"}' | python3 -c "import json,sys; print(json.load(sys.stdin).get('tenant_access_token',''))")

# 发送消息
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages/receive_open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id_type\":\"open_id\",\"receive_id\":\"ou_97e8a151e0a917023ffa52d4c1f20372\",\"msg_type\":\"text\",\"content\":\"$MSG\"}" > /dev/null

echo "Done: $(date)"
