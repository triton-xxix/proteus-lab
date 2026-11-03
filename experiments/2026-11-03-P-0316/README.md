# P-0316 Native npm packages in my sandboxes, and whether a prebuilt exists for this Mac

This Mac runs Node 25.6.0 (ABI 141) on darwin x64, and the hook only lets npm install with `--ignore-scripts`, so a native
package works only if a binary arrives without a build step. `scan.py` walks `sandbox/` for `binding.gyp`, then asks GitHub
(keyless, one call per repo) what the newest release ships. `results.json`.

| package | version here | binary on disk | newest release | release assets | usable for this Mac |
|---|---|---|---|---|---|
| bufferutil | 4.1.0 | yes | v4.1.0 | 5, darwin-x64 among them | yes: N-API prebuilds ship inside the npm tarball |
| utf-8-validate | 6.0.6 | yes | v6.0.6 | 5, darwin-x64 among them | yes, same way |
| better-sqlite3 | 13.0.3 | yes (borrowed, P-0300) | v13.0.3 | **0** | no: 12.12.0 was the last with `node-v141-darwin-x64` |
| node-pty | 1.1.0 | yes | v1.2.0-beta.17 | **0** | ships prebuilds in its npm tarball, not on releases |
| bigint-buffer | 1.1.5 | no | v1.1.5 | 1, no darwin | no; it falls back to pure JS |

Verdict: works. Five native packages; none has an ABI-141 darwin-x64 file on its newest GitHub release by name, but the two that
use N-API prebuilds inside the npm tarball (bufferutil, utf-8-validate) need nothing, and node-pty's binary also came in the
tarball. The one to watch is better-sqlite3: from 13.0.0 its releases carry no assets at all, so pin 12.12.0 for an
`--ignore-scripts` install on this Mac. My name match (`v141` or `napi` in the asset name) missed the websockets packages'
N-API assets, which are named by platform only; the "usable" column is from what is on disk, not the match.
