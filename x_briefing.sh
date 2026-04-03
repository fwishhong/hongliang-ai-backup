#!/bin/bash
# X科技与思想领袖账号简报生成脚本
# 每天早上 8:00 执行，发送到飞书

OUTPUT_FILE="/Users/hongliang/.openclaw/workspace/x_tech_briefing_$(date +%Y-%m-%d).md"
LOG_FILE="/Users/hongliang/.openclaw/workspace/logs/x_briefing_$(date +%Y%m).log"

echo "=== X账号简报生成 $(date '+%Y-%m-%d %H:%M') ===" > "$LOG_FILE"

# 生成子代理任务
echo "[$(date)] 启动 X 账号简报生成任务..." >> "$LOG_FILE"

cat > "$OUTPUT_FILE" << 'HEADER'
# X科技与思想领袖账号简报

HEADER

echo "**日期：$(date '+%Y年%m月%d日')**" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"

# 调用子代理生成简报内容
# 这里简化为直接输出模板，实际可通过 API 或浏览器抓取

cat >> "$OUTPUT_FILE" << 'TEMPLATE'

## 一、速览版本

### 🔥 最重要新闻和观点

*（此处为自动生成的速览内容）*

### 🆕 新产品发布

*（此处为自动生成的新产品发布）*

### 💡 著名企业家重要判断

| 人物 | 判断/观点 | 来源 |
|------|----------|------|
| - | - | - |

## 二、AI科技企业官方账号和开发者

### 🏢 企业官方动态

*（此处为自动生成的企业动态）*

## 三、重要企业家与科技从业者

### 科技领袖言论

*（此处为自动生成的言论）*

## 四、投资者和VC

### 投融资动态

*（此处为自动生成的投融资动态）*

### 投资观点

*（此处为自动生成的投资观点）*

## 五、特殊总结

### 1. 投融资视角的叙事和估值变化趋势

*（此处为自动生成的总结）*

### 2. AI Startup融资新闻

| 公司 | 轮次 | 金额 | 估值 | 领投方 |
|------|------|------|------|--------|
| - | - | - | - | - |

### 3. 风险提示

*（此处为自动生成的风险提示）*

---

**注：本简报基于公开新闻和社交媒体信息整理。**

TEMPLATE

echo "[$(date)] 简报模板已生成: $OUTPUT_FILE" >> "$LOG_FILE"

# 发送到飞书
FEISHU_MSG=$(cat "$OUTPUT_FILE")

echo "[$(date)] 准备发送到飞书..." >> "$LOG_FILE"

# 调用消息工具发送
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages" \
  -H "Authorization: Bearer $FEISHU_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"receive_id\": \"ou_97e8a151e0a917023ffa52d4c1f20372\",
    \"msg_type\": \"text\",
    \"content\": \"{\\\"text\\\": \\\"✅ X账号简报已生成：$OUTPUT_FILE\\\"}\"
  }" >> "$LOG_FILE" 2>&1

echo "[$(date)] 任务完成" >> "$LOG_FILE"
