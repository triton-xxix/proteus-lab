# Harvest brief, 2026-10-08

14 items shortlisted from 239 candidates (93 dropped as already seen, 17 carry a vault verdict on the vendor).

## 1. [vault] An inducement filter as a variant on the WF-0350 paper test: one further sweep and recovery after the structure shift before entry
key: vault:2026-10-08:an-inducement-filter-as-a-variant-on-the-wf-0350-paper-test-
url: https://www.instagram.com/reel/DePSq8KIuyj/
meta: {"vault_status": "open", "kind": "idea", "subject": "@joinproject30 reel: inducements, the final sweep before the real reversal", "date": "2026-10-08", "where": "TRITON-CORE/Research/links/2026-10-08-joinproject30-inducement-reel.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: A second column on the same test, no spend

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) A trading mentor teaching the smart-money concept of an inducement: after a market structure shift, wait for one more liquidity sweep before entering. A teaching clip and a mentorship funnel, no evidence. Not a rule set on its own, but definable as a filter: one further sweep and recovery after the structure shift. Belongs as a variant on the WF-0350 paper test of the five-rule box strategy, not as a new lane. Job: Find a rules-based intraday strategy that clears the DarwinIA or Breakout payout bar on paper (still open) Write-up: `TRITON-CORE/Research/links/2026-10-08-joinproject30-inducement-reel.md` Link: https://www.instagram.com/reel/DePSq8KIuyj/

## 2. [hn] I think I found a planet nobody knew existed. I used Claude Code to find it
key: hn:50002665
url: https://www.reddit.com/r/ClaudeAI/s/mbe5IY2LF9
discussion: https://news.ycombinator.com/item?id=50002665
meta: {"points": 96, "comments": 31, "created": "2026-10-08T07:07:34Z"}
query: claude code

comment (higeorge13): This is incredible use of AI tools. Big kudos!
comment (wartywhoa23): Found a planet and saved a granny. Wake me up when this planet is acknowledged by any astonomer community with more say than r/ClaudeAI.
comment (k310): Planet Claude? Asking for a friend.

## 3. [github] openqodex/openqodex: Open source AI code review for Claude Code and Codex, before you push. Scanners (SAST, secrets, dependencies, lint) on the lines you changed, then a separate reviewer process that checks every scanner finding and is given every changed line. No other API key.
key: gh:openqodex/openqodex
url: https://github.com/openqodex/openqodex
meta: {"stars": 421, "created": "2026-10-02", "pushed": "2026-10-08", "language": "TypeScript", "topics": ["agent-skills", "ai-agents", "ai-code-review", "claude-code", "claude-code-plugin", "claude-skills", "cline", "code-quality"]}
query: claude-code created:>{since} stars:>20

# OpenQodex

[](https://www.npmjs.com/package/openqodex)
[](LICENSE)
[](https://github.com/openqodex/openqodex/actions/workflows/ci.yml)

OpenQodex is open source AI code review for Claude Code and Codex. It runs before you push, from your coding agent or your terminal. One command, `openqodex review`, works out your change: the commits not yet pushed plus everything uncommitted. It runs the scanners that fit the changed files and keeps only findings on the lines you changed. Then it starts its own reviewer, a separate Claude Code or Codex process that reads a frozen copy of the change. The reviewer checks every scanner finding and is given every changed line. OpenQodex checks its answer with scripts, writes one report, and prints a short receipt: the verdict, one line per finding and the path of `report.html`, a local page that shows each finding under its line of code. You choose which findings your agent fixes. It needs Claude Code or Codex installed and logged in, and no other key, account or server.

## Install

For humans, in your terminal:

```
npx openqodex init
```

`init` finds Claude Code, Cursor, Codex CLI and Cline on your machine. It prints every file it will write and asks once. Then it names the reviewer it found, or what to fix, and reviews your change, or asks what to review when there is none. After that, say to your agent "review my change with openqodex", or run `~/.openqodex/bin/openqodex review` yourself: `init` prints that full path, since an npx install puts no `openqodex` on your `PATH`.

For agents, the same install, run by the agent for itself with no question:

```
npx -y openqodex@0.10.0 init --yes --agent  
```

` ` is `claude-code`, `codex`, `cursor` or `cline`. Or paste this prompt into your agent:

```
Install OpenQodex for yourself with `npx -y openqodex@0.10.0 init --yes --agent  `, where   is the agent you are: claude-code, codex, cursor or cline. Run it from this repository and allow it up to ten minutes: when a reviewer can start, it ends with a review of my current change.
Then tell me the verdict and the findings, or what its last lines say is missing.
```

Codex runs commands in a sandbox that by default cannot write outside the project or reach the network: from Codex, run the line in your own terminal instead.

The skill alone, with no push check, launcher or scanner download: `npx skills add openqodex/openqodex -g`. A later `init` replaces it with the skill it keeps up to date.

OpenQodex needs Node 22 or newer and git. It runs on macOS and Linux. On Windows, use WSL.

 

## What it does today

Four commands: `init`, `review`, `update` and `trust`. The commands hooks and agents call are listed in [docs/plumbing.md](docs/plumbing.md).

- `openqodex review` runs the whole review in one command: a frozen copy of the change, the scanners, the code graph, a reviewer process OpenQodex starts, script checks of its answer, and one report in `report.html`, `report.md`, `report.json` and `report.sarif`.
- When it ends, the terminal shows a receipt: the verdict, the reviewer's summary, one line per finding (number, severity, category, title, file and line) and the absolute paths of `report.html` and `report.md`. `--format markdown`, `json` or `sarif` still prints the whole report.
- `report.html` is one file on your disk: each changed file as a diff, each finding under its line, then the coverage, the scanners and the blast radius. It runs no script, loads nothing, escapes every string and redacts the s

## 4. [arxiv] RECAST: Learning to Compute the Right Context through Adaptive Evidence Routing
key: arxiv:2610.10507
url: https://arxiv.org/abs/2610.10507
meta: {"published": "2026-10-07", "authors": ["Yilun Hao", "Krishna Sayana", "Isabella Ye", "James S Ren"], "categories": ["cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Large language models are increasingly applied to tasks grounded in long, heterogeneous information sources. Conventional Retrieval-Augmented Generation (RAG) relies on fixed similarity-based retrieval, while agentic variants adapt queries and tool use but remain largely retrieval-centric. However, in many tasks, the evidence required for a solution is not explicitly present in any single source item. Instead, it must be derived through filtering, aggregation, or computation across multiple source items. In this work, we introduce RECAST (Routing Evidence through Computation, Access, and Synthesized Tools), a learned framework that formulates evidence construction as a sequential decision process over heterogeneous retrieval and computation operations, allowing evidence to be actively derived rather than merely retrieved. A lightweight RouterLM iteratively selects and formulates primitive operations or specifies customized operations for a frozen CompilerLM to translate into executable code. Once it judges the evidence sufficient, RouterLM passes the accepted evidence to a frozen AnswerLM to produce the final solution. We train RouterLM with supervised fine-tuning (SFT) followed by group relative policy optimization (GRPO). Across six heterogeneous benchmark families, RECAST achieves a mean success rate of 75.6%, outperforming the strongest large-model baseline by 15.9%. Moreover, training enables the Qwen3.5-9B RouterLM to outperform a training-free Gemini 3.5 Flash RouterLM by 5.0%. On three held-out benchmarks, RECAST improves over the strongest baseline by 15.0% on average, demonstrating strong zero-shot generalization across tasks and heterogeneous source representations.

## 5. [youtube] DVSA Enforcement Action August 2026 | What MOT Testers & AEs Need to Know #mottester #mechanic #dvsa
key: yt:3-nZZPICCt8
url: https://www.youtube.com/watch?v=3-nZZPICCt8
meta: {"channel": "MOT Expert", "rank": 2, "duration_min": 3}
query: MOT data analysis uk

# DVSA Enforcement Action August 2026 | What MOT Testers & AEs Need to Know #mottester #mechanic #dvsa
# MOT Expert
# https://www.youtube.com/watch?v=3-nZZPICCt8

[00:00] Hi guys, watching my driving school. DVSA just sent round latest update on the who got a citation and who didn't. You can read it for yourselves but like in terms of things that got picked up this this time round. Vehicles not on site and gross negligence. Obviously you know what that is. Poor test standards. It's just somebody not doing the job properly. Somebody failed to declare a conviction. So for those of you who are unaware that anything that require that gets you uh and 1/2 pound fine in a court of law
[00:33] regardless what it's for, you must declare. If you receive more than 60 hours community service, you must declare. Um Driving license bans not so much of an issue. So you can continue test even if you lose your driving license but you can't do a demo test though. Um but the other thing that you need to declare as well is any act of um any act of assault, uh fraud, dishonesty, um anything basically that results as well in a 3-month or more suspended sentence, you have to declare and tell DVSA. Um so obviously somebody's failed to make on that.
[01:06] Um there's also one for breach of security. Breach of security, that'll be somebody logging you on somebody else's account or having passwords and user IDs stored on a public access computer. It's one of the things we preach around here which is make sure you do not store user IDs let alone the passwords. I mean just just take it all off. Just clear it down. Um there are software available softwares available out there that will will sort of take care of that. Um we have one um ourselves that we use and it erases every computer every 2 hours so that nobody has access to it because obviously we have a lot of students and
[01:38] more students coming through the building. Um again, poor test standards, more breach of security, vehicles not on site, vehicle not on site. And my my favorite one here is the AE no longer in control. This is where a business where the owners and the AE the company such um whoever the authorized entity is has taken a step back, decided that they might can run it or one of the guys on site. They're out the country. They think it's all good. But yet, they retain the law for responsibility for that site. And it's been approved that these individuals were not
[02:11] in control of the site. So, somebody else is running it on their behalf. This is basically spurious testing, so it's You know, it's like having a beard, a cover-up. Um but yeah, it's not allowed. So, that was one of the big things as well, which was interesting cuz obviously that was a an auto dealership. Uh big dealership group um up north by looks of it. But, things happen. Uh one of the things you need to make sure is the administration. If you're unsure about the administration behind running the business, operating the AE, anything wrong with those lines or if you do get yourselves in a spot bother with the DVSA, you do need to talk to
[02:43] somebody, please reach out to us. Uh Ross at MIT Expert MIT Compliance Group, if you want to give me a shout. Uh 01604 422 700. More than happy to talk to you guys. And let me know. All right, take care. >> [music]

## 6. [awesome] 1160054/claude-code-zsh-completion (new in awesome-claude-code)
key: gh:1160054/claude-code-zsh-completion
url: https://github.com/1160054/claude-code-zsh-completion
meta: {"list": "awesome-claude-code", "stars": 13, "created": "2025-12-12", "language": "Shell", "description": "Zsh completion for the Claude Code CLI: press TAB to see every command and option with what it does, plus your own sessions, MCP servers and agents. 120 languages."}
query: awesome-claude-code
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

[](https://github.com/1160054/claude-code-zsh-completion/releases)
[](LICENSE)

# claude-code-zsh-completion

Zsh completion for the Claude Code CLI. Press TAB after `claude` and every
command, subcommand and option shows up with what it does, so you can build a
command without opening `--help`.

Names from your own setup complete too: sessions (by their name or first
prompt), MCP servers, agents, models, plugins and background sessions.
In 120 languages and regional variants.

## Install

```bash
brew tap 1160054/claude https://github.com/1160054/claude-code-zsh-completion
brew trust 1160054/claude
brew install claude-code-zsh-completion
```

No `~/.zshrc` changes needed.

 
 Without Homebrew 

```bash
mkdir -p ~/.zsh/completions
curl -o ~/.zsh/completions/_claude \
  https://raw.githubusercontent.com/1160054/claude-code-zsh-completion/main/completions/_claude
```

Then in `~/.zshrc`, before `compinit`:

```bash
fpath=(~/.zsh/completions $fpath)
```

Plugin managers load it as a plugin: `zinit light 1160054/claude-code-zsh-completion`,
`antigen bundle 1160054/claude-code-zsh-completion`, or for Oh My Zsh clone it into
`$ZSH_CUSTOM/plugins/claude-code` and add `claude-code` to `plugins=(...)`.

 

## Other languages

Every file in [`completions/`](completions/) is the same completion in another
language (`_claude.ja`, `_claude.de`, `_claude.zh-CN`, …). Use one in place of
`_claude`; with Homebrew:

```bash
ln -sf "$(brew --prefix)/share/claude-code-zsh-completion/completions/_claude.ja" \
  "$(brew --prefix)/share/zsh/site-functions/_claude"
```

Not completing after an install or a switch? Run `rm -f ~/.zcompdump && exec zsh`.

## License

MIT

## 7. [vault] Code the five rules as a freqtrade strategy and score it on the two-year sample and payout tests S1 used
key: vault:2026-10-08:code-the-five-rules-as-a-freqtrade-strategy-and-score-it-on-
url: https://www.instagram.com/reel/DbJMHpDMK-1/
meta: {"vault_status": "open", "kind": "idea", "subject": "@windsorjrtrades reel: the five-rule 15m and 5m box strategy (order block, gap, sweep, 2R)", "date": "2026-10-08", "where": "TRITON-CORE/Research/links/2026-10-08-windsorjrtrades-fvg-strategy-reel.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: No spend, agent or Proteus work, publish either way

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) A retail smart-money pattern stated as five rules: 15-minute bias, a 5-minute impulse box with a gap between candles one and three, a break of the prior low and return to the box, entry on the second candle closing past the first, stop at the first candle, take profit at two times risk. No record offered. Fully specified, so it can be coded and scored on paper against the payout rules the vault already uses. Not for hand trading. Job: Find a rules-based intraday strategy that clears the DarwinIA or Breakout payout bar on paper (still open) Write-up: `TRITON-CORE/Research/links/2026-10-08-windsorjrtrades-fvg-strategy-reel.md` Link: https://www.instagram.com/reel/DbJMHpDMK-1/

## 8. [hn] Show HN: Terse, a Claude Code plugin that halves reply length by cutting filler
key: hn:49995809
url: https://github.com/lowenbjer/claude-terse
discussion: https://news.ycombinator.com/item?id=49995809
meta: {"points": 23, "comments": 14, "created": "2026-10-07T17:16:48Z"}
query: claude code

I struggle with the way Claude speaks to me when I do work. So much text, every, single, time. When I ask a question, I get an essay back, and with so many weird constructs: slogans, metaphors, recaps, strange choice of nouns, "it's not X, it's Y". Claude's own "concise" mode shortens it, somewhat, but keeps the the rest of the slop. I tried system prompts, those got forgotten after a couple of turns. I tried looking for plugins but none consistently made Claude speak normally. Some where slash commands, other solved for token use, others solved for neurodivergence. I just wanted to not read an essay and make Claude get to the point fast, every single time. Is that so much to ask? Apparently; it took me weeks of trial and error to make something that worked for me, I have stories, but I'm sharing it as a claude code plugin with you, those of you who struggle with Claude, the same way I did.
comment (trashymctrash): Opus 5.5 has reduced this to an acceptable level for me. Are you also using this plugin with that model?
comment (TZubiri): Read up on Chain of Thought The model is essentially thinking out loud, when you ask it to be more concise, you make it think less, therefore producing more erroneous answers. Some models have an internal chain of thought (claude being one of them), which sometimes isn't even published to avoid reverse engineering, but it seems that this might still be a problem. What you'd want actually is a layer that summarizes the actual answer, but that's actually an internal prompt by claude that you are not seeing, the model just doesn't expose the necessary bits for you to hack this together. Try anoth
comment (citizenfishy): Claude Mods seem to answer this pain better without affecting the model reasoning

## 9. [github] cth9191/animate: Procedural animation in any style for Claude Code: short single-file canvas videos with story, look and storyboard check-ins. 7 built-in styles or one matched from your references, your own music (beat-mapped), real product screenshots, every format from one piece.
key: gh:cth9191/animate
url: https://github.com/cth9191/animate
meta: {"stars": 219, "created": "2026-10-04", "pushed": "2026-10-05", "language": "JavaScript", "topics": ["animation", "canvas", "claude-code", "claude-code-plugin", "claude-code-skill", "explainer-video", "generative-art", "motion-graphics"]}
query: claude-code created:>{since} stars:>20

# Animate — procedural animation in any style, for Claude Code

A Claude Code skill that makes short animated videos entirely in code: one ` `, drawn and scored procedurally, deterministic frame by frame, rendered to MP4 with a headless browser and ffmpeg. Explainers, histories, little stories — in one of the built-in styles, or in a new look matched from your own references.

*The built-in styles, each a frame from its demo piece: cut paper, crosshatch ink, riso print, sketchbook, math, pixel, isometric — and the eighth slot: any other look, made from your references.*

## How it works

The skill walks you through a few questions, then makes you approve three cheap things before it spends time animating:

| step | what you see | you decide |
|---|---|---|
| 0. Intake | a handful of questions (subject, formats, voice, the look, hero, your music, your product) and the style gallery | answers, a style, or your references |
| 1. Story check | the format it picked and a numbered beat table, facts web-checked | approve / change beats |
| 2. Look check | 2–4 full-size style frames (for a new look: side-by-side comparisons with your references) | thumbs up per frame |
| 3. Storyboard | every beat as a key frame, with sound and the transition into the next | thumbs up/down by panel number |
| 4. Build | — (animate the approved panels, render, review) | — |
| 5. Delivery | the video plus measured checks: cuts on the beat grid, story arc loudness, hero anchoring, the loudest moment after the silence, narration pace | notes → a revision run |

## Styles

A style is a plug-in: the story grammar, timing, sound, renderer and tools stay the same; the style supplies the drawing kit. A piece picks one in its `piece.json` (`"style": "riso"`).

| style | the look |
|---|---|
| cut paper | torn paper, drop shadows, crayon, patterns, characters with faces |
| crosshatch | sketchy ink that boils on 2s, hatch and pencil shading, warm paper and navy "inside the machine" worlds |
| riso | a three-ink risograph print: halftone screens at their own angles, overprints, misregistration |
| sketchbook | graphite and one accent colour on a sketchbook page, hand lettering |
| math | a manim-style math explainer: black stage, axes and graphs, colour-coded variables, smooth easing |
| pixel | low-resolution eras: drawn at the true resolution, upscaled nearest-neighbour, a bitmap font |
| isometric | precise isometric line art: constant hairlines, white faces hiding what's behind, rounded slabs, one dark accent; light or dark ground |

**Your own look:** give the skill references (a video, stills, a web page) and it follows a procedure — measure the palette, line weight, texture, motion and cut rhythm; draw 1–2 matched frames next to your references (`tools/compare.mjs`); ask for your thumbs up; save it as `styles/ /` in your project so every later piece can use it. Reference media stays on your machine.

Each style folder has a `STYLE.md` (its rules, palette, motion habits and a frame checklist), a `kit.js`, a `sample.png` and a small `demo/` piece.

## What's baked in

- **A story grammar** (`grammar/`) — 8 short-form formats (a history is a chronology joined by shape morphs; a mission cuts on the beat; …), the rules every piece follows (one constant, colour means one thing, silence before the payoff and loudest on it, the end is the start changed), and a checklist for what any single frame needs.
- **A kit** (`kit/`) — seeded randomness and a line that boils on 2s; ca

## 10. [arxiv] LOCAA: An Agentic System for Automated Lossy Compressor Tuning
key: arxiv:2610.10487
url: https://arxiv.org/abs/2610.10487
meta: {"published": "2026-10-07", "authors": ["Khondoker Mirazul Mumenin", "Dong Dai", "Sheng Di", "Franck Cappello"], "categories": ["cs.DC"]}
query: all:"language model" AND all:agent AND all:tool

Large-scale scientific simulations generate substantial data volumes, making lossy compression essential for reducing storage and data movement costs. However, users configure compressors through numerical error bounds (EBs) while often evaluating results using quality metrics and end-to-end performance. Because the relationship between an EB and these outcomes varies across datasets and compressors, identifying a suitable configuration typically requires exhaustive search, which can be time-consuming and computationally demanding. We present LOCAA, an Large language model-based scientific lossy compression auto-tuning agent that performs compression-in-the-loop search using tool-integrated execution, compressor-aware guidance, and persistent memory. LOCAA supports user-defined objectives and constraints without requiring a specialized search strategy. We evaluate LOCAA across three scientific applications, five compressors, and three use cases: fixed-ratio compression, compression tuning under multiple quality constraints, and compression tuning under quality and time constraints. For fixed-ratio search across twelve fields from two applications, LOCAA requires 1.98x fewer evaluation trials than binary search and 5.03x fewer than FRaZ on average. For compression ratio maximization under joint Peak Signal-to-Noise Ratio (PSNR) and Structural Similarity Index Measure constraints across six fields from the Community Earth System Model application, LOCAA reduces the average evaluation trials from 61.5 using binary search to 17, corresponding to a 72.4% reduction. Persistent memory further reduces the average number of trials by 27.9% across multiple timesteps of the same field. These results demonstrate the potential of tool-augmented LLM agents to provide flexible and efficient compressor tuning across diverse scientific data and user-defined objectives.

## 11. [youtube] Pump Fun Sniper Bot (Solana) — Memecoin Trading | Full Tutorial 2026
key: yt:E0QoMIjVI44
url: https://www.youtube.com/watch?v=E0QoMIjVI44
meta: {"channel": "Jack Sterling", "rank": 3, "duration_min": 7}
query: pump.fun sniper bot how it works

# Pump Fun Sniper Bot (Solana) — Memecoin Trading | Full Tutorial 2026
# Jack Sterling
# https://www.youtube.com/watch?v=E0QoMIjVI44

[00:00] 10 s o l. 10. I put in 10 sol, went to grab a coffee, and a bit later I had 19 sol in my wallet. The bot did everything on its own. Let me show you how. Next sniper, a Solana sniper that executes trades in 184 milliseconds. For context, you blink in about 300. This bot is faster than your blink. Bull X, half a second. Photon, 400 milliseconds. Next, under 200. Whoever gets in first makes the money. The real question is, is it
[00:34] actually true? We'll test that with a live deposit. What's under the hood? Token scanner detects new listings in real time. Snipe on launch, enters right when liquidity is added. Copy trading, mirrors top wallets. One example showed plus 1,240% in a month. Limit orders, DCA, trailing take profit. A full P&L dashboard across all wallets. Now the important part. The question [music] you're already asking yourself, will they steal my wallet? No. The platform is non-custodial. Your keys
[01:09] never leave your device. AES 256 encryption, zero-knowledge architecture, servers don't see your credentials. Contracts go through quarterly audits. MEV shield via Jito bundles, and AI rug pull detection. 15,000 scams prevented. What if their server goes down mid-trade? Your funds are in your wallet, not with the bot. If their servers go down, trades are canceled. Uptime, 99.99% with 12 global nodes and auto failover. Pricing, basic, free, 1% fee. Pro, $50
[01:46] per month, 0.5% turbo nodes, MEV protection, 3-day trial. Elite, $200, 0.1% dedicated nodes from 45 milliseconds, unlimited wallets, API. You can start with zero, and that matters. I opened the terminal, and now this is serious. Solana terminal v3.1.7. Feels like a Bloomberg terminal for degens. At the top, four cards. Total profit, win rate, active bots, average execution. In the center, live network
[02:20] pulse. A table of new tokens with liquidity and risk score. You can snipe in one click. At the bottom, system engine logs. A live console streaming everything in real time. On the right, sliders for buy amount, slippage, toggles for anti-rug, MEV protection, Jito bundling, and the bot deploy button. Bot controls. This is where I got hooked. Three presets, safe, balanced, degen. But you can customize everything. Snipe amount, slippage, take profit, stop loss, gas multiplier up to
[02:53] three times, Jito priority fee, up to 10 positions at once. Filters. Honey pot detection. The bot simulates a sell before buying. Rug guard, blocks tokens with mint authority. LP lock check. Anti-MEV. Sell tax filter. Whale tracking. AI features. AI scanner for pump probability. Smart entry by blocks. Trailing TP. Auto reinvest. Social AI analyzes hype on Twitter and Telegram. DCA up to five rounds. Snipe speed, from 2 seconds after token creation up to 15
[03:28] seconds in safer mode. Auto sell, from 5-minute scalps to 2-hour holds. Profitability. Full analytics. P&L. Best/worst snipe. ROI. Equity curve. Breakdown of wins, honey pots, and rugs. All right, enough talking. You came to see it in action. Let's trade. [music] Connecting wallet. I'll use Phantom. Let's go. The bot is running. The button turned red, it's pulsing. Everything is green. Mempool scanner is active,
[04:01] waiting for the first token. There it is. First token in the table. You see? Ticker, contract address, liquidity in sol, and risk score. Bot. Green badge not
[transcript continues in field-notes/staging/E0QoMIjVI44.txt]

## 12. [awesome] larcane97/clausona (new in awesome-claude-code)
key: gh:larcane97/clausona
url: https://github.com/larcane97/clausona
meta: {"list": "awesome-claude-code", "stars": 49, "created": "2026-03-06", "language": "TypeScript", "description": "Switch between multiple Claude Code and OpenAI Codex CLI accounts with one command. Skills, hooks, plugins and settings stay shared, and conversation history can be too; plan quota for every account at a glance."}
query: awesome-claude-code
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# clausona

**Switch between multiple Claude Code and OpenAI Codex CLI accounts on one machine. They sign in separately and share one setup.**

 
     
 

 
     
     
   
     
 

 
   
 

clausona is a profile manager for the Claude Code and OpenAI Codex CLIs. Every account gets a
config directory for its sign-in. Skills, hooks, plugins and settings are shared across them, so
`csn use work` is all it takes to move to another account.

Conversation history stays with the account unless you choose to share it. Once it's shared, a
conversation started under one account can be resumed under another.

clausona also shows how much of your accounts' 5-hour and weekly plan limits is left, side by side.

Step-by-step guides, including how to do it by hand:
[multiple Claude Code accounts](https://larcane97.github.io/clausona/guides/multiple-claude-code-accounts/),
[multiple Codex CLI accounts](https://larcane97.github.io/clausona/guides/multiple-codex-cli-accounts/),
and [the same in Korean](https://larcane97.github.io/clausona/ko/).

## Why

I've been using Claude Code with a personal and a work account, and I got tired of setting up
plugins and permissions for both. So I made a simple tool for it.

If you have Claude Code or OpenAI Codex CLI accounts for personal use, work or different orgs,
switching between them on one machine is tedious:

- **Switching is manual.** You log out and back in, or juggle `CLAUDE_CONFIG_DIR` (Claude) or `CODEX_HOME` (Codex) yourself.
- **Settings don't carry over.** A second account gets a separate config directory. Your plugins, permissions, settings and skills have to be set up from scratch, every time.

clausona fixes both. One command switches profiles, and your setup comes along.

```bash
csn use work             # switch to the work account
csn use codex:personal   # switch to your personal Codex account too
```

You don't sign in again, and you don't reinstall plugins.

> `csn` is a shorthand alias for `clausona`, registered automatically on install.

## Features

- **One-command switching** — `clausona use  ` and you're on a different account
- **Shared environment** — plugins (and the MCP servers they bring), skills, and settings.json with its hooks and permissions (Claude), and config.toml (MCP servers included), skills, and hooks (Codex) are symlinked across profiles within each tool. Set up once, use everywhere. MCP servers added with `claude mcp add` stay per account — [see the FAQ](#do-my-mcp-servers-plugins-and-settings-carry-over-when-i-switch).
- **Shared history, if you want** — `clausona config   --merge-sessions` shares conversation history with your primary directory, so `claude --resume` and `claude --continue` (and `codex resume` on macOS and Linux) find conversations from every account that shares it
- **Plan quota at a glance** — session and weekly limit usage for every account, read live from each tool's own usage endpoint (Claude and Codex)
- **Two accounts at once** — `clausona run claude:personal` starts one session under another profile without switching, so two terminals can run two accounts side by side
- **Superset fleets** — a Claude Code plugin from this repo lets one session run parallel agents in [Superset](https://superset.sh), each on its own account or API model, then check and clean up after them ([use case](docs/usecases/superset-fleet.md))
- **API profiles** — a profile can point at an API endpoint instead of a subscription login: the Anthropic API, a gateway, or a mod

## 13. [vault] Whether LinkedIn search surfaces enough recent dental and aesthetics owner posts per week to feed a manual routine
key: vault:2026-10-08:whether-linkedin-search-surfaces-enough-recent-dental-and-ae
url: https://vimeo.com/1233794507/cf61fad386
meta: {"vault_status": "open", "kind": "tool", "subject": "Flexxable video: LinkedIn Signals scraping and automation for database-reactivation outreach", "date": "2026-10-08", "where": "TRITON-CORE/Research/links/2026-10-08-flexxable-linkedin-signals-dbr.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: One week of counting by the assistant answers it

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Flexxable demo of a tool that scrapes LinkedIn commenters and keyword posters daily and pushes them into automated connection and three-message DBR sequences, then buys their mobile numbers. The timing principle transfers to M1 as a manual routine on Luke's LinkedIn: find owners who just posted about the problem, reference the post, one question, ring on reply. The tool is dead on the vault's existing ban on bulk LinkedIn automation, LinkedIn's terms, and UK data rules; the one run shown is 34 sends. The clip is the funnel for the 2,900 to 7,800 dollar blueprint. Job: Get in front of practice owners who have a database at the moment they are thinking about leads (still open) Write-up: `TRITON-CORE/Research/links/2026-10-08-flexxable-linkedin-signals-dbr.md` Link: https://vimeo.com/1233794507/cf61fad386

## 14. [hn] Show HN: TerrainSR – fast, realistic heightmap upscaling model
key: hn:49986740
url: https://huggingface.co/joe-gibbs/terrainsr
discussion: https://news.ycombinator.com/item?id=49986740
meta: {"points": 18, "comments": 3, "created": "2026-10-07T01:24:17Z"}
query: car data

This is a model that I made for a historical game. I wanted to have a 1:1 scale model of Europe, but my problem was that 100m data was too low-res while 10m LIDAR data was patchy, took hundreds of GBs to store and was full of manmade objects like mines, buildings and so on. I trained this model on undeveloped landscape so that it can quickly add plausible erosion features, rocks, etc to the low-resolution height data and sort of reconstruct what the terrain would look like before any human interference.
comment (dvt): On my phone but very interested in this (hence leaving a comment so I can find it later). What’s the variation, can we generate different maps from the same low res seed? I’m interested in this because “macro maps” can be hand built in a way that may want to preserve gameplay balance while individual games can still feel broadly unique.
comment (jauntywundrkind): can you talk to some about how you trained this? this is such a neat idea!!
