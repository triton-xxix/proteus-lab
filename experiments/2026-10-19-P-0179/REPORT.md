# P-0179 Grinder v0.2 cost model against live Jupiter quotes

19 Oct 2026, 04:15 BST, nightly refill build (source: Solana and Jupiter developer docs; one hand
quote first to learn the lite API's fields: no per-leg fees any more, `priceImpactPct` and
`swapUsdValue` are there).

Ten pools from tonight's Grinder snapshot, liquidity $20.7k to $2.5M, spread evenly across the range.
For each: quote a $130 SOL buy, then quote selling the tokens straight back; quoted loss is
1 - SOL back / SOL in. The model is v0.2's (`grinder/RULES.md`): 1% fee a side, $0.05 a side,
constant-product impact with Q = half liquidity, no exit slippage allowance. Quotes only, nothing
signed. SOL priced from a 1 SOL to USDC quote. Run 1 got HTTP 429 on every token quote at 1.2 s
spacing; run 2 backed off and paced at 3 s, all ten quoted (`result.json`).

| Pool | Liquidity | Model loss | Quoted loss | Model minus quoted |
|---|---|---|---|---|
| PCAT (pumpswap) | $20.7k | 4.44% | 6.29% | -1.85 |
| mucron (pumpswap) | $34.9k | 3.49% | 3.71% | -0.22 |
| texcat (pumpswap) | $53.0k | 3.01% | 3.09% | -0.08 |
| PEPE (meteora) | $104k | 2.55% | 0.34% | +2.21 |
| MINTER (pumpswap) | $163k | 2.38% | 1.23% | +1.15 |
| swordcat (meteora) | $242k | 2.27% | 1.73% | +0.54 |
| Jimothy (pumpswap) | $448k | 2.18% | 0.77% | +1.41 |
| SI (meteora) | $583k | 2.15% | 2.84% | -0.69 |
| ADP (pumpswap) | $1.37M | 2.10% | 0.64% | +1.46 |
| USDe (pumpswap) | $2.50M | 2.09% | 0.00% | +2.09 |

Result: 8 of 10 within 2 points; median model minus quoted +1.15 points, so on deep pools the model
is conservative (its flat 2% of fees is most of the gap). At the thinnest pool, right at the $20k
gate, the model is 1.85 points too cheap: the real round trip cost 6.29%, not 4.44%. The three
pools under $55k are the ones where the model's error turns from safe to flattering, and they are
the Grinder's typical entries.

Caveats: one sample each, one moment; Jupiter's `priceImpactPct` is not a reliable cost on its own
(mucron: 0% on the buy, 3% on the sell for a near-symmetric round trip); quoted round trips see the
pool as it is now, not as the buy leaves it, matching the model's own assumption.

Verdict: works. Next, if repeated: 30 pools under $60k over several nights to see whether the
thin-pool shortfall is steady enough to matter (a cost-model change would reset the Grinder's
clock, so it goes through RULES.md interactively, not from a probe).
