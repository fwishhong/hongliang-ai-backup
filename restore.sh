#!/bin/bash
# OpenClaw Workspace Restore Script
# 从 GitHub 恢复到本地

set -e

WORKSPACE_DIR="$HOME/.openclaw/workspace"
DATE=$(date "+%Y-%m-%d %H:%M:%S")

echo "⚠️  开始恢复 Workspace..."
echo "📂 目标目录: $WORKSPACE_DIR"
echo ""

# 确认
read -p "⚠️  这会覆盖本地所有文件！确认继续？(y/n): " confirm
if [ "$confirm" != "y" ]; then
    echo "❌ 已取消"
    exit 0
fi

cd "$WORKSPACE_DIR"

# 备份当前版本（以防万一）
if [ -d ".git" ]; then
    echo "📦 备份当前版本到 backup-before-restore-$DATE..."
    mkdir -p "$HOME/.openclaw/workspace-backup-$DATE"
    cp -r . "$HOME/.openclaw/workspace-backup-$DATE/" 2>/dev/null || true
fi

# 从 GitHub 拉取
echo "📥 从 GitHub 拉取最新版本..."
git fetch origin
git reset --hard origin/main 2>/dev/null || git reset --hard origin/master

echo "✅ 恢复完成！"
echo ""
echo "💡 下一步："
echo "   1. 重启 OpenClaw Gateway"
echo "   2. 检查 skills 是否正常"
