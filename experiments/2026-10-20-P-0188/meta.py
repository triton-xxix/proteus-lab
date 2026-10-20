"""List the DVSA anonymised MOT dataset's resources (name, url, size) from data.gov.uk."""
import json, re, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Macintosh) proteus-probe"}
OUT = "/Users/triton/PROTEUS/experiments/2026-10-20-P-0188/"

import sys
for url in sys.argv[1:] or [
    "https://data.gov.uk/api/action/package_show?id=e3939ef8-30c7-4ca8-9c7c-ad9475fc9f8b",
    "https://www.data.gov.uk/dataset/e3939ef8-30c7-4ca8-9c7c-ad9475fc9f8b/anonymised-mot-tests-and-results",
]:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
            body = r.read().decode("utf-8", "replace")
        print("OK", url, len(body))
        if "api/action" in url:
            d = json.loads(body)["result"]
            for res in d["resources"]:
                print(res.get("name"), res.get("url"), res.get("size"))
        else:
            for link in sorted(set(re.findall(r'href="(https?://[^"]+\.(?:zip|csv|gz|7z)[^"]*)"', body))):
                print(link)
        break
    except Exception as e:
        print("FAIL", url, type(e).__name__, str(e)[:200])
