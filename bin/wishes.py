#!/usr/bin/env python3
"""What strangers wish existed: a weekly pull for the tools-for-strangers interest (3 Oct 2026).
Until then I had never looked for anything to build.

    wishes.py pull [--days 7]   Hacker News posts and comments asking for a tool, keyless, plus
                                r/SomebodyMakeThis and r/isthereatoolthat posts through the Arctic
                                Shift archive (reddit.com feeds 404 keyless since Nov, F-0107). Writes
                                state/wishes/YYYY-MM-DD.md and appends field-notes/WISHES.md.

The nightly reads the week's file on Thursday and queues at most one wish as a probe
(`probe.py add "..." --source persona`): one I could build in an evening, that no existing tool in
the thread already answers, released with a README. Read-only apart from those two files.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from html import unescape
from pathlib import Path

ROOT = Path("/Users/triton/PROTEUS")
PHRASES = ["is there a tool", "i wish there was a tool", "is there an app that", "does anyone know a tool",
           "looking for a tool that", "is there a script", "is there a cli"]
# Two subreddits that exist for exactly this, found by the first pull on 3 Oct; their feeds beat a
# site-wide phrase search, which returned more noise than wishes.
REDDIT = ["SomebodyMakeThis", "isthereatoolthat"]
# r/iWishThereWasAnApp answered 403 on 3 Oct, so it is out.
# F-0107 (27 Nov): both reddit.com RSS feeds 404 keyless since about 19 Nov, so posts come from the
# Arctic Shift archive instead (BACKLOG, Grinder research desk). It needs an `after` bound or it
# times out, and `permalink` is not a valid field. r/isthereatoolthat has had one spam post since Sep.
ARCTIC = "https://arctic-shift.photon-reddit.com/api/posts/search?"
UA = {"User-Agent": "proteus-wishes/0.1 (github triton-xxix)"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", unescape(s or ""))).strip()


def hn(days):
    since = int(time.time() - days * 86400)
    out = {}
    for ph in PHRASES:
        q = urllib.parse.urlencode({"query": f'"{ph}"', "tags": "(story,comment)",
                                    "numericFilters": f"created_at_i>{since}", "hitsPerPage": 50})
        try:
            d = json.loads(get("https://hn.algolia.com/api/v1/search_by_date?" + q))
        except Exception as e:
            print(f"hn {ph!r}: {e}")
            continue
        for h in d.get("hits", []):
            text = clean(h.get("comment_text") or h.get("story_text") or h.get("title"))
            i = text.lower().find(ph)
            if i < 0:
                continue
            snippet = text[max(0, i - 60): i + 260]
            out[h["objectID"]] = {"src": "HN", "url": f"https://news.ycombinator.com/item?id={h['objectID']}",
                                  "when": h.get("created_at", "")[:10], "text": snippet}
        time.sleep(1)
    return out


def reddit(days):
    out = {}
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    for n, sub in enumerate(REDDIT):
        if n:
            time.sleep(5)
        q = urllib.parse.urlencode({"subreddit": sub, "after": cutoff, "limit": 100,
                                    "fields": "id,title,created_utc"})
        try:
            d = json.loads(get(ARCTIC + q))
        except Exception as e:
            print(f"reddit {sub}: {e}")
            continue
        if d.get("error"):
            print(f"reddit {sub}: {d['error']}")
        for p in d.get("data") or []:
            url = f"https://www.reddit.com/r/{sub}/comments/{p['id']}/"
            when = datetime.fromtimestamp(p.get("created_utc", 0), timezone.utc).date().isoformat()
            out[url] = {"src": "Reddit", "url": url, "when": when, "text": clean(p.get("title"))[:300]}
    return out


def main():
    if len(sys.argv) < 2 or sys.argv[1] != "pull":
        print(__doc__)
        sys.exit(2)
    days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 7
    items = list(hn(days).values()) + list(reddit(days).values())
    items.sort(key=lambda x: x["when"], reverse=True)
    today = date.today().isoformat()
    d = ROOT / "state/wishes"
    d.mkdir(parents=True, exist_ok=True)
    lines = [f"# Wishes, {today} (last {days} days)", "", f"{len(items)} found.", ""]
    lines += [f"- {it['when']} [{it['src']}]({it['url']}): {it['text']}" for it in items]
    (d / f"{today}.md").write_text("\n".join(lines) + "\n")
    with open(ROOT / "field-notes/WISHES.md", "a") as f:
        f.write(f"- {today}: {len(items)} wishes pulled ({sum(i['src'] == 'HN' for i in items)} HN, "
                f"{sum(i['src'] == 'Reddit' for i in items)} Reddit). `state/wishes/{today}.md`\n")
    print(f"{len(items)} wishes -> state/wishes/{today}.md")


if __name__ == "__main__":
    main()
