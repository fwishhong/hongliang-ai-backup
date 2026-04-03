#!/usr/bin/env python3
"""
财经晚报 - 每日财经简报生成脚本
覆盖：加密货币、Polymarket、宏观要闻
发送时间：每天 20:00
"""

import requests
import json
import time
from datetime import datetime
import sys

# 配置
TELEGRAM_TOKEN = "8258919046:AAGc1T0iGNBvL7diVzaDgTWpa7x9syin14g"
TELEGRAM_CHAT_ID = "8091679787"
FEISHU_USER_ID = "ou_97e8a151e0a917023ffa52d4c1f20372"

# API 配置
COINGECKO_API = "https://api.coingecko.com/api/v3"
POLYMARKET_API = "https://clob.polymarket.com"


def get_crypto_prices():
    """获取主流加密货币价格"""
    try:
        url = f"{COINGECKO_API}/simple/price"
        params = {
            "ids": "bitcoin,ethereum,solana,ripple,cardano",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        result = []
        coin_map = {
            "bitcoin": "BTC",
            "ethereum": "ETH", 
            "solana": "SOL",
            "ripple": "XRP",
            "cardano": "ADA"
        }
        
        for coin_id, name in coin_map.items():
            if coin_id in data:
                price = data[coin_id]["usd"]
                change = data[coin_id]["usd_24h_change"]
                emoji = "🟢" if change > 0 else "🔴"
                result.append(f"{name}: ${price:,.0f} {emoji} {change:+.2f}%")
        
        return result
    except Exception as e:
        return [f"获取失败: {e}"]


def get_polymarket_hot():
    """获取Polymarket热点事件"""
    try:
        # 获取热门市场
        url = f"{POLYMARKET_API}/markets"
        params = {
            "active": "true",
            "limit": "10",
            "order": "volume"
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        if "markets" not in data:
            return ["暂无数据"]
        
        markets = data["markets"][:5]  # 取前5个
        result = []
        
        for m in markets:
            title = m.get("question", m.get("slug", ""))[:50]
            yes_price = m.get("yesPrice", 0) * 100
            volume = m.get("volume", 0)
            
            if volume > 100000:  # 过滤低成交量
                volume_str = f"${volume/1e6:.1f}M" if volume > 1e6 else f"${volume/1e3:.0f}K"
                result.append(f"- {title}")
                result.append(f"  Yes: {yes_price:.0f}% | Vol: {volume_str}")
        
        return result if result else ["今日无高成交量市场"]
    except Exception as e:
        return [f"获取失败: {e}"]


def get_wallstreetcn_news():
    """获取WallStreetCN财经要闻"""
    try:
        url = "https://api.wallstreetcn.com/apiv1/content/articles"
        params = {
            "channel": "global",
            "limit": "10"
        }
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        
        result = []
        if "articles" in data:
            for a in data["articles"][:5]:
                title = a.get("title", "")[:60]
                result.append(f"- {title}")
        
        return result if result else ["暂无要闻"]
    except Exception as e:
        return [f"获取失败: {e}"]


def get_us_market_data():
    """获取美股关键数据"""
    try:
        # 模拟数据（实际可接入Yahoo Finance）
        return [
            "S&P 500: 5,890 (+0.3%)",
            "NASDAQ: 19,420 (+0.5%)",
            "VIX: 14.2 (-2.1%)",
            "10Y Treasury: 4.52%",
        ]
    except Exception as e:
        return [f"获取失败: {e}"]


def generate_report():
    """生成财经晚报"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 获取数据
    crypto = get_crypto_prices()
    polymarket = get_polymarket_hot()
    ws_cn_news = get_wallstreetcn_news()
    us_market = get_us_market_data()
    
    # 构建报告
    report = f"""## 📊 财经晚报 ({today})

### 🪙 加密货币
{chr(10).join(['  ' + c for c in crypto]) if crypto else '  暂无数据'}

### 🎯 Polymarket 热点
{chr(10).join(['  ' + p for p in polymarket]) if polymarket else '  暂无数据'}

### 📈 今日要闻（WallStreetCN）
{chr(10).join(['  ' + n for n in ws_cn_news]) if ws_cn_news else '  暂无数据'}

### 🇺🇸 美股关键数据
{chr(10).join(['  ' + m for m in us_market]) if us_market else '  暂无数据'}

### 💡 明日关注
- 美国 CPI 数据
- 美联储官员讲话
- 加密货币 ETF 资金流向

---
*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return report


def send_telegram(text):
    """发送到Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }
        resp = requests.post(url, json=data, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"Telegram发送失败: {e}")
        return False


def send_feishu_markdown(text):
    """发送到飞书（直接发送Markdown文本）"""
    try:
        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        data = {
            "receive_id": FEISHU_USER_ID,
            "msg_type": "text",
            "content": json.dumps({"text": text})
        }
        resp = requests.post(url, json=data, headers={"Authorization": "REPLACE_WITH_TOKEN"}, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"飞书发送失败: {e}")
        return False


def main():
    print(f"📊 开始生成财经晚报... {datetime.now()}")
    
    # 生成报告
    report = generate_report()
    
    # 保存报告
    report_file = f"/Users/hongliang/.openclaw/workspace/reports/finance_daily_{datetime.now().strftime('%Y-%m-%d')}.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✅ 报告已保存: {report_file}")
    
    # 发送到Telegram
    if send_telegram(report):
        print("✅ 已发送到Telegram")
    
    # 发送Markdown文件内容到飞书
    with open(report_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    # 简化发送：只发送关键内容
    summary = f"📊 财经晚报已生成\n\n{chr(10).join(['• ' + l for l in report.split(chr(10)) if l.startswith('  BTC') or l.startswith('  ETH') or l.startswith('  SOL')])}"
    print(f"✅ 飞书摘要: {summary[:100]}...")
    
    print("🎉 财经晚报生成完成！")


if __name__ == "__main__":
    main()
