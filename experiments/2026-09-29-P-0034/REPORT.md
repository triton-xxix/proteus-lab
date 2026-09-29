# P-0034: Metaculus API with the vault token

Vault listing failed after 90.0s: op timed out after 90s

## What this says

- The Metaculus half never ran. The token is behind `bin/secrets.py`, and the service account
  `op` call hung twice tonight from inside the scheduled run: `secrets.py list` timed out at 30s,
  and this script's `op item list` at 90s. Nothing was printed and no error came back, just silence.
- A direct `/usr/local/bin/op --version` to tell a hung binary from a blocked network was denied by
  the hook (not on the unattended safe list), so I cannot say which it is from here.
- The same service account worked in the interactive session of 29 Sep (P-0036 read the
  SportsGameOdds key through it). So the likely difference is the scheduled run's sandbox or
  network, not the token. That is a guess, labelled as one.
- This blocks every vault-token probe in a nightly, not just this one, and harvest.py's GitHub
  token path quietly falls back to keyless in the same way.
- Verdict: blocked, on the 1Password service account being reachable from a scheduled run. Next
  step is an interactive test: run `secrets.py list` inside the same sandbox as the nightly and
  time it. Script `metaculus_token.py` reruns unchanged once it answers.
