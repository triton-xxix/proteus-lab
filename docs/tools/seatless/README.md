# seatless

How many of a UK Parliament petition's UK signatures sit in no constituency? Every petition on
petition.parliament.uk publishes the UK row of `signatures_by_country` and a count per constituency;
the constituency counts add up to less than the UK row. This file fetches petitions, open or archived,
keyless, and reports the gap, the share, and the share by the month each petition opened.

```
python3 seatless.py --ids 300412 241584
python3 seatless.py --parliament 4 --top 400 --floor 10000 --out run.json --csv rows.csv
python3 seatless.py --from run.json
```

Standard library only. `--sleep` spaces requests (0.15 s default). `--from` re-scores a saved run.

First run, 21 Nov 2026, the 400 most-signed petitions of the 2019-24 Parliament: 399 read, 2.36% of
UK signatures in no seat, about 2.3% to 3.9% for petitions opened before December 2021 and 0.5% to
1.0% from February 2022. Size makes no difference. The cause of the step is not known.

From probes P-0516, P-0517 and P-0519. Page: https://triton-xxix.github.io/proteus-lab/tools/seatless/
