# P-0464: pump.fun TradeEvents decoded from live transactions

**Question.** The 16 Nov ran-it found that 65 of 132 pump.fun inner instructions were the Anchor event
wrapper `e445a52e51cb9a1d`, and left them undecoded. Decoded with the public IDL's TradeEvent layout, do
the events agree with the buy and sell instructions they come from, and do the fees follow the bps
the event itself states?

**Method.** `events.py` reuses the ran-it's RPC, base58 and solders set-up (definitions only), takes the
latest pump.fun signatures on the public mainnet RPC (keyless), and stops at 60 fetched or when it runs
out of successful signatures (it reached 47). It unpacks the TradeEvent's fixed-width prefix (offsets
in the docstring) and pairs events with `buy`, `sell` and `buy_exact_sol_in` instructions in order
within each transaction. Checks are in the docstring.

**Numbers** (results.json).

- 47 transactions, 47 TradeEvents, 41 trade instructions of the three kinds paired (10 buy, 11
  buy_exact_sol_in, 20 sell). The 6 unpaired events came from `buy_exact_quote_in_v3`, `sell_v2`
  and `sell_v3`, which I did not pair.
- **Args consistent: 41 of 41.** Token amount equal to the instruction's amount and SOL inside the
  slippage bound, on every buy and sell.
- **Fee within 1 lamport of sol_amount x bps / 10,000: 41 of 41**, creator fee the same, 41 of 41.
- But **18 of 41 trades show 0 fee bps and 0 creator bps**, and they pass trivially. The fee check
  that means something is **23 of 23** at 95 bps protocol plus 30 bps creator (1.25% all in).

**Reading.** The IDL layout decodes cleanly, and the event is a faithful receipt of the trade, so a
Grinder fill model can read the real SOL in and out and the real fee from the event instead of working
them out from balance changes. The 18 zero-fee trades are new to me: a fee-free class of trades on
pump.fun is either a fee tier I have not read about or fees moved to a field after `ix_name` (the
`shareholders` vector, cashback, buyback) that I did not decode.

**Called shot.** works at 0.60, "about 95% consistent, fee within 1 lamport on about 90%". Measured
100% and 100%, both above my numbers; the direction held.

**Not done.** Fields after the variable-length `ix_name` (cashback, buyback, shareholders, quote mint)
not decoded. The v2 and v3 instructions not paired. 47 transactions from one minute of traffic.
