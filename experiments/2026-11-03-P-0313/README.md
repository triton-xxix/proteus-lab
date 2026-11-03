# P-0313 HackerTV premise: do YouTube links in recent HN comments still resolve?

HackerTV (harvest H-0524) builds a video channel from YouTube links posted in Hacker News comments. The question for tonight: what share
of those links still resolve through YouTube oEmbed, keyless?

`check.py`: HN Algolia `search_by_date`, comments matching "youtube.com" and "youtu.be", three pages each (600 comments, 31 Oct 09:42Z to
3 Nov 22:48Z). Comment text is HTML-escaped (`&#x2F;`), so the first run found 0 ids until it was unescaped. 578 unique ids; the
first 150 were checked against oEmbed, one a second.

Result: 149 of 150 returned 200 (0.993); 1 returned 401 (private or embedding disabled). No 429 from oEmbed at one call a second,
twenty minutes after the captions endpoint had 429'd me (P-0312).

Verdict: works. Fresh HN links almost all resolve, so a HackerTV-style feed loses about 1 in 150 at the oEmbed step. The number says
nothing about link rot over years: every comment here is under four days old. That would be the deepen: the same check on comments
from 2016 and 2021.
