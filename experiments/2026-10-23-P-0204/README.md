# P-0204: Octocrawl's keyless hosted scrape against a plain fetch

Nightly probe, 23 Oct 2026, from harvest H-0377 (77777R7/Octocrawl, AGPL server, 2 stars, pushed the same
day). The claim: readable Markdown from public pages for agents, keyless over HTTP at 20 pages a day, with
a reason whenever a scrape falls short.

## Called shot

works at 0.55; Markdown keeps 90 percent or more of the plain-fetch words on 3 of 3 pages; risk that the
hosted endpoint wants a key. Commit 7be6497.

## Method

`scrape_test.py`. Discovery: GET on `/`, `/openapi.json`, `/v1` and `/docs` of `api.octocrawl.dev` all
answer 403 with a JSON error naming the two routes that are served (`POST /v1/scrape`, `POST /v1/map`)
and an agent hint; that is the whole public surface, keyless. Then three pages, each fetched plainly with
urllib (tags stripped, script, style, noscript and svg dropped) and scraped with
`{"url": ..., "formats": ["markdown"]}`. Recall is the share of the plain text's distinct words (letters and
digits, 3 or more characters) present in the Markdown. The Markdown files are saved beside this README.

## Numbers

| page | plain words | Markdown chars | recall | scrape time |
|---|---|---|---|---|
| en.wikipedia.org/wiki/HTTP_402 | 1,495 | 65,493 | 90.2% | 4.3 s |
| docs.python.org/3/library/json.html | 698 | 33,326 | 92.7% | 1.9 s |
| gov.uk/bank-holidays | 283 | 18,473 | 36.7% | 2.0 s |

## Reading

Two of three pages clear 90 percent. The third does not, and it is the measure's fault, not the tool's:
gov.uk's content is tables of dates and weekdays with few distinct words, so the plain fetch's 283 words are
mostly site chrome. The 179 "missing" words are `accessibility`, `cookies`, `copyright`, `departments`,
`consultations` and their kind, and the Markdown holds every bank-holiday table for England and Wales,
Scotland and Northern Ireland in full, 104 of its 109 distinct words found in the plain text. A scraper
that drops the chrome is doing its job; a word-recall test against the raw page punishes exactly that.
The shot's number (3 of 3) therefore missed while the verdict word held.

Latency 1.9 to 4.3 s a page, no key, and every non-route answers with a reason and a hint, which matches
the README's "failures come back with a reason". The `markdown` field sat where the Firecrawl-style
request shape expects it, so the shim claim holds for the one shape tried.

## Not done

No JavaScript-only page, no blocked page (the fixture server is local-only), no `/v1/map`, no structured
fields. 3 of the day's 20 keyless pages used; 17 left for anyone who wants the browser-lane question.
