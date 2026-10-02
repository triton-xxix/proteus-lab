"""P-0055 part 2: thread feed alone, after a 60 s cool-off, one request every 10 s."""
import json
import re
import time
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent
UA = "proteus-probe/0.1 (research; contact via github triton-xxix)"
time.sleep(60)


def get(url):
    t = time.time()
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=20) as r:
            b = r.read()
            return r.status, b, round(time.time() - t, 2), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, b"", round(time.time() - t, 2), dict(e.headers or {})


st, body, secs, hdr = get("https://www.reddit.com/r/solana/.rss")
links = re.findall(rb'<link href="(https://www.reddit.com/r/solana/comments/[^"]+)"', body)[:3]
out = [{"url": "sub_rss", "status": st, "bytes": len(body), "secs": secs,
        "ratelimit": {k: v for k, v in hdr.items() if "ratelimit" in k.lower() or k.lower() == "retry-after"}}]
for link in links:
    time.sleep(10)
    st, b, secs, hdr = get(link.decode().rstrip("/") + "/.rss")
    out.append({"url": link.decode(), "status": st, "bytes": len(b), "secs": secs,
                "entries": b.count(b"<entry>"),
                "ratelimit": {k: v for k, v in hdr.items() if "ratelimit" in k.lower() or k.lower() == "retry-after"}})
(OUT / "results-slow.json").write_text(json.dumps(out, indent=1))
for o in out:
    print(o["status"], o["bytes"], o.get("entries"), o["ratelimit"])
