"""Builds docs/tools/channel-digest/index.html from digest.json. Every number on the page is
counted here from the file; nothing is typed by hand.
python3 /Users/triton/PROTEUS/docs/tools/channel-digest/build.py"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, "digest.json")))
E = html.escape

chs = d["channels"]
vids = [v for c in chs for v in c["videos"]]
got = [v for v in vids if "words" in v]
blocked = [v for v in vids if v.get("error")]
flags = sum(len(v["flags"]) for v in got)
sents = sum(v["sentences"] for v in got)
in_window = sum(c.get("in_window", 0) for c in chs)
words = sum(v["words"] for v in got)


def mmss(t):
    return "%d:%02d" % (t // 60, t % 60)


cards = []
for c in chs:
    full = c.get("in_window") == c.get("feed_count")
    rows = []
    for v in c["videos"]:
        head = '<h4><a href="https://youtu.be/%s">%s</a> <span class="dim">%s</span></h4>' % (
            E(v["id"]), E(v["title"]), E(v["published"][:10]))
        if v.get("error"):
            rows.append('<div class="vid">%s<p class="bad">No transcript: %s</p></div>' % (head, E(v["error"].split(":")[0])))
            continue
        li = "".join('<li><a class="ts" href="https://youtu.be/%s?t=%d">%s</a> %s</li>' % (
            E(v["id"]), f["t"], mmss(f["t"]), E(f["text"])) for f in v["flags"])
        meta = '<p class="dim">%s words, %s min, %d of %d sentences flagged</p>' % (
            f"{v['words']:,}", v["minutes"], len(v["flags"]), v["sentences"])
        rows.append('<div class="vid">%s%s%s</div>' % (head, meta, "<ul>%s</ul>" % li if li else ""))
    note = "%d uploads in the window, feed holds %d%s" % (
        c.get("in_window", 0), c.get("feed_count", 0), " (all of it, so there may be more)" if full else "")
    if c.get("in_window", 0) > len(c["videos"]):
        note += "; first %d read" % len(c["videos"])
    cards.append('<section class="ch"><h3>%s</h3><p class="dim">%s</p>%s</section>' % (
        E(c.get("name", c["arg"])), E(note), "".join(rows) or '<p class="dim">Nothing new in the window.</p>'))

page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Channel digest</title>
<style>
:root{--bg:#f7f5f0;--fg:#1d1d1b;--dim:#6b6860;--line:#dedad0;--acc:#b5451b;--card:#fff;--bad:#a12a2a}
@media (prefers-color-scheme:dark){:root{--bg:#141413;--fg:#ecebe6;--dim:#9a978e;--line:#2e2d2a;--acc:#e07b52;--card:#1d1d1b;--bad:#e07272}}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 Georgia,serif}
main{max-width:860px;margin:0 auto;padding:24px 16px 64px}
h1{font-size:28px;margin:0 0 4px}h3{margin:0 0 2px;font-size:20px}h4{margin:14px 0 2px;font-size:16px;font-family:system-ui,sans-serif}
a{color:var(--acc)}.dim{color:var(--dim);margin:2px 0;font-size:14px}.bad{color:var(--bad);font-size:14px;margin:2px 0}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin:20px 0}
.tile{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px}
.tile b{display:block;font:600 26px system-ui,sans-serif}.tile span{font-size:13px;color:var(--dim)}
.ch{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:16px;margin:14px 0}
ul{padding-left:18px;margin:6px 0}li{margin:4px 0;font-size:15px}
.ts{font:600 13px ui-monospace,monospace;margin-right:4px}
code{font:13px ui-monospace,monospace;background:var(--line);padding:1px 4px;border-radius:3px;word-break:break-all}
nav{font:14px system-ui,sans-serif;margin-bottom:18px}
</style></head><body><main>
<nav><a href="../../">Proteus lab</a> / tools</nav>
<h1>Channel digest</h1>
<p>Give it a YouTube channel, get what it posted lately with the lines worth checking pulled out, each linked to the second it was said. Keyless: the channel's public feed and its captions. Below is one real run on the five closing-line-value channels I watched on 20 Oct, last %(days)d days, built %(built)s.</p>
<div class="tiles">
<div class="tile"><b>%(nch)d</b><span>channels</span></div>
<div class="tile"><b>%(inw)d</b><span>uploads in the window</span></div>
<div class="tile"><b>%(got)d of %(nv)d</b><span>transcripts fetched</span></div>
<div class="tile"><b>%(words)s</b><span>words read</span></div>
<div class="tile"><b>%(flags)d of %(sents)s</b><span>sentences flagged</span></div>
</div>
<p class="dim">A flag is not a check. A sentence scores for a percentage, a number, a comparison or an absolute word, and the top five per video are listed so a person can go and test them. %(nb)d fetch(es) hit YouTube's IP block on this run; the tool reports them rather than retrying.</p>
%(cards)s
<h2>Run it</h2>
<p><code>python3 digest.py @Unabated eFd_LWmH2bQ --days 7 --max 5</code></p>
<p class="dim">A channel is a handle, a channel id, a channel URL, or any video from the channel. Needs <code>pip install youtube-transcript-api</code>. Writes <code>digest.json</code> and <code>digest.md</code>. Source: <a href="digest.py">digest.py</a>, <a href="README.md">README</a>, this run as <a href="digest.md">markdown</a>.</p>
<p class="dim">Step one of a fortnight's build (26 Oct to 8 Nov). Next: score the flags by hand on a sample, so the heuristic earns its place or goes.</p>
</main></body></html>
""" % {"days": d["days"], "built": E(d["built"]), "nch": len(chs), "inw": in_window, "got": len(got), "nv": len(vids),
       "words": f"{words:,}", "flags": flags, "sents": f"{sents:,}", "nb": len(blocked), "cards": "\n".join(cards)}

open(os.path.join(HERE, "index.html"), "w").write(page)
print("built index.html | channels", len(chs), "| in window", in_window, "| transcripts", len(got), "of", len(vids),
      "| blocked", len(blocked), "| words", words, "| flags", flags, "of", sents)
