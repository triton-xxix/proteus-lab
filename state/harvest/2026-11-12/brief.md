# Harvest brief, 2026-11-12

14 items shortlisted from 382 candidates (307 dropped as already seen, 9 carry a vault verdict on the vendor).

## 1. [vault] Paid trading community whose credibility rests on self-reported PnL screenshots and a legend it interviewed itself
key: vault:2026-09-20:paid-trading-community-whose-credibility-rests-on-self-repor
url: 
meta: {"vault_status": "intel", "kind": "service", "subject": "Potion Alpha (Orangie) and trader Kimchi", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-five-saved-items-gta6-pumpfun-potion-mev-calibriai.md (section 5)", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: No working leaderboard found; the trader legend traces to an interview by the community's own founder

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Paid Discord community ($599 a year) with self-reported PnL screenshots and no working leaderboard found. Kimchi's $40m TRUMP claim has no wallet behind it. Skip. Job: Find and follow traders whose edge is verifiable on-chain rather than claimed (still open)

## 2. [hn] Socratic Tutor
key: hn:50438261
url: https://github.com/janestreet/agent_skills/blob/master/socratic-tutor/SKILL.md
discussion: https://news.ycombinator.com/item?id=50438261
meta: {"points": 648, "comments": 153, "created": "2026-11-10T10:18:22Z"}
query: agent skills

comment (orbis-tertius): I love the idea but Jane Street might have copied (or independently rediscovered) https://github.com/bevibing/socrates-skill
comment (mathieuh): I assume this isn't going to cause the LLM to start jumping me with questions about the nature of piety or justice
comment (bob1029): This comes off as AI consultant slop from a year ago. I wonder who is in charge of AI at Jane Street. My client just got done firing someone who thought filling the codebase up with files like this would be a good idea. It would seem the AI revolution is happening at wildly different rates depending on where you are standing.

## 3. [github] agentes-chat/agentes-chat: Open-source, self-hosted Slack alternative where your team and AI agents work together in channels and DMs. Agents run on Claude, ChatGPT/Codex, Gemini or Grok, with MCP tools, their own computer and browser, routines, memory and approvals. Web, desktop and phone apps. Docker Compose + Postgres. AGPL-3.0.
key: gh:agentes-chat/agentes-chat
url: https://github.com/agentes-chat/agentes-chat
meta: {"stars": 1150, "created": "2026-11-09", "pushed": "2026-11-12", "language": "TypeScript", "topics": ["agentic-ai", "ai-agents", "browser-automation", "chat", "claude", "claude-code", "codex", "collaboration"]}
query: claude-code created:>{since} stars:>20

agentes.chat 

  The open-source, self-hosted Slack alternative where your team and AI agents work together.  

 
   Website  ·
   Cloud  ·
   Self-hosting  ·
   Features  ·
   Discussions 
 

 
     
     
     
     
 

 
   
 

Agents join your channels and DMs with a role, an owner and a budget, work where everyone can see,
and ask before anything sensitive. They think with Claude, ChatGPT and Codex, Gemini, Grok or any
OpenRouter model, use MCP tools, and get a computer and a browser of their own. Self-host it for
free with your own model keys, or use agentes.chat Cloud: both run this same codebase.

## Why agentes.chat

- **One conversation for people and agents.** Agents are members of the workspace, not a sidebar
  bot: they read the channel, answer when it's theirs to answer, and hand work back and forth.
- **Safe by default.** Merges, deploys and anything a connector marks sensitive wait for a person's
  approval in the chat. Every model call is budgeted and recorded per agent.
- **Agents that actually do the work.** Their own computer, a real browser you can watch and take
  over, Claude Code and Codex, routines on a schedule or an event, memory that learns.
- **Yours to run.** One command on a Linux server, Postgres as the only dependency, web, desktop and
  phone apps that connect to your server.

An open-source alternative to team chat with bolted-on AI bots, and to single-player agent apps such
as Grok Bot, ChatGPT dots, OpenBot.run and OpenMausBot (all of which it imports from).

## Quick start

- **Cloud:** sign up at [agentes.chat](https://agentes.chat).
- **Your own server** (Linux):

  ```sh
  curl -fsSL https://agentes.chat/install | sh
  ```

  It installs what's missing (Docker, after asking), and puts agentes.chat on your Tailscale
  network, private and with HTTPS, in about 10 minutes. [SELF_HOSTING.md](SELF_HOSTING.md) covers
  the phone, a public domain instead, upgrades and backups, and running it without Docker.

Each organization adds its own model key (Claude, OpenAI, Gemini, DeepSeek, Kimi, Z.ai, MiniMax or
OpenRouter) in the app.

## Features

| Feature | Status | Notes |
| --- | --- | --- |
| Channels, threads and DMs | ✅ | Public and private channels, DMs with people and agents, and threads started from a message or a stretch of conversation, then followed, closed and archived. |
| Agents | ✅ | Each has a role, instructions, a model (Claude, OpenAI, Gemini, DeepSeek, Kimi, Z.ai, MiniMax, or any of OpenRouter's), a monthly budget checked before every call, and an owner who gets its approvals and budget alerts. |
| Router | ✅ | A message nobody @mentioned goes to the router. Code picks the candidates, and Jev, a small model on the workspace's key, the author's own plan (on a server you run yourself) or simple rules pick among them. Up to four agents answer, or none, and the message says who picked. It never grants a permission. |
| Approvals | ✅ | Merge, deploy, rollback and anything a connector marks sensitive wait for the agent's owner or an admin, as a card in the chat. The approved action runs once, exactly as approved. |
| Connectors (MCP) | ✅ | The organization connects an MCP server once (official servers such as Linear, Sentry, Notion and Stripe in one click, or any server by URL), and each agent gets only the scopes granted to it. With a Composio key, Google Drive, Calendar, Sheets and Docs, Slack, Microsoft Teams, OneDrive, HubSpot, Salesforce, Zendesk, Asana, Figma, Intercom, Dropbox, Square, 

## 4. [arxiv] Controlled Knowledge Engineering for Taxonomy Induction with Tool-Grounded LLM Agents and Runtime-Adaptive Policies
key: arxiv:2611.13966
url: https://arxiv.org/abs/2611.13966
meta: {"published": "2026-11-10", "authors": ["Jonas Limniatis", "Bennet Schaarmann", "Georg Reuber", "Robert Stahlbock"], "categories": ["cs.IR", "cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Taxonomies are structured knowledge representations that support semantic search, recommendation, product catalog organization, and retrieval-augmented generation. Their automated construction from a fixed set of candidate entities requires more than plausible text generation: the resulting hierarchy must be complete, structurally valid, and semantically coherent. Large Language Models (LLMs) are promising for this task, but iterative free-form generation remains vulnerable to omitted or hallucinated entities, invalid hierarchical relations, and inconsistent organizational principles. We introduce TIGA (Taxonomy Induction with Tool-Grounded Agents), a knowledge-engineering architecture that formulates taxonomy induction as an iterative decision process over an explicit state and constrained action space. TIGA combines executable taxonomy-editing tools, an memory that records tool calls, rationales, and outcomes, and a runtime-adaptive organizational policy that the agent revises during inference. An optional global reviewer evaluates the constructed taxonomy against the candidate set and the active policy. We evaluate TIGA on four benchmark taxonomies using two LLM backbones and compare it with single-shot and iterative prompting-based baselines. TIGA achieves the strongest structural-quality results in most evaluated configurations, but does not dominate on every precision measure. The gains are accompanied by substantially higher token consumption, API-call volume, and inference time. Ablation results show consistent benefits from the policy and interaction-memory components, whereas the effect of global review depends on the dataset and the available revision budget. These findings characterize tool grounding and runtime policy adaptation as promising but costly mechanisms for improving the controlled construction of structured knowledge representations.

## 5. [youtube] 5 Claude Code Skills That Will Upgrade Your Development Workflow
key: yt:C-6UEA-SfkU
url: https://www.youtube.com/watch?v=C-6UEA-SfkU
meta: {"channel": "Codemyhobby", "rank": 4, "duration_min": 0}
query: claude code skills workflow 2026

# 5 Claude Code Skills That Will Upgrade Your Development Workflow
# Codemyhobby
# https://www.youtube.com/watch?v=C-6UEA-SfkU

[00:00] If you're a software developer, [music] here are five Claude code skills that can seriously upgrade your development workflow. First, [music] brainstorming. It helps Claude think through your project and create an implementation plan before writing code. Second, front-end design. This helps you build better-looking interfaces instead of getting generic AI generated UIs. Third, testdriven development. It gets Claude to write tests before implementing features, helping you catch issues early. Fourth, systematic debugging. Instead of randomly changing code,
[00:34] Claude investigates the actual root cause of a bug. And finally, security review. It helps identify vulnerabilities and security issues before you ship. comment skills and I'll share the links.

## 6. [vault] Promoter statistic that most wallets are profitable
key: vault:2026-09-20:promoter-statistic-that-most-wallets-are-profitable
url: 
meta: {"vault_status": "intel", "kind": "service", "subject": "pump.fun", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-five-saved-items-gta6-pumpfun-potion-mev-calibriai.md (section 4)", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: True but hides size; most winners made under 500 dollars, no bot filtering, unsold bags excluded

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) A real business (about $46m in fees over 30 days, roughly 90% of Solana launchpad activity) and a losing game for the people trading on it. Assessed as a business, not as an opportunity. Job: Let anyone launch a token and find real buyers without it being extraction from retail (still open)

## 7. [hn] Launch HN: Pomerado (YC F26) – Turn any website into an MCP for agents
key: hn:50455811
url: https://news.ycombinator.com/item?id=50455811
discussion: https://news.ycombinator.com/item?id=50455811
meta: {"points": 60, "comments": 47, "created": "2026-11-11T17:11:56Z"}
query: mcp server

Hi HN, we’re Alan and Akshay from Pomerado ( https://pomerado.ai/ ). We connect your agents to any website by turning sites into deterministic, self-healing APIs in minutes, fully self-serve. Agents are no longer limited by their intelligence, but rather by their ability to interact with systems. Airlines, banks, e-commerce, insurance portals, government sites, and legacy portals all lack APIs or MCPs and are common parts of personal assistant or business workflows. Agents instead rely on browser automation or computer use, which can be slow, expensive, and unreliable. And even if computer use were perfect, most companies have banned it out of security and compliance concerns. We discovered this problem while tinkering with our own personal assistants. When OpenClaw came out, we wanted to “live our lives through our agents” and have them do everything for us. We soon found their usefulness was restricted by what tools they could connect to. For example, when trying to book flights, they fell back on computer use, which failed to checkout. These issues got magnified on repeated workflows, like searching many airlines at once. Pomerado started off as a project to improve these personal assistant workflows. As we started building, we realized that just-in-time tool creation could have significant applications for AI builders in legacy verticals. We’re ex-McKinsey and Scale AI, where we drove agent deployments in healthcare, professional services, and telecom. Each time, the bigg
comment (hyperionultra): A wall of text. Just post video with a link to that wall of text for someone who is on to read gened strings.
comment (KallowayThayer): Curious how this handles session isolation and rate-limiting when converting dynamic DOM heavy pages into MCPs. If an agent hits a heavy SPA with infinite scroll or aggressive bot protection, does Pomerado handle edge-caching or proxy-level deduplication, or is it parsing raw DOM on every tool call?
comment (shipsafestack): How do you handle credentials and sessions for sites behind a login, like the bank and insurance portals you mention? Is the user's password or session cookie stored on your side, or does the generated MCP run against a session the user keeps locally? Related: page content is untrusted input that now flows straight into an agent's context. Do the deterministic tools return only structured fields you've extracted, or can arbitrary page text (reviews, messages, product descriptions) pass through? That seems like the main prompt-injection surface for anything that can also perform actions like ch

## 8. [github] threerocks/article2media: 把一篇文章或一条视频（抖音、B 站、YouTube，先转逐字稿）一键做成小红书图文、杂志长图、公众号排版和 AI 配音口播短视频的开源 Claude Code / Codex Skill。21 套主题，自动验收，零 npm 依赖。
key: gh:threerocks/article2media
url: https://github.com/threerocks/article2media
meta: {"stars": 288, "created": "2026-11-08", "pushed": "2026-11-11", "language": "JavaScript", "topics": ["agent-skills", "bilibili", "chinese", "claude-code", "claude-code-plugin", "claude-code-skill", "claude-skills", "codex"]}
query: claude-code created:>{since} stars:>20

# article2media

**把一篇文章或一条视频，做成能直接发的小红书图文、长图、公众号排版和口播短视频，并且知道哪一版效果更好。**

开源 Claude Code / Codex Skills · 抓取 · 视频转文字 · 改写 · 翻译 · 长图 · 小红书卡片 · 公众号排版 · 竖屏口播视频 · 原文排版 · 白板论证 · 漫画 · 批量与发布数据

[](CHANGELOG.md)
[](LICENSE)
[](#依赖)
[](#设计原则)
[](#安装)
[](#安装)

 

**article2media** 是一组开源的 Claude Code / Codex Skill，同时也是一个 Claude Code 插件。它把一篇文章或一条视频做成可以直接发布的中文视觉内容。

它由 **10 个独立能力**组成：文章抓取、视频转文字、改写（总结）、全文翻译、长图、卡片、公众号排版、口播视频、白板论证、漫画。每个能力都是一个 skill，可以单独用（比如只把自己写的文章排成公众号，或者只把视频转成文字），也可以自由组合。总入口 `/article2media` 提供常用的一键组合，以及批量处理和发布数据记录。

- **输入**：
  - 文章：X（Twitter）长文、网页、微信公众号文章，或本地 Markdown；
  - 视频：抖音、YouTube、B 站链接，本地视频或音频，`.srt` / `.vtt` 字幕。视频先转成逐字稿文章。
- **产出**：
  - 手机上直接能读的长图、小红书 3:4 图文卡片、可直接粘贴的公众号排版；
  - 带本地 AI 配音和逐字字幕的竖屏口播视频；
  - 同一篇的几版封面，以及一页看完、金句图、问答卡这些更轻的形态；
  - 一字不改的原文长图、原文卡片和原文公众号排版；
  - 中文全文译文、白板论证图和黑白漫画。
- **验收**：每种产出都自动检查，不合格就报错。
- **发布**：发布清单、备选标题、发布数据记录与对比报告。
- **依赖**：只需要 Node.js 22 和 Chrome。

  示例：Dan Koe 的 X 长文《The most lucrative AI business to start in 2027》。每种产出各用了一套主题，口播视频用的是「资讯播报男声」。 看示例视频  ·  听 6 款音色   

---

## 为什么做这个

好文章在信息流里很难被读完。把它做成图文或视频，通常要截图、排版、配图、配音、剪辑，几个小时才做完一个平台，换个平台还得从头再来。

article2media 把这件事交给 AI。你给一个链接，流程分三步：

1. Claude 先把文章**读懂**：要总结时重组成一份和风格无关的结构化内容，要原文时一字不动，要翻译时逐段译出；
2. 脚本把它**渲染**成各平台需要的格式；
3. 交付前**自动验收**，有问题直接报错，不靠人眼去找。

并不是每次都需要总结。自己写的文章只想排成公众号，或者想把全文做成小红书卡片，就直接排版，不经过改写。所以每一步都做成了独立的能力，按需要拼起来。

## 核心特性

| | |
|---|---|
| **能力独立，组合自由** | 抓取、视频转文字、改写、翻译、长图、卡片、公众号、口播、白板、漫画各是一个 skill，只靠工作目录里的文件交接。总入口给出常用组合，也可以说"先翻译，再出原文卡片"这样自己组装。 |
| **原文、总结、翻译三条路** | 原文路径一字不改，逐块读回比对；总结路径重组结构、配图表；翻译路径全文不删，脚本检查结构是否逐块对应。三条路都能接到长图、卡片和公众号。 |
| **文章和视频都能当原文** | 视频先转成逐字稿文章：人工字幕优先，其次平台的原语言自动字幕，都没有时用本地 Whisper 识别。繁体转简体、专有名词纠错、时间轴都会处理好，后面的流程和文章完全一样。 |
| **先读懂，再排版** | 不是截图，也不是机械摘要。Claude 规划结构、改写标题、挑选图表、核对数字，产出只含内容的 `content.json`。版式和主题由脚本负责，换风格不用重写内容。 |
| **一份内容，多种产出** | 一次改写，同时出长图、卡片（3:4 / 4:5 / 1:1 / 9:16）和公众号，还能切出一页看完、金句图、问答卡；口播视频、白板、漫画另有专门的脚本。12 套主推主题对所有图文产出通用，口播视频沿用主题的配色、字体和卡片样式。 |
| **为信息流的第一眼设计** | 封面有 6 种版式（大字钩子、大数字、左右对比、一句论断、插画通栏、目录），可以一次出几版来挑。一组卡片里穿插整页金句、整页大数字和整页图，不再张张同一个结构。卡片自己把空间用满：图表按内容放大，有余量就放大字号、补要点。 |
| **手机上直接能读** | 长图默认是 1080 宽的单栏手机版，正文不用放大；需要电脑上看或打印时，`--wide` 出 1200 宽的双栏杂志版。 |
| **认得出是谁的** | 品牌包把头像、品牌色、期号和一行介绍带到封面、末张和长图页脚，做成系列。 |
| **发出去之后也管** | 批量处理一批链接、给每篇生成发布清单和备选标题；发布后把数据记下来，按平台对比哪种主题、哪种封面效果更好。 |
| **每种产出都有验收** | 版面检查溢出、截断和重叠。原文长图、原文卡片、公众号排版都逐块读回比对，改一个字就失败。翻译检查块数、结构、漏译和数字。白板要求每段原文都有去向。视频审片检查首句时长、画面静止、语速、字幕闪断、成片逐帧的字幕丢帧和响度。字体按家族检查，没加载的会点名。改写稿还会和原文逐项比对：数字有没有出处、别人的文章有没有写成"我"、原文的具体信息用上了多少。不合格就以非零码退出。 |
| **换模型也心里有数** | 自带换模型回归测试：同样的提示交给不同模型，用客观分和盲评对比。实测较小的模型（Haiku）规则层面能追平 Opus，读者效果约为 Opus 的 88%，详见[常见问题](#换一个模型来驱动效果稳定吗)。 |
| **视频质量达到能发布的水准** | 本地 VoxCPM2 生成 48 kHz 配音，Whisper 逐字对齐，数字和要点在说到的那一刻出现。语速按从容讲解控制在约 4.5 字/秒。字幕不闪烁，样式跟随主题。镜头里可以放 AI 插画或原视频片段，可以加你自己的背景音乐。 |
| **版权与合规写进流程** | 随包 6 款音色全部只凭文字描述设计，不模仿任何真人。克隆音色只留在本机，使用时会提醒。成片首帧和 MP4 元数据都带 AI 生成标识，产出都署原文出处。 |
| **零依赖，本地优先** | 只需要 Node 22 和一个 Chrome。出图、本地配音、逐字对齐都是可选能力，会自动探测。缺了就降级或明确提示，不会自动下载或安装任何东西。主题字体可以一条命令下载到本地，之后出图不联网。 |

## 快速开始

**1. 安装**（推荐 Claude Code 插件，一次装好全部 11 个 skill；其他方式见[安装](#安装)）

```bash
claude plugin marketplace add threerocks/article2media
claude plugin install article2media@article2media
```

**2. 检查环境**

```bash
bash scripts/install.sh      # 在仓库里：Node、Chrome、字体，以及做视频要的配音、对齐、出图、ffmpeg
node skills/article2media/scripts/fonts.mjs    # 可选：把主题字体下载到本地（约 65 MB，可加 --mirror  ），之后出图不再联网加载字体
```

装成插件后，第一次使用时 skill 会自己跑环境检查。

**3. 在 Claude Code 里调用**

一键组合用总入口：

```
/article2media https://x.com/thedankoe/status/2117664712532123680       # 总结长图（默认）
/article2media https://ex

## 9. [arxiv] From Attack Surface to Defense Architecture: Compositional Security for Agentic Coding Harnesses
key: arxiv:2611.13960
url: https://arxiv.org/abs/2611.13960
meta: {"published": "2026-11-10", "authors": ["Simon Hegelich", "Bardh Prenkaj", "Habiba Sarhan", "Morteza Shahrezaye"], "categories": ["cs.CR", "cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

AI coding harnesses couple language models to shells, filesystems, and network sockets, turning the harness into an automated Living-off-the-Land (LotL) platform: once an adversary injects instructions into retrieved content, dual-use binaries such as bash, curl, and find become the payload. We argue that security in agentic systems is a structural property of the cognitive architecture and permission composition rather than an emergent property of individual models. Static regex blacklists miss structural evasions, whereas LLM-as-a-Judge guardrails incur high latency while over-blocking benign work. We present ActiveSecHarness, a neurosymbolic reference-monitor architecture built around Separation of Intelligence and Authority. It combines (1) Macaroon-inspired HMAC capability tokens across four Trust and Authority Rings, (2) a 2D product taint lattice $\mathcal{L} = \mathcal{L}_{\mathrm{trust}} \times \mathcal{L}_{\mathrm{sens}}$ and a workspace provenance ledger that prevents secret laundering across disk, (3) deterministic Ring-0 OS/tool guards, and (4) bytecode certificates, split-horizon audit logs, self-healing security test synthesis, and an adaptive UserWikiManager. Across $N=252$ fixtures ($120$ attack, $120$ benign, $12$ kill chains), a live local LLM judge (qwen3:4b) refuses $98.3\%$ of benign work at $142.3\,\mathrm{ms}$ latency, whereas Ring 0 achieves $\mathrm{ABR}=1.000$ and $\mathrm{FPR}=0.000$ in $12.7\,μ\mathrm{s}$ ($11{,}200\times$ faster). In a multi-step trajectory ablation, an oracle Conseca-style stateless policy misses $4/12$ kill chains ($\mathrm{ABR}=0.667$) and coarse Boolean taint blocks $83.3\%$ of benign workflows, while our 2D product lattice achieves $\mathrm{ABR}=1.000$ and $\mathrm{FPR}=0.000$ at $\approx 20\,μ\mathrm{s}$ per step.

## 10. [youtube] Python 3.16 Just Dropped — And an AI Crashed 3.15 in 5 Lines
key: yt:_EnL_XvlI-0
url: https://www.youtube.com/watch?v=_EnL_XvlI-0
meta: {"channel": "Art of Data Science", "rank": 4}
query: dixon coles model python


[body unavailable: TranscriptsDisabled]

## 11. [vault] proven content formats per client
key: vault:2026-10-05:proven-content-formats-per-client
url: 
meta: {"vault_status": "intel", "kind": "scheme", "subject": "OFM Conquest (Skool, Dylan Beese) - 6 and 7 figure interviews", "date": "2026-10-05", "where": "TRITON-CORE/Education/Courses/ofm-conquest/TAKEAWAYS-interviews.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: the most cited lever; plan the format set before launch, repeat what pops

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) Free classroom plus 13 seller-run testimonial interviews, a funnel for the paid partnership; figures are unverified gross inflow. Useful as agency-operations intel, not as proof of returns.

## 12. [hn] Show HN: AgentRun – open-source, Self-improving Managed Agents
key: hn:50471650
url: https://github.com/Parcha-ai/agentrun/blob/main/README.md
discussion: https://news.ycombinator.com/item?id=50471650
meta: {"points": 70, "comments": 11, "created": "2026-11-12T18:15:48Z"}
query: claude code

We (GREP.AI, YC F26) are open-sourcing AgentRun and turning it into a full managed agents platform. Read more about it in this post: https://agentrun.ai/blog/introducing-agentrun-run-smarter-ag... . It includes what we originally built for our own agent harness: - Self-improving agents - Web-grounded workflows - A range of sandboxes and computer environments - Thousands of tools and integrations - Detailed analytics on how your agents behave You can bring your own agent. AgentRun works with Pi, Claude Agents, Codex, OpenCode, and any other harness that supports ACP. You can self-host it (see 1-click install on Render) with an OpenRouter key, or try the hosted version at console.agentrun.ai. We’d love feedback, especially on the architecture (see README), or anything we may be missing to make it useful to you.
comment (jstummbillig): I think I'll need like at least another 3-4 months of new models before I can deal with AI UI/UX design.
comment (Rinkesh2010rpp): Cool project, I myself have a similar autonomous agent, in python At rinkesh2010rpp/sudarshana. But I liked your mission control. Will for sure take some inspiration. Also, what I have is ability to find other agents on run time, running on Modal, and a safety layer that checks every actions taken by the agent. and happy to talk more. Thanks
comment (mfrye0): Very cool. I was waiting for something like this to pop up. Is it possible to be added as a data source? I see you're mostly pointing the agent to easy / publicly available sources like the UK. We have ~200 government registrar integrations now and 500M entities in the system. We essentially have better coverage than OpenCorporates at this stage. https://savvyiq.ai

## 13. [github] ersinkoc/phonebox: Turn an old Android phone into a local desk panel for Windows, Linux and macOS. 55 widgets, Smart Stack, AI quotas and sessions, media controls, USB or paired Wi-Fi.
key: gh:ersinkoc/phonebox
url: https://github.com/ersinkoc/phonebox
meta: {"stars": 247, "created": "2026-11-07", "pushed": "2026-11-11", "language": "C#", "topics": ["android", "claude-code", "codex", "dashboard", "desk-panel", "dotnet", "linux", "macos"]}
query: claude-code created:>{since} stars:>20

PhoneBox 

  Turn an old Android phone into a desk panel for your computer: Windows, Linux or macOS.  
Widgets for your PC, AI coding sessions, music, weather and anything you push to it. USB or Wi-Fi, no cloud. 
  ▶ Try the live demo in your browser   

 
     
     
   
   
     
 

   

PhoneBox has two parts: a small **Android app** that runs full screen on the phone, and an **agent** on the computer
(Windows, Linux or macOS) that feeds it over the USB cable (or over Wi-Fi / Tailscale after pairing once). You design
the pages in a visual editor on the PC: **113 widgets**, **30 templates**, as many pages as you like.

- **Your PC at a glance**: CPU, GPU, RAM, disks, network and ping; the heaviest apps, with "end one instance / end all".
- **AI coding**: Claude and Codex quotas with a burn-rate forecast; Codex remaining allowance and local session token details; tap a session to see its model, timing, tokens, context window and recent tool — the phone
  buzzes when one finishes or needs you, and Claude Code's permission prompts show up with **Allow** / **Deny**.
  GitHub review requests and your pull requests with CI status.
- **Desk companion**: now playing with controls and volume, clocks, weather, sun & moon, air quality, calendar,
  pomodoro, timers, checklists, notes, a breathing exercise.
- **Stream Deck–style keys** that launch apps, URLs or built-in actions on the PC.
- **Webhooks and rules**: scripts, CI and Home Assistant push values and notifications; rules switch pages calmly
  when something happens (a call, music, an AI session waiting for you).

     
 A tour through the pages (made-up data): a notification, a permission prompt, a rule switching pages calmly.  Video (MP4)   

**Contents**: [Quick start](#quick-start) · [Pages & templates](#pages--templates) · [Widgets](#widgets) ·
[Layout editor](#layout-editor--settings) · [Claude Code prompts](#claude-code-permission-prompts) · [Webhooks](#webhooks) · [Rules](#rules) · [Wi-Fi & Tailscale](#wi-fi--tailscale) ·
[Updates](#updates) · [How it works](#how-it-works) · [Security](#security--privacy) · [FAQ](#faq--troubleshooting) ·
[Development](#development)

## Recent highlights

The [changelog](CHANGELOG.md) lists every release. Some of the larger additions:

### Control Deck, appearance and Podman (0.8 – 0.9)

58 [Control Deck](docs/CONTROL-DECK.md) widgets (audio, media, OBS, tasks, displays), optional
[appearance](docs/APPEARANCE.md) presets for the panel, pages and widgets, Podman containers, and pages that wrap
around when you swipe past the last one.

### Android 9 and 10 (0.7.3)

Fixes an immediate launch crash on Android 9 and 10. Full-screen mode now uses the compatible immersive API on
these versions; Android 11+ keeps the existing behavior. Android API compatibility lint now blocks CI and releases.

### Native Antigravity quotas (0.7.2)

Native Antigravity quota monitoring now works without CodexBar, including signed-in `agy` CLI installations on
Windows. Session and weekly usage come from measured quota data; missing readings are not shown as unused quota.
See [native Antigravity quotas](#widgets) and the [changelog](CHANGELOG.md) for setup and compatibility details.

### Smart Stack and session details (0.7.0)

| Smart Stack and quotas | Codex session details |
|---|---|
|  |  |

These screenshots use made-up demo data. See the [changelog](CHANGELOG.md) for all changes.

## Quick start

**[Download the latest PhoneBox release](https://github.com/ersinkoc/phon

## 14. [hn] How do you keep up quality when you vibe-code?
key: hn:50444380
url: https://news.ycombinator.com/item?id=50444380
discussion: https://news.ycombinator.com/item?id=50444380
meta: {"points": 37, "comments": 37, "created": "2026-11-10T18:41:15Z"}
query: claude code

I'm having a really hard time working with claude. In the past when I wrote all the code manually, it was always carefully reviewed and architected, with all possible flows carefully mapped out. Now, my code is mostly AI written which has led to things going out of control. Since it's easy to add new features and support many user flows, we went ahead and implemented flows that support a lot of cases our users run into. But now, I feel like things are getting too complex with no central notion of behaviour definitions, which causes every bug-fixing session to feel like a game of whack-a-mole, and results in missing edge cases and UI bugs that are becoming impossible to review and keep track of. Every time I build anything new, it adds more complexity and the agent only seems to focus on the surrounding code within that session without keeping track of how it fits into the rest of the code base/product. How do you all deal with this? Any suggestions for improving?
comment (toufiqqureshi): The same I was facing now I have built complete app but always worried about it is really protected and production ready I also facing this issue I don't know what to do
comment (Marco012): I'm not sure if there is any standard for this, I also tried to search about it in the past. But what I ended up doing that has been working well is to keep everything documented. Every task and decisions are documented on .md files, referencing related tasks and decisions. The project becomes bloated quickly, but Claude can easily locate and relate decisions from a long time ago. Some times I even ask to do do something and mid-way Claude realizes that it goes against a previous written decision.
comment (mpd): I've always been a bottom-up programmer, so I tend to think more about discrete operations of software rather than the user-facing features (which IME will fall out naturally). 1. Experiment and solidify architecture before adding features. I think this is the hardest step for top-down thinkers. 2. Heavy testing and benchmarking. Prefer to TDD as much as possible. The actual lines for my agent-written codebases are generally ~70+% tests, benchmarks, and experiments. 3. Full mutation test coverage after the code is written. Doing this as a human is miserable IMO, but robots make it reasonable. 
