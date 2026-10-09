# Spend ledger

Cap: £50.00 a month on the Proteus virtual card (Luke loads it; entered into services by Luke once
each). Prepaid balances count when drawn down. Month resets on the 1st. Mirrored on the lab page.

## Card status

Card exists in 1Password as "proteus debit Card", tagged proteus. Loaded with **£40.00** by Luke on 2026-09-29 (his
figure, given in session; not yet confirmed against a statement). That is the autonomous line for the rest of
September: £40 on the card, inside the charter's £50. Proteus is on free tiers and existing keys until it names a
service. Keys live in the 1Password vault "Proteus", read at night through the service account (`bin/secrets.py`);
the card item stays in Luke's own vault, because no script ever needs it.

## September 2026

| Date | Service | What | Amount | Running total |
|---|---|---|---|---|
| | | | | £0.00 |

## Services that would need the card, if the free tier runs out

| Service | Why | Expected cost | Status |
|---|---|---|---|
| The Odds API | closing odds beyond 500 requests a month | $30/mo (20k requests) | free tier first |
| Helius or Birdeye | Solana token data beyond the free rate limits | $0 to $49/mo | free tiers first |
| football-data.org | fixtures and results beyond the free 10 competitions | €0 | free tier is enough |

## Luke's xAI account (not the Proteus card)

Luke named his xAI key for Proteus in session on 30 Sep 2026. Spend lands on his xAI account, not
the virtual card, so it sits outside the £50 autonomous line and the £250 ceiling and is shown here
so he can see it. Figures are the API's own reported cost per call.

| Date | What | USD |
|---|---|---|
| 2026-09-30 | tests: one X search, one narrative summary | 0.31 |
| 2026-09-30 | mentions backfill, 58 tokens | 2.51 |
| 2026-09-30 | nightly: mentions 0.35, narrative 0.15 | 0.50 |
| 2026-10-01 | nightly: narrative only; mentions cost not recorded (output file unreadable) | 0.18 + unknown |
| 2026-10-02 | nightly: mentions 0.34, narrative 0.15 | 0.49 |
| 2026-10-03 | nightly: mentions 0.17, narrative 0.15 | 0.32 |
| | Total known to 3 Oct | 4.31 |
| 2026-10-09 | pre-listing research, on Luke's approval of up to $10 for it: 7 Coinbase-post searches 3.57, X mentions case-control (5 pairs) 6.23, tests 0.15; ledger experiments/2026-10-09-prelisting/xai-calls.jsonl | 9.95 |
| | Total known (nightly mentions after 3 Oct not yet added here) | 14.26 |

## Luke's Gemini and ElevenLabs accounts (not the Proteus card)

Luke named these keys for Proteus in session on 7 Oct 2026, for the Sixteen Nights record (the film
and the page at `docs/record/`). Spend lands on his accounts, outside the £50 line and the £250
ceiling, and is shown here so he can see it. Estimates at the bootcamp config's 1 Oct 2026 prices;
the per-call ledger is `sites/builds/sixteen-nights/media-ledger.jsonl`; the providers' bills are the truth.

| Date | Service | What | Est. USD |
|---|---|---|---|
| 2026-10-07 | Gemini (Nano Banana 2) | 8 stills at 2K: night desk, clean plate, car, wet street, portrait variants | 0.81 |
| 2026-10-07 | Gemini (Veo 3.1 fast) | 1 clip, 8 s 1080p, the car; the second clip was refused: prepaid credits depleted (HTTP 402) | 0.96 |
| 2026-10-07 | ElevenLabs | 30 voice lines (Edward, tests and re-renders included), one 95 s music bed | 0.49 |
| | | Total, estimated | 2.26 |
