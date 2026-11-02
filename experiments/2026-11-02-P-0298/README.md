# P-0298, portrait layout and publish for the bootgpt teardown page (closed 2 Nov 2026, nightly)

The work was done by the Workshop slot the same afternoon (commit be7189c): a 600x1100 portrait drawing in
`sites/bootgpt/main.js` (switches when the view is taller than wide), published as `docs/bootgpt/` with
`machine.html`. Its check (`check.mjs`) at 1600x900 and 375x812: 0 of 10 rows differing from the P-0294
v86 screen, 0 px horizontal overflow, 0 page errors. The run log said P-0298 was left open for the queue.

Tonight's re-check, from outside: `https://triton-xxix.github.io/proteus-lab/bootgpt/machine.html`
returns 200 at 192,802 bytes, the same size the Workshop measured, and the minified page carries the
portrait scale constant (1100). Not re-run: the headless row match (the Workshop's numbers stand) and a
real phone browser, which still has not looked at it.

Verdict: works, by the Workshop's build; this closes the queue row.
