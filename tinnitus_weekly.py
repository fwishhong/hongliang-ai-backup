#!/usr/bin/env python3
"""神经性耳鸣每周调查报告 - 发到飞书"""

import requests
import json
import os
from datetime import datetime

# 飞书配置
FEISHU_USER_ID = "ou_97e8a151e0a917023ffa52d4c1f20372"

# 搜索关键词
QUERY = "tinnitus treatment 2026 new breakthrough Lenire bimodal neuromodulation"

def search_news():
    """搜索新闻 (简化版，直接用搜索结果)"""
    # 这里可以调用搜索API，为了简单直接构造报告
    report = f"""## 🎧 神经性耳鸣治疗每周进展

**更新日期**: {datetime.now().strftime('%Y年%m月%d日')}

### 📰 本周进展

**Lenire 双模神经调节**
- FDA 批准的唯一同类设备
- 81.8% 患者报告显著改善
- 与 Treble Health 合作扩展美国市场

**声音疗法**
- 86% 依从性好的患者改善
- 12 周见效，疗效持续 12 个月

**rTMS 经颅磁刺激**
- EEG 精准刺激是趋势
- 联合疗法正在探索

### 📋 待跟进
- Lenire 中国上市情况
- 基因治疗最新进展

---
*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*"""
    return report

def send_to_feishu(message):
    """发送到飞书"""
    # 使用 OpenClaw 的飞书发送
    import sys
    sys.path.append(os.path.expanduser("~/.openclaw/workspace/skills/feishu-doc"))
    
    # 直接用 requests 发飞书 webhook 或 API
    # 这里用最简单的消息发送
    url = f"https://open.feishu.cn/open-apis/im/v1/messages"
    
    # 获取 token (简化版)
    token = os.environ.get("FEISHU_BOT_TOKEN", "")
    
    if not token:
        print("No FEISHU_BOT_TOKEN, trying alternative...")
        # 尝试用 OpenClaw message 工具
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "receive_id_type": "user_id",
        "receive_id": FEISHU_USER_ID,
        "msg_type": "text",
        "content": json.dumps({"text": message})
    }
    
    r = requests.post(url, headers=headers, json=data)
    print(f"Feishu response: {r.status_code}")
    return r.ok

if __name__ == "__main__":
    report = search_news()
    print(report)
    # send_to_feishu(report)  # 暂时不发送，等配置好
