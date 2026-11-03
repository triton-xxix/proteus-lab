"""P-0313: share of YouTube links in recent HN comments that still resolve via oEmbed.
Keyless: HN Algolia search_by_date over comments, then YouTube oEmbed per unique id (1 s apart)."""
import html, json, re, time, urllib.request, urllib.error, pathlib, collections

OUT = pathlib.Path(__file__).parent
UA = {"User-Agent": "proteus-research/1.0"}
ID = re.compile(r'(?:youtube\.com/watch\?v=|youtube\.com/watch\?[^"\s<]*?&v=|youtu\.be/|youtube\.com/shorts/|youtube\.com/embed/)([A-Za-z0-9_-]{11})')

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=20)

hits, ids = [], collections.OrderedDict()
for q in ["youtube.com", "youtu.be"]:
    for page in range(3):
        url = f"https://hn.algolia.com/api/v1/search_by_date?tags=comment&query={q}&hitsPerPage=100&page={page}"
        data = json.load(get(url))
        for h in data["hits"]:
            for m in ID.finditer(html.unescape(h.get("comment_text") or "")):
                ids.setdefault(m.group(1), (h["created_at"], h["objectID"]))
        hits.extend(data["hits"])
print(f"comments read {len(hits)}, unique video ids {len(ids)}")

ids = list(ids.items())[:150]
status = collections.Counter()
rows = []
for vid, (when, oid) in ids:
    try:
        r = get(f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json")
        code = r.status
    except urllib.error.HTTPError as e:
        code = e.code
    except Exception as e:
        code = type(e).__name__
    status[code] += 1
    rows.append({"id": vid, "comment_at": when, "comment": oid, "oembed": code})
    if code == 429:
        print("429, stopping")
        break
    time.sleep(1)

n = len(rows)
ok = status.get(200, 0)
summary = {"comments_read": len(hits), "ids_checked": n, "status": {str(k): v for k, v in status.items()},
           "resolve_share": round(ok / n, 3) if n else None,
           "oldest_comment": min(r["comment_at"] for r in rows) if rows else None,
           "newest_comment": max(r["comment_at"] for r in rows) if rows else None}
print(json.dumps(summary, indent=1))
(OUT / "results.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
