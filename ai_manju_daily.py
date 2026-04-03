#!/usr/bin/env python3
"""
AI 漫剧每日热点追踪
每天检查前一天最火爆的 AI 漫剧，收集播放数据、制作公司、专访等信息
"""

import requests
import json
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def search_bilibili_ai_manju(limit=10):
    """搜索B站AI漫剧/AI动画"""
    results = []
    keywords = ['AI漫剧', 'AI动画', 'AI短剧', 'AI动漫', 'AI动态漫']
    
    for kw in keywords:
        url = 'https://api.bilibili.com/x/web-interface/search/type'
        params = {'search_type': 'video', 'keyword': kw, 'pn': 1, 'ps': limit}
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for v in data.get('data', {}).get('result', [])[:limit]:
                    title = v.get('title', '').replace('<em class="keyword">', '').replace('</em>', '')
                    view_str = str(v.get('play', '0'))
                    try:
                        # 处理 "10.2万" 格式
                        if '万' in view_str:
                            views = int(float(view_str.replace('万', '')) * 10000)
                        else:
                            views = int(view_str)
                    except:
                        views = 0
                    results.append({
                        'title': title,
                        'views': views,
                        'url': f"https://www.bilibili.com/video/{v.get('bvid', '')}",
                        'source': 'B站'
                    })
        except Exception as e:
            print(f"B站搜索失败: {e}")
    
    # 去重并按播放量排序
    seen = set()
    unique_results = []
    for r in results:
        if r['title'] not in seen:
            seen.add(r['title'])
            unique_results.append(r)
    
    return sorted(unique_results, key=lambda x: x['views'], reverse=True)[:limit]


def search_douyin_ai_manju(limit=10):
    """抖音AI漫剧 - 通过搜索热榜"""
    results = []
    # 尝试不同的搜索接口
    urls = [
        'https://www.douyin.com/aweme/v1/web/hot/search/',
        'https://www.douyin.com/aweme/v1/web/hot/word/',
    ]
    
    for url in urls:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                words = data.get('data', {}).get('word_list', []) or data.get('data', {}).get('realtime', [])
                for w in words[:limit*2]:
                    note = w.get('word', '') or w.get('note', '')
                    if any(k in note for k in ['漫剧', '动画', '短剧', 'AI']):
                        results.append({
                            'title': note,
                            'views': w.get('heat', 0),
                            'url': f"https://www.douyin.com/search/{note}",
                            'source': '抖音'
                        })
                if results:
                    break
        except:
            continue
    
    return sorted(results, key=lambda x: x['views'], reverse=True)[:limit]


def search_kuaishou_ai_manju(limit=10):
    """快手AI漫剧"""
    results = []
    try:
        # 快手热榜
        resp = requests.get('https://www.kuaishou.com/short-video/feed', headers=HEADERS, timeout=5)
        # 快手没有公开API，尝试搜索
        url = 'https://www.kuaishou.com/graphql'
        # 这个可能不工作，但留个接口
    except Exception as e:
        print(f"快手: {e}")
    
    return results[:limit]


def search_tech_news_ai_manju():
    """搜索科技媒体的AI漫剧报道"""
    articles = []
    
    # 36Kr
    try:
        resp = requests.get('https://36kr.com/newsflashes', headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for item in soup.select('.newsflash-item')[:20]:
            title = item.select_one('.item-title')
            if title:
                t = title.get_text(strip=True)
                if any(k in t for k in ['AI', '漫剧', '动画', '视频', '短剧']):
                    href = title.get('href', '')
                    articles.append({
                        'title': t,
                        'url': f"https://36kr.com{href}" if not href.startswith('http') else href,
                        'source': '36Kr'
                    })
    except Exception as e:
        print(f"36Kr: {e}")
    
    return articles


def search_baidu_ai_manju():
    """百度搜索 AI 漫剧热点新闻（需要手动或浏览器）"""
    # 注意：百度有反爬虫验证，建议通过以下方式获取：
    # 1. 每天手动在百度搜 "AI漫剧 播放量" 
    # 2. 或使用浏览器自动化
    # 3. 或订阅 DataEye/蝉妈妈等服务
    
    # 这里返回空列表，实际使用时需要其他方式
    return []


def search_interviews(keyword):
    """搜索专访"""
    interviews = []
    
    # 微博搜索（通过热搜）
    try:
        # 尝试不同的搜索方式
        kw = f"AI漫剧 专访 {keyword}"
        url = f"https://www.soku.com/merge-ajaxsuggest-searchResult?encode=1&keyword={requests.utils.quote(kw)}"
        resp = requests.get(url, headers=HEADERS, timeout=5)
        if resp.status_code == 200:
            data = resp.json().get('result', [])
            for d in data[:5]:
                if '专访' in d.get('title', '') or '采访' in d.get('title', ''):
                    interviews.append({
                        'title': d.get('title', ''),
                        'url': d.get('url', ''),
                        'source': '微博/搜狗'
                    })
    except Exception as e:
        print(f"专访搜索: {e}")
    
    return interviews


def generate_report():
    """生成每日报告"""
    report = []
    report.append(f"# 🤖 AI 漫剧每日热点 ({datetime.now().strftime('%Y-%m-%d')})")
    report.append("")
    
    # 1. B站热点
    report.append("## 📺 B站 AI 漫剧播放排行")
    report.append("")
    bili_results = search_bilibili_ai_manju(5)
    if bili_results:
        for i, r in enumerate(bili_results, 1):
            views_str = f"{r['views']:,}" if r['views'] else "未知"
            report.append(f"{i}. **{r['title']}**")
            report.append(f"   - 播放: {views_str} | [链接]({r['url']})")
            report.append("")
    else:
        report.append("暂无数据")
        report.append("")
    
    # 2. 抖音热点
    report.append("## 📱 抖音 AI 漫剧热点")
    report.append("")
    douyin_results = search_douyin_ai_manju(5)
    if douyin_results:
        for i, r in enumerate(douyin_results, 1):
            report.append(f"{i}. **{r['title']}**")
            report.append(f"   - 热度: {r['views']} | [链接]({r['url']})")
            report.append("")
    else:
        report.append("暂无数据（抖音接口限制）")
        report.append("")
    
    # 3. 行业报道 - 36Kr
    report.append("## 📰 行业动态")
    report.append("")
    news = search_tech_news_ai_manju()
    if news:
        for n in news[:5]:
            report.append(f"- [{n['title']}]({n['url']}) - {n['source']}")
        report.append("")
    else:
        report.append("暂无36Kr报道")
        report.append("")
    
    # 4. 百度搜索热点
    report.append("## 🔎 百度搜索热点")
    report.append("")
    baidu_news = search_baidu_ai_manju()
    if baidu_news:
        for n in baidu_news[:5]:
            report.append(f"- [{n['title']}]({n['url']})")
        report.append("")
    else:
        report.append("*百度有反爬虫验证，建议手动搜索或使用付费数据服务*")
        report.append("")
    
    # 4. 手动搜索关键词（每日建议）
    report.append("## 🔍 手动搜索关键词")
    report.append("")
    report.append("建议每日搜索以下关键词获取最新热点：")
    report.append("")
    report.append("| 关键词 | 平台 | 用途 |")
    report.append("|--------|------|------|")
    report.append("| AI漫剧 播放量 | 百度 | 获取最新热点 |")
    report.append("| AI短剧 排行榜 | 抖音 | 热门短剧 |")
    report.append("| 漫剧 制作公司 | 36Kr | 行业动态 |")
    report.append("")
    report.append("**推荐订阅**：")
    report.append("- DataEye（达扑海）- 需付费")
    report.append("- 蝉妈妈 - 需付费")
    report.append("- 飞瓜数据 - 需付费")
    report.append("")
    
    # 5. 制作公司/专访
    report.append("## 🎬 制作公司与专访")
    report.append("")
    # 搜索常见AI漫剧制作方
    companies = ['即梦', 'Seedance', 'Runway', 'Pika', 'Luma', '快手', '字节']
    report.append("**热门制作方观察：**")
    for c in companies[:5]:
        report.append(f"- {c}")
    report.append("")
    report.append("*注：详细专访信息需人工搜索特定公司名称*")
    report.append("")
    
    report.append("---")
    report.append(f"报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    return "\n".join(report)


if __name__ == "__main__":
    report = generate_report()
    print(report)
    
    # 保存到文件供 cron 调用
    output_file = "/Users/hongliang/.openclaw/workspace/memory/ai_manju_daily.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n报告已保存到: {output_file}")
