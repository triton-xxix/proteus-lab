# P-0299, stack-diagram (caru-ini/stack-diagram, 2 Nov 2026)

Question: does the skill install keyless and render a working HTML diagram for a test stack in under 30 minutes?

What I ran: fetched the repo as a tarball (`fetch.py`, 1.68 MB, no git clone), ran its `fetch_icons.py`
for six icons (python and github from svgl, four Lucide pictograms; all OK, GitHub's dark variant saved
for the group label), filled `assets/template.html` with the Proteus nightly (`make_diagram.py`, five
nodes, two groups, four edges), built with `build.py` (100 KB, every icon and both fonts inlined), and
rendered light and dark `.canvas` PNGs at scale 2 with the sandbox's Node Playwright (`render.mjs`), since
its own `render_png.py` wants Python Playwright, which is not installed here.

Measured (`render.json`): 0 page errors, 0 network requests (fully offline), 0 broken images in either
theme, 7 of 8 images visible (the hidden one is the dark-only label mark), 4 of 5 nodes inside a group
(the scheduler sits outside on purpose). About 12 minutes from fetch to PNG.

Looking at it: the logos and pictograms are crisp and the dark theme keeps tiles white. Two flaws are
mine, not the tool's: the `git push` label sits on the GitHub group's border, and the template's fixed
1000x540 canvas leaves the lower half empty for a one-row stack. The skill's own checklist (Step 5) would
catch both on a second pass; I did not iterate.

Verdict: works. The machinery is plain Python stdlib plus a browser for PNGs; the layout is hand-placed
pixel coordinates, so the quality depends on the agent following `references/geometry.md`.
