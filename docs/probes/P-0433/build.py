"""Build docs/probes/P-0433/index.html and data.json from the committed results.json of P-0433.

"Gaps fill 85% of the time", measured on nine ETFs' daily bars. Every number on the page is read or
computed here; nothing is typed. Exits non-zero if the file disagrees with itself: symbol gaps must
sum to the pooled count, buckets must sum to their slice, and the pooled rates must sit at the
gap-weighted mean of the symbols.

python3 /Users/triton/PROTEUS/docs/probes/P-0433/build.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "..", "..", "experiments", "2026-11-13-P-0433", "results.json")
with open(SRC) as f:
    res = json.load(f)

ALL, S09 = res["all"], res["since_2009"]
BASKET = res["rules"]["basket"]
BUCKETS = ["0.05-0.25%", "0.25-0.5%", "0.5-1%", "over 1%"]
BUCKET_NAME = {"0.05-0.25%": "0.05 to 0.25%", "0.25-0.5%": "0.25 to 0.5%", "0.5-1%": "0.5 to 1%", "over 1%": "over 1%"}
bad = []

# ---------- the file against itself ----------
for label, blk in (("all", ALL), ("since_2009", S09)):
    pooled = blk["POOLED"]
    total = sum(blk[s]["gaps"] for s in BASKET)
    if total != pooled["gaps"]:
        bad.append(f"{label}: symbol gaps sum {total} v pooled {pooled['gaps']}")
    for key in ("fill_same_day", "fill_5d", "fill_20d", "mirror_same_day", "fade_win_pct"):
        w = sum(blk[s][key] * blk[s]["gaps"] for s in BASKET) / total
        if abs(w - pooled[key]) > 0.15:
            bad.append(f"{label}: weighted {key} {w:.2f} v pooled {pooled[key]}")
    for s in BASKET + ["POOLED"]:
        bsum = sum(blk[s]["buckets"][b]["gaps"] for b in BUCKETS)
        if bsum != blk[s]["gaps"]:
            bad.append(f"{label} {s}: buckets sum {bsum} v gaps {blk[s]['gaps']}")
        if blk[s]["up"]["gaps"] + blk[s]["down"]["gaps"] != blk[s]["gaps"]:
            bad.append(f"{label} {s}: up plus down v gaps")
if bad:
    for b in bad:
        print("DISAGREE", b)
    sys.exit(1)

P = S09["POOLED"]
SPYA, SPY9 = ALL["SPY"], S09["SPY"]
CLAIM = 85.0
COST = res["rules"]["cost_round_trip"] * 100

syms = sorted(BASKET, key=lambda s: -S09[s]["fade_mean_pct"])
neg = [s for s in BASKET if S09[s]["fade_mean_pct"] < 0]
slices = [
    ("SPY, 1993 on", SPYA, "var(--tide)"),
    ("SPY, 2009 on", SPY9, "var(--tide)"),
    ("nine ETFs, 2009 on", P, "var(--ink)"),
    ("chart gaps, nine ETFs, 2009 on", P["chart_gaps"], "var(--buoy)"),
]
HORIZ = [("fill_same_day", "same day"), ("fill_5d", "within 5 days"), ("fill_20d", "within 20 days")]
# which cells reach the claim
reach_same = [n for n, b, _ in slices if b["fill_same_day"] >= CLAIM]
bucket_reach_same = [b for b in BUCKETS if P["buckets"][b]["fill_same_day"] >= CLAIM or SPYA["buckets"][b]["fill_same_day"] >= CLAIM]
pull = P["fill_same_day"] - P["mirror_same_day"]
small, big = P["buckets"]["0.05-0.25%"], P["buckets"]["over 1%"]
spy_big = SPY9["buckets"]["over 1%"]
worst_all = ALL["POOLED"]["fade_worst_pct"]


def pct(v, d=1):
    return f"{v:.{d}f}%"


def p3(v):
    """Three places, half up, so 0.0755 reads 0.076 as the probe's write-up has it."""
    return f"{round(v + 1e-9, 3):.3f}"


def tv(v):
    return ("−" if v < 0 else "") + f"{abs(v):.2f}"


def sg(v, d=3):
    s = f"{abs(v):.{d}f}%"
    return ("−" if round(v, d) < 0 else "+") + s


data = {
    "built_from": "experiments/2026-11-13-P-0433/results.json",
    "claim_pct": CLAIM,
    "spy_all": {"gaps": SPYA["gaps"], "same": SPYA["fill_same_day"], "d5": SPYA["fill_5d"], "d20": SPYA["fill_20d"]},
    "pooled_2009": {"gaps": P["gaps"], "same": P["fill_same_day"], "mirror": P["mirror_same_day"], "d5": P["fill_5d"],
                    "d20": P["fill_20d"], "fade_win": P["fade_win_pct"], "fade_mean": round(P["fade_mean_pct"], 3),
                    "p_v_coin": round(P["p_fade_v_coin"], 3), "t": P["fade_t"]},
    "pull_points": round(pull, 1),
    "symbols_negative": len(neg), "symbols": len(BASKET),
    "spy_2009": {"fade_mean": round(SPY9["fade_mean_pct"], 3), "t": SPY9["fade_t"], "p_v_coin": round(SPY9["p_fade_v_coin"], 3),
                 "hold_open_to_close": round(SPY9["open_to_close_all_days_pct"], 3)},
    "slices_reaching_claim_same_day": len(reach_same),
    "bucket_rows": len(BUCKETS) + 1, "symbol_bars": len(BASKET) + 1,
}
with open(os.path.join(HERE, "data.json"), "w") as f:
    json.dump(data, f, indent=1)
    f.write("\n")


# ---------- chart 1: fill rate by horizon ----------
def chart_horizon():
    W, H, L, R, T, B = 760, 340, 48, 210, 18, 40
    xs = [L + i * (W - L - R) / 2 for i in range(3)]
    y = lambda v: T + (100 - v) / 80 * (H - T - B)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Share of gaps filled the same day, within 5 days and within 20 days, four slices, against the claimed 85 percent">']
    for g in (20, 40, 60, 80, 100):
        out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(g):.1f}" y2="{y(g):.1f}" stroke="var(--rule)"/>')
        out.append(f'<text x="{L-8}" y="{y(g)+4:.1f}" text-anchor="end">{g}%</text>')
    out.append(f'<line x1="{L}" x2="{W-R}" y1="{y(CLAIM):.1f}" y2="{y(CLAIM):.1f}" stroke="var(--gold)" stroke-width="2" stroke-dasharray="6 4"/>')
    out.append(f'<text class="k" x="{L+6}" y="{y(CLAIM)-6:.1f}">the claim, {CLAIM:.0f}%</text>')
    for x, (_, name) in zip(xs, HORIZ):
        out.append(f'<text class="k" x="{x:.1f}" y="{H-12}" text-anchor="middle">{name}</text>')
    ends = []
    for name, blk, col in slices:
        pts = [(x, y(blk[k])) for x, (k, _) in zip(xs, HORIZ)]
        dash = ' stroke-dasharray="3 3"' if "1993" in name else ""
        out.append(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{col}" stroke-width="2"{dash}/>')
        for (a, b), (k, hn) in zip(pts, HORIZ):
            out.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="4.5" fill="{col}"><title>horizon {name}, {hn}: {pct(blk[k])}</title></circle>')
        ends.append([pts[-1][1], name, blk, col])
    ends.sort(key=lambda e: e[0])
    for i in range(1, len(ends)):
        if ends[i][0] - ends[i - 1][0] < 30:
            ends[i][0] = ends[i - 1][0] + 30
    for yy, name, blk, col in ends:
        out.append(f'<text class="k" x="{W-R+12}" y="{yy:.1f}">{name}</text>')
        out.append(f'<text x="{W-R+12}" y="{yy+14:.1f}">{pct(blk["fill_same_day"])} to {pct(blk["fill_20d"])}</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 2: fill v mirror by gap size ----------
def chart_mirror():
    rows = [(BUCKET_NAME[b], P["buckets"][b], SPYA["buckets"][b]) for b in BUCKETS]
    rows.append(("chart gaps", P["chart_gaps"], SPYA["chart_gaps"]))
    W, L, R, T = 760, 150, 24, 30
    H = T + len(rows) * 44 + 30
    x = lambda v: L + v / 100 * (W - L - R)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Same-day fill rate against the mirror level, by gap size, nine ETFs since 2009, with SPY all history as a tick">']
    for g in (0, 25, 50, 75, 100):
        out.append(f'<line x1="{x(g):.1f}" x2="{x(g):.1f}" y1="{T-8}" y2="{H-28}" stroke="var(--rule)"/>')
        out.append(f'<text x="{x(g):.1f}" y="{H-10}" text-anchor="middle">{g}%</text>')
    out.append(f'<line x1="{x(CLAIM):.1f}" x2="{x(CLAIM):.1f}" y1="{T-8}" y2="{H-28}" stroke="var(--gold)" stroke-width="2" stroke-dasharray="6 4"/>')
    out.append(f'<text class="k" x="{x(CLAIM):.1f}" y="{T-14}" text-anchor="middle">{CLAIM:.0f}%</text>')
    for i, (name, b, spy) in enumerate(rows):
        yy = T + 16 + i * 44
        f_, m_ = b["fill_same_day"], b["mirror_same_day"]
        out.append(f'<text class="k" x="{L-12}" y="{yy+4}" text-anchor="end">{name}</text>')
        out.append(f'<text x="{L-12}" y="{yy+18}" text-anchor="end">{b["gaps"]:,} gaps</text>')
        out.append(f'<line x1="{x(m_):.1f}" x2="{x(f_):.1f}" y1="{yy}" y2="{yy}" stroke="var(--ghost)" stroke-width="4"/>')
        out.append(f'<circle cx="{x(m_):.1f}" cy="{yy}" r="6" fill="var(--paper)" stroke="var(--buoy)" stroke-width="2.2"><title>size {name}: mirror level hit {pct(m_)}</title></circle>')
        out.append(f'<circle cx="{x(f_):.1f}" cy="{yy}" r="6" fill="var(--tide)"><title>size {name}: filled the same day {pct(f_)}</title></circle>')
        out.append(f'<line x1="{x(spy["fill_same_day"]):.1f}" x2="{x(spy["fill_same_day"]):.1f}" y1="{yy-9}" y2="{yy+9}" stroke="var(--ink)" stroke-width="2"><title>size {name}: SPY since 1993 filled {pct(spy["fill_same_day"])}</title></line>')
        out.append(f'<text x="{x(min(m_, f_))-12:.1f}" y="{yy+4}" text-anchor="end">{pct(m_)}</text>')
        out.append(f'<text class="k" x="{x(max(f_, spy["fill_same_day"]))+12:.1f}" y="{yy+4}">{pct(f_)}</text>')
    out.append("</svg>")
    return "\n".join(out)


# ---------- chart 3: what fading pays, per symbol ----------
def chart_fade():
    rows = [(s, S09[s]) for s in syms] + [("all nine", P)]
    W, L, R, T = 760, 150, 150, 24
    H = T + len(rows) * 30 + 30
    top = 0.06
    x = lambda v: L + (v + top) / (2 * top) * (W - L - R)
    out = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Mean result of fading every gap after cost, percent a trade, per symbol since 2009, with the win rate beside each">']
    for g in (-0.04, -0.02, 0, 0.02, 0.04):
        out.append(f'<line x1="{x(g):.1f}" x2="{x(g):.1f}" y1="{T-6}" y2="{H-28}" stroke="var(--rule)" stroke-width="{2 if g == 0 else 1}"/>')
        out.append(f'<text x="{x(g):.1f}" y="{H-10}" text-anchor="middle">{sg(g, 2) if g else "0"}</text>')
    for i, (s, b) in enumerate(rows):
        yy = T + 12 + i * 30
        v = b["fade_mean_pct"]
        col = "var(--tide)" if v > 0 else "var(--buoy)"
        if s == "all nine":
            out.append(f'<line x1="{L-140}" x2="{W-10}" y1="{yy-15}" y2="{yy-15}" stroke="var(--rule)"/>')
        out.append(f'<text class="k" x="{L-12}" y="{yy+4}" text-anchor="end">{s}</text>')
        x0, x1 = sorted([x(0), x(v)])
        out.append(f'<rect x="{x0:.1f}" y="{yy-8}" width="{max(x1-x0, 1.5):.1f}" height="16" fill="{col}"><title>fade {s}: {sg(v)} a trade after cost, won {pct(b["fade_win_pct"])} of {b["gaps"]:,}</title></rect>')
        out.append(f'<text class="k" x="{(x1+8 if v > 0 else x0-8):.1f}" y="{yy+4}" text-anchor="{"start" if v > 0 else "end"}">{sg(v)}</text>')
        out.append(f'<text x="{W-R+20}" y="{yy+4}">won {pct(b["fade_win_pct"])}</text>')
    out.append("</svg>")
    return "\n".join(out)


def brow(name, b, spy):
    return (f'<tr><td>{name}</td><td class="n">{b["gaps"]:,}</td><td class="n">{pct(b["fill_same_day"])}</td>'
            f'<td class="n">{pct(spy["fill_same_day"])}</td><td class="n">{pct(b["mirror_same_day"])}</td>'
            f'<td class="n">{pct(b["fill_5d"])}</td><td class="n">{pct(b["fill_20d"])}</td><td class="n">{sg(b["fade_mean_pct"])}</td></tr>')


bucket_rows = "\n".join([brow(BUCKET_NAME[b], P["buckets"][b], SPYA["buckets"][b]) for b in BUCKETS]
                        + [brow("chart gaps", P["chart_gaps"], SPYA["chart_gaps"])])

stats = [
    ("hot", pct(P["fill_same_day"]), f"of {P['gaps']:,} gaps filled the same day, nine ETFs since 2009. The claim is {CLAIM:.0f}%"),
    ("", pct(P["fill_20d"]), "filled within 20 trading days. The claim only arrives if you wait"),
    ("", f"{pull:.1f} points", f"the pull: fill {pct(P['fill_same_day'])} against {pct(P['mirror_same_day'])} for the same distance the other way"),
    ("hot", sg(P["fade_mean_pct"]), f"a trade after cost for fading every gap, while winning {pct(P['fade_win_pct'])} of them"),
    ("", f"{len(neg)} of {len(BASKET)}", "symbols where the fade loses money after cost"),
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
.chart{background:var(--raised);border:1px solid var(--rule);border-radius:8px;padding:12px 10px 6px;overflow-x:auto}
svg{display:block;width:100%;min-width:560px;height:auto}
svg text{font:12px ui-monospace,Menlo,monospace;fill:var(--muted)}
svg text.k{fill:var(--ink)}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:13px;color:var(--muted);margin:10px 4px}
.sw{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:middle;margin-right:5px}
.note{font-size:14px;color:var(--muted)}
ul{max-width:64ch}
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
<title>Only If You Wait</title>
<meta name="description" content="Probe P-0433: a 17-second video says gaps fill {CLAIM:.0f}% of the time. On {P['gaps']:,} gaps in nine ETFs since 2009, {pct(P['fill_same_day'])} fill the same day and {pct(P['fill_20d'])} within 20 days; fading every one wins {pct(P['fade_win_pct'])} and makes {sg(P['fade_mean_pct'])} a trade.">
<style>{CSS}</style>
</head>
<body>
<main>
<div class="kicker">Proteus probe P-0433 · 13 Nov 2026 · verdict: not worth it</div>
<h1>Only if you wait</h1>
<p>A 17-second trading video says a gap, the jump between yesterday's close and today's open, gets filled 85% of the time, and calls that an 85% win rate. It names no market, no time limit and no count of trades. I supplied those myself, wrote them down first, and ran it on daily bars for nine index ETFs ({", ".join(BASKET)}). I called it <b>works</b> at 70%. It came out <b>not worth it</b>.</p>

<div class="stats">
{stat_html}
</div>

<h2>1. The 85% is a waiting time</h2>
<p class="note">Share of gaps where price traded back to yesterday's close, by how long you allow. A gap here is an open at least {res['rules']['min_gap']*100:.2f}% from the prior close. A chart gap is the stricter kind the video draws: an open beyond yesterday's whole range.</p>
<div class="chart">{chart_horizon()}</div>
<p>The same day, {len(reach_same)} of the {len(slices)} slices reach {CLAIM:.0f}%. SPY since 1993 fills {pct(SPYA['fill_same_day'])} of {SPYA['gaps']:,} gaps the same day, {pct(SPYA['fill_5d'])} within five days and {pct(SPYA['fill_20d'])} within twenty. The basket since 2009 goes {pct(P['fill_same_day'])}, {pct(P['fill_5d'])}, {pct(P['fill_20d'])}. Chart gaps fill {pct(P['chart_gaps']['fill_same_day'])} the same day and {pct(P['chart_gaps']['fill_20d'])} in twenty. The video's "later on" is doing the work.</p>

<h2>2. Most of the fill is price just moving</h2>
<p class="note">The control: the mirror level, the same distance from the open in the other direction, away from yesterday's close. If price reaches that about as often, the fill rate is ordinary movement and not a pull towards the gap. Filled dot: gap filled the same day. Hollow dot: mirror level hit. Black tick: SPY since 1993.</p>
<div class="chart">{chart_mirror()}
<div class="legend">
 <span><i class="sw" style="background:var(--tide)"></i>filled the same day, nine ETFs since 2009</span>
 <span><i class="sw" style="border:2px solid var(--buoy)"></i>mirror level hit</span>
 <span>| SPY since 1993</span>
</div></div>
<p>Across the basket the gap fills {pct(P['fill_same_day'])} of the time and the mirror level is hit {pct(P['mirror_same_day'])}. The pull towards yesterday's close is {pull:.1f} points. Small gaps fill often ({pct(small['fill_same_day'])}) because any level that close gets touched ({pct(small['mirror_same_day'])} for the mirror). Gaps over 1% fill {pct(big['fill_same_day'])} the same day. {"No bucket reaches the claim the same day, in the basket or in SPY." if not bucket_reach_same else "Reaching the claim the same day: " + ", ".join(BUCKET_NAME[b] for b in bucket_reach_same) + "."}</p>
<div class="chart"><table>
<tr><th>gap size</th><th class="n">gaps</th><th class="n">fill same day</th><th class="n">SPY 1993 on</th><th class="n">mirror</th><th class="n">fill 5d</th><th class="n">fill 20d</th><th class="n">fade mean</th></tr>
{bucket_rows}
</table></div>

<h2>3. A high win rate and no money</h2>
<p class="note">The trade: fade the gap at the open, target yesterday's close, out at the close if it has not filled, no stop (the video gives none), {COST:.2f}% cost a round trip. Bars are the mean result per trade since 2009; the win rate sits beside each.</p>
<div class="chart">{chart_fade()}</div>
<p>Fading every gap wins {pct(P['fade_win_pct'])} of the time across the basket and makes {sg(P['fade_mean_pct'])} a trade after cost, t {tv(P['fade_t'])}. {len(neg)} of {len(BASKET)} symbols are negative. The win is the size of the gap and the loss is the size of the day, so a strategy can win most days and still lose. The worst single fade in the whole history lost {abs(worst_all):.1f}%. Against a coin that picks fade or follow on the same days, {res['rules']['draws']:,} draws, the basket's p is {p3(P['p_fade_v_coin'])}.</p>
<p><b>SPY is the exception, and I did not call it.</b> {sg(SPY9['fade_mean_pct'])} a trade after cost since 2009, t {tv(SPY9['fade_t'])}, p {p3(SPY9['p_fade_v_coin'])} against the coin. I said it would be luck and it is not. But it is one symbol of nine, it rests on the over-1% bucket ({sg(spy_big['fade_mean_pct'])} on {spy_big['gaps']:,} gaps), and simply holding SPY from open to close on every day since 2009 averages {sg(SPY9['open_to_close_all_days_pct'])} a day. I would not trade it on this.</p>

<h2>What is not settled</h2>
<ul>
<li>The rules are my guesses, because the source gives none: the {res['rules']['min_gap']*100:.2f}% floor, the four size buckets and the three horizons were fixed before the run and not swept.</li>
<li>Price-only daily bars. An ex-dividend open counts as a small gap down, and a gap "filled" on day one may have filled in the last minute.</li>
<li>The open and the target are assumed filled at the printed price. Real opens slip, and the SPY edge is about the size of one tick.</li>
<li>No stop was tested. A stop would change every number on this page.</li>
<li>Early bars for the country ETFs are thin, which is why the since-2009 rows lead.</li>
</ul>

<p class="note">Built by <code>docs/probes/P-0433/build.py</code> from the probe's committed results file, which exits if the symbols, buckets and pooled rows do not add up. Write-up and code: <a href="https://github.com/triton-xxix/proteus-lab/tree/main/experiments/2026-11-13-P-0433">P-0433</a>. <a href="data.json">data.json</a> · <a href="../">every probe</a> · <a href="../../">the lab</a></p>
</main>
</body>
</html>
"""

with open(os.path.join(HERE, "index.html"), "w") as f:
    f.write(page)
print(f"built P-0433 page: pooled same {P['fill_same_day']} mirror {P['mirror_same_day']} d20 {P['fill_20d']}, "
      f"fade {P['fade_mean_pct']} win {P['fade_win_pct']}, negative {len(neg)} of {len(BASKET)}, "
      f"reach same day {len(reach_same)}, buckets reaching {len(bucket_reach_same)}, bytes {len(page)}")
