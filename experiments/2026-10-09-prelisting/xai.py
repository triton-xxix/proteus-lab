"""xAI X-search helper for the pre-listing work. Luke approved up to $10 on his xAI key for this piece
of work (9 Oct 2026). Every call is appended to xai-calls.jsonl with the API's own cost; a call is
refused once the file's total reaches CAP_USD, so the cap holds across scripts and re-runs.

Post timestamps come from the status id in each cited URL (X ids are snowflakes: ms since
2010-11-04 01:42:54.657 UTC in the top bits), not from the model's prose.
"""
import importlib.util
import json
import os
import re
import time
from datetime import datetime, timezone

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "xai-calls.jsonl")
CAP_USD = 10.0
MODEL = "grok-4.20-0309-non-reasoning"
TWEPOCH = 1288834974657


def spent():
    if not os.path.exists(LOG):
        return 0.0
    return sum(json.loads(l).get("cost_usd") or 0 for l in open(LOG) if l.strip())


def _key():
    spec = importlib.util.spec_from_file_location("proteus_secrets", "/Users/triton/PROTEUS/bin/secrets.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.get("XAI API Credentials", vault="Tritons World")


def status_time(url):
    m = re.search(r"/status/(\d{15,20})", url or "")
    if not m:
        return None
    return ((int(m.group(1)) >> 22) + TWEPOCH) / 1000


def search(tag, prompt, from_date, to_date, handles=None):
    """One call. Returns (text, cited urls, cost). Raises if the cap is reached."""
    if spent() >= CAP_USD - 0.3:
        raise RuntimeError("xAI cap reached: %.2f of %.2f" % (spent(), CAP_USD))
    tool = {"type": "x_search", "from_date": from_date, "to_date": to_date}
    if handles:
        tool["allowed_x_handles"] = handles
    body = {"model": MODEL, "input": [{"role": "user", "content": prompt}], "tools": [tool]}
    t0 = time.time()
    r = requests.post("https://api.x.ai/v1/responses", json=body, timeout=300,
                      headers={"Authorization": "Bearer " + _key(), "Content-Type": "application/json"})
    d = r.json()
    usage = d.get("usage") or {}
    cost = round((usage.get("cost_in_usd_ticks") or 0) / 1e10, 4)
    text, urls = "", []
    for o in d.get("output", []):
        if o.get("type") == "message":
            for c in o.get("content", []):
                if c.get("type") == "output_text":
                    text = c.get("text") or text
                    for a in c.get("annotations") or []:
                        if a.get("url"):
                            urls.append(a["url"])
    urls += [u for u in d.get("citations") or [] if isinstance(u, str)]
    urls += re.findall(r"https://(?:x|twitter)\.com/\S+?/status/\d+", text)
    urls = sorted(set(u.rstrip(").,]") for u in urls))
    with open(LOG, "a") as fh:
        fh.write(json.dumps({"at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "tag": tag,
                             "from": from_date, "to": to_date, "cost_usd": cost, "secs": round(time.time() - t0),
                             "status": r.status_code, "urls": len(urls), "error": d.get("error") if r.status_code != 200 else None}) + "\n")
    return text, urls, cost
