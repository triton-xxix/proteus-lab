# jc 1.26.1, run 19 Oct 2026 (nightly ran-it)

Installed with pip into `sandbox/jc-venv` (Python 3.14.6). Clean install, pure Python.

Ran with the "magic" syntax (`jc -p <command>`), which runs the command and parses its output:

- `jc -p dig api.binance.com`: full structure, CNAME chain to CloudFront, TTLs, query time 26 ms.
  `when_epoch` filled, `when_epoch_utc` null, because the timestamp was BST, not UTC (documented
  behaviour: it only fills the UTC field for a UTC stamp).
- `jc -p ping -c 3 1.1.1.1`: per-reply rows plus summary (min 7.1, avg 20.9, max 47.5 ms, 0% loss).
- `jc -p netstat -rn`: every macOS route row parsed, with flags expanded to names (UGScg to UP,
  GATEWAY, STATIC, PRCLONING). Not reproduced here: it is this Mac's network.
- `jc -a`: 249 parsers (229 standard, 20 streaming, 16 slurpable).

Denied: one inline `python3 -c` call to count parsers through the library (not on the safe list);
`jc -a` gave the same counts.

Verdict: works. Useful where a Proteus script shells out and scrapes text (dig, ping, netstat);
the edge watcher's venue latency checks could log `jc ping` rows instead of hand regexes.
