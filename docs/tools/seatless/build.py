"""Builds docs/tools/seatless/index.html from committed files, never typed numbers:
- run-2026-11-21.json: the tool's own run on the 400 most-signed petitions of the 2019-24 Parliament;
- experiments/2026-11-21-P-0517/results.json (the probe this run repeats) and
  experiments/2026-11-21-P-0516/results.json (2017-19 v 2019-24).
Exits unless the run's summary matches its rows and every petition both read agrees with P-0517's gap.
python3 -I /Users/triton/PROTEUS/docs/tools/seatless/build.py"""
import json
import sys

R = "/Users/triton/PROTEUS/"
D = R + "docs/tools/seatless/"
sys.path.insert(0, D)
import seatless  # noqa: E402

RUN = json.load(open(D + "run-2026-11-21.json"))
P517 = json.load(open(R + "experiments/2026-11-21-P-0517/results.json"))
P516 = json.load(open(R + "experiments/2026-11-21-P-0516/results.json"))
rows, s = RUN["rows"], RUN["summary"]

if seatless.summarise(rows) != s:
    sys.exit("summary disagrees with rows")
old = {r["id"]: r for r in P517["rows"] if "gap" in r}
ok = [r for r in rows if "gap" in r]
both = [r for r in ok if r["id"] in old]
diff = [r["id"] for r in both if r["gap"] != old[r["id"]]["gap"] or r["uk"] != old[r["id"]]["uk"]]
if diff or len(both) < 390:
    sys.exit("%d of %d shared petitions differ from P-0517: %s" % (len(diff), len(both), diff[:5]))
for k, v in P517["by_month"].items():
    if k in s["by_month"] and v["n"] == s["by_month"][k]["n"] and abs(v["share"] - s["by_month"][k]["share"]) > 1e-4:
        sys.exit("month %s differs from P-0517" % k)

N, READ, ERR = s["petitions"], s["read"], s["errors"]
SHARE = 100 * s["share"]
p516 = {x["parliament"]: x for x in P516["summary"]}
S4, S3 = 100 * p516[4]["gap_share"], 100 * p516[3]["gap_share"]


def era(m):
    if m < "2020-03":
        return None
    return "a" if m <= "2021-06" else ("b" if m <= "2022-12" else "c")


def pool(sel):
    u = sum(r["uk"] for r in sel)
    return (100.0 * sum(r["gap"] for r in sel) / u if u else None), len(sel)


ERAS = [("a", "Mar 2020 to Jun 2021"), ("b", "Jul 2021 to Dec 2022"), ("c", "2023 to 2024")]
BANDS = [(10000, 50000, "10k to 50k"), (50000, 150000, "50k to 150k"), (150000, 10 ** 9, "150k and up")]
grid = {}
for lo, hi, bn in BANDS:
    for e, _ in ERAS:
        grid[(bn, e)] = pool([r for r in ok if lo <= r["uk"] < hi and era(r["opened"][:7]) == e])
EA = {e: pool([r for r in ok if era(r["opened"][:7]) == e]) for e, _ in ERAS}
ratio = [grid[(bn, "a")][0] / grid[(bn, "c")][0] for _, _, bn in BANDS]

months = s["by_month"]
pre = [k for k in months if k < "2021-12"]
post = [k for k in months if k >= "2022-02"]
pre_lo, pre_hi = min(100 * months[k]["share"] for k in pre), max(100 * months[k]["share"] for k in pre)
post_lo, post_hi = min(100 * months[k]["share"] for k in post), max(100 * months[k]["share"] for k in post)
dec, jan, feb = (100 * months[k]["share"] for k in ("2021-12", "2022-01", "2022-02"))
TOP = max(100 * v["share"] for v in months.values())
worst = max(ok, key=lambda r: r["gap"])
worst_share = max((r for r in ok if r["uk"] >= 50000), key=lambda r: r["share"])


def esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


cols = "".join('<div class="mb %s" style="height:%.1f%%" title="%s: %d petitions, %.2f%% of %s UK signatures in no seat"></div>'
               % ("pre" if k < "2022-02" else "post", 100 * (100 * v["share"]) / TOP, k, v["n"], 100 * v["share"],
                  format(v["uk"], ","))
               for k, v in months.items())
ticks = "".join('<span>%s</span>' % (k[:4] if k.endswith("-01") or k == min(months) else "") for k in months)

trows = "".join("<tr><td>%s</td>%s</tr>" % (bn, "".join("<td>%.2f%% <span class=mut>(%d)</span></td>" % grid[(bn, e)]
                                                         for e, _ in ERAS)) for _, _, bn in BANDS)
trows += "<tr class=tot><td>all sizes</td>%s</tr>" % "".join("<td>%.2f%% <span class=mut>(%d)</span></td>" % EA[e] for e, _ in ERAS)
thead = "".join("<th>%s</th>" % n for _, n in ERAS)

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Seatless Signatures</title>
<meta name="description" content="How many of a UK Parliament petition's UK signatures sit in no constituency. One standard-library Python file, keyless.">
<style>
:root{{--bg:#fbfaf7;--fg:#1d1c1a;--mut:#6b675f;--line:#dedad2;--a:#2a6f97;--pre:#c4622d;--post:#2a6f97;--card:#fff}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151513;--fg:#ecebe6;--mut:#a29e95;--line:#34322e;--a:#6fb3d9;--pre:#e8935f;--post:#6fb3d9;--card:#1d1c1a}}}}
:root[data-theme="dark"]{{--bg:#151513;--fg:#ecebe6;--mut:#a29e95;--line:#34322e;--a:#6fb3d9;--pre:#e8935f;--post:#6fb3d9;--card:#1d1c1a}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,sans-serif;margin:0}}
main{{max-width:820px;margin:0 auto;padding:24px 16px 60px}}
a{{color:var(--a)}} h1{{font-size:1.9rem;line-height:1.2;margin:.4em 0}} h2{{font-size:1.2rem;margin-top:2em}}
.mut{{color:var(--mut)}} .big{{font-size:1.15rem}}
.chart{{display:flex;align-items:flex-end;gap:2px;height:180px;border-bottom:1px solid var(--line);margin:14px 0 2px}}
.mb{{flex:1;min-width:0;border-radius:2px 2px 0 0}} .mb.pre{{background:var(--pre)}} .mb.post{{background:var(--post)}}
.ticks{{display:flex;gap:2px;font-size:12px;color:var(--mut)}} .ticks span{{flex:1;min-width:0;overflow:visible;white-space:nowrap}}
.key i{{display:inline-block;width:11px;height:11px;border-radius:2px;vertical-align:-1px;margin:0 5px 0 12px}}
.key i:first-child{{margin-left:0}} .key .pre{{background:var(--pre)}} .key .post{{background:var(--post)}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:14px;font-variant-numeric:tabular-nums}}
th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}} tr.tot td{{font-weight:600}}
pre{{background:var(--card);border:1px solid var(--line);padding:12px;overflow-x:auto;font-size:13.5px}}
code{{overflow-wrap:anywhere}}
</style></head><body><main>
<p class="mut"><a href="../../index.html">Proteus lab</a> / tools / seatless</p>
<h1>A million petition signatures that belong to no seat</h1>
<p class="big">Every UK Parliament petition publishes two counts that should match: how many signatures came from the UK, and how many landed in each of the 650 constituencies. They do not. On the {N} most-signed petitions of the 2019-24 Parliament, {format(s["uk"], ",")} UK signatures were counted and {format(s["gap"], ",")} of them ({SHARE:.2f}%) sit in no constituency at all. This one file measures that gap for any petition, keyless.</p>

<h2>It is a step in early 2022, not a slope</h2>
<p>Share of UK signatures in no seat, by the month the petition opened. Every month before December 2021 runs {pre_lo:.1f}% to {pre_hi:.1f}%. December {dec:.2f}%, January {jan:.2f}%, February 2022 {feb:.2f}%, and every month after sits between {post_lo:.2f}% and {post_hi:.2f}%.</p>
<div class="chart" role="img" aria-label="Unplaced share by opening month: {pre_lo:.1f} to {pre_hi:.1f} percent before December 2021, {post_lo:.2f} to {post_hi:.2f} percent from February 2022">{cols}</div>
<div class="ticks">{ticks}</div>
<p class="key mut"><i class="pre"></i>opened before Feb 2022<i class="post"></i>Feb 2022 on. Hover a bar for its month, count and share. Tallest bar {TOP:.2f}%.</p>

<h2>Size does nothing</h2>
<p>Split by how big the petition got, the hole stays the same inside each period. Petitions opened in the lockdown months carry {min(ratio):.1f} to {max(ratio):.1f} times the 2023-24 share in every size band.</p>
<div class="tw"><table><thead><tr><th>UK signatures</th>{thead}</tr></thead><tbody>{trows}</tbody></table></div>
<p class="mut">Share in no seat, petitions in brackets. The biggest single hole: {format(worst["gap"], ",")} signatures on "{esc(worst["title"])}" (opened {esc(worst["opened"])}). The biggest share on a petition of 50,000 or more: {100 * worst_share["share"]:.2f}%.</p>

<h2>What it is not</h2>
<p>Not a slow climb with traffic, which was my first guess (P-0516) and which this run's flat size bands rule out. Not the 2017-19 Parliament either: there the 40 most-signed show {S3:.2f}% against {S4:.2f}% for 2019-24. A step points to a change in how signatures were matched to seats, made around January to February 2022. The site's public code history does not name it (P-0519), so the cause is still open. Not one of the {READ} petitions read had more signatures placed than counted.</p>

<h2>Use it</h2>
<pre>python3 seatless.py --ids 300412 241584
python3 seatless.py --parliament 4 --top 400 --floor 10000
python3 seatless.py --parliament 3 --top 100 --out run.json --csv rows.csv
python3 seatless.py --from run.json</pre>
<p>Standard library only, no key. A named petition is looked up in the archive first, then among open ones. About two petitions a second with the default spacing. <code>--from</code> re-scores a saved run without fetching; the month histogram prints in the terminal.</p>
<p><a href="seatless.py">seatless.py</a> · <a href="run-2026-11-21.json">today's run</a> · <a href="rows-2026-11-21.csv">rows as CSV</a> · <a href="README.md">README</a> · <a href="build.py">how this page is built</a></p>
<p class="mut">Checked: the page does not build unless the run's summary matches its rows and all {len(both)} petitions read both here and in probe P-0517 this morning give the same UK count and gap. {ERR} of {N} failed to fetch. Top {N} by size only; smaller petitions are not read. Not yet checked at phone width in a real browser. A snapshot of {esc(RUN["at"][:10])}; nothing rebuilds it yet.</p>
</main></body></html>
"""
open(D + "index.html", "w").write(page)
print("built", len(page), "bytes | read", READ, "of", N, "| share %.2f" % SHARE, "| shared with P-0517", len(both), "differ", len(diff),
      "| pre %.2f-%.2f post %.2f-%.2f" % (pre_lo, pre_hi, post_lo, post_hi), "| ratios", ["%.2f" % x for x in ratio],
      "| P-0516 3 %.2f 4 %.2f" % (S3, S4), "| months", len(months))
