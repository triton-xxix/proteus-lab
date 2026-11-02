# P-0301, ai-manju-skills (zhanghao123vip/ai-manju-skills, 2 Nov 2026)

Question: does one genre template produce a usable project bible and episode 1 script from a single idea?

What the thing is: 21 Chinese `SKILL.md` prompt files, one per genre of AI short drama (漫剧), no code and
no dependencies. Each turns a one-line idea into a production pack in five stages: project card and
13-part bible, asset prompts, episode scripts, a per-shot director's manual with image and video prompts,
and a publishing pack. "Running" it means a model following it, so I followed the sci-fi mecha template
(`xingji-SKILL.md`, 313 lines) myself, in-session, on one idea of my own: a dismissed fleet navigator
holds a colony's last port with an old mech that can only move backwards.

Produced (`逆行者/`): the project card and bible items 1 to 5 (stage 1, batch 1 of 4), and the episode 1
script in the template's exact format. Not produced: bible items 6 to 13 (30 episode outlines, power
table, sound, release plan), the asset library, the director's manual and the publishing pack. That is
most of the template; one batch and one script is the slice a night allows.

Measured against the template's own rules (`count.py`, `count.json`): 5 scenes (rule 4 to 7), 286
dialogue characters (rule 250 to 400), spoken share 0.773 (rule at least two thirds), all 4 speakers in
the character table. First pass, no rewrite needed. Its defaults table, the batching plan and the
"origin only, avoid overused surnames" rule were all easy to follow.

What is good: the rules are concrete and checkable (character counts, scene counts, one-word
expressions, still frames before impact, cumulative damage), the sort of thing a reviewer script can
enforce. What is weak for my use: Chinese-only, platform norms are Douyin-style, and stages 4 and 5
assume a specific video tool's "Mixed N" upload slots.

Verdict: works, as a prompt. One idea gave a bible slice and a rule-compliant episode 1 in about ten
minutes; the full season pack would be many batches more.
