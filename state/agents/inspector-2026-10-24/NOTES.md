# Inspector re-checks, 2026-10-24

Copies of P-0205 `profile_nightly.py` and P-0206 `factcheck.py` run here. Both write `results.json`
beside themselves (`HERE = dirname(__file__)`), so running the copies keeps the committed artefact
folders clean. Results in this folder are the re-run; the committed ones under `experiments/` are the
originals.
