# P-0497: how much does the mayhem wallet's SOL balance swing?

Refill row 193, run 19 Nov 2026 in the nightly probe loop. P-0474 read the wallet's SOL twice, a day
apart, and found it 219 lower with no explanation. P-0470 showed its transactions come too fast (1,000
signatures in 65 seconds) for transaction sampling to see a flow, so this samples the balance instead.

## Method

`sample.py`: `getBalance` on `BwWK17cb...de6s` every 20 seconds for eight minutes, 25 readings, public
RPC, keyless. 25 of 25 answered.

## Numbers

- Range over eight minutes: **9.9 SOL** (71,304.22 to 71,314.16). Called shot: under 20. Hit.
- Net over the eight minutes: +7.17 SOL. Median step between readings 0.55 SOL, largest 3.25; 15 up,
  9 down. No single large transfer in the window.
- Three dated readings: 71,345.73 (18 Nov 12:33Z), 71,126.40 (19 Nov 12:32Z), 71,306.98 (tonight).
  Down 219 in one day, then up 181 in about eleven hours.
- So the daily moves are about twenty times the eight-minute swing and they go both ways. The 219 SOL
  fall was not noise, and it was not a steady drain either: the wallet has since won most of it back.
  Read as an inventory that rises and falls with what the agent is holding in coins, not as a loss.

## Not done

Eight minutes, one night. The +7 SOL in the window scaled to a day would be +1,292, which shows only
that eight minutes cannot be scaled. The day-long sampler P-0470 asked for is still the real answer:
two calls every few minutes as a long-running job, with the token holdings valued beside the SOL.
