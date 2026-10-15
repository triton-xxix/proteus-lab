#!/Users/triton/PROTEUS/sandbox/skool-venv/bin/python
"""Transcript for a lesson video link, whichever host it is on. Tested 29 Sep 2026.

    skool_transcript.py <youtube|loom url> [--out file.txt] [--force-whisper]

Order of attempts:
  YouTube  1. captions through youtube_transcript_api (the harvester's route; 43 cached hits in
              field-notes/staging, but YouTube answered 429 to this IP on 29 Sep after a burst)
           2. yt-dlp bestaudio -> ffmpeg 16 kHz mono wav -> whisper-cli with ggml-base.en
              (audio downloads were not throttled when captions were; 3 min of audio took 58 s
              on the Intel i7, so about a third of real time)
  Loom     GraphQL FetchVideoTranscript gives a signed CDN URL; the JSON is a list of {ts, value}.
  Vimeo    the embed page (player.vimeo.com/video/<id>, Referer skool.com) carries text_tracks with
           a signed captions.vimeo.com VTT, usually "en-x-autogen". The /config route answers 403
           for these domain-locked videos; the embed page does not. Added 14 Oct 2026.
Nothing here needs a key or a login. Whisper output is marked as such in the header.
"""
import argparse, json, os, re, subprocess, sys, tempfile, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, "skool-tools", "models", "ggml-base.en.bin")
YTDLP = os.path.join(HERE, "skool-venv", "bin", "yt-dlp")


def yt_id(url):
    m = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([A-Za-z0-9_-]{11})", url)
    return m.group(1) if m else None


def loom_id(url):
    m = re.search(r"loom\.com/(?:share|embed)/([0-9a-f]{32})", url)
    return m.group(1) if m else None


def stamp(sec):
    return "[%02d:%02d]" % divmod(int(sec), 60)


def bucket(segs, width=30):
    """segs: list of (start_sec, text). Returns lines of about `width` seconds each."""
    lines, buf, start = [], [], None
    for s, t in segs:
        if start is None:
            start = s
        buf.append(t.strip())
        if s - start >= width:
            lines.append(stamp(start) + " " + " ".join(buf))
            buf, start = [], None
    if buf:
        lines.append(stamp(start or 0) + " " + " ".join(buf))
    return lines


def youtube_captions(vid):
    from youtube_transcript_api import YouTubeTranscriptApi
    api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(vid, languages=["en", "en-GB", "en-US"])
    except Exception:
        fetched = api.fetch(vid)
    raw = fetched.to_raw_data()
    return bucket([(s["start"], s["text"].replace("\n", " ")) for s in raw]), "captions"


def youtube_whisper(url):
    if not os.path.exists(MODEL):
        sys.exit("model missing: %s (curl it from huggingface.co/ggerganov/whisper.cpp)" % MODEL)
    tmp = tempfile.mkdtemp(prefix="yt_")
    subprocess.run([YTDLP, "-q", "-f", "bestaudio", "-o", os.path.join(tmp, "a.%(ext)s"), url], check=True)
    src = [f for f in os.listdir(tmp)][0]
    wav = os.path.join(tmp, "a.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(tmp, src), "-ac", "1", "-ar", "16000", wav], check=True)
    out = subprocess.run(["whisper-cli", "-m", MODEL, "-f", wav, "-np", "-oj", "-of", os.path.join(tmp, "a")],
                         capture_output=True, text=True)
    if out.returncode:
        sys.exit("whisper-cli failed: " + out.stderr[-500:])
    j = json.load(open(os.path.join(tmp, "a.json")))
    segs = [(s["offsets"]["from"] / 1000.0, s["text"]) for s in j["transcription"]]
    return bucket(segs), "whisper base.en (local)"


def loom(vid):
    q = {"operationName": "FetchVideoTranscript", "variables": {"videoId": vid, "password": None},
         "query": "query FetchVideoTranscript($videoId: ID!, $password: String) { fetchVideoTranscript(videoId: $videoId, password: $password) { ... on VideoTranscriptDetails { source_url captions_source_url language __typename } ... on GenericError { message __typename } __typename } }"}
    req = urllib.request.Request("https://www.loom.com/graphql", data=json.dumps(q).encode(), headers={
        "content-type": "application/json", "user-agent": "Mozilla/5.0",
        "x-loom-request-source": "loom_web_5ab3e", "apollographql-client-name": "web",
        "apollographql-client-version": "5ab3e"})
    d = json.load(urllib.request.urlopen(req, timeout=30))
    r = d.get("data", {}).get("fetchVideoTranscript") or {}
    u = r.get("source_url") or r.get("captions_source_url")
    if not u:
        sys.exit("loom: no transcript url: %s" % json.dumps(d)[:300])
    j = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"user-agent": "Mozilla/5.0"}), timeout=30))
    phrases = j["phrases"] if isinstance(j, dict) else j  # schemaVersion 1.1.3 wraps them
    return bucket([(x["ts"], x["value"]) for x in phrases]), "loom transcript"


def vimeo_id(url):
    m = re.search(r"vimeo\.com/(?:video/)?(\d{6,})", url)
    return m.group(1) if m else None


def vtt_time(t):
    p = t.replace(",", ".").split(":")
    return sum(float(x) * 60 ** i for i, x in enumerate(reversed(p)))


def vimeo(vid, referer="https://www.skool.com/"):
    ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
    page = urllib.request.urlopen(urllib.request.Request("https://player.vimeo.com/video/" + vid,
                                  headers={"user-agent": ua, "referer": referer}), timeout=30).read().decode("utf-8", "replace")
    m = re.search(r'"text_tracks":(\[.*?\])', page)
    tracks = json.loads(m.group(1)) if m else []
    if not tracks:
        sys.exit("vimeo: no text tracks on the embed page")
    tr = sorted(tracks, key=lambda t: (not t.get("lang", "").startswith("en"), t.get("lang") == "en-x-autogen"))[0]
    vtt = urllib.request.urlopen(urllib.request.Request(tr["url"], headers={"user-agent": ua}), timeout=30).read().decode("utf-8", "replace")
    segs = []
    for cue in re.split(r"\n\s*\n", vtt):
        tm = re.search(r"([\d:.,]+)\s*-->\s*[\d:.,]+", cue)
        if tm:
            text = " ".join(l for l in cue[tm.end():].strip().splitlines() if l.strip())
            segs.append((vtt_time(tm.group(1)), re.sub(r"<[^>]+>", "", text)))
    return bucket(segs), "vimeo captions (%s)" % tr.get("lang")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--out")
    ap.add_argument("--force-whisper", action="store_true")
    ap.add_argument("--captions-only", action="store_true", help="fail instead of falling back to whisper (15 Oct 2026: YouTube IP-blocked the captions API and every video went to whisper)")
    a = ap.parse_args()
    if loom_id(a.url):
        lines, how = loom(loom_id(a.url))
    elif vimeo_id(a.url):
        lines, how = vimeo(vimeo_id(a.url))
    elif yt_id(a.url):
        vid = yt_id(a.url)
        lines, how = None, None
        if not a.force_whisper:
            try:
                lines, how = youtube_captions(vid)
            except Exception as exc:
                sys.stderr.write("captions failed (%s), falling back to whisper\n" % type(exc).__name__)
        if lines is None:
            if a.captions_only:
                sys.exit("captions unavailable and --captions-only set")
            lines, how = youtube_whisper(a.url)
    else:
        sys.exit("not a YouTube, Loom or Vimeo url")
    text = "# %s\n# via %s\n\n%s\n" % (a.url, how, "\n".join(lines))
    if a.out:
        with open(a.out, "w") as fh:
            fh.write(text)
        print("wrote %s (%d lines, via %s)" % (a.out, len(lines), how))
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
