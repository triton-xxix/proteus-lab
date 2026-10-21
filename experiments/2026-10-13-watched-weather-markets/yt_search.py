"""Keyless YouTube search: video ids from the results page, titles via oEmbed."""
import json, re, sys, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-GB"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode("utf-8", "replace")


def search(q, n=8):
    html = get("https://www.youtube.com/results?search_query=" + urllib.parse.quote(q))
    ids = []
    for vid in re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html):
        if vid not in ids:
            ids.append(vid)
    out = []
    for vid in ids[:n]:
        try:
            meta = json.loads(get("https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v=" + vid))
            out.append((vid, meta.get("author_name"), meta.get("title")))
        except Exception as e:
            out.append((vid, "?", f"oembed failed {e}"))
    return out


if __name__ == "__main__":
    for q in sys.argv[1:]:
        print("##", q)
        for row in search(q):
            print(" | ".join(str(x) for x in row))
