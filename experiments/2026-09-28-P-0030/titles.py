"""P-0030: print the scrimba explain page title for each story id given, with fetch time.
'Explain anything' means no explainer exists yet; anything else means one is generated."""
import re
import sys
import time
import urllib.request
from urllib.parse import urlencode

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36 proteus-p0030"
for sid in sys.argv[1:]:
    hn = "https://news.ycombinator.com/item?id=" + sid
    url = "https://scrimba.com/explain?" + urlencode({"link": hn, "embed": "1,fullwindow", "play": "1", "via": "hn_watch"})
    t = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    text = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
    title = (re.search(r"<title>(.*?)</title>", text, re.S) or [None, ""])[1]
    print(time.strftime("%H:%M:%S"), sid, round(time.time() - t, 2), "s", len(text), "bytes", title[:80])
