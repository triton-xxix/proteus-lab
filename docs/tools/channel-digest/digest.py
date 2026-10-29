"""Channel digest: a YouTube channel's recent uploads, keyless, with the lines worth checking flagged.

python3 digest.py <channel> [<channel> ...] [--days 7] [--max 5] [--out DIR]

<channel> is a handle (@Unabated), a channel id (UC...), a channel URL, or any video id or URL
from the channel (its channel is looked up from the watch page). Uploads come from the channel's
public RSS feed (the last 15), transcripts from youtube-transcript-api. Writes digest.json and
digest.md to --out (default: this folder).

"Checkable" is a flag, not a check: a sentence scores for a percentage, a number, a comparison
or an absolute word ("always", "never"). The top ones per video are listed with a timestamp
link so a person can go and test them. Big Expedition step one, 29 Oct 2026.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (Macintosh) channel-digest/0.1", "Accept-Language": "en-GB,en;q=0.8"}
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
      "media": "http://search.yahoo.com/mrss/"}

PCT = re.compile(r"\d+(\.\d+)?\s*(%|percent|per cent)", re.I)
NUM = re.compile(r"\b\d[\d,.]*\b")
YEAR = re.compile(r"\b(19|20)\d\d\b")
COMPARE = re.compile(r"\b(more than|less than|better than|worse than|beats?|outperform\w*|on average|"
                     r"win rate|rate of|times as|twice|half of|majority|most of|edge)\b", re.I)
ABSOLUTE = re.compile(r"\b(always|never|every|guaranteed|proven|the only)\b", re.I)


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def channel_id(arg):
    if re.fullmatch(r"UC[\w-]{22}", arg):
        return arg
    m = re.search(r"/channel/(UC[\w-]{22})", arg)
    if m:
        return m.group(1)
    vid = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", arg)
    if vid or re.fullmatch(r"[\w-]{11}", arg):
        html = get("https://www.youtube.com/watch?v=" + (vid.group(1) if vid else arg))
    else:
        handle = arg if arg.startswith("http") else "https://www.youtube.com/" + ("" if arg.startswith("@") else "@") + arg
        html = get(handle)
    m = re.search(r'"channelId":"(UC[\w-]{22})"', html) or re.search(r'"externalId":"(UC[\w-]{22})"', html)
    if not m:
        raise ValueError("no channel id found for " + arg)
    return m.group(1)


def uploads(cid):
    root = ET.fromstring(get("https://www.youtube.com/feeds/videos.xml?channel_id=" + cid))
    name = root.findtext("a:title", "", NS).strip()
    out = []
    for e in root.findall("a:entry", NS):
        out.append({"id": e.findtext("yt:videoId", "", NS), "title": e.findtext("a:title", "", NS),
                    "published": e.findtext("a:published", "", NS)})
    return name, out


def transcript(vid):
    from youtube_transcript_api import YouTubeTranscriptApi
    try:
        segs = YouTubeTranscriptApi().fetch(vid, languages=["en", "en-GB", "en-US"])
        return [(s.start, s.text) for s in segs]
    except AttributeError:
        return [(s["start"], s["text"]) for s in YouTubeTranscriptApi.get_transcript(vid, languages=["en"])]


def sentences(rows):
    """Caption segments rarely carry full stops, so cut on punctuation where there is some and
    every 30 words where there is none. Each piece keeps the start time of its first segment."""
    out, buf, t0 = [], [], None
    for t, text in rows:
        text = re.sub(r"\[(music|applause|laughter)\]|>>", " ", text.replace("\n", " "), flags=re.I)
        for w in text.split():
            if t0 is None:
                t0 = t
            buf.append(w)
            if w[-1:] in ".?!" or len(buf) >= 30:
                out.append((t0, " ".join(buf)))
                buf, t0 = [], None
    if buf:
        out.append((t0, " ".join(buf)))
    return out


def score(s):
    n = 0
    n += 3 if PCT.search(s) else 0
    n += min(2, len([x for x in NUM.findall(s) if not YEAR.fullmatch(x)]))
    n += 1 if YEAR.search(s) else 0
    n += 2 if COMPARE.search(s) else 0
    n += 1 if ABSOLUTE.search(s) else 0
    return n


def flag(rows, top):
    scored = [(score(s), t, s) for t, s in sentences(rows) if len(s.split()) >= 6]
    keep = sorted([x for x in scored if x[0] >= 3], key=lambda x: (-x[0], x[1]))[:top]
    return len(scored), [{"t": int(t), "score": n, "text": s} for n, t, s in sorted(keep, key=lambda x: x[1])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("channels", nargs="+")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--max", type=int, default=5, help="videos per channel")
    ap.add_argument("--top", type=int, default=5, help="flagged lines per video")
    ap.add_argument("--out", default=HERE)
    a = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc)
    since = now - dt.timedelta(days=a.days)
    digest = {"built": now.strftime("%Y-%m-%d %H:%M UTC"), "days": a.days, "channels": []}
    for arg in a.channels:
        ch = {"arg": arg, "videos": [], "error": None}
        try:
            ch["id"] = channel_id(arg)
            ch["name"], vids = uploads(ch["id"])
            ch["feed_count"] = len(vids)
            recent = [v for v in vids if dt.datetime.fromisoformat(v["published"]) >= since]
            ch["in_window"] = len(recent)
            for v in recent[:a.max]:
                try:
                    rows = transcript(v["id"])
                    v["words"] = sum(len(x.split()) for _, x in rows)
                    v["minutes"] = round(rows[-1][0] / 60, 1) if rows else 0
                    v["sentences"], v["flags"] = flag(rows, a.top)
                except Exception as e:
                    v["error"] = "%s: %s" % (type(e).__name__, str(e)[:120])
                ch["videos"].append(v)
        except Exception as e:
            ch["error"] = "%s: %s" % (type(e).__name__, str(e)[:160])
        digest["channels"].append(ch)
        print(ch.get("name", arg), "|", ch.get("in_window", "-"), "in window of", ch.get("feed_count", "-"),
              "| transcripts", sum(1 for v in ch["videos"] if "words" in v), "| error", ch["error"])
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, "digest.json"), "w") as f:
        json.dump(digest, f, indent=1)
    md = ["# Channel digest, last %d days, built %s" % (a.days, digest["built"]), ""]
    for ch in digest["channels"]:
        md.append("## %s" % ch.get("name", ch["arg"]))
        if ch["error"]:
            md += ["", "Error: " + ch["error"], ""]
            continue
        full = " The whole feed is inside the window, so there may be more." if ch["in_window"] == ch["feed_count"] else ""
        md += ["", "%d uploads in the window (feed holds the last %d).%s" % (ch["in_window"], ch["feed_count"], full), ""]
        for v in ch["videos"]:
            md.append("### [%s](https://youtu.be/%s) (%s)" % (v["title"], v["id"], v["published"][:10]))
            if v.get("error"):
                md += ["", "No transcript: " + v["error"], ""]
                continue
            md += ["", "%s words, %s min, %d of %d sentences flagged." % (
                f"{v['words']:,}", v["minutes"], len(v["flags"]), v["sentences"]), ""]
            for fl in v["flags"]:
                md.append("- [%d:%02d](https://youtu.be/%s?t=%d) %s" % (fl["t"] // 60, fl["t"] % 60, v["id"], fl["t"], fl["text"]))
            md.append("")
    with open(os.path.join(a.out, "digest.md"), "w") as f:
        f.write("\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
