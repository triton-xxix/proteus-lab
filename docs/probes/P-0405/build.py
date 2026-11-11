"""Build docs/probes/P-0405/index.html and data.json from two committed results.json files.

P-0404 (R01 shadow book, 29 entries against the minute candles) and P-0405 (main Grinder ledger,
89 entries, every path re-walked from the first candle's open). Every number on the page is read or
computed here; nothing is typed. Exits non-zero if a recomputed figure disagrees with the probe's own.

python3 /Users/triton/PROTEUS/docs/probes/P-0405/build.py
"""
import json
import math
import os
import statistics
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.join(HERE, "..", "..", "..", "experiments")


def load(folder):
    with open(os.path.join(EXP, folder, "results.json")) as f:
        return json.load(f)


p404 = load("2026-11-11-P-0404")
p405 = load("2026-11-11-P-0405")
rows = p405["rows"]
r01 = p404["rows"]
bad = []


def half_up(v, d=2):
    """Round half up on the decimal as written, so 4.335 reads 4.34 as the probe's write-up has it."""
    from decimal import Decimal, ROUND_HALF_UP
    return float(Decimal(repr(round(v, 6))).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


# ---------- recompute P-0405 and compare ----------
n = len(rows)
if n != p405["ledger_rows"]:
    bad.append(f"rows {n} v ledger_rows {p405['ledger_rows']}")
tot_l = sum(r["ledger_pnl_100"] for r in rows)
tot_c = sum(r["candle_pnl_100"] for r in rows)
if abs(tot_l - p405["total_pnl_100_stake_ledger_entry"]) > 0.02:
    bad.append(f"ledger total {tot_l:.2f} v {p405['total_pnl_100_stake_ledger_entry']}")
if abs(tot_c - p405["total_pnl_100_stake_candle_entry"]) > 0.02:
    bad.append(f"candle total {tot_c:.2f} v {p405['total_pnl_100_stake_candle_entry']}")
move = tot_c - tot_l
if abs(move - p405["total_moves_by"]) > 0.02:
    bad.append(f"move {move:.2f} v {p405['total_moves_by']}")
flips = [r for r in rows if r["flip"]]
if len(flips) != p405["exit_reason_flips"]:
    bad.append(f"flips {len(flips)} v {p405['exit_reason_flips']}")
med_all = statistics.median(abs(r["gap_pct"]) for r in rows)
if abs(med_all - p405["gap_all"]["median_abs_gap_pct"]) > 0.005:
    bad.append(f"median gap {med_all:.3f} v {p405['gap_all']['median_abs_gap_pct']}")
beyond5 = sum(1 for r in rows if abs(r["gap_pct"]) > 5)
if beyond5 != p405["gap_all"]["beyond_5pct"]:
    bad.append(f"beyond 5% {beyond5} v {p405['gap_all']['beyond_5pct']}")


def band(a):
    return "under_6_min" if a < 6 else ("6_to_15_min" if a < 15 else "15_min_plus")


bands = {}
for r in rows:
    bands.setdefault(band(r["snapshot_age_min"]), []).append(abs(r["gap_pct"]))
for k, want in p405["gap_by_snapshot_age"].items():
    got = bands.get(k, [])
    if len(got) != want["n"] or abs(statistics.median(got) - want["median_abs_gap_pct"]) > 0.005:
        bad.append(f"band {k}: n {len(got)} median {statistics.median(got):.3f} v {want}")

def diff(r):
    return r["candle_pnl_100"] - r["ledger_pnl_100"]


# the row whose written price was furthest from the market, not the row with the biggest swing
worst = max(rows, key=lambda r: abs(r["gap_pct"]))
worst_move = diff(worst)
rest_move = move - worst_move
flip_net = sum(diff(r) for r in flips)
nonflip_move = move - flip_net
flip_up = sorted([r for r in flips if diff(r) > 0], key=diff)
flip_down = sorted([r for r in flips if diff(r) < 0], key=diff)
biggest_up = flip_up[-1]
biggest_down = flip_down[0]
worst_below = (1 - worst["entry_candle"] / worst["entry_ledger"]) * 100

# ---------- recompute P-0404 and compare ----------
if len(r01) != p404["entries"]:
    bad.append(f"R01 rows {len(r01)} v {p404['entries']}")
for r in r01:
    r["age"] = (ts(r["entered_at"]) - ts(r["snapshot_ts"])).total_seconds() / 60
med_r01 = statistics.median(abs(r["gap_entry_close_pct"]) for r in r01)
if abs(med_r01 - p404["v_entry_minute_close"]["median_abs_pct"]) > 0.005:
    bad.append(f"R01 median {med_r01:.3f} v {p404['v_entry_minute_close']['median_abs_pct']}")
r01_young = [abs(r["gap_entry_close_pct"]) for r in r01 if r["age"] < 8]
r01_old = [abs(r["gap_entry_close_pct"]) for r in r01 if r["age"] >= 8]
r01_old_ages = [r["age"] for r in r01 if r["age"] >= 8]
inside = sum(1 for r in r01 if r["inside_entry_candle"])
if inside != p404["inside_entry_candle"]:
    bad.append(f"R01 inside {inside} v {p404['inside_entry_candle']}")

if bad:
    for b in bad:
        print("DISAGREE", b)
    sys.exit(1)

data = {
    "built_from": ["experiments/2026-11-11-P-0404/results.json", "experiments/2026-11-11-P-0405/results.json"],
    "main_rows": n, "median_abs_gap_pct": half_up(med_all), "beyond_5pct": beyond5,
    "flips": len(flips), "total_ledger": round(tot_l, 2), "total_candle": round(tot_c, 2),
    "move": round(move, 2), "worst_id": worst["id"], "worst_move": round(worst_move, 2),
    "rest_move": round(rest_move, 2), "rest_per_trade_pence": round(100 * rest_move / (n - 1)),
    "flip_net": round(flip_net, 2), "nonflip_move": round(nonflip_move, 2),
    "flips_up": len(flip_up), "flips_down": len(flip_down),
    "bands": {k: {"n": len(v), "median": round(statistics.median(v), 2)} for k, v in bands.items()},
    "r01_rows": len(r01), "r01_median_abs_gap_pct": half_up(med_r01), "r01_inside_candle": inside,
    "r01_young": {"n": len(r01_young), "median": round(statistics.median(r01_young), 2)},
    "r01_old": {"n": len(r01_old), "median": round(statistics.median(r01_old), 2)},
}
with open(os.path.join(HERE, "data.json"), "w") as f:
    json.dump(data, f, indent=1)
    f.write("\n")


def gbp(v, sign=False):
    s = f"£{abs(v):,.2f}"
    if v < 0:
        return "−" + s
    return ("+" + s) if sign else s


def pc(v, d=2):
    return f"{half_up(v, d):.{d}f}%"


REASON = {"take_profit": "take profit", "stop_loss": "stop", "rug": "rug", "time_stop": "time stop"}


# ---------- chart 1: snapshot age v gap, log scale ----------
def chart_scatter():
    W, H, L, R, T, B = 760, 330, 62, 16, 14, 40
    xmax = 27
    lo, hi = math.log10(0.05), math.log10(10000)
    x = lambda a: L + a / xmax * (W - L - R)
    y = lambda g: T + (hi - math.log10(max(g, 0.05))) / (hi - lo) * (H - T - B)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Snapshot age in minutes against the absolute gap between the ledger entry price and the candle, log scale, {n} main book entries and {len(r01)} R01 entries">']
    for g in [0.1, 1, 10, 100, 1000, 10000]:
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(g):.1f}" y2="{y(g):.1f}" stroke="var(--rule)"/>')
        out.append(f'<text x="{L-8}" y="{y(g)+4:.1f}" text-anchor="end">{g:g}%</text>')
    out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(5):.1f}" y2="{y(5):.1f}" stroke="var(--muted)" stroke-dasharray="4 4"/>')
    out.append(f'<text x="{W-R-4}" y="{y(5)-5:.1f}" text-anchor="end">5%</text>')
    for a in [0, 5, 10, 15, 20, 25]:
        out.append(f'<text x="{x(a):.1f}" y="{H-20}" text-anchor="middle">{a}</text>')
    out.append(f'<text x="{(L+W-R)/2:.1f}" y="{H-4}" text-anchor="middle">minutes between the scan snapshot and the stamped entry</text>')
    for r in r01:
        g = abs(r["gap_entry_close_pct"])
        out.append(f'<circle cx="{x(r["age"]):.1f}" cy="{y(g):.1f}" r="4" fill="none" stroke="var(--gold)" stroke-width="1.8"><title>{r["id"]} {r["token"]}: snapshot {r["age"]:.1f} min old, gap {g:.2f}%</title></circle>')
    for r in rows:
        g = abs(r["gap_pct"])
        col = "var(--buoy)" if r["flip"] else "var(--tide)"
        rad = 5 if r["flip"] else 3.5
        out.append(f'<circle cx="{x(r["snapshot_age_min"]):.1f}" cy="{y(g):.1f}" r="{rad}" fill="{col}" opacity=".8"><title>{r["id"]} {r["token"]}: snapshot {r["snapshot_age_min"]:.1f} min old, gap {g:.2f}%</title></circle>')
    wg = abs(worst["gap_pct"])
    out.append(f'<text class="k" x="{x(worst["snapshot_age_min"])+9:.1f}" y="{y(wg)+4:.1f}">{worst["id"]}, {wg:,.0f}%</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 2: median gap by snapshot age ----------
def chart_bands():
    W, L, R = 760, 250, 60
    bars = [
        (f"main book, under 6 min ({len(bands['under_6_min'])})", statistics.median(bands["under_6_min"]), "var(--tide)"),
        (f"main book, 6 to 15 min ({len(bands['6_to_15_min'])})", statistics.median(bands["6_to_15_min"]), "var(--tide)"),
        (f"main book, 15 min and over ({len(bands['15_min_plus'])})", statistics.median(bands["15_min_plus"]), "var(--tide)"),
        (f"R01, about 4 min ({len(r01_young)})", statistics.median(r01_young), "var(--gold)"),
        (f"R01, {min(r01_old_ages):.0f} to {max(r01_old_ages):.0f} min ({len(r01_old)})", statistics.median(r01_old), "var(--gold)"),
    ]
    H = 20 + len(bars) * 34
    top = max(v for _, v, _ in bars) * 1.05
    x = lambda v: L + v / top * (W - L - R)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Median absolute entry gap by snapshot age band, both books">']
    for i, (name, v, col) in enumerate(bars):
        yy = 24 + i * 34
        out.append(f'<text class="k" x="{L-10}" y="{yy+4}" text-anchor="end">{name}</text>')
        out.append(f'<line x1="{L}" x2="{x(v):.1f}" y1="{yy}" y2="{yy}" stroke="{col}" stroke-width="14" opacity=".85"><title>{name}: median {v:.2f}%</title></line>')
        out.append(f'<text class="k" x="{x(v)+6:.1f}" y="{yy+4}">{v:.2f}%</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 3: what the re-walk changed, row by row ----------
def chart_rows():
    W, H, L, R, T, B = 760, 300, 52, 12, 20, 30
    diffs = [r["candle_pnl_100"] - r["ledger_pnl_100"] for r in rows]
    top = 200
    y = lambda v: T + (top - v) / (2 * top) * (H - T - B)
    step = (W - L - R) / n
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Change in profit and loss per trade when the entry is priced from the first candle, {n} trades in ledger order">']
    for t in [-150, -100, -50, 0, 50, 100, 150]:
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(t):.1f}" y2="{y(t):.1f}" stroke="var(--rule)" stroke-width="{2 if t == 0 else 1}"/>')
        out.append(f'<text x="{L-8}" y="{y(t)+4:.1f}" text-anchor="end">{("+" if t > 0 else ("−" if t < 0 else ""))}£{abs(t)}</text>')
    for i, (r, d) in enumerate(zip(rows, diffs)):
        cx = L + (i + 0.5) * step
        tip = f'<title>trade {r["id"]} {r["token"]}: {gbp(d, True)}, {REASON[r["ledger_reason"]]} to {REASON[r["candle_reason"]]}</title>'
        if abs(d) < 0.005:
            out.append(f'<circle cx="{cx:.1f}" cy="{y(0):.1f}" r="1.8" fill="var(--ghost)">{tip}</circle>')
            continue
        col = "var(--buoy)" if d < 0 else "var(--tide)"
        y0, y1 = sorted([y(0), y(d)])
        out.append(f'<rect x="{cx-step*0.38:.1f}" y="{y0:.1f}" width="{step*0.76:.1f}" height="{max(y1-y0, 1.5):.1f}" fill="{col}">{tip}</rect>')
        if r["flip"]:
            ly = y(d) - 5 if d > 0 else y(d) + 14
            out.append(f'<text class="k" x="{cx:.1f}" y="{ly:.1f}" text-anchor="middle">{r["id"]}</text>')
    out.append(f'<text x="{L}" y="{H-8}">{rows[0]["id"]}, {rows[0]["entered_at"][:10]}</text>')
    out.append(f'<text x="{W-R}" y="{H-8}" text-anchor="end">{rows[-1]["id"]}, {rows[-1]["entered_at"][:10]}</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 4: the two totals on a zoomed line ----------
def chart_totals():
    W, H, L, R = 760, 150, 20, 20
    lo = math.floor(tot_l / 20) * 20 - 20
    hi = math.ceil(tot_c / 20) * 20 + 20
    x = lambda v: L + (v - lo) / (hi - lo) * (W - L - R)
    mid = tot_l + flip_net
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Book total from the ledger price and from the candle price, split into the changed exits and the rest">']
    out.append(f'<line x1="{L}" x2="{W-R}" y1="84" y2="84" stroke="var(--rule)" stroke-width="2"/>')
    t = lo
    while t <= hi:
        out.append(f'<line x1="{x(t):.1f}" x2="{x(t):.1f}" y1="80" y2="88" stroke="var(--rule)"/>')
        if t % 40 == 0:
            out.append(f'<text x="{x(t):.1f}" y="106" text-anchor="middle">−£{abs(t):,}</text>')
        t += 20
    out.append(f'<line x1="{x(tot_l):.1f}" x2="{x(mid):.1f}" y1="84" y2="84" stroke="var(--buoy)" stroke-width="10" opacity=".85"><title>the {len(flips)} changed exits, net: {gbp(flip_net, True)}</title></line>')
    out.append(f'<line x1="{x(mid):.1f}" x2="{x(tot_c):.1f}" y1="84" y2="84" stroke="var(--tide)" stroke-width="10" opacity=".85"><title>the other {n-len(flips)} rows: {gbp(nonflip_move, True)}</title></line>')
    out.append(f'<circle cx="{x(tot_l):.1f}" cy="84" r="6" fill="var(--ink)"/>')
    out.append(f'<circle cx="{x(tot_c):.1f}" cy="84" r="6" fill="var(--ink)"/>')
    out.append(f'<text class="k" x="{x(tot_l):.1f}" y="36">ledger price</text>')
    out.append(f'<text class="k" x="{x(tot_l):.1f}" y="52">{gbp(tot_l)}</text>')
    out.append(f'<text class="k" x="{x(tot_c):.1f}" y="36" text-anchor="end">candle price</text>')
    out.append(f'<text class="k" x="{x(tot_c):.1f}" y="52" text-anchor="end">{gbp(tot_c)}</text>')
    out.append(f'<text x="{(x(tot_l)+x(mid))/2:.1f}" y="70" text-anchor="middle" style="fill:var(--buoy)">the {len(flips)} changed exits, net {gbp(flip_net, True)}</text>')
    out.append(f'<text x="{x(tot_c):.1f}" y="130" text-anchor="end" style="fill:var(--tide)">the other {n-len(flips)}, {gbp(nonflip_move, True)}</text>')
    out.append(f'<text x="{L}" y="144">the line is zoomed and does not start at zero</text>')
    out.append("</svg>")
    return "\n".join(out)


flip_rows = "\n".join(
    f'<tr><td>{r["id"]}</td><td>{r["token"]}</td><td class="n">{r["snapshot_age_min"]:.1f}</td>'
    f'<td class="n">{("+" if r["gap_pct"] > 0 else "−")}{abs(r["gap_pct"]):,.1f}%</td>'
    f'<td>{REASON[r["ledger_reason"]]} to {REASON[r["candle_reason"]]}</td>'
    f'<td class="n">{gbp(r["ledger_pnl_100"], True)}</td><td class="n">{gbp(r["candle_pnl_100"], True)}</td></tr>'
    for r in flips)

mean_l, mean_c = tot_l / n, tot_c / n
age_med = statistics.median(r["snapshot_age_min"] for r in rows)
age_max = max(r["snapshot_age_min"] for r in rows)
c_above = p405["entry_above_candle"]
c_below = p405["entry_below_candle"]
old4 = [r for r in rows if r["snapshot_age_min"] >= 15]
old4_changed = sum(1 for r in old4 if abs(r["candle_pnl_100"] - r["ledger_pnl_100"]) > 0.005)
v404 = p404["v_entry_minute_close"]

stats = [
    ("hot", pc(med_all), f"typical miss between the price the book wrote down and the first minute candle, {n} entries"),
    ("", f"{p405['snapshot_price_is_entry']} of {n}", "entries priced from the scan snapshot, not from the market at entry"),
    ("", f"{len(flips)} of {n}", "exits that change when the entry is priced from the candle"),
    ("cool", gbp(move, True), f"move in the book total at £100 a trade, {gbp(flip_net, True)} of it from the {len(flips)} changed exits"),
    ("", f"{gbp(mean_l)} v {gbp(mean_c)}", "a trade, ledger price v candle price"),
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
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:22px 0}
.stat{background:var(--raised);border:1px solid var(--rule);border-radius:8px;padding:12px 14px}
.stat b{display:block;font:600 22px/1.15 ui-monospace,Menlo,monospace}
.stat span{font-size:13px;color:var(--muted)}
.stat.hot b{color:var(--buoy)}
.stat.cool b{color:var(--tide)}
.chart{background:var(--raised);border:1px solid var(--rule);border-radius:8px;padding:12px 10px 6px;overflow:hidden}
svg{display:block;width:100%;height:auto}
svg text{font:12px ui-monospace,Menlo,monospace;fill:var(--muted)}
svg text.k{fill:var(--ink)}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:13px;color:var(--muted);margin:10px 4px}
.sw{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:middle;margin-right:5px}
.note{font-size:14px;color:var(--muted)}
ul{max-width:64ch}
.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font:13px/1.4 ui-monospace,Menlo,monospace}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--rule);white-space:nowrap}
th{color:var(--muted);font-weight:600}
td.n,th.n{text-align:right}
"""

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Price Was Already Gone</title>
<meta name="description" content="Probes P-0404 and P-0405: a paper memecoin book that wrote down the scan's price with the time of the trade. Typical miss {pc(med_all)}, {len(flips)} of {n} exits change, and the total moves {gbp(move, True)}, nearly all of it one row. Drawn from the committed results.">
<style>{CSS}</style>
</head>
<body>
<main>
<div class="kicker">Proteus probes P-0404, P-0405 · 11 Nov 2026 · verdicts: works</div>
<h1>The price was already gone</h1>
<p>The Grinder is my paper memecoin desk. Each night it scans new Solana pools, picks a few, and writes a paper trade into a ledger. Both of its books are bust, and I went looking for whether the entry prices were part of why. They were wrong in a plain way: the book wrote down the price from the <b>scan</b> and stamped it with the time of the <b>trade</b>, minutes later. On {p405['snapshot_price_is_entry']} of {n} entries in the main book and {len(r01)} of {len(r01)} in the shadow book, the entry price is the scan snapshot's, to the last digit.</p>

<div class="stats">
{stat_html}
</div>

<h2>1. The older the snapshot, the wider the miss</h2>
<p class="note">Each dot is one paper entry: how old the scan snapshot was when the trade was stamped, against how far the written price sat from the minute candle (main book: open of the first candle after entry; R01: close of the entry minute). Log scale. Red dots are the entries whose exit changes in section 2.</p>
<div class="chart">{chart_scatter()}
<div class="legend">
 <span><i class="sw" style="background:var(--tide)"></i>main book, {n} entries</span>
 <span><i class="sw" style="background:var(--buoy)"></i>main book, exit changes ({len(flips)})</span>
 <span><i class="sw" style="border:2px solid var(--gold)"></i>R01 shadow book, {len(r01)} entries</span>
</div></div>
<p>In the main book the snapshot was {age_med:.1f} minutes old at the median and {age_max:.1f} at the worst. The typical miss is {pc(med_all)}, and {beyond5} of {n} entries miss by more than 5%. In the shadow book the written price sat inside the entry minute's own low to high range on only {inside} of {len(r01)}: on the other {len(r01)-inside} the book "bought" at a price nobody traded at in that minute.</p>
<div class="chart">{chart_bands()}</div>
<p>Before running P-0404 I called a median miss under 1%, on the strength of one row I had looked at. It came out at {pc(med_r01)}. One row misled me.</p>

<h2>2. Re-walk every trade from the real price</h2>
<p class="note">P-0405: all {n} main-book paths walked twice with the same rules and costs at £100 a trade, once from the ledger price and once from the first candle's open. Each bar is the change in that trade's result. Grey dots did not change.</p>
<div class="chart">{chart_rows()}</div>
<p>{len(flips)} exits change: some stops become take profits, some take profits become stops. The written price was above the candle on {c_above} entries and below on {c_below}, so there is no tilt, only noise.</p>
<div class="chart scroll"><table>
<tr><th>trade</th><th>token</th><th class="n">snapshot age, min</th><th class="n">ledger v candle</th><th>exit</th><th class="n">from ledger</th><th class="n">from candle</th></tr>
{flip_rows}
</table></div>

<h2>3. Seven trades hold all of it, and they mostly cancel</h2>
<div class="chart">{chart_totals()}</div>
<p>The total moves by {gbp(move, True)}, from {gbp(tot_l)} to {gbp(tot_c)}. The {len(flips)} changed exits net {gbp(flip_net, True)}: {len(flip_up)} go up (the largest {biggest_up['id']}, {gbp(diff(biggest_up), True)}) and {len(flip_down)} go down (the largest {biggest_down['id']}, {gbp(diff(biggest_down), True)}). The other {n-len(flips)} trades move the total by {gbp(nonflip_move, True)} between them.</p>
<p>The one where the price was truly gone is {worst['id']} ({worst['token']}). Its snapshot was {worst['snapshot_age_min']:.1f} minutes old; by the first candle after entry the token was trading {worst_below:.1f}% lower. It had collapsed before the book "bought" it. From the ledger price it is a rug in the first minute; from the candle price it is a flat time stop, a swing of {gbp(worst_move, True)}.</p>
<p>My write-up of P-0405 said that row carries the move, because taking it out leaves {gbp(rest_move, True)}. Drawn, that reads too neatly: take out {biggest_up['id']} instead and the move is {gbp(move - diff(biggest_up), True)}; take out {biggest_down['id']} and it is {gbp(move - diff(biggest_down), True)}. The fair reading is seven swings of £{min(abs(diff(r)) for r in flips):.0f} to £{max(abs(diff(r)) for r in flips):.0f} that nearly cancel. Either way the book loses {gbp(abs(mean_l))} a trade from the ledger price and {gbp(abs(mean_c))} from the candle price. <b>The entry noise is real and it is not why the Grinder lost.</b></p>

<h2>What is not settled</h2>
<ul>
<li>Both walks use the v0.2 rules and costs on every row, the v0.1 rows included, so these totals are not the published book totals. Only the difference between the two walks is the finding.</li>
<li>The shadow book's {len(r01)} paths were not re-walked; only its entry gaps were measured.</li>
<li>The two books are measured against slightly different candle prices (first open v entry-minute close), so their dots share a chart but not an exact yardstick.</li>
<li>A guard that skips any snapshot over 10 minutes old would have touched the {len(old4)} oldest entries and changed the result of {old4_changed} of them. Nothing in the paper desk was changed; both books are stopped pending a rules call.</li>
</ul>

<p class="note">Built by <code>docs/probes/P-0405/build.py</code> from the two committed results files, which exits if a recomputed total, median, band or flip count disagrees with the probe's own. Write-ups: <a href="https://github.com/triton-xxix/proteus-lab/tree/main/experiments/2026-11-11-P-0404">P-0404</a>, <a href="https://github.com/triton-xxix/proteus-lab/tree/main/experiments/2026-11-11-P-0405">P-0405</a>. <a href="data.json">data.json</a> · <a href="../">every probe</a> · <a href="../../">the lab</a></p>
</main>
</body>
</html>
"""

with open(os.path.join(HERE, "index.html"), "w") as f:
    f.write(page)
print(f"built P-0405 page: median {med_all:.3f}, flips {len(flips)}, totals {tot_l:.2f} to {tot_c:.2f}, move {move:.2f}, "
      f"{worst['id']} {worst_move:.2f} ({worst_below:.1f}% lower), rest {rest_move:.2f}, R01 median {med_r01:.3f}, "
      f"R01 young {len(r01_young)} {statistics.median(r01_young):.2f}, old {len(r01_old)} {statistics.median(r01_old):.2f} "
      f"ages {min(r01_old_ages):.1f}-{max(r01_old_ages):.1f}, old4 changed {old4_changed}, bytes {len(page)}")
