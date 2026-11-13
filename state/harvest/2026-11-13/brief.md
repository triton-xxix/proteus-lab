# Harvest brief, 2026-11-13

14 items shortlisted from 383 candidates (305 dropped as already seen, 10 carry a vault verdict on the vendor).

## 1. [vault] Gemini Omni blocks uploaded video edits for UK accounts and Seedance rejects real human faces
key: vault:2026-10-01:gemini-omni-blocks-uploaded-video-edits-for-uk-accounts-and-
url: 
meta: {"vault_status": "intel", "kind": "tool", "subject": "AI video tool stack as of October 2026 (Veo, Nano Banana, Seedance, Kling, MiniMax H3, Wan, HeyGen, fal)", "date": "2026-10-01", "where": "TRITON-CORE/Systems/video-bootcamp/STACK.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: (none)

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Checked on vendor pages 1 Oct while building the video framework. We already hold enough to draft most work by API: Veo 3.1 and the Nano Banana image models on a Gemini key, ElevenLabs for voice and sound, HyperFrames for the edit. The course picks have aged: MiniMax H3 and Wan 3.0 now out-rank Kling 3.0 and Veo 3.1 for image to video, Nano Banana 2 out-ranks Pro at half the price, Gemini Omni cannot edit uploaded video from the UK, and Seedance refuses real faces, so a real person on screen is a HeyGen job. Job: choose a draft route and a final route for each video job (solved)

## 2. [hn] Elevated errors on claude.ai, Claude Code, and platform.claude.com
key: hn:50481187
url: https://status.claude.com/incidents/nn11wk485zfn
discussion: https://news.ycombinator.com/item?id=50481187
meta: {"points": 480, "comments": 380, "created": "2026-11-13T10:18:13Z"}
query: claude code

page: Claude Status - Elevated errors on claude.ai, Claude Code, and platform.claude.com Elevated errors on claude.ai, Claude Code, and platform.claude.com Incident Report for Claude Resolved The issue affecting claude.ai and Claude Cowork has been resolved. Posted Nov 13 , 2026 - 11:58 UTC Monitoring A fix has been deployed for the issue affecting Claude services and we are monitoring for recovery. Posted Nov 13 , 2026 - 11:05 UTC Investigating We are investigating an issue with users authenticating to Claude.ai and Claude Code. We will provide an update as soon as possible. Posted Nov 13 , 2026 - 09:58 UTC This incident affected: claude.ai, Claude Console (platform.claude.com), Claude Code, and Claude Cowork. ← Current Status Powered by Atlassian Statuspage × Subscribe to Incident Subscribe to updates for Elevated errors on claude.ai, Claude Code, and platform.claude.com via email and/or text message. You'll receive email notifications when incidents are updated, and text message notifications whenever Claude creates or resolves an incident. VIA EMAIL: VIA SMS: Afghanistan (+93) Albania (+355) Algeria (+213) American Samoa (+1) Andorra (+376) Angola (+244) Anguilla (+1) Antigua and Barbuda (+1) Argentina (+54) Armenia (+374) Aruba (+297) Australia/Cocos/Christmas Island (+61) Austria (+43) Azerbaijan (+994) Bahamas (+1) Bahrain (+973) Bangladesh (+880) Barbados (+1) Belarus (+375) Belgium (+32) Belize (+501) Benin (+229) Bermuda (+1) Bolivia (+591) Bosnia and Herzegovina (+387) Botswana (+267) Brazil (+55) Brunei (+673) Bulgaria (+359) Burkina Faso (+226) Burundi (+257) Cambodia (+855) Cameroon (+237) Canada (+1) Cape Verde (+238) Cayman Islands (+1) Central Africa (+236) Chad (+235) Chile (+56) China (+86) Colombia (+57) Comoros (+269) Congo (+242) Congo, Dem Rep (+243) Costa Rica (+506) Croatia (+385) Cyprus (+357) Czech Republic (+420) Denmark (+45) Djibouti (+253) Dominica (+1) Dominican Republic (+1) Egypt (+20) El Salvador (+503) Equatorial Guinea (+240) Estonia (
comment (AndrewSwift): Yep, one instance can't connect, and one instance seems to have crashed but is pretending to keep working (Toulouse, France) 3 minutes later... I can reconnect, and the "crashed" instance woke up.
comment (aiaco): faaaaahhhh
comment (gregman1): Let the weekend start! Tech sabbatical is kinda enforced now =D

## 3. [github] op7418/guizang-game-skill: 歸藏 Game Skill：让 AI 从零做出能在浏览器里玩的 3D 动作游戏，附可玩演示《雾锁山门》。Agent skill for Claude Code / Codex that builds a playable browser 3D action game with AI-generated assets (three.js, single-HTML). Playable demo included.
key: gh:op7418/guizang-game-skill
url: https://github.com/op7418/guizang-game-skill
meta: {"stars": 311, "created": "2026-11-11", "pushed": "2026-11-11", "language": "JavaScript", "topics": ["3d-game", "action-game", "agent-skills", "ai-agents", "ai-generated", "browser-game", "claude-code", "claude-skills"]}
query: claude-code created:>{since} stars:>20

# 歸藏 Game Skill

**让 AI 从零做出一个能在浏览器里玩的 3D 动作游戏**

[English](README.en.md) · 简体中文

[](https://op7418.github.io/guizang-game-skill/)
[](LICENSE)
[](https://github.com/op7418/guizang-game-skill/stargazers)

   

*上面这段是演示游戏《雾锁山门》里的实机画面。[点这里直接玩](https://op7418.github.io/guizang-game-skill/)，电脑和手机都能打开，不用安装。*

 

---

## 这是什么

一个给 AI 编程助手（Claude Code、Codex 等）用的 Skill。装上之后，对它说"做一个武侠题材的俯视角 3D 动作游戏"，它会按一套走通过的流程去做：先问清楚你要什么，接上你手头的素材生成工具，自己推进画面、自己截图核对，最后把游戏打包成一个网页文件。

Skill 里写的不是理论，是我用 Fable 5.2 花一个下午做出《雾锁山门》的过程中踩过的坑，和最后留下来的做法。那次大约 6 小时、4.5 亿 Token（其中一部分是 Opus 5.5 跑的测试），很多都花在了返工和试错上。这个 Skill 的目的就是让你和你的 AI 少走这些弯路。

## 演示游戏：雾锁山门

 
 
   
 

一个仙侠题材的俯视角 3D 动作游戏：一个场景、一段小怪遭遇战、一场 Boss 战，有剧情和配音。**所有创意都是 AI 自己定的**，我只说了要做国风仙侠。

- **画面**：大片随风起伏的草，分层的雾、雪和远山，覆水石台上的反光。渲染流程是在 three.js 上自己搭的，只用兼容性最好的 WebGL，所以手机、电脑、小程序类容器里都能跑
- **角色与场景**：5 个带骨骼的 3D 角色、2 把武器、12 种场景道具、5 种掉落物。先用即梦出设定图，再用 Tripo 转成模型，提示词都是 AI 自己写的
- **战斗**：三段连招、闪避、格挡、弹反、处决，还有饮药、御剑和大招"万剑归宗"。Boss 有二阶段、起身过场和台词
- **声音**：8 条配音、配乐、环境音和音效
- **体积**：原始素材将近 100MB，打包后是一个约 33MB 的 HTML，里面包含全部模型、贴图、音乐和配音

 
 
 

 
 
   
   
   
 
 
 三段连招 
 剑诀 
 万剑归宗 
 
 

演示的三种形态，都是同一份源码打出来的：

| 形态 | 说明 |
|---|---|
| [在线版](https://op7418.github.io/guizang-game-skill/) | 先渲染出场景再边跑边加载；手机有触屏摇杆和按钮；设置里可以调画质、换高清材质、改按键 |
| 单文件版 | 一个约 33MB 的 HTML，没有任何网络请求 |
| 小程序容器版 | 按小红书小工具的限制（不能联网、不能用 WASM、包体 10MiB）单独构建，约 8MiB |

## 这个 Skill 帮你做什么

直接让 AI"做个 3D 游戏"，通常会得到一个方块灰模、手感发飘、要自己搭环境才能跑的东西。装上这个 Skill 之后：

1. **开工前先问清楚**。参考、视角、氛围、范围，以及你手头有哪些素材工具和多少额度。它不会闷头写一个方块模型出来，上来就把你给的工具接上
2. **自己验证，不用你反复试**。第一天就装好自测工具：逐帧推进画面、直达某一关的网址参数、F3 诊断面板。它自己截图核对，再告诉你哪些看过、哪些只是没报错
3. **战斗手感有章可循**。出招前摇和后摇、命中顿帧、分级击退、格挡与弹反、敌人轮流进攻而不是一拥而上、闪避能打断动作。打击感从哪来，都写进去了
4. **一份踩坑清单**。方向键卡住、预设动画把角色甩离原地、泛光过曝、镜头被屋顶挡住、打包后角色缩小一半……每条都有症状、原因和做法
5. **三种打包方式**。把很大的模型和素材压到很小：单个 HTML、先出画面再加载的静态站点、受限容器的离线包

## 安装

把这个仓库的链接发给你的 AI，让它安装即可。或者手动：

```bash
git clone https://github.com/op7418/guizang-game-skill ~/.claude/skills/guizang-game-skill
```

Codex 等其它工具，克隆到它们各自的 skills 目录。

然后直接说需求，比如：

```
做一个武侠题材的俯视角网页 3D 动作游戏，一个场景、一波小怪、一个 Boss。
我有 Tripo 和即梦可以用。
```

## 需要准备

| 东西 | 用途 | 没有的话 |
|---|---|---|
| Node.js 18+ | 本地服务器和打包 | 必需 |
| [Tripo](https://www.tripo3d.ai/) | 图片转 3D 模型、骨骼绑定 | 改用免费模型和程序化几何体，画面会打折扣 |
| [即梦](https://jimeng.jianying.com/) 或其它出图工具 | 角色设定图、图标、题字、配音 | 改用免费素材 |
| [Suno](https://suno.com/) | 配乐 | Skill 会写好提示词给你，或用程序生成的配乐 |

素材工具对最终效果影响很大。我一开始让它直接用文字生成模型，质量很差；改成"先出设定图，再转 3D"之后上了一个大档次。

## 流程

```
调研与规划 → 设定与素材 → 动作 → 手感与特效 → 声音与打包
```

1. **调研与规划**：读参考、查这类游戏的做法，写调研文档和分阶段计划
2. **设定与素材**：世界观、角色设定图、图转 3D、骨骼绑定
3. **动作**：平台给的预设动作不多，其余用程序算出每个姿势里手脚的位置
4. **手感与特效**：按战斗手感清单逐项做，特效走"网格 + 着色器"而不是堆粒子
5. **声音与打包**：音效、配音、配乐，然后压缩并打成单文件

## 目录

| 路径 | 内容 |
|---|---|
| [`SKILL.md`](SKILL.md) | 整体流程和每个阶段的检查点 |
| [`references/assets.md`](references/assets.md) | 素材生成与免费素材来源 |
| [`references/characters-animation.md`](references/characters-animation.md) | 角色、骨骼与动画 |
| [`references/combat-feel.md`](references/combat-feel.md) | 战斗手感 |
| [`references/vfx-ui-audio.md`](references/vfx-ui-audio.md) | 特效、界面与声音 |
| [`references/pitfalls.md`](references/pitfalls.md) | 踩坑清单 |
| [`references/packaging.md`](references/packaging.md) | 体积优化、单文件打包、在线托管、手机与受限容器 |
| [`scripts/`](scripts) | 可直接复用的输入处理、本地服务器、三种打包脚本 |

## 先说清楚的事

- **它不是一句话出成品**。《雾锁山门》我试玩了 7 轮，每轮提 5 到 10 个问题。我不懂做游戏，只会说"动作很僵硬""打击感很差"，AI 会把这些话翻译成专业做法去查、去改。你仍然需要来回试玩提意见
- **几件事我会坚持让 AI 做**：给它参考视频；要求"先调研再动手"；别让它自己造轮子，把现成的素材工具接上
- **Skill 目前只在一个项目上完整走过一遍**，另做过一次计划层面的对照测试。它能让方向少走弯路，不保证成品质量

## 许可

- **Skill 本身**（本仓库 `main` 分支的文档与脚本）：[AGPL-3.0](LICENSE)
- **演示游戏《雾锁山门》的内容**（美

## 4. [arxiv] CapLite: Prompt-Injection Defense for Small Language Model Agents without Model-Written Security Artifacts
key: arxiv:2611.17115
url: https://arxiv.org/abs/2611.17115
meta: {"published": "2026-11-12", "authors": ["Zimo Xu", "Wenzhuo Liu", "Hideki Nakayama"], "categories": ["cs.AI", "cs.CL", "cs.CR"]}
query: all:"language model" AND all:agent AND all:tool

Enforcement defenses against prompt injection, such as CaMeL, Progent, IPIGuard and DRIFT, ask the agent's own model to write a security artifact (a program, a privilege policy, a dependency graph or a constraint list) that code then enforces. We ask whether small language model (SLM) agents can be trusted to write these artifacts. Across 15 open-weight models, 13 of them between 1.7B and 12B parameters, they cannot: the policies, graphs and constraints that the agent's model writes admit attacks on 14 (Progent), 13 (IPIGuard) and 11 (DRIFT) of the models, and CaMeL's programs fail to run in up to 68% of episodes. We present CapLite, which derives its policy from the tool schemas, commits the write calls before any tool result is read, and admits a write only if every argument that decides whom or what it affects is stated in the user's request. This guarantees write integrity: injected text cannot add a write, and no write reaches a recipient, amount, object or destination that the user did not state. No attack succeeds in 13,935 attacked AgentDojo episodes. CapLite reaches utility under attack comparable to CaMeL's (29.0% vs. 27.2%) with fewer tokens than every other enforcement defense and than the undefended agent: 17.1k per episode, 18% of CaMeL's, and the highest utility per token of all enforcement defenses.

## 5. [youtube] PumpFun Sniper Bot Guide! | How to Use Solana Sniper Bot! | Solana Trading Crypto
key: yt:7uUo9g318sc
url: https://www.youtube.com/watch?v=7uUo9g318sc
meta: {"channel": "Memecoins Developer", "rank": 2, "duration_min": 6}
query: pump.fun sniper bot how it works

# PumpFun Sniper Bot Guide! | How to Use Solana Sniper Bot! | Solana Trading Crypto
# Memecoins Developer
# https://www.youtube.com/watch?v=7uUo9g318sc

[00:00] What's up, guys? Today, we've got something really hot. I came across a tool that people in the crypto community are already talking about a lot. And honestly, after digging into it myself, I understand why. This is the Salana Sniper Bot, a sniper trading bot for Salana and Pump Fun. And today, we're not just doing a review, we're trading live. You'll see everything with your own eyes. How it works, how fast it reacts, and what happens to the account after several trades. Let's go. So, we open the website and from the
[00:32] very first seconds, you can tell this isn't some quickly thrown together project. Everything is clean, fast, and the navigation is intuitive. Look at the numbers right on the homepage. More than 100,000 successful trades, 99.9% uptime, and pay attention, response time under 10 milliseconds. That's literally faster than you can blink. The rating is 4.9 out of five. And it's not just a number on the website. Trustpilot shows 4.7 real people, real reviews. Right now, almost 917 traders are trading online and the volume is $3.2 million.
[01:07] This is not a toy, but enough looking at pretty numbers. Let's trade. Before launching the bot, we need to configure it. And this is the part I really liked. Everything is extremely simple, even if it's your first day in crypto. Look, we set the minimum investment per trade and the maximum. That's your risk management directly in the interface. No magic. You decide how much to risk. Next, slippage tolerance, meaning the acceptable slippage. Take profit. We set a profit target and the bot will close the position automatically when it reaches
[01:39] it. Stop loss in case the market moves the wrong way. And max dev hold. This protects you from tokens where the developers hold too large a share. Smart, right? We turn on autoell and the bot runs fully automatically. Click save configuration. Son, and that's it. The strategy is saved. By the way, on the right side, it immediately shows a preview of the strategy, the risk level, and the target profit. Everything is right there. All right, let's launch the bot. We go to the trading section, and here it is, a live dashboard. We connect the wallet.
[02:13] Look how fast everything works. The bot is already scanning the market. Literally a few seconds after launch, the first trade. Boom. Entered a position faster than I could finish the sentence. That's what a response time under 10 milliseconds means. You're not competing with people. You're competing with other bots. And this one is among the fastest. Oh, here we go. First trade, profit. Second one, also green. Look how it works. Trade after trade. Non-stop. This isn't randomness. It's an algorithm that selects only promising tokens. Wait, look. The bot found a token but didn't enter. That's not a
[02:47] bug. That's AI protection in action. Pump Fun Sniper uses artificial intelligence to automatically filter out scams, rugpool projects, and honeypot traps, situations where you buy but can't sell. The bot checks all of this before entering a trade. That's why there are so many successful trades here. It simply avoids entering positions where money could be lost. This isn't luck, it's a system. While the bot is trading, uh let's quickly look through the other sections of the website because there are some interesting things there
[transcript continues in field-notes/staging/7uUo9g318sc.txt]

## 6. [vault] outbound with follow-ups
key: vault:2026-10-05:outbound-with-follow-ups
url: 
meta: {"vault_status": "intel", "kind": "scheme", "subject": "OFM Conquest (Skool, Dylan Beese) - 6 and 7 figure interviews", "date": "2026-10-05", "where": "TRITON-CORE/Education/Courses/ofm-conquest/TAKEAWAYS-interviews.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: daily tracked outreach, up to ten touches before a reply; never rely on referrals alone

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) Free classroom plus 13 seller-run testimonial interviews, a funnel for the paid partnership; figures are unverified gross inflow. Useful as agency-operations intel, not as proof of returns.

## 7. [hn] Show HN: Kapso – Iterative learning from enterprise data
key: hn:50471281
url: https://news.ycombinator.com/item?id=50471281
discussion: https://news.ycombinator.com/item?id=50471281
meta: {"points": 58, "comments": 13, "created": "2026-11-12T17:51:23Z"}
query: open data api

Hey HN! We're Alireza and Majid building Leeroo ( https://leeroo.com/ ). Previously we’ve built AI systems for products with millions of users, including at LinkedIn and Meta. We’re now focusing on building AI systems for enterprise data. Today, we're open-sourcing Kapso ( https://github.com/Leeroo-AI/kapso ), an engine that runs experiments, deploys the best solution, and learns from every run. The nature of data work is iterative: investigate, form hypotheses, experiment, and improve based on what you learn. This bottom-up process is the only way to deliver meaningful outcomes quickly in large, messy enterprise data environments. Consultants gathering context in meetings or teams defining a business ontology upfront to fit into the data has no chance of execution, in quarters and sometimes years. An AI-native system should automate this process, compounding learning to each new investigation and implementation. For instance, one of our enterprise projects was moving a company off its old data estate onto a lakehouse with more than 30 source-system families, thousands of tables and transformations, and hundreds of BI reports. No individual or AI agent knew how that data estate was connected and operated. The only way to learn it was to investigate the company's repos, dbt models, documentation, and data itself and propose hypotheses about the estate, run experiments, and learn from them, until we understand how each system behaves and under which conditions. The iterative wo
comment (granthamctaylor): Over at https://relflow.ai (an OSS model factory) used Kapso to help harness an HPO loop on RelArena. RelArena is like RelBench, but is maintained and regulated by Prior Labs to isolate data leakage that can taint modern benchmarks. Kapso was able to efficiently calibrate Relflow's hyperparameters on 21 structured data modeling tasks, and we were able to outperform TabPFN on the majority of the larger data modeling tasks despite not using any ICL, and using ~1% of the number of params of TabPFN.
comment (fcortes): FYI, you may want to reconsider the naming as there's already a fairly popular service named Kapso [1] for integrating WhatsApp into other products (not related btw). [1] https://kapso.com/

## 8. [github] Moh4696/cinematic-skill: Agent skill for narrated cinematic films built entirely from code: one continuous camera over photos, maps and cards, timed to the voice. Claude Code, Codex, Cursor, Gemini CLI.
key: gh:moh4696/cinematic-skill
url: https://github.com/Moh4696/cinematic-skill
meta: {"stars": 284, "created": "2026-11-09", "pushed": "2026-11-09", "language": "Python", "topics": ["agent-skills", "claude-code", "codex", "documentary", "explainer-video", "motion-graphics", "skia", "video"]}
query: claude-code created:>{since} stars:>20

Cinematic Skill 

 Narrated cinematic films, built entirely from code, by your coding agent. 

 
     
  &nbsp;
   
  &nbsp;
     
 

 
   
 

Ask your agent for "a 90 second documentary about the Wright brothers" and it writes the script, records a voice, finds public-domain photos with their licences, and builds one continuous camera move over a single designed world. Stamps slam, highlighters swipe and numbers roll up on the exact word the narrator says. It finishes with sound effects, an optional score and burned-in captions.

Nothing is generated video. Every frame is drawn by code (Skia, in Python), so the film renders the same every time, changes are cheap, and a new voice re-times the whole film by itself.

 
   
       
       
   
 

 Left: the final frame of "Twelve Seconds", the 90 second documentary that ships as the worked example, made from seven public-domain photos. Right: the starter explainer that every new project begins as. 

## Install

```bash
npx skills add Moh4696/cinematic-skill
```

That uses the [`npx skills`](https://github.com/vercel-labs/skills) CLI (Node 22.20+). It installs for Claude Code, Codex, Cursor, Gemini CLI, OpenCode and dozens more. Start a new agent session afterwards.

 
 Claude Code plugin 

```
/plugin marketplace add Moh4696/cinematic-skill
/plugin install cinematic-skill@cinematic-skill
```

 

 
 Codex plugin 

```bash
codex plugin marketplace add Moh4696/cinematic-skill
codex plugin add cinematic-skill@cinematic-skill
```

 

 
 Gemini CLI 

```bash
gemini extensions install https://github.com/Moh4696/cinematic-skill
```

 

 
 Without Node: the shell installer 

```bash
curl -fsSL https://raw.githubusercontent.com/Moh4696/cinematic-skill/main/install.sh | bash
```

It clones to `~/.cinematic-skill` and links the skill into every coding agent it finds. Run it again to update. From a clone: `./install.sh --claude --codex`, `./install.sh --dir path/to/skills`, `./install.sh --copy`, `./install.sh --uninstall`.

 

Then install what the scripts use:

```bash
pip install -r requirements.txt      # skia-python, numpy, pillow (scipy optional)
```

ffmpeg must be on your PATH. The skill's `check_setup.py` checks everything and says what's missing.

## What it makes

| Kind | Look | Images |
| --- | --- | --- |
| Documentary, history, true crime | Cork evidence wall, slate | Archive photos and documents, black and white |
| Product launch, brand or founder story | Studio, charcoal | Your own product shots and photos, in colour |
| Science, engineering, how it works | Blueprint, paper | Diagrams, archive or AI stills |
| Tech, space, trailers | Night | Screenshots, renders, AI stills |

The items work on every look:

- photos and torn newspaper clippings
- typeset documents with real quotes
- clean cards
- big distressed type and rolling counters
- stamps, pen circles and highlighter swipes
- red string between prints
- maps of any country, with filled regions, routes and markers

A spotlight follows the camera so each line has one hero.

## How it works

1. **Story.** The agent researches, fact-checks and writes the script: one idea per line, and time only moves forward after the opening. Each line also says what the camera shows. A beat table with a chronology lint goes to you for approval.
2. **Voice.** A free scratch voice (macOS `say` or espeak-ng) times the film first. The final voice can be any TTS or a person, recorded one section at a time and split into timed lines automatically. Suspe

## 9. [arxiv] AI for Biologists: The Knowledge Boundaries of Foundation Models in the Age of Agentic Systems
key: arxiv:2611.17015
url: https://arxiv.org/abs/2611.17015
meta: {"published": "2026-11-12", "authors": ["Tian Cai", "Andrew Kleist", "Jaimin Patel", "Duccio Malinverni"], "categories": ["q-bio.BM", "cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Artificial intelligence (AI) is changing how biological research is done. Biological foundation models trained on millions of nucleotides, protein, and single-cell measurements predict protein structures, mutation effects, and cellular responses to genetic perturbations. Agentic systems, AI assistants built on large language models, can run multistep analyses from plain-language requests and increasingly call foundation models as tools. Yet it is often unclear when these models' outputs can be trusted. We frame this as a model's knowledge boundary: the range of inputs, tasks, and conditions over which its outputs are reliable. This review explains how foundation models are built and proposes that five design elements (data, architecture, training scheme, evaluation scheme, and post-analysis) define this boundary. We examine evidence on where current models succeed or fail and present standardized descriptions of model limits so that researchers, and the agents acting for them, can use these tools reliably.

## 10. [youtube] PROPOSED 2027 MOT LAWS EXPLAINED 🦾
key: yt:d4XbDwboeCg
url: https://www.youtube.com/watch?v=d4XbDwboeCg
meta: {"channel": "OEMperformanceltd ", "rank": 2, "duration_min": 1}
query: MOT data analysis uk

# PROPOSED 2027 MOT LAWS EXPLAINED 🦾
# OEMperformanceltd 
# https://www.youtube.com/watch?v=d4XbDwboeCg

[00:00] The DVSA is trying to grab us by the short curlies. We've done a video on mapping and basically everybody is worried about the new MOT laws. What they're trying to do is essentially they are trying to crack down on the DPF and AdBlue deletes. Now, just quickly before I go into this, if you offer those services, change the wording because AI is such a thing now where they just go find DPF delete online and you will come up. Nothing really has changed. You shouldn't have ever really deleted your DPF. You shouldn't have ever really have deleted your cat. >> [music]
[00:30] >> They're just cracking down on it more, okay? And the people that are offering these services, just change the name of it and you probably get away with it. It's more of a case of they just want to look to be doing something at this point. They want to crack down on the people that are just trying to bust the missions. You're going to park in an airport, it's a lower emission zone. Is it You've got jets taking off constantly. It's not lower emissions. Obviously, yes people, you are right to have your concerns. It does change the emissions if you delete your DPF. If you change your AdBlue, it pretty much does nothing. So, I really won't worry about
[01:02] that too tough. But, they don't want people doing it. Also, stage ones as well. This doesn't really affect your emissions. Everything will be the same. I really won't worry too tough about it. They are changing the regulations, but it's always relatively been the same.

## 11. [vault] client tiering and concentration
key: vault:2026-10-05:client-tiering-and-concentration
url: 
meta: {"vault_status": "intel", "kind": "scheme", "subject": "OFM Conquest (Skool, Dylan Beese) - 6 and 7 figure interviews", "date": "2026-10-05", "where": "TRITON-CORE/Education/Courses/ofm-conquest/TAKEAWAYS-interviews.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: tier clients by value; one client at 80 percent of revenue, or one staffer holding every relationship, sank two agencies

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) Free classroom plus 13 seller-run testimonial interviews, a funnel for the paid partnership; figures are unverified gross inflow. Useful as agency-operations intel, not as proof of returns.

## 12. [hn] Ask HN: Can anyone name anything new that AI has done?
key: hn:50484426
url: https://news.ycombinator.com/item?id=50484426
discussion: https://news.ycombinator.com/item?id=50484426
meta: {"points": 27, "comments": 47, "created": "2026-11-13T14:53:56Z"}
query: car data

We're 2 years into this. Still looking for something that an AI did all by itself that is actually new. Everything I've seen so far still involves a human sussing out the new thing or the model is just aggregating data that is already there from disconnected sources that never got tied together.
comment (win311fwg): That's AI for ya. What you are seemingly looking for is AGI and that we do not yet have.
comment (scosman): https://github.com/openai/math among many others
comment (iugtmkbdfil834): Yep, it is all over. Nihil novi and all that. It it is totally pointless. No sane person uses AI. Can you step a little closer over there? Don't worry. It is totally not a trap.

## 13. [github] hitkeeen/blender-ai-mcp-addon: AI assistant and MCP server for Blender: visual chat, scene tools, multi-agent workflows. Works with ChatGPT/GPT, Claude, Gemini, Ollama, OpenCode. Blender AI addon, copilot for 3D, bpy Python scripting, MCP integration.
key: gh:hitkeeen/blender-ai-mcp-addon
url: https://github.com/hitkeeen/blender-ai-mcp-addon
meta: {"stars": 155, "created": "2026-11-12", "pushed": "2026-11-12", "language": null, "topics": ["ai-agents", "ai-assistant", "blender", "blender-addon", "blender-ai", "blender-automation", "blender-mcp", "blender-plugin"]}
query: mcp server created:>{since} stars:>30
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# mcp-for-blender-pro

### Your Blender scene. Your AI models. One creative workspace.

**An AI assistant for Blender that can inspect your scene, build objects, edit materials, find assets and carry out multi-step workflows—with a visual chat workspace and a built-in Model Context Protocol (MCP) server.**

[Download](https://github.com/hitkeeen/blender-ai-mcp-addon/releases/latest) · [Getting started](docs/QUICKSTART.md) · [Connections and agents](docs/CONNECTIONS.md)

## Turn a creative brief into scene operations

Start with an idea. Ask the assistant to inspect your scene, create a product-display layout, arrange objects, assign materials or prepare an export. Follow its actions in the conversation and inspect the result in the viewport preview. Keep working in Blender throughout the process.

**mcp-for-blender-pro brings conversation, scene tools, model choice and agent workflows together.** It is designed for artists who want faster iteration, technical artists who automate repetitive work, and developers connecting AI tools to Blender.

## Why choose mcp-for-blender-pro?

| Capability | What it gives you |
|---|---|
| **Blender-aware assistance** | Scene and object inspection gives the assistant context before it acts. |
| **A visual Studio workspace** | Chat, scene objects, viewport snapshots, approvals and a task board in a companion window. |
| **Your choice of AI** | Connect supported cloud providers, local Ollama models or compatible custom endpoints. |
| **Saved connections** | Keep work and personal connections separate, including multiple keys for the same provider. |
| **One assistant or a team** | Use a single model for quick changes, or managers, workers and reviewers for structured tasks. |
| **Built-in MCP server** | Connect OpenCode and other clients supporting authenticated Streamable HTTP MCP. |
| **21 scene tools** | Create, inspect, edit, capture, search assets, consult Blender APIs and export scenes. |
| **Multilingual menus** | Choose English, German, French, Spanish or Chinese for the main interface. |

## From a quick edit to an agent team

Use **Single assistant** for direct, conversational work. For larger tasks, configure a **Team chain** with individual responsibilities, instructions and models.

- **Manager:** breaks the request into assignments and acceptance criteria.
- **Workers:** perform the assigned scene operations.
- **Reviewers:** inspect results and approve work or return specific findings.

Tasks run sequentially so scene edits stay ordered. A blocked task gets one correction attempt; a second failed review stops the workflow. The task board exposes assignments, attempts and review findings as work progresses.

## Connect the models that fit your work

Supported connections include **OpenAI, Anthropic Claude, Google Gemini, OpenRouter, OpenCode Zen, Ollama and custom APIs**. Load the available model catalog and select a model directly in Blender or Studio.

Custom endpoints support OpenAI Chat Completions, Anthropic Messages and Ollama protocols. Choose models with tool-calling support; image-capable models can also interpret viewport screenshots. OpenCode-only free models are available through the OpenCode client.

## Install and create

1. Download **`mcp-for-blender-pro.zip`** from [Releases](../../releases/latest).
2. In Blender, open **Edit → Preferences → Get Extensions → menu → Install from Disk**.
3. Select the ZIP, enable **mcp-for-blender-pro**, then open **3D Viewport → N → MCP Pro

## 14. [youtube] The UK MOT postcode lottery: 8.4 points between best and worst
key: yt:V3ngobSPgqE
url: https://www.youtube.com/watch?v=V3ngobSPgqE
meta: {"channel": "Mot Faults", "rank": 3, "duration_min": 0}
query: MOT data analysis uk

# The UK MOT postcode lottery: 8.4 points between best and worst
# Mot Faults
# https://www.youtube.com/watch?v=V3ngobSPgqE

[00:00] London MOTs pass at 89.7%. Scotland 81.3%. Same test, same testers, same roads, and still a gap of 8.4 points. So Scotland must be better kept the score the same.
