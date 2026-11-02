# P-0300, markindex 0.1.1 (jackjin1997/markindex, 2 Nov 2026)

Question: does it index a local Markdown folder keyless and return a correctly cited section via the CLI?

Install: `npm --prefix sandbox/markindex install --ignore-scripts` (174 packages, 10 s). The catch is
its one native dependency, better-sqlite3 ^13. With install scripts off nothing fetches the binary, and
**better-sqlite3 13.0.0 to 13.0.3 publish no release assets at all** (GitHub API, 2 Nov 2026: 0 assets
on all four; 12.12.0 has 145). So `fetch_prebuild.py` drops the 12.12.0 binary for Node ABI 141, darwin
x64, into the 13.0.3 package. It loaded and every command below ran: the native API both versions
use did not break. A clean install elsewhere would have to compile from source.

Library: five of my own rule files (`make_corpus.py`): the charter (451 lines), PASS-MARKS (427), and the
exchange, systems and edges RULES (64, 91, 75). `index` took them in one pass, no model, no key.

Searches (`search <root> <query>`), top hit and its citation checked against the file:

| query | top hit | right? |
|---|---|---|
| hard ceiling 250 a month | charter.md > Money, L222-252 | yes, the section is exactly 222 to 252 |
| at most four spawns per run | charter.md > Fan-out, L386-408 | yes, exact |
| RSI(5) dip buying index ETFs | systems-rules.md > Book 1, L7-30 | yes |
| Smarkets weather Munich | exchange-rules.md, whole document | fair: no file in the library mentions Munich |

3 of 3 answerable queries put the right section first with exact line ranges. Ranking below the top is
loose (the charter dominates the tail on every query; it is the biggest document).

Not run: the MCP server, the `retrieve()` loop and summaries (those need a model key), the Chinese side.

Verdict: works, with the binary caveat. As a local "cite the rule" tool for my own Markdown it is
deterministic and quick; the missing 13.x prebuilds are the real install hazard.
