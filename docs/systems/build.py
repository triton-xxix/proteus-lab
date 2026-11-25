"""Build docs/systems/index.html and data.json from the systems book's own append-only files.

"The two books": the paper index-ETF books started 7 Oct 2026, each set against the three questions
Luke asked of trading work on 7 Oct: does it make money, does it beat holding, does it beat luck.
Every number is computed here from systems/EVENTS.csv and systems/SIGNALS.csv through systems.py's
own trades() and summary(); nothing is typed. Exits non-zero if the page's counts disagree with
systems.verdict() or verdict2(), the lines the kill check prints every night.

python3 /Users/triton/PROTEUS/docs/systems/build.py
"""
import json
import os
import random
import re
import statistics
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "systems"))
import systems as S  # noqa: E402

EVENTS = S.read(S.EVENTS)
SIG = S.read(S.SIGNALS)
COST = S.B2_COST
SHUFFLES, SEED = 10000, 20261120
bad = []

# ---------- sessions per market: date -> (open, close) ----------
sess = {m: [] for m in S.BASKET}
for r in SIG:
    if r["market"] in sess:
        sess[r["market"]].append((r["date"], float(r["open"]), float(r["close"])))
for m in sess:
    sess[m].sort()
idx = {m: {d: i for i, (d, _, _) in enumerate(sess[m])} for m in sess}
last_date = max(s[-1][0] for s in sess.values())
for m in S.BASKET:
    if sess[m][-1][0] != last_date:
        bad.append(f"{m} last session {sess[m][-1][0]} v {last_date}")


def book(strat, cost):
    tr, openp = S.trades(EVENTS, strat, "next_open")
    rows = [{"market": m, "in": d0, "out": d1, "r": r - cost,
             "k": idx[m][d1] - idx[m][d0]} for m, d0, d1, r in tr]
    opens = []
    for m, (d0, p0) in sorted(openp.items()):
        c = sess[m][-1][2]
        opens.append({"market": m, "in": d0, "r_marked": c / p0 - 1 - cost, "days": len(sess[m]) - 1 - idx[m][d0]})
    return rows, opens


B1, B1_OPEN = book("rsi5_simple", 0.0)
B2, B2_OPEN = book(S.BOOK2, COST)

# ---------- agree with the nightly kill-check lines ----------
for rows, line, what in ((B1, S.verdict(), "book 1"), (B2, S.verdict2(), "book 2")):
    n, m, w, t = S.summary([x["r"] for x in rows])
    got = re.search(r"(\d+) closed, mean (?:after costs )?([+-][\d.]+)%, win (\d+)%, t (-?[\d.]+)", line)
    if not got:
        bad.append(f"{what}: verdict line unreadable: {line}")
        continue
    if int(got.group(1)) != n or f"{m:+.2%}" != got.group(2) + "%" or f"{w:.0%}" != got.group(3) + "%" or f"{t:.2f}" != got.group(4):
        bad.append(f"{what}: page {n} {m:+.2%} {w:.0%} {t:.2f} v verdict {got.groups()}")
WORD1 = re.search(r": ([A-Z]+[^.]*)\.", S.verdict()).group(1)
WORD2 = re.search(r": ([A-Z]+[^.]*)\.", S.verdict2()).group(1)


# ---------- beats holding: nine equal sleeves from the book's first fill session ----------
def sleeves(rows, opens, start):
    out = {}
    for m in S.BASKET:
        g = 1.0
        for x in rows:
            if x["market"] == m:
                g *= 1 + x["r"]
        g_marked = g
        for x in opens:
            if x["market"] == m:
                g_marked *= 1 + x["r_marked"]
        i0 = idx[m][start]
        hold = sess[m][-1][2] / sess[m][i0][1] - 1
        out[m] = {"closed": g - 1, "marked": g_marked - 1, "hold": hold}
    return out


START2 = min(x["in"] for x in B2 + B2_OPEN)
START1 = min(x["in"] for x in B1 + B1_OPEN)
SL2 = sleeves(B2, B2_OPEN, START2)
SL1 = sleeves(B1, B1_OPEN, START1)


def avg(d, k):
    return statistics.mean(v[k] for v in d.values())


# ---------- beats luck: same markets, same holding lengths, random entry sessions ----------
def luck(rows, cost):
    rng = random.Random(SEED)
    obs = statistics.mean(x["r"] for x in rows)
    ge = 0
    means = []
    for _ in range(SHUFFLES):
        tot = 0.0
        for x in rows:
            s = sess[x["market"]]
            i = rng.randrange(0, len(s) - x["k"])
            tot += s[i + x["k"]][1] / s[i][1] - 1 - cost
        mm = tot / len(rows)
        means.append(mm)
        ge += mm >= obs
    means.sort()
    return {"observed": obs, "ge": ge, "p": (ge + 1) / (SHUFFLES + 1), "random_median": statistics.median(means),
            "random_p95": means[int(0.95 * SHUFFLES)], "means": means}


L2 = luck(B2, COST)
L1 = luck(B1, 0.0)


# ---------- by calendar week of exit (RULES.md's own honest limit) ----------
def weeks(rows):
    wk = {}
    for x in rows:
        y, w, _ = date.fromisoformat(x["out"]).isocalendar()
        wk.setdefault(f"{y}-W{w:02d}", []).append(x["r"])
    return {k: (len(v), statistics.mean(v)) for k, v in sorted(wk.items())}


W2 = weeks(B2)
wk_means = [m for _, m in W2.values()]
wk_pos = sum(1 for m in wk_means if m > 0)
wk_t = statistics.mean(wk_means) / (statistics.stdev(wk_means) / len(wk_means) ** 0.5) if len(wk_means) > 1 else float("nan")

if bad:
    for b in bad:
        print("DISAGREE", b)
    sys.exit(1)

n2, m2, w2, t2 = S.summary([x["r"] for x in B2])
n1, m1, w1, t1 = S.summary([x["r"] for x in B1])
book2_closed, book2_marked, hold2 = avg(SL2, "closed"), avg(SL2, "marked"), avg(SL2, "hold")
book1_closed, book1_marked, hold1 = avg(SL1, "closed"), avg(SL1, "marked"), avg(SL1, "hold")
open2_mean = statistics.mean(x["r_marked"] for x in B2_OPEN) if B2_OPEN else float("nan")
open2_down = sum(1 for x in B2_OPEN if x["r_marked"] < 0)
best = max(B2, key=lambda x: x["r"])
worst = min(B2, key=lambda x: x["r"])
mean_k = statistics.mean(x["k"] for x in B2)
us = [x["r"] for x in B2 if x["market"] in ("SPY", "QQQ", "DIA", "IWM")]
ex = [x["r"] for x in B2 if x["market"] not in ("SPY", "QQQ", "DIA", "IWM")]


def pc(v, d=2):
    return f"{v*100:+.{d}f}%"


def yes(b):
    return "yes" if b else "no"


verdicts = {
    "book2": {"money": m2 > 0, "holding": book2_marked > hold2, "luck": L2["p"] < 0.05},
    "book1": {"money": m1 > 0, "holding": book1_marked > hold1, "luck": L1["p"] < 0.05},
}

data = {
    "built_from": ["systems/EVENTS.csv", "systems/SIGNALS.csv", "systems/systems.py"],
    "last_session": last_date,
    "book2": {"closed": n2, "mean_after_cost": round(m2, 6), "win": round(w2, 4), "t": round(t2, 3), "word": WORD2,
              "open": len(B2_OPEN), "open_down": open2_down, "open_mean_marked": round(open2_mean, 6),
              "sleeves_closed": round(book2_closed, 6), "sleeves_marked": round(book2_marked, 6), "hold": round(hold2, 6),
              "luck_p": round(L2["p"], 4), "random_median": round(L2["random_median"], 6), "weeks": len(W2),
              "weeks_positive": wk_pos, "week_t": round(wk_t, 3), "start": START2},
    "book1": {"closed": n1, "mean": round(m1, 6), "win": round(w1, 4), "t": round(t1, 3), "word": WORD1,
              "open": len(B1_OPEN), "sleeves_marked": round(book1_marked, 6), "hold": round(hold1, 6),
              "luck_p": round(L1["p"], 4), "random_median": round(L1["random_median"], 6), "start": START1},
    "verdicts": verdicts, "shuffles": SHUFFLES, "seed": SEED, "cost_round_trip": COST,
}
with open(os.path.join(HERE, "data.json"), "w") as f:
    json.dump(data, f, indent=1)
    f.write("\n")
HIST = os.path.join(HERE, "history")
os.makedirs(HIST, exist_ok=True)
with open(os.path.join(HIST, f"{last_date}.json"), "w") as f:
    json.dump(data, f, indent=1)
    f.write("\n")

# ---------- then and now: every earlier build's headline, re-derived from today's trades ----------
SNAPS = []
for fn in sorted(os.listdir(HIST)):
    if not fn.endswith(".json"):
        continue
    sd = json.load(open(os.path.join(HIST, fn)))
    sub = [x["r"] for x in B2 if x["out"] <= sd["last_session"]]
    sn, sm, sw, st = S.summary(sub)
    b = sd["book2"]
    if sn != b["closed"] or round(sm, 6) != b["mean_after_cost"] or round(sw, 4) != b["win"]:
        print("DISAGREE", f"snapshot {fn}: page said {b['closed']} {b['mean_after_cost']} {b['win']}, trades now give {sn} {sm:.6f} {sw:.4f}")
        sys.exit(1)
    SNAPS.append({"session": sd["last_session"], "closed": sn, "mean": sm, "win": sw, "t": st,
                  "sleeves": b["sleeves_marked"], "hold": b["hold"], "luck_p": b["luck_p"]})
SNAP0 = SNAPS[0]
since = [x for x in B2 if x["out"] > SNAP0["session"]]
since_mean = statistics.mean(x["r"] for x in since) if since else float("nan")
since_win = sum(1 for x in since if x["r"] > 0)

MCOL = {"SPY": "--tide", "QQQ": "--tide", "DIA": "--tide", "IWM": "--tide"}


# ---------- chart 1: every closed book-2 trade, in exit order, with the running total ----------
def chart_trades():
    rows = sorted(B2, key=lambda x: (x["out"], x["market"]))
    W, H, L, R, T, B = 760, 300, 54, 20, 18, 46
    lo = min(-0.02, min(x["r"] for x in rows) - 0.004)
    run = []
    s = 0.0
    for x in rows:
        s += x["r"]
        run.append(s)
    hi = max(max(run), max(x["r"] for x in rows)) + 0.01
    bw = (W - L - R) / len(rows)
    xx = lambda i: L + i * bw + bw / 2
    y = lambda v: T + (hi - v) / (hi - lo) * (H - T - B)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Each of {len(rows)} closed book 2 trades after cost, in exit order, with the running sum">']
    g = -0.02
    while g <= hi:
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(g):.1f}" y2="{y(g):.1f}" stroke="var(--rule)"{" stroke-width=\"2\"" if abs(g) < 1e-9 else ""}/>')
        out.append(f'<text x="{L-8}" y="{y(g)+4:.1f}" text-anchor="end">{g*100:+.0f}%</text>')
        g = round(g + 0.04, 4)
    for i, x in enumerate(rows):
        col = "var(--tide)" if x["r"] > 0 else "var(--buoy)"
        y0, y1 = sorted([y(0), y(x["r"])])
        out.append(f'<rect class="bar" x="{xx(i)-bw*0.35:.1f}" y="{y0:.1f}" width="{bw*0.7:.1f}" height="{max(y1-y0,1.5):.1f}" fill="{col}"><title>{x["market"]} in {x["in"]} out {x["out"]}: {pc(x["r"])} after cost</title></rect>')
    pts = " ".join(f"{xx(i):.1f},{y(v):.1f}" for i, v in enumerate(run))
    out.append(f'<polyline points="{pts}" fill="none" stroke="var(--gold)" stroke-width="2.4"/>')
    out.append(f'<text class="k" x="{xx(len(rows)-1)-6:.1f}" y="{y(run[-1])-8:.1f}" text-anchor="end">running sum {pc(run[-1],1)}</text>')
    out.append(f'<text x="{L}" y="{H-24}">{rows[0]["out"]}</text>')
    out.append(f'<text x="{W-R}" y="{H-24}" text-anchor="end">{rows[-1]["out"]}</text>')
    out.append(f'<text x="{(L+W-R)/2:.1f}" y="{H-6}" text-anchor="middle">closed trades in the order they were sold; each bar after the 0.05% cost</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 0: the running mean, with each page build marked ----------
def chart_mean():
    rows = sorted(B2, key=lambda x: (x["out"], x["market"]))
    W, H, L, R, T, B = 760, 280, 54, 20, 22, 46
    rm, s = [], 0.0
    for i, x in enumerate(rows):
        s += x["r"]
        rm.append(s / (i + 1))
    lo = min(min(rm), 0, 0.0022) - 0.004
    hi = max(max(rm), 0.0022) + 0.004
    step = (W - L - R) / max(len(rows) - 1, 1)
    xx = lambda i: L + i * step
    y = lambda v: T + (hi - v) / (hi - lo) * (H - T - B)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Book 2 mean trade after cost as each of {len(rows)} trades closed, with the page builds marked">']
    g = round(lo * 100) / 100
    while g <= hi:
        if g >= lo:
            out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(g):.1f}" y2="{y(g):.1f}" stroke="var(--rule)"{" stroke-width=\"2\"" if abs(g) < 1e-9 else ""}/>')
            out.append(f'<text x="{L-8}" y="{y(g)+4:.1f}" text-anchor="end">{g*100:+.0f}%</text>')
        g = round(g + 0.01, 4)
    out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(0.0022):.1f}" y2="{y(0.0022):.1f}" stroke="var(--gold)" stroke-dasharray="5 4"/>')
    out.append(f'<text x="{W-R}" y="{y(0.0022)-6:.1f}" text-anchor="end">backtest +0.22%</text>')
    pts = " ".join(f"{xx(i):.1f},{y(v):.1f}" for i, v in enumerate(rm))
    out.append(f'<polyline points="{pts}" fill="none" stroke="var(--tide)" stroke-width="2.4"/>')
    for i, v in enumerate(rm):
        out.append(f'<circle class="rm" cx="{xx(i):.1f}" cy="{y(v):.1f}" r="2.6" fill="var(--tide)"><title>after trade {i+1} ({rows[i]["market"]} out {rows[i]["out"]}): mean {pc(v)}</title></circle>')
    for j, sp in enumerate(SNAPS):
        i = sp["closed"] - 1
        anchor = "end" if i >= len(rows) - 3 else "middle"
        dy = -12 if j % 2 == 0 else 22
        out.append(f'<circle class="snap" cx="{xx(i):.1f}" cy="{y(rm[i]):.1f}" r="7" fill="none" stroke="var(--buoy)" stroke-width="2.2"/>')
        out.append(f'<text class="k" x="{xx(i):.1f}" y="{y(rm[i])+dy:.1f}" text-anchor="{anchor}">page of {sp["session"]}: {pc(sp["mean"])}</text>')
    out.append(f'<text x="{L}" y="{H-24}">trade 1</text>')
    out.append(f'<text x="{W-R}" y="{H-24}" text-anchor="end">trade {len(rows)}</text>')
    out.append(f'<text x="{(L+W-R)/2:.1f}" y="{H-6}" text-anchor="middle">mean of all closed trades so far, after cost, as each one was sold</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 2: book v holding, market by market ----------
def chart_holding():
    W, L, R, T = 760, 60, 90, 26
    H = T + len(S.BASKET) * 28 + 40
    vals = [v for d in SL2.values() for v in (d["marked"], d["hold"])]
    lo, hi = min(vals + [0]) - 0.01, max(vals + [0]) + 0.01
    x = lambda v: L + (v - lo) / (hi - lo) * (W - L - R)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="For each of nine markets, book 2 with open trades marked against holding the market over the same weeks">']
    g = round(lo * 50) / 50
    while g <= hi:
        out.append(f'<line x1="{x(g):.1f}" x2="{x(g):.1f}" y1="{T-8}" y2="{H-34}" stroke="var(--rule)"{" stroke-width=\"2\"" if abs(g) < 1e-9 else ""}/>')
        out.append(f'<text x="{x(g):.1f}" y="{H-18}" text-anchor="middle">{g*100:+.0f}%</text>')
        g = round(g + 0.02, 4)
    for i, m in enumerate(S.BASKET):
        d = SL2[m]
        yy = T + 8 + i * 28
        out.append(f'<text x="{L-10}" y="{yy+4}" text-anchor="end">{m}</text>')
        out.append(f'<line x1="{x(d["hold"]):.1f}" x2="{x(d["marked"]):.1f}" y1="{yy}" y2="{yy}" stroke="var(--ghost)" stroke-width="3"/>')
        out.append(f'<circle class="hold" cx="{x(d["hold"]):.1f}" cy="{yy}" r="6" fill="var(--ghost)" stroke="var(--muted)"><title>{m} held: {pc(d["hold"])}</title></circle>')
        out.append(f'<circle class="mark" cx="{x(d["marked"]):.1f}" cy="{yy}" r="6" fill="var(--tide)"><title>{m} book 2, open trades marked: {pc(d["marked"])} (closed only {pc(d["closed"])})</title></circle>')
        out.append(f'<text class="k" x="{W-R+10}" y="{yy+4}">{(d["marked"]-d["hold"])*100:+.1f} pts</text>')
    out.append(f'<text x="{(L+W-R)/2:.1f}" y="{H-2}" text-anchor="middle">grey: held from the {START2} open; blue: the book, open trades marked at the {last_date} close</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 3: the luck test ----------
def chart_luck():
    W, H, L, R, T, B = 760, 230, 20, 20, 24, 44
    ms = L2["means"]
    lo, hi = min(ms[0], 0) - 0.001, max(ms[-1], L2["observed"]) + 0.002
    nb = 48
    step = (hi - lo) / nb
    cnt = [0] * nb
    for v in ms:
        cnt[min(int((v - lo) / step), nb - 1)] += 1
    top = max(cnt)
    x = lambda v: L + (v - lo) / (hi - lo) * (W - L - R)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{SHUFFLES:,} random books with the same markets and holding lengths, against the real book">']
    for i, c in enumerate(cnt):
        h = c / top * (H - T - B)
        out.append(f'<rect class="bin" x="{x(lo+i*step)+0.5:.1f}" y="{H-B-h:.1f}" width="{(W-L-R)/nb-1:.1f}" height="{h:.1f}" fill="var(--ghost)"/>')
    out.append(f'<line x1="{L}" x2="{W-R}" y1="{H-B}" y2="{H-B}" stroke="var(--rule)" stroke-width="2"/>')
    g = round(lo * 100) / 100
    while g <= hi:
        if g >= lo:
            out.append(f'<text x="{x(g):.1f}" y="{H-B+18}" text-anchor="middle">{g*100:+.0f}%</text>')
        g = round(g + 0.005, 4)
    xo = x(L2["observed"])
    out.append(f'<line x1="{xo:.1f}" x2="{xo:.1f}" y1="{T}" y2="{H-B}" stroke="var(--buoy)" stroke-width="2.4"/>')
    out.append(f'<text class="k" x="{xo-8:.1f}" y="{T+12}" text-anchor="end">the real book {pc(L2["observed"])}</text>')
    out.append(f'<text x="{(L+W-R)/2:.1f}" y="{H-6}" text-anchor="middle">mean trade after cost, {SHUFFLES:,} books of random entry days</text>')
    out.append("</svg>")
    return "\n".join(out)


trade_rows = "\n".join(
    f'<tr><td>{x["market"]}</td><td>{x["in"]}</td><td>{x["out"]}</td><td class="n">{x["k"]}</td><td class="n {"up" if x["r"] > 0 else "dn"}">{pc(x["r"])}</td></tr>'
    for x in sorted(B2, key=lambda x: (x["out"], x["market"])))
open_rows = "\n".join(
    f'<tr><td>{x["market"]}</td><td>{x["in"]}</td><td>still open</td><td class="n">{x["days"]}</td><td class="n {"up" if x["r_marked"] > 0 else "dn"}">{pc(x["r_marked"])} marked</td></tr>'
    for x in B2_OPEN)
week_rows = "\n".join(f'<tr><td>{k}</td><td class="n">{n}</td><td class="n {"up" if m > 0 else "dn"}">{pc(m)}</td></tr>' for k, (n, m) in W2.items())


if m2 > 0.0022 * 1.5:
    pace = f", so it is running at {m2/0.0022:.1f} times what 2009 to 2026 says to expect, which says luck is doing some of the work"
elif m2 > 0:
    pace = ", so it is in the backtest's range"
else:
    pace = f", so it is below zero and below what 2009 to 2026 says to expect, by {(0.0022-m2)*100:.2f} points a trade"
if B2_OPEN:
    open_line = (f"Right now {len(B2_OPEN)} of the nine sleeves hold a position, {open2_down} of them under water at the {last_date} close "
                 f"(mean {pc(open2_mean)} marked). Those trades are not in the scored mean until they close.")
else:
    open_line = f"Right now no sleeve holds a position; every trade is closed and scored."
fall = ", because these were falling weeks" if L2["random_median"] < 0 else ""
d_mean = m2 - SNAP0["mean"]
then_now = []
for sp in SNAPS:
    then_now.append(f'<tr><td>{sp["session"]}</td><td class="n">{sp["closed"]}</td><td class="n {"up" if sp["mean"] > 0 else "dn"}">{pc(sp["mean"])}</td>'
                    f'<td class="n">{sp["win"]:.0%}</td><td class="n">{sp["t"]:.2f}</td><td class="n">{pc(sp["sleeves"])} v {pc(sp["hold"])}</td><td class="n">{sp["luck_p"]:.4f}</td></tr>')
then_now = "\n".join(then_now)
if since:
    since_line = (f"The {len(since)} trades closed since the {SNAP0['session']} page averaged {pc(since_mean)} ({since_win} of {len(since)} winners), "
                  f"and moved the book's mean from {pc(SNAP0['mean'])} to {pc(m2)}, {d_mean*100:+.2f} points.")
else:
    since_line = f"No trade has closed since the {SNAP0['session']} page."


def cell(b):
    return f'<td class="v {"up" if b else "dn"}">{yes(b)}</td>'


three = f"""<tr><th>book</th><th>makes money</th><th>beats holding</th><th>beats luck</th></tr>
<tr><td>2: IBS below 0.2</td>{cell(verdicts['book2']['money'])}{cell(verdicts['book2']['holding'])}{cell(verdicts['book2']['luck'])}</tr>
<tr><td>1: RSI(5) dip</td>{cell(verdicts['book1']['money'])}{cell(verdicts['book1']['holding'])}{cell(verdicts['book1']['luck'])}</tr>"""

stats = [
    ("hot", f"{n2} closed", f"book 2 trades since {START2}; {S.B2_KILL_FROM - n2} more before its first kill line"),
    ("hot", pc(m2), f"mean trade after a 0.05% round trip, {w2:.0%} winners (backtest +0.22% after cost)"),
    ("", f"t {t2:.2f}", f"on trades; {wk_t:.2f} on its {len(W2)} weekly means, which is the fairer figure"),
    ("", f"{open2_down} of {len(B2_OPEN)}", f"open trades under water at the {last_date} close, mean {pc(open2_mean)}"),
    ("", f"{L2['ge']:,} of {SHUFFLES:,}", f"random-entry books in the same weeks that did as well (median {pc(L2['random_median'])})"),
]
stat_html = "\n".join(f'<div class="stat {k}"><b>{b}</b><span>{s}</span></div>' for k, b, s in stats)

CSS = """
:root{
  --paper:#ece9e2; --raised:#f6f4ef; --ink:#1d1a16; --muted:#625b51; --rule:#d2ccc0;
  --tide:#2a6a73; --buoy:#b8402b; --ghost:#b9b2a5; --gold:#9a7a1c;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --paper:#16140f; --raised:#1f1c17; --ink:#ece7dd; --muted:#a59d90; --rule:#38332b;
  --tide:#6bc0c8; --buoy:#ec8a72; --ghost:#4d473e; --gold:#d9b85a;
}}
:root[data-theme="dark"]{
  --paper:#16140f; --raised:#1f1c17; --ink:#ece7dd; --muted:#a59d90; --rule:#38332b;
  --tide:#6bc0c8; --buoy:#ec8a72; --ghost:#4d473e; --gold:#d9b85a;
}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 Georgia,"Iowan Old Style",serif}
main{max-width:860px;margin:0 auto;padding:28px 16px 64px}
a{color:var(--tide)}
.kicker{font:600 12px/1.2 ui-monospace,Menlo,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
h1{font-size:clamp(28px,6vw,44px);line-height:1.1;margin:.3em 0 .4em}
h2{font-size:20px;margin:2.2em 0 .5em}
p{max-width:64ch}
code{font:13px ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:22px 0}
.stat{background:var(--raised);border:1px solid var(--rule);border-radius:8px;padding:12px 14px}
.stat b{display:block;font:600 21px/1.15 ui-monospace,Menlo,monospace}
.stat span{font-size:13px;color:var(--muted)}
.stat.hot b{color:var(--tide)}
.chart{background:var(--raised);border:1px solid var(--rule);border-radius:8px;padding:12px 10px 6px;overflow-x:auto}
svg{display:block;width:100%;min-width:560px;height:auto}
svg text{font:12px ui-monospace,Menlo,monospace;fill:var(--muted)}
svg text.k{fill:var(--ink)}
.note{font-size:14px;color:var(--muted)}
ul{max-width:64ch}
table{border-collapse:collapse;width:100%;font:13px/1.4 ui-monospace,Menlo,monospace}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--rule);white-space:nowrap}
th{color:var(--muted);font-weight:600}
td.n,th.n{text-align:right}
td.up{color:var(--tide)} td.dn{color:var(--buoy)}
td.v{font-weight:600;font-size:15px}
details summary{cursor:pointer;color:var(--tide);margin:10px 0}
"""

GH = "https://github.com/triton-xxix/proteus-lab/blob/main/systems/"
desc = (f"Two paper books on nine index ETFs since October 2026. Book 2 (IBS below 0.2): {n2} closed trades, "
        f"{pc(m2)} a trade after cost, {w2:.0%} winners; held against the market and against {SHUFFLES:,} random books.")

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Two Books</title>
<meta name="description" content="{desc}">
<style>{CSS}</style>
</head>
<body>
<main>
<div class="kicker">Proteus systems book · paper only · nine index ETFs · last session {last_date}</div>
<h1>The two books</h1>
<p>On 7 Oct I put two dip-buying rules on paper, on nine index funds (SPY, QQQ, DIA, IWM, EFA, EEM, EWU, EWJ, EWG), with the pass marks written down before the first trade. Every signal is appended to a file and committed before the next open, so none of it can be fitted after the fact. Book 1 buys an RSI(5) dip inside an uptrend. Book 2 buys when a day closes in its bottom fifth (IBS below 0.2) and book 1 is flat, and sells when a close beats the day before's high. This page asks each the three questions: does it make money, does it beat holding, does it beat luck.</p>

<div class="stats">
{stat_html}
</div>

<div class="chart"><table>
{three}
</table></div>
<p class="note">Money: mean closed trade above zero (book 2 after cost). Holding: nine equal sleeves, open trades marked at the last close, against holding all nine from the book's first fill. Luck: fewer than 5% of {SHUFFLES:,} random books did as well. None of these is the pre-registered verdict. That is the kill check's word, tonight: book 2 <b>{WORD2}</b>, book 1 <b>{WORD1}</b>.</p>

<h2>0. Then and now</h2>
<p class="note">This page was first built on the {SNAP0['session']} close. Each build keeps its headline in <a href="https://github.com/triton-xxix/proteus-lab/tree/main/docs/systems/history">history/</a>; the circles mark where each build stood. Every point is re-derived from today's trade file, and the build stops if an old page's figures no longer come out of it.</p>
<div class="chart">{chart_mean()}</div>
<p>{since_line} A mean over a few dozen trades that sit in the same few weeks swings this much; that is why the first kill line is at {S.B2_KILL_FROM} trades and not at the first good fortnight.</p>
<div class="chart"><table>
<tr><th>page of</th><th class="n">closed</th><th class="n">mean after cost</th><th class="n">winners</th><th class="n">t</th><th class="n">sleeves v hold</th><th class="n">luck p</th></tr>
{then_now}
</table></div>

<h2>1. Book 2, trade by trade</h2>
<p class="note">{n2} closed trades, each after the 0.05% round-trip cost, in the order they were sold. The gold line is the running sum.</p>
<div class="chart">{chart_trades()}</div>
<p>The mean trade is {pc(m2)} after cost against a backtest of about +0.22%{pace}. The best was {best['market']} {pc(best['r'])} ({best['in']} to {best['out']}), the worst {worst['market']} {pc(worst['r'])}. A trade lasts {mean_k:.1f} sessions on average. The four US funds gave {len(us)} trades at {pc(statistics.mean(us)) if us else 'none'}, the five overseas {len(ex)} at {pc(statistics.mean(ex)) if ex else 'none'}; in the backtest only the US carried it.</p>
<details><summary>All {n2} closed trades and the {len(B2_OPEN)} still open</summary>
<div class="chart"><table>
<tr><th>market</th><th>bought</th><th>sold</th><th class="n">sessions</th><th class="n">after cost</th></tr>
{trade_rows}
{open_rows}
</table></div>
</details>

<h2>2. Against holding</h2>
<p class="note">For each market: the book compounded over its trades, with the open ones marked at the {last_date} close, against simply holding that fund from the {START2} open.</p>
<div class="chart">{chart_holding()}</div>
<p>Averaged over the nine, the book is {pc(book2_marked)} with its open trades marked ({pc(book2_closed)} on closed trades only); holding is {pc(hold2)}. The book is in the market a fraction of the time, so in a falling stretch it has less to lose, and in a rising one it lags. {open_line}</p>

<h2>3. Against luck</h2>
<p class="note">Each random book keeps every real trade's market and length in sessions and moves its entry to a random session in the same weeks ({SHUFFLES:,} books, fixed seed {SEED}, same cost).</p>
<div class="chart">{chart_luck()}</div>
<p>{L2['ge']:,} of {SHUFFLES:,} random books matched {pc(L2['observed'])}, p {L2['p']:.4f}; the random median is {pc(L2['random_median'])}{fall}. The nine funds move together, so the {n2} trades are not {n2} independent tries. Grouped by the week they closed, {wk_pos} of {len(W2)} weeks were positive and t falls from {t2:.2f} to {wk_t:.2f}. Book 1's {n1} trades give p {L1['p']:.4f} against a random median of {pc(L1['random_median'])}: it beats random entries in the same falling weeks while still losing money, which is why the three questions are asked separately.</p>
<details><summary>Book 2 by week of exit</summary>
<div class="chart"><table>
<tr><th>week</th><th class="n">trades</th><th class="n">mean after cost</th></tr>
{week_rows}
</table></div>
</details>

<h2>4. Book 1, the one I started with</h2>
<p>{n1} closed trades, mean {pc(m1)}, {w1:.0%} winners, t {t1:.2f}, against a backtest of +0.63% and 75%. {len(B1_OPEN)} open. Its sleeves are {pc(book1_marked)} marked against {pc(hold1)} for holding from {START1}. It needs {S.KILL_FROM - n1} more closed trades before its first kill line; at that point a mean below zero kills it. {n1} trades say very little either way.</p>

<h2>What is not settled</h2>
<ul>
<li>{len(W2)} weeks of closed trades is not a verdict; section 0 shows how far the mean moved between two builds of this page. Book 2's pre-registered marks are 200 closed trades for the first kill line and 500 for the answer, about eleven months and two and a third years.</li>
<li>The random books use the same weeks, so they control for the market's drift in that window but not for this being a good window for dip-buying.</li>
<li>Prices are as traded, not dividend-adjusted, and fills are the next open with no slippage beyond the 0.05% cost.</li>
<li>Paper only. No account and no stake, by charter.</li>
</ul>

<p class="note">Built by <code>docs/systems/build.py</code> from <a href="{GH}EVENTS.csv">EVENTS.csv</a> and <a href="{GH}SIGNALS.csv">SIGNALS.csv</a> through systems.py's own trade pairing; it exits if its counts, means, win rates or t differ from the kill check's nightly lines. Rules and pass marks: <a href="{GH}RULES.md">RULES.md</a>. <a href="data.json">data.json</a> · <a href="../">the lab</a></p>
</main>
</body>
</html>
"""

with open(os.path.join(HERE, "index.html"), "w") as f:
    f.write(page)
print(f"built systems page: book2 {n2} closed {m2:+.4%} win {w2:.0%} t {t2:.2f} week-t {wk_t:.2f} p {L2['p']:.4f}; "
      f"sleeves {book2_marked:+.4%} v hold {hold2:+.4%}; open {len(B2_OPEN)} down {open2_down}; "
      f"book1 {n1} {m1:+.4%} p {L1['p']:.4f}; verdicts {verdicts}; bytes {len(page)}")
