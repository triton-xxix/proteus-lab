"""P-0585: what happened to the 6 repos dropped from awesome-mcp-servers 17 to 26 Nov (P-0576)? Keyless GitHub API."""
import json
import urllib.error
import urllib.request

SRC = "/Users/triton/PROTEUS/experiments/2026-11-26-P-0576/results.json"
HERE = "/Users/triton/PROTEUS/experiments/2026-11-27-P-0585/"
names = json.load(open(SRC))["removed"]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "proteus-probe", "Accept": "application/vnd.github+json"})
    try:
        r = urllib.request.urlopen(req, timeout=30)
        return r.status, r.geturl(), json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, url, None


out = []
for n in names:
    code, final, j = get("https://api.github.com/repos/" + n)
    row = {"listed": n, "status": code}
    if j:
        row.update(full_name=j["full_name"], renamed=j["full_name"].lower() != n.lower(), archived=j["archived"],
                   created=j["created_at"], pushed=j["pushed_at"], stars=j["stargazers_count"], fork=j["fork"],
                   private=j.get("private"))
        c, _, cj = get("https://api.github.com/repos/%s/commits?per_page=1" % j["full_name"])
        row["last_commit"] = cj[0]["commit"]["committer"]["date"] if cj else None
    out.append(row)
    print(row)

def cls(r):
    if r["status"] == 404:
        return "deleted or private"
    if r.get("renamed"):
        return "renamed"
    if r.get("archived"):
        return "archived"
    return "live"

tally = {}
for r in out:
    r["class"] = cls(r)
    tally[r["class"]] = tally.get(r["class"], 0) + 1
live_recent = sum(1 for r in out if r["class"] == "live" and (r.get("last_commit") or "") >= "2026-11-17")
json.dump({"tally": tally, "live_with_commit_after_17_nov": live_recent, "rows": out}, open(HERE + "results.json", "w"), indent=1)
print(tally, "live with a commit after 17 Nov:", live_recent)
