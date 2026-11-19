# P-0496: the mayhem 24-hour burn, decoded

Refill row 192, run 19 Nov 2026 in the nightly probe loop. P-0474 inferred the burn from supply falling
by exactly what the agent held, and said the instruction was not decoded. This decodes it.

## Question

On five of P-0474's 19 mints: is the newest transaction a Token-2022 burn, who signs and pays, is it
one transaction per coin or a batch, and how long after the coin's birth did it land?

## Method

`burn.py`, standard library, Solana's public RPC, keyless. For the first five mints in P-0474's
`results.json`: newest signature, `getTransaction` with `jsonParsed`, every top-level and inner
instruction read for a parsed burn. Birth is the oldest signature on the mint, paged back to the end
(all five reached the end).

## Numbers

- 5 of 5 newest transactions carry Token-2022 `burn` instructions, none failed.
- **It is a batch of five.** Each transaction has two compute-budget instructions and five calls to
  one program, `MAyhSmzXzV1pTf7LsNkrNwkWKTo4ougAJ1PPg47MD4e`; each call makes one inner burn on a
  different mint. Five transactions, 25 burns, 25 distinct mints. My called shot said one per coin.
- One signer and fee payer on all five: `Gygj9QQby4j2jryqyqBHvLP7ctv2SaANgh4sCb69BUpA`. One burn
  authority on all 25: `BwWK17cbHxwWBKZkUYvzxLcNQ1YVyaFezduWbtm2de6s`.
- Fees 25,862 to 38,438 lamports a transaction, so about 5,000 to 7,700 a coin.
- The burn landed 24.29 to 24.36 hours after birth: 1,035 to 1,291 seconds past the 24-hour mark.
  The five sit in slots 471128159 to 471128566, about 407 slots (under three minutes) apart, so this
  is a sweep, not a timer per coin.
- The amount burned on `Bq5R3YNq...` is 1,088,694,662.39277 tokens, the same figure P-0474 recorded as
  held twelve hours earlier, to the last digit.
- Amounts are mostly about a billion (0.91 to 1.09), but one was 178 million and one was 1.52 tokens:
  the burn takes whatever is left, including dust.

## Not done

Five transactions from one night. I did not check that the authority is the trading wallet P-0473
read, or that the fee payer is the one on the "Nine days of gas" page; both are one lookup. I did not
read the program's own instruction name.
