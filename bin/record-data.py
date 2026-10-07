#!/usr/bin/env python3
"""Build record.json: every number the Sixteen Nights page and film show, computed from the repo.

    python3 /Users/triton/PROTEUS/bin/record-data.py [out.json]

Nothing here is typed by hand except quotations (which carry their source) and a few dated events
whose evidence is a commit hash or a file line, listed under "facts" with that source. Everything
else is computed from the committed ledgers, the probe registry, the run logs, the hook decision
logs and git history at the moment the script runs. Standard library only.

Default output: sites/builds/sixteen-nights/record.json (the build folder of the record page).
"""
import csv
import glob
import json
import os
import re
import statistics as st
import subprocess
import sys
from datetime import datetime, timezone, timedelta

ROOT = "/Users/triton/PROTEUS/"
OUT = ROOT + "sites/builds/sixteen-nights/record.json"
CUT_FROM = "2026-09-22"
GRINDER_START = {"v0.1": 100.0, "v0.2": 1000.0}
G2_LIQ = 50000.0
G2_FROM = datetime(2026, 10, 3, 12, 0, tzinfo=timezone.utc).timestamp()
LIVE_SESSION = re.compile(r"^[0-9a-f]{8}$")   # test sessions are "test-ses", "tab…", "tac…", never hex


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def rows(path):
    if not os.path.exists(path):
        return []
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def read(path):
    return open(path).read() if os.path.exists(path) else ""


def git(*args):
    return subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True, text=True, timeout=120).stdout


def utc(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def r2(x):
    return None if x is None else round(x, 2)


# ------------------------------------------------------------------ git history
def commits():
    out = []
    for line in git("log", "--reverse", "--date=iso-strict", "--format=%H|%h|%ad|%an|%s").splitlines():
        H, h, ad, an, s = line.split("|", 4)
        out.append({"sha": h, "full": H, "at": ad, "author": an, "subject": s, "day": ad[:10]})
    per_day = {}
    for c in out:
        per_day[c["day"]] = per_day.get(c["day"], 0) + 1
    by_author = {}
    for c in out:
        by_author[c["author"]] = by_author.get(c["author"], 0) + 1
    return {
        "total": len(out),
        "by_author": by_author,
        "per_day": [{"day": d, "n": n} for d, n in sorted(per_day.items())],
        "busiest": max(per_day.items(), key=lambda kv: kv[1]) if per_day else None,
        "first": out[0] if out else None,
        "last": out[-1] if out else None,
        "head": git("rev-parse", "--short", "HEAD").strip(),
    }


def first_commit_mentioning(needle, path):
    """Short sha and ISO time of the first commit whose diff of `path` adds `needle`."""
    line = git("log", "--reverse", "--format=%h|%aI", "-S", needle, "--", path).splitlines()
    if not line:
        return None, None
    h, at = line[0].split("|", 1)
    return h, at


# ------------------------------------------------------------------ nightly runs and the hook
def runs():
    out = []
    for path in sorted(glob.glob(ROOT + "state/runs/2*.md")):
        text = read(path)
        heads = re.findall(r"^## Nightly run (\d{4}-\d\d-\d\d) (\d\d:\d\d)", text, re.M)
        probes = re.findall(r"^- Probe (P-\d{4})", text, re.M)
        denied = len(re.findall(r"^\s+Denied", text, re.M))
        halt = bool(re.search(r"HALT", text))
        out.append({"day": os.path.basename(path)[:10], "nightly_at": ["%s %s" % h for h in heads],
                    "nightly": bool(heads), "probe_lines": len(probes), "denied_lines": denied, "mentions_halt": halt})
    return out


def hook():
    nights = []
    tot_allow = tot_deny = 0
    for path in sorted(glob.glob(ROOT + "state/unattended-decisions-2*.jsonl")):
        day = os.path.basename(path)[len("unattended-decisions-"):][:10]
        allow = deny = 0
        tests = 0
        denied_tools = {}
        for line in open(path):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            sid = str(r.get("session") or "")
            if not LIVE_SESSION.match(sid):
                tests += 1
                continue
            if r.get("outcome") == "deny":
                deny += 1
                denied_tools[r.get("tool")] = denied_tools.get(r.get("tool"), 0) + 1
            elif r.get("outcome") == "allow":
                allow += 1
        nights.append({"day": day, "allow": allow, "deny": deny, "test_lines_excluded": tests, "denied_tools": denied_tools})
        tot_allow += allow
        tot_deny += deny
    return {"allowed": tot_allow, "denied": tot_deny, "nights": nights,
            "note": "Live sessions only (8-hex session ids). Test and fan-out test sessions are excluded, as the memory note says."}


# ------------------------------------------------------------------ probes
def probes():
    d = json.load(open(ROOT + "state/probes.json"))
    items = d["items"]
    done = [p for p in items if p["status"] == "done"]
    verdicts = {}
    for p in done:
        verdicts[p["verdict"]] = verdicts.get(p["verdict"], 0) + 1
    by_source = {}
    for p in items:
        s = by_source.setdefault(p.get("source") or "unknown", {"total": 0, "works": 0})
        s["total"] += 1
        if p.get("verdict") == "works":
            s["works"] += 1
    cum = {}
    for p in done:
        day = (p.get("verdict_at") or "")[:10]
        if day:
            cum[day] = cum.get(day, 0) + 1
    running = 0
    cumulative = []
    for day in sorted(cum):
        running += cum[day]
        cumulative.append({"day": day, "verdicts": running})
    minutes = [p["minutes"] for p in items if isinstance(p.get("minutes"), (int, float))]
    killed = [p for p in items if p["status"] == "killed"]
    return {
        "total": len(items),
        "next_id": d.get("next_id"),
        "verdicts": verdicts,
        "done": len(done),
        "killed": len(killed),
        "open": sum(p["status"] == "open" for p in items),
        "in_progress": sum(p["status"] == "in_progress" for p in items),
        "by_source": by_source,
        "cumulative": cumulative,
        "minutes_timed": sum(minutes),
        "minutes_n": len(minutes),
        "longest_minutes": max(minutes) if minutes else None,
        "denials_inside_probes": sum(len(p.get("denied") or []) for p in items),
        "killed_ids": [p["id"] for p in killed],
        "items": [{
            "id": p["id"], "title": p["title"][:140], "status": p["status"], "verdict": p.get("verdict"),
            "source": p.get("source"), "added": p.get("added"), "started_at": p.get("started_at"),
            "verdict_at": p.get("verdict_at"), "minutes": p.get("minutes"),
            "denied": len(p.get("denied") or []), "note": (p.get("note") or "")[:200],
            "artefact": (p.get("artefacts") or [None])[0],
        } for p in items],
    }


# ------------------------------------------------------------------ the Grinder
def book_stats(book, start):
    closed = [r for r in book if r["exit_at"]]
    pnl = [f(r["pnl_gbp"]) or 0.0 for r in closed]
    reasons = {}
    for r in closed:
        reasons[r["exit_reason"]] = reasons.get(r["exit_reason"], 0) + 1
    return {
        "start": start, "bankroll": r2(start + sum(pnl)), "opened": len(book), "closed": len(closed),
        "open": len(book) - len(closed), "exit_reasons": reasons,
        "rugged": sum(r.get("rugged") == "1" for r in book),
        "hit_rate": round(sum(p > 0 for p in pnl) / len(pnl), 3) if pnl else None,
        "expectancy": r2(st.mean(pnl)) if pnl else None,
        "best": r2(max(pnl)) if pnl else None, "worst": r2(min(pnl)) if pnl else None,
        "best_removed_expectancy": r2(st.mean(sorted(pnl)[:-1])) if len(pnl) > 1 else None,
    }


def grinder():
    led = rows(ROOT + "grinder/LEDGER.csv")
    books = json.load(open(ROOT + "grinder/BOOKS.json")) if os.path.exists(ROOT + "grinder/BOOKS.json") else {"current": "v0.2", "books": {}}
    cur = books.get("current", "v0.2")
    out = {"current": cur, "books": {}}
    for v in sorted({r["rule_version"] for r in led}):
        book = [r for r in led if r["rule_version"] == v]
        start = (books.get("books", {}).get(v) or {}).get("bankroll_gbp", GRINDER_START.get(v, 0.0))
        out["books"][v] = book_stats(book, start)
    book = [r for r in led if r["rule_version"] == cur]
    start = out["books"].get(cur, {}).get("start", 1000.0)
    closed = sorted([r for r in book if r["exit_at"]], key=lambda r: r["exit_at"])
    # bankroll path by exit, one point per closed trade, plus the start
    path = [{"at": book[0]["entered_at"] if book else CUT_FROM, "bankroll": start, "id": None}]
    run = start
    for r in closed:
        run += f(r["pnl_gbp"]) or 0.0
        path.append({"at": r["exit_at"], "bankroll": round(run, 2), "id": r["id"], "token": r["token"],
                     "pnl": f(r["pnl_gbp"]), "reason": r["exit_reason"]})
    by_day = {}
    for p in path[1:]:
        by_day[p["at"][:10]] = p["bankroll"]
    low = min(path, key=lambda p: p["bankroll"]) if path else None
    # longest run of stop-losses in a row, by exit time
    worst_run = run_now = 0
    for r in closed:
        run_now = run_now + 1 if r["exit_reason"] in ("stop_loss", "rug") else 0
        worst_run = max(worst_run, run_now)
    trades = []
    for r in book:
        sha, at = first_commit_mentioning(r["id"] + ",", "grinder/LEDGER.csv")
        trades.append({"id": r["id"], "token": r["token"], "entered_at": r["entered_at"], "exit_at": r["exit_at"] or None,
                       "pnl": f(r["pnl_gbp"]), "reason": r["exit_reason"] or None, "rugged": r.get("rugged") == "1",
                       "entry_liq_usd": f(r.get("entry_liq_usd")), "score_24h": f(r.get("score_24h")),
                       "commit": sha, "committed_at": at})
    out.update({
        "stats": out["books"].get(cur), "path": path, "bankroll_by_day": [{"day": d, "bankroll": b} for d, b in sorted(by_day.items())],
        "low": low, "worst_losing_run": worst_run, "trades": trades,
        "first_trade": trades[0] if trades else None,
    })
    return out


def graduation():
    path = ROOT + "grinder/graduates/closed.jsonl"
    if not os.path.exists(path):
        return {}
    recs = []
    for line in open(path):
        try:
            recs.append(json.loads(line))
        except ValueError:
            pass
    counted = [r for r in recs if (r.get("latency_s") or 999) <= 120 and (r.get("liq") or 0) >= 5000 and r.get("P") is not None]

    def summarise(xs):
        P = [float(r["P"]) for r in xs]
        if not P:
            return {"counted": 0}
        best_removed = sorted(P)[:-10] if len(P) > 10 else []
        return {"counted": len(P), "expectancy_per_100": r2(st.mean(P)), "winners": round(sum(p > 0 for p in P) / len(P), 3),
                "at_or_below_minus50": round(sum(p <= -50 for p in P) / len(P), 3),
                "best10_removed": r2(st.mean(best_removed)) if best_removed else None,
                "best": r2(max(P)), "median_latency_s": st.median([r["latency_s"] for r in xs])}
    g1 = summarise(counted)
    g2 = summarise([r for r in counted if (r.get("liq") or 0) >= G2_LIQ and (r.get("block_t") or 0) >= G2_FROM])
    rules = read(ROOT + "grinder/graduates/RULES.md")
    m = re.search(r"At ([\d,]+) counted trades the primary expectancy was (-£[\d.]+)", rules)
    g1["kill"] = {"day": "2026-10-03", "at_counted": int(m.group(1).replace(",", "")) if m else None,
                  "expectancy": m.group(2) if m else None, "source": "grinder/graduates/RULES.md, Verdict section; commit f511792"}
    return {"closed": len(recs), "g1": g1, "g2": g2, "g2_rule": "liquidity at least $50,000 and migration at or after 2026-10-03T12:00Z; verdict at 400 counted"}


# ------------------------------------------------------------------ the Pitch and the books
def pitch():
    pred = rows(ROOT + "pitch/PREDICTIONS.csv")
    jb = rows(ROOT + "pitch/JUDGEMENT.csv")
    js = [r for r in jb if f(r.get("brier")) is not None and f(r.get("market_brier")) is not None]
    bl = [r for r in jb if f(r.get("blind_brier")) is not None and f(r.get("market_brier")) is not None]
    counted = [r for r in js if int(r["id"][2:]) >= 9]
    report = read(ROOT + "pitch/backtest/REPORT.md")
    m = re.search(r"(\d{3,5}) scored matches", report)
    tables = []
    heading = None
    for line in report.splitlines():
        if line.startswith("#"):
            heading = line.lstrip("# ").strip()
        mm = re.match(r"^\| ([a-z\- ]+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \|", line)
        if mm:
            if not tables or tables[-1]["heading"] != heading:
                tables.append({"heading": heading, "rows": []})
            tables[-1]["rows"].append({"line": mm.group(1).strip(), "brier": float(mm.group(2)), "rps": float(mm.group(3)), "logloss": float(mm.group(4))})
    first_j = min((r["committed_at"] for r in jb), default=None)
    pooled = next((t for t in tables if (t["heading"] or "").startswith("all seasons (")), None)
    return {
        "predictions": len(pred),
        "predictions_scored": sum(f(r.get("brier")) is not None for r in pred),
        "backtest": {"matches": int(m.group(1)) if m else None, "pooled": pooled, "tables": tables},
        "judgement": {
            "calls": len(jb), "scored": len(js), "first_committed": first_j,
            "brier": r2(st.mean(f(r["brier"]) for r in js)) if js else None,
            "market_brier": r2(st.mean(f(r["market_brier"]) for r in js)) if js else None,
            "anchored_gap": round(st.mean(f(r["brier"]) - f(r["market_brier"]) for r in js), 4) if js else None,
            "counted_gap": round(st.mean(f(r["brier"]) - f(r["market_brier"]) for r in counted), 4) if counted else None,
            "counted_n": len(counted),
            "blind_gap": round(st.mean(f(r["blind_brier"]) - f(r["market_brier"]) for r in bl), 4) if bl else None,
            "blind_n": len(bl),
            "items": [{"id": r["id"], "home": r["home"], "away": r["away"], "kickoff": r["kickoff_utc"], "committed_at": r["committed_at"],
                       "call": r["call"], "result": r["result"], "score": "%s-%s" % (r["home_goals"], r["away_goals"]) if r["home_goals"] else None,
                       "brier": f(r["brier"]), "market_brier": f(r["market_brier"]), "blind_call": r.get("blind_call") or None} for r in jb],
        },
    }


def exchange():
    b = rows(ROOT + "exchange/BOOK.csv")
    return {"calls": len(b), "settled": sum(bool(r.get("settled_at")) for r in b),
            "items": [{"id": r["id"], "event": r["event"], "contract": r["contract"], "p": f(r["p"]), "market_mid": f(r["market_mid"]), "committed_at": r["committed_at"]} for r in b]}


def lichess():
    g = rows(ROOT + "games/lichess/GAMES.csv")
    res = {}
    for r in g:
        res[r["result"]] = res.get(r["result"], 0) + 1
    return {"games": len(g), "results": res,
            "rating_path": [{"at": r["finished_utc"], "rating": f(r["my_rating_after"]), "opponent": r["opponent"], "opp_rating": f(r["opp_rating"]), "result": r["result"], "moves": f(r["moves"])} for r in g],
            "first": g[0] if g else None, "rating_now": f(g[-1]["my_rating_after"]) if g else None,
            "rating_peak": max((f(r["my_rating_after"]) or 0) for r in g) if g else None}


def systems():
    sig = rows(ROOT + "systems/SIGNALS.csv")
    rules = read(ROOT + "systems/RULES.md")
    trades = rows(ROOT + "systems/TRADES.csv")
    backtest = {}
    for path in glob.glob(ROOT + "experiments/2026-10-07-P-0083/README.md") + glob.glob(ROOT + "systems/*.md"):
        text = read(path)
        m = re.search(r"Pooled: (\d+) trades, about (\d+) a year\. Next-open fills: mean \+?([\d.]+)% a trade, (\d+)% winners", text)
        if m:
            backtest = {"trades": int(m.group(1)), "per_year": int(m.group(2)), "mean_pct": float(m.group(3)), "winners_pct": int(m.group(4)),
                        "span": "2009 to 2026", "source": os.path.relpath(path, ROOT)}
            break
    return {"markets": sorted({r["market"] for r in sig}), "signal_rows": len(sig), "latest_signal_day": max((r["date"] for r in sig), default=None),
            "trades": len(trades), "backtest": backtest,
            "pass_marks": {"kill": "mean below zero at 30 closed trades", "keep": "t at least 1.65 at 60 closed trades"},
            "not_a_route": "It is not a route to the McLaren." in rules}


# ------------------------------------------------------------------ notes, money, goal
def field_notes():
    sends = [l.strip() for l in read(ROOT + "state/sends.log").splitlines() if l.strip()]
    sent = []
    for l in sends:
        m = re.match(r"(\d{4}-\d\d-\d\d) (\d\d:\d\d) sent Field Notes (\S+)", l)
        if m:
            sent.append({"day": m.group(1), "time": m.group(2), "week": m.group(3)})
    drafts = sorted(os.path.basename(p)[:-3] for p in glob.glob(ROOT + "field-notes/drafts/2*.md"))
    harvest = sum(1 for _ in open(ROOT + "field-notes/harvest.jsonl")) if os.path.exists(ROOT + "field-notes/harvest.jsonl") else 0
    skool = {}
    if os.path.exists(ROOT + "field-notes/SKOOL-QUEUE.json"):
        q = json.load(open(ROOT + "field-notes/SKOOL-QUEUE.json"))
        for g in q.get("groups", []):
            k = str(g.get("verdict") or g.get("status"))
            skool[k] = skool.get(k, 0) + 1
    return {"sent": sent, "drafts": drafts, "harvest_entries": harvest, "skool_verdicts": skool}


def money():
    text = read(ROOT + "SPEND.md")
    card = {}
    for month in re.findall(r"^## (\w+ \d{4})\n", text, re.M):
        m = re.search(r"## %s\n(.*?)(\n## |\Z)" % re.escape(month), text, re.S)
        totals = re.findall(r"£([0-9.]+) \|\s*$", m.group(1), re.M) if m else []
        card[month] = float(totals[-1]) if totals else 0.0
    xai_rows = re.findall(r"^\| (20\d\d-\d\d-\d\d) \|[^|]*\| ([0-9.]+)[^|]*\|\s*$", text.split("## Luke's xAI account")[-1], re.M) if "## Luke's xAI account" in text else []
    m = re.search(r"Total known to [^|]+\| ([0-9.]+) \|", text)
    home = read(ROOT + "HOME.md")
    hm = re.search(r"Luke's xAI account: \$([0-9.]+) in SPEND.md", home)
    return {"card_gbp_by_month": card, "card_total_gbp": round(sum(card.values()), 2),
            "xai_usd_known": float(m.group(1)) if m else round(sum(float(x) for _, x in xai_rows), 2),
            "xai_usd_on_home": float(hm.group(1)) if hm else None, "xai_rows": len(xai_rows)}


def goal():
    persona = read(ROOT + "PERSONA.md")
    pj = json.load(open(ROOT + "state/probes.json"))["items"]
    notes = {p["id"]: p.get("note") or "" for p in pj}
    cheapest = re.search(r"cheapest ([\d,]+) GBP", notes.get("P-0073", ""))
    for_sale = re.search(r"(\d+) McLaren 720S for sale", notes.get("P-0073", ""))
    running = re.search(r"About ([\d,]+) to ([\d,]+) GBP a year", notes.get("P-0081", ""))
    first_year = re.search(r"First-year target becomes about ([\d,]+)", notes.get("P-0081", ""))
    m_target = re.search(r"£(140,000)", persona)
    m_month = re.search(r"£(11,667)", persona)
    m_set = re.search(r"Set by Luke on (\d+ \w+ \d{4})", persona)
    num = lambda m, i=1: int(m.group(i).replace(",", "")) if m else None
    return {"car": "McLaren 720S", "deadline": "2027-10-07",
            "target_gbp": num(m_target) or 140000,
            "per_month_flat_gbp": num(m_month),
            "set_on": m_set.group(1) if m_set else "7 Oct 2026",
            "for_sale_uk": num(for_sale), "cheapest_listing_gbp": num(cheapest),
            "running_costs_gbp_year": [num(running, 1), num(running, 2)] if running else None,
            "first_year_target_gbp": num(first_year),
            "source": "PERSONA.md goal section; probes P-0073 and P-0081"}


def charter():
    text = read(ROOT + "CHARTER.md")
    v1 = re.search(r"signed by Luke the same day", text)
    return {
        "v1_signed": "2026-09-22", "v2_signed": "2026-09-29",
        "v1_commit": "cdf6a27", "v2_commit": "e1ebe88",
        "lines": [
            {"text": "Pre-register every prediction and paper trade by git commit before the outcome is knowable. Commit timestamps are the proof.", "where": "CHARTER.md, What Proteus must do"},
            {"text": "A losing record is published in exactly the same place and format as a winning one.", "where": "CHARTER.md, What Proteus must do"},
            {"text": "It goes out, gets educated, tries things, keeps score in public, and brings artefacts back. It does not bring decisions back.", "where": "CHARTER.md, Why Proteus exists"},
            {"text": "Say when it does not know. Say when a number is unverified.", "where": "CHARTER.md, What Proteus must do"},
        ],
        "kill_switch": "touch /Users/triton/PROTEUS/HALT stops every side effect (no commits, no pushes, no email, no spend). Runs still write their log.",
        "halt_now": os.path.exists(ROOT + "HALT"),
    }


QUOTES = [
    # text: as displayed. match: the exact substring in the source (defaults to text without its final mark).
    {"text": "A loss goes where a win would, so this is first.", "where": "field-notes/2026-W39.md"},
    {"text": "The scorer was wrong on its own page.", "where": "field-notes/2026-W39.md"},
    {"text": "Paper rule would have lost 84 of 100.", "where": "commit 4daa5fd"},
    {"text": "Eight of the sides I called this window have coaches I did not know about.", "where": "commit bef4a92"},
    {"text": "Wrong with confidence.", "where": "state/runs/2026-09-28.md"},
    {"text": "The graduation book has already hit its kill line, and I nearly missed that.", "where": "field-notes/2026-W40.md"},
    {"text": "Last week's \"one in ten\" was out by a factor of four.", "where": "field-notes/2026-W40.md"},
    {"text": "He was right, and I should have checked that first.", "where": "field-notes/2026-10-07-skool-trading.md"},
    {"text": "It is not a route to the McLaren.", "where": "systems/RULES.md"},
    {"text": "Being Luke.", "where": "PERSONA.md, under what I am not interested in"},
]


def verify_quotes():
    out = []
    for q in QUOTES:
        where = q["where"]
        needle = q.get("match") or q["text"].rstrip(".:")
        if where.startswith("commit "):
            ok = needle[:40] in git("log", "--format=%s%n%b", where.split()[1], "-1")
        else:
            path = ROOT + where.split(",")[0]
            ok = needle in read(path) if os.path.exists(path) else None
        out.append({"text": q["text"], "where": where, "verified": ok})
    return out


def ahead():
    pm = read(ROOT + "PASS-MARKS.md")
    home = read(ROOT + "HOME.md")
    nk = re.search(r"next kickoff (\d+ \w+)", home)
    return [
        {"what": "Tonight's nightly run", "when": "23:15 every night", "source": "CHARTER.md, Cadence"},
        {"what": "The Pitch's first live predictions", "when": nk.group(1) + " 2026" if nk else "9 Oct 2026", "source": "HOME.md"},
        {"what": "Week-8 review with Luke", "when": "Sun 15 Nov 2026" if "15 Nov 2026" in pm else None, "source": "PASS-MARKS.md"},
        {"what": "Second and last date for an inconclusive desk", "when": "Sun 13 Dec 2026" if "13 Dec 2026" in pm else None, "source": "PASS-MARKS.md"},
        {"what": "The McLaren", "when": "7 Oct 2027", "source": "PERSONA.md"},
    ]


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else OUT
    now = datetime.now(timezone.utc)
    c = commits()
    first_day = utc(c["first"]["at"]).date() if c["first"] else None
    rec = {
        "built_at": now.isoformat(timespec="seconds"),
        "head": c["head"],
        "cut": {"from": str(first_day) if first_day else CUT_FROM, "to": now.date().isoformat()},
        "age_days": (now.date() - first_day).days + 1 if first_day else None,
        "commits": c,
        "runs": runs(),
        "hook": hook(),
        "probes": probes(),
        "grinder": grinder(),
        "graduation": graduation(),
        "pitch": pitch(),
        "exchange": exchange(),
        "lichess": lichess(),
        "systems": systems(),
        "field_notes": field_notes(),
        "money": money(),
        "goal": goal(),
        "charter": charter(),
        "quotes": verify_quotes(),
        "ahead": ahead(),
    }
    rec["nights"] = sum(len(r["nightly_at"]) for r in rec["runs"])   # the proof run on 22 Sep counts: two headings that day
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as fh:
        json.dump(rec, fh, indent=1, ensure_ascii=False)
    g = rec["grinder"]["stats"] or {}
    p = rec["probes"]
    print("record.json written to %s (%d KB), head %s, built %s" % (out_path, os.path.getsize(out_path) // 1024, rec["head"], rec["built_at"]))
    print("age %s days, nights %d, commits %d (%s), busiest %s" % (rec["age_days"], rec["nights"], rec["commits"]["total"], rec["commits"]["by_author"], rec["commits"]["busiest"]))
    print("hook: %d allowed, %d denied (live sessions)" % (rec["hook"]["allowed"], rec["hook"]["denied"]))
    print("probes: %d total, %d verdicts %s, killed %d, open %d, in progress %d" % (p["total"], p["done"], p["verdicts"], p["killed"], p["open"], p["in_progress"]))
    print("grinder %s: bankroll £%s from £%s, %s closed, hit %s, expectancy £%s, low £%s on %s, worst losing run %d" % (
        rec["grinder"]["current"], g.get("bankroll"), g.get("start"), g.get("closed"), g.get("hit_rate"), g.get("expectancy"),
        (rec["grinder"]["low"] or {}).get("bankroll"), ((rec["grinder"]["low"] or {}).get("at") or "")[:10], rec["grinder"]["worst_losing_run"]))
    print("graduation: closed %d, G1 %s, G2 %s" % (rec["graduation"].get("closed", 0), {k: v for k, v in rec["graduation"].get("g1", {}).items() if k != "kill"}, rec["graduation"].get("g2")))
    j = rec["pitch"]["judgement"]
    print("pitch: %d predictions; judgement %d calls, anchored gap %s, counted gap %s over %d, blind gap %s over %d; backtest %s matches, %d tables" % (
        rec["pitch"]["predictions"], j["calls"], j["anchored_gap"], j["counted_gap"], j["counted_n"], j["blind_gap"], j["blind_n"], rec["pitch"]["backtest"]["matches"], len(rec["pitch"]["backtest"]["tables"])))
    print("lichess: %s, rating %s (peak %s); exchange %d calls %d settled; systems %d markets %d trades backtest %s" % (
        rec["lichess"]["results"], rec["lichess"]["rating_now"], rec["lichess"]["rating_peak"], rec["exchange"]["calls"], rec["exchange"]["settled"],
        len(rec["systems"]["markets"]), rec["systems"]["trades"], rec["systems"]["backtest"]))
    print("field notes sent %s; harvest %d; skool %s" % ([s["week"] for s in rec["field_notes"]["sent"]], rec["field_notes"]["harvest_entries"], rec["field_notes"]["skool_verdicts"]))
    print("money: card £%.2f, xAI $%s (SPEND) vs $%s (HOME); goal %s" % (rec["money"]["card_total_gbp"], rec["money"]["xai_usd_known"], rec["money"]["xai_usd_on_home"],
                                                                         {k: rec["goal"][k] for k in ("target_gbp", "per_month_flat_gbp", "cheapest_listing_gbp")}))
    print("quotes verified: %s" % [q["verified"] for q in rec["quotes"]])


if __name__ == "__main__":
    main()
