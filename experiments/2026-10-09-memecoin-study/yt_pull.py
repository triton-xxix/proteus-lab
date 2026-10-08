"""Pull YouTube transcripts on Solana meme-coin selection and rug detection, keyless.

Searches YouTube's results page for each query, takes the top videos, fetches oEmbed (title,
channel) and the English transcript, and writes one text file per video plus index.json into
OUT. Usage: python yt_pull.py OUT_DIR
"""
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request

from youtube_transcript_api import YouTubeTranscriptApi

QUERIES = [
    "how to spot a rug pull solana memecoin before buying",
    "solana memecoin trading strategy dev wallet bundle check",
    "how I find 100x memecoins pump.fun after migration",
    "gmgn smart money wallet tracking memecoin",
    "memecoin insider bundled supply sniper wallets explained",
    "why memecoins dump then recover dead cat bounce solana",
]
PER_QUERY = 3
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/129.0 Safari/537.36",
      "Accept-Language": "en-GB,en;q=0.9"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def main():
    out = pathlib.Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    api = YouTubeTranscriptApi()
    seen, index = set(), []
    for q in QUERIES:
        html = get("https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(q))
        ids = []
        for vid in re.findall(r'"videoId":"([A-Za-z0-9_-]{11})"', html):
            if vid not in ids:
                ids.append(vid)
        taken = 0
        for vid in ids:
            if taken >= PER_QUERY:
                break
            if vid in seen:
                continue
            seen.add(vid)
            try:
                meta = json.loads(get("https://www.youtube.com/oembed?" + urllib.parse.urlencode(
                    {"url": "https://www.youtube.com/watch?v=" + vid, "format": "json"})))
            except Exception:
                continue
            try:
                tr = api.fetch(vid, languages=["en", "en-GB", "en-US"])
                text = " ".join(s.text for s in tr.snippets)
            except Exception as e:
                index.append({"id": vid, "query": q, "title": meta.get("title"), "channel": meta.get("author_name"),
                              "transcript": False, "error": type(e).__name__})
                continue
            if len(text) < 1500:
                continue
            (out / (vid + ".txt")).write_text("%s\n%s\nhttps://www.youtube.com/watch?v=%s\n\n%s" % (
                meta.get("title"), meta.get("author_name"), vid, text))
            index.append({"id": vid, "query": q, "title": meta.get("title"), "channel": meta.get("author_name"),
                          "transcript": True, "chars": len(text)})
            taken += 1
            time.sleep(1)
    (out / "index.json").write_text(json.dumps(index, indent=1))
    print(sum(x["transcript"] for x in index), "transcripts of", len(index), "videos tried")


if __name__ == "__main__":
    main()
