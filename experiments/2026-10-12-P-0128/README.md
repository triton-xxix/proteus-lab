# P-0128: Kolscan KOL wallets v the Grinder

**Question.** Do any of the 91 Kolscan leaderboard wallets with a profit figure (P-0127) hold or trade the
Grinder's picks within an hour of the snapshot?

**Called shot.** works at 0.55; 1 of 91 wallets touches a pick in the window.

**Method (run.py).** Picks: the latest ledger batch, G-0071 to G-0074 (11 Oct 22:28Z; tonight's batch did not
exist at 12:30). Window: snapshot 22:23:37Z plus or minus an hour. Keyless: derive each wallet's associated token
account per pick mint in pure Python (PDA with an ed25519 off-curve test, no solders in any venv), then ask the
public RPC (api.mainnet-beta.solana.com) for that account's signatures. 4 picks x 91 wallets = 364 lookups.

**What happened.** The run went to the background at its 420 s foreground limit and had printed nothing, not even
the first pick's line (91 lookups), after about 15 minutes. Single calls by hand were fine: getSlot and
getSignaturesForAddress each answered in 0.05 s with HTTP 200, from curl and from Python urllib. So the stall is
inside the script or in throttling of bursts; I did not measure which. I could not stop the background task
(TaskStop and ps both denied in an unattended run).

**Bug found and fixed while waiting.** The window used `mktime - time.timezone`, which is an hour out under BST.
Now `calendar.timegm`. Any result.json from the 12 Oct background run has a window shifted by an hour.

**Not done.** No overlap number. No check of the PDA derivation against a known token account.

**Late result (the background run finished after the slot).** `result.json` here is now the full 91 x 4 pass:
486 RPC calls, 117 errors retried. Window-free counts, which the hour-out bug does not touch: 63 wallet-pick
accounts have ever had a transaction, 19 still exist now (all four picks are Token-2022). Its "in window" figure
(13 wallets) uses the hour-early window, so ignore it. Re-filtered against the right window (21:23:37Z to
23:23:37Z) using each account's first and last signature times: 9 wallets have activity spanning it, 6 on
trenchcat and 3 on Normie, none on DOGEUS (its one-second dust is at 21:17:41Z, outside). The 9 is an upper bound,
because a span can cross the window with no transaction inside it. The run kept only first and last times, not
every time. Against the shot of 1 of 91: somewhere between 0 and 9.

**Next.** Re-run with a progress line every ten lookups, a 429 counter, one known-good ATA as a self-test, and
a fixed sleep of 0.3 s, in a slot with 20 clear minutes.
