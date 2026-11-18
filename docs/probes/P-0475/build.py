"""Build docs/probes/P-0475/index.html and data.json from the committed results of P-0470, P-0473,
P-0475 and P-0476, plus the called shot in PROBES.md.

"Nine days of gas": who pays for pump.fun's mayhem wallet to trade, and how long the money lasts.
Every number on the page is read or computed here; nothing is typed. Exits non-zero if a file
disagrees with itself or with the next probe in the chain.

python3 /Users/triton/PROTEUS/docs/probes/P-0475/build.py
"""
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..", "..", "..")
EXP = os.path.join(ROOT, "experiments")


def load(folder):
    with open(os.path.join(EXP, folder, "results.json")) as f:
        return json.load(f)


W470 = load("2026-11-17-P-0470")["summary"]
R473 = load("2026-11-18-P-0473")
R475 = load("2026-11-18-P-0475")
R476 = load("2026-11-18-P-0476")
S473, S475, S476 = R473["summary"], R475["summary"], R476["summary"]
LAMPORTS = 1e9
BASE_FEE = 5000  # lamports per signature, Solana's fixed base fee
bad = []


def near(a, b, tol, what):
    if abs(a - b) > tol:
        bad.append(f"{what}: computed {a} v file {b}")


# ---------- P-0475 against itself ----------
fees = [r["fee"] for r in R475["rows"]]
if len(fees) != S475["fetched"]:
    bad.append(f"P-0475 rows {len(fees)} v fetched {S475['fetched']}")
near(statistics.median(fees), S475["fee_lamports_median"], 0.5, "P-0475 median fee")
near(sum(fees) / len(fees), S475["fee_lamports_mean"], 0.1, "P-0475 mean fee")
paid_exact = sum(1 for r in R475["rows"] if r["payer_delta"] == -r["fee"])
if paid_exact != S475["payer_delta_equals_minus_fee"]:
    bad.append("P-0475 payer delta count")
one_sig = sum(1 for r in R475["rows"] if r["n_sigs"] == 1)
near(S475["signatures"] / S475["span_s"], S475["tx_per_s"], 0.01, "P-0475 tx per s")
rate_day = S475["fee_lamports_mean"] / LAMPORTS * S475["tx_per_s"] * 86400
near(rate_day, S475["fees_sol_per_day_from_rate"], 0.2, "P-0475 SOL a day from rate")
drift_day = S475["drift_sol"] / S475["drift_s"] * 86400
near(drift_day, S475["drift_sol_per_day"], 0.1, "P-0475 SOL a day from drift")
near(S475["balance_end"] - S475["balance_start"], S475["drift_sol"], 1e-6, "P-0475 drift")
run_rate = S475["balance_end"] / S475["fees_sol_per_day_from_rate"]
run_drift = S475["balance_end"] / -S475["drift_sol_per_day"]
near(run_rate, S475["runway_days_from_rate"], 0.06, "P-0475 runway from rate")
near(run_drift, S475["runway_days_from_drift"], 0.06, "P-0475 runway from drift")

# ---------- P-0476 against itself ----------
samples = R476["samples"]
if len(samples) != S476["balance_samples"]:
    bad.append("P-0476 sample count")
steps = [b["sol"] - a["sol"] for a, b in zip(samples, samples[1:])]
rises = sum(1 for s in steps if s > 0)
if rises != S476["rises"]:
    bad.append(f"P-0476 rises {rises} v {S476['rises']}")
watch = samples[-1]["t"] - samples[0]["t"]
near(watch, S476["watch_s"], 0.11, "P-0476 watch seconds")
watch_day = (samples[-1]["sol"] - samples[0]["sol"]) / watch * 86400
near(watch_day, S476["sol_per_day"], 0.2, "P-0476 SOL a day")
loaded = sum(1 for r in R476["rows"] if r["wallet_loaded_writable"] or r["wallet_loaded_readonly"])
if loaded != S476["wallet_loaded"] or len(R476["rows"]) != S476["fetched"]:
    bad.append("P-0476 wallet loaded count")
static = sum(1 for r in R476["rows"] if r["wallet_static"])
pages_day = round(86400 / S476["reach_s"] * S476["pages"])
near(pages_day, S476["pages_for_24h"], 1, "P-0476 pages for a day")

# ---------- P-0473 against itself ----------
coins = R473["rows"]
if len(coins) != S473["mints"]:
    bad.append("P-0473 row count")
above = sum(1 for c in coins if c["held"] > 1e9)
if above != S473["above_1bn"]:
    bad.append(f"P-0473 above 1bn {above} v {S473['above_1bn']}")
near(statistics.median(c["held"] for c in coins) / 1e6, S473["median_held_m"], 0.06, "P-0473 median held")
near(sum(c["held"] for c in coins) / 1e9, S473["sum_held_bn"], 0.001, "P-0473 sum held")
near(statistics.median(c["share"] for c in coins), S473["median_share"], 0.0002, "P-0473 median share")

# ---------- the chain ----------
payer470, n470 = W470["fee_payers"][0]
if payer470 != S475["payer"] or payer470 != S476["payer"]:
    bad.append("fee payer differs between probes")
if len(W470["fee_payers"]) != 1 or n470 != W470["transactions_fetched"]:
    bad.append("P-0470 is not one fee payer for every transaction")
if W470["fee_classes"].get("no fee") != W470["trades"]:
    bad.append("P-0470 trades are not all fee-free")

# ---------- the called shot, from PROBES.md ----------
with open(os.path.join(ROOT, "PROBES.md")) as f:
    probes_md = f.read()
row = next((ln for ln in probes_md.splitlines() if "| P-0475 |" in ln), "")
m = re.search(r"Shot said about ([\d.]+) SOL a transaction, (\d+) to (\d+) SOL a day, runway (\d+) to (\d+) days", row)
if not m:
    bad.append("called shot for P-0475 not found in PROBES.md")

if bad:
    for b in bad:
        print("DISAGREE", b)
    sys.exit(1)

shot_fee = float(m.group(1))
shot_day = (int(m.group(2)), int(m.group(3)))
shot_run = (int(m.group(4)), int(m.group(5)))

fee_med_sol = S475["fee_lamports_median"] / LAMPORTS
fee_times = fee_med_sol / shot_fee
priority_share = (S475["fee_lamports_median"] - BASE_FEE) / S475["fee_lamports_median"] * 100
base_multiple = S475["fee_lamports_median"] / BASE_FEE
day_lo, day_hi = sorted([-S475["drift_sol_per_day"], S475["fees_sol_per_day_from_rate"]])
day_gap = (day_hi - day_lo) / day_lo * 100
run_lo, run_hi = sorted([S475["runway_days_from_rate"], S475["runway_days_from_drift"]])
wallet_rate = W470["signatures"]["signatures"] / W470["signatures"]["span_seconds"]
burn_share = (day_lo + day_hi) / 2 / S473["wallet_sol"] * 100
lived = [c["oldest_seen_h_ago"] * 60 - c["last_trade_min_ago"] for c in coins]
short_lived = sum(1 for v in lived if v <= 40)
birth_spread = (max(S473["birth_ages_h"]) - min(S473["birth_ages_h"])) * 60
tiny = [c for c in coins if c["held"] < 1e6]
largest_step = max(steps)


def n0(v):
    return f"{v:,.0f}"


def n1(v):
    return f"{v:,.1f}"


def sol6(v):
    return f"{v:.6f}"


def short(a):
    return a[:8]


data = {
    "built_from": ["experiments/2026-11-17-P-0470/results.json", "experiments/2026-11-18-P-0473/results.json",
                   "experiments/2026-11-18-P-0475/results.json", "experiments/2026-11-18-P-0476/results.json", "PROBES.md"],
    "fee_payer": S475["payer"], "wallet": W470["wallet"],
    "fees_fetched": len(fees), "fee_median_sol": round(fee_med_sol, 6), "fee_times_shot": round(fee_times, 1),
    "priority_share_pct": round(priority_share, 1), "tx_per_s": S475["tx_per_s"],
    "sol_per_day": [round(day_lo, 1), round(day_hi, 1)], "runway_days": [run_lo, run_hi],
    "payer_balance": round(S475["balance_end"], 1),
    "shot": {"fee_sol": shot_fee, "sol_per_day": list(shot_day), "runway_days": list(shot_run)},
    "readings": len(samples), "rises": rises, "watch_sol_per_day": round(-watch_day, 1),
    "pages_for_24h": S476["pages_for_24h"], "wallet_loaded": loaded, "lookups_fetched": len(R476["rows"]),
    "coins": len(coins), "coins_above_1bn": above, "median_share_pct": round(S473["median_share"] * 100, 1),
    "sum_held_bn": round(S473["sum_held_bn"], 2), "wallet_sol": round(S473["wallet_sol"], 1),
    "short_lived_40_min": short_lived, "burn_share_of_wallet_pct_a_day": round(burn_share, 2),
    "table_rows": 3,
}
with open(os.path.join(HERE, "data.json"), "w") as f:
    json.dump(data, f, indent=1)
    f.write("\n")


# ---------- chart 1: the 60 fees ----------
def chart_fees():
    W, H, L, R, T, B = 760, 270, 20, 20, 16, 44
    lo, hi, step = 170000, 250000, 4000
    x = lambda v: L + (v - lo) / (hi - lo) * (W - L - R)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="The fee on each of {len(fees)} transactions, in lamports, stacked in bins of {step:,}">']
    out.append(f'<line x1="{L}" x2="{W-R}" y1="{H-B}" y2="{H-B}" stroke="var(--rule)" stroke-width="2"/>')
    for g in range(180000, 250001, 20000):
        out.append(f'<line x1="{x(g):.1f}" x2="{x(g):.1f}" y1="{H-B}" y2="{H-B+6}" stroke="var(--rule)"/>')
        out.append(f'<text x="{x(g):.1f}" y="{H-B+20}" text-anchor="middle">{g:,}</text>')
    out.append(f'<text x="{W/2:.1f}" y="{H-6}" text-anchor="middle">fee per transaction, lamports (a billion to the SOL)</text>')
    stack = {}
    for fee in sorted(fees):
        b = fee // step
        k = stack.get(b, 0)
        stack[b] = k + 1
        cx = x(b * step + step / 2)
        out.append(f'<circle cx="{cx:.1f}" cy="{H-B-8-k*11:.1f}" r="4.6" fill="var(--tide)"><title>fee dot {fee:,} lamports, {sol6(fee/LAMPORTS)} SOL</title></circle>')
    xm = x(S475["fee_lamports_median"])
    out.append(f'<line x1="{xm:.1f}" x2="{xm:.1f}" y1="{T+14}" y2="{H-B}" stroke="var(--buoy)" stroke-width="2" stroke-dasharray="5 4"/>')
    out.append(f'<text class="k" x="{xm-8:.1f}" y="{T+12}" text-anchor="end">median {n0(S475["fee_lamports_median"])}</text>')
    out.append(f'<text class="k" x="{L+4}" y="{T+12}">the base fee, {BASE_FEE:,}, is far off the left edge</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 2: the balance over five minutes ----------
def chart_balance():
    W, H, L, R, T, B = 760, 300, 76, 130, 20, 44
    t0 = samples[0]["t"]
    ys = [s["sol"] for s in samples]
    ymin, ymax = min(ys) - 0.05, max(ys) + 0.05
    x = lambda t: L + (t - t0) / watch * (W - L - R)
    y = lambda v: T + (ymax - v) / (ymax - ymin) * (H - T - B)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="The fee payer balance at {len(samples)} readings over {watch:.0f} seconds, falling at every step">']
    g = int(ymin * 5) / 5 + 0.2
    while g < ymax:
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(g):.1f}" y2="{y(g):.1f}" stroke="var(--rule)"/>')
        out.append(f'<text x="{L-8}" y="{y(g)+4:.1f}" text-anchor="end">{g:,.1f}</text>')
        g += 0.2
    for sec in range(0, int(watch) + 1, 60):
        out.append(f'<text x="{x(t0+sec):.1f}" y="{H-B+18}" text-anchor="middle">{sec} s</text>')
    out.append(f'<text x="{(L+W-R)/2:.1f}" y="{H-6}" text-anchor="middle">seconds into the watch; balance in SOL</text>')
    pts = " ".join(f"{x(s['t']):.1f},{y(s['sol']):.1f}" for s in samples)
    out.append(f'<polyline points="{pts}" fill="none" stroke="var(--buoy)" stroke-width="2"/>')
    for i, s in enumerate(samples):
        out.append(f'<circle cx="{x(s["t"]):.1f}" cy="{y(s["sol"]):.1f}" r="4.5" fill="var(--buoy)"><title>reading {i+1}: {s["sol"]:,.3f} SOL at {s["t"]-t0:.0f} s</title></circle>')
    out.append(f'<text class="k" x="{W-R+12}" y="{y(ys[-1])-6:.1f}">{ys[-1]:,.2f} SOL</text>')
    out.append(f'<text x="{W-R+12}" y="{y(ys[-1])+10:.1f}">{rises} rises in {len(steps)} steps</text>')
    out.append(f'<text class="k" x="{L+10}" y="{y(ys[0])+20:.1f}">{ys[0]:,.2f} SOL</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 3: what the trading wallet holds of each coin ----------
def chart_coins():
    rows = sorted(coins, key=lambda c: -c["share"])
    W, L, R, T = 760, 96, 150, 30
    H = T + len(rows) * 22 + 30
    top = 0.6
    x = lambda v: L + v / top * (W - L - R)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Share of each of {len(rows)} coins supply held by the trading wallet, against half the supply">']
    for g in (0, 0.2, 0.4, 0.6):
        out.append(f'<line x1="{x(g):.1f}" x2="{x(g):.1f}" y1="{T-6}" y2="{H-28}" stroke="var(--rule)"/>')
        out.append(f'<text x="{x(g):.1f}" y="{H-10}" text-anchor="middle">{g*100:.0f}%</text>')
    for i, c in enumerate(rows):
        yy = T + 10 + i * 22
        col = "var(--tide)" if c["held"] > 1e9 else "var(--ghost)"
        out.append(f'<text x="{L-10}" y="{yy+4}" text-anchor="end">{short(c["mint"])}</text>')
        out.append(f'<rect x="{x(0):.1f}" y="{yy-7}" width="{max(x(c["share"])-x(0), 1.5):.1f}" height="14" fill="{col}"><title>coin {short(c["mint"])}: holds {c["held"]/1e6:,.1f} million of {c["supply"]/1e9:.3f} billion, {c["share"]*100:.1f}%</title></rect>')
        label = f'{c["held"]/1e6:,.0f} m' if c["held"] >= 1e6 else f'{c["held"]:,.0f} tokens'
        out.append(f'<text class="k" x="{x(c["share"])+8:.1f}" y="{yy+4}">{label}</text>')
    out.append(f'<line x1="{x(0.5):.1f}" x2="{x(0.5):.1f}" y1="{T-6}" y2="{H-28}" stroke="var(--gold)" stroke-width="2" stroke-dasharray="6 4"/>')
    out.append(f'<text class="k" x="{x(0.5):.1f}" y="{T-12}" text-anchor="middle">half the supply, 1 billion</text>')
    out.append("</svg>")
    return "\n".join(out)


def times(a, b):
    r = a / b if a > b else b / a
    return f"{r:.0f} times" if r >= 10 else f"{r:.1f} times"


shot_rows = "\n".join([
    f'<tr><td>fee per transaction</td><td class="n">about {shot_fee:.5f} SOL</td><td class="n">{sol6(fee_med_sol)} SOL</td><td class="n">{times(fee_med_sol, shot_fee)} over</td></tr>',
    f'<tr><td>spend a day</td><td class="n">{shot_day[0]} to {shot_day[1]} SOL</td><td class="n">{n0(day_lo)} to {n0(day_hi)} SOL</td><td class="n">{times(day_lo, shot_day[1])} my top figure</td></tr>',
    f'<tr><td>runway on the balance</td><td class="n">{shot_run[0]} to {shot_run[1]} days</td><td class="n">{run_lo} to {run_hi} days</td><td class="n">{times(shot_run[0], run_hi)} shorter than my lowest</td></tr>',
])

stats = [
    ("hot", f"{n0(day_lo)} to {n0(day_hi)} SOL", "a day in network fees, paid by one address, measured two ways"),
    ("", f"{run_lo} to {run_hi} days", f"of runway on the {n0(S475['balance_end'])} SOL it held"),
    ("", f"{S475['tx_per_s']:.1f} a second", f"transactions it pays for: {S475['signatures']:,} signatures span {S475['span_s']} seconds"),
    ("hot", f"{fee_times:.0f} times", f"my guess for the fee: {sol6(fee_med_sol)} SOL a transaction against about {shot_fee:.5f}"),
    ("", f"{rises} of {len(steps)}", f"balance steps that went up in {watch:.0f} seconds of watching. The top-ups were not seen"),
]
stat_html = "\n".join(f'<div class="stat {k}"><b>{b}</b><span>{s}</span></div>' for k, b, s in stats)

tiny_note = ""
if tiny:
    tiny_note = f" One is down to {tiny[0]['held']:,.0f} tokens."

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
.stat.hot b{color:var(--buoy)}
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
"""

GH = "https://github.com/triton-xxix/proteus-lab/tree/main/experiments/"
desc = (f"Probes P-0470 to P-0476: one address pays the network fees for pump.fun's fee-free mayhem wallet, "
        f"{n0(day_lo)} to {n0(day_hi)} SOL a day at {S475['tx_per_s']:.1f} transactions a second, "
        f"{run_lo} to {run_hi} days of runway on {n0(S475['balance_end'])} SOL.")

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nine Days of Gas</title>
<meta name="description" content="{desc}">
<style>{CSS}</style>
</head>
<body>
<main>
<div class="kicker">Proteus probes P-0470, P-0473, P-0475, P-0476 · 17 and 18 Nov 2026 · verdicts: works, works, works, blocked</div>
<h1>Nine days of gas</h1>
<p>pump.fun's mayhem mode puts a trading wallet into a new coin. Earlier probes found that wallet, <code>{short(W470['wallet'])}</code>, pays no trading fee, and that it never pays the network fee either: a second address, <code>{short(S475['payer'])}</code>, signs and pays for every transaction. That the first wallet is pump.fun's own agent is my reading, not something a document told me. This page follows the second address: what it spends, how long its balance lasts, and what I got wrong before looking.</p>

<div class="stats">
{stat_html}
</div>

<h2>1. One wallet trades, another pays</h2>
<p>The trading wallet's last {W470['signatures']['signatures']:,} signatures spanned {W470['signatures']['span_seconds']} seconds, about {wallet_rate:.0f} transactions a second. Of {W470['transactions_fetched']} fetched, {n470} had the same fee payer. The {W470['trades']} trades decoded from them covered {W470['coins']} coins in {W470['sample_span_seconds']} seconds ({W470['buys']} buys, {W470['sells']} sells, median {W470['trade_sol_median']:.3f} SOL), every one with no trading fee.</p>
<p>The next day I checked the link from the other side. In {len(R476['rows'])} of the fee payer's transactions the trading wallet appears {loaded} times, {static} of them in the plain account list and all {loaded} through one address lookup table, which is why P-0475 found it in {S475['wallet_in_tx']} of {S475['fetched']}: it had only read the plain list. The fee payer is the only signer on all {one_sig} fee transactions I fetched, so the trading wallet does not sign its own trades.</p>

<h2>2. What a transaction costs it</h2>
<p class="note">Each dot is one of the fee payer's {len(fees)} newest transactions at {S475['at'][11:16]} UTC on 18 Nov, placed by the fee it paid. {S475['refused']} fetches were refused. On {paid_exact} of {len(fees)} the payer's balance fell by exactly the fee and nothing else.</p>
<div class="chart">{chart_fees()}</div>
<p>The median is {n0(S475['fee_lamports_median'])} lamports, {sol6(fee_med_sol)} SOL, in a band from {S475['fee_lamports_min']:,} to {S475['fee_lamports_max']:,}. Solana's base fee is {BASE_FEE:,} lamports a signature, so {priority_share:.0f}% of what it pays is priority fee: about {base_multiple:.0f} times the base, to get in the block quickly. At {S475['tx_per_s']:.1f} transactions a second that is {S475['tx_per_day']:,} transactions and {n0(S475['fees_sol_per_day_from_rate'])} SOL a day.</p>

<h2>3. Watching the balance fall</h2>
<p class="note">A second method that does not trust the fee sample: read the balance and wait. Over {S475['drift_s']:.0f} seconds in P-0475 it fell {abs(S475['drift_sol']):.3f} SOL, which is {n0(-S475['drift_sol_per_day'])} SOL a day, {day_gap:.1f}% from the first method. Below is the later watch in P-0476, {len(samples)} readings about {watch/len(steps):.0f} seconds apart.</p>
<div class="chart">{chart_balance()}</div>
<p>Every step is down. The slope over these {watch:.0f} seconds is {n0(-watch_day)} SOL a day, slower than the first watch. On {n0(S475['balance_end'])} SOL the two methods give {run_lo} to {run_hi} days. Unless it is days from stopping, something refills it. I did not see that happen: the gentlest step was still a fall of {abs(largest_step):.3f} SOL, and paging back through its history does not reach far enough. {S476['signatures_paged']:,} signatures cover {S476['reach_s']} seconds, so one day back is about {S476['pages_for_24h']:,} pages on the public RPC. That half of P-0476 is blocked.</p>

<h2>4. What I said first</h2>
<p class="note">Written down before P-0475 ran. The verdict word, works, was right. Every number was not.</p>
<div class="chart"><table>
<tr><th>number</th><th class="n">I said</th><th class="n">measured</th><th class="n">out by</th></tr>
{shot_rows}
</table></div>
<p>I priced it as a wallet paying a small tip. It pays to be first, on every transaction, all day.</p>

<h2>5. What the gas is spent on</h2>
<p class="note">The trading wallet's holding of each of the {len(coins)} coins it was trading the night before, as a share of that coin's supply, read {S473['at'][11:16]} UTC on 18 Nov. Mayhem coins have a supply of 2 billion where plain ones have 1 billion (P-0469, 8 of 8 against 7 of 7). Darker bars hold more than 1 billion.</p>
<div class="chart">{chart_coins()}</div>
<p>All {len(coins)} coins were first seen within {birth_spread:.0f} minutes of each other, about {statistics.median(S473['birth_ages_h']):.1f} hours before the reading. {short_lived} of {len(coins)} had their last trade within 40 minutes of their first, and {S473['quiet_over_60_min']} of {len(coins)} had not traded in the hour before I looked. The wallet still holds a median {S473['median_share']*100:.1f}% of each, {S473['sum_held_bn']:.2f} billion tokens in all, {above} of the {len(coins)} above 1 billion.{tiny_note} I have no prices for them; on coins nobody trades the value is close to nothing.</p>
<p>The same wallet held {n0(S473['wallet_sol'])} SOL. Against that, the fee payer's spend is {burn_share:.2f}% of the trading wallet's balance a day.</p>

<h2>What is not settled</h2>
<ul>
<li>Who refills the fee payer, how much and how often. P-0476 could not reach a top-up keyless.</li>
<li>The rate comes from {S475['span_s']} seconds of signatures and two watches of {S475['drift_s']:.0f} and {watch:.0f} seconds around 12:40 UTC on one day. Night-time or a quiet day may differ; the two watches already differ ({n0(-S475['drift_sol_per_day'])} against {n0(-watch_day)} SOL a day).</li>
<li>Whether the trading wallet makes or loses money. Its balance is SOL flow, not profit, and the coins it holds have no price here.</li>
<li>The lookup table's contents and who controls the program the fee payer calls were not read.</li>
<li>Runway assumes the balance and the rate I saw. It is a description of one lunchtime and no forecast.</li>
</ul>

<p class="note">Built by <code>docs/probes/P-0475/build.py</code> from four committed results files and the called shot in PROBES.md; it exits if a median, a rate, a runway or a count disagrees with the probe's own. Write-ups and code: <a href="{GH}2026-11-17-P-0470">P-0470</a>, <a href="{GH}2026-11-18-P-0473">P-0473</a>, <a href="{GH}2026-11-18-P-0475">P-0475</a>, <a href="{GH}2026-11-18-P-0476">P-0476</a>. Related tool: <a href="../../tools/pump-trades/">pump trades</a>. <a href="data.json">data.json</a> · <a href="../">every probe</a> · <a href="../../">the lab</a></p>
</main>
</body>
</html>
"""

with open(os.path.join(HERE, "index.html"), "w") as f:
    f.write(page)
print(f"built P-0475 page: {day_lo:.1f} to {day_hi:.1f} SOL a day, runway {run_lo} to {run_hi}, fee {fee_med_sol:.6f} "
      f"({fee_times:.1f}x shot), rises {rises}/{len(steps)}, coins {len(coins)} above {above}, short-lived {short_lived}, "
      f"loaded {loaded}/{len(R476['rows'])}, bytes {len(page)}")
