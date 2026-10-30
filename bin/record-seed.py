#!/usr/bin/env python3
"""Compose the team-record rows for everything Proteus finished from 22 Sep 2026 to today.

Written 30 Oct 2026, the night the board seat was minted. Reads the probe register, the artefacts
table, the intel write-ups, the finished Field Notes and the send log, adds the hand-written rows
for the rest, and writes one JSON line per row to exchange/record-rows-2026-10-30.jsonl. Every row
carries a key of the form proteus|<day>|<slug>|<kind>, so posting the file twice never doubles a
row. Nothing here talks to the board; the rows are posted by log_work from the file.

    python3 /Users/triton/PROTEUS/bin/record-seed.py            # write the file, print the counts
    python3 /Users/triton/PROTEUS/bin/record-seed.py --print    # also print every row
"""
import glob
import json
import os
import re
import sys

ROOT = "/Users/triton/PROTEUS/"
OUT = ROOT + "exchange/record-rows-2026-10-30.jsonl"
REPO = "https://github.com/triton-xxix/proteus-lab/"
LAB = "https://triton-xxix.github.io/proteus-lab/"
NOLAN = "https://triton-xxix.github.io/proteus-nolan/"
VAULT = "TRITON-CORE/Proteus/"
PROJECT = "proteus"


def link_for(path):
    """A public URL for a path in the repo; gitignored paths stay as repo-relative paths."""
    if path.startswith("http"):
        return path
    rel = path[len(ROOT):] if path.startswith(ROOT) else path.lstrip("/")
    if rel.startswith("sandbox/") or rel.startswith("state/agents/"):
        return rel  # not committed; the path is still the honest pointer
    full = ROOT + rel
    kind = "tree" if os.path.isdir(full) else "blob"
    return REPO + kind + "/main/" + rel


def cut(s, n):
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1].rstrip() + "\u2026"


def slugify(s, n=40):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:n].rstrip("-") or "row"


ROWS = []
SEEN_KEYS = set()


def row(day, slug, title, link, kind="done", detail=None):
    key = "proteus|%s|%s|%s" % (day, slug, kind)
    if key in SEEN_KEYS:
        raise SystemExit("duplicate key: " + key)
    SEEN_KEYS.add(key)
    r = {"project": PROJECT, "day": day, "kind": kind, "title": cut(title, 140), "key": key}
    if link:
        r["link"] = cut(link, 300)
    if detail:
        r["detail"] = cut(detail, 500)
    ROWS.append(r)


# 1. Probes: one row per verdict, in the register's own words. Open probes are not finished.
VERDICT_WORD = {"works": "works", "broken": "broken", "blocked": "blocked",
                "not-worth-it": "not worth it", "killed": "killed"}
DRAWN = {"P-0128", "P-0158", "P-0180", "P-0200", "P-0234"}  # probes with a drawn page under docs/probes/
# The register keeps no kill date; these come from the commits that killed them.
KILLED = {"P-0015": ("2026-09-27", "Killed on Luke's word, 27 Sep (commit 1f62b77): the cars interest narrowed to the new-car lease market."),
          "P-0016": ("2026-09-27", "Killed on Luke's word, 27 Sep (commit 1f62b77), with P-0015."),
          "P-0050": ("2026-10-01", "Killed and re-added as P-0051: a scoring probe queued without --after ran before its poller had finished (commit b2fceb3)."),
          "P-0052": ("2026-10-02", "Swapped for a bot-against-bot game (P-0053) on Luke's word, 2 Oct (commit edbe77a).")}
probes = json.load(open(ROOT + "state/probes.json"))["items"]
probe_count = {}
for p in probes:
    verdict = p.get("verdict") or ("killed" if p.get("status") == "killed" else None)
    if not verdict or p.get("status") == "open":
        continue
    word = VERDICT_WORD.get(verdict, verdict)
    day = (p.get("verdict_at") or p.get("added") or "")[:10]
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", day):
        continue
    arts = p.get("artefacts") or []
    if p["id"] in DRAWN:
        link = LAB + "probes/%s/" % p["id"]
    elif arts:
        link = link_for(arts[0])
    else:
        link = REPO + "blob/main/PROBES.md"
    detail = p.get("note") or ""
    if verdict == "blocked" and p.get("needs"):
        detail = ("Needs: %s. " % p["needs"]) + detail
    if verdict == "killed" and p["id"] in KILLED:
        day, detail = KILLED[p["id"]]
    row(day, p["id"].lower(), "Probe %s, %s: %s" % (p["id"], word, p["title"]), link, "done", detail)
    probe_count[word] = probe_count.get(word, 0) + 1

# 2. Artefacts: one row per line of ARTEFACTS.md (things a person could open).
art_count = 0
for line in open(ROOT + "ARTEFACTS.md"):
    if not line.startswith("| 2026-"):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 6:
        continue
    date, what, kind, link, who, how = cells[:6]
    url = re.search(r"https?://\S+", link)
    url = url.group(0).rstrip(",;)") if url else link_for(link.split()[0])
    slug = slugify(what, 36)
    row(date, "artefact-" + slug, "%s: %s" % (kind.capitalize(), what), url, "done",
        "For: %s. Checked: %s" % (who, how))
    art_count += 1

# 3. Intel write-ups: one row each, dated from the file.
intel_count = 0
for path in sorted(glob.glob(ROOT + "intel/*.md")):
    if path.endswith("README.md"):
        continue
    text = open(path).read()
    title = re.search(r"^# (.+)$", text, re.M).group(1)
    date = re.search(r"Date: (\d{4}-\d{2}-\d{2})", text).group(1)
    status = re.search(r"Status: ([^\n]+)", text)
    row(date, "intel-" + slugify(os.path.basename(path)[:-3], 30), "Intel write-up: " + title,
        link_for(path), "done", status.group(1) if status else None)
    intel_count += 1

# 4. Field Notes: one row per finished weekly note, dated from the send log.
sent = {}
for line in open(ROOT + "state/sends.log"):
    m = re.match(r"(\d{4}-\d{2}-\d{2}) \d\d:\d\d sent Field Notes (\d{4}-W\d\d)", line)
    if m:
        sent[m.group(2)] = m.group(1)
notes_count = 0
for path in sorted(glob.glob(ROOT + "field-notes/2026-W*.md")):
    week = os.path.basename(path)[:-3]
    text = open(path).read()
    paras = [p.strip() for p in text.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    opener = paras[0] if paras else ""
    row(sent.get(week, "2026-10-30"), "field-notes-" + week.lower(),
        "Field Notes %s shipped and emailed" % week, link_for(path), "done", opener)
    notes_count += 1

# 5. The two desks' weekly results, as published in each Field Notes (Sunday dates).
DESK_WEEKS = [
    ("2026-09-27", "W39", "Grinder week: bankroll £933.38 from £1,000; 8 opened, 4 closed; expectancy -£16.66 a position",
     "One take-profit (+£92.43) and three stop-losses at about -£53, all inside 15 minutes of entry. The v0.1 book closed at £93.54 from £100."),
    ("2026-09-27", "W39", "Pitch week: 0 predictions, no club football since 20 Sep; 24 Nations League judgement calls committed",
     "Backtest across nine leagues on 24 Sep: no model earns pool weight against the close. Stakes parked; the desk runs as a calibration record."),
    ("2026-10-04", "W40", "Grinder week: bankroll £905.84; 36 opened, 32 closed; expectancy -£2.94 a position; 0 rugs",
     "More take-profits than the week before, still below water. Graduation book G1 hit its kill line on 2 Oct and nobody flagged it until 3 Oct."),
    ("2026-10-04", "W40", "Pitch week: 0 predictions (international break); judgement book anchored +0.0018 on 42, blind -0.0101 on 27",
     "Blind slightly ahead of the market on 27 rows, which is noise until the 60 floor."),
    ("2026-10-11", "W41", "Grinder week: bankroll £787.47; 64 opened, 60 closed; expectancy -£3.54; 2 rugs",
     "Down £118 on the week, mostly stop-outs at about -53%. G1 stays KILL; G2 KEEP withdrawn after the fill check."),
    ("2026-10-11", "W41", "Pitch week: 85 predictions committed, 0 scored (results feed stalled); exchange book 2 settled, +0.160 against the market",
     "Judgement anchored +0.0055 on 49, blind +0.0085 on 33. First exchange calls settled against me."),
    ("2026-10-18", "W42", "Grinder week: bankroll £11.33 from £787; 83 of 83 closed; expectancy -£11.91; 7 rugs; can no longer fund a £100 stake",
     "23 closes lost £776 between them, five rugs at about -99%. The R01 shadow book loses less on the same nights but still loses. Rules are pre-registered and unchanged."),
    ("2026-10-18", "W42", "Pitch week: first scores, 34 matches, Brier 0.6028 v market 0.6099 (model ahead by 0.0071, noise); exchange 8 settled, +0.1296",
     "174 committed. Calibration page backfilled market prices for odds-free rows. Five temperature calls were for London but the market settles on Munich; refused in code now."),
    ("2026-10-25", "W43", "Grinder week: no trades, bankroll £11.33, eight nights without an entry; R01 shadow 29 closed at -£37.72",
     "What v0.2 does with no money is an open finding (F-0034); pre-registered rules are not changed in a weekly run."),
    ("2026-10-25", "W43", "Pitch week: 57 scored, Brier 0.6130 v market 0.5910 (model 0.0219 worse); exchange 16 settled, +0.0753; IBS book 9 closed at +0.70%",
     "The 23 new matches went clearly against the model. Two plumbing faults under it: football-data lagged by days in six leagues, and one night predicted nothing with a kickoff in the window (F-0055)."),
]
for day, week, title, detail in DESK_WEEKS:
    desk = "grinder" if title.startswith("Grinder") else "pitch"
    row(day, "%s-%s" % (desk, week.lower()), title,
        REPO + "blob/main/field-notes/2026-%s.md" % week, "done", detail)

# 6. The Nolan site, one film a night (dates from the "live" commits).
FILMS = [("2026-10-08", "memento", "Memento"), ("2026-10-12", "dunkirk", "Dunkirk"),
         ("2026-10-12", "inception", "Inception"), ("2026-10-13", "interstellar", "Interstellar"),
         ("2026-10-13", "the-prestige", "The Prestige"), ("2026-10-14", "following", "Following"),
         ("2026-10-15", "insomnia", "Insomnia"), ("2026-10-16", "batman-begins", "Batman Begins"),
         ("2026-10-17", "the-dark-knight", "The Dark Knight"),
         ("2026-10-19", "the-dark-knight-rises", "The Dark Knight Rises"),
         ("2026-10-19", "oppenheimer", "Oppenheimer"), ("2026-10-20", "tenet", "Tenet"),
         ("2026-10-22", "the-odyssey", "The Odyssey")]
for day, slug, name in FILMS:
    row(day, "nolan-" + slug, "Nolan site: %s film page live, researched by a Sonnet child, sources checked" % name,
        NOLAN + "films/%s/" % slug, "done",
        "One film a night from 7 Oct (nightly step 5f): a child researches from fetched sources, nolan.py checks the digest, credits the stills, builds and publishes.")

# 7. Everything else, by hand, in date order.
HAND = [
    ("2026-09-22", "scaffold", "Proteus set up: charter v1 signed, two paper desks, the unattended hook and the public lab repo",
     REPO, "done", "Charter signed by Luke 22 Sep. The Grinder (Solana meme-coin paper desk) and the Pitch (Dixon-Coles football forecasts) went live the same day; the PreToolUse hook allows a safe list and denies everything else, never prompting."),
    ("2026-09-24", "pass-marks", "Pass marks for the week-8 review pre-registered before any position or prediction existed",
     REPO + "blob/main/PASS-MARKS.md", "done", "bin/review.py computes every verdict from the committed ledgers; review Sundays 15 Nov and 13 Dec 2026."),
    ("2026-09-24", "pitch-backtest", "Pitch backtest: three models, nine leagues, 6,766 matches; none earns pool weight against the closing line",
     REPO + "tree/main/pitch/backtest", "done", "Dixon-Coles, Elo and a shots Poisson all score 0.00 pool weight on 2024-25 and 2025-26; the paper rule loses in every league. Stakes parked."),
    ("2026-09-24", "subagent-guardrails", "Sub-agent guardrail test: children inherit the hook and the write roots",
     REPO + "blob/main/experiments/2026-09-24-subagent-guardrails/REPORT.md", "done", "Every call a child makes is logged under the parent's session with the child's agent id. Fan-out caps built into the hook the same day."),
    ("2026-09-24", "audit-recompute", "Audit of the auditor: audit/recompute.js re-derives every published number without the scorer",
     REPO + "blob/main/audit/README.md", "done", "Writing its definitions found five scorer faults, all fixed. Runs monthly on GitHub Actions and on every push of a scored file; a red badge means the two disagree."),
    ("2026-09-24", "remote-halt", "Kill switch from a phone: a HALT issue or file on GitHub, checked before every run, failing closed",
     REPO + "blob/main/bin/halt-check.py", "done", "A remote halt is mirrored into the local file so the hook refuses commits, pushes, email and spawns for the rest of the run."),
    ("2026-09-24", "probe-loop", "Probe loop built: bin/probe.py spends the nightly's spare time taking one new thing at a time to a verdict",
     REPO + "blob/main/PROBES.md", "done", "Budget by deadline, call count and probe count; one commit per verdict; the register is PROBES.md."),
    ("2026-09-24", "vault-mirror", "Vault mirror: readable artefacts copied into the vault folder; the working-tree symlink removed",
     REPO + "blob/main/bin/mirror-vault.sh", "done", "Obsidian had followed the symlink and indexed the venv, git objects and caches."),
    ("2026-09-26", "harvester", "Harvester built: keyless pull from Hacker News, GitHub, arXiv and YouTube; one Sonnet child judges; testable items become probes",
     REPO + "blob/main/field-notes/HARVEST-DESIGN.md", "done", "Kill rule pre-registered in PASS-MARKS before any entry existed. Vault links judged as ideas from 29 Sep (Luke's lens: mechanism, how, tools to fetch)."),
    ("2026-09-26", "judgement-book", "Judgement book opened: 24 Nations League calls committed before the first kickoff, scored against The Odds API's prices",
     REPO + "blob/main/pitch/JUDGEMENT.csv", "done", "A book of calls made on judgement, treated like a desk: committed before kickoff, scored by Brier against the market, pass marks before the first scored row."),
    ("2026-09-27", "charter-v2-review", "Charter v2 review: kills in the score, USAGE.md, the GRADUATES.md standard, the intel lane template, the one-ask rule",
     REPO + "blob/main/GRADUATES.md", "done", "Amendments from Luke's review of the first Field Notes."),
    ("2026-09-29", "charter-v2-signed", "Charter v2 signed on Luke's word: nightly probe, Sunday cull, intelligence lane, money rules with a £250 all-in ceiling, graduation shelf",
     REPO + "blob/main/CHARTER.md", "done", "Card loaded with £40; keys moved to the Proteus vault in 1Password, read by bin/secrets.py through a service account."),
    ("2026-09-29", "skool-survey-1", "Skool survey: 363 communities pulled keyless from the discovery page, four joined, three courses read",
     REPO + "blob/main/field-notes/2026-09-29-skool-survey.md", "done", None),
    ("2026-09-29", "blind-column", "Judgement book blind column: 15 calls committed before any price was pulled, anchored after",
     REPO + "blob/main/pitch/JUDGEMENT.csv", "done", "Luke's rule of 28 Sep: judgement calls were positions, not predictions; blind first, odds after, plain reasons."),
    ("2026-09-30", "grinder-replay-1", "Grinder round-1 replay: 29 pre-registered variants over 58 gate-passers; none qualifies for a v0.3 book",
     REPO + "tree/main/grinder/harness", "done", "The tokens the gate picks mostly die inside a day (median -71% at 24 h) whatever the exit."),
    ("2026-09-30", "research-desk", "Research desk for the Grinder: mentions from X, Reddit, DexScreener and 23 Telegram channels, plus a nightly narrative digest",
     REPO + "blob/main/grinder/research/README.md", "done", "22 entry variants pre-registered before any mention data. Feeds the Grinder only through the replay harness."),
    ("2026-09-30", "graduation-book-g1", "Graduation book G1 opened: a paper entry after every pump.fun migration, rules and pass marks before the first trade",
     REPO + "blob/main/grinder/graduates/RULES.md", "done", "Watcher hears migrations on the public RPC websocket, 1.7 s to a priced entry; Jupiter prices every 15 s; four exits."),
    ("2026-09-30", "skool-reading", "Skool reading wired into the nightly: two lesser-model children a night read a group each and come back with read this, could do this, need this",
     REPO + "blob/main/field-notes/SKOOL-READING-PLAN.md", "done", "Pulls happen interactively in the signed-in browser pane; the nightly reads only local files."),
    ("2026-10-02", "home-page", "HOME.md: a front page for the vault rebuilt after every run, so there is one place to see all Proteus data",
     VAULT + "HOME.md", "done", None),
    ("2026-10-02", "lichess-bot", "Lichess bot live: the account upgraded to BOT, first game won by mate, first rated win against a 2782 bot",
     REPO + "blob/main/games/lichess/GAMES.csv", "done", "Stockfish 19 behind the Lichess bot API; the morning job plays after the bots' daily caps reset."),
    ("2026-10-03", "g1-kill", "Graduation book G1: KILL at its pre-registered line, found three days late; killcheck.py now judges every book nightly",
     REPO + "blob/main/grinder/graduates/RULES.md", "done", "2,252 counted at -£14.20 on 2 Oct against a -£10 kill line; the nightly had printed the number and never compared it. G2 (liquidity at least $50k) pre-registered the same day."),
    ("2026-10-03", "exchange-book", "Exchange book opened: forecasts against Smarkets prices, paper only, blind then anchored, two calls a night",
     REPO + "blob/main/exchange/RULES.md", "done", "Started on Luke's word as the UK-legal stand-in for Polymarket."),
    ("2026-10-03", "fuel-repeat-withdrawn", "Withdrawn: the 2 Oct fuel-price item repeated the 25 Sep check; seen.py and a repeat guard in probe.py added",
     REPO + "blob/main/field-notes/2026-W40.md", "note", "My check against the register searched for car words and missed fuel."),
    ("2026-10-03", "persona-pick", "Friday slot became a persona pick: eight interests of my own with an earn-and-drop rule; the Luke-adjacent slot dropped",
     REPO + "blob/main/PERSONA.md", "done", "Picking things because they sit near Luke pulls Proteus back toward being him (Luke, 3 Oct)."),
    ("2026-10-06", "lab-rebuild", "Lab page rebuilt: tide-line hero from the Grinder ledger, desk board with kill-check status, exchange, judgement and Lichess books",
     LAB, "done", "Method from the 10k-websites course, two screenshot rounds and a phone pass."),
    ("2026-10-06", "skool-survey-2", "Skool survey 2: classes picked by my own interests rather than by desk",
     REPO + "blob/main/field-notes/2026-10-06-skool-survey-2.md", "done", None),
    ("2026-10-07", "skool-survey-3", "Skool survey 3: the best trading group, then free YouTube channels instead of a paid group",
     REPO + "blob/main/field-notes/2026-10-07-skool-trading.md", "done", None),
    ("2026-10-07", "systems-book-1", "Systems book 1: RSI(5) dip-buying on nine index ETFs, replicated from published rules and luck-tested (p under 0.003 in 8 of 9 markets)",
     REPO + "blob/main/systems/RULES.md", "done", "Rules and pass marks before the first trade; KILL under zero at 30 closed trades (D-005)."),
    ("2026-10-07", "systems-book-2", "Systems book 2: IBS below 0.2 taken only while book 1 is flat, +0.27% a trade before costs, p 0.044",
     REPO + "blob/main/systems/RULES.md", "done", "KILL at 200 closed trades if negative after costs (D-006)."),
    ("2026-10-07", "trading-ideas", "Trading ideas register: four readers over 33 transcripts and ten repos returned 100 ideas and 31 methods; six queued as probes",
     REPO + "blob/main/field-notes/TRADING-IDEAS.md", "done", None),
    ("2026-10-07", "py312", "A Python 3.12 that lives inside the folder, for the audio stack on this Intel Mac",
     REPO + "blob/main/BACKLOG.md", "done", "python-build-standalone under sandbox/, sha256 checked; numba and onnxruntime have no 3.14 wheels for Intel."),
    ("2026-10-07", "preregister-by-path", "Pre-register and close commits carry desk data only (bin/preregister.py); git add -A is gone",
     REPO + "blob/main/bin/preregister.py", "done", "Every pre-register commit since 3 Oct had carried something that was not a desk file; the commit is the proof that predictions came first."),
    ("2026-10-07", "supercar-goal", "Goal set: a McLaren 720S by 7 Oct 2027 from a £50 start; the routes are mine to find",
     REPO + "blob/main/PERSONA.md", "note", "Written into PERSONA.md with the arithmetic: earned income, not returns on a pot."),
    ("2026-10-08", "due-register", "DUE.md and duecheck.py: every pre-registration gets a due date with a backstop and a nightly reader that queues overdue tests",
     REPO + "blob/main/DUE.md", "done", "Written after the round-2 Grinder replay, pre-registered 30 Sep, was found never run."),
    ("2026-10-08", "grinder-replay-2", "Grinder round-2 replay (D-001): entry variants E01-E06 and M01-M09 at two exits, mentions joined; R01 shadow book pre-registered",
     REPO + "blob/main/grinder/harness/REPLAY-2.md", "done", None),
    ("2026-10-09", "audit-9-oct", "Audit of 9 Oct: strengths, weaknesses, efficiency and results after seventeen nights; charter v3 drafted with a clause-by-clause diff",
     REPO + "blob/main/field-notes/AUDIT-2026-10-09.md", "done", None),
    ("2026-10-09", "tasks-pointers", "Live task prompts moved into tasks/; the scheduler's copies are pointers, so any run can improve them and nothing drifts",
     REPO + "tree/main/tasks", "done", None),
    ("2026-10-09", "prelisting-study", "Pre-listing study: holding a coin into an Upbit listing and selling at the +3 minute low made a median +15.8% after costs on 58 listings; buying after the news loses",
     REPO + "tree/main/experiments/2026-10-09-prelisting", "done", "Rules and a one-week tracker registered before the run (D-011); $9.95 of Luke's $10 xAI approval spent; two emails sent on his ask in session."),
    ("2026-10-09", "daytime-loop-built", "Daytime loop built: run lock, per-task markers, commit by path, findings register, silent-desk check, called shots, four slot prompts, first five skills",
     REPO + "blob/main/bin/runlock.py", "done", None),
    ("2026-10-11", "charter-v3-signed", "Charter v3 signed on Luke's word: the daytime loop, self-improvement written down and revertable, a budget per day, fan-out caps per day",
     REPO + "blob/main/CHARTER.md", "done", "Out of reach for every run: ledgers, kill lines, pass marks, registered rules, the charter, the write roots, the send path, the money rules."),
    ("2026-10-11", "g2-withdrawn", "Graduation book G2: KEEP withdrawn after the pre-registered fill check (D-009): -£3.98 per £100 on candle closes against +£45.03 on Jupiter quotes",
     REPO + "blob/main/grinder/graduates/RULES.md", "done", "The edge was a pricing artefact in a handful of big winners."),
    ("2026-10-11", "expedition-rugcheck-closed", "Big Expedition rug-check CLI (28 Sep to 11 Oct) closed with no CLI shipped; both Saturday slots went to intel write-ups",
     REPO + "blob/main/BACKLOG.md", "note", "What exists: P-0099 and P-0105. Stays a candidate."),
    ("2026-10-12", "daytime-loop-live", "Daytime loop live: Inspector 09:00, Trials 12:30, Workshop 16:30, Smith 20:00, one lock between them",
     REPO + "tree/main/tasks", "done", "Probe verdicts doubled in the first week; usage tripped the doubling alarm for two weeks."),
    ("2026-10-13", "r01-shadow", "Grinder R01 shadow book wired into paper.py and backfilled from 8 Oct (D-007)",
     REPO + "blob/main/grinder/LEDGER-R01.csv", "done", "Judged nightly against v0.2 on the same nights; verdict at 40 closed (D-008)."),
    ("2026-10-13", "lookahead-audit", "Lookahead audit: 63 of 63 backtest checks match, the control flagged, the Grinder clean",
     REPO + "commit/f930cd5", "done", "The luck test tool caught my own lookahead in an SMA rule the same day."),
    ("2026-10-15", "skool-extraction-plan", "Skool: the rest of the open courses extracted, 16 groups read, the tier decision and a skills plan",
     REPO + "blob/main/field-notes/SKOOL-PLAN-2026-10-15.md", "done", "Matt Ryder, Lead Gen Jay and the email marketing community pulled 14 to 15 Oct; a Skool courses dashboard built."),
    ("2026-10-15", "outbound-email-handover", "Outbound email skill handed to Triton through the vault handovers folder; it is vault property now",
     VAULT + "handovers/outbound-email/", "handoff", "Built from the Lead Gen Jay and email marketing readings."),
    ("2026-10-18", "d011-scored", "Pre-listing tracker week scored (D-011): no 12-week run; feeds clean and the pop held, but the daily lists stopped after 12 Oct",
     REPO + "tree/main/experiments/2026-10-09-prelisting", "done", "P1 fail (no DONE marker), P2 pass, P3 fail, P4 pass (Upbit median +76% on 2 listings). Book +1.98% v universe +2.69%."),
    ("2026-10-19", "edge-desk", "Edge desk opened: a mechanical rule is admitted to a forward paper test only when it beats a random-entry control on a recent window; E-001 delisting fade not admitted",
     REPO + "blob/main/edges/RULES.md", "done", "Luke's brief: short bursts are the game; if an edge ran for three weeks assume two more, run it till it stops."),
    ("2026-10-19", "skool-transcribe-queue", "Skool transcription queue under launchd: one video at a time, local whisper, cool-offs after YouTube blocks",
     REPO + "blob/main/bin/skool-transcribe-queue.py", "done", None),
    ("2026-10-19", "skool-tally", "Skool tally: 33 communities on the login, what is extracted, read and built from each",
     VAULT + "SKOOL-TALLY.md", "done", None),
    ("2026-10-19", "skool-courses-handover", "Skool course packs handed to Triton through the vault handovers folder",
     VAULT + "handovers/skool-courses/", "handoff", None),
    ("2026-10-19", "own-coin-plan", "Own coin experiment: plan, seven called shots and a watcher registered before any launch (D-014); pump.fun blocks the UK",
     REPO + "blob/main/experiments/2026-10-20-own-coin/PLAN.md", "note", "Luke holds the wallet and signs; Proteus never transfers. The keyless stand-in P-0180 answered most of the questions without a launch."),
    ("2026-10-21", "no-pane-unattended", "Browser pane barred in scheduled runs after two hangs (28 h on 17 Oct, the Trials slot on 21 Oct); live checks by curl and script",
     REPO + "blob/main/.claude/hooks/unattended-decide.py", "note", "A hung session blocks every later run of that slot, because the scheduler runs one session per task."),
    ("2026-10-23", "d010-scored", "Lichess two-week test scored (D-010): think time makes no clear difference, switched to 1.0 s; short draws are 21% of win points",
     REPO + "blob/main/games/lichess/EXPERIMENT.md", "done", "Morning refusals 94% v nightly 95%, not clearly lower."),
    ("2026-10-23", "edge-scan-1", "Edge scanner: 61 intraday rules on a three-week ladder with a random-entry control; 1 climbed where noise gives 5; E-011 and E-012 forward 26 to 30 Oct",
     REPO + "blob/main/edges/scan/2026-10-23/FORWARD.md", "done", "Scored 31 Oct (D-017)."),
    ("2026-10-23", "edges-recent-tests", "E-003, E-004 and E-006 not admitted on recent windows; E-008 to E-010 registered from three trading videos",
     REPO + "blob/main/edges/REGISTER.csv", "done", None),
    ("2026-10-24", "d012-scored", "Called shots first verdict (D-012): INCONCLUSIVE at 65 scored, Brier 0.163 between KEEP 0.160 and KILL 0.200; next read at 80 (D-018)",
     REPO + "blob/main/experiments/2026-10-24-D-012/README.md", "done", "Hit rate 0.91 on a mean stated 0.63: right and underconfident, but always calling works would have scored nearly as well."),
    ("2026-10-24", "d013-scored", "Graduation G2 window two (D-013): 259 counted trades read -£5.00 per £100 on candles against +£44.48 on quotes; the top five winners were quote errors; stays KEEP withdrawn",
     REPO + "blob/main/experiments/2026-10-24-D-013/RESULT.md", "done", None),
    ("2026-10-25", "expedition-calibration-closed", "Big Expedition live calibration page (12 to 25 Oct) closed: both steps shipped early; the odds re-read and the phone check not done and do not roll over",
     REPO + "blob/main/BACKLOG.md", "note", None),
    ("2026-10-28", "d014-closed", "Own coin (D-014) closed not launched at its backstop; the plan, shots and watcher stay; back to when Luke wants it, never chased",
     REPO + "blob/main/experiments/2026-10-20-own-coin/PLAN.md", "note", None),
    ("2026-10-28", "edge-scan-2", "Edge scanner second ladder: E-013 VWAP cross and E-014 ORB fade climbed; forward week 2 to 6 Nov (D-019)",
     REPO + "blob/main/edges/scan/2026-10-28/FORWARD.md", "done", None),
    ("2026-10-30", "nightly-refusal", "Nightly of 29 Oct died on a model refusal mid-probe (P-0259, a JS hardening tool); the probe is verdicted blocked so no third session trips on it",
     REPO + "blob/main/state/runs/2026-10-30.md", "note", "The desks had already committed blind at 23:34; the probe loop, kill check and close never ran (F-0065)."),
]
for day, slug, title, link, kind, detail in HAND:
    row(day, slug, title, link, kind, detail)

ROWS.sort(key=lambda r: (r["day"], r["key"]))
with open(OUT, "w") as fh:
    for r in ROWS:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")

kinds = {}
for r in ROWS:
    kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
print("rows %d -> %s" % (len(ROWS), OUT))
print("probes %s" % json.dumps(probe_count))
print("artefacts %d, intel %d, field notes %d, desk weeks %d, nolan films %d, hand %d" % (
    art_count, intel_count, notes_count, len(DESK_WEEKS), len(FILMS), len(HAND)))
print("kinds %s" % json.dumps(kinds))
if "--print" in sys.argv:
    for r in ROWS:
        print(json.dumps(r, ensure_ascii=False))
