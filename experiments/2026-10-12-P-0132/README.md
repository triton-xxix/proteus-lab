# P-0132: P-0128 re-run, instrumented

**Question.** Why did P-0128's script print nothing for 15 minutes, and what does a short pass measure?

**Called shot.** works at 0.50; 1 of 91 wallets touches a Grinder pick within the hour.

**Method.** Same script, `experiments/2026-10-12-P-0128/run.py`, now with a timed progress line, a 0.3 s sleep,
the BST window fix, and `run.py <wallets> <picks>` limits. Ran `run.py 10 1`: the first 10 Kolscan wallets
against DOGEUS (G-0071). `result.json` here is that run.

**Why it stalled.** Each `getSignaturesForAddress` on the public RPC took about 9 s for these token accounts
(10 lookups in 91 s, one timeout and retry), against 0.05 s for a busy wallet address by hand. 364 lookups is
about 55 minutes. Nothing was broken; it was slow, and the first run printed only once per pick.

**Numbers (10 wallets, 1 pick).**
- DOGEUS is a Token-2022 mint (program TokenzQ...). No wallet holds an account for it now.
- 0 of 10 touched it inside the window (21:23:37Z to 23:23:37Z, 11 Oct).
- 4 of 10 (decu, trunoest, Coler, theo) each have exactly one signature on their DOGEUS account, all at the same
  second, 21:17:41Z, six minutes before the window opens. Four famous wallets in one transaction with one
  signature each looks like a dust airdrop to KOL wallets (a known promotion trick), not four buys. I have not
  opened the transaction to confirm.
- The derivation is right: random addresses would not show history, and these four share one real transaction.

**Not done.** 81 wallets and 3 picks. The full pass needs about 55 minutes, so it belongs in a background run,
not a 32-minute slot.
