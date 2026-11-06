# P-0349: is a Smarkets sell-all book a real gap?

Question: tonight's book-sums item found 39 historical books whose bids sum over 100. How much size stands behind one,
does it survive commission, and is it there a minute later?

Method: `depth.py`, read-only, 107 open markets at 23:55Z on 6 Nov 2026, read twice 60 s apart. Nothing was traded.
This is one moment, not the 39 historical books.

- 65 books had a bid on every contract, median sell-all 94.81.
- 1 was over 100: Trump to serve 9+ years by end of 2030, two contracts, sum 101.18, unchanged after 60 s.
- Size at the top of the thinner side: 2.02 units, so the gross gap is 0.024 units. If a unit is a pound, that is 2p.
- It survives a 2% charge on net market profit and fails a 2% charge on all premium. I did not confirm which applies,
  or the quantity's unit, from a Smarkets document.

What it means: the gap on screen is real and it is not a trade. It sat there a minute because it is too small for
anyone to bother, and it pays out only when the market settles, by the end of 2030. My shot (0 to 2 books, under 50
units, none surviving harsh commission) hit.

Not done: only top-of-book size, one night. Bigger locks may have stood behind the 102.1 Texas Senate book on 2 Nov;
my snapshots keep no sizes, so that cannot be known now.
