"""Merge the reading children's JSON into one ranked list (stdout as markdown table rows + JSON).

    python3 /Users/triton/PROTEUS/sandbox/yt_ideas/merge.py
"""
import glob, json, os

DIR = "/Users/triton/PROTEUS/state/agents/2026-10-07"
ideas, frameworks, bad = [], [], []
for p in sorted(glob.glob(os.path.join(DIR, "yt-ideas-*.json"))):
    try:
        d = json.load(open(p))
    except Exception as e:
        bad.append((os.path.basename(p), str(e)[:80]))
        continue
    for i in d.get("ideas", []):
        i["_group"] = d.get("group", os.path.basename(p))
        ideas.append(i)
    for f in d.get("frameworks", []):
        f["_group"] = d.get("group", os.path.basename(p))
        frameworks.append(f)

def key(i):
    return (int(i.get("priority") or 9), not i.get("testable_free_daily"), not i.get("rules_complete"))

ideas.sort(key=key)
print("ideas", len(ideas), "frameworks", len(frameworks), "bad", bad)
for i in ideas:
    print("| %s | P%s | %s | %s | %s | %s | %s |" % (
        i.get("id"), i.get("priority"), (i.get("name") or "")[:50], i.get("kind"), i.get("timeframe"),
        "daily-ok" if i.get("testable_free_daily") else "needs-data",
        "complete" if i.get("rules_complete") else "incomplete"))
json.dump({"ideas": ideas, "frameworks": frameworks}, open(os.path.join(DIR, "yt-ideas-merged.json"), "w"), indent=1)
