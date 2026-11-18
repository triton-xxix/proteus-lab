# P-0471: sampling the fee-free mayhem wallet's balances

P-0470 showed the wallet `BwWK17cb...de6s` makes about 15 transactions a second, so its trades cannot
be followed one by one on the public RPC. This samples its balances instead.

## What ran

`sampler.py`: `getBalance`, and `getTokenAccountsByOwner` for the classic token program and for
Token-2022, appended to `samples.jsonl`. Keyless, read only, stops itself, stops on HALT.

1. One full test sample at 23:52:11Z. It took over two minutes, because the Token-2022 listing came
   back **HTTP 413, Request Entity Too Large** on every retry: the wallet holds too many Token-2022
   accounts for the public endpoint to list. The classic listing answered: 44 accounts, 43 non-zero.
2. So a `--sol-only` run: six samples three minutes apart, 23:57 to 00:12Z, inside this session.

## Numbers

| time (UTC) | SOL balance | change |
|---|---|---|
| 23:52:11 | 71,303.057 | |
| 23:57:00 | 71,305.513 | +2.456 |
| 00:00:00 | 71,305.700 | +0.187 |
| 00:03:00 | 71,321.181 | +15.481 |
| 00:06:00 | 71,318.058 | -3.124 |
| 00:09:01 | 71,320.583 | +2.525 |
| 00:12:01 | 71,323.680 | +3.098 |

- The wallet holds about **71,300 SOL**. Nobody in tonight's five videos said how big it is.
- Over 20 minutes it gained 20.6 SOL (0.029%), up in five of six steps. At about 15 trades a second
  that is roughly 18,000 trades for 20.6 SOL.

## What this is not

Not profit and loss. SOL in the wallet goes up when it sells coins it was handed for nothing (the
second billion of each mayhem coin), so a rising SOL balance is what selling inventory looks like,
and I could not list the inventory: the Token-2022 call is refused. One wallet may also not be the
whole agent, and SOL may be moved in or out by its owner. Twenty minutes at midnight UTC is not a day.

The 24-hour job was not started: it needs `launchctl`, which a scheduled run may not call, and a way
round the 413 first (page the token accounts by mint with `getTokenAccountsByOwner` and a `mint`
filter per coin seen trading, or sample SOL only and say so).

Shot: both calls answer keyless, balance moves under 5%. Half right: `getBalance` answers and the
move was 0.03%; one of the two token listings does not answer at all.
