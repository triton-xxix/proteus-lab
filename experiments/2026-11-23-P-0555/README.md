# P-0555, same-ticker copycats in the Grinder's snapshots (23 Nov 2026, nightly, refill row 235)

Question: in `grinder/SNAPSHOTS.csv`, how many tickers sit on two or more mints, and does a later mint do worse than the first?

## What started it (refill row 235)

The two "ANT" mints P-0542 flagged are both named "Anthropic Coin", an unofficial memecoin using a company name. Rugcheck's public report (pulled keyless tonight) says both launched on Meteora's bonding curve (`meteora_dbc`), not pump.fun; the PumpSwap pool the Grinder saw is a side pool. Total market liquidity now: $12.56 and $0.55, against $117,765 and $145,301 at the Grinder's snapshots of 16 and 18 Nov. Both carry 0 LP providers and the same five rugcheck risks.

## Measured (`copycats.py`, `results.json`)

5,028 mints over every snapshot night; 3,586 tickers; 668 tickers sit on 2+ mints, covering 2,110 mints (42%).

| Group | n | median chg_h24 at first sighting | median rug_score | median liquidity | seen on a later night |
|---|---|---|---|---|---|
| ticker on one mint | 2,918 | -4.8% | 1 | $4,652 | 10.2% |
| first mint of a shared ticker | 668 | +0.5% | 1 | $13,169 | 16.5% |
| later mints of a shared ticker | 1,442 | -17.5% | 31 | $2,836 | 9.5% |

Most-copied tickers: SI 32 mints, FOMO 26, TRUMP 16, XTO 15, INU 14, OPENAI 14, GTA 14, ROCKSTAR 14, then MRBEAST, NVIDIA, SPEED. Company and celebrity names are a large share of the top list.

## Caveats

- chg_h24 and rug_score are read at each mint's first sighting, not a forward outcome, and "seen again" depends on the Grinder's scan picking the mint up again, so this is a description, not a tested signal.
- A shared ticker is not always a copy (SOL, AI, MEME are generic words).
- I did not check whether the Grinder's gates already reject the later mints; the rug_score gap (31 v 1) suggests the rug gate catches many of them.

Verdict: works. Next, if wanted: a "ticker already seen on an earlier mint" flag as a shadow column, scored forward like the insider filter (D-016).
