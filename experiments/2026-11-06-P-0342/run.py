#!/usr/bin/env python3
"""Does NeuroCode's slicer hold 1,200 tokens in under a second, model-free, on a real repo?

The tool counts tokens as words * 1.3. Its output adds markdown it does not count. So each slice is also
counted with tiktoken cl100k_base where that loads, and chars / 4 always.
Args: repo_root label. Output appended to results.json beside this file.
"""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/neurocode-deps")
sys.path.insert(0, "/Users/triton/PROTEUS/sandbox/neurocode")

from src.graph.builder import RepoGraphBuilder  # noqa: E402
from src.graph.slicer import CodeGraphSlicer  # noqa: E402

try:
    import tiktoken

    ENC = tiktoken.get_encoding("cl100k_base")
except Exception as e:  # network or package failure is a result, not a crash
    print("tiktoken unavailable:", e)
    ENC = None

QUERIES = [
    ("url_for raises BuildError when a blueprint endpoint is missing", "url_for"),
    ("session cookie is not saved when the response is streamed", "save_session"),
    ("test client does not preserve the request context after dispatch_request", "dispatch_request"),
    ("send_file gives the wrong mimetype for a filename with no extension", "send_file"),
    ("jsonify sorts keys even when the app config turns sorting off", "jsonify"),
]

root, label = sys.argv[1], sys.argv[2]
BUDGET = 1200

t = time.perf_counter()
g = RepoGraphBuilder(root).build()
build_s = time.perf_counter() - t
n_py = sum(1 for d in g.nodes(data=True) if d[1].get("type") == "file")
print(label, "files", n_py, "nodes", g.number_of_nodes(), "edges", g.number_of_edges(), "build_s", round(build_s, 3))

rows = []
s = CodeGraphSlicer(g, max_tokens=BUDGET)
for q, want in QUERIES:
    for k in (1, 2):
        t = time.perf_counter()
        seeds = s.find_seed_nodes(q)
        sub = s.extract_subgraph(seeds, k_hops=k)
        text = s.format_slice_for_llm(sub, seeds, query=q)
        secs = time.perf_counter() - t
        est = None
        for line in text.splitlines():
            if "Estimated:" in line:
                est = int(line.split("Estimated:")[1].split("tokens")[0].strip())
        row = {
            "repo": label,
            "query_target": want,
            "k": k,
            "secs": round(secs, 4),
            "seeds": len(seeds),
            "sub_nodes": sub.number_of_nodes(),
            "tool_estimate": est,
            "chars_over_4": len(text) // 4,
            "cl100k": len(ENC.encode(text)) if ENC else None,
            "target_in_slice": want in text,
        }
        rows.append(row)
        print(row)

out = Path(__file__).with_name("results.json")
prior = json.loads(out.read_text()) if out.exists() else []
prior = [r for r in prior if r.get("repo") != label]
prior.extend(rows)
prior.append({"repo": label, "summary": True, "py_files": n_py, "nodes": g.number_of_nodes(), "edges": g.number_of_edges(), "build_s": round(build_s, 3)})
out.write_text(json.dumps(prior, indent=1))
