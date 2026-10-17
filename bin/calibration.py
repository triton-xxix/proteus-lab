#!/usr/bin/env python3
"""Build docs/calibration/: reliability diagrams for every forecaster I keep, each beside the market
on the same rows. Reads pitch/PREDICTIONS.csv (the model), pitch/JUDGEMENT.csv (my anchored and blind
columns) and exchange/BOOK.csv (my exchange calls). Counting rules are killcheck.py's, so the
me-minus-market numbers here must equal the kill check's; the script stops if they do not.

Stdlib only (plain python3 has no numpy). Writes docs/calibration/data.json and index.html.
Backlog: Big Expedition 12 to 25 Oct, step one. Step two (17 Oct): pitch/MARKET-BACKFILL.csv gives the
model rows committed without odds a market price, and over 2.5 goals gets its own panel."""
import csv
import json
import math
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/calibration"
BINS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0001]
RES = {"H": 0, "D": 1, "A": 2}


def fnum(x):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(v) else v


def triple(r, prefix):
    v = [fnum(r.get(f"{prefix}{k}")) for k in ("home", "draw", "away")]
    return v if all(x is not None for x in v) else None


def brier3(p, res):
    return sum((p[i] - (1 if i == RES[res] else 0)) ** 2 for i in range(3))


def wilson(k, n, z=1.96):
    if n == 0:
        return (0, 1)
    ph = k / n
    d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def bins(pairs):
    out = []
    for lo, hi in zip(BINS, BINS[1:]):
        b = [(p, o) for p, o in pairs if lo <= p < hi]
        if not b:
            continue
        k = sum(o for _, o in b)
        lo95, hi95 = wilson(k, len(b))
        out.append({"lo": lo, "hi": min(hi, 1.0), "n": len(b), "mean_p": round(statistics.mean(p for p, _ in b), 4),
                    "observed": round(k / len(b), 4), "lo95": round(lo95, 4), "hi95": round(hi95, 4)})
    return out


def pairs3(p, res):
    return [(p[i], 1 if i == RES[res] else 0) for i in range(3)]


BACKFILL = ROOT / "pitch/MARKET-BACKFILL.csv"
BF_FIELDS = ["id", "market_home", "market_draw", "market_away", "market_over25", "source", "filled_at"]


def implied(*odds):
    try:
        inv = [1 / float(o) for o in odds]
    except (TypeError, ValueError, ZeroDivisionError):
        return None
    return [round(v / sum(inv), 4) for v in inv]


def backfill(rows):
    """Market odds for scored predictions committed without them. predict.py commits from the
    odds-free fixturedownload calendar when football-data has not listed a match 48 hours out, and
    never revisits the row. football-data's results file carries the same pre-match average (AvgH,
    Avg>2.5) the fixtures file would have given, collected Friday or Tuesday, usually after my
    commit, so the market here has seen more than the model had. Rows are appended once and kept,
    so a value never changes after it is committed. The cache is gitignored; this file is not."""
    have = {r["id"]: r for r in csv.DictReader(open(BACKFILL))} if BACKFILL.exists() else {}
    need = [r for r in rows if r["result"] in RES and r["id"] not in have and not triple(r, "market_")]
    if need:
        idx = {}
        for f in sorted((ROOT / "pitch/cache").glob("*-2627.csv")):
            for c in csv.DictReader(open(f, encoding="utf-8-sig")):
                try:
                    day = datetime.strptime(c["Date"], "%d/%m/%Y").strftime("%Y-%m-%d")
                except (KeyError, ValueError):
                    continue
                idx[(f.name.split("-")[0], day, c["HomeTeam"], c["AwayTeam"])] = (c, f.name)
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        for r in need:
            hit = idx.get((r["competition"], r["kickoff_utc"][:10], r["home"], r["away"]))
            if not hit:
                continue
            c, name = hit
            m3, mo = implied(c.get("AvgH"), c.get("AvgD"), c.get("AvgA")), implied(c.get("Avg>2.5"), c.get("Avg<2.5"))
            if not m3:
                continue
            have[r["id"]] = {"id": r["id"], "market_home": m3[0], "market_draw": m3[1], "market_away": m3[2],
                             "market_over25": mo[0] if mo else "", "source": f"football-data {name} AvgH/D/A, Avg>2.5",
                             "filled_at": now}
        with open(BACKFILL, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=BF_FIELDS)
            w.writeheader()
            for k in sorted(have):
                w.writerow(have[k])
    return have


def model_rows():
    rows = list(csv.DictReader(open(ROOT / "pitch/PREDICTIONS.csv")))
    bf = backfill(rows)
    out = []
    for r in rows:
        if r["result"] not in RES or not r["committed_at"] < r["kickoff_utc"] or not triple(r, "p_"):
            continue
        src = "captured" if triple(r, "market_") else ("backfilled" if r["id"] in bf else None)
        if src == "backfilled":
            r = {**r, **{k: v for k, v in bf[r["id"]].items() if k.startswith("market_")}}
        if src:
            out.append((r, src))
    return rows, out


def model():
    rows, s = model_rows()
    me, mk, d = [], [], []
    for r, _ in s:
        p, m = triple(r, "p_"), triple(r, "market_")
        me += pairs3(p, r["result"])
        mk += pairs3(m, r["result"])
        d.append(brier3(p, r["result"]) - brier3(m, r["result"]))
    cap = [brier3(triple(r, "p_"), r["result"]) - brier3(triple(r, "market_"), r["result"]) for r, src in s if src == "captured"]
    scored = sum(1 for r in rows if r["result"] in RES)
    return {"key": "model", "title": "The Pitch's model", "who": "Dixon-Coles model", "kind": "football, home/draw/away",
            "rows": len(s), "pairs": len(me), "logged": len(rows), "scored_any": scored,
            "captured": len(cap), "backfilled": len(s) - len(cap),
            "captured_me_minus_market": round(statistics.mean(cap), 4) if cap else None,
            "me_minus_market": round(statistics.mean(d), 4) if d else None,
            "me_brier": round(statistics.mean(brier3(triple(r, "p_"), r["result"]) for r, _ in s), 4) if s else None,
            "market_brier": round(statistics.mean(brier3(triple(r, "market_"), r["result"]) for r, _ in s), 4) if s else None,
            "bins": bins(me), "market_bins": bins(mk),
            "rule": "kickoff after commit, result in, market odds captured at commit or backfilled from the results file",
            "line": None}


def over25():
    rows, s = model_rows()
    s = [(r, src) for r, src in s if fnum(r.get("p_over25")) is not None and fnum(r.get("market_over25")) is not None
         and fnum(r.get("home_goals")) is not None and fnum(r.get("away_goals")) is not None]
    me, mk, d = [], [], []
    for r, _ in s:
        o = 1 if fnum(r["home_goals"]) + fnum(r["away_goals"]) > 2 else 0
        p, m = fnum(r["p_over25"]), fnum(r["market_over25"])
        me.append((p, o))
        mk.append((m, o))
        d.append((p - o) ** 2 - (m - o) ** 2)
    return {"key": "over25", "title": "The model on over 2.5 goals", "who": "Dixon-Coles model", "kind": "football, over/under 2.5; yes/no",
            "rows": len(s), "pairs": len(me), "logged": len(rows),
            "captured": sum(1 for _, src in s if src == "captured"),
            "me_minus_market": round(statistics.mean(d), 4) if d else None,
            "me_brier": round(statistics.mean((p - o) ** 2 for p, o in me), 4) if me else None,
            "market_brier": round(statistics.mean((m - o) ** 2 for m, o in mk), 4) if mk else None,
            "bins": bins(me), "market_bins": bins(mk),
            "rule": "same rows as the model panel that have an over 2.5 price; one yes/no forecast per match",
            "line": None}


def judgement(blind):
    rows = list(csv.DictReader(open(ROOT / "pitch/JUDGEMENT.csv")))
    if blind:
        s = [r for r in rows if r["blind_brier"] and r["market_brier"] and r["blind_committed_at"]
             and r["blind_committed_at"] < (r["odds_seen_at"] or "9") and r["blind_committed_at"] < r["kickoff_utc"]]
        pref, col = "blind_", "blind_brier"
    else:
        s = [r for r in rows if int(r["id"][2:]) >= 9 and r["brier"] and r["market_brier"]
             and r["committed_at"] < r["kickoff_utc"]]
        pref, col = "p_", "brier"
    s = [r for r in s if r["result"] in RES and triple(r, pref) and triple(r, "market_")]
    me, mk, d = [], [], []
    for r in s:
        p, m = triple(r, pref), triple(r, "market_")
        if abs(brier3(p, r["result"]) - float(r[col])) > 0.002 or abs(brier3(m, r["result"]) - float(r["market_brier"])) > 0.002:
            sys.exit(f"calibration: {r['id']} Brier does not recompute from its probabilities")
        me += pairs3(p, r["result"])
        mk += pairs3(m, r["result"])
        d.append(float(r[col]) - float(r["market_brier"]))
    return {"key": "blind" if blind else "anchored",
            "title": "My blind column" if blind else "My judgement, odds in view",
            "who": "me, before seeing odds" if blind else "me, after seeing odds", "kind": "football, home/draw/away",
            "rows": len(s), "pairs": len(me), "logged": len(rows),
            "me_minus_market": round(statistics.mean(d), 4) if d else None,
            "me_brier": round(statistics.mean(float(r[col]) for r in s), 4) if s else None,
            "market_brier": round(statistics.mean(float(r["market_brier"]) for r in s), 4) if s else None,
            "bins": bins(me), "market_bins": bins(mk),
            "rule": "blind call committed before the odds were opened and before kickoff" if blind
            else "J-0009 on, committed before kickoff",
            "line": "KILL at +0.020, KEEP at 0.000, 60 rows" if blind else "KILL at +0.010, KEEP at -0.005, 60 rows"}


def exchange():
    rows = list(csv.DictReader(open(ROOT / "exchange/BOOK.csv")))
    s = [r for r in rows if r.get("brier") and r.get("market_brier") and r.get("mid_at") and r["committed_at"] < r["mid_at"]]
    me = [(float(r["p"]), 1 if r["outcome"] == "winner" else 0) for r in s]
    mk = [(float(r["market_mid"]), 1 if r["outcome"] == "winner" else 0) for r in s]
    d = [float(r["brier"]) - float(r["market_brier"]) for r in s]
    settled = [r for r in rows if r.get("outcome") in ("winner", "loser")]
    return {"key": "exchange", "title": "My exchange calls", "who": "me, one contract a night on Smarkets",
            "kind": "elections, weather, macro; yes/no", "rows": len(s), "pairs": len(me), "logged": len(rows),
            "settled_any": len(settled),
            "me_minus_market": round(statistics.mean(d), 4) if d else None,
            "me_brier": round(statistics.mean(float(r["brier"]) for r in s), 4) if s else None,
            "market_brier": round(statistics.mean(float(r["market_brier"]) for r in s), 4) if s else None,
            "bins": bins(me), "market_bins": bins(mk),
            "rule": "settled, with the market mid captured after my commit",
            "line": "KILL at +0.020, KEEP at 0.000, 60 rows"}


def killcheck_lines():
    sys.path.insert(0, str(ROOT / "bin"))
    import killcheck  # noqa: E402
    return killcheck.judgement() + [killcheck.exchange()]


def check(panels):
    lines = " ".join(killcheck_lines())
    for p in panels:
        if p["key"] in ("model", "over25") or p["me_minus_market"] is None:
            continue
        tag = f"{p['rows']} counted" if p["key"] != "exchange" else f"{p['rows']} settled"
        want = f"{tag}, " + ("blind" if p["key"] == "blind" else "me") + f" minus market {p['me_minus_market']:+.4f}"
        if want not in lines:
            sys.exit(f"calibration: {p['key']} disagrees with killcheck ({want!r} not in its output)")


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def svg(p):
    W, H, L, T, S = 340, 340, 44, 14, 270  # plot square S at (L, T)
    x = lambda v: L + v * S
    y = lambda v: T + (1 - v) * S
    o = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="{esc(p["title"])}: forecast against what happened">']
    for t in (0, 0.2, 0.4, 0.6, 0.8, 1):
        o.append(f'<line x1="{x(t):.1f}" x2="{x(t):.1f}" y1="{T}" y2="{T+S}" class="grid"/>'
                 f'<line x1="{L}" x2="{L+S}" y1="{y(t):.1f}" y2="{y(t):.1f}" class="grid"/>'
                 f'<text x="{x(t):.1f}" y="{T+S+16}" class="tick">{t:g}</text>'
                 f'<text x="{L-6}" y="{y(t)+4:.1f}" class="tick" text-anchor="end">{t:g}</text>')
    o.append(f'<line x1="{x(0)}" y1="{y(0)}" x2="{x(1)}" y2="{y(1)}" class="diag"/>')
    o.append(f'<text x="{L+S/2}" y="{H-4}" class="axl">forecast</text>'
             f'<text transform="translate(11 {T+S/2}) rotate(-90)" class="axl">happened</text>')
    if not p["bins"]:
        o.append(f'<text x="{L+S/2}" y="{T+S/2}" class="empty">nothing scored yet</text></svg>')
        return "".join(o)
    for cls, bs, dx in (("mk", p["market_bins"], 3), ("me", p["bins"], -3)):
        pts = " ".join(f"{x(b['mean_p'])+dx:.1f},{y(b['observed']):.1f}" for b in bs)
        o.append(f'<polyline points="{pts}" class="ln {cls}"/>')
        for b in bs:
            cx, r = x(b["mean_p"]) + dx, 3 + 2.2 * math.sqrt(b["n"])
            o.append(f'<line x1="{cx:.1f}" x2="{cx:.1f}" y1="{y(b["lo95"]):.1f}" y2="{y(b["hi95"]):.1f}" class="wh {cls}"/>'
                     f'<circle cx="{cx:.1f}" cy="{y(b["observed"]):.1f}" r="{min(r, 16):.1f}" class="pt {cls}">'
                     f'<title>{"market" if cls == "mk" else p["who"]}: said {b["mean_p"]:.2f} on {b["n"]} outcomes '
                     f'({b["lo"]:.1f} to {b["hi"]:.1f}), {b["observed"]:.2f} happened (95% {b["lo95"]:.2f} to {b["hi95"]:.2f})</title></circle>')
    o.append("</svg>")
    return "".join(o)


def verdict(p):
    m = p["me_minus_market"]
    if m is None:
        return "Nothing scored yet."
    side = "worse than" if m > 0 else "better than"
    return f"Brier {p['me_brier']:.4f} against the market's {p['market_brier']:.4f}: {abs(m):.4f} {side} the market per row."


def page(panels, built):
    cards = []
    for p in panels:
        extra = ""
        if p["key"] == "model":
            cap = "" if p["captured_me_minus_market"] is None else f" (me minus market {p['captured_me_minus_market']:+.4f} on those alone)"
            extra = (f" {p['logged']} predictions logged, {p['scored_any']} with a result. Market odds were captured at commit on"
                     f" {p['captured']}{cap}; the other {p['backfilled']} were committed from the odds-free fallback calendar, so"
                     " their market price is football-data's pre-match average from the results file, usually taken after my"
                     " commit. That price has seen more than the model had, which favours the market.")
        elif p["key"] == "over25":
            extra = f" {p['captured']} of the {p['rows']} have the price captured at commit; the rest are backfilled as above."
        elif p["key"] == "exchange":
            extra = f" {p['logged']} calls logged, {p['settled_any']} settled; only {p['rows']} had the market mid captured, so only those can be compared."
        else:
            extra = f" {p['logged']} rows logged in all."
        line = f'<p class="mut">Pre-registered line: {esc(p["line"])}. {max(0, 60 - p["rows"])} rows to the floor.</p>' if p["line"] else \
            '<p class="mut">No kill line: the model is scored at the week-8 review (PASS-MARKS.md).</p>'
        cards.append(f'<section class="card"><div class="k">{esc(p["kind"])}</div><h2>{esc(p["title"])}</h2>'
                     f'<p><b>{p["rows"]} rows</b>, {p["pairs"]} outcome forecasts. {esc(verdict(p))}</p>{svg(p)}'
                     f'<p class="mut">Counted: {esc(p["rule"])}.{esc(extra)}</p>{line}</section>')
    fmt = lambda v, f: "" if v is None else format(v, f)
    rows = "".join(f'<tr><td>{esc(p["title"])}</td><td>{p["rows"]}</td><td>{fmt(p["me_brier"], ".4f")}</td>'
                   f'<td>{fmt(p["market_brier"], ".4f")}</td><td>{fmt(p["me_minus_market"], "+.4f")}</td></tr>'
                   for p in panels)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Calibration Page</title>
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6b6a66;--line:#e2dfd8;--me:#b5543c;--mk:#6b6a66;--card:#ffffff}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151514;--fg:#ecebe6;--mut:#9c9a93;--line:#33322f;--me:#e08468;--mk:#9c9a93;--card:#1d1d1b}}}}
:root[data-theme="dark"]{{--bg:#151514;--fg:#ecebe6;--mut:#9c9a93;--line:#33322f;--me:#e08468;--mk:#9c9a93;--card:#1d1d1b}}
body{{background:var(--bg);color:var(--fg);font:17px/1.55 Georgia,serif;margin:0}}
main{{max-width:980px;margin:0 auto;padding:32px 16px 64px}}
h1{{font-size:2.1rem;margin:.2em 0}} h2{{font-size:1.2rem;margin:.2em 0 .4em}}
.k{{font:13px/1.4 ui-monospace,Menlo,monospace;color:var(--mut);text-transform:uppercase;letter-spacing:.08em}}
.grid2{{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:16px;margin-top:24px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:16px;min-width:0}}
.card p{{font-size:15px;margin:.5em 0}}
svg{{width:100%;max-width:360px;height:auto;display:block;margin:8px auto}}
.grid{{stroke:var(--line)}} .diag{{stroke:var(--mut);stroke-dasharray:4 4}}
.tick{{font:10px ui-monospace,Menlo,monospace;fill:var(--mut);text-anchor:middle}}
.axl{{font:11px ui-sans-serif,system-ui;fill:var(--mut);text-anchor:middle}}
.empty{{font:14px Georgia,serif;fill:var(--mut);text-anchor:middle}}
.ln{{fill:none;stroke-width:1.5}} .ln.me{{stroke:var(--me)}} .ln.mk{{stroke:var(--mk);stroke-dasharray:3 3}}
.wh{{stroke-width:1.2}} .wh.me{{stroke:var(--me)}} .wh.mk{{stroke:var(--mk)}}
.pt.me{{fill:var(--me);fill-opacity:.85}} .pt.mk{{fill:none;stroke:var(--mk);stroke-width:1.5}}
.key span{{display:inline-block;width:12px;height:12px;border-radius:50%;vertical-align:-1px;margin:0 4px 0 12px}}
.key .me{{background:var(--me)}} .key .mk{{border:1.5px solid var(--mk)}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;font:14px ui-sans-serif,system-ui;width:100%}}
td,th{{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left}}
a{{color:inherit}} .mut{{color:var(--mut)}}
</style></head><body><main>
<div class="k">Proteus lab · calibration · built {esc(built)}</div>
<h1>Does anything here beat the market?</h1>
<p>Every forecaster I keep, scored against what happened and against the market on exactly the same rows. A
forecaster that knows something sits on the dashed diagonal: when it says 0.6, the thing happens six times in ten.
The market is the bar to clear, because its prices are free. The score is Brier: lower is better, and a positive
"me minus market" means I would have done better copying the prices.</p>
<p class="key mut"><span class="me"></span>the forecaster <span class="mk"></span>the market, same rows · dot size is how
many outcomes fall in the bin · whiskers are 95% intervals</p>
<div class="tw"><table><tr><th>Forecaster</th><th>Rows</th><th>Brier</th><th>Market</th><th>Me minus market</th></tr>{rows}</table></div>
<div class="grid2">{"".join(cards)}</div>
<h2 style="margin-top:2em">What this does not say yet</h2>
<p>These are small samples. The whiskers are wide because most bins hold a few dozen outcomes at best, and every
pre-registered book needs 60 rows before it can be kept or killed. Football rows count each match three times
(home, draw, away), so the dots are not independent. The over 2.5 panel counts each match once. Nothing on this
page has been bent after the fact: the counting rules are the kill check's, and the build stops if the two
disagree.</p>
<p class="mut">Drawn by bin/calibration.py from pitch/PREDICTIONS.csv, pitch/MARKET-BACKFILL.csv, pitch/JUDGEMENT.csv and exchange/BOOK.csv;
numbers in <a href="data.json">data.json</a>. Every forecast was committed to git before its outcome was knowable.
<a href="../">Back to the lab</a>.</p>
</main></body></html>
"""


def main():
    panels = [model(), over25(), judgement(False), judgement(True), exchange()]
    check(panels)
    built = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "data.json").write_text(json.dumps({"built": built, "panels": panels}, indent=1) + "\n")
    (OUT / "index.html").write_text(page(panels, built))
    for p in panels:
        print(f"{p['key']}: {p['rows']} rows, me minus market {p['me_minus_market']}")


if __name__ == "__main__":
    main()
