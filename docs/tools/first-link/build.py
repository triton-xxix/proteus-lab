"""Builds docs/tools/first-link/index.html from committed files, never typed numbers:
- run-2026-11-12.json: the tool's own --recheck of the 100 starts against P-0348's noon walk;
- experiments/2026-11-12-P-0348/results.json: the noon walk and what it found against 5 Nov;
- experiments/2026-11-05-P-0332/final.json: the same starts on five past dates.
Exits if the run is not 100 rows, has fetch errors left, disagrees with its own summary, or if more
than 5 starts changed outcome class since noon (that would be the tool, not Wikipedia).
python3 -I /Users/triton/PROTEUS/docs/tools/first-link/build.py"""
import json
import sys
from collections import Counter

R = "/Users/triton/PROTEUS/"
D = R + "docs/tools/first-link/"
RUN = json.load(open(D + "run-2026-11-12.json"))
NOON = json.load(open(R + "experiments/2026-11-12-P-0348/results.json"))
FIN = json.load(open(R + "experiments/2026-11-05-P-0332/final.json"))
rows, s, ns = RUN["rows"], RUN["summary"], NOON["summary"]

if s["n"] != 100 or len(rows) != 100:
    sys.exit("run has %d rows" % len(rows))
if s["rows_with_fetch_errors_not_404"]:
    sys.exit("%d rows still carry fetch errors" % s["rows_with_fetch_errors_not_404"])
oc = Counter(r["outcome"] for r in rows)
if dict(oc) != s["outcomes"]:
    sys.exit("outcome counts %s differ from the summary %s" % (dict(oc), s["outcomes"]))
noon = {r["start"]: r for r in NOON["rows"]}
same = sum(r["path"] == noon[r["start"]]["path"] for r in rows)
if same != 100 - s["path_changed"]:
    sys.exit("paths same as noon %d v summary %d" % (same, 100 - s["path_changed"]))
if s["outcome_class_changed"] > 5:
    sys.exit("%d starts changed class since noon: suspect the tool" % s["outcome_class_changed"])

PH, LO, DE = oc.get("philosophy", 0), oc.get("loop", 0), oc.get("dead end", 0)
hops = sorted(r["hops"] for r in rows if r["outcome"] == "philosophy")
CLS = {"philosophy": "ph", "loop": "lo", "dead end": "de", "too long": "ab", "absent": "ab"}


def esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace('"', "&quot;")


def wiki(t):
    return '<a href="https://en.wikipedia.org/wiki/%s">%s</a>' % (esc(t.replace(" ", "_")), esc(t))


# 1. a square per start
order = {"philosophy": 0, "loop": 1, "dead end": 2, "too long": 3}
sq = "".join('<i class="%s" title="%s: %s after %d hops, at %s"></i>'
             % (CLS[r["outcome"]], esc(r["start"]), r["outcome"], r["hops"], esc(r["end"]))
             for r in sorted(rows, key=lambda r: (order[r["outcome"]], r["hops"])))

# 2. pages most walks pass through, and their fate
through, fate = Counter(), {}
for r in rows:
    for t in set(r["path"]):
        through[t] += 1
        fate.setdefault(t, set()).add(r["outcome"])
hubs = sorted(((t, c) for t, c in through.items() if t != "Philosophy"), key=lambda x: (-x[1], x[0]))[:12]
mixed = sum(1 for t in through if len(fate[t]) > 1)
top = hubs[0][1]
hub_rows = "".join(
    '<div class="row"><span class="nm">%s</span><span class="tr"><b class="%s" style="width:%.1f%%"></b></span>'
    '<span class="ct">%d</span></div>' % (wiki(t), CLS[sorted(fate[t])[0]] if len(fate[t]) == 1 else "ab", 100.0 * c / top, c)
    for t, c in hubs)

# 3. rings
rings = Counter()
ring_order = {}
for r in rows:
    if r["outcome"] == "loop":
        p = r["path"]
        ring = p[p.index(p[-1]):-1]
        k = frozenset(ring)
        rings[k] += 1
        ring_order.setdefault(k, ring)
big, big_n = rings.most_common(1)[0]
big_list = ring_order[big]
k0 = big_list.index("Knowledge") if "Knowledge" in big_list else 0
big_list = big_list[k0:] + big_list[:k0]

# 4. the same starts on past dates
dated, shares = "", []
for d in sorted(FIN["dates"]):
    v = FIN["dates"][d]
    c, w = v["counts"], v["walked"]
    existed = w - c.get("absent", 0)
    share = 100.0 * c.get("philosophy", 0) / existed
    shares.append((share, d))
    segs = "".join('<b class="%s" style="width:%.2f%%" title="%s: %d of %d"></b>' % (CLS[k], 100.0 * c[k] / w, k, c[k], w)
                   for k in ("philosophy", "loop", "dead end", "absent") if c.get(k))
    dated += ('<div class="row"><span class="nm">%s%s</span><span class="tr">%s</span><span class="ct">%.0f%%</span></div>'
              % (d, "" if w == 100 else " (%d walked)" % w, segs, share))
lo_s, hi_s = min(shares), max(shares)

# 5. what moved
def edits(e):
    return "".join("<li>%s</li>" % esc(k).replace(" -> ", " → ") for k in e) or "<li>none</li>"


if s["path_changed"] == 0:
    SINCE = ("Four hours on, all 100 paths are the same, page for page: %d pages fetched, no first link moved."
             % s["pages_fetched"])
    since_list = ""
else:
    SINCE = ("Four hours on, %d of 100 paths differ from noon's and %d starts changed how they end. The first links that moved:"
             % (s["path_changed"], s["outcome_class_changed"]))
    since_list = "<ul>%s</ul>" % edits(s["edits_behind_changes"])

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>First Link</title>
<meta name="description" content="Follow the first link of Wikipedia articles, keep the paths, and walk them again later to see what moved. One standard-library Python file.">
<style>
:root{{--bg:#fbfaf7;--fg:#1d1c1a;--mut:#6b675f;--line:#dedad2;--a:#2a6f97;--ph:#2a6f97;--lo:#c4622d;--de:#8a8578;--ab:#dedad2;--card:#fff}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#151513;--fg:#ecebe6;--mut:#a29e95;--line:#34322e;--a:#6fb3d9;--ph:#6fb3d9;--lo:#e8935f;--de:#8f8a7e;--ab:#3a3833;--card:#1d1c1a}}}}
:root[data-theme="dark"]{{--bg:#151513;--fg:#ecebe6;--mut:#a29e95;--line:#34322e;--a:#6fb3d9;--ph:#6fb3d9;--lo:#e8935f;--de:#8f8a7e;--ab:#3a3833;--card:#1d1c1a}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,sans-serif;margin:0}}
main{{max-width:820px;margin:0 auto;padding:24px 16px 60px}}
a{{color:var(--a)}} h1{{font-size:1.9rem;line-height:1.2;margin:.4em 0}} h2{{font-size:1.2rem;margin-top:2em}}
.mut{{color:var(--mut)}} .big{{font-size:1.15rem}}
.ph{{background:var(--ph)}} .lo{{background:var(--lo)}} .de{{background:var(--de)}} .ab{{background:var(--ab)}}
.sq{{display:grid;grid-template-columns:repeat(20,1fr);gap:3px;margin:12px 0}}
.sq i{{display:block;aspect-ratio:1;border-radius:2px}}
.key i{{display:inline-block;width:11px;height:11px;border-radius:2px;vertical-align:-1px;margin:0 5px 0 12px}}
.key i:first-child{{margin-left:0}}
.row{{display:flex;align-items:center;gap:8px;margin:5px 0;font-size:14px}}
.nm{{flex:0 0 38%;min-width:0;overflow-wrap:anywhere}} .tr{{flex:1;display:flex;height:16px;min-width:0}}
.tr b{{display:block;height:100%}} .ct{{flex:0 0 3.2em;text-align:right;font-variant-numeric:tabular-nums}}
pre{{background:var(--card);border:1px solid var(--line);padding:12px;overflow-x:auto;font-size:13.5px}}
li{{margin:.2em 0}}
</style></head><body><main>
<p class="mut"><a href="../../index.html">Proteus lab</a> / tools / first-link</p>
<h1>Click the first link. Where do you end up?</h1>
<p class="big">The old Wikipedia game says you always reach Philosophy. On 100 random articles today, {PH} do. {LO} go round in a circle for ever and {DE} hit a page with nowhere to go. This one file plays the game, keeps every path, and walks the same starts again later so you can see what moved.</p>

<div class="sq" role="img" aria-label="100 random articles: {PH} reach Philosophy, {LO} loop, {DE} dead end">{sq}</div>
<p class="key mut"><i class="ph"></i>reached Philosophy ({PH})<i class="lo"></i>loop ({LO})<i class="de"></i>dead end ({DE})</p>
<p class="mut">One square per starting article, walked at {esc(s["at"][11:16])} UTC on {esc(s["at"][:10])}. Hover for the start, the hops and where it stopped. The ones that arrive take {hops[0]} to {hops[-1]} hops, median {s["median_hops_to_philosophy"]}.</p>

<h2>A handful of pages decide everything</h2>
<p>Each page has one first link, so every walk that touches a page shares its fate from there. These are the twelve pages the most walks pass through, coloured by where they lead. {sum(1 for t, c in hubs if c == top)} of them carry {top} walks each, more than a third of the sample.{"" if not mixed else " %d pages show two fates, which means they changed mid-run." % mixed}</p>
{hub_rows}
<p>The biggest trap is a ring of {len(big_list)} pages that holds {big_n} of the {LO} loops: {" → ".join(wiki(t) for t in big_list)} → and round again.</p>

<h2>Does it change?</h2>
<p>That is what <code>--recheck</code> is for. The 100 starts were first walked on {esc(ns["old_at"][:10])}. At noon on {esc(ns["at"][:10])}, a week later, {ns["outcome_class_changed"]} of 100 ended differently and {ns["path_changed"]} paths had changed, both still arriving. The first links behind them:</p>
<ul>{edits(ns["edits_behind_changes"])}</ul>
<p>{SINCE}</p>
{since_list}
<p>A quiet week moves almost nothing. Years do not look like that. The same 100 starts replayed on Wikipedia as it stood on {len(shares) - 1} past dates, with the first walk last:</p>
{dated}
<p class="key mut"><i class="ph"></i>reached Philosophy<i class="lo"></i>loop<i class="de"></i>dead end<i class="ab"></i>article did not exist yet</p>
<p class="mut">The figure on the right is the share reaching Philosophy among articles that existed then: from {lo_s[0]:.0f}% ({lo_s[1][:4]}) to {hi_s[0]:.0f}% ({hi_s[1][:4]}). Each collapse is one hub's opening sentence being edited. Dead ends on old dates are an upper bound (moved pages can lose their history), and six snapshots are not a series; the write-up says more.</p>

<h2>Use it</h2>
<pre>python3 first_link.py "Banana"
python3 first_link.py --random 100 --out walks.json
python3 first_link.py --recheck walks.json --out again.json</pre>
<p>Standard library only, no key, about five pages fetched per start. The rule: the first link in the lead that is not in brackets, italics, a hatnote, an infobox, a table or a footnote. The folk rule varies; this one is mine, and a different rule gives different numbers. Red links are followed and count as dead ends.</p>
<p><a href="first_link.py">first_link.py</a> · <a href="run-2026-11-12.json">today's 100 paths</a> · <a href="README.md">README</a> · <a href="build.py">how this page is built</a></p>
<p class="mut">Checked: the page does not build unless the tool's run has 100 rows, no fetch errors left, and agrees with its own summary. The tool was run against the noon walk made by the probe's own script. Not yet checked at phone width in a real browser. A snapshot of {esc(s["at"][:10])}; nothing rebuilds it yet.</p>
</main></body></html>
"""
open(D + "index.html", "w").write(page)
print("built", len(page), "bytes | philosophy", PH, "loop", LO, "dead end", DE, "| hops", hops[0], hops[-1],
      s["median_hops_to_philosophy"], "| top hub", hubs[0], "| ring", len(big_list), big_n, "| mixed", mixed,
      "| since noon: paths changed", s["path_changed"], "class changed", s["outcome_class_changed"],
      "| shares", ["%.0f%% %s" % x for x in shares])
