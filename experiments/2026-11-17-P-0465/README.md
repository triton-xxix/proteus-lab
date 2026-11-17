# P-0465: the zero-fee pump.fun trades

**Question.** P-0464 found that 18 of 41 decoded TradeEvents carried 0 fee bps and 0 creator bps. Decoded
past the variable-length `ix_name`, what are those trades, and has their take moved to another field?

**Method.** `tail.py` reuses P-0464's definitions and unpacks the rest of the TradeEvent (layout in
the docstring): mayhem_mode, cashback and buyback bps and amounts, the shareholders vector, quote mint
and amount, holder rewards. 60 fresh transactions from the public RPC; only 19 carried a full-length
TradeEvent this time (P-0464's minute had 47 in 47), so this is a smaller and different sample.

**Numbers** (results.json).

- 10 zero-fee trades (7 buy, 3 sell): **all 10 in mayhem mode**, SOL quote (the quote-mint field holds
  the all-ones system default), and **0 in every fee field**: fee, creator, cashback, buyback, holder
  rewards. The take has not moved anywhere in the event.
- 9 paid trades: 4 of them also in mayhem mode, so mayhem mode alone is not the rule. 4 of the 9 show
  95 + 30 bps as in P-0464; 5 show buyback_fee_basis_points 5000 and 4 show holder rewards 30 bps.
- 2 paid trades use a non-SOL quote mint (`SPCXxcqX...`) with sol_amount 0 and quote_amount set: the
  `buy_exact_quote_in` path, which P-0464 did not pair.
- **Correction to my own script:** `total_bps` adds buyback_fee_basis_points to the others, but 5000
  can only be a share of the fee (half to buyback), not 50% of the trade. The 5155 and 5125 totals in
  results.json are wrong for that reason; the per-field counts stand.

**Reading.** On this sample, zero-fee trades are mayhem-mode trades that pay nothing the event records.
Either the fee is truly waived for some mayhem-mode curves, or it is taken outside the event (a
transfer the event does not report). The event alone cannot tell, so a fill model should not assume
1.25% on every trade, and should not assume 0 on mayhem trades either.

**Called shot.** works at 0.50, "take moved to buyback or cashback, total still about 125 bps". Missed:
every fee field is 0 on all 10.

**Not done.** The SOL balance changes of the zero-fee transactions (the one way to see a fee the event
does not record). The mayhem-mode paid trades not separated from the unpaid ones by any other field.
19 events is small.
