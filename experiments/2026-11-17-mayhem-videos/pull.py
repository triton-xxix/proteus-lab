"""Watched-it, 17 Nov 2026: what YouTube says pump.fun's mayhem mode does to fees,
against the trade events I decoded today (P-0464, P-0465, the pump-trades tool).

Keyless: YouTube search HTML for ids, oEmbed for titles, youtube_transcript_api for captions.
Transcripts stay in sandbox/ (gitignored); only counts and short claim lines are written here.
Stops at the first block (IpBlocked or 429) rather than hammering.
"""
import json, re, sys, urllib.parse, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = Path("/Users/triton/PROTEUS/sandbox/watched-mayhem")
RAW.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0", "Accept-Language": "en-GB,en;q=0.8"}
QUERY = "pump.fun mayhem mode explained"
N = 5


def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")


def main():
    html = get("https://www.youtube.com/results?search_query=" + urllib.parse.quote(QUERY))
    ids = []
    for vid in re.findall(r'"videoId":"([A-Za-z0-9_-]{11})"', html):
        if vid not in ids:
            ids.append(vid)
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    out = []
    pat = re.compile(r"(fee|free|agent|\bai\b|bot|percent|%|supply|billion|24 hours|burn|buyback)", re.I)
    for vid in ids[:14]:
        if len(out) >= N:
            break
        row = {"id": vid}
        try:
            meta = json.loads(get("https://www.youtube.com/oembed?format=json&url=https://www.youtube.com/watch?v=" + vid))
            row["title"], row["channel"] = meta.get("title"), meta.get("author_name")
        except Exception as e:
            row["title_error"] = repr(e)[:120]
        try:
            fetched = api.fetch(vid, languages=["en", "en-GB", "en-US"])
            snips = [(s.start, s.text.replace("\n", " ")) for s in fetched]
        except Exception as e:
            name = type(e).__name__
            print("no transcript", vid, name)
            if name in ("IpBlocked", "RequestBlocked", "YouTubeRequestFailed"):
                print("BLOCKED, stopping")
                break
            continue
        text = " ".join(t for _, t in snips)
        (RAW / (vid + ".txt")).write_text(text)
        row["words"] = len(text.split())
        row["minutes"] = round((snips[-1][0] if snips else 0) / 60, 1)
        row["mayhem_mentions"] = len(re.findall(r"mayhem", text, re.I))
        row["fee_mentions"] = len(re.findall(r"\bfees?\b", text, re.I))
        claims = []
        for i, (start, t) in enumerate(snips):
            near = " ".join(x for _, x in snips[max(0, i - 2): i + 3])
            if pat.search(t) and re.search(r"mayhem", near, re.I):
                claims.append({"at_s": int(start), "text": near[:320]})
        row["claim_lines"] = len(claims)
        row["claims"] = claims[:16]
        out.append(row)
        print("ok", vid, row.get("title"), "|", row.get("channel"), "|", row["words"], "words", row["minutes"], "min, mayhem", row["mayhem_mentions"], "fee", row["fee_mentions"])
    (HERE / "videos.json").write_text(json.dumps({"query": QUERY, "ids_found": len(ids), "videos": out}, indent=1))
    print("wrote", len(out), "videos of", len(ids), "ids")


if __name__ == "__main__":
    sys.exit(main())
