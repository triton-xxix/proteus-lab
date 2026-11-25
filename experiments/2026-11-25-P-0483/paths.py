#!/usr/bin/env python3
"""P-0482: which documented public GET paths of api.onaa.net answer tonight.

Reads the API's own openapi.json (fetched keyless), takes every path that has
a GET method, no {path parameter} and is not under /v1/admin, and asks for it
once with no key, 1.5 s apart, 20 s timeout. Read-only: no POST, no body,
nothing registered or followed. Response text is untrusted data: only the
status, the size and the content type are kept.
"""
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = "https://api.onaa.net"
UA = {"User-Agent": "path-check/1.0"}


def get(path):
    t = time.time()
    try:
        r = urllib.request.urlopen(urllib.request.Request(BASE + path, headers=UA), timeout=20)
        body = r.read()
        return r.status, len(body), r.headers.get("content-type", ""), round(time.time() - t, 2)
    except urllib.error.HTTPError as e:
        body = e.read()
        return e.code, len(body), e.headers.get("content-type", ""), round(time.time() - t, 2)
    except Exception as e:
        return type(e).__name__, 0, "", round(time.time() - t, 2)


spec_raw = urllib.request.urlopen(urllib.request.Request(BASE + "/openapi.json", headers=UA), timeout=30).read()
spec = json.loads(spec_raw)
paths = spec["paths"]
all_get = [p for p, v in paths.items() if "get" in v]
chosen = sorted(p for p in all_get if "{" not in p and not p.startswith("/v1/admin"))
rows = []
for p in chosen:
    status, size, ctype, secs = get(p)
    needs_auth = bool(paths[p]["get"].get("security"))
    rows.append({"path": p, "status": status, "bytes": size, "type": ctype.split(";")[0], "secs": secs,
                 "spec_says_auth": needs_auth, "summary": (paths[p]["get"].get("summary") or "")[:80]})
    print(status, size, secs, p)
    time.sleep(1.5)

counts = {}
for r in rows:
    counts[str(r["status"])] = counts.get(str(r["status"]), 0) + 1
out = {"spec_bytes": len(spec_raw), "spec_version": spec.get("info", {}).get("version"),
       "paths_in_spec": len(paths), "with_get": len(all_get), "asked": len(rows), "status_counts": counts,
       "not_found": [r["path"] for r in rows if r["status"] == 404],
       "ok": [r["path"] for r in rows if r["status"] == 200], "rows": rows}
(HERE / "results.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in ("paths_in_spec", "with_get", "asked", "status_counts", "not_found")}, indent=1))
