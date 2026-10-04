---
title: How the Grinder's nightly works
---

## The loop

The scan pulls new Solana pools. The rules pick gate-passers. The scorer marks exits.

```flow
scan -> rules -> ledger
ledger -> score
```

## What each step costs

| Step | Calls | Time |
|---|---|---|
| scan | 120 | 40 s |
| rules | 0 | 2 s |
| score | 46 | 20 s |

## Why it matters

Paper trades are committed before the outcome is known. The commit time is the proof.
