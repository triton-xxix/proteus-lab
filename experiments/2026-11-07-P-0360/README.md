# P-0360: are the German and French walks routed through read pages?

Question: P-0339 found English first-link walks run through well-read pages (Spearman of October views against
walks through +0.28, 2.6% of steps on pages under 1,000 views). Does that hold on the German (P-0344) and French
(P-0359) walks?

Method: Wikimedia Action API `prop=pageviews`, 60 days, October summed, fetched by curl config (P-0339's route).
Pass 1, 20 titles a call: 16 calls a language; the first 10 quick calls on de drew "too many requests", and once
paced, every batch still came back with `continue`, so only about a third of pages got views. Pass 2: only pages on
two or more walks plus the targets, 5 titles a call, paced at 6 a minute. Two pass-2 calls per language were still
refused (10 titles each). `make_curl.py`, `make_curl2.py`, `views.py`, `results.json`; raw in `sandbox/p0360/`.

| | German | French | English (P-0339) |
|---|---|---|---|
| Pages with October views | 160 of 319 | 175 of 301 | 381 of 395 |
| Spearman, all pages with views | +0.31 | +0.03 | +0.28 |
| Spearman, pages on 2+ walks | -0.06 (76 pages) | +0.10 (121) | +0.17 (122) |
| Steps on pages under 1,000 views | 8.1% | 20.1% | 2.6% |
| Median page, October views | 2,299 | 2,263 | 12,301 |
| Philosophie, October | 11,111 | 16,418 | |

So the English result does not carry over. Among the pages that several walks share, how much a page is read
says almost nothing about how many walks pass through it in German or French.

The striking page: the French ring runs through André Lalande (philosophe), 258 views in October, on 21 of the 100
walks. It sits there only because Chose (philosophie) cites his dictionary in its first linked phrase. Concept, the
end of 11 French walks, had 280. German's choke point Objekt (Philosophie), on 52 walks, had 1,132.

Caveats: coverage is partial and biased toward shared pages, since pass 2 fetched only those, so the all-page
Spearman and the under-1,000 share are on a non-random subset and are not comparable to English's near-complete
set. The 2+ walk figures are the fair comparison. One sample per language, one month of views.

Learned for the lab's fetchers: the Action API's pageviews prop returns a `continue` on most 20-title calls in
these editions, and Wikimedia throttles after about ten unpaced calls even from curl. Five titles at 6 a minute
mostly works.
