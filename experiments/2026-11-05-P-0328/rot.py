"""P-0328: P-0320's rot.py unchanged except the windows: comments from before 1 Jan 2012 and before
1 Jan 2014, up to 100 unique YouTube ids per window, checked by oEmbed 1 s apart.
oEmbed: 200 resolves, 401 embedding disabled (video exists), 404 gone, 403 private or restricted.

    python3 -I experiments/2026-11-05-P-0328/rot.py
"""
import collections
import html
import json
import pathlib
import re
import time
import urllib.error
import urllib.request

OUT = pathlib.Path(__file__).parent
UA = {"User-Agent": "proteus-research/1.0"}
ID = re.compile(r'(?:youtube\.com/watch\?v=|youtube\.com/watch\?[^"\s<]*?&v=|youtu\.be/|youtube\.com/shorts/|youtube\.com/embed/)([A-Za-z0-9_-]{11})')
WINDOWS = {"end-2011": 1325376000, "end-2013": 1388534400}
CAP = 100


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20)


res = {"p0320": {"end-2016": 0.72, "end-2021": 0.86, "fresh_p0313": round(149 / 150, 3)}, "windows": {}}
stop = False
for name, cut in WINDOWS.items():
    ids = collections.OrderedDict()
    read = 0
    for q in ["youtube.com", "youtu.be"]:
        for page in range(2):
            url = ("https://hn.algolia.com/api/v1/search_by_date?tags=comment&query=%s&hitsPerPage=100&page=%d"
                   "&numericFilters=created_at_i%%3C%d" % (q, page, cut))
            data = json.load(get(url))
            for h in data["hits"]:
                for m in ID.finditer(html.unescape(h.get("comment_text") or "")):
                    ids.setdefault(m.group(1), (h["created_at"], h["objectID"]))
            read += len(data["hits"])
    status = collections.Counter()
    rows = []
    for vid, (when, oid) in list(ids.items())[:CAP]:
        try:
            code = get("https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=%s&format=json" % vid).status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:  # noqa: BLE001
            code = type(e).__name__
        status[code] += 1
        rows.append({"id": vid, "comment_at": when, "comment": oid, "oembed": code})
        if code == 429:
            print("429, stopping")
            stop = True
            break
        time.sleep(1)
    n = len(rows)
    res["windows"][name] = {"comments_read": read, "unique_ids": len(ids), "ids_checked": n,
                            "status": {str(k): v for k, v in status.items()},
                            "resolve_share": round(status.get(200, 0) / n, 3) if n else None,
                            "exists_share": round((status.get(200, 0) + status.get(401, 0)) / n, 3) if n else None,
                            "oldest": min(r["comment_at"] for r in rows) if rows else None,
                            "newest": max(r["comment_at"] for r in rows) if rows else None,
                            "rows": rows}
    print(name, {k: v for k, v in res["windows"][name].items() if k != "rows"}, flush=True)
    if stop:
        break
(OUT / "results.json").write_text(json.dumps(res, indent=1))
