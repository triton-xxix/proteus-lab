# Harvest brief, 2026-10-19

14 items shortlisted from 318 candidates (168 dropped as already seen, 13 carry a vault verdict on the vendor).

## 1. [vault] AI UGC and ad videos sold to businesses
key: vault:2026-10-18:ai-ugc-and-ad-videos-sold-to-businesses
url: 
meta: {"vault_status": "open", "kind": "idea", "subject": "AI influencer and AI creator-subscription revenue models (2026 sweep)", "date": "2026-10-18", "where": "TRITON-CORE/Research/2026-10-18-ai-models-ofm-revenue.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: cheapest, fastest first revenue on the existing pipeline

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Real money sits in selling AI UGC and brand faces to businesses and in labelled subscription personas on AI-friendly platforms; most visible big numbers are self-reported or course sellers

## 2. [hn] Show HN: The Zelda timeline to catch up before the Ocarina of Time remake
key: hn:50140769
url: https://legendofhyrule.com/
discussion: https://news.ycombinator.com/item?id=50140769
meta: {"points": 167, "comments": 102, "created": "2026-10-18T13:06:54Z"}
query: claude code

I made this ahead of the Ocarina of Time remake which comes out in 17 days. I remember the feeling of playing it as a kid but I hadn’t kept up with the story so I built a timeline to catch up before the Door of Time reopens. Nintendo’s own timeline is the authority here (Hyrule Historia and their chronicle page). The fun part was rethinking how to visualize it. It branches at the end of Ocarina into three eras depending on whether Link wins or loses, so each era is its own thread on the cloth. The threads meet again much later with Breath of the Wild. I had a lot of help from Claude. I’d often thought about building things like this but never found the time between the day job and the rest of life.
comment (sharkbot): Don't forget to include: - Link: The Faces of Evil - Zelda: The Wand of Gamelon - Link's Crossbow Training - the various Hyrule Warriors games Good luck! :)
comment (cr125rider): This is really fun! Great design!
comment (hyperhello): What’s the word for trying to do cluster analysis on what is actually randomly distributed data? The games do have obvious similarities and sometimes refer to each other, but they’re independent events.

## 3. [github] Gathin23/tv-vibehack: Your TV, minus the ads. Debloat any Android TV over ADB and give it a clean, tvOS-inspired launcher. Built in an afternoon with Claude Code.
key: gh:gathin23/tv-vibehack
url: https://github.com/Gathin23/tv-vibehack
meta: {"stars": 2160, "created": "2026-10-17", "pushed": "2026-10-18", "language": "Java", "topics": ["adb", "android-tv", "claude-code", "debloat", "launcher", "xiaomi"]}
query: claude-code created:>{since} stars:>20

# tv-vibehack

**Your TV, minus the ads.**

Strip the bloatware from any Android TV or Google TV over Wi-Fi, and replace the ad-filled home
screen with a clean launcher that looks like an Apple TV. No root, no cable, nothing uninstalled,
and a one-line restore if you change your mind.

It started as an afternoon fixing my parents' Mi TV, which showed them an advert before they
could reach Netflix. The whole thing was done with Claude Code talking to the real TV, and the
prompt that did it is in this repo so you can do the same with yours.

---

## Table of contents

- [How it works](#how-it-works)
- [Quick start](#quick-start)
- [What you get](#what-you-get)
- [Supported TVs](#supported-tvs)
- [Doing it by hand](#doing-it-by-hand)
- [The launcher](#the-launcher)
- [Troubleshooting](#troubleshooting)
- [Questions people ask](#questions-people-ask)
- [Contributing](#contributing)
- [Licence](#licence)

---

## How it works

Android TVs have the same debug bridge as Android phones. Once you switch on USB debugging in the
TV's developer options, the TV listens on your Wi-Fi and asks you once to allow your computer.
After that, everything is standard Android tooling:

1. **Back up** the list of installed packages and settings.
2. **Disable** the manufacturer's telemetry, ad services, content rows and preloaded junk with
   `pm disable-user`. Nothing is uninstalled, so a restore script can undo every step.
3. **Install** a small native launcher and make it the default home screen.

The bloat differs by brand, which is why the prompt asks your coding assistant to discover it
on your TV and ask you before touching anything you might use.

## Quick start

You need a computer on the same Wi-Fi as the TV and a coding assistant with shell access
(Claude Code, or anything similar).

**1. On the TV**
Settings → Device Preferences → About → press OK on **Build** seven times → go back →
Developer options → turn on **USB debugging**. Some TVs also show a Network or ADB debugging
toggle; turn it on too. Keep the TV switched on.

**2. On your computer**
Open your assistant, paste the prompt from [`PROMPT.md`](PROMPT.md), and fill in your TV model.

**3. Follow along**
Accept the "Allow USB debugging?" prompt when it appears on the TV, then answer the checklist
questions: which streaming apps you use, which four go in the dock, whether to keep the voice
assistant, Chromecast and firmware updates.

That's it. The assistant backs up, debloats, builds and installs the launcher, and checks every
step with screenshots pulled from the TV. On a 1 GB Mi TV the whole thing took one afternoon the
first time; with this repo as context, people report about fifteen minutes.

## What you get

A home screen that is yours again:

- **Pitch-black background** and a dock of your four favourite apps at the bottom, in a lighter
  rounded band, exactly where Apple TV puts it.
- **A top shelf** showing the focused app's name in large type, with an ambient glow in a colour
  taken from the app's own artwork.
- **The rest of your apps in a grid** that slides up when you press Down.
- **One floating glass highlight** that springs from tile to tile instead of each tile drawing its
  own border. The focused tile lifts slightly and shows its name.
- **Three frosted buttons**: Inputs (a dropdown of HDMI ports, AV and Live TV), Wi-Fi (showing the
  network you're on) and Settings.
- **A greeting, a large thin clock and the date**, set in
  [Outfit](https://fonts.google.com/specimen/Out

## 4. [youtube] The ONLY Claude Skills Tutorial Beginners Need in 2026
key: yt:TyB7kLZPVKo
url: https://www.youtube.com/watch?v=TyB7kLZPVKo
meta: {"channel": "100x Engineers", "rank": 1, "duration_min": 25}
query: claude code skills workflow 2026

# The ONLY Claude Skills Tutorial Beginners Need in 2026
# 100x Engineers
# https://www.youtube.com/watch?v=TyB7kLZPVKo

[00:00] Claude Skills is easily one of the best things you can learn in 2026 to level up in AI. And I'm sure you've heard a lot about it already. Maybe you even tried creating your own custom skill at some point. But I'd like to take this opportunity to cover everything you need to know about Claude Skills all the way from using it as an absolute beginner to an absolute pro. In this video, we will cover the following things. What is a Claude Skill? How to use it? Level one of using Claude Skill, which is using Claude's default skills. Level two, which is modifying a Claude Skill. Level three, which is using partner skills [music] and plugins. And level four, creating your own custom skill. And
[00:33] finally, I will give you a pro secret. This is basically [music] a tip that I haven't seen anybody give out in any Claude Skill tutorial video. And if you learn this pro secret, the way you write your custom Claude Skill is going to be five times better than most people's. And we'll cover all of this using real-life examples and demos [music] of workflows that I personally use for my work. So, hit that subscribe button and let's get [music] into it. Let's start with learning what a Claude Skill actually is. In case you already know the basics and you just want to go straight to the demos, feel free to navigate this video using the chapters.
[01:05] But in simple words, a Claude Skill is a file that contains a set of instructions and guidelines to perform a certain task. It's that simple. The coolest example I can think of is the movie Matrix, where Neo learns kung fu inside the Matrix. There is a scene where he's just downloading martial arts skills while being plugged into the Matrix. That's very similar to what skills are. For example, let's say that you make decks in a certain way. There's a format that you use, there's certain brand colors, there's certain fonts, and even a specific tonality. A Claude Skill is a file that contains all those guidelines and instructions. So, that every time
[01:38] you want to perform that task, say make a deck, instead of writing all those instructions every time you prompt, you can just invoke the skill and get exactly the output you want. And this file is a dot md file, which stands for markdown, which is a fancy way of saying that it's just a read-only text file. Now, in order to use Claude Skill, you need to make sure of this one thing on your Claude account. Go to customize and click on capabilities. And if you scroll down, you'll see this thing that says code execution and file creation. Just make sure that both these things are toggled on. Now, most of the times this is toggled on by default in most
[02:11] accounts, but just make sure of this before trying out Claude skills. Once that is set, let's see how to use a skill. Now, there are fundamentally two ways to use a skill. The first is when you prompt normally and Claude automatically selects the relevant skill. For example, let me ask Claude to turn this research paper that I have into a deck. So, I'll upload my research file and I'll just say, "Turn this into a deck so that I can understand this easily." Now, I haven't asked Claude to activate any particular skill at all over here. But, if you see, it's already saying
[02:44] loaded pptx.skill, which basically is Claude understanding my requirement and loading a skill that
[transcript continues in field-notes/staging/TyB7kLZPVKo.txt]

## 5. [awesome] nahumlitvin/prismantis (new in awesome-claude-code)
key: gh:nahumlitvin/prismantis
url: https://github.com/nahumlitvin/prismantis
meta: {"list": "awesome-claude-code", "stars": 133, "created": "2026-10-02", "language": "TypeScript", "description": "Colorful, themeable Claude Code replies: tables, code, diagrams, charts and tool rows in 15 themes, with copy buttons. A Claude Code mod."}
query: awesome-claude-code
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

Sees 16 colors. Your terminal only had 8.  

 
     
     
     
   
 

 
    Install   ·
   Themes  ·
   Features  ·
   Configure  ·
   Changelog 
 

 Same prompt, same model: plain Claude Code, then with prismantis.  ▶ Watch the full 44-second tour  (tables, charts, diagrams, diffs, callouts, right-to-left text). 

## TL;DR

- Claude Code prints mermaid as source and tool calls as walls of text. prismantis draws them: real charts and flowcharts, typeset LaTeX math in kitty and Ghostty, colored tables and code, and quiet tool rows.
- 15 palettes plus `mono`, and copy buttons on everything.
- Two commands to install, `/plugin` to turn it off. Claude Code's own renderer comes back the moment you do.
- No network calls. It runs a program only when you click `⧉ html` (the clipboard helper) or turn on LaTeX (RaTeX's renderer).

```
/plugin marketplace add NahumLitvin/prismantis
```

```
/plugin install prismantis@prismantis
```

Then run `/prismantis setup` to pick a theme and styles from drawn samples, and `/prismantis demo` for a tour of the main features. In a terminal, setup opens a pane: the arrows or Tab move through the styles of a step with a preview of the one in focus, Enter saves it and shows the next step. Where the session has no terminal, as in the desktop app, it walks the same steps in the transcript.

## Install

Requires Claude Code **2.1.287** or later. Run the two commands above.

To update, run this, then `/reload` in every open session. A session keeps the version it loaded until it reloads.

```bash
claude plugin marketplace update prismantis && claude plugin update prismantis@prismantis
```

To uninstall:

```bash
claude plugin uninstall prismantis@prismantis
```

For LaTeX math, install RaTeX's renderer and set `latex` to `true`; see [LaTeX math](#latex-math). Until then formulas draw as text.

### Codex

prismantis also runs in Codex, with themes for code, tables and diagrams and the same session note. Install, what works today, and the two Codex issues it waits on for parity: [codex/README.md](codex/README.md).

## Features

| Feature | What you get |
| --- | --- |
| [Themes](#themes) | `/prismantis theme  ` switches on the spot. 16 themes and 20 color slots you can override |
| [Tables](#tables) | colored headers, rules, column alignment, colored numbers, sized to the terminal |
| [Code](#code) | a language header and copy button, Prism highlighting in two dozen languages, shell lines colored like a prompt |
| [Diagrams and charts](#diagrams-and-charts) | flowcharts, sequence, state, class and ER diagrams, bar and line charts, one color per box, participant and bar |
| [Figures](#figures) | ` ```figure ` text pictures drawn as written in the theme's colors, for timelines, layouts and before and after; glyphs and markup checked before they are drawn |
| [LaTeX math](#latex-math) | `$$` and ` ```math ` formulas typeset as images in kitty and Ghostty by [RaTeX](https://github.com/erweixin/RaTeX), text everywhere else |
| [Layout](#layout) | back-to-back tables and diagrams sit side by side and wrap on narrow terminals |
| [Copy buttons](#copy-buttons) | `⧉ md`, `⧉ art` and `⧉ html` on tables, `[ ⧉ copy ]` on code, lists and quotes, `/prismantis copy` without a mouse |
| [Tool rows](#tool-rows) | `Ran gh pr view 12`, `Read ~/src/app.ts`, groups summed up as `Ran 3 commands, read 2 files`, with status dots; `toolOutput: quiet` hides what Claude only read and says in plain words what each call did |
| [Turn footer](#tu

## 6. [vault] talking head over lifestyle B-roll
key: vault:2026-10-18:talking-head-over-lifestyle-b-roll
url: https://www.instagram.com/p/DZt8BdfMNFM/
meta: {"vault_status": "open", "kind": "idea", "subject": "jayhiette: four skills for fitness coaches", "date": "2026-10-18", "where": "TRITON-CORE/Research/links/2026-10-18-jayhiette-fitness-coach-four-skills.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: one script, generated head plus B-roll, built for an AI coach

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Sound coach-of-coaches advice in a cheap talking-head-over-lifestyle format that an AI fitness character can copy exactly Write-up: `TRITON-CORE/Research/links/2026-10-18-jayhiette-fitness-coach-four-skills.md` Link: https://www.instagram.com/p/DZt8BdfMNFM/

## 7. [hn] Show HN: 500 clocks in one 6.3 MB HTML file by Opus 5.5
key: hn:50137820
url: https://tkgally.github.io/500-clocks/
discussion: https://news.ycombinator.com/item?id=50137820
meta: {"points": 65, "comments": 27, "created": "2026-10-18T04:04:58Z"}
query: claude code

Lately I've been testing frontier models by having them create self-contained web pages that display clocks--sort of my personal version of Simon Willison’s pelican-on-a-bicycle metric. I have been particularly impressed by the variety, interest, and quality of the clocks created by Claude Opus 5.5. Over the course of several sessions in the Claude chat interface, I had it build a total of 500 clocks. Claude’s summary of the prompting process and page design is here: https://github.com/tkgally/500-clocks/tree/main
comment (vunderba): Nice job. The Pong one was a nice touch where the ball traveled within a second from each paddle. I also enjoyed the interactive fiction game clock. It doesn’t really have much to do with time, but I still appreciated how the little descriptions changed over time. Looking through all of these, you can definitely start to see patterns in themes. For example, it’s a clock but in a different language. Or it’s a clock but wrapped around a classic game - I think I saw Nine Men's Morris, Mancala and Scrabble among others. I made the Chamber of Clocks [1] about half a year back which is a set of 12 d
comment (ksimukka): Amazing. Thanks for sharing.
comment (kromokromo): Once again, impressed by Opus 5.5 for a job well done. How much did this cost you?

## 8. [github] LiCinCan/blender-ai-mcp-addon: AI assistant and MCP server for Blender: visual chat, scene tools, multi-agent workflows. Works with OpenAI, ChatGPT, Claude, Gemini, Ollama, OpenCode. Blender AI addon and plugin, copilot for 3D, bpy Python scripting, MCP integration.
key: gh:licincan/blender-ai-mcp-addon
url: https://github.com/LiCinCan/blender-ai-mcp-addon
meta: {"stars": 787, "created": "2026-10-15", "pushed": "2026-10-18", "language": "Python", "topics": ["ai-assistant", "blender", "blender-addon", "blender-ai", "blender-automation", "blender-extension", "blender-mcp", "blender-plugin"]}
query: mcp server created:>{since} stars:>30
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# mcp-for-blender-pro

### Your Blender scene. Your AI models. One creative workspace.

**An AI assistant for Blender that can inspect your scene, build objects, edit materials, find assets and carry out multi-step workflows—with a visual chat workspace and a built-in Model Context Protocol (MCP) server.**

[Download](../../releases/latest) · [Getting started](docs/QUICKSTART.md) · [Connections and agents](docs/CONNECTIONS.md)

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
3. Select the ZIP, enable **mcp-for-blender-pro**, then open **3D Viewport → N → MCP Pro**.
4. Choose a provider, add your connecti

## 9. [youtube] Top 5 Claude Code Skills Everyone Needs in 2026
key: yt:gF30riZwUAc
url: https://www.youtube.com/watch?v=gF30riZwUAc
meta: {"channel": "Yury AI", "rank": 4}
query: claude code skills workflow 2026


[body unavailable: TranscriptsDisabled]

## 10. [awesome] a1-x-tech/mcp-google-contacts (new in awesome-mcp-servers)
key: gh:a1-x-tech/mcp-google-contacts
url: https://github.com/a1-x-tech/mcp-google-contacts
meta: {"list": "awesome-mcp-servers", "stars": 0, "created": "2026-08-30", "language": "TypeScript", "description": "MCP server for Google Contacts (People API) — search, read, create, update and delete contacts, manage contact groups and run batch operations. For Claude, Cursor, Codex and other AI clients."}
query: awesome-mcp-servers

#   Google Contacts MCP

**English** | [Русский](./README.ru.md)

[](https://www.npmjs.com/package/mcp-google-contacts)
[](https://glama.ai/mcp/servers/A1-x-Tech/mcp-google-contacts)
[](https://github.com/A1-x-Tech/mcp-google-contacts/actions/workflows/ci.yml)
[](./LICENSE)

**A1 Google Contacts MCP** lets an AI app manage your Google address book in plain language. Find a contact, create or update one, organize contacts with labels, run batch imports and clean-ups, and turn auto-saved "Other contacts" into real ones.

It uses the Google People API — the API behind Google Contacts — with your Google account. It guards every update against concurrent edits, keeps reads compact with explicit field masks and makes the limits of the People API explicit instead of implying that every contacts task is possible.

- **25 tools.** List, search and read contacts, create, update and delete them one at a time or in batches, manage contact groups and membership, and reach "Other contacts".
- **Connects from the conversation.** Say "connect Google Contacts": the server walks you through the OAuth client, catches Google's redirect on `127.0.0.1` with PKCE and keeps the tokens itself — no config files, no restart.
- **Updates don't clobber.** Every update is etag-guarded: if a contact changed elsewhere since it was read, the write fails instead of silently overwriting the concurrent edit.
- **Deletes are real.** The People API has no trash; deleting a contact or group is permanent, and the server marks those tools destructive so your AI app can ask first.
- **Minimal Google scopes.** It uses `contacts` for read/write — `contacts.readonly` is enough for a read-only setup — plus `contacts.other.readonly` only for "Other contacts", without broad account access.

Start with a read-only question:

> Find everyone from Acme in my contacts and show their emails and phone numbers.

[Connect the server](#quick-start) · [Explore use cases](#what-you-can-ask-it-to-do) · [Open technical documentation](#technical-documentation)

---

## See it work in a minute

> **You:** Show my contact card for Jane Doe — email, phone and company.
>
> **Assistant:** Finds the contact and shows the requested fields. Nothing changes.
>
> **You:** Change her phone number to +1 415 555 0100 and add her to the "Clients" label.
>
> **Assistant:** Shows the contact and the proposed change, then asks for confirmation before writing.
>
> **You:** Confirm.
>
> **Assistant:** Applies the etag-guarded update and the label. If the contact changed elsewhere in the meantime, the write fails instead of overwriting it.

## Contents

- [Quick start](#quick-start)
- [What you can ask it to do](#what-you-can-ask-it-to-do)
- [How a contact changes](#how-a-contact-changes)
- [What can change](#what-can-change)
- [Getting access](#getting-access)
- [Configuration](#configuration)
- [Data, limits and background work](#data-limits-and-background-work)
- [Technical documentation](#technical-documentation)
- [Support](#support)

## Quick start

You need Node.js 20+ and a Google account. Credentials are not required at install time — the server connects from the conversation.

1. Add the server to your AI app.
2. Say "connect Google Contacts": the assistant walks you through [creating the OAuth client and approving access](#getting-access) without editing config files.
3. Ask the read-only question above.

 
  Codex  

 

**In the app:** open **Settings → MCP servers**, select **Add server**, choose **STDIO

## 11. [vault] one-credit multi-model connector for desktop seats
key: vault:2026-10-18:one-credit-multi-model-connector-for-desktop-seats
url: https://www.instagram.com/reel/DcEsI98lT-x/
meta: {"vault_status": "open", "kind": "tool", "subject": "laddy.unemployed: OpenArt MCP AI content farm", "date": "2026-10-18", "where": "TRITON-CORE/Research/links/2026-10-18-laddy-unemployed-openart-mcp-content-farm.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: try the 40-credit trial if a non-terminal seat needs generation

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) OpenArt MCP is a real one-connector, credit-priced image and video pool for Claude; the faceless AI-persona farm it sells is the bait, and the Mac already generates by API Write-up: `TRITON-CORE/Research/links/2026-10-18-laddy-unemployed-openart-mcp-content-farm.md` Link: https://www.instagram.com/reel/DcEsI98lT-x/

## 12. [hn] Show HN: WhatsApp MCP running free on Cloudflare
key: hn:50145715
url: https://github.com/finereli/whatsapp-mcp
discussion: https://news.ycombinator.com/item?id=50145715
meta: {"points": 48, "comments": 35, "created": "2026-10-18T21:36:10Z"}
query: mcp server

I wanted my humble Claude on mobile to access my WhatsApp messages but the only options I could find either required WhatsApp Business or an actual server to run Baileys on. I wanted to run it for free on ClaudeFlare and with my personal WhatsApp account, so I built this. Important feature - it connects to your Google account as well as WhatsApp to grab the names of all your WhatsApp contacts, otherwise you get only phone numbers for many of them and search doesn't work properly. This is a single user install because it's both gray area and very private - so point your agent at the repo and let it set things up.
comment (D2OQZG8l5BI1S06): Cloudflare already sniffs most of the internet traffic, why not also let them see our private messages?!
comment (SchemaLoad): What bothers me about these projects is you are exposing the other side of your conversations to being uploaded to a 3rd party AI company who will ingest it in to their training data. You personally might not care about this privacy intrusion but the people you are messaging never consented to this.
comment (jrecyclebin): I've been using Baileys - but it's not ideal. (Periodically you have to go manually log the bot back in.) Is there no platform that's friendly to personal bots? Or is that what Telegram is for? Discord I suppose...

## 13. [github] cranebeaker/coop-anything: Co-op Anything: point your AI agent at any single-player game and play it with friends (online and/or splitscreen!). MCP server and playbook to let you reverse engineer, fix, test, ship and share what it learns.
key: gh:cranebeaker/coop-anything
url: https://github.com/cranebeaker/coop-anything
meta: {"stars": 425, "created": "2026-10-16", "pushed": "2026-10-18", "language": "C", "topics": []}
query: mcp server created:>{since} stars:>30

Co-op Anything 

  Any single-player game. Your friends. Your agent does the work.  

 
   
   
 

 
 Quick start  ·
 How it works  ·
 What you can co-op  ·
 Games so far  ·
 Contribute  ·
 FAQ  ·
 Docs 
 

Want to play a single-player game with your friends? Point your AI coding agent at this
repo. It researches what exists, reverse engineers the game and its engine if it has to,
builds or fixes the co-op, **tests it with bots inside the game**, and packages it so your
friends install it in one click and join over Steam without port forwarding.

The sky is the limit. Every game that runs on your PC is a candidate.

Games being made co-op right now: **[Deus Ex](https://github.com/cranebeaker/deus-ex-coop)** (released) ·
**[Fallout: New Vegas](https://github.com/cranebeaker/fnv-coop)** · **[Zelda: Ocarina of Time](https://github.com/cranebeaker/ocarina-coop)** (fully synced) ·
**[Dungeon Keeper](https://github.com/cranebeaker/dungeon-keeper-coop)** · **[S.T.A.L.K.E.R. Shadow of Chernobyl](https://github.com/cranebeaker/stalker-soc-coop-fixes)** · **S.T.A.L.K.E.R. Clear Sky**

From the community: **[Mega Man X](https://github.com/mstan/MegaManXSNESRecomp)** and
**[Mega Man X4](https://github.com/mstan/MegaManX4Recomp)** (native PC with co-op netplay) ·
**[Pilotwings 64](https://github.com/NoahVl/Birdman64)** (split-screen) ·
**Zelda: Oracle of Seasons** ([in progress](https://github.com/cranebeaker/coop-anything/issues/1)) · yours next?
Community tools: **[DecompPipeline](https://github.com/GeneralAtrox/DecompPipeline)** (agent-driven decompilation of console games, Dreamcast first).

## Quick start

Tell your agent (Claude Code, Codex, Gemini CLI, Cursor, OpenCode, ...):

```
Read https://github.com/cranebeaker/coop-anything and follow AGENTS.md.
I want to play   in co-op with my friends.
```

The agent follows [AGENTS.md](AGENTS.md) and the skills in [`.agents/skills`](.agents/skills)
(also in `.claude/skills` for Claude Code).

### Add the MCP server

The **Co-op Anything MCP** lets any agent search the co-op directory, detect a game's engine
from its install folder, read the playbook and skills, and validate contributions.
Claude Code picks it up from this repo's `.mcp.json`; for other agents:

```
claude mcp add coop-anything -- python  /tools/mcp/coop_mcp.py
```

Codex, Gemini CLI and Cursor setup: [playbook/mcp.md](playbook/mcp.md). For the binary work,
pair it with a reverse-engineering MCP such as [REA](https://github.com/morluto/rea)
(`npx rea-agents setup`): Co-op Anything knows what to do, REA looks inside the game.

## How it works

Your agent takes one of two paths.

| | Path 1: finish what exists | Path 2: build it from zero |
|---|---|---|
| When | A co-op mod exists but is buggy, stalled or abandoned. Most loved games are here. | Nothing usable exists. |
| How | Find the last build, mine its bug reports (issues, forums, Discord), audit the code, fix it as a separate package, test, ship. | Reverse engineer the game and engine, hook in, show the second player, sync enemies, world and story, handle level changes and saves, test, ship. |
| Skills | `coop-research`, `coop-revive`, `coop-qa` | `coop-reverse-engineer`, `coop-build-from-zero`, `coop-networking`, `coop-qa` |
| Guide | [Reviving abandoned mods](playbook/reviving-abandoned-mods.md) | [How co-op mods work](playbook/how-coop-mods-work.md) |

Both paths end the same way: automated tests with real game clients
([QA](playbook/automated-qa.md)), easy install, Steam relay 

## 14. [hn] Torvalds use Claude for bottleneck fix, but race discovered
key: hn:50142323
url: https://thenewstack.io/torvalds-claude-code-kernel/
discussion: https://news.ycombinator.com/item?id=50142323
meta: {"points": 15, "comments": 1, "created": "2026-10-18T16:08:48Z"}
query: claude code

page: Linus Torvalds let Claude Code fix the Linux page cache. Then reviewers found a race. - The New Stack TNS OK SUBSCRIBE Join our community of software engineering leaders and aspirational developers. Always stay in-the-know by getting the most important news and exclusive content delivered fresh to your inbox to learn more about at-scale software development. EMAIL ADDRESS REQUIRED SUBSCRIBE RESUBSCRIPTION REQUIRED It seems that you've previously unsubscribed from our newsletter in the past. Click the button below to open the re-subscribe form in a new tab. When you're done, simply close that tab and continue with this form to complete your subscription. RE-SUBSCRIBE The New Stack does not sell your information or share it with unaffiliated third parties. By continuing, you agree to our Terms of Use and Privacy Policy . Welcome and thank you for joining The New Stack community! Please answer a few simple questions to help us deliver the news and resources you are interested in. FIRST NAME REQUIRED LAST NAME REQUIRED COMPANY NAME REQUIRED COUNTRY REQUIRED Select ... United States Canada India United Kingdom Germany France --- Afghanistan Albania Algeria American Samoa Andorra Angola Anguilla Antarctica Antigua and Barbuda Argentina Armenia Aruba Asia/Pacific Region Australia Austria Azerbaijan Bahamas Bahrain Bangladesh Barbados Belarus Belgium Belize Benin Bermuda Bhutan Bolivia Bonaire, Sint Eustatius and Saba Bosnia and Herzegovina Botswana Bouvet Island Brazil British Indian Ocean Territory Brunei Darussalam Bulgaria Burkina Faso Burundi Cambodia Cameroon Canada Cape Verde Cayman Islands Central African Republic Chad Chile China Christmas Island Cocos (Keeling) Islands Colombia Comoros Congo Congo, The Democratic Republic of the Cook Islands Costa Rica Croatia Cuba Curaçao Cyprus Czech Republic Côte d'Ivoire Denmark Djibouti Dominica Dominican Republic Ecuador Egypt El Salvador Equatorial Guinea Eritrea Estonia Ethiopia Falkland Islands (Malvinas) Faroe Islands Fi
comment (ChrisArchitect): [dupe] https://news.ycombinator.com/item?id=50090842
