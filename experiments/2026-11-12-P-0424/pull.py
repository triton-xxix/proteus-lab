"""Refill row 157: pull two arXiv papers' abstract and HTML pages, keep the text, list the tables
and every sentence that mentions Brier, the market or accuracy with a number. Read only on the web.

Usage: python3 pull.py   (writes <id>.abs.txt, <id>.html.txt, tables.json beside itself)
"""
import html
import json
import os
import re
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
IDS = ["2609.28876", "2607.18269"]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research reader)"})
    try:
        return urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace"), None
    except Exception as e:  # a refusal is a result
        return "", "%s: %s" % (type(e).__name__, e)


def text_of(h):
    h = re.sub(r"(?s)<(script|style|math)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?s)<annotation[^>]*>.*?</annotation>", " ", h)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h)))


out = {}
for i in IDS:
    row = {}
    a, err = get("https://arxiv.org/abs/" + i)
    row["abs_error"] = err
    m = re.search(r'(?s)<blockquote class="abstract[^>]*>(.*?)</blockquote>', a)
    row["abstract"] = text_of(m.group(1)).strip() if m else ""
    t = re.search(r"(?s)<title>(.*?)</title>", a)
    row["title"] = text_of(t.group(1)).strip() if t else ""
    open(os.path.join(HERE, i + ".abs.txt"), "w").write(row["title"] + "\n\n" + row["abstract"] + "\n")
    h, err = get("https://arxiv.org/html/" + i)
    row["html_error"], row["html_chars"] = err, len(h)
    tables = []
    for tm in re.finditer(r"(?s)<table.*?</table>", h):
        rows = []
        for tr in re.finditer(r"(?s)<tr.*?</tr>", tm.group(0)):
            cells = [text_of(c).strip() for c in re.findall(r"(?s)<t[dh][^>]*>(.*?)</t[dh]>", tr.group(0))]
            if any(cells):
                rows.append(cells)
        if rows:
            tables.append(rows)
    caps = [text_of(c).strip()[:300] for c in re.findall(r"(?s)<figcaption.*?</figcaption>", h)]
    body = text_of(h)
    open(os.path.join(HERE, i + ".html.txt"), "w").write(body)
    sents = [s.strip() for s in re.split(r"(?<=[.!?]) ", body)
             if re.search(r"Brier|market|accura|baseline", s, re.I) and re.search(r"\d\.\d", s) and len(s) < 500]
    row["tables"], row["captions"], row["sentences"] = tables, caps, sents[:60]
    out[i] = row
    print("==", i, row["title"][:90], "| abs", bool(row["abstract"]), "| html chars", len(h), "err", err,
          "| tables", len(tables), "| captions", len(caps), "| sentences", len(sents))
json.dump(out, open(os.path.join(HERE, "tables.json"), "w"), indent=1)
