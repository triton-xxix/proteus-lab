# P-0341: 25% per doubling against constant product

Question, from the rLoop video in tonight's harvest: does a curve that adds 25% per supply doubling beat a
constant-product curve for an early buyer, measured when supply reaches 10x?

Method: closed forms in `curves.py`, no chain data. 25% per doubling is a power law, price proportional to
supply^0.3219. The constant product uses pump.fun's launch figures (1.073bn virtual tokens, 30 virtual SOL,
793.1M sellable). Both are matched in price at the buyer's entry, 1% fee each way, three buy sizes.

Result: the answer turns on where the buyer enters. The power curve pays the same anywhere: 2.10x before fees,
2.06x after. Constant product pays 1.00x at 0.1% of virtual supply, 1.19x at 1%, 2.06x at 3.33%, 5.41x at 6%,
12.3x at 7.39% (the last entry where 10x still fits on the curve). Crossover before fees: 35.7M tokens, 3.33%
of virtual supply, reached after 1.03 SOL has gone in.

Read: "10x supply" flatters the power curve at the very start, because 10x of almost nothing is still almost
nothing on a constant product. It is one way to measure; a fixed target supply would read differently.

Not done: no real launch was replayed, and the buy-size rows move the 10x target with the buy, so they are not
strictly comparable across sizes. The marginal rows are the clean ones.
