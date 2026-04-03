#!/bin/bash
# Quick qmd search for OpenClaw docs/skills
# 用法: ./qsearch.sh "关键词" [collection]

export PATH="$HOME/.bun/bin:$PATH"
QMD_PATH="$HOME/.bun/bin/qmd"

if [ -z "$1" ]; then
    echo "用法: $0 <搜索词> [collection]"
    echo ""
    echo "Collections:"
    echo "  openclaw-docs   - OpenClaw 官方文档 (20 docs)"
    echo "  openclaw-skills - OpenClaw Skills (53 skills)"
    echo "  youtube-skill  - YouTube 摘要技能 (3 docs)"
    echo "  remotion-skills - Remotion 视频制作 (34 docs)"
    echo ""
    echo "示例:"
    echo "  $0 \"memory\""
    echo "  $0 \"animation\" remotion-skills"
    exit 1
fi

COLLECTION="${2:-openclaw-docs}"

echo "🔍 搜索: \"$1\" in $COLLECTION"
echo "---"
$QMD_PATH search "$1" -c "$COLLECTION" -n 5 --json 2>/dev/null | jq -r '.[] | "- [\(.title)](\(.file)) (Score: \(.score))"' 2>/dev/null || echo "搜索失败或无结果"
