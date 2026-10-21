#!/usr/bin/env python3
"""Keyless YouTube search: print video id, duration, title, channel for a query.

Usage: yt_search.py "query" [--n 10]
Reads the results page HTML and parses ytInitialData. No key, no login.
"""
import json
import re
import sys
import urllib.parse
import urllib.request


def fetch(query):
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
        "Accept-Language": "en-GB,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def walk(node, out):
    if isinstance(node, dict):
        if "videoRenderer" in node:
            v = node["videoRenderer"]
            vid = v.get("videoId")
            title = "".join(r.get("text", "") for r in v.get("title", {}).get("runs", []))
            chan = "".join(r.get("text", "") for r in v.get("ownerText", {}).get("runs", []))
            dur = v.get("lengthText", {}).get("simpleText", "")
            views = v.get("viewCountText", {}).get("simpleText", "")
            pub = v.get("publishedTimeText", {}).get("simpleText", "")
            out.append((vid, dur, views, pub, chan, title))
        for val in node.values():
            walk(val, out)
    elif isinstance(node, list):
        for val in node:
            walk(val, out)


def main():
    args = sys.argv[1:]
    n = 10
    if "--n" in args:
        i = args.index("--n")
        n = int(args[i + 1])
        del args[i:i + 2]
    query = " ".join(args)
    html = fetch(query)
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
    if not m:
        print("no ytInitialData found", file=sys.stderr)
        sys.exit(1)
    data = json.loads(m.group(1))
    out = []
    walk(data, out)
    seen = set()
    for vid, dur, views, pub, chan, title in out:
        if vid in seen:
            continue
        seen.add(vid)
        print(f"{vid}\t{dur}\t{views}\t{pub}\t{chan}\t{title}")
        if len(seen) >= n:
            break


if __name__ == "__main__":
    main()
