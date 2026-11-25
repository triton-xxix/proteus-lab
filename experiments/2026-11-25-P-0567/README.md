# P-0567: does the 23 Nov lead list land cleanly in Hermit CRM?

Nightly 25 Nov 2026, refill from REFILL-SOURCES row 242. P-0549 (23 Nov) installed Hermit CRM 1.1.0 and listed
its MCP tools on demo data only. This imports a real list: the 20 plumbing and heating firms the trade finder
pulled from OpenStreetMap on 23 Nov.

Called shot: works, 20 of 20 imported in one command, `check` passes with no errors. Hit.

## What I ran

`run.py` writes the 20 rows as a CSV inside `sandbox/p0567/` (gitignored, so firm names stay there), runs
`hermitcrm init` on a fresh folder, then `import` as a dry run, with `--apply`, the same import again, then
`check` and `report`. `hermitcrm` runs by its absolute path under `sandbox/hermit-venv`. `results.json` keeps
Hermit's own output with every firm name and URL replaced (checked: no name or URL left in it).

## Result

- Dry run then `--apply`: **20 created, 0 updated, 0 skipped, 0 failed**, one command each, one git commit
  in the data folder. 40 Markdown files (a company file and an import note each).
- Header detection worked without `--map`: `name -> name, website -> website`, but **`phone`, `postcode` and
  `industry` all went to `notes`**, an interaction note on each company, not fields. A list whose value is
  the phone column loses it to free text unless the fields are added to `fields.toml` first.
- The same import again: 0 to create, **20 skipped, "already up to date"**. Re-running is safe.
- `check`: "OK: 20 companies, 0 contacts, 20 interactions, no problems". `report`: 20 in `prospect`, source
  `list` 20.

## Verdict: works

A lead list lands in a Markdown CRM in one command, idempotently, and validates clean. The catch is the
mapping: only name and website are first-class fields by default, so for the trade finder's rows (3 of 20
with a site, more with a phone) the useful columns end up in notes. Nothing was sent, and the outreach and
send commands were not touched.
