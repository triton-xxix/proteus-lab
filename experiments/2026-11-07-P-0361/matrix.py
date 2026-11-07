"""P-0361: which factor draws Wikimedia's refusal for Python urllib (P-0339) when curl was served?
Cells: client (python urllib here; curl via curl.cfg), user agent (bare lab name v name plus contact URL),
endpoint (api.php prop=pageviews, api.php prop=info, REST page/html). Two tries a cell, 4 s apart.
Writes results.json beside this file. Usage: python3 -I matrix.py
"""
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
UAS = {
    "bare": "ProteusLab-pageviews-check/1.1",
    "contact": "ProteusLab-pageviews-check/1.1 (https://github.com/triton-xxix; one-off research script)",
}
ENDS = {
    "api_pageviews": "https://en.wikipedia.org/w/api.php?action=query&prop=pageviews&titles=Philosophy&pvipdays=5&format=json&formatversion=2",
    "api_info": "https://en.wikipedia.org/w/api.php?action=query&prop=info&titles=Philosophy&format=json&formatversion=2",
    "rest_html": "https://en.wikipedia.org/api/rest_v1/page/html/Philosophy",
}
rows = []
for ua_name, ua in UAS.items():
    for end_name, url in ENDS.items():
        for attempt in (1, 2):
            t = time.time()
            try:
                with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": ua}), timeout=30) as r:
                    code, body = r.status, r.read(200)
            except urllib.error.HTTPError as e:
                code, body = e.code, e.read(200)
            except Exception as e:
                code, body = "error", str(e)[:100].encode()
            rows.append({"client": "python-urllib", "ua": ua_name, "endpoint": end_name, "attempt": attempt,
                         "code": code, "refused_text": b"too many" in body.lower(),
                         "secs": round(time.time() - t, 2), "at": time.strftime("%H:%M:%S")})
            print(rows[-1], flush=True)
            time.sleep(4)
(HERE / "results.json").write_text(json.dumps(rows, indent=1))

# curl config for the same cells, run separately: curl -K curl.cfg  (writes one file per cell)
lines = ["silent", 'rate = "15/m"']
for ua_name, ua in UAS.items():
    for end_name, url in ENDS.items():
        lines += [f'url = "{url}"', f'user-agent = "{ua}"',
                  f'output = "/Users/triton/PROTEUS/sandbox/p0361/curl-{ua_name}-{end_name}.txt"',
                  'write-out = "%{url_effective} %{http_code}\\n"']
(HERE / "curl.cfg").write_text("\n".join(lines) + "\n")
