"""P-0429: read the saved NOAA page for the 2019 panel's figures. Prints every sentence that
mentions a sunspot number, a peak date or a range, so the quote can be checked by eye."""
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
h = open(os.path.join(HERE, "panel-2019.html"), errors="replace").read()
t = re.search(r"(?s)<title>(.*?)</title>", h)
print("title:", html.unescape(t.group(1)).strip() if t else None)
h = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", h)
txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h)))
open(os.path.join(HERE, "panel-2019.txt"), "w").write(txt)
for s in re.split(r"(?<=[.!?]) ", txt):
    if re.search(r"\b(115|peak|maximum|minimum|sunspot number|months)\b", s, re.I) and re.search(r"\d", s) and len(s) < 600:
        print("-", s.strip())
