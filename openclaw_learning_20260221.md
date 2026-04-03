# OpenClaw 每日学习 2026-02-21 09:00

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
- [OpenClaw 🦞](qmd://openclaw-docs/index.md) - Score: 0.31
- [Pi Integration Architecture](qmd://openclaw-docs/pi.md) - Score: 0.51

### 搜索 'skill install' 相关：
- [ClawHub CLI](qmd://openclaw-skills/clawhub/skill.md) - Score: 1
- [blogwatcher](qmd://openclaw-skills/blogwatcher/skill.md) - Score: 1
- [Whisper (CLI)](qmd://openclaw-skills/openai-whisper/skill.md) - Score: 1

## 📖 精选技能文档预览

### skill
文件: qmd://openclaw-skills/weather/skill.md

---
name: weather
description: Get current weather and forecasts (no API key required).
homepage: https://wttr.in/:help
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "bins": ["curl"] } } }
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
   errno: -2,
    code: "ENOENT"


Bun v1.3.8 (macOS arm64)

## 🎯 今日学习要点

- [ ] 待补充：今天学到的关键点

