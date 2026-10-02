"""P-0055: does a keyless fetch of Reddit RSS/JSON return text from this machine?"""
import json
import time
import urllib.request
from pathlib import Path

OUT = Path(__file__).parent
URLS = [
    ("sub_rss", "https://www.reddit.com/r/solana/.rss"),
    ("sub_rss_old", "https://old.reddit.com/r/solana/.rss"),
    ("sub_json", "https://www.reddit.com/r/solana/new.json?limit=10"),
    ("search_rss", "https://www.reddit.com/search.rss?q=pump.fun&sort=new"),
]
UAS = {
    "browser": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/128 Safari/537.36",
    "script": "proteus-probe/0.1 (research; contact via github triton-xxix)",
}
results = []


def get(url, ua):
    t = time.time()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        with urllib.request.urlopen(req, timeout=20) as r:
            body = r.read()
            return {"status": r.status, "bytes": len(body), "secs": round(time.time() - t, 2),
                    "ctype": r.headers.get("Content-Type"), "head": body[:160].decode("utf8", "replace")}, body
    except urllib.error.HTTPError as e:
        return {"status": e.code, "error": str(e), "secs": round(time.time() - t, 2)}, b""
    except Exception as e:
        return {"status": None, "error": f"{type(e).__name__}: {e}", "secs": round(time.time() - t, 2)}, b""


thread_url = None
for name, url in URLS:
    for uan, ua in UAS.items():
        res, body = get(url, ua)
        res.update(name=name, url=url, ua=uan)
        if body and name == "sub_rss" and b"<entry>" in body:
            res["entries"] = body.count(b"<entry>")
            # first thread link for the thread-feed test
            i = body.find(b'<link href="https://www.reddit.com/r/solana/comments/')
            if i > 0 and not thread_url:
                j = body.find(b'"', i + 12)
                thread_url = body[i + 12:j].decode()
        results.append(res)
        time.sleep(2)

if thread_url:
    for uan, ua in UAS.items():
        res, body = get(thread_url.rstrip("/") + "/.rss", ua)
        res.update(name="thread_rss", url=thread_url, ua=uan)
        if body:
            res["entries"] = body.count(b"<entry>")
        results.append(res)
        time.sleep(2)

(OUT / "results.json").write_text(json.dumps(results, indent=1))
for r in results:
    print(r["name"], r["ua"], r["status"], r.get("bytes"), r.get("entries"), r.get("error", "")[:80])
