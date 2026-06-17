#!/bin/bash
# AI 记忆自动备份脚本
# 每天自动备份到 GitHub

BACKUP_REPO="/tmp/hongliang-ai-backup"
SOURCE_DIR="$HOME/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)

# 需要备份的文件/目录
BACKUP_FILES=(
    "memory/"
    "MEMORY.md"
    "SESSION-STATE.md"
    "SOUL.md"
    "USER.md"
    "IDENTITY.md"
    "AGENTS.md"
    "scripts/"
    ".openclaw/"
)

echo "=== AI 记忆备份 $DATE ==="

# 进入备份仓库
cd "$BACKUP_REPO" || exit 1

# 复制文件（排除敏感文件和大目录）
for item in "${BACKUP_FILES[@]}"; do
    if [ -e "$SOURCE_DIR/$item" ]; then
        # 排除 .git、日志、凭证、node_modules、skills
        rsync -av \
            --exclude='.git' \
            --exclude='*.log' \
            --exclude='*.err' \
            --exclude='credentials.json' \
            --exclude='*.key' \
            --exclude='node_modules' \
            --exclude='skills' \
            "$SOURCE_DIR/$item" "./" 2>/dev/null || true
    fi
done

# 检查是否有变化（空仓库没有commit时跳过）
if git rev-parse HEAD >/dev/null 2>&1 && git diff --quiet 2>/dev/null; then
    echo "没有变化，无需提交"
    exit 0
fi

# 配置 git
git config user.name "hongliang-ai"
git config user.email "ai@hongliang.local"

# 添加所有文件
git add -A

# 提交
git commit -m "backup: $DATE AI memory update" 2>/dev/null || echo "没有需要提交的内容"

# 推送
git push origin main 2>&1 || echo "推送失败"

echo "=== 备份完成 ==="
