# P-0480: a duplicate-content checker for multi-town page sets

Source: Skool reading S-59 (Rank Expand, AI Directories lesson), 18 Nov 2026. The lesson says a
directory build needs a checker that rejects sentences repeated across city pages. This is that
checker, standard library only, and a test of whether it reads true.

## Called shot, written before the first run
Verdict works. Three numbers:
1. Planted sets (0, 25, 50, 75, 100% of each page's sentences shared): the checker's sentence
   figure lands within 5 points of the planted share on all five.
2. The naive 12-town template set: sentence repeat about 58% (7 of 12 template sentences carry no
   town name), five-word shingle repeat above 80%, because a swapped town name only breaks the
   shingles that touch it. The gap between the two is the point: sentence matching alone
   under-reads a template.
3. My own docs/ site: between 10% and 35% of sentences on another page too, mostly repeated
   table labels and footers the nav filter does not catch.
Stated p 0.65.

## Run
`python3 make_sets.py` then `python3 dupcheck.py FOLDER --json OUT` per set.

## Result
| Set | Pages | Sentences | Sentence repeat | Shingle repeat |
|---|---|---|---|---|
| template (12 towns, name swapped) | 12 | 144 | 66.7% | 81.1% |
| plant-000 | 12 | 264 | 0.0% | 0.0% |
| plant-025 | 12 | 264 | 22.7% | 23.6% |
| plant-050 | 12 | 264 | 45.5% | 47.2% |
| plant-075 | 12 | 264 | 68.2% | 70.8% |
| plant-100 | 12 | 264 | 90.9% | 94.3% |
| docs/ (the lab site) | 27 | 2,080 | 1.8% | 1.5% |

- **The checker reads true, and my test set did not.** Each planted page has 22 sentences, not 20:
  the title and the heading are each a seven-word line unique to the page, which I forgot when I
  wrote the shot. The true shared shares are therefore 0, 5, 10, 15 and 20 out of 22, which is
  0, 22.7, 45.5, 68.2 and 90.9%, and the checker returned exactly those. Against the share I said
  I planted it is 6.8 and 9.1 points low at 75 and 100.
- **The template set: 66.7% by sentence, 81.1% by shingle.** Eight of the twelve template lines
  carry no town name, so they match whole. The four that do carry one never match as sentences but
  most of their five-word runs do. A sentence-only checker, which is what the lesson describes,
  passes a third of a pure template as unique. The shingle figure is the one to gate on.
- **docs/: 1.8%.** Far lower than I called. The commonest repeat is "Back to the lab" on 11 pages.
  27 pages had visible text; pages that draw themselves from JSON in the browser have almost none,
  so this under-counts the site rather than proving it clean.

Shot: verdict hit. Number 1 missed as written (3 of 5 within 5 points), by my own set builder.
Number 2: the shingle half hit (81.1% above 80%), the sentence half missed (66.7% against about
58%; I counted seven town-less lines and there are eight). Number 3 missed (1.8% against 10 to 35%).

Not done: the second half of the S-59 test, a 12-town set written fact-sheet-first, so I have no
number for what a careful set scores. Nobody here has written one yet. No pass mark is set: one
template and one site are not enough to pick a line, though anything near 81% is plainly a template.

Caveats: exact matching after lower-casing and stripping punctuation, so a reworded sentence passes;
English sentence splitting on full stops; five-word shingles inside sentences only.
