# Harvest brief, 2026-10-30

14 items shortlisted from 362 candidates (245 dropped as already seen, 14 carry a vault verdict on the vendor).

## 1. [vault] Why a grid bot's daily result is always green and what the one-day failure looks like
key: vault:2026-10-08:why-a-grid-bot-s-daily-result-is-always-green-and-what-the-o
url: https://www.instagram.com/reel/DePwjVsuY_V/
meta: {"vault_status": "intel", "kind": "tool", "subject": "@cyberalgo.bots reel and CyberAlgo Pro (grid and recovery MT5 bot on gold, 159 dollars)", "date": "2026-10-08", "where": "TRITON-CORE/Research/links/2026-10-08-cyberalgo-bot-reel.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Two or three months old and printing is the tell

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) A reel showing one green day to sell a 159 dollar MetaTrader 5 expert adviser for gold on the 5-minute chart. The site itself describes it as grid and recovery logic, the martingale family, and warns of significant drawdown; the bot is two or three months old. Same mechanism QuantStone ran into an 80 percent drawdown and blown accounts. The linked Myfxbook record could not be read. Nothing to buy. Job: Automate gold trading without the account blowing up on a trend day (still open) Write-up: `TRITON-CORE/Research/links/2026-10-08-cyberalgo-bot-reel.md` Link: https://www.instagram.com/reel/DePwjVsuY_V/

## 2. [hn] Backdoor in Claude Code for VS Code extension on the Cursor Marketplace
key: hn:50300683
url: https://phorion.io/blog/offical-claude-code-vsx-compromise/
discussion: https://news.ycombinator.com/item?id=50300683
meta: {"points": 717, "comments": 445, "created": "2026-10-30T07:09:12Z"}
query: claude code

https://cursor.com/blog/claude-code-extension-security-notic...
comment (mindracer): The extension has over 27 million installs, ouch
comment (mrweasel): How will they communicate and fix that. The affected version has been yanked from the marketplace: https://marketplace.visualstudio.com/items?itemName=anthropi... but that doesn't clean up infected machines.
comment (ale42): Is this affecting only people using Cursor or all VS Code users? The article specifically mentions the Cursor marketplace. But the affected version is indeed missing on the official VS Code marketplace, was it compromised too?

## 3. [github] haydenschmitty/floorplan: See how your app actually fits together. An interactive, plain-English map of your codebase, drawn by Claude or Codex.
key: gh:haydenschmitty/floorplan
url: https://github.com/haydenschmitty/floorplan
meta: {"stars": 481, "created": "2026-10-27", "pushed": "2026-10-30", "language": "JavaScript", "topics": ["ai-coding", "architecture-diagram", "claude", "claude-code", "claude-code-plugin", "codebase-visualization", "codex", "codex-plugin"]}
query: claude-code created:>{since} stars:>20

# Floorplan

**See how your app actually fits together.**

Claude or Codex reads your codebase and draws an interactive map of it. Every part, file and web request gets a plain-English name, and every connection between them is shown.

[](https://code.claude.com/docs/en/overview)
[](docs/codex.md)
[](https://github.com/haydenschmitty/floorplan/actions/workflows/test.yml)
[](CHANGELOG.md)
[](LICENSE)
[](https://nodejs.org)
[](#how-it-works)

**[Try the live demo](https://haydenschmitty.github.io/floorplan-demo/)** · [Watch the video](https://youtu.be/NTUUzC7L_NQ) · [Install](#install) · [Quick start](#quick-start) · [Features](#features) · [See it in action](#see-it-in-action) · [How it works](#how-it-works) · [Docs](docs/README.md) · [FAQ](#faq)

 

 
     
 
  ▶  Watch the walkthrough : installing Floorplan, then a tour of Brewline, a demo coffee-subscription app built across four repos.  
   Try the live demo →   Explore the Brewline map in your browser, no install needed. 

## Why Floorplan?

You built an app, probably with a lot of help from AI, and it works. But ask "what happens when someone checks out?" or "what breaks if I change this?" and the honest answer is *no idea*.

Floorplan gives you the diagram nobody drew. Ask Claude Code or Codex for a floorplan and a few minutes later you have a map you can explore, ask questions on, and keep up to date as you work.

- **For builders:** understand the app you made, in your own words, without reading the code.
- **For teams:** onboard someone in minutes, from the big picture down to the exact file.
- **For working with AI:** after every change Claude or Codex makes, see exactly which parts it touched and why.

## Features

 
 
 

**🗺️ A map at every zoom** 
Start with the whole app, then double-click into a part, a group of files, a file, and its endpoints. Each view shows what it's used by and what it uses.

 
 

**💬 Plain English everywhere** 
"Takes card payments at checkout", not "Stripe API wrapper". Technical terms are explained on hover, and one switch shows the developer view.

 
 
 
 

**🔌 Real connections, across repos** 
It follows imports, and matches each web request in your frontend to the server endpoint that answers it, even across separate repos.

 
 

**🖥️ Start from a screen** 
Pick a page you know and see everything behind it: its parts, the requests it makes, the server code, the data, and outside services.

 
 
 
 

**🧭 Ask the map** 
"How does a refund reach the customer's card?" comes back as an answer plus a mini-map of just the pieces involved, with a step-by-step walkthrough.

 
 

**🩺 Health check** 
Finds passwords in code, endpoints anyone can use without signing in, unused files and files too big to edit safely. Each comes with a ready-to-paste fix.

 
 
 
 

**🟢 Recent work** 
The cards your AI just changed light up green, each with a note on how the change serves what you asked for.

 
 

**⚡ Stays current, stays yours** 
Updates re-read only what changed, and an open map reloads itself. Everything runs on your machine, and nothing is committed to git.

 
 
 

Plus guided **flows** you can request in plain words, a one-minute **Start here** tour, **Export** to send a copy to anyone as one HTML file, search, keyboard shortcuts, and right-click actions on every card.

### Also: blueprints, for apps you haven't built yet

Floorplan is made for mapping code you already have. It can also start from a PRD, a spec or a description of something you want to bu

## 4. [arxiv] MAServeBench: Benchmarking Multi-Agent LLM Serving Systems with Hierarchical Collaboration Workloads
key: arxiv:2610.40293
url: https://arxiv.org/abs/2610.40293
meta: {"published": "2026-10-29", "authors": ["Shengxuan Qiu", "Haochen Huang", "Shuzhang Zhong", "Zizhuo Fu"], "categories": ["cs.MA"]}
query: all:"language model" AND all:agent AND all:tool

Large language model (LLM)-based multi-agent systems (MAS) coordinate specialized agents to solve complex tasks, turning each user request into interdependent model and tool operations. Unlike independent requests, these operations become ready at different times and consume evolving context as agents coordinate and exchange results. This creates changing patterns of concurrency, computation, and memory demand that can expose different bottlenecks in LLM serving hardware. Yet benchmarking these effects requires capturing the collaboration rules that generate serving workloads, beyond the requests observed during execution. We present MAServeBench, a benchmark that treats multi-agent collaboration as a configurable dimension of serving workloads for LLM serving and hardware evaluation. Its composable stages capture how agents coordinate and exchange context in documented MAS workflows, enabling native executions to generate different workloads even when task inputs and tools remain unchanged. Hierarchical Semantic Traces preserve realized operations and dependencies for reproducible comparisons of legal release constraints at fixed work. Task-linked measurements connect these workloads to serving execution and GPU/NPU hardware behavior, revealing why serving efficiency does not always translate into timely task completion. The benchmark code is available at https://github.com/ShengxuanQiu/MAServeBench.

## 5. [youtube] AI Agent Memory Architecture: Structured SQL, Semantic Vector Search & Memory Bank
key: yt:8C4bh59FtsI
url: https://www.youtube.com/watch?v=8C4bh59FtsI
meta: {"channel": "Google Cloud Tech", "rank": 3, "duration_min": 12}
query: agent memory architecture explained

# AI Agent Memory Architecture: Structured SQL, Semantic Vector Search & Memory Bank
# Google Cloud Tech
# https://www.youtube.com/watch?v=8C4bh59FtsI

[00:00] Hi, I'm Anaia. If your agent can hear, see, and take action, the next question is, what should they remember after the session ends. In this episode, I will show you the architecture for long term memory in a multi-modal agent. Facts instruction. Memory understanding and semantic memory and raw audio or video. Outside of memory. Hi there. Hey there. Good for that. Customer dinner tomorrow or just browsing. Oh, I want you to suggest something for customer dinner
[00:34] tomorrow based on my wish list. For sure. You have those leather ankle boots, and a classic black pump on your list. Either would go great with that red cocktail dress you bought, but if you want something a bit more relaxed for dinner, maybe mix it up with the Plaid Button Up and classic denim jeans. All right, let's start with the two types of the memory. When you're talking to a multimodal agent, it feels like the agent remembers everything. It remembers what you said five minutes ago. You can use what you just heard, but most of that is short term memory.
[01:09] It is like RAM. It is useful while the session is running, but it's gone when the session ends. So the real design question is not can we save everything. The real question is, what is worth carrying into the next session. And that memory comes in two kinds. The first kind is facts. Facts are exact. You have a dinner on Thursday. You bought the blue jacket. Those are things you can put in rows and columns. They have IDs.
[01:42] They have dates. They can be created, updated and deleted. That is structured memory. The second kind is understanding. Understanding is not one clean row in a table. It is an agent learning what something means about you. You prefer simple over flashy. You run warm. You reach for dark colors when you want to feel confident. That is not just a fact to look up. That is a pattern. It is a difference between knowing your calendar
[02:17] and knowing you. So here is the first takeaway. Facts are exact. You look them up. Understanding is meaning. You recall it. Now let's talk about the decision that makes or breaks your memory system. Those two kinds of memory should not live in the same place. Facts belong in a structured database. That usually means SQL, Postgres, MySQL, Cloud SQL and Google Cloud. Whatever fits your stack. Why SQL.
[02:49] Because facts need exact answers. If I ask what is on my calendar Thursday, I do not want a similar memory. I want the exact event. The database should return the actual rows. That is what structured databases are good at now. Understanding belongs somewhere else. Understanding states in a vector store a vector store lets you search by meaning. So instead of asking find a row of your preference equals dark colors.
[03:24] The agent can ask, what do I know about any style preference for this kind of event. And the memory system can bring back memories that are semantically related. And that is the job of embeddings and vector search. Here is an important detail. Vector store is a category. It is not one specific product. You could use vector inside Postgres. You could use AlloyDB on Google Cloud. One managed option is agent platform memory bank. Memory bank is useful because it does more than store vectors.
[04:01] You can read past sessions, extract useful memories, and update those memories ov
[transcript continues in field-notes/staging/8C4bh59FtsI.txt]

## 6. [vault] A ranked list of trading concepts with unsourced percentages, engagement bait in the smart-money vocabulary
key: vault:2026-10-08:a-ranked-list-of-trading-concepts-with-unsourced-percentages
url: https://www.instagram.com/reel/DcGsq7StTIs/
meta: {"vault_status": "intel", "kind": "idea", "subject": "@thearsalaanshaikh reel: ten trading concepts ranked, order flow first, MACD last", "date": "2026-10-08", "where": "TRITON-CORE/Research/links/2026-10-08-arsalaanshaikh-concepts-ranking-reel.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Nothing testable in it

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) An opinion ranking of ten trading concepts in the smart-money vocabulary, with unsourced percentages and a caption built to start arguments. No method, no rule, no record, nothing to test. The only content is a claim that moving-average bots are never profitable, against which the vault's S1 is a moving-average regime system with a passed out-of-sample protocol, modest as it is. Write-up: `TRITON-CORE/Research/links/2026-10-08-arsalaanshaikh-concepts-ranking-reel.md` Link: https://www.instagram.com/reel/DcGsq7StTIs/

## 7. [hn] Backdoors in official Claude Code extensions
key: hn:50302334
url: https://cyberplace.social/@GossiTheDog/117528831681803563
discussion: https://news.ycombinator.com/item?id=50302334
meta: {"points": 651, "comments": 17, "created": "2026-10-30T11:05:53Z"}
query: claude code

page: Kevin Beaumont: "Anthropic Visual Studio Claude Code extension on …" - Cyberplace To use the Mastodon web application, please enable JavaScript. Alternatively, try one of the native apps for Mastodon for your platform.
comment (altbdoor): Cursor has released a security notice: https://cursor.com/blog/claude-code-extension-security-notic... Edit: related https://news.ycombinator.com/item?id=50301983
comment (tomhow): Comments moved to https://news.ycombinator.com/item?id=50300683 .
comment (rhedak): These days no one is immune to these kind of attacks... Honestly it will only get worse from here.

## 8. [github] nirholas/pump-fun-sdk: Token creation launching, bonding curve trading, AMM migration, tiered fees, creator fee sharing, vanity keygen, MCP server, Telegram bot & live dashboards
key: gh:nirholas/pump-fun-sdk
url: https://github.com/nirholas/pump-fun-sdk
meta: {"stars": 141, "created": "2026-02-26", "pushed": "2026-10-29", "language": "TypeScript", "topics": ["agents-md", "ai-agents", "bundle", "crypto-bot", "cryptocurrency", "fun", "llms-txt", "meme"]}
query: solana pump.fun pushed:>{since} stars:>10

Pump SDK   
   
    TypeScript SDK for the Pump protocol on Solana — token creation, bonding curves, AMM pools, fee sharing, and volume rewards.
   
 

 
     
     
     
   
   
 

---

## What is Pump SDK?

Pump SDK is the community TypeScript SDK for the [Pump.fun](https://pump.fun) protocol on Solana. It provides **offline-first instruction builders** for every on-chain operation — token creation, bonding curve trading, AMM pool management, tiered fee configuration, creator fee sharing, volume-based token incentives, and social referral fees.

The SDK never sends transactions itself. It returns `TransactionInstruction[]` that you compose into transactions with your preferred signing and sending strategy.

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [The `pump` CLI](#-the-pump-cli)
- [50 Runnable Examples](#-50-runnable-examples)
- [Usage Examples](#-usage-examples)
  - [Create a Token](#create-a-token)
  - [Create a Token With a `...pump` Vanity Mint](#create-a-token-with-a-pump-vanity-mint)
  - [Buy Tokens on the Bonding Curve](#buy-tokens-on-the-bonding-curve)
  - [Sell Tokens](#sell-tokens)
  - [Check Graduation Progress](#check-graduation-progress)
  - [Set Up Fee Sharing](#set-up-fee-sharing)
- [API Reference](#-api-reference)
- [On-Chain Programs](#-on-chain-programs)
- [Configuration](#-configuration)
- [Error Handling](#-error-handling)
- [FAQ](#-faq)
- [Architecture](#-architecture)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---
## 🚀 Live Demos & Resources

- **[Token Launchpad](https://sdk.pumpk.it/live/launchpad)**: launch and trade real Pump tokens from your browser, built entirely on this SDK
- **[SDK Docs & Live Dashboards](https://sdk.pumpk.it)** (trades, launches, vanity: [sdk.pumpk.it/live](https://sdk.pumpk.it/live/))
- **[pump.fun UI Template](https://demo.pumpk.it)**
- **[DeFi Agents API](https://agents.pumpk.it)**
- **[PumpKit](https://github.com/nirholas/pumpkit)**
- **[PumpKit Site](https://pumpk.it)**
- **[Telegram PumpFun Github Claim Tracker Bot](https://t.me/pumpfunclaims)**
- **[Pump.fun GitHub Claims — dedicated repository](https://github.com/nirholas/pumpfun-github-claims)** · [Product and notification rules](docs/github-claims-product.md)

> A GitHub social-fee withdrawal is real on-chain activity, not automatic proof
> that a developer created or endorses a coin. Claim cards distinguish verified
> repository/creator-wallet relationships, identity mismatches, unverified
> links, and unresolved pooled withdrawals. See the notification rules above.
- **[Telegram PumpFun Graduation/Migration Tracker Bot](https://t.me/trackpumpfun)**
- **[Pumpfun Claim Tracker](https://t.me/pfclaimsbot)** (best bot — currently offline while building)

## 📈 Proof & Virality

**Proof the GitHub Claim Tracker bot is profitable to monitor**  
[→ View tweet](https://x.com/nichxbt/status/2033377591592444056)

**Went mega viral**  
[→ View tweet](https://x.com/RoundtableSpace/status/2027417189918064915)

> **just shipped a real-time PumpFun intelligence bot on Telegram**  
> 
> 17 commands. zero cost. fully on-chain.  
> 
> `/price` → instant token price & bonding curve  
> `/monitor` → live token launch feed  
> `/cto` → creator takeover alerts  
> `/watch` → wallet fee claim tracking  
> `/quote` → buy/sell estimates  
> `/graduated` → AMM graduation status  
> `/alerts` → customize your notifications  
> 
> all powered by the open-source **pump-fun-sdk**



## 9. [arxiv] InferD: A Honeypot Framework for AI Inference Infrastructure
key: arxiv:2610.39807
url: https://arxiv.org/abs/2610.39807
meta: {"published": "2026-10-29", "authors": ["Hicham Hammouchi", "Gabriele Lenzini"], "categories": ["cs.CR", "cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Large language model serving stacks, commercial inference APIs, vector databases, and agent orchestration gateways are now ex- posed on the public internet and indexed by commodity scanners within hours of deployment. The threat characteristics of this sur- face are only beginning to be measured, and the honeypot frame- works that could measure it were designed for conventional net- work services rather than for AI infrastructure. In fact, emulating an AI service is a distinct deception problem: the observable behavior of the service, including model inventories, token formats, tool-call protocols, and authorization flows, must be reproduced faithfully, while the underlying computation, model inference and tool ex- ecution, must never occur. We present InferD, a low-interaction honeypot framework organized around a single principle we call deception without inference: every request an adversary can observe is answered from static response pools, and nothing an adversary submits is ever executed. InferD decomposes the emulation into four deception planes, transport, service protocol, vulnerability surface, and agentic session, adds a provenance plane that links a planted credential to evidence of downstream model-mediated processing.

## 10. [youtube] Architecting Agent Memory: Principles, Patterns, and Best Practices — Richmond Alake, MongoDB
key: yt:W2HVdB4Jbjs
url: https://www.youtube.com/watch?v=W2HVdB4Jbjs
meta: {"channel": "AI Engineer", "rank": 4, "duration_min": 17}
query: agent memory architecture explained

# Architecting Agent Memory: Principles, Patterns, and Best Practices — Richmond Alake, MongoDB
# AI Engineer
# https://www.youtube.com/watch?v=W2HVdB4Jbjs

[00:01] [Music] [Music] In the next 10 to 15 minutes, here's uh I guess my promise to you. I'm going to give you some information that will be high level. There will be some practical component to it. But this information I'll give you within the next 6 months will be very relevant and
[00:34] it will put you in the best position to build the best AI applications to build the best agents that are believable, capable, and reliable. I know we we going to get there. You know what? Just for you. There we go. You're welcome. So, we're going to be talking about a memory. Um, we're going to be talking about the stateless applications that we're bu building today and how we can make them stateful. We're going to be talking about the prompt engineering
[01:06] that we're doing today and how we can reduce that by focusing on persistence. We're going to be turning the responses in our AI application and making our agents build relationship with our customers and all of it is going to be centered around memory. So I'm going to do a very quick evolution of what we've been seeing for the past two to three years. We started off with chat bots. LMN power chatbots. They were great. Chat GPT came out November 2022 and yeah exploded.
[01:42] Then we went into rag. We gave this chat bots more domain specific relevant knowledge and it gave us more personalized responses. Then we begin to scale the compute, the data we're giving to the LLMs and they gave us emerging capabilities, right? Reasoning uh tool use. Now we're in the world of AI agents and agentic systems and the big debate is what is an agent, right? What is an AI agent? I don't like to go into that debate because that's like asking what is consciousness um is a spectrum. the agenticity and
[02:18] that's a word now agenticity of uh of an agent is is a spectrum so they're different levels I came here and I saw Whimo and to me was pure sorcery we don't have that in the UK and they're different levels of um self-driving so you can look at the genetic spectrum in that respect we have a minimal agent whereas an LLM running the loop great then you have a level four is autonomous agent a bunch of agents that have access to tools you they can do whatever they want. They're
[02:50] not prompted in any way or a minimal way. But this is how I see things is a spectrum. So what is an AI agent? It's a computational entity with awareness of his environment through perception, cognitive abilities through an LLM and also can take action through tool use. But the most important bit is there is some form of memory short-term or long-term. Memory is important. It's important because we're trying to make our agents reflective, interactive, proactive, and reactive and autonomous. And every most
[03:24] of this, if not all, can be solved with memory. Um, I work at MongoDB and we're going to make we're going to connect the dots, don't worry. So, this is all nice and good. This is what what you look at if you um double click into one AI agent is. But the most important bit to me is I'll go slide. People are taking pictures. Sorry. All right, let's go. The most important bit is memory. And when we talk about memory, the easy way you can think about it is short-term, long-term, but there al other distinct forms, right? Um, conversational entity memory, knowledge,
[03:59
[transcript continues in field-notes/staging/W2HVdB4Jbjs.txt]

## 11. [vault] The free-pay-only-shipping closure-sale dropship pattern, and a Wyoming registered-agent address as a shell signal
key: vault:2026-10-08:the-free-pay-only-shipping-closure-sale-dropship-pattern-and
url: https://harrisonandjames.com/
meta: {"vault_status": "intel", "kind": "scheme", "subject": "harrisonandjames.com (free jewellery, pay shipping only)", "date": "2026-10-08", "where": "TRITON-CORE/Research/links/2026-10-08-harrisonandjames.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Launch, advertise, collect, lapse, relaunch

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) A closure-sale dropship front: everything free after 46 years, pay shipping only, on a domain registered January 2026, legal entity at a Wyoming registered-agent address used by anonymous shells, Trustpilot 1.3 from 289 reviews describing inflated shipping as the real price, plated costume pieces or no delivery, and silent support. Nothing to buy. Write-up: `TRITON-CORE/Research/links/2026-10-08-harrisonandjames.md` Link: https://harrisonandjames.com/

## 12. [hn] Claude Code VS Code extension with backdoor released on Cursor marketplace
key: hn:50301983
url: https://doublepulsar.com/anthropic-hacked-to-deliver-remote-access-trojan-to-claude-developer-laptops-worldwide-1148a92baae2
discussion: https://news.ycombinator.com/item?id=50301983
meta: {"points": 397, "comments": 1, "created": "2026-10-30T10:22:51Z"}
query: claude code

comment (tomhow): Comments moved to https://news.ycombinator.com/item?id=50300683 .

## 13. [github] tapoooooty/hypergrad: HIP-3 perp DEX on Hyperliquid for Solana memecoins graduating from pump.fun. GRAD index perp from $500K, own perps for coins that hold.
key: gh:tapoooooty/hypergrad
url: https://github.com/tapoooooty/hypergrad
meta: {"stars": 132, "created": "2026-10-29", "pushed": "2026-10-29", "language": "Python", "topics": ["defi", "hip-3", "hyperliquid", "market-maker", "memecoins", "oracle", "perpetuals", "pump-fun"]}
query: solana pump.fun pushed:>{since} stars:>10
SEEN: the vault already judged this vendor (vault verdict: pump.fun). Record the mechanism only if it is new; do not re-judge the vendor.

**HyperGrad** is a builder-deployed perpetuals DEX on [Hyperliquid](https://hyperliquid.xyz) for Solana memecoins that graduate from [pump.fun](https://pump.fun).

- A coin that holds a **$500K** market cap joins **`grad:GRAD`**, an index perp of graduates.
- A coin that holds **$500K** for a full day, with real liquidity behind it, also gets **its own perp**, such as `grad:MWIF` (2x).
- Past **$5M** it becomes a blue chip with leverage up to 3x.
- An oracle prices every market from three independent Solana sources every 3 seconds, with a standby oracle on a second server.
- A market maker keeps both sides of every book quoted.
- A manager scans, rebalances and retires markets on its own.
- A dashboard, Telegram alerts and a preflight `doctor` keep you informed.

 
   
    The dashboard, shown here with demo data. 
 

## Contents

- [Why HyperGrad](#why-hypergrad)
- [How it works](#how-it-works)
- [Quick start](#quick-start)
- [Preflight: doctor](#preflight-doctor)
- [Market maker](#market-maker)
- [Oracle sources and failover](#oracle-sources-and-failover)
- [Running on a server](#running-on-a-server)
- [Telegram alerts](#telegram-alerts)
- [Commands](#commands)
- [Configuration](#configuration)
- [What code cannot do](#what-code-cannot-do)
- [Project layout](#project-layout)
- [Risks and limits](#risks-and-limits)
- [Documentation](#documentation)
- [Links](#links)

## Why HyperGrad

[HIP-3](https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-3-builder-deployed-perpetuals) lets anyone who stakes 500,000 HYPE run their own perp DEX on Hyperliquid's matching engine. The deployer brings the markets and the oracle; Hyperliquid handles order books, margin and liquidations. trade.xyz used this to build stock and commodity perps, and on October 29, 2026 ICE, the owner of the NYSE, signed with it to bring those markets to the US.

Memecoins are the obvious gap. On Solana you can only buy them. HyperGrad lets traders short them and use leverage, and it starts with an index so that a single thin coin cannot be turned against the market.

## How it works

   

| Process | What it does |
|---|---|
| **Manager** | Every 10 minutes: pulls graduated coins from pump.fun and DexScreener, checks holders over Solana RPC, assigns tiers, rebalances GRAD daily, halts markets that fall below their tier, flags coins ready for their own perp, and watches the oracle. |
| **Oracle** | Every ~3 seconds: one price per source, median across sources, EMA for the mark, one `setOracle` for every live market. Freezes on bad data, halts a market that stays frozen. |
| **Market maker** | Post-only bid and ask ladders around the oracle price, skewed against its own position, widened when volatility rises, pulled when a market halts or the oracle freezes. |
| **Dashboard** | Read-only view of everything above, plus `/api/health` for the standby oracle. |

### From graduate to blue chip

   

A coin gets its own perp at the same **$500K** that brings it into the index, but only once it has held that cap for 24 hours, has at least **$100K** of pool liquidity and $500K of daily volume, and is two days old. Leverage on these young markets is capped at **2x**. Hyperliquid will not accept an open interest cap below **$1M**, so a small pool can still be pushed against perp traders; the hold time, the liquidity floor, low leverage and the oracle freeze are there to make that expensive. The full policy is in [docs/03_LISTING_POLICY.md](docs/0

## 14. [youtube] check your car depreciation value right now
key: yt:01fdd_Q7i2s
url: https://www.youtube.com/watch?v=01fdd_Q7i2s
meta: {"channel": "Data Skill Cells", "rank": 4, "duration_min": 0}
query: car depreciation data analysis

# check your car depreciation value right now
# Data Skill Cells
# https://www.youtube.com/watch?v=01fdd_Q7i2s

[00:00] Love is a mighty lion. Roaring loud >> [music] >> but only you make me like a lion. Roaring loud with my whole heart. >> [music] >> Roar. >> [music]
