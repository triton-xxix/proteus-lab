#!/usr/bin/env python3
"""P-0009: TfL unified API with no app key. Pull one line's live arrivals and the tube status, then
burst-call until it throttles and read the headers. Output: REPORT.md."""
import json, time, urllib.request, urllib.error
B = "https://api.tfl.gov.uk"
def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe/0.1", "Accept": "application/json"})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=20) as r: return r.status, dict(r.headers), json.load(r), time.time() - t
    except urllib.error.HTTPError as e: return e.code, dict(e.headers), None, time.time() - t
L = ["# P-0009: TfL unified API, no key", ""]
st, hd, d, dt = get(B + "/Line/victoria/Arrivals")
L.append("`/Line/victoria/Arrivals`: HTTP %d in %.2fs, %s predictions." % (st, dt, len(d) if d else 0))
if d:
    d.sort(key=lambda a: a.get("timeToStation", 0))
    L += ["", "| station | platform | towards | seconds |", "|---|---|---|---|"]
    for a in d[:8]: L.append("| %s | %s | %s | %s |" % (a.get("stationName"), a.get("platformName"), a.get("towards"), a.get("timeToStation")))
    L.append("")
st, hd, d, dt = get(B + "/Line/Mode/tube/Status")
L.append("`/Line/Mode/tube/Status`: HTTP %d in %.2fs. %s" % (st, dt, "; ".join("%s: %s" % (l["name"], l["lineStatuses"][0]["statusSeverityDescription"]) for l in (d or [])[:11])))
L.append("Rate headers on a normal reply: %s" % ({k: v for k, v in hd.items() if "rate" in k.lower() or "limit" in k.lower()} or "none"))
codes, times, t0, hit = [], [], time.time(), None
for i in range(120):
    st, hd, d, dt = get(B + "/Line/%s/Arrivals" % ["victoria", "central", "northern", "jubilee"][i % 4])
    codes.append(st); times.append(dt)
    if st == 429:
        hit = (i + 1, time.time() - t0, {k: v for k, v in hd.items() if "retry" in k.lower() or "rate" in k.lower()}); break
L += ["", "Burst: %d calls in %.1fs, codes %s, mean %.2fs, max %.2fs." % (len(codes), time.time() - t0, sorted(set(codes)), sum(times) / len(times), max(times))]
L.append("Throttled at call %d after %.1fs, headers %s." % hit if hit else "No 429 in %d calls." % len(codes))
open("/Users/triton/PROTEUS/experiments/2026-09-24-P-0009/REPORT.md", "w").write("\n".join(L) + "\n")
print("\n".join(L))
