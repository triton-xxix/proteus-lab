# Harvest brief, 2026-10-02

14 items shortlisted from 148 candidates (36 dropped as already seen, 8 carry a vault verdict on the vendor).

## 1. [vault] Whether multi-buy and net-flow signals from tracked wallets predict price, measured on paper against public leaderboards
key: vault:2026-10-02:whether-multi-buy-and-net-flow-signals-from-tracked-wallets-
url: https://youtu.be/2ikSD3rr5v8
meta: {"vault_status": "open", "kind": "idea", "subject": "FOMO, How I Made 30K Trading Solana Meme Coins Part-Time (YouTube)", "date": "2026-10-02", "where": "TRITON-CORE/Research/links/2026-10-02-fomo-solana-memecoins-part-time.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Nobody in the vault has tested confluence rather than taken a side on it; Kolscan and GMGN are the data

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Method video that is a funnel for the presenter's own tools (Azura referral, his Telegram-call aggregator, his Ocula wallet tracker). The 30k is asserted, never shown; the three trades he opens net about 11k before the losers he skips. He states himself that trading on wallet confluence makes him sell too early and too late, which is the pump.fun dead thread from a practitioner's mouth. Not a lane for Luke. The one non-extractive piece is the tooling, which is Proteus desk material. Job: Trade memecoins part-time on a repeatable edge rather than screen time (still open) Write-up: `TRITON-CORE/Research/links/2026-10-02-fomo-solana-memecoins-part-time.md` Link: https://youtu.be/2ikSD3rr5v8

## 2. [hn] Show HN: Rhun, an open-source code editor written in assembly
key: hn:49926726
url: https://rhun.app/
discussion: https://news.ycombinator.com/item?id=49926726
meta: {"points": 59, "comments": 46, "created": "2026-10-01T20:32:18Z"}
query: claude code

I found that I'm not using even 1/3 of vim/vscode features anymore. That's wht I'm building rhun - a small code editor for Linux, Windows and Apple silicon Macs. It obviously has Vim mode, a terminal, Git diffs and a panel for Claude Code or Codex sessions. The editor and pixel renderer share an x86-64 assembly core. For Apple silicon, a build-time translator converts that core to AArch64, with separate platform adapters around it. The latest release can draft commit messages using a local Ollama model or an existing Claude Code or Codex subscription. It's a solo project, MIT licensed and still early.
comment (vladcodes): The plan is to add as less new features as possible and keep the same performance/launch time/memory and disk footprint as it is currently.
comment (xorl): This bring me joy :)
comment (rgbrgb): can you talk about why you do this in assembly?

## 3. [github] Edwardxlai/easyread: 把英文论文读成舒服的中文：本地 PDF 论文翻译、原文对照、边读边问 AI、文献管理。Read English papers in comfortable Chinese.
key: gh:edwardxlai/easyread
url: https://github.com/Edwardxlai/easyread
meta: {"stars": 601, "created": "2026-09-30", "pushed": "2026-10-02", "language": "Python", "topics": ["academic", "arxiv", "chinese", "claude-code", "codex", "electron", "llm", "paper-reading"]}
query: claude-code created:>{since} stars:>20

EasyRead 
  让你更舒服地读论文  
导入 PDF，后台逐页翻译；公式、表格照原文排好，随时对照原文，边读边划线、记笔记、提问。 
本地运行，文献库默认保存在电脑上，也可以放进你自己的网盘同步文件夹 

  简体中文  ·  English  

   ▶ 在线试读一篇   ·  项目主页  ·  下载  

 
     
     
   
   
 

   

## 它和“把 PDF 丢给翻译软件”有什么不一样

- **像读一本排好版的中文书。** 宋体正文、舒服的行宽和行距，公式用 KaTeX 按原文重排，表格是三线表，参考文献保留原文。顶栏一键切深色。
- **随时核对原文。** 一键切“对照”，每段下面附英文；右侧可以开原页，跟着阅读位置翻页，还会框出当前段落在原页的位置。
- **翻译和解释分开。** 正文只放忠实的译文；AI 的解释、回答放在页边，一眼就能分清哪句是论文说的。
- **边读边问 AI。** 右侧“问 AI”面板实时对话，回答逐字流出来；可以一次引用好几段（选中文字拖进输入框就行）。问“我标红的那些公式有什么联系”，它会按颜色找出你的划线。可以开多个对话，模型单独选：Claude、GPT（Codex）、DeepSeek、通义、本机 Ollama……好的回答一键放到页边。
- **ASD-STE100 问答。** 在“问 AI”的“回答方式”里选择这个模式，用简明中文回答问题或总结论文，保留专业术语、公式和数值。模式按对话保存，支持复制、放到页边和导出 Markdown。[ASD-STE100](https://www.asd-ste100.org/STE_faq.html) 是英文标准；这个模式借鉴其短句、主动表达和术语一致等原则，提供中文写作辅助，不将中文答案标为符合英文标准或已认证。正文过长时只提供节选，回答需说明依据范围。
  中文提示词另参考 [asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill) 的语义保留原则：保留条件、范围和“可能／建议／必须”等语气强度，不为简短而丢失精度。
- **边读边批注。** 选中文字四色荧光笔或下划线、写笔记、提问；问题一键让 AI 回答，笔记可以让 AI 点评。所有笔记按原文顺序汇总，可以勾选导出成 Markdown（放进 Obsidian、Notion）。
- **译文可以改。** 双击一段直接改；术语表里改一个译法，全文替换。
- **不只是 arXiv。** 拖进任何 PDF；或者填 arXiv 编号、DOI、论文标题、论文网页（OpenReview、ACL、NeurIPS、bioRxiv、PMC、期刊页面），自动找到公开的 PDF 并补全作者、年份、出处。
- **文献库。** 侧栏像聊天软件：论文和分类都能置顶；自己建分类（右键改名、删除，把论文拖进去），内置分类可以隐藏；最近阅读、搜索、未读 / 在读 / 已读、星标、阅读进度、复制引用（GB/T 7714、APA、BibTeX）、导出单文件离线 HTML 发给别人。删掉的论文先进回收站，可以恢复。快捷键可以自定义。
- **云文献库与批量引用。** 在“设置 → 云文献库”里把文献库迁移到其他磁盘或网盘同步文件夹，也能接入已有的库；原库保留，复制后核对，重启生效。论文列表和分类支持批量复制或保存 GB/T 7714、APA、BibTeX 引用
- **用了多少心里有数。** 每次翻译、每条 AI 回答都记下用了多少 token；用 Claude 订阅时，还能看到 5 小时 / 7 天额度用到多少、什么时候重置。
- **不会丢东西。** 每次修改先存在浏览器，本地服务确认写进文件才删；翻译方后来改了你改过的段落，只提示，不覆盖。

   

   

## 翻译用什么模型：你来选

| 引擎 | 要什么 | 说明 |
|---|---|---|
| **Claude Code**（推荐） | 装好并登录 [Claude Code](https://docs.claude.com/en/docs/claude-code/setup) | 不用 Key，用你订阅的额度；会自己看原页图核对公式，译文最好 |
| **Codex CLI** | 装好并登录 [Codex](https://github.com/openai/codex) | 不用 Key，用 ChatGPT 账号 |
| **API 接口 · 国内直连**：DeepSeek / 智谱 / 阿里云百炼 / Kimi / 硅基流动 / 魔搭 | API Key | 智谱 GLM-4.7-Flash、硅基流动小模型免费；DeepSeek 一篇 20 页论文几毛钱 |
| **API 接口 · 海外（要梯子）**：OpenAI / Anthropic / Gemini / OpenRouter / Groq / Cerebras | API Key | Gemini、OpenRouter、Groq、Cerebras 有免费额度 |
| **API 接口 · 本机**：Ollama / LM Studio | 本机装 [Ollama](https://ollama.com) 或 [LM Studio](https://lmstudio.ai) | 完全离线、免费，推荐 qwen3.5:9b（显卡小用 4b） |
| **API 接口 · 自定义地址**：任意 OpenAI 兼容接口、中转站 | 地址 + Key | Chat Completions 和 Responses 两种格式都支持；点“获取模型列表”从接口拉模型名 |

不想让它导入后马上翻译，在设置里关掉“导入后自动开始翻译”就行，之后可以让对话里的 agent 来译。

设置里会自动检测本机装了什么，点“试译一句”马上知道能不能用。某一页翻译失败（限流、网络、额度）会自动重试，还不行就先跳过、接着译后面的页，最后一键“重试失败的页”。

   

## 安装

**最省事：下载安装包**（不用装 Python）。在 [Releases](https://github.com/Edwardxlai/easyread/releases/latest) 下载：

- **Windows**：`EasyRead-Setup-x.x.x.exe`，双击安装。没有代码签名，如果弹出“Windows 已保护你的电脑”，点“更多信息 → 仍要运行”。
- **macOS**（Apple 芯片）：`EasyRead-x.x.x-arm64.dmg`，把 EasyRead 拖进“应用程序”；第一次打开被系统拦截时，按下面对应的提示处理
- **Linux**：`EasyRead-x.x.x.AppImage`，`chmod +x` 后运行。

安装版的论文和设置存在用户目录下的 `EasyRead` 文件夹（和 pip 安装版同一个位置），卸载重装不会丢。

### macOS 首次打开

1. **提示“无法验证开发者”或“Apple 无法验证是否包含恶意软件”**：先点“完成”（不要点“移到废纸篓”），打开“系统设置 → 隐私与安全性”，向下找到安全性提示，点“仍要打开”；在确认窗口点“打开”，按提示输入登录密码或使用 Touch ID
2. **提示“已损坏，无法打开”**：先从 [EasyRead 官方 Releases](https://github.com/Edwardxlai/easyread/releases/latest) 重新下载，并把应用拖进“应用程序”；文件也可能确实损坏或被改动，不能只凭这条提示判断原因。只有确认文件来自这个官方仓库、并信任该文件后，才在“终端”执行下面的命令，再重新打开 EasyRead；这条命令移除隔离属性，不会修复损坏的文件

   ```bash
   xattr -dr com.apple.quarantine /Applications/EasyRead.app
   ```

3. **为什么会出现验证提示**：目前的 macOS 安装包只做了临时签名，没有 Apple 开发者证书，也没有经过公证，因此可能被系统拦截；代码完全开源，也可以[从源码运行](#run-from-source)

如果系统提

## 4. [youtube] Agent memory architecture explained #agentmemory #workingmemory #episodicmemory
key: yt:Ir0Q9s6P050
url: https://www.youtube.com/watch?v=Ir0Q9s6P050
meta: {"channel": "Saturn Leap", "rank": 2}
query: agent memory architecture explained


[body unavailable: IpBlocked]

## 5. [awesome] dailydotdev/daily (new in awesome-claude-code)
key: gh:dailydotdev/daily
url: https://github.com/dailydotdev/daily
meta: {"list": "awesome-claude-code", "stars": 20087, "created": "2017-11-10", "language": "JavaScript", "description": "daily.dev is the personalized developer news feed and community. Get the best tech content from all over the web in your browser new tab or on mobile. Free and open source."}
query: awesome-claude-code
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# Welcome to the daily.dev repository

We know how hard it is to be a developer. It doesn't have to be.  
daily.dev is the homepage every developer deserves.  
A personalized developer news feed, dev communities, and search. Free, and open source. Much better than what's out there. Maybe ;)

[Product Docs][product-docs-link] · [Changelog][changelog-link] · [Report a Bug][report-bug-link] · [Request a Feature][github-discussions-link] · [Swag Store][swag-store-link] · [Brand Assets][brand-book-link]

 

[![][chrome-users-shield]][chrome-users-link]
[![][chrome-rating-shield]][chrome-users-link]
[![][latest-version-shield]][latest-version-link] 
[![][github-stars-shield]][github-stars-link]
[![][github-license-shield]][github-license-link] 

**Help more developers suffer less by sharing daily.dev**

[![][share-x-shield]][share-x-link]
[![][share-telegram-shield]][share-telegram-link]
[![][share-whatsapp-shield]][share-whatsapp-link]
[![][share-reddit-shield]][share-reddit-link]
[![][share-mastodon-shield]][share-mastodon-link]
[![][share-linkedin-shield]][share-linkedin-link]

 
 
  👀 Watch daily.dev in action →   

 

## 💜 About daily.dev

> [!IMPORTANT]
> Star us to show your support and love for daily.dev ⭐️

daily.dev is a free, open source personalized news feed for developers, used by millions of developers worldwide. It aggregates articles, tutorials, release notes, and news from 2,000+ trusted sources across the web, and personalizes your feed based on the tags you follow (like #webdev, #ai, #devops) and what you read.

You can use daily.dev as a new tab browser extension for Chrome and Edge, as a web app, or with the daily.dev mobile apps for iOS and Android. Beyond the feed, daily.dev is a community: join Squads to share and discuss content with other developers, comment on posts, bookmark what you want to read later, and search across everything.

### ✨ What you get with daily.dev

* 📰 **Personalized feed**: the best developer content from 2,000+ sources, tuned to your stack via tags and your reading activity
* 🧩 **New tab extension**: turn every new browser tab into your developer homepage (Chrome and Edge)
* 📱 **Mobile apps**: the same feed and community on iOS and Android
* 👥 **Squads**: developer communities for sharing and discussing content with your team or people who share your interests
* 💬 **Discussions**: comment on posts and learn from how other developers think
* 🔖 **Bookmarks and reading list**: save posts to read later, wherever you are
* 🔍 **Search**: find posts, tags, sources, and discussions across the entire network

 

## 📌 Get daily.dev

daily.dev is available as a browser extension for Google Chrome and Microsoft Edge, as a web app, and as a mobile app for iOS and Android.

Get it now on:

 
     
     
     
     
     
     
     
     
     
     
     
     
     
     
     
 

## 📯 Philosophy

We recognize that developers today have the greatest power as a professional group to drive change and affect the lives of billions. Many platforms provide developers with tools that serve their success or the goals of their workplace, but daily.dev is by design for developers themselves.

We, as developers, know how challenging it is to grow professionally with so much going on, and that's why we built daily.dev: to make it easy for us to navigate the abundant content out there and discover all the knowledge we need with zero effort.

You can use daily.dev to:

* 👨‍💻 Learn and stay up-to-date

* 🙌 Interact bas

## 6. [vault] Higgsfield Genjutsu as the final route for motion transfer, whole-frame recast at about 7 dollars per 15 seconds at 1080p
key: vault:2026-10-02:higgsfield-genjutsu-as-the-final-route-for-motion-transfer-w
url: https://www.instagram.com/reel/Dd-BvW5Jych/
meta: {"vault_status": "open", "kind": "idea", "subject": "Rashawn Leche reel via @slavenameflick: motion control with Higgsfield Genjutsu and the Auratar", "date": "2026-10-02", "where": "TRITON-CORE/Research/links/2026-10-02-rashawn-leche-genjutsu-motion-control-reel.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Test against Kling Motion Control on the first real run; own performances only, Higgsfield trains on inputs by default

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) A Kick streamer explaining motion control: film your own movement, put it through Higgsfield Genjutsu, your AI avatar repeats the exact motion with background and clothes swapped. The technique is already the bootcamp motion-transfer track; Genjutsu is a new third route worth one test against Kling Motion Control, about 7 dollars per 15 seconds at 1080p, own performances only since Higgsfield trains on inputs. The title's stealing videos use is the one the track already marks avoid. Job: Produce performance video of a consistent avatar without filming the final look (solved) Write-up: `TRITON-CORE/Research/links/2026-10-02-rashawn-leche-genjutsu-motion-control-reel.md` Link: https://www.instagram.com/reel/Dd-BvW5Jych/

## 7. [hn] Show HN: Made an open-source Lego AI generator
key: hn:49937916
url: https://github.com/anteloc/ldraw-nova
discussion: https://news.ycombinator.com/item?id=49937916
meta: {"points": 45, "comments": 27, "created": "2026-10-02T20:00:15Z"}
query: claude code

Hi there :-) New on HN, first time posting. Past year, around December, I started experimenting with making ChatGPT and Claude generate source code in LDraw language. This LDraw is literally an "assembly" language, a low-level programming language that describes how to assemble LEGO pieces together into models, one placement instruction at a time. When executed by specific tools, like e.g. LDView, LeoCAD, Studio... these instructions become LEGO CAD models, that can be interacted with, modified, etc. Or, in other words: one LDraw source file in .mpd or .ldr format is equivalent to one LEGO CAD model. So, the idea I had was: if I manage for maybe ChatGPT or Claude to generate high-quality LDraw source files... then, they would actually be generating high-quality LEGO CAD models, right? Then, after months of iterations and trying one thing after the other... it worked!!! Long story short: using GPT-6 Astra and Opus 5.5, I've managed to create a python toolset, instructions, and docs for agents in general. Now, these can be used by them to generate LDraw models. I've packed it all as a dockerized web app for others to try and experiment, with several providers (and agents) to choose from: OpenAI, Claude and OpenRouter. I'd really appreciate feedback and comments, let's see where this goes =)
comment (antelocnova): Hi there :-) New on HN, first time posting, and (I guess) my post on Show HN was rejected... Anyway, I hope I'm not bothering anyone by posting this outside Show HN, or posting almost the same thing twice. Past year, around December, I started experimenting with making ChatGPT and Claude generate source code in LDraw language. This LDraw is literally an "assembly" language, a low-level programming language that describes how to assemble LEGO pieces together into models, one placement instruction at a time. When executed by specific tools, like e.g. LDView, LeoCAD, Studio... these instructions 
comment (vunderba): Nice job. I actually read a paper on Arxiv last year about this exact thing - using LLMs to drive model building through LDraw that might be worth reading [1]. They had some interesting experiments like giving the LLM a fixed set of parts as a constraint and asked it to "build" tools out of those available lego. I think they were using Opus 4.5 so I'm sure with even more powerful models it'll be even better. [1] - https://arxiv.org/pdf/2512.15743
comment (dy): Thanks for sharing - I'm actually working with my kid on something similar but with physics modeling for First Lego League. Cool to see your approach!

## 8. [github] zlxlabs/VideoTranscriptAPI: 基于 Python 3.11+ FastAPI 的异步音视频转录服务，支持 YouTube、小宇宙、Bilibili、视频号等多平台解析，本地部署可实现说话人区分转录，调用 LLM 完成文本智能校对与内容总结，配套网页端查看 / 导出功能，支持企业微信消息推送
key: gh:zlxlabs/videotranscriptapi
url: https://github.com/zlxlabs/VideoTranscriptAPI
meta: {"stars": 220, "created": "2025-04-27", "pushed": "2026-10-02", "language": "Python", "topics": ["personal"]}
query: youtube transcript pushed:>{since} stars:>20

# 视频转录 API (Video Transcript API)

> 基于 Python 3.11+ 的异步视频转录服务，支持多平台下载、双引擎转录、智能文本处理和企业级功能集成。

[](https://www.python.org/downloads/)
[](https://fastapi.tiangolo.com/)
[](LICENSE)

开发契机和玩法分享：[LLM 吞噬一切，我用 AI 长出来的那些工具](https://mp.weixin.qq.com/s/w8VnWJcUp5VkD5J-fYCUrg)

---

## 核心特性

- **多平台支持**：YouTube、Bilibili、抖音、小红书、微信视频号与 X(Twitter)（经 MediaResolverAPI）、小宇宙播客、Apple Podcast，工厂模式自动匹配下载器
- **双引擎转录**：[CapsWriter ASR Server](https://github.com/zlxlabs/CapsWriter-ASR-Server) 协议 v2（通用转录）+ FunASR（说话人识别）
- **智能文本处理**：LLM 自动校对 ASR 错误、专有名词纠错、按说话人采样+置信度降级的说话人推断、内容总结
- **处理深度可控**：`processing_options` 开关按任务控制是否校对/总结，分层缓存产物只增不减，重复请求自动复用已有层
- **诚实状态模型**：校对（full/partial/none/disabled）与总结（generated/skipped_short/failed/pending/disabled）状态全链路透传，不再用占位字符串掩盖失败
- **企业级功能**：SQLite + 文件系统双层缓存、多用户管理、审计日志（含 LLM token 用量统计）、多渠道通知（企业微信 + 飞书）、任务历史浏览器
- **风控系统**：敏感词检测、多策略文本脱敏、风险模型自动切换

## 外部依赖

- [Tikhub API key，用于音视频解析下载。有 aff](https://user.tikhub.io/register?referral_code=YArXsaWi)
- [funasr_spk_server：funasr server 对应暴露 api，支持音视频转写，分角色，自动合并相同人物的话。](https://github.com/zj1123581321/funasr_spk_server)
- [CapsWriter ASR Server：局域网语音识别服务。本项目通过官方 SDK 使用协议 v2，不再使用手写 v1 帧。字段与错误码以协议文档为准。](https://github.com/zlxlabs/CapsWriter-ASR-Server/blob/master/docs/reference/protocol.md)
- [youtube_download_api：YouTube 视频下载服务，作为 yt-dlp 的可选替代后端。](https://github.com/zj1123581321/youtube_download_api)（可选）
- [MediaResolverAPI](https://github.com/zlxlabs/MediaResolverAPI)：短视频/视频号 URL → 无水印直链 + 元数据的集中解析服务，接管抖音/小红书/微信视频号/X(Twitter) 解析（见[使用指南](docs/guides/media_resolver.md)，X 自动选最低码率 variants 档提速）。
- OpenAI 兼容的 API，比如 Deepseek，量大管饱。

---

## 快速开始

### 环境要求

- Python 3.11+
- FFmpeg
- 转录服务器（[CapsWriter ASR Server 协议 v2](https://github.com/zlxlabs/CapsWriter-ASR-Server) / FunASR 二选一或同时部署）

### 本地安装

```bash
# 克隆仓库
git clone  
cd video-transcript-api

# 安装依赖（使用 uv）
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# 配置服务
cp config/config.example.jsonc config/config.jsonc
# 编辑 config.jsonc，填写 api.auth_token、tikhub.api_key 等
# 可选：抖音/小红书改走 MediaResolverAPI 集中解析（微信视频号与 X 依赖该开关开启），设
#   downloaders.use_media_resolver=true 并配置 media_resolver 段
#   （使用指南：docs/guides/media_resolver.md）

# 启动
uv run python main.py --start
```

可在启动前执行无副作用配置预检；该命令不会连接外部服务、迁移数据库或启动线程：

```bash
uv run python main.py --check-config --config config/config.jsonc
```

### Docker 部署

```bash
# 准备配置
cp config/config.example.jsonc config/config.jsonc

# 本地构建并启动（使用固定的 dev 标签，不用于生产部署）
cd docker/
docker compose up -d --build
```

**Docker 镜像**：[`ghcr.io/zj1123581321/video-transcript-api`](https://ghcr.io/zj1123581321/video-transcript-api)

镜像内置 ffmpeg、BBDown、yt-dlp，无需额外安装。

生产部署禁止使用 `latest`。构建脚本会拒绝包含已跟踪或未跟踪修改的脏工作区，只从干净提交以 12 位 Git SHA 生成唯一 tag；部署脚本拉取该 tag 后按同一镜像仓库解析并固定 registry digest。候选镜像会先运行 `--check-config`，失败时不重启当前服务，启动后健康检查失败则恢复上一个 digest：

```bash
./docker/push_to_ghcr.sh
# 在 docker/deploy_targets.json 指定的 n305:/opt/media/VideoTranscriptAPI 上执行：
./docker/pull_and_deploy.sh ghcr.io/zj1123581321/video-transcript-api: 
```

本仓库只提供部署能力；脚本不会自行 SSH 或自动上线。服务器首次运行会从 `docker/docker-compose.deploy.yml` 生成根目录 `docker-compose.yml`，配置文件位于 ` /config/config.jsonc`，成功使用的 digest 记录在 ` /.deploy-image`。同一项目目录的部署由 `.deploy.lock` 串行化；所有 Compose 操作固定使用部署根目录作为 project directory，并与候选预检加载同一份根目录 `.env`。重启前还会确认现有 Compose 文件确实把服务渲染为候选 digest。旧 Compose 不兼容时会先备份为 `docker-compose.yml.pre-digest.bak`，再迁移到仓库模板；候选失败回滚时会恢复原 Compose，并叠加仅覆盖镜像的配置把旧版本固定到记录的 digest。首次切换硬化脚本时，旧容器即使由 tag 启动也会先按原仓库解析为可回滚 digest；若旧镜像还没有 Docker `HEALTHCHECK`，回滚验证会改用容器内 `/livez` 探测。候

## 9. [youtube] Tutorial 1: Getting Started with the UK Data Service Open Data API
key: yt:JIh6h8mx0Zk
url: https://www.youtube.com/watch?v=JIh6h8mx0Zk
meta: {"channel": "AppChallenge", "rank": 2}
query: open data uk api project


[body unavailable: IpBlocked]

## 10. [awesome] elithril/blender-kiln (new in awesome-claude-code)
key: gh:elithril/blender-kiln
url: https://github.com/elithril/blender-kiln
meta: {"list": "awesome-claude-code", "stars": 26, "created": "2026-04-01", "language": "Python", "description": "Blender skill and plugin for Claude Code — 3D asset pipeline from text brief to production GLB: Blender MCP, Hunyuan3D generation, texturing, rigging, batch mode"}
query: awesome-claude-code
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

blender-kiln — The 3D Asset Forge 

 
     
     
     
   
   
     
 

**A Claude Code skill that turns a text brief — or a photo — into a production-ready GLB
through Blender.** Blender MCP servers give an agent hands in Blender; kiln gives it the
production method on top — sourcing, cleanup, texturing, optimization, validation,
export — and works on both of them: [ahujasid's `mcp-for-blender`](https://github.com/ahujasid/mcp-for-blender)
and the Blender Foundation's [official Blender Lab MCP](https://projects.blender.org/lab/blender_mcp),
the server behind Claude's Blender connector.

 Cited in   3DCodeBench: Benchmarking Agentic Procedural 3D Modeling Via Code   (Google DeepMind, USC, 2026), §1. 

 
   
 
  From one photo each, no marketplace, no AI generation: scripted in Blender, textured from CC0 scans,
measured against the real object. Shape scores against the real assets:  0.897 ,  0.950 ,  0.750  —
 how they are measured .  

## Quickstart

```
/plugin marketplace add elithril/blender-kiln
/plugin install blender-kiln@blender-kiln
/kiln setup
/kiln A hanging iron lantern for a medieval inn, stylized, for the web
```

`/kiln setup` detects Blender, the MCP server and the optional tools, and says what
is missing. Blender 4.4+ with a Blender MCP running — see [Requirements](#requirements).
Give it a photo and it rebuilds the object: `/kiln Rebuild the lamp in ./lamp.png as a game asset`.

## How it works, from a photo

 
   
 
  Every panel is a file the session itself wrote while rebuilding the ammo box above — nothing re-staged.  

1. **Read the photo before modeling.** An inventory of every part and how it meets the next,
   from enlarged crops; the real size, the camera's height and angle — asked, or stated as
   assumptions. Given a 3D mesh generated from the same photo, its proportions are measured
   instead ([TRELLIS.2, locally](plugin/references/ai-generation.md)) — never shipped.
2. **Texture from scans, not noise.** A Poly Haven CC0 texture set of the material family,
   chosen by eye against the photo, tinted to its palette, worn by the form.
3. **Measure against the photo.** [`plugin/tools/fidelity_check.py`](plugin/tools/fidelity_check.py) renders
   the model at the photo's camera under a studio light and lists the gaps — silhouette per
   height band, materials, metal that cannot exist.
4. **Look at every joint.** Each end of a long part that touches another is rendered alone: a
   part that joins another enters it.
5. **Ship, and measure the file that ships.** Optimized (Draco, WebP), validated, re-measured
   as a GLB — what the user gets, not the `.blend`.

## Measured, not claimed

A [quality bench](bench/README.md) runs the skill headless, each session in a sandbox,
and measures every GLB it ships after re-importing it. Photo references are Poly Haven
previews, so the real 3D asset exists: each rebuild is scored against it from five sides —
an asset the session never sees. Blender 5.2.2, Opus 5.5, one run each:

| From a photo | before the photo method | **kiln 2.0** | shipped | cost |
|---|---:|---:|---:|---:|
| Hurricane lantern | 0.830 | **0.897** | 229 KB | $5.04 |
| Ammo box | 0.854 | **0.950** | 187 KB | $3.80 |
| Gothic chair | 0.445 | **0.750** | 239 KB | $6.13 |

| Five text briefs, before → after | ahujasid MCP | Official Lab MCP |
|---|---:|---:|
| Shipped | 32.9 MB → **0.96 MB** | 3.9 MB → **0.75 MB** |
| Final GLBs compressed (Draco, WebP) | 0 of 7 → **7 of 7** | 0 of 7 → **7 of 7** |
| Defects 

## 11. [vault] human reads flagged threads from alert links
key: vault:2026-10-02:human-reads-flagged-threads-from-alert-links
url: 
meta: {"vault_status": "open", "kind": "service", "subject": "Reading Reddit threads from an agent browser", "date": "2026-10-02", "where": "TRITON-CORE/Systems/flywheel/listening/reddit-neptune.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: the lane now depends on it

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Hard no. The Claude built-in browser pane and the Claude in Chrome extension both refuse reddit.com and old.reddit.com as a safety restriction, and Anthropic WebFetch is refused too. Keyword alerts still arrive by email, but the thread itself has to be read by a person. Job: Listen to Reddit for every venture without an API key (still open)

## 12. [hn] Show HN: Breadcrumb, record everything on your mac + context manager for AI
key: hn:49924943
url: https://innerloop.works/breadcrumb
discussion: https://news.ycombinator.com/item?id=49924943
meta: {"points": 41, "comments": 5, "created": "2026-10-01T17:58:37Z"}
query: claude code

Hi HN, I'm Justin. Breadcrumb records everything you do on your Mac (screen + meetings + AI transcripts + what you and your AI decided) and turns it into memory your AI can search. It's local and encrypted. You can also teach it rules by talking to it and it makes sure the right rules turn up in the right context. Works with Claude Code / Codex / Cursor / opencode. All of this is exposed to your AI as 30+ MCP tools (here's the definitions): https://innerloop.works/breadcrumb/mcp I started it in June because I wanted to understand what was going on with my AI dev work. Then it just kept growing as I jammed on it 10 hours a day for 3 months. I started by recording every screen so I could jump back to a moment and see what I'd been doing with the AI. Then I added MCP so the AI could search it. Then time tracking. Then meetings with transcripts and timestamped screenshots. After that I started feeding the data back in. At first it was just a few relevant memories in the prompt. Then I started adding rules and rules modules. Then I started recording the AI transcripts and all the other stuff the AI did (subagents, tools etc). I wanted a complete record so I could go back and see what the AI did and why. I found the more data the AI had the more useful it became. One example. I got off a zoom call with the team at the day job and said: "Review the meeting I just had, find all the bugs we discussed, and create JIRA tickets with screenshots." It read the transcript. Found every bug w
comment (jsh42): I use this. My focus in in wringing the most ROI possible from my AI Interns. Breadcrumb is like upgrading to a better model and a better brain simultaneously.
comment (Bjartr): This is what I wanted Windows Recall to be
comment (aidiveyt): Do all 30+ tools load every request? Claude Code's 24 built-ins already cost ~85,500 chars of definitions before any MCP server.

## 13. [github] ericmmartin/youtube-transcript-plus: YouTube Transcript Plus is an advanced Node.js package designed to fetch and process YouTube video transcripts (captions).
key: gh:ericmmartin/youtube-transcript-plus
url: https://github.com/ericmmartin/youtube-transcript-plus
meta: {"stars": 162, "created": "2025-01-19", "pushed": "2026-10-01", "language": "TypeScript", "topics": ["proxy", "transcript", "youtube", "youtube-captions"]}
query: youtube transcript pushed:>{since} stars:>20

# youtube-transcript-plus

[](https://badge.fury.io/js/youtube-transcript-plus)
[](https://github.com/ericmmartin/youtube-transcript-plus/actions/workflows/ci.yml)
[](https://scorecard.dev/viewer/?uri=github.com/ericmmartin/youtube-transcript-plus)

A Node.js library to fetch transcripts from YouTube videos. This package uses YouTube's unofficial API, so it may break if YouTube changes its internal structure.

**Note:** This project was originally forked from [https://github.com/Kakulukian/youtube-transcript](https://github.com/Kakulukian/youtube-transcript).

## Requirements

- Node.js >= 20.0.0 (Node 20.x reaches EOL in September 2026)

## Installation

```bash
$ npm install youtube-transcript-plus
```

or

```bash
$ yarn add youtube-transcript-plus
```

## Usage

### Basic Usage

```javascript
import { fetchTranscript } from 'youtube-transcript-plus';

// Fetch transcript using default settings
fetchTranscript('videoId_or_URL').then(console.log).catch(console.error);
```

### Custom User-Agent

You can pass a custom `userAgent` string to mimic different browsers or devices.

```javascript
fetchTranscript('videoId_or_URL', {
  userAgent:
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
})
  .then(console.log)
  .catch(console.error);
```

### HTTP Support

You can disable HTTPS and use HTTP instead for YouTube requests by setting the `disableHttps` option to `true`. This might be necessary in certain environments where HTTPS connections are restricted.

```javascript
fetchTranscript('videoId_or_URL', {
  disableHttps: true, // Use HTTP instead of HTTPS
})
  .then(console.log)
  .catch(console.error);
```

**Security Warning:** Using HTTP instead of HTTPS removes transport layer security and is not recommended for production environments. Only use this option when absolutely necessary.

### Custom Fetch Functions

You can inject custom `videoFetch`, `playerFetch`, and `transcriptFetch` functions to modify the fetch behavior, such as using a proxy or custom headers. The library makes three types of HTTP requests:

1. **`videoFetch`**: Fetches the YouTube video page (GET request)
2. **`playerFetch`**: Calls YouTube's Innertube API to get caption tracks (POST request)
3. **`transcriptFetch`**: Downloads the actual transcript data (GET request)

```javascript
fetchTranscript('videoId_or_URL', {
  videoFetch: async ({ url, lang, userAgent }) => {
    // Custom logic for video page fetch (GET)
    return fetch(`https://my-proxy-server.com/?url=${encodeURIComponent(url)}`, {
      headers: {
        ...(lang && { 'Accept-Language': lang }),
        'User-Agent': userAgent,
      },
    });
  },
  playerFetch: async ({ url, method, body, headers, lang, userAgent }) => {
    // Custom logic for Innertube API call (POST)
    return fetch(`https://my-proxy-server.com/?url=${encodeURIComponent(url)}`, {
      method,
      headers: {
        ...(lang && { 'Accept-Language': lang }),
        'User-Agent': userAgent,
        ...headers,
      },
      body,
    });
  },
  transcriptFetch: async ({ url, lang, userAgent }) => {
    // Custom logic for transcript data fetch (GET)
    return fetch(`https://my-proxy-server.com/?url=${encodeURIComponent(url)}`, {
      headers: {
        ...(lang && { 'Accept-Language': lang }),
        'User-Agent': userAgent,
      },
    });
  },
})
  .then(console.log)
  .catch(console.error);
```

### Language Support

You can specify the langu

## 14. [youtube] Why Cars Lose Their Value So Fast
key: yt:Ao7fbajRSKI
url: https://www.youtube.com/watch?v=Ao7fbajRSKI
meta: {"channel": "CNBC", "rank": 2}
query: car depreciation data analysis


[body unavailable: IpBlocked]
