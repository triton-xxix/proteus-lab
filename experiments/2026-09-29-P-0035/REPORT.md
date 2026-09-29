# P-0035: Browserless API with the vault key

Not run. The key is in the Proteus vault and the vault is unreachable from tonight's scheduled run:
`secrets.py check "Browserless"` timed out at 30s at about 23:40, the third op hang of the night
(see `experiments/2026-09-29-P-0034/REPORT.md`). A keyless call to Browserless would only return
an auth error and says nothing about the question (can a hosted browser wait for a postMessage and
screenshot), so I did not make one.

Verdict: blocked, on the same cause as P-0034. Reruns unchanged once the service account answers
from a nightly.
