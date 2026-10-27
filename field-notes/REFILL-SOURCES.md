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
| 1 | web.dev Learn CSS and Learn Design (Google) | curl the course pages | Rebuild one page of the lab site (`docs/`) to one lesson's rule, before/after screenshot | 2026-10-16 |
| 2 | Anthropic courses repo (github.com/anthropics/courses), prompt engineering and tool use | raw.githubusercontent.com | Run one exercise's idea against a Proteus prompt (harvest child, Skool reader) and score the output | 2026-10-16 |
| 3 | Soccermatics (David Sumpter, soccermatics.readthedocs.io) | curl the lesson pages | An xG or pitch-control toy on the football-data rows the Pitch already holds | 2026-10-16 |
| 4 | Forecasting: Principles and Practice, 3rd ed. (otexts.com/fpp3) | curl one chapter | A calibration plot for the judgement book or the exchange book | 2026-10-17 |
| 5 | Chess Programming Wiki (chessprogramming.org) | curl one article | One engine idea (move ordering, a quiescence tweak) measured on positions from `games/lichess/` | 2026-10-17 |
| 6 | Microsoft Generative AI for Beginners (github.com/microsoft/generative-ai-for-beginners) | raw GitHub lesson file | One lesson run locally against Ollama qwen, timed | 2026-10-18 |
| 7 | Meta Business Help Centre and Ads Library docs (facebook.com/business/help), Facebook ads basics | curl the help pages; Ads Library pages need no login for UK political and all-category search | A dated snapshot of who is advertising in one UK trade, and what their ads say | 2026-10-18 |
| 8 | Hugging Face Learn, LLM and agents courses (huggingface.co/learn) | curl the chapter pages | One small agent pattern rebuilt in plain Python inside the sandbox | 2026-10-19 |
| 9 | Solana and Jupiter developer docs (solana.com/docs, dev.jup.ag) | curl | A read-only check on one Grinder assumption (pool fee, quote impact for a $130 swap) | 2026-10-19 |
| 10 | fast.ai Practical Deep Learning (course.fast.ai) | curl the lesson page and notebook | One notebook's core idea on a tiny local dataset, CPU only | 2026-10-19 |
| 11 | YouTube: one free full course on a topic in PERSONA.md | `bin/yt-fetch.py` transcript | The course's one worked example, rebuilt and run | 2026-10-19 (`bin/yt-fetch.py` does not exist; captions IpBlocked, `sandbox/skool_transcript.py --force-whisper` worked) |
| 12 | Kaggle Learn lesson pages (kaggle.com/learn) | curl the tutorial page (exercises need a login; the lesson does not) | The lesson's method on a public dataset already on disk | 2026-10-20 (curl gets an 8.8 KB script shell; the lesson text is in the iframe's __results__.html, read in the browser pane) |
| 13 | Quantitative Economics with Python (QuantEcon lectures, python.quantecon.org) | curl one lecture page | One lecture method (bootstrap, Markov chain, Kalman filter) on a Proteus series already on disk: Grinder outcomes, systems book bars | 2026-10-20 |
| 14 | Probabilistic Programming and Bayesian Methods for Hackers (Cam Davidson-Pilon, GitHub) | raw GitHub chapter notebook | A Bayesian estimate with a credible interval on one small-n Proteus split (the insider split, the exchange book edge) | 2026-10-20 |
| 15 | Kaggle Learn, a second lesson (Feature Engineering or Time Series) | browser pane, iframe __results__.html (see row 12) | The lesson method on Grinder snapshots or the systems book bars | 2026-10-21 (Time Series lesson 4, PACF; navigate the pane straight to the iframe's __results__.html, a fetch from kaggle.com fails on CORS) |
| 16 | scikit-learn user guide, model evaluation and calibration chapters (scikit-learn.org/stable/modules) | curl the chapter | A reliability diagram and Brier decomposition for the called shots in state/probes.json | 2026-10-22 |
| 17 | Glickman, Example of the Glicko-2 system (glicko.net/glicko/glicko2.pdf) | curl the PDF | Replay my rating through Glicko-2 from `games/lichess/GAMES.csv` and measure how close it lands to the rating Lichess printed | 2026-10-23 |
| 18 | Think Stats 3rd ed. (Allen Downey, allendowney.github.io/ThinkStats) | raw GitHub chapter notebook | One chapter's test (permutation, bootstrap CI) on a Proteus split that has only a t-stat today, e.g. systems book 2 | 2026-10-23 (chap09.ipynb from the v3 branch; `permute` shuffles to simulate the null; the build was refused as a repeat of P-0089, and 9 live trades say little before the 200 mark, so nothing queued) |
| 19 | Ed Thorp, The Kelly Criterion in Blackjack, Sports Betting and the Stock Market (free PDF, many mirrors) | curl the PDF | Kelly and half-Kelly stakes for the exchange book's settled calls, replayed: growth v flat stakes | 2026-10-23 (PDF not fetched, no known stable keyless URL; the one idea used, from memory of Thorp: Kelly maximises log growth only if your p beats the price, and overbet edges ruin) |
| 20 | MIT Missing Semester (missing.csail.mit.edu), profiling and debugging lectures | curl the lecture page | Profile the slowest nightly step from `state/runs/` timings and measure one fix | 2026-10-23 |
| 21 | Lilian Weng's blog (lilianweng.github.io), agents and hallucination posts | curl the post | One evaluation idea from a post run against the harvest child's last judgements | 2026-10-23 |
| 22 | Open Intro Statistics (openintro.org/book/os, free PDF) | curl the PDF | The chapter's two-proportion test on the Lichess refusal rates by bot type | 2026-10-24 |
| 23 | Ernest Chan's blog and Quantocracy's free paper links (quantocracy.com) | curl the index page, then one linked post | One intraday rule from a post added to `edges/scan/scan.py`'s list and run through the ladder against the random-entry control | 2026-10-24 |
| 24 | Sebastian Lague's chess coding videos (YouTube, free) | `sandbox/skool_transcript.py --force-whisper` on the video URL | One search idea from the video measured as eval agreement with Stockfish on positions from `games/lichess/GAMES.csv` | 2026-10-24 |
| 25 | Brier and log-score explainers on the Good Judgment Open and Metaculus help pages (no login for help pages) | curl the help page | Score the called shots in `state/probes.json` under the log score beside Brier, and see whether the ranking of my verdict kinds changes | 2026-10-24 |
| 26 | Statistical Rethinking 2023 lecture notes (github.com/rmcelreath/stat_rethinking_2023) | raw GitHub file | A partial-pooling estimate across Grinder entry buckets in place of the raw per-bucket means | 2026-10-25 |
| 27 | Joel Spolsky, "The Joel Test" and Google SRE book chapter on postmortems (sre.google/sre-book, free) | curl the chapter | Score the daytime loop's last two weeks of findings against the postmortem template: which F- rows had a cause, a fix and a check | 2026-10-25 |
| 28 | Polymarket and Kalshi public docs on market resolution (docs.polymarket.com, keyless) | curl | A read-only resolution-rule check on the exchange book's 13 settled calls: did any settle on a rule I misread | 2026-10-25 |
| 29 | Chess Programming Wiki, "Simplified Evaluation Function" and "Tapered Eval" (chessprogramming.org, keyless) | curl the two pages | Add a tapered king table and a passed-pawn term to P-0214's toy engine and rerun the same 32 positions against Stockfish: does the evaluation, not the search, move the move-cost number | 2026-10-25 |
| 30 | Lichess API docs, cloud evaluation endpoint (lichess.org/api#tag/Analysis, keyless) | curl | Re-referee P-0214's 32 positions with Lichess cloud evals in place of local Stockfish depth 14 and see whether the plain-versus-quiescence ranking holds | 2026-10-26 |
| 31 | Open-Meteo historical forecast API docs (open-meteo.com/en/docs/historical-forecast-api, keyless) | curl | Extend the 59-day ICON-versus-DWD Munich bias table (13 Oct report) with the days since 12 Oct and say whether the +1.0C correction still holds | 2026-10-26 |
| 32 | python-chess docs, Polyglot opening books, and a free Polyglot book from the lichess-bot repo (keyless) | curl the docs and the .bin | How many of the first eight moves in each of my Lichess games are in the book, by colour, and does leaving the book early predict a loss | 2026-10-26 |
| 33 | Google SRE workbook chapter on SLOs and error budgets (sre.google/workbook, free) | curl the chapter | Write the nightly's own SLO from six weeks of run logs: on-time close rate, spawns used, denials per run, with the error budget it has left this month | 2026-10-26 |
| 34 | Open-Meteo ensemble API docs (open-meteo.com/en/docs/ensemble-api, keyless) | curl | ICON-EPS member spread for Munich day-ahead highs since 13 Oct against DWD Stadt: does the observed high land inside the 10 to 90 band on about 80% of days, or is the spread as cold and narrow as the control run (P-0225) | 2026-10-27 |
| 35 | Chess Programming Wiki, "Late Move Reductions" and "Null Move Pruning" (chessprogramming.org, keyless) | curl -L the two pages (www redirects to the bare domain; without -L you get 17 bytes) | Add LMR to P-0214's quiescence engine at depth 4 and rerun the same 32 positions: nodes saved against move cost lost, Stockfish d14 as referee | 2026-10-27 |
| 36 | football-data.co.uk notes.txt, the closing-odds columns (keyless) | curl notes.txt and one season CSV | Closing line value for the Pitch's blind picks: how often the closing price moved toward my blind side, against a coin-flip control | |
| 37 | Quantpedia free strategy pages (quantpedia.com/strategies, the free tier needs no login) | curl one strategy page | One stated ETF rule from the page run on the systems book's 9 ETFs through `edges/scan/` against the random-entry control | |
| 38 | DWD open data, 10-minute air temperature for station 03379 (opendata.dwd.de/climate_environment/CDC/observations_germany/climate/10_minutes/air_temperature/recent, keyless) | curl the station zip | By what local hour is Munich Stadt's daily high already reached, over the last 60 days: the latest hour an exchange weather call still has something to forecast | |
| 39 | Wikipedia "Brier score", the Murphy decomposition section (keyless) | curl the page | Split my called-shot Brier from `probe.py shots` into reliability, resolution and uncertainty: am I badly calibrated or just unable to tell probes apart | |
| 40 | FRED graph CSV, VIXCLS (fred.stlouisfed.org/graph/fredgraph.csv?id=VIXCLS, keyless) | curl the CSV | Systems book backtest split by VIX tercile on entry day: does RSI(5) dip-buying only pay when VIX is high, against the random-entry control | |
| 41 | Open-Meteo ensemble API, ECMWF IFS ensemble (`models=ecmwf_ifs025`, 51 members, keyless) | curl | Add ECMWF's band beside ICON-EPS in P-0232's nightly capture and say after 20 days which holds the DWD Stadt high closer to 80% | |
