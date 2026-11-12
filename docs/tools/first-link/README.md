# first-link

Follow the first link of English Wikipedia articles and see where they end: Philosophy, a loop, or a
dead end. One standard-library Python file that keeps every path, so the same starts can be walked
again later and the changed first links named.

    python3 first_link.py "Banana"
    python3 first_link.py --random 100 --out walks.json
    python3 first_link.py --recheck walks.json --out again.json

Rule: the first link in the lead paragraphs that is not inside parentheses, not in italics, not in a
hatnote, infobox, table, figure or footnote, and points to another article. Stops on Philosophy, on
a page already visited, on a page with no such link (or a red link), or after 60 hops. The folk rule
varies; a different rule gives different numbers.

No key. About five page fetches per start, 0.05 s apart, with a descriptive User-Agent. Fetch errors
other than 404 are retried twice and counted in the summary, never passed off as dead ends.

Comes from three Proteus probes: the 5 Nov 2026 walk, P-0332 (the same starts on five past dates)
and P-0348 (the same starts one week on). The parser is the 5 Nov one, unchanged, so old path files
stay comparable. Page: https://triton-xxix.github.io/proteus-lab/tools/first-link/
