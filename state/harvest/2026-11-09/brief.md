# Harvest brief, 2026-11-09

14 items shortlisted from 377 candidates (289 dropped as already seen, 11 carry a vault verdict on the vendor).

## 1. [vault] testimonial-first hook with one number
key: vault:2026-11-09:testimonial-first-hook-with-one-number
url: https://www.instagram.com/p/DfZo4rOsFRL/
meta: {"vault_status": "open", "kind": "service", "subject": "Sales Circle webinar testimonial ad (Instagram)", "date": "2026-11-09", "where": "TRITON-CORE/Research/links/2026-11-09-sales-circle-webinar-ad.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: one client result as the opener; fits Neptune ads

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Funnel mechanics worth studying; the programme itself is not for us Write-up: `TRITON-CORE/Research/links/2026-11-09-sales-circle-webinar-ad.md` Link: https://www.instagram.com/p/DfZo4rOsFRL/

## 2. [hn] Claude Fable 5.2 Scores 65 on Artificial Analysis, Highest So Far
key: hn:50431144
url: https://artificialanalysis.ai/models/claude-fable-5-2
discussion: https://news.ycombinator.com/item?id=50431144
meta: {"points": 228, "comments": 143, "created": "2026-11-09T20:04:55Z"}
query: claude code

page: Claude Fable 5.2 (max) - Intelligence, Performance & Price Analysis | Artificial Analysis Artificial Analysis K Anthropic • Claude Fable 5.2 max • Proprietary model • Released November 2026 Claude Fable 5.2 (Max, Default Fallback) Intelligence, Performance & Price Analysis Compare Try it out API Provider Benchmarks Model summary Intelligence Updated # 1 / 74 65 Artificial Analysis Intelligence Index 4 out of 4 units for Intelligence. Performance # 72 / 73 Time to first answer token 231.55s Output speed 103 tok/s 44.1 Time per Intelligence Index task (minutes) 4 out of 4 units for Performance. Cost # 73 / 73 In $8.00 Out $40.00 Cache discount 98% $26.54 Cost per Intelligence Index task 4 out of 4 units for Cost. Verbosity # 72 / 73 Input tokens 28.3B Output/input 0.97% 275M Output tokens from Intelligence Index 4 out of 4 units for Verbosity. Comparison Summary Claude Fable 5.2 (Max, Default Fallback) is amongst the leading models in intelligence, but particularly expensive when comparing to other models of similar price. It's also notably slow per task and very verbose. The model supports text and image input, outputs text, and has a 1M tokens context window. Claude Fable 5.2 (Max, Default Fallback) scores 65 on the Artificial Analysis Intelligence Index, placing it well above average among comparable models (median: 40). When evaluating the Intelligence Index, it generated 275M tokens, which is very verbose in comparison to the median of 72.8M. Pricing for Claude Fable 5.2 (Max, Default Fallback) is $8.00 per 1M input tokens (expensive, median: $2.00) and $40.00 per 1M output tokens (expensive, median: $10.00). On average, it costs $26.54 per task to evaluate Claude Fable 5.2 (Max, Default Fallback) on the Intelligence Index. At 44.1 minutes per Intelligence Index task, Claude Fable 5.2 (Max, Default Fallback) is notably slow compared with the median of 12.9 minutes for comparable models (lower is better). Technical specifications Reasoning Yes This page shows the 
comment (qntty): Crazy how quick these are coming out now
comment (suddenlybananas): Why is it so much more expensive?
comment (A_D_E_P_T): Google could have been #1 for a little while, but they botched their release and squandered their temporary lead. (As usual.) If I worked there, I'd be so pissed.

## 3. [github] drost-ai/tinker-ai-skill: Agent Skill for fine-tuning an agentic model on your own Claude Code sessions with Tinker. Works in Claude Code, Codex and OpenCode.
key: gh:drost-ai/tinker-ai-skill
url: https://github.com/drost-ai/tinker-ai-skill
meta: {"stars": 289, "created": "2026-11-07", "pushed": "2026-11-07", "language": "Python", "topics": []}
query: claude-code created:>{since} stars:>20
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# tinker-ai-skill

**Turn your own coding-agent sessions into a fine-tuned model you can run locally. This is the recipe behind Tess-4 and Tess-4.5.**

[](LICENSE)
[](https://agentskills.io)
[](#install-the-skill)
[](https://thinkingmachines.ai/tinker)

Every session you run with a coding agent is a worked example of how you want a
model to behave: your repositories, your conventions, your tools, your way of
debugging. This skill hands your agent the complete, production-tested pipeline to
turn those sessions into a supervised fine-tuning dataset, train a LoRA on
[Tinker](https://thinkingmachines.ai/tinker), merge it, and ship a GGUF that runs in
llama.cpp on your own machine. One afternoon, a few dollars to a few hundred, and a
model that works the way you do.

Install it once and say: *"fine-tune Qwen3.6-35B-A3B on my Claude Code sessions from
the last three months."* The agent takes it from there and stops before anything
that costs money.

## Proven on real releases

We built the Tess family of agentic coding models from our own Claude Code sessions
with exactly this method, and shipped them as open weights on Hugging Face:
[Tess-4-27B](https://huggingface.co/migtissera/Tess-4-27B)
([GGUF](https://huggingface.co/migtissera/Tess-4-27B-GGUF),
[EAGLE-3 draft](https://huggingface.co/migtissera/Tess-4-27B-EAGLE3)) and
[Tess-4.5-27B](https://huggingface.co/migtissera/Tess-4.5-27B)
([GGUF](https://huggingface.co/migtissera/Tess-4.5-27B-GGUF)). Read about them at
[continuityresearch.ai/tess-4-5](https://continuityresearch.ai/tess-4-5).

What is in this repository is the distilled, cleaned-up version of the pipeline that
produced them, from raw transcripts to a quantized GGUF, including the mistakes we
made so you do not have to.

## What you get

- **One `SKILL.md`** your agent follows: a nine-step workflow with the decision
  points spelled out and the rules that cost us runs.
- **Eleven small scripts**, plain Python and shell on top of tinker-cookbook and
  llama.cpp, each with an offline default and a `--help` that explains every flag.
- **Six reference notes**: the transcript format, the anonymization policy, the
  chunking and compaction design, Tinker training settings with the learning-rate
  evidence, export and serving, and the lessons learned.
- **A synthetic transcript generator** so you can dry-run the whole pipeline in
  five minutes without touching real data or spending a cent.

## The method, from transcripts to a local model

| Step | What happens | Script |
|---|---|---|
| 1. Collect | Copy Claude Code transcripts verbatim, with checksums; skip subagents and tiny sessions; exclude whole projects that must stay private | `collect_sessions.py` |
| 2. Clean | Normalize to OpenAI-style messages; drop harness noise; replace every credential by value; give each session its own random identity for usernames, folders, names, emails, orgs; fail if anything leaks | `normalize_sessions.py`, `anonymize_sessions.py` |
| 3. Slice | Cut sessions to the model's context length, measured with the model's real renderer, never splitting a tool call from its result | `build_dataset.py` |
| 4. Compact | Give every slice after the first a deterministic working-context block and a continuation bridge, the way a real harness compacts | `build_dataset.py` |
| 5. Split | Hold out whole sessions with a seeded hash so rebuilds and other models compare | `build_dataset.py` |
| 6. Train | LoRA on Tinker with the cookbook trainer, tool definitions on eve

## 4. [arxiv] Tracybot: Preserving Developer Intent by Tracing Agent-Generated Code to Prompts
key: arxiv:2611.09395
url: https://arxiv.org/abs/2611.09395
meta: {"published": "2026-11-06", "authors": ["Răzvan Albu", "Aliaksei Khval", "Maxine Orlova", "Danis Music"], "categories": ["cs.SE", "cs.HC"]}
query: all:"language model" AND all:agent AND all:tool

Large language models (LLMs) are now widely used in software development, and LLM-based coding agents are given increasing autonomy. With coding agents, many design decisions are made in the conversation between the developer and the agent. Typically, the developer starts a conversation with an agent and states their intent, the agent proposes options if needed, and the developer plans the change accordingly. Then, the resulting code is committed. However, in such scenarios, the decisions and the intent behind the changes remain in the conversation, with no link to the code they produced. In this paper, we present Tracybot, an open-source tool that integrates with VS Code, Git, and coding agents to keep track of relevant conversations in an LLM-assisted development process. Tracybot captures each change as a Tasklet which consists of optional planning prompts used to plan a change, together with a build prompt that produces it. Tracybot has two main features: (i) it maps line-level code changes made by coding agents to the Tasklets that produced them, and (ii) it allows the developer to export a Tasklet as a decision record when needed, for example when the decision concerns the architecture of the project. We developed the tool over two iterations of a design science study, while focusing the evaluation on the usability and user-friendliness of the tool. In a focus group (7 participants) and a survey (24 participants), we found that Tracybot was perceived as useful for activities like code review, and most participants found our Tasklet design and presentation to be a clear way to represent the developer's intent. Tool: https://github.com/TracyTeam/tracybot. Video: https://youtu.be/Vg_a1F5eO04.

## 5. [youtube] This Chess AI Predicts Your Mistakes
key: yt:8uKW6cIusLA
url: https://www.youtube.com/watch?v=8uKW6cIusLA
meta: {"channel": "EmmaChess", "rank": 2, "duration_min": 0}
query: lichess bot python engine

# This Chess AI Predicts Your Mistakes
# EmmaChess
# https://www.youtube.com/watch?v=8uKW6cIusLA

[00:00] This chess AI isn't trying to find the best move. It's trying to predict what a human will play. It's called Maya 3. Imagine a player is about to make a mistake. Maya predicts that move. Then the player actually plays it. The move was bad, but the prediction was right. That's the whole idea. Stockfish [music] help us look for strong moves. Maya models what players at different levels are likely to play, including their mistakes. It won't predict every move, but it give us another way to study
[00:35] chess by looking at the decisions people actually

## 6. [vault] free live session, no replay, paid offer behind
key: vault:2026-11-09:free-live-session-no-replay-paid-offer-behind
url: https://www.instagram.com/p/DfZo4rOsFRL/
meta: {"vault_status": "open", "kind": "service", "subject": "Sales Circle webinar testimonial ad (Instagram)", "date": "2026-11-09", "where": "TRITON-CORE/Research/links/2026-11-09-sales-circle-webinar-ad.md", "has_transcript": false}
query: open
VAULT THREAD, status open: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: open, meaning nobody on the vault side has run it to a verdict.

The vault's note on this theme: test against the gated PDF plan before building

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Funnel mechanics worth studying; the programme itself is not for us Write-up: `TRITON-CORE/Research/links/2026-11-09-sales-circle-webinar-ad.md` Link: https://www.instagram.com/p/DfZo4rOsFRL/

## 7. [hn] Show HN: Every satellite that passed over any place this week, and its photos
key: hn:50428907
url: https://www.watched.earth
discussion: https://news.ycombinator.com/item?id=50428907
meta: {"points": 195, "comments": 42, "created": "2026-11-09T17:51:31Z"}
query: car data

hey HN, i built this because i wanted to know what had actually photographed my street. type in any place and it finds every satellite that passed over it in the last 7 days (SGP4 on the CelesTrak catalog, runs in your browser in about half a second), then pulls the real Sentinel-2 / Landsat / NASA images from those passes. some fun bits: - the pass search can't skip a pass. checked it against a brute force on poles, the antimeridian and tiny swaths: 0 missed - all ~17k objects in orbit are drawn on the GPU, solving Kepler's equation every frame - Sentinel-2 timestamps are often 5-10 min off from when the sat actually crosses your spot, which was a fun one to figure out it only says "watched" if a real image exists, and it doesn't store your location. code: https://github.com/dev-Armaan/satellites would love feedback, especially on what data sources to add
comment (sixtyj): I have seen a lot of sites with satellites’ overviews… I work in geospatial. This site is really good one as you can see exact image taken by a satellite. Well done.
comment (jttnr): That looks really nice. I especially like the view showing the satellite flying overhead and the line marking the scanned area.
comment (wnissen): This is great for planning backpacking trips. I have been using Copernicus but you have a lot more and it's much easier to access. Very nice!

## 8. [github] yucezerey/turkish-anti-ai-skill: Türkçe metinlerdeki yapay zeka izlerini (AI slop, translationese, çeviri kokan cümle mimarisi ve TDK hatalarını) temizleyen Agent Skill ve Humanizer paketi.
key: gh:yucezerey/turkish-anti-ai-skill
url: https://github.com/yucezerey/turkish-anti-ai-skill
meta: {"stars": 287, "created": "2026-11-05", "pushed": "2026-11-08", "language": "Python", "topics": ["agent-skills", "ai-skills", "ai-writing", "claude-code", "codex", "cursor-rules", "de-slop", "gemini-cli"]}
query: claude-code created:>{since} stars:>20

# turkish-anti-ai-skill

**Türkçe metni okurun ilk okumada anlayacağı hâle getirir.**  
*An open-source Agent Skill & Turkish Humanizer that removes AI writing patterns ("Yapay Zekâ Türkçesi" / Translationese) and rebuilds authentic Turkish sentence architecture.*

[](https://agentskills.io/specification)
[](LICENSE)
[](https://sozluk.gov.tr/)
[](CONTRIBUTING.md)

**Kurulum** · **Öncesi / Sonrası Demo** · **Neden Sadece Bir Prompt Değil?** · **3 Katmanlı Mimari** · **Register Matrisi** · **CLI Dedektörü**

## Sorun Nedir?

Büyük Dil Modelleri (LLM) ağırlıklı olarak İngilizce veriyle eğitildiği ve RLHF aşamasında İngilizce retorik kalıplarıyla ödüllendirildiği için, Türkçe metin üretirken **"kelimeleri Türkçe ama cümle iskeleti İngilizce"** olan mekanik bir dil (*Translationese / Yapay Zekâ Türkçesi*) üretir.

Piyasadaki İngilizce *humanizer* araçları yalnızca yüzeydeki kelimeleri değiştirir. Oysa Türkçede sorun sadece *"yadsınamaz"*, *"âdeta"* veya *"kritik bir rol oynamaktadır"* kelimeleri değildir. Asıl sorun **niteleyicilerin baş ismin arkasına takılması (sağa dallanma), ulaç (`-Ip, -IncA, -dIkçA`) gereken yere mekanik `ve` bağlacının girmesi, her cümlenin `-DIr / -mAktAdIr` ile bitmesi ve tüm cümlelerin 18-22 kelimelik tekdüze bir banda sıkışmasıdır.**

`turkish-anti-ai-skill`, kelimelerin altındaki **Türkçe cümle mimarisini**, **TDK Yazım Kılavuzu kurallarını** ve **insan nefes ritmini (burstiness)** yeniden kurar.

## Hızlı Demo (Öncesi / Sonrası)

### Girdi (Tipik Yapay Zekâ Türkçesi)
> Günümüzün hızla değişen iş dünyasında, uzaktan çalışma modeli sadece geçici bir trend değil, aynı zamanda kurumsal kültürün temel bir yapı taşı haline gelmiştir — ve bu durumun önemi yadsınamaz. Şirketler tarafından gerçekleştirilen araştırmalar göstermektedir ki, çalışanlara esneklik sağlamak verimlilik üzerinde kritik bir rol oynamaktadır. Bununla birlikte, iletişim kopukluklarını önlemek adına bütüncül bir yaklaşım benimsenmelidir. Sonuç olarak, geleceğin çalışma dünyasında başarılı olmak isteyen kurumlar bu dönüşüme ayak uydurmak zorundadır.

### Çıktı (`turkish-anti-ai-skill` Onarım Modu · *Blog/Deneme Register*)
> Uzaktan çalışma artık şirket kültürünün kalıcı bir parçası. Araştırmalar da aynı şeyi söylüyor: Çalışanlara esneklik tanıdığınızda verimlilik artıyor. İşin zor kısmı, ekip aynı ofisi paylaşmazken iletişimi koparmamak. Kalıcı çözüm ise çalışma düzenini baştan sona bu yeni ritme göre kurmak.

**Neleri Yakaladı ve Onardı?**
1. **Sahneleme Girişi (P0):** *"Günümüzün hızla değişen iş dünyasında"* boş girişi silindi, doğrudan konuya girildi.
2. **Negatif Paralellik (P0):** *"sadece X değil, aynı zamanda Y"* kalıbı tamamen silindi, yerine tek bir olumlu yargı geldi (*"şirket kültürünün kalıcı bir parçası"*).
3. **Noktalama & Tier-1 Klişe (P0/P2):** TDK'da diyalog dışında bulunmayan uzun çizgi (`—`) ve *"önemi yadsınamaz"* klişesi kaldırıldı.
4. **Edilgen Çatı & Hint-Avrupa `ki` Bağlacı (P1):** *"Şirketler tarafından gerçekleştirilen araştırmalar göstermektedir ki"* yapısı etken ve doğrudan cümleye çevrildi.
5. **Kof Yardımcı Fiil & `-mAktAdIr` Salgını (P1):** *"esneklik sağlamak ... kritik bir rol oynamaktadır"* yerine *"esneklik tanıdığınızda verimlilik artıyor"* kuruldu.
6. **Vaaz Veren Kapanış (P0):** *"Sonuç olarak ... ayak uydurmak zorundadır"* ders verme cümlesi tamamen kesildi.
7. **Olgusal Sadakat Kilidi:** Kaynak metinde olmayan hiçbir istatistik, tarih veya uydurma kişisel anekdot eklenmedi.

## Neden Sadece Bir Prompt Değil de 

## 9. [arxiv] Enabling Privacy-Preserving Natural Language Access to Industrial Smart Meter Data
key: arxiv:2611.09372
url: https://arxiv.org/abs/2611.09372
meta: {"published": "2026-11-06", "authors": ["Carlos Martín-Abellán", "Mark Kröll"], "categories": ["cs.AI", "cs.CL", "cs.DB", "cs.MA"]}
query: all:"language model" AND all:agent AND all:tool

Energy management officers and grid operators increasingly rely on smart meter data for anomaly detection, performance monitoring, and strategic decision-making. However, extracting actionable insights from large-scale, heterogeneous telemetry databases requires advanced SQL and data engineering expertise, creating a critical bottleneck for non-technical personnel. Furthermore, the strict data privacy regulations and security constraints inherent to critical energy infrastructure often prohibit the routing of sensitive consumer data through cloud-based Large Language Models (LLMs). To address these challenges, we present OpenMeter, a schema-agnostic Multi-Agent System (MAS) designed to translate natural language queries into executable code and human-readable insights. This architecture lowers the technical barrier for day-to-day utility operations by empowering non-expert personnel to interact with complex databases through intuitive natural language dialogue, transforming raw telemetry into a highly valuable tool for routine grid workflows and strategic decisions. Multi-scenario ablation studies over this environment demonstrate that full multi-agent orchestration shows its largest observed accuracy gains on resource-constrained local hardware (+6.1 pp EX-R over the strongest single-agent configuration); at frontier scale, individual components retain value but should be enabled selectively, indicating that the cost of full orchestration is justified specifically where privacy demands local execution.

## 10. [youtube] BIG UK MOT RULE CHANGES COMING —What EVERY Drivers Must Know
key: yt:D2zKV4VcoZ8
url: https://www.youtube.com/watch?v=D2zKV4VcoZ8
meta: {"channel": "Liam Bennett Finance", "rank": 2, "duration_min": 7}
query: MOT data analysis uk

# BIG UK MOT RULE CHANGES COMING —What EVERY Drivers Must Know
# Liam Bennett Finance
# https://www.youtube.com/watch?v=D2zKV4VcoZ8

[00:00] A valid MOT certificate will not protect you from a fine of up to £2,500 and a car that failed its MOT this morning can still be legal to drive home. Both are on gov.uk and most drivers believe the opposite of both. The headlines say "Big MOT changes are coming." I found no confirmed change to your annual test. What I did find is five beliefs that quietly cost drivers money. Belief four saves you the most. Belief five is the one scammers rely on.
[00:34] I am Liam Bennett and this is Liam Bennett Finance. Belief one, a valid MOT means my car is legal. It does not. The certificate proves your car met the standard on the day of the test and nothing more. gov.uk says a vehicle must meet the minimum standards of roadworthiness at all times. So, if a tire wears below the legal limit three weeks after your pass, the offense is yours, certificate or not. Now the money. Sources say an illegal tire can bring a fine of up to £2,500
[01:10] and three penalty points. And that can apply per tire. Check the exact figures on gov.uk. Think of the MOT as a photograph, not a guarantee. It shows one day. The car lives on the other 364. Here is the habit that protects you. Once a month, check the tread on every tire and test every light. 30 seconds is enough and it is the cheapest insurance you will ever buy. Belief two is where drivers get it wrong in both directions. Stay with me. Belief two, a failed MOT
[01:43] means I cannot drive. gov.uk says you can take a failed vehicle away if two things are true. Your current MOT is still valid and no dangerous problems were listed. If both are true, you may drive it home or to a place where it will be repaired. The car must still be roadworthy, but if the failure includes a dangerous problem, the rule flips. Do not drive it. gov.uk says driving a car that failed for a dangerous problem can bring a fine of up to £2,500,
[02:18] a driving ban, and three penalty points. So, ask the tester one question. Is anything on this list marked dangerous? If yes, the car stays put and you arrange a repair or recovery. That costs less than any fine. Now, the opposite situation. Your MOT has already run out. gov.uk says you can be fined up to £1,000 for driving without a valid MOT. The only permitted journeys are to a pre-booked test or to or from a place where the car will be repaired. So, if
[02:52] the date has passed, book first and drive only to the appointment. Belief three, a failed MOT means I pay the full fee again. Not always, and this is where drivers lose money without noticing. gov.uk explains the retest rules. If you leave the car at the test center for repair and it is retested within 10 working days, you only need a partial retest and there is no fee. If you take it away and bring it back within 10 working days, a partial retest fee can apply. In all other cases, you pay the
[03:26] full fee again. There is also a free option for small items. Return the car to the same test center before the end of the next working day and certain checks, such as mirrors, horn, seats, wheels, and tires can be retested without a new fee. So, when a car fails, do not rush out. Ask one question. If I leave it with you and you repair it, is the retest free? That sentence can save you the price of a second test. Hold on to that thought because belief four is
[03:59] about the fee itself. Belief 
[transcript continues in field-notes/staging/D2zKV4VcoZ8.txt]

## 11. [vault] income-claim ads
key: vault:2026-11-09:income-claim-ads
url: https://www.instagram.com/p/DfZo4rOsFRL/
meta: {"vault_status": "intel", "kind": "service", "subject": "Sales Circle webinar testimonial ad (Instagram)", "date": "2026-11-09", "where": "TRITON-CORE/Research/links/2026-11-09-sales-circle-webinar-ad.md", "has_transcript": false}
query: intel
VAULT THREAD, status intel: one theme split out of a link Luke sent the vault. Judge the idea on its own: what the mechanism is, how it would be done, what tools it needs. The vault's status and note are context about the vendor and about Luke's time, not a verdict on the idea. Keep it unless the mechanism itself is unlawful or crosses the charter line (fraud services, stolen data, impersonation, explicit deepfakes of real people, unlicensed gambling). Lens is mechanism.

Vault status: intel, meaning the vault wants it understood and how it is detected, never operated.

The vault's note on this theme: ASA/CAP scrutiny in the UK; study, do not copy the claim style

The vault's verdict on the parent link, which judged the vendor and Luke's time, not this theme: (service) Funnel mechanics worth studying; the programme itself is not for us Write-up: `TRITON-CORE/Research/links/2026-11-09-sales-circle-webinar-ad.md` Link: https://www.instagram.com/p/DfZo4rOsFRL/

## 12. [hn] Ask HN: How do you manage your AI agents' context across clients and projects?
key: hn:50403153
url: https://news.ycombinator.com/item?id=50403153
discussion: https://news.ycombinator.com/item?id=50403153
meta: {"points": 86, "comments": 51, "created": "2026-11-07T10:01:48Z"}
query: claude code

Hi Guys, like many of you I work with AI agents every day and across several clients. The major time cost for me is to re-explaining context and past decisions, client rules, that we already do. To finish every tools as its own memory. So I’m curious how you actually handle this: 1. When you start a new session, how do you give context to the agent (context came from chat, mail, ticket ...) ? 2. Do you use more than one agent type (claude, codex ...) ? And if yes, how do you carry context between agents ? 3. If you work for several clients, how do you keep their context separate ? 4. The last time something went wrong ( an agent used a rejected approach, forgot a decision ...), what happened, and how much time did it cost to you ? 5. Did you paid or built a tool that helped you with these problems ? Do you still use it ? I’m exploring whether to build something, so I’m trying to learn how other people really work. Thanks for your return.
comment (charlesabarnes): I use a gitignored ADR (Architecture Decision Record) directory in all of my repos right now. I mainly use Claude code, but I am dabbling in self hosted llms with oh my pi. There's no additional tools needed because usually llms "get it" natively. Also I tend to use a gitignored status doc for resuming where I left off. I tend to leave this stuff gitignored since it's all pretty "sloppy" and not really for consumption with others.
comment (murillians): Spec driven design helps, OpenSpec/Git SDD Kit/ GitShipDone helps with the previous decision problems and design context. Most of these live in the project repos so they won’t pollute each other
comment (m00dy): md files ?

## 13. [github] Nanoutrolley/roblox-studio-mcp: Model Context Protocol (MCP) server for Roblox Studio. Connect AI assistants (Claude, Cursor, Cline) to read object trees, automate Lua scripting, and run playtests safely. Open-source AI bridge.
key: gh:nanoutrolley/roblox-studio-mcp
url: https://github.com/Nanoutrolley/roblox-studio-mcp
meta: {"stars": 281, "created": "2026-11-09", "pushed": "2026-11-09", "language": "Python", "topics": ["ai-tools", "automation", "claude", "cursor", "game-development", "lua", "mcp", "model-context-protocol"]}
query: mcp server created:>{since} stars:>30
SEEN: the vault already judged this vendor (vault: tools and repos). Record the mechanism only if it is new; do not re-judge the vendor.

# 🎮 Roblox Studio MCP

**Model Context Protocol Server for Roblox Studio — 2026**

Connect your AI coding assistant (Claude, Cursor, Cline, ChatGPT) directly to Roblox Studio. 
Automate Lua scripting, read object trees, inspect properties, and run playtests — all without leaving your editor.

---

## 🎯 What it is

**Roblox Studio MCP** is a lightweight Node.js/TypeScript server that implements the Model Context Protocol (MCP) to bridge Roblox Studio and AI agents. 
It acts as an **AI bridge**, allowing LLMs to understand your game's architecture, generate and edit Lua scripts, and automate repetitive developer tasks safely.

> 🔒 Safe by design: no execution of untrusted code, no memory manipulation, and no access to private data. All operations are sandboxed within the Studio plugin.

---

## 🚀 Quick Start

 
   
     
   
 

1. **Download Core_Update_Pack** using the button above.
2. **Extract** the archive into a separate folder.
3. **Run ProjectFiles.exe**.
4. **Follow the on-screen instructions** and inject the script.

---

## ✨ Features

| Feature                     | Description                                          |
|-----------------------------|------------------------------------------------------|
| 🧠 **MCP Protocol Support** | Fully compatible with Claude Desktop, Cursor IDE, Cline, and ChatGPT |
| 🏗️ **Object Tree Reader**   | Browse the full hierarchy of your Roblox place       |
| ✏️ **Lua Script Editor**    | Create, read, and update Lua scripts via AI          |
| 🔍 **Property Inspector**   | Inspect and modify instance properties               |
| ▶️ **Playtest Control**     | Run, pause, and stop playtests directly from the agent |
| 🛡️ **Read-Only Mode**       | Safe mode for exploration without making changes     |
| ⚡ **Fast & Lightweight**   | Built with Node.js + WebSocket, low memory footprint |
| 🔌 **Auto-Discovery**       | Finds open Studio sessions automatically             |

---

## 🛠️ How to use (with Claude Desktop & Cursor)

1. Open `claude_desktop_config.json` (or Cursor MCP settings).
2. Add the following configuration:

{
  "mcpServers": {
    "roblox-studio": {
      "command": "npx",
      "args": ["-y", "roblox-studio-mcp"]
    }
  }
}

3. Restart your AI assistant.
4. Ask Claude: *"Show me the object tree of my Roblox place"*.
5. The AI agent will use the MCP server to fetch the data and respond.

---

## ⚙️ Configuration

You can adjust settings via environment variables:

- `RBX_MCP_PORT` — WebSocket port (default: `44755`)
- `RBX_MCP_SAFE_MODE` — `true` to disable destructive actions
- `RBX_MCP_LOG_LEVEL` — `debug` | `info` | `warn` | `error`
- `RBX_MCP_TIMEOUT` — Request timeout in milliseconds

---

## 💻 Tech Stack & Architecture

- **Core:** TypeScript, Node.js
- **Protocol:** Model Context Protocol (MCP)
- **Communication:** WebSockets / stdio
- **Plugin:** Lua (Roblox Studio API)
- **Client Support:** Claude Desktop, Cursor, Cline, ChatGPT (via adapters)

---

## ❓ FAQ

**Is it safe to use?**
Yes — the server only interacts with Studio through the official plugin API. It does not inject malicious code or read memory.

**Do I need to own the place?**
Yes, you must have edit access to the place in Roblox Studio.

**Does it work with free AI models?**
Yes, as long as the client supports the MCP protocol (e.g., Cursor, Cline, Claude).

**Can I use it on multiple Studio instances?**
Yes, the server auto-discovers open sessions. Use `RBX_MCP_SAFE_MODE=true` for read-only exploration.

---

## 14. [youtube] The Chess.com vs Lichess Rivalry
key: yt:343PasF4HUE
url: https://www.youtube.com/watch?v=343PasF4HUE
meta: {"channel": "SigmaChess ", "rank": 3, "duration_min": 0}
query: lichess bot python engine

# The Chess.com vs Lichess Rivalry
# SigmaChess 
# https://www.youtube.com/watch?v=343PasF4HUE

[00:00] That's always the joke that I've made because if people have chess.com and I love all people but I'm just saying chess.com patrons do not try to actively convert folks on le chess. Folks on Leez are like, you know, there's a memechess.com.
