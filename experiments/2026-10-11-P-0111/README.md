# P-0111: Korean pre-listing chatter on DCInside, 11 Oct 2026

Called shot (before the run): the source works keyless, no case/control gap shows, and the short
common tickers are mostly noise.

**Source.** DCInside coin gallery `bitcoins_new1`, title+body search, keyless, no login. Search runs over
10,000-post chunks (`search_pos`) and every row carries an exact KST timestamp, so dated windows can be
measured. About 1,450 posts a day (pos 9,160,000 on 11 Feb, 9,511,564 tonight). About 7 s a request,
207 requests in 460 s, 0 errors.

**Design.** The nine case/control pairs from `../2026-10-09-prelisting/data/xmention_pairs.json`,
windows as in `xmentions.py` (A days -28 to -15, B days -14 to -1). Chunk positions were interpolated
from three bisected anchors with two chunks of margin each side; every pair's scanned range was checked
to cover both windows (all nine did).

**Result** (`dc-result.json`). Real tickers barely appear: ICP 0 then 1, CHIP, PROS, BLEND, CHESS,
RDNT, BOME, SENT and ZBT were all zero in both windows. The only big counts are common words (CC 60 then
40, AI 53 then 40, CAP 40 then 20). Those are noise, and they fell before listing anyway. Median growth
was case 0.5 against control 0.0, and the case grew more in 4 of 9 pairs: no signal. Korean posters
name coins in Hangul (e.g. 인터넷컴퓨터 for ICP), so ticker search under-counts. A Korean-name test
would need a hand-made name map.

**Caveat.** The scan reads at most 4 result pages a chunk and stops when a page holds fewer than 50 rows.
If DCInside pages hold fewer than 50 search rows, the common-word counts are understated. That doesn't
change the zero rows.

`result.json` is the first run, which broke on `search_pos=-0` (every range collapsed to the newest
chunk), kept as a record.
