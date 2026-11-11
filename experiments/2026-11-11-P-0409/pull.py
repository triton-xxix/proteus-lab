"""P-0409: what real gap-and-go videos state. The 10 Nov watched-it pull.py with the exact phrase
in the query, a five-minute floor and a check that the captions actually say "gap and go".

Keyless: YouTube search HTML for ids, oEmbed for titles, youtube_transcript_api for captions.
Transcripts stay in sandbox/ (gitignored); only counts and short claim lines are written here.
Stops at the first block (IpBlocked or 429) rather than hammering. At most five kept, twelve tried.
"""
import json, re, sys, time, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = Path("/Users/triton/PROTEUS/sandbox/watched-gapgo-2")
RAW.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-GB,en;q=0.8"}
QUERY = '"gap and go" strategy backtest'
N, TRIES, FLOOR_MIN = 5, 30, 5.0   # first run tried 12 and kept 1; second run tries 30, same filters


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read().decode("utf-8", "replace")


def main():
    html = get("https://www.youtube.com/results?search_query=" + urllib.parse.quote(QUERY))
    ids = []
    for vid in re.findall(r'"videoId":"([A-Za-z0-9_-]{11})"', html):
        if vid not in ids:
            ids.append(vid)
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    kept, dropped, blocked = [], [], False
    win = re.compile(r"(win rate|win percentage|winning percentage|winners|accuracy|percent of the time|% of the time|profit factor)", re.I)
    cnt = re.compile(r"(\d[\d,]*)\s+(trades|setups|gaps|occurrences|samples|instances|times)\b", re.I)
    for vid in ids[:TRIES]:
        if len(kept) >= N:
            break
        row = {"id": vid}
        try:
            meta = json.loads(get("https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v=" + vid))
            row["title"], row["channel"] = meta.get("title"), meta.get("author_name")
        except Exception as e:
            row["title_error"] = type(e).__name__
        try:
            fetched = api.fetch(vid, languages=["en", "en-GB", "en-US"])
            snips = [(s.start, s.text.replace("\n", " ")) for s in fetched]
        except Exception as e:
            name = type(e).__name__
            row["dropped"] = "no transcript: " + name
            dropped.append(row)
            print("no transcript", vid, name)
            if name in ("IpBlocked", "RequestBlocked", "YouTubeRequestFailed"):
                blocked = True
                print("BLOCKED, stopping")
                break
            continue
        time.sleep(1.5)
        text = " ".join(t for _, t in snips)
        row["words"] = len(text.split())
        row["minutes"] = round((snips[-1][0] if snips else 0) / 60, 1)
        row["gap_and_go_mentions"] = len(re.findall(r"gap[\s-]*(and|&|n)[\s-]*go", text, re.I))
        if row["minutes"] < FLOOR_MIN:
            row["dropped"] = "under five minutes"
        elif row["gap_and_go_mentions"] == 0:
            row["dropped"] = "captions never say gap and go"
        if "dropped" in row:
            dropped.append(row)
            print("dropped", vid, row.get("title"), row["dropped"])
            continue
        (RAW / (vid + ".txt")).write_text(text)
        wins, counts = [], []
        for i, (start, t) in enumerate(snips):
            ctx = " ".join(x for _, x in snips[max(0, i - 1): i + 2])
            if win.search(t) and re.search(r"\d", ctx):
                wins.append({"at_s": int(start), "text": ctx[:240]})
            if cnt.search(t):
                counts.append({"at_s": int(start), "text": ctx[:240]})
        row["win_lines"], row["count_lines"] = len(wins), len(counts)
        row["win_claims"], row["count_claims"] = wins[:10], counts[:10]
        kept.append(row)
        print("kept", vid, row.get("title"), row["minutes"], "min", row["gap_and_go_mentions"], "mentions", len(wins), "win lines", len(counts), "count lines")
    (HERE / "videos.json").write_text(json.dumps({"query": QUERY, "ids_found": len(ids), "tried": len(kept) + len(dropped),
                                                  "blocked": blocked, "kept": kept, "dropped": dropped}, indent=1))
    print("kept", len(kept), "dropped", len(dropped), "of", len(ids), "ids; blocked", blocked)


if __name__ == "__main__":
    sys.exit(main())
