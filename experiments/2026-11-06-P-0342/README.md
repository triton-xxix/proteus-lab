# P-0342: NeuroCode's slicer and its 1,200-token limit

Question: does the graph slicer cut a real repo to under 1,200 tokens in under a second, with no model?

Method: fetched the repo tarball, installed only tree-sitter, tree-sitter-python, networkx and tiktoken into
`sandbox/neurocode-deps/`, ran `RepoGraphBuilder` and `CodeGraphSlicer` on Flask (83 Python files, 911 nodes,
1,446 edges) with five bug reports I wrote, at one and two hops. `run.py`, `results.json`.

| | Measured |
|---|---|
| Graph build | 0.313 s |
| Slice time | 3.4 to 43.1 ms (README says 0.62 ms) |
| Tool's own estimate | 1,136 to 1,200, never over |
| Real size, cl100k_base | 1,985 to 3,318; median 2,164 at one hop, 2,726 at two |
| chars / 4 | 2,078 to 3,206 |
| Named function in the slice | 3 of 5 at one hop, 4 of 5 at two |

Where it breaks: `slicer.py` counts `len(code.split()) * 1.3`. Code has few spaces and many tokens per word, so
the count runs low, and the markdown wrapper is not counted at all. The "formally guarantees" line in its
docstring holds for its own estimate, not for what a model is sent. Real slices are 1.65 to 2.76 times the
budget.

Speed holds: well under a second, no model called.

Caveats: cl100k_base is not the tokeniser of a small local model, though chars / 4 agrees. One repo, five
queries of my own that mostly name the function, so the retrieval row is generous. No model was run, so nothing
here tests the SWE-bench or RepoBench figures.
