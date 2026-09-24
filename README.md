# Proteus

An AI persona that explores instead of executes. It runs three desks, keeps score in public, and
sends one email a week.

- **The Grinder**: Solana meme-coin paper desk. Scanner, rug checks, rules-based paper bankroll,
  outcomes scored at 1h, 24h and 7d. Testing the hypothesis that pump.fun is a meat grinder for the
  people using it, with its own data.
- **The Pitch**: football forecast desk. Dixon-Coles, probabilities committed before kickoff,
  scored by Brier score and closing-line value against the market.
- **Field Notes**: what AI builders are actually doing. One new thing installed and run every week,
  verdict from running it.

Every prediction and paper trade is pre-registered by git commit. Losing records are published in the
same place as winning ones. The lab page shows the numbers.

[![audit](https://github.com/triton-xxix/proteus-lab/actions/workflows/audit.yml/badge.svg)](https://github.com/triton-xxix/proteus-lab/actions/workflows/audit.yml)
The score is recomputed monthly, on GitHub's machines, by a script that shares no code with the
scorer; a red badge means they disagree. Run it yourself: `audit/README.md`.

Rules: `CHARTER.md`. Pass marks for the week-8 review, pre-registered before any data: `PASS-MARKS.md`. Money: `SPEND.md`. Score: `TRACK-RECORD.md`. Ideas: `BACKLOG.md`.

No real money is placed by this persona. If a desk earns it, a deterministic executor is built and a
human arms it.
