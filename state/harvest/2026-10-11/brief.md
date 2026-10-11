# Harvest brief, 2026-10-11

12 items shortlisted from 240 candidates (117 dropped as already seen, 13 carry a vault verdict on the vendor).

## 1. [vault] Extract the free classroom for the product-validation and repeat-purchase method, if Luke joins
key: vault:2026-10-11:extract-the-free-classroom-for-the-product-validation-and-re
url: https://www.skool.com/supplements
meta: {"vault_status": "open", "kind": "service", "subject": "Supplement Brand Accelerator (Skool, Lou Antonio Matera, free, 3,445 members)", "date": "2026-10-11", "where": "TRITON-CORE/Research/links/2026-10-11-supplement-brand-accelerator-skool.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Desktop extraction route; the validation method transfers to FBA product selection

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) A free private Skool community from a founder claiming a 3 million dollar supplement brand: 11 hidden courses on finding supplements people want, funnels, content, ad tests and repeat buyers, plus weekly calls. Written for the US market. A UK supplement brand is a regulated food product with a claims register, possible MHRA borderline, Amazon category approval, liability insurance and manufacturing minimums in the low thousands, so it is not a lane at Luke's capital. The method material is extractable if he joins; the validation method transfers to FBA product selection. Job: Pick physical products people already want before paying for stock (still open) Write-up: `TRITON-CORE/Research/links/2026-10-11-supplement-brand-accelerator-skool.md` Link: https://www.skool.com/supplements

## 2. [hn] Show HN: Littleguys – Claude Code, Codex and OpenClaw agents in your menu bar
key: hn:50038883
url: https://littleguys.hervalicio.us
discussion: https://news.ycombinator.com/item?id=50038883
meta: {"points": 15, "comments": 0, "created": "2026-10-11T01:19:18Z"}
query: claude code

page: littleguys: Mac menu bar app for Claude Code, OpenClaw & Hermes One look tells you everything. The guy in your menu bar acts out what your agents are doing. No dashboards, no tab-hunting. Everyone, at a glance. Click the guy for every agent on every machine, with a live status ring, the last message and a quick reply. Approve in one click. Commands that need you show up as cards: allow once, always allow or deny. No more “[y/N]” buried in terminal tab #9. Routines that just run. Morning digests, nightly dependency bumps, weekly numbers. Friendly schedules, run-now, and results that land in a thread. From any machine. Guys on your Mac mini, your homelab and your laptop, all in one place. Finds gateways on your tailnet and LAN by itself. Bring any guy. Claude Code Codex Gemini CLI Goose OpenCode OpenClaw gateway Hermes agent any ACP agent littleguys speaks the Agent Client Protocol, so new agents are one click away from the ACP registry. It's a friendly face for the agents you already run, not a new place to run them. Free. Open source. Yours. littleguys holds your gateway tokens and approves real commands on your machines. You should be able to read every line of it, so you can. Read the code 🔒 Talks straight to your agents. No littleguys account, no cloud. 📭 No analytics, no telemetry. 🦀 Rust core + React, built on Tauri. Install it. One app for Apple silicon and Intel, signed and notarized, for macOS 13 or later. Open the .dmg and drag littleguys into Applications. ↓ Download littleguys 0.1.1 or with Homebrew: brew install herval/tap/littleguys Copy Then look for the guy in your menu bar. It keeps itself up to date, and every release is on GitHub . Rather build it yourself? This one-liner builds littleguys from source for this Mac and puts it in /Applications : curl -fsSL https://www.littleguys.dev/install.sh | bash Copy It installs anything missing (the Xcode Command Line Tools, Rust, Node, pnpm) into ~/.littleguys , without sudo or touching your shell profile. Th

## 3. [github] aindeev/agent-chrome-relay: Let your AI agents use your Chrome, signed in as you, in background tabs. By Alexey Indeev · blog: read.aindeev.com · X: @AlexeyIndeev
key: gh:aindeev/agent-chrome-relay
url: https://github.com/aindeev/agent-chrome-relay
meta: {"stars": 251, "created": "2026-10-10", "pushed": "2026-10-11", "language": "Go", "topics": ["agent-browser", "ai-agents", "browser-automation", "cdp", "chrome-extension", "claude", "claude-code", "codex"]}
query: claude-code created:>{since} stars:>20

# Chrome Relay

 
     
     
     
     
     
 

**Website:** https://agent-chrome-relay.aindeev.com

Lets your coding agents (Claude Code, Codex, Cursor, Paseo) use **your everyday Chrome**, with your real
logins, from the command line, **in background tabs**: nothing takes focus, no dialogs, ~0.15s per command.

```bash
agent-browser --cdp "$(chrome-relay url you@company.com)" open https://app.example.com/
agent-browser snapshot -i          # the page's buttons, links and fields, each with a ref like @e5
agent-browser click @e5
agent-browser close
```

It's opt-in: nothing installs the extension for you, and it only runs on Macs whose owner set it up.

**The core** is background tabs with your logins, Google sign-in hops and an audit trail. **Everything else is
optional** and off until you turn it on: signing in with 1Password (passwords, 2-step codes, passkeys) and
Secure Enclave passkeys. See [What's optional](#whats-optional).

## How it works

```
agent-browser (CLI) ──ws──▶ relay (127.0.0.1:9333, LaunchAgent) ──ws──▶ Chrome Relay extension ──chrome.debugger──▶ agent tab
```

- **Extension** (`extension/`, MV3, one per Chrome profile you load it in): opens each agent tab **inactive**
  in a collapsed "Agents" tab group and runs DevTools commands in it via `chrome.debugger`. No remote-debugging
  port, so Chrome never shows "Allow remote debugging?". Chrome does show "Chrome Relay started debugging this
  browser" while agents work.
- **`chrome-relay`**: one Go program, **built and signed on your own Mac** (`./build`). As a background service
  (`chrome-relay serve`) it is the relay: a DevTools endpoint per agent, where each agent sees and controls only
  the tabs it opened and commands that could raise or focus the browser are swallowed. It is also the CLI
  (setup, the connection URL, diagnostics, audit trail), and the optional 1Password vault and passkeys, whose
  Secure Enclave and Touch ID code (`internal/macos`, Swift) is linked into the same signed binary when Xcode's
  command line tools are installed.

## Setup (once per Mac, ~2 minutes)

Fastest: paste [this prompt](https://agent-chrome-relay.aindeev.com/setup-prompt.txt) into Claude Code, Codex or
Cursor and let your agent do it. By hand:

Needs macOS, Google Chrome, [Go](https://go.dev/dl/) 1.25+ (`brew install go`) and
[`agent-browser`](https://github.com/vercel-labs/agent-browser) (`npm i -g agent-browser`).

```bash
git clone https://github.com/aindeev/agent-chrome-relay
cd agent-chrome-relay
./build                    # compiles chrome-relay and signs it on this Mac (see below)
./chrome-relay setup       # secret, background service, identities, `chrome-relay` on PATH, Claude Code skill
```

**Why you build it yourself**: the binary is signed on your Mac, and macOS ties Chrome Relay's Keychain item to
that signature, so only your own build can read it (see the 1Password section). The build uses the hardened
runtime, so other programs can't attach a debugger to the relay or inject code into it. Two things make the
build fuller, and neither is required:

| You have | `./build` makes | |
|---|---|---|
| Go only | the **core**: tabs, Google sign-in hops, audit trail | passkeys you keep in 1Password still work (1Password's prompt) |
| + Xcode's command line tools (`xcode-select --install`) | the core **plus 1Password and Secure Enclave passkeys** | |
| + a code signing identity | the same, **signed by you** | without one it signs ad-hoc: macOS may ask once after each r

## 4. [arxiv] Narrow and Deep: An Ontology Tower as the Knowledge of an LLM Agent for an Industrial Equipment System
key: arxiv:2610.11768
url: https://arxiv.org/abs/2610.11768
meta: {"published": "2026-10-08", "authors": ["Younghwan Joo", "Sung-il Kim"], "categories": ["eess.SY", "cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

Large language model (LLM) agents are beginning to operate industrial energy equipment, and what they get right depends on what they are told about the plant. Established building ontologies name many kinds of points across many sites, whereas an industrial equipment system needs few entities with much knowledge about each. This study proposes the ontology tower, a narrow-and-deep ontology of a single equipment system whose knowledge deepens in two ways: through quantities derived from the measured points by physical relations, and through lessons from the operating journal incorporated as knowledge nodes. On a real low-humidity air-handling test plant operated daily through a programmable logic controller, agents received a text projected from its tower in a preregistered evaluation of nine tasks replayed from the plant's records, using four open-weight models from 9 to about 750 billion parameters. This knowledge raised the rate at which the agents avoided the most plausible misjudgment of each task by about 20 percentage points, and the overall task score of the 9-billion-parameter model as much as that of the largest. Operating lessons were used when incorporated into the tower or placed in the prompt as records, but seldom when left in the journal behind a search tool. In live runs through an invariant safety layer, the agents brought the controlled variable into its target band in 12 of 14 runs. An ontology narrow in entities but deep in what is known about them can thus supply the knowledge that an agent for an industrial equipment system needs.

## 5. [youtube] How the Top 1% Use Claude Code Differently
key: yt:J9NQTYUP6k0
url: https://www.youtube.com/watch?v=J9NQTYUP6k0
meta: {"channel": "Simon Scrapes", "rank": 1, "duration_min": 18}
query: claude code skills workflow 2026

# How the Top 1% Use Claude Code Differently
# Simon Scrapes
# https://www.youtube.com/watch?v=J9NQTYUP6k0

[00:00] Every piece of claw code advice for the last year has said the same thing. Start in plan mode, including the person who built it. So in January, Boris Churnney said most of his sessions start in plan mode. But two weeks ago on Hacker News, he said plan mode is no longer useful. So 9 months apart, the way Boris and the other 1% use Claude has completely changed. So here are the 10 things the top 1% are doing so you can have the best setup and stop wasting time on old advice, starting with what they use instead of plan mode. So when you consider what plan mode actually did, it never changed what Claude could actually
[00:32] do. So it just added a reminder to every prompt message along the lines of you're in plan mode, please don't start coding yet. So he came up with that late one Sunday night because he was tired of asking Claude to plan before it actually started building. And it's kind of funny that the idea that he just came up with on a Sunday night ended up being so integral to the way that we worked with claw code every single day. Now at the time it was actually really useful because the older models, think back to things like Sonic 4.6 and early Opus, they all had a tendency to jump straight in and just get on and do the work. So, it was a model limitation. But with the newer models, he just stopped using it because
[01:05] planning now happens while the model works. So, what he does instead, as he explained at the YC startup school, is he describes the task, describes the guardrails that surround the task, describes what done looks like, so our definition of done, and then let the model actually work it out. So, for example, for your weekly client report, that might just be three lines. The task is this week's report from the CRM export, for example. The guardrails are don't amend the template that we've set and don't email anyone. And then the definition of done is every figure matches the export. And now instead of reading a plan before that task starts,
[01:39] you can now check what it did after. And that is the advice now. So for his bigger changes, Boris asked Claude for a diagram or even an interactive demo of what it changed. And if you'd seen just yesterday, Claude also announced that it now has a built-in capability to produce live dashboards and animated explainers. So, it's even easier to get that interactive output. So, when the task finishes, you're going to ask it for a onepage visual of what it did and what it assumed whilst it was doing that task. So, here's the picture we're building throughout this video. On the left is you, and the only thing you write is actually the brief. Claude is going to do the work, and what comes back is the output plus that onepage
[02:13] explainer. So you're basically checking the result now and you're no longer planning it up front in as much detail. Now that brief that we've got, it says exactly what to do and what guardrails, but a lot of us still try to control how hard Claude thinks about it. But actually the new advice is to ignore that entirely. So you might remember back to last year when they said you had to write things like think, think hard, think harder, or ultra think. And each one got Claude a bigger thinking budget. But now Claw Code reads think hard as effectively just part of the prompt. It reads it as ordinary words. So this became its own setting 
[transcript continues in field-notes/staging/J9NQTYUP6k0.txt]

## 6. [vault] Phone-gated lead magnet to free workshop to done-for-you app build agency
key: vault:2026-09-20:phone-gated-lead-magnet-to-free-workshop-to-done-for-you-app
url: https://keza.studio/10-app-templates
meta: {"vault_status": "open", "kind": "idea", "subject": "Keza Studio \"10 app templates\"", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-jev-sideshift-invo-keza.md (section 5)", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: How a UK agency packages a founder funnel; SMS-verified phone gate is a deliberately higher-value capture

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) Real London studio with real directors. The templates are ten planning documents, a lead magnet for an app-build agency, not code. No. Job: Go from an app idea to a shipped product without being able to code (still open) Write-up: `TRITON-CORE/Research/links/2026-09-20-jev-sideshift-invo-keza.md (section 5)` Link: https://keza.studio/10-app-templates

## 7. [github] LingCore/WinShun: Win顺：免费开源的 Windows 快速搜索启动器。双击 Ctrl，拼音秒搜文件、全文搜索 Word/Excel/PDF、剪贴板历史（代替 Win+V）、对话框搜索、任务栏搜索、插件、AI 助手 MCP。Free Windows search launcher: pinyin file search, full-text search, clipboard history, MCP server. Everything/Listary alternative.
key: gh:lingcore/winshun
url: https://github.com/LingCore/WinShun
meta: {"stars": 185, "created": "2026-10-08", "pushed": "2026-10-11", "language": "C++", "topics": ["chinese", "clipboard-history", "clipboard-manager", "cpp", "everything", "file-search", "full-text-search", "launcher"]}
query: mcp server created:>{since} stars:>30

Win顺 · WinShun 

 
   双击 Ctrl，搜遍整台电脑  —— 免费开源的 Windows 文件搜索、快速启动器 
   Press Ctrl twice, search your whole PC  — a free, open-source file search and launcher for Windows
 

 
     
   
   
     
     
 

 
   中文  ·  English  ·  截图 Screenshots 
 

 
   
 

 
  拼音秒搜文件 · 文件内容全文搜索（Word / Excel / PPT / PDF） · 应用和系统设置 · 网页搜索 · 收藏夹 · 插件 
  “打开 / 另存为”对话框搜索 · 剪贴板历史（代替 Win+V，图片文字也能搜） · 任务栏搜索框（代替 Win+S） · AI 助手 MCP 
   Pinyin file search · full-text search in documents · apps and settings · web search · favorites · plugins · file dialog search · clipboard history with OCR · taskbar search box · MCP server for AI assistants 
 

---

  

## 截图 · Screenshots

 
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
 

---

  

## 中文

**Win顺** 是 Windows 上免费开源的快速搜索启动器：连按两下 Ctrl 弹出搜索框，边打字边出结果。按文件名或拼音秒找文件，搜 Word、Excel、PDF 里的文字，打开应用和系统设置，还有剪贴板历史、对话框搜索、任务栏搜索框、插件和给 AI 用的 MCP 搜索。

它直接读 NTFS 主文件表（MFT）建索引，三百多万个文件几秒建好，增删改名实时跟上，**不用装 Everything**。不需要账号，不上传数据。界面有简体中文和英文。

### 功能

#### 🔍 文件搜索

- **双击 Ctrl** 打开，再按一次或 `Esc` 关闭；三百多万个文件里搜一次只要几毫秒。
- **拼音和首字母**：`ndbg` → 年度报告，`baog` → 报告；多音字按常用读音。
- **搜整台电脑**：所有本地磁盘，U 盘可选；**NAS、内网共享文件夹（SMB）** 也能加进来一起搜，服务器关机时收录过的照样能搜到。
- **排序懂你**：自己的文件在前，系统目录、`node_modules` 在后，名字完全一样的最前。每行显示修改日期，`Ctrl+S` 在最匹配、最新、最早之间切换。不输入时列出最近打开或最近修改的文件。
- **数字键直达**：按住 `Ctrl` 显示序号，`Ctrl+1`～`Ctrl+9` 打开第几行（也可改成 `Alt`）。
- **只找文件夹**：选中 **文件** 后再按 `Tab`。
- **拖出去就能用**：结果直接拖进微信、邮件、资源管理器。
- **实时更新**：读 USN 变更日志，改名、新建、删除马上搜得到；拔 U 盘不会提示“设备正在使用”。

| 搜索语法 | 含义 |
|---|---|
| `报告 2024` | 每个词都要有（空格分隔，顺序不限）；也可以在所在文件夹的名字里 |
| `ndbg`、`niandubaogao` | 拼音全拼、首字母，可以混用 |
| `"年度 报告"` | 引号内作为整体 |
| `!草稿`、`!node_modules\` | 排除文件名、排除文件夹 |
| `*.pdf`、`报告?.docx` | 通配符 |
| `ext:pdf,docx` | 只要这些扩展名 |
| `项目\readme` | 在名字含“项目”的文件夹下 |
| `tools/out/`、`D:\My Files\` | 路径直达：回车进去，列出里面的内容 |

#### 📄 文件内容全文搜索

- 切到 **内容** 范围，搜文件里的文字，结果显示命中的那一行。
- **能搜的文件**：
  - 纯文本：txt、md、log、csv、json、代码等；
  - 文档：**Word、Excel、PowerPoint、PDF、WPS**，结果里显示第几页、第几张幻灯片或哪个表的第几行。
- **怎么找**：可以写多个词、用引号找整个短语，结果按相关度排。
- **编码和速度**：自动识别 UTF-8、UTF-16、GBK 编码；有内容索引，几十万个文件也很快。
- **安全**：文档由一个权限受限的独立进程读取。

#### 🚀 应用和系统设置

- **应用**：开始菜单里的所有应用都能搜，含 Microsoft Store 应用。名称、拼音、首字母（`vsc`）、程序名（`winword`）都行；`Ctrl+Shift+Enter` 以管理员身份运行。
- **系统设置**：约 1200 个 Windows 设置页和控制面板项。`shipeiqi`、“网卡”、`ncpa.cpl` 都能打开网络连接；另外补了组策略、磁盘管理、hosts、AppData 等开始菜单里没有的。

#### 🌐 网页搜索 · ⭐ 收藏夹 · 🧩 插件

- **网页搜索**：`baidu 天气`、`zhihu 显卡`、`jingdong 键盘`，关键词加空格就在那个网站上搜。
  - 自带百度、必应、B 站、知乎、微博、抖音、小红书、淘宝、京东、翻译。
  - 可以用 `%s` 网址添加自己的网站，图标、列表都能导入导出。
- **收藏夹**：
  - 右键“加入收藏夹”，不打字时排在最前；
  - 起个关键词，一打就开；
  - 收藏的文件夹按 `Tab` 进去接着搜。
- **插件**：
  - 随包的小工具：`= 1+2*3` 计算器、`12 inch to cm` 单位换算、`#ff8800` 颜色，还有时间戳、UUID、Base64、哈希；
  - `kill` 结束进程，`bm` 搜浏览器书签，`tr` 翻译；
  - 自己写插件：零代码的 `plugin.json`、任意语言的脚本或常驻进程都行，附 Python / PowerShell / C++ SDK；
  - 插件以普通权限、限内存运行。见 [docs/plugins.md](docs/plugins.md)。

#### 📂 “打开”“另存为”对话框

- **对话框旁的搜索框**：输入文件夹或文件名（拼音也行），回车，对话框直接转过去；网页上传文件、WPS 的对话框也认。
- **`Ctrl+G`**：转到资源管理器、Total Commander 或 Directory Opus 正在显示的文件夹，和 Listary 的同名快捷键一样。
- **不输入时**：列出打开着的文件夹、刚复制的路径、收藏和最近用过的文件夹。
- **自动转过去**：可以设成对话框一出现就转到文件管理器的文件夹。

#### 📋 剪贴板历史（代替 Win+V）

- **记什么**：复制过的文字、图片、文件都记下来。
- **怎么打开**：`Win+V` 或自设的快捷键；开在输入光标旁，不抢焦点。
- **怎么粘贴**：双击或 `Enter` 粘贴，`Shift+Enter` 粘贴为纯文本，`Alt+1`～`9` 直接粘贴第几条。
- **能搜**：拼音搜索，`@wx` 只看微信里复制的；**图片里的字也能搜**（Windows 自带的文字识别 OCR，在本机，不联网）。
- **预览**：全文、大图、颜色值的 HEX / RGB / HSL。
- **整理**：固定、分组、多选按顺序合并粘贴，钉住后可以一条接一条地往表格里填。
- **隐私**：密码管理器复制的密码不记录，历史只存在本机。

#### 🔎 任务栏搜索框（代替 Windows 搜索）

- 在 Windows 11 任务栏上放 Win顺 自己的搜索框（Windows 10 是固定一个按钮），结果从任务栏上方滑出。
- 可以接管 `Win+S`，开始菜单里

## 8. [arxiv] TRACE: Diagnosing Verifier Brittleness in Agentic Evaluation
key: arxiv:2610.11678
url: https://arxiv.org/abs/2610.11678
meta: {"published": "2026-10-08", "authors": ["Radhika Gaonkar"], "categories": ["cs.CL"]}
query: all:"language model" AND all:agent AND all:tool

Verifier scores now serve as both benchmark metrics and training rewards for large language model (LLM) agents, and a change in score is routinely read as a change in capability. It may instead reflect a change in the evaluation. We introduce TRACE, a protocol that turns a score change from a verdict into a testable diagnosis: it applies a targeted change to one part of an evaluation, compares paired runs, checks whether the agent's behavior changed, and rescores unchanged trajectories to test whether the scoring rule is responsible. In a controlled suite of 25 synthetic tasks, renaming tools lowers a scripted agent's score by 0.250 even though it performs exactly the same operations; restoring the original names at scoring time closes the entire gap, while the same mutation exposes a genuine behavioral failure in a second agent. On public $τ^2$-bench tasks with four LLM agents, an initial 30-task study finds mixed reward changes whose one clear effect does not replicate. In a larger follow-up on 88 new tasks with repeated runs per condition, renaming tools or reformatting tool outputs leaves reward unchanged to within $\pm$0.10 for seven of eight agent-change pairs, whereas tool names that deliberately mislead lower every agent's reward by 0.20-0.44, showing that the setup can detect real effects. Identical reruns flip 15-36% of task outcomes, so single-run comparisons cannot separate presentation effects from run-to-run variation. Two frontier LLM judges give consistent verdicts when a fixed trajectory is presented differently, yet disagree with each other on 57% of the same records, largely because one grades procedure rather than outcome. TRACE thus separates what a score change says about the agent from what it says about the measurement.

## 9. [youtube] Anthropic Engineers Just 10x'd Everyone's Claude Code
key: yt:oz2CwrPV2Rg
url: https://www.youtube.com/watch?v=oz2CwrPV2Rg
meta: {"channel": "Nate Herk | AI Automation", "rank": 2, "duration_min": 12}
query: claude code skills workflow 2026

# Anthropic Engineers Just 10x'd Everyone's Claude Code
# Nate Herk | AI Automation
# https://www.youtube.com/watch?v=oz2CwrPV2Rg

[00:00] So, Anthropic engineers just 10x Claude code by deleting over 80% of its system prompt, but they also changed everything that we know about prompting. Because a lot of us were told the best way to get Claude to behave the way we want it to was to give it as much information and context as possible. But with this change, almost all of your information is actually slowing Claude down and slowing down its thinking speed. So, today I'm going to show you how to fix your projects using the engineering approach from Anthropic. So, let's get into it. All right, so Thoric, one of the engineers at Anthropic, recently published an article called The New Rules of Context Engineering for Claude 5 generation models. His team removed
[00:32] over 80% of Claude code system prompt for models like Opus 5 and Fable 5 and 5.1 and future models, and they reported no measurable loss on their evaluations of these models. The system prompt is basically the rulebook that comes with Claude code. So, your own instructions and whatever context gets loaded for the task sit right alongside of the system prompt. So, they're saying that they could cut most of that rulebook and keep the performance that they had measured. And in my own setup, I used their guidance to review the instructions that I'd accumulated and clean up how my skills work together. And this goes right alongside with Boris Cherny, the creator of Claude code said himself, which was basically like every 6 months you should delete all of your skills.
[01:06] And we've been told that skills are what makes Claude code much smarter and much more consistent. Now, Anthropic describes that rules they needed for older models became too restrictive as Claude actually just got better and better. One example was comments in code because they used to put a hard limit on how much Claude could write even though some projects needed more explanation. [music] The replacement now tells it to follow the style of the surrounding code. I think it's pretty easy to end up with the same problem in your own setup. You know, Claude makes a mistake, you add a rule, and then a few months later you've got that rule in your Claude.md file or in a skill, maybe a slightly different version of it somewhere else, and you don't actually need that rule because you keep upgrading the model,
[01:38] but the instructions still stay in there. And the model might not need all of that extra context now. I recently did a video about prompting Fable 5.1. I talked about the idea of defining to the model what done looks like. You basically need to give it the outcome that you're after, why you're doing it, and the constraints that it needs to respect. And then you just have to get out of its way. Leave it some room to actually do [music] the work. So, for this video, I asked Claude to look at how I get from a YouTube idea to a script that I could film [music] or an outline that I could film about, and I wanted it to find a small improvement and point me to the file so that I could check the recommendation for myself. So I'll show you guys that demo of me actually doing this later in the video.
[02:10] Now, Anthropic's applied AI team recommends using the smallest amount of context that gets the result you want, and I turn that into sort of my own saying, which is the best context is the smallest amount of con
[transcript continues in field-notes/staging/oz2CwrPV2Rg.txt]

## 10. [vault] Public on-chain leaderboards as the check on any trader's claimed record
key: vault:2026-09-20:public-on-chain-leaderboards-as-the-check-on-any-trader-s-cl
url: 
meta: {"vault_status": "open", "kind": "service", "subject": "Potion Alpha (Orangie) and trader Kimchi", "date": "2026-09-20", "where": "TRITON-CORE/Research/links/2026-09-20-five-saved-items-gta6-pumpfun-potion-mev-calibriai.md (section 5)", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: Kolscan, GMGN, Solana Tracker and Dune are the genuine ones; none belong to the paid community

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Paid Discord community ($599 a year) with self-reported PnL screenshots and no working leaderboard found. Kimchi's $40m TRUMP claim has no wallet behind it. Skip. Job: Find and follow traders whose edge is verifiable on-chain rather than claimed (still open)

## 11. [github] liyupi/ai-promo-video-maker: 一句话让 AI 帮你做产品宣传片！把产品名或网址告诉 Cursor、Claude Code、Codex 等 AI 编程工具，它会自己调研产品、画出多种风格样图让你挑选、截取 4K 真实页面、按音乐节拍卡点剪辑、生成 AI 旁白并逐句转写校验、自动审图，最后交付一支 4K 商业宣传视频和可在线播放的网页版。App、网站、SaaS、开源项目、课程、AI 模型都能做，你只需确认需求、试听配乐。不用学剪辑软件，也不用花钱找外包。基于 Remotion + ElevenLabs，可直接克隆使用，也能一键安装为 Agent Skill。
key: gh:liyupi/ai-promo-video-maker
url: https://github.com/liyupi/ai-promo-video-maker
meta: {"stars": 139, "created": "2026-10-09", "pushed": "2026-10-09", "language": "Python", "topics": ["agent-skills", "ai-agent", "ai-video", "ai-video-generator", "aigc", "claude-code", "claude-skills", "codex"]}
query: claude-code created:>{since} stars:>20
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# 产品宣传视频制作器

**一句话告诉 AI 你要宣传什么，它会自己调研、提问、截图、配乐、配音、剪辑和校验，最后交给你一支 4K 商业宣传片。**

[](LICENSE)

 

上面这段动图依次截取了 5 支宣传片的开场，它们全部由这个工具做出来，风格却完全不同。编程学习社区用的是浅色等距 3D 地图，面试刷题平台用的是黑白热血漫画，AI 导航网站用的是明亮的水下 Q 版画风，一个还没正式发布的 AI 模型用的是泄密档案风，零基础编程教程则做成了一支电影预告片。这些风格都不来自预设模板，而是 AI 针对每个产品提出几个方向、画出样图，再由产品作者亲自挑选的结果。

## 这是什么

做一支像样的产品宣传片，通常要经过写脚本、找素材、设计画面、剪辑卡点、配音混音好几道工序。外包一支往往要花几千甚至上万元，自己做又得学会一整套专业软件。

这个项目把整套制作流程写成了一份 AI 能读懂、能照着执行的工作规范（`AGENTS.md`），并配上一个 Remotion 视频工程模板和十几个辅助脚本。你可以把仓库克隆到本地，用 Cursor、Claude Code、Codex 这类 AI 编程工具打开目录；也可以把它安装成一个 Skill，在任何项目里随时调用。无论哪种方式，你都只需要用一句话说明想给什么做宣传片。至于产品有哪些卖点、该用什么风格、哪些画面能打动人，这些不确定的事情都由 AI 先去调研，再拿着具体的选项来问你。

这里说的「产品」范围很广，App、网站、SaaS 工具、开源项目、课程教程、AI 模型、社区和线下活动都可以，只要它有能拿出来展示的界面或作品。

## 快速开始

制作过程会用到 Node.js 18 以上版本、Python 3.9 以上版本和 ffmpeg，请先确认电脑上已经装好这三样软件。其余的 Python 依赖和截图用的浏览器内核，AI 在开工前做环境体检时会提示你安装。

接下来可以从两种用法里选一种。如果只是想试一试，或者要宣传的产品没有本地代码，选择克隆仓库更直接；如果你想在自己的产品仓库里随时说一句「给这个项目做个宣传片」，就安装成 Skill。

### 克隆仓库直接使用

把仓库克隆到本地，再安装 Python 依赖和截图用的浏览器内核。

```bash
git clone https://github.com/liyupi/ai-promo-video-maker.git
cd ai-promo-video-maker
pip install -r template/requirements.txt
playwright install chromium
```

如果不确定环境是否齐全，可以运行一次体检脚本。它只做检查、不会安装任何东西，并且会逐项告诉你缺了什么、该用什么命令补上。

```bash
python3 template/scripts/doctor.py
```

然后用 AI 编程工具打开这个目录就可以开始了。做好的成片会保存在 `outputs/ /` 目录里。

### 安装成 Skill 使用

这个仓库本身就是一个标准的 Agent Skill，可以用 [skills](https://github.com/vercel-labs/skills) 命令行工具一键安装到 Claude Code、Cursor、Codex 等 AI 工具里。加上 `-g` 表示安装到用户目录，这样所有项目都能用。

```bash
npx skills add liyupi/ai-promo-video-maker -g
```

安装以后，在任意项目里对 AI 说「给这个项目做一支宣传片」，它就会自动调用这个 Skill。这种用法特别适合在产品自己的代码仓库里使用，因为 AI 可以直接读取源码、文档和 README，拿到最准确的一手素材。成片会保存在当前项目的 `宣传片/` 目录里，AI 也会提醒你把这个目录加进 `.gitignore`，以免几个 GB 的工程文件被提交上去。以后想更新到最新版本，运行 `npx skills update` 即可。

### 配置 ElevenLabs（可选）

如果你有 [ElevenLabs](https://elevenlabs.io) 账号，可以把 `.env.example` 复制到工作区根目录并改名为 `.env`，然后填上 API Key；也可以直接设置环境变量 `ELEVENLABS_API_KEY`。这样 AI 就能为片子生成旁白、按分镜定制配乐和音效，还会用语音转写逐句检查旁白有没有读错字。

没有账号也完全可以做片子。这种情况下 AI 会从免费可商用的 Mixkit 曲库里挑选配乐，再用醒目的大字幕代替旁白。

### 用一句话开始

不管用哪种方式，开始的方法都一样：像跟同事交代任务一样说一句话就行。下面是几种常见的说法。

```text
帮我给 https://example.com 做一支宣传片
```

```text
给我的开源项目做一支 1 分钟的介绍视频，仓库地址是 https://github.com/xxx/yyy
```

```text
我们的记账 App 下周上线，做一支能发抖音的竖屏宣传片
```

说完之后，AI 会先花几分钟了解你的产品，然后分两轮向你提问，问题涉及画幅时长、目标受众、风格方向、开场方式、配乐和截图来源等方面。每个问题都会附带一个针对你的产品的推荐选项和理由，拿不定主意时直接选推荐项，或者回答「你来决定」都可以。

等你确认需求以后，AI 就会自动完成剩下的全部工作。中途它只会在三种情况下来找你：需要你登录某个网站以便截图、需要你试听配乐和音色、遇到只有你才能核实的事实。

### 推荐使用的模型

推荐使用 **Claude Opus 5.5** 或者更先进的模型。一支宣传片要经过十几个步骤，以及反复多轮的截图审查和音频校验，模型需要在很长的上下文里始终记得规范里的要求，同时还要有不错的审美判断。能力较弱的模型往往会跳过校验步骤，或者不知不觉把每个产品都做成千篇一律的深色科技风。

## AI 会先给你看样图，再动手

在开始制作之前，AI 会针对你的产品提出 3 到 4 个差异明显的风格方向，并为每个方向画一张样帧，让你直观地看到「这个风格用在我的产品上是什么样子」。下面是面试刷题平台「面试鸭」在需求问询阶段收到的 4 张样帧，最终作者选择了右上角的热血漫画风格。

同样的流程用在 AI 导航网站上，得到的候选完全不同。这一次作者选了右上角的 Q 版小鱼风格，吉祥物就是以网站 logo 为原型设计的。

你可以从中挑一个，也可以混搭，比如「A 的配色加上 C 的角色」。AI 会把你的选择连同其他所有决定一起写进 `需求确认.md`，等你确认无误后才开始制作。

## 成片展示

下面这 5 支片子都是用这个工具完成的。每支片子都经历过几轮真实的修改意见，这些意见后来都被提炼成了规范里的规则。

### 编程导航：等距 3D 导航地图

编程导航是一个编程学习社区。这支片子用代码绘制了一座浅色的等距 3D 城市，把学习路线、项目教程、面试求职串成一条通往 Offer 的道路。片子以三个学编程的痛点开场，第 4.4 秒音乐爆发、品牌登场，随后用 10 张登录后截取的 4K 真实页面逐一展示各个板块。配乐、音效和旁白全部由 ElevenLabs 生成。

### 面试鸭：黑白热血漫画

面试鸭是一个程序员面试刷题平台。片子采用黑白漫画风格，全片只用一种鸭黄色作点缀。开场直接连发 4 道站内浏览量最高的真实面试题，配乐由 AI 按分镜作曲，包含两次爆发和一段回落，旁白恰好在回落段讲解答案。漫画分格由 AI 生成后再经过 4 倍超分，保证在 4K 画面里线条依然清晰。

### 鱼皮 AI 导航：明亮水下 Q 版

鱼皮 AI 导航是一个 AI 工具与资源导航网站。片子的主角是一条以网站 logo 为原型的小鱼，它游过一个个浏览器窗口，窗口里滚动播放着网站各个栏目的真实页面。这支片子前后改了 5 轮，「配乐要先让用户试听」「截图必须保持原比例」「品牌名要逐字校验读音」这几条规则都是在这个过程中总结出来的。

### Claude Fable 5.5：泄密档案风

这是一支比较特别的「抢先看」。片子介绍的 AI 模型版

## 12. [youtube] How to Build Your First MCP Server (in Less Than 5 Minutes)
key: yt:Y4bpWRLdRoA
url: https://www.youtube.com/watch?v=Y4bpWRLdRoA
meta: {"channel": "Postman", "rank": 3, "duration_min": 8}
query: mcp server build tutorial

# How to Build Your First MCP Server (in Less Than 5 Minutes)
# Postman
# https://www.youtube.com/watch?v=Y4bpWRLdRoA

[00:00] Let's build your first MCP server together in less than five minutes. Hey everyone, Sterling here. Everyone in the AI space is talking about MCP. So, let's talk about what it is, how it works, and let's build your first server together. Let's get started. Let's start by giving a little context on MCP. If you want to jump straight ahead into building your first MCP server, feel free to skip ahead. You'll find the timestamps in the description down below. Traditionally, when we wanted an AI to interact with
[00:33] APIs, we had to be extremely prescriptive. Imagine having a skilled mechanic but being forced to micromanage their every move. Now, use the 10 mm wrench. No, not that way. This way. Now, put it down and grab the socket set. We'd code explicit instructions for every scenario. If the user asks about weather, then call this endpoint with these parameters. The AI had no autonomy. Everything was hard-coded logic requiring extensive programming for every possible path. This is where MCP changes everything. Think of it like
[01:08] giving a skilled mechanic a wellorganized toolbox of specialized tools and letting them choose the right tool for each job. Instead of hovering over their shoulder and dictating every move, you simply provide the tools and let them apply their expertise. MCP works the same way. An MCP server acts as a toolbox defining what tools are available to the AI. The server tells Claude, "Here are the tools you have access to without prescribing exactly when or how to use each one." Claude can then autonomously select the appropriate tool based on the conversation. Just
[01:41] like a good mechanic knows exactly which tool to reach for. An MCP server provides three types of capabilities for AI models. First is tools. These are functions that the agent can call like a weather API. Second are resources. This is filel-like data that the agent can read. And lastly, three prompts. These are the pre-written templates for specific tasks. Let's take a look at the simplified structure of an MCP server to show how all the parts fit together. First, we have the helper functions. This is where we're actually calling the
[02:13] APIs and formatting the data that Cloud will use. Next, we have the server instance. This is where we're defining the server's metadata, including the capabilities, resources, and tools. And lastly, the magic happens in the server.tool method. This is where we define what tools Claude can use, how to call them, and what parameters they accept. Each tool is like a specialized instrument in a mechanics toolbox. All right, let's get to building our first MCP server. Before we dive into the code, there are a few prerequisites that we need to have. First, you'll need to
[02:46] download the Cloud Desktop app. Second, you'll need your ID of choice. I'm using cursor, but VS Code, WebStorm, or any other JavaScript friendly editor will work just fine. And you'll need node and TypeScript. So, in my terminal over here, I'm going to type I'm going to go make dur weather and I'll CD into weather. And now I'll mpm in it. And we'll install the necessary dependencies. Don't worry, all of this
[03:18] will be in the description down below. All right. And now let's make a digital folder and files. So we'll cd Oh, we'll make dur source. And I'm just going to CD into source and touch index.ts. There 
[transcript continues in field-notes/staging/Y4bpWRLdRoA.txt]
