"""P-0056: youtube-transcript-plus 2.0.3's fetch path, ported line for line to Python
(npm and node are off the unattended safe list), run on the three videos that drew IpBlocked
from youtube-transcript-api in tonight's harvest. Control: youtube-transcript-api on the same IDs.
"""
import json
import re
import time
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")
RE_XML = re.compile(r'<text start="([^"]*)" dur="([^"]*)">([^<]*)</text>')
IDS = ["Ir0Q9s6P050", "JIh6h8mx0Zk", "Ao7fbajRSKI"]


def req(url, data=None, headers=None):
    h = {"User-Agent": UA}
    h.update(headers or {})
    r = urllib.request.Request(url, data=data, headers=h, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return resp.status, resp.read().decode("utf8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf8", "replace")


def plus(vid):
    t = time.time()
    st, page = req(f"https://www.youtube.com/watch?v={vid}")
    if st != 200:
        return {"stage": "watch", "status": st}
    if 'class="g-recaptcha"' in page:
        return {"stage": "watch", "error": "recaptcha"}
    m = re.search(r'"INNERTUBE_API_KEY":"([^"]+)"', page)
    if not m:
        return {"stage": "apikey", "error": "no key"}
    body = json.dumps({"context": {"client": {"clientName": "ANDROID", "clientVersion": "20.10.38"}},
                       "videoId": vid}).encode()
    st, pj = req(f"https://www.youtube.com/youtubei/v1/player?key={m.group(1)}", body,
                 {"Content-Type": "application/json"})
    if st != 200:
        return {"stage": "player", "status": st}
    pj = json.loads(pj)
    play = (pj.get("playabilityStatus") or {})
    tl = (pj.get("captions") or {}).get("playerCaptionsTracklistRenderer")
    tracks = (tl or {}).get("captionTracks") or []
    if not tracks:
        return {"stage": "tracks", "playability": play.get("status"), "reason": play.get("reason")}
    url = re.sub(r"&fmt=[^&]+", "", tracks[0]["baseUrl"])
    st, xml = req(url)
    segs = RE_XML.findall(xml)
    return {"stage": "done", "status": st, "lang": tracks[0].get("languageCode"),
            "tracks": len(tracks), "segments": len(segs), "chars": sum(len(s[2]) for s in segs),
            "first": segs[0][2][:80] if segs else None, "xml_bytes": len(xml),
            "title": (pj.get("videoDetails") or {}).get("title"), "secs": round(time.time() - t, 1)}


def control(vid):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        api = YouTubeTranscriptApi()
        tr = api.fetch(vid)
        return {"ok": True, "segments": len(tr.snippets)}
    except Exception as e:
        return {"ok": False, "error": type(e).__name__}


out = []
for vid in IDS:
    row = {"id": vid, "plus_port": plus(vid)}
    time.sleep(3)
    row["control_youtube_transcript_api"] = control(vid)
    out.append(row)
    time.sleep(3)
(OUT / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
