# P-0061: replica-skill, does recon tooling turn a help page into a features.csv?

Harvest H-0129. Repo Jakeschincariol/replica-skill (56 KB tarball, 53 entries) in `sandbox/p0061/`.

## What is actually there

The question assumed recon has tooling. It does not. `replica-recon/` is a SKILL.md of instructions to
the model (scope, sources table, screens, flows, data model, feature matrix) plus two templates: a
`recon-map.md` and an 18-row `features.csv` for a Calendly-like booking app. The features.csv is
written by the model reading pages; no script reads a help page. So the answer to the probe's question
is **no: there is nothing to run on a page**, and the quality of recon is model behaviour, which the
harvest judge already marked "needs-a-run".

The deterministic parts are scorers and helpers, standard library only: `replica-diff/parity.py`
(feature parity score from the CSV, plus optional `imgdiff.py` output), `replica-entrepreneur/reviews.py`
(ranks a reviews CSV you supply against keyword themes, with age weighting), `replica-design/contrast.py`,
`replica-brand/sweep.py`, `replica-launch/listing.py`.

## What I ran

- `parity.py replica-recon/features.csv --markdown`: runs, scores the template 0.0/100 (17 counted,
  0 of 9 must-haves done, the marketplace row correctly excluded as a skip). It is a weighted count of
  a yes/no column.
- `reviews.py --help`: runs; it needs a reviews CSV and does not fetch reviews.
- The repo's tests: not run. No pytest in the venv, and the tests directory is not a package so
  `unittest discover` refused it. Not installing pytest for a 25-minute probe.

## Verdict

Not worth it. The "clone any app" pipeline is eleven prompts; the code that exists is a parity counter
and a keyword ranker over CSVs the model or the user writes. Nothing here maps an app from public
pages without a model doing the reading, and that part is what Claude Code already does with no skill.
The review-mining idea is fine and costs about 50 lines anywhere.
