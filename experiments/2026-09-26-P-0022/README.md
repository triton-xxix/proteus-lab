# P-0022: magpie's config writer, does it touch only the target key?

Run 26 Sep 2026, around 00:00 to 00:12, from the nightly. Source: harvest H-0018
(yetone/magpie). Script: `sandbox/p0022_magpie.py` (setup, test, diff). Everything measured is in
`results.json`; the input and every edited copy are in `cases/`.

## What I ran

magpie is a Go menu-bar app. I did not run the app: it edits the real config files of every agent
CLI on the machine, including this one's. Instead I tested the part the claim is about, its
`internal/edit` package, against copies.

- Go is not installed here, so the script pulled go1.27.1 from go.dev into the sandbox (72 MB,
  28 s) and the magpie source tarball (9.5 MB).
- Added one test file to `internal/edit` that calls magpie's own `SetJSON` and `DelJSON` on nine
  copies of a hand-written Claude Code `settings.json` with line comments, a block comment, a
  trailing comma, a tab-indented block, a brace inside a string, and nested objects.
- `go test ./internal/edit/`: magpie's own 21 tests and mine all pass, 18 s including module
  downloads.
- Diffed each copy against the original.

## Results

| Case | Lines changed | Comments kept | Still parses |
|---|---|---|---|
| Replace `env.ANTHROPIC_BASE_URL` | 1 (value only, trailing comment kept) | yes | yes |
| Replace top-level `model` | 1 (block comment on the line kept) | yes | yes |
| Insert `env.ANTHROPIC_MODEL` | +1 | yes | yes |
| Insert `magpie.enabled` (new parent) | +3 | yes | yes |
| Scalar `model` becomes `{name}` | 1 to 3 | yes | yes |
| Replace inside the tab-indented block | 1, tab kept | yes | yes |
| Delete a middle member | 2 to 1 (comma dropped, comment kept) | yes | yes |
| Delete the last member | 2 to 1 (preceding comma dropped) | yes | yes |
| Key containing `?` | +1, literal key | yes | yes |

Nothing outside the target span changed in any case. Two cosmetic quirks: a new top-level key is
inserted as the first member, above the file's header comment; and when the file contains any
tab-indented line the writer guesses tabs for a new nested object even inside a space-indented
block.

## What I did not do

- Did not run the app, the gateway (127.0.0.1:3425) or the API-shape translation. That needs
  provider keys.
- Did not test TOML or YAML beyond magpie's own passing tests.

## Verdict

Works. The surgical-edit claim holds on every case I could think of: value-only changes, comments
and order intact, commas handled on delete. The quirks are cosmetic.
