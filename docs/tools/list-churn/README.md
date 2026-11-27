# list-churn

Diff two versions of an awesome list and check every "removed" repo before you count it.

A plain diff of GitHub links counts a renamed or transferred repo twice: the old name as removed, the
new one as added. `list_churn.py` asks the keyless GitHub API about each removed name (it follows the
redirect) and sorts it into one of:

- **moved, re-listed**: the repo has a new full name and that name is in the new list. Not a removal.
- **moved, not re-listed**, **archived**, **deleted or private**, **live, dropped**: real removals.
- **unchecked**: past `--max`, or the API errored. Counted, never guessed.

```
python3 list_churn.py OLD NEW [--out run.json] [--max 50] [--sleep 0.5]
python3 list_churn.py --from run.json
```

OLD and NEW are paths or https URLs, either a README (markdown) or a file of `owner/repo` lines. An old
version of a list on GitHub: `https://raw.githubusercontent.com/OWNER/LIST/<sha>/README.md`. Standard
library only. Keyless GitHub allows 60 calls an hour.

## First runs (27 Nov 2026)

- awesome-mcp-servers, 17 to 26 Nov: 371 added and 6 removed by URL; all 6 moved and re-listed, 0 real
  removals, 365 net additions. Matches Proteus probe P-0585 name for name.
- awesome-mcp-servers, 26 Oct commit to 27 Nov: 435 added, the same 6 removed, 0 real removals.
- awesome-mcp-servers, 26 Nov snapshot to 27 Nov, and awesome-claude-code 22 Oct to 27 Nov: no change.

`build.py` draws the page from the `run-*.json` files and exits if a summary does not recompute or the
first run disagrees with P-0585. `lint.py` checks the page. From probes P-0576 and P-0585.
