# P-0398: modern-web-guidance legacy-scan, is the 92% precision real?

Source: harvest H-0600, a Show HN from the Chrome team for `modern-web-guidance` 1.0.0 (npm,
publisher GoogleChrome, Apache-2.0). Claim: a deterministic `legacy-scan`, "92% avg precision on
held-out repos".

What I ran: the package installed into `sandbox/mwg` with `--ignore-scripts` (one package, no
dependencies), `legacy-scan` on three targets fetched or held as plain files (`fetch.py`):

| target | files | findings, source only | findings, with docs and tests |
|---|---|---|---|
| Bootstrap 3.4.1 (2019 tag; js, less, docs, no dist) | 178 | 0 | 47 |
| HTML5 Boilerplate 5.3.0 | 8 | 0 | 0 |
| my own lab site, `docs/` | | 0 | 0 |

Three targets, not the five the probe title asked for; only one produced anything.

The 47, each read against the rubric the tool prints with it (`keepWhen` and `dropWhen`):

| rule | flags | meet the rubric |
|---|---|---|
| progress (`div role="progressbar"` with aria-valuenow) | 32 | 32 |
| autofill-sign-in-form (password input with no autocomplete) | 12 | 12 |
| scrollspy (`data-spy="scroll"`) | 3 | 3 |

47 of 47, so precision 100% on this sample, above the 92% claimed and above my shot (70 to 95%).

What that number hides:

- One labeller, me, using their rubric. Every flag sits in documentation: demo markup, and about half
  of them the same markup a second time inside a code-sample block. Nothing here is a shipped app.
- By default the scan skips docs and tests and found nothing at all in Bootstrap 3's own source, the
  library that hand-builds modals, tooltips, tabs and collapses in jQuery. The docs folder has 38 lines
  of modal markup and calls (`.modal(`, `data-toggle="modal"`, `class="modal `) and none was flagged,
  though the launch post leads with `<dialog>`.
- The tool says why: 35 deterministic rules cover 33 guides, "~20% of the guidance corpus". Precision
  is high because the rules are narrow. Recall is what I would ask about next, and no figure is given.

Not run: the search and retrieve commands, the skill itself, any JSX or framework code.
