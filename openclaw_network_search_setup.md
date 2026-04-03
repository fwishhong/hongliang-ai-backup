# OpenClaw 联网搜索增强方案

> 从中级到高级的第一步：把联网搜索做到极致

## 方案概述

本方案针对云上 OpenClaw（在不方便文件互传的情况下）的最佳搭配：

1. **联网搜索**: Tavily + Multi Search Engine v2.0.1
2. **难啃链接解析**: x-reader + Agent Reach
3. **浏览器自动化**: BrowserWing
4. **Gemini 增强**: ModSearch + Gemini Deep Research
5. **主动找 Skills**: find-skills + Clawhub
6. **被动信息源**: ClawFeed
7. **免费模型兜底**: Free Ride

---

## 一键安装命令

```bash
# ========== 0. 安装 clawhub ==========
npm install -g clawhub

# ========== 1. 联网搜索（必须）==========

# Tavily - 每月1000次免费，专门给Agent用的搜索API
clawhub install tavily-search

# Multi Search Engine - 集成17个搜索引擎（8中文+9全球）
cd ~/.openclaw/workspace/skills
git clone https://github.com/sanjay3290/ai-skills

# ========== 2. 难啃链接解析 ==========

# x-reader - 覆盖 yt，某站，X，公众号，tg，rss，播客，某书
# ⚠️ 需要 Docker
cd ~/.openclaw/workspace/skills
git clone https://github.com/runesleo/x-readerwe

# Agent Reach - 在x-reader基础上多了某抖，Reddit，Github
# ⚠️ 需要 Docker，优先用Cookie登录（建议用小号）
cd ~/.openclaw/workspace/skills
git clone https://github.com/Panniantong/Agent-Reach

# ========== 3. 浏览器自动化 ==========

# BrowserWing - 记录浏览器操作做成Skills，精确重放
cd ~/.openclaw/workspace/skills
git clone https://github.com/browserwing/browserwing

# ========== 4. Gemini 增强（需要Gemini账号）==========

# ModSearch - Gemini CLI 联网搜索
cd ~/.openclaw/workspace/skills
git clone https://github.com/liustack/modsearch

# Gemini Deep Research - Gemini 3.1 Pro 驱动
# 需自行查找安装

# ========== 5. 主动找 Skills ==========

# find-skills - 遇到问题主动找合适的Skills
clawhub install find-skills

# Clawhub - Skills 市场
npm install -g clawhub

# ========== 6. 被动信息源 ==========

# ClawFeed - 订阅 X，RSS，HackerNews，Reddit，GitHub Trending
# 4小时更新一次
cd ~/.openclaw/workspace/skills
git clone https://github.com/kevinho/clawfeed

# ========== 7. 免费模型兜底 ==========

# Free Ride - OpenRouter 免费模型自动选择
# ⚠️ 当前 rate limit，等会再试
# 方案1: clawhub install freeride-ai
# 方案2: 
cd ~/.openclaw/workspace/skills
git clone https://github.com/Shaivpidedi/Free-Ride

# ========== 8. 配置 OpenRouter 免费 Provider ==========
# 在 OpenClaw 配置中添加 free-openrouter provider
```

---

## 详细说明

### Tavily
- **免费额度**: 每月 1000 次
- **特点**: 专门给 Agent 做的搜索 API，返回内容已处理
- **获取 API Key**: https://tavily.com
- **环境变量**: `TAVILY_API_KEY`

### Multi Search Engine
- **集成**: 17 个搜索引擎（8个中文 + 9个全球）
- **优点**: 不需要 API，直接安装

### x-reader / Agent Reach
- **需要**: Docker 虚拟机
- **用途**: 模拟操作解析难啃的链接
- **安全建议**: 用小号登录

### BrowserWing
- **功能**: 记录浏览器操作做成 Skills
- **用途**: 点击确定、滑动页面等自动化

### ModSearch
- **需要**: Gemini 账号
- **优点**: Google 信息搜索本来就很强，不是反代

### ClawFeed
- **更新频率**: 4 小时
- **订阅源**: X, RSS, HackerNews, Reddit, GitHub Trending

### Free Ride
- **功能**: 调用 OpenRouter 免费模型
- **优点**: 自动按质量排名，不用担心额度

---

## 当前已安装状态

| Skill | 状态 | 位置 |
|-------|------|------|
| tavily-search | ✅ | ~/.openclaw/workspace/skills/tavily-search |
| ai-skills (Multi Search) | ✅ | ~/.openclaw/workspace/skills/ai-skills |
| find-skills | ✅ | ~/.openclaw/workspace/skills/find-skills |
| Agent-Reach | ✅ | ~/.openclaw/workspace/skills/Agent-Reach |
| ClawFeed | ✅ | ~/.openclaw/workspace/skills/clawfeed |
| BrowserWing | ✅ | ~/.openclaw/workspace/skills/browserwing |
| ModSearch | ✅ | ~/.openclaw/workspace/skills/modsearch |
| x-reader | ❌ | 克隆失败（需要认证） |
| Free Ride | ❌ | 克隆失败 / rate limit |

---

## 注意事项

1. **x-reader 和 Agent Reach** 需要 Docker 支持
2. **ModSearch 和 Gemini Deep Research** 需要 Gemini 账号
3. **Tavily** 需要申请 API Key
4. **Free Ride** 当前 rate limit，需要稍后重试
