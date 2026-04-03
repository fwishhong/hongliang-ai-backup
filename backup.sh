#!/bin/bash
# OpenClaw Workspace Backup Script
# 自动备份到 GitHub

set -e

WORKSPACE_DIR="$HOME/.openclaw/workspace"
BACKUP_SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATE=$(date "+%Y-%m-%d %H:%M:%S")

echo "🕐 开始备份... $DATE"

cd "$WORKSPACE_DIR"

# 检查是否有 .git 目录
if [ ! -d ".git" ]; then
    echo "❌ 不是 Git 仓库，请先初始化"
    exit 1
fi

# 添加所有文件
git add -A

# 检查是否有变化
if git diff --staged --quiet; then
    echo "✅ 没有变化，跳过提交"
else
    # 提交
    git commit -m "Backup: $DATE"
    
    # 推送到 GitHub
    echo "📤 推送到 GitHub..."
    git push -u origin main 2>/dev/null || git push -u origin master 2>/dev/null
    
    echo "✅ 备份完成！"
fi
