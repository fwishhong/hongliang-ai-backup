# OpenClaw 每日学习 2026-02-22 09:00

## 📚 文档更新检查

### 最近更新的文档：
- vps.md
- tts.md
- prose.md
- pi.md
- pi-dev.md
- perplexity.md
- network.md
- logging.md
- index.md
- date-time.md

### Skills 目录变化：
1password
apple-notes
apple-reminders
bear-notes
blogwatcher
blucli
bluebubbles
camsnap
canvas
clawhub
coding-agent
discord
eightctl
food-order
gemini
gh-issues
gifgrep
github
gog
goplaces
healthcheck
himalaya
imsg
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
- [OpenClaw 🦞](qmd://openclaw-docs/index.md) - Score: 0.29
- [Pi Integration Architecture](qmd://openclaw-docs/pi.md) - Score: 0.49

### 搜索 'skill install' 相关：
- [ClawHub CLI](qmd://openclaw-skills/clawhub/skill.md) - Score: 1
- [blogwatcher](qmd://openclaw-skills/blogwatcher/skill.md) - Score: 1
- [Whisper (CLI)](qmd://openclaw-skills/openai-whisper/skill.md) - Score: 1

## 📖 精选技能文档预览

### skill
文件: qmd://openclaw-skills/weather/skill.md

---
name: weather
description: "Get current weather and forecasts via wttr.in or Open-Meteo. Use when: user asks about weather, temperature, or forecasts for any location. NOT for: historical weather data, severe weather alerts, or detailed meteorological analysis. No API key needed."
homepage: https://wttr.in/:help
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["curl"] } } }
---

# Weather Skill

Get current weather conditions and forecasts.

## When to Use

✅ **USE this skill when:**

- "What's the weather?"
- "Will it rain today/tomorrow?"
- "Temperature in [city]"
- "Weather forecast for the week"
- Travel planning weather checks

## When NOT to Use

❌ **DON'T use this skill when:**

- Historical weather data → use weather archives/APIs
- Climate analysis or trends → use specialized data sources
- Hyper-local microclimate data → use local sensors
- Severe weather alerts → check official NWS sources
- Aviation/marine weather → use specialized services (METAR, etc.)

## Location

Always include a city, region, or airport code in weather queries.

## Commands

### Current Weather

```bash
# One-line summary
curl "wttr.in/London?format=3"

# Detailed current conditions
curl "wttr.in/London?0"

# Specific city
curl "wttr.in/New+York?format=3"
```

### Forecasts

```bash
# 3-day forecast
curl "wttr.in/London"

# Week forecast
curl "wttr.in/London?format=v2"

# Specific day (0=today, 1=tomorrow, 2=day after)
curl "wttr.in/London?1"
```

### Format Options

```bash
# One-liner
curl "wttr.in/London?format=%l:+%c+%t+%w"

# JSON output
curl "wttr.in/London?format=j1"

# PNG image
curl "wttr.in/London.png"
```

### Format Codes

- `%c` — Weather condition emoji
- `%t` — Temperature

## 🔧 索引维护

### 更新索引...
   errno: -2,
    code: "ENOENT"


Bun v1.3.8 (macOS arm64)

## 🎯 今日学习要点

- [ ] 待补充：今天学到的关键点

