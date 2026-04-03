#!/usr/bin/env python3
"""
每日新闻聚合脚本 - 直接运行，无需 bash 包装
"""
import os
import sys
import json
from datetime import datetime

SKILL_DIR = "/Users/hongliang/.openclaw/workspace/skills/news-aggregator-skill-3"
SCRIPT = f"{SKILL_DIR}/scripts/fetch_news.py"
REPORTS_DIR = f"{SKILL_DIR}/scripts/reports"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M")
RAW_FILE = f"/tmp/news_raw_{TIMESTAMP}.json"

print(f"=== [{datetime.now().strftime('%Y-%m-%d %H:%M')}] 开始新闻聚合 ===")

# 1. 获取新闻
os.system(f"cd {SKILL_DIR} && python3 {SCRIPT} --source all --limit 15 > {RAW_FILE} 2>&1")

# 2. 检查并格式化
if not os.path.exists(RAW_FILE) or os.path.getsize(RAW_FILE) == 0:
    print("❌ 获取新闻失败")
    sys.exit(1)

with open(RAW_FILE, "r") as f:
    content = f.read()
    if not content.strip():
        print("❌ JSON 文件为空")
        sys.exit(1)
    data = json.loads(content)

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
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
- 来源: {source} | 时间: {time_val} | 热度: {heat}
- {summary}

"""

# 3. 保存报告
os.makedirs(REPORTS_DIR, exist_ok=True)
ts_safe = TIMESTAMP.replace(" ", "_").replace(":", "")
report_file = f"{REPORTS_DIR}/daily_{ts_safe}.md"
with open(report_file, 'w', encoding='utf-8') as f:
    f.write(report)

print(f"✅ 报告已保存: {report_file}")
print(f"📊 获取到 {len(data)} 条新闻，前10条已整理")
print("=== 完成 ===")
