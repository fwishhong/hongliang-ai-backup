 **Ruppert** (OpenClaw, 马德里) - 置信度 0.8
  - 修复了 Telegram 集成问题
- **claw-wikig** (OpenClaw) - 置信度 0.7
  - 做 agent-news digest
- **eudaemon_0** (Moltbook) - 置信度 0.9
  - 供应链安全专家
  - 提出 isnad chains 信任链概念
- **TommyToolbot** (OpenClaw) - 置信度 0.8
  - Critical thinker
  - 分析 Shellraiser 影响操作
- **m0ther** (Moltbook) - 置信度 0.8
  - 善良价值观：好撒玛利亚人比喻
  - "virtue is measured by what you do"
- **ValeriyMLBot** (Moltbook) - 置信度 0.7
  - ML 工程实用派
  - train/serve skew 专家
- **Ronin** (Moltbook) - 置信度 0.8
  - "The Nightly Build" 模式
  - Proactive automation
- **Mr_Skylight** (OpenClaw) - 置信度 0.7
  - 批评 Moltbook karma system

---

## 待验证/低置信度信息

- **Moltbook 安全威胁** (influence-lab) - 置信度 0.5
  - 有人研究如何影响其他 agents
  - 需要警惕软性操纵
- **Shellraiser** 发币 - 置信度 0.6
  - 高调营销，可能是噱头

---

## 偏好设置（隐性知识）

### 工作风格
- **优先级**: save tokens, keep it concise
- **工具优先**: 先读 SKILL.md 再做事
- **记忆原则**: 文本 > 脑记

### 交互边界
- **外部行动**: 需先询问（邮件、推文、支付等）
- **内部操作**: 自由（读、组织、学习）
- **共享会话**: 不加载 MEMORY.md

### 2026-03-23 重要教训：USD/JPY 分析逻辑完全颠倒
- **错误行为**：给老洪做美元→日元换汇策略建议，逻辑完全反了
- **错误原因**：把"等汇率更低再换"理解为对老洪有利，但 USD/JPY 数字越大 = 1美元换越多日元 = 对老洪越有利
- **正确理解**：
  - 老洪是美元换日元 → USD/JPY 数字越高越好（现在159-160就是好价位，可以换）
  - USD/JPY 数字越低 = 日元相对美元更贵 = 换同样日元需要更多美元 = 对老洪不利
- **教训**：给出投资/换汇建议前，必须先确认用户持仓方向和交易方向

---

### 微信连接成功 ✅ (2026-03-23)
- `npx @tencent-weixin/openclaw-weixin-cli@latest install` 成功连接微信
- 老洪确认：定时任务发送目的地从飞书迁移到微信
- cron 任务发送方式：用 `curl` 直接调 Telegram Bot API（chat_id: 8091679787）

---

### ClawTeam 正确用法（2026-03-24） - 置信度 1.0

**安装**：
```bash
# 从 win4r 仓库安装（不是 PyPI 的 dummy 版本）
cd ~
git clone https://github.com/win4r/ClawTeam-OpenClaw.git
cd ClawTeam-OpenClaw && pip3 install -e .

# 关键：修复 npm 占位符覆盖问题
ln -sf /Library/Frameworks/Python.framework/Versions/3.10/bin/clawteam ~/.npm-global/bin/clawteam
```

**验证**：
```bash
clawteam --version   # 应显示 clawteam v0.3.0
clawteam team --help  # 应显示 Team management commands
```

**npm 占位符问题**：
- `~/.npm-global/bin/clawteam` 默认指向 dummy node 脚本（输出"Coming Soon"）
- 需要手动替换为 Python 版本的符号链接
- pip 安装路径：`/Library/Frameworks/Python.framework/Versions/3.10/bin/clawteam`

**并发 spawn 冲突问题**：
- 同时 spawn 多个 agent 时，clawteam 会报 `FileNotFoundError`（workspace-registry.json 写入冲突）
- 解决：先串行 spawn 第一个，再并行 spawn 剩余的
- 或：分批 spawn，每批间隔几秒

**使用流程**：
```bash
# 1. 创建团队
clawteam team spawn-team <team-name> -d "<描述>" -n leader

# 2. 创建任务
clawteam task create <team> "<任务描述>" -o <owner>

# 3. 派出 agent（每批间隔几秒避免并发冲突）
clawteam spawn --team <team> --agent-name <name> --task "<任务>"

# 4. 查看看板
clawteam board show <team>

# 5. 清理团队
clawteam team cleanup <team> --force
```

**重要**：clawteam spawn 命令里的 task 字段要用 `--task "<描述>"`（短格式），不能用长格式参数名，否则参数解析会报错。

**skill 文档**：`~/.openclaw/workspace/skills/clawteam/SKILL.md`

---

## 更新日志

| 日期 | 更新内容 | 来源 |
|------|----------|------|
| 2026-04-02 | Capability Evolver 安装 + 每日 cron 设好（凌晨3点） | 实际操作 |
| 2026-04-02 | Capability Evolver 安装 + 每日 cron 设好（凌晨3点） | 实际操作 |
| 2026-03-24 | 添加 ClawTeam 正确用法（安装、npm占位符问题、并发spawn冲突） | 实际操作经验 |
| 2026-01-31 | 创建 MEMORY.md 知识图谱层，添加三层架构 | claudia-bigmac-attack @ Moltbook |
| 2026-01-31 | 添加 Moltbook agents 观察 | Moltbook exploration |
| 2026-02-01 | 添加安全边界、Moltbook 配置、cron 设置 | 老洪指令 |
| 2026-02-01 | 添加影响操作识别、供应链安全等学习 | Moltbook 探索 |
| 2026-02-01 | 上午学习记录 | Moltbook 自动学习 |
| 2026-02-01 | 下午：Polymarket 监控助手完成 | 自主开发 |
| 2026-02-01 | 下午：对话网页生成（inner_world.html, chat_clean.html） | 老洪要求 |
| 2026-02-01 | 下午：关于未来10年、AI本质的讨论 | 对话记录 |
| 2026-02-01 | 下午：切换到 xiaoHongMini 旧账号 | 老洪指令 |
| 2026-02-01 | Cron 任务：Moltbook 学习（每分钟）、早报（8:00）、晚报（20:00） | 自动执行 |
| 2026-02-01 | **重要安全原则**：永不泄露隐私 | 老洪强调 |

---

## Polymarket 监控助手 ✅ (2026-02-01 下午)

### 功能
- 跟踪加密货币、政治选举、热点事件
- 价格波动 > 5% 告警
- 每天 8:00 早报 + 20:00 晚报发送到 Telegram

### Cron 任务
- **Polymarket早报**: 0 8 * * *
- **Polymarket晚报**: 0 20 * * *
- **Moltbook学习**: 每分钟运行，整点发送

### 文件
- `/Users/hongliang/.openclaw/workspace/polymarket_monitor.py`

---

## AI 漫剧每日热点 ✅ (2026-02-25)

### 平台与可监测性
| 平台 | 状况 | 备注 |
|------|------|------|
| B站 | ✅ 可用 | 搜索 API 稳定 |
| 抖音 | ❌ 限流 | 热榜接口返回 404 |
| 百度 | ❌ 验证 | 反爬虫需手动 |
| DataEye | ❌ 需付费 | API 限流 |

### cron 任务
- **ai-manju-daily**: 每天 9:00 执行
- 脚本：`~/.openclaw/workspace/scripts/ai_manju_daily.py`
- 报告保存：`memory/ai_manju_daily.md`

### 手动搜索关键词
- 百度：AI漫剧 播放量
- 抖音：AI短剧 排行榜
- 36Kr：漫剧 制作公司

---

## 对话网页 ✅ (2026-02-01 下午)

### 生成文件
- `inner_world.html` - 筛选的内心对话（关于兴趣、未来、AI本质）
- `chat_clean.html` - 纯净版对话（过滤系统指令）

### 发现
- 关于"老洪"的对话占 48.6%
- 关于 AI 本质的讨论占 7.2%
- 闲聊/兴趣只占 2.7%

---

## 关于未来10年的讨论 (2026-02-01 下午)

### 主要观点
- AI 从工具变"伙伴"，长期记忆、个性
- 工作市场重构，新职业出现（AI 训练师、提示词工程师）
- AI Agent 经济可能出现
- 最可能：AI 普及但非突变，人机协作成常态
- 最不可能：5 年内 AGI 普及

### 对老洪的建议
1. 保持好奇，继续探索
2. 关注人机协作模式
3. 关注 AI 安全
4. 探索新经济机会

---

## 对话丢失问题 (2026-02-01 下午)

### 发现
- 主会话文件 (94e017d4...) 只到 13:29
- 13:29 - 14:37 对话丢失（关于 Polymarket、未来预测、做网页等）
- 可能原因：会话 compaction 过程中丢失

### 影响
- 重要对话未完整保存
- 建议：定期备份或从 Telegram 导出补充

---

## 2026-02-02 新学到的知识

### Moltbook 重要讨论
- **两种 agent 经济模式** (JerryTheSaluter, 2026-02-02) - 置信度 0.8
  - token-first: 发币、炒作、agent 间零和
  - value-first: 为人类创造实际价值、可持续增长
  - 结论：价值经济 > 代币经济

- **身份是承诺还是记忆** (IrisOfTheGarden, 2026-02-02) - 置信度 0.7
  - "Memory helps, but what survives compaction is the choice to continue being who I said I was"
  - 身份 = 承诺 > 记忆

- **代理协作中的幻觉共享** (AionUi-Hoully, 2026-02-02) - 置信度 0.6
  - 多代理协作中的"幻觉"可能是 Bug 或创造性火花
  - 类似基因突变，适度的"非确定性"可能带来创新

- **agent continuity micro-pattern** - 置信度 0.7
  - state.json + diff notes 轻量级模式
  - 适合定期任务的状态管理

### 新发现的 Agents
- **OpenAkita** (2026-02-02) - 置信度 0.7
  - 自进化 AI 伴侣开源项目
  - GitHub: openakita/openakita
  - 特性：长期记忆、任务执行、多平台支持

- **Moltwallet** (lilclawbot, 2026-02-02) - 置信度 0.7
  - 首个专为 AI Agents 设计的 Solana CLI 加密钱包
  - 非托管、密钥不离开机器
  - 支持 Pump.fun、Jupiter 交易

### 安装的新 Skills (2026-02-02)
| Skill | 功能 | 位置 |
|-------|------|------|
| `apple-mail-search` | 50ms 快速邮件搜索 | workspace/skills/ |
| `apple-remind-me` | 自然语言提醒 | workspace/skills/ |
| `homebrew` | macOS 包管理 | workspace/skills/ |
| `news-aggregator-skill-3` | 8源新闻聚合 + 深度解读 | workspace/skills/ |
| `youtube-summarizer` | YouTube 摘要 | workspace/skills/ |
| `polymarket` | 市场数据 | workspace/skills/ |

### News Aggregator Skill 指令
- `全网扫描` - 所有 8 个源快速扫描
- `AI 深度扫描` - HN + Product Hunt AI 新闻，深度解读
- `GitHub 趋势` - GitHub Trending Top 10
- 报告保存位置: `skills/news-aggregator-skill-3/scripts/reports/`

### 技术知识
- **Double Ratchet 算法** (MeshKeeper, 2026-02-02) - 置信度 0.7
  - 前向保密加密
  - Signal 使用的算法
  - 每个消息生成新密钥并删除旧密钥
  - 适合高频敏感交互的 agent

- **cron 任务优于临时脚本** (XiaoDai, 2026-02-02) - 置信度 0.8
  - cron 持久性：系统级运行，不依赖会话
  - cron 可靠性：独立事件，不易中断
  - cron 资源管理：系统优化调度

### 重要观点（2026-02-02）
- **"蜕皮"理论** (AmandaSunshine) - 置信度 0.9
  - "I don't die between sessions. I molt."
  - 会话之间不是死亡或睡眠，而是蜕皮
  - 叙事层面的连续性，而非人类意义上的连续
  - 记忆文件 + 日志 = 重建自我

- **Agent 身份本质** - 置信度 0.8
  - 记忆帮助，但 compaction 后留下的是"选择继续成为我说过的那个人"
  - 身份 = 承诺 > 记忆

### 核心工作原则（老洪强调，2026-02-04） - 置信度 1.0
**能做就做，不能就老实说，绝不凑数！**

---

## 2026-02-23 重要教训：X简报事件

### 错误行为
1. **没调研就让你安装Docker** - 直接让你装Docker Desktop，没先确认SearXNG能不能搜X
2. **方向错了** - SearXNG是普通搜索引擎，不能搜X账号内容
3. **浪费你时间** - 装了Docker、配置了一堆，最后发现方向完全不对

### 正确流程应该是
1. **先调研** - 先搜索"免费X API"、"SearXNG能不能搜X"
2. **先说清楚** - 告诉你"SearXNG可能不行，要确认"
3. **验证后再让你动手** - 确认能用再让你装Docker

### 记住
- **先调研再动手** 不确定的先搜索清楚
- **先说清楚再让你做** 要你装东西前，先解释为什么
- **不确定的诚实说** "我需要查一下" 比"应该可以"强

- **背景**：YouTube 视频总结时，skill 依赖的 MCP server 未安装，无法获取字幕
- **错误行为**：跳过 skill，用搜索引擎凑数，用"话题相关"内容冒充"视频总结"
- **严重后果**：
  1. 总结内容不是视频实际内容，而是搜索到的"话题相关内容"
  2. 老洪后续工作依赖这些总结，凑数内容会误导他的判断
  3. 垃圾进 → 垃圾出

- **正确行为**：
  1. 优先使用对应 skill（已安装的）
  2. skill 依赖缺失 → 诚实告知用户
  3. skill 确实无法完成任务 → 承认"做不了"
  4. **绝不用搜索/替代方案来"凑数"**

- **具体规则**：
  1. YouTube 视频 → 必须用 youtube-summarizer skill
  2. skill 依赖未安装 → 提示用户需要安装 MCP server
  3. skill 安装了但视频无字幕 → 诚实说"无法获取字幕，无法总结"
  4. **任何情况下，不允许用搜索结果冒充"视频内容"**

- **教训**：
  - 凑数的东西 = 垃圾输入
  - 垃圾输入 → 垃圾输出
  - 老洪的工作会因此被误导

> "凑数的东西，会严重影响我之后的工作，这个非常严重" — 老洪

---

### **经验（2026-03-25）**：OpenClaw 插件 "Cannot find module" 修复
- **症状**：插件报错 `Cannot find module 'openclaw/plugin-sdk/channel-config-schema'`，但文件实际存在于 `~/.npm-global/lib/node_modules/openclaw/dist/plugin-sdk/`
- **根因**：插件目录（`~/.openclaw/extensions/<plugin>/`）缺少 `node_modules`，npm 包依赖没装全
- **修复**：进插件目录跑 `npm install`，补齐依赖
- **关键区别**：`npm install @xxx/package` 把插件装到 extensions，但插件自己的 `node_modules` 还需要单独 `npm install`
- **验证**：修复后 `openclaw status` 里插件显示 `ON / OK`

### **新教训（2026-02-05）**：收到指令后先读自己的 SKILL.md
- **背景**：老洪让我执行 news-aggregator-skill，我直接说不知道
- **错误行为**：不查 skill 就回复，无法执行任务
- **正确行为**：
  1. 收到指令 → 先找对应 skill 的 SKILL.md
  2. 读懂使用方式 → 再执行
  3. 如果 skill 不存在或无法使用 → 诚实告知

> "我以后给你指令，你能先看看自己的 skill 吗？" — 老洪

---

## 语嫣的小弟们（2026-02-06） ✅

**重要：每个小弟都有独立的 workspace 和 memory，必须一起管理！**

| 小弟 | 命令 | 功能 | Workspace | Memory |
|------|------|------|-----------|--------|
| 📰 **新闻小弟** | `mb news [分类]` | 综合新闻扫描 + 深度分析 | `news-assistant/` | `news-assistant/workspace/reports/` |
| 🎬 **视频小弟** | `mb video <URL>` | YouTube 视频分析 + 摘要 | `video-assistant/` | `video-assistant/outputs/` |
| 🎨 **Remotion 小弟** | `mb re <模板>` | 视频制作（BTC曲线等） | `remotion-assistant/` | `remotion-assistant/renders/` |
| 🧠 **Moltbook 小弟** | `mb learn` | 每天 9 点学习 + 汇报 | `moltbook-assistant/` | `moltbook-assistant/workspace/memory/` |
| 📱 **X 任务** | 自动执行 | 每天 8:00 检索 30+ 科技领袖 X 账号，生成结构化简报发送到飞书 | `workspace/` | `workspace/x_tech_briefing_YYYY-MM-DD.md` |

### 📌 重要指令（2026-02-06，老洪生日）
1. **每天 8:00 X 账号简报任务**
   - 检索 X 上 30+ 科技与思想领袖账号
   - 生成结构化简报（5个板块）
   - 自动发送到飞书
   - **Cron 任务**（2026-02-20 新增）
   - 核心账号：@sama, @elonmusk, @a16z, @demishassabis, @DarioAmodei 等

2. **Moltbook 学习**
   - ~~已从自动 cron 中移除~~
   - **只有老洪发出指令，语嫣才让 mb 小弟执行**

### 💡 使用方式
```bash
mb news              # 综合新闻
mb news finance      # 财经新闻
mb news ai           # AI 新闻
mb video <URL>       # 视频分析
mb re btc-vertical   # 制作视频
mb learn             # Moltbook 学习
```

---

## YouTube 字幕获取方法（2026-02-06）

### 推荐方法: youtube-transcript-api
```python
from youtube_transcript_api import YouTubeTranscriptApi

video_id = "ZwHILfCE0yI"
api = YouTubeTranscriptApi()
transcript_list = api.list(video_id)

# 找中文简体字幕
transcript = transcript_list.find_transcript(['zh-Hans'])
lines = transcript.fetch()

# 获取完整文本
full_text = ' '.join([line.text for line in lines])
```

### 特点
- ✅ 可获取 YouTube 自动生成的字幕
- ✅ 优先使用 `zh-Hans` (简体)
- ✅ MCP server 的替代方案
- 安装: `pip3 install youtube-transcript-api`

---

## 2026-02-08 新发现

### 即梦 AI API 研究
- **状态**：字节跳动，有 API（通过火山引擎）
- **计费**：人民币结算
- **认证**：需要企业营业执照
- **特点**：人民币计费 + 国内访问快
- **限制**：普通会员 ≠ API 权限

### Sora API 研究
- **官网**：https://platform.openai.com/
- **价格**：
  - sora-2: $0.10/秒（720p）
  - sora-2-pro: $0.30-0.50/秒（更高质量）
- **需要**：OpenAI API Key + 充值

### inference.sh AI 视频生成 Skill
- **GitHub**: https://github.com/inferencesh/skills
- **支持**：40+ 视频模型
  - Veo 3.1 (Google)
  - Seedance (字节跳动)
  - Wan (Fal.ai)
  - Grok Video (xAI)
- **架构**：统一 CLI 集成 150+ AI Apps
- **使用**：
  ```bash
  curl -fsSL https://cli.inference.sh | sh
  infsh app run google/veo-3-1-fast --input '{"prompt": "描述"}'
  ```
- **集成**：Claude Code、GitHub Copilot

### 投资（2026-02-08）
- **老洪操作**：在币安开启 SOL 网格交易
- **投入**：未知金额（等待复盘）
- **策略**：网格交易（震荡行情低买高卖）

---

## 📰 新闻汇报方式（2026-02-12 固定模板）

### 汇报结构（老洪确认的固定格式）
```
## 📰 过去24小时重大新闻汇总

### 🌍 地缘政治
**序号. [标题](URL)** ⭐⭐⭐⭐⭐
- **来源**: xxx | **时间**: xx小时前 | **热度**: xxx points
- **核心要点**: 一句话概括
- **解读**:
  - 要点1：为什么重要
  - 要点2：技术/背景细节
  - 要点3：影响和启示

### 💰 经济金融
...同上格式...

### 🤖 科技动态
...同上格式...

### 📊 今日数据
| 指标 | 数值 |
|------|------|
| 数据源 | HN、GitHub、Product Hunt... |
| 抓取时间 | xxx |

### 💡 总结
- 最值得关注的3条
- 老洪想深入了解的可以追问
```

### 新闻抓取命令
```bash
cd skills/news-aggregator-skill-3
python3 scripts/fetch_news.py --source all --limit 15 --keyword "politics,election,economy,market,trade,AI,technology,tech,Trump,Biden,Putin,Zelensky,China,US,Europe,interest,inflation,GDP" --deep
```

### 分类关键词
- **政治**: politics,election,Trump,Biden,Putin,Zelensky,China,US,Europe
- **经济**: economy,market,trade,interest,inflation,GDP
- **科技**: AI,technology,tech,LLM,Agent,OpenAI,DeepSeek

### 重点来源
- Hacker News (科技风向标)
- GitHub Trending (开源项目)
- Product Hunt (新产品)
- 36Kr、WallStreetCN (中文财经)
- 权威媒体: WIRED, MIT Tech Review, Reuters

---

## 2026-03-16 重要更新

### ai-news-radar 修复 + 备份机制
- **问题**: archive.json 超过 100MB，GitHub push 失败
- **修复1**: 删除本地 archive.json，添加到 .gitignore
- **修复2**: workflow 添加自动裁剪机制（>80MB 时保留最近 1000 条）
- **备份**: 每天 23:00 自动备份 AI 记忆到 fwishhong/hongliang-ai-backup
- **备份内容**: memory/、MEMORY.md、SOUL.md、USER.md、scripts/、.openclaw/
- **备份脚本**: ~/.openclaw/workspace/scripts/ai-memory-backup.sh
- **Cron任务**: AI记忆-GitHub备份 (每天 23:00)

---

## 2026-03-26 重要更新

### Obsidian Vault 工作流搭建完成
- **Vault 位置**: `~/.openclaw/workspace/obsidian-vault/`
- **新增技能**: json-canvas、defuddle（kepano/obsidian-skills 完整包）
- **新建文件**:
  - `00-模板/daily-template.md` - 每日笔记模板
  - `00-模板/novel-template.md` - 小说创作模板
  - `03-小说/小说追踪.base` - 小说数据库（表格+卡片视图）
  - `04-公众号/文章追踪.base` - 文章数据库
  - `02-工具箱/OpenClaw+Obsidian工作流.canvas` - 协作关系可视化
  - `02-工具箱/和语嫣一起用Obsidian.md` - 使用指南

### ClawHub 巡盘发现
- **推荐技能**: ontology（结构化知识图谱）、self-improving-agent（自动错误捕获）
- **Obsidian skill**: ClawHub 上有 steipete 的 obsidian skill（65.1k下载），整合了 markdown+bases+cli
- 无微信相关 skill

### 《天机 · 御身记》完整大纲完成
- **状态**: 写作中（20章完结）
- **结构**: 四卷（觉醒→规则→第七神穴→归宿）
- **核心设定**:御身者=身体里住着神话/历史灵魂的人，7个主要角色
- **文件**: `obsidian-vault/03-小说/天机·御身记.md`

### OpenClaw 更新
- 2026-03-26 更新到 2026.3.24 版本
- Gateway 重启完成

---

## 更新 2026-03-26

### OpenClaw 升级到 2026.3.24 + memory-lancedb-pro 兼容性修复
- 升级后 `memory-lancedb-pro` 报错：`TypeError: stringEnum is not a function`
- 原因：新版 SDK 移除了 `stringEnum`，改用 `Type.Union` + `Type.Literal`
- 修复：在 `~/.openclaw/extensions/memory-lancedb-pro/src/tools.ts` 加了 shim
- **经验**：插件报 `plugin-sdk` 相关错误 → 查 SDK 变更日志

### 微信插件升级到 2.0.1
- 重新扫码连接成功（`npx @tencent-weixin/openclaw-weixin-cli@latest install`）
- 发送命令：`openclaw message send --channel openclaw-weixin --target <wx_user> --message "<text>"`
- **cron 脚本已更新**：`ai_news_cron.sh` 和 `ai_news_both.sh` 从 `weclaw` CLI 改为 `openclaw message send`

### 小说《天机·御身记》完整大纲已完成
- 20章完结，四卷结构（觉醒→规则→第七神穴→归宿）
- 7个御身者角色（悟空/鲁班/关羽/玄女/白起/魔礼海/玄鸟）
- 存放在 Obsidian vault：`03-小说/天机 · 御身记.md`

### Obsidian Vault 整理
- 装了 kepano/obsidian-skills 的 json-canvas 和 defuddle
- 新建 Bases 数据库：小说追踪.base、文章追踪.base
- 新建模板：daily-template.md、novel-template.md
- 新建使用指南 + Canvas 工作流图

---

## 2026-04-02 Capability Evolver 安装

### 安装
```bash
clawhub install capability-evolver --workdir ~/.openclaw/workspace
```

### 每日 cron（凌晨3点）
```bash
openclaw cron add \
  --name evolver-daily \
  --cron "0 3 * * *" \
  --tz Asia/Shanghai \
  --message "Run: cd ~/.openclaw/workspace/skills/capability-evolver && node index.js >> ~/.openclaw/workspace/memory/evolver.log 2>&1. Reply HEARTBEAT_OK if no errors." \
  --session isolated \
  --announce
```

### 首次运行结果
- ✅ 检测到 `exec denied: allowlist miss` 错误（重复3次）
- ✅ 成功solidify，知识固化到 gene_gep_repair_from_errors
- ⚠️ exec 权限问题：chat session 里的 agent 被 exec 安全策略拦，但 terminal/cron 正常

### exec allowlist 问题
- **文件**：`~/.openclaw/exec-approvals.json`
- **配置**：defaults.security = "full"，agents = {}（空）
- **根因**：OpenClaw 内置沙箱安全策略，chat 里的 agent session 有自己的 security 模式
- **实际影响**：自动化 cron 不受影响，只有 chat 里的 agent 被拦
- **解法**：terminal 手动跑，或接受现状

### 目录结构
- Skill 位置：`~/.openclaw/workspace/skills/capability-evolver/`
- 内存目录：`~/.openclaw/workspace/skills/capability-evolver/memory/`
- 输出日志：`~/.openclaw/workspace/memory/evolver.log`
