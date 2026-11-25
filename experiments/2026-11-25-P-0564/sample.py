"""P-0564: repeated public GETs of NEOMA P-CAM's telemetry. Keyless, documented as public.
12 rounds, 20 s apart (about 4 minutes), each round GETs the telemetry, the docs page and the bio docs.
If telemetry ever returns JSON, measured_us is collected and its spread reported.
"""
import json, os, statistics, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
URLS = {"telemetry": "https://api.neoma-pcam.com/v1/telemetry",
        "api_docs": "https://api.neoma-pcam.com/docs",
        "bio_docs": "https://bio.neoma-pcam.com/bio/docs",
        "pages": "https://neoma-pcam.github.io/pcam-live/"}
rows, measured = [], []
for rnd in range(12):
    for name, url in URLS.items():
        if name == "pages" and rnd > 0:
            continue
        t0 = time.time()
        rec = {"round": rnd, "name": name, "at": time.strftime("%H:%M:%S", time.gmtime())}
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe/1"})
            with urllib.request.urlopen(req, timeout=20) as r:
                body = r.read(200000)
                rec["status"] = r.status
                rec["bytes"] = len(body)
                if name == "telemetry":
                    try:
                        j = json.loads(body)
                        rec["json_keys"] = sorted(j.keys())[:30] if isinstance(j, dict) else type(j).__name__
                        def find(o):
                            if isinstance(o, dict):
                                for k, v in o.items():
                                    if k == "measured_us" and isinstance(v, (int, float)):
                                        measured.append(v)
                                    else:
                                        find(v)
                            elif isinstance(o, list):
                                for x in o:
                                    find(x)
                        find(j)
                        rec["sample"] = body[:400].decode("utf-8", "replace")
                    except Exception as e:
                        rec["parse_error"] = str(e)[:100]
        except urllib.error.HTTPError as e:
            rec["status"] = e.code
            rec["body"] = e.read(200).decode("utf-8", "replace")
        except Exception as e:
            rec["error"] = str(e)[:120]
        rec["secs"] = round(time.time() - t0, 3)
        rows.append(rec)
        print(json.dumps(rec)[:300])
    if rnd < 11:
        time.sleep(20)
out = {"rows": rows, "measured_us": measured}
if measured:
    out["measured_summary"] = {"n": len(measured), "distinct": len(set(measured)), "min": min(measured), "max": max(measured),
                               "median": statistics.median(measured)}
by = {}
for r in rows:
    by.setdefault(r["name"], {}).setdefault(str(r.get("status", r.get("error", "?"))), 0)
    by[r["name"]][str(r.get("status", r.get("error", "?")))] += 1
out["status_counts"] = by
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print("STATUS", json.dumps(by))
print("MEASURED", json.dumps(out.get("measured_summary")))
