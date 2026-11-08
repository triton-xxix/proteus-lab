# Harvest brief, 2026-11-08

14 items shortlisted from 360 candidates (285 dropped as already seen, 8 carry a vault verdict on the vendor).

## 1. [vault] Anonymous trading account demos an unnamed app so viewers must DM to learn what it is
key: vault:2026-09-21:anonymous-trading-account-demos-an-unnamed-app-so-viewers-mu
url: https://www.instagram.com/reel/DdUmxThJ5k2/
meta: {"vault_status": "intel", "kind": "account", "subject": "@tradewithjarvisss Instagram reel", "date": "2026-09-21", "where": "TRITON-CORE/Research/links/2026-09-21-tradewithjarvisss-reel.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Matches the Instagram to DM to Telegram pattern documented by F-Secure and Bitdefender; no firm name means no regulator warning-list check is possible

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (account) Anonymous DM funnel. Two-week-old account, no name, no company, no track record, reposted clips of other traders, an unnamed trading app. Do not engage. Write-up: `TRITON-CORE/Research/links/2026-09-21-tradewithjarvisss-reel.md` Link: https://www.instagram.com/reel/DdUmxThJ5k2/

## 2. [hn] Goldman Sachs is pulling Claude Code from its bankers and traders
key: hn:50415628
url: https://www.thestateofai.com/news/goldman-sachs-claude-code-traders-bankers
discussion: https://news.ycombinator.com/item?id=50415628
meta: {"points": 525, "comments": 320, "created": "2026-11-08T18:16:07Z"}
query: claude code

comment (MallocVoidstar): Original source appears to be Bloomberg via https://www.fa-mag.com/news/goldman-restricts-traders-and-ba... , with State of AI being some kind of AI-written site run by a spam company.
comment (CharlieDigital): > A trading floor is a bad place for unreviewed code written by people who can't read it, and the information barrier problem would be reason enough on its own. Requiring that agent-written code come from people trained to review it is a sensible rule for a regulated business. Jokes on them: devs are also losing the capacity to read the code. Can't mix move fast, high volume with "read code". Agentic engineering needs to be "all in".
comment (Ericson2314): I dunno, I have a lot more sympathy for non-technical users writing slop than engineers. I think it's really great that more people get to "properly" use the computer, in that they experience a flexible programmable environment, rather than a fixed set of discreet programs "take it or leave it". If the issue is security, a much more interesting problem for the engineering team to do is design the programming environment for the bankers so they cannot hurt themselves. If the issue a performance, designing great abstractions that the bankers' agents can use is "low code done right". I hope the b

## 3. [github] shanselman/sandbox-mcp: Fresh, throwaway Windows machines for testing your apps: an MCP server and CLI that automate Windows Sandbox
key: gh:shanselman/sandbox-mcp
url: https://github.com/shanselman/sandbox-mcp
meta: {"stars": 335, "created": "2026-11-06", "pushed": "2026-11-07", "language": "JavaScript", "topics": ["ai-agents", "mcp", "mcp-server", "testing", "ui-automation", "windows", "windows-sandbox"]}
query: mcp server created:>{since} stars:>30

# sandbox-mcp

## Give your AI agent a brand-new Windows PC. Then throw it away.

Not your desktop. Not a container pretending to be Windows. **A real, disposable Windows 11 machine**:
boot it, deploy your app, drive the controls, catch the crash, keep the evidence, delete the PC.
Run it directly with `sbx`; the optional MCP adapter exposes discoverable tools and inline images for clients that want them.
Both interfaces use the same engine. The measured GUI samples take roughly **40-50 seconds** end to end.
See the [website](https://shanselman.github.io/sandbox-mcp/).

*Real app, real guest: Haptics Everywhere's self-contained WPF/WinForms desktop app in a fresh, network-off Sandbox.
UIA selects the Inspector, the guest switches light to dark, the app relaunches and exits, then the guest is destroyed.
10-second, 183 KB edited footage: light Inspector slowed for readability, repeated dark frames trimmed.
Boot/teardown title cards summarize actual logs, not filmed boot/shutdown.
No guest runtime installation or haptic-hardware claim. [Fresh dark lab screenshot](docs/haptics-teaser.png) ·
[Earlier light-theme inspector](docs/haptics-inspector.png).*

### 🤖 Let your agent set it up

Give this to your bot. It checks the PC, verifies the download and asks before admin changes or a restart.
The CLI works on its own; configure MCP only if your agent needs that interface:

```text
Set up the sandbox-mcp CLI by following:
https://raw.githubusercontent.com/shanselman/sandbox-mcp/main/docs/agent-setup.md
Install the latest verified release. The CLI must work without MCP; configure the optional MCP adapter only if my agent needs it. Ask before admin changes or a restart.
```

**[Download v1.2.0](https://github.com/shanselman/sandbox-mcp/releases/tag/v1.2.0)**: portable CLI + optional MCP server,
bundled Node.js, guest agent and setup instructions. No Node/npm installation needed.

### “Works on my machine.” Caught in 30 seconds.

The dev box had Visual C++ installed. The fresh, **network-off** customer PC did not:

```text
FAIL  NativeProof.exe on a fresh Windows Sandbox (29.8s)
  why      exited with code -1073741515; Missing dependency: VC++ redistributable.
```

Opt in to the verified runtime install, then repeat on another fresh guest:

```text
PASS  NativeProof.exe on a fresh Windows Sandbox (30.9s)
  baseline PROVISIONED (not a clean-machine pass): VC++ redistributable  x64
  process  exited with code 0
```

Those are [actual measured results](docs/compatibility.md#combined-feature-verification), not illustrative output.
The installer was Microsoft-signed **14.51.36247.0**, downloaded and verified on the host. Guest networking stayed
off. `sbx deps app.exe` diagnoses; `sbx run app.exe --provision auto` installs **only when explicitly requested**.

### What your agent gets

| A clean customer PC | A real desktop to drive | Evidence that survives |
|---|---|---|
| Fresh on every boot; no implicit app-runtime installs | Native UIA: inspect, type, click, toggle, wait | PNGs, bounded recordings, self-contained HTML, optional MP4 |
| Dependency diagnosis; explicit verified provisioning | WinUI, WPF, WinForms, Win32; MSIX/AUMID activation | Process state, exit codes, crash events, reports |
| Network **off / firewall / on** | CLI + MCP share state; verified warm incremental deploy | Installer/uninstaller diffs; detonation observations |

Same clean-machine loop, different frameworks:

| WinUI 3, packaged | WPF, self-contained | Native Win32, packaged

## 4. [arxiv] ChemE-as-Code: An Open-Source Platform for Agentic AI in Chemical Engineering
key: arxiv:2611.07947
url: https://arxiv.org/abs/2611.07947
meta: {"published": "2026-11-05", "authors": ["Artur M. Schweidtmann"], "categories": ["cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

ChemE-as-Code provides an open-source environment in which AI agents built on large language models (LLMs) can carry out chemical engineering work and engineers can check it. Its calculation tools range from catalysis through process simulation to plant layout, HAZOP and life cycle assessment, and skills tell a general-purpose agent how to use them. Engineering files are linked, machine-readable and versioned in Git; calculations run outside the LLM, each value records its origin, and automated checks report inconsistencies and out-of-date results by file and line. In an illustrative ammonia case, agents developed a written task into a preliminary basic-engineering package (simulation files, P&IDs, layout, HAZOP, datasheets, relief) for USD 224 of API cost in the design sessions. Planted faults and engineering changes show that the checks find what their rules cover and miss the rest, so they guide human review rather than replace it. No independent engineer has reviewed the design.

## 5. [youtube] Football Goals probability calculator #learnpython  #football #soccer #pythonforbeginners #python
key: yt:uXlw9dVxVxg
url: https://www.youtube.com/watch?v=uXlw9dVxVxg
meta: {"channel": "ciao.football", "rank": 2}
query: dixon coles model python


[body unavailable: TranscriptsDisabled]

## 6. [vault] Free trading community paid per lot its members trade through an offshore introducing-broker rebate
key: vault:2026-09-21:free-trading-community-paid-per-lot-its-members-trade-throug
url: https://www.instagram.com/p/DdgEcsPsrpe/
meta: {"vault_status": "intel", "kind": "service", "subject": "TCFX / Trading Central FX (@amirscentral)", "date": "2026-09-21", "where": "TRITON-CORE/Research/links/2026-09-21-tcfx-amirscentral.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Its own Trustpilot reply admits a required 1-lot trade triggers commission; broker discloses 75.2 percent of retail accounts lose; on the FCA Warning List twice

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) On the FCA Warning List under two entries since June 2025. "Free" leads to EUR 497 and EUR 1,497 products and per-lot broker rebates through an unregulated Seychelles broker. Avoid. Job: Learn to trade from people whose incentives are not tied to how much you trade (still open) Write-up: `TRITON-CORE/Research/links/2026-09-21-tcfx-amirscentral.md` Link: https://www.instagram.com/p/DdgEcsPsrpe/

## 7. [hn] Show HN: An offline desktop companion to help maintain a healthy blink rhythm
key: hn:50408350
url: https://eyesrhythm.com/
discussion: https://news.ycombinator.com/item?id=50408350
meta: {"points": 38, "comments": 22, "created": "2026-11-07T21:47:47Z"}
query: car data

Profession like software engineer, mechanical / graphics designer takes a lot of strain on your eyes, observing minute details for hours and hours on screen can significantly reduce the blink rate which you might not even notice until it gets irreversibly painful, leaving you with dry eyes. I am already a victim of it, working 20 years as a research engineer in computer vision, zooming into pixel level details to hand craft algorithms. Now the doctors says its only regular use of lubricating drops can keep your eyes safe. Now with AI and available fantastic libraries it's possible to play safe so that your body does not pay the price of your profession. EyesRhythm is build to help you keep the blink rhythm healthy by giving small audio / visual indication to maintain healthy blink rhythm not just by monitoring healthy blink rate but also keeping a watch on how rhythmic they are. EyeRhythm also has a visual log for the neck movement. It is also capable to automatically track the face using multiple webcams that you might have on your working desk to get the best view of your eyes for accurate blink detection. Most importantly it works completely local no internet required.
comment (pluc): I had an employer who did that inadvertently by taking screenshots of the entire desktop fleet every hour (or was it 30 mins?). Things would freeze for a second and then you would blink.
comment (absoluteunit1): This is a great idea and can help with dry eye. Many people who work in front of a computer have dry eye which can be literally be solved by blinking more. Great idea
comment (splittydev): Really cool idea, but I'm very careful with installing non-OSS stuff on my computer that records my webcam 24/7. If this was OSS, I'd probably use it.

## 8. [github] kubai087/kubai-icons: An agent skill that draws animated icons in one consistent style, for Claude Code, Codex and other coding agents. Comes with 2,600+ open-source icons for React, Vue and SVG, and a website to browse them.
key: gh:kubai087/kubai-icons
url: https://github.com/kubai087/kubai-icons
meta: {"stars": 280, "created": "2026-11-03", "pushed": "2026-11-08", "language": "JavaScript", "topics": ["agent-skills", "ai-agents", "animated-icons", "animation", "claude", "claude-skill", "codex", "design-system"]}
query: claude-code created:>{since} stars:>20

Kubai Icons 

 
   An agent skill that draws animated icons in one consistent style.  
  Plus 2,800+ open-source icons drawn with it, for React, Vue and the web.
 

 
   Install the skill  ·
   Browse the icons  ·
   Use them in code  ·
   Docs 
 

 
   
 

## What's included

| Part | What you get |
| --- | --- |
| **Agent skill** | The rules, engine and self-check that draw every icon in one hand. Give Claude Code, Codex or another coding agent a product, and it draws the icons that product needs. |
| **Icon library** | 2,800+ icons: nearly 900 objects, plus badged and slashed "off" versions. For React, Vue, plain JavaScript, web components and static SVG. MIT licensed. |
| **Website** | [icons.kubai.design](https://icons.kubai.design/), in English and Chinese. Search every icon by name, shape or meaning, recolor it, copy its code or a prompt for your agent, download it as SVG or PNG, and save a collection as a ZIP. |

## Install the skill

Copy this into your agent and send it:

```text
Install the Kubai Icons skill for me:
clone https://github.com/kubai087/kubai-icons into your skills folder as kubai-icons
(~/.claude/skills in Claude Code, ~/.agents/skills in Codex;
if it's already there, pull the latest version instead),
make sure SKILL.md exists in that folder, and tell me when it's ready.
```

Restart your agent, and the skill is ready. An agent without skill support can read `SKILL.md` from the cloned folder and follow it.

> [!TIP]
> The skill asks for careful geometry and several rounds of looking at its own screenshots, so use a capable model that can read images. It was developed and blind-tested with **Claude Opus 5.5**, which we recommend. Other models, such as GPT in Codex, can use the same skill. In Claude Code, run `claude --model claude-opus-5-5`.

 
  Install it yourself  

 

Clone the repository into your skills folder. In Codex, use `~/.agents/skills` instead.

```bash
git clone https://github.com/kubai087/kubai-icons.git ~/.claude/skills/kubai-icons
```

Or download `kubai-icons-v*.zip` from the [latest release](https://github.com/kubai087/kubai-icons/releases/latest) and unzip it there:

```bash
unzip kubai-icons-v*.zip -d ~/.claude/skills/
```

The agent picks the skill up the next time it starts.

Publishing to a skill marketplace that asks for a version and display names in `SKILL.md`? Upload `kubai-icons-v*-platform.zip` from the same release. It carries those fields at the top of the frontmatter.

 

## Ask for icons

Describe what you need in plain words. The skill triggers on requests about icons, so you don't need to name it.

- "Read this repository and draw dynamic icons for its main features."
- "Add a scissors icon and a map icon to this set."
- "We need an icon for Export that matches the others."
- "Give me static SVG files I can drop into Figma."

The agent then:

1. Reads the rules and writes one line per feature: an everyday object and what it does on hover ("a folder opens", "a lock springs open").
2. Draws each icon after the closest existing one, reusing the engine.
3. Runs the self-check beside existing icons, compares sizes, outlines, layers and colors, and repeats until every item on the checklist passes.

To start a set for your own product, the skill copies the engine, gallery and self-check into your project and works there.

 
   
 

  Drawn by a fresh Claude session that had nothing but  SKILL.md  and  PROMPT.md . Each blind test closes the gaps it finds in the rules.  

## Use the ico

## 9. [arxiv] tok: a textual concrete syntax of BPMN and DMN for humans and AI agents
key: arxiv:2611.07945
url: https://arxiv.org/abs/2611.07945
meta: {"published": "2026-11-05", "authors": ["Marek Deja"], "categories": ["cs.CY", "cs.AI", "cs.SE"]}
query: all:"language model" AND all:agent AND all:tool

tok is a plain-text notation for Business Process Model and Notation (BPMN) 2.0.2 process models and Decision Model and Notation (DMN) 1.5 decisions. One engine checks a tok document against both standards, compiles the document to XML with an automatic diagram, and serves language-model applications through the Model Context Protocol. The paper classifies the notation as an alternative concrete syntax of the BPMN and DMN metamodels and reports one study. A tok model takes 2.2 times fewer tokens than the smallest BPMN XML of 893 files exported by 37 tools and 7.7 times fewer than the files as exported. The checker signals 98.2% of 1,411 injected faults, against 85.8% for the XML Schema with bpmnlint. Four language models new to tok write valid tok from a one-page reference for 85.7 to 100% of 87 process descriptions from two datasets and valid BPMN XML for every description, and the strongest model writes tok with 25% and 19% fewer tokens than BPMN XML. As agents with a lean skill and one checker tool, the models write valid tok for 97.6 to 100% of the descriptions, the strongest model spends 21% and 14% fewer tokens on tok than on BPMN XML, and a skill which sends the model to read the reference through a tool costs 1.7 to 2.8 times the tokens of the lean skill. Of 47 event logs simulated from public models, 44 fit their source models, and tok imports every model discovered from the logs.

## 10. [youtube] Fixing This Pass Map 👇 #soccer #datascience #data #dataanalytics #sports #sportsanalysis #python
key: yt:QgfOCmyhpHc
url: https://www.youtube.com/watch?v=QgfOCmyhpHc
meta: {"channel": "Analytica FC", "rank": 3}
query: dixon coles model python


[body unavailable: IpBlocked]

## 11. [vault] Account boosting and grey-market sale of game accounts and in-game items
key: vault:2026-09-20:account-boosting-and-grey-market-sale-of-game-accounts-and-i
url: 
meta: {"vault_status": "intel", "kind": "idea", "subject": "GTA 6 \"four ways to earn\" carousel (_vorken_)", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-five-saved-items-gta6-pumpfun-potion-mev-calibriai.md (sections 1 to 3)", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Needs handed-over credentials, breaches terms, gets accounts banned; Take-Two is suing PlayerAuctions over it

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Premise false. The game is not out until 19 Nov 2026, consoles only, no PC version and no mod SDK, so every listed earner needs something that does not exist. The only real angle is content and search positioning in the weeks before launch. Job: Earn from a huge game launch without breaching the publisher's terms (still open)

## 12. [hn] GrapheneOS accuses YC of funding surveillance and enabling HN harassment
key: hn:50395623
url: https://twitter.com/GrapheneOS/status/2118490356958597210
discussion: https://news.ycombinator.com/item?id=50395623
meta: {"points": 22, "comments": 6, "created": "2026-11-06T17:42:49Z"}
query: bonding curve

page: GrapheneOS on X: "Y Combinator invests in dozens of surveillance companies including Flock along with helping to enable them. Their moderators put their thumb on the scales at Hacker News actively supporting attacks on the GrapheneOS project including libel and harassment towards our team members." / X Post Log in Sign up Post Log in Sign up GrapheneOS on X: "Y Combinator invests in dozens of surveillance companies including Flock along with helping to enable them. Their moderators put their thumb on the scales at Hacker News actively supporting attacks on the GrapheneOS project including libel and harassment towards our team members." Conversation GrapheneOS @GrapheneOS Y Combinator invests in dozens of surveillance companies including Flock along with helping to enable them. Their moderators put their thumb on the scales at Hacker News actively supporting attacks on the GrapheneOS project including libel and harassment towards our team members. 23:47 · 5 Nov 2026 · 57.4k Views 40 331 3.2k 352 Log in or sign up for X See what’s happening and join the conversation Continue with phone Continue with Apple Continue with Google or Log in with username or email Relevant people GrapheneOS @ GrapheneOS Follow Open source privacy and security focused mobile OS with Android app compatibility. Forum, Discord and Matrix: grapheneos.org/contact#commun… What’s happening Show more GrapheneOS @GrapheneOS Y Combinator invests in dozens of surveillance companies including Flock along with helping to enable them. Their moderators put their thumb on the scales at Hacker News actively supporting attacks on the GrapheneOS project including libel and harassment towards our team members. 23:47 · 5 Nov 2026 · 57.4k Views 40 331 3.2k 352 GrapheneOS @GrapheneOS 5 Nov Nearly every Hacker News thread about GrapheneOS has a dozen accounts posting blatant fabrications about it. There's a mix of fresh accounts and long term serial harassers who have engaged in years of personal attacks. We've tal
comment (user_7832): Related? https://news.ycombinator.com/item?id=49673372
comment (beansovertoast): Despite all the evidence showing this to be true, I refuse to believe it. I post this from my shadow banned account of course - shadow banned with no warning or explanation.
comment (smallerize): Posts also available on bsky https://bsky.app/profile/grapheneos.org/post/3mzm2j56ws22q

## 13. [github] artemchuikin/youtube-skills: YouTube transcript skills for Claude Code, Cursor and Codex. Agent Skills to get transcripts, search YouTube, read channels and playlists, and bulk export.
key: gh:artemchuikin/youtube-skills
url: https://github.com/artemchuikin/youtube-skills
meta: {"stars": 273, "created": "2026-08-22", "pushed": "2026-11-05", "language": null, "topics": ["agent-skills", "ai-agents", "captions", "claude-code", "claude-skills", "codex", "cursor", "hermes"]}
query: youtube transcript pushed:>{since} stars:>20

# YouTube Skills for AI Agents 🎬

> Drop-in skills that let a coding or chat agent pull YouTube transcripts, run searches, walk
> channels and export whole playlists.

An [Agent Skill](https://skills.sh) is a folder of instructions an agent loads when the task
matches. The 12 skills in this repo cover YouTube end to end. Each one names its endpoint, shows
the exact request, lists every parameter with defaults and limits, and maps every error code to a
recovery, so the agent makes the right call on the first try instead of guessing. No yt-dlp, no
headless browser, no Google Cloud project. One HTTPS request per answer.

Works with Claude Code, Cursor, Antigravity, Cline, Codex, OpenClaw, Hermes Agent, and anything
else that reads the Agent Skills format.

Made by [TranscriptOut](https://transcriptout.com/?utm_source=youtube-skills&utm_medium=readme) · [API docs](https://transcriptout.com/docs?utm_source=youtube-skills&utm_medium=readme) · [MCP server](https://github.com/artemchuikin/youtube-mcp)

---

## ⚡ Quick start

```bash
npx skills add artemchuikin/youtube-skills --skill youtube-full
```

Then ask the agent something it previously had to refuse.

```txt
What does this talk actually claim? https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

The first run also takes care of the API key, without leaving the chat. The agent asks for your
email, a 6-digit code arrives in your inbox, you read it back, and a fresh `sk_` key lands in your
shell or agent config. The account behind it is free, starts with 100 credits and never asks for a
card.

 
  Other install paths  

**Hermes Agent**

```bash
hermes skills install skills-sh/artemchuikin/youtube-skills/skills/youtube-full
```

**All 12 skills at once**

```bash
npx skills add artemchuikin/youtube-skills
```

**Manual (git clone)**

```bash
git clone https://github.com/artemchuikin/youtube-skills.git
cp -r youtube-skills/skills/youtube-full ~/.claude/skills/
```

**OpenClaw (ClawdBot/Moltbot).** Copy a folder from `clawhub/` into your skills directory. The
`clawhub/` tree carries the same 12 skills with bash-style examples.

**No terminal at all.** Paste this into the agent and let it do the work.

```txt
Install the youtube skills from this GitHub repo: https://github.com/artemchuikin/youtube-skills
I want to get YouTube transcripts, search YouTube, and browse channel videos from my agent.
Set everything up for me.
```

Installing skills and creating the API key are both things these skills teach the agent to do.

 

---

## 💬 What you can ask

Every row is something you can say to the agent word for word. The skill turns it into the
right API call.

| Ask for | For example |
|---------|-------------|
| **A transcript** | "What does this video actually say? [URL]" |
| **A summary or quote** | "Pull the three strongest quotes from this talk" |
| **Subtitles as files** | "Export this video's subtitles as SRT" |
| **A YouTube search** | "Find recent talks about Rust async and pick the best three" |
| **A channel's news** | "Anything new on @kurzgesagt this week?" |
| **A channel's catalogue** | "List everything @3blue1brown has ever uploaded" |
| **Search inside a channel** | "Find every Fireship video that mentions Postgres" |
| **A whole playlist** | "Turn this lecture course into study notes" |
| **A bulk export** | "Queue transcripts for all 800 videos on this channel" |
| **RAG-ready chunks** | "Fetch this playlist's transcripts in ~1000-character segments for my index" |

---

## 🧰 Which s

## 14. [youtube] Build Anything With a CUSTOM MCP Server - Python Tutorial
key: yt:-8k9lGpGQ6g
url: https://www.youtube.com/watch?v=-8k9lGpGQ6g
meta: {"channel": "Tech With Tim", "rank": 4}
query: mcp server build tutorial


[body unavailable: IpBlocked]
