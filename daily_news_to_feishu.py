#!/usr/bin/env python3
"""
每日新闻聚合脚本 - 运行 news-aggregator-skill 并发送到飞书
"""

import os
import sys
import json
from datetime import datetime

# 配置
SKILL_DIR = "/Users/hongliang/.openclaw/workspace/skills/news-aggregator-skill-3"
REPORTS_DIR = f"{SKILL_DIR}/scripts/reports"
SCRIPT_PATH = f"{SKILL_DIR}/scripts/fetch_news.py"

# 飞书配置 (需要老洪提供)
FEISHU_APP_ID = os.environ.get("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
FEISHU_DOC_TOKEN = os.environ.get("FEISHU_DOC_TOKEN", "")


def run_news_scan():
    """运行全网扫描"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    print(f"🕐 [{timestamp}] 开始新闻扫描...")
    
    # 全局扫描策略：先广后深
    os.chdir(SKILL_DIR)
    
    cmd = f"""
    python3 {SCRIPT_PATH} --source all --limit 15 --deep
    """
    print(f"执行命令: {cmd}")
    
    result = os.popen(cmd).read()
    return result


def format_for_feishu(news_data):
    """将新闻格式化为飞书文档格式"""
    # 这里解析 news_data 并格式化为飞书兼容的 markdown
    pass


def send_to_feishu(content, title):
    """发送到飞书文档"""
    if not FEISHU_APP_ID or not FEISHU_DOC_TOKEN:
        print("⚠️  飞书配置缺失，请设置环境变量:")
        print("   FEISHU_APP_ID")
        print("   FEISHU_APP_SECRET") 
        print("   FEISHU_DOC_TOKEN")
        return False
    
    wechat_user = "o9cq807HpYgjyGEiwS4skQyWez-o@im.wechat"
    import subprocess
    result = subprocess.run(
        ["/Users/hongliang/bin/weclaw", "send",
         "--to", wechat_user,
         "--text", content[:4000]],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 0:
        print(f"✅ 发送到微信: 成功")
    else:
        print(f"❌ 微信发送失败: {result.stderr}")
    print(f"📤 准备发送到飞书文档: {FEISHU_DOC_TOKEN}")
    return True


def save_report(content, timestamp):
    """保存报告到本地"""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    filename = f"{REPORTS_DIR}/daily_news_{timestamp}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"💾 报告已保存: {filename}")
    return filename


def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    
    # 1. 运行新闻扫描
    news_raw = run_news_scan()
    
    # 2. 解析和处理结果
    try:
        news_items = json.loads(news_raw)
        
        # 格式化为报告
        report = f"""# 每日新闻摘要 - {datetime.now().strftime("%Y-%m-%d %H:%M")}

## 全网热点

"""
        for item in news_items[:10]:
            title = item.get('title', '无标题')
            url = item.get('url', '')
            source = item.get('source', '未知')
            time = item.get('time', '')
            heat = item.get('heat', 0)
            
            report += f"### [{title}]({url})\n"
            report += f"- 来源: {source} | 时间: {time} | 热度: {heat}\n\n"
        
        # 3. 保存报告
        report_file = save_report(report, timestamp)
        
        # 4. 发送到飞书
        send_to_feishu(report, f"每日新闻 - {timestamp}")
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON解析失败: {e}")
        print(f"原始输出: {news_raw[:500]}")


if __name__ == "__main__":
    main()
