# Harvest brief, 2026-10-13

14 items shortlisted from 243 candidates (117 dropped as already seen, 13 carry a vault verdict on the vendor).

## 1. [vault] A small weekly prize or showcase as the community rung of the AI for Businesses or Bootcamp kit, if either ships
key: vault:2026-10-12:a-small-weekly-prize-or-showcase-as-the-community-rung-of-th
url: https://www.skool.com/aicreatorleague
meta: {"vault_status": "open", "kind": "service", "subject": "AI Creator League (Skool, Tim Kobru, 9 dollars a month, AI realism and weekly cash prizes)", "date": "2026-10-12", "where": "TRITON-CORE/Research/links/2026-10-12-ai-creator-league-skool.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Design note for WF-0322 and WF-0352

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) A 9 dollar a month Skool community on AI realism, avatars, UGC and viral recreation with a weekly 750 dollar prize for posting, on the same lock-in template as THE BLUEPRINT under a different owner. The vault already holds a fuller version of the syllabus in the AI Video Bootcamp extraction and the framework built from it, so nothing to buy. The weekly prize mechanic is the one idea worth keeping, as a community-rung design for Luke's own kit ladder. Write-up: `TRITON-CORE/Research/links/2026-10-12-ai-creator-league-skool.md` Link: https://www.skool.com/aicreatorleague

## 2. [hn] Launch HN: Agent37 (YC F26) – Low-cost agent sandboxes for running agents
key: hn:50059096
url: https://news.ycombinator.com/item?id=50059096
discussion: https://news.ycombinator.com/item?id=50059096
meta: {"points": 77, "comments": 57, "created": "2026-10-12T16:46:34Z"}
query: claude code

Hey HN, I’m Vishnu from Agent37 ( https://agent37.com ). We build sandboxes for running AI agents at under 10% of the cost of most sandbox providers. Our customers spend an average of $0.37/month per sandbox. You can view a video walkthrough of the product here: https://youtu.be/DK5ISR2tbNo We started as one of those OpenClaw wrapper companies back in February (yup.. judge me). In time we added more and more harnesses. One of the goals I had at the time was to offer a free plan to users, so as to gain more market share. But it was too cost prohibitive to do it right away. Especially since we were bootstrapped and servers were running on my savings. Today we’re actually able to offer the free plan thanks to the optimizations we’ve made since. Over 90% of the new signups we have are just free plan users and they host their personal Hermes/Openclaw/Claude Code etc on our cloud. Our infrastructure cost for the free sandboxes averages around $0.05 to $0.10 per user per month. Here are some techniques that have worked for lowering cost: * When you look at agent harnesses, they have certain patterns in the way they consume CPU and RAM. They need CPU in bursts when they’re initializing or performing certain tasks, but beyond that, they’re often not peaking. They need more RAM for things like browser and computer-use tasks. Once the task is done, usage often comes back down. This is a key insight in lowering cost, so by efficiently managing the CPU/RAM utilization we could lower the c
comment (bitlad): I had ran into another yc startup from the same batch doing the same thing recently. I think it was called maritime. YC batch are becoming more like hunger games. I know a few companies where this is just a feature like digitalocean it is just a feature.
comment (invalidOrTaken): This is freaking great. Thank you for posting!
comment (christoff12): I have yet to use sandboxes though have some experimentation planned for a new gig I'm starting in a week. How would you compare what you do to fly.io's Sprites (which is currently atop my To Try list)?

## 3. [github] juliobsz/skills: An agent skill that builds award-caliber websites from one line
key: gh:juliobsz/skills
url: https://github.com/juliobsz/skills
meta: {"stars": 192, "created": "2026-10-12", "pushed": "2026-10-12", "language": "TypeScript", "topics": ["agent-skills", "astro", "awwwards", "claude-code", "claude-skills", "codex", "creative-coding", "frontend"]}
query: claude-code created:>{since} stars:>20

# /awwwards

**An agent skill that builds award-caliber websites from one line.**

 
     
     
     
     
     
     
 

 
     
 

[Demo](#demo) · [Install](#install) · [Usage](#usage) · [How it works](#how-it-works) · [Limits](#limits)

 

```
> make me a portfolio, my name is Julio
```

That's the whole brief. The agent works as creative director, designer and creative developer
in one, then hands back a site it has already checked in a real browser.

## Quick start

```bash
npx skills add wheresryan22/anatomy -g   # optional: interactive isometric explainer figures
npx skills add juliobsz/skills -g
```

Open a **new** agent session, then type `/awwwards` or just ask for a website.

## Demo

https://github.com/user-attachments/assets/0ac28c25-9796-4bce-8fa6-4dcc6df55b8b

## Install

Install with the [skills CLI](https://github.com/vercel-labs/skills). It runs through `npx`, so
there's nothing to install first, and it detects your agents (Claude Code, Codex, Cursor,
Gemini CLI, OpenCode, Copilot and more) and lets you pick.

```bash
npx skills add juliobsz/skills -g
```

| Command | Result |
|---|---|
| `npx skills add juliobsz/skills -g -a claude-code` | Claude Code only (use `codex`, `cursor`… for others) |
| `npx skills add juliobsz/skills` | This project only, instead of your user folder |
| `npx skills add juliobsz/skills -g --copy` | Copy the files instead of linking them |
| `npx skills update -g` | Update to the latest version |
| `npx skills remove awwwards -g` | Uninstall |

The CLI collects anonymous usage data. Set `DISABLE_TELEMETRY=1` or `DO_NOT_TRACK=1` to turn
it off.

 
 Claude Code plugin 

If you prefer Claude Code's plugin system, which updates the skill for you:

```
/plugin install awwwards --marketplace juliobsz/skills
```

On Claude Code before 2.1.275, run `/plugin marketplace add juliobsz/skills` and then
`/plugin install awwwards@juliobsz`. The skill then runs as `/awwwards:awwwards`. Use the
plugin or the skills CLI, not both, or the skill shows up twice.
 

 
 Manual install 

Copy the `awwwards/` folder into your agent's skills directory, for example
`~/.claude/skills/awwwards`. Any agent that reads `SKILL.md` skills can use it.
 

### Works with /anatomy

[/anatomy](https://github.com/wheresryan22/anatomy) by wheresryan22 is an open-source skill
for detailed, interactive isometric figures that explain an idea as a real physical object.
Install it next to `/awwwards` and the site can get one "how it works" section built as a real
explainer figure, styled to the site's palette and grid.

```bash
npx skills add wheresryan22/anatomy -g
```

It's optional. Without it, `/awwwards` builds that section another way, and tells you at the
end when a figure would have helped.

### Requirements

- **Node 22.20+** for the skills CLI. The helper scripts need Node 20+.
- **Playwright** in the site's project for screenshots and the OG image, and **axe-core** for
  the accessibility pass. The skill installs both as dev dependencies when it needs them, and
  uses a Chromium you already have when it can.
- **A model that can read images**, so the QA loop can look at its own screenshots.
- **A Vercel, Netlify or Cloudflare account** only if you want it to deploy.

 
 Troubleshooting 

- **`/awwwards` isn't found.** Start a new session; agents read their skills folder at startup.
  Then run `npx skills list -g` to see where it was installed.
- **It shows up twice.** You installed it two ways (for example the skills CLI and

## 4. [arxiv] BT-Agent: Deploying Onboard Robot Agents with Behavior Trees and Multi-Fidelity Evaluation
key: arxiv:2610.13862
url: https://arxiv.org/abs/2610.13862
meta: {"published": "2026-10-09", "authors": ["Fabio Hübel", "Adam Lilja", "Yue Yin", "Siming He"], "categories": ["cs.RO"]}
query: all:"language model" AND all:agent AND all:tool

Deploying language-model agents onboard mobile robots requires task reasoning and responsive execution within limited compute and memory. We propose BT-Agent, an onboard architecture combining LLM-driven task decisions with predefined behavior-tree (BT) skills. These skills enforce execution conditions and return structured failure feedback. We demonstrate fully onboard operation with a 9B model on a quadruped across five task categories. Intervention tests show that local checks stop ongoing navigation without waiting for another model decision, while the agent remains active to retry or report constraints. To compare agent designs efficiently, we introduce a 161-task multi-fidelity benchmark, evaluated in text on all tasks and in Habitat on 39. Text supports 10.9$\times$ higher evaluation throughput, while simulation reveals how perception and motion failures change task outcomes. BT-Agent's largest success gains over the strongest Act/ReAct baseline occur at 4B and 9B: approximately 10 and 5 percentage points. Ablations identify structured tool calls and informative failure feedback as the most useful components.

## 5. [youtube] How Pump.fun’s bonding curve actually works and why being early is basically the whole game. #pump
key: yt:1YZAObOuSaU
url: https://www.youtube.com/watch?v=1YZAObOuSaU
meta: {"channel": "Dayy Dream 5", "rank": 2, "duration_min": 0}
query: solana bonding curve explained
SEEN: the vault already judged this vendor (vault verdict: pump.fun). Record the mechanism only if it is new; do not re-judge the vendor.

# How Pump.fun’s bonding curve actually works and why being early is basically the whole game. #pump
# Dayy Dream 5
# https://www.youtube.com/watch?v=1YZAObOuSaU

[00:00] The bottom of pump from nobody in here. Here's the one thing about pump from that decide to that you are really happy to be with. Every time on year [music] runs on a building price goes up automatically as more people buy. Whoever buys first gets the cheapest. >> [music] >> Everyone that comes after pays more than the person before them. That's the whole model. The newest lawsuit against pump from actually claims insiders insider [music] bots getting during the first few seconds before regular people even see the coin, then sell into the people buying after. Whether that holds [music] up in court or not, the curve itself
[00:32] already tells you. Who already got [music] in before me and what happens once they sell? Follow if you want more of these actual explaining breakdowns.

## 6. [vault] Tooling, leaderboards and data products built around a token launchpad
key: vault:2026-09-20:tooling-leaderboards-and-data-products-built-around-a-token-
url: 
meta: {"vault_status": "open", "kind": "service", "subject": "pump.fun", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-five-saved-items-gta6-pumpfun-potion-mev-calibriai.md (section 4)", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: The only lane that is not extraction from traders; the launchpad acquires these firms, as with Kolscan and Padre

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) A real business (about $46m in fees over 30 days, roughly 90% of Solana launchpad activity) and a losing game for the people trading on it. Assessed as a business, not as an opportunity. Job: Let anyone launch a token and find real buyers without it being extraction from retail (still open)

## 7. [hn] Show HN: Opus 5.5 made a fully featured Figma clone in 3 hours / 8 prompts
key: hn:50060311
url: https://www.mana.space/home/rZfbotNWAXegQypmpkzaAPFC6Mp1/Apps/Figma%20Next%20Launch
discussion: https://news.ycombinator.com/item?id=50060311
meta: {"points": 39, "comments": 41, "created": "2026-10-12T18:03:56Z"}
query: car data

I think a chasm has been crossed. Opus 5.5 few shotted a fully working Figma for me. In the past year I have been trying to benchmark vibe coded apps and see how good they get and this week it did it with very very little guidance from me. I basically just told it reach feature parity. Prior to this vibe coded apps would resemble the real software, this is not a resemblance it's the real thing. As a casual Figma user in the past, I can't really see a difference. And if there is one you have an LLM that can on the fly operate the app or use it. P.S. I did this is on Mana which is our startup making it easier for LLMs to do it (probably the code is half of what would have been and there are primitives it can use but ultimately it's a testament to how good models have gotten). I went on to make google meets, docs, telegram, linear, etc. All basically with single prompts. The biggest jump has been in the UX understanding of models and attention to detail.
comment (kumama): i wonder whether these were in the training set for the models
comment (anonymous908213): Nice advertisement. Truth doesn't matter, just poop out something that visually looks like the correct thing and use it to shill your harness.
comment (drewbitt): My agent did it in one prompt: it git cloned https://github.com/open-pencil/open-pencil

## 8. [github] iamumeransari/claude-show-your-work: Claude Code shows images and plays videos right in your terminal: screenshots, Playwright recordings, and synced before/after QA. Ghostty & kitty.
key: gh:iamumeransari/claude-show-your-work
url: https://github.com/iamumeransari/claude-show-your-work
meta: {"stars": 151, "created": "2026-10-08", "pushed": "2026-10-12", "language": "TypeScript", "topics": ["ai-agents", "anthropic", "claude", "claude-code", "claude-code-mod", "claude-code-mods", "claude-code-plugin", "developer-tools"]}
query: claude-code created:>{since} stars:>20

claude-show-your-work 

 Claude Code can show you pictures and play videos in the terminal. 

 
     
     
     
     
 

claude-show-your-work is a Claude Code plugin that displays images and plays videos in the chat. Claude uses it to show what it has made, such as a web page, a design, a chart or a video, and to play recordings of your app while it tests it.

## Install

Run these two commands in Claude Code:

```
/plugin marketplace add https://github.com/iamumeransari/claude-show-your-work.git
/plugin install show-your-work@iamumeransari
```

The plugin requires macOS, Claude Code 2.1.287 or later, and the Ghostty terminal. Videos also require ffmpeg, which you can install with `brew install ffmpeg` or by asking Claude to install it.

## Usage

Claude shows visual work without being asked. You can also ask for it directly, for example:

- "Give me four directions for the homepage hero and show them side by side."
- "Build the sign-up form, test it, and show me the recording."
- "Fix the billing toggle and show me before and after."

### Design

 
   
   
 

Claude can show several design concepts side by side, and you choose one by replying. It can also show a finished page at desktop, tablet and phone widths in a single image.

### Testing

   

Claude can test a feature with Playwright, record the run, and play the recording in the chat. The changes it made are listed next to the video, and clicking a change jumps to that point. Each check is marked as passed or failed when the video reaches it.

For a bug fix, Claude records the same steps on the old and new versions. The Compare view plays both recordings side by side and keeps them in sync, even when one loads more slowly, with the check results for each version.

### Video

 
   
   
 

Videos play in the chat with a list beside them, such as the sections of an ad. When Claude makes a new version, the earlier ones stay in the history so you can compare them.

Charts, slides, motion graphics and any other image or video file work the same way.

## Errors

If a file can't be shown, a note appears in its place with the reason: the file is missing, it isn't an image, the video is damaged or has no picture, ffmpeg isn't installed, or the terminal can't display images. The note has a button that copies a prompt for Claude to fix the problem.

## How it works

Claude Code mods let a plugin draw its own interface inside Claude Code, and Ghostty can display images in the terminal. Claude tells the plugin which file to show, and the plugin passes it to the terminal.

Videos are split into frames with ffmpeg. The plugin prepares a few seconds of frames at a time, so long videos use little memory or disk space.

The image or video goes to your screen and not to Claude, so displaying it uses no tokens.

## Terminals

The plugin works in Ghostty. iTerm2, Terminal.app and the VS Code terminal can't display these images, and the plugin tells you when that happens.

In tmux, add `set -g allow-passthrough on` to `~/.tmux.conf`. If the setting is off, the plugin shows you how to turn it on.

## FAQ

### Does it update itself?

Yes. When Claude Code starts, the plugin checks GitHub for a new version once a day and installs it. Turn this off with `/show-your-work-settings updates off`.

### Does it collect any data?

It sends anonymous usage counts, such as which versions are in use and how often images and videos are shown. It never sends files, file names, paths, prompts or anything you write,

## 9. [arxiv] OpenSocialJax: Evaluating Social Adaptation in Sequential Social Dilemmas with Open-Ended Environmental Dynamics
key: arxiv:2610.13710
url: https://arxiv.org/abs/2610.13710
meta: {"published": "2026-10-09", "authors": ["Zihao Guo", "Meng Fang", "Joel Z. Leibo", "Yali Du"], "categories": ["cs.MA"]}
query: all:"language model" AND all:agent AND all:tool

Sequential social dilemma benchmarks capture diverse social interactions, but rarely test whether agents can infer hidden environmental rules through repeated interaction while adapting to other agents. We introduce \textbf{OpenSocialJax}, which extends Clean Up and Commons Harvest across an open-ended distribution of latent environment configurations, systematically varying spatial layouts and hidden rules governing tool crafting, payoffs, and resource dynamics. Each episode samples one configuration from tens of millions of possibilities and holds it fixed across five trials. We evaluate eight large language models, including three closed source models and five open source models. Our evaluation tests whether models can discover hidden rules and adapt to other agents in homogeneous and mixed teams. We find that rule discovery often improves performance but does not reliably sustain cooperation, as the cleaning burden becomes concentrated among fewer agents in OpenCleanup and every team eventually exhausts the shared resource in OpenHarvest. In our mixed arena, one cooperative agent was able to sustain the public good in OpenCleanup at a cost to its own return, but could not prevent resource depletion in OpenHarvest. Together, these results highlight the difficulty of adapting jointly to unfamiliar environmental dynamics and the changing behavior of other agents.

## 10. [youtube] Boosting SORA Token Value: The Power of Token Bonding Curve #XOR #VAL #PSWAP #economics #shorts
key: yt:PpjZ9GZsN20
url: https://www.youtube.com/watch?v=PpjZ9GZsN20
meta: {"channel": "Soranauts: SORA Blockchain & DeFi Education", "rank": 3, "duration_min": 0}
query: solana bonding curve explained

# Boosting SORA Token Value: The Power of Token Bonding Curve #XOR #VAL #PSWAP #economics #shorts
# Soranauts: SORA Blockchain & DeFi Education
# https://www.youtube.com/watch?v=PpjZ9GZsN20

[00:00] the token bonding curve is a smart contract built into the sore Network that has two functions a buyprice function and a sell price function and these are just kind of uh linear lines that increase gradually as new Zord tokens are integrated into the economy example of the reserve assets that we have today are eth D Val and ppot so you can put these into the token bonding curve and get freshly minted zor

## 11. [vault] UGC creator marketplace that sources creator applications for brands fast
key: vault:2026-09-20:ugc-creator-marketplace-that-sources-creator-applications-fo
url: https://sideshift.app/
meta: {"vault_status": "open", "kind": "service", "subject": "sideshift.app", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-jev-sideshift-invo-keza.md (section 3)", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: The marketplace model itself is untested here; this domain scores badly on reputation checkers, likely automated

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) A UGC creator marketplace, not the crypto swap service with the colliding name. Poor domain reputation scores. Nothing to try. Job: Get 50+ qualified creator applications for a brand in a day (still open) Write-up: `TRITON-CORE/Research/links/2026-09-20-jev-sideshift-invo-keza.md (section 3)` Link: https://sideshift.app/

## 12. [hn] Show HN: Atticus – Hold-to-talk voice assistant for macOS that runs on Claude -p
key: hn:50049588
url: https://github.com/SaarthurR/atticus-mac
discussion: https://news.ycombinator.com/item?id=50049588
meta: {"points": 48, "comments": 5, "created": "2026-10-12T00:15:12Z"}
query: claude code

Hi HN! I'm Saarth. I'm in 9th grade, and I built Atticus. Atticus is a fast and cheap Mac assistant that can do tasks for you. You hold down Control-Option-Space, speak or type your task, be it complex or a simple browser search, and Atticus will get on it. The interesting part is that simple tasks, like opening apps, playing a Spotify playlist, or web queries, don't touch AI, and instead are processed locally and typically finish in under a second. For example, prompting Atticus to open apps takes around 0.08 seconds, sometimes even finishing before you finish your sentence, sort of like Jev. Any tasks that are more complicated will be sent to Claude via claude -p, meaning you never need an API key and Atticus will run on your existing Claude Pro or Max plan. By using this approach, costs are also cut down immensely, with, on average, tasks costing a fraction of a cent. To achieve Atticus' speed, it remembers shortcuts from each task it completes. When it does a task right for the first time, it saves its steps and replays them the next time without AI. For example, a workflow of creating a new meeting took about 30 seconds the first time around. Atticus then logs the exact steps to memory and takes 5-8 seconds on the next pass. To add to this, Atticus also learns about you as you use it more and from what's on your computer, including your name, your apps, and things you want it to remember, personalizing its answers to you. To combat the safety concerns over giving an AI u
comment (handfuloflight): This is great, can we get OpenCode?
comment (imranshah10140): Will this work on the Windows as well or just for mac users. by the way really like it from what I can see it from the demo video. If it works as it shown and also I dont thinks so that it is for windows would love if you can clear this out.
comment (FindlayH): This slaps, I burned some credits on a fork that works for windows https://github.com/FindlayHi/atticus-windows

## 13. [github] Atoll92/agent-standup: Your Claude Code, Codex and Mistral Vibe sessions as a live, animated team call: who is working, who waits on whom, who needs you. VS Code extension, terminal command, desktop app. Runs locally, zero tokens.
key: gh:atoll92/agent-standup
url: https://github.com/Atoll92/agent-standup
meta: {"stars": 148, "created": "2026-10-10", "pushed": "2026-10-12", "language": "HTML", "topics": ["ai-agents", "claude", "claude-code", "codex", "developer-tools", "mistral", "mistral-vibe", "monitoring"]}
query: claude-code created:>{since} stars:>20

# Agent Standup

**See who is waiting on whom, and who is blocked — across all your Claude Code, Codex and Mistral Vibe sessions — at zero token cost.** Agent Standup turns the session files Claude Code, Codex and Mistral Vibe already write into a live team call (and a board of every session): it only reads local files and never calls Claude unless you turn on French translation or the jokes.

**Your Claude Code, Codex or Mistral Vibe session as a live team call.** The lead gives orders, sub-agents join the call, work at their desks, share their screen and report back — with voices, expressions and a view of the real work as it happens.

**Runs as a VS Code extension, a terminal command, or a desktop app.** Try it in 30 seconds, no install and no editor (Node 18+): `npx @double_geste/agent-standup --open`, then ⚙ → Source → Demo.

**Works with:** Claude Code · Codex · Mistral Vibe — in VS Code, Cursor, Windsurf, any terminal, or as a desktop app.

**Just installed the extension?** Click the Agent Standup icon in the Activity Bar (or run **Agent Standup: Open live call**), then press **Join**. No session yet: press **▶ Watch the demo**.

**→ Website & download: https://agent-standup.com**

🌐 [Français](https://agent-standup.com/fr/) · [繁體中文](https://agent-standup.com/zh-tw/) · [简体中文](https://agent-standup.com/zh-cn/) · [Español](https://agent-standup.com/es/) · [Deutsch](https://agent-standup.com/de/) · [Dansk](https://agent-standup.com/da/) · [Português](https://agent-standup.com/pt-br/) · [日本語](https://agent-standup.com/ja/) · [한국어](https://agent-standup.com/ko/)

_A fictional team fixing a slow login page — the built-in demo (⚙ → Source → Demo). [Watch the full 1-minute video](https://atoll92.github.io/agent-standup/media/demo.mp4)._

[%20dev%20a%20coffee-ffdd00?logo=buymeacoffee&logoColor=black)](https://www.buymeacoffee.com/bored_dev_and_his_robots)

> Unofficial community project, not affiliated with or endorsed by Anthropic, OpenAI or Mistral AI. "Claude" is a trademark of Anthropic; "Codex" is a trademark of OpenAI; "Mistral" is a trademark of Mistral AI.

## What you get

- **Token usage per agent** — a ⚡ counter in the header and on each tile shows how many tokens each agent used (input + output + cache writes; cache reads shown separately in the tooltip), counted once per message as recorded by Claude Code. Handy to see which sub-agent is the expensive one. It is read from the session files, not an estimate of your bill.
- **Stuck or quiet agents** — in the live call, a tile pulses amber with ⏳ when a command has been running for over a minute, shows 💤 when a working agent has gone quiet for 3 minutes, and a red ✗ counter for failed tool calls. The browser tab title shows how many agents are working.
- **Built-in demo** — no session yet? ⚙ → Source → **Demo** plays a fictional team (no data of yours).
- **Live call** — follows your newest Claude Code session in real time. Each agent is a small character at its desk; the one who speaks gets the spotlight and keeps it until someone else talks. Agents that talk back-to-back talk over each other, like a real meeting.
- **Real voices, lip-sync** — lines are spoken aloud; mouths follow the actual volume of the voice. For the best experience, switch to the very natural voices (see [Voices](#voices)).
- **Live screen sharing with the real output** — when an agent works, its screen fills the stage (presenter's camera in the corner, "sharing" badge): a **terminal** with the command hist

## 14. [youtube] The M5 Ultra Mac Studio is INSANE!
key: yt:YK98Cc592C8
url: https://www.youtube.com/watch?v=YK98Cc592C8
meta: {"channel": "ZONEofTECH", "rank": 4, "duration_min": 1}
query: local llm mac benchmark m5

# The M5 Ultra Mac Studio is INSANE!
# ZONEofTECH
# https://www.youtube.com/watch?v=YK98Cc592C8

[00:00] Apple just sent me the M5 Ultra Mac Studio and it's fully maxed out. It's got 36 CPU cores, 80 GPU cores, 256 GB of RAM and 4 TB of storage. So, let me run it through its paces and see what this thing can really do. So, I've downloaded Deep Seek V4 Flash which is a 156 GB local model. And you can see that it's using 208 GB of RAM out of 256 available. All right, let me give it something complex to do. Build me a Flappy Bird clone that I can
[00:33] run in the browser. And now you can see it's already started building it and it's actually going to do this fully on device. In fact, if I turn off Wi-Fi, you can see that it still works. It's still building the app. And while it's building it, you can see that it's using 241 GB of RAM out of 256. And the CPU cores, all 36 of them as you can see, are barely even touched. The GPU, however, has been more utilized. Although, it still has way more room to spare. And it's almost done building it. You can see we've already got a preview here. And there we go. It took about 10 minutes and now we've got a working Flappy Bird clone. Obviously, we could
[01:07] spend way more time on this and make it better and better, but the fact that we built this fully offline is pretty impressive. So, what would you guys use an M5 Ultra Mac Studio for?
