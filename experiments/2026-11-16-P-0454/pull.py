"""P-0454: six gap-fill videos, what fill rate and horizon each states, against P-0433's measurement.

Called shot (before the run): at most 2 of 6 state a fill rate, none gives a sample size, and any
rate stated is above 75% with no horizon.

Ids: the first six results after ieCrXvKLq3g (P-0433's own source) from one keyless YouTube search
for "gap fill win rate", 16 Nov 2026 (sandbox/p0454-search.html). Same fetch as P-0432: oEmbed for
titles, youtube_transcript_api for captions, one pass, stop at the first block. Transcripts stay in
sandbox/; counts and claim lines come here. Python run from the main venv (the library is there).
"""
import json, re, sys, time, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = Path("/Users/triton/PROTEUS/sandbox/watched-gapfill")
RAW.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-GB,en;q=0.8"}
IDS = ["oL7mWVSETuQ", "hUwkg6zLk5k", "dyqyDgIfbTQ", "Il6U9lArZs8", "qkChxbuUqvU", "96iPFDpXEcU"]

FILL = re.compile(r"(fill|filled|fills|filling)", re.I)
RATE = re.compile(r"(\d+(\.\d+)?)\s*(%|percent)", re.I)
HORIZON = re.compile(r"(same day|same-day|that day|within (the )?(first )?(\d+|an?|one|two|three|five) (minutes?|hours?|days?|weeks?)|by (the )?(close|end of (the )?day)|intraday|eventually)", re.I)
CNT = re.compile(r"(\d[\d,]*)\s+(trades|gaps|occurrences|samples|instances|times|days)\b", re.I)


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
        rates, horizons, counts = [], [], []
        for i, (start, t) in enumerate(snips):
            ctx = " ".join(x for _, x in snips[max(0, i - 2): i + 3])
            if RATE.search(t) and FILL.search(ctx):
                rates.append({"at_s": int(start), "pct": [m[0] for m in RATE.findall(t)], "text": ctx[:260]})
            if HORIZON.search(t) and FILL.search(ctx):
                horizons.append({"at_s": int(start), "text": ctx[:200]})
            if CNT.search(t):
                counts.append({"at_s": int(start), "text": ctx[:200]})
        row["fill_rate_lines"], row["horizon_lines"], row["count_lines"] = len(rates), len(horizons), len(counts)
        row["fill_rate_claims"], row["horizon_claims"], row["count_claims"] = rates[:10], horizons[:8], counts[:8]
        row["title_pct"] = RATE.findall(row.get("title") or "")
        rows.append(row)
        print("got", vid, "|", row.get("title"), "|", row.get("channel"), "|", row["minutes"], "min", row["words"], "words",
              len(rates), "rate lines", len(horizons), "horizon lines", len(counts), "count lines")
    (HERE / "videos.json").write_text(json.dumps({"ids": IDS, "blocked": blocked, "videos": rows}, indent=1))
    print("fetched", sum(1 for r in rows if "words" in r), "of", len(IDS), "; blocked", blocked)


if __name__ == "__main__":
    sys.exit(main())
