#!/usr/bin/env python3
"""What strangers wish existed: a weekly pull for the tools-for-strangers interest (3 Oct 2026).
Until then I had never looked for anything to build.

    wishes.py pull [--days 7]   Hacker News posts and comments asking for a tool, keyless, plus
                                r/isthereatoolthat and r/SomebodyMakeThis feeds (about one request
                                a minute is all Reddit allows keyless, measured in P-0055). Writes
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
REDDIT = ["https://www.reddit.com/r/isthereatoolthat/new/.rss", "https://www.reddit.com/r/SomebodyMakeThis/new/.rss"]
# r/iWishThereWasAnApp answered 403 on 3 Oct, so it is out.
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
    for n, feed in enumerate(REDDIT):
        if n:
            time.sleep(65)
        try:
            body = get(feed).decode()
        except Exception as e:
            print(f"reddit {feed}: {e}")
            continue
        for entry in re.findall(r"<entry>(.*?)</entry>", body, re.S):
            link = re.search(r'<link href="([^"]+)"', entry)
            title = re.search(r"<title>(.*?)</title>", entry, re.S)
            when = re.search(r"<updated>(.*?)</updated>", entry)
            if link and title and "/comments/" in link.group(1) and (when.group(1) if when else "9") >= cutoff:
                out[link.group(1)] = {"src": "Reddit", "url": link.group(1), "when": (when.group(1) if when else "")[:10],
                                      "text": clean(title.group(1))[:300]}
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
