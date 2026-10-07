"""Keyless: neurotrader888's main repos (MIT) -> sandbox/yt_ideas/transcripts/D-systematic-pros/github/.
YouTube blocked transcripts on 7 Oct, so the fourth reader gets his code instead of his videos."""
import json, os, time, urllib.request

OUT = "/Users/triton/PROTEUS/sandbox/yt_ideas/transcripts/D-systematic-pros/github"
REPOS = ["mcpt", "TechnicalAnalysisAutomation", "TrendLineAutomation", "TrendlineBreakoutMetaLabel",
         "market-structure", "VolatilityHawkes", "RSI-PCA", "IntramarketDifference", "TimeSeriesVisibilityGraphs",
         "PermutationEntropy"]
UA = {"User-Agent": "proteus-reader/0.1", "Accept": "application/vnd.github+json"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()


os.makedirs(OUT, exist_ok=True)
for repo in REPOS:
    try:
        items = json.loads(get("https://api.github.com/repos/neurotrader888/%s/contents" % repo))
    except Exception as e:
        print("ERR", repo, e)
        continue
    n = 0
    with open(os.path.join(OUT, repo + ".txt"), "w") as fh:
        fh.write("# neurotrader888/%s (MIT) https://github.com/neurotrader888/%s\n\n" % (repo, repo))
        for it in items:
            if it["type"] == "file" and (it["name"].endswith(".py") or it["name"].lower().startswith("readme")) and it["size"] < 60000:
                fh.write("\n\n===== %s =====\n" % it["name"])
                fh.write(get(it["download_url"]).decode("utf-8", "replace"))
                n += 1
                time.sleep(0.3)
    print(repo, n, "files")
