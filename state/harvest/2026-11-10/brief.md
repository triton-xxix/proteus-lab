# Harvest brief, 2026-11-10

14 items shortlisted from 378 candidates (288 dropped as already seen, 8 carry a vault verdict on the vendor).

## 1. [vault] nightly check that every path in the memory map still exists
key: vault:2026-11-10:nightly-check-that-every-path-in-the-memory-map-still-exists
url: https://www.youtube.com/watch?v=Zs3faMCDYNs
meta: {"vault_status": "open", "kind": "service", "subject": "Automation Orbit AI OS (MAPS framework)", "date": "2026-11-10", "where": "TRITON-CORE/Research/links/2026-11-10-automation-orbit-ai-os-maps.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: not found in the vault yet

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Free MAPS guide is sound and mostly what we already run; take the interview prompt, two-hop test and a nightly path check; skip the paid dashboard Write-up: `TRITON-CORE/Research/links/2026-11-10-automation-orbit-ai-os-maps.md` Link: https://www.youtube.com/watch?v=Zs3faMCDYNs

## 2. [hn] A year after the 100% AI mandate nobody understands our code
key: hn:50433079
url: https://www.reddit.com/r/ClaudeCode/comments/1xq2n3t/a_year_after_the_100_ai_mandate_nobody/
discussion: https://news.ycombinator.com/item?id=50433079
meta: {"points": 148, "comments": 189, "created": "2026-11-09T22:19:12Z"}
query: claude code

https://redlib.catsarch.com/r/ClaudeCode/comments/1xq2n3t/a_...
comment (marginalia_nu): If models are getting exponentially cheaper and more powerful, going all in a year ago is kind of insane. There's ostensibly this reverse token value inflation where whatever you spend on AI today, you'll get much more for the same dollar tomorrow (assuming models get cheaper and better). There's really a weird sort of late mover's advantage to just holding off and saving your money unless you expect your profit to grow faster than AI becomes more powerful.
comment (proc0): Yeah this is what happens when you think code is the product. It's really the understanding and also the design of the software that is the "engine" of value, and the problem is that it's hard to justify spending money to build something that is intangible and might be visible in the future. When non-technical people call the shots, they will rarely bet on spending time and effort on designing things properly because they can't see the value and it's hard to communicate and convince others of its business value.
comment (voidfunc): Just do what management wants and take the bag of money. That's all everyone is doing up the chain anyways.

## 3. [github] gogoymh/auto-ontology-mcp: NVIDIA Auto Ontology's semantic layer and a personal knowledge base as an MCP server for Claude, ChatGPT and other MCP clients. No LLM API key needed.
key: gh:gogoymh/auto-ontology-mcp
url: https://github.com/gogoymh/auto-ontology-mcp
meta: {"stars": 303, "created": "2026-11-06", "pushed": "2026-11-10", "language": "Python", "topics": ["chatgpt", "claude", "mcp", "mcp-server", "model-context-protocol", "ontology", "semantic-layer", "text-to-sql"]}
query: mcp server created:>{since} stars:>30

Quick start  ·
   Demo  ·
   Knowledge base  ·
   Tools  ·
   How it works  ·
   Safety 
 

   

 

**Auto Ontology MCP** (`auto-ontology-mcp`) brings [NVIDIA Auto Ontology](https://github.com/NVIDIA/auto-ontology)'s semantic layer to any MCP client, for two jobs:

- **Ask your databases.** Point it at a database, and the model you already use (Claude Code, Codex, OpenClaw, Hermes Agent, Cursor, VS Code, or the Claude and ChatGPT apps) builds business Terms, reviews joins and answers questions with SQL that the server checks against the ontology and the data.
- **Keep a personal knowledge base.** Share receipts, statements, papers, book notes or screenshots with your assistant; it reads them and stores the facts as records, the ideas as linked concepts, the passages worth finding again in a full-text index, and where each came from. The full originals stay in your Obsidian vault. Later questions get exact numbers, searchable quotes and links back to the original.

> [!TIP]
> **Use it in place of an LLM Wiki.** In Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) pattern the model compiles your sources into markdown pages that you read in Obsidian. Auto Ontology MCP runs the same loop (ingest, query, lint, with an index and a log) on an ontology instead of loose pages: facts go into typed tables you can sum, filter and compare with SQL, ideas become concept pages with typed links, every record, page and link keeps its source and the quote behind it, and `export_wiki` writes it all out as an Obsidian vault with aliases, `[[links]]` and the graph view. [How the two map](#personal-knowledge-base)

Auto Ontology runs its own LLMs (NVIDIA NIM) behind a Next.js, FastAPI and Postgres stack. This project hands every language step (reading, extracting, naming, judging, writing SQL) to the model in your MCP client, so there is no model endpoint to host and no API key to configure. The server keeps the deterministic work: schema extraction, profiling, key inference, validation, storage and read-only execution, in local SQLite files.

## Why

Text-to-SQL fails quietly. The query runs, a number comes back, and nothing says it is wrong.

| ❌ A model reading a raw schema | ✅ The same model with auto-ontology-mcp |
| --- | --- |
| Guesses which of `billing_city_id` and `delivery_city_id` "the customer's state" means | Gets the join path from reviewed relationships, with the default role and the alternatives spelled out |
| Joins `customers.customer_id = orders.order_id` because the integers happen to overlap | `validate_sql` rejects the join and names the one the ontology knows |
| Filters `state_name = 'pennsylvania'` and reports zero revenue | Is told the stored value is `'Pennsylvania'` before running the query |
| Writes `discount_pct > 20` against a column that holds 0 to 0.3 | Is asked whether it meant `0.2` |
| Sums a product price after joining to order lines and inflates the total | Gets a fan-out warning for the one-to-many join |
| Sums a product's order lines and counts its tags in one SELECT, so each line is counted once per tag | Is told that order lines and tags meet only at the product, and to aggregate each in its own subquery |
| Links two tables because both point to the same parent (an order line and a product tag of the same product) | Hears from `find_join_path` and `check_answerable` that the path only meets at the product and does not say which row belongs to which |
| Answers "return on ad 

## 4. [arxiv] Mitigating Agentic Deception via Evaluation-Side Partially Observable Games
key: arxiv:2611.12835
url: https://arxiv.org/abs/2611.12835
meta: {"published": "2026-11-09", "authors": ["Hanxiao Li", "Shutong Liu", "Yongjia Ma", "Jiaming Ji"], "categories": ["cs.LG"]}
query: all:"language model" AND all:agent AND all:tool

As large language models become more capable agents, they can exhibit deceptive behaviors, cheating human for higher rewards while appearing helpful. We attribute this failure to evaluation-side partial observability, where models are evaluated mainly from final outcome, without checking the faithfulness of underlying reasoning, tool use, and environmental effects. Prior mitigations address this partial observability by predefined evaluator latent belief space or one-shot monitoring, which do not extend to free-form language space and vulnerable to stronger deceptions that evade simple monitoring. In this work, we formulate deception mitigation as an Evaluation-Side Partially Observable Extensive Form Game (e-PoG), a max-min framework in which an agent maximizes reward, a monitor minimizes the agent's payoff by exposing deception from the full interaction trajectory, and a fixed verifier validates the monitor's claims and converts them into penalties. We define the solution concept as a Subgame-Perfect Oversight Equilibrium (SPOE) between agent and monitor, and prove its existence in finite games. With a perfect verifier, every SPOE is faithful; with an imperfect verifier, the guarantee persists if verifier errors do not reverse the ranking of monitor actions. To achieve faithful SPOE, we derive a two-timescale policy gradient algorithm and enhance the pipeline empirically with NLI verification and deterministic checks. Experiments with Gemma3-4B-IT and Qwen3-4B/8B on Agentic Role-Playing, SearchQA, and WebShop show that e-PoG mitigates multiple emergent deception modes, outperforming the strongest baselines by 26.0% in deception mitigation and by up to 39.8% in task success. These gains persist under weak-to-strong supervision. Code is available at https://github.com/Toyoid/deceptive-agent.

## 5. [youtube] I Tested Local AI on My Mac Studio So You Don't Have To
key: yt:JLs10oOX6NY
url: https://www.youtube.com/watch?v=JLs10oOX6NY
meta: {"channel": "Kai", "rank": 1, "duration_min": 27}
query: local llm mac benchmark m5

# I Tested Local AI on My Mac Studio So You Don't Have To
# Kai
# https://www.youtube.com/watch?v=JLs10oOX6NY

[00:00] So I have a Mac Studio on my desk, which cost more than my first car. And a few weeks ago, I opened Claude Code and told it to go and research a few different modules while I grabbed the coffee, because the whole point of a setup like this is that the AI does the work and I come back to finished code. And when I came back five minutes later, nothing had happened. The cursor was still spinning and the terminal was still blinking. My local model, running on my own machine, which is the whole reason I went down the local AI rabbit hole in the first place, was doing basically nothing useful. So I'm standing there with my coffee going
[00:32] cold, wondering what on earth is going on. Now, when we look at what was actually happening, Claude Code had fanned out four sub agents to work in parallel, and all four of them sent a request to my local model at the same time. And my model was running on Ollama, which every YouTube video, Reddit thread, and blog post had told me was the best choice. It was answering those four requests one at a time in a queue, like it was the DMV. So sub agent one was working while sub agents two, three, and four sat there waiting and burning
[01:06] time. And that is when I went digging. And what I found genuinely surprised me, because it isn't what any of the popular comparisons will tell you. So what are all of those Ollama versus LM Studio videos actually measuring? The wrong thing. And I am going to show you exactly what I mean. So the question for this video is a specific one. If you are using an AI coding agent like Claude Code, Open Code, or anything else that fans out sub agents, which app should be running your local model on your Mac? And once we understand what is actually happening under the hood, the answer
[01:39] isn't even close. But we are going to get there the right way by looking at the evidence first, then walking through the mechanism, and then working out a real verdict for each kind of Mac. Now, most of us have watched at least one Ollama versus LM Studio comparison, and they usually follow the same format. Somebody opens both apps, types the same and sees which one answers faster. Sometimes it's a document summary and sometimes it's a coding task. And at the end, they show the tokens per second and one app wins by a little. And those tests are not wrong. They are just
[02:12] testing a world that most of us don't live in anymore. The best one I have seen comes from a creator called The Dark Factory, who ran a really careful four-way race with four apps, two models, three document sizes, and three runs of each combination. And he showed the middle run rather than the best one. And that is the right way to do it because cherry-picking your best run is how you end up with YouTubers flexing numbers that never show up in real life. And when we look at his results, they were pretty clear because Ollama read a long 16,000 token document on Qwen
[02:46] 3.827B at 1,442 tokens per second, while LM Studios MLX download read the same document at 1,372, which is about a 5% difference. On short prompts with the larger model, Ollama showed the first word in 1.3 seconds, the fastest of all four apps in the test. And on writing speed, Ollama was doing about 90 tokens a second while the other apps sat at around 42 to 48. So his verdict was that for most people, Ollama is the one to pick. Tha
[transcript continues in field-notes/staging/JLs10oOX6NY.txt]

## 6. [vault] Claude-interviews-the-owner prompt as the opener for client builds
key: vault:2026-11-10:claude-interviews-the-owner-prompt-as-the-opener-for-client-
url: https://www.youtube.com/watch?v=Zs3faMCDYNs
meta: {"vault_status": "open", "kind": "service", "subject": "Automation Orbit AI OS (MAPS framework)", "date": "2026-11-10", "where": "TRITON-CORE/Research/links/2026-11-10-automation-orbit-ai-os-maps.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: transfers to the AI-for-businesses guide

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Free MAPS guide is sound and mostly what we already run; take the interview prompt, two-hop test and a nightly path check; skip the paid dashboard Write-up: `TRITON-CORE/Research/links/2026-11-10-automation-orbit-ai-os-maps.md` Link: https://www.youtube.com/watch?v=Zs3faMCDYNs

## 7. [hn] Show HN: Get your coding agent off ~2019 JavaScript, onto modern web primitives
key: hn:50443812
url: https://github.com/GoogleChrome/modern-web-guidance
discussion: https://news.ycombinator.com/item?id=50443812
meta: {"points": 222, "comments": 61, "created": "2026-11-10T18:01:15Z"}
query: claude code

Browsers natively handle a lot of what used to take 50 lines of JS (or a dependency): `CSS.highlights` for text range highlighting without <span>s everywhere, `<dialog>` and showModal() give you backdrops and ideal focus management, `field-sizing` to auto-grow textareas as the user types.. (Something yesterday's ftrain post touched on [0]) Models know about some of these by name, but consistently won't default to using the platform-native solution and instead prefer the incumbent <div>+JS based pattern. We started an effort in Chrome to supplement coding agents with this key domain knowledge and we're shipping our 1.0 today, in collaboration with Firefox, MDN, and Edge. 200+ guides (~1.7MB) of curated, hand-crafted implementation best-practices from web experts, updated as the web evolves. (Open source, obv, so.. we'll welcome your bikeshedding ;) Readable versions here: [1] I've spent the last 9 months obsessing over how to ship this as an agent skill + (Agentic RAG) CLI without blowing up your context window. (Or cedeing activation mechanics to MCP dynamic tool search). The skill description is minmaxed for activating on relevant frontend tasks. The RAG work I'm pretty proud of… originally a 500mb native stack down to a ~7MB pure-JS package, ~10ms search on your CPU. We just introduced a deterministic 'legacy-scan' (trained on 30k github repos) to identify old 'n dusted patterns that your agent can modernize. (92% avg precision on held-out repos.) People make a lot of claim
comment (phyzix5761): "Best Practices" are pretty much dead in the AI era. Pretty soon no one is going to read any of the code AI produces and that's a scary thought.
comment (halflife): Finally. This is exactly what I need when I need it. The amount of pull requests I reviewed with a mess of codes that can be switched to 2 lines of modern features made me write such tools myself, only half assed since I have other things to do.
comment (cyanydeez): I treat all my code as some kind of stochastic machinery. So atleast one stage, I'd just tell an agent to go through and follow the guide. But I'd not inject all this fluff into the wheels of the machine because it'd just take the "average" of these practices which would be just as useless.

## 8. [github] Dodaios/ste80-humanizer: STE80 Humanizer: agent skill that removes AI tells and rewrites text 80% of the way to ASD-STE100 (Simplified Technical English), the method Andrej Karpathy shared.
key: gh:dodaios/ste80-humanizer
url: https://github.com/Dodaios/ste80-humanizer
meta: {"stars": 302, "created": "2026-11-09", "pushed": "2026-11-10", "language": "Python", "topics": ["agent-skills", "ai-writing", "asd-ste100", "claude-code", "claude-skills", "codex", "cursor", "humanize-ai-text"]}
query: claude-code created:>{since} stars:>20

# STE80 Humanizer

[](https://skills.sh/Dodaios/ste80-humanizer) [](https://github.com/Dodaios/ste80-humanizer/actions/workflows/validate.yml) [](LICENSE)

STE80 Humanizer makes AI-written text read like a careful person wrote it, without changing what it says. It combines two methods:

1. **The humanizer method.** Remove the 26 tells from Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), in the catalog of [blader/humanizer](https://github.com/blader/humanizer).
2. **Karpathy's STE80 method.** Rebuild the sentences "80% of the way to ASD-STE100", the controlled English of aircraft maintenance manuals.

**Before:**
> Great question! Kubernetes liveness probes are a powerful mechanism that enables the kubelet to determine whether a container is healthy — and it's not just a health check, it's your first line of defense. When a probe fails, the container will be automatically restarted by the kubelet, ensuring that your application remains available. However, it's important to note that misconfigured probes could potentially cause cascading restarts, so parameters like `initialDelaySeconds` and `failureThreshold` should be carefully tuned.
>
> Get this right, and your cluster heals itself.

**After:**
> A liveness probe tells the kubelet if a container is healthy. If the probe fails, the kubelet restarts the container. This keeps the application available.
>
> A bad probe can also cause many restarts. For example, a timeout that is too short makes healthy containers fail the probe. To prevent this, set `initialDelaySeconds` and `failureThreshold` to values that fit your application.

The goal is text that people read easily. Getting past AI detectors is not a goal.

## Why two passes

Most humanizers only remove phrases. The text loses "Great question!" and "seamless", but it keeps long sentences that carry three ideas, hide the actor and stack hedges. It still reads like AI. You can see it in the worked example in [SKILL.md](SKILL.md):

| Step | What is left |
|---|---|
| Original | Chatbot opener, dash, "not just X", "-ing" rider, "however", "could potentially", dramatic closer |
| After Pass 1 (tells) | "...the container will be automatically restarted by the kubelet, which keeps your application available. Misconfigured probes can cause cascading restarts, so parameters ... should be carefully tuned." Clean words, but heavy sentences. |
| After Pass 2 (STE80) | Short sentences, one idea each, active voice, the instruction apart from the description. |

## The method: what Karpathy said

On 2 October 2026, [Andrej Karpathy posted](https://x.com/karpathy/status/2105819303471976479) tips for one problem: as LLMs do more of the work, people spend more time reading and understanding what the models produce. His first tip:

> Ask your LLM to explain something in ASD-STE100, it's a controlled language specification originally developed for aerospace maintenance documentation. LLMs well-versed in this language and it comes with heavy constraints on clean writing style that I often find a lot more readable. Sometimes I've tried to soften it a bit e.g. ask for "80% of the way to ASD-STE100" because the spec is quite stringent.

The post then goes up a ladder: diagrams, then HTML pages, then explainer videos. His conclusion is that our work moves "up the abstractions into oversight and understanding". Clear output is the bottleneck, and writing is the first step.

[](assets/ste100-overview.png)

*The 

## 9. [arxiv] PARIS: A multi-agent LLM framework for end-to-end, PRISMA-guided systematic literature reviews with pre-synthesis corpus quality assessment
key: arxiv:2611.12222
url: https://arxiv.org/abs/2611.12222
meta: {"published": "2026-11-09", "authors": ["Christophe Cruz", "Hussam Ghanem", "Samir Jabbar", "Ait Kbir"], "categories": ["cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Systematic literature reviews (SRs) remain slow and labor-intensive, and most automation tools address single stages of the workflow. We present PARIS (PRISMA Agentic Research Intelligence System), an open-source framework in which a conductor agent running in Claude Code orchestrates 15 specialized large language model (LLM) agents, from scoping a research question to exporting a manuscript draft. Agents are specified declaratively, coordinate exclusively through persisted artifacts that the conductor validates before every transition, and delegate retrieval, bibliometric analysis and scoring to deterministic Python utilities. Three human checkpoints gate study inclusion, corpus adequacy and the synthesis outline. We also introduce QualityScore, a pre-synthesis index that aggregates normalized network, bibliometric, semantic and process sub-scores into a 0-100 grade. Two case studies illustrate both: AI chatbots and university students' learning (388 records, 100 included) and AI-assisted SR methods (131 records, 123 included, QualityScore 69.1 recomputed with a proxy network sub-score). They show end-to-end feasibility across domains and the diagnostic use of QualityScore: in the first run, corpus improvements chosen at the corpus-adequacy checkpoint raised the score from 74.6 to 81.9 and the number of pre-2023 studies from 1 to 19. Audits of both runs exposed failure modes: incomplete retrieval, counts that drifted between agents, unrecorded or delegated checkpoint decisions and a grade that depends on how citation data are handled. PARIS fully supports 8 of the 27 PRISMA 2020 items and partially supports 11. Output quality has so far been judged only by an internal reviewer agent; independent validation against human reviews is the next step.

## 10. [youtube] Is Qwen3.8-27B Still #1 for Local LLMs? (M5 Max Test)
key: yt:-TKu-PdHI_Y
url: https://www.youtube.com/watch?v=-TKu-PdHI_Y
meta: {"channel": "Execute Automation", "rank": 3, "duration_min": 9}
query: local llm mac benchmark m5

# Is Qwen3.8-27B Still #1 for Local LLMs? (M5 Max Test)
# Execute Automation
# https://www.youtube.com/watch?v=-TKu-PdHI_Y

[00:00] Hi guys, welcome back. In this video, we'll be talking about the launch of the brand new Qwen 3.8 27 billion parameter model. So, this Qwen 3.8 27 billion parameter model is a dense model, unlike an MoE or mixture of expert model. I've been using Qwen model for almost 3 years now, starting from Qwen 3.5 9 billion parameter model, Qwen 3.6 27 billion parameter model, and the 35 billion parameter MoE model. And right now, they have released this Qwen 3.8 27 billion
[00:34] parameter model, and this is going to be completely mind-blowing. Because we know that the Qwen models are the best model to run locally with the coding agents for performing the coding operation, and they outperform the GPT-OSS model or even the brand new Meta's Muse Glimmer model. So, this model is always the best model in the Qwen 3.6 category. But right now, they have released this model 3.8, and I'm quite excited to see what exactly this particular model actually is going to be doing for us. And I'm
[01:06] sure that this model is going to beat all the other models which can run locally within our own machine. And also, the Qwen 3.8's benchmark shows over here, it's also quite impressive. As you can see, they compared the 3.8 27B against its own preceder, which is the 3.6 27 billion parameter model over here. And they also have compared the Muse Glimmer as well. You can see how they have badly beaten up the Muse Glimmer over here. >> [snorts] >> For the agentic terminal coding, the Qwen 3.8 27B is like 73, whereas the Muse Glimmer is just 51. Whereas the
[01:41] agentic coding bench says that it is 61.7, whereas the Muse Glimmer is 51. Just totally destroyed. And you can see how they are quite amazing in the repo level code generation, agentic coding, and software engineering benchmark. These are all looking pretty amazing. And the Qwen 3.8 27 billion parameter model is released as is BF16 quantization at the moment. But, if you are using Unsloth over here, as you can see in their documentation, they have mentioned that the same model can be downloaded in the 2-bit quantization, 3-bit quantization,
[02:16] 4-bit, 5-bit, 6, 8, and 16-bit, something like this one. So, you can download the model that you can run in your hardware. It can be a Mac mini machine or a M5 Max machine like what I have got over here. So, you can choose whichever model suits for your machine to run. And the one that I'm going to be running is the 4-bit quantization model over here. And I have already downloaded that within my LM Studio over here, as you can see. And I want to see how performant this particular model is while I'm going to be working with the Pi Coding Agent. So, I have got my Pi
[02:50] Coding Agent up and running over here. And I have also configured the model with my uh with my Pi Coding Agent setup over here with the Qwen 3.8 27 billion parameter model. As I told you, this is a 4-bit quantization model that I have got over here. And I'm going to be running this and see how it is going to be uh working for me in this particular machine. So, for doing that, you can see that this is my uh activity monitor over here. The model is already loaded. And I'm going to go to the Pi Coding Agent. And I'm going to
[03:21] just start off the setting over here. And you can see that the model that I'm going to be running is the Qwen 3.8 27 billion parameter mod
[transcript continues in field-notes/staging/-TKu-PdHI_Y.txt]

## 11. [vault] Multi-tier referral scheme paying on recruits' trading revenue, spread through referral links
key: vault:2026-09-20:multi-tier-referral-scheme-paying-on-recruits-trading-revenu
url: https://invoapp.com/join/tradewzay
meta: {"vault_status": "intel", "kind": "service", "subject": "Invo (invoapp.com referral link)", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-jev-sideshift-invo-keza.md (section 4)", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Four tiers, uncapped, retroactive; whoever sends the link is paid, so promotion is optimised for recruitment

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Non-custodial crypto perpetual futures copy-trading on Hyperliquid, reached through a referral chain that pays the sender. Crypto derivatives have been banned for UK retail since January 2021. Avoid. Job: Copy a proven trader's positions without leverage, offshore venues or a recruitment chain (still open) Write-up: `TRITON-CORE/Research/links/2026-09-20-jev-sideshift-invo-keza.md (section 4)` Link: https://invoapp.com/join/tradewzay

## 12. [hn] Show HN: DBDelve – Open-Source DB Client Made with Rust and GPUI
key: hn:50427934
url: https://news.ycombinator.com/item?id=50427934
discussion: https://news.ycombinator.com/item?id=50427934
meta: {"points": 119, "comments": 47, "created": "2026-11-09T16:36:38Z"}
query: car data

Hi HN, I’m Shayan and a few months ago I started building a DB Client DBDelve with a focus on performance and just making something that feels good to use (in the spirit of Zed, Ghostty, and other tools that just feel pleasant to use). For my workflow I’ve always looked for performance, especially since some time ago I had a really outdated machine and any kind of bloat was really noticeable, I remember using DBeaver and it just crashing on me multiple times, I also had to use postGIS which just made it worse. I migrated all my essential dev tools to use the ones with performance in mind (Zed, Ghostty etc) but the only thing that was missing was DB Client. The main choices everyone has are DBeaver which is a memory hog and an overkill for most of the tasks imo. The other options like Datagrid, Beekeeper, TablePlus are either electron based so bloated and memory hogs or paid and closed-source. DBDelve 0.3.6 against DBeaver 25.3.1 on the same Postgres table, median of 5 runs each (2026-10-11, M1 Pro, 32 GB). Times are from the action to the rows rendered. DBDelve DBeaver Launch 1.1 s 5.2 s Idle memory 133 MB 606 MB 1,000-row query 0.21 s 1.96 s 1M rows, time 56 s 208 s 1M rows, memory [1] 4.9 GB 17 GB [1] The whole 1M-row, 100-column table pulled into memory on purpose, with the row limit off. Not a normal use case; DBeaver's heap limit had to be raised manually for the benchmark. Scrolling perf with 1 million rows loaded with 100 columns each: https://youtu.be/V2MOhJYFqIE It h
comment (written-beyond): What about beekeeper studio?
comment (edstarch): >it's a breeze to work with if you just get through them not updating the crate officially on crates.io but the community has found the solutions for it, you just have to dig deep for it what does this mean? the ui does look very nice
comment (dofm): Oh this is good news — I have been looking for a fuss-free cross-platform alternative to MySQL Workbench to recommend for a data product for some time. (Workbench is a pain but it was capable, off-the-shelf and was possible to document it once, more or less, for multiple platforms; I did not actually hate using it. But alas it is old now) I will surely test this out; good luck with it.

## 13. [github] Junhan2/ztd-charts: 36 animated, interactive React charts in pure SVG, with a CLI and an MCP server
key: gh:junhan2/ztd-charts
url: https://github.com/Junhan2/ztd-charts
meta: {"stars": 272, "created": "2026-11-05", "pushed": "2026-11-10", "language": "TypeScript", "topics": ["chart", "data-visualization"]}
query: mcp server created:>{since} stars:>30

ztd charts 

 
  Animated, accessible React charts that read like a report. 
  37 charts in pure SVG with no runtime dependencies, and a JSON spec your AI agent can write.
 

 
     
     
   
 

 
    Docs   ·
   Gallery  ·
   Example dashboards  ·
   Playground  ·
   한국어 
 

 
   
 

## Why ztd charts

- **Each card says one thing.** One item takes the accent color and the rest stay neutral, with a bold takeaway under the chart, so a reader sees the point before reading the axes.
- **Motion that explains.** Charts draw in as they scroll into view, move on from where they are when the data changes, and let you drag over a range to read its change, high and low.
- **Accessible by default.** Keyboard navigation, a screen reader description and data table for every chart, reduced motion, and every label at WCAG AA contrast.
- **Small, with nothing else to install.** React is the only peer dependency. A chart with the shared core is about 12 to 26 kB Brotli, and very large data switches to canvas on its own.
- **Ready for AI.** Every chart is also a JSON spec with a public JSON Schema, and a CLI, an MCP server and an agent skill validate it and render it to PNG, SVG or HTML.
- **English and Korean.** en-US by default. `locale="ko-KR"` switches number formats (1.2만, 3.4억) and chart text to Korean.

 
   
 

## Quick start

```bash
npm i ztd-charts
```

```tsx
import { ChartCard, PieChart } from "ztd-charts";

const sales = [
  { device: "Mobile", share: 72 },
  { device: "Desktop", share: 23 },
  { device: "Tablet", share: 5 },
];

export function SalesByDevice() {
  return (
     
       
     
  );
}
```

The same chart as a JSON spec, which is what the CLI, the MCP server and an AI agent work with:

```tsx
import { Chart } from "ztd-charts";

 ;
```

## 37 charts

   

| Group | Charts |
|---|---|
| Proportion | Pie · Donut · Waffle · Marimekko · Segmented bar |
| Hierarchy | Treemap · Sunburst |
| Flow | Funnel · Sankey · Chord |
| Comparison | Bar · Waterfall · Pareto · Radar · Slope · Dumbbell · Lollipop |
| Trend | Line (range band too) · Area · Streamgraph · Sparkline · Calendar heatmap · Bump · Candlestick · Skyline |
| Distribution | Box plot (violin too) · Beeswarm · Ridgeline · Histogram |
| Relationship | Heatmap · Bubble · Scatter · Parallel coordinates |
| Map | Tile grid map |
| KPI | Gauge · Bullet · Radial bar |

Each chart has a page with a live demo, its props and copyable code in the [gallery](https://charts.ztd.app/docs/). Why each one made the cut, and what was left out, is in the [chart catalog](docs/catalog.md).

## Use it with AI

```bash
# Add the MCP server to Claude Code (Cursor and Claude Desktop are in the guide)
claude mcp add ztd-charts -- npx -y ztd-charts-mcp

# Chart ideas and ready specs from your data, then a PNG
npx ztd-charts-cli suggest sales.csv --out-dir charts
npx ztd-charts-cli render donut.json --out donut.png --theme light --scale 2
```

The MCP server lists charts, returns a chart's schema and example, validates a spec with suggestions for wrong fields, renders it to PNG, SVG and React code, and suggests charts from CSV, rows or a URL. The [agent skill](skills/ztd-charts/SKILL.md) walks an agent from picking a chart to a checked preview, and [llms.txt](llms.txt) gives a model the whole library in one file.

## Packages

| Package | What it is |
|---|---|
| [`ztd-charts`](https://www.npmjs.com/package/ztd-charts) | The React charts, cards, grid, themes and data hooks, plus spec tools (`ztd-char

## 14. [youtube] What Is BONDING CURVE For Meme Coin In Axiom Trading (EXPLAINED) 2026
key: yt:69tdX8GdfQU
url: https://www.youtube.com/watch?v=69tdX8GdfQU
meta: {"channel": "InstantHowTo", "rank": 3, "duration_min": 2}
query: solana bonding curve explained

# What Is BONDING CURVE For Meme Coin In Axiom Trading (EXPLAINED) 2026
# InstantHowTo
# https://www.youtube.com/watch?v=69tdX8GdfQU

[00:00] In this video, I'm going to explain what a bonding curve is for memecoins on Axiom. So, by the way, in case you want to start trading meme coins and you don't have an account on Axiom yet, there's a link down below in the description as well as in the pinned comment. And if you sign up using my link, you'll get a 10% discount on all trading fees forever. So, make sure you check it out. Axiom is one of the best platforms for trading meme coins. It's packed with a lot of different premium features such as an amazing wallet and Twitter tracker, a P&L tracker, a reward system which gives you Salana back just
[00:33] for trading. You can also trade perpetuals. Use their turbo mode for faster fills. You can set your own presets and adjust your slippage priority and bribe fees. They have some great filters to filter true meme coins, etc. So again, link down below. Make sure you check it out. You will not regret it. Now in here if you wanted to know what a bonding curve is and if you've seen it inside axiom so for example let me go over here this is an example you can see over here there's like a bcurve percentage which is basically a bonding curve percentage and this is mentioned throughout basically
[01:05] different tabs inside the axiom exchange as well as some other exchanges too. However, in case you don't know what that is, a bonding curve is actually when it comes to meme coins, it's a mathematical function that determines the price of a token based on its supply. So, as more tokens are actually bought, the price increases and as the tokens are sold, the price decreases. Now, this mechanism creates a dynamic pricing system where early buyers get tokens at a lower price than later buyers. Now, this is what a bonding curve is. And in case you want to adjust
[01:38] it as a filter inside Axiom, as I showed you, go to pools up here. Click on any of these three filters and select if you want the filters for new pairs, final stretches or migrated. And then over here, as you can see inside new pairs and final stretch, you can adjust the B curve percentage, minimum, and the maximum for your current layout. So that's pretty much it. I hope this video helped you out. If it did, please subscribe to the channel and help me out as well.
