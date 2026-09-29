#!/usr/bin/env python3
"""P-0034: Metaculus with the vault token (reopens P-0007). Find the Metaculus item in the Proteus
vault through the service account, then list open binary questions with community forecasts,
measure the throttle, and look for sports questions. Never prints the token. Output: REPORT.md."""
import json, sys, time, urllib.request, urllib.error
sys.path.insert(0, "/Users/triton/PROTEUS/bin")
import secrets as vault

OUT = "/Users/triton/PROTEUS/experiments/2026-09-29-P-0034/"
BASE = "https://www.metaculus.com/api"
L = ["# P-0034: Metaculus API with the vault token", ""]

def done():
    open(OUT + "REPORT.md", "w").write("\n".join(L) + "\n")
    print("\n".join(L))
    sys.exit(0)

t = time.time()
try:
    items = json.loads(vault._op(["item", "list", "--vault", vault.VAULT, "--format", "json"], timeout=90))
    names = [i.get("title", "") for i in items]
    L.append("Vault listing: %d items in %.1fs." % (len(names), time.time() - t))
except vault.SecretError as e:
    L.append("Vault listing failed after %.1fs: %s" % (time.time() - t, e))
    done()
hits = [n for n in names if "metaculus" in n.lower()]
L.append("Items matching 'metaculus': %s" % (hits or "none"))
if not hits:
    L.append("All titles (no values): %s" % ", ".join(sorted(names)))
    done()
token = None
for field in ("credential", "token", "password", "api_token"):
    try:
        token = vault._op(["read", "op://%s/%s/%s" % (vault.VAULT, hits[0], field)], timeout=60).strip()
        L.append("Token read from field '%s', length %d." % (field, len(token)))
        break
    except vault.SecretError as e:
        L.append("Field '%s': %s" % (field, str(e)[:120]))
if not token:
    done()

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe/0.2", "Accept": "application/json",
                                               "Authorization": "Token " + token})
    t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, dict(r.headers), json.load(r), time.time() - t
    except urllib.error.HTTPError as e:
        body = e.read()[:200].decode("utf-8", "replace")
        return e.code, dict(e.headers), {"_error": body}, time.time() - t

def cp_of(q):
    agg = ((q.get("aggregations") or {}).get("recency_weighted") or {}).get("latest") or {}
    c = agg.get("centers") or agg.get("means")
    return (c[0] if c else None), agg.get("forecaster_count")

st, hd, d, dt = get(BASE + "/posts/?statuses=open&forecast_type=binary&limit=100&order_by=-hotness")
rate = {k: v for k, v in hd.items() if "rate" in k.lower() or "limit" in k.lower()}
L.append("")
L.append("`/api/posts/` open binary, 100 by hotness: HTTP %d in %.2fs. Rate headers: %s" % (st, dt, rate or "none"))
if st != 200:
    L.append("Body: %s" % (d or {}).get("_error", ""))
    done()
posts = d.get("results", [])
L.append("Returned %d posts; total count reported %s." % (len(posts), d.get("count")))
rows = []
for p in posts:
    q = p.get("question") or {}
    cp, n = cp_of(q)
    rows.append((p.get("id"), (p.get("title") or "").replace("|", "/")[:80], (q.get("scheduled_close_time") or "")[:10], cp, n))
have = [r for r in rows if r[3] is not None]
L.append("Community forecast present on %d of %d." % (len(have), len(rows)))
L += ["", "Top 15 by hotness:", "", "| id | title | closes | community p | forecasters |", "|---|---|---|---|---|"]
for r in rows[:15]:
    L.append("| %s | %s | %s | %s | %s |" % r)

# sports: search endpoint and keyword filter
SPORT = ("football", "premier league", "champions league", "world cup", "uefa", "fifa", "soccer",
         "arsenal", "liverpool", "manchester", "chelsea", "tottenham", "nations league", "euro 20")
sport_rows = [r for r in rows if any(k in r[1].lower() for k in SPORT)]
st2, _, d2, dt2 = get(BASE + "/posts/?statuses=open&forecast_type=binary&limit=100&search=football")
extra = []
if st2 == 200:
    for p in d2.get("results", []):
        q = p.get("question") or {}
        cp, n = cp_of(q)
        extra.append((p.get("id"), (p.get("title") or "").replace("|", "/")[:80], (q.get("scheduled_close_time") or "")[:10], cp, n))
L += ["", "Search 'football' (open binary): HTTP %d in %.2fs, %d results. Keyword hits in the hotness 100: %d." % (st2, dt2, len(extra), len(sport_rows))]
seen = set()
L += ["", "| id | title | closes | community p | forecasters |", "|---|---|---|---|---|"]
for r in sport_rows + extra:
    if r[0] in seen: continue
    seen.add(r[0]); L.append("| %s | %s | %s | %s | %s |" % r)

# history on the first post
if posts:
    st3, _, d3, dt3 = get(BASE + "/posts/%s/" % posts[0]["id"])
    q = (d3 or {}).get("question") or {}
    hist = ((q.get("aggregations") or {}).get("recency_weighted") or {}).get("history") or []
    L += ["", "Single post detail: HTTP %d in %.2fs, recency-weighted history points: %d." % (st3, dt3, len(hist))]

# burst: 30 calls, stop at the first 429
codes, times, t0 = [], [], time.time()
for i in range(30):
    s, h, _, x = get(BASE + "/posts/?statuses=open&limit=5&offset=%d" % (i * 5))
    codes.append(s); times.append(x)
    if s == 429:
        L.append("429 at call %d after %.1fs; headers %s" % (i + 1, time.time() - t0, {k: v for k, v in h.items() if "retry" in k.lower() or "rate" in k.lower()}))
        break
L += ["", "Burst: %d calls in %.1fs, codes %s, mean %.2fs per call." % (len(codes), time.time() - t0, sorted(set(codes)), sum(times) / len(times))]
json.dump({"rows": rows, "sport": sport_rows + extra, "burst_codes": codes}, open(OUT + "pull.json", "w"))
done()
