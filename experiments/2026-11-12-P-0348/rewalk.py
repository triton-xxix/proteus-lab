"""P-0348: the 5 Nov first-link walk, one week on.

Same 100 starts (experiments/2026-11-05-philosophy/walks.json), same rule and parser
(experiments/2026-11-05-P-0332/walk_rule.py, imported unchanged), today's revisions. Counts how many
starts change outcome class, end page or path, and names the page where each changed path first
departs from the old one. Fetch errors are retried and reported, never counted as dead ends silently.
"""
import importlib.util
import json
import time
from collections import Counter

ROOT = "/Users/triton/PROTEUS"
OLD = ROOT + "/experiments/2026-11-05-philosophy/walks.json"
OUT = ROOT + "/experiments/2026-11-12-P-0348/results.json"
spec = importlib.util.spec_from_file_location("wr", ROOT + "/experiments/2026-11-05-P-0332/walk_rule.py")
wr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wr)


def careful(title):
    """resolve_and_first, with fetch errors retried twice (429s were the fault on 6 Nov)."""
    for attempt in range(3):
        res = wr.resolve_and_first(title)
        if res[2] is None or "404" in res[2]:
            return res
        wr.CACHE.pop(title, None)
        time.sleep(2 + 3 * attempt)
    return wr.resolve_and_first(title)


def walk(start):
    path, seen, errs, t = [], set(), [], start
    for _ in range(60):
        canon, nxt, err = careful(t)
        path.append(canon)
        if err:
            errs.append([canon, err])
        if canon == "Philosophy":
            return "philosophy", path, errs
        if canon in seen:
            return "loop", path, errs
        seen.add(canon)
        if err or not nxt:
            return "dead end", path, errs
        t = nxt
    return "too long", path, errs


def main():
    old = json.load(open(OLD))
    rows = []
    for o in old["rows"]:
        outcome, path, errs = walk(o["start"])
        diverge = None
        if path != o["path"]:
            for i, (a, b) in enumerate(zip(o["path"], path)):
                if a != b:
                    diverge = {"after": o["path"][i - 1] if i else None, "was": a, "now": b}
                    break
            else:
                k = min(len(path), len(o["path"]))
                diverge = {"after": path[k - 1], "was": o["path"][k] if len(o["path"]) > k else None,
                           "now": path[k] if len(path) > k else None}
        rows.append({"start": o["start"], "old_outcome": o["outcome"], "outcome": outcome,
                     "old_end": o["path"][-1], "end": path[-1], "old_hops": o["hops"],
                     "hops": len(path) - 1, "same_path": path == o["path"], "diverge": diverge,
                     "errors": errs, "path": path})
        print("%-10s -> %-10s %s%s" % (o["outcome"], outcome, o["start"],
                                       "" if path == o["path"] else "   CHANGED at %s" % diverge), flush=True)
    n = len(rows)
    non_404 = [r for r in rows if any("404" not in e[1] for e in r["errors"])]
    summary = {
        "old_at": old["at"], "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n": n,
        "old_outcomes": dict(Counter(r["old_outcome"] for r in rows)),
        "outcomes": dict(Counter(r["outcome"] for r in rows)),
        "outcome_class_changed": sum(r["old_outcome"] != r["outcome"] for r in rows),
        "end_page_changed": sum(r["old_end"] != r["end"] for r in rows),
        "path_changed": sum(not r["same_path"] for r in rows),
        "transitions": dict(Counter("%s -> %s" % (r["old_outcome"], r["outcome"]) for r in rows
                                    if r["old_outcome"] != r["outcome"])),
        "edits_behind_changes": dict(Counter(
            "%s: %s -> %s" % (r["diverge"]["after"], r["diverge"]["was"], r["diverge"]["now"])
            for r in rows if r["diverge"])),
        "rows_with_fetch_errors_not_404": len(non_404),
        "pages_fetched": len(wr.CACHE),
    }
    print(json.dumps(summary, indent=1))
    json.dump({"summary": summary, "rows": rows}, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    main()
