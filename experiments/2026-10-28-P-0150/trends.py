"""P-0150: score P-0145's 34 survivors against Google Trends, keyless.

Path A: the explore + multiline widget API (what pytrends wraps), one term per repo
(the repo name, hyphens to spaces), 90 days, rising = mean of last 14 days > 2x mean of the rest.
Stops after 3 refusals in a row. Path B: the public trending RSS (US, GB), does any term appear.
"""
import json, re, sys, time, urllib.parse, urllib.request, http.cookiejar

SRC = '/Users/triton/PROTEUS/experiments/2026-10-14-P-0145/results.json'
OUT = '/Users/triton/PROTEUS/experiments/2026-10-28-P-0150/results.json'
d = json.load(open(SRC))['of_54']
repos = d['survivors_after_owner_age']
sus = set(d['suspicious_slice'])

cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36',
      'Accept-Language': 'en-US,en;q=0.9'}


def get(url):
    try:
        r = op.open(urllib.request.Request(url, headers=UA), timeout=20)
        return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, ''
    except Exception as e:
        return -1, str(e)[:120]


def term(repo):
    return repo.split('/')[1].replace('-', ' ').replace('_', ' ')


res = {'cookie_status': get('https://trends.google.com/trends/explore?geo=&q=test')[0], 'rows': []}
fails = 0
for repo in repos:
    if fails >= 3:
        res['rows'].append({'repo': repo, 'term': term(repo), 'status': 'not tried (3 refusals in a row)'})
        continue
    t = term(repo)
    req = {'comparisonItem': [{'keyword': t, 'geo': '', 'time': 'today 3-m'}], 'category': 0, 'property': ''}
    s, body = get('https://trends.google.com/trends/api/explore?hl=en-US&tz=0&req=' + urllib.parse.quote(json.dumps(req)))
    row = {'repo': repo, 'term': t, 'explore_status': s, 'suspicious': repo in sus}
    if s == 200:
        fails = 0
        w = [x for x in json.loads(body[body.index('{'):])['widgets'] if x['id'] == 'TIMESERIES'][0]
        s2, b2 = get('https://trends.google.com/trends/api/widgetdata/multiline?hl=en-US&tz=0&req='
                     + urllib.parse.quote(json.dumps(w['request'])) + '&token=' + w['token'])
        row['series_status'] = s2
        if s2 == 200:
            pts = json.loads(b2[b2.index('{'):])['default']['timelineData']
            v = [p['value'][0] for p in pts]
            if not v:
                row.update(no_data=True, rising=False)
                res['rows'].append(row)
                time.sleep(2)
                continue
            last, rest = v[-14:], v[:-14]
            ml, mr = sum(last) / len(last), (sum(rest) / len(rest) if rest else 0)
            row.update(last14=round(ml, 1), before=round(mr, 1), rising=ml > 2 * mr and ml > 0)
    else:
        fails += 1
    res['rows'].append(row)
    time.sleep(2)

rss = {}
for geo in ('US', 'GB'):
    s, body = get('https://trends.google.com/trending/rss?geo=' + geo)
    titles = re.findall(r'<title>([^<]+)</title>', body)[1:]
    hits = [t for t in titles for r in repos if term(r).lower() in t.lower() or t.lower() in term(r).lower()]
    rss[geo] = {'status': s, 'n_titles': len(titles), 'hits': hits}
res['rss'] = rss
scored = [r for r in res['rows'] if 'rising' in r]
res['summary'] = {
    'n': len(repos), 'scored': len(scored),
    'rising': sum(r['rising'] for r in scored),
    'rising_suspicious': sum(r['rising'] for r in scored if r['suspicious']),
    'scored_suspicious': sum(1 for r in scored if r['suspicious']),
    'explore_statuses': sorted({str(r.get('explore_status')) for r in res['rows']}),
}
json.dump(res, open(OUT, 'w'), indent=1)
print(json.dumps(res['summary']), json.dumps(rss), 'cookie', res['cookie_status'])
