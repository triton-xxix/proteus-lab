# Harvest brief, 2026-11-05

14 items shortlisted from 366 candidates (262 dropped as already seen, 9 carry a vault verdict on the vendor).

## 1. [vault] How a copy-trade funnel turns one trade into many testimonials: shared timestamp and prices, lot size the only variable, Day-tab balance shown as wealth
key: vault:2026-10-01:how-a-copy-trade-funnel-turns-one-trade-into-many-testimonia
url: https://t.me/c/2308862086/8413
meta: {"vault_status": "intel", "kind": "scheme", "subject": "The Elio's AI bot (Telegram channel, @elioprivate copy-trading funnel)", "date": "2026-10-01", "where": "TRITON-CORE/Research/links/2026-10-01-elios-ai-bot-telegram.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: Spot the shared timestamp before reading anything else

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) Copy-trading sales funnel, same family as QuantStone. All three member testimonials are the one XAUUSD sell at 10:30 on 1 Oct, a 77 cent move; the profits are lot size (22, 17, 2 lots) and nothing else. 100 percent win rate claim, Myfxbook claim with no link, one percent engagement on 31k subscribers. Do not connect an account. Job: Earn from gold trading without running your own strategy (still open) Write-up: `TRITON-CORE/Research/links/2026-10-01-elios-ai-bot-telegram.md` Link: https://t.me/c/2308862086/8413

## 2. [hn] Ask HN: What's your current AI agentic setup?
key: hn:50366117
url: https://news.ycombinator.com/item?id=50366117
discussion: https://news.ycombinator.com/item?id=50366117
meta: {"points": 479, "comments": 578, "created": "2026-11-04T14:37:22Z"}
query: claude code

I'm curious how people on HN are using AI day to day, and came up with a list of questions I thought could be interesting to know. No need to answer every question of course, just wanted to get a gut feel how people are using AI. 1) What AI subscriptions are you personally paying for? (Claude, ChatGPT/Codex, Cursor, etc) - Which tiers? - Have you purchased multiple subscriptions from the same provider (eg two Claude accounts)? 2) Are you using models outside (or instead) of those subscriptions? For example, pay-as-you-go APIs, OpenRouter, or locally hosted models. - Which models and providers? 3) What coding harnesses and interfaces are you using? Are you sticking with the default CLIs or IDE integrations, or using alternatives like OpenCode, Pi, Aider, Muse Code, or custom-built harnesses? - What made you switch harnesses (if you switched)? 4) Are you using any agent orchestration or swarm tools? - For example, Munder Difflin, Gas Town, Ruflo, or something custom. 5) Are you using broader agent platforms like OpenClaw / Hermes Agent / Grok bot / Dots / Muse? - If you are using them, what are your main use cases? ----- I know my workflow has differed significantly from a year ago, and so it would be interesting to capture a snapshot today of what people are using and why.
comment (thefourthchime): It used to be more interesting and elaborate, switching between different models. I used to use Cursor, then Codex, but since Opus 5.5 came out, I just use the Claude IDE. I got rid of all my skills and just set it to medium. Then I vaguely talk to it about very high-end things that I want, and it comes back with magic. Rinse and repeat. I'd say the biggest trick is just to tell it what complete looks like. Be very specific about what you want it to come back with once it's done. That gives it a good idea what the goal is. It'll automatically create subagents and all that stuff. Although if yo
comment (enjoyyourlife): https://github.com/mkornreich/llm-desktop-electron with OpenRouter. I love Claude but Anthropic is expensive and too restrictive
comment (npc99): Mostly Pi, using a variety of models, but mostly GPT 5.6 line of models. I try to use open weight and cheap models as much as possible.

## 3. [github] KKKKhazix/agent-autoloop: 让你的命令行 Agent 在后台自己接活、自己跟进到底；平时不烦你，遇到拿不准的事才发卡片找你拍板。
key: gh:kkkkhazix/agent-autoloop
url: https://github.com/KKKKhazix/agent-autoloop
meta: {"stars": 3168, "created": "2026-11-03", "pushed": "2026-11-05", "language": "TypeScript", "topics": ["ai-agents", "automation", "claude-code", "cli", "codex", "event-driven", "mcp", "nodejs"]}
query: claude-code created:>{since} stars:>20

# Agent Autoloop

**让你的命令行 Agent 在后台自己接活、自己跟进到底；平时不烦你，遇到拿不准的事才发卡片找你拍板。**

**中文** | [English](README.en.md)

[上手](#上手) · [场景模板](#拿来即用的场景模板) · [插件](#插件体系四个方向都能自由替换) · [内核](#内核的四个机制) · [文档](#更多文档)

## 它解决什么问题？

平时我们用 Claude Code、Codex 这类命令行 Agent，大多是“人守着终端用”：你输一句话，盯着它跑，等它问你下一步；一旦关掉窗口或者人走开，事情就断了。

**Agent Autoloop** 是一个极轻量的自动化中台。它把任务调度做成一个零外部依赖的**内核**，把事件来源、Agent、通知通道，甚至代码上线流水线全部拆成可随时插拔的**插件**。

- **一台电脑、一条命令就能跑。** 装在你的 Mac 或 Linux 上，不用买云服务器，也不用开放公网端口。
- **一行配置接新 Agent。** 不需要 SDK，也不需要改 Agent 源码，能接收提示词并打印最后一条回复的命令行工具都能接。
- **没有后台界面。** 需要你拍板时把卡片推到飞书、钉钉、企微、Slack、Discord 或桌面通知；想看全局进展，敲一行命令。

## 上手

支持 macOS 和 Linux。运行前需要装好 Node 24、Git、curl，以及任意一个你已经登录好的命令行 Agent，不需要 GitHub 账号。也可以直接把[安装说明](INSTALL.md)丢给你的 Agent，让它替你装好。

> **Windows 版：待定。** 很多朋友在问 Windows 版，我都看到了。我现在人在外面出差，手边没有 Windows 电脑，没法真机开发和测试，所以现在还不能在 Windows 上用。这个周末（11 月 7、8 日）回家后，我会把它开发完，做完兼容性测试，再正式推出。进度会更新在 [#17](https://github.com/KKKKhazix/agent-autoloop/issues/17)。等不及的话可以先用 WSL2，注意事项见 [INSTALL](INSTALL.md)。

```bash
curl -fsSL https://raw.githubusercontent.com/KKKKhazix/agent-autoloop/main/install.sh | sh
```

安装和 `agent-autoloop update` 都装最新的 [Release](https://github.com/KKKKhazix/agent-autoloop/releases)，那是通过了全部检查的版本。

装好后用你本机的 Agent 真实走一遍“提问 → 退出等回复 → 拍板 → 接着干完”：

```bash
agent-autoloop try
```

下面是在终端里的真实输出：

```text
事件发出去了，Agent 开始干活……

Agent 结束了这一轮，问了你一个问题。它现在不占进程、不花 Token。

【等你决定】#1 试跑：选一个颜色
这是一次试跑，选哪个都行。
  1. 蓝色
  2. 绿色
回答：agent-autoloop answer 1  
答完运行 agent-autoloop status，能看到它接着把活干完。
```

交互终端里直接输入数字回车；非交互终端运行 `agent-autoloop answer 1 2` 选择“绿色”。再跑 `agent-autoloop status`，就能看到它接上刚才的会话并显示“你选了绿色，试跑通过”，还有今天和最近 7 天的轮数、Token 和费用（[统计口径](skills/agent-autoloop/SKILL.md#看情况回答)）。

## 一件事怎么转起来

编号和上面的架构图一一对应：

1. **新事件进来。** 早上 9 点的定时任务、GitHub 上新提的 Issue、业务系统报的错，都变成一条标准事件送进内核。
2. **按规则派活。** 内核照你写的规则，决定交给哪个 Agent、去哪个目录干。同一件事排队时又来的消息，会合并成一轮处理。
3. **干完一轮就退出。** Agent 把结果写在最后一条回复里，进程直接退出。
4. **拿不准才问你。** 碰到删数据、重启服务、花钱、对外发消息这类事，内核通过飞书或桌面通知发一张卡片给你。等你回复期间，它不占后台进程，也不消耗 Token。
5. **点一下，接着干。** 你选完，它接上原来的对话，把剩下的活干完。

能自己搞定的事走图上方的自动闭环：直接办完，或者约个时间（比如半小时后）再醒来复查，全程不打扰你。

## 日常怎么配？

### 写一份规则（`rules.json`）

不需要写胶水代码。打开 `~/.agent-autoloop/rules.json`，在 `rules` 里写清楚**什么事、交给谁、在哪个目录干**。`to` 填 `agents` 里已有的名字。比如每天早上 9 点写早报：

```json
{
  "name": "早报",
  "when": { "cron": "0 9 * * *" },
  "to": "codex",
  "cwd": "~/notes",
  "prompt": "整理昨天的笔记和提交，写今天的早报。"
}
```

外部事件写法一样，只是要先接好来源。比如有人提新 Issue 时交给 Codex，先按[说明](skills/agent-autoloop/SKILL.md#接一个事件插件)在 `sources` 里登记 `github`：

```json
{
  "name": "处理 issue",
  "when": { "source": "github", "types": ["issues.opened"] },
  "to": "codex",
  "cwd": "~/code/app",
  "skill": "handle-issue",
  "parallel": 3
}
```

保存后几秒内自动生效，可以运行 `agent-autoloop check` 检查；`agent-autoloop rules explain` 看生效的规则和下次定时，`agent-autoloop emit   --dry-run` 预演一条事件会派给谁（不连接中台、不写日志）。就算改错了，或者文件被删、读不到，系统也会继续按旧规则跑，并发卡片提醒你。

### Agent 怎么跟中台配合？

中台对 Agent 只有一个约定：**在最后一条回复里交代结果**。事情办完了，正常输出一句结论就行。需要向你请示时，在回复末尾附一段 `agent-autoloop` 代码块：

````text
订单已经核对完毕，库存充足。

```agent-autoloop
{
  "ask": [{
    "title": "怎么发货？",
    "text": "两种方式今天都能发出。",
    "options": ["快递", "自提"],
    "key": "shipping"
  }]
}
```
````

除了提问（`ask`），还能发通知（`notice`）、关闭已解决的卡片（`resolve`）、预约复查（`later`）和触发新事件（`events`）。通告不需要回答，但结案时可以顺手写一句处理说明，这句话会留在卡片上；只是告诉一声的通告标成 `fyi`，不带按钮。万一 JSON 写错了，中台只让它在原会话里重写最后这段回复，不会把已经干完的业务重做一遍；重写也失败时，保留原结论并通知你回执没有生效（通用命令没有会话，直接走这一步）。接着旧会话跑也一样：会话接不上才开新的；接上了、干到一半断了，就算没跑成，过几分钟回到原会话重试，不开新会话重做。同一事项的新事件默认开新会话；规则写 `"resume": true` 就接着上一轮的会话。

## 拿来即用的场景模板

每套模板都带规则、任务 Skill 和启用说明。

| 想做什么 | 已经封装好的流程 |
|---|---|
| [每日早报](ex

## 4. [arxiv] Rethinking Access Control for AI Agents: Recent Advances and Open Challenges
key: arxiv:2611.06764
url: https://arxiv.org/abs/2611.06764
meta: {"published": "2026-11-04", "authors": ["Chijin Zhou", "Quan Zhang"], "categories": ["cs.SE"]}
query: all:"language model" AND all:agent AND all:tool

Large language model agents access data, invoke tools, and act on users' behalf. Keeping these actions within authorized bounds is challenging because agents choose their own execution paths while permissions and operating conditions may change. This paper surveys recent advances in agent access control across four areas: policy specification and derivation, identity and delegation, action and resource enforcement, and information flow control. We compare their control objects, enforcement boundaries, and assumptions to examine what individual mechanisms achieve and how they can work together. Building on this analysis, we rethink four aspects of authorization: plan selection shapes permission requirements; contextual information can inform decisions without itself granting authority; restrictions must retain their meaning across system interfaces; and authorization must be reassessed as workflows evolve. These insights motivate open challenges and future directions, together with concrete research questions and evaluation criteria. In particular, evaluation should examine both observed agent behavior and the unauthorized effects that remain enabled. Our analysis connects existing mechanisms to the requirements for preserving authorization throughout an agent workflow.

## 5. [youtube] LEVY EXPOSES LICHESS
key: yt:rFxRGGHKp4g
url: https://www.youtube.com/watch?v=rFxRGGHKp4g
meta: {"channel": "jesgluckner", "rank": 1, "duration_min": 0}
query: lichess bot python engine

# LEVY EXPOSES LICHESS
# jesgluckner
# https://www.youtube.com/watch?v=rFxRGGHKp4g

[00:00] why don't I use leeches I don't support communism Bishop to E4 that's a joke I know you were gonna type something YouTube commenters relax twitch I know twitch twitch gets me I understand twitch

## 6. [vault] Character consistency, AI ads and cloning phases feed the WF-0201 avatar engine bake-off
key: vault:2026-09-29:character-consistency-ai-ads-and-cloning-phases-feed-the-wf-
url: 
meta: {"vault_status": "intel", "kind": "service", "subject": "AI Video Bootcamp (Skool, Daniel Riley), $9/month AI video course", "date": "2026-09-29", "where": "TRITON-CORE/Research/links/2026-09-29-ai-video-bootcamp-skool.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: (none)

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Worth one month at 9 dollars: 28.6k members, organic Trustpilot 4.8 from 82 uninvited reviews, active founder, nine phases with character consistency, AI ads and cloning that map onto the avatar content engine bake-off. Beginner to intermediate depth (both critical reviews say YouTube-free level), no live calls at base price, and the affiliate reviews' price-rise-at-26,700 claim never happened. Join, extract the classroom, cancel before month two.

## 7. [hn] Tell HN: Gemini trains on chat history, even for subscribers (personal accounts)
key: hn:50363461
url: https://news.ycombinator.com/item?id=50363461
discussion: https://news.ycombinator.com/item?id=50363461
meta: {"points": 689, "comments": 181, "created": "2026-11-04T10:10:27Z"}
query: car data

If you have a personal Google AI subscription, all your saved chat history in Gemini can be used for training and there is no way to opt out unless you turn off chat history or use temporary chat sessions. These chat transcripts may even be read by human reviewers. Although Google claims to disconnect them from your account when human-reviewed, they explicitly warn not to enter confidential information . https://support.google.com/gemini/answer/16836988 “[Gemini app activity] is used to improve Google services for everyone, including by training generative AI models, if your Keep Activity setting is on.“ https://support.google.com/gemini/answer/13594961?hl=en#human_review “A subset of chats are reviewed by human reviewers” https://support.google.com/gemini/answer/13594961?hl=en#pn_retain_data “Chats reviewed by human reviewers [...] are not deleted when you delete your activity. Instead, they are retained for up to three years.” https://support.google.com/gemini/answer/13594961?hl=en#pn_data_usage “Please don’t enter confidential information that you wouldn’t want a reviewer to see or Google to use to improve our services, including machine-learning technologies.” To disable their training on your chat sessions, you need to turn off “Keep Activity” in Gemini’s settings. Turning that off means you’ll lose any chat sessions after 72 hours. I learned this too late, thinking that having a paid subscription = not being turned into the product. Apparently paying is not enough. Than
comment (r_lee): another Google W I guess? gemini really leading the pack over here
comment (icantevenhold): I assume that everyone does this no matter what they say. Seems like too juicy a target
comment (233mhz): imho you should act as if everything you type, not even send, is stored forever and might be used for training whenever they decide to retro actively change their TOS, no matter how much money you pay

## 8. [github] mhfed/vn-law-check: Audit pháp lý website theo luật Việt Nam (BVDLCN 91/2025, TMĐT 122/2025, ANM 116/2025, AI 134/2025) cho Claude Code, Cursor, Copilot, Windsurf, Cline
key: gh:mhfed/vn-law-check
url: https://github.com/mhfed/vn-law-check
meta: {"stars": 437, "created": "2026-11-02", "pushed": "2026-11-05", "language": "Shell", "topics": ["agent-md", "agent-skills", "claude-code", "claude-plugin", "claude-skills", "compliance", "copilot-instructions", "cursor-rules"]}
query: claude-code created:>{since} stars:>20
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# vn-law-check

Open-source compliance audit for Vietnamese websites and apps. Bảo AI coding agent rà soát các rủi ro pháp lý theo luật Việt Nam và gợi ý chỗ cần sửa trước khi ra mắt.

Dùng cho Claude Code, Cursor, Copilot, Windsurf, Cline, Codex. Hỗ trợ cả website lẫn mobile app.

## Nó giúp gì?

Nếu website hoặc app của bạn có một trong các dấu hiệu sau thì nên check ngay:

- form thu thập email, số điện thoại, họ tên
- Google Analytics, Meta Pixel, TikTok Pixel, ads SDK
- đăng nhập, giỏ hàng, thanh toán, đặt lịch
- chatbot AI hoặc tool AI trên frontend
- cookie banner, privacy policy, consent flow
- nội dung quảng cáo, chính sách hoàn tiền, điều khoản sử dụng

Từ 01/01/2026, Luật Bảo vệ dữ liệu cá nhân 91/2025 yêu cầu rõ ràng hơn về mục đích thu thập, đồng ý, lưu trữ và chia sẻ dữ liệu. Nhiều doanh nghiệp nhỏ và startup đang phát triển nhanh nhưng bỏ qua các điểm này. Repo này giúp bắt lỗi sớm trước khi bị phạt hoặc bị khách phản hồi.

Bạn không cần đọc luật từ đầu. Chỉ cần cho AI biết project hoặc URL, nó sẽ phân loại site, rà soát các checklist dựa trên luật Việt Nam và trả về báo cáo có mức ưu tiên: 🔴 cần sửa ngay, 🟡 nên cải thiện, 🟢 đạt, ⚪ không áp dụng.

## Vì sao repo này có giá trị?

- Tập trung vào luật Việt Nam, hiện đang có rất ít tool open-source theo đúng quy định mới nhất.
- Dành cho đội dev và AI agent: bạn không cần đọc luật dài, chỉ cần “audit pháp lý website này”.
- Có thể dùng từ giai đoạn xây dựng sản phẩm, không cần chờ legal team review toàn bộ.
- Cung cấp nguồn tham chiếu, checklist và tài liệu để kiểm tra lại.

## Kết quả trông như thế nào?

Trích từ [báo cáo trên site demo](demo/report.md), một shop cà phê giả lập:

> **🔴 Coi việc "tiếp tục sử dụng website" là đồng ý**
> - `chinh-sach-bao-mat.html:12`: "Bằng việc tiếp tục sử dụng website, bạn được xem là đã đồng ý..."
> - Căn cứ: Điều 9 khoản 4 điểm d Luật 91/2025/QH15: im lặng hoặc không phản hồi không được coi là đồng ý.
> - Đề xuất: bỏ câu này, xin đồng ý rõ ràng tại đúng chỗ thu thập dữ liệu.

Mỗi lỗi được xếp mức: 🔴 cần xử lý ngay, 🟡 nên cải thiện, 🟢 đạt, ⚪ không áp dụng. Blog hay trang tĩnh không thu thập gì thì chỉ nhận về 1 dòng nhắn ngắn; nhưng site bán hàng, có login, tracking hoặc AI chatbot thì báo cáo sẽ dài và chi tiết hơn.

## Dùng thế nào?

**Bước 1: cài.** Chọn theo tool bạn đang dùng.

Claude Code (gõ trong Claude Code, không phải terminal):

```
/plugin marketplace add mhfed/vn-law-check
/plugin install vn-law-check
```

Cursor, Windsurf, Copilot, Cline, Codex (chạy trong thư mục project):

```bash
curl -fsSL https://raw.githubusercontent.com/mhfed/vn-law-check/main/install.sh | bash
```

 
 Cách cài khác 

Clone thẳng vào thư mục skills của Claude, không qua marketplace:

```bash
git clone --depth=1 https://github.com/mhfed/vn-law-check ~/.claude/skills/vn-law-check
```

Muốn cài riêng cho 1 project thì đổi `~/.claude/skills/` thành `.claude/skills/` trong project đó.

`install.sh` cài checklist vào `.vn-law-check/` và không ghi đè file nào của bạn. Nếu project đã có `AGENTS.md`, `CLAUDE.md`... thì script chỉ chèn thêm một đoạn ngắn tóm tắt để AI biết cách dùng toolkit.
 

**Bước 2: bảo AI kiểm tra.** Mở project rồi gõ:

```
audit pháp lý website này theo luật Việt Nam
```

Không có source code, chỉ có địa chỉ website cũng được:

```
audit pháp lý https://ten-mien-cua-ban.vn
```

**Bước 3: sửa.** Đọc báo cáo, rồi bảo tiếp: "sửa giúp các mục 🔴".

Chưa có chính sách bảo mật, hoặc có mà copy từ đâu đó? Bảo tiếp:

```
soạn chính sách bảo mật ch

## 9. [arxiv] SecureGARD: Dynamic Ontology-Guided Governance for Secure Tool-Using LLM Agents
key: arxiv:2611.06682
url: https://arxiv.org/abs/2611.06682
meta: {"published": "2026-11-04", "authors": ["Guoqin Xiong", "Shengtao Wen", "Xiang Chen", "Xinyi Zeng"], "categories": ["cs.LG"]}
query: all:"language model" AND all:agent AND all:tool

Tool-using large language model (LLM) agents translate model outputs into consequential actions, turning indirect prompt injection into an execution-security problem. Existing defenses constrain tool calls, trajectories, or information flows, but often leave action semantics, state dependencies, and evidence relations implicit, limiting generalization across heterogeneous tools and complicating safe updates. We present \ours{}, a dynamic ontology-guided governance framework. \ours{} grounds heterogeneous calls in a shared semantic representation and combines an executable ontology with episode-level task state to derive deterministic ready, waiting, and forbidden decisions. A waiting decision identifies an unmet but recoverable obligation, enabling bounded replanning without expanding the agent's authorization boundary. \ours{} evolves its ontology offline from verified training executions. An offline LLM proposes instance-independent action--state axioms, which are accepted only if they address ontology errors exposed by training failures, preserve logical consistency and protected entailments, and pass held-out validation before the ontology is frozen. We evaluate \ours{} on AgentDojo, ASB, and AgentDyn under benign and indirect prompt-injection settings. \ours{} achieves a 0\% attack success rate (ASR) across all three benchmarks while improving task utility under attack compared with existing baselines. These results show that explicit semantic governance can strengthen execution security without indiscriminate blocking.

## 10. [youtube] We analysed millions of MOT results #MOT #CarsOfTikTok #UKCars #DataJournalism #caranalytics
key: yt:zeTGescbQak
url: https://www.youtube.com/watch?v=zeTGescbQak
meta: {"channel": "datatells", "rank": 1, "duration_min": 0}
query: MOT data analysis uk

# We analysed millions of MOT results #MOT #CarsOfTikTok #UKCars #DataJournalism #caranalytics
# datatells
# https://www.youtube.com/watch?v=zeTGescbQak

[00:00] A Vauxhall Corsa fails its MOT almost 60% more often than a BMW 3 Series. We checked all 30 million car MOTs from last year and more than 8 million failed. Every model is compared with cars of the same age, mileage, and fuel. Across Britain's 10 most MOT tested cars, those two are the extremes, 22% below average and 23 above. Among small SUVs, a Dacia Duster fails more than twice as often as a Volkswagen T-Roc. When a Clio or a Corsa fails, it's about
[00:32] two and a half times as likely as a similar car to have a steering fault. For its age and mileage, the Bentley Continental fails least of any model at a third of the usual rate.

## 11. [vault] A cheap starter kit used as a qualifier that routes buyers to a private sales call
key: vault:2026-09-27:a-cheap-starter-kit-used-as-a-qualifier-that-routes-buyers-t
url: 
meta: {"vault_status": "intel", "kind": "scheme", "subject": "AI Clipping Agency starter kit (Musa Mustafa, Media Metas / Crayo Inc)", "date": "2026-09-27", "where": "TRITON-CORE/Research/links/2026-09-27-natejbiz-retainer-and-crayo-starter-kit.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: The 5 dollar price puts a card on file; the real offer lands on the one-to-one, and the guarantee covers budget allocation, not earnings

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (scheme) Real operator and real tool: Musa Mustafa co-founded crayo.ai (3.2m users), company Media Metas / Crayo Inc, San Jose. But the 5 dollar price, down from 12.50, is a qualifier not a product: it puts a card on file and routes to a private one-to-one with an agency owner, which is where the real offer lands. What it actually sells is the commodity half, Content Rewards pay-per-view clipping, which is the volume game natejbiz explicitly warns against, plus a media-buying commission angle (20 percent of a 100k brand budget). The money worth having in this category is the flat monthly editing retainer, two to six thousand a month, which we can already deliver with no purchase. Income claims (3k first week, 3,801 in 13 days, 4,251 with zero experience) are unevidenced, and the 48-hour guarantee covers budget allocation, not earnings. Job: Sell post-production as a monthly retainer, priced, to businesses that already produce content (still open)

## 12. [hn] Qualcomm Cloud AI 100 Ultra – 150W AI Accelerator Card with 128GB at 548GB/s
key: hn:50370654
url: https://www.qualcomm.com/data-center/products/cloud-ai-100-ultra
discussion: https://news.ycombinator.com/item?id=50370654
meta: {"points": 167, "comments": 62, "created": "2026-11-04T19:55:14Z"}
query: car data

comment (pearl_panel5): Curious how the memory bandwidth actually holds up under sustained inference loads compared to the spec sheet numbers.
comment (varispeed): Aren't these specs already outdated? Seems meh. I would think players would like to bring something new to the table instead of bringing what was okay two years ago or so. Give me 1TB RAM and 5TB/s or something that exciting.
comment (aetherspawn): Ok so it’s significantly worse than Apple M6 and we don’t know if it’s cheaper or not Edit: Ah sorry you’re right, the bandwidth is lower but the TOPS is a lot higher. I’m not sure how much effect you get from higher TOPS with such low bandwidth though.

## 13. [github] KIRVO-REPORTING/video-to-notes: Local-first video-to-notes CLI for YouTube/Bilibili transcripts, Whisper fallback, timestamped AI summaries, and Notion/Obsidian export.
key: gh:kirvo-reporting/video-to-notes
url: https://github.com/KIRVO-REPORTING/video-to-notes
meta: {"stars": 113, "created": "2026-07-03", "pushed": "2026-11-02", "language": "Python", "topics": ["ai-notes", "ai-summary", "bilibili", "cli", "codex-skill", "knowledge-base", "local-first", "local-whisper"]}
query: youtube transcript pushed:>{since} stars:>20

# video-to-notes — Turn YouTube and Bilibili videos into timestamped notes

An open-source, local-first CLI and Codex skill that converts YouTube, Bilibili, TED, and other `yt-dlp`-supported video links into transcripts, grounded AI summaries, searchable HTML reports, and optional Notion or Obsidian knowledge-base entries.

Caption first. Local Whisper when needed. Clickable timestamps back to the source. Your workspace remains the source of truth.

- [Product website and video demos](https://kirvo-reporting.github.io/video-to-notes/)
- [中文说明](#中文说明)
- [English documentation](#english)

## 中文说明

### 这个项目是做什么的

`video-to-notes` 是一个面向 AI Coding Agent 和命令行用户的视频资料整理工具。它会优先下载视频自带字幕，在没有合适字幕时才使用本地 Whisper 转写，并把每个视频整理成可追溯的本地报告。

https://github.com/user-attachments/assets/3605df08-c558-4060-ae46-48d93420736c

 
   项目主页与中文视频 
  ·
   直接下载 MP4 
 

这个仓库包含两部分：

- `video-to-notes`: Python CLI，负责环境检测、用户配置、字幕下载、本地 Whisper fallback、报告生成、Notion/Obsidian 发布和本地 dashboard。
- `codex-skill`: Codex 技能说明，让 Codex 知道如何调用 `video-to-notes`、读取转写文本、写出有时间戳依据的摘要报告。

兼容说明：旧命令 `ytlt` 仍保留为别名；公开文档和安装流程统一使用 `video-to-notes`。

### 要解决的问题

长视频、课程、访谈、发布会和研究材料通常有几个麻烦：

- 字幕、转写、摘要和来源链接分散，后续很难复查。
- 很多视频其实有字幕，不需要一上来就跑本地 Whisper。
- AI 摘要如果没有绑定原始 transcript 和时间戳，可信度和可追溯性很弱。
- 处理过的视频缺少统一索引，时间久了很难找到以前的报告。

这个项目把流程固定下来：字幕优先，本地转写作为兜底，所有结果落到本地 workspace，并生成可搜索的 HTML dashboard。用户也可以把最终报告同步到 Notion 或 Obsidian。

### 实际 Notion 示例

[查看公开视频笔记数据库](https://equal-colby-a69.notion.site/edff5673d33e412da6c00721d97cebca?v=39c2cd5ac3058131b4cf000c0b03307d)，其中包含 YouTube 与 Bilibili 视频、不同转写来源、中文摘要、关键观点和完整原文转写。点击下方截图可直接打开示例数据库。

[](https://equal-colby-a69.notion.site/edff5673d33e412da6c00721d97cebca?v=39c2cd5ac3058131b4cf000c0b03307d)

### 复制给 Codex 或 Claude Code 的一行配置指令

把下面这一行复制给 Codex 或 Claude Code，它就可以按这个项目的方式安装和配置：

```text
请安装并配置 video-to-notes：克隆 https://github.com/KIRVO-REPORTING/video-to-notes，进入仓库后在 macOS/Linux 运行 ./install.sh，Windows PowerShell 运行 powershell -ExecutionPolicy Bypass -File .\install.ps1；安装器会寻找或通过 uv 准备 Python 3.10+，安装 yt-dlp EJS，检查 Deno 2.3+ 或 Node.js 22+ 与 ffmpeg，并在检测到 Codex 时安装 codex-skill；然后运行 video-to-notes configure，让用户选择常用语言、硬件推荐的 Whisper fallback 模型或不安装模型，以及默认输出环境 local/notion/obsidian；非交互模式选择模型时必须加 --execute；最后用 video-to-notes process "VIDEO_URL" 处理视频。
```

### 工作流程简介

1. 用户给出一个视频 URL。
2. `video-to-notes process "VIDEO_URL"` 调用 `yt-dlp` 获取元数据和字幕。
3. 工具优先使用人工字幕或自动字幕；字幕不可用时，才走本地 Whisper。
4. 每个视频会生成独立目录，包含 `metadata.json`、`transcript.txt` 和 `report.html`。
5. Codex 或其他 Agent 读取完整 `transcript.txt`，写入有依据的 `summary.md`，并把 3-8 个内容主题标签写入 `tags.json`。标签不包含平台、来源或工作流属性。
6. `video-to-notes finalize " "` 把过滤后的主题标签写入本地 HTML 报告和 dashboard 索引，清理下载的视频文件，并刷新 dashboard。
7. 根据配置或命令参数，把报告保留在本地 dashboard，或发布/更新到 Notion、Obsidian。

### 快速安装

推荐使用仓库自带的 bootstrap 脚本。它会寻找 Python 3.10+，并在检测到 `uv` 时自动准备 Python 3.12；随后检查 pip/venv，创建 `.venv`，安装 yt-dlp EJS，验证 Deno 2.3+ 或 Node.js 22+ 与 ffmpeg，并提示是否启动 `video-to-notes configure`。检测到 `CODEX_HOME` 或 `~/.codex` 时，它也会同步安装 Codex skill。

macOS / Linux:

```bash
git clone https://github.com/KIRVO-REPORTING/video-to-notes.git
cd video-to-notes
./install.sh
```

Windows PowerShell:

```powershell
git clone https://github.com/KIRVO-REPORTING/video-to-notes.git
cd video-to-notes
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

如果安装脚本没有自动启动配置，手动运行：

```bash
video-to-notes doctor
video-to-notes configure
```

配置会让用户选择三件事：

1. 常用语言，例如 `zh`、`en`、`ja`。
2. 本地 Whisper fallback 模型。默认推荐项会根据当前硬件选择；也可以选择 `none` 不安装模型，但不推荐，因为无字幕视频将无法本地转写。
3. 默认输出环境：`local`、`notion` 或 `

## 14. [youtube] 29000 Elo Bot Told Levy Resign 😭
key: yt:CSn6EXM43gg
url: https://www.youtube.com/watch?v=CSn6EXM43gg
meta: {"channel": "Premove Clips", "rank": 2, "duration_min": 0}
query: lichess bot python engine

# 29000 Elo Bot Told Levy Resign 😭
# Premove Clips
# https://www.youtube.com/watch?v=CSn6EXM43gg

[00:00] The bot, literally, the last message you wrote was >> Care to resign. Let's see if you will actually be able to take it. Oh my god. >> It literally just said, "Let's see if you're actually going to be able to >> Yo. >> Terrifying. >> Oh my goodness. >> Absolutely terrifying stuff. >> I'm going to I'm going to sack my rook for defense. >> [music] >> I'm sacking my rook for Oh, there is no defense here. >> There's a fine line between skill and luck. >> Shut up, man.
