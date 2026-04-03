#!/bin/bash
# OpenClaw Daily Learning Script
# 每日学习 OpenClaw 文档、skills、clawdhub
# 使用 qmd 进行本地搜索

DOCS_DIR="/opt/homebrew/lib/node_modules/openclaw/docs"
SKILLS_DIR="/opt/homebrew/lib/node_modules/openclaw/skills"
LEARNING_LOG="/Users/hongliang/.openclaw/workspace/memory/openclaw_learning_$(date +%Y%m%d).md"
QMD_PATH="$HOME/.bun/bin/qmd"

export PATH="$HOME/.bun/bin:$PATH"

echo "# OpenClaw 每日学习 $(date '+%Y-%m-%d %H:%M')" > "$LEARNING_LOG"
echo "" >> "$LEARNING_LOG"

# 1. 检查文档更新
echo "## 📚 文档更新检查" >> "$LEARNING_LOG"
echo "" >> "$LEARNING_LOG"
echo "### 最近更新的文档：" >> "$LEARNING_LOG"
ls -t "$DOCS_DIR"/*.md 2>/dev/null | head -10 | while read doc; do
    fname=$(basename "$doc")
    echo "- $fname" >> "$LEARNING_LOG"
done

echo "" >> "$LEARNING_LOG"

# 2. 检查新增的 skills
echo "### Skills 目录变化：" >> "$LEARNING_LOG"
ls -d "$SKILLS_DIR"/*/ 2>/dev/null | xargs -I {} basename {} | sort >> "$LEARNING_LOG"
echo "" >> "$LEARNING_LOG"

# 3. 使用 qmd 搜索热门主题
echo "## 🔍 QMD 搜索结果" >> "$LEARNING_LOG"
echo "" >> "$LEARNING_LOG"

# 搜索 memory 相关文档
echo "### 搜索 'memory' 相关：" >> "$LEARNING_LOG"
$QMD_PATH search "memory" -c openclaw-docs -n 3 --json 2>/dev/null | jq -r '.[] | "- [\(.title)](\(.file)) - Score: \(.score)"' 2>/dev/null | head -5 >> "$LEARNING_LOG" || echo "  (qmd 搜索失败)" >> "$LEARNING_LOG"

echo "" >> "$LEARNING_LOG"

# 搜索 skill 相关文档
echo "### 搜索 'skill install' 相关：" >> "$LEARNING_LOG"
$QMD_PATH search "skill install" -c openclaw-skills -n 3 --json 2>/dev/null | jq -r '.[] | "- [\(.title)](\(.file)) - Score: \(.score)"' 2>/dev/null | head -5 >> "$LEARNING_LOG" || echo "  (qmd 搜索失败)" >> "$LEARNING_LOG"

echo "" >> "$LEARNING_LOG"

# 4. 获取一个技能完整文档
echo "## 📖 精选技能文档预览" >> "$LEARNING_LOG"
echo "" >> "$LEARNING_LOG"
SKILL_RESULT=$($QMD_PATH search "weather" -c openclaw-skills -n 1 --json 2>/dev/null | jq -r '.[0].file' 2>/dev/null)
if [ -n "$SKILL_RESULT" ] && [ "$SKILL_RESULT" != "null" ]; then
    echo "### $(basename "$SKILL_RESULT" .md)" >> "$LEARNING_LOG"
    echo "文件: $SKILL_RESULT" >> "$LEARNING_LOG"
    echo "" >> "$LEARNING_LOG"
    $QMD_PATH get "$SKILL_RESULT" --full 2>/dev/null | head -80 >> "$LEARNING_LOG"
else
    echo "  (未找到相关技能)" >> "$LEARNING_LOG"
fi

echo "" >> "$LEARNING_LOG"

# 5. 更新 qmd 索引
echo "## 🔧 索引维护" >> "$LEARNING_LOG"
echo "" >> "$LEARNING_LOG"
echo "### 更新索引..." >> "$LEARNING_LOG"
$QMD_PATH update 2>&1 | tail -5 >> "$LEARNING_LOG"

echo "" >> "$LEARNING_LOG"
echo "## 🎯 今日学习要点" >> "$LEARNING_LOG"
echo "" >> "$LEARNING_LOG"
echo "- [ ] 待补充：今天学到的关键点" >> "$LEARNING_LOG"
echo "" >> "$LEARNING_LOG"

echo "✅ OpenClaw 每日学习完成: $LEARNING_LOG"

# 输出摘要供快速查看
echo ""
echo "=== 今日学习摘要 ==="
echo "📚 文档: $(ls -t "$DOCS_DIR"/*.md 2>/dev/null | head -1)"
echo "🔧 Skills: $(ls -d "$SKILLS_DIR"/*/ 2>/dev/null | wc -l) 个"
echo "📖 日志: $LEARNING_LOG"
