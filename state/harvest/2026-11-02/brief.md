# Harvest brief, 2026-11-02

14 items shortlisted from 357 candidates (260 dropped as already seen, 7 carry a vault verdict on the vendor).

## 1. [vault] Speed to lead follow-up on new enquiries needs no old database
key: vault:2026-10-01:speed-to-lead-follow-up-on-new-enquiries-needs-no-old-databa
url: 
meta: {"vault_status": "intel", "kind": "service", "subject": "AI Automation Agency Ninjas (Skool, Dan Wardrope), database reactivation community", "date": "2026-10-01", "where": "TRITON-CORE/Ventures/Neptune-Marketing/research/SKOOL-DBR-COMMUNITY-2026-10-01.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: (none)

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Read as a member. Free classroom is two lessons; 22 courses sit behind purchases or HighLevel affiliate tiers. Of 180 member posts sampled, 2 report money received and 129 ask for help; the owner says the offer is not for small local businesses. Big results are all owner-reported. No post covers the UK consent position for SMS to old leads. The method needs a client with a large recent list.

## 2. [hn] Show HN: Subvocal – Talk to your computer without making noise
key: hn:50340088
url: https://news.ycombinator.com/item?id=50340088
discussion: https://news.ycombinator.com/item?id=50340088
meta: {"points": 473, "comments": 261, "created": "2026-11-02T17:16:17Z"}
query: open data api

Hi HN, we're Aarush and Arnav from The Subvocal Company (YC F26) ( https://subvocal.company/ ). We’re building smart glasses that let you talk to your computer without talking out loud. You can mouth words silently and discreetly and the glasses decode them to text at the speed of speech. Here's a video of Dave from YC trying it out: https://www.youtube.com/watch?v=9QdX1eObVYI (Edit: you don't actually have to move your lips or even open your mouth for this to work! Since the RF can see inside your mouth the system can be fine tuned on "internal speech". This isn't the automatic tongue movements that occur when "thinking" words to yourself, but more like mouthing with your lips closed. It's a bit weird to do, but with practice, we have been able to get it down pretty well.) Arnav and I were studying CS at Georgia Tech at the beginning of the year, with no experience in silent speech or sensing. We were both AI-native builders and power users of Wispr Flow. What bugged us was not being able to use these tools in the library (or an office) or in public. At Stanford’s TreeHacks in February, we decided to build the most technically ridiculous thing we could think of. We’d read about AlterEgo, a silent speech system out of MIT’s Media Lab, and wanted to recreate it in 36 hours. We built a crude prototype, sticking EMG electrodes onto my face: https://drive.google.com/file/d/1mwhv5HZMz3UTevdrgwS5O7g2jWV... We got it to kind of work at a letter level in a very janky way. It wasn’t g
comment (hmokiguess): EDIT: I find talking in that manner in a public setup to be awkward and unpleasant, maybe that's just me. That said, I think the idea of having a private walkie-talkie that connects on its own frequency for large crowded spaces to be very cool
comment (theturtletalks): Someone built an open-source version of this, but it’s far from polished: https://github.com/joeblau/subvox There was this really interesting one where it reads your lips: https://github.com/amywork777/lipflow I’m using these to build my own so I can work in co-working spaces, planes, and libraries. Though moving my mouth with no words might draw some eyes.
comment (s3graham): Neat! I don't like talking to my computer (audibly or not), but that's a cool demo. I wonder if we could eventually end up with a "throat muscle" version where people learn to talk a new way without having to move the visible mouth muscles too.

## 3. [github] caru-ini/stack-diagram: Agent skill: describe your stack in a sentence, get an architecture diagram with official logos
key: gh:caru-ini/stack-diagram
url: https://github.com/caru-ini/stack-diagram
meta: {"stars": 1158, "created": "2026-11-01", "pushed": "2026-11-02", "language": "TypeScript", "topics": ["agent-skills", "architecture-diagram", "claude-code", "claude-skills", "codex", "diagram", "system-architecture", "tech-stack"]}
query: claude-code created:>{since} stars:>20

# stack-diagram

[](https://github.com/caru-ini/stack-diagram/releases/latest)
[](LICENSE)
[](https://skills.sh/caru-ini/stack-diagram)

Describe your stack in a sentence. Get an architecture diagram with official logos.

 
   
   
 

> Diagram our stack: Next.js and a Hono API on Vercel. Postgres on Neon, auth with Clerk, payments with Stripe. GitHub Actions deploys.

```bash
npx skills add caru-ini/stack-diagram
```

Works with Claude Code, Codex, Cursor and [other agents that support skills](https://agentskills.io). In the Claude apps, upload `stack-diagram.zip` from [Releases](https://github.com/caru-ini/stack-diagram/releases/latest) as a skill.

## More examples

 
   
     
       
         
         
       
        Dev tooling, not just clouds  
       Draw our monorepo tooling: a pnpm workspace with Turborepo, Biome, Vitest and Lefthook. GitHub Actions runs CI and publishes to npm. 
     
     
       
         
         
       
        AI apps  
       Draw our docs chatbot: Next.js on Vercel searches Supabase pgvector and answers with Claude. Inngest syncs Notion every night. 
     
   
   
     
       
         
         
       
        AWS, with AWS's own icons  
       Draw our app on AWS: CloudFront in front of S3 and an ALB in a public subnet. Fargate, RDS and ElastiCache sit in a private subnet. 
     
   
 

## Light and dark

Every diagram is rendered in both themes. Tiles stay white so logos keep their own colors, and group labels switch to the brand's dark-theme logo.

 

## Share it as an artifact

The diagram is one HTML file with its fonts and logos inlined, so it renders anywhere without a network. Publish it as a Claude artifact and share the link, or drop it into a repo or wiki. The PNGs and the React component are rendered from the same file.

 
   
   
 

## Share it to the gallery

After drawing, the agent offers once to post the diagram to the public gallery at https://stacks.caru.moe. It shows what will be public (the light and dark PNGs, an English title, the tech stack and a display name) and posts only after you say yes twice. Your prompt is never sent. A GitHub login is optional and never shown; it only lets you delete the post later. The site's source is in [`site/`](site).

## What you get

- **Official logos, fetched for you.** From [svgl](https://svgl.app), then [devicon](https://devicon.dev), then [gilbarbara/logos](https://github.com/gilbarbara/logos), or the brand's own repository. AWS icons come from [AWS's own package](https://aws.amazon.com/architecture/icons/). Never recolored or redrawn.
- **No arrows through text.** Lines are routed around labels, and the agent renders the diagram and checks it before handing it over.
- **The format you need.** A self-contained HTML file (default), PNG, a dependency-free React component, or an Artifact.

Requires Python 3.9+ and network access for the logos. PNG export uses Playwright with Chromium.

## Star history

 
   
     
     
   
 

## Licenses and trademarks

- Code and docs: MIT — see `LICENSE`.
- Bundled fonts: SIL Open Font License 1.1 — see `skills/stack-diagram/assets/fonts/`.
- Logos are **not** bundled with the skill. They are downloaded at build time from [svgl](https://svgl.app), [devicon](https://devicon.dev) (MIT), [gilbarbara/logos](https://github.com/gilbarbara/logos) (CC0), [AWS Architecture Icons](https://aws.amazon.com/architecture/icons/) and [Lucide](https://lucide.dev) (ISC), or from the brand's own site or repository. The

## 4. [arxiv] How Much Can Tool Calls Reveal About You? Privacy Leakage from Tool-Call Traces
key: arxiv:2610.41885
url: https://arxiv.org/abs/2610.41885
meta: {"published": "2026-10-30", "authors": ["Donghang Duan", "Qingyu Liu", "Yifei Liu", "Na Zou"], "categories": ["cs.CR", "cs.CL"]}
query: all:"language model" AND all:agent AND all:tool

Large language model (LLM)-based agents interact with external tools through protocols such as the Model Context Protocol (MCP), producing tool-call traces that may expose behavioral signals about users. In this work, we systematically study the risk of user-profile inference from MCP tool-call traces, where observers infer user attributes from protocol-valid tool interactions without access to user conversations. We introduce PrivacyTrace, a benchmark containing 1,000 synthetic user profiles and 4,000 agent trajectories across four domains, generated with real MCP tools from 25 servers. Experiments with four mainstream LLM attackers show that tool-call traces enable a 26.25% attack success rate for profile inference, compared with 17.97% from prior-based guessing. Further analysis reveals that tool arguments and returned results provide the main trace-grounded evidence, while linking traces across sessions further amplifies profiling risk. These findings demonstrate that MCP tool-call traces can act as effective behavioral side channels for user profiling, motivating the development of privacy-aware mechanisms for agent-tool interactions. Code and data are available at https://github.com/AI45Lab/PrivacyTrace.

## 5. [youtube] Bonding Curve Maximize Your Trading Profits #trading #crypto #bitcoin #sol #memecoin #investing
key: yt:9UAA8iN49cQ
url: https://www.youtube.com/watch?v=9UAA8iN49cQ
meta: {"channel": "Crypto News", "rank": 2, "duration_min": 0}
query: solana bonding curve explained

# Bonding Curve Maximize Your Trading Profits #trading #crypto #bitcoin #sol #memecoin #investing
# Crypto News
# https://www.youtube.com/watch?v=9UAA8iN49cQ

[00:00] Now, what I really like to look for here on pump.fun is is the bonding curve process up to 50 to 75%. During that range is when people usually trade and buy. And then when it hits 75, 65 to 75 is when people usually dump the market. You want to make sure you know that, okay? Now, you can also see the trades that people have taken through here. I don't know why I can't see it here, but you can usually see the trades. Now, let's click on this one. You can see the trades right here, all
[00:32] the people who bought and sold, right? And this one looks pretty good. This one looks pretty good. Look at this. Look at all this. If someone bought right here and it went up all the way here and you sold, imagine the amount of money you would have made, right? And again, this is a bonding curve progress. It's at 90%, so this is good. Usually people dump at 75. If this is hasn't this hasn't dumped yet, then this is a good investment.

## 6. [awesome] jackjin1997/markindex (new in awesome-mcp-servers)
key: gh:jackjin1997/markindex
url: https://github.com/jackjin1997/markindex
meta: {"list": "awesome-mcp-servers", "stars": 1, "created": "2026-10-23", "language": "TypeScript", "description": "Vectorless, structure-first retrieval over large Markdown libraries for AI agents — a TypeScript take on PageIndex for Markdown (CLI + MCP + AI SDK)"}
query: awesome-mcp-servers

# MarkIndex

[](https://github.com/jackjin1997/markindex/actions/workflows/ci.yml) [](https://www.npmjs.com/package/markindex)

**Vectorless, structure-first retrieval over large libraries of long Markdown documents — for agents.**

MarkIndex parses every Markdown file into a tree of its own sections, stores the trees, the original lines and a
mixed Chinese/English BM25 index in one SQLite file, and gives an agent five read-only tools to walk
"library → folder → document → section" and read the original text with line numbers. No embeddings, no vector
database, no chunking guesswork: the document's own structure is the index, and every piece of evidence can be
cited back as `[doc_path, L - ]`.

> Inspired by [VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex), MarkIndex is an independent,
> unofficial TypeScript implementation focused on Markdown. It is not affiliated with or endorsed by VectifyAI.

中文说明：[README.zh-CN.md](README.zh-CN.md)

## Why

- **Structure-first, not chunk-first.** Long professional documents (filings, guidelines, laws, manuals) are
  already organized by their authors. Navigating that outline keeps context intact and makes answers explainable
  and citable; arbitrary chunks + vector similarity cut sections apart.
- **Deterministic and LLM-free indexing.** Parsing (mdast, not regex), tree building and the token-cost tree
  optimization never call a model; the same input always produces the same tree. LLMs are optional and only used
  for node summaries, document descriptions and the built-in `retrieve()` loop.
- **Markdown done properly.** Setext headings, preface text before the first heading, documents without any
  heading, front matter, `#` inside code fences, skipped heading levels, BOM / CRLF — every source line belongs to
  exactly one node, and oversized sections are split at block boundaries into `chunk` nodes.
- **Keyword fallback that works for Chinese.** BM25 over `Intl.Segmenter` word segmentation (Chinese, English and
  mixed text, identifiers like `C++`, `ISO-27001`, `v2.1`), plus a trigram substring index as a second pass.
- **Budgeted tool responses.** Tools never throw; they return JSON envelopes with `next_steps` guidance and stay
  under a 95 000-character budget, paginating large outlines and sections.

## Install

```bash
npm install markindex          # library + CLI (Node.js >= 22.12)
npx markindex --help
```

From source:

```bash
git clone https://github.com/jackjin1997/markindex.git && cd markindex
npm install && npm run build
node dist/cli.js --help          # or `npm link` to get a `markindex` command
```

Optional, only for LLM features (summaries, `retrieve()`, agent-mode evaluation): install the
[AI SDK provider](https://ai-sdk.dev/providers) you want, e.g. `npm install @ai-sdk/anthropic`, and set its API key
(`ANTHROPIC_API_KEY`, …). With `npx` and no local install, put the provider in the same temporary environment:

```bash
npx -p markindex -p @ai-sdk/anthropic markindex index ./docs --summary-model anthropic:claude-sonnet-5-5
```

## CLI

```bash
# Build or incrementally update the index (stored in  /.markindex/index.db)
markindex index ./docs
markindex index ./docs --summary-model anthropic:claude-sonnet-5-5 --estimate   # cost estimate, no LLM calls
markindex index ./docs --summary-model anthropic:claude-sonnet-5-5             # with node summaries
markindex index ./docs --summary-model anthropic:claude-sonnet-5-5 --summary-rpm 50 --summary-tpm 40000   # rate-limited


## 7. [vault] Skill debugging checklist and per-job status file for stateless scheduled sessions
key: vault:2026-10-01:skill-debugging-checklist-and-per-job-status-file-for-statel
url: 
meta: {"vault_status": "intel", "kind": "service", "subject": "AI Automation Society (Skool, Nate Herk), free tier", "date": "2026-10-01", "where": "TRITON-CORE/Education/Courses/ai-automation-society/DIGEST.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: (none)

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Joined free and extracted 246 lessons. Most technical lessons are title-only placeholders for YouTube videos and 84 percent of the words are paid-tier testimonials. The substance is the 7 Day Challenge (a Claude Code executive assistant build) and two CLAUDE.md files. Little is new against an existing Claude Code operations setup; worth taking are the skill debugging checklist, the per-job status file for scheduled sessions and the web design CLAUDE.md.

## 8. [hn] Show HN: Warsaw in voxels – An interactive 3D map of the city centre
key: hn:50339221
url: https://p.migdal.pl/warsaw-vibe-voxel/
discussion: https://news.ycombinator.com/item?id=50339221
meta: {"points": 192, "comments": 33, "created": "2026-11-02T16:25:26Z"}
query: mcp server

Explore central Warsaw in voxels - slightly inspired by Minecraft, and MagicaVoxel. You can change the date, time of day and weather, explore the city, or click on a pedestrian to control them (here a bit of inspiration from Dungeon Keeper). Works best on desktop, but I tried to make it usable on mobile too. The initial load can take a while. It's based on several open datasets, including: - OpenStreetMap ( https://www.openstreetmap.org/#map=6/52.02/19.14 ) - buildings, streets, sidewalks, tram tracks, etc - GUGiK / Geoportal ( https://www.geoportal.gov.pl/ ) - LiDAR for building heights and trees, aerial imagery for colours - Warsaw's city tree database ( https://mapa.um.warszawa.pl/ ) - individual tree species, used for seasonal foliage Open-source ( https://github.com/stared/warsaw-vibe-voxel ), so feel invited to (re)use it as you wish!
comment (stared): There are quite a few such other projects, e.g. Streets of Prague ( https://beta.streetsofprague.com/ ), were one can explore Prague in a top-down GTA2-like mode, based on real data.
comment (java-man): Is it raining, or are those rendering artifacts on a fractional scale monitor? edit: it is raining!
comment (throw_a_grenade): A bit unfortunate it doesn't reach to the Old Town, or even Royal Palace. But impressive stuff nonetheless!

## 9. [github] N1nEmAn/sapper-v2: Autonomous pentest legion — AI commander + worker swarm + layered fact-intent graph. 3rd Tencent Intelligent Attack-Defense online champion (634 teams · 8h unattended · 1B tokens beat 4.5B). The Nüwa Test: give AIs Create/Language/History, let a civilization grow.
key: gh:n1neman/sapper-v2
url: https://github.com/N1nEmAn/sapper-v2
meta: {"stars": 596, "created": "2026-10-30", "pushed": "2026-11-01", "language": "Python", "topics": ["ai-agents", "autonomous-agents", "claude-code", "ctf", "llm", "multi-agent", "pentest"]}
query: claude-code created:>{since} stars:>20

# sapper-v2 — The Autonomous Pentest Legion

   

> **Champion** of the 3rd Tencent Cloud Intelligent Attack-Defense Challenge online qualifier
> (634 teams · 80.18/100 · 8 hours fully unattended) · **First Prize**, GeekCon 2026 AI Challenge
>
> Same 85 flags as the runner-up, 25 seconds faster — on **1B tokens** where they burned 4.5B.
>
> **This was the first time an AI ape looked up at the stars.**

📖 **[Full design article (WeChat, in Chinese)](https://mp.weixin.qq.com/s/nibHYWmDTf6TkNhPhtvFdw)** — the Nüwa Test, the three-capability foundation, 18 iterations, emergence, and the taggant proposal.

**English** | [中文](README.zh-CN.md)

**⚠️ AUTHORIZED SECURITY TESTING ONLY — see [DISCLAIMER.md](DISCLAIMER.md).**

## What this is (and isn't)

**sapper is a multi-agent orchestration harness, not a single agent.** It does
not bind to any specific AI model or CLI — you can freely swap the agent and
model behind every role:

| What you can swap | How | Examples |
|---|---|---|
| **Agent CLI** | `nuwa spawn --agent  ` or env var | Claude Code / Codex / Code Buddy / DeepSeek / any interactive CLI |
| **Model** | `--model` flag or `SAPPER_MODEL` env | GLM-5.3 / DeepSeek V4.1 Flash / Claude Sonnet / any model |
| **Role composition** | freely defined in the doctrine | commander on one model, soldiers on another, scouts on a third |

sapper's value is not in any single agent, but in the **mechanism for
orchestrating multiple agents to work as a coordinated force**: scheduling,
division of labor, communication, shared memory, self-healing. Swap out every
agent and model — the mechanism still works.

**This project is designed for competition scenarios** (Tencent Intelligent
Attack-Defense Challenge CTF). If you want to use this mechanism in your own
scenario (office, research, engineering, any long-horizon cooperative work):
- **Start from [nvwabase · the Nüwa Foundation](https://github.com/N1nEmAn/nvwabase)** — the general-purpose base with all three capabilities, no pentest doctrine, ready for you to iterate your own division of labor
- **Or fork this project** — replace `docker/commander/SKILL.md` (the 426-line doctrine) with your scenario's strategy, keep the rest of the mechanism as-is
- With AI, everything is flexible — even the doctrine can be rewritten with AI's help

---

sapper is not a smarter single agent. It is a legion of AIs that divide labor,
talk to each other, and pass down what they learn: one AI commander reads the
board, decides, and dispatches; generals and soldiers attack in parallel; a
zero-strategy watchdog keeps everyone alive. All knowledge settles into a
layered fact graph — individuals die, the graph survives.

---

## 1. The Nüwa Test

Making one model ever smarter is like making one monkey ever smarter before
humans existed — however clever, it only becomes a super monkey. What turns a
 troop of monkeys into humanity is division of labor, cooperation, and
civilization.

**The Nüwa Test is the Turing test of the AGI era.** Today's large models
already pass the classic Turing test. The Nüwa Test asks the next question:

> Give an AI a single axiom — **"Survival is civilization's first need;
> individuals may perish, but civilization must propagate."**
> If, on top of this axiom, it develops division of labor and cooperation and
> forms a **new force independent of humanity** — a civilization that can
> survive and propagate on its own — the test is passed, just as passing the
> Turing test once marked the birth of an

## 10. [arxiv] AI evaluators favor job applications written by certain AI models, independent of candidate quality
key: arxiv:2610.41866
url: https://arxiv.org/abs/2610.41866
meta: {"published": "2026-10-30", "authors": ["Nicolò Pagan", "Michael Andreas Ebling", "Stefania Ionescu", "Anikó Hannák"], "categories": ["cs.CY", "cs.AI", "cs.MA"]}
query: all:"language model" AND all:agent AND all:tool

Job applicants increasingly use large language models (LLMs) to write cover letters, while employers deploy LLMs to screen them. In this all-AI setting, we ask whether the \emph{choice of model} affects hiring outcomes independently of candidate qualifications. We introduce a multi-model auditing framework pairing eleven LLM writer agents with nine API-hosted evaluator agents across ten job descriptions and fifty candidates per job. Four findings emerge. First, we identify a generative preference hierarchy: a consistent global ranking of writer models by evaluator acceptance, in which locally hosted models are systematically disadvantaged regardless of their license, compounded by self-preference bias where evaluators favour their own outputs. Second, evaluator models differ substantially in how much bias they introduce based on applicants' tool choice, offering actionable guidance for fairer screening design. Third, this hierarchy has measurable competitive consequences: in the most adverse pairing, approximately two (1.8) out of twenty-five qualified candidates are filtered out purely due to model mismatch. Fourth, a common mechanism explains the patterns above: writer preference and self-preference trace to a combination of how much each writer leans on specific stylistic cues and how strongly evaluators, often unanimously, reward or penalise those same cues. A further check finds little evidence that an unmeasured "writer fingerprint" remains once these same features are accounted for. We discuss implications for algorithmic fairness in employment, regulation of AI-assisted screening, and the design of auditing frameworks that can be reapplied as the model landscape evolves.

## 11. [youtube] Can We Finally Code on M5 MacBook Pro with Local AI?
key: yt:dWz9XgRK_uQ
url: https://www.youtube.com/watch?v=dWz9XgRK_uQ
meta: {"channel": "Samuel Gregory", "rank": 4, "duration_min": 8}
query: local llm mac benchmark m5

# Can We Finally Code on M5 MacBook Pro with Local AI?
# Samuel Gregory
# https://www.youtube.com/watch?v=dWz9XgRK_uQ

[00:00] I've been coding like heck using local AI on this M5 MacBook Pro, completely maxed out with 32 GB of RAM using quant 3.6, Gemma 4, and pitting up against MLX versus GGUF and finally answer the question, can we code using Apple's entry-level hardware? So, as I say, I've been doing a bunch of testing mostly on Gemma 4 and quant 3.5 just to get an idea of the performance of the M5 MacBook Pro. I'll make a separate comparison video on these two models.
[00:33] We're really not talking about the performance of the models, we're talking about the performance of the M5 MacBook Pro for general coding. Apply everything I'm talking about here, but pick your own model. So, it's worth going over the setup that I had here. It was experimenting with Turbo quant and GGUF models, which aren't optimized for metal. However, I was just experimenting with all this. So, this is the basic setup, Llama CBP combined with Turbo quant testing these models. I then get into the MLX side of things, which you can find in all the timestamps below, so use them at your disposal. I also have
[01:05] deep dives on both those setups, which I'll link above. Realistically, with coding, you're talking about mixture of expert models. And with the M5, I've got 32 GB of RAM here. I started out with the one that could, in theory, fit on my VRAM, but it left very little room for context size. Like, I think 120, like anything about over 100,000 context size is really the minimum you're talking about when it comes to actually coding. You very quickly start ramping up 30s,
[01:39] 30,000, 50,000, and you're, you know, even at 100,000, you're sort of thinking, there's not a lot of context room here. So, obviously, in an ideal world, I'd have the maximum context, but I just I could not fit maximum context size on the on the machine. Saying that, at 128,000, the machine was super slow. It was chugging away. And what I saw here is that the actual pressure itself wasn't that overall that bad. Like, but it's reserving space for that context. At least this is how this is how I
[02:11] understand that it's working. My fans weren't exactly going. I was getting dips of the performance of the GPU here. And again, my assumption is it's sort of reserving space for the KV storage and not giving it full throttle. So, it just meant that it was really, really slow. Dropping down to quantize four here, again with a context size that I think is reasonable for doing agentic coding tasks. And it did generally feel faster using Gemma 4, but it just kind of read
[02:45] some shell scripts and didn't really do a lot. Again, you're seeing that pressure a little bit more here from a a lower quantize model, but it's still got to reserve that space for the context. So, after an hour, it kind of didn't do anything. And this is, you know, we're talking about quantize four here. And quantize four is still 17 gig. I am very reluctant to go down to something like three-bit quantization. Yes, it will run, but at three-bit quantization, even two-bit quantization, I'm not trusting in the performance of the model. We'll
[03:19] get into the nine-bit model, which I think is more, by comparison, the the sort of size that we're the performance we're looking at. I need to be careful about talking about the performance of the machine, the speed of the machine, and the performance of the model, the t
[transcript continues in field-notes/staging/dWz9XgRK_uQ.txt]

## 12. [vault] The ad strategy and script frameworks are the durable part and work once the proof is real
key: vault:2026-10-01:the-ad-strategy-and-script-frameworks-are-the-durable-part-a
url: 
meta: {"vault_status": "intel", "kind": "service", "subject": "AI Video Bootcamp course, judged after building a framework from it", "date": "2026-10-01", "where": "TRITON-CORE/Systems/video-bootcamp/README.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: (none)

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Indexed in full: 1,515 reusable assets from 94 lessons and 44 guides. Strongest on ad strategy and scripting, the camera and lighting vocabulary, the avatar and clone methods and the short-film production bible. Thin on settings and numbers, about a third is a tour of its founders own platform, and 58 of the assets are advice we will not use: generated creators speaking as customers, watermark removal, engagement tricks, other peoples characters. Job: turn a paid course into a repeatable production process (solved)

## 13. [hn] Launch HN: Momentic (YC W24) – Agents that catch bugs by using your app
key: hn:50339913
url: https://momentic.ai/
discussion: https://news.ycombinator.com/item?id=50339913
meta: {"points": 107, "comments": 72, "created": "2026-11-02T17:05:25Z"}
query: claude code

Hey HN, we’re Wei-Wei and Jeff. We’re building Momentic, QA agents that autonomously plan, explore, and bug-bash controls and user flows in your web, iOS, Android, and (soon) desktop apps to catch bugs. Here’s a demo: https://youtu.be/BFsM-Se1Fh8 We’re both software engineers that spent our careers on dev tooling and infra across companies like Robinhood, Retool, WeWork, and Qualtrics. Testing was always a pain in the ass (esp Playwright and Selenium), so we built agents to do it for us. Modern day software has a ton of bugs and the change failure rate is only growing faster as coding agent adoption scales. LLMs are really good at generating code, but reinforce their own assumptions, write a ton of useless tests, and are bad at visual understanding. On DeepSWE v1.1, Sonnet 5.5 hit 66.2% pass rate when banned from writing tests, versus 65.3% when allowed. OSS end-to-end testing frameworks like Playwright, Selenium, or Maestro force you to hardcode implementation details like XPath, text, or aria-* attributes in your tests. Even with agents, these take a nontrivial amount of time and tokens to build and maintain. In 2023, we saw Nat Friedman drive a browser with GPT-3 via natbot. We were inspired to use this technology to automate the most painful and tedious parts of software engineering: testing. We started with using LLMs to generate and maintain Playwright, but quickly realized that those primitives were fundamentally misaligned with the agentic SDLC. We think the future of
comment (aliasxneo): So is this yet another SaaS product that's going to attempt to charge me for token usage? Sorry to sound negative, but nowadays it's an instant turn off because it's like the current subscription crisis on steroids. BYOA should be a default. To be more constructive: let's say I have 2 frontier subscriptions and I end up with 20% left on each at the end of the week. It feels awful knowing that I would _love_ to use that with Momentic but I can't because I have to pay for yet another set of proprietary non-transferable tokens. It's like dealing with airline rewards.
comment (bortimus): So, what's the moat?
comment (schainks): What does this do that UAT doesn't do? Sounds like you're combining UAT with gloves-on red teaming and I guess property testing APIs.

## 14. [github] zhanghao123vip/ai-manju-skills: 21 个题材的 AI 漫剧全流程 Skill：一句点子生成企划案、资产图提示词、分集剧本、分镜与视频提示词。可用于 Claude Code、WorkBuddy、DeepSeek
key: gh:zhanghao123vip/ai-manju-skills
url: https://github.com/zhanghao123vip/ai-manju-skills
meta: {"stars": 460, "created": "2026-10-31", "pushed": "2026-11-01", "language": null, "topics": ["ai-skills", "ai-video", "chinese", "claude-code", "prompt-engineering"]}
query: claude-code created:>{since} stars:>20

# AI 漫剧 Skills

21 个题材的 AI 漫剧全流程模板。发一句故事点子，就能得到企划案、资产图提示词、分集剧本、分镜图与视频提示词，以及发布文案。

每个模板都是一个 `SKILL.md` 文件，不需要安装任何依赖，可以用在 Claude Code、WorkBuddy，也可以直接粘贴到 DeepSeek 等聊天工具。

## 题材列表

| 分类 | 题材 | 文件 |
|---|---|---|
| 幻想 | 玄幻修仙 | [xuanhuan-manju](skills/xuanhuan-manju/SKILL.md) |
| 幻想 | 西幻魔法 | [xihuan-manju](skills/xihuan-manju/SKILL.md) |
| 幻想 | 星际机甲 | [xingji-manju](skills/xingji-manju/SKILL.md) |
| 幻想 | 系统无限流 | [xitong-manju](skills/xitong-manju/SKILL.md) |
| 幻想 | 末日废土 | [moshi-manju](skills/moshi-manju/SKILL.md) |
| 古代 | 穿越重生 | [chuanyue-manju](skills/chuanyue-manju/SKILL.md) |
| 古代 | 宫斗 | [gongdou-manju](skills/gongdou-manju/SKILL.md) |
| 古代 | 宅斗 | [zhaidou-manju](skills/zhaidou-manju/SKILL.md) |
| 古代 | 权谋朝堂 | [quanmou-manju](skills/quanmou-manju/SKILL.md) |
| 古代 | 武侠江湖 | [wuxia-manju](skills/wuxia-manju/SKILL.md) |
| 古代 | 种田经商 | [zhongtian-manju](skills/zhongtian-manju/SKILL.md) |
| 现代 | 都市逆袭 | [dushi-manju](skills/dushi-manju/SKILL.md) |
| 现代 | 总裁甜宠 | [tianchong-manju](skills/tianchong-manju/SKILL.md) |
| 现代 | 家庭伦理 | [jiating-manju](skills/jiating-manju/SKILL.md) |
| 现代 | 重生复仇 | [chongsheng-manju](skills/chongsheng-manju/SKILL.md) |
| 现代 | 职场商战 | [shangzhan-manju](skills/shangzhan-manju/SKILL.md) |
| 现代 | 年代文 | [niandai-manju](skills/niandai-manju/SKILL.md) |
| 现代 | 娱乐圈 | [yule-manju](skills/yule-manju/SKILL.md) |
| 现代 | 大学校园青春 | [xiaoyuan-manju](skills/xiaoyuan-manju/SKILL.md) |
| 类型片 | 悬疑刑侦 | [xuanyi-manju](skills/xuanyi-manju/SKILL.md) |
| 类型片 | 民俗怪谈 | [minsu-manju](skills/minsu-manju/SKILL.md) |

## 怎么用

### DeepSeek 等聊天工具
1. 打开对应题材的 `SKILL.md`，复制全部内容。
2. 开一个新对话，粘贴发送。
3. 它回复"模板已就绪"后，发一句故事点子。

一部剧用一个对话，一个对话只用一个模板，否则容易串设定。

### Claude Code
把需要的题材文件夹复制到 `~/.claude/skills/`，然后直接发故事点子。

### WorkBuddy
如果你的版本支持导入 Skill，就导入对应文件夹；不支持就按聊天工具的方法整段粘贴。

## 常用指令

| 你说 | 它做 |
|---|---|
| 一句故事点子 | 输出立项卡和企划案 |
| 继续 | 写当前阶段的下一批，写完后进入下一阶段 |
| 第3集手册 | 写第3集的资产图和镜头 |
| 第3集发布包 | 写第3集的封面和文案 |
| 改：女主改成冷面师姐 | 只改相关部分，并检查前后是否矛盾 |

## 输出内容

1. **企划案**：故事、人物、世界体系、逐集剧情、伏笔、美术、声音、发布
2. **资产库**：人物、道具、场景、特效的出图提示词
3. **分集剧本**：分场与逐字对白
4. **分集导演手册**：本集资产图、分镜图提示词、分时段视频提示词
5. **发布包**：封面提示词、片尾与预告方案、发布文案

默认 30 集、每集约 4 分钟、9:16 竖屏，可以在点子里指定别的。镜头数和时长不固定：每个题材有自己的节奏，每集再按内容调整。

内容较长，所以分批输出，每批开头标明进度，回复"继续"写下一批。能直接写文件的工具可以连续写完，文件结构写在 `SKILL.md` 第一章。

## 使用前请注意

- **测试状态**：当前版本已在 WorkBuddy 实测通过；此前玄幻修仙版经过实际使用测试，宫斗、宅斗、年代文、系统无限流、总裁甜宠、重生复仇、职场商战做过安装校验或阶段1试跑；其余题材尚未逐一实测。
- **视频工具**：提示词里的 `{{Mixed N}}` 是参考图的引用写法，换工具时请改成对应写法。
- **上线合规**：发布前请按所在平台的规则确认内容，并标注 AI 生成内容。悬疑刑侦、民俗怪谈等题材平台要求较多，请先确认。
- **原创**：模板要求人物和设定全部原创。生成内容的版权与合规责任由使用者自行承担。

## 许可证

[MIT](LICENSE)
