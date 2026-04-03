#!/bin/bash
# 正常新闻自动汇报 - 每天 8:30 和 19:30 自动执行
# 使用 news-aggregator-skill 获取新闻，发送到飞书

# ===== 修复 cron 环境变量问题 =====
# 强制加载用户环境变量
if [ -f ~/.zshrc ]; then
    source ~/.zshrc
elif [ -f ~/.bashrc ]; then
    source ~/.bashrc
fi

# 如果代理仍未生效，强制设置
if [ -z "$http_proxy" ]; then
    export http_proxy=http://127.0.0.1:7897
    export https_proxy=http://127.0.0.1:7897
    export HTTP_PROXY=http://127.0.0.1:7897
    export HTTPS_PROXY=http://127.0.0.1:7897
fi

export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"
PYTHON3="/usr/local/bin/python3"

NEWS_DIR="$HOME/.openclaw/workspace/skills/news-aggregator-skill-3"
LOCK_FILE="/tmp/normal_news_cron.lock"
TIMESTAMP=$(date +%Y-%m-%d\ %H:%M)
HOUR=$(date +%H)

# 防止重复运行（10分钟内只运行一次）
if [ -f "$LOCK_FILE" ]; then
    LOCK_TIME=$(stat -f %m "$LOCK_FILE" 2>/dev/null || stat -c %Y "$LOCK_FILE" 2>/dev/null)
    CURRENT_TIME=$(date +%s)
    if [ $((CURRENT_TIME - LOCK_TIME)) -lt 600 ]; then
        echo "=== 10分钟内已运行过，跳过 ==="
        exit 0
    fi
fi
touch "$LOCK_FILE"

echo "=== [$(date '+%Y-%m-%d %H:%M')] 正常新闻汇报 ==="

# 获取新闻
cd "$NEWS_DIR"
NEWS_JSON=$($PYTHON3 scripts/fetch_news.py --source hackernews,36kr,weibo,wallstreetcn --limit 15 2>/dev/null)

if [ -z "$NEWS_JSON" ] || [ "$NEWS_JSON" = "[]" ]; then
    echo "No news fetched"
    exit 1
fi

# 生成报告
REPORT=$($PYTHON3 << ENDPY
import json
import sys

timestamp = "$TIMESTAMP"
hour = int("$HOUR")

try:
    items = json.loads('''$NEWS_JSON''')
except:
    print("Failed to parse news")
    sys.exit(1)

# 分类新闻
geo_news = []
econ_news = []
tech_news = []

for item in items:
    title = item.get('title', '')
    source = item.get('source', '')
    url = item.get('url', '')
    time = item.get('time', '')
    heat = item.get('heat', '')
    
    # 简单分类
    keywords_geo = ['伊朗', '以色列', '美国', '中国', '俄罗斯', '欧洲', '中东', '导弹', '战争', '特朗普', '普京']
    keywords_econ = ['GDP', '股市', '美元', '油价', '关税', '美联储', '经济', '金融', '通胀', '非农']
    keywords_tech = ['AI', 'OpenAI', '苹果', '谷歌', '微软', '小鹏', '汽车', '芯片', '科技']
    
    if any(k in title for k in keywords_geo):
        geo_news.append((title, source, time, heat, url))
    elif any(k in title for k in keywords_econ):
        econ_news.append((title, source, time, heat, url))
    elif any(k in title for k in keywords_tech):
        tech_news.append((title, source, time, heat, url))
    else:
        econ_news.append((title, source, time, heat, url))

# 生成报告
report = f"""## 📰 过去24小时重大新闻汇总

### 🌍 地缘政治
"""

if geo_news:
    for i, (title, source, time, heat, url) in enumerate(geo_news[:5], 1):
        heat_str = f"**热度**: {heat}" if heat else ""
        report += f"""**{i}. {title}**
- **来源**: {source} | **时间**: {time} {heat_str}
- **链接**: {url}

"""
else:
    report += "_暂无_\n\n"

report += """### 💰 经济金融
"""

if econ_news:
    for i, (title, source, time, heat, url) in enumerate(econ_news[:5], 1):
        heat_str = f"**热度**: {heat}" if heat else ""
        report += f"""**{i}. {title}**
- **来源**: {source} | **时间**: {time} {heat_str}
- **链接**: {url}

"""
else:
    report += "_暂无_\n\n"

report += """### 🤖 科技动态
"""

if tech_news:
    for i, (title, source, time, heat, url) in enumerate(tech_news[:5], 1):
        heat_str = f"**热度**: {heat}" if heat else ""
        report += f"""**{i}. {title}**
- **来源**: {source} | **时间**: {time} {heat_str}
- **链接**: {url}

"""
else:
    report += "_暂无_\n\n"

report += f"""### 📊 今日数据
| 指标 | 数值 |
|------|------|
| 数据源 | HN、36Kr、微博、华尔街见闻 |
| 抓取时间 | {timestamp} |

### 💡 总结
- 最值得关注的3条详见上方"""

print(report)
ENDPY
)

# 发送到飞书 - 写入临时文件后用 Python 发送
echo "$REPORT" > /tmp/news_report_$$.txt
$PYTHON3 << ENDPY
import subprocess
with open("/tmp/news_report_$$.txt") as f:
    report = f.read()
subprocess.run([
    "openclaw", "message", "send",
    "--channel", "feishu",
    "--target", "ou_97e8a151e0a917023ffa52d4c1f20372",
    "--message", report
], check=True)
ENDPY
rm -f /tmp/news_report_$$.txt

echo "=== 完成 ==="
