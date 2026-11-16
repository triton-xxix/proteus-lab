# P-0456: pump.fun creator plus same-slot bundle, share of supply

Called shot: at least 8 of 20 creates have a same-slot buyer besides the creator, median
creator-plus-bundle share 2% to 10%. Wrong on both, on a thin sample.

`bundle.py` reuses P-0440's listener (mint-authority logs on the public websocket, 2 s pace on
getTransaction). For each sampled create it reads every successful transaction in the create's
slot (up to 8) and takes each owner's last balance of the new mint in that slot. Read-only.

## The bug and the fix

Run 1 dropped only the largest owner as the bonding curve and reported creator plus bundle at
100% of supply on 9 of 13. The holder dump in run 2 shows why: on 4 of 7 creates one owner,
`BwWK17cb...`, holds a full 1,000,000,000 alongside the curve's own ~99%. So two curve-sized
balances sit in the slot; I have not identified that account. Run 2 treats every owner at or above
half the supply as curve stock.

## Run 2 (`results.json`)

- 49 creates heard in 1.5 minutes (P-0440 said 29.6 a minute; this is 32.7). 20 sampled, **7
  read**; the other 13 returned no transaction or no mint balance under the public RPC's pace.
- Same-slot buyer besides the creator: **1 of 7** (0.15% of supply).
- Creator share: median 0.70%, max 7.9%. Creator plus bundle: median 0.70%, max 8.0%, none at 10%.

## Verdict

Works, and the answer is small: in this sample, buyers in the creation slot other than the creator
are rare and hold almost nothing; P-0180's 9 of 20 counted the creator's own bundled buy, not
outsiders. Seven reads is too few to quote hard. The unexplained full-supply account is the first
thing to look at next time.
