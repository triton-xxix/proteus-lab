# pump-trades

One standard-library Python file that reads the latest pump.fun transactions from Solana's public RPC,
keyless, decodes every TradeEvent the program logs, and checks each fee against amount x bps.

```
python3 pump_trades.py                                  # 60 transactions, summary to stdout
python3 pump_trades.py --n 300 --out run.json --csv trades.csv
python3 pump_trades.py --rpc https://your.rpc/ --n 1000
python3 pump_trades.py --from run.json                  # re-score a saved run, no fetching
```

Fields kept per trade: mint, user, sol_amount, token_amount, is_buy, timestamp, virtual reserves,
fee and creator fee (bps and amount), ix_name, mayhem mode, cashback, buyback, shareholders count,
quote mint and amount, holder rewards, and the signature.

Where it came from: probes P-0464 (decode and fee check, 41 of 41) and P-0465 (the tail past
ix_name, the zero-fee trades are mayhem mode) on 17 Nov 2026. The first run of this tool added one
fact: on a trade quoted in a token other than SOL, `sol_amount` is 0 and the fee is charged on
`quote_amount`.

Limits: the public RPC is slow and drops or rate-limits many fetches (the run says how many). The
buyback bps field can read 5000, a share of the fee and not of the trade, so bps are never summed.
The event cannot show a fee taken outside it; for that, read the transaction's balance changes.

`build.py` draws `index.html` from `run-2026-11-17.json` and the two probes' results; `lint.py`
checks it.
