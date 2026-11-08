# P-0369: why French Wikipedia's Concept page stops the walks

**Question.** P-0359: 11 of 100 French first-link walks ended on Concept with no link under the rule. Where
is its lead link hiding, and with the rule bent once on that one page, where do those walks end?

**Called shot.** works at 0.65; lead link inside parentheses; 11 of 11 reach Philosophie once bent, all or
none as they share the suffix.

**Method.** `bend.py` fetches the page, lists every article link before the first heading with where it
sits, then walks on from the first three under P-0359's unchanged rule.

**Numbers.** Concept is a disambiguation page, not a stub. Its lead has no link in running text: all 8 links
sit in a bulleted list, and the rule does not read lists. So the parentheses half of my shot was wrong.

| Link taken (order in the list) | Outcome | Hops |
|---|---|---|
| Philosophie (1st) | reaches Philosophie | 0 |
| Concept (philosophie) (2nd) | reaches Philosophie | 1 |
| Concept marketing (3rd) | dead end | 0 |

Bending on either of the first two links takes all 11 stuck walks to Philosophie, which would move P-0359's
arrivals from 53 of 100 to 64 of 100. All 11 share the suffix, so this is one fact counted eleven times.

**What this does not say.** The first bullet here literally is the target, because the page's first listed
sense is the philosophical one. That is an accident of this page's editors, and taking it is close to
cheating. Whether a general "read disambiguation lists" rule helps needs a re-run of the walk, not this one
page. I did not change the rule or re-run P-0359.
