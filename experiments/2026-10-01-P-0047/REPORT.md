# P-0047: sports-skills' Understat and ClubElo pulls, keyless

Ran 1 Oct 2026, about 23:50 BST. I tested the two upstream endpoints the skill wraps, not the skill
code: if the sources do not answer, the wrapper cannot.

| Call | Result |
|---|---|
| `http://api.clubelo.com/2026-10-01` | HTTP 502, 0 bytes |
| `https://api.clubelo.com/2026-09-30` | no response in 40 s |
| `http://clubelo.com/` (control) | HTTP 301, host is up |
| `https://understat.com/league/EPL/2026` | no response (curl exit 28) |
| `https://understat.com/league/EPL`, browser user agent | no response in 40 s |

GitHub raw over https answered from the same machine ten minutes earlier (P-0046), so outbound
https works in general. So: both data sources failed tonight, and the comparison with the Pitch
ratings never started.

Unknown: whether this is the sources being down, rate limiting of this IP, or this Mac's sandbox
network filter blocking those two hosts. One more attempt on another night tells them apart; if
it fails the same way, the next step is the browser pane in an interactive session.
