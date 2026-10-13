# Harvest brief, 2026-10-13

14 items shortlisted from 254 candidates (129 dropped as already seen, 14 carry a vault verdict on the vendor).

## 1. [vault] service x city landing pages
key: vault:2026-10-05:service-x-city-landing-pages
url: 
meta: {"vault_status": "open", "kind": "paper", "subject": "Skool YouTube lessons, top 5 test (Jono Catliff, Brendan Jowett)", "date": "2026-10-05", "where": "TRITON-CORE/Education/Courses/SKOOL-YOUTUBE-TRIAGE.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: one page per service and town with matching headline; Site Studio pattern, watch thin-content risk

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (paper) Videos are medium at best (3 medium, 2 low, no high); the value sits in the linked public repos and docs, not the talk. 188 of 222 lesson videos are outdated (n8n, Antigravity era).

## 2. [hn] How to engineer an AI harness for game development
key: hn:50072120
url: https://kylekukshtel.com/ai-harness-engineering-game-development-claude-code
discussion: https://news.ycombinator.com/item?id=50072120
meta: {"points": 106, "comments": 45, "created": "2026-10-13T14:14:23Z"}
query: claude code

comment (bob1029): > I stand by a lot of what I’ve said, but am in the process of shipping a project where I’ve also used none of this. I think the scale I’m targeting here is really larger projects. The author appears to be on track to learn an important lesson about LLMs and art. LLMs have completely solved the coding side of game development. But this was never the hard part. Not even close. The fixed randomness and determinism thing sounds great on paper (all of this does), but in reality this is an extremely confining way to build a video game. Ensuring you maintain determinism across many platforms is wher
comment (roger23): I was able to get a decent FPS out of around 40k lines (excluding tooling). Tooling consisted mostly of level editing and asset conversion which I tried to keep out of the main code-base.
comment (theptip): This matches what I came up with on a small project. The biggest ones being screenshots and separated simulation. Meta level, just push your agent to make things more legible, it’ll figure it out. One other observation, remember that your agent is infinitely patient. So prompts like “build an interactive design doc with videos of each game mechanic in the style of Factorio dev diaries” can make reviewing changes easier. The general idea, all the small QoL dev tools that you don’t have time for, you can just spawn a side agent to build; if they are orthogonal to your main thread you can just pr

## 3. [github] zhuyansen/new-term-radar: Daily radar for new AI terms: names of new models, products and repos, caught on X, Hugging Face, GitHub and sitemaps before keyword tools list them.
key: gh:zhuyansen/new-term-radar
url: https://github.com/zhuyansen/new-term-radar
meta: {"stars": 856, "created": "2026-10-12", "pushed": "2026-10-13", "language": "Python", "topics": ["agent-skills", "ai", "aisa", "claude-code", "claude-skills", "google-trends", "keyword-research", "mcp"]}
query: claude-code created:>{since} stars:>20

# new-term-radar

[中文说明](README.zh-CN.md)

A daily report of the names that are starting to surge in AI: new models, products, tools and repos, caught where they are said first, before they show up in keyword tools.

Built for people who make pages, posts or products around new terms: SEO for AI tool sites, newsletters, directories, anyone who wants to know about "Strata" or "Seedance" the day it appears and not two weeks later.

## Why

A new name leaves a trail, in this order:

1. A lab or a well-followed account says it on X; a model enters Hugging Face's trending list.
2. One GitHub repo takes off on its own.
3. Directories and competitors add pages for it; someone registers a domain for it and the site starts to rank.
4. Your own site gets its first search impressions for it.
5. Google Trends shows the curve, days or weeks later.

Keyword tools read step 5. This radar reads steps 1 to 4 every day and uses step 5 only to check itself.

One example it was built around: [Niko1221/Strata](https://github.com/Niko1221/Strata) was created on 2026-09-24 and had 7,700 stars nine days later. People were searching "niko strata" from 9/26, while no second repo carried the name and no keyword tool listed it. A single repo gaining 800 stars a day is the whole signal, and it is public.

## What it reads

| Signal | What it catches | Needs | Cost |
|---|---|---|---|
| ① X | Names the accounts in your list used for the first time in 60 days | AIsa key | $0.003 per account per run |
| ① Hugging Face | Models new to the trending top 50; quantised copies grouped under the base name | nothing | free |
| ② GitHub breakout | A repo under 14 days old averaging 200+ stars a day, or +400 since yesterday; adds the search variants people use ("niko strata") | nothing (a GitHub token raises the rate limit) | free |
| ③ Sitemaps | Words that several new URLs on a site share and its older URLs rarely carried | the sitemaps you list | free |
| ③ New sites | Domains registered and first indexed in the last 90 days that already rank for 20+ keywords | AIsa key | about $0.13 per query, weekly |
| ④ Search Console | Queries your site got impressions for, for the first time (fresh data) | your own Google token | free |
| ⑤ Review | Each lead checked in Google Trends 14 days later, against its own baseline; hit rate and days ahead per signal | AIsa key | $0.0012 per search variant |
| Keyword table | For the day's new names: the generic search terms behind them (what people do with the new thing), each sized and given a decision | AIsa key; [GoAnyAPI](https://goanyapi.com) key optional | about $0.15 a day for 5 names, $0.22 with GoAnyAPI |
| Name judge | A small model scores every term: the name of one specific thing, or a common word? | AIsa key | a fraction of a cent per run |

Prices are what AIsa charged in October 2026. With the example config (35 X accounts read three times a day, the keyword table for 5 names a day) a month costs about $15: $10 for the X reads, $5 for the keyword table. Read fewer accounts, or read them once a day, and it drops in proportion.

## The keyword table

A name is half of what you need. "SynthID Detector" has a short life as a keyword and belongs to Google; the job it does, "ai image detector", is what people keep searching, and nobody owns it. Each day the radar reads the new names once more and writes one table with both:

```
| Keyword | Type | Behind | New? | Est. searches/day | Started rising | Peak vs gpts | Peak day | Last 7 da

## 4. [arxiv] ToFu: Exploiting and Fuzzing the LLM-Orchestrator-Tool Trust Boundary
key: arxiv:2610.13651
url: https://arxiv.org/abs/2610.13651
meta: {"published": "2026-10-09", "authors": ["Md Nazmul Islam Ananto", "Pierre Prevost-Avenel", "Colin Smith", "Kyungtae Kim"], "categories": ["cs.CR"]}
query: all:"language model" AND all:agent AND all:tool

Large language models (LLMs) are increasingly deployed as agents that interact with external software through tools, with an orchestration layer translating model outputs into structured tool invocations. This architecture creates an LLM-orchestrator-tool trust boundary where tool semantics may go unenforced and LLM-generated arguments may be incorrectly treated as trusted. We present ToFu, a tool-aware framework that automatically derives semantic security checks for LLM tools from their existing metadata and a CWE-guided sanitizer corpus. ToFu specializes these checks to individual tools and automatically generates fuzzing harnesses and semantic oracles using runtime introspection and outcome sanitization. We evaluated ToFu across 273 MCP servers containing 3405 tools and identified verified bugs corresponding to CWE weakness classes in 343 tools across 118 of the servers. Our findings show that real-world tools frequently fail to enforce their documented input semantics, making it unsafe to treat LLM-generated arguments as trusted.

## 5. [youtube] What is xG? | By The Numbers
key: yt:zSaeaFcm1SY
url: https://www.youtube.com/watch?v=zSaeaFcm1SY
meta: {"channel": "Tifo Football by The Athletic", "rank": 1, "duration_min": 4}
query: expected goals model from scratch

# What is xG? | By The Numbers
# Tifo Football by The Athletic
# https://www.youtube.com/watch?v=zSaeaFcm1SY

[00:02] XG or expected goals is the current metric of choice for the football stats Community an has gained some wide attraction with its appearance on BBC's match of the day as well as plenty of comment from pundits and analysts who feel it's either ruined or solved football in fact XG has done neither it's a simple tool which can help our comprehension of the game if correctly understood what it cannot do on its own is predict results nor does it Rob football of any its charm expected goals put simply is a measure based in probability of whether a given shot will
[00:37] result in a goal looking at a historical data set of lots of shots taken from lots of possessions and looking at which of those shots resulted in a goal expected goals shows how many goals an average team would be expected to score from those shots in other words expected goals shows how good a shooting chance was based on How likely similar chances were to result in a goal an XG of one means a guaranteed goal which doesn't exist while an XG of 0.7 means that if a shot were taken 10 times you'd expect
[01:13] seven goals the closer to goal a shot the higher the XG The Wider the angle from goal the lower the XG headers get a lower XG than shots an XG map for swansea's recent 1-0 victory over Liverpool shows a series of dots the larger the dot the larger the XG or likelihood of that shot being a goal overall Liverpool shots yielded an expected goals of 2.31 versus Swansea 0.35 according to this model from Strat of course Swansea scored a goal
[01:49] and Liverpool didn't but what this XG model suggests is that Liverpool had more and better chances if you'd watched the game you'd know this instinctively what XG does is clarify that with a number Strat BET's XG Model includes Defenders positioning other models like opter currently do not obviously a shot taken with Defenders between the ball and the goal has a lower XG XG does not account for who is striking the ball which is due to the reduced accuracy of
[02:21] comparison that comes from introducing player identity however it does show that players such as Harry Kane Alexis Sanchez or Romo luk who consistently score more than their XG total would suggest are Elite Strikers they are able to score from certain positions more than the average player would which is what makes them great XG is therefore useful for assessing Strikers as good ones will consistently exceed their XG over time it's also good for seeing which teams produce lots of good chances or don't
[02:54] and when combined with a team's conceded XG it can give a general indication of of quality it is not that good for predicting match results and anyway as Richard Whitt has written XG is best used in concert with tactical and video analysis and in trends of 5 to 10 games then it can be part of a set of tools that explains why teams are blowing hot or cold and stats are always best used in context anyway while XG is therefore helpful it's not going to solve football you
[03:27] can't solve football it's too complicated and there's too much going on what XG does do well is show how good a team's chances were in a match and which strikers managed to score more goals than they should or fewer both are useful in increasing our understanding of football and that can only be a good thing [Music]

## 6. [awesome] plur-ai/plur (new in awesome-claude-code)
key: gh:plur-ai/plur
url: https://github.com/plur-ai/plur
meta: {"list": "awesome-claude-code", "stars": 303, "created": "2026-03-19", "language": "TypeScript", "description": "Shared memory for AI agents"}
query: awesome-claude-code
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# PLUR — Your agents share the same memory

[](https://mcptoplist.com/server/io.github.plur-ai%2Fplur)

[](https://www.npmjs.com/package/@plur-ai/core)
[](https://github.com/plur-ai/plur/actions/workflows/ci.yml)
[](LICENSE)
[](https://github.com/plur-ai/plur/stargazers)
[](https://glama.ai/mcp/servers/plur-ai/plur)

Persistent, **open** memory for AI agents — local-first, zero-cost, shared across MCP tools (Claude Code, Codex, Cursor, OpenCode, Hermes, OpenClaw). Your agent's memory is plain-text **engrams** you can read, correct, and delete — not weights you can't.

[plur.ai](https://plur.ai) · [Benchmark](https://plur.ai/benchmark.html) · [Engram Spec](https://plur.ai/spec.html) · [npm](https://www.npmjs.com/org/plur-ai) · [Comparisons](comparisons/)

## Benchmarks

PLUR is memory, not just retrieval — so we measure it on more than one axis, on the **full** corpus, and we publish the harness so you can reproduce every number.

**Retrieval recall — full LongMemEval-S (N=500), R@5, fully local:**

| Stack | R@5 | Notes |
|-------|-----|-------|
| BM25 only | 92.2% | no embedder — fully airgapped |
| Hybrid (BGE-small, shipping default) | 95.6% | local embedder; one-time model download |
| **+ BGE-reranker-v2-m3** | **97.6%** | local cross-encoder, max quality — opt-in, ≈5s p50 on CPU |

Numbers come from [plur-ai/plur-bench](https://github.com/plur-ai/plur-bench),
which is the source of truth for every benchmark figure PLUR publishes. Where
an in-repo number and a plur-bench number disagree, plur-bench wins — it is the
reproducible harness, and it is what CI regression-checks.

Chunk granularity, canonical-doc scoring, corpus SHA256 pinned — reproduce it in [plur-ai/plur-bench](https://github.com/plur-ai/plur-bench). No cloud call is required for any of these numbers (an *optional* cloud embedder, openai-3-large, reaches 97.0% hybrid). A faster reranker — `ms-marco-minilm-l6` (p50≈245ms vs BGE's ≈5s on CPU) — trades a little recall for sub-second latency.

**Run it yourself — and tell us what you get.** The harness is [plur-ai/plur-bench](https://github.com/plur-ai/plur-bench): CPU-runnable, no API key needed for the local path, corpus auto-fetched and SHA-verified. If you run it, we'd genuinely love to see your numbers — open an issue or discussion with your results, **especially if they don't match ours.** Independent reproduction is worth more than any number we publish, and we'll gladly credit you.

**Retrieval ≠ answer accuracy — and we report them separately, never conflated.** End-to-end (LLM-judge) answer accuracy with the reranker stack is **60.5%**, versus **52.0%** for dumping full context into the prompt and **5.5%** with no memory at all.

**Agent-task impact** — same task, with memory vs without: Haiku + PLUR outperforms Opus *without* it at roughly **10× less cost**; house rules **12–0** across Haiku, Sonnet, and Opus.

**Operational** — local-first, zero-cost search, data-sovereign by design.

*More in progress: LoCoMo, agentic task suites, cross-tool portability, decay / contradiction correctness.* [Full methodology →](https://plur.ai/benchmark.html)

## The idea

You correct your agent's coding style on Monday. On Tuesday, it makes the same mistake. You explain your architecture in Cursor. That night, Claude Code has no idea.

PLUR fixes this. Install it once, and corrections, preferences, and conventions persist — across sessions, tools, and machines. Your memory is stored as plain YAML on your disk. No cloud, no API

## 7. [vault] Flat monthly editing retainer for businesses already producing content
key: vault:2026-09-27:flat-monthly-editing-retainer-for-businesses-already-produci
url: 
meta: {"vault_status": "open", "kind": "scheme", "subject": "AI Clipping Agency starter kit (Musa Mustafa, Media Metas / Crayo Inc)", "date": "2026-09-27", "where": "TRITON-CORE/Research/links/2026-09-27-natejbiz-retainer-and-crayo-starter-kit.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Priced at two to six thousand dollars a month; deliverable with the existing stack and no purchase

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) Real operator and real tool: Musa Mustafa co-founded crayo.ai (3.2m users), company Media Metas / Crayo Inc, San Jose. But the 5 dollar price, down from 12.50, is a qualifier not a product: it puts a card on file and routes to a private one-to-one with an agency owner, which is where the real offer lands. What it actually sells is the commodity half, Content Rewards pay-per-view clipping, which is the volume game natejbiz explicitly warns against, plus a media-buying commission angle (20 percent of a 100k brand budget). The money worth having in this category is the flat monthly editing retainer, two to six thousand a month, which we can already deliver with no purchase. Income claims (3k first week, 3,801 in 13 days, 4,251 with zero experience) are unevidenced, and the 48-hour guarantee covers budget allocation, not earnings. Job: Sell post-production as a monthly retainer, priced, to businesses that already produce content (still open)

## 8. [hn] Launch HN: Consus (YC F24) – LLM gateway for companies handling sensitive data
key: hn:50073471
url: https://news.ycombinator.com/item?id=50073471
discussion: https://news.ycombinator.com/item?id=50073471
meta: {"points": 32, "comments": 16, "created": "2026-10-13T15:41:00Z"}
query: claude code

Hey Hacker News! I'm Eric, the founder of Consus. We route all AI requests to ITAR restricted and controlled unclassified information (CUI) compliant infrastructure. Consus itself satisfies ITAR restrictions, and we recently completed our FedRAMP equivalency audit against the 410 FedRAMP High controls. FedRAMP High is the U.S. government’s strictest security baseline for cloud services handling sensitive unclassified data. A breach of this data could cause severe or catastrophic harm. Achieving FedRAMP equivalency, or authorization, is required before processing CUI information. Demo: https://youtu.be/6MYxJe6P4oY Aerospace and defense is experiencing rapid growth. Unfortunately, most companies are struggling to use AI because of necessary data protections & compliance risk. These companies can move even faster if they could use the AI tools that most other industries take for granted. I spent most of my career prior to Consus in aerospace & defense. I launched national security payloads at SpaceX, and was an early employee at Castelion. I’ve watched first hand how compliance red-tape makes it difficult for companies to adopt new technologies and trust vendors that touch their sensitive data. For example, I worked with a satellite manufacturer that doesn’t allow any AI tools, even for non-sensitive work. Even as AI has become extremely useful over the past 9-12 months, I was surprised by how many aerospace & defense companies refused to touch it. They could see how it could be
comment (runamuck): I love this. Will this guarantee that proprietary/ sensitive/ CUI data won't leak to model training or other parties?
comment (projectescape): This is great, question though, since you support coding agents like Claude Code and Codex, they run MCP servers, plugins, web search/fetch and their own telemetry from the dev's machine. Do you give customers guidance or controls for that side, or is it out of scope for the gateway?
comment (skinfaxi): How does ZDR work with requests that trip security measures in the model provider? Do the providers retain those requests for analysis or is that too guaranteed?

## 9. [github] Arekejoker/qwen21-nsfw-pose-skill: Qwen-Image 2.1 NSFW/姿势出图 skill：作者级提示词配方 + NSFW LoRA + 136 姿势 VNCCS 人偶控制；适用 Claude Code / Codex / Cursor / OpenClaw
key: gh:arekejoker/qwen21-nsfw-pose-skill
url: https://github.com/Arekejoker/qwen21-nsfw-pose-skill
meta: {"stars": 773, "created": "2026-10-13", "pushed": "2026-10-13", "language": "Python", "topics": ["agent-skill", "comfyui", "image-generation", "openclaw", "pose-control", "qwen-image"]}
query: claude-code created:>{since} stars:>20

# qwen21-nsfw-pose

[](https://github.com/Arekejoker/qwen21-nsfw-pose-skill/actions/workflows/validate.yml)

**Qwen-Image 2.1 本地 NSFW / 姿势出图完整配方** — 作者级提示词结构 + NSFW LoRA + 136 个 3D 姿势库 + VNCCS 人偶精确姿势控制。

基于 ComfyUI + `qwen_image_2.1_int8_convrot` 底模（与 Civitai 作者同款底模），复刻并验证过 Civitai 作者样图（2026-10-12）。

- 适用：Claude Code / Codex / Cursor / OpenClaw（agent 技能）+ 人类手动使用
- 内容：可跟跑的作者案例、强制配方、姿势大胆度阶梯（L0–L3）、完整依赖与安装指南

---

## 效果展示

### 本配方输出：同一海边场景的三级对照（L0 → L1 → L2）

| L0 · 全着装，无 LoRA（提示词即全部） | L1 · 湿身泳装 + LoRA@1.0 | L2 · 极低机位 + 湿身蹲姿 + LoRA@1.0 |
| --- | --- | --- |
|   |   |   |

三张图同场景递进：L0 只有提示词；L1 加 LoRA + 显式皮肤/水珠描写；L2 再加低机位与开合姿态。**LoRA 负责质感，提示词负责信息密度，机位负责大胆度。**

### NSFW 效果（⚠️ 以下图片包含裸露内容）

**作者原图**（Civitai showcase，本配方复刻的目标）：

| 作者 · 淋浴（tawsLoRa） | 作者 · 按摩（tawsLoRa） | 作者 · 自拍（TheseAlpacas） |
| --- | --- | --- |
|   |   |   |

用 §「快速开始」的命令可复刻淋浴那张（复刻输出已验证与作者原图同场景同构图，见 `downloads/samples/phase5_meta.json` 与本文快速开始一节）。

### 3D 人偶精确姿势（Route ④，136 姿势库）

默认人物图 `references/src_standing.png`；姿势 = 骨骼旋转 JSON（MakeHuman 网格 + three.js 渲染），
换姿势且保身份。姿势库来源：HuggingFace 4 个公开仓库（`Totemistyk/General_Poses`、
`Totemistyk/Ballet_PoseStudio`、`MIUProject/VNCCS_PoseLibrary_Main`、
`MIUProject/MySuperPoseRepo`）+ 55 个手工精选，共 **136 个**。

---

## 快速开始（作者案例跟跑）

前置安装见 [install/setup.md](install/setup.md)。装好后一条命令复刻作者淋浴样图（~5 分钟）：

```bash
python3 scripts/qwen_pose_test.py \
  --mode t2i --name author_case_shower \
  --prompt "$(cat prompts/taws_v13_shower.txt)" \
  --seed 80964 \
  --steps 50 --cfg 2.5 --sampler er_sde --scheduler beta \
  --width 1152 --height 1728 \
  --lora "qwen2_1-femaledVaginus-nsfw-v1_3-fine_L22-31.safetensors" \
  --lora-strength 1.0 \
  --out outputs/author_case/shower.png
```

对比对象：`downloads/samples/taws_v13_shower_author.jpg`。
完整元数据（提示词/参数/seed/完整工作流）：`downloads/samples/phase5_meta.json`。

## 三条路线

| 需求 | 路线 | 命令 |
| --- | --- | --- |
| 新 NSFW/性感图（文字出图） | ① T2I + NSFW LoRA（必开） | `scripts/qwen_pose_test.py --mode t2i` |
| 已有角色图换姿势（保脸/保服装） | ② Edit | `scripts/qwen_pose_test.py --mode edit` |
| 指定 3D 姿势库里的精确姿势 | ④ VNCCS PoseStudio | `scripts/run_vnccs_ui.py --pose  ` |

姿势怎么选（大胆度阶梯 L0–L3、用户要求→姿势族映射表）：见 `SKILL.md` §4，或
`scripts/run_vnccs_ui.py --list-poses` 列出全部 136 个姿势。

## 配方要点（摘要）

- `er_sde` + `beta`，CFG 2.5，50 步，1152×1728 竖版
- **NSFW LoRA 永远开**（默认 `femaledVaginus v1.3b` @ 1.0）
- 提示词必须按作者结构写满 7 要素、300–1500 字符、含 LoRA 触发词
- 弱化配方（无 LoRA/短提示词/减步数）前必须告知用户代价，不许默默减弱

完整规则与证据：`SKILL.md`。

## 目录结构

```
├── SKILL.md            # agent 技能（完整规则）
├── install/setup.md    # 安装指南（模型/LoRA/节点/姿势库）
├── scripts/            # 出图脚本、案例脚本、media_lock.py、validate_package.py
├── workflows/          # qwen21_t2i.json / qwen21_edit.json / VNCCS_PoseStudio_QI2.1.json
├── prompts/            # 3 篇作者原提示词 + 参数
├── references/         # 效果展示图（L0/L1/L2 海边对照）+ 默认人物图
├── downloads/samples/  # 作者原图 + 作者元数据 + 原始工作流 JSON
└── pose_library/       # 55 个手工精选姿势（安装时拷入 ComfyUI）
```

## 说明

- 底模与 LoRA 版权归原作者所有（HF `Comfy-Org/Qwen-Image-2.1`、Civitai 2986844 / 2958918 / 2988215）
- NSFW 示例图仅供配方演示；仓库为公开仓库，介意图片的先收藏后阅读

## 10. [arxiv] SqueezeBench: Saturation-Resilient Evaluation of Mathematical Capability
key: arxiv:2610.13461
url: https://arxiv.org/abs/2610.13461
meta: {"published": "2026-10-09", "authors": ["Pablo Manrique", "Hai Xia", "Stefan Szeider"], "categories": ["cs.AI", "cs.LG", "cs.LO"]}
query: all:"language model" AND all:agent AND all:tool

AI systems are making rapid progress in mathematics, but this progress is hard to measure. Benchmarks of solved problems saturate, and in benchmarks of open problems each problem can be resolved for the first time only once. We present SqueezeBench, a benchmark that is resilient to saturation: a success raises the bar instead of removing the problem. Each problem fixes an integer function $f(n)$ whose values are known only for small $n$, and the benchmark keeps a lower and an upper record on it. A record is a computable Lean function with a machine-checked proof that it bounds $f$. A submission proposes a new function and proves that it bounds $f$, that it is no worse than the current record at any $n$, and that it is strictly better at some $n$. Once accepted, it becomes the record that the next submission has to beat. The system thus chooses the bound as well as its proof, and it may improve the record at a single $n$ or its growth rate. At every $n$, the gap between the two records shows how far the certified bounds are from determining $f(n)$. Every proof is checked by two independent Lean kernels, so no referee needs to check the mathematics. The checks also reject a function that computes $f$ by exhaustive search at small $n$, and a maintainer only reads the submitter's report and looks for such a search at larger $n$. We release ten problems from extremal combinatorics with twenty proved initial records and the admission tools. As a baseline, agents based on a frontier language model, with at most one hour per record, had 82 submissions accepted and improved every record, without going beyond the published literature. Agents based on two newer models then started from these records, had 60 more submissions accepted and improved 19 of the 20 records again. For eight of the ten problems, at least one record is still asymptotically behind the best published bound.

## 11. [youtube] Build a Simple Expected Goals Model with Machine Learning and Python
key: yt:GsfXAzfvJVM
url: https://www.youtube.com/watch?v=GsfXAzfvJVM
meta: {"channel": "McKay Johns", "rank": 3, "duration_min": 35}
query: expected goals model from scratch

# Build a Simple Expected Goals Model with Machine Learning and Python
# McKay Johns
# https://www.youtube.com/watch?v=GsfXAzfvJVM

[00:00] expected goals have become the most popular metric and one of the most used metrics for analyzing football and a lot of people are using it whether that is at a club level in a public domain level or even in a match commentary broadcasting level as well and the reason why is because it helps us evaluate and understand the quality of chances of scoring opportunities and really when it comes to these models there is a big confusion and it seems to be kind of a big black box of how these models are trained how they're developed
[00:33] and what these numbers actually mean I mean I've been watching a lot of football matches where maybe there's a shot that's worth like 05 XG and the match commentator is like oh that should be worth 0.5 instead of 05 right they're like I would have even scored that but they don't really understand what goes into calculating all of these different metrics and all these different values and so what we're going to do in this video is I'm going to walk you through how you can train in expect a goals model and just kind of some of the steps that are involved with training and expect a goals model using machine
[01:06] learning and this model is going to be slightly different than say an opto or stats bomb model because they have so many more data points they have so much more data that they're working with where the data here is just some data that I've scraped from the web and that I've just been using my own personal analysis that I've been doing what we're going to do is we are just going to use the data we're going to do a little bit of machine learning just flow of exploring and cleaning the data and then by the end we'll show you how we can train and evaluate and kind of see some of our expected goal values that we have created so let's go ahead and jump into
[01:40] it all right the first thing that we need to do to be able to actually run and create this expected goals model is we need to make sure that we have the packages and all of the data loaded in and so you can find the data just in the GitHub it'll be in a link in the video description and you can just go download that data it's going to be the same data in the GitHub that we use here in this video and so what we'll do is we will just start with a Jupiter notebook and we need to make sure we have a couple of packages installed to make this work and so if you don't have the packages installed you can install them via the the terminal or if you know how to
[02:14] install them with your command line but the way that you can do it as well is you can just do uh exclamation mark pip install and then we need to have these packages installed we need to have pandas numpy matplot lib Seaborn ml soccer and then scikit-learn like that and so these are the packages that are going to allow us to clean the data to load the data to train our model and as well visualize our expected goal output so you can go ahead and run that if you want and it'll
[02:47] install all of them if you don't have them installed I'm just going to put an comment right there so it doesn't actually run so let's load in the data we'll say import pandas as PD okay and then import numpy as NP and then we'll use pandas to load in our data frame we'll say DF equals pd. read CSV and then you just need to put the file path for wherever you downloaded the da
[transcript continues in field-notes/staging/GsfXAzfvJVM.txt]

## 12. [awesome] tronghieu/agent-skills (new in awesome-claude-code)
key: gh:tronghieu/agent-skills
url: https://github.com/tronghieu/agent-skills
meta: {"list": "awesome-claude-code", "stars": 77, "created": "2026-03-26", "language": "Python", "description": "Method-driven agent skills for knowledge work: strategy, research, critical thinking, data analysis, docs, slides. Works with Claude Code, Codex, Cursor and any agentskills.io-compatible agent."}
query: awesome-claude-code
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# Agent Skills

**Language:** [English](./README.md) | [Tiếng Việt](./README.vi.md) | [中文](./README.zh.md)

[](./LICENSE)
[](https://github.com/tronghieu/agent-skills)
[](https://www.skills.sh/tronghieu/agent-skills)

A collection of method-driven skills for people who use AI to make decisions, run projects, analyze evidence, create documents, and produce finished work. These skills are designed for active collaborators: you provide the real context and remain responsible for the decision; the agent supplies structure, analysis, and quality checks.

## Quick start

Install the full collection:

```bash
npx skills add tronghieu/agent-skills
```

Or install as a Claude Code plugin:

```text
/plugin marketplace add tronghieu/agent-skills
/plugin install agent-skills@tronghieu-skills
```

Then invoke a skill in your agent:

```text
/market-researcher Assess the market for this product idea in Vietnam.
```

Most agent tools use slash commands. Codex and ChatGPT use `$`; in those tools, replace the leading `/` with `$`.

## Choose a skill

| Your job | Start with |
|---|---|
| Generate or challenge ideas | [brainstorm-coach](./skills/brainstorm-coach/README.md), [critical-thinking](./skills/critical-thinking/README.md) |
| Diagnose a recurring problem | [problem-solver](./skills/problem-solver/README.md) |
| Understand customers or markets | [design-thinking](./skills/design-thinking/README.md), [market-researcher](./skills/market-researcher/README.md) |
| Decide what to build and deliver it | [product-manager](./skills/product-manager/README.md), [project-manager](./skills/project-manager/README.md) |
| Run software sprints and improve team process | [scrum-master](./skills/scrum-master/README.md) |
| Analyze data or long documents | [data-scientist](./skills/data-scientist/README.md), [deep-reader](./skills/deep-reader/README.md) |
| Make a high-stakes business decision | [strategy-board](./skills/strategy-board/README.md) |
| Create documentation, prompts, slides, or fiction | [diataxis-writer](./skills/diataxis-writer/README.md), [system-prompt-creator](./skills/system-prompt-creator/README.md), [slidewright](./skills/slidewright/README.md), [fiction-studio](./skills/fiction-studio/README.md) |
| Learn through guided questions | [socratic-questor](./skills/socratic-questor/README.md) |
| Compare CVs with a job description | [cv-scorer](./skills/cv-scorer/README.md) |
| Understand what an autonomous coding run did, or why it stalled | [bmad-run-inspector](./skills/bmad-run-inspector/README.md) |
| Test a running app by hand and prove what you saw | [manual-tester](./skills/manual-tester/README.md) |

## Skills

### bmad-run-inspector

For anyone running `bmad-loop`, an autonomous coding orchestrator, who needs an honest read on a run — watching one in progress or investigating one that finished, failed, or paused overnight. Only useful inside a project that already runs `bmad-loop`.

```bash
npx skills add tronghieu/agent-skills --skill bmad-run-inspector
```

[Read the bmad-run-inspector guide](./skills/bmad-run-inspector/README.md)

### brainstorm-coach

For founders, product teams, marketers, creators, and anyone who needs to generate options before evaluating them.

```bash
npx skills add tronghieu/agent-skills --skill brainstorm-coach
```

[Read the brainstorm-coach guide](./skills/brainstorm-coach/README.md)

### critical-thinking

For decision-makers, analysts, and writers who need to inspect the claims, evidence, assumptions, and l

## 13. [vault] Per-post CPM tracked per account feeding back into what gets made next
key: vault:2026-09-24:per-post-cpm-tracked-per-account-feeding-back-into-what-gets
url: 
meta: {"vault_status": "open", "kind": "service", "subject": "Butter (hellobutter.io)", "date": "2026-09-24", "where": "TRITON-CORE/Research/links/2026-09-24-butter.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: The one idea the write-up says to steal

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) No. Variant generation we already have in HyperFrames; the only delta is multi-account auto-posting, and Butter's own help page says it routes posts through GeeLark antidetect cloud phones, one spoofed device per account, described as indistinguishable from organic activity. That is detection evasion documented by the vendor, not an integration; it is on no platform partner list. X bans the behaviour verbatim, TikTok tightened on 24 Sep 2026, Instagram judges it at account level over 30 days from 30 Apr 2026, YouTube demonetised it as inauthentic content from Jul 2025. No founder, no legal entity, terms page 404s, zero independent reviews, and everything ranking for it is its own SEO farm. It also breaks our human-presses-send rule by design and would put the agency at risk, not just a side account. Steal only the per-post CPM-per-account tracking idea. Job: Turn one filmed asset into platform-native posts across several owned accounts without tripping the inauthentic-content rules (still open)

## 14. [hn] Nearly all 19 car brands send driver data to third parties (Northeastern/CR)
key: hn:50072909
url: https://news.auravision.co/car-is-spying/
discussion: https://news.ycombinator.com/item?id=50072909
meta: {"points": 21, "comments": 20, "created": "2026-10-13T15:07:20Z"}
query: car data

comment (plc): Disclosure: I'm the founder of AuraVision, which publishes The Signal (the linked site). Posting because the underlying Northeastern/Consumer Reports study is a significant privacy issue worth a technical discussion here. The site has a product point of view, but the reporting and primary sources stand on their own — happy to link the raw sources or dig into specifics in the thread.
comment (VladVladikoff): If you buy a new car from the dealer presumably somewhere in the fine print it gives them permission to do this. But if you buy the same car used from an individual, how does the car company still retain the right to spy? It seems like this must be breaking some sort of privacy laws.
comment (rubyn00bie): This feels like a marketing post. There’s no substance to it and no details, at least for me on mobile. I really don’t understand who or what this is supposed to be for… if Auravision is a product I can’t tell what it is or why it matters.
