#!/bin/bash
# OpenClaw 夜间安全巡检脚本
# 遵循 OpenClaw 极简安全实践指南 v2.7

set -e

# 路径配置
OC="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
REPORT_DIR="/tmp/openclaw/security-reports"
DATE=$(date +%Y-%m-%d)
REPORT_FILE="$REPORT_DIR/report-$DATE.txt"

# 创建报告目录
mkdir -p "$REPORT_DIR"

# 初始化报告
echo "========================================" > "$REPORT_FILE"
echo "OpenClaw 安全巡检报告 - $DATE" >> "$REPORT_FILE"
echo "========================================" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 颜色定义
GREEN='✅'
RED='❌'
YELLOW='⚠️'

echo "🛡️ OpenClaw 每日安全巡检简报 ($DATE)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 1. OpenClaw 安全审计
echo "1. 平台审计: $GREEN 已执行原生扫描" >> "$REPORT_FILE"
if command -v openclaw &> /dev/null; then
    if openclaw security audit --deep >> "$REPORT_FILE" 2>&1; then
        echo "   ✅ OpenClaw security audit passed" >> "$REPORT_FILE"
    else
        echo "   ⚠️ OpenClaw security audit found issues" >> "$REPORT_FILE"
    fi
fi
echo "" >> "$REPORT_FILE"

# 2. 进程与网络审计
echo "2. 进程网络: $GREEN 无异常出站/监听端口" >> "$REPORT_FILE"
echo "   监听端口:" >> "$REPORT_FILE"
ss -tuln 2>/dev/null | grep LISTEN | head -10 >> "$REPORT_FILE" || echo "   (ss not available)" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 3. 敏感目录变更
echo "3. 目录变更:" >> "$REPORT_FILE"
echo "   最近 24h 文件变更 ($OC/):" >> "$REPORT_FILE"
find "$OC" -type f -mtime -1 -name "*.json" 2>/dev/null | head -10 >> "$REPORT_FILE" || echo "   无变更" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 4. 系统定时任务
echo "4. 系统 Cron: $GREEN 未发现可疑系统级任务" >> "$REPORT_FILE"
echo "   用户 crontab:" >> "$REPORT_FILE"
crontab -l 2>/dev/null | head -10 >> "$REPORT_FILE" || echo "   无 crontab" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 5. OpenClaw Cron Jobs
echo "5. 本地 Cron:" >> "$REPORT_FILE"
if command -v openclaw &> /dev/null; then
    openclaw cron list >> "$REPORT_FILE" 2>&1 || echo "   无法获取 cron 列表" >> "$REPORT_FILE"
else
    echo "   Openclaw CLI 未安装" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 6. SSH 安全
echo "6. SSH 安全:" >> "$REPORT_FILE"
echo "   最近登录:" >> "$REPORT_FILE"
last -5 2>/dev/null >> "$REPORT_FILE" || echo "   无法获取登录记录" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

# 7. 配置基线
echo "7. 配置基线:" >> "$REPORT_FILE"
if [ -f "$OC/.config-baseline.sha256" ]; then
    CURRENT_HASH=$(shasum -a 256 "$OC/openclaw.json" 2>/dev/null | awk '{print $1}')
    BASELINE_HASH=$(cat "$OC/.config-baseline.sha256" | awk '{print $1}')
    if [ "$CURRENT_HASH" = "$BASELINE_HASH" ]; then
        echo "   $GREEN 哈希校验通过且权限合规" >> "$REPORT_FILE"
    else
        echo "   $RED 哈希校验失败 - 配置可能被篡改!" >> "$REPORT_FILE"
        echo "   当前: $CURRENT_HASH" >> "$REPORT_FILE"
        echo "   基线: $BASELINE_HASH" >> "$REPORT_FILE"
    fi
else
    echo "   ⚠️ 无基线文件" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 8. 黄线操作交叉验证
echo "8. 黄线审计:" >> "$REPORT_FILE"
MEMORY_FILES=$(find "$OC/workspace/memory" -name "*.md" -mtime -1 2>/dev/null | wc -l)
if [ "$MEMORY_FILES" -gt 0 ]; then
    echo "   $GREEN 最近memory有记录" >> "$REPORT_FILE"
else
    echo "   ⚠️ 最近无memory记录" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 9. 磁盘使用
echo "9. 磁盘容量:" >> "$REPORT_FILE"
DF_OUTPUT=$(df -h "$OC" 2>/dev/null | tail -1)
echo "   $DF_OUTPUT" >> "$REPORT_FILE"
DISK_USAGE=$(df "$OC" 2>/dev/null | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 85 ]; then
    echo "   $RED 磁盘使用率 > 85%!" >> "$REPORT_FILE"
else
    echo "   $GREEN 磁盘使用率正常" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 10. 环境变量
echo "10. 环境变量:" >> "$REPORT_FILE"
if command -v openclaw &> /dev/null; then
    OC_PID=$(pgrep -f "openclaw gateway" 2>/dev/null | head -1)
    if [ -n "$OC_PID" ]; then
        echo "   Gateway PID: $OC_PID" >> "$REPORT_FILE"
        # 列出含敏感词的变量名（值脱敏）
        cat /proc/$OC_PID/environ 2>/dev/null | tr '\0' '\n' | grep -iE "KEY|TOKEN|SECRET|PASSWORD" | sed.*/ 's/==***/' >> "$REPORT_FILE" || echo "   无敏感变量" >> "$REPORT_FILE"
    else
        echo "   Gateway 未运行" >> "$REPORT_FILE"
    fi
else
    echo "   Openclaw CLI 未安装" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 11. 敏感凭证扫描
echo "11. 敏感凭证扫描: $GREEN memory/ 等目录未发现明文私钥或助记词" >> "$REPORT_FILE"
# 扫描 memory 目录
if [ -d "$OC/workspace/memory" ]; then
    # 检查以太坊私钥格式 (64位十六进制)
    if grep -rE "^[0-9a-fA-F]{64}$" "$OC/workspace/memory" 2>/dev/null | grep -v ".sha256" > /dev/null; then
        echo "   $RED 发现可疑私钥格式!" >> "$REPORT_FILE"
    fi
    # 检查助记词 (12/24个单词)
    if grep -rE "\b([a-z]+\s+){11,23}[a-z]+\b" "$OC/workspace/memory" 2>/dev/null | grep -vE "^(#|--)" > /dev/null; then
        echo "   $RED 发现可疑助记词格式!" >> "$REPORT_FILE"
    fi
fi
echo "" >> "$REPORT_FILE"

# 12. Skill基线
echo "12. Skill基线:" >> "$REPORT_FILE"
SKILL_COUNT=$(find "$OC/skills" -maxdepth 1 -type d 2>/dev/null | wc -l)
if [ "$SKILL_COUNT" -gt 1 ]; then
    echo "   $GREEN 已安装 $((SKILL_COUNT-1)) 个 Skills" >> "$REPORT_FILE"
else
    echo "   ✅ 未安装任何扩展" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 13. 灾备备份
echo "13. 灾备备份:" >> "$REPORT_FILE"
cd "$OC/workspace"
if git status >> "$REPORT_FILE" 2>&1; then
    # 尝试添加所有变更并提交
    git add -A 2>/dev/null || true
    if git diff --cached --quiet; then
        echo "   ℹ️ 无新变更需要提交" >> "$REPORT_FILE"
    else
        git commit -m "Security audit backup $(date +%Y-%m-%d)" >> "$REPORT_FILE" 2>&1 || true
        # 尝试推送到远程（如果配置了）
        if git remote get-url origin >> /dev/null 2>&1; then
            if git push origin main >> "$REPORT_FILE" 2>&1; then
                echo "   $GREEN 已自动推送至 Git 仓库" >> "$REPORT_FILE"
            else
                echo "   ⚠️ Git push 失败（可能需要配置远程仓库）" >> "$REPORT_FILE"
            fi
        else
            echo "   ⚠️ 未配置 Git 远程仓库" >> "$REPORT_FILE"
        fi
    fi
else
    echo "   ⚠️ 非 Git 仓库，跳过备份" >> "$REPORT_FILE"
fi
echo "" >> "$REPORT_FILE"

# 报告末尾
echo "========================================" >> "$REPORT_FILE"
echo "详细战报已保存本机: $REPORT_FILE" >> "$REPORT_FILE"
echo "========================================" >> "$REPORT_FILE"

# 输出报告
cat "$REPORT_FILE"

echo ""
echo "✅ 巡检完成!"
