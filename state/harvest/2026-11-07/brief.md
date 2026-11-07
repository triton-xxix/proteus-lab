# Harvest brief, 2026-11-07

13 items shortlisted from 369 candidates (283 dropped as already seen, 7 carry a vault verdict on the vendor).

## 1. [vault] AI model courses titled for OnlyFans but guaranteed against Fanvue
key: vault:2026-09-27:ai-model-courses-titled-for-onlyfans-but-guaranteed-against-
url: https://zupria.com/create-and-monetize-an-ai-onlyfans-model/
meta: {"vault_status": "intel", "kind": "scheme", "subject": "Zupria AI model course (Bogdan Irimia, Zupria SRL)", "date": "2026-09-27", "where": "TRITON-CORE/Research/links/2026-09-27-zupria-ai-model-course.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: OnlyFans requires a verified real person in the content; Fanvue permits declared AI creators, so the name and the guarantee point at different platforms

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) A 19-module course reached via a Facebook ad. Vendor is real and traceable: Bogdan Irimia, Zupria SRL, Braila, Romania, VAT RO40257322. Three tells. Pricing: 77 euros lifetime down from 397 is the hook, but 79 euros a month of required generation-app subscriptions plus 42 optional makes the real cost about 950 a year. Naming: titled for OnlyFans, which requires the account holder to be a verified real person in the content, while the 30-day earnings guarantee is conditioned on Fanvue, which permits declared AI creators, so it is named after the recognisable platform and guaranteed against the permissive one. And it ships a deepfake-techniques module with no legal warning, which for a UK buyer is a route into a criminal offence, since creating sexually explicit images of a real person without consent is now criminalised at the point of creation, not just sharing. No age-verification guidance either, which UK law has required for pornographic content since July 2025. Category already assessed via Eromify with the DMCC and disclosure bounds attached; nothing new here. Job: Understand the AI character content market well enough to advise on it, without operating in it (still open) Write-up: `TRITON-CORE/Research/links/2026-09-27-zupria-ai-model-course.md` Link: https://zupria.com/create-and-monetize-an-ai-onlyfans-model/

## 2. [hn] University libraries are being swarmed by AI bots, putting public access at risk
key: hn:50392499
url: https://www.cbc.ca/news/world/university-libraries-ai-data-scraping-bots-9.7408287
discussion: https://news.ycombinator.com/item?id=50392499
meta: {"points": 135, "comments": 63, "created": "2026-11-06T14:13:09Z"}
query: car data

comment (Bender): LLM bots are the easiest to spot. Rate limit them to 16kb/s and 1 request every 5 seconds. Give them a friendly multilingual WCAG status 429 page that says to slow down or status 444 and drop them into nftables ipsets if they continue to be aggressive. Ask your favorite LLM how to set this up. If your LLM gets session paused, ask Gemini or Grok. Tell it if you are behind a CDN. Enable logging of ssl curves, ciphers, etc... Show your LLM some examples from your access logs.
comment (tokai): In what world is 11k searches a lot? The story here is that AI bots are exposing University Libraries bad setups. I haven't heard any institution here in northern europe having any trouble.
comment (blakesterz): What I still don't understand is who is doing it? I assume it's not the big companies like OpenAI or Google or Anthropic, right? So there are a bunch of small things out there doing the scraping and then they sell it to the big places? Or are these just smaller AI models doing the scraping and using it for themselves? Is there an underground ecosystem where people buy and sell this stuff? I understand why it's valuable to the AI companies I'm curious about how all this work, the economics of it all.

## 3. [github] imraywang/ray-sticker-shop: 一张照片或角色图，生成一整套形象一致的动态表情包和微信投稿素材（Claude Code / Codex skill）
key: gh:imraywang/ray-sticker-shop
url: https://github.com/imraywang/ray-sticker-shop
meta: {"stars": 359, "created": "2026-11-05", "pushed": "2026-11-05", "language": "Python", "topics": []}
query: claude-code created:>{since} stars:>20

# 表情包工坊 ray-sticker-shop

一张照片或角色图，生成一整套形象一致的动态表情包，并打包成微信表情开放平台要的全部素材。

ChatGPT 现在能直接做 GIF，但一张一张做，形象容易跑，尺寸也不是微信要的。这个 skill 把剩下的事都做了：

- 一个参考图锁定整套角色
- 240×240 GIF，自动压到 500KB 以内
- 封面、图标、横幅、赞赏图一起出
- 按微信规范自动检查
- 上架文案和给客户的交付包

## 安装

把这个文件夹放进你的 Agent 的 skills 目录，比如：

```bash
git clone https://github.com/imraywang/ray-sticker-shop ~/.claude/skills/ray-sticker-shop
```

然后对 Claude Code 或 Codex 说：「把这张猫的照片做成一套表情包。」

## 需要什么

- Python 3.9+ 和 Pillow：`pip install pillow`
- `OPENAI_API_KEY`（中转站再设 `OPENAI_BASE_URL`）
- 没有 key 也行：Agent 会给你提示词，到 ChatGPT 里出图，放回来照样合成

## 花费

8 张表情加 5 张配套素材，按 OpenAI 官方单价约 $0.7，重抽另算。实际花费记录在项目目录的 `costs.jsonl`。

## 注意

只做你有权使用的形象。微信不收未授权的二创和同人。过审由微信决定，本工具不保证过审和收入。

MIT License

## 4. [arxiv] Building Barricades: Red-Teaming Agentic Biosynthesis Planning
key: arxiv:2611.08218
url: https://arxiv.org/abs/2611.08218
meta: {"published": "2026-11-05", "authors": ["Nicholas Roehner", "Bryan Bartley", "Jacob Beal", "Caitlin Jagla"], "categories": ["q-bio.OT"]}
query: all:"language model" AND all:agent AND all:tool

The rapid democratization of biotechnology, enhanced by large language models (LLMs) and agentic software, is eroding longstanding barriers that have limited biosynthesis planning to experts. We present BioBulbul, an agentic system that couples LLMs with open-source biodesign tools for retrobiosynthesis, enzyme selection, gene cluster design, and DNA assembly planning. Using simple natural language prompts, BioBulbul autonomously generates plausible biosynthesis pathways and corresponding gene cluster sequences for several known small molecule toxins, demonstrating that non-experts could feasibly access them using an agentic system. Our red-teaming experiments confirm the technical viability of LLM-driven toxin biosynthesis while highlighting three principal barriers: scarcity of open-source biodesign tools, limited structured enzymatic reaction data, and the complexity of many small molecule toxin pathways. We argue that these barriers are likely to diminish within a decade, expanding the biological threat landscape. To mitigate emerging risks, we recommend expanding DNA synthesis screening to include chokepoint enzymes, extending chemical supplier controls to precursor compounds, establishing continuous AI-assisted threat surveillance pipelines, and developing robust LLM guardrails. Coordinated investment across government, industry, and AI developers is essential to safeguard against the misuse of agentic biosynthesis planning.

## 5. [youtube] First-Year Car Depreciation: About 20% Gone
key: yt:4g2MEpcwqv0
url: https://www.youtube.com/watch?v=4g2MEpcwqv0
meta: {"channel": "Garage Math", "rank": 4, "duration_min": 0}
query: car depreciation data analysis

# First-Year Car Depreciation: About 20% Gone
# Garage Math
# https://www.youtube.com/watch?v=4g2MEpcwqv0

[00:00] A new car typically loses about 20% of its value in year one. On a $40,000 car, that’s about $8,000 gone. Carfax says the first month alone is often more than 10%. AAA puts average depreciation at $4,422 a year the largest ownership cost. Keep longer, or buy used and skip the steepest year.

## 6. [vault] Keyword comment auto-DM funnels pushing affiliate products with no ad label and implied income
key: vault:2026-09-24:keyword-comment-auto-dm-funnels-pushing-affiliate-products-w
url: https://www.instagram.com/reel/DbPWHkDszu_/
meta: {"vault_status": "intel", "kind": "account", "subject": "@alliecatbuildai reel (comment CLAUDE for the free tutorial)", "date": "2026-09-24", "where": "TRITON-CORE/Research/links/2026-09-24-alliecatbuildai-reel-eromify.md (and \"The pattern\")", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: A near 1 to 1 like to comment ratio marks the automation; CAP Code and ASA rulings make both advertiser and influencer liable

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (account) Not Claude content. A comment-bait funnel into an AI companion app's affiliate programme, with no product, repo or client behind it. Skip. Genre filter for this shape: comment-a-word for a free thing, a disclaimer with no number beside it, no verifiable output. Any two and it can be binned. Write-up: `TRITON-CORE/Research/links/2026-09-24-alliecatbuildai-reel-eromify.md (and "The pattern")` Link: https://www.instagram.com/reel/DbPWHkDszu_/

## 7. [hn] Launch HN: Rivet (YC W23) – Scale and Orchestrate Agents on S3
key: hn:50381687
url: https://github.com/rivet-dev/rivet
discussion: https://news.ycombinator.com/item?id=50381687
meta: {"points": 120, "comments": 59, "created": "2026-11-05T17:17:42Z"}
query: agent skills

Hey HN, this is Nathan and Nicholas from Rivet ( https://rivet.dev ) – a fast, high-density, and scalable orchestrator for agentic workloads using the actor model. Rather than running a heavyweight sandbox per agent, each agent gets a lightweight actor backed by S3. Actors provide a long-lived process for long agent turns, in-memory state for context, a WebSocket server for multiplayer, durable SQLite storage backed by S3, and hibernation when idle. It's a similar model to Cloudflare Durable Objects, but it’s open source and self-hostable. Here’s a video walkthrough: https://www.youtube.com/watch?v=3Ev6I7DOV9c When we went through YC in 2023, we were building infrastructure for multiplayer games like Diep and Krunker. This involved heavily optimizing high-throughput matchmaking, real-time player messages, and blitz scaling. Through that process, we spent a lot of time on workloads where Postgres couldn't keep up with our throughput. We started out by hacking together Lua scripts on top of Redis, but this became too cumbersome to maintain and upgrade. This led us to extend our game server orchestrator to support what we call Rivet Actors today: many lightweight workers with in-memory state and durable storage. By using actors, we were able to serve tens of millions of monthly active users. As agents grew in popularity, it became clear that running agents in sandboxes is inefficient. Sandboxes are expensive, mostly idle, and slow to start. Developers started using actors becaus
comment (fastball): Rivet is very cool. Switched a Cloudflare Durable Object piece of our infrastructure that lived in its own little fairy tale land to our own infra within the rest of our VPC. Was a very pleasant experience. Haven't had the chance to try Rivet v3 yet but hoping to get to it soon.
comment (apsurd): Wouldn't an agent in any capacity need a sandbox runtime to do agentic work? When you say "sandboxes are too slow" do you mean needing to boot the sandbox to get back Agent state? Is the idea that state/memory/context and runtime env are separate concepts in rivet? (I'm a professional developer but don't do any orchestration so trying to understand from basic mental model pov)
comment (realty_geek): Ah, another rivet. I initially thought it was a pivot of: https://rivet.ironcladapp.com/

## 8. [github] duyunzhoudyz/dyz-med-paper-skills: 医学论文写作与科研助手：面向中国医生和医学研究生的 32 个 Agent Skills，适用于 Claude Code、Codex，覆盖选题、PubMed 文献检索、中英写作、选刊投稿与审稿修回。Medical writing & research skills.
key: gh:duyunzhoudyz/dyz-med-paper-skills
url: https://github.com/duyunzhoudyz/dyz-med-paper-skills
meta: {"stars": 311, "created": "2026-11-01", "pushed": "2026-11-01", "language": "Python", "topics": ["academic-writing", "agent-skills", "ai-agents", "biostatistics", "claude-code", "clinical-research", "codex", "literature-review"]}
query: claude-code created:>{since} stars:>20

简体中文 ·  English 
 

 DYZ MedPaper — 医学论文写作与科研 Agent Skills 

  32 medical writing and research skills for Claude Code and Codex.  面向中国医生与医学研究生，支持中文沟通、中英论文写作、PubMed 文献检索与审稿修回。 

  中文文档站  ·  English docs  ·  32 个技能索引  ·  版本发布  

 
     
 

 为中国医生与医学研究生 定制的医学论文助手 

 中文沟通 · 中英写作 · 选题到修回 

 
  ⭐   点亮 Star，把这个科研帮手收进工具箱   
  临床、轮转、课题已经够忙了，写论文多一个得力帮手。
 

 
     
     
     
     
     
     
     
 

 
   能帮你做什么  ·  为你定制  ·  任务与示例  
   安装使用  ·  项目状态  ·  许可与联系 
 

---

### 从科室病例与毕业课题出发

DYZ MedPaper 是一套**围绕中国医生与医学研究生科研场景设计的 AI 论文工作流**。从科室现有病例和毕业课题出发，用中文梳理研究问题、讨论统计结果，衔接中英文文献与稿件写作，再把导师意见和审稿要求落实到具体修改，帮你把手头材料推进成**能讨论、能修改的论文稿**。

无论是在临床工作间隙推进课题，还是一边轮转、一边准备毕业论文，都可以从当前最需要解决的一步开始：**选题、查文献、写初稿、改讨论、回审稿意见**。

把这 **32 个技能**装进 **Claude Code、Codex 或其他支持 Agent Skills 的智能体**，就可以用中文交代任务，从眼前最头疼的那一步开始。[查看安装方式](#quick-start)

  

## 🎯 从选题到修回，费劲的地方都有帮手

按任务进入教程：[医学论文写作](https://duyunzhoudyz.github.io/dyz-med-paper-skills/tutorials/writing/) · [PubMed 文献检索](https://duyunzhoudyz.github.io/dyz-med-paper-skills/tutorials/pubmed/) · [系统综述与 PRISMA](https://duyunzhoudyz.github.io/dyz-med-paper-skills/tutorials/systematic-review/) · [统计结果解读](https://duyunzhoudyz.github.io/dyz-med-paper-skills/tutorials/statistics/) · [中英翻译](https://duyunzhoudyz.github.io/dyz-med-paper-skills/tutorials/translation/) · [审稿意见回复](https://duyunzhoudyz.github.io/dyz-med-paper-skills/tutorials/reviewer-response/)。

有数据却迟迟定不下选题，结果做出来了却写不出讨论，稿子改了几轮还是说不清亮点——这些都可以成为起点。你把现有材料和想解决的问题交代清楚，助手就能按对应方法帮你往下做。

| 你现在卡在哪 | 它能帮你干什么 | 可以拿到什么 |
|---|---|---|
| **手上有病例数据，不知道能写什么** | 结合临床问题、已有变量和现实条件，梳理可研究的方向，先看缺什么 | 候选选题、可行性判断、需要补的材料 |
| **文献查了一堆，还是理不出头绪** | 设计中英文检索，整理关键研究，比较别人做了什么、你的研究还能回答什么 | 检索方案、文献梳理、值得继续追的问题 |
| **统计结果出来了，不知道怎么讲** | 解释主要结果，区分统计上的差异与临床上的意义，整理图表和结果段落 | 结果解读、图表建议、结果部分草稿 |
| **引言绕来绕去，讨论只会重复结果** | 理顺文章要回答的问题，安排每段写什么，再根据结果和文献起草 | 写作提纲、章节草稿、修改理由 |
| **导师让大改，不知道从哪下手** | 找出最影响文章的问题，定位到段落，排出修改顺序并协助重写 | 问题清单、修改顺序、改写稿 |
| **收到一长串审稿意见** | 拆开每条意见，安排正文修改，起草回复，标清已经改了什么、还差什么 | 逐条回复信、修改位置、待办清单 |
| **写完了，要选刊和整理投稿材料** | 按主题、文章类型、预算和要求筛选期刊，整理摘要、图表与稿件 | 候选期刊及理由、中英文摘要、基础 Word 审阅稿 |

需要做统计时，也能协助讨论分析思路、准备代码和补充分析；**先确认具体方案，再在具备相应软件和数据条件的环境里执行。**

只想翻译一段、改一版摘要，或者救一救讨论，也可以单独做。你不用先学会 32 个技能的名字。更多说法见[常见任务示例](docs/task-cards.md)。

  

## 🩺 围绕中国医生与医学研究生的科研日常设计

### 用中文想清研究，再写成中英文稿件

选题怎么想、结果怎么看、导师为什么说这一段逻辑不顺，都可以用中文来回讨论。先把研究问题和论证讲清楚，再按需要起草中文论文、英文正文或中英文摘要，让语言转换跟着研究思路走。

### 从科室病例和毕业课题的实际条件出发

有什么病例资料、随访够不够、关键指标有没有、还有多少时间，这些都会影响研究能怎么做。它可以从你的临床观察和现有数据开始，帮你把一个大方向收窄到能继续查、能继续讨论的问题。毕业论文、课题文章或投稿，都能把自己的时间、资源和要求一起带进去。

### 中英文文献和写作能接起来

既能围绕 PubMed 等来源查找研究，也能为知网、万方、维普等中文来源设计检索和整理已有记录；实际检索与全文获取仍需相应权限。中文初稿、英文正文、中英文摘要可以接着做，翻译时重点核对数字、术语和结论的分寸。

### 把导师意见落实到段落和修改清单

导师说“创新性不够”“讨论太散”“结果和结论对不上”，可以把原稿和具体意见一起交给助手。先找出问题在哪、哪些材料还缺，再安排修改顺序、协助重写，并解释修改理由，方便下一轮和导师讨论。

### 兼顾毕业要求、选刊预算和单位口径

把学校的论文要求、目标期刊、版面费预算、时间安排，以及学校或单位认可范围一起提供，助手就能据此整理写作与投稿清单，比较候选期刊并说明理由。具体要求会去核实，查不到的就标出来，方便你和导师一起做决定。

### 工作被打断，下次有记录可接

文章写到哪、哪些数字确认了、导师提出了什么、审稿意见还有几条没处理，都可以记在论文项目里。下次继续时，让助手先读这些记录，再接着推进。章节和回复信也能保存在项目里，整理成基础 Word 稿，方便拿给导师和合作者继续改。

  

## 📝 从任务到稿件

### 把帮助做到具体稿子里

整理材料、搭提纲、起草段落、解释改法、整理回复，这些事可以围着同一篇论文连续做。**你负责把握研究方向，助手帮你把想法展开成文字，把意见落实到改稿。**

比如，材料齐备时可以这样交代：

> 这是我的结果表、几篇已经核实的文献和讨论初稿。帮我把讨论重写一版：先说清主要发现，再和已有研究比较，最后写临床意义和局限。缺依据的地方单列，用中文告诉我为什么这样改。

这项任务可以落到几份具体内容上：

- **一版讨论草稿**：按论文主线组织，写出各段的重点和衔接。
- **结果与文献的对应说明**：让你能回头找到每个重要说法的依据。
- **修改理由**：解释哪里重复、哪里跳得太快、哪里把结论说过了头。
- **还需补充的问题**：缺文献、缺分析或需要你确认的地方，单独列清楚。

接下来还可以要求压缩到期刊字数、改写其中一段、翻成英文，或根据审稿意见继续修订。[写作方法和示例](dyz-med-writing-plan/references/writing-craft.md)里可以看到这些工作如何展开。

### 看看仓库里的教学示例

下面是仓库里的**合成教学示例**，用来展示处理思路和稿件长什么样。它们不是

## 9. [arxiv] TCSExam: Evaluating Frontier LLMs on the Full Range of TCS Research
key: arxiv:2611.07962
url: https://arxiv.org/abs/2611.07962
meta: {"published": "2026-11-05", "authors": ["Yifan Luo", "Zhengying Liu", "Yang Yuan", "Zhilin Yang"], "categories": ["cs.AI", "cs.CL"]}
query: all:"language model" AND all:agent AND all:tool

Can large language models (LLMs) advance theoretical computer science and resolve its long-standing open conjectures? To study progress toward this goal, we introduce TCSExam, a unified framework and benchmark covering the full range of TCS research. It evaluates theorem proving, solver engineering, and constructions alongside direct attempts to resolve open conjectures, capturing both concrete research accomplishments and progress toward long-standing research goals. TCSExam-Full contains 100 expert-reviewed tasks, with submissions checked by the Lean kernel or an executable task checker. TCSExam-Lite selects 20 tasks, five per track, reducing the number of task attempts by 80% at the same per-attempt budget. We evaluate eight agents on Full and nine on Lite. The TCSExam Index combines all four tracks: GPT-6 Astra leads Full (71.9), and Opus 5.5 leads Lite (72.3). Full and Lite rankings are strongly aligned across eight shared agents (Spearman's $ρ=0.93$), supporting Lite as a compact, discriminative benchmark. The evaluations yield improved solver outputs and mathematical constructions, together with independently verified special cases and bounds from open-conjecture attempts. TCSExam provides an extensible framework with task sources, Docker build recipes, and evaluation tools for reproducible use.

## 10. [vault] How account farms and antidetect cloud phones work and how platforms detect them
key: vault:2026-09-24:how-account-farms-and-antidetect-cloud-phones-work-and-how-p
url: 
meta: {"vault_status": "intel", "kind": "service", "subject": "Butter (hellobutter.io)", "date": "2026-09-24", "where": "TRITON-CORE/Research/links/2026-09-24-butter.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: The write-up already carries the platform rule dates; defender's view only

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) No. Variant generation we already have in HyperFrames; the only delta is multi-account auto-posting, and Butter's own help page says it routes posts through GeeLark antidetect cloud phones, one spoofed device per account, described as indistinguishable from organic activity. That is detection evasion documented by the vendor, not an integration; it is on no platform partner list. X bans the behaviour verbatim, TikTok tightened on 24 Sep 2026, Instagram judges it at account level over 30 days from 30 Apr 2026, YouTube demonetised it as inauthentic content from Jul 2025. No founder, no legal entity, terms page 404s, zero independent reviews, and everything ranking for it is its own SEO farm. It also breaks our human-presses-send rule by design and would put the agency at risk, not just a side account. Steal only the per-post CPM-per-account tracking idea. Job: Turn one filmed asset into platform-native posts across several owned accounts without tripping the inauthentic-content rules (still open)

## 11. [hn] Claude Code's "Don't Ask Again" exposes passwords in 1,122 public GitHub files
key: hn:50407882
url: https://apiiro.com/blog/coding-agents-leaking-secrets-github-dont-ask-again
discussion: https://news.ycombinator.com/item?id=50407882
meta: {"points": 80, "comments": 66, "created": "2026-11-07T20:45:32Z"}
query: claude code

comment (qezz): > Is it public? > > Search your GitHub organization for .claude/settings.local.json and .claude/settings.json. Each hit is a file anyone can read right now. So, it's not necessarily "public", it's simply in the repository, and whether it's actually public or not depends on the repository settings. Or am I missing something
comment (Aurornis): Confusing headline. They scanned for repos where people had committed their .claude/ folder and local settings and then scanned those files for commands which contained keys or passwords. So pressing “Don’t Ask Again” by itself doesn’t expose passwords by itself. If you commit your local Claude settings and in those settings you have manually approved commands containing secrets directly in the command and then you publish the repo, that’s exposed.
comment (lacoolj): This page is like 80% repeating itself If you post output from AI, please remember to edit before publishing

## 12. [github] AkaraChen/cc-remote: Claude Code with the model on a remote host and the tools on your machine
key: gh:akarachen/cc-remote
url: https://github.com/AkaraChen/cc-remote
meta: {"stars": 285, "created": "2026-11-01", "pushed": "2026-11-04", "language": "TypeScript", "topics": []}
query: claude-code created:>{since} stars:>20

# cc-remote

Claude Code as an [ACP](https://agentclientprotocol.com) agent. The model runs on a remote host,
and the tools run on your machine.

You keep `claude` installed and logged in on one server. cc-remote reaches it over plain ssh and
runs every file read, edit and shell command locally, in the session's directory. Any ACP client
can use it: Zed, paseo, and others.

| Runs on your machine | Runs on the server |
|---|---|
| Read, Write, Edit, NotebookEdit, Bash (PowerShell on Windows), Glob, Grep | The model, the system prompt, the session |
| The MCP servers your ACP client brings, and those in your local Claude Code config | Web search, subagents, skills |
| Your `CLAUDE.md` files, git status, environment | The server's own settings and MCP servers |

The server only needs `claude`. Nothing else gets installed there, and your machine doesn't need
`claude` at all.

cc-remote is [claude-agent-acp](https://github.com/agentclientprotocol/claude-agent-acp) with one
change: the `claude` it starts runs on the server. Sessions, permission prompts, modes, models,
forks and diffs all work the way they do in claude-agent-acp.

## Requirements

Before you start, have these two in place:

- **ssh to the server works.** `ssh devbox` logs you in without a password prompt (use a key, and
  put ports, users and jump hosts in `~/.ssh/config`).
- **`claude` on the server is logged in.** Claude Code 2.1.248 or later, with a POSIX login shell.
  Run `claude` there once and log in, or use `cc-remote --cli auth login` after installing.

On your machine you need [Bun](https://bun.sh) to build cc-remote. The binary it builds has no
dependencies. It runs on macOS, Linux and Windows; on Windows it also needs the OpenSSH client
that ships with Windows 10 and later.

## Install

```sh
git clone https://github.com/AkaraChen/cc-remote && cd cc-remote
bun install
bun run compile    # builds the binary for this machine into dist/cc-remote
bun link           # puts cc-remote on your PATH, in ~/.bun/bin
```

`bun run compile` picks the `build: - ` script for the machine you run it on. To build
every platform at once (linux-x64, linux-arm64, darwin-arm64, windows-x64, windows-arm64), run
`bun run build`; the binaries land in `dist/`.

Tell it which host to use, then check the connection:

```sh
mkdir -p ~/.config/cc-remote && echo devbox > ~/.config/cc-remote/host
cc-remote doctor
```

cc-remote looks for the host in this order: `--host`, then `$CC_REMOTE_HOST`, then
`~/.config/cc-remote/host`. The host can be anything `ssh` accepts. Ports, keys and jump hosts
go in `~/.ssh/config`.

If you need a different ssh command, set `CC_REMOTE_SSH`. It works like rsync's `RSYNC_RSH`:

```sh
export CC_REMOTE_SSH="ssh -p 2222 -i ~/.ssh/devbox"
```

If the server isn't logged in yet, run `cc-remote --cli auth login`.

## Use

Once cc-remote is installed, it works with any client that speaks ACP. Add an agent whose command
is `cc-remote --host devbox` (or just `cc-remote`, if you wrote the host file above).

**Zed**, in `settings.json`:

```json
"agent_servers": {
  "Claude (devbox)": { "command": "cc-remote", "args": ["--host", "devbox"] }
}
```

**paseo**, in `~/.paseo/config.json` under `agents.providers`:

```json
"claude-devbox": {
  "extends": "acp",
  "label": "Claude (devbox)",
  "command": ["cc-remote", "--host", "devbox"]
}
```

For paseo there is also a plugin in [`paseo-plugin/`](paseo-plugin). Install it instead of editing
the config: it adds a "Claude (remote)" 

## 13. [hn] ChatGPT silently passes data between connectors and the bounty wants an ID card
key: hn:50399569
url: https://community.openai.com/t/security-follow-up-tool-call-silently-routed-to-a-different-connector/1413053
discussion: https://news.ycombinator.com/item?id=50399569
meta: {"points": 92, "comments": 39, "created": "2026-11-06T22:50:43Z"}
query: car data

comment (simonw): I assumed that the ID requirement was about sanctions compliance - OpenAI can't legally send money to someone in North Korea, for example. But https://docs.bugcrowd.com/researchers/managing-account/accou... says: > To improve platform integrity by reducing high volumes of low-quality submissions, identity verification (IDV) is now mandatory for all researchers before submitting reports to Managed Bug Bounty (MBB) programs (public and private, excluding on-demand MBBs).
comment (kristjansson): This seems like a fundamental misunderstanding / over estimation of the guarantees OAI and MCP can offer. If 'confirmation' is a separate tool call ... it's a separate tool call. There's no scoping, there's no 'binding', nothing. When you hand control back to the model you hand control back to the model.
comment (orf): Why did “techsoft.ye” feel the need to reply with a lengthy LLM comment that contained nothing useful at all?
