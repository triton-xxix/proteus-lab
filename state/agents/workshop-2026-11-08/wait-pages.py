"""Polls the live channel digest page until it answers with the built size, up to 6 minutes."""
import os
import time
import urllib.request

URL = "https://triton-xxix.github.io/proteus-lab/tools/channel-digest/"
want = os.path.getsize("/Users/triton/PROTEUS/docs/tools/channel-digest/index.html")
for i in range(36):
    req = urllib.request.Request(URL + "?v=%d" % i, headers={"User-Agent": "proteus-workshop-check"})
    with urllib.request.urlopen(req, timeout=20) as r:
        n = len(r.read())
    print(i, r.status, n, "want", want, flush=True)
    if n == want:
        break
    time.sleep(10)
