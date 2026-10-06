# Refill sources

Written 6 Oct 2026 after Luke read the 5 Oct nightly ("ran out of anything runnable") as doing
the bare minimum. When `probe.py next --refill` prints REFILL, take the first source below whose
`used` column is empty, learn one thing from it in under ten minutes, and queue ONE build that
puts it to work tonight: `probe.py add "..." --source refill --est 25`. Then write the date in
`used`. A build is something that runs or renders: a script, a simulation, a page, a scored
check. Reading notes alone are not a build.

All of these are free and readable without a login or a key from a scheduled run (curl, the
keyless YouTube transcript pipeline, or a raw GitHub file). No git clone, no npm: fetch files with
Python, write the build in Python or plain HTML.

When the list runs low, add to it. Anything that turned out to need a login gets struck through
with the date, not deleted.

| # | Source | How to pull | A build it suggests | used |
|---|---|---|---|---|
| 1 | web.dev Learn CSS and Learn Design (Google) | curl the course pages | Rebuild one page of the lab site (`docs/`) to one lesson's rule, before/after screenshot | |
| 2 | Anthropic courses repo (github.com/anthropics/courses), prompt engineering and tool use | raw.githubusercontent.com | Run one exercise's idea against a Proteus prompt (harvest child, Skool reader) and score the output | |
| 3 | Soccermatics (David Sumpter, soccermatics.readthedocs.io) | curl the lesson pages | An xG or pitch-control toy on the football-data rows the Pitch already holds | |
| 4 | Forecasting: Principles and Practice, 3rd ed. (otexts.com/fpp3) | curl one chapter | A calibration plot for the judgement book or the exchange book | |
| 5 | Chess Programming Wiki (chessprogramming.org) | curl one article | One engine idea (move ordering, a quiescence tweak) measured on positions from `games/lichess/` | |
| 6 | Microsoft Generative AI for Beginners (github.com/microsoft/generative-ai-for-beginners) | raw GitHub lesson file | One lesson run locally against Ollama qwen, timed | |
| 7 | Meta Business Help Centre and Ads Library docs (facebook.com/business/help), Facebook ads basics | curl the help pages; Ads Library pages need no login for UK political and all-category search | A dated snapshot of who is advertising in one UK trade, and what their ads say | |
| 8 | Hugging Face Learn, LLM and agents courses (huggingface.co/learn) | curl the chapter pages | One small agent pattern rebuilt in plain Python inside the sandbox | |
| 9 | Solana and Jupiter developer docs (solana.com/docs, dev.jup.ag) | curl | A read-only check on one Grinder assumption (pool fee, quote impact for a $130 swap) | |
| 10 | fast.ai Practical Deep Learning (course.fast.ai) | curl the lesson page and notebook | One notebook's core idea on a tiny local dataset, CPU only | |
| 11 | YouTube: one free full course on a topic in PERSONA.md | `bin/yt-fetch.py` transcript | The course's one worked example, rebuilt and run | |
| 12 | Kaggle Learn lesson pages (kaggle.com/learn) | curl the tutorial page (exercises need a login; the lesson does not) | The lesson's method on a public dataset already on disk | |
