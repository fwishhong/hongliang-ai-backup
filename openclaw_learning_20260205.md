# OpenClaw 每日学习 2026-02-05 11:50

## 📚 文档更新检查

### 最近更新的文档：
- vps.md
- tui.md
- tts.md
- token-use.md
- testing.md
- scripts.md
- prose.md
- plugin.md
- perplexity.md
- network.md

### Skills 目录变化：
1password
apple-notes
apple-reminders
bear-notes
bird
blogwatcher
blucli
bluebubbles
camsnap
canvas
clawdhub
coding-agent
discord
eightctl
food-order
gemini
gifgrep
github
gog
goplaces
himalaya
imsg
local-places
mcporter
model-usage
nano-banana-pro
nano-pdf
notion
obsidian
openai-image-gen
openai-whisper
openai-whisper-api
openhue
oracle
ordercli
peekaboo
sag
session-logs
sherpa-onnx-tts
skill-creator
slack
songsee
sonoscli
spotify-player
summarize
things-mac
tmux
trello
video-frames
voice-call
wacli
weather

## 🔍 QMD 搜索结果

### 搜索 'memory' 相关：
- [Hooks](qmd://openclaw-docs/hooks.md) - Score: 0.2
- [Plugins (Extensions)](qmd://openclaw-docs/plugin.md) - Score: 0.21
- [Multi-Agent Sandbox & Tools Configuration](qmd://openclaw-docs/multi-agent-sandbox-tools.md) - Score: 0.25

### 搜索 'skill' 相关：
- [ClawdHub CLI](qmd://openclaw-skills/clawdhub/skill.md) - Score: 1
- [blogwatcher](qmd://openclaw-skills/blogwatcher/skill.md) - Score: 1
- [Whisper (CLI)](qmd://openclaw-skills/openai-whisper/skill.md) - Score: 1

## 📖 精选技能文档预览

### skill
文件: qmd://openclaw-skills/weather/skill.md

---
name: weather
description: Get current weather and forecasts (no API key required).
homepage: https://wttr.in/:help
metadata: {"openclaw":{"emoji":"🌤️","requires":{"bins":["curl"]}}}
---

# Weather

Two free services, no API keys needed.

## wttr.in (primary)

Quick one-liner:
```bash
curl -s "wttr.in/London?format=3"
# Output: London: ⛅️ +8°C
```

Compact format:
```bash
curl -s "wttr.in/London?format=%l:+%c+%t+%h+%w"
# Output: London: ⛅️ +8°C 71% ↙5km/h
```

Full forecast:
```bash
curl -s "wttr.in/London?T"
```

Format codes: `%c` condition · `%t` temp · `%h` humidity · `%w` wind · `%l` location · `%m` moon

Tips:
- URL-encode spaces: `wttr.in/New+York`
- Airport codes: `wttr.in/JFK`
- Units: `?m` (metric) `?u` (USCS)
- Today only: `?1` · Current only: `?0`
- PNG: `curl -s "wttr.in/Berlin.png" -o /tmp/weather.png`

## Open-Meteo (fallback, JSON)

Free, no key, good for programmatic use:
```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=51.5&longitude=-0.12&current_weather=true"
```

Find coordinates for a city, then query. Returns JSON with temp, windspeed, weathercode.

Docs: https://open-meteo.com/en/docs


## 🔧 索引维护

### 更新索引...
Indexed: 0 new, 0 updated, 52 unchanged, 0 removed

✓ All collections updated.

Run 'qmd embed' to update embeddings (72 unique hashes need vectors)

## 🎯 今日学习要点

- [x] **qmd 技能已安装并配置** ✓
- [x] **每日学习脚本集成 qmd** ✓
- [x] **快捷搜索命令已创建** ✓
- [x] **YouTube Summarizer 解决方案已记录** (2026-02-05)
  - MCP 服务器位置：`~/clawd/mcp-server-youtube-transcript`（不是 /root/clawd）
  - Skill 文档有误，需要修正
  - 已添加 youtube-skill 集合到 qmd

**后续可用命令：**
- `bash scripts/qsearch.sh "关键词" [collection]` - 搜索文档/技能
  - collection: openclaw-docs, openclaw-skills, youtube-skill
- `bash scripts/openclaw_daily_learning.sh` - 每日学习（自动）

