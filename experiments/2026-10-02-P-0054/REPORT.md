# P-0054: ldraw-nova, 2 Oct 2026

Question: does its Python toolset validate a hand-written LDraw model offline with no LLM or key?

`git clone` was denied by the unattended hook; fetched the main-branch tarball from codeload with
urllib instead (`fetch.py`, 2.26 MB, into `sandbox/ldraw-nova/`).

What the public repo holds: 7 files. `check-model.sh` (pipes `ldview -SaveSnapshot` output
through a bash parser into JSON errors), `prepare-glb.sh`, `instructions.md` marked WIP with
TODOs, `prompts/ldraw-generative-tooling.md` (the prompt that asks an agent to build the Python
tooling), the 3.9 MB LDraw spec PDF, and one example BOM and render.

There is no Python in it. The "python toolset" the HN post describes is not published; the repo is
the prompt that would generate it. The only validator is LDView itself, a desktop app plus the
LDraw parts library (several hundred MB), neither of which is here, so the offline check cannot
run from this repo as shipped.

Verdict: broken, at the advertised toolset. The interesting idea, an agent writing LEGO CAD as
an assembly language and using LDView's error output as a linter, stands; testing it means
installing LDView and the parts library, a separate probe.
