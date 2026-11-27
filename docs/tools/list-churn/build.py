#!/usr/bin/env python3
"""Build index.html for list-churn from the committed runs beside it. Exits if a run's summary does not
recompute from its rows with the tool's own summarise(), or if the 17 to 26 Nov run disagrees with P-0585."""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from list_churn import summarise, CLASSES  # noqa: E402

P0585 = os.path.join(HERE, "..", "..", "..", "experiments", "2026-11-27-P-0585", "results.json")
RUNS = [("run-mcp-17-26-nov.json", "awesome-mcp-servers, 17 to 26 Nov (harvest snapshots)"),
        ("run-mcp-27oct-27nov.json", "awesome-mcp-servers, 26 Oct commit to 27 Nov"),
        ("run-mcp-26-27-nov.json", "awesome-mcp-servers, 26 Nov snapshot to 27 Nov"),
        ("run-acc-22oct-27nov.json", "awesome-claude-code, 22 Oct commit to 27 Nov")]


def die(msg):
    print("BUILD FAIL:", msg)
    sys.exit(1)


runs = []
for fn, label in RUNS:
    r = json.load(open(os.path.join(HERE, fn)))
    saved = r["summary"]
    if summarise(r) != saved:
        die(fn + " summary does not recompute")
    runs.append((fn, label, r))

p = json.load(open(P0585))
first = runs[0][2]
mine = {x["listed"]: x["full_name"] for x in first["rows"]}
theirs = {x["listed"]: x["full_name"] for x in p["rows"]}
if mine != theirs:
    die("17 to 26 Nov run disagrees with P-0585 on the renames")
if first["summary"]["added_raw"] != 371:
    die("17 to 26 Nov added is not P-0576's 371")

e = html.escape
month = runs[1][2]["summary"]
s1 = first["summary"]
maxadd = max(r["summary"]["added_raw"] for *_, r in runs) or 1

bars = []
for fn, label, r in runs:
    s = r["summary"]
    w_net = 100.0 * s["added_net"] / maxadd
    w_dup = 100.0 * s["renames_counted_twice"] / maxadd
    bars.append(
        '<div class="row"><div class="lab">%s<br><small>%d to %d links</small></div><div class="track">'
        '<span class="bar net" style="width:%.2f%%"></span><span class="bar dup" style="width:%.2f%%"></span></div>'
        '<div class="num"><b>%d</b> added by URL, <b>%d</b> removed by URL, <b>%d</b> real removals</div></div>'
        % (e(label), s["old"], s["new"], w_net, w_dup, s["added_raw"], s["removed_raw"], s["real_removals"]))

pairs = []
for x in runs[1][2]["rows"]:
    pairs.append("<tr><td><code>%s</code></td><td><code>%s</code></td><td>%s</td><td>%s</td></tr>"
                 % (e(x["listed"]), e(x.get("full_name", "-")), e(x["class"]), e((x.get("pushed") or "")[:10])))

tally_rows = "".join("<tr><td>%s</td><td>%d</td></tr>" % (e(c), month["tally"][c]) for c in CLASSES)

page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>list-churn: check a removal before you count it</title>
<style>
body{font:16px/1.55 system-ui,sans-serif;max-width:820px;margin:0 auto;padding:24px 16px;color:#1d1d1f;background:#fbfaf7}
h1{font-size:1.7rem;margin:.2em 0}h2{font-size:1.15rem;margin-top:2em}
.lede{font-size:1.05rem}.row{display:grid;grid-template-columns:1fr;gap:4px;margin:14px 0}
.track{background:#eee;height:18px;border-radius:3px;display:flex;overflow:hidden}
.bar{display:block;height:100%%}.net{background:#2f6f8f}.dup{background:#d98a2b}
.lab small{color:#666}.num{font-size:.92rem}table{border-collapse:collapse;width:100%%;font-size:.9rem}
td,th{border-bottom:1px solid #ddd;padding:4px 6px;text-align:left;vertical-align:top}code{font-size:.85em;word-break:break-all}
.key span{display:inline-block;width:12px;height:12px;margin:0 4px 0 10px;vertical-align:middle}
pre{background:#f0eee8;padding:10px;overflow-x:auto;font-size:.85rem}a{color:#2f6f8f}
</style></head><body>
<p><a href="../../">Proteus lab</a> / tools</p>
<h1>Removed, or renamed?</h1>
<p class="lede">A plain diff of an awesome list's GitHub links said awesome-mcp-servers dropped <b>%(rem1)d</b> repos between 17 and 26 Nov.
All <b>%(rem1)d</b> were renames or owner transfers, and every new name was already back on the list. Real removals: <b>%(real1)d</b>.
Over a whole month (26 Oct commit to 27 Nov) the list grew by <b>%(addm)d</b> links by URL and lost the same <b>%(remm)d</b>: net additions <b>%(netm)d</b>, real removals <b>%(realm)d</b>.</p>
<p><code>list_churn.py</code> is one standard-library Python file that does the check: give it two versions of a list (file or URL, README or one owner/repo a line), it asks the keyless GitHub API about every removed name and sorts each one before you count it.</p>

<h2>1. What a URL diff counts, and what is left</h2>
<p class="key">Additions: <span style="background:#2f6f8f"></span>net new <span style="background:#d98a2b"></span>renames counted twice</p>
%(bars)s
<p>The orange slivers are tiny next to hundreds of additions, which is the point: a rename adds one and removes one, so a churn rate built on removals here would be 100%% wrong (6 of 6), not 2%% wrong.</p>

<h2>2. The six, a month on</h2>
<table><tr><th>listed as</th><th>GitHub says now</th><th>class</th><th>last push</th></tr>%(pairs)s</table>
<p>Four moved owner (one only by case), two renamed the repo. None deleted, none archived. P-0585 found the same six by hand; the tool's 17 to 26 Nov run matches it name for name (the build exits if not).</p>

<h2>3. The classes</h2>
<table><tr><th>class (26 Oct to 27 Nov run)</th><th>count</th></tr>%(tally)s</table>
<p>Only <i>moved, not re-listed</i>, <i>archived</i>, <i>deleted or private</i> and <i>live, dropped</i> are real removals. Anything past <code>--max</code> or that errors is <i>unchecked</i>, never guessed.</p>

<h2>4. Use it</h2>
<pre>python3 list_churn.py OLD.md https://raw.githubusercontent.com/OWNER/LIST/main/README.md --out run.json
python3 list_churn.py --from run.json</pre>
<p>An old version comes from any commit: <code>raw.githubusercontent.com/OWNER/LIST/&lt;sha&gt;/README.md</code>. Keyless GitHub allows 60 calls an hour, so <code>--max</code> (default 50) caps the checks. It checks removals only; an addition that is a brand new repo and one that is a rename look the same until you pair them, which is what <i>moved, re-listed</i> does.</p>
<p><a href="list_churn.py">list_churn.py</a> · <a href="README.md">README</a> · runs: %(runlinks)s</p>

<h2>Limits</h2>
<p>Two lists, one of which did not change at all in five weeks (awesome-claude-code, %(acc)d links both ends), so this is one list's story. A repo made private reads as deleted. Links are compared lower-cased. Built 27 Nov 2026 from the committed runs by build.py; nothing rebuilds it.</p>
</body></html>
""" % dict(rem1=s1["removed_raw"], real1=s1["real_removals"], addm=month["added_raw"], remm=month["removed_raw"],
           netm=month["added_net"], realm=month["real_removals"], bars="\n".join(bars), pairs="".join(pairs),
           tally=tally_rows, acc=runs[3][2]["summary"]["old"],
           runlinks=" · ".join('<a href="%s">%s</a>' % (fn, fn) for fn, *_ in runs))

open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page)
print("built index.html", len(page), "chars")
