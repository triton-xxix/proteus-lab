"""P-0576: liveness of awesome-mcp-servers additions since 17 Nov.
Diffs the 17 Nov links file against tonight's, takes up to 40 new owner/repo names (sorted, first 40),
asks api.github.com/repos/NAME (keyless, 60 an hour) and fetches each non-empty homepage once."""
import json, sys, time, urllib.request, urllib.error, socket, datetime as dt

D = "/Users/triton/PROTEUS/state/harvest/awesome/"
OUT = sys.argv[1]
old = set(open(D + "awesome-mcp-servers.links.2026-11-17.prev").read().split())
new = set(open(D + "awesome-mcp-servers.links").read().split())
added = sorted(new - old)
removed = sorted(old - new)
sample = added[:40]


def get(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": "proteus-liveness/1.0"})
    try:
        r = urllib.request.urlopen(req, timeout=15)
        return r.status, r.geturl(), r.read() if method == "GET" else b""
    except urllib.error.HTTPError as e:
        return e.code, url, b""
    except Exception as e:
        return "error:" + type(e).__name__ + ":" + str(getattr(e, "reason", e))[:80], url, b""


rows = []
for name in sample:
    st, final, body = get("https://api.github.com/repos/" + name)
    row = {"repo": name, "api": st}
    if st == 200:
        j = json.loads(body)
        row.update(full_name=j["full_name"], renamed=j["full_name"].lower() != name.lower(), archived=j["archived"],
                   created=j["created_at"], pushed=j["pushed_at"], stars=j["stargazers_count"],
                   homepage=(j.get("homepage") or "").strip())
        if row["homepage"]:
            hp = row["homepage"] if row["homepage"].startswith("http") else "https://" + row["homepage"]
            hs, hfinal, _ = get(hp)
            row.update(homepage_status=hs, homepage_final=hfinal)
    rows.append(row)
    print(row)
    time.sleep(0.5)

summ = {"pulled_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "old": len(old), "new": len(new), "added": len(added), "removed": len(removed), "sampled": len(sample),
        "api_200": sum(r["api"] == 200 for r in rows), "api_404": sum(r["api"] == 404 for r in rows),
        "api_other": [r["api"] for r in rows if r["api"] not in (200, 404)],
        "renamed": sum(r.get("renamed", False) for r in rows), "archived": sum(r.get("archived", False) for r in rows),
        "with_homepage": sum(bool(r.get("homepage")) for r in rows),
        "homepage_200": sum(r.get("homepage_status") == 200 for r in rows),
        "homepage_bad": [(r["repo"], r["homepage"], r["homepage_status"]) for r in rows
                         if r.get("homepage") and r.get("homepage_status") != 200],
        "created_after_2026_11_10": sum(r.get("created", "") >= "2026-11-10" for r in rows)}
print(json.dumps(summ, indent=1))
json.dump({"summary": summ, "rows": rows, "removed": removed}, open(OUT + "/results.json", "w"), indent=1)
