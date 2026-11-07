"""P-0351: how far off is 'tokens = words x 1.3' for source code, by language?

Fetches a codeload tarball (keyless) per repo, counts every source file of the repo's language with tiktoken
cl100k_base, whitespace words and characters. Per repo: cl100k per word (the factor that would hold), and
how far words x 1.3 and chars / 4 land from cl100k. Skips vendored, built and minified files and any file
over 512 KB.
Usage: sandbox/py312-venv/bin/python count.py OUT.json
"""
import io
import json
import statistics
import sys
import tarfile
import time
import urllib.request

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/neurocode-deps")  # tiktoken, built for 3.12 (P-0342)
import tiktoken  # noqa: E402

ENC = tiktoken.get_encoding("cl100k_base")
REPOS = {
    "Python": ["psf/requests", "pallets/flask", "fastapi/fastapi", "encode/httpx", "psf/black", "Textualize/rich"],
    "JS/TS": ["expressjs/express", "axios/axios", "lodash/lodash", "vuejs/core", "chalk/chalk", "sindresorhus/got"],
    "Go": ["gin-gonic/gin", "spf13/cobra", "gorilla/mux", "sirupsen/logrus", "junegunn/fzf", "prometheus/client_golang"],
}
EXT = {"Python": (".py",), "JS/TS": (".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx"), "Go": (".go",)}
SKIP = ("/node_modules/", "/dist/", "/build/", "/vendor/", ".min.js", ".d.ts")
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
        files = toks = words = chars = 0
        per_file = []
        with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tf:
            for m in tf.getmembers():
                if not m.isfile() or not m.name.endswith(EXT[lang]) or m.size > 512_000:
                    continue
                if any(s in "/" + m.name for s in SKIP):
                    continue
                text = tf.extractfile(m).read().decode("utf-8", "replace")
                w = len(text.split())
                if not w:
                    continue
                t = len(ENC.encode(text, disallowed_special=()))
                files += 1
                toks += t
                words += w
                chars += len(text)
                per_file.append(t / w)
        row = {"lang": lang, "repo": repo, "tarball_bytes": len(raw), "files": files, "cl100k": toks,
               "words": words, "chars": chars, "tokens_per_word": round(toks / words, 3),
               "words_x1.3_over_cl100k": round(words * 1.3 / toks, 3),
               "chars_over_4_over_cl100k": round(chars / 4 / toks, 3),
               "file_ratio_p10_p90": [round(x, 2) for x in statistics.quantiles(per_file, n=10)[::8]] if len(per_file) > 9 else None}
        res["repos"].append(row)
        print(json.dumps(row))
        time.sleep(1)

rows = res["repos"]
f = statistics.median(r["tokens_per_word"] for r in rows)
res["one_factor_median"] = round(f, 3)
res["repos_within_15pct_of_one_factor"] = sum(abs(f * r["words"] / r["cl100k"] - 1) <= 0.15 for r in rows)
res["repos_counted"] = len(rows)
res["by_lang"] = {}
for lang in REPOS:
    rs = [r["tokens_per_word"] for r in rows if r["lang"] == lang]
    if rs:
        res["by_lang"][lang] = {"median": round(statistics.median(rs), 3), "min": min(rs), "max": max(rs),
                                "pooled": round(sum(r["cl100k"] for r in rows if r["lang"] == lang)
                                                / sum(r["words"] for r in rows if r["lang"] == lang), 3)}
res["words_x1.3_share_of_true_median"] = round(statistics.median(r["words_x1.3_over_cl100k"] for r in rows), 3)
res["chars_over_4_share_of_true_median"] = round(statistics.median(r["chars_over_4_over_cl100k"] for r in rows), 3)
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "repos"}, indent=1))
