"""P-0371: P-0351 and P-0362's counter on the same 30 repos, counting both cl100k_base and o200k_base.

Same file filters as the two earlier probes (each language keeps its own skip list: the
Python/JS/Go list from P-0351, the Rust/Java list from P-0362). Repos are HEAD tonight, not
the commits those probes saw, so the cl100k column is re-measured here and the comparison is
made inside this run.
Usage: sandbox/py312-venv/bin/python count.py OUT.json
"""
import io
import json
import os
import statistics
import sys
import tarfile
import time
import urllib.request

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/neurocode-deps")
os.environ["TIKTOKEN_CACHE_DIR"] = "/Users/triton/PROTEUS/sandbox/neurocode-deps/.tiktoken-cache"
os.makedirs(os.environ["TIKTOKEN_CACHE_DIR"], exist_ok=True)
import tiktoken  # noqa: E402

CL = tiktoken.get_encoding("cl100k_base")
O2 = tiktoken.get_encoding("o200k_base")
print("vocab", CL.n_vocab, O2.n_vocab, flush=True)

REPOS = {
    "Python": ["psf/requests", "pallets/flask", "fastapi/fastapi", "encode/httpx", "psf/black", "Textualize/rich"],
    "JS/TS": ["expressjs/express", "axios/axios", "lodash/lodash", "vuejs/core", "chalk/chalk", "sindresorhus/got"],
    "Go": ["gin-gonic/gin", "spf13/cobra", "gorilla/mux", "sirupsen/logrus", "junegunn/fzf", "prometheus/client_golang"],
    "Rust": ["BurntSushi/ripgrep", "sharkdp/bat", "sharkdp/fd", "serde-rs/serde", "tokio-rs/axum", "clap-rs/clap"],
    "Java": ["google/gson", "junit-team/junit4", "apache/commons-lang", "square/javapoet", "google/guice", "jhy/jsoup"],
}
EXT = {"Python": (".py",), "JS/TS": (".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx"), "Go": (".go",),
       "Rust": (".rs",), "Java": (".java",)}
SKIP_A = ("/node_modules/", "/dist/", "/build/", "/vendor/", ".min.js", ".d.ts")
SKIP_B = ("/node_modules/", "/dist/", "/build/", "/vendor/", "/target/")
SKIP = {"Python": SKIP_A, "JS/TS": SKIP_A, "Go": SKIP_A, "Rust": SKIP_B, "Java": SKIP_B}

out = sys.argv[1]
res = {"repos": [], "errors": []}
for lang, repos in REPOS.items():
    for repo in repos:
        url = "https://codeload.github.com/%s/tar.gz/HEAD" % repo
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "ProteusLab/1.0"}),
                                         timeout=120).read()
        except Exception as e:  # noqa: BLE001
            res["errors"].append({"repo": repo, "error": repr(e)})
            continue
        files = cl = o2 = words = chars = 0
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
            for m in tf.getmembers():
                if not m.isfile() or not m.name.endswith(EXT[lang]) or m.size > 512_000:
                    continue
                if any(s in "/" + m.name for s in SKIP[lang]):
                    continue
                text = tf.extractfile(m).read().decode("utf-8", "replace")
                w = len(text.split())
                if not w:
                    continue
                files += 1
                cl += len(CL.encode(text, disallowed_special=()))
                o2 += len(O2.encode(text, disallowed_special=()))
                words += w
                chars += len(text)
        if not words:
            res["errors"].append({"repo": repo, "error": "no files counted"})
            continue
        row = {"lang": lang, "repo": repo, "files": files, "words": words, "chars": chars, "cl100k": cl, "o200k": o2,
               "cl_per_word": round(cl / words, 3), "o2_per_word": round(o2 / words, 3),
               "o2_over_cl": round(o2 / cl, 4), "chars4_over_o2": round(chars / 4 / o2, 3)}
        res["repos"].append(row)
        print(json.dumps(row), flush=True)
        time.sleep(1)

rows = res["repos"]
res["repos_counted"] = len(rows)
res["median_o2_over_cl"] = round(statistics.median(r["o2_over_cl"] for r in rows), 4)
res["min_o2_over_cl"] = min(r["o2_over_cl"] for r in rows)
res["max_o2_over_cl"] = max(r["o2_over_cl"] for r in rows)
res["median_cl_per_word"] = round(statistics.median(r["cl_per_word"] for r in rows), 3)
res["median_o2_per_word"] = round(statistics.median(r["o2_per_word"] for r in rows), 3)
res["repos_within_15pct_of_2.51_o200k"] = sum(abs(2.51 * r["words"] / r["o200k"] - 1) <= 0.15 for r in rows)
res["repos_within_15pct_of_2.51_cl100k"] = sum(abs(2.51 * r["words"] / r["cl100k"] - 1) <= 0.15 for r in rows)
res["chars4_share_of_o200k_median"] = round(statistics.median(r["chars4_over_o2"] for r in rows), 3)
res["by_lang"] = {}
for lang in REPOS:
    rs = [r for r in rows if r["lang"] == lang]
    if rs:
        res["by_lang"][lang] = {
            "repos": len(rs),
            "cl_per_word_median": round(statistics.median(r["cl_per_word"] for r in rs), 3),
            "o2_per_word_median": round(statistics.median(r["o2_per_word"] for r in rs), 3),
            "o2_over_cl_pooled": round(sum(r["o200k"] for r in rs) / sum(r["cl100k"] for r in rs), 4),
        }
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "repos"}, indent=1))
