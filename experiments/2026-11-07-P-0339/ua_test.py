"""P-0339 side test: is the 429 about Python's client, or about this IP? One title, three clients."""
import json
import urllib.error
import urllib.request

URL = ("https://en.wikipedia.org/w/api.php?action=query&prop=pageviews&titles=Philosophy&pvipdays=5"
       "&format=json&formatversion=2")
for name, headers in [
    ("python, lab UA", {"User-Agent": "ProteusLab-pageviews-check/1.1"}),
    ("python, curl UA", {"User-Agent": "curl/8.7.1", "Accept": "*/*"}),
    ("python, lab UA + Accept", {"User-Agent": "ProteusLab-pageviews-check/1.1", "Accept": "*/*"}),
]:
    try:
        r = urllib.request.urlopen(urllib.request.Request(URL, headers=headers), timeout=30)
        print(name, r.status, len(json.load(r)["query"]["pages"]))
    except urllib.error.HTTPError as e:
        print(name, e.code, e.read()[:200])
