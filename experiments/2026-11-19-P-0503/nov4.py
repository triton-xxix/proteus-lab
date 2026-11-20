#!/usr/bin/env python3
"""What turned over in Wikipedia's top 1,000 between 3 and 4 Nov 2026? Keyless pageviews API, paced."""
import json, os, re, time, urllib.request
from collections import Counter
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/%04d/%02d/%02d"
SKIP = ("Special:", "Main_Page", "Wikipedia:", "Portal:", "File:", "Help:", "Category:", "Talk:")


def fetch(d):
    req = urllib.request.Request(URL % (d.year, d.month, d.day), headers={"User-Agent": "probe/1.0 (research script)"})
    arts = json.loads(urllib.request.urlopen(req, timeout=30).read())["items"][0]["articles"]
    time.sleep(2)
    return {a["article"]: (a["rank"], a["views"]) for a in arts if not a["article"].startswith(SKIP)}


days = {d: fetch(date(2026, 11, d)) for d in (1, 2, 3, 4, 5, 6)}
s = {d: set(v) for d, v in days.items()}
entered = sorted(s[4] - s[3], key=lambda a: days[4][a][0])
left = sorted(s[3] - s[4], key=lambda a: days[3][a][0])
words = Counter()
for a in entered:
    for w in set(re.findall(r"[A-Za-z]{4,}", a.replace("_", " ").lower())):
        words[w] += 1
pat = re.compile(r"election|senate|governor|congress|mayor|proposition|representatives|ballot|gubernatorial|referendum|midterm", re.I)
out = {"sizes": {d: len(v) for d, v in s.items()},
       "share_kept": {"1to2": round(len(s[1] & s[2]) / len(s[1]), 3), "2to3": round(len(s[2] & s[3]) / len(s[2]), 3),
                      "3to4": round(len(s[3] & s[4]) / len(s[3]), 3), "4to5": round(len(s[4] & s[5]) / len(s[4]), 3),
                      "5to6": round(len(s[5] & s[6]) / len(s[5]), 3)},
       "entered_4nov": len(entered), "left_after_3nov": len(left),
       "entered_also_new_vs_2nov": len([a for a in entered if a not in s[2]]),
       "entered_still_listed_5nov": len([a for a in entered if a in s[5]]),
       "entered_still_listed_6nov": len([a for a in entered if a in s[6]]),
       "left_back_by_5nov": len([a for a in left if a in s[5]]), "left_back_by_6nov": len([a for a in left if a in s[6]]),
       "overlap_5nov_with_2nov": round(len(s[5] & s[2]) / len(s[2]), 3), "overlap_6nov_with_2nov": round(len(s[6] & s[2]) / len(s[2]), 3),
       "overlap_3nov_with_2nov": round(len(s[3] & s[2]) / len(s[2]), 3),
       "entered_matching_election_words": len([a for a in entered if pat.search(a)]),
       "entered_with_a_year": len([a for a in entered if re.search(r"(19|20)\d\d", a)]),
       "common_words_in_entrants": words.most_common(25),
       "top_40_entrants": [[a, days[4][a][0], days[4][a][1]] for a in entered[:40]],
       "top_25_leavers": [[a, days[3][a][0]] for a in left[:25]],
       "views_sum_top": {d: sum(v[1] for v in days[d].values()) for d in days}}
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k not in ("top_25_leavers",)}))
