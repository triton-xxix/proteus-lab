"""P-0432: the six short gap-and-go videos P-0409 dropped under its five-minute floor.

Same fetch and the same two regexes as experiments/2026-11-11-P-0409/pull.py, no search step and no
length floor: the ids are fixed. Keyless: oEmbed for titles, youtube_transcript_api for captions.
Transcripts stay in sandbox/ (gitignored); counts and short claim lines are written here.
Stops at the first block rather than hammering. One pass, no retry.
"""
import json, re, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = Path("/Users/triton/PROTEUS/sandbox/watched-gapgo-3")
RAW.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-GB,en;q=0.8"}
IDS = ["6PLI1Wvn3fE", "VsF0W2FuQOM", "WCuEgMPvKwc", "sEpI4T4UvhU", "9Y4x-QKkZqU", "d9mDpbN4zFI"]

WIN = re.compile(r"(win rate|winrate|win percentage|winning percentage|winners|accuracy|percent of the time|% of the time|profit factor|success rate)", re.I)
CNT = re.compile(r"(\d[\d,]*)\s+(trades|setups|gaps|occurrences|samples|instances|times)\b", re.I)
PCT = re.compile(r"\d+(\.\d+)?\s*(%|percent)", re.I)


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25).read().decode("utf-8", "replace")


def main():
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    rows, blocked = [], False
    for vid in IDS:
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
            row["error"] = name
            rows.append(row)
            print("no transcript", vid, name)
            if name in ("IpBlocked", "RequestBlocked", "YouTubeRequestFailed"):
                blocked = True
                print("BLOCKED, stopping")
                break
            continue
        time.sleep(2.0)
        text = " ".join(t for _, t in snips)
        (RAW / (vid + ".txt")).write_text(text)
        row["words"] = len(text.split())
        row["minutes"] = round((snips[-1][0] if snips else 0) / 60, 1)
        row["gap_and_go_mentions"] = len(re.findall(r"gap[\s-]*(and|&|n)[\s-]*go", text, re.I))
        wins, counts, pcts = [], [], []
        for i, (start, t) in enumerate(snips):
            ctx = " ".join(x for _, x in snips[max(0, i - 1): i + 2])
            if WIN.search(t) and re.search(r"\d", ctx):
                wins.append({"at_s": int(start), "text": ctx[:240]})
            if CNT.search(t):
                counts.append({"at_s": int(start), "text": ctx[:240]})
            if PCT.search(t):
                pcts.append({"at_s": int(start), "text": ctx[:240]})
        row["win_lines"], row["count_lines"], row["percent_lines"] = len(wins), len(counts), len(pcts)
        row["win_claims"], row["count_claims"], row["percent_claims"] = wins[:10], counts[:10], pcts[:12]
        row["title_has_win_rate"] = bool(re.search(r"win\s*rate|winrate|\d+\s*%", row.get("title") or "", re.I))
        rows.append(row)
        print("got", vid, "|", row.get("title"), "|", row.get("channel"), "|", row["minutes"], "min", row["words"], "words",
              row["gap_and_go_mentions"], "mentions", len(wins), "win lines", len(counts), "count lines", len(pcts), "percent lines")
    (HERE / "videos.json").write_text(json.dumps({"ids": IDS, "blocked": blocked, "videos": rows}, indent=1))
    print("fetched", sum(1 for r in rows if "words" in r), "of", len(IDS), "; blocked", blocked)


if __name__ == "__main__":
    sys.exit(main())
