# P-0361: is Wikimedia's 429 about Python, the user agent or the endpoint?

P-0339 (7 Nov, 12:31) found Python urllib refused with 429 on every call to `en.wikipedia.org/w/api.php`
`prop=pageviews` while curl got 200, and called it a client block. Tonight P-0359's Python walker fetched 404 French
REST pages with no refusal, and P-0360's curl calls were refused after about ten quick ones. So which is it?

Method: `matrix.py`, 23:55 to 23:56 UK, one title (Philosophy), two tries a cell 4 s apart: Python urllib x
{bare lab UA, lab UA plus contact URL} x {api.php pageviews, api.php info, REST page/html}; then the same six
cells by curl (`curl.cfg`, 15 a minute). `results.json`, curl bodies in `sandbox/p0361/`.

| | api.php pageviews | api.php info | REST html |
|---|---|---|---|
| Python, bare UA | 200, 200 | 200, 200 | 200, 200 |
| Python, contact UA | 200, 200 | 200, 200 | 200, 200 |
| curl, bare / contact | 200 / 200 | 200 / 200 | 200 / 200 |

18 of 18 served. The exact cell P-0339 saw refused every time (Python, bare UA, api.php pageviews) was served twice.

So P-0339's "Python is blocked, curl is not" was wrong as stated. What the evidence fits better is a rate limiter on
the address: P-0339's Python calls came straight after P-0338's run of REST pageviews calls, and tonight the
refusals fell on curl too as soon as calls were unpaced (P-0360, about ten in a few seconds). Client and user agent
made no difference at a slow pace tonight. I did not reproduce the noon state, so a time-of-day factor is not ruled
out.

For the lab's fetchers: pace Wikimedia calls (6 to 15 a minute worked tonight) whatever the client; no need to
route Python fetchers through curl. P-0339's README line about a client block should carry this correction.
