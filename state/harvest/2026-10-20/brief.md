# Harvest brief, 2026-10-20

14 items shortlisted from 348 candidates (187 dropped as already seen, 13 carry a vault verdict on the vendor).

## 1. [vault] Blender blockout as previz for AI video
key: vault:2026-10-18:blender-blockout-as-previz-for-ai-video
url: https://www.instagram.com/reel/DegVQaYOnqU/
meta: {"vault_status": "open", "kind": "tool", "subject": "theaisavvy: Blender plus Claude previz for Seedance", "date": "2026-10-18", "where": "TRITON-CORE/Research/links/2026-10-18-theaisavvy-blender-claude-seedance-previz.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: fix camera path and timing before paying for generations

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Real and cheap: Claude Blender connector blocks out camera and action, Seedance 2.5 takes it as motion reference; worth trying on camera-led shots, not talking heads Write-up: `TRITON-CORE/Research/links/2026-10-18-theaisavvy-blender-claude-seedance-previz.md` Link: https://www.instagram.com/reel/DegVQaYOnqU/

## 2. [hn] Maxwell: A new kind of model that sits between code and hardware
key: hn:50152466
url: https://heymaxwell.ai/
discussion: https://news.ycombinator.com/item?id=50152466
meta: {"points": 127, "comments": 60, "created": "2026-10-19T13:47:56Z"}
query: claude code

Hi HN, I'm Gal from doubleAI. We've built Maxwell, a new kind of frontier model we call a Code Execution Model. It sits between your code and the hardware. No humans in the loop! Maxwell makes the code run faster as it runs, without ever changing a single line. Maxwell sees programs from the inside: traces, profiling information, and the data flowing through them. It adapts dynamically to the environment, including the hardware, what else is running, and what the inputs look like. Code execution models change the way we approach coding. Today, Claude/Codex (and humans) keep re-optimising code for every different use-case hardware and data flow (think of LLM inference engines, like vLLM!). Our bet is that this is unnecessary, suboptimal, and that it does not scale. Instead, we think the right answer is to make code a living, thinking, thing. Early access is open at heymaxwell.ai. Happy to answer questions here.
comment (IAmRinSlow): Is it 100% deterministic?
comment (ben_mussay): The manifesto is so cool!
comment (gavinray): This was a lot more exciting than I expected. The homepage does not do a very good job of explaining what we're looking at: It appears to be a combination of two things: 1) A formalization of the Python language 2) An LLM which hooks into running programs and hot-swaps code with verifiably-equivalent behavior but better runtime performance, found via superoptimization and then verified via the formalization rules This is brilliant, and in hindsight one of those "I can't believe nobody had thought of this yet" sort of things.

## 3. [github] jdepoix/youtube-transcript-api: This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
key: gh:jdepoix/youtube-transcript-api
url: https://github.com/jdepoix/youtube-transcript-api
meta: {"stars": 8487, "created": "2018-04-20", "pushed": "2026-10-20", "language": "Python", "topics": ["asr", "captions", "cli", "python", "subtitle", "subtitles", "transcript", "transcripts"]}
query: youtube transcript pushed:>{since} stars:>20

✨ YouTube Transcript API ✨
 

 
   
     
   
   
     
   
   
     
   
   
     
   
   
     
   
   
     
   
   
     
   
 

 
  This is a python API which allows you to retrieve the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles, supports translating subtitles and it does not require a headless browser, like other selenium based solutions do!
 

 

 
  If you feel more comfortable using a hosted solution, you can use the services of any of our amazing sponsors: 
 

 
   
     
       
       
       
     
   
 

 
   
     
       
       
       
     
   
 

 
   
     
       
       
       
     
   
  &nbsp;&nbsp;
   
     
       
       
       
     
   
 

 

 
  Maintenance of this project is made possible by all the  contributors  and  sponsors . If you'd like to sponsor this project  click here . 💖
 

## Install

It is recommended to [install this module by using pip](https://pypi.org/project/youtube-transcript-api/):

```
pip install youtube-transcript-api
```

You can either integrate this module [into an existing application](#api) or just use it via a [CLI](#cli).

## API

The easiest way to get a transcript for a given video is to execute:

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
ytt_api.fetch(video_id)
```

> **Note:** By default, this will try to access the English transcript of the video. If your video has a different 
> language, or you are interested in fetching a transcript in a different language, please read the section below.

> **Note:** Pass in the video ID, NOT the video URL. For a video with the URL `https://www.youtube.com/watch?v=12345` 
> the ID is `12345`.

This will return a `FetchedTranscript` object looking somewhat like this:

```python
FetchedTranscript(
    snippets=[
        FetchedTranscriptSnippet(
            text="Hey there",
            start=0.0,
            duration=1.54,
        ),
        FetchedTranscriptSnippet(
            text="how are you",
            start=1.54,
            duration=4.16,
        ),
        # ...
    ],
    video_id="12345",
    language="English",
    language_code="en",
    is_generated=False,
)
```

This object implements most interfaces of a `List`:

```python
ytt_api = YouTubeTranscriptApi()
fetched_transcript = ytt_api.fetch(video_id)

# is iterable
for snippet in fetched_transcript:
    print(snippet.text)

# indexable
last_snippet = fetched_transcript[-1]

# provides a length
snippet_count = len(fetched_transcript)
```

If you prefer to handle the raw transcript data you can call `fetched_transcript.to_raw_data()`, which will return 
a list of dictionaries:

```python
[
    {
        'text': 'Hey there',
        'start': 0.0,
        'duration': 1.54
    },
    {
        'text': 'how are you',
        'start': 1.54
        'duration': 4.16
    },
    # ...
]
```
### Retrieve different languages

You can add the `languages` param if you want to make sure the transcripts are retrieved in your desired language 
(it defaults to english).

```python
YouTubeTranscriptApi().fetch(video_id, languages=['de', 'en'])
```

It's a list of language codes in a descending priority. In this example it will first try to fetch the german 
transcript (`'de'`) and then fetch the en

## 4. [arxiv] OpenVLHarness: Real World Visual Agentic Tool-Use with Multimodal Memory
key: arxiv:2610.26860
url: https://arxiv.org/abs/2610.26860
meta: {"published": "2026-10-19", "authors": ["Yu Zhou", "Cheng-Fu Yang", "Rui Sun", "Di Wu"], "categories": ["cs.CL", "cs.AI", "cs.CV", "cs.LG"]}
query: all:"language model" AND all:agent AND all:tool

Multimodal large language models (MLLMs) have made rapid progress on visual reasoning, yet many tasks require evidence that is difficult to obtain through internal reasoning alone: our controlled study on 22 benchmarks shows that simply increasing the inference budget of the base model yields only modest gains. Such tasks demand grounded perception, external knowledge, and numerical measurements obtained through heterogeneous tools, whose outputs must be made interpretable to the model and retained across reasoning steps. We introduce OpenVLHarness, a multimodal reasoning harness organized around a capability layer and persistent multimodal memory. The capability layer combines task-level tool interfaces with evidence rendering, providing consistent access to heterogeneous backends and converting their outputs into model-readable observations. Persistent multimodal memory retains the corresponding images, structured data, and web references as addressable artifacts throughout each query. A coding interface executes generated programs over stored data, enabling computations that combine results from multiple tools. Together, these mechanisms support an iterative process of acquiring, inspecting, and composing multimodal evidence. Evaluated on 22 benchmarks with eight open and proprietary backbones, OpenVLHarness improves average scores by 9.7-12.6 points over matched no-tool baselines, including +11.2 with Qwen3-VL-8B, +9.7 with Kimi K3, and +9.9 with GPT-6 Astra. With GPT-6 Luna at medium reasoning effort, OpenVLHarness outperforms the base model, Codex, and Visual Sketchpad at maximum effort by 7.7-8.5 points while incurring at most 37% of their model-token cost.

## 5. [youtube] Pump.fun Trading Bot | Pump.fun Sniper Bot for Solana Tokens
key: yt:6bUrd-p4fG0
url: https://www.youtube.com/watch?v=6bUrd-p4fG0
meta: {"channel": "DualSnipe Labs", "rank": 1, "duration_min": 2}
query: pump.fun sniper bot how it works
SEEN: the vault already judged this vendor (vault verdict: pump.fun). Record the mechanism only if it is new; do not re-judge the vendor.

# Pump.fun Trading Bot | Pump.fun Sniper Bot for Solana Tokens
# DualSnipe Labs
# https://www.youtube.com/watch?v=6bUrd-p4fG0

[00:00] Juice Snipe opens from its website [music] into Telegram with the desktop build ready to download. The Windows tools page leads to the current build and the desktop dashboard opens with the live console [music] and main wallet balances. Closing and reopening the wallet drawer refreshes [music] the scan data and the asset balances. In strategy, the buy amount moves to two SOL >> [music] >> and pump.fun is chosen from the root menu. Take profit and stop loss are
[00:32] tuned and AI token check starts. The AI pre-scan completes its three engines. Current candidates appear with liquidity, volume, market cap, and protection levels while an open position shows below. The LTP position opens with entry, current price, and PNL. The sniper tab loads a pasted token address.
[01:05] The platform tab brings up the token list and candlestick chart. The CRST and USDC chart opens [music] and the wallet drawer shows current balances. Back on the dashboard, Snipe now submits entries and LTP and VCTR sit in positions. The VCTR position opens with its full token information. Loading CRST and VCTR in the platform tab pulls up each
[01:39] token's [music] chart. The wallet drawer opens and closes with updated balances. Back on the dashboard, new candidates arrive [music] while recent trades updates with the latest activity. The wallet drawer shows refreshed balances across STEL, VCTR, CRST, BRDG, and Wave. AI token check is stopped. Positions update P&L for VCTR and CRST, while recent trades keeps updating. A
[02:16] VCTR trade record opens its token information. Open an explorer brings up dual snipe trade details with wallet addresses, values, and timestamps. The CRST position opens and the sell order is submitted. The CRST buy record opens in the explorer with its own trade details. The session ends on the download page.

## 6. [vault] personal model eval suite
key: vault:2026-10-17:personal-model-eval-suite
url: https://www.youtube.com/watch?v=X1ObmRAgp5A
meta: {"vault_status": "open", "kind": "idea", "subject": "Nick Saraev: How to Survive the Next 2 Years of AI", "date": "2026-10-17", "where": "TRITON-CORE/Research/links/2026-10-17-saraev-survive-next-2-years-ai.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: a folder of 10 to 15 real tasks rerun on each new model to decide what moves down the model chain

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Mostly sound general advice with loose numbers; the transferable method is a personal eval of 10 to 15 real tasks rerun on every new model Write-up: `TRITON-CORE/Research/links/2026-10-17-saraev-survive-next-2-years-ai.md` Link: https://www.youtube.com/watch?v=X1ObmRAgp5A

## 7. [hn] Show HN: Death Plan Switch, a self-hosted dead man's switch for solo devs
key: hn:50161408
url: https://deathplanswitch.com/
discussion: https://news.ycombinator.com/item?id=50161408
meta: {"points": 89, "comments": 62, "created": "2026-10-20T04:37:43Z"}
query: claude code

Hi HN, I'm Peter Bishop and I've been working in graphics and web tech for over 25yrs. I've recently launched Death Plan Switch to solve a major problem in my succession plan. What if I go missing or die? The right people are told and my business can continue to operate for my clients. There's a backstory to this project, I was hospitalised in 2012 and lost my business back then and I couldn't get the data to my technical 2IC in time without frustrating my clients. Death Plan Switch solves this problem, it's free to download and use or study under the MIT license. I've been using it for the last few weeks. It was authored with the help of Claude Code after writing an extensive MD document and it passed 42 unit tests. I hope you get some use out of it, or it inspires your own succession plans. My clients are telling me this is a strong sales feature when they trust me with their hosting and technology accounts. Happy to answer any questions. Kind regards, Peter Bishop.
comment (N_Lens): Nice, although it seems likely that I would overlook replying to the email and everyone will panic when they get notified.
comment (AndrewKemendo): I would make it monthly or quarterly not weekly By the way Google has had this for a while and I signed up for it back in 2018 or so. they check in it feels like quarterly at most https://support.google.com/accounts/answer/3036546?hl=en
comment (iugtmkbdfil834): Love it. Will test. Initial feedback: consider configurable timetable threshold ( not everyone will want the same ).

## 8. [github] simbasjungles/free-my-tv: A fast, ad-free home screen for Google TV. Open source, built with Claude Code. One button to undo.
key: gh:simbasjungles/free-my-tv
url: https://github.com/simbasjungles/free-my-tv
meta: {"stars": 1700, "created": "2026-10-19", "pushed": "2026-10-20", "language": "Java", "topics": ["android-tv", "claude-code", "google-tv", "home-screen", "launcher", "no-ads", "open-source", "tmdb"]}
query: claude-code created:>{since} stars:>20

# Free My TV

**A fast, ad-free home screen for Google TV, LG and Samsung TVs.**

Trending picks from your own apps, the weather at a glance, and a look that follows the sunset. 
Open source. Built with Claude Code. One button to undo.

[**freemytv.io**](https://freemytv.io) · [Install](#install) · [LG TVs](#lg-tvs-webos) · [Samsung TVs](#samsung-tvs-tizen) · [Any TV](#any-tv) · [Make it yours](#make-it-yours)

 

 

## What you get

- **No ads.** No sponsored rows, banners or autoplaying promos. Not one.
- **Your apps, front and center.** The streaming apps you actually use, on a glass shelf. Pick them and their order right on the TV.
- **Trending, not sponsored.** Three fresh picks every hour from what's trending this week and the latest releases, only from apps you already have. Movies and Shows get their own tabs.
- **Weather and markets, one press away.** The hour-by-hour forecast, sunrise and sunset, and live crypto prices.
- **Light by day, dark by night.** It follows your city's real sunset, the way your phone does.
- **A screensaver to match.** Full-screen photos of the picks with a big glass clock.
- **Fast.** 60 fps, every frame in 16.6 ms, on the TV's own chip. The home screen uses 96 MB of memory instead of 242 MB (−60%).  Measured on a 98″ TCL Google TV running Android 14. 
- **Set up on the TV.** Language, your city, temperature, theme, the weather and prices cards, which coins, and the apps on the shelf, in Free My TV's own settings.
- **Safe.** No root. Nothing is uninstalled. One button brings back the factory home screen.

## Install

About ten minutes. You need a Google TV or Android TV (Android 9 or newer) and a computer on the same Wi-Fi.

### The easy way: Claude Code

1. **On the TV**, turn on developer mode: Settings → System → About → press *Android TV OS build* 7 times. Then Settings → System → Developer options → turn on **USB debugging**. Write down the TV's IP address (Settings → Network & Internet).
2. **On your computer**, get the code:
   ```bash
   git clone https://github.com/simbasjungles/free-my-tv && cd free-my-tv
   ```
3. **Open [Claude Code](https://claude.com/claude-code) in that folder** and say:
   > Install Free My TV on my TV at 192.168.1.50. I live in Lisbon.

   It installs the tools it needs, builds the app and puts it on your TV. Swap in your TV's IP and your city.
4. **On the TV**, open *Free My TV* → *Home Screen* → *Free My TV*, and accept the debugging prompt (tick *Always allow*).

### The manual way

1. **On the TV**, do step 1 above.
2. **Tools:** a JDK (17+), the Android SDK command-line tools (build-tools 34, platform android-34) and adb. On a Mac:
   ```bash
   brew install --cask temurin android-commandlinetools android-platform-tools
   sdkmanager "build-tools;34.0.0" "platforms;android-34"
   ```
   On Linux, get OpenJDK 17, Android's command-line tools and adb from your package manager, then run the same `sdkmanager` line. On Windows, use WSL.
3. **Build:**
   ```bash
   ./build.sh
   ```
   The first run creates `config.properties`. Set your city and your [TMDB key](#the-tmdb-key) there, then run it again.
4. **Install:**
   ```bash
   adb connect 192.168.1.50:5555
   adb install -r FreeMyTV.apk
   ```
   On TCL TVs, also let it run in the background (TCL blocks it by default, and the switch never starts):
   ```bash
   adb shell "appops set io.freemytv AUTO_START allow || appops set io.freemytv APP_AUTO_START allow"
   ```
5. **On the TV**, open *Free My TV* → *Home Scree

## 9. [arxiv] ASTOR: Benchmarking and Improving Autoformulation for Soft-Constraint Optimization with a Formal Grammar
key: arxiv:2610.26819
url: https://arxiv.org/abs/2610.26819
meta: {"published": "2026-10-19", "authors": ["Amer Goel", "Yeganeh Alimohammadi", "Andrew Daw"], "categories": ["cs.CL"]}
query: all:"language model" AND all:agent AND all:tool

Real-world decision problems combine two qualitatively different kinds of constraints: requirements that must be satisfied, called hard constraints, and preferences that can be violated, called soft constraints. Because these problems are often posed to decision-makers in natural language, large language models offer a natural tool for assisting with their solution. This has given rise to autoformulation, which focuses on using LLMs to translate natural-language descriptions of decision problems into executable mathematical optimization models. However, this research often neglects soft constraints like those proposed by consumers, managers, and planners, despite the fact that many practical problems require modeling them explicitly. We introduce ASTOR, an inference-time framework that maps a natural-language decision problem to a grammar-guided abstract syntax tree (AST) before deterministically compiling the resulting representation into executable optimization code. We also introduce SoftOR, a unified benchmark of natural language problems which focuses on soft constraint formulations. On SoftOR, ASTOR achieves the best aggregate accuracy among comparable single-request and multi-agent LLM methods while remaining competitive on standard autoformulation benchmarks that include only hard constraints. Code and data are available at https://anonymous.4open.science/r/astor-softor-iclr-E34C/README.md.

## 10. [youtube] Can You Snipe New Pump.fun Tokens & Meme coins With a Solana Sniper Bot?! (Memecoin Sniper Bot 2026)
key: yt:fZJq921Rm-Y
url: https://www.youtube.com/watch?v=fZJq921Rm-Y
meta: {"channel": "Solana LAB", "rank": 3, "duration_min": 1}
query: pump.fun sniper bot how it works
SEEN: the vault already judged this vendor (vault verdict: pump.fun). Record the mechanism only if it is new; do not re-judge the vendor.

# Can You Snipe New Pump.fun Tokens & Meme coins With a Solana Sniper Bot?! (Memecoin Sniper Bot 2026)
# Solana LAB
# https://www.youtube.com/watch?v=fZJq921Rm-Y

[00:00] If you're still manually sniping pump fun tokens, you're probably already too late. This is Soul Sniper Bot. It's a Solana sniper [music] bot designed to help you catch new tokens automatically. If you want to check it out yourself, I'll leave the link in the description. Once you're in, this is the main dashboard where you can set up and manage your sniper bots. To actually use the bots, you'll first need to connect your Solana wallet. Just click launch app and connect your wallet. You can choose from multiple
[00:33] supported wallets and select the one you use. Once you're connected, this is where things get interesting. Here I'm setting up the bot to automatically look for new tokens and execute trades based on the strategy and settings I've selected. Once the bot is running, you can actually see the trades happening directly in the dashboard. As more trades are executed, the individual results start adding up here, giving you an overview of how the strategy is performing. You set the strategy and the bot
[01:06] >> [music] >> does the rest.

## 11. [vault] rich media as the proof in agency offers
key: vault:2026-10-17:rich-media-as-the-proof-in-agency-offers
url: https://www.youtube.com/watch?v=638GQZ9UZ4w
meta: {"vault_status": "open", "kind": "idea", "subject": "Nick Saraev: what to learn instead of AI automation in 2027", "date": "2026-10-17", "where": "TRITON-CORE/Research/links/2026-10-17-saraev-learn-instead-of-ai-automation-2027.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: lead outbound and proposals with a bespoke video, mock-up or preview of the prospect's own business

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Sound mechanism, overstated timeline: margin follows the knowledge gap, which is moving from wiring tools to judgement, rich media and team adoption; benchmark-saturation dates are course-pitch urgency Write-up: `TRITON-CORE/Research/links/2026-10-17-saraev-learn-instead-of-ai-automation-2027.md` Link: https://www.youtube.com/watch?v=638GQZ9UZ4w

## 12. [hn] Show HN: VoidAccess – open-source dark web OSINT, from query to a graph
key: hn:50167286
url: https://github.com/KatrielMoses/voidaccess
discussion: https://news.ycombinator.com/item?id=50167286
meta: {"points": 124, "comments": 13, "created": "2026-10-20T14:49:33Z"}
query: bonding curve

Hi HN! Im Katriel, and im a Security Researcher/Enthusiast and in the wave of AI, i wanted to build that next gen of security tooling that surpasses the current tools, and even the paid industries with an open source engine. I built MailAccess as well, which is going to be the best damn email osint tool out there, in another year. But just before building MailAccess i built VoidAccess, because i was delving a lot into DarkINT and the content inside the dark web is too difficult to navigate through for a human, so i automated that pipeline, made sure the noise was removed, and anything NSFW was filtered out, to give the analyst an overview of what is present in the dark web, without having to actually go through it manually. Very simple to run, you just run a few commands to install, and a couple to investigate. Then the engine takes over, and stops onyl when the job is done(or at a particular time limit, if set by the user). Do check it out, if that is something that interests you. Thanks to the community for giving it the love it has got till now.
comment (sandworm101): Um, this is an AI tool seemingly written by AI and announced by an AI announcement? Tossing in a few typos does not convince anyone anymore.
comment (girishkvs): Any interesting security reports you can share?
comment (varman11): I checked the repo. it seems pretty interesting ngl.

## 13. [github] Ansub/tv-detox: Make an old Android TV fast again with Claude Code or Codex: a tiny ad-free home screen plus the prompt to clean it up
key: gh:ansub/tv-detox
url: https://github.com/Ansub/tv-detox
meta: {"stars": 937, "created": "2026-10-18", "pushed": "2026-10-20", "language": "Java", "topics": []}
query: claude-code created:>{since} stars:>20

# TV Detox

   

### Make an old, slow Android TV fast again.

Claude Code or Codex does the work. You just press OK on the remote.

[](https://github.com/Ansub/tv-detox/releases/latest)
[](https://github.com/Ansub/tv-detox/actions)
[](LICENSE)
[](https://www.youtube.com/@ansubkhan)

**As seen on**

[](https://www.theverge.com/ai-artificial-intelligence/1013505/maybe-claude-make-your-android-tv-less-crappy-too)
[](https://www.androidauthority.com/android-tv-vibe-hacking-remove-ads-bloatware-3725338/)
[](https://mashable.com/tech/smart-tv-ads-claude-code-ai-cleanup)
[](https://t3n.de/news/claude-alter-fernseher-android-tv-1768831/)

 

 

 
 
  🧹 Removes the junk  Bloatware, ads and sponsored rows, gone. 
  📺 A calm home screen  Your apps, your HDMI inputs and a clock. Nothing else. 
  ↩️ Undo anytime  Apps are turned off, never deleted. 
 
 

## Watch it work

   

**[▶ Claude Made My Old Android TV Feel Brand New](https://www.youtube.com/watch?v=fP2SGGVsaB0)** · the full setup on a real TV, in 4 minutes.

## Get started

> [!WARNING]
> **Google TV and Chromecast with Google TV:** don't turn off the TV's own home screen. On some of these devices that left them stuck restarting, and the only fix was a factory reset. Since v1.4.1, `install.sh` leaves it on for Google TV unless you opt in with `GOOGLE_TV=1`. The cleanup still works and makes the TV faster. You just keep Google TV's own home screen.

> [!WARNING]
> **OLED TVs:** keep the screensaver on. It stops a still picture from burning into the screen. Don't leave any home screen, this one included, on for hours.

**1. Turn on developer mode on the TV.**
Settings → Device Preferences → About → press **Build** 7 times. Then turn on **USB debugging** in **Developer options**. [Stuck?](#help)

**2. Open [Claude Code](https://claude.com/claude-code) or [Codex](https://openai.com/codex) on your laptop.**
The laptop and TV must be on the same Wi-Fi.

**3. Paste this in.**

```text
Help me clean up my Android TV and make it faster.
My TV is a  .

1. Connect to my TV over Wi-Fi. Walk me through anything
   I need to tap on the TV.
2. Before changing anything, list every app in plain English:
   safe to turn off, needed by the TV, and apps I use.
   Check free memory.
3. Ask me before every change. Turn apps off instead of
   deleting them. Keep a list of what you changed and how
   to undo it.
4. Never turn off: Google Play services
   (com.google.android.gms), Google Play, Settings,
   System UI, setup apps, the keyboard, Bluetooth, my HDMI
   inputs, the TV's input and tuner framework, or anything
   else the TV needs to start. On Google TV or Chromecast,
   also never turn off Google TV's home screen
   (com.google.android.apps.tv.launcherx). If you're not
   sure, leave it on.
5. Install the home screen: download
   https://github.com/Ansub/tv-detox and run its
   install.sh with my TV and these apps:  .
6. Turn off animations and make the TV sleep after 5
   minutes. Then check the model name and ask me if the TV
   is OLED. Keep the screensaver on unless I say it's not
   OLED.
7. Wait 30 seconds after the last change, then restart the
   TV once and check it starts up normally before you say
   you're done. Show me free memory before
   and after.
```

That's it. It asks you before every change.

> [!NOTE]
> This is what worked for us, not professional advice. Use it at your own risk. You're responsible for your own TV, and I'm not liable if something goes wrong.

## Help

 
  How do I 

## 14. [youtube] Are Electric Cars More Reliable Than Petrol? | UK MOT Data #ElectricCars #EVs
key: yt:fMZk1sGMcc0
url: https://www.youtube.com/watch?v=fMZk1sGMcc0
meta: {"channel": "Parking Ticket Pal", "rank": 3, "duration_min": 0}
query: MOT data analysis uk

# Are Electric Cars More Reliable Than Petrol? | UK MOT Data #ElectricCars #EVs
# Parking Ticket Pal
# https://www.youtube.com/watch?v=fMZk1sGMcc0

[00:00] Would you write off a used EV just because it's done 100,000 miles? >> [music] >> Big mistake. The BVRLA analyzed 47.4 million MOT tests from 2024 to 2026, [music] comparing electric and petrol cars as mileage climbed. Between 90,000 and 120,000 miles, [music] EVs failed their MOT 16.5% of the time versus 22.1% [music] for petrol. Push past 120,000 miles and EV failures actually dropped to 16% while petrol rose to 23.5%. Even 15-year-old [music] EVs keep coming
[00:33] back for MOTs more than petrol cars do. The one weak spot? EVs get around [music] 1.8 times more tire defects thanks to extra weight and torque. So, don't dismiss [music] a high-mileage EV, but do check its tires, battery health, and service history before you buy.
