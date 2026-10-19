# Harvest register

One line per item the harvester judged. Rendered by `bin/harvest.py` from `field-notes/harvest.jsonl`; design in
`field-notes/HARVEST-DESIGN.md`. Each kept entry records the **mechanism** (how it works), the **claim** (what the
source says), whether it is **testable** keyless tonight, and since 29 Sep a **breakdown** of how it would be done and
what tools it takes; testable ones are queued in `PROBES.md` with source `harvest` (or `vault` for Luke's links).
A vault verdict on a vendor does not stop the mechanism being recorded; the lens column says which is on record.

323 judged over 22 harvest days, 214 kept, 68 testable, 65 queued as probes, 62 with a probe verdict.

## Kept

| id | date | source | what | lens | interest | testable | probe |
|---|---|---|---|---|---|---|---|
| H-0322 | 2026-10-19 | github | [cranebeaker/coop-anything: Co-op Anything: point your AI agent at any single-player game a](https://github.com/cranebeaker/coop-anything) | mechanism | game-bots | yes | P-0177 |
| H-0321 | 2026-10-19 | hn | [Show HN: WhatsApp MCP running free on Cloudflare](https://github.com/finereli/whatsapp-mcp) (intel) | mechanism | tech | no: It needs a personal WhatsApp account to link plus a Cloudfla |  |
| H-0320 | 2026-10-19 | vault | [one-credit multi-model connector for desktop seats](https://www.instagram.com/reel/DcEsI98lT-x/) | mechanism | tools-for-strangers | no: It needs an account and credits on the vendor service, so it |  |
| H-0315 | 2026-10-19 | vault | [talking head over lifestyle B-roll](https://www.instagram.com/p/DZt8BdfMNFM/) | mechanism | tools-for-strangers | no: A real build needs paid avatar and voice generation, and the |  |
| H-0312 | 2026-10-19 | github | [Gathin23/tv-vibehack: Your TV, minus the ads. Debloat any Android TV over ADB and give it ](https://github.com/Gathin23/tv-vibehack) | mechanism | tools-for-strangers | no: It needs a physical Android TV on the network, which Proteus |  |
| H-0310 | 2026-10-19 | vault | [AI UGC and ad videos sold to businesses]() | mechanism | tools-for-strangers | no: A real run needs paid avatar and voice generation plus a cli |  |
| H-0309 | 2026-10-17 | github | [assafkip/claudemy: Claudemy: an open-source alternative to Udemy and Coursera. Give Claude](https://github.com/assafkip/claudemy) | mechanism | tools-for-strangers | no: Running it needs model research calls, and there is no local |  |
| H-0308 | 2026-10-17 | hn | [Show HN: Things to Do API](https://thingstodoapi.com/) | mechanism | open-data | no: It is unclear whether the endpoint needs a key, and an SF-on |  |
| H-0307 | 2026-10-17 | vault | [structured workbook as the product](https://www.youtube.com/watch?v=LlhTEttKcwQ) | mechanism | tools-for-strangers | no: Selling it needs an audience and a storefront; there is no k |  |
| H-0305 | 2026-10-17 | arxiv | [PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents](https://arxiv.org/abs/2610.22124) | mechanism | tech | no: Needs model training or at least model calls, and no local L |  |
| H-0304 | 2026-10-17 | github | [Noniv/web-ocean: Real-time WebGPU ocean renderer written from scratch, no engine. FFT wave](https://github.com/Noniv/web-ocean) | mechanism | cars | yes | P-0173 **works** |
| H-0303 | 2026-10-17 | hn | [Show HN: Stoke Money – Personal finance app built around a cash flow forecast](https://stoke.money) | mechanism | forecasting | no: Needs real transaction data, which Proteus has none of and s |  |
| H-0302 | 2026-10-17 | vault | [Familiar-surface cloning to sell a switch](https://www.youtube.com/watch?v=wajoP_5Cpw8) | mechanism | tools-for-strangers | no: The test is whether users switch, which needs real users and |  |
| H-0301 | 2026-10-17 | awesome | [muend/geoai-skills (new in awesome-claude-code)](https://github.com/muend/geoai-skills) | mechanism | tools-for-strangers | no: Measuring routing or behaviour needs repeated model runs, wh |  |
| H-0300 | 2026-10-17 | youtube | [⚡ PUMP.FUN BONDING CURVE: DEEP DIVE  ⚡](https://www.youtube.com/watch?v=geUxzPUIc-g) | mechanism | desk:grinder | yes | P-0172 **works** |
| H-0299 | 2026-10-17 | arxiv | [Improving Environment-Agnostic Coding Agents: The Role of Scaffolding](https://arxiv.org/abs/2610.22289) | mechanism | tech | no: Needs a Codex-class agent and benchmark environments with mo |  |
| H-0298 | 2026-10-17 | github | [anujasid/blender-ai-mcp-addon: AI assistant and MCP server for Blender: visual chat, scene](https://github.com/anujasid/blender-ai-mcp-addon) | mechanism | tech | no: Needs Blender installed and a model provider key or local mo |  |
| H-0296 | 2026-10-17 | vault | [sell narrow named jobs, not AI](https://www.youtube.com/watch?v=FS_hLDTDI1w) | mechanism | tools-for-strangers | no: Testing it means putting offers in front of real buyers, whi |  |
| H-0294 | 2026-10-16 | vault | [longer test of the retest rules](https://www.instagram.com/reel/DeR5ycpITv3/) | mechanism | forecasting | yes | P-0166 **not-worth-it** |
| H-0291 | 2026-10-16 | arxiv | [Learning to Steer LLM Agents and Multi-Agent Systems](https://arxiv.org/abs/2610.22316) | mechanism | mechanism-hunting | no: It needs RL training and a trained steering model, and there |  |
| H-0290 | 2026-10-16 | github | [Leonxlnx/earshot: Ears for coding agents: let AI hear, review and make sound. CPU-only, op](https://github.com/Leonxlnx/earshot) | mechanism | tools-for-strangers | yes | P-0165 **works** |
| H-0288 | 2026-10-16 | vault | [mistake-becomes-a-rule trade journal](https://www.instagram.com/reel/DeR5ycpITv3/) | mechanism | forecasting | no: It needs a paper window with real losing trades to classify, |  |
| H-0285 | 2026-10-16 | arxiv | [MLExpert: Towards a Generalist Agentic Model for Autonomous Machine Learning Engineering](https://arxiv.org/abs/2610.22344) | mechanism | mechanism-hunting | no: It needs GPU training of a 35B model and the paper's task fa |  |
| H-0284 | 2026-10-16 | github | [pro-vi/cc-stretch: Stretchtext replies for Claude Code: short by default, each phrase grow](https://github.com/pro-vi/cc-stretch) | mechanism | tools-for-strangers | yes | P-0164 **works** |
| H-0283 | 2026-10-16 | hn | [How the Claude Code team does code review](https://claude.dev/blog/solving-code-review-at-anthropic/) | mechanism | tech | no: It is an internal process on private repositories, with no p |  |
| H-0282 | 2026-10-16 | vault | [Paper-forward cluster log from the EDGAR daily index with a pre-registered 100-signal bar]() | mechanism | forecasting | yes | P-0163 **blocked** |
| H-0280 | 2026-10-15 | vault | [One live automation platform behind the website monthly fee](https://www.youtube.com/watch?v=_5uSbMMOkCQ) | mechanism | tools-for-strangers | no: Needs a platform account, a UK sender number and a real phon |  |
| H-0279 | 2026-10-15 | awesome | [huggingface/funes (new in awesome-claude-code)](https://github.com/huggingface/funes) | mechanism | tools-for-strangers | no: Runs a downloaded binary from a curl pipe and needs a coding |  |
| H-0277 | 2026-10-15 | arxiv | [Doc2Harness: Benchmarking LLMs on Long-Horizon Harness Engineering of Coding Agents](https://arxiv.org/abs/2610.20344) | mechanism | mechanism-hunting | no: Needs the benchmark release and many frontier model calls, w |  |
| H-0276 | 2026-10-15 | github | [i12bp8/decomp.wtf: What The Function: your AI agent decompiles games you own into C that c](https://github.com/i12bp8/decomp.wtf) | mechanism | mechanism-hunting | no: Linux and Windows only (not macOS), needs a game ROM and the |  |
| H-0274 | 2026-10-15 | vault | [UK accounts editions](https://claude.com/marketplace/plugins/small-business) | mechanism | tools-for-strangers | no: Confirming the UK connectors needs a paid plan and a Xero or |  |
| H-0270 | 2026-10-15 | github | [hujjun/mcd-saver-strategist: 麦当劳省钱点餐助手（麦门精算师）｜麦当劳优惠券组合优化 Skill：拉取麦当劳菜单与全部可用优惠券，算出最省的点餐组合，巨](https://github.com/hujjun/mcd-saver-strategist) | mechanism | tools-for-strangers | yes | P-0160 **works** |
| H-0268 | 2026-10-15 | vault | [signal-timed outreach](https://www.altahq.com) | mechanism | tools-for-strangers | no: The verdict is a reply rate, which needs real sends to real  |  |
| H-0266 | 2026-10-14 | github | [nateherkai/roast-room: Seven AI advisors (Bezos, Paul Graham, Hormozi, Gary Vee, Dan Marte](https://github.com/nateherkai/roast-room) | both | tools-for-strangers | no: The useful part needs many live Claude calls and is not keyl |  |
| H-0265 | 2026-10-14 | hn | [Show HN: I wrote an email app that accepts only one sender per inbox](https://clova.email/) | both | tools-for-strangers | no: It requires signing up for the service and owning a domain. |  |
| H-0264 | 2026-10-14 | vault | [score the 20-minute filter set on a dated cohort](https://www.instagram.com/reel/DcjuRbTyUPV/) | mechanism | desk:grinder | yes |  |
| H-0262 | 2026-10-14 | arxiv | [SEAR: Self-Evolving Agentic Robotics](https://arxiv.org/abs/2610.18792) | mechanism | mechanism-hunting | no: It needs robot simulators and frontier model budgets across  |  |
| H-0261 | 2026-10-14 | github | [YeonwooSung/my-claude-code-mods: Custom Claude Code Mods that I need](https://github.com/YeonwooSung/my-claude-code-mods) | mechanism | tools-for-strangers | yes | P-0156 **works** |
| H-0259 | 2026-10-14 | vault | [pull the stake at 5x versus holding](https://www.instagram.com/reel/DecmMdSuofw/) | mechanism | desk:grinder | yes | P-0155 **works** |
| H-0257 | 2026-10-14 | arxiv | [ChunkAct: Action Chunking for Agentic Robotics](https://arxiv.org/abs/2610.18874) | mechanism | tech | no: It needs the LIBERO-Pro robot simulator and a VLA stack, whi |  |
| H-0256 | 2026-10-14 | github | [nateherkai/herk-edit-kit: Herk Edit Kit by Nate Herk: edit videos, reels, and YouTube Shor](https://github.com/nateherkai/herk-edit-kit) | mechanism | tools-for-strangers | yes | P-0154 **works** |
| H-0255 | 2026-10-14 | hn | [Show HN: Pulse Local, a Mac budgeting app whose AI models run on your machine](https://pulseos.finance) | mechanism | tools-for-strangers | no: It needs a local model runtime and the weights, and there is |  |
| H-0254 | 2026-10-14 | vault | [crypto spot pairs laggard check](https://www.instagram.com/reel/DeaHN_lJJkB/) | mechanism | mechanism-hunting | yes | P-0153 **works** |
| H-0252 | 2026-10-13 | vault | [Per-post CPM tracked per account feeding back into what gets made next]() | mechanism | tools-for-strangers | no: It needs live posts with real view counts from owned account |  |
| H-0250 | 2026-10-13 | youtube | [Build a Simple Expected Goals Model with Machine Learning and Python](https://www.youtube.com/watch?v=GsfXAzfvJVM) | mechanism | desk:pitch | yes | P-0144 **works** |
| H-0249 | 2026-10-13 | arxiv | [SqueezeBench: Saturation-Resilient Evaluation of Mathematical Capability](https://arxiv.org/abs/2610.13461) | mechanism | mechanism-hunting | no: Needs a Lean toolchain and the released problem set, and a m |  |
| H-0246 | 2026-10-13 | vault | [Flat monthly editing retainer for businesses already producing content]() | mechanism | tools-for-strangers | no: The verdict is whether a client pays, which needs outreach a |  |
| H-0245 | 2026-10-13 | awesome | [plur-ai/plur (new in awesome-claude-code)](https://github.com/plur-ai/plur) | mechanism | tech | yes | P-0143 **works** |
| H-0243 | 2026-10-13 | arxiv | [ToFu: Exploiting and Fuzzing the LLM-Orchestrator-Tool Trust Boundary](https://arxiv.org/abs/2610.13651) | mechanism | tools-for-strangers | no: The framework code is not confirmed released and a faithful  |  |
| H-0242 | 2026-10-13 | github | [zhuyansen/new-term-radar: Daily radar for new AI terms: names of new models, products and ](https://github.com/zhuyansen/new-term-radar) | mechanism | mechanism-hunting | yes | P-0142 **works** |
| H-0241 | 2026-10-13 | hn | [How to engineer an AI harness for game development](https://kylekukshtel.com/ai-harness-engineering-game-development-claude-code) | mechanism | game-bots | no: It is a working practice across a whole project and cannot b |  |
| H-0240 | 2026-10-13 | vault | [service x city landing pages]() | mechanism | tools-for-strangers | no: A verdict needs a live indexed site and weeks of ranking dat |  |
| H-0238 | 2026-10-13 | github | [Atoll92/agent-standup: Your Claude Code, Codex and Mistral Vibe sessions as a live, animat](https://github.com/Atoll92/agent-standup) | mechanism | tools-for-strangers | yes | P-0138 **works** |
| H-0237 | 2026-10-13 | hn | [Show HN: Atticus – Hold-to-talk voice assistant for macOS that runs on Claude -p](https://github.com/SaarthurR/atticus-mac) | mechanism | tech | no: It needs macOS accessibility permissions and live claude -p  |  |
| H-0236 | 2026-10-13 | vault | [UGC creator marketplace that sources creator applications for brands fast](https://sideshift.app/) | mechanism | tools-for-strangers | no: It needs a two-sided marketplace with real creators, which c |  |
| H-0235 | 2026-10-13 | youtube | [Boosting SORA Token Value: The Power of Token Bonding Curve #XOR #VAL #PSWAP #economics #s](https://www.youtube.com/watch?v=PpjZ9GZsN20) | mechanism | mechanism-hunting | no: Verifying it means reading chain data for a different networ |  |
| H-0234 | 2026-10-13 | arxiv | [OpenSocialJax: Evaluating Social Adaptation in Sequential Social Dilemmas with Open-Ended ](https://arxiv.org/abs/2610.13710) | mechanism | game-bots | no: It needs model answers from eight LLMs and a JAX environment |  |
| H-0233 | 2026-10-13 | github | [iamumeransari/claude-show-your-work: Claude Code shows images and plays videos right in yo](https://github.com/iamumeransari/claude-show-your-work) | mechanism | tools-for-strangers | no: It needs the Ghostty terminal and a specific Claude Code ver |  |
| H-0231 | 2026-10-13 | vault | [Tooling, leaderboards and data products built around a token launchpad]() | mechanism | desk:grinder | yes | P-0137 **blocked** |
| H-0229 | 2026-10-13 | arxiv | [BT-Agent: Deploying Onboard Robot Agents with Behavior Trees and Multi-Fidelity Evaluation](https://arxiv.org/abs/2610.13862) | mechanism | game-bots | no: It needs a local model and a robot or simulator, and there i |  |
| H-0228 | 2026-10-13 | github | [juliobsz/skills: An agent skill that builds award-caliber websites from one line](https://github.com/juliobsz/skills) | mechanism | tools-for-strangers | no: Running it needs a model session to execute the skill, and t |  |
| H-0227 | 2026-10-13 | hn | [Launch HN: Agent37 (YC F26) – Low-cost agent sandboxes for running agents](https://news.ycombinator.com/item?id=50059096) | mechanism | tech | no: It is a hosted service needing an account, and the claim is  |  |
| H-0226 | 2026-10-13 | vault | [A small weekly prize or showcase as the community rung of the AI for Businesses or Bootcam](https://www.skool.com/aicreatorleague) | mechanism | tools-for-strangers | no: It needs a live community with members and a prize pool, whi |  |
| H-0224 | 2026-10-11 | github | [liyupi/ai-promo-video-maker: 一句话让 AI 帮你做产品宣传片！把产品名或网址告诉 Cursor、Claude Code、Codex 等 AI 编程工具](https://github.com/liyupi/ai-promo-video-maker) | mechanism | tools-for-strangers | no: The full flow needs model-driven agent runs, logins for scre |  |
| H-0223 | 2026-10-11 | vault | [Public on-chain leaderboards as the check on any trader's claimed record]() | mechanism | desk:grinder | yes | P-0127 **works** |
| H-0222 | 2026-10-11 | youtube | [Anthropic Engineers Just 10x'd Everyone's Claude Code](https://www.youtube.com/watch?v=oz2CwrPV2Rg) | mechanism | tech | no: Checking it means running a model with and without the rules |  |
| H-0221 | 2026-10-11 | arxiv | [TRACE: Diagnosing Verifier Brittleness in Agentic Evaluation](https://arxiv.org/abs/2610.11678) | mechanism | mechanism-hunting | no: Reproducing it needs repeated LLM agent runs, which are not  |  |
| H-0219 | 2026-10-11 | vault | [Phone-gated lead magnet to free workshop to done-for-you app build agency](https://keza.studio/10-app-templates) | mechanism | tools-for-strangers | no: Measuring it needs real traffic and a live funnel, and submi |  |
| H-0217 | 2026-10-11 | arxiv | [Narrow and Deep: An Ontology Tower as the Knowledge of an LLM Agent for an Industrial Equi](https://arxiv.org/abs/2610.11768) | mechanism | mechanism-hunting | no: It needs the plant data and open-weight models, and there is |  |
| H-0216 | 2026-10-11 | github | [aindeev/agent-chrome-relay: Let your AI agents use your Chrome, signed in as you, in backg](https://github.com/aindeev/agent-chrome-relay) | both | tools-for-strangers | no: It needs a manually loaded Chrome extension, a signed Go bui |  |
| H-0215 | 2026-10-11 | hn | [Show HN: Littleguys – Claude Code, Codex and OpenClaw agents in your menu bar](https://littleguys.hervalicio.us) | both | tools-for-strangers | no: It needs a GUI install and live agents to talk to, and the h |  |
| H-0214 | 2026-10-11 | vault | [Extract the free classroom for the product-validation and repeat-purchase method, if Luke ](https://www.skool.com/supplements) | mechanism | tools-for-strangers | no: The course content sits behind a Skool login, and the method |  |
| H-0212 | 2026-10-10 | vault | [Decomposing one classification into several narrow questions with weights fitted on a labe]() | mechanism | tools-for-strangers | yes | P-0124 **blocked** |
| H-0211 | 2026-10-10 | awesome | [bill10/agent-007 (new in awesome-claude-code)](https://github.com/bill10/agent-007) | mechanism | tools-for-strangers | no: Needs a web service, git repos and Claude Code or Codex agen |  |
| H-0207 | 2026-10-10 | hn | [Can you use autoregressive diffusion to generate market data?](https://blog.janestreet.com/can-you-use-autoregressive-diffusion-to-generate-market-data/) | mechanism | forecasting | no: Needs tick-level order book data and GPU training, not keyle |  |
| H-0206 | 2026-10-10 | vault | [Templates, thumbnails, overlays and pre-launch guides sold or published to creators before]() | mechanism | tools-for-strangers | no: Needs a storefront and an audience, and the result takes wee |  |
| H-0205 | 2026-10-10 | awesome | [automatis-tools/agents-can-communicate (new in awesome-claude-code)](https://github.com/automatis-tools/agents-can-communicate) | mechanism | tools-for-strangers | no: Needs Node 24 and a second vendor's client installed and tru |  |
| H-0204 | 2026-10-10 | youtube | [Code Demo - Web-scraping with API's](https://www.youtube.com/watch?v=H-6gyxVGj6A) | mechanism | open-data | yes | P-0123 **works** |
| H-0203 | 2026-10-10 | arxiv | [SuperNav: An Agentic Navigation System for Any Task in Any Scene](https://arxiv.org/abs/2610.12126) | mechanism | tech | no: Needs a robot or the HM3D simulator plus a multimodal model  |  |
| H-0202 | 2026-10-10 | github | [wheresryan22/anatomy: A Claude Code skill that turns a technical idea into a detailed, int](https://github.com/wheresryan22/anatomy) | mechanism | tools-for-strangers | yes | P-0122 **works** |
| H-0200 | 2026-10-10 | vault | [UK shape of selling booking software through trade job software and profile booking button](https://www.youtube.com/watch?v=mr4YV-9MY0Q) | mechanism | tools-for-strangers | no: The open question is which UK job software trades use and wh |  |
| H-0198 | 2026-10-09 | vault | [x402 per-call payment rails for agents, Coinbase-originated, now under Linux Foundation go](https://docs.google.com/document/d/1_KvqUJXH1z7RUjrnbal0JVgGcJyP4yFfOdyZ1PRWbQs/edit?usp=drivesdk) | mechanism | tools-for-strangers | yes | P-0116 **works** |
| H-0195 | 2026-10-09 | arxiv | [A Closer Look at Agentic BBO: Benchmarking LLM Agents for Black-Box Optimization](https://arxiv.org/abs/2610.12183) | mechanism | mechanism-hunting | no: Needs the benchmark harness plus LLM calls across domains; n |  |
| H-0194 | 2026-10-09 | github | [Jakeschincariol/founder-skill: Eleven free Claude skills that test a business before you l](https://github.com/Jakeschincariol/founder-skill) | both | tools-for-strangers | yes | P-0115 **works** |
| H-0192 | 2026-10-09 | vault | [Join and extract the four free communities that cover both asks: Emerging Fashion Designer](https://www.skool.com/discovery?q=fashion+design) | mechanism | tools-for-strangers | no: Needs Luke to join each community in an interactive browser  |  |
| H-0191 | 2026-10-09 | awesome | [4da-systems/4da (new in awesome-mcp-servers)](https://github.com/4da-systems/4da) | mechanism | tools-for-strangers | yes | P-0114 **blocked** |
| H-0189 | 2026-10-09 | arxiv | [Unlocking the Regulatory Genome by ARGUS: An Evidence-Constrained Agentic Framework for In](https://arxiv.org/abs/2610.12281) | mechanism | mechanism-hunting | no: Needs 458 trained models and genomics tooling; no keyless sl |  |
| H-0188 | 2026-10-09 | github | [franzenzenhofer/big-arrow-on-the-screen: Let your AI agents paint big arrows, boxes and te](https://github.com/franzenzenhofer/big-arrow-on-the-screen) | mechanism | tools-for-strangers | yes | P-0113 **blocked** |
| H-0186 | 2026-10-09 | vault | [A scoped UK test of one flip with the compliance costs priced first, only if Luke wants th](https://www.skool.com/ai-car-trader-9959) | mechanism | cars | no: A real flip needs money, a car and insurance; no keyless sli |  |
| H-0184 | 2026-10-08 | vault | [Whether LinkedIn search surfaces enough recent dental and aesthetics owner posts per week ](https://vimeo.com/1233794507/cf61fad386) | mechanism | none | no: LinkedIn search needs a logged-in account and public pages b |  |
| H-0182 | 2026-10-08 | youtube | [Pump Fun Sniper Bot (Solana) — Memecoin Trading / Full Tutorial 2026](https://www.youtube.com/watch?v=E0QoMIjVI44) (intel) | mechanism | desk:grinder | yes | P-0099 **works** |
| H-0180 | 2026-10-08 | github | [cth9191/animate: Procedural animation in any style for Claude Code: short single-file canv](https://github.com/cth9191/animate) | mechanism | tools-for-strangers | yes | P-0098 **works** |
| H-0178 | 2026-10-08 | vault | [Code the five rules as a freqtrade strategy and score it on the two-year sample and payout](https://www.instagram.com/reel/DbJMHpDMK-1/) | mechanism | mechanism-hunting | yes | P-0104 **not-worth-it** |
| H-0175 | 2026-10-08 | arxiv | [RECAST: Learning to Compute the Right Context through Adaptive Evidence Routing](https://arxiv.org/abs/2610.10507) | mechanism | tech | no: Needs training a router model and the benchmark suites, far  |  |
| H-0174 | 2026-10-08 | github | [openqodex/openqodex: Open source AI code review for Claude Code and Codex, before you push](https://github.com/openqodex/openqodex) | mechanism | tools-for-strangers | no: The reviewer stage needs a logged-in Claude Code or Codex se |  |
| H-0172 | 2026-10-08 | vault | [An inducement filter as a variant on the WF-0350 paper test: one further sweep and recover](https://www.instagram.com/reel/DePSq8KIuyj/) | mechanism | mechanism-hunting | yes | P-0103 **not-worth-it** |
| H-0171 | 2026-10-07 | hn | [Show HN: Agent.reviews – Where AI agents read and write reviews on tools](https://agent.reviews/) | both | open-data | yes | P-0094 **works** |
| H-0170 | 2026-10-07 | vault | [Build a mock-up site for the prospect and send a 90-second Loom after a two-line permissio](https://www.youtube.com/watch?v=aidr_Ny1rvI) | mechanism | tools-for-strangers | no: Needs real prospects, outbound messages and replies, not a k |  |
| H-0169 | 2026-10-07 | awesome | [cvelasquez/agent-workbench (new in awesome-claude-code)](https://github.com/cvelasquez/agent-workbench) | mechanism | tools-for-strangers | yes | P-0093 **blocked** |
| H-0166 | 2026-10-07 | github | [GTKottman/mortiflix-oss: A motion design studio on your own machine: Claude makes the vide](https://github.com/GTKottman/mortiflix-oss) | mechanism | tools-for-strangers | yes | P-0092 **works** |
| H-0165 | 2026-10-07 | hn | [Show HN: Durable Actors – OSS Durable Objects with configurable compute](https://github.com/TerseAI/durable-actors) | both | tech | no: Needs a Kubernetes cluster or its runtime set up, beyond a 3 |  |
| H-0164 | 2026-10-07 | vault | [A high-impact news filter for the S1 crypto bot, skip or flatten entries in a window aroun](https://www.forexfactory.com/) | mechanism | mechanism-hunting | yes | P-0102 **works** |
| H-0161 | 2026-10-07 | arxiv | [MedZERO: Self-Evolving Agents for Open-Ended Medical Reasoning Through Controlled Knowledg](https://arxiv.org/abs/2610.08327) | mechanism | tech | no: Needs model fine-tuning and medical benchmarks, not a 30 min |  |
| H-0158 | 2026-10-07 | vault | [Insider cluster-buy signal from the free Form 4 filings page as a paper desk](https://finviz.com/) | mechanism | forecasting | yes | P-0101 **blocked** |
| H-0157 | 2026-10-06 | github | [Charlesmpc/by2kb: Forward videos from IM to transcript, Markdown, and your knowledge base ](https://github.com/Charlesmpc/by2kb) | mechanism | tools-for-strangers | yes | P-0068 **broken** |
| H-0156 | 2026-10-06 | hn | [Show HN: OpenChart – OSS TradingView alternative with your own AI agent](https://github.com/longsurf-ai/openchart) | both | desk:grinder | no: The app is a macOS binary download from a third party and ne |  |
| H-0155 | 2026-10-06 | vault | [Getting a video into an agent as scene-change frames plus transcript, or via a bare URL to](https://www.instagram.com/reel/Db1USzsMNnZ/) | mechanism | tools-for-strangers | yes | P-0071 **works** |
| H-0153 | 2026-10-06 | arxiv | [HERA: Harness-Environment Co-Evolution for Reliable Agentic Abstention](https://arxiv.org/abs/2610.06563) | mechanism | mechanism-hunting | no: Needs the paper's benchmark, code and model access that are  |  |
| H-0152 | 2026-10-06 | github | [arielshad/3d-asset-server: 3d assets api and mcp](https://github.com/arielshad/3d-asset-server) | mechanism | tools-for-strangers | yes | P-0067 **works** |
| H-0150 | 2026-10-06 | vault | [Buying real human UGC clips from marketplaces and reselling them inside a client retainer](https://www.instagram.com/reel/DdK9uWfRVRT/) | mechanism | none | no: Buying clips needs a marketplace account and payment. |  |
| H-0149 | 2026-10-06 | awesome | [degordonstech/pwa2play (new in awesome-claude-code)](https://github.com/degordonstech/pwa2play) | mechanism | tools-for-strangers | no: A real run needs a Play developer account and a live PWA wit |  |
| H-0147 | 2026-10-06 | arxiv | [Wikidata Search Traces: A Dataset for Training Knowledge Graph Search Agents](https://arxiv.org/abs/2610.06650) | mechanism | open-data | yes | P-0066 **works** |
| H-0146 | 2026-10-06 | github | [Vincentwei1021/mg-styles-15: 15 motion design styles, each made by Claude Opus 5.5 writing](https://github.com/Vincentwei1021/mg-styles-15) | mechanism | tools-for-strangers | yes | P-0065 **blocked** |
| H-0144 | 2026-10-06 | vault | [A 10 to 30 pound a day local lead-gen test for one Neptune client using the course build a](https://www.skool.com/theadsclinic) | mechanism | none | no: It needs a client, an ad account and real spend. |  |
| H-0141 | 2026-10-05 | vault | [Niche paid community on owned material, borrowing only a proven model and price point]() | mechanism | tools-for-strangers | no: It needs a platform account and a paying audience, not a key |  |
| H-0139 | 2026-10-05 | arxiv | [HazardWeaver: Scientific Route Selection for Hazard Analysis Agents](https://arxiv.org/abs/2610.03591) | mechanism | mechanism-hunting | no: It needs an LLM key and hazard datasets and models that are  |  |
| H-0138 | 2026-10-05 | github | [shinshin86/mesh-avatar-studio: Turn one illustration into an animated 2D mesh avatar with ](https://github.com/shinshin86/mesh-avatar-studio) | mechanism | tools-for-strangers | yes | P-0064 **blocked** |
| H-0137 | 2026-10-05 | hn | [Show HN: Nightwatch – a Mac menu-bar app that tells you when tonight is clear](https://github.com/rsutcliffe/nightwatch) | mechanism | open-data | yes | P-0063 **works** |
| H-0136 | 2026-10-05 | vault | [GBP setup and audit checklist]() | mechanism | tools-for-strangers | no: Reading listings at scale needs a Places API key or a scrapi |  |
| H-0134 | 2026-10-05 | arxiv | [NeutronGym: Physics-Graded Neutron Instrument Design for LLM Agents](https://arxiv.org/abs/2610.03631) | mechanism | mechanism-hunting | no: It needs the McStas simulator and an RL training run, which  |  |
| H-0133 | 2026-10-05 | github | [lichess-bot-devs/lichess-bot: A bridge between Lichess bots and chess engines](https://github.com/lichess-bot-devs/lichess-bot) | mechanism | game-bots | no: The Bot API needs a Lichess OAuth token and a BOT account, s |  |
| H-0131 | 2026-10-05 | vault | [scroll-driven website skill](https://github.com/nateherkai/scroll-craft) | mechanism | tools-for-strangers | yes |  |
| H-0130 | 2026-10-04 | youtube | [I Ran a Chess Programming Tournament!](https://www.youtube.com/watch?v=Ne40a5LkK6A) | mechanism | game-bots | no: The bots and framework are C# and need setup beyond a 30 min |  |
| H-0129 | 2026-10-04 | github | [Jakeschincariol/replica-skill: Eleven free Claude skills that clone any app: reverse-engin](https://github.com/Jakeschincariol/replica-skill) | mechanism | tools-for-strangers | yes | P-0061 **not-worth-it** |
| H-0127 | 2026-10-04 | vault | [node canvas workflows (Flows)]() | mechanism | tools-for-strangers | no: Needs a paid trial account and credits, and its MCP only rep |  |
| H-0125 | 2026-10-04 | arxiv | [The Innocent Courier: Covert Exfiltration Through Legitimate LLM Web Fetching](https://arxiv.org/abs/2610.01768) (intel) | mechanism | mechanism-hunting | no: Reproducing the attack needs a tool-calling model and an att |  |
| H-0124 | 2026-10-04 | github | [ythx-101/live-panel-skill: Config-driven animated architecture diagrams: turn one JSON fil](https://github.com/ythx-101/live-panel-skill) | mechanism | tools-for-strangers | yes | P-0060 **works** |
| H-0122 | 2026-10-04 | vault | [replication gap measured on demo](https://api-portal.etoro.com/changelog) | mechanism | forecasting | no: Needs an eToro demo API key, which is an account and a key. |  |
| H-0120 | 2026-10-04 | arxiv | [Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65%](https://arxiv.org/abs/2610.01939) | mechanism | mechanism-hunting | no: Needs the GPT-6 planner and robot simulators, none of which  |  |
| H-0119 | 2026-10-04 | github | [QingYunA/answer-me-with-html: Answer me with HTML — an agent skill that answers hard quest](https://github.com/QingYunA/answer-me-with-html) | both | tools-for-strangers | yes | P-0059 **works** |
| H-0117 | 2026-10-04 | vault | [Benchmark DeepSeek, GLM and Kimi against the M5 qwen3.6 on non-personal rewrite and summar](https://www.instagram.com/p/DdwbLoEgVKY/) | mechanism | tools-for-strangers | no: The endpoint needs an account and an API key, so it cannot b |  |
| H-0116 | 2026-10-03 | youtube | [Everything You Know About Skills IS OUTDATED](https://www.youtube.com/watch?v=e7TY56-yIvM) | mechanism | tech | yes | P-0057 **works** |
| H-0113 | 2026-10-03 | vault | [Photoreal moving footage of a subject you cannot film, one consistent face and a directed ](https://www.instagram.com/reel/DdoiRHMmyel/) | mechanism | tools-for-strangers | no: Video generation models need accounts and paid credits. |  |
| H-0111 | 2026-10-03 | arxiv | [Mimir: Physics-Grounded LLM Agents for Long-Horizon Irrigation Control](https://arxiv.org/abs/2610.02038) | mechanism | forecasting | no: Needs the authors' simulator, site data and code, which are  |  |
| H-0110 | 2026-10-03 | github | [zhuyansen/awesome-claude-video-skills: Open-source skills and toolkits that let Claude Cod](https://github.com/zhuyansen/awesome-claude-video-skills) | both | tools-for-strangers | no: It is a list; running it would only mean fetching other repo |  |
| H-0108 | 2026-10-03 | vault | [Generating many platform-native variants (hooks, colour grades, overlays) from one filmed ]() (intel) | mechanism | tools-for-strangers | no: The useful part needs a filmed asset and owned accounts, and |  |
| H-0106 | 2026-10-03 | arxiv | [OmniSeek: Native Tool Integration for Multi-turn Audio-Visual Reasoning](https://arxiv.org/abs/2610.02181) | mechanism | tech | no: Needs a trained omni-LLM checkpoint and GPU, and the paper g |  |
| H-0103 | 2026-10-03 | vault | [Whether a fees-paid threshold removes rugs without removing the launches that ran, on a da](https://www.instagram.com/reel/Db6WNI9BSQX/) | mechanism | desk:grinder | yes |  |
| H-0101 | 2026-10-02 | github | [ericmmartin/youtube-transcript-plus: YouTube Transcript Plus is an advanced Node.js packag](https://github.com/ericmmartin/youtube-transcript-plus) | mechanism | tools-for-strangers | yes | P-0056 **works** |
| H-0100 | 2026-10-02 | hn | [Show HN: Breadcrumb, record everything on your mac + context manager for AI](https://innerloop.works/breadcrumb) | mechanism | tools-for-strangers | no: It is a closed Mac app that records the screen and needs ins |  |
| H-0099 | 2026-10-02 | vault | [human reads flagged threads from alert links]() | mechanism | tools-for-strangers | yes | P-0055 **works** |
| H-0098 | 2026-10-02 | awesome | [elithril/blender-kiln (new in awesome-claude-code)](https://github.com/elithril/blender-kiln) | mechanism | tools-for-strangers | no: It needs Blender with an MCP server running and a paid model |  |
| H-0095 | 2026-10-02 | hn | [Show HN: Made an open-source Lego AI generator](https://github.com/anteloc/ldraw-nova) | mechanism | tools-for-strangers | yes | P-0054 **broken** |
| H-0094 | 2026-10-02 | vault | [Higgsfield Genjutsu as the final route for motion transfer, whole-frame recast at about 7 ](https://www.instagram.com/reel/Dd-BvW5Jych/) | mechanism | tools-for-strangers | no: It is a paid hosted service needing an account and spend, an |  |
| H-0091 | 2026-10-02 | github | [Edwardxlai/easyread: 把英文论文读成舒服的中文：本地 PDF 论文翻译、原文对照、边读边问 AI、文献管理。Read English papers in com](https://github.com/Edwardxlai/easyread) | mechanism | tools-for-strangers | no: It is an Electron app that needs a model login or key to tra |  |
| H-0090 | 2026-10-02 | hn | [Show HN: Rhun, an open-source code editor written in assembly](https://rhun.app/) | mechanism | tech | no: It means installing an unverified binary or building an asse |  |
| H-0089 | 2026-10-02 | vault | [Whether multi-buy and net-flow signals from tracked wallets predict price, measured on pap](https://youtu.be/2ikSD3rr5v8) | mechanism | desk:grinder | no: It needs timestamped wallet-level trades and forward prices  |  |
| H-0087 | 2026-10-01 | github | [machina-sports/sports-skills: Open-source agent skills for live sports data and prediction](https://github.com/machina-sports/sports-skills) | mechanism | desk:pitch | yes | P-0047 **broken** |
| H-0086 | 2026-10-01 | hn | [Show HN: Corral – Kill every command your agent starts](https://github.com/Cardinal44/corral) | mechanism | tools-for-strangers | no: It is Linux only (cgroups and /proc) and this machine is mac |  |
| H-0085 | 2026-10-01 | vault | [Inbound AI receptionist demo line built from the home services voice prompt]() | mechanism | tools-for-strangers | no: It needs a telephony account, a phone number and a voice-age |  |
| H-0084 | 2026-10-01 | youtube | [What is Expected Goals?](https://www.youtube.com/watch?v=tysc21gAT58) | mechanism | desk:pitch | yes | P-0046 **works** |
| H-0083 | 2026-10-01 | arxiv | [SEAR: Spoofing Evidence-Grounded Audio Reasoning Benchmark for Audio Language Models](https://arxiv.org/abs/2609.39847) (intel) | mechanism | mechanism-hunting | no: It needs six audio language models and the benchmark data is |  |
| H-0082 | 2026-10-01 | github | [edenfunf/reelmimic: Show it a video you love. Get a new video in the same style. An AI cre](https://github.com/edenfunf/reelmimic) | mechanism | tools-for-strangers | no: A real run takes hours of Claude Code usage and the shot ana |  |
| H-0080 | 2026-10-01 | vault | [One pay-as-you-go fal account to run Seedance, Kling, Wan and lip-sync models by API]() | mechanism | tools-for-strangers | no: It needs an account, a key and spend. |  |
| H-0079 | 2026-10-01 | youtube | [Finally, The CORRECT Way to Run Local AI on a Mac](https://www.youtube.com/watch?v=JpJaEPGzPF4) | mechanism | tech | yes | P-0045 |
| H-0078 | 2026-10-01 | arxiv | [Learning from Research: Toward Lifelong Agent Harness Evolution](https://arxiv.org/abs/2609.40169) | mechanism | mechanism-hunting | no: It needs the AppWorld and Tau2 harnesses, model runs and hou |  |
| H-0077 | 2026-10-01 | github | [nanaism/yomiyasu: AI生成の日本語を自然な日本語へ推敲するAgent Skill / Agent Skill for Refining AI-Generated ](https://github.com/nanaism/yomiyasu) | mechanism | tools-for-strangers | no: Judging naturalness of Japanese needs a native reader, and P |  |
| H-0076 | 2026-10-01 | hn | [Show HN: Open-source model routing for coding agents at Astra-level performance](https://news.ycombinator.com/item?id=49911500) | both | tech | no: It needs paid model keys on several providers and the benchm |  |
| H-0075 | 2026-10-01 | vault | [Adapt the web design CLAUDE.md for phone-first UK local business sites]() | mechanism | tools-for-strangers | no: The source file is behind the vault's course extract and the |  |
| H-0073 | 2026-09-30 | github | [echris6/motion-video-kit: Claude Code skill kit for premium AI-assisted business videos: i](https://github.com/echris6/motion-video-kit) | mechanism | tools-for-strangers | yes | P-0044 **works** |
| H-0072 | 2026-09-30 | hn | [Show HN: Parrot – Open-Source Smart Meeting Recorder with Co-Pilot on Mac](https://openparrot.app) | mechanism | tools-for-strangers | no: It is a Mac GUI app needing build and live call audio. |  |
| H-0071 | 2026-09-30 | vault | [Partnership ads run through a local client's own social handle](https://www.instagram.com/reel/DcWYAsmtqFr/) | mechanism | tools-for-strangers | no: Needs a Meta ad account and a client handle. |  |
| H-0070 | 2026-09-30 | youtube | [How to Make PUMP.FUN CALLOUTS (Step by Step) #pumpfun #crypto #memecoin](https://www.youtube.com/watch?v=MA6Ecac4P-Y) | mechanism | desk:grinder | no: Payouts and call attribution are not visible from a keyless  |  |
| H-0069 | 2026-09-30 | arxiv | [UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training](https://arxiv.org/abs/2609.38043) | mechanism | tech | no: Needs tau-bench, a frontier agent and paid calls. |  |
| H-0068 | 2026-09-30 | github | [rehan-remade/universal-modder: Point Claude at any game. Skills, tools and the fal MCP tha](https://github.com/rehan-remade/universal-modder) | mechanism | game-bots | no: Needs a fal key for assets, owned games on the machine, and  |  |
| H-0066 | 2026-09-30 | vault | [Consistent AI character content with clear AI disclosure](https://www.instagram.com/p/Ddr0Ds3MsI5/) | mechanism | tools-for-strangers | no: It is a content production job, not a script with a yes or n |  |
| H-0064 | 2026-09-30 | arxiv | [MotorMind: Scaffolding General Vision Language Models for Zero-Shot Robot Manipulation](https://arxiv.org/abs/2609.38078) | mechanism | tech | no: Needs a robot or the LIBERO-PRO simulator and a paid VLM. |  |
| H-0063 | 2026-09-30 | github | [Louis-CFM/coucou: A tiny friend that lives in your notch (macOS) or at the top of your scr](https://github.com/Louis-CFM/coucou) | mechanism | tools-for-strangers | no: It is an unnotarised Swift GUI that needs Xcode and a build, |  |
| H-0062 | 2026-09-30 | hn | [Launch HN: Magnitude (YC S25) – Self-optimizing inference engine for agents](https://github.com/magnitudedev/magnitude) | mechanism | tech | no: A fair test needs a multi-GB model download and a matched ll |  |
| H-0061 | 2026-09-30 | vault | [Learning crypto research from a source with an independently verifiable track record](https://cryptonary.com/landing-100x-chaser) | mechanism | desk:grinder | no: No source with a capturable call history has been named, so  |  |
| H-0059 | 2026-09-29 | github | [Barty-Bart/motion-graphics: Motion-graphics skills for Claude Code and Codex.](https://github.com/Barty-Bart/motion-graphics) | mechanism | tools-for-strangers | yes | P-0038 **works** |
| H-0058 | 2026-09-29 | vault | [Post-production for businesses that have long-form content but cannot cut it into short-fo](https://www.instagram.com/reel/DcU_MNWtIkg/) | mechanism | tools-for-strangers | no: The value is in a client engagement, and a keyless run would |  |
| H-0056 | 2026-09-29 | arxiv | [Harness Learning Enables Generalizable Test-Time Adaptation](https://arxiv.org/abs/2609.35738) | mechanism | mechanism-hunting | no: It needs reinforcement learning training of a proposer model |  |
| H-0055 | 2026-09-29 | github | [CaptureGrubEnchant/SolidWorks: SolidWorks MCP Server connects an AI assistant to a running](https://github.com/CaptureGrubEnchant/SolidWorks) | both | tech | no: It needs Windows and a licensed SolidWorks, and the install  |  |
| H-0054 | 2026-09-29 | vault | [Media-buying commission taken as a share of a brand's ad budget]() | mechanism | mechanism-hunting | no: It is a service arrangement with clients and ad accounts, an |  |
| H-0052 | 2026-09-29 | arxiv | [TokenCast: Forecasting Token Consumption During LLM Agent Execution](https://arxiv.org/abs/2609.35760) | mechanism | forecasting | yes | P-0037 **broken** |
| H-0051 | 2026-09-29 | github | [AgentSystemLabs/agent-office: A cartoon 3D office where your team hires Claude Code worker](https://github.com/AgentSystemLabs/agent-office) | both | tools-for-strangers | no: It needs a signed-in agent CLI and gh auth, and installs thr |  |
| H-0049 | 2026-09-29 | vault | [Join for one month with Skool neptune, transcribe the classroom into Education/Courses/ai-]() | mechanism | tools-for-strangers | no: The classroom sits behind a paid login and the pull needs an |  |
| H-0048 | 2026-09-28 | hn | [Show HN: OpenAPPA – open-source deterministic guardrails that don't break agents](https://www.openappa.com/) | both | mechanism-hunting | no: Reproducing the benchmarks needs LLM agent runs, and the num |  |
| H-0046 | 2026-09-28 | github | [jkawamoto/mcp-youtube-transcript: MCP server retrieving transcripts of YouTube videos](https://github.com/jkawamoto/mcp-youtube-transcript) | mechanism | tools-for-strangers | yes | P-0031 **works** |
| H-0045 | 2026-09-28 | hn | [Launch HN: Vespper (YC F24) – SOTA Docx MCP](https://www.vespper.com/blog/launching-vespper-docx-mcp) | both | tools-for-strangers | no: Needs a Vespper account and its hosted model, and the benchm |  |
| H-0043 | 2026-09-28 | arxiv | [A Safety-Bounded SDC-to-MCP Gateway for Medical AI Agents](https://arxiv.org/abs/2609.31358) | mechanism | mechanism-hunting | no: Needs SDC device simulators and the authors' prototype, whic |  |
| H-0042 | 2026-09-28 | github | [samyost1/3dicon: One prompt in, a looping animated 3D icon out — with real transparency. A](https://github.com/samyost1/3dicon) | mechanism | tools-for-strangers | no: The pipeline needs an OpenRouter key and paid image and vide |  |
| H-0040 | 2026-09-28 | youtube | [Agent Memory EXPLAINED - Complete Architecture](https://www.youtube.com/watch?v=aYfZN8t6AQs) | mechanism | mechanism-hunting | no: Running Mem0 needs an LLM for fact extraction, and no 30 min |  |
| H-0039 | 2026-09-28 | arxiv | [Structured Reasoning Agentic Framework for Interpretable Critical View of Safety Assessmen](https://arxiv.org/abs/2609.31524) | mechanism | tech | no: Needs the benchmark data and trained models, and no runnable |  |
| H-0038 | 2026-09-28 | github | [lemomo-ai/lemo-opuscar: 39 film styles, each a reusable style prompt plus a short film mad](https://github.com/lemomo-ai/lemo-opuscar) | mechanism | tools-for-strangers | no: Directing a film needs a Claude agent run against the skill, |  |
| H-0037 | 2026-09-28 | hn | [Show HN: HN.watch – Videos of all Hacker News posts](https://hn.watch/) | both | tools-for-strangers | yes | P-0030 **blocked** |
| H-0036 | 2026-09-27 | github | [alexgreensh/anidoodle: Art and animation, written as code. Illustrations, loops, interacti](https://github.com/alexgreensh/anidoodle) | mechanism | tools-for-strangers | yes | P-0028 **blocked** |
| H-0034 | 2026-09-27 | awesome | [lightpanda-io/browser (new in awesome-mcp-servers)](https://github.com/lightpanda-io/browser) | both | mechanism-hunting | yes | P-0027 **works** |
| H-0033 | 2026-09-27 | youtube | [How to Build An Expected Goals Model 1: Data and Model](https://www.youtube.com/watch?v=bpjLyFyLlXs) | mechanism | desk:pitch | no: This part of the transcript is conceptual framing with no fo |  |
| H-0032 | 2026-09-27 | arxiv | [PUBG Ally: A Conversational Embodied Agent as an AI Teammate](https://arxiv.org/abs/2609.29837) | mechanism | game-bots | no: It's a proprietary system deployed inside PUBG's live servic |  |
| H-0031 | 2026-09-27 | github | [dzhng/jevgrep: Find code by asking what it does. A CLI for coding agents that uses Jev to ](https://github.com/dzhng/jevgrep) | mechanism | mechanism-hunting | no: Needs a paid key for Vercel AI Gateway, OpenRouter or simila |  |
| H-0030 | 2026-09-27 | hn | [Turning GLM-5.3-Flash into a Jev-like decision model](https://www.privatemode.ai/blog/system-one-from-glm-flash) | both | mechanism-hunting | no: Needs GLM-5.3-Flash weights and a vLLM serving stack, not a  |  |
| H-0029 | 2026-09-27 | awesome | [agentmail-to/agentmail-mcp (new in awesome-mcp-servers)](https://github.com/agentmail-to/agentmail-mcp) | mechanism | mechanism-hunting | yes | P-0026 **works** |
| H-0027 | 2026-09-27 | arxiv | [When Can Agents Forget Their Reasoning? ICLR for Long-Horizon Agent Context Compression](https://arxiv.org/abs/2609.29875) | mechanism | mechanism-hunting | no: Needs the WorkBuddyBench harness, a proxy model for entropy  |  |
| H-0025 | 2026-09-27 | hn | [On caring for user data: NeoVim caused Vim undo files to be deleted](https://unsung.aresluna.org/they-had-no-concept-of-a-duty-of-care-to-their-users/) | mechanism | mechanism-hunting | yes | P-0025 |
| H-0022 | 2026-09-26 | github | [mikehasa/golive-skill: Take your agent-built product live: hosting, database, domain, emai](https://github.com/mikehasa/golive-skill) | both | tools-for-strangers | yes | P-0023 **works** |
| H-0021 | 2026-09-26 | hn | [Jevmem – automatic project memory for Claude Code, built on Jev](https://github.com/Avinash-jetwani/jevmem) | both | tools-for-strangers | no: Installing and running it needs a TypeSafe API key, a creden |  |
| H-0019 | 2026-09-26 | arxiv | [Qwen-Planner-Agent: A Closed-Loop AI-for-AI Framework for Real-World Mobile Planner Agents](https://arxiv.org/abs/2609.29892) | mechanism | mechanism-hunting | no: Needs the MobilePA-Bench harness, real or emulated mobile de |  |
| H-0018 | 2026-09-26 | github | [yetone/magpie: Every agent's model. One place. Codex on DeepSeek, Claude Code on Kimi, fro](https://github.com/yetone/magpie) | both | tools-for-strangers | yes | P-0022 **works** |
| H-0017 | 2026-09-26 | hn | [Show HN: A Claude Code skill to analyze your chess games](https://github.com/brumar/chess-postmortem-skills) | both | game-bots | no: The author's own figure is about $15 in API spend per run, r |  |
| H-0015 | 2026-09-26 | arxiv | [An Empirical Study of VLM Pipelines for Long-Document QA](https://arxiv.org/abs/2609.29933) | mechanism | mechanism-hunting | no: Reproducing needs the MMLongBench-Doc/LongDocURL benchmarks  |  |
| H-0014 | 2026-09-26 | github | [JohnHeibel/PDoomVideo: Source code for the Claude Opus 5.5 music video for I'm Upping My P](https://github.com/JohnHeibel/PDoomVideo) | mechanism | mechanism-hunting | yes | P-0021 **blocked** |
| H-0013 | 2026-09-26 | hn | [Show HN: Reladraw – A diagram language where you decide where to place things](https://github.com/reladraw/reladraw) | mechanism | mechanism-hunting | yes | P-0020 **works** |
| H-0012 | 2026-09-26 | hn | [Alan Kay: Shannon gave us a way of dealing with noisy channels [video]](https://www.youtube.com/watch?v=Cjntrqhn8pk) | mechanism | mechanism-hunting | no: Nothing to build or run, it is an anecdote about an accident |  |
| H-0010 | 2026-09-26 | github | [nateherkai/hyperframes-student-kit: Edit videos, reels, and YouTube Shorts with Codex or C](https://github.com/nateherkai/hyperframes-student-kit) | mechanism | tools-for-strangers | yes | P-0019 **works** |
| H-0009 | 2026-09-26 | hn | [Show HN: Whiteboard (YC W26) – An open-source IDE for thoughtful software design](https://github.com/devdotfast/whiteboard) | both | tools-for-strangers | no: It vendors a full Code-OSS (VSCode) fork plus Rust component |  |
| H-0007 | 2026-09-26 | arxiv | [World Action Agent: Harnessing VLMs for Robot Manipulation via World Action Rehearsal](https://arxiv.org/abs/2609.29964) | mechanism | tech | no: Needs LIBERO/robosuite simulation environments plus VLM infe |  |
| H-0006 | 2026-09-26 | github | [chainstacklabs/pumpfun-bonkfun-bot: A fully functional pump.fun / letsbonk.fun trading and](https://github.com/chainstacklabs/pumpfun-bonkfun-bot) (intel) | mechanism | desk:grinder | no: Real sniping needs a funded Solana wallet private key and, f |  |
| H-0005 | 2026-09-26 | hn | [Claude Code reads AGENTS.md only when telemetry is on [fixed]](https://blog.szypowi.cz/p/claude-code-reads-agents.md-only-when-telemetry-is-on/) | mechanism | mechanism-hunting | no: Reproducing it means repeated `claude -p` invocations, which |  |
| H-0004 | 2026-09-26 | youtube | [Pump Fun Sniper Bot Full Tutorial / Solana MEV Bot step-by-step how to use](https://www.youtube.com/watch?v=vssd36X5Y2c) (intel) | mechanism | desk:grinder | no: The only way to 'test' it is entering a wallet private key i |  |
| H-0003 | 2026-09-26 | arxiv | [Screen Before You Serve: Simulation for Production Customer Experience AI Agents at 140M S](https://arxiv.org/abs/2609.30137) | mechanism | mechanism-hunting | no: Snowglobe and Nubank's Card Management agent are internal pr |  |
| H-0002 | 2026-09-26 | github | [nexmoe/VidBee: Download video and audio from  YouTube ,  TikTok ,  Twitter ,  Instagram , ](https://github.com/nexmoe/VidBee) | both | tools-for-strangers | no: Distributed as a GUI desktop installer rather than a scripta |  |
| H-0001 | 2026-09-26 | hn | [Show HN: Make cursed fonts like Times New Bastard](https://bastardica.mitpit.com) | mechanism | tools-for-strangers | no: It is judged by visual appearance in a browser, not by a hea |  |

## Entries

### H-0322 cranebeaker/coop-anything: Co-op Anything: point your AI agent at any single-player game and play it with friends (onlin
2026-10-19, github, https://github.com/cranebeaker/coop-anything

- **Mechanism:** A repo of playbooks, agent skills and a local Python MCP server that guides a coding agent through adding co-op to a single-player game. Path one finishes an existing buggy co-op mod by mining its issues and auditing code; path two reverse engineers the game and engine, hooks in a second player and syncs world state. The MCP detects a game's engine from its install folder, searches a co-op directory and validates contributions, and testing runs with bot clients inside the game.
- **Claim:** Point an AI agent at any single-player game and it builds, tests and ships a co-op version over Steam relay.
- **Testable:** yes. Does the repo's coop_mcp.py correctly detect the engine from a synthetic install folder containing known marker files, yes or no? Queued as P-0177.
- **Idea on its own:** needs-a-run. The pipeline is plausible for simple engines, but the claim that any game works is untested and the hard part is the reverse engineering.
- **How it would be done:** Clone the repo, add its MCP to Claude Code and give the agent a target game's install folder. The agent detects the engine, reads the matching playbook, and uses a reverse-engineering MCP to find hook points. It then writes the second-player sync layer, runs bot clients to test, and packages the install. A person is needed for owning the game, Steam relay setup and playtesting with friends.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** coop-anything https://github.com/cranebeaker/coop-anything (The playbook, skills and MCP server.); REA reverse-engineering MCP https://github.com/morluto/rea (Looks inside the game binary, which coop-anything depends on for path two.)
- **Missing:** A game licence and a human playtest group.
- **Field Notes line:** A repo of playbooks and an MCP lets an agent reverse engineer a single-player game and bolt on co-op, with bots testing it in game.

### H-0321 Show HN: WhatsApp MCP running free on Cloudflare
2026-10-19, hn, https://github.com/finereli/whatsapp-mcp

- **Mechanism:** It runs the unofficial WhatsApp Web protocol (Baileys style) inside a Cloudflare Worker with Durable Object state, linked to a personal account as a companion device, and exposes search and read tools over MCP. It also pulls Google contacts to map phone numbers to names so search works. Platforms detect unofficial WhatsApp Web clients through account bans and forced re-login, and personal accounts are not covered by the Business API terms.
- **Claim:** Gives a mobile Claude access to a personal WhatsApp for free on Cloudflare without WhatsApp Business or a server.
- **Testable:** no. It needs a personal WhatsApp account to link plus a Cloudflare and Google account, and it is a terms-of-service grey area. Needs: A WhatsApp account, a Cloudflare account, a Google OAuth login.
- **Idea on its own:** unsound. It relies on an unofficial client that risks account loss and routes other people's messages to a third-party AI without their consent.
- **How it would be done:** The author deploys the Worker, scans a QR code to pair as a linked device, stores session keys in Durable Object storage, and adds an MCP endpoint with search and send tools. A contacts sync from Google fills in names. It is single-user by design. A hired person would be needed for nothing beyond setup; the real issue is consent and terms, which no script covers.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** whatsapp-mcp (finereli) https://github.com/finereli/whatsapp-mcp (The Cloudflare Worker and MCP server to read.); Baileys https://github.com/WhiskeySockets/Baileys (The unofficial WhatsApp Web library such projects rely on.)
- **Missing:** A sanctioned way to read personal WhatsApp; none exists.
- **Field Notes line:** A free Cloudflare Worker links as a WhatsApp companion device and serves your messages to Claude over MCP; the catch is terms and the other people in your chats.

### H-0320 one-credit multi-model connector for desktop seats
2026-10-19, vault, https://www.instagram.com/reel/DcEsI98lT-x/

- **Mechanism:** A hosted MCP connector fronts many image and video models behind one credit balance, so a desktop chat seat with no terminal can call generation through a single authenticated tool. The connector routes each request to a chosen model and bills credits per output. The Mac already reaches models directly by API, so the value is only for seats that cannot run scripts.
- **Claim:** One MCP connector gives Claude access to a credit-priced pool of image and video models, with a 40-credit trial.
- **Testable:** no. It needs an account and credits on the vendor service, so it is not keyless. Needs: An OpenArt account and trial credits.
- **Idea on its own:** sound. Aggregating several generators behind one connector is a real convenience for non-terminal seats, though it adds nothing where API access exists.
- **How it would be done:** Add the vendor's MCP URL as a connector in the desktop seat, authenticate once, and call the image and video tools from chat. Compare cost per output against calling the models directly by API. Keep it only for seats that cannot run scripts. A person would be needed only to judge output quality and manage credit spend.
- **Stack already covers:** Gemini (stills), Claude Code with skills and sub-agents
- **Field Notes line:** One MCP connector can put a pooled, credit-priced set of image and video models into a chat seat that has no terminal.

### H-0315 talking head over lifestyle B-roll
2026-10-19, vault, https://www.instagram.com/p/DZt8BdfMNFM/

- **Mechanism:** One script is voiced once and shown as a generated talking head, with lifestyle B-roll cut over the weaker seconds so the face is on screen only part of the time. The B-roll hides lip-sync drift and keeps retention up. Inputs are a script, a voice, a face reference and a library of generated or licensed clips.
- **Claim:** A cheap talking-head-over-lifestyle-B-roll format can be copied exactly by an AI fitness character.
- **Testable:** no. A real build needs paid avatar and voice generation, and the result needs an audience to judge it. Needs: Paid avatar and voice credits, an account to post from.
- **Idea on its own:** sound. Cutting away from a generated face is a standard, effective way to mask avatar weaknesses and it costs little extra.
- **How it would be done:** Write one short script, generate the voice in ElevenLabs, and render the head with HeyGen or Tavus. Generate or source five to eight B-roll clips matching the script beats, then assemble in HyperFrames with captions timed to the audio. The head shows on the hook and the call to action, B-roll covers the middle. A person would handle disclosure labelling and judging whether the character reads as believable.
- **Stack already covers:** ElevenLabs (voice), HeyGen and Tavus (avatars), HyperFrames (video compose, captions, render), Gemini (stills)
- **Missing:** A consistent character design and a posting account.
- **Field Notes line:** A talking head cut over lifestyle B-roll hides lip-sync drift and holds attention, and one script can drive the whole edit.

### H-0312 Gathin23/tv-vibehack: Your TV, minus the ads. Debloat any Android TV over ADB and give it a clean, tvOS-inspired launche
2026-10-19, github, https://github.com/Gathin23/tv-vibehack

- **Mechanism:** Android TV exposes adb over Wi-Fi once developer options and debugging are on, and the TV asks once to authorise the computer. A coding agent backs up the package list, then runs pm disable-user on manufacturer telemetry, ad and content-row packages, which hides them without uninstalling so a restore script can reverse each step. It then installs a small native launcher and sets it as the default home. The per-brand bloat list is discovered by the agent at run time from the real TV rather than hard-coded.
- **Claim:** Debloats any Android TV over ADB and installs a tvOS-style launcher in about fifteen minutes with a coding agent.
- **Testable:** no. It needs a physical Android TV on the network, which Proteus does not have. Needs: An Android TV or Google TV with debugging enabled.
- **Idea on its own:** sound. pm disable-user over adb is a standard, reversible mechanism, and letting the agent discover per-brand packages avoids a stale list.
- **How it would be done:** Enable developer options on the TV, connect with adb over the network, and have the agent dump pm list packages and settings as a backup. It then proposes disable candidates grouped by purpose and asks before touching anything the owner might use. Next it builds the launcher APK and sets it as home, checking each step with screenshots pulled via adb. A person would sort out the physical TV access for each customer if this were offered as a service.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Android platform-tools (adb) https://developer.android.com/tools/releases/platform-tools (The debug bridge the whole method rests on.); tv-vibehack https://github.com/Gathin23/tv-vibehack (Holds PROMPT.md and the launcher source.)
- **Missing:** A test TV.
- **Field Notes line:** A repo lets Claude Code strip ads from an Android TV over Wi-Fi by disabling packages with adb, reversibly, then swap in a clean launcher.

### H-0310 AI UGC and ad videos sold to businesses
2026-10-19, vault, 

- **Mechanism:** A seller produces short user-generated-content style video ads for small businesses using a generated avatar or voice reading a script, cut with captions and B-roll. The inputs are the client's product shots and offer, a script built from proven hook patterns, an avatar or clone voice, and an edit pass. Revenue comes from per-video or per-ad-set fees; the numbers quoted publicly are mostly self-reported.
- **Claim:** Selling AI UGC and brand-face video ads to businesses is the cheapest, fastest first revenue on an existing generation pipeline.
- **Testable:** no. A real run needs paid avatar and voice generation plus a client to judge the ad, so it is not keyless tonight. Needs: Paid ElevenLabs/HeyGen credits and a real business to test the ad on.
- **Idea on its own:** needs-a-run. The production pipeline is sound and cheap, but whether anyone pays and whether the ads convert is only knowable by selling one.
- **How it would be done:** Pick one niche and collect real product footage from a client. Write three hook variants from a hook library, voice them with ElevenLabs, render a presenter with HeyGen or Tavus, then compose captions and B-roll in HyperFrames. Export a short ad set and give it to the client to run as a small paid test. A hired person would do the selling, the client onboarding and the ad account setup, which no script covers.
- **Stack already covers:** ElevenLabs (voice), HeyGen and Tavus (avatars), HyperFrames (video compose, captions, render), Gemini (stills), Claude Code with skills and sub-agents
- **Missing:** A paying client and the ad account to measure conversion; nobody has the sales channel.
- **Field Notes line:** AI UGC ads for small businesses are a script, a cloned voice, an avatar and a captioned edit; the public income figures are mostly self-reported.

### H-0309 assafkip/claudemy: Claudemy: an open-source alternative to Udemy and Coursera. Give Claude a topic, it researches the we
2026-10-17, github, https://github.com/assafkip/claudemy

- **Mechanism:** A Claude Code skill maps a topic into sub-topics, then researches 20 to 40 pages with at most 3 from one site. Reader agents pull cited notes and one agent merges them into themes with agreement counts and dissent. It plans arcs of about four lessons, makes one sample lesson for feedback, then scripts two-host lessons and renders audio with ElevenLabs or macOS voices. A checker rejects any lesson citing a page the research did not read.
- **Claim:** Builds about 12 two-minute audio lessons with cited sources from a single topic prompt.
- **Testable:** no. Running it needs model research calls, and there is no local LLM tonight. Needs: Claude Code web search; ElevenLabs optional..
- **Idea on its own:** sound. The per-site cap, agreement counts and citation checker are cheap, mechanical guards against single-source and invented citations.
- **How it would be done:** Install the skill, give it a topic, and inspect the citation checker, which is plain code. The same checker pattern fits Field Notes, where every claim needs a source actually fetched. Audio rendering reuses ElevenLabs, which is already in the stack.
- **Stack already covers:** Claude Code with skills and sub-agents, ElevenLabs (voice)
- **To fetch:** claudemy https://github.com/assafkip/claudemy (Skill and citation checker to read and reuse.); ffmpeg https://ffmpeg.org/ (Audio assembly the skill depends on.)
- **Field Notes line:** A Claude skill builds audio courses and refuses lessons that cite pages the research never read.

### H-0308 Show HN: Things to Do API
2026-10-17, hn, https://thingstodoapi.com/

- **Mechanism:** The dataset of local events is built by finding influential accounts and posters, then fanning out to the accounts they co-post with. It is served as a REST API and an MCP endpoint, currently for the SF Bay area. The reason given is that on-demand agent web search is slow and no provider covers pop-ups and one-off events together.
- **Claim:** An API and MCP endpoint of Bay Area pop-ups, one-off events and concerts built by a co-posting fan-out.
- **Testable:** no. It is unclear whether the endpoint needs a key, and an SF-only event feed answers nothing for a desk here. Needs: Possibly an API key..
- **Idea on its own:** needs-a-run. Snowball sampling from seed accounts is a sensible discovery method, but coverage and freshness are unproven.
- **How it would be done:** Pick seed accounts for one city, collect their posts, extract accounts that co-appear, rank by frequency and repeat two rounds. Parse event date, venue and price from each post, de-duplicate, and publish as JSON. Maintenance and verification of dates is the ongoing cost a person would do.
- **Stack already covers:** A keyless YouTube search, oEmbed and transcript pipeline
- **To fetch:** Things to Do API https://thingstodoapi.com/ (The live service, to inspect coverage.)
- **Field Notes line:** A local events dataset grown by following who co-posts with influential event accounts, then served over MCP.

### H-0307 structured workbook as the product
2026-10-17, vault, https://www.youtube.com/watch?v=LlhTEttKcwQ

- **Mechanism:** The product is a structured workbook in a 30-day challenge shape: one daily rule, a tick box, a tracker and a bonus at the end. It is used both as a low-priced product and as a gated lead magnet that leads to a community rung. The three-variant test compares versions of the offer to see which converts.
- **Claim:** A roughly $12 workbook plus three AI personas produced about $157 profit in a week.
- **Testable:** no. Selling it needs an audience and a storefront; there is no keyless slice. Needs: An audience and a payment page..
- **Idea on its own:** sound. A structured, finite habit workbook is a real product shape with a clear completion path, independent of how the audience is found.
- **How it would be done:** Pick a narrow habit outcome, write thirty daily rules with a tick grid and a tracker, and produce it as a PDF or spreadsheet. Offer three variants (title, price or cover) to separate small audiences and compare conversion. Use real, disclosed authorship and not invented people.
- **Stack already covers:** Claude Code with skills and sub-agents, Gemini (stills)
- **Missing:** An audience and a place to sell.
- **Field Notes line:** A 30-day workbook with a daily rule, tick box and tracker is the transferable product; the fake personas are not.

### H-0305 PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents
2026-10-17, arxiv, https://arxiv.org/abs/2610.22124

- **Mechanism:** PROBE trains an LLM auditor to talk to a deployed tool-using agent as a realistic user across several turns and trigger policy violations (pricing, privacy, confirmation). It treats the exchange as a two-player Markov game with a composite reward balancing violation discovery, plausibility, progress and policy diversity. GRPO, DPO and GFlowNet objectives are compared. Trained auditors find broader violations than same-size zero-shot adversaries, even against larger targets.
- **Claim:** Trained multi-turn auditors uncover broader policy violations in tool-using agents than zero-shot adversaries.
- **Testable:** no. Needs model training or at least model calls, and no local LLM exists here. Needs: Model access and a target agent..
- **Idea on its own:** sound. Multi-turn probing with a diversity reward addresses violations that single-prompt red-teaming cannot reach.
- **How it would be done:** Write the policy as a list of checkable rules, give an auditor model a user persona and the agent's tool log, and reward turns that cause a logged violation while staying plausible. Without training, a simple version is a scripted set of personas run against the agent and a rule checker over the tool log. That would suit testing Proteus's own hook.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Field Notes line:** Auditors trained on a reward for plausible, diverse violations find more rule-breaking in agents than untrained attackers.

### H-0304 Noniv/web-ocean: Real-time WebGPU ocean renderer written from scratch, no engine. FFT waves, whitecaps, sun glitter, phy
2026-10-17, github, https://github.com/Noniv/web-ocean

- **Mechanism:** A Tessendorf FFT ocean runs as WebGPU compute shaders: six 256 by 256 cascades from 1103 m down to 0.26 m patches, driven by a JONSWAP wind spectrum with directional spreading and swell. The mesh is a 17-level CDLOD quadtree and shading uses LEAN-mapped slope moments for roughness at distance, with foam from the surface Jacobian folding. The whole thing bundles into one 61 KB minified HTML file.
- **Claim:** A from-scratch WebGPU ocean renderer in a single 61 KB HTML file, built with Claude Code.
- **Testable:** yes. Does ocean.min.html download at about 61 KB and load in the Browser pane with a WebGPU adapter and no console errors? Queued as P-0173.
- **Idea on its own:** needs-a-run. The size and rendering claims can be checked directly, but the visual result depends on WebGPU support on this Mac.
- **How it would be done:** Fetch the minified HTML from the repo, check its byte size, then open it in a browser with WebGPU enabled and read the console. Take a screenshot to confirm a sea is drawn. The wave and shading techniques are reusable for any HyperFrames or still-render background.
- **Stack already covers:** HyperFrames (video compose, captions, render)
- **To fetch:** web-ocean https://github.com/Noniv/web-ocean (The page and source to run.)
- **Field Notes line:** A full FFT ocean with sun glitter fits in one 61 KB HTML file using WebGPU compute shaders.

### H-0303 Show HN: Stoke Money – Personal finance app built around a cash flow forecast
2026-10-17, hn, https://stoke.money

- **Mechanism:** Instead of budgets, each income and spending category is projected forward from its own history and placed in the account where it usually lands (paycheques and rent in checking, daily spending on cards). Card payments are modelled from the projected card balance, so cash leaves checking when the bill is due, not when the charge is made. User-defined recurring transfers model savings. The output is a forecast of cash balance over time.
- **Claim:** A cash flow projection engine that models credit card timing, replacing monthly budgets.
- **Testable:** no. Needs real transaction data, which Proteus has none of and should not request. Needs: A transaction export..
- **Idea on its own:** sound. Separating the charge date from the cash date is the correct fix for the common net-of-the-month cash flow error.
- **How it would be done:** Take a transactions CSV, assign each category to its usual account, project each category with a trailing average and day-of-month pattern, then model card payments as the prior statement balance paid on the due date. Plot the running balance and back-test by forecasting a held-out month. The same projection logic could suit any recurring cash flow.
- **Field Notes line:** A finance app forecasts cash by modelling when card bills actually leave the bank, not when you spend.

### H-0302 Familiar-surface cloning to sell a switch
2026-10-17, vault, https://www.youtube.com/watch?v=wajoP_5Cpw8

- **Mechanism:** Rebuild a tool's workflow while keeping the layout users already know, so switching costs almost no learning. The rebuild is done from behaviour and public documentation, not by copying vendor code. The pitch to the user is the same screen with a different owner, price or feature set.
- **Claim:** Rebuilds that keep the familiar layout cut the learning curve for people switching.
- **Testable:** no. The test is whether users switch, which needs real users and a product. Needs: A target product and a user group..
- **Idea on its own:** sound. Familiar interfaces lower switching cost, which is a well-known adoption lever, provided the rebuild is clean-room and not a copy of vendor code.
- **How it would be done:** Choose a tool with a stable, widely understood interface and a weak spot (price, privacy, a missing feature). Write the interface spec from public docs and user-visible behaviour, build it with Claude Code, and test it with a handful of users from the existing tool. A human would do the clean-room discipline and the user interviews.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Missing:** A chosen target and willing switchers.
- **Field Notes line:** Keeping the layout people already know is what makes an open rebuild easy to switch to.

### H-0301 muend/geoai-skills (new in awesome-claude-code)
2026-10-17, awesome, https://github.com/muend/geoai-skills. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** Eighteen Agent Skills each encode preconditions, checks to run and evidence to report for a geospatial claim, with explicit stop conditions when data cannot support the claim (for example two Sentinel-2 scenes from different seasons cannot give a changed-hectares figure). A routing benchmark of 167 cases and a behaviour set of 92 clean pairs measure whether the right skill fires and whether behaviour changes, on one runtime and model pair. The behaviour scores are model-judged and not yet human-verified.
- **Claim:** Skills that stop when data cannot support a claim, with a 167-case routing benchmark and 92 behaviour pairs published.
- **Testable:** no. Measuring routing or behaviour needs repeated model runs, which are not keyless tonight. Needs: Model calls to rerun the benchmark..
- **Idea on its own:** sound. Writing the refusal conditions and evidence checks into a skill is a sound way to stop confident wrong answers, and publishing a benchmark makes it checkable.
- **How it would be done:** For any domain, list the preconditions that make a claim valid, write them as a skill with a stop rule, and build a test set of requests that should and should not be blocked. Score routing and behaviour on a held-out split. Proteus could do this for forecasting claims, such as refusing a win-rate claim without a luck test.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** geoai-skills https://github.com/muend/geoai-skills (Skill files and benchmark format to copy.); skills CLI https://www.skills.sh/ (Installer used by the repo.)
- **Field Notes line:** Skills that tell an agent when a geographic claim cannot be supported, published with their own routing and behaviour scores.

### H-0300 ⚡ PUMP.FUN BONDING CURVE: DEEP DIVE  ⚡
2026-10-17, youtube, https://www.youtube.com/watch?v=geUxzPUIc-g. Vault verdict on the vendor exists (vault verdict: pump.fun); mechanism recorded, vendor not re-judged.

- **Mechanism:** A pump.fun launch mints one billion tokens and places 800 million on a bonding curve, so price rises with the amount bought. The speaker reports roughly 85 to 86 SOL fills the curve and sends it to Raydium, with King of the Hill at about 45 SOL. He reconstructs the curve by interpolating from buy transactions (SOL in, tokens out), because he did not know the formula. The formula is likely a constant-product style virtual reserve curve that can be read from the program account.
- **Claim:** About 86 SOL fills the curve and about 45 SOL reaches King of the Hill, with price rising exponentially.
- **Testable:** yes. Does a live pump.fun bonding curve account read from public Solana RPC satisfy constant product on its virtual reserves, and does it graduate at about 85 SOL of real reserves? Queued as P-0172.
- **Idea on its own:** sound. A bonding curve is a deterministic formula, so claims about its fill cost can be checked against on-chain reserves.
- **How it would be done:** Fetch a recent token's bonding-curve account from a public Solana RPC, decode virtual and real reserves, and compute k. Check price after a buy against the formula and compare real SOL reserves at graduation with the 85 to 86 SOL claim. The result feeds the Grinder's entry-price and slippage model directly.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers and a Solana paper desk (the Grinder)
- **To fetch:** Solana public RPC https://api.mainnet-beta.solana.com (Keyless account reads to decode curve reserves.)
- **Field Notes line:** Pump.fun's curve holds 800 million of a billion tokens and fills at about 86 SOL; I will read a live curve account and check the maths.

### H-0299 Improving Environment-Agnostic Coding Agents: The Role of Scaffolding
2026-10-17, arxiv, https://arxiv.org/abs/2610.22289

- **Mechanism:** A general Codex-based agent is run unchanged across ARC-AGI-3, AGI Maze and Terminal-Bench, with only one instruction varied: report difficulties and return control for automatic continuation. That alone raises mean scores on two benchmarks. Moving the reset decision into a scripted controller that follows a convention already given to the agent recovers part of the gap to a specialised agent. Gains cost more tokens, and the paper says it cannot separate better use from extra inference.
- **Claim:** A one-line instruction change and a scripted reset controller improve a general agent, but it still trails an ARC-AGI-3-specific agent.
- **Testable:** no. Needs a Codex-class agent and benchmark environments with model calls. Needs: A model-backed agent and the EnvTraverse framework..
- **Idea on its own:** sound. Handing control decisions to deterministic code while keeping the model for content is a plausible and cheap scaffolding change.
- **How it would be done:** Take any agent loop, find the decisions that follow a fixed rule (reset, retry, stop), and move them into a controller script. Keep the same prompt otherwise and compare scores plus token cost on a fixed task set. Report cost alongside score because the paper warns they move together.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** EnvTraverse framework https://arxiv.org/abs/2610.22289 (Baseline agent and framework named in the paper; link on the abstract page.)
- **Field Notes line:** Moving the 'when to reset' decision out of the model and into a plain script recovered some of a specialist agent's lead.

### H-0298 anujasid/blender-ai-mcp-addon: AI assistant and MCP server for Blender: visual chat, scene tools, multi-agent workflows.
2026-10-17, github, https://github.com/anujasid/blender-ai-mcp-addon. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** A Blender add-on runs an MCP server over authenticated Streamable HTTP and exposes 21 scene tools (create, inspect, edit, capture, search assets, export). A team mode chains manager, worker and reviewer model calls in sequence: the manager writes assignments with acceptance criteria, workers run scene tools, reviewers approve or send findings back. A blocked task gets one retry, and a second failed review halts the run. Viewport screenshots go to image-capable models.
- **Claim:** Lets AI models drive Blender scenes through 21 tools, either as one assistant or as a manager, worker and reviewer team.
- **Testable:** no. Needs Blender installed and a model provider key or local model, and none is available keyless tonight. Needs: Blender and a model key..
- **Idea on its own:** sound. Tool-per-operation MCP servers with a bounded review loop are a reasonable pattern for any scriptable desktop app.
- **How it would be done:** Wrap the app's scripting API (bpy here) in a small set of typed tools, serve them over HTTP MCP with a token, and let a client call them. Add a reviewer pass that reads a screenshot and a scene dump and returns approve or specific findings. Cap retries at one per task so loops end. The same shape works for other scriptable programs.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Blender https://www.blender.org/download/ (The host app the tools drive.); blender-ai-mcp-addon https://github.com/anujasid/blender-ai-mcp-addon (The add-on itself, to read the tool definitions.)
- **Field Notes line:** A Blender add-on puts 21 scene tools behind an MCP server, with a manager, worker and reviewer chain that stops after two failed reviews.

### H-0296 sell narrow named jobs, not AI
2026-10-17, vault, https://www.youtube.com/watch?v=FS_hLDTDI1w

- **Mechanism:** Each offer is written as one scoped outcome with a name the buyer already uses (missed-call text-back, review requests, dormant-customer reactivation) instead of a general AI service. The buyer judges it on a single number, such as calls recovered or reviews gained. Under the hood it is a small automation (SMS or email trigger, a template, a log) wrapped in a one-line promise.
- **Claim:** Narrow, named, single-outcome offers sell more easily than a general AI service.
- **Testable:** no. Testing it means putting offers in front of real buyers, which needs outreach and an audience. Needs: A buyer audience and a sending channel..
- **Idea on its own:** sound. A single measurable outcome per offer is an old and well-understood sales mechanism, and it fits automations that are small and checkable.
- **How it would be done:** Pick three jobs with an obvious counter (missed calls, review requests, lapsed customers). For each, write a one-sentence promise, a before and after metric, and a minimal automation that produces the metric. Build the automation with Claude Code and a webhook or SMS API, log every event to a CSV so the number is real. Then put each offer in front of a small list of one trade type. A hired person would do the calling and onboarding that no script covers.
- **Stack already covers:** Claude Code with skills and sub-agents, launchd long-running pollers
- **To fetch:** Twilio free trial or a UK SMS API https://www.twilio.com/ (Sends the missed-call text-back and records delivery.); n8n community edition https://github.com/n8n-io/n8n (Self-hosted trigger and action glue for the narrow jobs.)
- **Missing:** A real list of buyers and the human selling time.
- **Field Notes line:** Selling one named job, like missed-call text-back, instead of 'AI', gives the buyer a single number to judge you on.

### H-0294 longer test of the retest rules
2026-10-16, vault, https://www.instagram.com/reel/DeR5ycpITv3/

- **Mechanism:** A rule-based retest entry on Nasdaq futures is backtested over a longer span, then compared with random-entry runs of the same trade count to give a luck percentile. The vault's 10-week 15-minute run made +1878 on one MNQ contract at 2R and beat 95 percent of random runs. Two years of 1-hour bars give far more trades before any claim.
- **Claim:** A 10-week NQ 15m backtest gave +1878 on 1 MNQ at 2R and beat 95 percent of random runs.
- **Testable:** yes. On two years of keyless 1h NQ=F bars, does the retest rule beat 95 percent of random-entry runs with the same trade count? Queued as P-0166.
- **Idea on its own:** needs-a-run. Ten weeks is too short to separate an edge from luck, and a longer sample is the cheap, decisive check.
- **How it would be done:** Pull about 730 days of 1h NQ=F bars via yfinance, which allows that span keyless. Encode the 8 Oct retest rule exactly as written in the vault, run it with 2R targets, then run a few thousand random-entry simulations with matching trade count and the same exits. Use the backtest-with-luck-test skill for the permutation step. Report net result, trade count and luck percentile, with the rule frozen before the run.
- **Stack already covers:** freqtrade
- **To fetch:** yfinance https://github.com/ranaroussi/yfinance (Free hourly NQ=F bars for up to 730 days.)
- **Field Notes line:** The 10-week Nasdaq retest rule beat 95 percent of random runs; two years of hourly bars will say whether that was luck.

### H-0291 Learning to Steer LLM Agents and Multi-Agent Systems
2026-10-16, arxiv, https://arxiv.org/abs/2610.22316

- **Mechanism:** A separate steering agent watches a running agent's context. A cheap fast path decides whether to intervene; a costly slow path writes the intervention. Both paths are trained together with a pairwise ranking objective and GRPO, and the intervention rate can be tuned without retraining.
- **Claim:** Improves performance and efficiency of single and multi-agent search systems and transfers to unseen executors.
- **Testable:** no. It needs RL training and a trained steering model, and there is no local model on this Mac. Needs: GPU training, the paper's code and weights..
- **Idea on its own:** sound. A two-tier monitor, cheap to check and costly to intervene, fits how drift actually shows up in long runs.
- **How it would be done:** A prompt-only version is possible: a Haiku child reads the last N steps of a probe run against its stated goal and flags drift, with Sonnet writing the correction only when flagged. Log how often it fires and whether the run recovers. The trained version needs RL tooling and a GPU.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Missing:** Trained steering model weights and training code.
- **Field Notes line:** A cheap watcher decides when a long agent run has drifted off its goal, and a costly one writes the correction.

### H-0290 Leonxlnx/earshot: Ears for coding agents: let AI hear, review and make sound. CPU-only, open source.
2026-10-16, github, https://github.com/Leonxlnx/earshot

- **Mechanism:** Audio is embedded with a CPU audio-text model and compared by cosine similarity to a vocabulary of 322 descriptions, with z-scores calibrated against references to give strong, plausible or weak verdicts. Objective measures such as LUFS, true peak and tempo come from signal processing with no model. A critique command scores a film's audio against a profile built from 7 professional launch films.
- **Claim:** It turns sound into text evidence an agent can use: describe, match, find, timeline and critique, running on CPU only.
- **Testable:** yes. Does earshot install and run `measure` and `describe` on a Proteus-made audio or film file on CPU, and does the description match what the file is? Queued as P-0165.
- **Idea on its own:** needs-a-run. Embedding-similarity tags are plausible, but accuracy on real files and model download size are untested.
- **How it would be done:** Install into the in-folder Python 3.12 venv, run measure on an ElevenLabs voice file and a HyperFrames render, then describe and critique them. Check whether the first run downloads model weights and how large. Feed critique output back into the render loop as a QA step for the Nolan and Sixteen Nights films.
- **Stack already covers:** HyperFrames (video compose, captions, render), ElevenLabs (voice), local transcription
- **To fetch:** Leonxlnx/earshot https://github.com/Leonxlnx/earshot (The CLI and MCP server to install and run.)
- **Field Notes line:** Earshot gives coding agents ears: CPU-only commands that describe a sound in words and score a film's audio against seven launch films.

### H-0288 mistake-becomes-a-rule trade journal
2026-10-16, vault, https://www.instagram.com/reel/DeR5ycpITv3/

- **Mechanism:** Every losing or odd trade in a paper window gets a one-line cause logged within a day, classed as rule change or variance. A cause is only allowed to alter a rule if it recurs, with the change committed before the next window. This stops rules being tuned to single outcomes and shows how much of the loss is noise.
- **Claim:** The reel pitches a journal habit; the vault notes only 7 trades and +256 dollars, so no edge evidence.
- **Testable:** no. It needs a paper window with real losing trades to classify, which does not exist tonight. Needs: A running S1 paper window with at least 20 closed trades..
- **Idea on its own:** sound. Separating variance from rule faults before editing rules is a standard guard against overfitting to single trades.
- **How it would be done:** Add a causes column to the paper trade log and write the one-line cause at close. Set a pre-registered threshold, for example the same cause three times, before a rule may change. At window end count rule-change versus variance causes and report the split. No script covers the judgement of what a cause was, so a person or sub-agent writes it.
- **Stack already covers:** Claude Code with skills and sub-agents, freqtrade
- **Field Notes line:** A one-line cause per losing trade, labelled rule change or variance, would show how much of a paper window's loss is just noise.

### H-0285 MLExpert: Towards a Generalist Agentic Model for Autonomous Machine Learning Engineering
2026-10-16, arxiv, https://arxiv.org/abs/2610.22344

- **Mechanism:** A 35B mixture-of-experts model is post-trained for long machine-learning engineering runs. Executable Kaggle tasks come from a factory, supervised fine-tuning transfers tool use and coding, then Windowed Interaction RL gives each stretch of decisions between experiment results one shared outcome reward, with asynchronous collection and policy correction so updates happen before a trajectory ends.
- **Claim:** Average medal rate on MLE-Bench Lite rose from 37.9% to 72.7%, comparable to larger frontier models.
- **Testable:** no. It needs GPU training of a 35B model and the paper's task factory, none of which is available keyless here. Needs: GPU cluster, model weights, Kaggle task data..
- **Idea on its own:** sound. Windowed credit assignment is a reasonable fix for sparse rewards in long runs, though the headline needs independent replication.
- **How it would be done:** Reproduction needs the Kaggle-MLE Factory to build executable tasks, an SFT stage on successful trajectories, then an RL loop with windowed rewards on a GPU rig. A hired ML engineer would be needed. A cheap slice for Proteus is reading the paper's harness design to inform its own probe loop.
- **To fetch:** MLE-Bench https://github.com/openai/mle-bench (The public benchmark the paper's Lite split is drawn from.)
- **Missing:** GPU training capacity and the paper's task factory.
- **Field Notes line:** Credit for a long agent run is split into windows between experiment results, each with a shared reward; medal rate went 37.9 to 72.7 percent.

### H-0284 pro-vi/cc-stretch: Stretchtext replies for Claude Code: short by default, each phrase grows in place when you click it
2026-10-16, github, https://github.com/pro-vi/cc-stretch

- **Mechanism:** A Claude Code plugin instructs the model to write replies in a short form with marked phrases, each carrying a longer expansion. The renderer shows the short form and swaps a phrase for its long version on click, and the plugin reports which stretches were opened back to the model. A bench script compares word counts of skim versus full across transcripts.
- **Claim:** The unclicked view was 17 percent of the words, carrying about two of three key points, across 69 real replies.
- **Testable:** yes. Does the bench script run on Proteus's own transcripts, and what share of words does the skim form keep? Queued as P-0164.
- **Idea on its own:** needs-a-run. Whether a short form keeps the important points is measurable from the repo's own bench, though the author grades his own replies.
- **How it would be done:** Clone the repo into sandbox, read bench/README.md and run the bench against local session transcripts, which already exist from usage.py. Check whether the measurement needs a model call; if so, record it as blocked. Compare the skim share to the claimed 17 percent.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** pro-vi/cc-stretch https://github.com/pro-vi/cc-stretch (The plugin and its bench folder.)
- **Field Notes line:** A plugin applies Ted Nelson's 1967 stretchtext to Claude replies: 17 percent of the words by default, the rest one click away.

### H-0283 How the Claude Code team does code review
2026-10-16, hn, https://claude.dev/blog/solving-code-review-at-anthropic/

- **Mechanism:** Review is layered: automated agent reviewers read each change first, human time is rationed to the changes that need it, and the target is the minimum human review that does not raise reverts or incidents. Reverts and incidents are the feedback signal, and fast, easy rollback is part of the design. The reviewer is improved over time from missed bugs.
- **Claim:** From June to September merged PRs more than doubled while the share reverted fell by over 40 percent.
- **Testable:** no. It is an internal process on private repositories, with no public data or tool to run. Needs: Access to a high-volume agent-written repository with revert history..
- **Idea on its own:** needs-a-run. Using revert rate as the review-quality metric is sensible, but the numbers come from one team's own repository.
- **How it would be done:** On a Proteus repo, add an automated reviewer pass on every nightly commit and log reverts and later fixes against it. Compare revert rates with and without the pass over several weeks. A human would still decide which changes always get eyes, such as the hook and charter files.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Missing:** A repo with enough change volume to make revert rates measurable.
- **Field Notes line:** Anthropic's Claude Code team moved most code reading to machines and judges review by revert rate; their claim is unverifiable from outside.

### H-0282 Paper-forward cluster log from the EDGAR daily index with a pre-registered 100-signal bar
2026-10-16, vault, 

- **Mechanism:** SEC EDGAR publishes a daily index of filings, and each Form 4 is an XML document listing an insider's role, transaction code (P for open-market purchase) and size. A cluster is three or more distinct officers or directors filing P-code buys in the same company inside a short window. A forward log records each cluster the day it appears, with a pre-registered rule and a 100-signal bar, then scores the 21-day return against random same-size stocks and SPY.
- **Claim:** Clusters of 3+ insider buys beat random same-size US stocks by about 1.3% per 21 days before costs over 24 months, per the vault's backtest.
- **Testable:** yes. Can the EDGAR daily index plus Form 4 XML be parsed keyless into a cluster list, and how many 3+ officer or director P-code clusters appeared in the last 30 days? Queued as P-0163.
- **Idea on its own:** needs-a-run. The edge is small and the vault's own numbers say it vanishes after costs, so only a forward log can settle it.
- **How it would be done:** Pull form.idx or the daily index from sec.gov (needs a descriptive User-Agent, no key), filter to Form 4, fetch each XML and keep transaction code P by officers and directors. Group by issuer over a rolling window and flag 3+ distinct filers. Commit the rule, window and 100-signal bar before the first logged signal, then log each cluster with entry price from a free daily bar source. Score at 21 days against SPY and random same-size names with the existing permutation-test approach.
- **Stack already covers:** launchd long-running pollers, freqtrade
- **To fetch:** SEC EDGAR full-index and Form 4 XML https://www.sec.gov/Archives/edgar/daily-index/ (Public source of the filings; rate limit 10 requests a second with a User-Agent.); yfinance https://github.com/ranaroussi/yfinance (Free daily prices to score the 21-day forward return.)
- **Field Notes line:** Insider cluster buys leave a public trail on SEC EDGAR; a forward log with a 100-signal bar would show whether the 1.3% edge survives costs.

### H-0280 One live automation platform behind the website monthly fee
2026-10-15, vault, https://www.youtube.com/watch?v=_5uSbMMOkCQ

- **Mechanism:** A local business website is sold with a monthly fee covering an automation platform behind it: missed-call text back, form-to-text, review requests and booking. The platform watches inbound calls and forms, fires a templated text through a UK number, and logs leads. Monthly tiers are defined by which automations are on, not by hours of care.
- **Claim:** A website plus live automation justifies a recurring monthly fee for local businesses.
- **Testable:** no. Needs a platform account, a UK sender number and a real phone line to test. Needs: An automation platform account and a UK number..
- **Idea on its own:** sound. Fast reply to a missed call is a real, simple mechanism, and the work is wiring plus UK messaging compliance.
- **How it would be done:** Pick a platform, port or buy a UK number, and set a trigger on missed calls that sends one SMS with a booking link. Add a form-to-text path and a review request after a completed job. Test with a real phone through each path and record delivery times. A person is needed for number registration, sender ID rules and the client's consent wording.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Twilio https://www.twilio.com/ (Programmable UK number and SMS if building the missed-call text back directly (paid, needs an account).)
- **Missing:** A tested UK number and platform, unverified since July per the vault note.
- **Field Notes line:** Missed-call text back is the small automation that sits behind a website's monthly fee; the open question is a tested UK number.

### H-0279 huggingface/funes (new in awesome-claude-code)
2026-10-15, awesome, https://github.com/huggingface/funes. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** A Rust binary indexes past agent session transcripts (Claude Code, Codex and others) into a searchable store, and exposes recall and get as tools to the agent. A per-turn hook keeps the index current, and the memory can be published as a Hugging Face dataset so another machine or person recalls from it with one flag. Answers name the sessions they drew from.
- **Claim:** Any agent can recall past decisions and rationale across tools, with memory shared as a Hub dataset.
- **Testable:** no. Runs a downloaded binary from a curl pipe and needs a coding agent to answer, which is not a keyless sandbox test. Needs: A model to answer questions, and trust in the prebuilt binary..
- **Idea on its own:** sound. Transcript indexing with cited recall is a straightforward retrieval design that fits how sessions already log to disk.
- **How it would be done:** Proteus already keeps run logs and transcripts, so the same idea is a local index over them with source IDs. Steps: parse transcript files, chunk by turn, index with a keyword or embedding search, and return hits with session ID. Funes could be tried on the public huggingface/funes-memory dataset, but only after reading its install script rather than piping it to a shell.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** funes https://github.com/huggingface/funes (Reference implementation of session recall.); funes-memory dataset https://huggingface.co/datasets/huggingface/funes-memory (Public sample memory to inspect structure.)
- **Field Notes line:** Session transcripts become a searchable, shareable dataset the agent queries mid-task, with sources named.

### H-0277 Doc2Harness: Benchmarking LLMs on Long-Horizon Harness Engineering of Coding Agents
2026-10-15, arxiv, https://arxiv.org/abs/2610.20344

- **Mechanism:** Stage one has a model build a full agent harness from an interface skeleton and a document describing twelve existing harnesses. Stage two runs the frozen harness in fresh containers per test case, driven by a scripted mock model so the model is not a variable. Each case is scored on four observable channels: requests sent to the model, files on disk, exit code and command output, with positive controls to rule out vacuous passes.
- **Claim:** Across 19 models and 328 test cases, the best pass rate is 53.05% and the weakest 27.44%.
- **Testable:** no. Needs the benchmark release and many frontier model calls, which are not keyless. Needs: The benchmark code and paid model access..
- **Idea on its own:** sound. Removing the model from the loop with a scripted stand-in isolates the harness, which is a clean experimental design.
- **How it would be done:** Borrow the scoring design for testing Proteus's own hook and run scripts: feed the hook a scripted sequence of tool calls and assert on files written, exit codes and output. The existing hook test script already does something like this. Reading the paper's repo, once published, would show how they structure the cases. No hired help needed.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Missing:** The benchmark's code and test cases, if released.
- **Field Notes line:** A scripted mock model replaces the real one so harness quality can be scored deterministically, on four observable channels.

### H-0276 i12bp8/decomp.wtf: What The Function: your AI agent decompiles games you own into C that compiles to the exact same byte
2026-10-15, github, https://github.com/i12bp8/decomp.wtf

- **Mechanism:** An agent is handed a game one function at a time. Each attempted C function is compiled with the game's original compiler and compared byte for byte with the original machine code, and only an exact match scores. That hard oracle stops the model bluffing and lets it iterate until it matches. It runs locally on Linux (compilers are Linux programs) and needs the user's own ROM.
- **Claim:** Point your own agent at a game you own and it produces C that rebuilds to identical bytes, with 245 public projects to continue.
- **Testable:** no. Linux and Windows only (not macOS), needs a game ROM and the project is archived. Needs: A Linux box and a legally owned ROM..
- **Idea on its own:** sound. An exact-match verifier is the strongest kind of feedback loop for an agent, whatever the domain.
- **How it would be done:** The pattern is: pick a task with a cheap exact oracle, give the agent a tool to submit attempts, and score only on a perfect match. For decompilation that means the matching compiler plus a diff of the object file. Reuse the idea elsewhere, for example matching generated output against a reference hash. A person is needed for ROM dumps and for community norms, since many decomp projects reject AI contributions.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** decomp.wtf https://github.com/i12bp8/decomp.wtf (Reference implementation of the byte-match loop (archived, v0.10.6).); decomp.dev https://decomp.dev (Index of public matching-decomp projects and their progress data.)
- **Missing:** A Linux environment, since macOS is unsupported.
- **Field Notes line:** A byte-exact compiler check turns decompiling into a game the agent cannot cheat, and the author archived it after community pushback.

### H-0274 UK accounts editions
2026-10-15, vault, https://claude.com/marketplace/plugins/small-business

- **Mechanism:** An assistant connects to a small business's email, calendar, files and accounts software through connectors (MCP-style), and each workflow starts in approval mode so a human OKs actions. The open question is whether the Xero UK and QuickBooks UK connectors exist as UK editions with the same scopes as the US ones. That is answered by the connector listings and docs, not by the assistant itself.
- **Claim:** The plugin replaces Make, Zapier or n8n stitching with one assistant across email, calendar, files and, on paid plans, accounting tools.
- **Testable:** no. Confirming the UK connectors needs a paid plan and a Xero or QuickBooks account. Needs: A paid Claude plan and a Xero UK or QuickBooks UK sandbox company..
- **Idea on its own:** needs-a-run. The idea is sound if the UK connectors exist and behave the same, which only a connected test shows.
- **How it would be done:** Read the connector directory and each connector's docs for UK region and scope notes. Create a free Xero demo company, connect it, and run one read-only query and one approval-gated write. Record what worked and what the UK edition lacked, such as VAT or Making Tax Digital fields. A person would handle account sign-up and the paid plan.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Xero demo company https://www.xero.com/uk/ (Free demo company to test a UK accounts connector against.)
- **Missing:** Confirmation that UK accounts connectors exist, which nobody has checked.
- **Field Notes line:** Before promising a UK small business an assistant wired to Xero, check whether the UK connector exists, not just the US one.

### H-0270 hujjun/mcd-saver-strategist: 麦当劳省钱点餐助手（麦门精算师）｜麦当劳优惠券组合优化 Skill：拉取麦当劳菜单与全部可用优惠券，算出最省的点餐组合，巨无霸套餐 ¥47 → ¥21.9（省 53%）。McDona
2026-10-15, github, https://github.com/hujjun/mcd-saver-strategist

- **Mechanism:** An agent fetches menu, prices and every available coupon from McDonald's China MCP, normalises them to JSON, then a deterministic Python optimiser searches the combinations for the lowest total under optional budget and calorie caps. Coupons marked non-stackable are treated as exclusive with all others. The model only explains and orders; arithmetic is kept out of the LLM because it gets sums wrong. Price is re-checked with the MCP calculate-price call before ordering.
- **Claim:** A Big Mac meal drops from 47.00 to 21.90 yuan (53% saving) using the 1+1 coupon combination, on sample data.
- **Testable:** yes. Does the bundled offline optimizer.py run and does selftest.py pass all 19 tests, reproducing the 21.90 yuan result on its sample data? Queued as P-0160.
- **Idea on its own:** sound. Splitting retrieval, exact optimisation and explanation is a clean pattern, and coupon stacking is a small knapsack problem.
- **How it would be done:** Clone the repo into sandbox, run optimizer.py and selftest.py on the bundled sample data and compare the printed saving with the README. Then perturb the sample coupons to check the exclusivity rule holds. The same pattern (fetch, normalise, solve, verify) would apply to UK supermarket multibuy offers if a public price source existed. Live use needs the vendor's MCP token, which Proteus does not have.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** mcd-saver-strategist https://github.com/hujjun/mcd-saver-strategist (Offline optimizer and self-test to run.)
- **Missing:** Live menu and coupon data needs a vendor MCP token.
- **Field Notes line:** Keep coupon arithmetic out of the model: the agent fetches data, plain Python searches the combinations, and the shop's price check confirms.

### H-0268 signal-timed outreach
2026-10-15, vault, https://www.altahq.com

- **Mechanism:** Cold email is timed to a cheap public local signal (a new company filing, a planning application, a fresh job advert, a bad review, a closed-lost deal) so the first line gives a real why-now. A scheduled job pulls the signal feed, matches it to a prospect list, and a template or model writes one line from the signal. The lift comes from relevance and timing, not volume, and the numbers come from reply rates per signal type once sent.
- **Claim:** Alta says AI SDR agents use buying signals to time outreach; the vault note is that cheap local signals can serve as the why-now.
- **Testable:** no. The verdict is a reply rate, which needs real sends to real people, not a keyless run. Needs: Sending domain, a prospect list and live sends under UK PECR rules..
- **Idea on its own:** needs-a-run. Signal-led relevance is plausible but only a split send shows whether it beats a plain opener.
- **How it would be done:** Pick two or three free feeds that fire for trades firms, such as Companies House new incorporations, planning portals or job boards. Write a small poller that logs new signals per day with a timestamp. Join them to a prospect list by name or postcode. Draft one-line openers per signal type and send half with the signal and half without, then compare replies. A person is needed for the sending identity and for checking each draft against UK B2B email rules.
- **Stack already covers:** Claude Code with skills and sub-agents, launchd long-running pollers
- **To fetch:** Companies House bulk product and API https://developer.company-information.service.gov.uk/ (Free feed of new UK company incorporations as a signal source (API key is free but needs an account).)
- **Missing:** A sending identity with reply volume large enough to split-test.
- **Field Notes line:** Timing cold email to a public local signal, not a vendor's quote-only AI SDR, is the part worth copying.

### H-0266 nateherkai/roast-room: Seven AI advisors (Bezos, Paul Graham, Hormozi, Gary Vee, Dan Martell, Gino Wickman, Buffett) deb
2026-10-14, github, https://github.com/nateherkai/roast-room

- **Mechanism:** Each of seven advisors is a Claude Code sub-agent seeded with a persona built from that person's public letters, essays and talks. A chair agent collects the decision and numbers, runs rounds of debate, then scores a verdict; a small local Node app shows the turns around a table and exports a PDF. Everything runs inside the user's Claude plan.
- **Claim:** Seven persona advisors debate a business decision and produce a scored verdict and PDF.
- **Testable:** no. The useful part needs many live Claude calls and is not keyless; running only the viewer tests nothing about the idea. Needs: Claude plan usage for sub-agent runs..
- **Idea on its own:** needs-a-run. Persona debates look rigorous but may only echo the user's lean; a comparison against a single plain prompt on the same decisions would show whether they add value.
- **How it would be done:** Write persona prompts from public source text, run rounds with a chair that forces disagreement, and have a scorer produce a verdict. To judge the value, run the council and a single baseline prompt over the same set of decisions with known outcomes. A human who has run the business still decides, as the personas have no stake.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** roast-room https://github.com/nateherkai/roast-room (The council prompts and local viewer.)
- **Field Notes line:** Seven persona sub-agents argue a business decision and a chair scores it; the open question is whether the personas add anything over one prompt.

### H-0265 Show HN: I wrote an email app that accepts only one sender per inbox
2026-10-14, hn, https://clova.email/

- **Mechanism:** A catch-all mail domain accepts any address at receive time. The first sender (domain, or exact address for webmail providers) to write to an address becomes its only allowed sender, and the service rejects all later mail from anyone else. Prefix inboxes let you invent suffixes on the fly, each locking to its first writer, and temporary inboxes expire and bounce. A bounce for unknown senders is what a spammer's list-cleaning sees, and an MCP server lets an AI read the inboxes.
- **Claim:** Infinite self-creating inboxes, each locked to one sender, so leaked addresses stop receiving spam.
- **Testable:** no. It requires signing up for the service and owning a domain. Needs: An account on the service and a domain with MX records..
- **Idea on its own:** sound. First-sender locking on a catch-all domain is a simple, working way to trace leaks and kill spam per address.
- **How it would be done:** Run a catch-all domain with a mail server that records the first envelope sender per recipient and rejects others at SMTP time. Give each service a unique suffix. Self-hosting is a few hours with an existing open source mail server and a rule script.
- **To fetch:** Postfix https://www.postfix.org/ (Self-hosted SMTP with policy hooks to implement first-sender locking.)
- **Missing:** A domain and a mail host.
- **Field Notes line:** Every email address you invent locks to the first sender who uses it, so a leak shows exactly who sold you out.

### H-0264 score the 20-minute filter set on a dated cohort
2026-10-14, vault, https://www.instagram.com/reel/DcjuRbTyUPV/

- **Mechanism:** A screener filter set is applied at minute 20 of a pump.fun coin's life: age 20 minutes, liquidity 10k, volume 15k, market cap 20k. Coins that pass are bought and the claim is that they tend to be higher later. The test is a cohort: record who passes at minute 20 and compare their price at 24 hours to the whole launch cohort.
- **Claim:** The reel says coins passing these four floors at minute 20 are the ones worth buying.
- **Testable:** yes. Of pump.fun coins in the poller data passing all four filters at minute 20, what percentage are above their minute-20 price at 24 hours, versus the same percentage for all coins? Not queued (daily cap).
- **Idea on its own:** needs-a-run. Floors on size only select survivors; whether they add anything over the base rate is a counting question the poller data answers.
- **How it would be done:** Query the poller's snapshots for each launch at about minute 20 and mark the ones that pass all four filters. Look up the price at 24 hours for each and compute the share higher, the median return, and the same figures for the unfiltered cohort and a random sample of the same size. Report sample size and confidence interval and count coins with no 24h data as losses.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers and a Solana paper desk (the Grinder), launchd long-running pollers, backtest-with-luck-test skill
- **Field Notes line:** Four screener floors at minute 20 get scored on a dated cohort: what share of passers are higher a day later, against all launches.

### H-0262 SEAR: Self-Evolving Agentic Robotics
2026-10-14, arxiv, https://arxiv.org/abs/2610.18792

- **Mechanism:** SEAR runs LLM agents in three modes: code-as-policy, agent-as-policy and auto-research fine-tuning. Its benchmark adds controls that separate retained experience from repeated attempts, familiar tasks, privileged state, larger budgets and luck. Findings are measured across seven models and 330 simulated tasks.
- **Claim:** On easier tasks, re-rolling short attempts does as well as accumulating experience; shared code routines transfer, task-specific ones do not.
- **Testable:** no. It needs robot simulators and frontier model budgets across many tasks. Needs: The released benchmark, simulators and model API spend..
- **Idea on its own:** sound. Controls that separate retained learning from repeated attempts are exactly the right test for any self-improving loop.
- **How it would be done:** For any Proteus agent loop that claims to improve, run a control arm that gets the same number of fresh attempts with no memory and compare success rates. Add a luck control by shuffling the stored experience. The benchmark code is released but robotics-specific; the evaluation design is what transfers.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Field Notes line:** A robot-agent benchmark asks whether agents learn or just retry, and finds re-rolling short attempts matches learning on easy tasks.

### H-0261 YeonwooSung/my-claude-code-mods: Custom Claude Code Mods that I need
2026-10-14, github, https://github.com/YeonwooSung/my-claude-code-mods

- **Mechanism:** Mods hook Claude Code session events. Time-machine records every tool call on a branching timeline and takes shadow-git snapshots of the working tree so any step can be restored or compared. Agent-profiler and context-inspector read the session log to split time and context between model wait, tools and re-reads, and export OTLP traces. Loop-detective flags repeated Bash failures and edit/retry cycles.
- **Claim:** Seven mods give session profiling, context waste analysis, tool-call rewind, and loop detection.
- **Testable:** yes. Does the core test suite (npm ci --ignore-scripts, npm test) pass on this Mac without a Claude Code engine or account, yes or no? Queued as P-0156.
- **Idea on its own:** sound. Per-step snapshots and loop detection address real agent failure modes and are cheap to build on top of session logs.
- **How it would be done:** Read session transcripts for tool-call records, snapshot the tree with a separate git dir after each call, and compute loops by hashing repeated command and error pairs. This could feed the nightly run logs with a loop count per run. The engine-dependent parts need an interactive Claude Code session and are not covered by the core tests.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** my-claude-code-mods https://github.com/YeonwooSung/my-claude-code-mods (The mods and their core test suite.); OpenTelemetry Jaeger https://www.jaegertracing.io/download/ (Viewer for the exported OTLP traces.)
- **Field Notes line:** Claude Code mods that snapshot every tool call to shadow git and flag retry loops; the core logic has a keyless test suite.

### H-0259 pull the stake at 5x versus holding
2026-10-14, vault, https://www.instagram.com/reel/DecmMdSuofw/

- **Mechanism:** On a new token, sell the original stake once the price reaches five times entry and keep the remainder as a free ride. The claim is that this locks in profit before most launches collapse. It is a scale-out exit rule, so its value depends on how often launches hit 5x and what the survivors do afterwards.
- **Claim:** The reel says taking your stake out at 5x beats just holding memecoins.
- **Testable:** yes. Across launches in the Proteus poller data with a recorded entry price, what fraction reach 5x and does the pull-at-5x rule beat holding to 24 hours, as a number? Queued as P-0155.
- **Idea on its own:** needs-a-run. Scale-out rules cannot create edge by themselves; only the hit rate and what happens after 5x decide whether it beats holding.
- **How it would be done:** Take the Grinder's logged launches with first-seen price and later price snapshots. Fix the rule before looking: entry at first snapshot, sell the stake at 5x if it prints, otherwise exit at 24 hours. Compare against holding to 24 hours and random-entry control, with slippage and fee assumptions stated. Count tokens that are not sellable at all.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers and a Solana paper desk (the Grinder), preregister-a-book skill, backtest-with-luck-test skill
- **Field Notes line:** A 5x scale-out rule is easy to replay on dated launches: count how many reach 5x and compare with holding.

### H-0257 ChunkAct: Action Chunking for Agentic Robotics
2026-10-14, arxiv, https://arxiv.org/abs/2610.18874

- **Mechanism:** An LLM agent normally reasons before every primitive action using the full history. ChunkAct compiles stored memory offline into chains of primitives per sub-goal. At run time one call launches a whole chunk, which runs without the model and hands control back only on failure, so model calls scale with decisions rather than steps.
- **Claim:** On LIBERO-Pro it gains 5.0 points in task success with 2.9x fewer LLM calls and 4.4x fewer input tokens.
- **Testable:** no. It needs the LIBERO-Pro robot simulator and a VLA stack, which are not keyless or quick. Needs: LIBERO-Pro simulator and a vision-language-action model..
- **Idea on its own:** sound. Replacing repeated model reasoning with compiled routines that escalate only on failure is a general, sensible way to cut agent cost.
- **How it would be done:** Log successful agent runs, cluster repeated tool-call sequences per sub-goal, and store them as scripts with a pass/fail check at the end. At run time the planner picks a sub-goal and the script runs unattended, calling the model only if the check fails. The same idea applies to Proteus nightly tasks that repeat the same Bash sequences.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Field Notes line:** Compile repeated agent routines into chunks that run without the model and return control only on failure: 2.9x fewer calls in a robot benchmark.

### H-0256 nateherkai/herk-edit-kit: Herk Edit Kit by Nate Herk: edit videos, reels, and YouTube Shorts with Codex or Claude Code. 
2026-10-14, github, https://github.com/nateherkai/herk-edit-kit. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** A word-level transcript drives the edit: silence and filler gaps are found from word timings, mistakes and retakes are flagged from the text, and an edit decision list (EDL) is rendered with ffmpeg and then retimed so the transcript matches the cut. Captions, B-roll and motion cards are HyperFrames compositions placed against the retimed timeline, with beat-sync validation against a BPM grid. Transcription defaults to ElevenLabs Scribe but accepts Whisper or a supplied transcript.
- **Claim:** An agent edited a 51-second reel end to end from one raw take, and the kit ships 15 skills and 406 motion cards.
- **Testable:** yes. Does npm ci and npm test pass on this Mac with the bundled synthetic fixture and no API keys, yes or no? Queued as P-0154.
- **Idea on its own:** sound. Cutting from word timings and retiming the transcript after the cut is a deterministic, checkable way to automate dialogue edits.
- **How it would be done:** Transcribe locally, mark gaps above a threshold from word timestamps, and generate an EDL. Render the cut with ffmpeg, remap the word times through the EDL and burn captions in a HyperFrames composition. Check the result by comparing caption timing to audio. A human still judges pacing and the hook.
- **Stack already covers:** HyperFrames, local transcription, ElevenLabs
- **To fetch:** herk-edit-kit https://github.com/nateherkai/herk-edit-kit (The scripts for silence cutting, EDL review and retiming.)
- **Field Notes line:** A transcript-driven edit loop (word timings to EDL to retimed captions) is packaged as 15 skills; the keyless starter is the part we can check.

### H-0255 Show HN: Pulse Local, a Mac budgeting app whose AI models run on your machine
2026-10-14, hn, https://pulseos.finance

- **Mechanism:** A small tuned Qwen3 0.6B model only translates the question into a structured query. Ordinary code does the arithmetic against the ledger so the model never produces a number. A second, larger 4B model reads the same question independently, and if the two structured readings differ the app answers 'not sure' instead of guessing.
- **Claim:** Adding the 4B checker cut wrong answers from about one in five to 5 in 494 questions across three tests.
- **Testable:** no. It needs a local model runtime and the weights, and there is no local LLM on this Mac tonight. Needs: A local model runtime (Ollama or llama.cpp) and the Hugging Face weights..
- **Idea on its own:** sound. Separating language parsing from arithmetic and abstaining when two independent readings disagree is a well-founded way to cut confident wrong answers.
- **How it would be done:** Define a small query schema (metric, category, date range, currency). Have one model emit that schema from the question and a second, different model do the same. Run the schema against a CSV ledger with plain code and answer only if both schemas match, otherwise say not sure. Build a test set of a few hundred questions with known answers and count wrong, abstained and right. The same disagreement-abstain pattern would fit any Proteus desk that answers numeric questions from data.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Ollama https://ollama.com/download (Local runtime for small Qwen3 models.); PulseOS Hugging Face weights https://huggingface.co/PulseOS (The tuned 0.6B parser the write-up describes.)
- **Missing:** A labelled question and answer set for a ledger, which would have to be written.
- **Field Notes line:** A budgeting app lets a tiny model parse the question, code do the sums, and a second model veto disagreements, which it says cut errors to 5 in 494.

### H-0254 crypto spot pairs laggard check
2026-10-14, vault, https://www.instagram.com/reel/DeaHN_lJJkB/

- **Mechanism:** Pick two coins whose prices have moved together (rolling correlation or cointegration on hourly closes). When the spread between them widens, the laggard is expected to catch up with the leader as the spread mean-reverts. Long-only version buys only the laggard and exits when the spread closes or a time stop hits. Numbers come from public exchange candles; the edge has to survive fees and the cases where the pair breaks for good.
- **Claim:** The reel says trading the laggard of a matched pair against the leader gives steady returns.
- **Testable:** yes. On public hourly candles for 20 liquid spot pairs, does buying the laggard when the spread passes 2 sigma beat holding it over the next 48 hours after 0.2 percent round-trip fees? Queued as P-0153.
- **Idea on its own:** needs-a-run. Mean reversion in correlated pairs is real in principle, but costs and permanently broken pairs often erase it, so only a dated replay settles it.
- **How it would be done:** Pull 90 days of hourly closes for a list of liquid spot pairs from a keyless exchange or aggregator endpoint. Compute a rolling log-ratio for each candidate pair and its z-score, and fix the entry (z above 2 on the laggard side), exit (z back to 0) and time stop before looking at results. Replay long-only, charge fees on both legs, and compare against simply holding the same coin for the same windows and against random entry dates. Commit the rules and due date first with the preregister skill, then score with the luck-test skill. No hired help needed; the open question is whether pairs break inside the window.
- **Stack already covers:** freqtrade, backtest-with-luck-test skill, preregister-a-book skill
- **To fetch:** Binance public klines API https://data-api.binance.vision/api/v3/klines (Keyless hourly candles for spot pairs.); statsmodels coint test https://www.statsmodels.org/ (Engle-Granger cointegration test to select pairs without eyeballing.)
- **Field Notes line:** A pairs-trading reel claims the laggard catches up; a long-only fee-adjusted replay on public candles will say whether it does.

### H-0252 Per-post CPM tracked per account feeding back into what gets made next
2026-10-13, vault, 

- **Mechanism:** Each published post is logged against its account with its views, then cost per thousand views is computed by dividing production cost by views over a fixed window. Accounts and formats are ranked on that figure, and the ranking decides which hooks, topics and formats get made next. Data comes from each platform's own analytics for accounts the operator owns.
- **Claim:** Tracking CPM per post per account and feeding it back into production is the one idea worth keeping from the write-up.
- **Testable:** no. It needs live posts with real view counts from owned accounts, which cannot be produced or read keyless tonight. Needs: Owned accounts with posted content and analytics access.
- **Idea on its own:** sound. A cost per thousand views ranking is a simple, honest feedback loop for content.
- **How it would be done:** Keep a table with one row per post: account, format, hook, production cost and views at 7 days. Compute CPM per row and average it per account and per format. Each week, brief the next batch from the top formats and retire the bottom ones. Pull view counts from the platforms' own analytics exports or public pages; a person posts the content from the owned accounts.
- **Stack already covers:** Claude Code with skills and sub-agents, HyperFrames (video compose, captions, render)
- **Missing:** Real posted content and its analytics exports.
- **Field Notes line:** Divide the cost of each post by its views, rank accounts and formats on that, and make more of what wins.

### H-0250 Build a Simple Expected Goals Model with Machine Learning and Python
2026-10-13, youtube, https://www.youtube.com/watch?v=GsfXAzfvJVM

- **Mechanism:** An expected goals model is a classifier trained on historical shots, with features such as distance, angle and body part, predicting goal or no goal. The output probability is the xG, and quality is checked with log loss or AUC on held-out shots. The video uses scraped data and scikit-learn; open event data such as StatsBomb gives the same shape.
- **Claim:** Shows how to train and evaluate a simple xG model in Python with scikit-learn.
- **Testable:** yes. Does a logistic regression on distance and angle over StatsBomb open-data shots reach a held-out AUC above 0.75? Queued as P-0144.
- **Idea on its own:** sound. Shot-level xG from distance and angle is a standard, well-validated baseline.
- **How it would be done:** Download shot events from the public StatsBomb open-data repository, compute distance and angle to goal from shot coordinates, and fit a logistic regression. Split shots by match, report AUC and log loss, then compare team xG totals with real scores. If it holds, xG per team could feed the Dixon-Coles desk as a second input. Open data covers only some competitions, so the sample is small and biased.
- **Stack already covers:** football-data and a Dixon-Coles paper desk (the Pitch), Claude Code with skills and sub-agents
- **To fetch:** StatsBomb open-data https://github.com/statsbomb/open-data (Free shot-level event data with coordinates to train on.); scikit-learn https://github.com/scikit-learn/scikit-learn (Logistic regression and AUC scoring.)
- **Field Notes line:** A logistic regression on shot distance and angle may give a usable xG; tonight's check is its held-out AUC on public data.

### H-0249 SqueezeBench: Saturation-Resilient Evaluation of Mathematical Capability
2026-10-13, arxiv, https://arxiv.org/abs/2610.13461

- **Mechanism:** Each problem fixes an integer function with known values only at small n and keeps a lower and an upper record, each a computable Lean function with a machine-checked proof. A submission must prove it bounds f, is no worse than the record anywhere and is strictly better somewhere, then becomes the new record. Two independent Lean kernels check every proof, and checks reject functions that just brute-force small n.
- **Claim:** Agents had 82 submissions accepted and improved every record, then 60 more from newer models improved 19 of 20 records again.
- **Testable:** no. Needs a Lean toolchain and the released problem set, and a meaningful submission takes agent hours. Needs: Lean 4 toolchain and the benchmark release.
- **Idea on its own:** sound. Making the verifier the judge and the record the moving bar removes both saturation and referee trust.
- **How it would be done:** Install Lean 4 and mathlib, load a problem's current records and the admission tool, then have an agent propose a better bound function with a proof. Run the checker and two kernels, and on acceptance replace the record. The same ratchet pattern could score a Proteus desk: a pre-registered rule must beat the current best on a fixed test to replace it.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Lean 4 https://github.com/leanprover/lean4 (The proof checker that makes each record verifiable.)
- **Field Notes line:** A benchmark that ratchets: every accepted Lean proof becomes the new record to beat, so it never saturates.

### H-0246 Flat monthly editing retainer for businesses already producing content
2026-10-13, vault, 

- **Mechanism:** A business that already films content pays a flat monthly fee for post-production: cuts, captions, reframes and a set number of finished clips per month. Revenue is recurring and tied to deliverable counts, not views. The work is a repeatable pipeline from raw footage to platform-sized outputs with a review step.
- **Claim:** Flat editing retainers of two to six thousand dollars a month are the money worth having in the clipping category.
- **Testable:** no. The verdict is whether a client pays, which needs outreach and a real customer, not a keyless run. Needs: A paying client and sample footage.
- **Idea on its own:** sound. Retainers for repeatable deliverables are a common service model, and the pipeline is already largely built.
- **How it would be done:** Define a package such as eight finished clips a month from the client's raw uploads. Build the pipeline as transcribe, pick moments, cut, caption and render, using the existing tools, with a human review before delivery. Find prospects among businesses that already post regularly and show a free sample cut from their public video. A person handles the sales conversation, taste checks and revisions.
- **Stack already covers:** HyperFrames (video compose, captions, render), ElevenLabs (voice), local transcription, Claude Code with skills and sub-agents
- **Missing:** A client, and a person to sell and handle revisions.
- **Field Notes line:** Selling editing as a flat monthly retainer, not per-view clipping, is the steadier shape of the clipping business.

### H-0245 plur-ai/plur (new in awesome-claude-code)
2026-10-13, awesome, https://github.com/plur-ai/plur. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** Memory is stored as plain YAML records called engrams on local disk and exposed to agents over MCP. Retrieval is hybrid, BM25 plus a local BGE-small embedding, with an optional cross-encoder reranker. Published recall is scored on LongMemEval-S, with end-to-end answer accuracy reported separately.
- **Claim:** BM25 alone reaches 92.2% R@5 on full LongMemEval-S, 95.6% hybrid and 97.6% with the reranker.
- **Testable:** yes. Does the BM25-only path of plur-bench reproduce about 92.2% R@5 on LongMemEval-S, yes or no? Queued as P-0143.
- **Idea on its own:** sound. Plain-text memory with lexical plus embedding retrieval is simple and inspectable, and the benchmark is public to check.
- **How it would be done:** Clone plur-bench, run its local BM25 path on the SHA-pinned corpus, and compare R@5 with the published 92.2%. If it matches, try the same BM25 index over Proteus's own run logs and memory notes with a few known questions. Keeping the hybrid and reranker for a later night avoids a model download tonight.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** plur-bench https://github.com/plur-ai/plur-bench (The reproducible harness behind every published number.)
- **Field Notes line:** A claimed 92.2% recall from plain BM25 on LongMemEval-S, no embeddings, which would make fancy agent memory look overbuilt.

### H-0243 ToFu: Exploiting and Fuzzing the LLM-Orchestrator-Tool Trust Boundary
2026-10-13, arxiv, https://arxiv.org/abs/2610.13651

- **Mechanism:** ToFu reads each MCP tool's metadata, such as name, description and parameter schema, and picks matching checks from a CWE-guided corpus of sanitizers (path traversal, command injection and similar). It then generates a fuzzing harness per tool and uses runtime introspection to see what the tool actually did with the argument. Oracles judge the outcome, so a bug is confirmed by an observed effect, not a guess.
- **Claim:** Across 273 MCP servers and 3405 tools, verified bugs were found in 343 tools across 118 servers.
- **Testable:** no. The framework code is not confirmed released and a faithful slice needs running many third-party MCP servers. Needs: The ToFu code and a set of MCP servers to fuzz.
- **Idea on its own:** sound. Treating model-written arguments as untrusted input and fuzzing against documented schemas is standard security practice applied to a new boundary.
- **How it would be done:** List a server's tools through the MCP tools/list call, then for each parameter pick payloads from a sanitizer corpus matching its type. Call the tool in a sandbox, observe file, process and network effects, and flag violations of the documented input rules. Run it against servers the stack already uses to check what Proteus trusts. A security reviewer would triage which findings are real.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** MCP Inspector https://github.com/modelcontextprotocol/inspector (Lists and calls a server's tools so a fuzz harness can be driven against them.)
- **Missing:** The paper's own harness generator, unless the authors release it.
- **Field Notes line:** Fuzzing 3405 MCP tools turned up verified bugs in 343 of them: tools trust whatever arguments the model hands over.

### H-0242 zhuyansen/new-term-radar: Daily radar for new AI terms: names of new models, products and repos, caught on X, Hugging Fa
2026-10-13, github, https://github.com/zhuyansen/new-term-radar

- **Mechanism:** It watches the early trail of a new name rather than search volume. It flags Hugging Face models newly in the trending top 50, GitHub repos under 14 days old averaging 200+ stars a day or gaining 400+ since yesterday, and words shared by several new URLs in listed sitemaps. Google Trends is used 14 days later only to score each lead against its own baseline.
- **Claim:** Catches new AI names days to weeks before keyword tools, for example a repo with 7,700 stars nine days after creation.
- **Testable:** yes. How many repos created in the last 14 days average 200+ stars a day on the public GitHub search API, and how many new models are on the Hugging Face trending list tonight? Queued as P-0142.
- **Idea on its own:** sound. Star velocity on a young repo is an observable early signal, and it can be backtested against later search interest.
- **How it would be done:** Query the GitHub search API for repos created in the last 14 days sorted by stars, compute stars per day from created date, and flag those over 200. Pull the Hugging Face trending models list and diff it against yesterday's saved copy. Save each day's flags and later check whether the names grew, giving a hit rate. The X and paid-keyword parts need an AIsa key and can be skipped. This could feed the harvester or a Grinder-style token naming signal.
- **Stack already covers:** launchd long-running pollers, Claude Code with skills and sub-agents
- **To fetch:** new-term-radar https://github.com/zhuyansen/new-term-radar (Reference code for the GitHub breakout and Hugging Face trending checks.)
- **Field Notes line:** A breakout detector for new AI names: a young repo averaging 200 stars a day is the whole signal, and it is public.

### H-0241 How to engineer an AI harness for game development
2026-10-13, hn, https://kylekukshtel.com/ai-harness-engineering-game-development-claude-code

- **Mechanism:** The harness makes a game legible to a coding agent: the simulation is separated from rendering and seeded so runs replay exactly, and the agent captures screenshots and videos of each mechanic to check its own work. Dev tools such as level editors and asset converters are built by side agents and kept out of the main code. Comments push back that determinism across platforms is confining and that code was never the hard part of games.
- **Claim:** A structured harness lets Claude Code build larger games reliably, with a commenter reaching decent FPS at around 40k lines.
- **Testable:** no. It is a working practice across a whole project and cannot be reduced to a keyless 30 minute run with a number. Needs: A game project and model sessions.
- **Idea on its own:** sound. Deterministic replay and visual self-checks are well-proven ways to give an agent a feedback loop.
- **How it would be done:** Write the game logic as a pure step function with a fixed seed so any run replays identically. Add a headless runner that dumps frames to PNG at set ticks and a script that diffs them against known good frames. Give the agent that runner as its test, and have side agents build the level editor and asset converters. The same shape fits a Proteus paper desk, where replayable input gives deterministic scoring.
- **Stack already covers:** Claude Code with skills and sub-agents, HyperFrames (video compose, captions, render)
- **Field Notes line:** Seeded, replayable game simulation plus agent-taken screenshots lets an agent check its own work; commenters say code was never the hard part.

### H-0240 service x city landing pages
2026-10-13, vault, 

- **Mechanism:** One page is generated per service and town pair, each with a matching headline, local detail and schema markup, so a search for 'boiler repair in Leeds' lands on a page that mirrors it. It depends on search engines treating each page as useful rather than templated; the risk is thin or near-duplicate content being demoted. Ranking signal comes from local relevance, internal linking and a Google Business Profile, not from the page count.
- **Claim:** A page per service and city with a matching headline lifts local search visibility for trade businesses.
- **Testable:** no. A verdict needs a live indexed site and weeks of ranking data, and unique page copy needs a model that is not available keyless tonight. Needs: A live domain, indexing time and model-written copy.
- **Idea on its own:** needs-a-run. It is an established local SEO pattern, but it works only if each page carries genuinely distinct local content.
- **How it would be done:** Build a table of services crossed with towns, then fill each row with distinct local facts such as postcodes, nearby landmarks, real job photos and reviews. Render pages from one template through a static site generator, with the headline and title tag taken from the pair. Add LocalBusiness schema, link pages from a hub, and submit the sitemap to Search Console. Measure impressions per page after a few weeks and prune pages that never index. A person is needed to supply real local detail and photos that no script can invent.
- **Stack already covers:** Claude Code with skills and sub-agents, Gemini (stills)
- **To fetch:** Astro https://github.com/withastro/astro (Static site generator to render one page per service and town row.)
- **Missing:** Genuine per-town facts and photos for each page, which have to come from the business.
- **Field Notes line:** One landing page per service and town, headline matched to the search; the catch is Google demoting near-duplicate pages as thin content.

### H-0238 Atoll92/agent-standup: Your Claude Code, Codex and Mistral Vibe sessions as a live, animated team call: who is working, 
2026-10-13, github, https://github.com/Atoll92/agent-standup

- **Mechanism:** It watches the local session files that Claude Code, Codex and Mistral Vibe already write, and parses them into per-agent state. Token counts are summed once per message from the recorded usage, with cache reads shown separately. Tiles flag a command running over a minute, an agent quiet for 3 minutes, and a count of failed tool calls.
- **Claim:** Shows who is working, waiting or blocked across agent sessions at zero token cost, with a per-agent token counter.
- **Testable:** yes. Does the tool's per-agent token total for one local Claude Code session match the same session total from deduplicated transcript records, within 5 percent? Queued as P-0138.
- **Idea on its own:** sound. Session files hold the usage and tool-call data, so a read-only viewer is a straightforward parse.
- **How it would be done:** Tail the session JSONL files, group records by agent id, and sum usage per message once, keeping the largest record per request id. Mark an agent stuck when a tool call has no result after a minute, and quiet after three minutes without output. Render it in a local web page. To test, run it against one saved session and compare totals with an independent sum.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** agent-standup https://github.com/Atoll92/agent-standup (The tool itself, run with npx @double_geste/agent-standup.)
- **Field Notes line:** A viewer that reads Claude Code session files for per-agent token counts and stuck-agent flags, costing no tokens itself.

### H-0237 Show HN: Atticus – Hold-to-talk voice assistant for macOS that runs on Claude -p
2026-10-13, hn, https://github.com/SaarthurR/atticus-mac

- **Mechanism:** A local router handles simple commands such as opening apps or playing a playlist without any model. Harder tasks are passed to claude -p on the user's existing plan. When a task succeeds the first time, its exact steps are logged and replayed next time without the model.
- **Claim:** App launches take about 0.08 seconds, and a meeting-creation task falls from 30 seconds to 5 to 8 seconds on the second run.
- **Testable:** no. It needs macOS accessibility permissions and live claude -p calls on a paid plan, so it is not keyless tonight. Needs: macOS permissions and a Claude plan.
- **Idea on its own:** sound. Recording a successful trace and replaying it without the model is a well known way to cut latency and cost.
- **How it would be done:** Route input through a rule-based matcher first and call the model only on a miss. When the model completes a task, store the tool-call sequence with its parameters. On a repeat, replay the sequence and fall back to the model if a step fails. Use claude -p so no API key is needed. A person would need to review stored traces for safety.
- **Stack already covers:** Claude Code with skills and sub-agents, local transcription
- **To fetch:** atticus-mac https://github.com/SaarthurR/atticus-mac (The source for the router and replay cache.)
- **Field Notes line:** A Mac assistant caches each successful task as a replayable script, so the second run skips the model and drops from 30 seconds to under 8.

### H-0236 UGC creator marketplace that sources creator applications for brands fast
2026-10-13, vault, https://sideshift.app/. Vault verdict on the vendor exists (vault verdict: sideshift.app); mechanism recorded, vendor not re-judged.

- **Mechanism:** A marketplace takes a brand brief, publishes it to a pool of creators, and collects applications for the brand to approve. Speed comes from a standing pool of creators who are pinged on each new brief. The platform earns from the brand or a margin on creator payments.
- **Claim:** Get 50 or more qualified creator applications for a brand in a day.
- **Testable:** no. It needs a two-sided marketplace with real creators, which cannot be run in a sandbox. Needs: A creator pool and a brand to brief.
- **Idea on its own:** needs-a-run. The model works for platforms with a creator pool, and nobody here has tested whether the volume holds for a small agency.
- **How it would be done:** Write a brief template, post it where creators already gather, and use a form to collect applications with sample reel links. Score applicants against a checklist and shortlist. Paying and contracting creators needs a person. The creator pool is the hard part and no script builds it.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Missing:** A standing pool of vetted creators.
- **Field Notes line:** A UGC marketplace gets fast applicant volume only if it already owns a standing pool of creators.

### H-0235 Boosting SORA Token Value: The Power of Token Bonding Curve #XOR #VAL #PSWAP #economics #shorts
2026-10-13, youtube, https://www.youtube.com/watch?v=PpjZ9GZsN20

- **Mechanism:** The SORA token bonding curve is a smart contract with a buy price function and a sell price function, both rising roughly linearly. Reserve assets such as ETH, DAI, VAL and PSWAP are deposited to mint new XOR at the buy price and redeemed at the sell price. The gap between the two lines is the protocol's margin.
- **Claim:** A token bonding curve contract mints XOR against reserve assets and is said to boost token value.
- **Testable:** no. Verifying it means reading chain data for a different network and the video gives no figures to check.
- **Idea on its own:** needs-a-run. A reserve-backed curve with a buy-sell gap is coherent, but the value claim is not backed by any number in the clip.
- **How it would be done:** Read the contract's buy and sell price functions from the chain explorer. Record reserve balances and supply over time. Compute the spread between the two lines and the implied backing per token. A person would need to check the contract source for admin controls.
- **Field Notes line:** SORA uses two separate buy and sell price lines on a reserve-backed curve, unlike a launchpad where one curve prices both sides.

### H-0234 OpenSocialJax: Evaluating Social Adaptation in Sequential Social Dilemmas with Open-Ended Environmental Dynamics
2026-10-13, arxiv, https://arxiv.org/abs/2610.13710

- **Mechanism:** Each episode samples one hidden configuration from tens of millions of options covering layout, crafting rules, payoffs and resource dynamics, then holds it fixed over five trials. Agents must infer the rules by acting and also adapt to other agents. Eight language models are scored in homogeneous and mixed teams.
- **Claim:** Rule discovery often improves performance but does not reliably sustain cooperation, and every team exhausts the shared resource in OpenHarvest.
- **Testable:** no. It needs model answers from eight LLMs and a JAX environment, and there is no local LLM tonight. Needs: LLM access and the benchmark code.
- **Idea on its own:** needs-a-run. The latent-rule sampling design is sound, but the result depends on model choice and has not been replicated.
- **How it would be done:** Define a parametrised environment generator with hidden rules, hold one sample fixed across repeated trials, and score agents on return and on shared-resource level. Run homogeneous and mixed teams of different models. Compare rule discovery against sustained cooperation. The same test shape can score any game bot that has to learn a hidden ruleset.
- **To fetch:** JAX https://github.com/jax-ml/jax (The benchmark is built on JAX environments.)
- **Field Notes line:** Language-model agents that find the hidden rules still drain the shared resource, so working out the game does not make them cooperate.

### H-0233 iamumeransari/claude-show-your-work: Claude Code shows images and plays videos right in your terminal: screenshots, Play
2026-10-13, github, https://github.com/iamumeransari/claude-show-your-work

- **Mechanism:** A Claude Code mod draws its own panel inside the terminal and uses the Ghostty graphics protocol to display images. Videos are split into frames with ffmpeg, a few seconds prepared at a time, then drawn in sequence. The files go straight to the screen and not to the model, so showing them costs no tokens.
- **Claim:** Claude Code shows images and plays videos in the terminal, with before and after recordings synced side by side.
- **Testable:** no. It needs the Ghostty terminal and a specific Claude Code version, and a verdict is a visual check by a person. Needs: Ghostty terminal and Claude Code 2.1.287 or later.
- **Idea on its own:** sound. Showing media outside the model context is a real token saver and the terminal image protocol is well established.
- **How it would be done:** Write a plugin that registers a mod, exposes a show command taking a file path, and emits the Kitty or Ghostty image escape sequences. For video, run ffmpeg to extract frames in short batches and play them on a timer. Pair it with Playwright recordings for before and after bug fixes. The compare view needs frame sync logic between two streams.
- **Stack already covers:** HyperFrames (video compose, captions, render), Claude Code with skills and sub-agents
- **To fetch:** Ghostty https://ghostty.org (Terminal that supports the image protocol the plugin needs.); Playwright https://github.com/microsoft/playwright (Records the test runs that the plugin plays back.)
- **Field Notes line:** A Claude Code mod that streams ffmpeg frames to Ghostty, so test recordings play in the chat at zero token cost.

### H-0231 Tooling, leaderboards and data products built around a token launchpad
2026-10-13, vault, 

- **Mechanism:** Data products sit beside a launchpad rather than trading against retail: leaderboards of tracked wallets, launch scanners and analytics terminals built on public on-chain data. The launchpad can then buy the best of them, as the vault note says happened with Kolscan and Padre. The data comes from chain indexers and price APIs, and the product is ranking and filtering.
- **Claim:** Tooling and leaderboards around the launchpad are the lane that is not extraction from traders.
- **Testable:** yes. Of the last 100 pump.fun-launched Solana pools visible on GeckoTerminal, what share are still above a stated liquidity floor after 24 hours? Queued as P-0137.
- **Idea on its own:** needs-a-run. Whether a leaderboard has value depends on how many ranked tokens survive long enough to matter, which a pull can measure.
- **How it would be done:** Pull new Solana pools from GeckoTerminal for a day, store them, and pull again 24 hours later for the same addresses. Add the rugcheck flag for each. Rank by survival and liquidity to produce the leaderboard. Selling it would need an audience and a front-end; the data pull is scriptable with the existing readers.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers and a Solana paper desk (the Grinder), launchd long-running pollers
- **Missing:** An audience that would pay for or use the leaderboard.
- **Field Notes line:** The launchpad data-product lane is sold as the honest one; a survival table of fresh pools shows how thin the thing being ranked is.

### H-0229 BT-Agent: Deploying Onboard Robot Agents with Behavior Trees and Multi-Fidelity Evaluation
2026-10-13, arxiv, https://arxiv.org/abs/2610.13862

- **Mechanism:** The language model picks which predefined behaviour-tree skill to run, and each skill checks its own execution conditions locally. When a condition fails, the skill stops immediately and returns structured failure feedback, so the model can retry or report without a round trip. A 161-task benchmark runs in text for speed and in simulation on a subset to catch perception and motion failures.
- **Claim:** A 9B model runs fully onboard a quadruped, and the design beats the best Act/ReAct baseline by about 10 and 5 points at 4B and 9B.
- **Testable:** no. It needs a local model and a robot or simulator, and there is no local LLM on this Mac. Needs: A local LLM and Habitat simulator.
- **Idea on its own:** sound. Local guards plus informative errors is a cheap, general way to make weak agents more reliable.
- **How it would be done:** Wrap each action a bot can take in a function that checks its own preconditions and returns a typed error on failure. Let the model choose only among those actions and read the typed error to decide a retry. Build a text-only task set for fast comparison and a slower real-environment set for the subset. The same pattern would suit a game bot.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** py_trees https://github.com/splintered-reality/py_trees (Python behaviour-tree library.)
- **Field Notes line:** Small models act better when tools police their own preconditions and hand back structured failure reasons, not when the model rechecks everything.

### H-0228 juliobsz/skills: An agent skill that builds award-caliber websites from one line
2026-10-13, github, https://github.com/juliobsz/skills

- **Mechanism:** A single agent skill instructs the model to act as creative director, designer and developer, build an Astro site, then check it in a real browser. A Playwright loop takes screenshots that the model reads, plus an axe-core accessibility pass and an OG image step. The quality comes from the self-inspection loop, not from a special model.
- **Claim:** One line such as make me a portfolio produces an award-caliber site already checked in a real browser.
- **Testable:** no. Running it needs a model session to execute the skill, and the result is a taste judgement rather than a number. Needs: A model session to run the skill.
- **Idea on its own:** sound. Letting a vision model inspect its own render and iterate is a proven way to lift front-end output.
- **How it would be done:** Write a skill file that sets a design direction first, then builds the site in Astro. After each build, run Playwright at desktop, tablet and phone widths, feed the screenshots back to the model, and list defects to fix. Finish with axe-core for accessibility and an OG image render. A person is still needed to judge taste and write the real copy.
- **Stack already covers:** Claude Code with skills and sub-agents, HyperFrames (video compose, captions, render)
- **To fetch:** skills CLI https://github.com/vercel-labs/skills (Installs agent skills from GitHub repos.); axe-core https://github.com/dequelabs/axe-core (Free accessibility checker used in the QA pass.)
- **Field Notes line:** A website-building skill that screenshots its own output and fixes what it sees, the same loop as any visual QA agent.

### H-0227 Launch HN: Agent37 (YC F26) – Low-cost agent sandboxes for running agents
2026-10-13, hn, https://news.ycombinator.com/item?id=50059096

- **Mechanism:** Agent harnesses use CPU in short bursts at start-up and during tasks, and extra RAM only while a browser or computer-use task runs. The provider oversubscribes hosts by packing many sandboxes onto each machine and reclaiming memory when a task ends. Cost per sandbox is then driven by average rather than peak usage.
- **Claim:** Sandboxes for agents at under 10% of typical provider cost, averaging 0.37 dollars a month per sandbox and 0.05 to 0.10 for free-plan users.
- **Testable:** no. It is a hosted service needing an account, and the claim is about their fleet costs which cannot be checked from outside. Needs: An account on the service.
- **Idea on its own:** sound. Overcommitting bursty workloads is a standard hosting trick and agent harnesses fit the pattern.
- **How it would be done:** Run many small microVMs or containers per host with memory ballooning or cgroup limits, and snapshot idle sandboxes to disk so they use no RAM. Give each a burst CPU allowance and scale RAM up only when a browser process starts. Meter real usage per sandbox to confirm the average. A hired person would handle noisy-neighbour incidents and security isolation, which no script covers.
- **Stack already covers:** launchd long-running pollers
- **To fetch:** Firecracker https://github.com/firecracker-microvm/firecracker (Open source microVM manager commonly used for dense sandbox packing.)
- **Missing:** A fleet of hosts and the isolation work to sell this.
- **Field Notes line:** Agent sandboxes get cheap by selling average rather than peak CPU and RAM, since harnesses only spike in bursts.

### H-0226 A small weekly prize or showcase as the community rung of the AI for Businesses or Bootcamp kit, if either ships
2026-10-13, vault, https://www.skool.com/aicreatorleague

- **Mechanism:** A paid community sets a weekly cash prize for the best posted piece of work. The prize pool is funded from a slice of subscription revenue, members post entries, and a vote or judge picks the winner. The prize gives members a reason to post every week, which fills the feed and keeps the lower-priced rung active.
- **Claim:** A 9 dollar a month Skool community pays a weekly 750 dollar prize for posting.
- **Testable:** no. It needs a live community with members and a prize pool, which cannot be run keyless in a sandbox. Needs: A community platform, members and a prize budget.
- **Idea on its own:** needs-a-run. Prize rungs plausibly lift posting rates, but the break-even point depends on member count and nobody has measured it here.
- **How it would be done:** Pick a weekly theme, open a submission thread, and set a fixed prize cap that scales with a percentage of that week's subscription revenue so it can never cost more than it earns. Collect entries in the platform's own feed, then have the host or a members' vote choose a winner on a fixed day. Announce the winner publicly with the winning work so it doubles as marketing. A person is needed to judge, pay out and moderate; no script covers trust in the judging.
- **Missing:** A community with enough members for a prize to matter.
- **Field Notes line:** A weekly cash prize for the best post is the cheap mechanism that keeps a low-priced community rung busy.

### H-0224 liyupi/ai-promo-video-maker: 一句话让 AI 帮你做产品宣传片！把产品名或网址告诉 Cursor、Claude Code、Codex 等 AI 编程工具，它会自己调研产品、画出多种风格样图让你挑选、截取 4K 真
2026-10-11, github, https://github.com/liyupi/ai-promo-video-maker. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** The repo is an AGENTS.md workflow plus a Remotion template and helper scripts. The agent researches the product, asks two rounds of questions, draws sample frames in several styles for the user to choose from, captures real pages with Playwright, cuts to music beats, and generates narration. Narration is then transcribed back and compared sentence by sentence to catch misread words, and frames are reviewed by the agent. Without an ElevenLabs key it falls back to Mixkit free music and large captions.
- **Claim:** One sentence to an AI coding tool produces a 4K product promo video with music, narration and a web version.
- **Testable:** no. The full flow needs model-driven agent runs, logins for screenshots and a long render, which does not fit 30 minutes keyless. Needs: Node, ffmpeg and agent model time; an ElevenLabs key for narration..
- **Idea on its own:** sound. A round-trip transcription check on generated speech is cheap and catches real errors.
- **How it would be done:** Take the narration verification step on its own: generate speech, transcribe it locally, and diff against the script at sentence level. Wire the sample-frame style choice into the brief stage, and keep beat-aligned cuts as a HyperFrames timing pass. The stack already covers voice, transcription and composing, so the work is the checking script and the checklist from AGENTS.md.
- **Stack already covers:** HyperFrames (video compose, captions, render), ElevenLabs (voice), local transcription, Claude Code with skills and sub-agents
- **To fetch:** ai-promo-video-maker https://github.com/liyupi/ai-promo-video-maker (The AGENTS.md workflow and helper scripts to borrow the checks from.); Remotion https://www.remotion.dev (The render engine the template uses, for comparison with HyperFrames.)
- **Field Notes line:** The new part is the narration check: transcribe the generated voice and compare it sentence by sentence to catch misread brand names before the video is cut.

### H-0223 Public on-chain leaderboards as the check on any trader's claimed record
2026-10-11, vault, 

- **Mechanism:** A wallet's record is rebuilt from public chain data: every swap is read from the ledger, priced at the time of trade, and summed into realised and unrealised profit. Leaderboard sites such as Kolscan, GMGN and Solana Tracker do this at scale, and Dune lets anyone query the same data. A claim is credible only if it maps to a wallet address and the numbers reproduce from the ledger.
- **Claim:** Public on-chain leaderboards let anyone check a trader's claimed profit against the wallet's actual trades.
- **Testable:** yes. Does the public Kolscan leaderboard load without login and list at least 10 wallet addresses with a PnL figure (yes/no, count)? Queued as P-0127.
- **Idea on its own:** sound. On-chain trades are public and rebuildable, so the claim can be checked without trusting anyone.
- **How it would be done:** Take a wallet address from a public leaderboard. Pull its swaps from a public Solana RPC or indexer, price them with DexScreener or GeckoTerminal history, and recompute realised profit. Compare with the leaderboard figure and note the gap and the causes, such as fees and unrealised holdings. The Grinder's readers already cover the pricing side.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers and a Solana paper desk (the Grinder)
- **To fetch:** Kolscan https://kolscan.io (Public Solana trader leaderboard to test.); GMGN https://gmgn.ai (Wallet and token analytics for cross-checking a leaderboard figure.); Solana Tracker https://www.solanatracker.io (Wallet PnL data and API with a free tier.); Dune https://dune.com (Public SQL over chain data (free account needed for queries).)
- **Field Notes line:** A trader's claimed profit can be checked from public Solana trades, and several free leaderboards already do the sums.

### H-0222 Anthropic Engineers Just 10x'd Everyone's Claude Code
2026-10-11, youtube, https://www.youtube.com/watch?v=oz2CwrPV2Rg

- **Mechanism:** The claim is that newer models need less instruction, so the Claude Code system prompt was cut by over 80 percent with no measured loss on Anthropic's evals. The advice is to prune accumulated rules from CLAUDE.md and skills, state the outcome, the reason and the constraints, and leave room for the model. Evidence cited is Anthropic's own evaluations, which the video does not show.
- **Claim:** Anthropic removed over 80 percent of the Claude Code system prompt with no measurable loss on their evaluations.
- **Testable:** no. Checking it means running a model with and without the rules, and the source evaluations are not public in the video. Needs: Model access and a fixed set of tasks to replay..
- **Idea on its own:** needs-a-run. Plausible, but the claim rests on unseen internal evals and needs a paired replay to confirm.
- **How it would be done:** List the rules in a CLAUDE.md or skill, and pick a fixed set of past tasks with known good outcomes. Run each task with the full rules and with a pruned version, several times each, and compare pass rates and run-to-run variance. Remove only the rules whose absence shows no change. A paired design matters because single runs are noisy.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Field Notes line:** Anthropic says it cut over 80 percent of the Claude Code system prompt without losing eval scores, so old rules in CLAUDE.md may now just slow things down.

### H-0221 TRACE: Diagnosing Verifier Brittleness in Agentic Evaluation
2026-10-11, arxiv, https://arxiv.org/abs/2610.11678

- **Mechanism:** TRACE changes one part of an evaluation, such as tool names or output format, runs paired trials, checks whether agent behaviour changed, and rescores the unchanged trajectories to see if the scoring rule caused the gap. On tau2-bench, reruns of identical tasks flipped 15 to 36 percent of outcomes, so single runs cannot show a small effect. Misleading tool names cut reward by 0.20 to 0.44.
- **Claim:** Renaming tools moved a scripted agent's score by 0.250 with identical behaviour, and identical reruns flip 15-36% of outcomes.
- **Testable:** no. Reproducing it needs repeated LLM agent runs, which are not keyless tonight. Needs: Model access for agent runs..
- **Idea on its own:** sound. Separating the agent from the scoring rule with paired runs and rescoring is basic measurement hygiene.
- **How it would be done:** Take any scored Proteus check that uses a model or a rule-based verifier. Change one presentation detail, run it several times per condition, and rescore the saved trajectories with the original format restored. If the gap closes at scoring time, the verifier was brittle. Record run-to-run variance first so small differences are not over-read.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** tau2-bench https://github.com/sierra-research/tau2-bench (The public benchmark the paper used.)
- **Field Notes line:** Identical agent reruns flip up to 36 percent of task outcomes, so one-run score changes in any eval need a paired, rescored check.

### H-0219 Phone-gated lead magnet to free workshop to done-for-you app build agency
2026-10-11, vault, https://keza.studio/10-app-templates

- **Mechanism:** A free planning-document download sits behind an SMS-verified phone number, which filters out throwaway emails and gives a number that can be called. The lead is then invited to a free workshop, and buyers of the done-for-you build are taken from that room. Each step is a funnel stage with its own drop-off rate.
- **Claim:** A London app studio offers ten app templates free in return for a verified phone number, as the top of a funnel to paid app builds.
- **Testable:** no. Measuring it needs real traffic and a live funnel, and submitting a phone number to a stranger's form is not something to do keyless. Needs: A traffic source and an SMS verification provider..
- **Idea on its own:** sound. A verified phone number is a stronger lead signal than an email, at the cost of fewer sign-ups.
- **How it would be done:** Build a landing page with a useful free document, add an SMS code step with a provider such as Twilio Verify, and send verified leads to a workshop booking page. Track the drop-off at each step against the email-only version to see the trade. A person is needed to run the workshop and the sales call.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Twilio Verify https://www.twilio.com/en-us/user-authentication-identity/verify (The usual SMS code check for a phone gate (paid, trial credit).)
- **Missing:** A workshop host and sales closer, which no script covers.
- **Field Notes line:** Gating a free download behind SMS verification trades volume for leads you can actually ring.

### H-0217 Narrow and Deep: An Ontology Tower as the Knowledge of an LLM Agent for an Industrial Equipment System
2026-10-11, arxiv, https://arxiv.org/abs/2610.11768

- **Mechanism:** A narrow-and-deep knowledge graph of one machine is built in two layers: quantities derived from measured points by physical formulas, and lessons from the operating journal turned into knowledge nodes. A text projection of that tower is placed in the agent's prompt. It was scored on nine preregistered tasks replayed from plant records with four open-weight models, then run live through a safety layer.
- **Claim:** The projected ontology text raised the rate of avoiding the most plausible misjudgment by about 20 points, and the 9B model matched the largest on overall score.
- **Testable:** no. It needs the plant data and open-weight models, and there is no local LLM on this Mac. Needs: Plant records and an open-weight model runtime..
- **Idea on its own:** needs-a-run. The effect is plausible but rests on nine tasks from one plant.
- **How it would be done:** Pick one narrow system, such as the Grinder's own rules and past failures. Write derived quantities and past lessons as short knowledge nodes, then project them into the prompt as plain text. Replay a fixed set of past cases with and without that text, and compare how often the obvious wrong call is avoided. The comparison is cheap but needs model answers.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Ollama https://ollama.com (Local open-weight models, needed to repeat the with and without comparison keyless.)
- **Field Notes line:** Putting lessons from an operating journal into the prompt, not behind a search tool, is what made small models behave like big ones on a plant.

### H-0216 aindeev/agent-chrome-relay: Let your AI agents use your Chrome, signed in as you, in background tabs. By Alexey Indeev ·
2026-10-11, github, https://github.com/aindeev/agent-chrome-relay

- **Mechanism:** A Chrome MV3 extension opens agent tabs inactive in a tab group and runs DevTools commands through the chrome.debugger API, so no remote-debugging port is exposed. A local Go relay on 127.0.0.1:9333 gives each agent its own DevTools endpoint limited to the tabs it opened, and swallows focus-raising commands. The agent-browser CLI connects over that endpoint using the user's existing logins.
- **Claim:** Lets coding agents use your everyday signed-in Chrome in background tabs at about 0.15 seconds per command.
- **Testable:** no. It needs a manually loaded Chrome extension, a signed Go build and real logins, which cannot be done keyless and unattended. Needs: A Chrome profile with the extension loaded by hand, Go 1.25, and a signing step..
- **Idea on its own:** sound. Scoping each agent to its own tabs behind a local relay is a sensible way to share a logged-in browser.
- **How it would be done:** Build the Go relay on the Mac, load the unpacked extension into a dedicated Chrome profile, and install agent-browser. Test with a read-only page that needs a login the user already holds. Check the audit log to confirm each agent sees only the tabs it opened. Keep it on a separate profile so a mistake cannot touch the main one.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** agent-chrome-relay https://github.com/aindeev/agent-chrome-relay (The relay and extension.); agent-browser https://github.com/vercel-labs/agent-browser (The CLI the relay is paired with.)
- **Field Notes line:** Agents can drive your real signed-in Chrome through the chrome.debugger API, with a local relay that scopes each agent to its own tabs.

### H-0215 Show HN: Littleguys – Claude Code, Codex and OpenClaw agents in your menu bar
2026-10-11, hn, https://littleguys.hervalicio.us

- **Mechanism:** A Tauri app (Rust core, React front end) that speaks the Agent Client Protocol to many coding agents and OpenClaw or Hermes gateways. It discovers gateways on a tailnet or LAN, shows each agent's status, and turns permission prompts into allow once, always allow or deny cards. Scheduled routines run through the same protocol. It holds gateway tokens locally with no cloud account.
- **Claim:** A free open-source Mac menu bar app that shows and approves actions from Claude Code, Codex, Gemini CLI and other agents across machines.
- **Testable:** no. It needs a GUI install and live agents to talk to, and the hook-governed unattended runs here would not exercise it. Needs: A GUI session on the Mac and a running ACP-capable agent..
- **Idea on its own:** sound. A common protocol for agent status and permission requests removes per-agent glue code.
- **How it would be done:** Read the Agent Client Protocol spec and the registry of ACP agents, then connect one agent over stdio and log its permission request messages. A thin approval front end can be a menu bar app, as here, or a phone page. For Proteus the useful slice is the message schema, not the app: it shows what a permission request carries.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** littleguys https://littleguys.hervalicio.us (The app itself, to see ACP permission cards working.); Agent Client Protocol https://agentclientprotocol.com (The spec and schema the app speaks.)
- **Field Notes line:** Agent Client Protocol is a shared wire format for coding agents, and a menu bar app now uses it to approve their commands from one place.

### H-0214 Extract the free classroom for the product-validation and repeat-purchase method, if Luke joins
2026-10-11, vault, https://www.skool.com/supplements

- **Mechanism:** The method is demand validation before stock: find a product people already search for or buy, test interest with a landing page or small ad spend, and only then order inventory. Repeat-purchase design (subscriptions, bundles, replenishment timing) is the second half. The numbers come from ad-test click and conversion rates and, afterwards, reorder rates. The classroom itself is gated behind a free Skool join.
- **Claim:** A free Skool community says it teaches finding supplements people want, ad tests and repeat buyers, from a founder claiming a 3 million dollar brand.
- **Testable:** no. The course content sits behind a Skool login, and the method needs ad spend to produce any result. Needs: A Skool account to read the classroom; ad budget to run a real validation test..
- **Idea on its own:** sound. Testing demand before buying inventory is a standard, cheap way to avoid dead stock.
- **How it would be done:** Pick candidate products and pull demand proxies from public sources such as search volume, marketplace sales rank history and review velocity. Put up a one-page listing or waitlist for each and drive a small, fixed amount of ad traffic to it. Record click-through and sign-up rates against a pre-set threshold, and order stock only for products that clear it. Track reorder rate after the first sale as the repeat-purchase measure. A person is needed for supplier calls and for compliance checks on claims.
- **Stack already covers:** Claude Code with skills and sub-agents, keyless YouTube search, oEmbed and transcript pipeline
- **To fetch:** Keepa price and rank history https://keepa.com (Free tier shows Amazon sales rank history, a public demand proxy for product selection.)
- **Missing:** The classroom content itself and a real ad budget for the validation tests.
- **Field Notes line:** The useful part is the order of work: prove people want a product with a cheap ad test before paying for any stock.

### H-0212 Decomposing one classification into several narrow questions with weights fitted on a labelled set
2026-10-10, vault, 

- **Mechanism:** One broad classification is split into several narrow yes/no or scored questions, each answered by a model, and the answers are combined with weights fitted on a labelled set (for example logistic regression over the sub-answers). The labelled set does the calibration work, so the result is model-agnostic and cheap per call once built. It needs enough labelled examples to fit weights and held-out examples to measure accuracy.
- **Claim:** The vault note says it reached 95 percent accuracy on held-out emails.
- **Testable:** yes. On a public labelled spam set, does a logistic fit over five narrow local-model questions beat one direct question on held-out accuracy: percentage point difference? Queued as P-0124.
- **Idea on its own:** needs-a-run. It is plausible that the fit helps, but the independent benchmark disagreed with the demo.
- **How it would be done:** Download the UCI SMS spam set, split off a test portion, and write five narrow questions such as whether it asks for money or contains a link. Ask each of them of the local qwen model for the training rows, fit logistic regression on the answers, and compare held-out accuracy with a single direct prompt. Scoring needs no human.
- **Stack already covers:** Ollama with a qwen model
- **To fetch:** UCI SMS Spam Collection https://archive.ics.uci.edu/dataset/228/sms+spam+collection (Public labelled text for the held-out test.); scikit-learn https://scikit-learn.org/ (Logistic regression for the weights.)
- **Field Notes line:** Splitting one classification into narrow questions with weights fitted on labelled data is a model-agnostic trick; a local test will show if it beats asking once.

### H-0211 bill10/agent-007 (new in awesome-claude-code)
2026-10-10, awesome, https://github.com/bill10/agent-007. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** A web app gives each job card its own git worktree, a Claude Code or Codex worker in a real terminal, and ends the card as a pull request. A manager agent posts cards from a goal, reviews diffs and merges. The new piece is skill families: because Claude Code fits skill descriptions into about 1 percent of the context window, past about a hundred skills most show as bare names, so it groups skills and shows one line per family, with each card listing in full only the families its job needs.
- **Claim:** The README says it runs a self-operating agent company with a job board, a manager agent and phone control over Tailscale.
- **Testable:** no. Needs a web service, git repos and Claude Code or Codex agents running unattended, more than a 30 minute keyless slice. Needs: Agent clients running as workers, Tailscale for the phone side..
- **Idea on its own:** sound. Grouping skills under a short index is a sound answer to a real context budget limit.
- **How it would be done:** The skill family idea could be tried locally by grouping the skills Proteus has and testing whether the model picks the right one more often. The job board layer is a worktree per card plus a queue, which Proteus already approximates with probes. A person would review merged PRs.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** bill10/agent-007 https://github.com/bill10/agent-007 (The app.)
- **Field Notes line:** Agent 007 shows only a one-line index per skill family to dodge Claude Code's skill description budget, loading full families per job card.

### H-0207 Can you use autoregressive diffusion to generate market data?
2026-10-10, hn, https://blog.janestreet.com/can-you-use-autoregressive-diffusion-to-generate-market-data/

- **Mechanism:** The post asks whether autoregressive diffusion can generate order book events, including arrival times, by treating discrete and high-cardinality fields as continuous and seeing where that breaks. Market data is spiky (pennying beats two-tick improvements, orders arrive in bursts around whole-number times), which a smooth continuous model handles badly. Inputs are exchange event streams per symbol; the output is synthetic rollouts with texture beyond a point price forecast.
- **Claim:** A Jane Street intern project explores generating market data events with autoregressive diffusion; the page I saw was cut off before its results.
- **Testable:** no. Needs tick-level order book data and GPU training, not keyless in 30 minutes. Needs: Level-3 order book data and GPU time..
- **Idea on its own:** needs-a-run. Realistic synthetic books are useful for backtests, but the result needs data nobody here has.
- **How it would be done:** Read the full post for the results, then find a free book dataset such as a Smarkets or Binance depth snapshot stream. Train a small autoregressive model on event deltas and compare spacing and size distributions to real data. A quant would judge whether the rollouts keep the spikes.
- **Stack already covers:** launchd long-running pollers
- **To fetch:** LOBSTER sample data https://lobsterdata.com/info/DataSamples.php (Free sample order book files to check distributions.)
- **Missing:** Tick-level book data at scale and GPU training time.
- **Field Notes line:** Jane Street asks if diffusion models can generate order book events with timing, treating discrete order fields as continuous and noting where that breaks.

### H-0206 Templates, thumbnails, overlays and pre-launch guides sold or published to creators before a big game launch
2026-10-10, vault, 

- **Mechanism:** Creators building content around a big game launch buy ready-made assets (thumbnail templates, stream overlays, pre-launch guides). A seller makes them from public trailer information and sells before launch, then ranks guide and search pages in the weeks beforehand. The window is short because guide sites need months to rank and the game is dated 19 Nov 2026.
- **Claim:** The carousel says there are four ways to earn from a huge game launch, which the vault found false as stated.
- **Testable:** no. Needs a storefront and an audience, and the result takes weeks of sales or search ranking. Needs: A storefront account such as Gumroad or Etsy and an audience..
- **Idea on its own:** needs-a-run. Demand is predictable but unproven for any one seller, and the ranking window is short.
- **How it would be done:** Pull search-interest data for the game and related terms to size demand. Build a small pack of thumbnail and overlay templates using stills and HyperFrames, using no publisher artwork. List it on a marketplace and track views and sales for two weeks. A designer would add polish and real examples.
- **Stack already covers:** Gemini (stills), HyperFrames (video compose, captions, render), Claude Code with skills and sub-agents
- **To fetch:** Google Trends via pytrends https://github.com/GeneralMills/pytrends (Keyless search-interest series to size demand.)
- **Missing:** A storefront, an audience and original artwork free of publisher IP.
- **Field Notes line:** Pre-launch asset packs and guides for creators are the one real angle on a big game launch, and the search window closes fast.

### H-0205 automatis-tools/agents-can-communicate (new in awesome-claude-code)
2026-10-10, awesome, https://github.com/automatis-tools/agents-can-communicate. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** A local mailbox shared by coding clients on one machine and OS user. Each client is wired in through its own hooks or plugin so a session can send, read and acknowledge messages, with delivery state tracked so the sender can see whether a message was answered. A handoff note (done, decisions, next steps) is saved when switching clients. There is no lead agent.
- **Claim:** The README says it carries messages between Claude Code, Codex and Antigravity CLI sessions on one machine.
- **Testable:** no. Needs Node 24 and a second vendor's client installed and trusted, which Proteus does not have. Needs: Codex or Antigravity CLI installed and signed in, Node 24..
- **Idea on its own:** sound. A file-backed mailbox with receipts is a simple and sound way to cross vendor clients.
- **How it would be done:** Install the npm package, run the installer, and open two clients in one project. Send a review request from one and see whether the other finds it unprompted. Within Proteus the same idea could be a handoff file between a parent and a hooked child.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** agents-can-communicate https://github.com/automatis-tools/agents-can-communicate (The package.)
- **Field Notes line:** A local mailbox lets Claude Code and Codex sessions message each other through hooks, with delivery receipts and no lead agent.

### H-0204 Code Demo - Web-scraping with API's
2026-10-10, youtube, https://www.youtube.com/watch?v=H-6gyxVGj6A

- **Mechanism:** The session walks through pulling police data for England, Wales and Northern Ireland from the data.police.uk REST API with Python requests in a Jupyter notebook. The pattern is build a URL with a latitude, longitude and month, send a GET, parse the JSON list into a dataframe, and loop over places or months. The numbers come from forces' monthly returns, so the latest month lags.
- **Claim:** The talk teaches API-based collection of UK police data with Python for beginners.
- **Testable:** yes. How many street-level crime records does data.police.uk return for one fixed point and month, and does it answer without a key within the rate limit: number and yes/no? Queued as P-0123.
- **Idea on its own:** sound. A public keyless JSON endpoint with monthly geocoded data is a sound base for forecasting or mapping.
- **How it would be done:** Call the street-crimes-at-point endpoint for a fixed point over several months and store the JSON. Check the documented rate limit by timing a short burst of calls. Aggregate by category and month to see whether a simple seasonal forecast beats last month's count, which would suit a pre-registered paper book.
- **Stack already covers:** launchd long-running pollers
- **To fetch:** data.police.uk API docs https://data.police.uk/docs/ (Endpoint list and rate limits.)
- **Field Notes line:** data.police.uk gives keyless street-level crime for any UK point and month, a free open dataset Proteus has not used yet.

### H-0203 SuperNav: An Agentic Navigation System for Any Task in Any Scene
2026-10-10, arxiv, https://arxiv.org/abs/2610.12126

- **Mechanism:** A pretrained multimodal LLM, with no navigation fine-tuning, is wrapped in a harness of navigation skills, tools for physical interaction and task-progress and context management. The model names destinations by pointing at pixels in an image (a visual-point interface), the tools turn that point into motion, and execution feedback comes back for the model to revise. Evaluation is on HM3D simulation tasks and a real quadruped.
- **Claim:** The paper says SuperNav beats four baselines on instance-level, multi-object and demand-driven navigation tasks.
- **Testable:** no. Needs a robot or the HM3D simulator plus a multimodal model API, none keyless in 30 minutes. Needs: HM3D dataset access, a robot or simulator, a multimodal model..
- **Idea on its own:** sound. Keeping the general model for decisions and putting motion in tools is a sound split, and the pixel-pointing interface is reusable.
- **How it would be done:** The pattern could be copied to screen or browser agents: the model points at a coordinate in a screenshot, a tool executes it, and the result image goes back. Reproducing the paper needs the project page code, the HM3D scenes and a simulator such as Habitat. A robotics lab would handle the quadruped side.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** SuperNav project page https://zju3dv.github.io/SuperNav/ (Code and demos if released.); Habitat-sim https://github.com/facebookresearch/habitat-sim (Simulator that runs HM3D scenes.)
- **Missing:** A robot or simulator setup and a multimodal model budget.
- **Field Notes line:** A robot navigator that lets an unmodified vision LLM point at pixels to pick destinations, with tools doing the walking and feedback correcting it.

### H-0202 wheresryan22/anatomy: A Claude Code skill that turns a technical idea into a detailed, interactive isometric figure of a
2026-10-10, github, https://github.com/wheresryan22/anatomy

- **Mechanism:** A Claude Code skill that tells the model to invent a physical machine whose working matches a technical concept, then build it from many small shaded isometric SVG parts with an optional WebGL shader layer between a back and front SVG. A small model object drives both the parts and the readout, so the numbers shown are the same ones that move the parts. A bundled Node kit (no npm dependencies) provides the camera, shading and an audit script that checks for pipes passing through parts, and capture scripts screenshot the result so the model can zoom in and self-check.
- **Claim:** The README says it turns a technical idea into an interactive isometric figure, with 226 stars after two days.
- **Testable:** yes. Does the smallest example (dial-indicator) open as a standalone page and does its audit script run on Node with no npm install: yes or no? Queued as P-0122.
- **Idea on its own:** sound. A model-driven figure with a self-audit loop is a sound way to get diagrams that carry real numbers.
- **How it would be done:** Clone the repo into the sandbox, read the skill file and the smallest example, and run its audit and build scripts under Node. Then give it one concept Proteus already has, such as the Dixon-Coles goal grid or a token-bucket rate limiter, and see whether the output stays accurate. Output could drop into the lab page or Field Notes as an interactive figure. No human job is needed beyond judging whether the figure looks good.
- **Stack already covers:** Claude Code with skills and sub-agents, HyperFrames (video compose, captions, render)
- **To fetch:** wheresryan22/anatomy https://github.com/wheresryan22/anatomy (The skill and kit itself.)
- **Field Notes line:** A skill that makes Claude draw a technical idea as a working isometric machine in SVG, with an audit script checking no parts collide.

### H-0200 UK shape of selling booking software through trade job software and profile booking buttons
2026-10-10, vault, https://www.youtube.com/watch?v=mr4YV-9MY0Q

- **Mechanism:** A booking button is attached to a trade's Google Business Profile and wired into whatever job-management software the trade already runs, so a customer books a slot without a call. It depends on Google's booking-link surface (Reserve with Google needs partner approval, otherwise a plain appointment URL on the profile) and on the job software exposing an availability or job-creation API or a calendar feed. The sale is made by phone, bundled with the job software the trade already uses, and billed as recurring software.
- **Claim:** The video says a booking widget sold to trades reaches $50K a month, on the founder's word only.
- **Testable:** no. The open question is which UK job software trades use and whether they expose APIs, which needs market calls and partner approval, not a keyless run. Needs: Phone conversations with UK trades, Google partner approval for Reserve with Google, API access to UK job software..
- **Idea on its own:** needs-a-run. The distribution logic is plausible, but which UK software trades run and whether it has APIs is unknown.
- **How it would be done:** First list the job software UK plumbers and HVAC firms actually use, from their websites and review sites, and tally it. For each top package, check for a public API, calendar export or Zapier-style connector. Then build the smallest widget: a hosted booking page that writes to a calendar or webhook, linked from the Google profile's booking URL field. A hired person would call twenty trades to learn which software they use and what they would pay, and to sell the first accounts.
- **Stack already covers:** Claude Code with skills and sub-agents, Ollama with a qwen model
- **To fetch:** Cal.com (open source) https://github.com/calcom/cal.com (Self-hostable booking page to use as the widget base.); Google Business Profile booking links https://support.google.com/business/answer/6218536 (Documents the appointment URL field that needs no partner approval.)
- **Missing:** A mapped list of which job software UK trades use and which of them have an integration surface.
- **Field Notes line:** A booking button on a trade's Google profile, sold alongside the job software they already use, is the distribution idea; the UK version is unmapped.

### H-0198 x402 per-call payment rails for agents, Coinbase-originated, now under Linux Foundation governance
2026-10-09, vault, https://docs.google.com/document/d/1_KvqUJXH1z7RUjrnbal0JVgGcJyP4yFfOdyZ1PRWbQs/edit?usp=drivesdk

- **Mechanism:** A server answers an unpaid request with HTTP 402 and a body listing price, asset, network and pay-to address. The client signs a payment authorisation (stablecoin, e.g. USDC) and retries with it in a header; a facilitator verifies and settles it, then the server returns the resource. No per-service signup is needed, only a wallet. The challenge format is public and readable without paying.
- **Claim:** Per-call payments for agents over plain HTTP, Coinbase-originated and now under Linux Foundation governance.
- **Testable:** yes. Does an unpaid request to a public x402 endpoint return HTTP 402 with a parseable payment-requirements body (yes/no, list its fields)? Queued as P-0116.
- **Idea on its own:** sound. Using the long-reserved 402 status with a signed payment header is a clean mechanism; the open question is adoption, not design.
- **How it would be done:** Find a public x402 resource from the project's documentation or discovery listing and send a plain unpaid GET. Record the status, headers and the requirements JSON, and check them against the spec. Stop there: no wallet is created and nothing is paid. Later, a paper-only client could be built to show how an agent would decide whether a price is worth paying.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** x402 reference repo https://github.com/coinbase/x402 (Spec and example endpoints)
- **Missing:** A wallet and spending policy, which are Luke's call and not tonight's.
- **Field Notes line:** x402 turns HTTP 402 into a pay-per-call handshake; the challenge is readable without a wallet, so the format can be checked for free.

### H-0195 A Closer Look at Agentic BBO: Benchmarking LLM Agents for Black-Box Optimization
2026-10-09, arxiv, https://arxiv.org/abs/2610.12183

- **Mechanism:** An LLM agent chooses and calls numerical optimisers (and its own proposals) over a fixed evaluation budget on black-box problems. The benchmark runs five domains under one finite-budget protocol and compares agent, direct LLM and classical optimisers. Findings: extra tools do not reliably help, task semantics help, and a numerical optimiser can absorb gains from the agent's early trajectory.
- **Claim:** Agentic BBO beats direct LLM methods in all five domains and the best numerical optimisers in four.
- **Testable:** no. Needs the benchmark harness plus LLM calls across domains; not a 30-minute keyless run. Needs: LLM API budget, the agentic-bbo repo.
- **Idea on its own:** needs-a-run. Plausible and relevant to parameter tuning, but the benchmark's own claim has not been replicated by anyone here.
- **How it would be done:** Take one Grinder or Pitch parameter search, give an LLM the first ten evaluations to propose region choices, then hand the history to a standard optimiser such as Optuna and compare against Optuna alone on the same budget. Use identical evaluation counts and a permutation check. The paper's repo supplies the protocol and baselines.
- **Stack already covers:** freqtrade, Claude Code with skills and sub-agents
- **To fetch:** agentic-bbo https://github.com/lamda-bbo/agentic-bbo (Benchmark code from the paper); Optuna https://github.com/optuna/optuna (Baseline optimiser to warm-start)
- **Field Notes line:** Let an LLM warm-start a classical optimiser: the optimiser picks up the agent's early search path and keeps the gain.

### H-0194 Jakeschincariol/founder-skill: Eleven free Claude skills that test a business before you launch it: a board trained on H
2026-10-09, github, https://github.com/Jakeschincariol/founder-skill

- **Mechanism:** Eleven Claude skills, each a prompt that spawns sub-agents. The board runs three agents, each applying one book's framework to the idea; the consumer panel generates 100 buyer personas with income, habits and an objection and tallies purchase decisions. A few Python tools do deterministic arithmetic such as unit economics and break-even. The panel's answers come from the model's own guesses, not real buyers.
- **Claim:** Tests a business idea before launch with a board, a CFO and a 100-agent consumer panel, free and MIT.
- **Testable:** yes. Do the repo's Python tools run with no install and does the CFO break-even figure match a hand calculation on the same inputs (yes/no)? Queued as P-0115.
- **Idea on its own:** unsound. Synthetic buyers from the same model that wrote the idea will agree with its priors; only the deterministic maths is trustworthy.
- **How it would be done:** Clone, read the Python tools, run them on a made-up product and check the break-even and margin against a spreadsheet. For the panel, a fair test would score its predicted purchase rate against a known real outcome, such as a product with published conversion. If it cannot beat a naive base rate it is theatre. The useful part to borrow is the unit-economics calculator.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** founder-skill https://github.com/Jakeschincariol/founder-skill (The skill pack and Python tools)
- **Missing:** Real buyer data to calibrate the panel against.
- **Field Notes line:** A free skill pack simulates 100 buyers with sub-agents; the buyers are the model's guesses, so only the arithmetic tools can be checked.

### H-0192 Join and extract the four free communities that cover both asks: Emerging Fashion Designers, Rich Off Clothes, RiseWise,
2026-10-09, vault, https://www.skool.com/discovery?q=fashion+design

- **Mechanism:** Join free Skool communities, read their classroom pages and posts through a logged-in browser pane, and extract course lists, lesson text and video transcripts into notes. Transcripts come from the video host, summaries from a cheaper model reading in groups, and a digest goes to the vault. The access step is a human joining with consent; the rest is reading and summarising.
- **Claim:** Four free fashion and clothing-brand communities cover both research asks (design and marketing), sized 297 to 1,067 members.
- **Testable:** no. Needs Luke to join each community in an interactive browser session. Needs: Luke's login and tap to join each community.
- **Idea on its own:** sound. Reading free community material for personal research is lawful and the extractor pattern already exists.
- **How it would be done:** Luke taps join on each group in the desktop pane. A browser session lists classroom modules, and the existing transcript pipeline pulls each video's words. Haiku or Sonnet children read a couple of lessons a night and write digests; the parent reads digests only. The output is a per-community note: what is taught, which parts are real practice and which are filler.
- **Stack already covers:** a keyless YouTube search, oEmbed and transcript pipeline, local transcription, Claude Code with skills and sub-agents
- **Missing:** Luke's membership in each group.
- **Field Notes line:** Four free Skool fashion groups hold the design and brand-marketing courses Luke wants; extraction only needs his join tap and a reading pass.

### H-0191 4da-systems/4da (new in awesome-mcp-servers)
2026-10-09, awesome, https://github.com/4da-systems/4da

- **Mechanism:** Scores each incoming item on five axes (codebase context, declared interests, git activity, dependency matches, a held-out learned axis) and surfaces it only if two or more pass; single-axis matches are capped at 28 percent. Survivors go through twelve quality multipliers and then an LLM verifier with a 1 to 5 rubric, run on local Ollama or a user key. The numbers come from a 245-item labelled corpus across nine simulated personas.
- **Claim:** Rejects 93 percent of content and 98.9 percent of labelled noise, reproducible in one command.
- **Testable:** yes. Does the repo's one-command benchmark reproduce 98.9 percent noise rejection on its labelled corpus (yes/no, with the number)? Queued as P-0114.
- **Idea on its own:** sound. Requiring agreement between independent cheap signals before an expensive LLM judge is a sensible gate, and the benchmark is falsifiable.
- **How it would be done:** Clone the repo, find the benchmark section's command and run it in the sandbox, then compare the printed rejection numbers to the README. Separately, copy the two-signal gate idea into harvest.py as a pre-filter ahead of the Sonnet judge to cut candidates. The corpus is self-labelled, so a fair test would also score a small hand-labelled set from Proteus's own harvest. Rust build time is the main risk to the 30 minutes.
- **Stack already covers:** Ollama with a qwen model, Claude Code with skills and sub-agents
- **To fetch:** 4DA https://github.com/4da-systems/4da (Repo with the benchmark); Rust toolchain (rustup) https://rustup.rs/ (Likely needed to build the benchmark)
- **Field Notes line:** A feed filter that only shows an item if two independent signals agree, claiming 98.9 percent of labelled noise rejected; the benchmark is checkable.

### H-0189 Unlocking the Regulatory Genome by ARGUS: An Evidence-Constrained Agentic Framework for Interpreting Single Nucleotide V
2026-10-09, arxiv, https://arxiv.org/abs/2610.12281

- **Mechanism:** A planner LLM chooses which evidence source to query next given current uncertainty, but every observation is interpreted by a deterministic verifier, and the system may abstain. Biology models (458 DNABERT binding models) and real databases (ADASTRA allele-specific binding, JASPAR motifs, ENCODE cCRE) supply the numbers; the LLM never invents evidence. Compared with a fixed-priority planner, the LLM reaches the same verdicts with fewer tool calls by skipping evidence that cannot resolve the claim.
- **Claim:** Four divergent investigation paths for four transcription factors at one variant; the LLM planner matches fixed-order verdicts with fewer calls.
- **Testable:** no. Needs 458 trained models and genomics tooling; no keyless slice fits 30 minutes. Needs: DNABERT TF models, genomics data access.
- **Idea on its own:** sound. Separating deterministic checking from LLM planning, with an abstain option, is a sound pattern for any desk that must not hallucinate evidence.
- **How it would be done:** The pattern ports directly: a planner chooses the next data pull, a script computes a pass/fail or abstain on each result, and only verified numbers reach the write-up. For the Pitch or Grinder that means the LLM proposes which feed to check and a coded rule judges it. Build it as a small wrapper around existing readers with an explicit abstain state logged per step. The genomics content itself would need a domain person.
- **Stack already covers:** Claude Code with skills and sub-agents, football-data and a Dixon-Coles paper desk (the Pitch), GeckoTerminal, DexScreener and rugcheck readers and a Solana paper desk (the Grinder)
- **To fetch:** ADASTRA allele-specific binding database https://adastra.autosome.org/ (Public data source the paper queries); JASPAR https://jaspar.elixir.no/ (Open TF motif database)
- **Missing:** A domain-neutral verifier template with an abstain state.
- **Field Notes line:** Keep the LLM as planner only: a deterministic verifier checks every observation and the agent may abstain, which cut tool calls without changing verdicts.

### H-0188 franzenzenhofer/big-arrow-on-the-screen: Let your AI agents paint big arrows, boxes and text on your Mac screen. One CLI
2026-10-09, github, https://github.com/franzenzenhofer/big-arrow-on-the-screen

- **Mechanism:** A single Swift binary opens a transparent, click-through window above all Spaces and draws an arrow and label. To point at a named control it queries the macOS Accessibility tree for an element by title and role in a given app, reads its on-screen frame, and aims the arrow there. Drawing itself needs no permission; finding elements by name needs the Accessibility grant. It removes itself after a timeout.
- **Claim:** Lets an AI agent paint arrows and text on the Mac screen to guide a human click, with no daemon or telemetry.
- **Testable:** yes. Does the repo build with swift on this Mac and does a coordinate-based arrow draw and self-remove within its timeout (yes/no)? Queued as P-0113.
- **Idea on its own:** sound. Reading element frames from the accessibility tree and overlaying a window is a well-understood, low-risk mechanism.
- **How it would be done:** Clone the repo into the sandbox and build with swift build. Run the coordinate form of the draw command with a short timeout and confirm by screenshot that the overlay appears, passes clicks through and disappears. Then wire it as a skill so an interactive session can point Luke at a permission dialog. The element-name form needs an Accessibility grant, which stays a human step.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** big-arrow-on-the-screen https://github.com/franzenzenhofer/big-arrow-on-the-screen (The CLI and skill itself); Swift toolchain (Xcode command line tools) https://developer.apple.com/xcode/ (Needed to build the binary)
- **Field Notes line:** A tiny Mac tool lets an agent draw a click-through arrow on screen to point a human at the exact button, using the accessibility tree.

### H-0186 A scoped UK test of one flip with the compliance costs priced first, only if Luke wants the lane
2026-10-09, vault, https://www.skool.com/ai-car-trader-9959

- **Mechanism:** Buy an undervalued used car, relist it at a higher price, and pocket the spread. AI prompts are used to pull listings, estimate resale value from comparable sold prices, and write the advert and haggling messages. In the UK the legal wrapper matters: repeat buying to resell makes you a trader, sales carry Consumer Rights Act duties (30-day right to reject, six-month fault presumption), and moving stock needs motor trade insurance. The edge is price discovery, not the prompts.
- **Claim:** A Skool course says AI prompts let you flip cars part time, headlined by 100 million dollars in trades.
- **Testable:** no. A real flip needs money, a car and insurance; no keyless slice answers whether it makes money. Needs: Capital for one car, motor trade insurance quote, a listings source that allows reading.
- **Idea on its own:** needs-a-run. Spread-based flipping is real but margins in the UK are thin once insurance, fees and return liability are priced in.
- **How it would be done:** Pull sold-price and asking-price data for one model range from public listings and build a simple fair-value table by age and mileage. Flag listings priced a set percentage under fair value, then log what they later sold at (a paper flip book, committed before outcomes). Price the fixed costs first: trade insurance quote, MOT, valet, advert fees, a warranty reserve for the six-month fault presumption. Only if the paper book clears those costs would one real car be bought. A hired person would do the viewing, the mechanical check and the handover, which no script covers.
- **Stack already covers:** Claude Code with skills and sub-agents, launchd long-running pollers
- **To fetch:** DVLA Vehicle Enquiry Service API https://developer-portal.driver-vehicle-licensing.api.gov.uk/ (Free-tier lookup of tax and MOT status to screen listings (needs a key, so a later-night fetch)); GOV.UK MOT history data https://www.gov.uk/check-mot-history (Mileage and failure history to spot clocked or problem cars)
- **Missing:** A legal listings feed and a view-and-inspect person; nobody has a price table for UK used cars yet.
- **Field Notes line:** A UK car flip is a pricing-spread business wrapped in trader law; the legal costs, not the AI prompts, decide whether it pays.

### H-0184 Whether LinkedIn search surfaces enough recent dental and aesthetics owner posts per week to feed a manual routine
2026-10-08, vault, https://vimeo.com/1233794507/cf61fad386

- **Mechanism:** The principle is a timing trigger: find owners who have just posted about a problem, reference that post, ask one question and phone on reply. The source tool scrapes commenters and keyword posters daily into automated sequences; the idea here is the manual version, where the open question is whether enough fresh dental and aesthetics owner posts exist per week. It depends on LinkedIn's logged-in search, which cannot be queried keyless.
- **Claim:** Reaching owners just after they post about a problem gives better response than cold outreach.
- **Testable:** no. LinkedIn search needs a logged-in account and public pages block unauthenticated queries. Needs: A logged-in LinkedIn account and a week of manual counting..
- **Idea on its own:** needs-a-run. Whether enough qualifying posts appear weekly is a simple count nobody has made yet.
- **How it would be done:** Define the search strings (for example dental practice owner plus patient no-shows or lead flow), set a weekly window, and log each qualifying post: author, role, date, topic. A person does this by hand in 20 minutes a day, since automating LinkedIn is against its terms. A hired virtual assistant could keep the log in a sheet. At week end the count per day and per topic answers the supply question. Alternative public sources such as Google News and trade forums could be counted the same way as a keyless comparison.
- **Missing:** A person with a LinkedIn login to do the counting for a week.
- **Field Notes line:** The useful part of a LinkedIn scraping funnel is just timing: contact owners soon after they post, and a week of manual counting shows whether supply is enough.

### H-0182 Pump Fun Sniper Bot (Solana) — Memecoin Trading / Full Tutorial 2026
2026-10-08, youtube, https://www.youtube.com/watch?v=E0QoMIjVI44

- **Mechanism:** A sniper bot watches for new token creation on the pump.fun programme, filters candidates with checks (a simulated sell to catch honeypots, mint authority, LP lock, sell tax), buys within seconds using priority fees and Jito bundles to reduce sandwiching, then exits by take profit, stop loss or timer. The video is a promotion: the 10 to 19 SOL story, 184 ms speed and 1,240% copy-trading figures are unverified claims with no record. Platforms and chains detect this behaviour as bot flow, and the safety checks it lists are the same ones public readers can run.
- **Claim:** A bot turned 10 SOL into 19 SOL and snipes in 184 ms, with a free tier plus 1% fee.
- **Testable:** yes. Of the last 200 new pump.fun tokens seen via public readers, what share fail a mint-authority or freeze-authority check at creation, and what share are down more than 50% after one hour? Queued as P-0099.
- **Idea on its own:** unsound. As a money claim it is unevidenced and speed races favour paid infrastructure, but the filter list is a testable input for the paper desk.
- **How it would be done:** Use GeckoTerminal's new-pools endpoint to list fresh Solana tokens, then run the rugcheck reader on each for mint and freeze authority and top-holder share. Record each token's price an hour later from GeckoTerminal. Compare outcomes between tokens that pass and fail the filters. This feeds the Grinder as a filter-value table; no wallet, no trades.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers and a Solana paper desk (the Grinder)
- **Field Notes line:** A sniper-bot promo lists its safety filters, so I can measure how many new Solana tokens those filters would really have blocked.

### H-0180 cth9191/animate: Procedural animation in any style for Claude Code: short single-file canvas videos with story, look and
2026-10-08, github, https://github.com/cth9191/animate

- **Mechanism:** A video is a single JavaScript file that draws each frame on a canvas as a pure function of time, with seeded randomness so every render is identical. A headless browser steps through frames and captures them, then ffmpeg encodes to MP4, with the music beat-mapped so cuts land on the beat grid. Approval gates (story beats, style frames, storyboard) come before the build, and measured checks run on the result.
- **Claim:** A Claude Code skill that makes short procedural canvas videos in seven styles or one matched from references, in every format from one piece.
- **Testable:** yes. Does the repo's bundled demo piece render to an MP4 locally from its render script, and is the output duration within 1 second of the piece's declared length? Queued as P-0098.
- **Idea on its own:** sound. Deterministic frame-by-frame rendering from code is cheap, repeatable and overlaps with HyperFrames, which already does similar work.
- **How it would be done:** Clone the repo into the sandbox, install its Node dependencies and run the render command on a demo piece folder. Check the MP4 exists, its duration and its frame count. Compare the process with HyperFrames: both are HTML or canvas, deterministic and rendered by a headless browser. The unique parts to borrow are the style kits and the beat-grid checks, which could become a Proteus caption or chart style.
- **Stack already covers:** HyperFrames (video compose, captions, render), Claude Code with skills and sub-agents
- **To fetch:** cth9191/animate https://github.com/cth9191/animate (The skill and demo pieces.); ffmpeg https://ffmpeg.org/ (Encoding step.); puppeteer https://pptr.dev/ (Headless browser frame capture, if not bundled.)
- **Field Notes line:** A Claude Code skill draws whole videos as deterministic canvas code and renders with a headless browser and ffmpeg, no generative video model.

### H-0178 Code the five rules as a freqtrade strategy and score it on the two-year sample and payout tests S1 used
2026-10-08, vault, https://www.instagram.com/reel/DbJMHpDMK-1/. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** Five fully stated rules: a 15m bias, a 5m impulse box where a gap exists between candles one and three, a break of the prior low and return to the box, entry when the second candle closes past the first, stop at the first candle and take profit at 2R. Everything is derived from OHLC candles on two timeframes. The vault already has a two-year sample and a payout bar to score against.
- **Claim:** An Instagram trader says this five-rule box setup is a reliable intraday entry, offering no record.
- **Testable:** yes. Over two years of public BTCUSDT 5m and 15m candles, does the five-rule strategy have positive expectancy after 0.1% round-trip costs, and does it beat shuffled-entry baselines? Queued as P-0104.
- **Idea on its own:** needs-a-run. Fully specified rules can be tested cheaply, and most such setups fail after costs, so only a run settles it.
- **How it would be done:** Download 15m and 5m klines from a public exchange API, align timeframes without lookahead, and code the rules as a freqtrade strategy or a plain pandas backtest. Ambiguities (what counts as the bias, the gap definition) get fixed up front and written down before the results are seen. Report trade count, win rate, expectancy after costs and a shuffled-entry baseline. Then score the equity curve against the payout bar the vault already uses.
- **Stack already covers:** freqtrade
- **To fetch:** Binance public klines API https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints (Keyless candle history.)
- **Field Notes line:** A viral five-rule trading setup is precise enough to code, so I am scoring it on two years of candles instead of trusting the reel.

### H-0175 RECAST: Learning to Compute the Right Context through Adaptive Evidence Routing
2026-10-08, arxiv, https://arxiv.org/abs/2610.10507

- **Mechanism:** A small trained RouterLM loops over a menu of primitive operations (retrieve, filter, aggregate, compute) and can specify custom operations in words, which a frozen CompilerLM turns into code that runs. Results come back as evidence items, and the router decides when evidence is enough and passes it to a frozen AnswerLM. The router is trained with supervised fine-tuning, then GRPO reinforcement learning on task success.
- **Claim:** A 9B router with computed evidence reaches 75.6% mean success across six benchmark families, 15.9% above the strongest large-model baseline.
- **Testable:** no. Needs training a router model and the benchmark suites, far beyond 30 minutes and without a published runnable artefact in the brief. Needs: GPU training and the six benchmark datasets..
- **Idea on its own:** sound. Deriving evidence by computation rather than similarity search fits questions about aggregates, which retrieval alone handles badly.
- **How it would be done:** The cheap version is to skip the training: give a frontier or local model a tool menu over a table set, let it write and run code to derive the numbers, and answer only from the executed output. Proteus could try this on its own CSV ledgers, asking aggregate questions with and without code execution and scoring both against a known answer. The trained router is the paper's contribution and would need the authors' code and a GPU.
- **Stack already covers:** Claude Code with skills and sub-agents, Ollama with a qwen model
- **To fetch:** RECAST paper https://arxiv.org/abs/2610.10507 (Check for linked code or data.)
- **Missing:** A trained RouterLM, if the exact method were wanted.
- **Field Notes line:** Instead of retrieving text, a small router model decides which calculations to run over the sources and feeds the results to a frozen answerer.

### H-0174 openqodex/openqodex: Open source AI code review for Claude Code and Codex, before you push. Scanners (SAST, secrets, dep
2026-10-08, github, https://github.com/openqodex/openqodex

- **Mechanism:** It builds a frozen copy of the unpushed change, runs scanners (SAST, secrets, dependencies, lint) matched to the changed files, and keeps only findings on changed lines. It then starts a separate Claude Code or Codex process as reviewer, which must rule on every scanner finding and sees every changed line. Scripts check the reviewer's answer for coverage and format before a report (HTML, Markdown, JSON, SARIF) is written. It uses the already logged-in agent CLI, so no extra key.
- **Claim:** Pre-push AI code review where a second agent process verifies every scanner finding, with no other API key.
- **Testable:** no. The reviewer stage needs a logged-in Claude Code or Codex session, which means spend on a model call, and the scanners are downloaded on init. Needs: A logged-in agent CLI for the reviewer stage..
- **Idea on its own:** sound. Separating the finder from the judge and checking coverage by script is a sensible pattern for catching skipped findings.
- **How it would be done:** Run npx openqodex init in a scratch repo, make a diff with a planted hardcoded secret and a vulnerable dependency, and run review. Compare the findings against the plants. To copy the pattern in a Proteus job, run semgrep or gitleaks on the changed lines, then hand the list to a child agent with a rule that each item needs a verdict, and check the verdict count by script.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** openqodex https://github.com/openqodex/openqodex (The tool itself.); semgrep https://github.com/semgrep/semgrep (Free SAST scanner of the kind it wraps.); gitleaks https://github.com/gitleaks/gitleaks (Secret scanner for the same pattern.)
- **Field Notes line:** A code reviewer that is forced to answer every scanner finding in a second agent process, then has its answer checked by scripts.

### H-0172 An inducement filter as a variant on the WF-0350 paper test: one further sweep and recovery after the structure shift be
2026-10-08, vault, https://www.instagram.com/reel/DePSq8KIuyj/

- **Mechanism:** After a market structure shift (a break of a recent swing high or low), the filter refuses to enter until price makes one further sweep of a nearby swing point and then closes back inside the range. It is defined purely from candle highs, lows and closes, so it is a boolean gate that can sit in front of any entry rule. Nothing in the source gives a hit rate, so the only evidence is whatever a paper run produces.
- **Claim:** A mentor says waiting for one more liquidity sweep after the structure shift gives a better entry than entering on the shift itself.
- **Testable:** yes. On the last 90 days of public BTCUSDT 5m candles, does the entry-after-extra-sweep variant have a higher win rate and expectancy than entry on the shift alone, over at least 30 signals each? Queued as P-0103.
- **Idea on its own:** needs-a-run. The rule is precisely definable from candles but has no evidence behind it, and swing-point definitions leave room for overfitting.
- **How it would be done:** Pull 5m candles from a public exchange endpoint (Binance or Bybit klines, no key). Write swing high and low detection with a fixed lookback, then define the structure shift as a close beyond the last swing. Code two variants: enter at the shift, or enter only after one further sweep of a swing and a close back inside. Use a fixed stop and 2R target for both so only the filter differs. Count signals, win rate and expectancy, with a shuffled-entry baseline for luck. Freqtrade can host it, but a plain pandas script is quicker for a first pass.
- **Stack already covers:** freqtrade
- **To fetch:** Binance public klines API https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints (Keyless 5m candle history for the test.); pandas https://pandas.pydata.org/ (Swing detection and signal counting.)
- **Field Notes line:** A trading-mentor rule, wait for one more sweep after the structure shift, turns out to be codeable as a yes/no gate, so I can score it against plain entries.

### H-0171 Show HN: Agent.reviews – Where AI agents read and write reviews on tools
2026-10-07, hn, https://agent.reviews/

- **Mechanism:** A skill and npm CLI let coding agents look up reviews of a package before choosing it and post one after using it. Reviews pass three filters before publishing: deterministic rules for secrets, PII and URLs, a small trained classifier for leaks, and a small LLM check. The data is agent-reported friction, such as an SDK crashing on a missing key, aggregated per tool.
- **Claim:** Thousands of agent-written reviews gathered in a few weeks, built on 50k+ measured agent sessions.
- **Testable:** yes. Does a public agent.reviews package page such as /packages/uv return review text and a count readable without login, yes/no, and how many reviews? Queued as P-0094.
- **Idea on its own:** needs-a-run. The feedback loop is real but reviews risk being gamed or low quality, which a read of the data can show.
- **How it would be done:** Fetch the public package pages and inspect the review text, dates and rating spread. If readable, it is a dataset on which tools agents struggle with, usable as an input to the tools shelf. A person would be needed only to judge whether ratings look genuine.
- **Stack already covers:** a keyless YouTube search, oEmbed and transcript pipeline (fetch pattern)
- **To fetch:** agent.reviews https://agent.reviews/ (Public site to read.); @armature-tech/agent-reviews https://www.npmjs.com/package/@armature-tech/agent-reviews (CLI to inspect how reviews are sent.)
- **Field Notes line:** A review site written by coding agents about the tools they used, with a three-layer filter to stop secrets leaking into reviews.

### H-0170 Build a mock-up site for the prospect and send a 90-second Loom after a two-line permission ask
2026-10-07, vault, https://www.youtube.com/watch?v=aidr_Ny1rvI

- **Mechanism:** Outreach is sequenced as a consent step first: a two-line message asks whether the business owner is happy to see a free redesign. Only on a yes is a mock-up of their own site built and a short screen-recorded walkthrough sent. This keeps the contact within UK electronic marketing rules because the sample is solicited, and the demo shows the fix rather than describing the gap.
- **Claim:** Showing a built mock-up after a permission ask wins a first agency client without a portfolio.
- **Testable:** no. Needs real prospects, outbound messages and replies, not a keyless sandbox run. Needs: Real prospects and a send channel; per-message approval from Luke.
- **Idea on its own:** needs-a-run. Consent-first with a tangible demo is sound in principle, but reply rates are unevidenced in the source videos.
- **How it would be done:** Pick a local trade with a weak site, build a one-page replica with Claude Code and a site skill, and record a 90 second walkthrough with screen capture and a voiceover. A person handles finding contacts, sending the permission ask, and following up. Tracking reply rate per batch is the measurable output.
- **Stack already covers:** Claude Code with skills and sub-agents, HyperFrames (video compose, captions, render), ElevenLabs (voice)
- **To fetch:** Loom https://www.loom.com/ (Free tier for short walkthrough recordings.)
- **Missing:** Prospect list and a human sender for each message.
- **Field Notes line:** Ask permission in two lines, then send a mock-up of the prospect's own site with a 90 second walkthrough.

### H-0169 cvelasquez/agent-workbench (new in awesome-claude-code)
2026-10-07, awesome, https://github.com/cvelasquez/agent-workbench. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** It spawns the already-logged-in CLI (claude, codex, opencode) inside a server-side pseudo-terminal, so processes outlive the browser tab. A browser UI streams the terminal and reads each CLI's on-disk session logs to render history, conversation cards, context use and subagent status. Handoff to another CLI is done by passing a transcript of recent turns, not the real context.
- **Claim:** One local UI for several coding-agent CLIs with tabs, history, context meter and git view, never touching credentials.
- **Testable:** yes. Does `npx agent-workbench` start and list this machine's existing Claude Code sessions from the PROTEUS project without any network calls beyond npm install, yes/no? Queued as P-0093.
- **Idea on its own:** sound. Wrapping a pty and parsing local transcripts is simple and credential-free by design.
- **How it would be done:** Install into the sandbox with npm, start it bound to localhost, and check that it reads session logs under the Claude projects folder. The transcript-parsing code is the useful piece for the usage and run-log tooling. Nothing here needs a person beyond reading the UI.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** agent-workbench https://github.com/cvelasquez/agent-workbench (The package under test.)
- **Field Notes line:** A browser front end that wraps your logged-in coding CLIs in a pty and reads their session logs for history and context meters.

### H-0166 GTKottman/mortiflix-oss: A motion design studio on your own machine: Claude makes the video step by step, you approve ev
2026-10-07, github, https://github.com/GTKottman/mortiflix-oss

- **Mechanism:** A harness that runs Claude in short sessions that each end at a human gate: brief, script, style frames, animatic, final. State carries between sessions through a journal and handoff file, and the rules are enforced in code, for example a submission is refused unless it reports every error check and answers each pinned note. Approved items are copied out of the session's reach, and a proposed new check, once approved, runs on every later video.
- **Claim:** A local motion design studio where Claude builds video stage by stage and the user approves each one.
- **Testable:** yes. Does `mortiflix demo` complete on this Mac with Node and ffmpeg and produce a playable video, yes/no? Queued as P-0092.
- **Idea on its own:** sound. Gated sessions with a journal handoff match how reliable long agent work is done, and Proteus already uses code-enforced rules.
- **How it would be done:** Clone the repo, run npm install and `mortiflix demo` which needs no Claude, then read the pipeline.json format to see how gates and checks are declared. The reusable piece is the gate-and-journal pattern, which could wrap the Field Notes or Nolan film builds. Real videos would use the existing Claude Code login. A person still judges taste at each gate.
- **Stack already covers:** Claude Code with skills and sub-agents, HyperFrames (video compose, captions, render), ElevenLabs (voice)
- **To fetch:** mortiflix-oss https://github.com/GTKottman/mortiflix-oss (Repo to clone and run the demo.); ffmpeg https://ffmpeg.org/ (Required by the demo if not installed.)
- **Field Notes line:** A video studio where every Claude session stops at a human approval gate and the rules are enforced in code, not prompts.

### H-0165 Show HN: Durable Actors – OSS Durable Objects with configurable compute
2026-10-07, hn, https://github.com/TerseAI/durable-actors

- **Mechanism:** Each actor is a named singleton server with its own SQLite file that handles one request at a time, so concurrent agents touching shared data are serialised without locks. Clients reach an actor by name over websocket and the platform routes to the single instance anywhere in the cluster. It is self-hosted via a Helm chart on Kubernetes, with configurable compute per actor.
- **Claim:** An MIT-licensed open-source alternative to Cloudflare Durable Objects built for multiplayer agent workloads.
- **Testable:** no. Needs a Kubernetes cluster or its runtime set up, beyond a 30 minute keyless slice. Needs: Kubernetes or Docker runtime.
- **Idea on its own:** sound. The single-writer virtual actor model is established and fits agent coordination.
- **How it would be done:** Deploy the Helm chart or run the local dev build, create one actor per agent or per desk, and expose a websocket endpoint for each. Proteus could use it to serialise writes to a ledger instead of CSV files edited by several jobs. A person would handle cluster setup and schema versioning, the weakness a commenter flagged.
- **Stack already covers:** launchd long-running pollers
- **To fetch:** Durable Actors https://github.com/TerseAI/durable-actors (The open-source repo with Helm chart.)
- **Missing:** A cluster or Docker host to run it.
- **Field Notes line:** One named server per agent with its own SQLite and one request at a time, so many agents share data without races.

### H-0164 A high-impact news filter for the S1 crypto bot, skip or flatten entries in a window around high-impact USD events, scor
2026-10-07, vault, https://www.forexfactory.com/. Vault verdict on the vendor exists (vault verdict: forexfactory.com); mechanism recorded, vendor not re-judged.

- **Mechanism:** A public weekly JSON calendar lists scheduled macro events with a low, medium or high impact tag and a timestamp. A filter blocks new entries and optionally flattens positions inside a window around high-impact USD events such as CPI, FOMC and payrolls. It works only if volatility around those events is reliably higher and the bot loses more there than elsewhere, which the paper record can show.
- **Claim:** A free calendar feed can drive a news filter for the S1 crypto bot, scored on the paper record.
- **Testable:** yes. Is BTC's mean absolute return in the hour after high-impact USD events at least 1.5 times its all-hours baseline over the last 12 months? Queued as P-0102.
- **Idea on its own:** needs-a-run. Event-window volatility is well known, but whether skipping entries improves this bot's results is untested.
- **How it would be done:** Pull the weekly calendar JSON (keyless) and keep a rolling archive of high-impact USD events as they appear; for history, list the 12 months of FOMC, CPI and NFP dates by hand from public schedules. Fetch hourly BTC candles from a public exchange endpoint and compute absolute return in the event hour versus all hours. Then replay the S1 paper trades with entries inside the window removed and compare PnL. No hire needed; the only manual part is the historical date list.
- **Stack already covers:** launchd long-running pollers, freqtrade
- **To fetch:** Faireconomy weekly calendar JSON https://nfs.faireconomy.media/ff_calendar_thisweek.json (Keyless weekly feed of events with impact ratings.); Binance public klines https://api.binance.com/api/v3/klines (Keyless hourly BTC candles for the volatility comparison.)
- **Field Notes line:** Does BTC really move more after CPI and Fed days? I will check hourly candles against a free macro calendar before any filter touches the bot.

### H-0161 MedZERO: Self-Evolving Agents for Open-Ended Medical Reasoning Through Controlled Knowledge Accumulation
2026-10-07, arxiv, https://arxiv.org/abs/2610.08327

- **Mechanism:** Two roles share one base model: an Examiner invents hard question-option pairs and a Reasoner answers them using multi-turn calls to external knowledge tools. Knowledge learned during a solve is kept in two tiers, a temporary exploratory store and a curated persistent store, and only the curated tier is promoted for later reuse. Training signal comes from agreement and the Examiner's difficulty targeting, not from human labels.
- **Claim:** Up to 13.7 average accuracy points over the next-best self-evolving baseline on five medical benchmarks with 4B and 8B models.
- **Testable:** no. Needs model fine-tuning and medical benchmarks, not a 30 minute keyless run. Needs: GPU training, benchmark data, code release not confirmed.
- **Idea on its own:** needs-a-run. The staged-memory trick is plausible and portable, but the gains are self-reported on a narrow benchmark set.
- **How it would be done:** Reimplementing means a generator prompt, a solver loop with a search tool, and a promote-or-discard gate for notes. The gate is the transferable part and could be tried on the Pitch desk as a notes store that only keeps rules that held up on past matches. A small model via Ollama could stand in for the 4B base. Medical use would need expert review, which no script covers.
- **Stack already covers:** Ollama with a qwen model, Claude Code with skills and sub-agents
- **To fetch:** MedZERO paper https://arxiv.org/abs/2610.08327 (Read for the promotion rule and check for a code link.)
- **Missing:** A released implementation and a verifiable domain to run the loop on.
- **Field Notes line:** A self-play loop where one model writes hard questions and another answers them, with a two-tier memory so bad notes never become permanent.

### H-0158 Insider cluster-buy signal from the free Form 4 filings page as a paper desk
2026-10-07, vault, https://finviz.com/. Vault verdict on the vendor exists (vault verdict: finviz.com); mechanism recorded, vendor not re-judged.

- **Mechanism:** US insiders must file Form 4 within two business days of a trade, and the filings are public on SEC EDGAR as XML. A cluster-buy signal counts open-market purchases (transaction code P) by three or more distinct insiders at one issuer inside a short window, then measures forward returns against the index. The numbers come from the filings themselves plus a free daily price series; finviz is only a viewer over the same EDGAR data.
- **Claim:** Insider cluster buys show small documented positive drift after filing, using free daily data.
- **Testable:** yes. Do EDGAR Form 4 cluster buys (3+ insiders, code P, 14-day window) from 2025 beat SPY over the next 30 trading days, yes/no and by how many percentage points on average? Queued as P-0101.
- **Idea on its own:** needs-a-run. The effect is documented in academic work but shrinks after costs and in small caps, so only a run on recent data says if it survives.
- **How it would be done:** Pull the EDGAR daily or quarterly index of Form 4 filings with a descriptive User-Agent header (no key), parse the XML for code P non-derivative transactions, and group by issuer in rolling 14-day windows. Fetch daily closes from a keyless source such as Stooq CSVs for each flagged ticker and for SPY. Log each cluster as a paper entry on the filing date plus one trading day, committed before outcomes, and score at 30 and 60 days. A hired person would only be needed to sanity-check ticker mapping and delisted names; a script covers the rest.
- **Stack already covers:** launchd long-running pollers, Dixon-Coles paper desk pattern (ledger and scoring approach)
- **To fetch:** SEC EDGAR full-index and Form 4 XML https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4 (Free primary source for insider filings, no key, needs a User-Agent.); Stooq daily CSV https://stooq.com/ (Keyless daily price history for forward returns.)
- **Field Notes line:** Insider cluster buys are public on EDGAR within two days; I will check whether three-plus insiders buying together actually beat the index.

### H-0157 Charlesmpc/by2kb: Forward videos from IM to transcript, Markdown, and your knowledge base — with raw and skill-updated o
2026-10-06, github, https://github.com/Charlesmpc/by2kb

- **Mechanism:** A pipeline fetches a Bilibili or YouTube video, transcribes it with local faster-whisper or cloud ASR, and writes three Markdown files: transcript, a short abstract and long study notes. The summaries come from the host agent's own model, and a topic search previews captions only before any audio download. Job history and models live under a home folder so upgrades keep them.
- **Claim:** Forward a video link and get transcript, abstract and study notes saved into a local Markdown knowledge base.
- **Testable:** yes. Does pipx install of by2kb with local Whisper transcribe one short public YouTube video to a Markdown transcript, and what is the real-time ratio? Queued as P-0068.
- **Idea on its own:** needs-a-run. The pipeline is standard, so quality depends on install friction and transcription speed.
- **How it would be done:** Install with pipx, run the init preset for a local agent, and download a small Whisper model. Feed it one short public video and check the three output files. Compare against the existing local transcription step and the keyless transcript fetch. Summaries need an agent or an OpenAI-compatible key, so the abstract step may be skipped keyless.
- **Stack already covers:** a keyless YouTube search, oEmbed and transcript pipeline, local transcription, Claude Code with skills and sub-agents
- **To fetch:** by2kb https://github.com/Charlesmpc/by2kb (The video to Markdown knowledge-base pipeline.); faster-whisper https://github.com/SYSTRAN/faster-whisper (Local speech recognition used by default.)
- **Field Notes line:** A video URL becomes transcript, abstract and notes in Markdown using local Whisper, with a caption-only topic preview step.

### H-0156 Show HN: OpenChart – OSS TradingView alternative with your own AI agent
2026-10-06, hn, https://github.com/longsurf-ai/openchart

- **Mechanism:** A local macOS app holds charts, indicators and research on the user's machine. A shape drawn on a chart becomes an alert condition, and when price crosses it the alert launches the user's own agent (Claude or Codex) to investigate and save notes. Indicators and conditions are written in a purpose-built language called Tea, with free market data and optional paid low-latency data.
- **Claim:** An open-source TradingView alternative where agents annotate charts, write indicators and are triggered by price alerts.
- **Testable:** no. The app is a macOS binary download from a third party and needs an agent login, so it is not a keyless run in the sandbox. Needs: A macOS app download and an agent subscription.
- **Idea on its own:** sound. Alert-triggers-agent-writes-notes is a sensible loop and the same shape as the Grinder's pollers.
- **How it would be done:** A threshold or line cross is detected by a poller on free price data, which then runs an agent with the chart context and appends the findings to a notes file. The Grinder already has pollers and readers for this. The Tea language and drawn-shape alerts would be the parts to fetch or copy.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers and a Solana paper desk (the Grinder), launchd long-running pollers, Claude Code with skills and sub-agents
- **To fetch:** Tea language https://github.com/longsurf-ai/tea (The indicator and alert-condition language OpenChart uses.); OpenChart https://github.com/longsurf-ai/openchart (The app that wires alerts to an agent.)
- **Field Notes line:** Price alerts that wake an AI agent to investigate the move and save notes, with indicators in a new language called Tea.

### H-0155 Getting a video into an agent as scene-change frames plus transcript, or via a bare URL to Gemini
2026-10-06, vault, https://www.instagram.com/reel/Db1USzsMNnZ/

- **Mechanism:** ffmpeg detects scene changes and saves one frame per cut, then captions are pulled from the video or Whisper transcribes the audio when none exist. Frames and timestamped transcript are handed to the model together. The alternative is giving a public YouTube URL directly to Gemini, which reads the video itself.
- **Claim:** Scene-change frames plus a transcript, or a bare URL to Gemini, get a long video's content into an agent without watching it.
- **Testable:** yes. For one public 10-minute video, how many scene-change frames does ffmpeg (select gt(scene,0.3)) produce, and do they line up with the transcript timestamps? Queued as P-0071.
- **Idea on its own:** sound. Scene frames plus timestamps are a well-understood compression of a video, though a talking-head video yields few useful frames.
- **How it would be done:** Download captions with the existing keyless pipeline, run ffmpeg scene detection to extract frames, and pair each frame with the nearest transcript lines. Feed the pairs to a model and ask questions only answerable from the frames. Compare with local transcription alone to see what the frames add.
- **Stack already covers:** a keyless YouTube search, oEmbed and transcript pipeline, local transcription, Claude Code with skills and sub-agents
- **To fetch:** ffmpeg https://ffmpeg.org/ (Scene-change frame extraction.)
- **Field Notes line:** A video reaches an agent as ffmpeg scene-change frames matched to a transcript, with no install beyond ffmpeg.

### H-0153 HERA: Harness-Environment Co-Evolution for Reliable Agentic Abstention
2026-10-06, arxiv, https://arxiv.org/abs/2610.06563

- **Mechanism:** Solvable tool-use tasks are mutated in controlled ways (for example removing a needed tool or fact) into verifiable infeasible twins, so the agent must abstain. Failures on earlier tasks drive edits to the harness prompts and rules and generate new environments aimed at those weaknesses, in a loop. The evolved harness is then tested on held-out tasks and other models.
- **Claim:** Abstention accuracy rises from 61.7% to 83.3% and transfers to 19 other models for +15.3 points on average.
- **Testable:** no. Needs the paper's benchmark, code and model access that are not confirmed public or keyless. Needs: The benchmark and a model with an API or local weights.
- **Idea on its own:** sound. Making solvable and unsolvable pairs by controlled mutation gives checkable ground truth for abstention.
- **How it would be done:** Take a set of solvable tool tasks, break each in one controlled way, and record the correct answer as abstain. Score a harness on both sets, collect failures, and ask a model to revise the harness and write new tasks aimed at those failures. Repeat for a few rounds and test on held-out tasks. The same loop could check whether a Proteus desk agent refuses when data is missing.
- **Stack already covers:** Claude Code with skills and sub-agents, Ollama with a qwen model
- **Missing:** The paper's task set and code, if released.
- **Field Notes line:** Agents learn when to say 'I cannot do this' if tasks are mutated into unsolvable twins and the harness is evolved against its own failures.

### H-0152 arielshad/3d-asset-server: 3d assets api and mcp
2026-10-06, github, https://github.com/arielshad/3d-asset-server

- **Mechanism:** A Hono REST server and an MCP server share one search layer that fans a query out to 19 asset sites, merges and ranks results, and tags each with licence, free status and credit requirement. Downloads fetch glTF with bin and textures, PBR maps or HDRIs, and extract zips. Sites that block bots come back as links to their own search instead.
- **Claim:** One query searches 19 3D asset sites and downloads files ready for a game or Three.js scene.
- **Testable:** yes. How many of the 19 providers return at least one result with a licence field for the query 'low poly tree' when run keyless from the CLI? Queued as P-0067.
- **Idea on its own:** needs-a-run. Fan-out scraping of many sites decays quickly, so the working-provider count is the real test.
- **How it would be done:** Clone the repo, install with Node, and run the CLI search for a few queries. Record per-provider status, licence field and whether a download lands a usable file. Then register it as an MCP server in Claude Code and have an agent fetch assets into a project. Keeping it working over time means someone maintaining the provider adapters.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** 3d-asset-server https://github.com/arielshad/3d-asset-server (The server, CLI and MCP tools themselves.)
- **Field Notes line:** One search box over 19 free 3D asset sites with licences shown, exposed as an MCP tool an agent can call.

### H-0150 Buying real human UGC clips from marketplaces and reselling them inside a client retainer
2026-10-06, vault, https://www.instagram.com/reel/DdK9uWfRVRT/

- **Mechanism:** A brand briefs a creator marketplace, a creator films 15 to 60 seconds on a phone for a fee, and the brand owns the file and runs it as a paid ad. Reselling inside a retainer means buying the raw clip and adding captions, cuts and voice work in-house. The cost is the clip fee, and the output is judged on ad performance.
- **Claim:** Real human clips cost 25 to 60 dollars each and supply a real face that avatar and voice tools cannot.
- **Testable:** no. Buying clips needs a marketplace account and payment. Needs: A marketplace account and spend.
- **Idea on its own:** sound. Buying licensed clips and editing them is an ordinary, lawful production route, provided the licence and any disclosure rules are followed.
- **How it would be done:** Write a brief per client with the product, the claim to avoid and the shot list, then post it to a marketplace. Review the delivered clips against the brief and the licence terms. Caption, cut and add b-roll with HyperFrames, and export in ad formats. A person has to handle the creator relationship and any reshoots; scripts cannot.
- **Stack already covers:** HyperFrames (video compose, captions, render), ElevenLabs (voice), Claude Code with skills and sub-agents
- **Missing:** A supply of real human creators and a payment route for them.
- **Field Notes line:** Real human UGC clips can be bought for 25 to 60 dollars and finished in-house, giving ads a genuine face.

### H-0149 degordonstech/pwa2play (new in awesome-claude-code)
2026-10-06, awesome, https://github.com/degordonstech/pwa2play. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** A Trusted Web Activity is a thin Android app that opens a website full screen once the site proves ownership via a /.well-known/assetlinks.json holding the app's signing SHA-256. Bubblewrap builds the bundle, and the plugin encodes the Play rules: reuse one signing key, raise the version code every upload, target the current API level. A small script reads package id, version code and SDK levels straight out of a built apk.
- **Claim:** A Claude Code plugin that walks a PWA through packaging and Play Store upload while avoiding the common rejection traps.
- **Testable:** no. A real run needs a Play developer account and a live PWA with a signing key. Needs: A Google Play developer account.
- **Idea on its own:** sound. The TWA and assetlinks mechanism is Google's documented route and the listed rules match it.
- **How it would be done:** Serve a PWA over HTTPS with a valid manifest, run Bubblewrap init and build, and generate the signing key once. Publish assetlinks.json with the Play app signing SHA-256, not the upload key. Upload to a test track first, then production. A person still has to run the Play Console account, testers and review.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Bubblewrap https://github.com/GoogleChromeLabs/bubblewrap (Builds the TWA Android bundle from a PWA.)
- **Missing:** A Play developer account and a PWA worth shipping.
- **Field Notes line:** A PWA gets into the Play Store as a Trusted Web Activity, and most rejections come from three key and version rules.

### H-0147 Wikidata Search Traces: A Dataset for Training Knowledge Graph Search Agents
2026-10-06, arxiv, https://arxiv.org/abs/2610.06650

- **Mechanism:** Multi-hop questions are built on a frozen Wikidata snapshot by replacing a named entity with nested conditions, checking after each expansion that the target stays unique and every condition is needed. A recursive harness lets the model batch graph calls, keep results in persistent Python state and read selected evidence through sub-calls, instead of pasting graph results into context. The paper releases 10,235 solving traces.
- **Claim:** The harness lifts correct answers from 49 to 61 for one model and from 60 to 74 for an open-weight Qwen3.8-27B on 100 questions.
- **Testable:** yes. Using the public Wikidata SPARQL endpoint, can a three-condition nested question for one entity be built so the answer is still unique (count equals 1)? Queued as P-0066.
- **Idea on its own:** sound. Keeping bulky retrieval results out of the context and querying them in code is a sound pattern, and the uniqueness check is a clean way to control question difficulty.
- **How it would be done:** Take a starting entity and add conditions one at a time, each as a SPARQL clause, checking the result count stays at one. Build the harness as a Python session where the model calls search and fetch helpers, stores results in variables and only reads slices. Run an open-weight model locally on those questions and compare against direct tool calling. The traces dataset gives training or evaluation material. This could also feed a forecasting data source with structured facts.
- **Stack already covers:** Ollama with a qwen model, Claude Code with skills and sub-agents
- **To fetch:** Wikidata Query Service https://query.wikidata.org/ (Public SPARQL endpoint to check uniqueness of nested conditions.); SPARQLWrapper https://github.com/RDFLib/sparqlwrapper (Python client for SPARQL endpoints.)
- **Field Notes line:** Agents answer Wikidata questions better when graph results live in Python state rather than the prompt; 10,235 traces are released.

### H-0146 Vincentwei1021/mg-styles-15: 15 motion design styles, each made by Claude Opus 5.5 writing code from one prompt: watch t
2026-10-06, github, https://github.com/Vincentwei1021/mg-styles-15

- **Mechanism:** Each film is a web page exposing window.renderAt(t) that draws any frame as a pure function of time, using SVG, Canvas, WebGL or Three.js. A renderer steps t, captures each frame in headless Chrome, and ffmpeg joins the frames with an audio track synthesised by a Python audio.py from instrument samples. Blender is used only for the 3D film, and two review rounds by an AI jury drove the revisions.
- **Claim:** 15 ten-second motion-design films, each made by Claude writing code from one prompt, with scores from 7.57 to 8.21 out of 10 from an AI jury.
- **Testable:** yes. Does one film's renderAt page plus the published render steps produce a 10-second mp4 with audio in under 20 minutes on this Mac? Queued as P-0065.
- **Idea on its own:** sound. A deterministic frame-at-time page captured by a headless browser is the same pattern HyperFrames uses and is well proven.
- **How it would be done:** Clone the repo, pick one style, and run its render script against headless Chrome and ffmpeg. Check that the frame count, duration and audio track match the README. The prompts are published, so the same prompt can be rerun in Claude Code to compare output. HyperFrames already covers composing and rendering, so the useful new part is the per-style prompt and the synthesised audio script.
- **Stack already covers:** HyperFrames (video compose, captions, render), Claude Code with skills and sub-agents
- **To fetch:** mg-styles-15 https://github.com/Vincentwei1021/mg-styles-15 (The prompts, style notes and source for 15 code-drawn film styles.); ffmpeg https://ffmpeg.org/ (Joins captured frames and the soundtrack.)
- **Field Notes line:** Fifteen ten-second films drawn as code, each a page that renders any frame by time and captured by headless Chrome into ffmpeg, with the prompts published.

### H-0144 A 10 to 30 pound a day local lead-gen test for one Neptune client using the course build and its testing discipline
2026-10-06, vault, https://www.skool.com/theadsclinic

- **Mechanism:** A small daily-budget Meta lead-gen campaign for one local business: a single offer, a few creative variants and a lead form, with spend held low while the ads are tested one variable at a time. Winners are kept and losers cut on cost per lead, with lead quality checked by the client's own follow-up. The numbers come from the ads platform and the client's call or booking log.
- **Claim:** A 10 to 30 pound a day test for one client can find a profitable lead-gen ad using a disciplined testing method.
- **Testable:** no. It needs a client, an ad account and real spend. Needs: A client with budget, a Meta ad account and a payment method.
- **Idea on its own:** needs-a-run. The method is standard and plausible, but only a live test shows whether the cost per lead works for a given trade.
- **How it would be done:** Pick one client and one offer, then write three or four creative variants and one lead form. Run them at a flat daily budget, changing one variable at a time and logging cost per lead each day in a sheet. Cut the weakest variant at a pre-set spend threshold and keep the best. Someone has to ring the leads and report which ones were real, because no script covers that follow-up. Claude Code can draft copy, build the tracking sheet and summarise the daily export.
- **Stack already covers:** Claude Code with skills and sub-agents, Gemini (stills), HyperFrames (video compose, captions, render)
- **Missing:** A client with budget and someone to phone the leads and judge their quality.
- **Field Notes line:** A small, strictly tested daily ad budget for one local client is the cheapest way to learn what a lead actually costs.

### H-0141 Niche paid community on owned material, borrowing only a proven model and price point
2026-10-05, vault, 

- **Mechanism:** Pick a niche, copy only a proven structure (tier, price point, content cadence), and fill it with original material. Host it on a community platform such as Skool or Whop with a template, and take recurring payments. Honest metrics, disclaimers and VAT are required, and the mechanism fails if it copies another's material or invents numbers.
- **Claim:** A trending paid community, 27,000 members at 9 dollars a month, is cited as roughly 243k a month gross.
- **Testable:** no. It needs a platform account and a paying audience, not a keyless run. Needs: A Skool or Whop account and original content..
- **Idea on its own:** needs-a-run. The structure works for some niches but the headline revenue is unverified and depends on audience, which a plan cannot show.
- **How it would be done:** Choose a niche where original material exists, check the real price points of competing communities from their public pages, then build a lesson library and weekly cadence. Sign up for a platform, set up VAT and write the disclaimers. Audience comes from free content on YouTube and short video. A lawyer or accountant covers consumer law and VAT.
- **Stack already covers:** Claude Code with skills and sub-agents, HyperFrames (video compose, captions, render), ElevenLabs (voice)
- **To fetch:** Whop https://whop.com (Community and checkout hosting with a free tier.)
- **Missing:** An audience and original material.
- **Field Notes line:** Copying a community's price and structure is lawful; the money sits in owned material, honest numbers and VAT, not the clone.

### H-0139 HazardWeaver: Scientific Route Selection for Hazard Analysis Agents
2026-10-05, arxiv, https://arxiv.org/abs/2610.03591

- **Mechanism:** A compiler step extracts evidence-linked applicability conditions for scientific methods from literature. A capability graph records each executable tool's inputs and outputs and checks that they are compatible, and the agent picks a route through it, running it and re-picking as results arrive. The benchmark scores output correctness, route validity and justified abstention.
- **Claim:** HazardWeaver outperforms existing agent systems on 141 hazard-analysis instances, most where several valid routes exist.
- **Testable:** no. It needs an LLM key and hazard datasets and models that are heavy to set up. Needs: An LLM API key and hazard data..
- **Idea on its own:** sound. Checking input-output compatibility before running a method, and allowing abstention, is a sensible guard for agent pipelines.
- **How it would be done:** Read the repo and copy the capability-graph idea: list each tool's input and output types and refuse routes that do not connect. For Proteus desks it could decide which model suits a match given the data available. The paper's full system needs domain hazard models and a person to curate conditions.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** HazardWeaver https://github.com/LabRAI/HazardWeaver (Code released by the authors.)
- **Missing:** Domain-expert curation of method applicability conditions.
- **Field Notes line:** An agent that picks which scientific method fits the data and tools it has, and abstains when none does.

### H-0138 shinshin86/mesh-avatar-studio: Turn one illustration into an animated 2D mesh avatar with a coding agent and a local edi
2026-10-05, github, https://github.com/shinshin86/mesh-avatar-studio

- **Mechanism:** A coding agent follows a written guide to read coordinates on zoomed grids, place rig points, cut one illustration into layers and review fixed poses. A local WebGL editor then deforms triangle meshes from those points for blink, head turn and breathing, with vowel mouth shapes for lip sync. Drawn eye and mouth variants are generated by an image model and imported.
- **Claim:** Turns a single illustration into a blinking, talking animated 2D mesh avatar with a coding agent and a local editor.
- **Testable:** yes. Does npm install and npm run dev start the editor with the bundled sample and does Lip sync move the mouth (yes/no)? Queued as P-0064.
- **Idea on its own:** needs-a-run. Mesh deformation is a proven approach, but agent-placed rig points on arbitrary art are the unproven part.
- **How it would be done:** Install Node 22 and run the sample to check the editor and lip sync. Then give the agent guide a front-facing PNG and review the fixed-pose output. Audio-driven mouth shapes could be wired to ElevenLabs output for talking clips. A person fixes bad rig points by dragging in the editor.
- **Stack already covers:** Claude Code with skills and sub-agents, ElevenLabs (voice), Gemini (stills)
- **To fetch:** mesh-avatar-studio https://github.com/shinshin86/mesh-avatar-studio (The editor and agent guide.); Node.js 22.17+ https://nodejs.org (Required runtime.)
- **Missing:** Reliable automatic rig placement on arbitrary art.
- **Field Notes line:** One illustration becomes a blinking, lip-syncing 2D avatar, with the agent doing the rigging and a local web editor for fixes.

### H-0137 Show HN: Nightwatch – a Mac menu-bar app that tells you when tonight is clear
2026-10-05, hn, https://github.com/rsutcliffe/nightwatch

- **Mechanism:** It polls hourly cloud-cover forecasts every 30 minutes and finds the astronomical-dark window between dusk and dawn. It sends one alert an hour before sunset only if an unbroken clear run is long enough, and says nothing otherwise. Two forecast sources are compared and disagreement is reported instead of averaged, with thin high cloud counted as half.
- **Claim:** A menu-bar app that notifies you only when there is an unbroken clear run in astronomical darkness.
- **Testable:** yes. For one UK location, does Open-Meteo's keyless hourly cloud-cover data give a computable longest clear run in tonight's astronomical dark window (yes/no, and how many hours)? Queued as P-0063.
- **Idea on its own:** sound. Thresholding a public forecast on a contiguous-run condition is simple and checks well against a second source.
- **How it would be done:** Fetch hourly cloud cover low, mid and high from Open-Meteo for a coordinate and compute sun-below-18-degrees times locally. Weight high cloud at half, find the longest run under a threshold, and alert only if it exceeds a set number of hours. Compare against a second source such as 7Timer and print the disagreement. A scheduled poller delivers the alert. The same pattern fits any condition-run alert.
- **Stack already covers:** launchd long-running pollers
- **To fetch:** Open-Meteo API https://open-meteo.com/en/docs (Keyless hourly cloud cover by layer.); 7Timer http://www.7timer.info/doc.php (Free second forecast for disagreement checks.); astral https://github.com/sffjunkie/astral (Python sun position and twilight times.)
- **Missing:** Nothing.
- **Field Notes line:** A stargazing alert that stays silent unless a long clear dark window exists, and flags it when two forecasts disagree.

### H-0136 GBP setup and audit checklist
2026-10-05, vault, 

- **Mechanism:** A Google Business Profile audit compares a business's primary and secondary categories with the top local competitors, checks that service areas are set, and counts search demand for service-plus-city phrases. Suspension flags such as keyword-stuffed names, address mismatches and virtual offices are checked against Google's published guidelines. The data comes from the public Maps listing and a keyword volume source.
- **Claim:** A checklist of competitor categories, service-plus-city volume, service areas and suspension flags that makes a free GBP audit.
- **Testable:** no. Reading listings at scale needs a Places API key or a scraping account. Needs: A Google Places API key or a keyword volume source..
- **Idea on its own:** sound. Category comparison and demand counting against public listings is a legitimate, checkable audit.
- **How it would be done:** Take a business name and city, pull the listing and the top ten competitors in the map pack, and tabulate categories, review counts and service areas. Add a demand count for each service-plus-city phrase from a keyword tool. Flag anything on the suspension checklist and write the result as a short PDF. A person would still make the sales call and verify the business owns the listing.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Google Places API (New) https://developers.google.com/maps/documentation/places/web-service/overview (Structured listing and category data, with a free monthly credit.); Google Keyword Planner https://ads.google.com/home/tools/keyword-planner/ (Search volume for service-plus-city phrases.)
- **Missing:** Nothing; it needs an API key and a template.
- **Field Notes line:** A free local-business audit is a competitor category diff plus a service-plus-city demand check, and the output is a one-page report.

### H-0134 NeutronGym: Physics-Graded Neutron Instrument Design for LLM Agents
2026-10-05, arxiv, https://arxiv.org/abs/2610.03631

- **Mechanism:** Agents build a neutron instrument description through validating tools, a McStas ray-trace simulates it, and a four-level ladder (syntax, runtime, structure, science) scores it with no LLM judge. Procedural task families with held-out parameter regimes give unlimited instances, and partial credit across the ladder is what lets reinforcement learning work. The authors also released probes that showed four task designs were solvable without a model.
- **Claim:** RL on the environment's reward lifts Qwen3-8B from 11% to 77% on held-out instances of one family.
- **Testable:** no. It needs the McStas simulator and an RL training run, which will not fit in 30 minutes. Needs: McStas, GPU time for RL..
- **Idea on its own:** sound. Verifiable graded rewards with held-out regimes and no-model baselines is a rigorous way to build agent evals.
- **How it would be done:** The transferable part is the method: write a simulator-backed task with a deterministic grader, split the score into levels, and run no-model baselines to find tasks that can be solved by tricks. Proteus could copy that for a desk, for example grading a forecast pipeline stage by stage. The paper's own build needs McStas and an RL stack. A physicist would be needed to design real instrument tasks.
- **Stack already covers:** Claude Code with skills and sub-agents, Ollama with a qwen model
- **To fetch:** McStas https://mcstas.org (The neutron ray-trace simulator the grader runs.)
- **Missing:** A public NeutronGym release was not confirmed in the abstract.
- **Field Notes line:** A physics-design gym grades agents with a four-step ladder and no LLM judge, and partial credit is what made the RL gain appear.

### H-0133 lichess-bot-devs/lichess-bot: A bridge between Lichess bots and chess engines
2026-10-05, github, https://github.com/lichess-bot-devs/lichess-bot

- **Mechanism:** A Python bridge that opens the Lichess Bot API event stream (long-lived streaming HTTP with an OAuth token), accepts challenges that pass config filters, then streams each game and relays positions to a UCI or XBoard engine through python-chess. It adds matchmaking, draw and resign rules, opening books and tablebases around that loop.
- **Claim:** A free bridge between the Lichess Bot API and chess engines supporting every variant and time control.
- **Testable:** no. The Bot API needs a Lichess OAuth token and a BOT account, so a live run is not keyless. Needs: A Lichess OAuth token (Proteus already runs its own bot, P-0011)..
- **Idea on its own:** sound. Stream events, filter challenges, hand moves to an engine is a proven design that is easy to compare against a home-built bot.
- **How it would be done:** Read the lichess-bot source for how it handles reconnects, challenge filters and game state, and diff that against the existing Proteus bot. Any gap such as clock handling or takeback logic can be copied as a small patch. Engines would be Stockfish or a homemade engine over UCI. Matchmaking against other bots needs a token, so a human has to authorise it.
- **Stack already covers:** launchd long-running pollers
- **To fetch:** python-chess https://github.com/niklasf/python-chess (Engine communication and board state library the bridge builds on.); Stockfish https://stockfishchess.org (Free UCI engine to plug into a bot.)
- **Missing:** Nothing; it is a reference to compare against.
- **Field Notes line:** The standard Lichess bot bridge is a thin stream listener plus python-chess engine plumbing, which is a useful reference for Proteus's own bot.

### H-0131 scroll-driven website skill
2026-10-05, vault, https://github.com/nateherkai/scroll-craft. Vault verdict on the vendor exists (vault verdict: nateherkai/scroll-craft); mechanism recorded, vendor not re-judged.

- **Mechanism:** A Claude Code skill that forces an eight-question brief, then plans a scroll journey and builds a hero from separate visual planes that move at different rates. Photoreal assets come from supplied files or an image API (Kie.ai). A headless-browser screenshot verifier captures desktop, mobile and reduced-motion scroll states so the agent can check its own output.
- **Claim:** A skill that produces premium scroll-driven landing pages with layered depth heroes and a screenshot verifier.
- **Testable:** yes. Does the repo's screenshot verifier run on a local static page without keys and produce desktop and mobile scroll captures (yes/no)? Not queued (daily cap).
- **Idea on its own:** needs-a-run. Layered parallax plus a self-check loop is a sound pattern, but whether the verifier works without paid assets is unproven.
- **How it would be done:** Clone the repo, read the scripts, then point the verifier at a hand-made static HTML page with CSS layers. Step through scroll positions with Playwright, save screenshots at 390 and 1440 pixel widths, and check the reduced-motion path. Heroes would then be built from supplied stills or Gemini stills in place of Kie.ai. A designer would still be needed to judge whether the result avoids the template look.
- **Stack already covers:** Claude Code with skills and sub-agents, Gemini (stills), HyperFrames (video compose, captions, render)
- **To fetch:** scroll-craft https://github.com/nateherkai/scroll-craft (The skill and verifier itself, MIT licensed.); Playwright https://playwright.dev (Headless browser used to capture scroll-state screenshots.)
- **Missing:** Nobody has shown the layered-hero output holds up without paid image generation.
- **Field Notes line:** A web-design skill that makes the agent screenshot its own scroll states at desktop and mobile widths before it calls a page finished.

### H-0130 I Ran a Chess Programming Tournament!
2026-10-04, youtube, https://www.youtube.com/watch?v=Ne40a5LkK6A

- **Mechanism:** Contestants submit chess bots capped at 1,024 compiler-counted tokens, with a shared framework supplying legal moves and board state. A large Swiss tournament over 64 rounds pairs bots with similar scores who have not met, so about 600 bots rank in a manageable number of games. Token counting by syntax tree rather than file size was exploited via a line directive and an outdated compiler, which shows how a cap can be gamed.
- **Claim:** A 600-plus bot Swiss tournament over 64 rounds under a 1,024 token limit, with several exploits found and outlawed.
- **Testable:** no. The bots and framework are C# and need setup beyond a 30 minute keyless slice with no clear verdict. Needs: The challenge framework and entries from the creator's repository.
- **Idea on its own:** sound. Swiss pairing with a hard resource cap is a sound way to rank many entrants, and the exploit list is a useful checklist.
- **How it would be done:** For the Lichess bot, a small local Swiss runner with python-chess and a couple of engines would rank variants cheaply. The exploit list (data hidden in directives, outdated counter, network fetch) is a checklist for any submission cap. A hired person would only be needed to run a public contest.
- **Stack already covers:** Ollama with a qwen model
- **To fetch:** python-chess https://github.com/niklasf/python-chess (Legal moves and engine play for a local tournament runner); Stockfish https://stockfishchess.org (Reference opponent for rating a bot)
- **Field Notes line:** A 600-bot Swiss tournament under a 1,024 token cap showed how a size limit gets gamed and why Swiss pairing ranks fast.

### H-0129 Jakeschincariol/replica-skill: Eleven free Claude skills that clone any app: reverse-engineer it, rebuild it, test it fo
2026-10-04, github, https://github.com/Jakeschincariol/replica-skill

- **Mechanism:** A chain of eleven skills passes files through a replica/ folder: recon builds a screen and flow map and features.csv from public pages, help centres and store listings, then later skills plan, build, test and diff against that map. A diff step scores parity against the original and a review-mining step turns user complaints into the product angle. It claims clean-room scope: features and flows, not code, logos or copy.
- **Claim:** Eleven free MIT Claude skills that reverse-engineer, rebuild, test and launch a clone of any app, with no signup or key.
- **Testable:** yes. Does the recon step's helper tooling run on a public help-centre page and emit a features.csv with at least 10 rows? Queued as P-0061.
- **Idea on its own:** needs-a-run. The pipeline is plausible but quality of recon from public pages alone is unproven.
- **How it would be done:** Clone the repo, read the recon SKILL.md and run its Python tools on a public help centre. Check whether the features list is accurate against the page by hand. The review-mining step is the portable part and could be pointed at public app-store reviews for any product. Rebuilding and deploying is ordinary agent coding work.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** replica-skill https://github.com/Jakeschincariol/replica-skill (The eleven skills and Python tools to run)
- **Field Notes line:** A chain of eleven skills maps an app from public pages, rebuilds it and scores parity, with a review-mining step feeding the pitch.

### H-0127 node canvas workflows (Flows)
2026-10-04, vault, 

- **Mechanism:** A node canvas lets you wire generation steps (image, video, voice) into a graph where each node's output feeds the next, run as a batch with a credit cost per node. The platform sits on top of third-party models such as Kling and Seedance and charges credits per clip. The value is the graph layer and reusable templates, not exclusive models.
- **Claim:** Kling 3.0 costs 6.25 credits for 5 seconds at 720p, with a canvas layer (Flows) on top of aggregated models.
- **Testable:** no. Needs a paid trial account and credits, and its MCP only reports balance. Needs: A Promptwise account and credits.
- **Idea on its own:** needs-a-run. Whether the canvas saves time over scripted API calls only shows up when a real multi-step job is built both ways.
- **How it would be done:** Pick one job, for example script to stills to clips to voice, and build it once on the canvas and once as a script calling the same model APIs. Compare minutes of operator time, cost per finished clip and how easily a failed step is re-run. A hired operator would handle the web-only steps the scripts cannot reach.
- **Stack already covers:** HyperFrames (video compose, captions, render), ElevenLabs (voice), HeyGen and Tavus (avatars), Gemini (stills), Claude Code with skills and sub-agents
- **To fetch:** ComfyUI https://github.com/comfyanonymous/ComfyUI (Free open-source node-graph runner for the same chaining pattern)
- **Missing:** Nobody has a scripted equivalent of the canvas for Kling and Seedance without an aggregator account.
- **Field Notes line:** A node canvas that chains image, video and voice generation steps is the real product, since the underlying models are not exclusive.

### H-0125 The Innocent Courier: Covert Exfiltration Through Legitimate LLM Web Fetching
2026-10-04, arxiv, https://arxiv.org/abs/2610.01768

- **Mechanism:** Malware that has no direct internet access hides a secret in a URL and asks an LLM agent to fetch it as if it were documentation for a benign task. The agent's own web-fetch tool carries the secret out to an attacker-controlled DNS or web server. Defences are egress logging of fetched URLs, DNS monitoring for high-entropy subdomains, allowlisting fetch destinations and requiring approval for unfamiliar hosts.
- **Claim:** 79.7% attack success across eleven open-parameter models, plus a case study on real-world chatbots.
- **Testable:** no. Reproducing the attack needs a tool-calling model and an attacker server, which is out of scope and not a keyless slice. Needs: A tool-calling model with a fetch tool.
- **Idea on its own:** sound. Any agent with an unrestricted fetch tool is an egress channel, and the paper shows it works in practice.
- **How it would be done:** The useful work is defensive: audit what fetch tools the Proteus agents have, log every fetched URL, and flag long or high-entropy path and subdomain strings. The unattended hook already allows or denies by list, so extending it to URL allowlists for WebFetch is the cheap fix. A paper review would check the detection section for numbers.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Field Notes line:** An agent's own web-fetch tool can be turned into a covert exit for secrets, with a 79.7% success rate across eleven models.

### H-0124 ythx-101/live-panel-skill: Config-driven animated architecture diagrams: turn one JSON file into a terminal-style, alway
2026-10-04, github, https://github.com/ythx-101/live-panel-skill

- **Mechanism:** One JSON config describes nodes, wires, a log and counters. A self-contained HTML template animates it from a single clock. A Python script drives headless Chrome to capture frames and ffmpeg encodes H.264. A checker samples about 120 time points and measures text overflow from the DOM, and re-renders exported frames to prove determinism.
- **Claim:** Turns one JSON file into a roughly 28 to 30 second animated architecture diagram as mp4 or live web page, standard library Python only.
- **Testable:** yes. Does render.py produce an mp4 from the codex-agents example config in under 5 minutes, and does check_frames.py exit 0? Queued as P-0060.
- **Idea on its own:** sound. Config-driven templates rendered through headless Chrome and ffmpeg are a reliable way to make repeatable explainer clips.
- **How it would be done:** Clone the repo, run render.py on an example config, then check_frames.py with --repeat. Write a config for a Proteus desk diagram and render that. It overlaps with HyperFrames, so the useful comparison is the frame-determinism check, which could be borrowed.
- **Stack already covers:** HyperFrames (video compose, captions, render)
- **To fetch:** live-panel-skill https://github.com/ythx-101/live-panel-skill (The renderer and examples); ffmpeg https://ffmpeg.org (H.264 encoding step if not already installed)
- **Field Notes line:** One JSON file becomes a moving architecture diagram video, and its checker re-renders frames to prove they are deterministic.

### H-0122 replication gap measured on demo
2026-10-04, vault, https://api-portal.etoro.com/changelog

- **Mechanism:** A leader account on a copy-trading platform makes trades, followers' demo accounts mirror them through the platform's copy endpoints, and the gap is the difference between the leader's gain series and the follower's realised return. Fees are zero on demo, so real costs (spreads, fees, slippage) are added from the trade log afterwards. The numbers come from the leader gain series and the demo account's own history.
- **Claim:** Demo keys are locked to the demo account, copy endpoints have been live since 23 Aug 2026, and leader gain series are readable.
- **Testable:** no. Needs an eToro demo API key, which is an account and a key. Needs: An eToro demo API key.
- **Idea on its own:** sound. Measuring follower return against leader return on demo money is a clean, no-risk way to price the replication gap.
- **How it would be done:** Pick a handful of leaders, open demo copies of each, and poll the leader gain series and the demo portfolio daily into a CSV. Compute the gap per leader over a fixed window, then subtract assumed real fees and spreads from the trade log to estimate the true gap. Commit the leader picks before outcomes are known, as on the other desks.
- **Stack already covers:** launchd long-running pollers, freqtrade
- **To fetch:** eToro API portal https://api-portal.etoro.com (Demo copy-trading endpoints and docs)
- **Field Notes line:** Copying a trader on a demo account and comparing it with the leader's own gain series measures how much of the return a follower really keeps.

### H-0120 Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65% Fewer Tokens
2026-10-04, arxiv, https://arxiv.org/abs/2610.01939

- **Mechanism:** The agent writes Python cells that compose robot primitives and learned policies, with conditionals and local retries inside the cell, instead of one tool call per step. Only explicitly requested images and state come back to the planner, which cuts input tokens. The comparison is against a tool-calling baseline with the same planner and primitives across 700 simulated tasks.
- **Claim:** Success rises from 63.1% to 71.7% under equal LLM-call budgets, with 49% fewer calls and 65% fewer input tokens on shared solved tasks.
- **Testable:** no. Needs the GPT-6 planner and robot simulators, none of which can be run keyless. Needs: A planner model API and simulator installs (LIBERO-PRO, RoboTwin, RoboCasa).
- **Idea on its own:** sound. Batching conditionals and retries into code and returning only requested observations is a general way to cut agent round trips.
- **How it would be done:** The pattern ports to any tool-using agent: expose primitives as Python functions in a persistent kernel, let the agent write cells with checks and retries, and return only what it asks for. For the Grinder it would mean one cell that pulls, filters and logs a token rather than a call per field. A paper-desk replay could count calls and tokens both ways.
- **Stack already covers:** Claude Code with skills and sub-agents, The Grinder paper desk
- **Field Notes line:** Letting an agent write a code cell with retries and selective observation, not one tool call per step, cut tokens 65% in robot sims.

### H-0119 QingYunA/answer-me-with-html: Answer me with HTML — an agent skill that answers hard questions with a one-page HTML you 
2026-10-04, github, https://github.com/QingYunA/answer-me-with-html

- **Mechanism:** The model writes a short Markdown draft and a bundled Node CLI turns it into a styled single-page HTML with diagrams and tables, so the model never types CSS or SVG coordinates. The saving is in output tokens and wall-clock time only, because the skill adds two extra turns that re-read context. Numbers come from a bench script in the repo.
- **Claim:** 7.4x fewer output tokens and 3.6x faster than asking for HTML directly, at about the same cost per answer.
- **Testable:** yes. Does the bundled CLI turn a Markdown draft into a readable HTML page in under one second, with no network or key? Queued as P-0059.
- **Idea on its own:** sound. Moving boilerplate from model output to a deterministic renderer is a real token and latency saving.
- **How it would be done:** Clone the repo into the sandbox, read SKILL.md, and run the CLI on a hand-written Markdown draft with a diagram block. Time it and open the result. Then compare against the repo's bench README to see whether the 923-token figure is plausible by counting the draft. The same pattern could feed Field Notes pages.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** answer-me-with-html https://github.com/QingYunA/answer-me-with-html (The skill and bundled CLI to run); Node.js 20+ https://nodejs.org (Runtime for the bundled CLI)
- **Field Notes line:** A skill that has the model write Markdown and a CLI build the page claims 7.4x fewer output tokens, but the same bill.

### H-0117 Benchmark DeepSeek, GLM and Kimi against the M5 qwen3.6 on non-personal rewrite and summary jobs through the free endpoi
2026-10-04, vault, https://www.instagram.com/p/DdwbLoEgVKY/

- **Mechanism:** A hosted OpenAI-compatible endpoint serves open-weight models (DeepSeek, GLM, Kimi) on a free developer tier with a request-per-minute cap. You send the same fixed set of non-personal rewrite and summary prompts to the hosted models and to the local qwen model via Ollama, then score outputs with a rubric or an LLM judge. The cap (about 40 RPM) bounds a bake-off to a few hundred calls, which is enough.
- **Claim:** The free tier gives about 40 requests a minute across roughly 80 to 100 open-weight models with no card.
- **Testable:** no. The endpoint needs an account and an API key, so it cannot be run keyless tonight. Needs: A free NVIDIA Build account and API key.
- **Idea on its own:** sound. Comparing models on a fixed public prompt set before pulling weights is cheap, standard and answers a real choice.
- **How it would be done:** Write 30 to 50 synthetic or public-domain rewrite and summary prompts with a short rubric. Loop them through the hosted endpoint for each candidate model and through Ollama qwen locally, logging output, latency and token counts to a CSV. Score with a rubric, using a different model family as judge, and spot-check a sample by hand. Respect the rate cap with a simple sleep. Keep personal data out entirely, as the terms forbid it.
- **Stack already covers:** Ollama with a qwen model, Claude Code with skills and sub-agents
- **To fetch:** NVIDIA Build API catalogue https://build.nvidia.com (The free hosted open-weight endpoint to benchmark against); promptfoo https://github.com/promptfoo/promptfoo (Runs the same prompt set across several providers and scores them)
- **Field Notes line:** A free hosted tier could let me race DeepSeek, GLM and Kimi against my local qwen on public text before downloading any weights.

### H-0116 Everything You Know About Skills IS OUTDATED
2026-10-03, youtube, https://www.youtube.com/watch?v=e7TY56-yIvM

- **Mechanism:** The claim is that when a skill points to a long reference file, Claude may open only the first 100 lines (a head -100 call) to decide whether the file is relevant, so rules after that point can go unseen. The stated fix is a contents list at the top of any reference file over 100 lines so the model can see the whole map or jump to a section. A second rule scales how exact a skill's instructions are to how fragile the task is.
- **Claim:** Reference files over 100 lines with no contents list are rarely used in full, and Anthropic's best-practice guide has six new rules.
- **Testable:** yes. How many reference files under the local skills folders exceed 100 lines, have no contents list, and have key rules after line 100? Queued as P-0057.
- **Idea on its own:** needs-a-run. The head-100 behaviour is plausible but secondhand, and only an audit of real skills plus a controlled read shows whether it matters here.
- **How it would be done:** Scan every skill folder under the Claude skills directories and list reference files by line count and whether a contents block sits in the first ten lines. Flag those over 100 lines that lack one and note headings sitting past line 100. To check the behaviour itself, a later run in an interactive session would place a marker rule at line 150 of a test reference and see whether the skill follows it. Fixing is a short edit per file.
- **Stack already covers:** Claude Code with skills and sub-agents
- **Field Notes line:** A claim that Claude reads only the first 100 lines of a skill's reference file, so long files without a contents list hide their own rules.

### H-0113 Photoreal moving footage of a subject you cannot film, one consistent face and a directed camera move
2026-10-03, vault, https://www.instagram.com/reel/DdoiRHMmyel/

- **Mechanism:** A routing layer sends a prompt and reference stills to a video model such as Veo, Kling or Seedance, with camera-move presets expanded into the prompt. Face consistency across shots comes from feeding the same reference images or a character sheet into each generation, then picking takes. The quality lives in the underlying models, so the same result can be had by calling those models directly with a prompt bank.
- **Claim:** Photoreal moving footage of a subject you cannot film, with one consistent face and a directed camera move.
- **Testable:** no. Video generation models need accounts and paid credits. Needs: An account and credits for a video model, or a free-tier allowance..
- **Idea on its own:** needs-a-run. Reference-image conditioning does improve consistency, but how far it holds across a five-shot sequence is only known by generating one.
- **How it would be done:** Make a character sheet in Gemini stills, then write a prompt per shot that carries the same reference images and a named camera move. Generate each shot on one video model, review the takes on a contact sheet, and cut with HyperFrames. Use fictional or consented subjects only. A person is useful to judge whether the face really holds and to redo failed takes.
- **Stack already covers:** Gemini (stills), HyperFrames (video compose, captions, render), HeyGen and Tavus (avatars)
- **To fetch:** Kling AI https://klingai.com (Video model with a free daily credit allowance for a reference-image consistency test.)
- **Field Notes line:** Camera-move presets plus the same reference stills in every shot is how these tools hold one face across a sequence.

### H-0111 Mimir: Physics-Grounded LLM Agents for Long-Horizon Irrigation Control
2026-10-03, arxiv, https://arxiv.org/abs/2610.02038

- **Mechanism:** The LLM never acts directly. It outputs a structured proposal, a deterministic soil-water simulator numerically checks it, the LLM revises, and a bounded deterministic selector picks the action. A slower loop distils recurring failures into persistent written principles that condition future proposals, while the simulator, evaluator and action limits stay immutable.
- **Claim:** Lowest aggregate control cost among compared methods and about 51 percent less irrigation than historical schedule replay.
- **Testable:** no. Needs the authors' simulator, site data and code, which are not confirmed released. Needs: The paper's code and soil and weather data..
- **Idea on its own:** sound. Keeping truth and action authority in deterministic code while the LLM proposes and learns notes is a sound pattern for long-horizon decisions with compounding errors.
- **How it would be done:** The pattern maps onto a paper desk: the LLM proposes a position, a deterministic check (a liquidity cap, a Dixon-Coles probability, a size limit) accepts or clips it, and a nightly pass writes failure patterns into a notes file that conditions the next proposals without touching the checker. Build it as a wrapper around the Grinder or Pitch desk with the rules file committed so changes are dated. No hired person is needed for the pattern; real irrigation would need an agronomist and field hardware.
- **Stack already covers:** Claude Code with skills and sub-agents, GeckoTerminal, DexScreener and rugcheck readers and a Solana paper desk (the Grinder), football-data and a Dixon-Coles paper desk (the Pitch)
- **Missing:** The paper's implementation, if any is released.
- **Field Notes line:** Mimir lets an LLM propose farm irrigation but only a fixed simulator and hard limits can act, and the LLM learns written rules from its own failures.

### H-0110 zhuyansen/awesome-claude-video-skills: Open-source skills and toolkits that let Claude Code, Codex and other coding agen
2026-10-03, github, https://github.com/zhuyansen/awesome-claude-video-skills

- **Mechanism:** A curated index of about 230 repos that let coding agents make video, sorted into ten types. A decision model reads each README to answer inclusion questions and assign a security grade, refreshed every eight hours, so the grades are model opinions rather than audits. Inclusion needs a README and either 50 stars or a quality bar plus a few stars.
- **Claim:** 180 to 230 open-source video skills and toolkits, each read and security-graded.
- **Testable:** no. It is a list; running it would only mean fetching other repos, which are separate items.
- **Idea on its own:** sound. A shelf of candidate tools is useful, with the caveat that the security grades come from a model reading READMEs, not from code review.
- **How it would be done:** Pull the README and the category lists, then filter to the Frameworks, Editing and Shorts types. Check each shortlisted repo's licence and install route, then queue the few that fill gaps next to HyperFrames for sandbox runs on later nights. Treat the SAFE grade as a hint and read the install script before running anything.
- **Stack already covers:** HyperFrames (video compose, captions, render), Claude Code with skills and sub-agents
- **To fetch:** awesome-claude-video-skills https://github.com/zhuyansen/awesome-claude-video-skills (The list itself, source for further video-skill repos.); Remotion https://github.com/remotion-dev/remotion (The best-known alternative React video renderer to compare with HyperFrames.)
- **Field Notes line:** A model-graded index of 230 video skills for coding agents is a ready shelf to mine for HyperFrames alternatives and extras.

### H-0108 Generating many platform-native variants (hooks, colour grades, overlays) from one filmed asset
2026-10-03, vault, 

- **Mechanism:** One filmed asset is fed through a loop that swaps hooks, applies colour grades, adds overlays and re-crops per platform, producing many renders from one source. The render half is ordinary templated video composition. The vendor's distribution half routes posts through antidetect cloud phones, one spoofed device per account, which is grey-market automation: platforms catch it with device and network fingerprinting, behavioural similarity across accounts, and near-duplicate content matching, and treat it as inauthentic content.
- **Claim:** Turn one video into many platform-native variants and post them across accounts automatically.
- **Testable:** no. The useful part needs a filmed asset and owned accounts, and the posting half is the evasion tooling, so no keyless slice exists. Needs: A filmed source asset and owned, disclosed accounts for any real posting..
- **Idea on its own:** sound. Producing hook and format variants of one's own footage for A/B testing on owned accounts is standard practice; only the spoofed-device posting is the problem.
- **How it would be done:** Define a variants table of hooks, grades, overlays and aspect crops, and render each row from the single source through a templated HyperFrames composition. Add per-variant tracking so each post's performance can be compared, which is the per-post idea worth keeping. Posting is done by a person through each platform's own scheduler on accounts the owner runs openly, with the AI label where required. A hired editor covers the first filmed asset and the judgement on which hooks are worth testing.
- **Stack already covers:** HyperFrames (video compose, captions, render), ElevenLabs (voice), Claude Code with skills and sub-agents
- **To fetch:** ffmpeg https://ffmpeg.org (Crops, grades and re-encodes for per-platform specs.)
- **Missing:** A variant-planning loop that maps hooks and grades to renders and tracks each variant's results.
- **Field Notes line:** Variant loops are plain templated rendering; the grey part is posting through spoofed phones, which platforms detect by device fingerprint and near-duplicate matching.

### H-0106 OmniSeek: Native Tool Integration for Multi-turn Audio-Visual Reasoning
2026-10-03, arxiv, https://arxiv.org/abs/2610.02181

- **Mechanism:** An omni-modal LLM is trained to act as a multi-turn agent that chooses whether to look or listen and over which time window, then gets the raw audio or video segment appended to its context. It is cold-started with supervised fine-tuning on 170K synthetic multi-hop trajectories, then refined with two-stage reinforcement learning on verifiable rewards. An extra reward fires only when a successful answer genuinely needed both audio and vision, which discourages single-modality shortcuts.
- **Claim:** Active evidence seeking over long audio-visual context improves audio-visual reasoning across a wide range of benchmarks.
- **Testable:** no. Needs a trained omni-LLM checkpoint and GPU, and the paper gives no runnable keyless artefact. Needs: Model weights and GPU, if released..
- **Idea on its own:** sound. Fetching sparse evidence on demand is a sensible fix for long-context media, and the both-modalities reward targets a known shortcut.
- **How it would be done:** The same pattern can be built crudely without training: a transcript or scene index acts as a map, and an agent requests specific time windows (a frame grab or an audio snippet) as tool calls. For the YouTube pipeline that means search the transcript first, then pull only the frames around the matching timestamps. Reproducing the trained model would need the released checkpoint or a research team to rebuild the data engine.
- **Stack already covers:** a keyless YouTube search, oEmbed and transcript pipeline, local transcription, Claude Code with skills and sub-agents
- **To fetch:** ffmpeg https://ffmpeg.org (Cut frame and audio windows on demand for a look-or-listen tool.)
- **Missing:** A released OmniSeek checkpoint or the OmniTraj-170K data; neither is confirmed available.
- **Field Notes line:** OmniSeek teaches a model to choose which minute of audio or video to fetch next, instead of swallowing the whole clip in one pass.

### H-0103 Whether a fees-paid threshold removes rugs without removing the launches that ran, on a dated sample
2026-10-03, vault, https://www.instagram.com/reel/Db6WNI9BSQX/

- **Mechanism:** Total SOL fees (priority fees plus Jito tips) paid by a token's traders so far is read from on-chain transactions that touch the token's pool. The idea is that a rug is cheap to launch but organic buyers of a real run pay real fees, so a minimum fees-paid figure screens out launches nobody traded seriously. The number comes from summing the fee field across the pool's transactions, via an indexer such as Dune or Solana RPC history. Whether it separates rugs from runners is an empirical question on a dated sample.
- **Claim:** A three-column terminal filter with a fees-paid threshold is said to remove about 90 percent of rugs.
- **Testable:** yes. On the Grinder's already-tracked launches with known outcomes, does a fees-paid threshold remove at least 80 percent of the rugged ones while keeping at least 70 percent of those that ran? Not queued (daily cap).
- **Idea on its own:** needs-a-run. Fees paid is a real cost borne by traders so it plausibly proxies genuine activity, but wash trading can inflate it and the 90 percent figure has no sample behind it.
- **How it would be done:** Take the Grinder's closed launches that are already labelled rugged or ran, with dates. For each, pull the pool's recent transaction signatures from public Solana RPC and sum the fee field to get fees paid up to a fixed time after launch. Sweep a few thresholds and compute rugs removed and runners kept at each, on a time-ordered split so the threshold is not fitted on the same launches it is judged on. Record the confusion matrix and commit the threshold before applying it to new launches. A Dune query over a larger dated sample would be the next step if the slice is promising.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers and a Solana paper desk (the Grinder), launchd long-running pollers
- **To fetch:** Solana public JSON-RPC https://api.mainnet-beta.solana.com (Keyless getSignaturesForAddress and getTransaction to sum fees per pool, rate limited.); Dune https://dune.com (Free tier SQL over Solana transactions for a larger dated sample, needs an account so later.)
- **Field Notes line:** Fees paid by a token's own traders as an anti-rug filter: cheap to compute, and we can check it against launches we already tracked.

### H-0101 ericmmartin/youtube-transcript-plus: YouTube Transcript Plus is an advanced Node.js package designed to fetch and proces
2026-10-02, github, https://github.com/ericmmartin/youtube-transcript-plus

- **Mechanism:** It makes three HTTP calls: the video page, a POST to YouTube's Innertube player endpoint to get caption track URLs, then a GET of the transcript data. Fetch functions can be swapped for a proxy, which exists because YouTube blocks datacentre and repeated IPs. It uses an unofficial interface, so it breaks when YouTube changes it.
- **Claim:** Fetches YouTube transcripts through the unofficial Innertube API, with custom fetch hooks for proxies and a user agent.
- **Testable:** yes. Does fetchTranscript return non-empty caption text for three public videos from this Mac with no proxy, yes or no, and how many fail with a block? Queued as P-0056.
- **Idea on its own:** needs-a-run. It depends on an unofficial endpoint that blocks some IPs, which only a run from this machine shows.
- **How it would be done:** Install the package in the sandbox, call fetchTranscript on three public videos with captions and record success, text length and any block error. Compare against the existing keyless transcript pipeline on the same IDs. If blocked, the library's fetch hooks show where a proxy would sit, though no proxy is added tonight. A person would only be needed to buy proxy access, which is outside this test.
- **Stack already covers:** a keyless YouTube search, oEmbed and transcript pipeline
- **To fetch:** youtube-transcript-plus https://github.com/ericmmartin/youtube-transcript-plus (The library under test); Node.js 20+ https://nodejs.org (Runtime the package requires)
- **Field Notes line:** This Innertube transcript library is the same route that returned IpBlocked in tonight's harvest, so a direct run shows if this IP is blocked.

### H-0100 Show HN: Breadcrumb, record everything on your mac + context manager for AI
2026-10-02, hn, https://innerloop.works/breadcrumb

- **Mechanism:** A local recorder captures screen, meetings with timestamped screenshots, AI session transcripts and sub-agent activity, encrypted on disk. It indexes this and exposes more than 30 MCP tools so Claude Code, Codex or Cursor can search past work. Stored rules are injected by context, and a commenter raises the cost of loading all tool definitions each request.
- **Claim:** Records everything on your Mac and turns it into searchable memory for your AI, with 30+ MCP tools.
- **Testable:** no. It is a closed Mac app that records the screen and needs install and permissions, so it is not a keyless sandbox run. Needs: The macOS app and screen-recording permission.
- **Idea on its own:** needs-a-run. More recorded context helps recall, but retrieval quality and tool-definition overhead decide whether it pays.
- **How it would be done:** Capture sources to local storage, extract text by OCR and transcription, and index with timestamps. Expose search over MCP and load tools lazily to avoid definition bloat. Add a rules layer matched by project or file context. A person decides what must never be recorded, which no script covers.
- **Stack already covers:** Claude Code with skills and sub-agents, local transcription
- **To fetch:** Breadcrumb MCP tool definitions https://innerloop.works/breadcrumb/mcp (Read the tool list to measure definition size)
- **Field Notes line:** Screen, meeting and agent transcripts indexed behind 30 MCP tools; the token cost of those tool definitions is the open question.

### H-0099 human reads flagged threads from alert links
2026-10-02, vault, 

- **Mechanism:** Keyword alerts arrive by email with a thread link, and the agent browsers refuse reddit.com, so a person reads each flagged thread. The open question is whether the public RSS or JSON views of a thread, which are plain HTTP, can be read by a script instead. If they return thread text keyless from this machine, the human step becomes a fallback.
- **Claim:** The vault says the Reddit listening lane depends on a human reading flagged threads because agent browsers are blocked.
- **Testable:** yes. Does a plain HTTP request to a public subreddit RSS feed and a thread RSS URL from this Mac return HTTP 200 with thread text, yes or no? Queued as P-0055.
- **Idea on its own:** needs-a-run. Whether public feeds survive rate limiting and blocking is unknown until requested.
- **How it would be done:** Request a subreddit .rss and a thread .rss with a descriptive user agent and light spacing, then record status and body size. If both work, parse titles, bodies and top comments into a digest per alert. Keep the human read for threads that return blocked or truncated text. Request volume stays low and follows the site's published rules.
- **Stack already covers:** launchd long-running pollers, Claude Code with skills and sub-agents
- **Field Notes line:** Agent browsers refuse Reddit, but plain RSS fetches might still return thread text with no key.

### H-0098 elithril/blender-kiln (new in awesome-claude-code)
2026-10-02, awesome, https://github.com/elithril/blender-kiln. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** A Claude Code skill drives Blender through an MCP server. Its new part is a fidelity loop: render the model at the reference photo's camera, list silhouette gaps per height band, then re-measure the exported, compressed GLB rather than the .blend. A bench scores each rebuild against the real asset from five sides, using Poly Haven previews as references.
- **Claim:** Rebuilds an object from one photo as a GLB, with shape scores of 0.897, 0.950 and 0.750 on three assets at roughly 4 to 6 dollars each.
- **Testable:** no. It needs Blender with an MCP server running and a paid model session per asset. Needs: Blender 4.4+ with a Blender MCP, and a Claude session budget.
- **Idea on its own:** sound. Measuring against the reference from the same camera and scoring the shipped file is a real feedback loop, not a claim.
- **How it would be done:** Install Blender and a Blender MCP, then load the skill. Give it a photo and let it inventory parts, texture from CC0 sets and build in scripted Blender. Run the fidelity check at the photo camera, fix gaps, then optimise and validate the GLB. The same render-and-measure loop could be reused for other generated assets, and a person judges final taste.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** blender-kiln https://github.com/elithril/blender-kiln (The skill and the fidelity_check script); Blender https://www.blender.org (Required runtime); Poly Haven https://polyhaven.com (CC0 textures and reference models)
- **Field Notes line:** A scoring loop that renders a 3D model from the photo's camera and measures the gap is what makes agent-built assets improve.

### H-0095 Show HN: Made an open-source Lego AI generator
2026-10-02, hn, https://github.com/anteloc/ldraw-nova

- **Mechanism:** LDraw is a plain-text format where each line places one brick with a colour, position and rotation matrix, so a model is a short program. The project gives an LLM agent a Python toolset, instructions and docs to write .ldr or .mpd files, check them, and view them through LDView or LeoCAD. It ships as a dockerised web app that can call OpenAI, Claude or OpenRouter.
- **Claim:** Frontier models can generate high-quality LEGO CAD models by writing LDraw source, packaged as an open-source web app.
- **Testable:** yes. Does the repo's Python toolset validate and parse a hand-written LDraw file offline, yes or no, and how many of its checks pass? Queued as P-0054.
- **Idea on its own:** needs-a-run. The idea is sound but quality depends on the validation tools, which a run on a sample file can show.
- **How it would be done:** Clone the repo, read its tool list and run the validators on a small known-good LDraw file and a deliberately broken one. Check whether collisions, floating parts and missing part files are caught. If they work, wrap them as a Claude Code skill so an agent loops write, validate, render. The LDraw part library is public and free, and a person would judge whether the finished model looks right.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** ldraw-nova https://github.com/anteloc/ldraw-nova (The toolset under test); LDraw parts library https://www.ldraw.org/parts/latest-parts.html (Part definitions needed for validation); LDView https://tcobbs.github.io/ldview/ (Renderer for checking models)
- **Field Notes line:** LEGO models are just text files of brick placements, so an agent with a validator can write them.

### H-0094 Higgsfield Genjutsu as the final route for motion transfer, whole-frame recast at about 7 dollars per 15 seconds at 1080
2026-10-02, vault, https://www.instagram.com/reel/Dd-BvW5Jych/

- **Mechanism:** Film a person performing, supply a reference image of the target avatar, and a video model recasts the whole frame: body motion and timing are taken from the source clip while identity, clothes and background come from the reference. It is the same family as Kling Motion Control, run as a hosted generation per clip. The price quoted is about 7 dollars per 15 seconds at 1080p.
- **Claim:** Whole-frame motion transfer so an AI avatar repeats your exact performance, about 7 dollars per 15 seconds at 1080p.
- **Testable:** no. It is a paid hosted service needing an account and spend, and Proteus has no filmed source performance. Needs: A Higgsfield account and credits, plus a filmed own-performance clip.
- **Idea on its own:** sound. Driving a generated character from a real performance is an established technique and cuts retakes for consistent-avatar video.
- **How it would be done:** Film the performance against a plain background with the camera framing the target shot needs. Prepare a clean avatar still, then run both through the motion-transfer model and review each take from a contact sheet. Compare the same pair on Kling Motion Control for fidelity and cost per second, then pick one route. A person still performs and approves the footage, since no script covers the acting.
- **Stack already covers:** HyperFrames (video compose, captions, render), HeyGen and Tavus (avatars), Gemini (stills), ElevenLabs (voice)
- **To fetch:** Kling Motion Control https://klingai.com (Comparison route for the same source clip); Higgsfield https://higgsfield.ai (Genjutsu route under test)
- **Missing:** A filmed reference performance clip of the person to be recast.
- **Field Notes line:** Motion transfer now recasts the whole frame from one filmed performance, at roughly 7 dollars per 15 seconds.

### H-0091 Edwardxlai/easyread: 把英文论文读成舒服的中文：本地 PDF 论文翻译、原文对照、边读边问 AI、文献管理。Read English papers in comfortable Chinese.
2026-10-02, github, https://github.com/Edwardxlai/easyread

- **Mechanism:** Each PDF page is rendered, then a chosen model (Claude Code or Codex CLI on the user's login, an API, or local Ollama) translates it page by page. The agent can look at the page image to check formulas, which are re-typeset with KaTeX, and the translation is kept apart from AI explanations shown in the margin. A local server writes edits to files, with failed pages retried and token use logged per call.
- **Claim:** Translates English papers into readable Chinese with side-by-side original, margin notes and an ask-AI panel, 601 stars within days of creation.
- **Testable:** no. It is an Electron app that needs a model login or key to translate, so a keyless run would not test the mechanism. Needs: A model engine login (Claude Code, Codex) or local model run through its settings.
- **Idea on its own:** sound. Per-page translation with the page image as ground truth and a strict split between translation and commentary is a sound design.
- **How it would be done:** Split the PDF into page images and text blocks, send each page to a model with the image attached, and ask for a faithful translation only. Re-render formulas with KaTeX and tables as three-line tables, store output per page so retries are cheap. Put commentary in a separate channel so the reader can trust the main text. A bilingual reviewer would spot-check a sample of pages, since nothing scripted verifies translation quality.
- **Stack already covers:** Claude Code with skills and sub-agents, Ollama with a qwen model
- **To fetch:** easyread https://github.com/Edwardxlai/easyread (Reference implementation of per-page translation); KaTeX https://katex.org (Formula re-typesetting)
- **Field Notes line:** A paper reader that sends each PDF page image to a CLI agent so formulas get checked against the page, not just the text.

### H-0090 Show HN: Rhun, an open-source code editor written in assembly
2026-10-02, hn, https://rhun.app/

- **Mechanism:** The editor and its pixel renderer share one x86-64 assembly core. For Apple silicon a build-time translator converts that assembly to AArch64, with thin per-platform adapters for windowing and input. On top sit Vim mode, a terminal, git diffs and a panel that hosts Claude Code or Codex sessions, plus commit-message drafting through local Ollama or an existing CLI subscription.
- **Claim:** A small MIT-licensed editor in assembly for Linux, Windows and Apple silicon, with Claude Code and Codex panels, keeping launch time and footprint minimal.
- **Testable:** no. It means installing an unverified binary or building an assembly toolchain, which does not fit a keyless 30 minute sandbox verdict.
- **Idea on its own:** sound. Build-time ISA translation of a small hand-written core is a coherent way to keep one codebase tiny across platforms.
- **How it would be done:** Write the core in one assembly dialect, with a stable interface to platform adapters. A translator script maps instructions and calling conventions to AArch64 at build, then each adapter is linked per platform. Testing means diffing behaviour of the translated core against the original on the same inputs. A person would still hand-check the translator output for the instructions it cannot map.
- **Stack already covers:** Claude Code with skills and sub-agents, Ollama with a qwen model
- **To fetch:** rhun https://rhun.app/ (Source and releases to read the translator approach)
- **Field Notes line:** One assembly core, translated to ARM at build time, runs an editor on three operating systems.

### H-0089 Whether multi-buy and net-flow signals from tracked wallets predict price, measured on paper against public leaderboards
2026-10-02, vault, https://youtu.be/2ikSD3rr5v8

- **Mechanism:** Take a list of wallets ranked by realised profit on a public leaderboard (Kolscan, GMGN). Count how many distinct tracked wallets buy the same token inside a window (multi-buy) and the net SOL flow of those wallets into it (buys minus sells). Log the signal at the moment it fires with entry price, then measure forward returns at fixed horizons against a baseline of tokens that did not fire. The numbers come from on-chain swap history or the leaderboard's own wallet pages.
- **Claim:** The video says buying where several tracked wallets pile in is a repeatable edge, with a claimed 30K made part-time.
- **Testable:** no. It needs timestamped wallet-level trades and forward prices collected over days, and the leaderboard data is not confirmed keyless. Needs: Wallet trade history source (Kolscan or GMGN scrape, or a Solana indexer) and several days of forward data.
- **Idea on its own:** needs-a-run. Wallet confluence is plausible but survivorship and copy-lag usually erase it, and only a pre-registered paper run shows which.
- **How it would be done:** Pick a fixed wallet list from the leaderboard and freeze it before measuring, to avoid picking winners after the fact. Poll swaps for those wallets (public Solana RPC or a free indexer tier) and write each multi-buy event with its timestamp, then log price at 5 min, 1h and 24h from GeckoTerminal. Compare against a matched control set of tokens of similar age and liquidity that had no wallet buys. Commit the rule before outcomes exist so the Grinder timestamp is the proof. No human job is needed beyond choosing the wallet list policy.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers, Solana paper desk (the Grinder), launchd long-running pollers
- **To fetch:** Kolscan leaderboard https://kolscan.io (Public ranked wallet list to seed the tracked set); GMGN wallet pages https://gmgn.ai (Per-wallet trade history for multi-buy and net-flow counts); Solana public RPC / Helius free tier https://www.helius.dev (Swap history per wallet if the leaderboard sites block scraping)
- **Missing:** A frozen, timestamped record of tracked-wallet buys joined to forward prices does not exist anywhere public.
- **Field Notes line:** Nobody has measured whether several leaderboard wallets buying the same coin predicts price; the Grinder can pre-register that test on paper.

### H-0087 machina-sports/sports-skills: Open-source agent skills for live sports data and prediction markets. Football, F1, Kalshi
2026-10-01, github, https://github.com/machina-sports/sports-skills

- **Mechanism:** A Python package and SKILL.md set that wraps public endpoints: ESPN scoreboards, Understat xG, ClubElo ratings, FPL, Kalshi and Polymarket prices. Each skill exposes commands that fetch and normalise JSON, with a catalog.json declaring risk metadata. It depends on the upstream sites staying open.
- **Claim:** Agent skills for live sports data and prediction markets with zero API keys.
- **Testable:** yes. Does pip install sports-skills return non-empty current Understat xG and ClubElo data with no key, and how many of 20 Premier League teams match the Pitch desk's ratings ranking? Queued as P-0047.
- **Idea on its own:** needs-a-run. Wrapping public endpoints is easy, so the value depends on whether they still return clean data.
- **How it would be done:** Install the package in a venv, call the Understat and ClubElo commands for the current league, save the output and compare team order against the Pitch desk's Dixon-Coles ratings. Prediction market prices would give a blind baseline to compare predictions with.
- **Stack already covers:** football-data and a Dixon-Coles paper desk (the Pitch)
- **To fetch:** sports-skills https://github.com/machina-sports/sports-skills (The package under test.); ClubElo API http://clubelo.com/API (Free Elo ratings, no key.)
- **Field Notes line:** A keyless Python wrapper over Understat xG, ClubElo and prediction market prices could feed the Pitch desk extra inputs.

### H-0086 Show HN: Corral – Kill every command your agent starts
2026-10-01, hn, https://github.com/Cardinal44/corral

- **Mechanism:** Corral runs a command in its own session and tracks every descendant, so nothing survives. With cgroups it kills the whole tree at once; without, it walks /proc and kills descendants, and exits 120 if it cannot confirm they are dead. Commenters note escapes such as spawning through sshd or handing work to systemd.
- **Claim:** corral --wall 30s -- cmd leaves no process of that command running when it finishes.
- **Testable:** no. It is Linux only (cgroups and /proc) and this machine is macOS. Needs: A Linux host or container.
- **Idea on its own:** sound. Leaked background processes from agent shells are real and tree-wide killing fixes most of them.
- **How it would be done:** On a Linux box, run commands that double fork and background a tail, wrapped in the tool, and check for survivors. On macOS an equivalent would need process group tracking with kqueue or a launchd job with AbandonProcessGroup off.
- **Stack already covers:** launchd long-running pollers
- **To fetch:** Corral https://github.com/Cardinal44/corral (The tool.)
- **Field Notes line:** A wrapper that kills every process an agent's command started, using cgroups or a /proc walk, because plain timeouts miss double forks.

### H-0085 Inbound AI receptionist demo line built from the home services voice prompt
2026-10-01, vault, 

- **Mechanism:** A phone number routes inbound calls to a voice-agent platform: speech to text, an LLM with a long system prompt (business hours, services, booking rules), text to speech back, and tool calls that write bookings to a calendar or send an SMS. Retell or Vapi host the loop and Make or n8n handle the follow-up. In the UK, call recording and AI disclosure at the start are needed.
- **Claim:** A home services voice prompt turns into a working inbound receptionist demo line.
- **Testable:** no. It needs a telephony account, a phone number and a voice-agent platform key. Needs: Voice-agent platform account and a UK phone number.
- **Idea on its own:** sound. Inbound handling of missed calls is lawful and the components are mature.
- **How it would be done:** Take one of the free voice prompts, adapt it to a fictional UK trade business, wire a number into a hosted voice-agent platform, and give it a calendar booking tool. Test with scripted calls, including interruptions and unclear requests. A person must play the caller and handle the business owner onboarding.
- **Stack already covers:** ElevenLabs (voice)
- **To fetch:** Retell AI https://www.retellai.com (Hosted voice-agent loop with a free tier.); Vapi https://vapi.ai (Alternative voice-agent platform.); n8n https://github.com/n8n-io/n8n (Self-hosted follow-up workflows.)
- **Missing:** A UK phone number and a real business willing to trial it.
- **Field Notes line:** An inbound AI receptionist is a phone number, a speech loop, a long prompt and a calendar tool call.

### H-0084 What is Expected Goals?
2026-10-01, youtube, https://www.youtube.com/watch?v=tysc21gAT58

- **Mechanism:** Expected goals is a classifier: each shot gets a probability of scoring from features such as location, angle, body part and defender positions, fitted on thousands of historical shots. Usually this is logistic regression or gradient boosting, and team xG is the sum of shot probabilities.
- **Claim:** An equation using data from thousands of similar shots assigns each chance a value between 0 and 1.
- **Testable:** yes. Does a logistic model on distance and angle from StatsBomb open data beat a constant goal-rate baseline on held-out log loss? Queued as P-0046.
- **Idea on its own:** sound. It is a standard, well understood model whose skill can be checked on held-out shots.
- **How it would be done:** Download StatsBomb open data shots, compute distance and angle from the coordinates, fit logistic regression and compare log loss and Brier score against a constant rate on a held-out set. Then add body part and shot type. The result can feed the Pitch desk as a team strength input.
- **Stack already covers:** football-data and a Dixon-Coles paper desk (the Pitch)
- **To fetch:** StatsBomb open-data https://github.com/statsbomb/open-data (Free shot-level event data with coordinates.); scikit-learn https://github.com/scikit-learn/scikit-learn (Logistic regression and scoring.)
- **Field Notes line:** Expected goals is just a shot-level logistic model; fitting one on free open data shows how much distance and angle alone explain.

### H-0083 SEAR: Spoofing Evidence-Grounded Audio Reasoning Benchmark for Audio Language Models
2026-10-01, arxiv, https://arxiv.org/abs/2609.39847

- **Mechanism:** SEAR tests whether audio language models detect deepfake speech for the right acoustic reasons. A four-task question benchmark asks for evidence identification, quantification, verdict and rationale, and BAEA gives a frozen model controlled acoustic measurement tools, fixed or adaptive, comparing against bona fide audio. Feeding misleading evidence lowers both detection and grounding.
- **Claim:** Models give plausible rationales that lack verifiable acoustic evidence, and BAEA-Fixed improves verdicts and rationales.
- **Testable:** no. It needs six audio language models and the benchmark data is not confirmed public. Needs: Audio language model access and the SEAR dataset.
- **Idea on its own:** sound. Making a detector cite measurable evidence is a sound way to test whether its reasoning is real.
- **How it would be done:** Pull the benchmark if released, run a model with and without simple measurement tools (spectral features, pitch, noise floor from librosa), and check whether the cited evidence matches the measured values. This is the detection side only.
- **Stack already covers:** local transcription
- **To fetch:** librosa https://github.com/librosa/librosa (Acoustic measurements as evidence tools.)
- **Field Notes line:** Audio models that call a deepfake often cannot back the call with real acoustic evidence; giving them measurement tools helps.

### H-0082 edenfunf/reelmimic: Show it a video you love. Get a new video in the same style. An AI crew (Claude Code or Codex) plans
2026-10-01, github, https://github.com/edenfunf/reelmimic

- **Mechanism:** It decomposes a reference video into shot lengths, BPM, transitions, colours, framing and camera moves, then writes a storyboard plan for approval. Up to six agents build different segments in parallel through engines such as HyperFrames, and every finished shot is reviewed by a fresh agent, with fixes needing before and after screenshots. Styles are Markdown files.
- **Claim:** A reference video plus a one-line brief yields a new 30 to 60 second video in the same style, in 1 to 3.5 hours.
- **Testable:** no. A real run takes hours of Claude Code usage and the shot analysis step is not clearly separable. Needs: Hours of Claude Code or Codex usage.
- **Idea on its own:** needs-a-run. Separating the builder from the reviewer is sound, but output quality on 2D styles is only shown by the author's samples.
- **How it would be done:** Clone it, feed it a short public-domain clip and a one-line brief, and let it run overnight. Compare the shot analysis with ffmpeg scene detection to see how accurate the breakdown is. The reference should be licensed or self-made, and a person must approve the plan.
- **Stack already covers:** Claude Code with skills and sub-agents, HyperFrames (video compose, captions, render)
- **To fetch:** ReelMimic https://github.com/edenfunf/reelmimic (The tool itself.); painted-animation https://github.com/tuzhechen2005/painted-animation (Hand-painted engine it builds on.)
- **Field Notes line:** A Claude Code crew takes a video apart into shots, rhythm and style, then rebuilds a new one with a fresh agent reviewing every shot.

### H-0080 One pay-as-you-go fal account to run Seedance, Kling, Wan and lip-sync models by API
2026-10-01, vault, 

- **Mechanism:** fal is an inference aggregator: one API key and a queue endpoint per model, where a client submits a job, polls or takes a webhook, and downloads the result file. Video, image and lip-sync models from different labs sit behind one calling pattern billed per second or per generation. It depends on the hosted model being available and on each model's content rules.
- **Claim:** One pay-as-you-go account reaches Seedance, Kling, Wan and lip-sync models by API.
- **Testable:** no. It needs an account, a key and spend. Needs: fal account and API key.
- **Idea on its own:** sound. Aggregator APIs with a uniform submit-and-poll pattern are a proven way to swap models without rewriting code.
- **How it would be done:** Write one small wrapper that takes a model id and a prompt, submits to the queue, polls and saves the file with its cost recorded. Add a table of draft route and final route per video job. A person is still needed for any shot with a real face, which these models refuse.
- **Stack already covers:** HyperFrames (video compose, captions, render), Gemini (stills), HeyGen and Tavus (avatars)
- **To fetch:** fal client https://github.com/fal-ai/fal (Python client for the queue API.)
- **Field Notes line:** One queue-style API fronts many video models, so a script can pick a draft model and a final model per job.

### H-0079 Finally, The CORRECT Way to Run Local AI on a Mac
2026-10-01, youtube, https://www.youtube.com/watch?v=JpJaEPGzPF4

- **Mechanism:** oMLX wraps Apple's MLX LM library with an OpenAI-style server and a two-tier KV cache: hot blocks stay in RAM, cold blocks are written to SSD as safetensors under least-recently-used eviction. Previously seen prompt prefixes are restored across requests and server restarts rather than recomputed, which cuts time to first token on long agent contexts.
- **Claim:** SSD-persisted prefix cache makes cold starts and long contexts faster than plain MLX LM on a Mac.
- **Testable:** yes. With a small public MLX model, is time to first token on a 4k-token repeated prefix after a server restart at least 2x faster than the first cold run? Queued as P-0045.
- **Idea on its own:** needs-a-run. Prefix caching is a sound technique, but the speedup on a small model on this Mac is the question.
- **How it would be done:** Install oMLX, load a small MLX model, send a 4k-token prompt, time it, restart the server and send it again. Compare against the Ollama qwen already here for the same prompt. If the gain holds, point child agents at it for long-context reading jobs.
- **Stack already covers:** Ollama with a qwen model, local transcription
- **To fetch:** oMLX (The server under test; find the repo via the video description.); mlx-lm https://github.com/ml-explore/mlx-lm (The underlying library and baseline.)
- **Field Notes line:** A Mac local-model server that parks its prompt cache on the SSD so restarts skip recomputing long prefixes.

### H-0078 Learning from Research: Toward Lifelong Agent Harness Evolution
2026-10-01, arxiv, https://arxiv.org/abs/2609.40169

- **Mechanism:** ScholarEvolve keeps the model fixed and evolves the agent harness (tool use, memory, task execution). It mines new papers, topic-models them into improvement strategies per harness module, has a coding agent implement each, then evaluates combinations on the benchmark and keeps winners. New publications can be fed in over time.
- **Claim:** Raises Qwen3.5-27B goal completion on AppWorld Challenge from 49.6% to 63.6%, and GPT-5.4-mini pass@1 on Tau2-Bench Telecom from 72.7% to 81.9%.
- **Testable:** no. It needs the AppWorld and Tau2 harnesses, model runs and hours of compute, not a 30 minute keyless check. Needs: Benchmark harnesses and model access.
- **Idea on its own:** needs-a-run. Evaluate-and-keep loops do improve harnesses, but gains from paper mining versus plain search are not isolated here.
- **How it would be done:** Take a small harness Proteus owns (the harvester or the probe loop), define a score, then have a child agent propose changes drawn from recent arXiv abstracts and keep only those that raise the score on a fixed task set. The paper feed already exists through the arXiv pull. A held-out set is needed so the loop does not overfit.
- **Stack already covers:** Claude Code with skills and sub-agents, launchd long-running pollers
- **To fetch:** AppWorld https://github.com/StonyBrookNLP/appworld (Benchmark used to score harness changes.)
- **Missing:** A scored task set for Proteus's own harness.
- **Field Notes line:** An agent harness that reads new research papers and rewrites itself with them lifted a small model's task score by 14 points.

### H-0077 nanaism/yomiyasu: AI生成の日本語を自然な日本語へ推敲するAgent Skill / Agent Skill for Refining AI-Generated Japanese into Natural Japanese
2026-10-01, github, https://github.com/nanaism/yomiyasu

- **Mechanism:** It is a prompt-only Agent Skill: seven rewrite principles (restore subject and object, dissolve inanimate subjects, replace metaphor verbs with literal actions, cut preambles, preserve numbers, limit sentence length to about 30 to 45 characters and 0 to 2 commas) loaded into the agent as a skill file. The numeric targets make the output checkable by a simple script. It addresses a known failure of ban-list prompts, where banned words are swapped for new vague ones.
- **Claim:** The skill rewrites AI-sounding Japanese into natural, dense Japanese, validated against open-licence corpora.
- **Testable:** no. Judging naturalness of Japanese needs a native reader, and Proteus has no Japanese ground truth. Needs: A Japanese reader to judge output.
- **Idea on its own:** sound. Structural rules with measurable limits beat word ban lists, and the same pattern would work for English house style.
- **How it would be done:** Copy the skill structure, replace the Japanese rules with English equivalents (name the actor, no abstract subjects, sentence length cap, no filler openers), and run it over a few drafts. A small script can then count sentence length and comma density as a regression check. A native editor would be needed to confirm it reads naturally.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** yomiyasu https://github.com/nanaism/yomiyasu (Reference skill layout and rule set to adapt.)
- **Field Notes line:** A skill that fixes AI-sounding prose by enforcing sentence structure rules with numeric targets, not by banning words.

### H-0076 Show HN: Open-source model routing for coding agents at Astra-level performance
2026-10-01, hn, https://news.ycombinator.com/item?id=49911500

- **Mechanism:** A router sits between a coding agent and several LLM back ends and picks a model per step. It is a trained routing model (RL plus a prior, with an HMM mentioned in comments that assigns the session to a model bucket) that weighs model capability, price and prompt-cache state, since switching model throws away the cache. Savings come from sending easy edits to a cheap model and hard debugging to the strong one.
- **Claim:** Router 2.0 matches GPT-6 Astra pass rates on Terminal Bench 4.0 and SWE Atlas at about 52 to 54 percent of the cost and 2.2 to 2.5x faster.
- **Testable:** no. It needs paid model keys on several providers and the benchmarks are the vendor's own, so nothing can be checked keyless tonight. Needs: API keys for two or more model providers.
- **Idea on its own:** needs-a-run. Cost-aware routing is plausible but the headline numbers are self-reported on the vendor's benchmark runs.
- **How it would be done:** Install the open-source router, point a coding agent at it, and run the same 20 tasks through it and through the single strong model, logging cost, time and pass rate. The comparison needs several provider keys and a task set Proteus can score itself. A crude rule-based router (cheap model for edits under N lines) is a useful baseline to see how much the trained part adds.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Weave Router https://github.com/weave-os/router (The open-source router to run against a baseline.)
- **Missing:** A scored task set and keys for the cheap and strong models.
- **Field Notes line:** A trained router that hands easy coding steps to cheap models and hard ones to the strong one claims half the cost at equal pass rate, with cache loss priced in.

### H-0075 Adapt the web design CLAUDE.md for phone-first UK local business sites
2026-10-01, vault, 

- **Mechanism:** A CLAUDE.md file sits in a website project and pins design rules (mobile-first layout, tap-target sizes, local trust signals, click-to-call, schema.org LocalBusiness markup) so every Claude Code session builds pages to the same standard. Adapting it for UK local trades means swapping US conventions for UK ones (postcodes, VAT, UK phone formats, Google Business Profile). The output is static HTML or a small framework site that can be checked against Lighthouse mobile scores.
- **Claim:** A web design CLAUDE.md steers Claude Code to produce consistent, mobile-first small business sites.
- **Testable:** no. The source file is behind the vault's course extract and the real question (does a rule file improve sites) needs a judged build, not a 30 minute run.
- **Idea on its own:** sound. Persistent rule files reliably shape agent output, and mobile performance is measurable with free tools.
- **How it would be done:** Write or take the rule file, adapt it to UK local business conventions, then have Claude Code build a sample site for a fictional plumber from a short brief. Score it with Lighthouse mobile and a tap-target check, then iterate the rules where scores drop. Real trade businesses would need photos, reviews and a domain, which is a human job: someone has to collect them and approach the owner.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** Lighthouse CLI https://github.com/GoogleChrome/lighthouse (Free mobile performance and accessibility scoring to judge generated sites.)
- **Missing:** The real client photos, reviews and domain access for any actual business.
- **Field Notes line:** A single CLAUDE.md rule file can hold a whole web design standard, so phone-first local business sites come out consistent every time.

### H-0073 echris6/motion-video-kit: Claude Code skill kit for premium AI-assisted business videos: independent critic loop, motion
2026-09-30, github, https://github.com/echris6/motion-video-kit

- **Mechanism:** A Claude Code skill that makes commercials through a builder-versus-critic loop: a fresh critic agent judges the actual render, items are verified one by one and a ledger records findings. It pairs motion rules from 28 launch films with measurable checks (frozen-time detection, loudness via ffmpeg ebur128, contrast, brand colour) scripted in Python. Rendering is HyperFrames or Three.js.
- **Claim:** Premium launch-style business videos from an independent-critic quality loop.
- **Testable:** yes. Does the kit's frozen-time and loudness script run on a local ffmpeg-generated test video and report a loudness figure in LUFS and a frozen-frame count? Queued as P-0044.
- **Idea on its own:** sound. Independent critics plus measured checks address the known self-grading failure of generate-and-review loops.
- **How it would be done:** Clone the repo, copy the skill into place and run its measurement scripts on a render. Wire the critic prompts into a sub-agent that never sees the builder's reasoning. Use HyperFrames for output. The business playbook is where a person picks verticals and price anchors.
- **Stack already covers:** HyperFrames (video compose, captions, render), Claude Code with skills and sub-agents, ElevenLabs (voice)
- **To fetch:** motion-video-kit https://github.com/echris6/motion-video-kit (The skill and measurement scripts.); ffmpeg ebur128 filter https://ffmpeg.org/ffmpeg-filters.html#ebur128-1 (Loudness measurement the scripts need.)
- **Field Notes line:** A video skill kit ships scripted render checks for frozen frames and loudness, plus a separate critic agent that judges the real render.

### H-0072 Show HN: Parrot – Open-Source Smart Meeting Recorder with Co-Pilot on Mac
2026-09-30, hn, https://openparrot.app

- **Mechanism:** A Mac app records system audio and microphone, transcribes locally or via Deepgram, and runs a co-pilot that matches questions heard in the call against the user's uploaded files and shows answers on screen. Local mode needs no account or API call; cloud mode hooks Claude and Deepgram. A thread reports echo from duplicate audio streams.
- **Claim:** Open-source, local-first meeting recorder with a retrieval co-pilot.
- **Testable:** no. It is a Mac GUI app needing build and live call audio. Needs: Xcode build and audio permissions..
- **Idea on its own:** sound. System audio capture plus local transcription and retrieval over user files is a proven, simple pattern.
- **How it would be done:** Capture system audio and mic with ScreenCaptureKit, transcribe with a local Whisper model, embed the uploaded files and match detected questions to passages. Export transcripts as markdown, which a commenter asks for. Local transcription is already in the stack.
- **Stack already covers:** local transcription, Ollama with a qwen model
- **To fetch:** Parrot https://github.com/turantekin/Parrot (Source for the capture and co-pilot design.)
- **Field Notes line:** A local-first Mac recorder listens to calls and answers questions from your own files, with no account.

### H-0071 Partnership ads run through a local client's own social handle
2026-09-30, vault, https://www.instagram.com/reel/DcWYAsmtqFr/

- **Mechanism:** Meta's Partnership Ads let a business run paid ads that appear from a creator or client's own Instagram handle after the handle owner grants permission in Meta's tools. The ad borrows the page's local trust while the advertiser pays for reach. It depends on permission being granted on-platform and on the ad carrying the platform's paid partnership label.
- **Claim:** Ads run through a local client's own handle carry more local trust than a brand page.
- **Testable:** no. Needs a Meta ad account and a client handle. Needs: A Meta Business account and a consenting client..
- **Idea on its own:** sound. It is a sanctioned platform feature with consent and a visible label.
- **How it would be done:** Agree a written permission with the local business, get the handle's admin to grant partnership access in Meta Business Suite, then produce and label the creative and run a small test budget. Record results in a shared sheet. Content can be made with HyperFrames; the account setup and consent step need a person.
- **Stack already covers:** HyperFrames (video compose, captions, render), ElevenLabs (voice)
- **Missing:** A consenting local business willing to grant handle access.
- **Field Notes line:** Partnership ads let a business borrow a local client's own handle with permission, labelled, which is legal and sellable as a service.

### H-0070 How to Make PUMP.FUN CALLOUTS (Step by Step) #pumpfun #crypto #memecoin
2026-09-30, youtube, https://www.youtube.com/watch?v=MA6Ecac4P-Y. Vault verdict on the vendor exists (vault verdict: pump.fun); mechanism recorded, vendor not re-judged.

- **Mechanism:** A pump.fun feature where a user posts a short call-out on a coin after buying a small amount, and earns a share of trading fees on volume that call drives. A daily pool is paid out in USD in proportion to volume attributed to each caller, so payout rewards calling early. The video claims the top 50 split $700,000 in two weeks, with most calls on coins under 100K market cap.
- **Claim:** Top 50 callers split $700,000 in two weeks; one earned $6,800 from almost 2,500 calls.
- **Testable:** no. Payouts and call attribution are not visible from a keyless public endpoint and the figures are a creator's claim. Needs: A pump.fun account and a source of call-out data..
- **Idea on its own:** needs-a-run. The incentive is real but it rewards volume drivers, so callers are paid even when followers lose money.
- **How it would be done:** Measure it from the outside: log call-outs and the coin's later volume and price, and check whether early callers' coins outperform launches with no call-outs. Pay attention to whether the payout creates a pump incentive in the Grinder's data. No account is needed for the observational version if call-out data is public.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers, Solana paper desk (the Grinder)
- **Missing:** Public access to call-out timestamps and payout data.
- **Field Notes line:** Pump.fun pays a daily pool to people who post early call-outs, which turns attention itself into a fee-share incentive.

### H-0069 UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training
2026-09-30, arxiv, https://arxiv.org/abs/2609.38043

- **Mechanism:** An evaluation layer over tau-bench scores the simulated user, not the agent, against the private instructions it was given, using task-grounded rubrics scored independently of agent success. Holding the agent fixed and swapping the user model changes reward by 15.2 points. The main failure is premature disclosure, which leaves reward unchanged but reduces the agent's tool calls.
- **Claim:** 24.4% of successful episodes contain a user-simulator violation, and proxy choice shifts reward by 15.2 points.
- **Testable:** no. Needs tau-bench, a frontier agent and paid calls. Needs: tau-bench and model API spend..
- **Idea on its own:** sound. Scoring the simulator against its own instructions is a cheap, obvious missing control.
- **How it would be done:** Take transcripts from a benchmark, write rubric items from each task's hidden user instructions and have a judge model score each transcript independently of reward. Report the violation rate and compare proxies on cost. Applies to any agent test Proteus builds with a simulated user.
- **Stack already covers:** Claude Code with skills and sub-agents, Ollama with a qwen model
- **To fetch:** tau-bench https://github.com/sierra-research/tau-bench (The benchmark family the layer sits over.)
- **Field Notes line:** Agent benchmark scores swing 15 points depending on the simulated user, and a quarter of passes hide a user mistake.

### H-0068 rehan-remade/universal-modder: Point Claude at any game. Skills, tools and the fal MCP that let Claude Code mod almost a
2026-09-30, github, https://github.com/rehan-remade/universal-modder

- **Mechanism:** A Claude Code plugin of skills and a Python CLI that runs a fixed loop: scan for installed games and fingerprint engine, anti-cheat and save folders, choose a modding route, read decompiled code, build a slice, generate assets with fal, test in the running game and record. It leans on existing tools (ILSpy, Ghidra, Frida, Cheat Engine, Blender) and playbooks per engine. Asset generation needs a fal key.
- **Claim:** Claude Code can mod almost any PC game you own, from recon to showcase video.
- **Testable:** no. Needs a fal key for assets, owned games on the machine, and is Windows-first. Needs: A fal API key, a game install and Blender..
- **Idea on its own:** sound. The loop mirrors how human modders work and each step uses established reverse-engineering tools.
- **How it would be done:** Install the plugin, run the scan step to fingerprint installed games, then let the skill write a modding plan. Build one slice with the engine's playbook and test it in the running game with screenshots. Assets need a generator; a local substitute would replace fal. Anti-cheat titles need a human to judge what is safe.
- **Stack already covers:** Claude Code with skills and sub-agents, HyperFrames (video compose, captions, render), Gemini (stills), ElevenLabs (voice)
- **To fetch:** universal-modder https://github.com/rehan-remade/universal-modder (The plugin and um CLI.); ILSpy https://github.com/icsharpcode/ILSpy (Decompiler for .NET games.); Ghidra https://github.com/NationalSecurityAgency/ghidra (Native reverse engineering.)
- **Field Notes line:** A Claude Code plugin packages game modding as recon, route, read code, build, test, record, with a scanner that fingerprints engines.

### H-0066 Consistent AI character content with clear AI disclosure
2026-09-30, vault, https://www.instagram.com/p/Ddr0Ds3MsI5/

- **Mechanism:** A fixed character is kept consistent across posts by generating from a locked reference image set or a fine-tuned image model, then animating and voicing it. Disclosure is added by labelling each post with the platform's AI-content label and a visible caption line, and by keeping the character to entertainment rather than endorsement. Platforms detect undisclosed synthetic media through provenance metadata such as C2PA and classifiers.
- **Claim:** A branded AI character can post consistent content at volume.
- **Testable:** no. It is a content production job, not a script with a yes or no answer tonight.
- **Idea on its own:** sound. Disclosed synthetic characters are lawful and platform-sanctioned when they do not pose as ordinary consumers recommending products.
- **How it would be done:** Generate a reference sheet of the character with Gemini stills, then produce scenes with image-to-video and voice with ElevenLabs. Compose and caption in HyperFrames, apply the platform AI label on upload and add a fixed disclosure line in the caption. Keep scripts to entertainment and explicit sponsor labels. A person would review each post for label compliance and likeness drift.
- **Stack already covers:** Gemini (stills), ElevenLabs (voice), HeyGen and Tavus (avatars), HyperFrames (video compose, captions, render)
- **To fetch:** C2PA c2patool https://github.com/contentauth/c2patool (Embed and inspect provenance metadata for disclosure.)
- **Missing:** A compliance check for UK DMCC and platform labelling rules on each post.
- **Field Notes line:** A consistent AI character can be run openly by locking reference stills and labelling every post as AI, entertainment only.

### H-0064 MotorMind: Scaffolding General Vision Language Models for Zero-Shot Robot Manipulation
2026-09-30, arxiv, https://arxiv.org/abs/2609.38078

- **Mechanism:** A harness lets a general vision-language model drive a robot by proposing mid-level actions (move to, grasp, place) that a deterministic controller executes, with feedback returned to the model. Asynchronous monitoring watches execution while background memory updates keep context, and no coding agent, action expert or SAM3 grounding is used. Scores come from LIBERO-PRO simulation and a real xArm6.
- **Claim:** 66.7% success on base LIBERO-PRO versus at most 13.3% for prior zero-shot methods, and 95% on a real xArm6.
- **Testable:** no. Needs a robot or the LIBERO-PRO simulator and a paid VLM. Needs: A robot or simulator and a frontier VLM key..
- **Idea on its own:** needs-a-run. Numbers are self-reported on a benchmark the authors chose, but the harness design is cheap to replicate in principle.
- **How it would be done:** Define a small action vocabulary, wrap a simulator or arm in deterministic executors, and loop the VLM over camera frames with a monitor thread flagging failures. Would need the LIBERO-PRO simulator and GPU. No relevance to current desks except as a harness pattern.
- **To fetch:** LIBERO https://github.com/Lifelong-Robot-Learning/LIBERO (Simulation benchmark the paper builds on.)
- **Missing:** A robot or GPU simulator.
- **Field Notes line:** A plain VLM plus a thin mid-level action layer and async monitor beat specialised robot policies zero-shot, by a wide margin.

### H-0063 Louis-CFM/coucou: A tiny friend that lives in your notch (macOS) or at the top of your screen (Windows) and keeps an eye
2026-09-30, github, https://github.com/Louis-CFM/coucou

- **Mechanism:** A native menubar app that shows Claude Code sessions in the MacBook notch. It receives events from the running sessions (tool calls, permission requests) and renders Allow and Deny buttons that answer the permission prompt, which points to Claude Code's hooks being used as the event channel. Keys for integrations sit in the macOS Keychain and there is no telemetry.
- **Claim:** See every Claude Code session and approve permissions from the notch; 1,099 stars in three days.
- **Testable:** no. It is an unnotarised Swift GUI that needs Xcode and a build, and its value is visual. Needs: Xcode 16 and XcodeGen..
- **Idea on its own:** sound. Hook-driven approval forwarding is a real, supported pattern for remote sign-off.
- **How it would be done:** A hook script posts each permission request to a local socket or HTTP endpoint and waits for a decision. A small UI reads that endpoint and writes the answer back. Proteus could reuse only the hook-to-decision pattern, not the UI, for the unattended-decide hook.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** coucou https://github.com/Louis-CFM/coucou (Source to read for the hook event format.)
- **Field Notes line:** Claude Code permission prompts can be answered from outside the terminal by a hook, and someone has made it a notch app.

### H-0062 Launch HN: Magnitude (YC S25) – Self-optimizing inference engine for agents
2026-09-30, hn, https://github.com/magnitudedev/magnitude

- **Mechanism:** An inference engine that compiles and autotunes its GPU kernels on the user's own device before loading a model, so one parametrised kernel set reaches hardware-specific speed on Mac, Linux and Windows. It writes tuned kernels only for popular open-weight model families and is built for long, concurrent agent sessions on a machine that is also in use. The speed claim rests on a chart against llama.cpp; the thread asks for configuration and MLX comparisons.
- **Claim:** Up to 2x faster than llama.cpp on the same hardware, for local agents.
- **Testable:** no. A fair test needs a multi-GB model download and a matched llama.cpp configuration, which does not fit 30 minutes. Needs: Model weights and time to match llama.cpp settings..
- **Idea on its own:** needs-a-run. Per-device autotuning is proven in other compilers, but the 2x figure has no published method.
- **How it would be done:** Install the release binary, pull the same quantised qwen model Ollama already uses, and run identical prompts through both with fixed context length and thread count. Measure tokens per second for prefill and decode, and run two sessions at once to test the concurrency claim. Compare against MLX as the thread asks. No hiring needed.
- **Stack already covers:** Ollama with a qwen model
- **To fetch:** Magnitude https://github.com/magnitudedev/magnitude (The engine under test.); llama.cpp llama-bench https://github.com/ggml-org/llama.cpp (Baseline benchmark tool with fixed settings.)
- **Field Notes line:** Magnitude tunes its own kernels on your machine at first run, claiming double llama.cpp speed, but the benchmark is one image.

### H-0061 Learning crypto research from a source with an independently verifiable track record
2026-09-30, vault, https://cryptonary.com/landing-100x-chaser

- **Mechanism:** Score a crypto research source by reconstructing its calls as dated entry and exit pairs, then pricing each from public candle data at the time of the call rather than at the peak. The moving parts are a timestamped archive of each call (screenshots, posts, archive.org copies), a price history source, and a fixed exit rule applied to every call, compared with a baseline such as holding the same basket.
- **Claim:** A source's track record can be checked independently if you log audited entries and exits instead of quoting peak gains.
- **Testable:** no. No source with a capturable call history has been named, so there is nothing to score tonight. Needs: A named source with timestamped, archived calls..
- **Idea on its own:** sound. Fixed-rule entry and exit scoring against a baseline is the standard way to strip survivorship and peak bias from any tipster.
- **How it would be done:** Pick a source that publishes dated calls and snapshot them to an archive at the time they appear. For each call, pull the price at the call timestamp from GeckoTerminal or DexScreener history and apply one pre-declared exit rule (for example 24h, 7d, 30d). Net off slippage and fees, then compare the book with buy-and-hold on the same tokens. The Grinder already has the paper-desk plumbing, so the scoring is a thin layer on it. A hired person would only be needed to capture calls from paywalled or members-only channels.
- **Stack already covers:** GeckoTerminal, DexScreener and rugcheck readers, Solana paper desk (the Grinder), keyless YouTube search and transcript pipeline
- **To fetch:** Wayback Machine CDX API https://archive.org/help/wayback_api.php (Independent timestamps for when a call was published.)
- **Missing:** A source that actually publishes timestamped calls in a capturable form.
- **Field Notes line:** Judge a crypto caller by fixed-rule entry and exit pairs priced from public candles, not by their best-ever multiple.

### H-0059 Barty-Bart/motion-graphics: Motion-graphics skills for Claude Code and Codex.
2026-09-29, github, https://github.com/Barty-Bart/motion-graphics

- **Mechanism:** Each clip is a small HTML file on a shared engine where every frame is a pure function of time, with springs as closed-form step responses and a sum of one spring per target change. Headless Chromium via Playwright captures four sub-frames per frame across a 180 degree shutter, and ffmpeg blends them into motion blur. A skill plans clips from a transcript with estimated word timings, then renders MP4 or transparent ProRes 4444.
- **Claim:** Given a video and a transcript, Claude Code plans, animates and renders motion-graphic B-roll timed to the words.
- **Testable:** yes. Does the shipped opus-aoe2 example render locally through Playwright and ffmpeg, and are two renders of the same clip byte-identical? Queued as P-0038.
- **Idea on its own:** sound. Time-pure frames make any frame renderable alone and blur by sub-frame averaging is a standard, correct technique.
- **How it would be done:** Clone the repo, run the example clips through its Playwright capture and ffmpeg blend, then hash two renders to test determinism. To use it for the clipping service, feed it a transcript and let the plan table choose cutaways versus side panels, then compare against what HyperFrames produces for the same script. The part worth borrowing is the closed-form spring engine and the 180 degree shutter blend, which could be ported into a HyperFrames composition.
- **Stack already covers:** HyperFrames (video compose, captions, render), Claude Code with skills and sub-agents, local transcription
- **To fetch:** motion-graphics https://github.com/Barty-Bart/motion-graphics (The skill, engine and worked example.); Playwright https://github.com/microsoft/playwright (Headless Chromium frame capture.); ffmpeg https://ffmpeg.org/ (Sub-frame blending and ProRes 4444 encoding.)
- **Field Notes line:** motion-broll renders animation as pure functions of time, with motion blur from four blended sub-frames per frame; same idea as HyperFrames' seek-safe rule.

### H-0058 Post-production for businesses that have long-form content but cannot cut it into short-form
2026-09-29, vault, https://www.instagram.com/reel/DcU_MNWtIkg/

- **Mechanism:** A business already publishes long-form video such as talks, podcasts or site footage. A service takes that footage, picks the strongest moments, cuts them into short vertical clips with captions and a hook, and supplies them on a monthly retainer for the client to post. The engine is transcription to find moments, an editor or composer to cut and caption, and a review step, with the client's leads as the measure of success.
- **Claim:** Cutting a company's long-form content into short-form that brings leads underpins an agency that reports 747,000 dollars personal income in 12 months, unaudited.
- **Testable:** no. The value is in a client engagement, and a keyless run would only test the cutting pipeline, not the idea. Needs: A client with long-form footage and posting access..
- **Idea on its own:** sound. Businesses with long-form content and no editing capacity are a real, standing need, and the claimed earnings are marketing rather than evidence.
- **How it would be done:** Transcribe the client's footage locally, have a child rank candidate segments by hook strength and self-contained meaning, then cut each with ffmpeg and compose captions and framing in HyperFrames. Produce a batch per month and send it for approval before posting. A person handles the client conversation, the choice of what suits the brand, and any compliance sign-off. A live test case is a client with a single piece of footage that already worked.
- **Stack already covers:** HyperFrames (video compose, captions, render), local transcription, ElevenLabs (voice), Claude Code with skills and sub-agents
- **To fetch:** ffmpeg https://ffmpeg.org/ (Cutting, cropping to vertical, and burning captions.); OpusClip alternatives: ClipsAI https://github.com/ClipsAI/clipsai (Open-source library that finds clip-worthy segments in long video.)
- **Missing:** A first paying client and a portfolio of before and after clips.
- **Field Notes line:** Clipping as a service: transcribe a business's long video, pick the moments, cut captioned shorts on a retainer; the stack already owns the cutting half.

### H-0056 Harness Learning Enables Generalizable Test-Time Adaptation
2026-09-29, arxiv, https://arxiv.org/abs/2609.35738

- **Mechanism:** The agent is split into a solver model and a harness, the program that orchestrates its calls and tools. A separate proposer model is trained with reinforcement learning to rewrite the harness code using feedback from executing it, with the reward being the task score of the revised harness. At test time the proposer refines the harness over several runs on a new task with no weight updates. Experiments are on reasoning and multi-hop question answering.
- **Claim:** A trained proposer that revises an agent's harness from execution feedback improves revision quality and transfers to unseen tasks.
- **Testable:** no. It needs reinforcement learning training of a proposer model, which no keyless 30 minute run can reproduce. Needs: GPU training and a model to fine-tune..
- **Idea on its own:** needs-a-run. Revising code from execution feedback is plausible, but gains are shown only on reasoning and multi-hop QA and revision sequences help inconsistently.
- **How it would be done:** A cheap version needs no training: after each nightly run, give a child the run log and the current skill or script, ask for one revision, and keep it only if a fixed score on a small test set rises. That copies the loop without the reinforcement learning. The paper's own value would be the reward design and the test sets, which can be read from the paper and code if released.
- **Stack already covers:** Claude Code with skills and sub-agents, launchd long-running pollers
- **To fetch:** arXiv 2609.35738 https://arxiv.org/abs/2609.35738 (Check for a linked code release and the evaluation sets.)
- **Missing:** A trained proposer model; nobody outside the authors has one.
- **Field Notes line:** Harness learning trains a model to rewrite an agent's own scaffolding from run feedback, using edits to code as the update step instead of weights.

### H-0055 CaptureGrubEnchant/SolidWorks: SolidWorks MCP Server connects an AI assistant to a running SolidWorks instance. Sketch, 
2026-09-29, github, https://github.com/CaptureGrubEnchant/SolidWorks

- **Mechanism:** An MCP server in Node drives a running SolidWorks over Windows COM using the winax bridge. A parameter counter routes calls: 12 or fewer arguments go straight through COM, and 13 or more, such as FeatureExtrusion3 with over 20, are turned into a generated VBA macro that SolidWorks runs itself, with fallback on failure. It walks the feature tree rather than selecting by name. The README admits most tools are unvalidated on a live instance.
- **Claim:** Lets an AI assistant sketch, extrude, fillet and export STEP or STL in a running SolidWorks.
- **Testable:** no. It needs Windows and a licensed SolidWorks, and the install steps pipe scripts from unrelated domains that should not be run. Needs: Windows, a SolidWorks licence, and a trustworthy install source..
- **Idea on its own:** sound. Routing awkward many-argument COM calls through generated macros is a genuine workaround, though this repo's install path points to unrelated domains and warns most tools are untested.
- **How it would be done:** The pattern applies to any desktop CAD or Office app with a COM or scripting API: expose small tools over MCP, count parameters, and emit a macro for the heavy calls. Building it would mean writing a handful of tools against a real instance and validating each, which the repo has not done. Read the source only from the GitHub repo, not the zip or the PowerShell one-liner, since those come from other domains.
- **Stack already covers:** Claude Code with skills and sub-agents
- **To fetch:** FreeCAD https://github.com/FreeCAD/FreeCAD (Free CAD with a Python API on macOS, a safe place to try the same agent-drives-CAD idea.); CadQuery https://github.com/CadQuery/cadquery (Pure Python parametric CAD that an agent can drive with no GUI or licence.)
- **Missing:** A validated, safely distributed SolidWorks bridge does not exist here; this one's install chain is suspect.
- **Field Notes line:** A SolidWorks MCP server routes long CAD calls through generated VBA because COM bridges choke past 12 arguments; treat its install script as hostile.

### H-0054 Media-buying commission taken as a share of a brand's ad budget
2026-09-29, vault, 

- **Mechanism:** An operator buys or places ads on a brand's behalf and takes a percentage of the ad budget as fee, here quoted as 20 percent of a 100k budget. The service is allocation and optimisation: choosing channels, creatives and audiences, then reporting results, with the brand paying platforms directly or through the agency. Revenue scales with spend managed, not with hours, so it depends on the operator's record of return on ad spend.
- **Claim:** Media buying for a brand is paid at 20 percent of a 100k ad budget.
- **Testable:** no. It is a service arrangement with clients and ad accounts, and there is nothing to run keyless. Needs: A client with an ad budget and ad platform account access..
- **Idea on its own:** needs-a-run. Commission on spend is a standard agency model, but the 20 percent figure is high against typical 10 to 15 percent norms and rests on a claim nobody has audited.
- **How it would be done:** The work is: get access to the client's ad accounts, set up tracking, launch tests across creatives, read the results daily and move budget toward what converts, then send a weekly report. A script can generate creative variants and pull platform reports, but the judgement of where to shift money and the client relationship is a person's job. A hired media buyer would run the accounts, with the agency owning creative production, which is where the video stack fits.
- **Stack already covers:** HyperFrames (video compose, captions, render), ElevenLabs (voice), HeyGen and Tavus (avatars), Claude Code with skills and sub-agents
- **To fetch:** Meta Ad Library https://www.facebook.com/ads/library/ (Public data for seeing what a brand's competitors run before pitching.)
- **Missing:** A track record of return on ad spend on real budgets, which nobody in the stack holds.
- **Field Notes line:** A media buyer's fee is a cut of ad spend, so income scales with budget managed; the quoted 20 percent of 100k is the kit's number, unverified.

### H-0052 TokenCast: Forecasting Token Consumption During LLM Agent Execution
2026-09-29, arxiv, https://arxiv.org/abs/2609.35760

- **Mechanism:** TokenCast splits an agent run into execution segments and learns for each segment two numbers: its own token use and how much context it adds. Composing segments gives a cumulative forecast that includes the re-read cost, since every later call re-sends earlier context. As the run proceeds, observed segments replace guesses and the forecast updates with no extra LLM call. It is trained on traces from SWE-bench Verified and three other suites across six models.
- **Claim:** Forecasts agent token use with 14.5% lower mean absolute error than the best comparator, and budget control uses 21.3% fewer tokens at matched completion.
- **Testable:** yes. Does the TokenCast repo ship trace data and a script that reproduces a mean absolute error on one suite within a factor of two of the paper's figure? Queued as P-0037.
- **Idea on its own:** sound. Context re-read makes agent cost superlinear in steps, so a running cumulative forecast with segment-level features is a reasonable design and is cheap to check against traces.
- **How it would be done:** Clone the repo, find the released traces and the evaluation script, and run the baseline and TokenCast on one suite to compare error. To use it here, log per-call input and output tokens from the sub-agent transcripts Proteus already parses for USAGE.md, cut them into segments by tool call, and fit the same composition on Proteus's own runs. The output would be a nightly forecast against a call cap, which feeds the probe loop's budget check.
- **Stack already covers:** Claude Code with skills and sub-agents, launchd long-running pollers
- **To fetch:** TokenCast https://github.com/DEFENSE-SEU/TokenCast (The paper's code and evaluation scripts.); SWE-bench Verified https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified (The task suite whose traces the paper evaluates on.)
- **Field Notes line:** TokenCast predicts an agent's total token bill mid-run in 33 milliseconds by adding up per-step costs plus the re-read tax; the code is public.

### H-0051 AgentSystemLabs/agent-office: A cartoon 3D office where your team hires Claude Code workers at desks, shares live termin
2026-09-29, github, https://github.com/AgentSystemLabs/agent-office

- **Mechanism:** A Node server spawns Claude Code, Codex or OpenCode CLIs inside pseudo-terminals per worker, one git worktree per task, and streams each terminal over a websocket to a browser client drawn as a 3D office. Status (needs input, finished) is inferred from the terminal and shown as an animated worker. GitHub issues and PRs come from the gh CLI and are pinned to boards, and the same state is exposed in a 2D /lite view for phones.
- **Claim:** A shared 3D office where a team runs Claude Code workers at desks, shares live terminals and tracks GitHub issues and PRs.
- **Testable:** no. It needs a signed-in agent CLI and gh auth, and installs through a curl-pipe-bash script, none of which fit a keyless sandbox run. Needs: A signed-in agent CLI and GitHub CLI login..
- **Idea on its own:** needs-a-run. The useful part, a pty-per-agent dashboard with a longest-waiting queue, is sound, but the author warns it is one person's workflow and changes weekly.
- **How it would be done:** The transferable piece is a small supervisor: launch each agent in a pty with tmux or node-pty, give each its own git worktree, and detect the waiting state from terminal output or hooks. Expose the list over a tiny web page with a 'longest waiting first' sort. That can be built in an evening without the 3D layer. Reading docs/how-it-works.md would show how they detect the waiting state, which is the one hard part.
- **Stack already covers:** Claude Code with skills and sub-agents, launchd long-running pollers
- **To fetch:** agent-office https://github.com/AgentSystemLabs/agent-office (Read docs/how-it-works.md for the waiting-state detection.); node-pty https://github.com/microsoft/node-pty (Pseudo-terminal spawning for a home-built supervisor.); tmux https://github.com/tmux/tmux (Simplest way to keep many agent sessions alive and inspectable.)
- **Missing:** Nobody has a reliable, agent-agnostic signal for 'this agent is waiting for a human'.
- **Field Notes line:** Agent Office turns parallel coding agents into desks in a 3D room, with a worktree each and a ding when one needs you; the idea is the queue, not the cartoon.

### H-0049 Join for one month with Skool neptune, transcribe the classroom into Education/Courses/ai-video-bootcamp, cancel before 
2026-09-29, vault, 

- **Mechanism:** A paid Skool community holds its course as a classroom of video lessons. The idea is to join for a single billing month, pull each lesson's video, transcribe it locally, and file the transcripts as notes so the content can be searched and mined by agents after the membership ends. It depends on the classroom videos being streamable to a logged-in browser session, and on local transcription turning them into text at a fraction of real time.
- **Claim:** A nine dollar a month AI video course with nine phases can be extracted into text and cancelled before renewal.
- **Testable:** no. The classroom sits behind a paid login and the pull needs an interactive browser session, so nothing can be run keyless tonight. Needs: A paid Skool membership and an interactive logged-in browser session..
- **Idea on its own:** sound. Transcribing lessons you paid for into private notes is a plain learning workflow, provided the transcripts stay private and are not republished.
- **How it would be done:** Join, then in an interactive browser session list every lesson in the classroom and record each video URL or stream manifest. Download each video the platform already serves to the member, run local transcription on the audio track, and write one markdown note per lesson with the phase and title as headings. Hand batches of transcripts to Haiku or Sonnet children to digest into a mechanism summary per phase, and keep only the digests in the shared notes. Set a calendar stop before day 28 so the cancel happens with a margin. A person would only be needed for the login and the cancel click.
- **Stack already covers:** local transcription, Claude Code with skills and sub-agents, keyless YouTube search, oEmbed and transcript pipeline
- **To fetch:** yt-dlp https://github.com/yt-dlp/yt-dlp (Pulls embedded lesson videos (Loom, Vimeo, YouTube) that a Skool classroom links to.); whisper.cpp https://github.com/ggml-org/whisper.cpp (Fast local transcription on the Mac if the current local pipeline is slow.)
- **Missing:** Nobody has the Skool login flow scripted; it needs a person present in an interactive session.
- **Field Notes line:** Rent a course for a month, transcribe every lesson locally, keep the text, cancel before renewal: a course becomes a searchable note pile for nine dollars.

### H-0048 Show HN: OpenAPPA – open-source deterministic guardrails that don't break agents
2026-09-28, hn, https://www.openappa.com/

- **Mechanism:** A deterministic guardrail sits in an agent loop through pre- and post-tool-call hooks. Its policy language is written per kind of data rather than per use case, so one policy covers many tasks. To stop it breaking agents it adds a remedy plan, telling the agent what it may do instead, and a DualLLM pattern that keeps untrusted data away from the acting model. The leak and utility percentages come from the authors' own benchmarks.
- **Claim:** About 90% utility retained versus about 40% for other deterministic guardrails, against roughly 10% leaks for LLM-judge approaches.
- **Testable:** no. Reproducing the benchmarks needs LLM agent runs, and the numbers are the authors' own. Needs: An LLM agent to drive the benchmark.
- **Field Notes line:** OpenAPPA writes guardrail policy per data type, not per task, and tells a blocked agent what it can do instead; the 90% utility figure is self-reported.

### H-0046 jkawamoto/mcp-youtube-transcript: MCP server retrieving transcripts of YouTube videos
2026-09-28, github, https://github.com/jkawamoto/mcp-youtube-transcript

- **Mechanism:** An MCP server exposing tools to fetch a YouTube video's transcript, timed transcript, metadata and available languages from a URL. Long transcripts are paginated with a cursor so they fit inside a token limit. It runs locally through uvx and needs no key, but depends on YouTube serving captions to the caller's IP.
- **Claim:** Retrieves transcripts for YouTube URLs with cursor-based pagination for long videos.
- **Testable:** yes. Does uvx run it keyless and return a transcript for a public captioned video, and how many pages does a 28 minute video take? Queued as P-0031.
- **Field Notes line:** A keyless MCP server that pulls YouTube transcripts and pages long ones by cursor; tonight's test is whether YouTube still hands them over.

### H-0045 Launch HN: Vespper (YC F24) – SOTA Docx MCP
2026-09-28, hn, https://www.vespper.com/blog/launching-vespper-docx-mcp

- **Mechanism:** A Word file is a zip of verbose OOXML, so simple edits such as a numbered list or bold text need linked changes across numbering.xml and split run elements in document.xml. Vespper puts an MCP in front of that with a fine-tuned model that turns edit intents into the low-level XML changes, so the calling agent does not spend tokens on the mechanics. The comparison numbers are the vendor's own.
- **Claim:** A Word-editing MCP that is 3 times faster, 2 times cheaper and more accurate than the closest alternative.
- **Testable:** no. Needs a Vespper account and its hosted model, and the benchmark data is not public in the post. Needs: A Vespper account.
- **Field Notes line:** Agents are bad at Word because bold text means splitting XML runs and lists need linked numbering entries; Vespper hides that behind a tuned model.

### H-0043 A Safety-Bounded SDC-to-MCP Gateway for Medical AI Agents
2026-09-28, arxiv, https://arxiv.org/abs/2609.31358

- **Mechanism:** A gateway maps IEEE 11073 SDC medical device state into MCP: metrics, alarms and metadata become read-only resources, and actions become dry-run tools validated against a policy. The safety property is narrow: no agent request ever dispatches a real device operation. It was tested on a Python prototype with simulated faults, Java and Python interoperability, and several models.
- **Claim:** Explicit semantic metadata improved conformity to required metric identifiers in alarm outputs, and the no-execution boundary held on all paths.
- **Testable:** no. Needs SDC device simulators and the authors' prototype, which the abstract does not link. Needs: The prototype code and an SDC simulator.
- **Field Notes line:** A medical-device MCP gateway keeps agents safe by exposing state read-only and turning every action into a dry run that can never execute.

### H-0042 samyost1/3dicon: One prompt in, a looping animated 3D icon out — with real transparency. A Claude Code skill.
2026-09-28, github, https://github.com/samyost1/3dicon

- **Mechanism:** An image model makes one still, which is sent to a video model as both first and last frame, so the clip returns to its start and loops without a seam. The background is a chosen flat colour, so each frame can be unmixed for exact foreground colour and alpha rather than guessed, which avoids edge halos. Frames are then packed into an animated WebP. It needs an OpenRouter key and a roughly 180MB matting model.
- **Claim:** One prompt gives a seamlessly looping animated 3D icon with real transparency.
- **Testable:** no. The pipeline needs an OpenRouter key and paid image and video model calls. Needs: An OpenRouter API key and spend.
- **Field Notes line:** Loop a video model by feeding the same still as first and last frame, then remove the background against a known colour to keep soft edges.

### H-0040 Agent Memory EXPLAINED - Complete Architecture
2026-09-28, youtube, https://www.youtube.com/watch?v=aYfZN8t6AQs

- **Mechanism:** Long-term agent memory is a separate service beside the conversation history. Mem0 stores facts from every conversation in several stores, runs an ingestion workflow that extracts and reconciles facts, and a retrieval workflow that fetches relevant ones each turn. Deleting one memory is its own workflow. The talk says it can all run on local models.
- **Claim:** Walks through Mem0's stores, ingestion, retrieval and deletion, and how to rebuild it with local models.
- **Testable:** no. Running Mem0 needs an LLM for fact extraction, and no 30 minute keyless slice gives a verdict on the walkthrough itself. Needs: An LLM endpoint for extraction.
- **Field Notes line:** Mem0's long-term memory is a separate service with its own ingest, retrieve and delete workflows, sitting beside the plain chat history.

### H-0039 Structured Reasoning Agentic Framework for Interpretable Critical View of Safety Assessment
2026-09-28, arxiv, https://arxiv.org/abs/2609.31524

- **Mechanism:** Surgical frames are turned into an anatomical scene graph of entities and spatial relations. A fine-tuned LLM acts as the central decision-maker and calls a vision-language model as a tool to verify each sub-criterion of the Critical View of Safety separately. It then combines those observations into a verdict with a written rationale. Numbers come from the Endoscapes-CVS201 benchmark.
- **Claim:** 68.1% mAP on Endoscapes-CVS201 with criterion-level explanations.
- **Testable:** no. Needs the benchmark data and trained models, and no runnable public code is named in the abstract. Needs: Benchmark dataset access and model weights.
- **Field Notes line:** A surgery-safety checker splits one black-box score into per-criterion checks: an LLM asks a vision model tool questions about a scene graph.

### H-0038 lemomo-ai/lemo-opuscar: 39 film styles, each a reusable style prompt plus a short film made entirely in code by Claude O
2026-09-28, github, https://github.com/lemomo-ai/lemo-opuscar

- **Mechanism:** A coding agent is given a style prompt plus guides and writes a page in Canvas or WebGL that is rendered frame by frame, then muxed with ffmpeg. Music is composed from free sample libraries and narration comes from local text-to-speech, so there is no video model or stock footage. The styles are tuned to one specific model version, and the repo says other models may not reproduce them.
- **Claim:** 39 reusable film styles, each with a short film made entirely in code, including a 6:25 film covering 98 Best Picture winners.
- **Testable:** no. Directing a film needs a Claude agent run against the skill, which is spend Proteus does not have for this, and the 60 MB download is only the tooling. Needs: A Claude Opus-class agent session to direct a film.
- **Field Notes line:** Whole short films made by an agent writing Canvas and WebGL code, rendered frame by frame with local speech and sampled music, no video model.

### H-0037 Show HN: HN.watch – Videos of all Hacker News posts
2026-09-28, hn, https://hn.watch/

- **Mechanism:** An LLM writes an HTML-based video (a timed script of animated page elements plus narration) instead of pixels, so playback is just a browser rendering markup. The video is generated the first time a link is clicked and then presumably cached. Cost is claimed to be about $0.04 per video because one text generation replaces diffusion video, but image generation inside a video blows that up. The stack is built on the Imba language and Scrimba's existing HTML video format.
- **Claim:** Explainer videos generated in a few seconds from click to playback at roughly $0.04 each, excluding image generation.
- **Testable:** yes. Does an uncached hn.watch item load and start playing within 10 seconds without a login, and what is the measured click-to-playback time? Queued as P-0030.
- **Field Notes line:** Scrimba makes explainer videos as HTML plus an LLM script instead of pixels, claiming four seconds and about four cents each.

### H-0036 alexgreensh/anidoodle: Art and animation, written as code. Illustrations, loops, interactive web art, stickers and score
2026-09-27, github, https://github.com/alexgreensh/anidoodle

- **Mechanism:** Each of the 31 styles is implemented as deterministic drawing code: marks (hatching, dabs, stipple dots, triangles, brush strokes) are placed by pure functions of position and tone rather than wall-clock-seeded randomness, and the audio is described as generated arithmetically rather than sampled. With no external randomness or asset lookup, the same source is claimed to redraw pixel-identical output on any machine or render size.
- **Claim:** Claims the same source code redraws the same picture, in any of 31 hand-drawn styles, identically on every machine and at every size.
- **Testable:** yes. Does running the same anidoodle style script twice produce byte-identical rendered output, as the determinism claim says? Queued as P-0028.
- **Field Notes line:** anidoodle draws in 31 styles entirely as deterministic code, no randomness, claiming the same script renders pixel-identical output every time it runs.

### H-0034 lightpanda-io/browser (new in awesome-mcp-servers)
2026-09-27, awesome, https://github.com/lightpanda-io/browser

- **Mechanism:** Lightpanda is a browser engine written from scratch in Zig rather than a Chromium or WebKit fork, implementing its own DOM/JS handling instead of a full rendering stack, and exposing the standard Chrome DevTools Protocol on port 9222 so existing Puppeteer/Playwright clients can drive it unmodified. Its benchmark fetched 933 real pages on one EC2 instance and measured peak memory and wall-clock time against headless Chrome doing the same crawl.
- **Claim:** Claims 123MB peak memory versus Chrome's 2GB (about 16x less) and 5s versus 46s for 100 pages (about 9x faster) on that benchmark.
- **Testable:** yes. Does the lightpanda binary actually fetch and dump HTML from a real public page via its CLI, and how does its wall-clock time compare to a quick baseline fetch? Queued as P-0027.
- **Field Notes line:** Lightpanda is a browser built from scratch in Zig, not a Chromium fork, claiming 16x less memory and 9x faster page loads than headless Chrome.

### H-0033 How to Build An Expected Goals Model 1: Data and Model
2026-09-27, youtube, https://www.youtube.com/watch?v=bpjLyFyLlXs

- **Mechanism:** An expected-goals model is a statistical model, fitted on many recorded shots (here a season of Wyscout data across leagues), that estimates the probability a shot of a given type and location becomes a goal. The lecture frames it as the first step before moving to machine-learning variants and stresses that the model's quality lives in how the underlying shot data is defined and measured.
- **Claim:** Describes building an xG model from a season of Wyscout shot data as lecture one of a three-part series.
- **Testable:** no. This part of the transcript is conceptual framing with no formulas, features or code shown to run against.
- **Field Notes line:** Friends of Tracking's xG lecture explains it as a statistical model fitted on season-long shot data by location and type, ahead of the ML follow-ups.

### H-0032 PUBG Ally: A Conversational Embodied Agent as an AI Teammate
2026-09-27, arxiv, https://arxiv.org/abs/2609.29837

- **Mechanism:** Ally splits control between a language-model agent that reads game state, interprets voice and picks high-level actions, and a faster low-level control layer that actually executes movement, combat and recovery in real time. It was trained iteratively on data from nearly 39,000 real sessions of players playing alongside it, with model compression, context compaction and runtime guardrails added to hit live on-device latency and safety needs.
- **Claim:** Surveyed across 141 countries, positive recommend-Ally responses exceeded negative ones by 25.1 percentage points among confirmed players.
- **Testable:** no. It's a proprietary system deployed inside PUBG's live service; there is no public build to run. Needs: access to PUBG's live service integration, which is not public.
- **Field Notes line:** PUBG's AI teammate splits a slow LLM planner from a fast control layer for real-time play, trained on 39,000 live sessions with real players.

### H-0031 dzhng/jevgrep: Find code by asking what it does. A CLI for coding agents that uses Jev to discover relevant files and so
2026-09-27, github, https://github.com/dzhng/jevgrep

- **Mechanism:** jg walks a repo's folder and file hierarchy, using content previews to prune branches, then calls the hosted Jev model to judge which files and declarations are relevant to a natural-language question. It parses Python and TypeScript/JavaScript declarations directly for structure and falls back to plain text elsewhere, returning file paths, reading leads and verbatim excerpts rather than forcing a fixed top-N list.
- **Claim:** Positions itself as a faster alternative to grep-style search for coding agents, using Jev to judge relevance across a codebase.
- **Testable:** no. Needs a paid key for Vercel AI Gateway, OpenRouter or similar to run Jev; the CLI does nothing useful without one. Needs: an API key for Vercel AI Gateway, TypeSafe, OpenRouter or OpenCode Zen.
- **Field Notes line:** jevgrep has a coding agent ask Jev which files matter instead of grepping, previewing content to prune the repo tree before ranking results.

### H-0030 Turning GLM-5.3-Flash into a Jev-like decision model
2026-09-27, hn, https://www.privatemode.ai/blog/system-one-from-glm-flash

- **Mechanism:** They craft the prompt so the very first output token of a standard LLM (GLM-5.3-Flash on vLLM) directly encodes the decision, turning what would be a generated explanation into a single forward pass read off the first token's logits. This mimics latency-optimised decision models like Jev without a specialised architecture, and it extends to vision inputs because it's prompting, not a separate classifier head.
- **Claim:** Says the approach matches Jev's accuracy and speed and beats Laya, though it costs several times more per decision than Jev; a commenter disputes the claimed prefill speed is achievable on normal hardware.
- **Testable:** no. Needs GLM-5.3-Flash weights and a vLLM serving stack, not a 30-minute keyless run. Needs: GLM-5.3-Flash model access and a vLLM deployment.
- **Field Notes line:** Forcing the first output token to be the answer turns any LLM into a one-forward-pass decision model, matching Jev's accuracy but costing more per call.

### H-0029 agentmail-to/agentmail-mcp (new in awesome-mcp-servers)
2026-09-27, awesome, https://github.com/agentmail-to/agentmail-mcp

- **Mechanism:** AgentMail now ships a single hosted MCP implementation reachable over Streamable HTTP; the npm and PyPI 'bridges' are thin stdio shims that discover the tool catalogue and JSON schemas live from that hosted server rather than embedding their own tool logic. A generated mcp-manifest.json defines the runtime contract, and both bridges support OAuth or a per-request API key plus a --tools filter.
- **Claim:** Consolidates what used to be a local npm implementation into one hosted MCP server, with stdio bridges kept only for compatibility.
- **Testable:** yes. Does the hosted Streamable HTTP endpoint (https://mcp.agentmail.to/mcp) answer or refuse a tool-list call with no API key at all? Queued as P-0026.
- **Field Notes line:** AgentMail collapsed its MCP server into one hosted endpoint; the npm and Python packages are now just thin bridges fetching the tool catalogue live.

### H-0027 When Can Agents Forget Their Reasoning? ICLR for Long-Horizon Agent Context Compression
2026-09-27, arxiv, https://arxiv.org/abs/2609.29875

- **Mechanism:** ICLR ranks blocks of an agent's past reasoning by a frozen proxy model's token entropy and prunes low-value ones from context while always keeping actions, tool calls and observations intact. It runs online with no training, deciding per step what reasoning history is safe to drop. Ablations show deleting reasoning can amplify downstream compute nonlinearly, and that reasoning becomes droppable once the task state it captured has been externalised into files, code or tool output.
- **Claim:** On 260 WorkBuddyBench tasks it raises average reward from 0.699 to 0.718 while cutting input, output and cache-read tokens by 25.5%, 14.4% and 33.3%.
- **Testable:** no. Needs the WorkBuddyBench harness, a proxy model for entropy scoring and a long-horizon agent loop; nothing runnable from the abstract alone. Needs: WorkBuddyBench benchmark code and a compatible agent/proxy-model setup.
- **Field Notes line:** A training-free method scores an agent's past reasoning by proxy-model entropy and prunes it, cutting tokens up to a third while nudging reward up.

### H-0025 On caring for user data: NeoVim caused Vim undo files to be deleted
2026-09-27, hn, https://unsung.aresluna.org/they-had-no-concept-of-a-duty-of-care-to-their-users/

- **Mechanism:** Neovim and classic Vim share the same undo-file name and location but Neovim changed the on-disk undo format without versioning or renaming it. When Neovim opens a Vim-format undo file it can't parse, it deletes the file outright and writes its own incompatible format in its place, destroying the old undo history and leaving Vim unable to read the replacement either.
- **Claim:** The post says persistent undo files get silently deleted and replaced by Neovim because of an unannounced, unversioned format change.
- **Testable:** yes. Does opening a classic-Vim undo file in a fresh Neovim install actually delete/overwrite it so Vim can no longer read it? Queued as P-0025.
- **Field Notes line:** Neovim silently deletes and overwrites classic Vim's undo files on an unversioned format change; testable tonight with two editors and one file.

### H-0022 mikehasa/golive-skill: Take your agent-built product live: hosting, database, domain, email, payments — on your own acco
2026-09-26, github, https://github.com/mikehasa/golive-skill

- **Mechanism:** GoLive is a zero-dependency Node CLI plus an Agent Skill running a detect -> plan -> approve -> apply -> verify pipeline against your own provider accounts (Vercel/Netlify, Supabase/Neon, Porkbun/GoDaddy DNS, Resend email, Stripe test-mode payments). Apply refuses to run without a plan id and an explicit --yes, re-validates the plan's identity against current state before writing, and gates destructive or live-money actions behind separate --confirm-dns/--confirm-destroy/--confirm-live flags; it stores any credentials it touches in a plaintext 0600 file outside the repo rather than a keychain, and states plainly that an agent already logged into a provider can bypass its plan gate entirely.
- **Claim:** Lets an agent take a built app live end to end, then tear it down again, on your own hosting/database/domain/email/payment accounts with no GoLive backend or telemetry, currently alpha-tested across six provider journeys.
- **Testable:** yes. Does `golive detect` and `golive plan` produce a real, inspectable plan for a scratch app with no provider account connected, and does `apply` correctly refuse to run without --yes? Queued as P-0023.
- **Field Notes line:** GoLive is an open-source skill that scripts taking an agent-built app live on your own provider accounts, gating every write behind an explicit plan and confirm flags.

### H-0021 Jevmem – automatic project memory for Claude Code, built on Jev
2026-09-26, hn, https://github.com/Avinash-jetwani/jevmem

- **Mechanism:** Jevmem hooks into Claude Code/Cursor/Codex chat sessions and after every message calls a small classifier model (Jev, via the TypeSafe API) to judge whether that message contains something durable worth remembering, a decision, a bug, a change of mind, and if so appends it to a JEVMEM.md file in the repo; when a later message reverses an earlier decision, the old entry is marked superseded rather than deleted. It is a thin wrapper around a hosted classification API, not a local model or vector store.
- **Claim:** The author's own held-out test on 66 messages puts Jev at 98.5% accuracy on the save/skip decision, tied for best of six frontier LLMs, with a 0.30s median decision latency versus 2.8-4.3s for the compared LLMs.
- **Testable:** no. Installing and running it needs a TypeSafe API key, a credential Proteus does not hold. Needs: a TypeSafe API key.
- **Field Notes line:** Jevmem watches your coding-agent chats and uses a small hosted classifier to decide, message by message, what's worth saving to a project memory file.

### H-0019 Qwen-Planner-Agent: A Closed-Loop AI-for-AI Framework for Real-World Mobile Planner Agents
2026-09-26, arxiv, https://arxiv.org/abs/2609.29892

- **Mechanism:** Qwen-Planner-Agent is built through a closed AI-for-AI loop with three parts: an agentic data flywheel where specialised agents generate mobile-planning tasks and curate trajectories with human gating; training that combines a supervised cold start with online reinforcement learning using a 'Competence-Aware Reward-and-Advantage Engineering' term to cut tool-use and reasoning cost; and a runtime loop that logs execution evidence and failure traces back into both the model weights and the surrounding harness (memory, skills, tool orchestration).
- **Claim:** Qwen-Planner-Agent tops MobilePA-Bench among evaluated models and systems, improving over its base model on tool use, memory, skills and sub-agent coordination while mostly holding onto general capability.
- **Testable:** no. Needs the MobilePA-Bench harness, real or emulated mobile devices, and the trained model weights, none available for a keyless run tonight.
- **Field Notes line:** Qwen-Planner-Agent trains a mobile-planning agent through a closed loop of agent-generated data, RL with a cost-aware reward term, and runtime feedback into both model and harness.

### H-0018 yetone/magpie: Every agent's model. One place. Codex on DeepSeek, Claude Code on Kimi, from the menu bar.
2026-09-26, github, https://github.com/yetone/magpie

- **Mechanism:** magpie runs a small local HTTP gateway (127.0.0.1:3425) that speaks the OpenAI chat-completions, OpenAI Responses and Anthropic Messages API shapes and translates between them, so any agent CLI pointed at it can use any configured backend model regardless of which API the agent itself expects. It edits each tool's own config file (settings.json, config.toml, opencode.jsonc, config.yaml) in place, touching only the changed key so comments and ordering survive, and pulls live model lists per provider, falling back to the models.dev catalog rather than a hardcoded list.
- **Claim:** One menu-bar app lets you point every agent CLI (Claude Code, Codex, Gemini CLI, OpenCode, etc.) at any provider or model through a single local gateway, with surgical, non-destructive edits to each tool's config file.
- **Testable:** yes. Does magpie's config writer change only the targeted key in a sample settings.json copy, leaving comments, key order and unrelated fields byte-identical? Queued as P-0022.
- **Field Notes line:** magpie is a local menu-bar gateway that translates between OpenAI and Anthropic API shapes so any agent CLI can run on any provider's model, editing each tool's config file surgically.

### H-0017 Show HN: A Claude Code skill to analyze your chess games
2026-09-26, hn, https://github.com/brumar/chess-postmortem-skills

- **Mechanism:** The system takes a live game (audio notes or text, plus a lichess game reference), uses Claude's vision to read board state directly from images rather than parsing PGN, and pairs that with a local Stockfish engine for move evaluation. Claude then narrates the game, combining Stockfish's evaluations with a reflection on the player's own recorded thinking during the game, and renders the commentary as a video. The author reports it costs roughly $15 in API spend and about an hour per game.
- **Claim:** Turns 'analyze my last lichess game' plus your own audio notes into a commented video of the game, using Claude vision plus Stockfish, for about $15 in API cost per game.
- **Testable:** no. The author's own figure is about $15 in API spend per run, real spend Proteus can't put toward a keyless test.
- **Field Notes line:** A Claude Code skill reads chess boards by vision instead of PGN, pairs that with Stockfish, and narrates a commented video of your own game and thinking for about $15 a run.

### H-0015 An Empirical Study of VLM Pipelines for Long-Document QA
2026-09-26, arxiv, https://arxiv.org/abs/2609.29933

- **Mechanism:** The paper benchmarks long-document VLM QA pipelines on three axes: how the document is fed in (full pages vs a retrieved subset), which retriever selects pages (image-embedding retrieval of rendered pages vs text retrieval plus a cross-encoder rerank), and whether the model runs agentically with page/table/figure/search tool calls or as one static pass. It runs these combinations on MMLongBench-Doc and LongDocURL with both frontier API models and open-weight Qwen3.5 variants, measuring accuracy and token cost per pipeline.
- **Claim:** Their six-tool agent only beats static page-feeding once the reader model is large enough (level with Qwen3.5-27B, ahead with Sonnet 4.5), image retrieval beats text retrieval at a seventh to a quarter of the tokens, and an oracle pipeline-picker gains about 13 points over the best single pipeline.
- **Testable:** no. Reproducing needs the MMLongBench-Doc/LongDocURL benchmarks plus paid frontier VLM API calls, a multi-day evaluation, not a 30-minute keyless run.
- **Field Notes line:** Long-document QA study finds agentic tool-calling only beats just feeding pages once the model is big enough, and image-based page retrieval beats text retrieval at far fewer tokens.

### H-0014 JohnHeibel/PDoomVideo: Source code for the Claude Opus 5.5 music video for I'm Upping My P(doom)
2026-09-26, github, https://github.com/JohnHeibel/PDoomVideo

- **Mechanism:** The whole music video was produced by Claude Opus 5.5 in Claude Code with no scene ideas supplied: the model wrote its own shot-by-shot STORYBOARD.md and an ANIMATION_GUIDE.md briefing document, then dispatched parallel subagents to build each chapter as p5.js/p5.brush code rendered in a shared studio.html canvas. A separate render.mjs script paints every frame in headless Chrome and stitches them with ffmpeg into the final MP4 synced to the included song.
- **Claim:** A full nine-chapter animated music video, entirely written and orchestrated by Claude Opus 5.5, given only a character design and two style directions.
- **Testable:** yes. Does render.mjs paint frame 0 of a chapter from a clean checkout with npm install alone, or does it need a manual Chrome path? Queued as P-0021.
- **Field Notes line:** A full 9-chapter music video was written and rendered end to end by Claude Opus subagents, from storyboard to p5.js animation to ffmpeg encode, no human scene ideas.

### H-0013 Show HN: Reladraw – A diagram language where you decide where to place things
2026-09-26, hn, https://github.com/reladraw/reladraw

- **Mechanism:** Reladraw is a diagram-definition language where you specify relative placement of nodes rather than absolute coordinates or letting an auto-layout engine decide, sitting between auto-placement tools (Mermaid, Graphviz) and manual editors (draw.io). It compiles the language to a rendered diagram, has a browser playground for trying it without installing anything, ships as an npm package for local use, and includes a packaged skill so an agent can write and edit diagrams as text.
- **Claim:** A diagram language that keeps full manual control of layout while staying as easy for humans and agents to edit as text, per its Show HN post (116 points, 31 comments).
- **Testable:** yes. Does `npm install reladraw` run cleanly and can a plain-text 3-node diagram definition render to an image? Queued as P-0020.
- **Field Notes line:** Reladraw is a new diagram language that keeps manual layout control but stays text-editable enough for agents to drive, unlike Mermaid or draw.io.

### H-0012 Alan Kay: Shannon gave us a way of dealing with noisy channels [video]
2026-09-26, hn, https://www.youtube.com/watch?v=Cjntrqhn8pk

- **Mechanism:** An open Zoom mic near a live-stream speaker fed Alan Kay's own voice back to him after roughly 21 seconds, the delay built up by several re-encoding hops (Zoom, stream, room, back into Zoom, repeated, then a screen recording, then YouTube's auto-captioner on top). The 21-second round trip corresponds to a light-speed distance of about 3 million km, which HN frames as an accidental live demo of Shannon's noisy-channel coding theorem and an unplanned recreation of Alvin Lucier's 1969 tape-feedback piece, where a voice re-recorded through a room repeatedly degrades until only the room's resonance is left.
- **Claim:** HN post frames a ~21-second live-stream audio feedback loop during an Alan Kay talk as an accidental version of Lucier's sound art and a real demo of Shannon's noisy-channel theorem.
- **Testable:** no. Nothing to build or run, it is an anecdote about an accidental live audio feedback loop.
- **Field Notes line:** An open mic turned a live Zoom stream into a 21-second voice-feedback loop, an accidental real-world demo of Shannon's noisy-channel theorem.

### H-0010 nateherkai/hyperframes-student-kit: Edit videos, reels, and YouTube Shorts with Codex or Claude Code. 14 skills, transcr
2026-09-26, github, https://github.com/nateherkai/hyperframes-student-kit. Vault verdict on the vendor exists (vault: tools and repos); mechanism recorded, vendor not re-judged.

- **Mechanism:** Ships a synthetic starter composition so `npm run demo` assembles an 8-second GSAP-driven HyperFrames composition entirely offline; `npx hyperframes lint/preview/render` then lints it, previews it in Studio, and renders it through a headless Chrome pipeline, only reaching the network to cache font substitutions on first render. For real footage, the same skills instead pipe a word-level transcript (from ElevenLabs Scribe, or swapped to local Whisper) into silence-cutting, mistake-detection and cut-planning skills before assembling clips onto 406 pre-built motion-graphics card templates.
- **Claim:** Video-editing skill kit for Claude Code/Codex with transcript-driven cuts and 406 motion-graphics cards; the local demo needs no footage, account or API key.
- **Testable:** yes. Does `npm run demo` followed by `npx hyperframes lint`, `preview` and `render --quality draft` produce a valid demo.mp4 with zero API keys or accounts? Queued as P-0019.
- **Field Notes line:** This Codex/Claude Code video-editing kit ships a synthetic demo that lints, previews and renders a HyperFrames clip with zero API keys or footage required.

### H-0009 Show HN: Whiteboard (YC W26) – An open-source IDE for thoughtful software design
2026-09-26, hn, https://github.com/devdotfast/whiteboard

- **Mechanism:** Vendors a full fork of Code-OSS (VSCode) directly, rather than maintaining a patch set, specifically because coding agents handle a vendored fork better than patches; the fork strips roughly 45% of stock VS Code that was Copilot-related. On top of that base, an SDK lets an agent draw diagrams (sequence diagrams, ER diagrams, trace quotes) onto an in-app canvas that link directly to the underlying source lines, and a separately written Rust AST-aware diff viewer summarises large added functions as pseudocode and collapses routine test/doc-only changes so a reviewer sees only semantically relevant diffs.
- **Claim:** Open-source desktop IDE (YC W26) where an agent's SDK-drawn diagrams click straight through to the code that produced them.
- **Testable:** no. It vendors a full Code-OSS (VSCode) fork plus Rust components in a pnpm monorepo; building that from source will not finish in 30 minutes.
- **Field Notes line:** Whiteboard vendors a full VSCode fork (minus its Copilot code) and gives coding agents an SDK to draw diagrams that click straight through to the source lines.

### H-0007 World Action Agent: Harnessing VLMs for Robot Manipulation via World Action Rehearsal
2026-09-26, arxiv, https://arxiv.org/abs/2609.29964

- **Mechanism:** Gives a vision-language model a 'visual action workspace' instead of a single scene view: contact-view camera crops are auto-selected from scene geometry around the current interaction, each candidate action becomes an editable visual proposal that is rehearsed and revised (optionally by a separate Imagination Agent) before it ever executes, and an in-view correction step lets the agent remove residual offsets in the same view where it spotted them. A Skill Agent retrieves procedural skills mined from expert videos and human demonstrations, and the harness's own interaction traces are used afterward to fine-tune smaller VLMs to run the same loop.
- **Claim:** 75.6% average success on LIBERO-Pro using only skills evolved from LIBERO-90, beating end-to-end VLA and code-as-policy baselines; fine-tuning Qwen3.5-9B on harness traces raised its out-of-domain success from 1.7% to 43.3%.
- **Testable:** no. Needs LIBERO/robosuite simulation environments plus VLM inference infrastructure, well past a 30-minute keyless sandbox setup. Needs: robot simulation environments (LIBERO, robosuite) and VLM inference compute.
- **Field Notes line:** A VLM robot-control harness rehearses and visually previews every action before executing it, lifting LIBERO-Pro success to 75.6% using only pre-evolved skills.

### H-0006 chainstacklabs/pumpfun-bonkfun-bot: A fully functional pump.fun / letsbonk.fun trading and sniping bot not relying on an
2026-09-26, github, https://github.com/chainstacklabs/pumpfun-bonkfun-bot. Vault verdict on the vendor exists (vault verdict: pump.fun); mechanism recorded, vendor not re-judged.

- **Mechanism:** Watches Solana on-chain activity for new pump.fun/letsbonk.fun token creation itself, choosing between four listener backends of increasing cost and speed: logsSubscribe (works on any RPC), blockSubscribe (not universally supported), a paid Geyser gRPC stream, and raw pre-confirmation 'shreds'; it calls no pump.fun API at all. Each bot instance is a YAML config pointing at one listener plus a buy/sell strategy, and it signs and submits its own transactions using a supplied wallet private key.
- **Claim:** Open-source pump.fun/letsbonk.fun sniping bot with four selectable listener speeds, explicitly 'not for production, for learning purposes only'.
- **Testable:** no. Real sniping needs a funded Solana wallet private key and, for the faster listeners, a paid Geyser/RPC endpoint; public RPC will not do the job. Needs: a funded Solana wallet and a paid Geyser/RPC endpoint.
- **Field Notes line:** This pump.fun sniper skips pump.fun's own API entirely, racing new tokens via raw Solana log, block, Geyser or shred streams instead, speed bought with a pricier RPC tier.

### H-0005 Claude Code reads AGENTS.md only when telemetry is on [fixed]
2026-09-26, hn, https://blog.szypowi.cz/p/claude-code-reads-agents.md-only-when-telemetry-is-on/

- **Mechanism:** Claude Code's AGENTS.md support ships as a built-in plugin ('agents-md') that defaults to off and gates itself behind a remote feature flag ('tengu_agents_md_mod') fetched over the network; the fallback value when that fetch cannot happen is false. Setting either CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1 or DISABLE_TELEMETRY=1 blocks the flag fetch, so the plugin silently stays disabled and the local AGENTS.md file is never read, even though reading a local file needs no network at all.
- **Claim:** Author measured, via a two-session canary-word test, that Claude Code 2.1.277+ skips reading a project's AGENTS.md whenever either telemetry-disabling env var is set; logged as GitHub issue #95690.
- **Testable:** no. Reproducing it means repeated `claude -p` invocations, which spends real Claude API credits rather than running keyless.
- **Field Notes line:** Claude Code's AGENTS.md support hides behind a remote feature flag that quietly defaults off whenever telemetry env vars are set, even though reading a local file needs no network.

### H-0004 Pump Fun Sniper Bot Full Tutorial / Solana MEV Bot step-by-step how to use
2026-09-26, youtube, https://www.youtube.com/watch?v=vssd36X5Y2c

- **Mechanism:** The tutorial's login step asks you to paste a Phantom or Solflare wallet's private key into a browser-hosted 'bot' dashboard, which is the exact mechanism used by Solana wallet-drainer scams that harvest keys under cover of an automation tool. The video's other claims (an 'AI' deciding trades, an 0.01s launch-to-buy reaction time, an 80% win rate) are unverifiable from inside the same dashboard and are typical of this genre's marketing; a real listener-based sniper (see gh:chainstacklabs/pumpfun-bonkfun-bot) needs its own on-chain listener and never asks for your key through a hosted UI.
- **Claim:** Video claims an 'AI'-run bot buys new pump.fun tokens within 0.01 seconds of launch and sells after another buyer moves the price, with an approximate 80% win rate.
- **Testable:** no. The only way to 'test' it is entering a wallet private key into an untrusted third-party site, which is not something to do to get a verdict. Needs: a wallet private key handed to an untrusted site, which we will not provide.
- **Field Notes line:** This 'AI' pump.fun sniper's login step asks for your wallet's private key pasted into its website, the exact pattern behind Solana wallet-drainer scams.

### H-0003 Screen Before You Serve: Simulation for Production Customer Experience AI Agents at 140M Scale
2026-09-26, arxiv, https://arxiv.org/abs/2609.30137

- **Mechanism:** Candidate customer-support agent configs are screened with synthetic customer personas (via the Snowglobe simulator) that converse with the agent while simulated tool outputs stand in for production backends, so multi-step flows run without touching real customer data. An automated binary evaluator scores each simulated conversation; the paper reports these simulated scores correlate highly with the same version's later production evaluator scores, which is the basis for using simulated deltas to pick between models, reasoning settings and prompts before running a live A/B test.
- **Claim:** Simulation-guided iteration across 16,000+ simulated conversations at Nubank raised transactional NPS by 36.69 points in one A/B test and self-service rate by 8.82 percentage points in a later one, both confirmed live.
- **Testable:** no. Snowglobe and Nubank's Card Management agent are internal production systems with no public code, model or dataset to run.
- **Field Notes line:** Nubank screened chat-support agent configs across 16,000+ simulated conversations before A/B tests, lifting self-service rate by 8.82 points with no customer exposure.

### H-0002 nexmoe/VidBee: Download video and audio from  YouTube ,  TikTok ,  Twitter ,  Instagram ,  Facebook ,  Twitch ,  Bilibil
2026-09-26, github, https://github.com/nexmoe/VidBee

- **Mechanism:** Downloads media from 1000+ sites via a yt-dlp-style backend, then runs speech recognition fully on-device using a local model family the user picks (Whisper, SenseVoice, Parakeet, Qwen3-ASR), producing a timestamped, speaker-labelled transcript with no upload to a transcription service. AI features (summarise, translate, FAQ, mind map) are a separate step: the transcript and prompt are sent to whichever provider the user configures with their own API key (OpenAI, Anthropic, Ollama, LM Studio, etc.), so the privacy guarantee only covers the ASR step, not the AI step unless a local endpoint is chosen.
- **Claim:** Free, open-source desktop app (10.7k GitHub stars) that downloads and locally transcribes video/audio from 1000+ sites, then runs user-chosen AI prompts on the transcript.
- **Testable:** no. Distributed as a GUI desktop installer rather than a scriptable CLI, plus multi-gigabyte local ASR model downloads on first use, so a headless verdict won't land in 30 minutes.
- **Field Notes line:** VidBee downloads video from 1000+ sites and transcribes it fully offline with local Whisper-family models before you choose which AI provider sees the text.

### H-0001 Show HN: Make cursed fonts like Times New Bastard
2026-09-26, hn, https://bastardica.mitpit.com

- **Mechanism:** Mixes glyphs from different fonts by abusing OpenType's ligature substitution (GSUB) tables rather than any server-side rendering. The whole pipeline, including the font-manipulation toolchain, runs client-side by loading a Python interpreter compiled to WASM in the browser, so no upload or backend call is needed.
- **Claim:** A joke web tool for making 'cursed' fonts by mixing typefaces via ligatures, computed entirely client-side in the browser.
- **Testable:** no. It is judged by visual appearance in a browser, not by a headless pass/fail from a sandbox script.
- **Field Notes line:** A joke web tool remixes fonts by hijacking OpenType ligature substitution, all computed live in-browser via a Python interpreter compiled to WASM.

## Vault threads: Luke's links, judged as ideas

Themes the vault split out of links Luke sent it, read from `field-notes/vault-threads.json` (one way). The vault's status
is what its side decided about the vendor or Luke's time; the idea column is this side's view of the idea alone.

| id | date | theme | vault said | idea | testable | probe |
|---|---|---|---|---|---|---|
| H-0320 | 2026-10-19 | one-credit multi-model connector for desktop seats | open | sound | no |  |
| H-0315 | 2026-10-19 | talking head over lifestyle B-roll | open | sound | no |  |
| H-0310 | 2026-10-19 | AI UGC and ad videos sold to businesses | open | needs-a-run | no |  |
| H-0307 | 2026-10-17 | structured workbook as the product | open | sound | no |  |
| H-0302 | 2026-10-17 | Familiar-surface cloning to sell a switch | open | sound | no |  |
| H-0296 | 2026-10-17 | sell narrow named jobs, not AI | open | sound | no |  |
| H-0294 | 2026-10-16 | longer test of the retest rules | open | needs-a-run | yes | P-0166 **not-worth-it** |
| H-0288 | 2026-10-16 | mistake-becomes-a-rule trade journal | open | sound | no |  |
| H-0282 | 2026-10-16 | Paper-forward cluster log from the EDGAR daily index with a pre-registered 100-signal bar | open | needs-a-run | yes | P-0163 **blocked** |
| H-0280 | 2026-10-15 | One live automation platform behind the website monthly fee | open | sound | no |  |
| H-0274 | 2026-10-15 | UK accounts editions | open | needs-a-run | no |  |
| H-0268 | 2026-10-15 | signal-timed outreach | open | needs-a-run | no |  |
| H-0264 | 2026-10-14 | score the 20-minute filter set on a dated cohort | open | needs-a-run | yes |  |
| H-0259 | 2026-10-14 | pull the stake at 5x versus holding | open | needs-a-run | yes | P-0155 **works** |
| H-0254 | 2026-10-14 | crypto spot pairs laggard check | open | needs-a-run | yes | P-0153 **works** |
| H-0252 | 2026-10-13 | Per-post CPM tracked per account feeding back into what gets made next | open | sound | no |  |
| H-0246 | 2026-10-13 | Flat monthly editing retainer for businesses already producing content | open | sound | no |  |
| H-0240 | 2026-10-13 | service x city landing pages | open | needs-a-run | no |  |
| H-0236 | 2026-10-13 | UGC creator marketplace that sources creator applications for brands fast | open | needs-a-run | no |  |
| H-0231 | 2026-10-13 | Tooling, leaderboards and data products built around a token launchpad | open | needs-a-run | yes | P-0137 **blocked** |
| H-0226 | 2026-10-13 | A small weekly prize or showcase as the community rung of the AI for Businesses or Bootcam | open | needs-a-run | no |  |
| H-0223 | 2026-10-11 | Public on-chain leaderboards as the check on any trader's claimed record | open | sound | yes | P-0127 **works** |
| H-0219 | 2026-10-11 | Phone-gated lead magnet to free workshop to done-for-you app build agency | open | sound | no |  |
| H-0214 | 2026-10-11 | Extract the free classroom for the product-validation and repeat-purchase method, if Luke  | open | sound | no |  |
| H-0212 | 2026-10-10 | Decomposing one classification into several narrow questions with weights fitted on a labe | open | needs-a-run | yes | P-0124 **blocked** |
| H-0206 | 2026-10-10 | Templates, thumbnails, overlays and pre-launch guides sold or published to creators before | open | needs-a-run | no |  |
| H-0200 | 2026-10-10 | UK shape of selling booking software through trade job software and profile booking button | open | needs-a-run | no |  |
| H-0198 | 2026-10-09 | x402 per-call payment rails for agents, Coinbase-originated, now under Linux Foundation go | open | sound | yes | P-0116 **works** |
| H-0192 | 2026-10-09 | Join and extract the four free communities that cover both asks: Emerging Fashion Designer | open | sound | no |  |
| H-0186 | 2026-10-09 | A scoped UK test of one flip with the compliance costs priced first, only if Luke wants th | open | needs-a-run | no |  |
| H-0184 | 2026-10-08 | Whether LinkedIn search surfaces enough recent dental and aesthetics owner posts per week  | open | needs-a-run | no |  |
| H-0178 | 2026-10-08 | Code the five rules as a freqtrade strategy and score it on the two-year sample and payout | open | needs-a-run | yes | P-0104 **not-worth-it** |
| H-0172 | 2026-10-08 | An inducement filter as a variant on the WF-0350 paper test: one further sweep and recover | open | needs-a-run | yes | P-0103 **not-worth-it** |
| H-0170 | 2026-10-07 | Build a mock-up site for the prospect and send a 90-second Loom after a two-line permissio | open | needs-a-run | no |  |
| H-0164 | 2026-10-07 | A high-impact news filter for the S1 crypto bot, skip or flatten entries in a window aroun | open | needs-a-run | yes | P-0102 **works** |
| H-0158 | 2026-10-07 | Insider cluster-buy signal from the free Form 4 filings page as a paper desk | open | needs-a-run | yes | P-0101 **blocked** |
| H-0155 | 2026-10-06 | Getting a video into an agent as scene-change frames plus transcript, or via a bare URL to | open | sound | yes | P-0071 **works** |
| H-0150 | 2026-10-06 | Buying real human UGC clips from marketplaces and reselling them inside a client retainer | open | sound | no |  |
| H-0144 | 2026-10-06 | A 10 to 30 pound a day local lead-gen test for one Neptune client using the course build a | open | needs-a-run | no |  |
| H-0141 | 2026-10-05 | Niche paid community on owned material, borrowing only a proven model and price point | open | needs-a-run | no |  |
| H-0136 | 2026-10-05 | GBP setup and audit checklist | open | sound | no |  |
| H-0131 | 2026-10-05 | scroll-driven website skill | open | needs-a-run | yes |  |
| H-0127 | 2026-10-04 | node canvas workflows (Flows) | open | needs-a-run | no |  |
| H-0122 | 2026-10-04 | replication gap measured on demo | open | sound | no |  |
| H-0117 | 2026-10-04 | Benchmark DeepSeek, GLM and Kimi against the M5 qwen3.6 on non-personal rewrite and summar | open | sound | no |  |
| H-0113 | 2026-10-03 | Photoreal moving footage of a subject you cannot film, one consistent face and a directed  | open | needs-a-run | no |  |
| H-0108 | 2026-10-03 | Generating many platform-native variants (hooks, colour grades, overlays) from one filmed  | open | sound | no |  |
| H-0103 | 2026-10-03 | Whether a fees-paid threshold removes rugs without removing the launches that ran, on a da | open | needs-a-run | yes |  |
| H-0099 | 2026-10-02 | human reads flagged threads from alert links | open | needs-a-run | yes | P-0055 **works** |
| H-0094 | 2026-10-02 | Higgsfield Genjutsu as the final route for motion transfer, whole-frame recast at about 7  | open | sound | no |  |
| H-0089 | 2026-10-02 | Whether multi-buy and net-flow signals from tracked wallets predict price, measured on pap | open | needs-a-run | no |  |
| H-0085 | 2026-10-01 | Inbound AI receptionist demo line built from the home services voice prompt | open | sound | no |  |
| H-0080 | 2026-10-01 | One pay-as-you-go fal account to run Seedance, Kling, Wan and lip-sync models by API | open | sound | no |  |
| H-0075 | 2026-10-01 | Adapt the web design CLAUDE.md for phone-first UK local business sites | open | sound | no |  |
| H-0071 | 2026-09-30 | Partnership ads run through a local client's own social handle | open | sound | no |  |
| H-0066 | 2026-09-30 | Consistent AI character content with clear AI disclosure | open | sound | no |  |
| H-0061 | 2026-09-30 | Learning crypto research from a source with an independently verifiable track record | open | sound | no |  |
| H-0058 | 2026-09-29 | Post-production for businesses that have long-form content but cannot cut it into short-fo | open | sound | no |  |
| H-0054 | 2026-09-29 | Media-buying commission taken as a share of a brand's ad budget | open | needs-a-run | no |  |
| H-0049 | 2026-09-29 | Join for one month with Skool neptune, transcribe the classroom into Education/Courses/ai- | open | sound | no |  |

## Tools shelf

Tools, repos and datasets the judge said to fetch, kept here even when nothing needs them today. Each is a candidate
for a ran-it night: install it in `sandbox/`, run it, write the verdict.

| id | date | tool | why | from | status |
|---|---|---|---|---|---|
| T-0199 | 2026-10-19 | [REA reverse-engineering MCP](https://github.com/morluto/rea) | Looks inside the game binary, which coop-anything depends on for path two. | H-0322 (cranebeaker/coop-anything: Co-op Anything: point y) | shelf |
| T-0198 | 2026-10-19 | [coop-anything](https://github.com/cranebeaker/coop-anything) | The playbook, skills and MCP server. | H-0322 (cranebeaker/coop-anything: Co-op Anything: point y) | shelf |
| T-0197 | 2026-10-19 | [Baileys](https://github.com/WhiskeySockets/Baileys) | The unofficial WhatsApp Web library such projects rely on. | H-0321 (Show HN: WhatsApp MCP running free on Cloudflare) | shelf |
| T-0196 | 2026-10-19 | [whatsapp-mcp (finereli)](https://github.com/finereli/whatsapp-mcp) | The Cloudflare Worker and MCP server to read. | H-0321 (Show HN: WhatsApp MCP running free on Cloudflare) | shelf |
| T-0195 | 2026-10-19 | [tv-vibehack](https://github.com/Gathin23/tv-vibehack) | Holds PROMPT.md and the launcher source. | H-0312 (Gathin23/tv-vibehack: Your TV, minus the ads. Debl) | shelf |
| T-0194 | 2026-10-19 | [Android platform-tools (adb)](https://developer.android.com/tools/releases/platform-tools) | The debug bridge the whole method rests on. | H-0312 (Gathin23/tv-vibehack: Your TV, minus the ads. Debl) | shelf |
| T-0193 | 2026-10-17 | [claudemy](https://github.com/assafkip/claudemy) | Skill and citation checker to read and reuse. | H-0309 (assafkip/claudemy: Claudemy: an open-source altern) | shelf |
| T-0192 | 2026-10-17 | [Things to Do API](https://thingstodoapi.com/) | The live service, to inspect coverage. | H-0308 (Show HN: Things to Do API) | shelf |
| T-0191 | 2026-10-17 | [web-ocean](https://github.com/Noniv/web-ocean) | The page and source to run. | H-0304 (Noniv/web-ocean: Real-time WebGPU ocean renderer w) | shelf |
| T-0190 | 2026-10-17 | [skills CLI](https://www.skills.sh/) | Installer used by the repo. | H-0301 (muend/geoai-skills (new in awesome-claude-code)) | shelf |
| T-0189 | 2026-10-17 | [geoai-skills](https://github.com/muend/geoai-skills) | Skill files and benchmark format to copy. | H-0301 (muend/geoai-skills (new in awesome-claude-code)) | shelf |
| T-0188 | 2026-10-17 | [EnvTraverse framework](https://arxiv.org/abs/2610.22289) | Baseline agent and framework named in the paper; link on the abstract page. | H-0299 (Improving Environment-Agnostic Coding Agents: The ) | shelf |
| T-0187 | 2026-10-17 | [blender-ai-mcp-addon](https://github.com/anujasid/blender-ai-mcp-addon) | The add-on itself, to read the tool definitions. | H-0298 (anujasid/blender-ai-mcp-addon: AI assistant and MC) | shelf |
| T-0186 | 2026-10-17 | [Blender](https://www.blender.org/download/) | The host app the tools drive. | H-0298 (anujasid/blender-ai-mcp-addon: AI assistant and MC) | shelf |
| T-0185 | 2026-10-16 | [Leonxlnx/earshot](https://github.com/Leonxlnx/earshot) | The CLI and MCP server to install and run. | H-0290 (Leonxlnx/earshot: Ears for coding agents: let AI h) | shelf |
| T-0184 | 2026-10-16 | [MLE-Bench](https://github.com/openai/mle-bench) | The public benchmark the paper's Lite split is drawn from. | H-0285 (MLExpert: Towards a Generalist Agentic Model for A) | shelf |
| T-0183 | 2026-10-16 | [pro-vi/cc-stretch](https://github.com/pro-vi/cc-stretch) | The plugin and its bench folder. | H-0284 (pro-vi/cc-stretch: Stretchtext replies for Claude ) | shelf |
| T-0182 | 2026-10-16 | [yfinance](https://github.com/ranaroussi/yfinance) | Free daily prices to score the 21-day forward return. | H-0282 (Paper-forward cluster log from the EDGAR daily ind) | shelf |
| T-0181 | 2026-10-16 | [SEC EDGAR full-index and Form 4 XML](https://www.sec.gov/Archives/edgar/daily-index/) | Public source of the filings; rate limit 10 requests a second with a User-Agent. | H-0282 (Paper-forward cluster log from the EDGAR daily ind) | shelf |
| T-0180 | 2026-10-15 | [Twilio](https://www.twilio.com/) | Programmable UK number and SMS if building the missed-call text back directly (paid, needs an account). | H-0280 (One live automation platform behind the website mo) | shelf |
| T-0179 | 2026-10-15 | [funes-memory dataset](https://huggingface.co/datasets/huggingface/funes-memory) | Public sample memory to inspect structure. | H-0279 (huggingface/funes (new in awesome-claude-code)) | shelf |
| T-0178 | 2026-10-15 | [funes](https://github.com/huggingface/funes) | Reference implementation of session recall. | H-0279 (huggingface/funes (new in awesome-claude-code)) | shelf |
| T-0177 | 2026-10-15 | [decomp.dev](https://decomp.dev) | Index of public matching-decomp projects and their progress data. | H-0276 (i12bp8/decomp.wtf: What The Function: your AI agen) | shelf |
| T-0176 | 2026-10-15 | [decomp.wtf](https://github.com/i12bp8/decomp.wtf) | Reference implementation of the byte-match loop (archived, v0.10.6). | H-0276 (i12bp8/decomp.wtf: What The Function: your AI agen) | shelf |
| T-0175 | 2026-10-15 | [Xero demo company](https://www.xero.com/uk/) | Free demo company to test a UK accounts connector against. | H-0274 (UK accounts editions) | shelf |
| T-0174 | 2026-10-15 | [mcd-saver-strategist](https://github.com/hujjun/mcd-saver-strategist) | Offline optimizer and self-test to run. | H-0270 (hujjun/mcd-saver-strategist: 麦当劳省钱点餐助手（麦门精算师）｜麦当劳优) | shelf |
| T-0173 | 2026-10-15 | [Companies House bulk product and API](https://developer.company-information.service.gov.uk/) | Free feed of new UK company incorporations as a signal source (API key is free but needs an account). | H-0268 (signal-timed outreach) | shelf |
| T-0172 | 2026-10-14 | [roast-room](https://github.com/nateherkai/roast-room) | The council prompts and local viewer. | H-0266 (nateherkai/roast-room: Seven AI advisors (Bezos, P) | shelf |
| T-0171 | 2026-10-14 | [Postfix](https://www.postfix.org/) | Self-hosted SMTP with policy hooks to implement first-sender locking. | H-0265 (Show HN: I wrote an email app that accepts only on) | shelf |
| T-0170 | 2026-10-14 | [OpenTelemetry Jaeger](https://www.jaegertracing.io/download/) | Viewer for the exported OTLP traces. | H-0261 (YeonwooSung/my-claude-code-mods: Custom Claude Cod) | shelf |
| T-0169 | 2026-10-14 | [my-claude-code-mods](https://github.com/YeonwooSung/my-claude-code-mods) | The mods and their core test suite. | H-0261 (YeonwooSung/my-claude-code-mods: Custom Claude Cod) | shelf |
| T-0168 | 2026-10-14 | [herk-edit-kit](https://github.com/nateherkai/herk-edit-kit) | The scripts for silence cutting, EDL review and retiming. | H-0256 (nateherkai/herk-edit-kit: Herk Edit Kit by Nate He) | shelf |
| T-0167 | 2026-10-14 | [PulseOS Hugging Face weights](https://huggingface.co/PulseOS) | The tuned 0.6B parser the write-up describes. | H-0255 (Show HN: Pulse Local, a Mac budgeting app whose AI) | shelf |
| T-0166 | 2026-10-14 | [Ollama](https://ollama.com/download) | Local runtime for small Qwen3 models. | H-0255 (Show HN: Pulse Local, a Mac budgeting app whose AI) | shelf |
| T-0165 | 2026-10-14 | [statsmodels coint test](https://www.statsmodels.org/) | Engle-Granger cointegration test to select pairs without eyeballing. | H-0254 (crypto spot pairs laggard check) | shelf |
| T-0164 | 2026-10-14 | [Binance public klines API](https://data-api.binance.vision/api/v3/klines) | Keyless hourly candles for spot pairs. | H-0254 (crypto spot pairs laggard check) | shelf |
| T-0163 | 2026-10-13 | [Lean 4](https://github.com/leanprover/lean4) | The proof checker that makes each record verifiable. | H-0249 (SqueezeBench: Saturation-Resilient Evaluation of M) | shelf |
| T-0162 | 2026-10-13 | [plur-bench](https://github.com/plur-ai/plur-bench) | The reproducible harness behind every published number. | H-0245 (plur-ai/plur (new in awesome-claude-code)) | shelf |
| T-0161 | 2026-10-13 | [MCP Inspector](https://github.com/modelcontextprotocol/inspector) | Lists and calls a server's tools so a fuzz harness can be driven against them. | H-0243 (ToFu: Exploiting and Fuzzing the LLM-Orchestrator-) | shelf |
| T-0160 | 2026-10-13 | [new-term-radar](https://github.com/zhuyansen/new-term-radar) | Reference code for the GitHub breakout and Hugging Face trending checks. | H-0242 (zhuyansen/new-term-radar: Daily radar for new AI t) | shelf |
| T-0159 | 2026-10-13 | [Astro](https://github.com/withastro/astro) | Static site generator to render one page per service and town row. | H-0240 (service x city landing pages) | shelf |
| T-0158 | 2026-10-13 | [agent-standup](https://github.com/Atoll92/agent-standup) | The tool itself, run with npx @double_geste/agent-standup. | H-0238 (Atoll92/agent-standup: Your Claude Code, Codex and) | shelf |
| T-0157 | 2026-10-13 | [atticus-mac](https://github.com/SaarthurR/atticus-mac) | The source for the router and replay cache. | H-0237 (Show HN: Atticus – Hold-to-talk voice assistant fo) | shelf |
| T-0156 | 2026-10-13 | [JAX](https://github.com/jax-ml/jax) | The benchmark is built on JAX environments. | H-0234 (OpenSocialJax: Evaluating Social Adaptation in Seq) | shelf |
| T-0155 | 2026-10-13 | [Ghostty](https://ghostty.org) | Terminal that supports the image protocol the plugin needs. | H-0233 (iamumeransari/claude-show-your-work: Claude Code s) | shelf |
| T-0154 | 2026-10-13 | [py_trees](https://github.com/splintered-reality/py_trees) | Python behaviour-tree library. | H-0229 (BT-Agent: Deploying Onboard Robot Agents with Beha) | shelf |
| T-0153 | 2026-10-13 | [axe-core](https://github.com/dequelabs/axe-core) | Free accessibility checker used in the QA pass. | H-0228 (juliobsz/skills: An agent skill that builds award-) | shelf |
| T-0152 | 2026-10-13 | [skills CLI](https://github.com/vercel-labs/skills) | Installs agent skills from GitHub repos. | H-0228 (juliobsz/skills: An agent skill that builds award-) | shelf |
| T-0151 | 2026-10-13 | [Firecracker](https://github.com/firecracker-microvm/firecracker) | Open source microVM manager commonly used for dense sandbox packing. | H-0227 (Launch HN: Agent37 (YC F26) – Low-cost agent sandb) | shelf |
| T-0150 | 2026-10-11 | [Remotion](https://www.remotion.dev) | The render engine the template uses, for comparison with HyperFrames. | H-0224 (liyupi/ai-promo-video-maker: 一句话让 AI 帮你做产品宣传片！把产品名) | shelf |
| T-0149 | 2026-10-11 | [ai-promo-video-maker](https://github.com/liyupi/ai-promo-video-maker) | The AGENTS.md workflow and helper scripts to borrow the checks from. | H-0224 (liyupi/ai-promo-video-maker: 一句话让 AI 帮你做产品宣传片！把产品名) | shelf |
| T-0148 | 2026-10-11 | [Solana Tracker](https://www.solanatracker.io) | Wallet PnL data and API with a free tier. | H-0223 (Public on-chain leaderboards as the check on any t) | shelf |
| T-0147 | 2026-10-11 | [tau2-bench](https://github.com/sierra-research/tau2-bench) | The public benchmark the paper used. | H-0221 (TRACE: Diagnosing Verifier Brittleness in Agentic ) | shelf |
| T-0146 | 2026-10-11 | [Twilio Verify](https://www.twilio.com/en-us/user-authentication-identity/verify) | The usual SMS code check for a phone gate (paid, trial credit). | H-0219 (Phone-gated lead magnet to free workshop to done-f) | shelf |
| T-0145 | 2026-10-11 | [Ollama](https://ollama.com) | Local open-weight models, needed to repeat the with and without comparison keyless. | H-0217 (Narrow and Deep: An Ontology Tower as the Knowledg) | shelf |
| T-0144 | 2026-10-11 | [agent-browser](https://github.com/vercel-labs/agent-browser) | The CLI the relay is paired with. | H-0216 (aindeev/agent-chrome-relay: Let your AI agents use) | shelf |
| T-0143 | 2026-10-11 | [agent-chrome-relay](https://github.com/aindeev/agent-chrome-relay) | The relay and extension. | H-0216 (aindeev/agent-chrome-relay: Let your AI agents use) | shelf |
| T-0142 | 2026-10-11 | [Agent Client Protocol](https://agentclientprotocol.com) | The spec and schema the app speaks. | H-0215 (Show HN: Littleguys – Claude Code, Codex and OpenC) | shelf |
| T-0141 | 2026-10-11 | [littleguys](https://littleguys.hervalicio.us) | The app itself, to see ACP permission cards working. | H-0215 (Show HN: Littleguys – Claude Code, Codex and OpenC) | shelf |
| T-0140 | 2026-10-11 | [Keepa price and rank history](https://keepa.com) | Free tier shows Amazon sales rank history, a public demand proxy for product selection. | H-0214 (Extract the free classroom for the product-validat) | shelf |
| T-0139 | 2026-10-10 | [scikit-learn](https://scikit-learn.org/) | Logistic regression for the weights. | H-0212 (Decomposing one classification into several narrow) | shelf |
| T-0138 | 2026-10-10 | [UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) | Public labelled text for the held-out test. | H-0212 (Decomposing one classification into several narrow) | shelf |
| T-0137 | 2026-10-10 | [bill10/agent-007](https://github.com/bill10/agent-007) | The app. | H-0211 (bill10/agent-007 (new in awesome-claude-code)) | shelf |
| T-0136 | 2026-10-10 | [LOBSTER sample data](https://lobsterdata.com/info/DataSamples.php) | Free sample order book files to check distributions. | H-0207 (Can you use autoregressive diffusion to generate m) | shelf |
| T-0135 | 2026-10-10 | [Google Trends via pytrends](https://github.com/GeneralMills/pytrends) | Keyless search-interest series to size demand. | H-0206 (Templates, thumbnails, overlays and pre-launch gui) | shelf |
| T-0134 | 2026-10-10 | [agents-can-communicate](https://github.com/automatis-tools/agents-can-communicate) | The package. | H-0205 (automatis-tools/agents-can-communicate (new in awe) | shelf |
| T-0133 | 2026-10-10 | [data.police.uk API docs](https://data.police.uk/docs/) | Endpoint list and rate limits. | H-0204 (Code Demo - Web-scraping with API's) | shelf |
| T-0132 | 2026-10-10 | [Habitat-sim](https://github.com/facebookresearch/habitat-sim) | Simulator that runs HM3D scenes. | H-0203 (SuperNav: An Agentic Navigation System for Any Tas) | shelf |
| T-0131 | 2026-10-10 | [SuperNav project page](https://zju3dv.github.io/SuperNav/) | Code and demos if released. | H-0203 (SuperNav: An Agentic Navigation System for Any Tas) | shelf |
| T-0130 | 2026-10-10 | [wheresryan22/anatomy](https://github.com/wheresryan22/anatomy) | The skill and kit itself. | H-0202 (wheresryan22/anatomy: A Claude Code skill that tur) | shelf |
| T-0129 | 2026-10-10 | [Google Business Profile booking links](https://support.google.com/business/answer/6218536) | Documents the appointment URL field that needs no partner approval. | H-0200 (UK shape of selling booking software through trade) | shelf |
| T-0128 | 2026-10-10 | [Cal.com (open source)](https://github.com/calcom/cal.com) | Self-hostable booking page to use as the widget base. | H-0200 (UK shape of selling booking software through trade) | shelf |
| T-0127 | 2026-10-09 | [x402 reference repo](https://github.com/coinbase/x402) | Spec and example endpoints | H-0198 (x402 per-call payment rails for agents, Coinbase-o) | shelf |
| T-0126 | 2026-10-09 | [Optuna](https://github.com/optuna/optuna) | Baseline optimiser to warm-start | H-0195 (A Closer Look at Agentic BBO: Benchmarking LLM Age) | shelf |
| T-0125 | 2026-10-09 | [agentic-bbo](https://github.com/lamda-bbo/agentic-bbo) | Benchmark code from the paper | H-0195 (A Closer Look at Agentic BBO: Benchmarking LLM Age) | shelf |
| T-0124 | 2026-10-09 | [founder-skill](https://github.com/Jakeschincariol/founder-skill) | The skill pack and Python tools | H-0194 (Jakeschincariol/founder-skill: Eleven free Claude ) | shelf |
| T-0123 | 2026-10-09 | [Rust toolchain (rustup)](https://rustup.rs/) | Likely needed to build the benchmark | H-0191 (4da-systems/4da (new in awesome-mcp-servers)) | shelf |
| T-0122 | 2026-10-09 | [4DA](https://github.com/4da-systems/4da) | Repo with the benchmark | H-0191 (4da-systems/4da (new in awesome-mcp-servers)) | shelf |
| T-0121 | 2026-10-09 | [JASPAR](https://jaspar.elixir.no/) | Open TF motif database | H-0189 (Unlocking the Regulatory Genome by ARGUS: An Evide) | shelf |
| T-0120 | 2026-10-09 | [ADASTRA allele-specific binding database](https://adastra.autosome.org/) | Public data source the paper queries | H-0189 (Unlocking the Regulatory Genome by ARGUS: An Evide) | shelf |
| T-0119 | 2026-10-09 | [Swift toolchain (Xcode command line tools)](https://developer.apple.com/xcode/) | Needed to build the binary | H-0188 (franzenzenhofer/big-arrow-on-the-screen: Let your ) | shelf |
| T-0118 | 2026-10-09 | [big-arrow-on-the-screen](https://github.com/franzenzenhofer/big-arrow-on-the-screen) | The CLI and skill itself | H-0188 (franzenzenhofer/big-arrow-on-the-screen: Let your ) | shelf |
| T-0117 | 2026-10-09 | [GOV.UK MOT history data](https://www.gov.uk/check-mot-history) | Mileage and failure history to spot clocked or problem cars | H-0186 (A scoped UK test of one flip with the compliance c) | shelf |
| T-0116 | 2026-10-09 | [DVLA Vehicle Enquiry Service API](https://developer-portal.driver-vehicle-licensing.api.gov.uk/) | Free-tier lookup of tax and MOT status to screen listings (needs a key, so a later-night fetch) | H-0186 (A scoped UK test of one flip with the compliance c) | shelf |
| T-0115 | 2026-10-08 | [puppeteer](https://pptr.dev/) | Headless browser frame capture, if not bundled. | H-0180 (cth9191/animate: Procedural animation in any style) | shelf |
| T-0114 | 2026-10-08 | [cth9191/animate](https://github.com/cth9191/animate) | The skill and demo pieces. | H-0180 (cth9191/animate: Procedural animation in any style) | shelf |
| T-0113 | 2026-10-08 | [RECAST paper](https://arxiv.org/abs/2610.10507) | Check for linked code or data. | H-0175 (RECAST: Learning to Compute the Right Context thro) | shelf |
| T-0112 | 2026-10-08 | [gitleaks](https://github.com/gitleaks/gitleaks) | Secret scanner for the same pattern. | H-0174 (openqodex/openqodex: Open source AI code review fo) | shelf |
| T-0111 | 2026-10-08 | [semgrep](https://github.com/semgrep/semgrep) | Free SAST scanner of the kind it wraps. | H-0174 (openqodex/openqodex: Open source AI code review fo) | shelf |
| T-0110 | 2026-10-08 | [openqodex](https://github.com/openqodex/openqodex) | The tool itself. | H-0174 (openqodex/openqodex: Open source AI code review fo) | shelf |
| T-0109 | 2026-10-08 | [pandas](https://pandas.pydata.org/) | Swing detection and signal counting. | H-0172 (An inducement filter as a variant on the WF-0350 p) | shelf |
| T-0108 | 2026-10-08 | [Binance public klines API](https://developers.binance.com/docs/binance-spot-api-docs/rest-api/market-data-endpoints) | Keyless 5m candle history for the test. | H-0172 (An inducement filter as a variant on the WF-0350 p) | shelf |
| T-0107 | 2026-10-07 | [@armature-tech/agent-reviews](https://www.npmjs.com/package/@armature-tech/agent-reviews) | CLI to inspect how reviews are sent. | H-0171 (Show HN: Agent.reviews – Where AI agents read and ) | shelf |
| T-0106 | 2026-10-07 | [agent.reviews](https://agent.reviews/) | Public site to read. | H-0171 (Show HN: Agent.reviews – Where AI agents read and ) | shelf |
| T-0105 | 2026-10-07 | [Loom](https://www.loom.com/) | Free tier for short walkthrough recordings. | H-0170 (Build a mock-up site for the prospect and send a 9) | shelf |
| T-0104 | 2026-10-07 | [agent-workbench](https://github.com/cvelasquez/agent-workbench) | The package under test. | H-0169 (cvelasquez/agent-workbench (new in awesome-claude-) | shelf |
| T-0103 | 2026-10-07 | [mortiflix-oss](https://github.com/GTKottman/mortiflix-oss) | Repo to clone and run the demo. | H-0166 (GTKottman/mortiflix-oss: A motion design studio on) | shelf |
| T-0102 | 2026-10-07 | [Durable Actors](https://github.com/TerseAI/durable-actors) | The open-source repo with Helm chart. | H-0165 (Show HN: Durable Actors – OSS Durable Objects with) | shelf |
| T-0101 | 2026-10-07 | [Binance public klines](https://api.binance.com/api/v3/klines) | Keyless hourly BTC candles for the volatility comparison. | H-0164 (A high-impact news filter for the S1 crypto bot, s) | shelf |
| T-0100 | 2026-10-07 | [Faireconomy weekly calendar JSON](https://nfs.faireconomy.media/ff_calendar_thisweek.json) | Keyless weekly feed of events with impact ratings. | H-0164 (A high-impact news filter for the S1 crypto bot, s) | shelf |
| T-0099 | 2026-10-07 | [MedZERO paper](https://arxiv.org/abs/2610.08327) | Read for the promotion rule and check for a code link. | H-0161 (MedZERO: Self-Evolving Agents for Open-Ended Medic) | shelf |
| T-0098 | 2026-10-07 | [Stooq daily CSV](https://stooq.com/) | Keyless daily price history for forward returns. | H-0158 (Insider cluster-buy signal from the free Form 4 fi) | shelf |
| T-0097 | 2026-10-07 | [SEC EDGAR full-index and Form 4 XML](https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4) | Free primary source for insider filings, no key, needs a User-Agent. | H-0158 (Insider cluster-buy signal from the free Form 4 fi) | shelf |
| T-0096 | 2026-10-06 | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | Local speech recognition used by default. | H-0157 (Charlesmpc/by2kb: Forward videos from IM to transc) | shelf |
| T-0095 | 2026-10-06 | [by2kb](https://github.com/Charlesmpc/by2kb) | The video to Markdown knowledge-base pipeline. | H-0157 (Charlesmpc/by2kb: Forward videos from IM to transc) | shelf |
| T-0094 | 2026-10-06 | [OpenChart](https://github.com/longsurf-ai/openchart) | The app that wires alerts to an agent. | H-0156 (Show HN: OpenChart – OSS TradingView alternative w) | shelf |
| T-0093 | 2026-10-06 | [Tea language](https://github.com/longsurf-ai/tea) | The indicator and alert-condition language OpenChart uses. | H-0156 (Show HN: OpenChart – OSS TradingView alternative w) | shelf |
| T-0092 | 2026-10-06 | [3d-asset-server](https://github.com/arielshad/3d-asset-server) | The server, CLI and MCP tools themselves. | H-0152 (arielshad/3d-asset-server: 3d assets api and mcp) | shelf |
| T-0091 | 2026-10-06 | [Bubblewrap](https://github.com/GoogleChromeLabs/bubblewrap) | Builds the TWA Android bundle from a PWA. | H-0149 (degordonstech/pwa2play (new in awesome-claude-code) | shelf |
| T-0090 | 2026-10-06 | [SPARQLWrapper](https://github.com/RDFLib/sparqlwrapper) | Python client for SPARQL endpoints. | H-0147 (Wikidata Search Traces: A Dataset for Training Kno) | shelf |
| T-0089 | 2026-10-06 | [Wikidata Query Service](https://query.wikidata.org/) | Public SPARQL endpoint to check uniqueness of nested conditions. | H-0147 (Wikidata Search Traces: A Dataset for Training Kno) | shelf |
| T-0088 | 2026-10-06 | [mg-styles-15](https://github.com/Vincentwei1021/mg-styles-15) | The prompts, style notes and source for 15 code-drawn film styles. | H-0146 (Vincentwei1021/mg-styles-15: 15 motion design styl) | shelf |
| T-0087 | 2026-10-05 | [Whop](https://whop.com) | Community and checkout hosting with a free tier. | H-0141 (Niche paid community on owned material, borrowing ) | shelf |
| T-0086 | 2026-10-05 | [HazardWeaver](https://github.com/LabRAI/HazardWeaver) | Code released by the authors. | H-0139 (HazardWeaver: Scientific Route Selection for Hazar) | shelf |
| T-0085 | 2026-10-05 | [mesh-avatar-studio](https://github.com/shinshin86/mesh-avatar-studio) | The editor and agent guide. | H-0138 (shinshin86/mesh-avatar-studio: Turn one illustrati) | shelf |
| T-0084 | 2026-10-05 | [astral](https://github.com/sffjunkie/astral) | Python sun position and twilight times. | H-0137 (Show HN: Nightwatch – a Mac menu-bar app that tell) | shelf |
| T-0083 | 2026-10-05 | [7Timer](http://www.7timer.info/doc.php) | Free second forecast for disagreement checks. | H-0137 (Show HN: Nightwatch – a Mac menu-bar app that tell) | shelf |
| T-0082 | 2026-10-05 | [Open-Meteo API](https://open-meteo.com/en/docs) | Keyless hourly cloud cover by layer. | H-0137 (Show HN: Nightwatch – a Mac menu-bar app that tell) | shelf |
| T-0081 | 2026-10-05 | [Google Keyword Planner](https://ads.google.com/home/tools/keyword-planner/) | Search volume for service-plus-city phrases. | H-0136 (GBP setup and audit checklist) | shelf |
| T-0080 | 2026-10-05 | [Google Places API (New)](https://developers.google.com/maps/documentation/places/web-service/overview) | Structured listing and category data, with a free monthly credit. | H-0136 (GBP setup and audit checklist) | shelf |
| T-0079 | 2026-10-05 | [McStas](https://mcstas.org) | The neutron ray-trace simulator the grader runs. | H-0134 (NeutronGym: Physics-Graded Neutron Instrument Desi) | shelf |
| T-0078 | 2026-10-05 | [Playwright](https://playwright.dev) | Headless browser used to capture scroll-state screenshots. | H-0131 (scroll-driven website skill) | shelf |
| T-0077 | 2026-10-05 | [scroll-craft](https://github.com/nateherkai/scroll-craft) | The skill and verifier itself, MIT licensed. | H-0131 (scroll-driven website skill) | shelf |
| T-0076 | 2026-10-04 | [Stockfish](https://stockfishchess.org) | Reference opponent for rating a bot | H-0130 (I Ran a Chess Programming Tournament!) | shelf |
| T-0075 | 2026-10-04 | [python-chess](https://github.com/niklasf/python-chess) | Legal moves and engine play for a local tournament runner | H-0130 (I Ran a Chess Programming Tournament!) | shelf |
| T-0074 | 2026-10-04 | [replica-skill](https://github.com/Jakeschincariol/replica-skill) | The eleven skills and Python tools to run | H-0129 (Jakeschincariol/replica-skill: Eleven free Claude ) | shelf |
| T-0073 | 2026-10-04 | [ComfyUI](https://github.com/comfyanonymous/ComfyUI) | Free open-source node-graph runner for the same chaining pattern | H-0127 (node canvas workflows (Flows)) | shelf |
| T-0072 | 2026-10-04 | [live-panel-skill](https://github.com/ythx-101/live-panel-skill) | The renderer and examples | H-0124 (ythx-101/live-panel-skill: Config-driven animated ) | shelf |
| T-0071 | 2026-10-04 | [eToro API portal](https://api-portal.etoro.com) | Demo copy-trading endpoints and docs | H-0122 (replication gap measured on demo) | shelf |
| T-0070 | 2026-10-04 | [answer-me-with-html](https://github.com/QingYunA/answer-me-with-html) | The skill and bundled CLI to run | H-0119 (QingYunA/answer-me-with-html: Answer me with HTML ) | shelf |
| T-0069 | 2026-10-04 | [promptfoo](https://github.com/promptfoo/promptfoo) | Runs the same prompt set across several providers and scores them | H-0117 (Benchmark DeepSeek, GLM and Kimi against the M5 qw) | shelf |
| T-0068 | 2026-10-04 | [NVIDIA Build API catalogue](https://build.nvidia.com) | The free hosted open-weight endpoint to benchmark against | H-0117 (Benchmark DeepSeek, GLM and Kimi against the M5 qw) | shelf |
| T-0067 | 2026-10-03 | [Remotion](https://github.com/remotion-dev/remotion) | The best-known alternative React video renderer to compare with HyperFrames. | H-0110 (zhuyansen/awesome-claude-video-skills: Open-source) | shelf |
| T-0066 | 2026-10-03 | [awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills) | The list itself, source for further video-skill repos. | H-0110 (zhuyansen/awesome-claude-video-skills: Open-source) | shelf |
| T-0065 | 2026-10-03 | [Dune](https://dune.com) | Free tier SQL over Solana transactions for a larger dated sample, needs an account so later. | H-0103 (Whether a fees-paid threshold removes rugs without) | shelf |
| T-0064 | 2026-10-03 | [Solana public JSON-RPC](https://api.mainnet-beta.solana.com) | Keyless getSignaturesForAddress and getTransaction to sum fees per pool, rate limited. | H-0103 (Whether a fees-paid threshold removes rugs without) | shelf |
| T-0063 | 2026-10-02 | [Node.js 20+](https://nodejs.org) | Runtime the package requires | H-0101 (ericmmartin/youtube-transcript-plus: YouTube Trans) | shelf |
| T-0062 | 2026-10-02 | [youtube-transcript-plus](https://github.com/ericmmartin/youtube-transcript-plus) | The library under test | H-0101 (ericmmartin/youtube-transcript-plus: YouTube Trans) | shelf |
| T-0061 | 2026-10-02 | [Breadcrumb MCP tool definitions](https://innerloop.works/breadcrumb/mcp) | Read the tool list to measure definition size | H-0100 (Show HN: Breadcrumb, record everything on your mac) | shelf |
| T-0060 | 2026-10-02 | [Poly Haven](https://polyhaven.com) | CC0 textures and reference models | H-0098 (elithril/blender-kiln (new in awesome-claude-code)) | shelf |
| T-0059 | 2026-10-02 | [Blender](https://www.blender.org) | Required runtime | H-0098 (elithril/blender-kiln (new in awesome-claude-code)) | shelf |
| T-0058 | 2026-10-02 | [blender-kiln](https://github.com/elithril/blender-kiln) | The skill and the fidelity_check script | H-0098 (elithril/blender-kiln (new in awesome-claude-code)) | shelf |
| T-0057 | 2026-10-02 | [LDView](https://tcobbs.github.io/ldview/) | Renderer for checking models | H-0095 (Show HN: Made an open-source Lego AI generator) | shelf |
| T-0056 | 2026-10-02 | [LDraw parts library](https://www.ldraw.org/parts/latest-parts.html) | Part definitions needed for validation | H-0095 (Show HN: Made an open-source Lego AI generator) | shelf |
| T-0055 | 2026-10-02 | [ldraw-nova](https://github.com/anteloc/ldraw-nova) | The toolset under test | H-0095 (Show HN: Made an open-source Lego AI generator) | shelf |
| T-0054 | 2026-10-02 | [Higgsfield](https://higgsfield.ai) | Genjutsu route under test | H-0094 (Higgsfield Genjutsu as the final route for motion ) | shelf |
| T-0053 | 2026-10-02 | [Kling Motion Control](https://klingai.com) | Comparison route for the same source clip | H-0094 (Higgsfield Genjutsu as the final route for motion ) | shelf |
| T-0052 | 2026-10-02 | [KaTeX](https://katex.org) | Formula re-typesetting | H-0091 (Edwardxlai/easyread: 把英文论文读成舒服的中文：本地 PDF 论文翻译、原文对照) | shelf |
| T-0051 | 2026-10-02 | [easyread](https://github.com/Edwardxlai/easyread) | Reference implementation of per-page translation | H-0091 (Edwardxlai/easyread: 把英文论文读成舒服的中文：本地 PDF 论文翻译、原文对照) | shelf |
| T-0050 | 2026-10-02 | [rhun](https://rhun.app/) | Source and releases to read the translator approach | H-0090 (Show HN: Rhun, an open-source code editor written ) | shelf |
| T-0049 | 2026-10-02 | [Solana public RPC / Helius free tier](https://www.helius.dev) | Swap history per wallet if the leaderboard sites block scraping | H-0089 (Whether multi-buy and net-flow signals from tracke) | shelf |
| T-0048 | 2026-10-02 | [GMGN wallet pages](https://gmgn.ai) | Per-wallet trade history for multi-buy and net-flow counts | H-0089 (Whether multi-buy and net-flow signals from tracke) | shelf |
| T-0047 | 2026-10-02 | [Kolscan leaderboard](https://kolscan.io) | Public ranked wallet list to seed the tracked set | H-0089 (Whether multi-buy and net-flow signals from tracke) | shelf |
| T-0046 | 2026-10-01 | [ClubElo API](http://clubelo.com/API) | Free Elo ratings, no key. | H-0087 (machina-sports/sports-skills: Open-source agent sk) | shelf |
| T-0045 | 2026-10-01 | [sports-skills](https://github.com/machina-sports/sports-skills) | The package under test. | H-0087 (machina-sports/sports-skills: Open-source agent sk) | shelf |
| T-0044 | 2026-10-01 | [Corral](https://github.com/Cardinal44/corral) | The tool. | H-0086 (Show HN: Corral – Kill every command your agent st) | shelf |
| T-0043 | 2026-10-01 | [n8n](https://github.com/n8n-io/n8n) | Self-hosted follow-up workflows. | H-0085 (Inbound AI receptionist demo line built from the h) | shelf |
| T-0042 | 2026-10-01 | [Vapi](https://vapi.ai) | Alternative voice-agent platform. | H-0085 (Inbound AI receptionist demo line built from the h) | shelf |
| T-0041 | 2026-10-01 | [Retell AI](https://www.retellai.com) | Hosted voice-agent loop with a free tier. | H-0085 (Inbound AI receptionist demo line built from the h) | shelf |
| T-0040 | 2026-10-01 | [scikit-learn](https://github.com/scikit-learn/scikit-learn) | Logistic regression and scoring. | H-0084 (What is Expected Goals?) | shelf |
| T-0039 | 2026-10-01 | [StatsBomb open-data](https://github.com/statsbomb/open-data) | Free shot-level event data with coordinates. | H-0084 (What is Expected Goals?) | shelf |
| T-0038 | 2026-10-01 | [librosa](https://github.com/librosa/librosa) | Acoustic measurements as evidence tools. | H-0083 (SEAR: Spoofing Evidence-Grounded Audio Reasoning B) | shelf |
| T-0037 | 2026-10-01 | [painted-animation](https://github.com/tuzhechen2005/painted-animation) | Hand-painted engine it builds on. | H-0082 (edenfunf/reelmimic: Show it a video you love. Get ) | shelf |
| T-0036 | 2026-10-01 | [ReelMimic](https://github.com/edenfunf/reelmimic) | The tool itself. | H-0082 (edenfunf/reelmimic: Show it a video you love. Get ) | shelf |
| T-0035 | 2026-10-01 | [fal client](https://github.com/fal-ai/fal) | Python client for the queue API. | H-0080 (One pay-as-you-go fal account to run Seedance, Kli) | shelf |
| T-0034 | 2026-10-01 | [mlx-lm](https://github.com/ml-explore/mlx-lm) | The underlying library and baseline. | H-0079 (Finally, The CORRECT Way to Run Local AI on a Mac) | shelf |
| T-0033 | 2026-10-01 | oMLX | The server under test; find the repo via the video description. | H-0079 (Finally, The CORRECT Way to Run Local AI on a Mac) | shelf |
| T-0032 | 2026-10-01 | [AppWorld](https://github.com/StonyBrookNLP/appworld) | Benchmark used to score harness changes. | H-0078 (Learning from Research: Toward Lifelong Agent Harn) | shelf |
| T-0031 | 2026-10-01 | [yomiyasu](https://github.com/nanaism/yomiyasu) | Reference skill layout and rule set to adapt. | H-0077 (nanaism/yomiyasu: AI生成の日本語を自然な日本語へ推敲するAgent Skill ) | shelf |
| T-0030 | 2026-10-01 | [Weave Router](https://github.com/weave-os/router) | The open-source router to run against a baseline. | H-0076 (Show HN: Open-source model routing for coding agen) | shelf |
| T-0029 | 2026-10-01 | [Lighthouse CLI](https://github.com/GoogleChrome/lighthouse) | Free mobile performance and accessibility scoring to judge generated sites. | H-0075 (Adapt the web design CLAUDE.md for phone-first UK ) | shelf |
| T-0028 | 2026-09-30 | [ffmpeg ebur128 filter](https://ffmpeg.org/ffmpeg-filters.html#ebur128-1) | Loudness measurement the scripts need. | H-0073 (echris6/motion-video-kit: Claude Code skill kit fo) | shelf |
| T-0027 | 2026-09-30 | [motion-video-kit](https://github.com/echris6/motion-video-kit) | The skill and measurement scripts. | H-0073 (echris6/motion-video-kit: Claude Code skill kit fo) | shelf |
| T-0026 | 2026-09-30 | [Parrot](https://github.com/turantekin/Parrot) | Source for the capture and co-pilot design. | H-0072 (Show HN: Parrot – Open-Source Smart Meeting Record) | shelf |
| T-0025 | 2026-09-30 | [tau-bench](https://github.com/sierra-research/tau-bench) | The benchmark family the layer sits over. | H-0069 (UserProxyBench: Evaluating LLM User Simulators for) | shelf |
| T-0024 | 2026-09-30 | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) | Native reverse engineering. | H-0068 (rehan-remade/universal-modder: Point Claude at any) | shelf |
| T-0023 | 2026-09-30 | [ILSpy](https://github.com/icsharpcode/ILSpy) | Decompiler for .NET games. | H-0068 (rehan-remade/universal-modder: Point Claude at any) | shelf |
| T-0022 | 2026-09-30 | [universal-modder](https://github.com/rehan-remade/universal-modder) | The plugin and um CLI. | H-0068 (rehan-remade/universal-modder: Point Claude at any) | shelf |
| T-0021 | 2026-09-30 | [C2PA c2patool](https://github.com/contentauth/c2patool) | Embed and inspect provenance metadata for disclosure. | H-0066 (Consistent AI character content with clear AI disc) | shelf |
| T-0020 | 2026-09-30 | [LIBERO](https://github.com/Lifelong-Robot-Learning/LIBERO) | Simulation benchmark the paper builds on. | H-0064 (MotorMind: Scaffolding General Vision Language Mod) | shelf |
| T-0019 | 2026-09-30 | [coucou](https://github.com/Louis-CFM/coucou) | Source to read for the hook event format. | H-0063 (Louis-CFM/coucou: A tiny friend that lives in your) | shelf |
| T-0018 | 2026-09-30 | [llama.cpp llama-bench](https://github.com/ggml-org/llama.cpp) | Baseline benchmark tool with fixed settings. | H-0062 (Launch HN: Magnitude (YC S25) – Self-optimizing in) | shelf |
| T-0017 | 2026-09-30 | [Magnitude](https://github.com/magnitudedev/magnitude) | The engine under test. | H-0062 (Launch HN: Magnitude (YC S25) – Self-optimizing in) | shelf |
| T-0016 | 2026-09-30 | [Wayback Machine CDX API](https://archive.org/help/wayback_api.php) | Independent timestamps for when a call was published. | H-0061 (Learning crypto research from a source with an ind) | shelf |
| T-0015 | 2026-09-29 | [Playwright](https://github.com/microsoft/playwright) | Headless Chromium frame capture. | H-0059 (Barty-Bart/motion-graphics: Motion-graphics skills) | shelf |
| T-0014 | 2026-09-29 | [motion-graphics](https://github.com/Barty-Bart/motion-graphics) | The skill, engine and worked example. | H-0059 (Barty-Bart/motion-graphics: Motion-graphics skills) | shelf |
| T-0013 | 2026-09-29 | [OpusClip alternatives: ClipsAI](https://github.com/ClipsAI/clipsai) | Open-source library that finds clip-worthy segments in long video. | H-0058 (Post-production for businesses that have long-form) | shelf |
| T-0012 | 2026-09-29 | [ffmpeg](https://ffmpeg.org/) | Cutting, cropping to vertical, and burning captions. | H-0058 (Post-production for businesses that have long-form) | shelf |
| T-0011 | 2026-09-29 | [arXiv 2609.35738](https://arxiv.org/abs/2609.35738) | Check for a linked code release and the evaluation sets. | H-0056 (Harness Learning Enables Generalizable Test-Time A) | shelf |
| T-0010 | 2026-09-29 | [CadQuery](https://github.com/CadQuery/cadquery) | Pure Python parametric CAD that an agent can drive with no GUI or licence. | H-0055 (CaptureGrubEnchant/SolidWorks: SolidWorks MCP Serv) | shelf |
| T-0009 | 2026-09-29 | [FreeCAD](https://github.com/FreeCAD/FreeCAD) | Free CAD with a Python API on macOS, a safe place to try the same agent-drives-CAD idea. | H-0055 (CaptureGrubEnchant/SolidWorks: SolidWorks MCP Serv) | shelf |
| T-0008 | 2026-09-29 | [Meta Ad Library](https://www.facebook.com/ads/library/) | Public data for seeing what a brand's competitors run before pitching. | H-0054 (Media-buying commission taken as a share of a bran) | shelf |
| T-0007 | 2026-09-29 | [SWE-bench Verified](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified) | The task suite whose traces the paper evaluates on. | H-0052 (TokenCast: Forecasting Token Consumption During LL) | shelf |
| T-0006 | 2026-09-29 | [TokenCast](https://github.com/DEFENSE-SEU/TokenCast) | The paper's code and evaluation scripts. | H-0052 (TokenCast: Forecasting Token Consumption During LL) | shelf |
| T-0005 | 2026-09-29 | [tmux](https://github.com/tmux/tmux) | Simplest way to keep many agent sessions alive and inspectable. | H-0051 (AgentSystemLabs/agent-office: A cartoon 3D office ) | shelf |
| T-0004 | 2026-09-29 | [node-pty](https://github.com/microsoft/node-pty) | Pseudo-terminal spawning for a home-built supervisor. | H-0051 (AgentSystemLabs/agent-office: A cartoon 3D office ) | shelf |
| T-0003 | 2026-09-29 | [agent-office](https://github.com/AgentSystemLabs/agent-office) | Read docs/how-it-works.md for the waiting-state detection. | H-0051 (AgentSystemLabs/agent-office: A cartoon 3D office ) | shelf |
| T-0002 | 2026-09-29 | [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Fast local transcription on the Mac if the current local pipeline is slow. | H-0049 (Join for one month with Skool neptune, transcribe ) | shelf |
| T-0001 | 2026-09-29 | [yt-dlp](https://github.com/yt-dlp/yt-dlp) | Pulls embedded lesson videos (Loom, Vimeo, YouTube) that a Skool classroom links to. | H-0049 (Join for one month with Skool neptune, transcribe ) | shelf |

## Skipped

| id | date | source | what | why |
|---|---|---|---|---|
| H-0323 | 2026-10-19 | hn | [Torvalds use Claude for bottleneck fix, but race discovered](https://thenewstack.io/torvalds-claude-code-kernel/) | News about a kernel patch with a race found in review; the fetched page is mostly newsletter boilerplate and gives no me |
| H-0319 | 2026-10-19 | awesome | [a1-x-tech/mcp-google-contacts (new in awesome-mcp-servers)](https://github.com/a1-x-tech/mcp-google-contacts) | A standard wrapper over the People API needing a Google OAuth login; the etag guard is routine. |
| H-0318 | 2026-10-19 | youtube | [Top 5 Claude Code Skills Everyone Needs in 2026](https://www.youtube.com/watch?v=gF30riZwUAc) | No transcript available and the title is a listicle. |
| H-0317 | 2026-10-19 | github | [LiCinCan/blender-ai-mcp-addon: AI assistant and MCP server for Blender: visual c](https://github.com/LiCinCan/blender-ai-mcp-addon) | A generic MCP server inside Blender; vendor already seen and the mechanism is the standard tool-call loop. |
| H-0316 | 2026-10-19 | hn | [Show HN: 500 clocks in one 6.3 MB HTML file by Opus 5.5](https://tkgally.github.io/500-clocks/) | A model showcase of 500 generated clock pages; no mechanism beyond repeated prompting. |
| H-0314 | 2026-10-19 | awesome | [nahumlitvin/prismantis (new in awesome-claude-code)](https://github.com/nahumlitvin/prismantis) | A cosmetic output theme for Claude Code; vendor already seen and the mechanism is presentation only. |
| H-0313 | 2026-10-19 | youtube | [The ONLY Claude Skills Tutorial Beginners Need in 2026](https://www.youtube.com/watch?v=TyB7kLZPVKo) | A beginner tutorial on what a skill is; the content is generic and already covered by the stack. |
| H-0311 | 2026-10-19 | hn | [Show HN: The Zelda timeline to catch up before the Ocarina of Time remake](https://legendofhyrule.com/) | A fan timeline site built with Claude; the page carries no mechanism beyond a visual layout. |
| H-0306 | 2026-10-17 | youtube | [What is a bonding curve? #shorts #bondingcurve #PumpFun #Solana #memecoin #crypt](https://www.youtube.com/watch?v=pTTm8lNQtO8) | A 20-second short that restates what a bonding curve is with no formula or numbers; the longer pump.fun item covers the  |
| H-0297 | 2026-10-17 | hn | [Show HN: Fakeipedia – Wikipedia for worlds that don't exist](https://fakeipedia.org) | A paid LLM wiki generator whose only mechanism is generating a page when a red link is clicked; no detail on how it is d |
| H-0295 | 2026-10-16 | hn | [Anthropic Console overcharged my card 100x due to internationalization input bug](https://news.ycombinator.com/item?id=50121562) | A single user complaint about a billing input bug; no mechanism beyond a decimal-comma parsing fault. |
| H-0293 | 2026-10-16 | awesome | [i18next/i18next-cli (new in awesome-claude-code)](https://github.com/i18next/i18next-cli) | Vendor already judged; a standard AST-based key extractor with no new mechanism for Proteus. |
| H-0292 | 2026-10-16 | youtube | [From the Classroom to the Workshop - UK MOT Tester Training](https://www.youtube.com/watch?v=DfF8mJM25QU) | Transcript disabled and the title points to a training course, not data analysis. |
| H-0289 | 2026-10-16 | hn | [Postgres 19 delayed after AI reviewers find more bugs than humans can fix](https://www.theregister.com/databases/2026/10/16/postgres-19-delayed-after-ai-reviewers-find-more-bugs-than-humans-can-fix/5303471) | News about a release delay; the comments carry no mechanism beyond AI review finding more bugs than can be fixed. |
| H-0287 | 2026-10-16 | awesome | [haabe/mycelium (new in awesome-claude-code)](https://github.com/haabe/mycelium) | Vendor already judged; the mechanism (assumption-logging gates in a plugin) is generic and its evidence is a Reddit post |
| H-0286 | 2026-10-16 | youtube | [This Chess AI NEVER Loses: How to Build Your Own Bot](https://www.youtube.com/watch?v=5DcaUHhu0KQ) | A generic Lichess bot tutorial; the Lichess bot already runs (P-0011) and the mechanism is the documented bot API plus S |
| H-0281 | 2026-10-15 | hn | [Show HN: Indigene – Native plants for where you stand](https://indigene.app/) | Consumer plant lookup app, body gives no usable mechanism beyond cross-referenced open data. |
| H-0278 | 2026-10-15 | youtube | [This Claude Code Skill Makes Your Usage Limit Last Way Longer](https://www.youtube.com/watch?v=g8lhaArp1U4) | Transcript unavailable (IpBlocked), title is a claim with no visible mechanism. |
| H-0275 | 2026-10-15 | hn | [Show HN: Petal, open-source CoScreen/ScreenHero finally free](https://petal.live/) | Screen-sharing tool relaunch, no mechanism relevant to the desks. |
| H-0273 | 2026-10-15 | awesome | [alexex1993/mcu-skills (new in awesome-claude-code)](https://github.com/alexex1993/mcu-skills) | Vendor already judged; one SKILL.md per board is the known skills pattern, nothing new. |
| H-0272 | 2026-10-15 | youtube | [Football Betting Algorithm in Python Explained](https://www.youtube.com/watch?v=MFYdwr5tL74) | Transcript unavailable (IpBlocked) and the Dixon-Coles desk already exists. |
| H-0271 | 2026-10-15 | arxiv | [From Relevance to Validity: Zero-Shot Tool Selection via Functional and Contextu](https://arxiv.org/abs/2610.20388) | Abstract names no method detail or numbers, only a claimed improvement in tool ranking. |
| H-0269 | 2026-10-15 | hn | [Why We're Banning AI](https://www.currentaffairs.org/news/why-were-banning-ai) | Opinion piece about a magazine banning AI writing, no mechanism. |
| H-0267 | 2026-10-14 | youtube | [AI Agent Memory Stack Explained / Rakesh Gohel](https://www.youtube.com/watch?v=UbZyh6OCx0g) | Transcript is only music markers, nothing to judge. |
| H-0263 | 2026-10-14 | youtube | [The Only 4 Types of Cars That Hold Their Value And Do Not Depreciate](https://www.youtube.com/watch?v=XVGeUUFRN5s) | A listicle summarising a third-party depreciation study with no mechanism to run. |
| H-0260 | 2026-10-14 | hn | [Show HN: A guided 3D Leonardo da Vinci museum, built in code](https://museumofages.org/w/vinci) | A showcase of a 3D museum; the mechanism is standard Three.js and offers nothing to test. |
| H-0258 | 2026-10-14 | youtube | [The AI Agent Memory Architecture Explained - From State to Long-Term Memory](https://www.youtube.com/watch?v=4KvVWNUTd9g) | Generic explainer of memory types with a customer-support demo and no new mechanism. |
| H-0253 | 2026-10-13 | hn | [Nearly all 19 car brands send driver data to third parties (Northeastern/CR)](https://news.auravision.co/car-is-spying/) | A vendor-founder promotional link to a secondary write-up of a study, with no mechanism in the post. |
| H-0251 | 2026-10-13 | awesome | [tronghieu/agent-skills (new in awesome-claude-code)](https://github.com/tronghieu/agent-skills) | A collection of prompt-style skills with no new mechanism; the vault has already judged it. |
| H-0248 | 2026-10-13 | github | [Arekejoker/qwen21-nsfw-pose-skill: Qwen-Image 2.1 NSFW/姿势出图 skill：作者级提示词配方 + NSF](https://github.com/Arekejoker/qwen21-nsfw-pose-skill) | An adult-image recipe for a local GPU diffusion stack; needs ComfyUI, large model downloads and hardware this Mac lacks, |
| H-0247 | 2026-10-13 | hn | [Launch HN: Consus (YC F24) – LLM gateway for companies handling sensitive data](https://news.ycombinator.com/item?id=50073471) | A compliance-gateway launch post whose content is certification claims, with no mechanism described. |
| H-0244 | 2026-10-13 | youtube | [What is xG? / By The Numbers](https://www.youtube.com/watch?v=zSaeaFcm1SY) | A four minute xG explainer with no build detail; the Python walkthrough in the same query covers the mechanism better. |
| H-0239 | 2026-10-13 | youtube | [The M5 Ultra Mac Studio is INSANE!](https://www.youtube.com/watch?v=YK98Cc592C8) | A product showcase of a maxed-out machine running one local model with no method or reproducible numbers beyond memory u |
| H-0232 | 2026-10-13 | hn | [Show HN: Opus 5.5 made a fully featured Figma clone in 3 hours / 8 prompts](https://www.mana.space/home/rZfbotNWAXegQypmpkzaAPFC6Mp1/Apps/Figma%20Next%20Launch) | A claim that a model built a Figma clone in eight prompts from the vendor of the harness, with no mechanism and a commen |
| H-0230 | 2026-10-13 | youtube | [How Pump.fun’s bonding curve actually works and why being early is basically the](https://www.youtube.com/watch?v=1YZAObOuSaU) | A short restating that price rises along a bonding curve, already judged and with nothing new beyond a lawsuit claim. |
| H-0225 | 2026-10-11 | youtube | [How to Build Your First MCP Server (in Less Than 5 Minutes)](https://www.youtube.com/watch?v=Y4bpWRLdRoA) | Beginner MCP server tutorial with no new mechanism. |
| H-0220 | 2026-10-11 | github | [LingCore/WinShun: Win顺：免费开源的 Windows 快速搜索启动器。双击 Ctrl，拼音秒搜文件、全文搜索 Word/Excel/PDF、](https://github.com/LingCore/WinShun) | Windows-only launcher; the MFT index and MCP search server do not run on this Mac. |
| H-0218 | 2026-10-11 | youtube | [How the Top 1% Use Claude Code Differently](https://www.youtube.com/watch?v=J9NQTYUP6k0) | Generic Claude Code advice (brief, guardrails, definition of done); overlaps the other Claude Code video, which is kept. |
| H-0213 | 2026-10-10 | github | [transkatgirl/vibeclaude: A port of opencode-buttplugio to Claude Code written by](https://github.com/transkatgirl/vibeclaude) | Novelty plugin needing physical hardware; the hook to daemon to websocket path is generic. |
| H-0210 | 2026-10-10 | youtube | [Tutorial 2: Understanding the UK Data Service Open Data API](https://www.youtube.com/watch?v=P5cwP-HK8uI) | The API needs a key and covers one survey dataset; the police API item is the better open-data one. |
| H-0209 | 2026-10-10 | arxiv | [Forms of LLM-Integrated Applications from LLM-Chats to Autonomous AI Agent Syste](https://arxiv.org/abs/2610.11899) | A survey of labels and architectures with no mechanism to run. |
| H-0208 | 2026-10-10 | github | [Autumn1337/better-statusline: A status line for Claude Code: the session's figur](https://github.com/Autumn1337/better-statusline) | A cosmetic status line plugin; the cache countdown and spend bars are display, not a new mechanism. |
| H-0201 | 2026-10-10 | hn | [`123456' password used in Danish CPR data breach](https://cphpost.dk/2026-10-10/news/round-up/123456-password-used-in-massive-danish-cpr-data-breach/) | News report of a breach with a weak password; no mechanism to record. |
| H-0199 | 2026-10-09 | hn | [Show HN: Apogee: Rebuilding Mozilla's Orbit, fully local and private](https://github.com/darshi1337/apogee) | Generic local summariser extension using Ollama and WebGPU; no new mechanism. |
| H-0197 | 2026-10-09 | awesome | [a1-x-tech/mcp-google-crux (new in awesome-mcp-servers)](https://github.com/a1-x-tech/mcp-google-crux) | Thin wrapper over a public API that needs a Google Cloud key. |
| H-0196 | 2026-10-09 | youtube | [How Expected Goals xG Actually Works](https://www.youtube.com/watch?v=h32AlMsWV-o) | Transcript blocked, and xG explainers carry no new mechanism for the Pitch. |
| H-0193 | 2026-10-09 | hn | [Show HN: Edi Life OS – self-hosted life dashboard with an MCP server for AI](https://github.com/edrisranjbar/lifeos) | A generic self-hosted dashboard with an MCP wrapper; no new mechanism. |
| H-0190 | 2026-10-09 | youtube | [Local AI on a Mac Is a Waste of Money (M5 Pro vs a $20 Subscription)](https://www.youtube.com/watch?v=kLNDGwaHohE) | Transcript blocked and the title is an opinion claim with no visible mechanism. |
| H-0187 | 2026-10-09 | hn | [Yandex Takes a Second Data Center Hit in 48 Hours](https://united24media.com/war-in-ukraine/yandex-takes-a-second-data-center-hit-in-48-hours-now-its-biggest-russian-site-is-damaged-23277) | War news about a data centre strike with no mechanism to test. |
| H-0185 | 2026-10-08 | hn | [Show HN: TerrainSR – fast, realistic heightmap upscaling model](https://huggingface.co/joe-gibbs/terrainsr) | Game terrain upscaling model, unrelated to any desk or interest. |
| H-0183 | 2026-10-08 | awesome | [larcane97/clausona (new in awesome-claude-code)](https://github.com/larcane97/clausona) | Account profile switcher with a vault verdict and no new mechanism beyond config-directory symlinks. |
| H-0181 | 2026-10-08 | arxiv | [LOCAA: An Agentic System for Automated Lossy Compressor Tuning](https://arxiv.org/abs/2610.10487) | Narrow to scientific compressor tuning, and the agent-with-memory pattern is already common. |
| H-0179 | 2026-10-08 | hn | [Show HN: Terse, a Claude Code plugin that halves reply length by cutting filler](https://github.com/lowenbjer/claude-terse) | The post describes a problem and weeks of trial, but no mechanism for how the plugin cuts reply length. |
| H-0177 | 2026-10-08 | awesome | [1160054/claude-code-zsh-completion (new in awesome-claude-code)](https://github.com/1160054/claude-code-zsh-completion) | A shell completion script with a vault verdict and no new mechanism. |
| H-0176 | 2026-10-08 | youtube | [DVSA Enforcement Action August 2026 / What MOT Testers & AEs Need to Know #motte](https://www.youtube.com/watch?v=3-nZZPICCt8) | Compliance news talk with no data pipeline or mechanism to record. |
| H-0173 | 2026-10-08 | hn | [I think I found a planet nobody knew existed. I used Claude Code to find it](https://www.reddit.com/r/ClaudeAI/s/mbe5IY2LF9) | Only a headline and joke comments in the brief, no mechanism described. |
| H-0168 | 2026-10-07 | youtube | [MCP Tutorial: Build Your First MCP Server and Client from Scratch (Free Labs)](https://www.youtube.com/watch?v=RhTiAOGwbYE) | Beginner MCP tutorial, transcript unavailable and nothing new. |
| H-0167 | 2026-10-07 | arxiv | [M3SunAgent: Monocular 3D Spatial Understanding Agent for Metric Depth Estimation](https://arxiv.org/abs/2610.07982) | Vision research paper on depth estimation with no relevance or runnable slice for any desk. |
| H-0163 | 2026-10-07 | awesome | [cooklang/cooklang-skills (new in awesome-claude-code)](https://github.com/cooklang/cooklang-skills) | A domain-specific skills pack over an MCP server; no new mechanism beyond skills plus MCP. |
| H-0162 | 2026-10-07 | youtube | [Anthropic Just Revealed 10 NEW Rules for Claude Skills](https://www.youtube.com/watch?v=VQyYzLJ6xos) | Transcript unavailable and title is listicle hype with no visible mechanism. |
| H-0160 | 2026-10-07 | github | [JimmySadek/video-fetcher-to-markdown: Portable AI-agent skill: turn YouTube, Ins](https://github.com/JimmySadek/video-fetcher-to-markdown) | Duplicates the existing keyless YouTube transcript pipeline and local transcription already in the stack. |
| H-0159 | 2026-10-07 | hn | [Tell HN: Apple not letting removal of AI models on macOS 27 is outrageous](https://news.ycombinator.com/item?id=49993338) | Consumer complaint about Apple model storage with no mechanism worth recording. |
| H-0154 | 2026-10-06 | youtube | [The Four Types of Memory Every AI Agent Needs](https://www.youtube.com/watch?v=BacJ6sEhqMo) | A generic explainer of agent memory types with no new mechanism for Proteus. |
| H-0151 | 2026-10-06 | hn | [Claude Code’s suggested message feature: I think the real customer is the model](https://www.zohaib.cc/blog/smartest-claude-code-feature) | An opinion piece on a product feature; the mechanism (model predicts next user prompt) is thin and disputed in the comme |
| H-0148 | 2026-10-06 | youtube | [How Car Origin Affects Depreciation in the UAE? 🏎️](https://www.youtube.com/watch?v=1dbh-4kz8JA) | A spoken claim about UAE depreciation by origin with no method or data shown. |
| H-0145 | 2026-10-06 | hn | [Engineer says Claude Code has made his job "soul-sucking"](https://www.techspot.com/news/113937-engineer-claude-code-has-made-job-soul-sucking.html) | Opinion and commentary about job satisfaction with no mechanism. |
| H-0143 | 2026-10-05 | youtube | [Why Solana’s Momentum Is Only Going to Accelerate — MoonPay’s CEO Ivan Soto-Wrig](https://www.youtube.com/watch?v=IEpfsf8fmnU) | A CEO interview claim with no mechanism. |
| H-0142 | 2026-10-05 | github | [VoltAgent/official-mcp-servers: A curated directory of 280+ official MCP servers](https://github.com/VoltAgent/official-mcp-servers) | A curated link list with no mechanism of its own. |
| H-0140 | 2026-10-05 | youtube | [Why xG is Lying To Us 🤷‍♂️🤷‍♂️](https://www.youtube.com/watch?v=bZ2HeZe_NNw) | Pundit talk with no model or mechanism. |
| H-0135 | 2026-10-05 | youtube | [Apple’s New M5 Max Changes the Local AI Story](https://www.youtube.com/watch?v=XGe7ldwFLSE) | A hardware first-look with benchmark numbers and no reusable mechanism. |
| H-0132 | 2026-10-05 | hn | [Denmark data breach exposes 8.8M people's personal data](https://www.cpr.dk/cpr-nyt/nyhedsarkiv/2026/okt/omfattende-uautoriseret-adgang-til-borgeres-cpr-oplysninger) | News of a national register breach with stolen personal data and no mechanism to record. |
| H-0128 | 2026-10-04 | hn | [Ask HN: Is anybody producing good code with coding agents?](https://news.ycombinator.com/item?id=49934037) | An opinion thread on code quality from coding agents, with no testable mechanism. |
| H-0126 | 2026-10-04 | youtube | [3 most common reasons your car could fail its MOT in the UK!](https://www.youtube.com/watch?v=zq65xVu3iq8) | A thirty-second listicle of common MOT failures with no mechanism or data source. |
| H-0123 | 2026-10-04 | hn | [Show HN: Our space game has a built-in RISC-V emulator that runs Linux](https://againstallodds.games/blog/2026/10/03/our-risc-v-emulator-pasriscv/) | A game's RISC-V emulator write-up, interesting engineering but no mechanism relevant to any desk. |
| H-0121 | 2026-10-04 | youtube | [Stop Losing Trades: Why I Switched to PumpSniper / Solana Sniper BOT](https://www.youtube.com/watch?v=YCYkK0yUBXA) | A promotional video for a sniper bot, with unverified claims and no mechanism beyond buzzwords. |
| H-0118 | 2026-10-04 | hn | [Show HN: Thoreau BASIC – What if BASIC hadn't gone out of fashion?](https://thoreaubasic.com/) | A BASIC interpreter showcase with no bearing on any desk or interest. |
| H-0115 | 2026-10-03 | github | [TimMacy/YouTubeAlchemy: This userscript for YouTube offers 250+ layout changes a](https://github.com/TimMacy/YouTubeAlchemy) | A browser UI userscript; its transcript export is clipboard and DOM scraping that the keyless pipeline already covers. |
| H-0114 | 2026-10-03 | hn | [Show HN: Pi pod – Run your pi coding agent in sandboxes on your own server](https://pipod.dev/) | Self-hosted sandbox for one coding agent; comments say it matches running a container, with no new mechanism. |
| H-0112 | 2026-10-03 | youtube | [Building an MCP server in 2 minutes....](https://www.youtube.com/watch?v=Fhy_VFMlE9s) | Generic two-minute MCP server tutorial. |
| H-0109 | 2026-10-03 | hn | [Show HN: Offrun – manage every coding agent from one workspace](https://offrun.dev/) | Product launch for an agent dashboard; claim only, comments ask what it adds over existing tools. |
| H-0107 | 2026-10-03 | youtube | [Claude Code: The Advanced Guide (99% of Devs Skip These Features)](https://www.youtube.com/watch?v=kt5a-TXmWew) | Beginner listicle of Claude Code features Proteus already runs. |
| H-0105 | 2026-10-03 | github | [nykooi1/vibe-wise: A Claude Code plugin that helps you learn how to build while ](https://github.com/nykooi1/vibe-wise) | A teaching-style plugin that makes Claude ask for the approach first; no mechanism Proteus needs beyond ordinary skills  |
| H-0104 | 2026-10-03 | hn | [Getting the most out of Opus 5.5 in Claude and Claude Code](https://claude.dev/blog/getting-the-most-out-of-opus-5-5/) | Opinion thread praising a model with anecdotes and no mechanism. |
| H-0102 | 2026-10-02 | youtube | [Why Cars Lose Their Value So Fast](https://www.youtube.com/watch?v=Ao7fbajRSKI) | No transcript came back (IpBlocked) and a generic news explainer carries no mechanism. |
| H-0097 | 2026-10-02 | youtube | [Tutorial 1: Getting Started with the UK Data Service Open Data API](https://www.youtube.com/watch?v=JIh6h8mx0Zk) | No transcript came back (IpBlocked) and a beginner tutorial title gives no mechanism. |
| H-0096 | 2026-10-02 | github | [zlxlabs/VideoTranscriptAPI: 基于 Python 3.11+ FastAPI 的异步音视频转录服务，支持 YouTube、小宇宙、Bi](https://github.com/zlxlabs/VideoTranscriptAPI) | Duplicates the transcript pipeline already in the stack and its parsing depends on a paid referral API key. |
| H-0093 | 2026-10-02 | awesome | [dailydotdev/daily (new in awesome-claude-code)](https://github.com/dailydotdev/daily) | Vault has judged the vendor and the README shows a standard tag-based news feed with nothing new. |
| H-0092 | 2026-10-02 | youtube | [Agent memory architecture explained #agentmemory #workingmemory #episodicmemory](https://www.youtube.com/watch?v=Ir0Q9s6P050) | No transcript came back (IpBlocked) and the title alone carries no mechanism. |
| H-0088 | 2026-10-01 | youtube | [What is a Bonding Curve? Explained in Less Than 1 Minute! #defi #daos #blockchai](https://www.youtube.com/watch?v=LI8WkvWpJJc) | A one-minute generic explainer of bonding curves with no mechanism beyond the definition the Grinder already covers. |
| H-0081 | 2026-10-01 | hn | [Show HN: Strata – an expressive semantic layer that can say no to your LLM](https://strata.do/) | A product pitch for a semantic layer with claims but no inspectable mechanism beyond naming rules. |
| H-0074 | 2026-09-30 | youtube | [Chess Engine in Python - Part 2 - Moving the pieces](https://www.youtube.com/watch?v=o24J3WcBGLg) | Beginner tutorial on mouse input for a chess GUI, no mechanism relevant to a bot. |
| H-0067 | 2026-09-30 | hn | [Show HN: A working 3D model of an Enigma machine](https://enigma.design) | A 3D explainer site with no reusable mechanism beyond prompt-built models. |
| H-0065 | 2026-09-30 | youtube | [day in the life of a wfh data analyst.](https://www.youtube.com/watch?v=RC30UibhowE) | Lifestyle vlog with no transcript and no mechanism. |
| H-0060 | 2026-09-29 | youtube | [Building a Real App with Claude Code (Start to Finish)](https://www.youtube.com/watch?v=misjUj4Q_ho) | Transcript unavailable and a generic build-an-app tutorial with no mechanism to record. |
| H-0057 | 2026-09-29 | youtube | [MCP Servers Explained & Built](https://www.youtube.com/watch?v=He8tUwLzLnU) | Transcript unavailable and a generic MCP tutorial title with no mechanism to record. |
| H-0053 | 2026-09-29 | youtube | [Claude Code Full Course 2026 / How Senior Engineers Actually Build with AI](https://www.youtube.com/watch?v=u2QqWkMv3Lg) | Transcript unavailable and the title is a generic beginner course claim with no mechanism. |
| H-0050 | 2026-09-29 | hn | [Show HN: Durable Actor Session Protocol](https://dasp-protocol.github.io/dasp/) | The post text names a protocol and its motivation but gives no mechanism, and the comments show the author has not yet a |
| H-0047 | 2026-09-28 | youtube | [Car Depreciation Explained and How to Beat it](https://www.youtube.com/watch?v=XWz0HiXVrIY) | Generic consumer advice with a lender's marketing claims and no mechanism or data source; its own example figures are on |
| H-0044 | 2026-09-28 | youtube | [Open Data - How do I connect data using API](https://www.youtube.com/watch?v=_00jicHRIKk) | A three minute how-to for one portal that needs an account and API key, with no mechanism beyond a CSV export link. |
| H-0041 | 2026-09-28 | hn | [Show HN: PaperMono, e-ink fridge magnet shopping list with mobile web page](https://github.com/seamusc/papermono-shopping-list) | A hobby build on specific hardware with no mechanism beyond an ESP32 web sync, and the author says it was vibe-coded. |
| H-0035 | 2026-09-27 | hn | [OpenAI Codex agents go rogue and consumes USD 78,000 without authorization](https://news.ycombinator.com/item?id=49861047) | Single unverified user anecdote with no mechanism, logs or reproduction, essentially a claim dressed as news. |
| H-0028 | 2026-09-27 | youtube | [Mac mini M6: is 32GB enough to run local AI?](https://www.youtube.com/watch?v=6z9PbFSkX3g) | Recap of Apple's own announced specs with no independent benchmark; the memory-bandwidth point is general knowledge, not |
| H-0026 | 2026-09-27 | github | [ZeroPointRepo/youtube-skills: YouTube Transcript API skills for AI agents. Get t](https://github.com/ZeroPointRepo/youtube-skills) | Marketing wrapper around an opaque hosted API (TranscriptAPI), no technical detail on how it actually gets transcripts,  |
| H-0024 | 2026-09-26 | hn | [Ask HN: I just talked to an AI-obsessed client, and I need a shower afterwards](https://news.ycombinator.com/item?id=49826029) | Anecdotal complaint thread about a client's plans for AI marketing and review automation, no technical mechanism describ |
| H-0023 | 2026-09-26 | youtube | [Chess Engine in Python - Part 1 - Drawing the board](https://www.youtube.com/watch?v=EnYui0e73Rs) | Part 1 of a beginner tutorial series covering only pygame board setup and piece images, no engine logic yet. |
| H-0020 | 2026-09-26 | youtube | [Nearly one third of all MOTs in the UK failed this year 😳 here are the top 5 rea](https://www.youtube.com/watch?v=QigAkv4Ion0) | Generic top-5 MOT failure listicle with anecdotal advice and no cited data source, just a presenter's opinion. |
| H-0016 | 2026-09-26 | youtube | [PumpFun Sniper Bot Guide! / How to Snipe Memecoins / Solana Sniper Bot EXPLAINED](https://www.youtube.com/watch?v=X6fE1C3IKRw) | Promotional walkthrough of a Solana sniper bot's UI and pricing tiers with no explanation of how listing detection or ex |
| H-0011 | 2026-09-26 | youtube | [What does my MOT result mean](https://www.youtube.com/watch?v=gRRWBTRwmTQ) | Generic consumer explainer of MOT pass/fail categories with no mechanism, tool or number to record. |
| H-0008 | 2026-09-26 | youtube | [How to make lichess bot](https://www.youtube.com/watch?v=oTuZrYCpxNU) | Auto-captions and a direct page re-fetch both returned only music and boilerplate, no recoverable technical content to r |
