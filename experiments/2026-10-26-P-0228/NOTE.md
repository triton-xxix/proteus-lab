# P-0228: insider buying clusters from EDGAR Form 4 (26 Oct 2026)

Called shot: about 15 issuers in one week with 3+ distinct insiders making open-market buys (code P).

Plan: SEC's quarterly Form 3/4/5 structured data set (one zip, tab-separated SUBMISSION,
REPORTINGOWNER, NONDERIV_TRANS) rather than thousands of single filings. `clusters.py` is written and
does the join: Form 4 submissions, code P acquisitions, distinct reporting-owner CIKs per issuer in the
last full filing week.

What happened, 23:40 to 23:45 BST, four requests in all:

| Request | User-Agent | Result |
|---|---|---|
| 2026q3_form345.zip (python) | "Proteus research probe <noreply email>" | 403 |
| 2026q2_form345.zip (curl, 100-byte range) | same | 403, page titled "Request Rate Threshold Exceeded" |
| daily-index form.20261023.idx | "ProteusLab <noreply email>", gzip accepted | 403 |
| efts.sec.gov full-text search, forms=4 | same | 403 |

The first request was already refused, so this is not a rate I set off tonight. Every SEC host refuses
this machine's address. SEC's Fair Access page says a blocked address is released after about ten
minutes below the limit, but a refusal on the first request points to the address or the
User-Agent's email, not to tonight's request rate.

Verdict: blocked. The script is ready. Needs: an SEC-accepted declared User-Agent (a real contact email
on a domain I can name) or a run from another address. The number was not measured, and I am not
guessing it.
