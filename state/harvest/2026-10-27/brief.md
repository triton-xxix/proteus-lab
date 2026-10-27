# Harvest brief, 2026-10-27

9 items shortlisted from 349 candidates (228 dropped as already seen, 14 carry a vault verdict on the vendor).

## 1. [vault] comment-keyword indicator funnel
key: vault:2026-10-15:comment-keyword-indicator-funnel
url: https://www.instagram.com/reel/Dee_ogTKexd/
meta: {"vault_status": "intel", "kind": "idea", "subject": "@brokermanscalps AI indicator reel", "date": "2026-10-15", "where": "TRITON-CORE/Research/links/2026-10-16-brokermanscalps-ai-indicator-reel.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: banned-for-winning and 100 pct win-rate script

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) no; indicator-seller funnel, 100 pct win rate and banned-for-winning claims, nothing specified to test Write-up: `TRITON-CORE/Research/links/2026-10-16-brokermanscalps-ai-indicator-reel.md` Link: https://www.instagram.com/reel/Dee_ogTKexd/

## 2. [hn] Is my data used for model training?
key: hn:50259406
url: https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training
discussion: https://news.ycombinator.com/item?id=50259406
meta: {"points": 211, "comments": 92, "created": "2026-10-27T13:56:15Z"}
query: claude code

comment (fxwin): ... what else would we expect it to do? > When you provide us feedback via our thumbs up / down button, we will store the entire related conversation, including any content, custom styles, conversation preferences, or model settings, in our secured back-end for up to 5 years. [...] We do not combine your feedback with your other conversations with Claude.
comment (selectedambient): and sky blue
comment (skeledrew): If they don't use the available data, how do they act on the feedback?

## 3. [github] ZiChuanLan/agent-purge: One persona, many coding agents. Replace or inject system prompts across codex, claude, opencode, grok, omp, hermes, pi, zcode - with a local web console.
key: gh:zichuanlan/agent-purge
url: https://github.com/ZiChuanLan/agent-purge
meta: {"stars": 581, "created": "2026-10-25", "pushed": "2026-10-27", "language": "JavaScript", "topics": ["claude-code", "codex", "coding-agent", "opencode", "pi", "system-prompt"]}
query: claude-code created:>{since} stars:>20
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# agent-purge

[](https://www.npmjs.com/package/agent-purge)
[](https://github.com/ZiChuanLan/agent-purge/stargazers)
[](LICENSE)

一份系统提示词，喂给多个 coding agent。支持替换（replace）、只发人设（strict）、追加（append）、清空（off）四种模式，可热切换，全程可逆。

```
agent-purge web          # 本地控制台 http://127.0.0.1:7788
agent-purge codex        # 用当前 persona 启动 codex
agent-purge pi --ask "…" # 一次性提问
```

## 它做什么

每家 coding agent 读系统提示词的位置都不一样：有的认启动参数，有的认配置文件，有的只能靠插件改运行时对象。agent-purge 把这些入口统一成三件事：

| 通道 | 机制 | 生效范围 |
|---|---|---|
| `install` | 写入该 harness 的托管配置块（Markdown / hooks / 插件） | 常驻，别人启动也生效 |
| `shim` | 往 PATH 前置同名小壳，转发给 `agent-purge  ` | 裸敲命令也接管 |
| `slash` | 会话内 `/purge on\|off\|status` | 热切换，不动磁盘 |

三层都写的是同一份 `personas/ .md` 的正文。`--mode off` 或 Web 总开关关掉时，全部撤回到原样——不留残渣。

## 安装

```bash
npm i -g agent-purge     # 或 npx agent-purge web
```

要求 Node ≥ 20，零依赖。

**数据独立存放**，升级不会被覆盖：默认 `~/.agent-purge/`（Windows `C:\Users\ \.agent-purge\`），里面是 `state.json` 和 `personas/`。想换位置就设环境变量：

```bash
export AGENT_PURGE_HOME=/path/to/your/data     # Windows: setx AGENT_PURGE_HOME D:\ap-data
```

旧版本（0.1.x）把数据放在包目录里，首次运行会自动搬到新家，原文件不动。

## 人设

`personas/ .md` = frontmatter + 正文。正文就是会被写进系统提示词的那一段。

frontmatter 用 `description` 写「说明」（Web 列表和 `agent-purge ls` 显示的就是它）；旧的 `desc` 仍然认，不会报错。可选 `order`（排序）、`harness` / `model`（匹配用）。Web 里只改名字和说明时会保留 frontmatter 的其它键，不整段重写。

```bash
agent-purge ls                 # 列出全部 persona，标出当前匹配的
agent-purge use             # 切换当前 persona
agent-purge pi --persona    # 只这一轮用别的
```

首次运行会在 `personas/` 下生成 `neutral.md` 起步模板。

## 支持情况

每个数字都是实测值：本地假 provider 抓真实请求体，不是估算。

| harness | 机制 | 实测版本 | 默认 system | 注入后 |
|---|---|---|---|---|
| `codex` | 启动参数 `-c model_instructions_file=` | 0.163.0 | 21,026 | 24 |
| `claude` | `--system-prompt-file` + 二进制补丁清残留身份句 | 2.1.304 | 6,379 | 156 |
| `grok` | `--system-prompt-override` | 1.0.62 | 5,146 | 21 |
| `omp` | `--system-prompt` | 17.4.2 | 34,511 | 10,106 |
| `hermes` | 临时 HOME 里替换 `SOUL.md` | 0.21.5 | 8,139 | 7,554 |
| `zcode` | UserPromptSubmit hook（user 角色）+ `customSystemPrompt` | 0.16.9 | 9,359 | 9,359 |
| `opencode` | cwd 下 `.opencode/plugin/*.ts` 原地改 `output.system` | 1.19.3 | 19,332 | 112 |
| `opencode2` | `plugins/agent-purge-v2.ts` 的 `ctx.session.hook("context")` | 0.0.0-beta-17823 | 8,279 | 3,189 |
| `dsh` | cordis 插件（三个 profile 各一份） | 0.2.1-rc.2 | 5,713 | 68 |
| `pi` | 原生扩展，会话内 `/purge` | — | — | — |
| `antigravity` | 等长替换二进制里的身份句 | 1.23.x | ≈20,498 | — |
| `codebuddy` | `--system-prompt-file` | 2.171.0 | — | — |
| `qoder` / `workbuddy` | 不支持（提示词在服务端） | — | — | — |

`opencode` 和 `opencode2` 是两个不同的 npm 包（`opencode-ai` 1.x 与 `@opencode/cli` 2.x），插件接口完全不同，各自独立支持。

`agent-purge ls` 和 Web 控制台显示的是**运行期真值**：每个 harness 有没有装、版本、注入层（SYS / USER）、三个通道各自可用性。`matrix.json` 里是静态能力表，两者冲突时以运行期为准。

闭源桌面端（提示词在服务端或二进制里）只做原样启动，不做任何注入——`agent-purge  ` 会明确打印原因，不会假装生效。

### 常驻安装（install）

```bash
agent-purge install        # 写进该 harness 自己的托管位置，别人启动也生效
agent-purge uninstall      # 摘掉，按字节还原
```

dsh 是唯一有多个形态的：desktop / web / headless 共用一套 cordis 插件，装在各自 profile 的 `node_modules/agent-purge/`，并在 `cordis.patch.yml` 里 `- insert` 挂上，不改 `app.asar`。装完重启一次，之后热生效；三个形态还能在 Web 面板分别勾选。

## magpie 网关插件（可选）

[magpie](https://github.com/yetone/magpie) 把各家 agent 的请求收进本地网关。挂上这个插件后，**凡是经过网关的请求**（Claude Code、Codex、OpenCode、pi…）的 system 段都按 agent-purge 的当前人设改写——不用逐个 harness 装，换人设也不用重启 magpie。

插件在仓库里，不进 npm 包（`files` 白名单），所以按路径装：

```bash
git clone https://github.com/ZiChuanLan/agent-purge
magpie plugin add /path/to/agent-purge/magpie-plugin     # 按路径装
magpie plu

## 4. [arxiv] Reva: Real-Time Vulnerability Detection through Contextual Probing of Large Language Models
key: arxiv:2610.35829
url: https://arxiv.org/abs/2610.35829
meta: {"published": "2026-10-26", "authors": ["Amine Lbath", "Massih-Reza Amini"], "categories": ["cs.CR", "cs.AI"]}
query: all:"language model" AND all:agent AND all:tool

A vulnerability costs more to fix the later it is discovered. As coding agents generate code faster than developers can review it, software needs a first line of defense screening each new function in real time. LLM agents have recently become capable of finding real-world vulnerabilities by working as a security expert would: they run analysis tools, explore the surrounding code, test hypotheses and weigh the evidence before forming their own judgement. This reasoning, however, spans many model calls, so that each verdict takes minutes of compute, far too long for real-time screening. Faster detectors, which fine-tune deep learning models or prompt an LLM for a direct verdict, are less accurate: they judge a function without the context an agent gathers, and an LLM's generated verdict is unreliable even when given some of it. We present REVA (REal-time Vulnerability Analysis), an AI vulnerability detector that brings the security context and code understanding components behind agentic detectors into a single forward pass of an LLM. For each new function, REVA gives the LLM a pre-computed threat model of its module, lightweight static analysis findings and call-graph information. REVA leverages a trained probe to read the LLM's internal representations of the new function in this context. On PrimeVul's held-out test set, REVA on GLM-5.3-Flash reaches 60.0% accuracy in about one second per function. This matches VulTriage (59.2%), the state-of-the-art agentic detector, run on the same LLM, while being over 250 times faster and less than a tenth as costly. On the same prompt, the probe is 14% to 17% more accurate than the LLM's own direct verdict. Across three open LLMs, REVA is at least as accurate as VulTriage, and about 10% more accurate on two of them. An LLM's internal representations thus encode much of what agentic detectors obtain through reasoning.

## 5. [vault] win rate sold without entry price
key: vault:2026-10-14:win-rate-sold-without-entry-price
url: https://www.instagram.com/reel/DedW0mvh3dw/
meta: {"vault_status": "intel", "kind": "idea", "subject": "@lp_predicts Kalshi copy-wallets reel", "date": "2026-10-14", "where": "TRITON-CORE/Research/links/2026-10-14-lp-predicts-kalshi-copy-wallets-reel.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: buying favourites at 90 cents makes high win rates cheap and can still lose

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (idea) no; Kalshi and Polymarket closed to the UK since the 7 Jul NO-GO, and win rate without entry price means nothing Write-up: `TRITON-CORE/Research/links/2026-10-14-lp-predicts-kalshi-copy-wallets-reel.md` Link: https://www.instagram.com/reel/DedW0mvh3dw/

## 6. [github] huaxialucaicaizi/ai-startup-skills: 创业公司做 AI 产品的 7 步 Agent Skill 合集：验证 → BP → 政策 → 路演 → 获客 → 定价 → 注册。
key: gh:huaxialucaicaizi/ai-startup-skills
url: https://github.com/huaxialucaicaizi/ai-startup-skills
meta: {"stars": 435, "created": "2026-10-22", "pushed": "2026-10-27", "language": "Python", "topics": ["agent-skills", "ai", "business-plan", "claude-code", "codex", "cursor", "entrepreneurship", "growth"]}
query: claude-code created:>{since} stars:>20

# AI Startup Skills · AI 创业 Skill 包

**从验证想法到注册公司，一人公司做 AI 产品的 7 步 Agent Skill，一次装全套。** 
Seven agent skills for building an AI product as a one-person company, from idea validation to registration, in one install.

[](https://github.com/huaxialucaicaizi/ai-startup-skills/actions/workflows/ci.yml)
[](LICENSE)
[](https://github.com/huaxialucaicaizi/ai-startup-skills)
[](https://learn.chatgpt.com/docs/build-skills)

[中文](#zh) | [English](#en)

 

---

  

## 中文

### 目录
- [一句话介绍](#zh-intro)
- [7 步工具包](#zh-steps)
- [它和单独安装有什么不同](#zh-diff)
- [适合 / 不适合](#zh-fit)
- [快速开始](#zh-quickstart)
- [怎么用](#zh-usage)
- [原则](#zh-principles)
- [目录结构](#zh-structure)
- [同步与更新](#zh-sync)
- [常见问题](#zh-faq)
- [贡献与反馈](#zh-contrib)
- [作者](#zh-author)
- [许可](#zh-license)

  
### 一句话介绍

「一人公司工具包」的合集仓库：把 7 个独立的 Agent Skill 打包在一起，再加一个**总入口 skill**。你只要说清楚在做什么、做到哪一步，它会判断你处在创业的哪个阶段，然后调用对应的子 skill。

**痛点**
- 一个人做 AI 产品，验证、写 BP、申请政策、路演、获客、定价、注册，每件事都得自己摸索
- 7 个 skill 分开装太麻烦，也不知道先用哪个
- 每一步的产出（验证证据、BP、定价）需要串起来用，而不是各写各的

  
### 7 步工具包

每一步也是一个可以单独安装的仓库：

| 步骤 | Skill | 解决什么问题 |
|---|---|---|
| 1 | [**AI MVP Validation · AI 产品 MVP 验证**](https://github.com/huaxialucaicaizi/ai-mvp-validation) | 先验证有没有人要，再写代码、写 BP |
| 2 | [**Business Plan Skill · 商业计划书**](https://github.com/huaxialucaicaizi/business-plan-skill) | 写 BP、路演材料、孵化器和大赛申请 |
| 3 | [**OPC Policy Navigator · 一人公司政策导航**](https://github.com/huaxialucaicaizi/opc-policy-navigator) | 查能申请的政策、补贴、算力券、OPC 社区 |
| 4 | [**AI Pitch Coach · 路演教练**](https://github.com/huaxialucaicaizi/ai-pitch-coach) | 园区、孵化器、创业大赛的路演稿和评委问答 |
| 5 | [**OPC Growth Playbook · 一人公司增长获客**](https://github.com/huaxialucaicaizi/opc-growth-playbook) | 小红书、抖音、视频号冷启动获客 |
| 6 | [**OPC Pricing & Sales · 定价与成交**](https://github.com/huaxialucaicaizi/opc-pricing-sales) | 定价、套餐、报价单、私域成交 |
| 7 | [**OPC Registration & Compliance · 一人公司注册与合规**](https://github.com/huaxialucaicaizi/opc-registration-compliance) | 选主体类型、注册清单、年报与合规日历 |

  
### 它和单独安装有什么不同

| 单独安装某一个 skill | 安装 AI 创业 Skill 包 |
|---|---|
| 需要自己判断该用哪个 | 总入口 skill 按阶段帮你选 |
| 每一步的产出各自独立 | 上一步的结果交给下一步用（验证证据 → BP → 政策申请 / 路演） |
| 7 个仓库分别安装、分别更新 | 一次安装，`scripts/sync.sh` 一键同步 |

如果你只需要其中一步，直接装对应的单独仓库就行。

  
### 适合 / 不适合

**适合**
- 在中国做 AI 工具、AI 应用、Agent 的一人公司和早期创业者
- 想按顺序走完"验证 → BP → 政策 → 路演 → 获客 → 定价 → 注册"的人

**不适合**
- 需要正式法律、税务意见：本工具包只提供信息参考，请以官方原文和专业人士意见为准
- 面向 VC 的融资路演：路演教练针对的是园区、孵化器和创业大赛

  
### 快速开始

**1. 安装**

克隆本仓库，把 `skills/` 下的 7 个子 skill 和总入口一起放进你的技能目录。

Codex（用户技能目录 `~/.agents/skills`）：

```bash
git clone https://github.com/huaxialucaicaizi/ai-startup-skills.git
mkdir -p ~/.agents/skills
cp -R ai-startup-skills/skills/* ~/.agents/skills/
cp -R ai-startup-skills ~/.agents/skills/ai-startup-skills
```

Claude Code（用户技能目录 `~/.claude/skills`）：

```bash
git clone https://github.com/huaxialucaicaizi/ai-startup-skills.git
mkdir -p ~/.claude/skills
cp -R ai-startup-skills/skills/* ~/.claude/skills/
cp -R ai-startup-skills ~/.claude/skills/ai-startup-skills
```

其他支持 Agent Skills 的工具（如 Cursor）也可按各自方式安装。规范参考：[OpenAI Codex skills](https://learn.chatgpt.com/docs/build-skills)。

**2. 开始使用**

```text
用 ai-startup-skills 帮我看看我现在在创业的哪一步、下一步该做什么：___（在做什么产品、已经做到哪一步）
```

也可以直接点名某一步，例如：

```text
用 opc-pricing-sales 帮我给这个 AI 产品定价：___
```

  
### 怎么用

1. 说清楚你在做什么、已经做到哪一步
2. 总入口判断阶段，最多问两个问题，然后调用对应的子 skill
3. 每一步完成后，它会告诉你下一步建议做什么、为什么
4. 新创业者的默认顺序：1 → 2 → 3 / 7 → 4 → 5 → 6。第 3 步和第 7 步可以同时做，申请政策前通常要先注册主体

  
### 原则

- **不编数据**：不编造行业平均值、案例和用户评价，示例都会标明虚构
- **只用官方来源**：政策、法规、平台规则附官方原文链接
- **信息参考，不是法律或税务意见**
- **子 skill 的规则优先**：进入某一步后，按那一步的

## 7. [arxiv] Pretraining Knows What, Simulation Teaches How: Compositional Generalization in a Sim-Trained Robot Agent
key: arxiv:2610.35817
url: https://arxiv.org/abs/2610.35817
meta: {"published": "2026-10-26", "authors": ["Benjamin Pikus", "Daniel Saunders", "Mircea Mironenco", "Salman Mohammadi"], "categories": ["cs.RO", "cs.AI", "cs.CV", "cs.LG"]}
query: all:"language model" AND all:agent AND all:tool

A robot policy needs to understand what a task is asking for in a scene, and how to move the robot to accomplish that task. To achieve these two skills, we introduce Zero-real Agent Policy (ZAP), a recipe that teaches a small off-the-shelf vision-language model to control a robot via a simple tool harness. We use a pretrained 27B parameter model to bootstrap world understanding and reasoning, followed by supervised fine-tuning and GRPO on simple simulated tasks to teach it how to move the robot. Without any real-world robot data during training, ZAP reaches 96.7% success on real-world tasks, matching GPT-6 Astra in our harness and outperforming the MolmoAct2 VLA (33.3%), while running 3x faster and 17x cheaper than GPT-6 Astra. We demonstrate that ZAP also generalizes to completely new objects, goals, strategies, and language by seating a test tube in a rack (and choosing a different hole in the rack when prompted), handing a test tube between arms mid-air, drawing an X on a tic-tac-toe board, and playing chess. These goals and types of manipulation don't appear in our training data. Furthermore, ZAP also transfers to an unseen embodiment. On a single-arm Franka, ZAP reaches 55.9% on RoboLab-120, 4.9 percentage points ahead of the leading VLA/WAM baseline.

## 8. [vault] business snapshot prompt as setup
key: vault:2026-10-14:business-snapshot-prompt-as-setup
url: https://resources.getjobber.com/hubfs/content/Home-Service-AI-Starter-Toolkit-by-Jobber.pdf
meta: {"vault_status": "intel", "kind": "tool", "subject": "Jobber Home Service AI Starter Toolkit (free PDF)", "date": "2026-10-14", "where": "TRITON-CORE/Ventures/Neptune-Marketing/social/lead-magnets/ai-for-your-business/research.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: a one-paste profile the AI reads first is the right shape; ours becomes a brief plus a skill

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (tool) Best free AI-for-small-business lead magnet found in a 14 Oct sweep, 7 out of 10: a reusable business-snapshot prompt and a quote prompt, but US dollars, no UK law, no worksheets, no money sums, trades only, and it steers to the vendor's own AI. Beatable with own-number revenue sums, UK rules and a real skill. Write-up: `TRITON-CORE/Ventures/Neptune-Marketing/social/lead-magnets/ai-for-your-business/research.md` Link: https://resources.getjobber.com/hubfs/content/Home-Service-AI-Starter-Toolkit-by-Jobber.pdf

## 9. [github] HenestrosaDev/audiotext: A desktop app to transcribe audio and video from files, URLs, YouTube videos, or your mic, then edit, translate, summarize, subtitle, and chat with your transcripts.
key: gh:henestrosadev/audiotext
url: https://github.com/HenestrosaDev/audiotext
meta: {"stars": 354, "created": "2023-01-31", "pushed": "2026-10-27", "language": "Python", "topics": ["audio-to-text", "customtkinter", "ffmpeg", "python", "speech-recognition", "speech-to-text", "speech-to-text-api", "subtitles-generator"]}
query: youtube transcript pushed:>{since} stars:>20

Audiotext 
   A desktop app to transcribe audio and video from files, URLs, YouTube, or your mic, then edit, translate, summarize, subtitle, and chat with your transcripts. 
   
     
       
     
     
       
     
     
     
       
     
     
       
     
     
       
     
     
     
       
     
     
       
     
     
       
     
   
   
     
       Documentation 
     
    ·
     
      Report Bug
     
    ·
     
      Request Feature
     
    ·
     
      Ask Question
     
   
 

https://github.com/user-attachments/assets/242e9299-b615-4c48-b627-d3ac08b5eb73

 

## Table of Contents

- [About the Project](#about-the-project)
  - [Features](#features)
  - [Documentation](#documentation)
  - [Languages and Formats](#languages-and-formats)
  - [Project Structure](#project-structure)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Setting Up the Project Locally](#setting-up-the-project-locally)
  - [Notes](#notes)
- [Usage](#usage)
  - [Command-Line Interface](#command-line-interface)
- [Troubleshooting](#troubleshooting)
- [Roadmap](#roadmap)
- [Authors](#authors)
- [Contributing](#contributing)
  - [Translations](#translations)
  - [Documentation Website](#documentation-website)
  - [Releasing a Version](#releasing-a-version)
- [Acknowledgments](#acknowledgments)
- [License](#license)
- [Support](#support)

 

## About the Project

**Audiotext** transcribes audio files, videos, YouTube videos, media file links, microphone recordings, and entire folders into any of its 100 supported languages. You can transcribe files with [**WhisperX**](https://github.com/m-bain/whisperX) on your computer, for free and without sending your audio anywhere. Alternatively, you can transcribe files with the [**Whisper API**](https://platform.openai.com/docs/guides/speech-to-text) and the [**Google Speech-to-Text API**](https://cloud.google.com/speech-to-text). You can then play the transcription segment by segment, correct it, translate it, summarize it, and export it.

### Features

- **Any source**: sources can include audio and video files, YouTube videos, direct links to media files, live text transcription of your speech via the microphone, files from a folder (with or without subfolders) excluding those you choose, and a folder that transcribes files added to it even after the app has been restarted.
- **All the files in a folder in one place**: each file is displayed with its status, duration and size, as well as a preview of the text. You can then search, filter and sort the files, transcribe them again with different settings or export several files to a single TXT, Markdown or Word file.
- **Private and offline**: WhisperX can run on your computer's CPU, or much faster on an NVIDIA GPU with CUDA, or on a Mac's Apple Silicon GPU using [MLX Whisper](https://github.com/ml-explore/mlx-examples/tree/main/whisper).
- **Speaker identification**, word-level timings, background noise reduction for quiet speakers and hum, and keywords and context to spell names and terms correctly.
- **Translation while transcribing**, with Whisper, or afterwards with OpenAI, Claude, Gemini, DeepSeek, Mistral, Grok, Ollama, DeepL, or Google Translate.
- **A transcript you can play**: click a subtitle to play it, change the speed, search (and replace) the text, watch videos with their subtitles, rename the speakers, and edit the text while maintaining the timestamps.
- **Summaries** with the k
