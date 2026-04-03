#!/bin/bash
# 每日新闻聚合 - Cron 调用版本
# 每天 8:00, 12:00, 16:00, 22:00 自动运行

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"
SKILL_DIR="/Users/hongliang/.openclaw/workspace/skills/news-aggregator-skill-3"
SCRIPT="$SKILL_DIR/scripts/fetch_news.py"
REPORTS_DIR="$SKILL_DIR/scripts/reports"
TIMESTAMP=$(date +%Y%m%d_%H%M)
RAW_FILE="/tmp/news_raw_${TIMESTAMP}.json"

mkdir -p "$REPORTS_DIR"

echo "=== [$(date '+%Y-%m-%d %H:%M')] 开始新闻聚合 ==="

# 1. 获取新闻
cd "$SKILL_DIR"
python3 "$SCRIPT" --source all --limit 15 > "$RAW_FILE" 2>&1

# 2. 检查并格式化
if [ ! -s "$RAW_FILE" ]; then
    echo "❌ 获取新闻失败"
    exit 1
fi

python3 << ENDPY
import json
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
ts = "$TIMESTAMP"
raw_file = f"/tmp/news_raw_{ts}.json"

with open(raw_file, "r") as f:
    content = f.read()
    if not content.strip():
        print("❌ JSON 文件为空")
        exit(1)
    data = json.loads(content)

report = f"""# 📰 每日新闻摘要

**生成时间**: {timestamp}

---

## 🔥 热点新闻

"""

for i, item in enumerate(data[:10], 1):
    title = item.get('title', '无标题')
    url = item.get('url', '#')
    source = item.get('source', '未知')
    time_val = item.get('time', '')
    heat = item.get('heat', 0)
    summary = item.get('summary', '')[:200]
    
    report += f"""### {i}. [{title}]({url})
- 来源: {{source}} | 时间: {{time_val}} | 热度: {{heat}}
- {{summary}}

"""

# 保存报告
ts_safe = ts.replace(" ", "_").replace(":", "")
report_file = f"{REPORTS_DIR}/daily_{{ts_safe}}.md"
with open(report_file, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✅ 报告已保存: {{report_file}}")
print(f"📊 获取到 {{len(data)}} 条新闻，前10条已整理")

ENDPY

echo "=== 完成 ==="
