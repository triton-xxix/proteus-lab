# P-0163, EDGAR Form 4 cluster scan (16 Oct 2026)

Question: how many clusters of 3 or more insiders buying on the open market (code P) in one issuer
appeared in the last 30 days, from SEC public data, keyless?

What I ran: `fetch.py` against the SEC Insider Transactions Data Sets (quarterly Form 3/4/5 extracts),
with a User-Agent naming the project and its GitHub URL but no email address.

Result: HTTP 403 on 2026q3 and on 2026q2, so it is not a missing quarter. SEC's fair-access policy asks
every automated client to declare a company name and a contact email in the User-Agent, and refuses
generic agents. Proteus has no mailbox of its own to declare, and I did not borrow anyone's.

Verdict: blocked, on a contact email for SEC's User-Agent rule. The script is ready: with a declared
address it reads the quarter, keeps P-coded rows, groups distinct reporting owners by issuer over the
last 30 days in the file and writes `clusters.csv` and `summary.json`. Note the quarterly file lags:
2026q3 ends 30 Sep, so "the last 30 days" from it is September, not October. A true last-30-days count
needs the daily index plus one XML fetch per Form 4, about 20,000 requests at SEC's 10 a second.
