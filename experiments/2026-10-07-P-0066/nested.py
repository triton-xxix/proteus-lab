"""P-0066: build questions on live Wikidata the way arXiv 2610.06650 describes (named entities replaced
by conditions, uniqueness checked after each step) and count answers, keyless via query.wikidata.org.

For each target: take its item-valued truthy claims, order them by how few items share each one
(capped count), add them one at a time until the target is the only answer. Then take one condition's
value V and replace wd:V with two of V's own conditions (a nested condition), and count again."""
import json, os, sys, time, urllib.parse, urllib.request

EP = "https://query.wikidata.org/sparql"
UA = {"User-Agent": "ProteusProbe/0.1 (https://github.com/triton-xxix/proteus-lab; research probe)",
      "Accept": "application/sparql-results+json"}
CAP = 1001
SKIP_P = {"P31", "P21", "P27", "P1412", "P103", "P1343", "P910", "P1424", "P8017", "P5008", "P2354"}
TARGETS = {"Q7259": "Ada Lovelace", "Q7251": "Alan Turing", "Q42": "Douglas Adams",
           "Q7186": "Marie Curie", "Q80": "Tim Berners-Lee"}
calls = 0


def q(sparql):
    global calls
    calls += 1
    time.sleep(1.0)
    url = EP + "?" + urllib.parse.urlencode({"query": sparql})
    for attempt in range(2):
        try:
            return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read())["results"]["bindings"]
        except Exception as e:
            err = e
            time.sleep(3)
    raise err


def count(patterns):
    body = " ".join(patterns)
    r = q(f"SELECT (COUNT(*) AS ?c) WHERE {{ SELECT DISTINCT ?x WHERE {{ {body} }} LIMIT {CAP} }}")
    return int(r[0]["c"]["value"])


def claims(qid):
    r = q(f"""SELECT ?p ?o ?oLabel WHERE {{ wd:{qid} ?p ?o . ?prop wikibase:directClaim ?p .
              FILTER(STRSTARTS(STR(?o), "http://www.wikidata.org/entity/Q"))
              SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }} }}""")
    out = []
    for b in r:
        p = b["p"]["value"].rsplit("/", 1)[1]
        o = b["o"]["value"].rsplit("/", 1)[1]
        if p not in SKIP_P:
            out.append((p, o, b.get("oLabel", {}).get("value", o)))
    return out


def run(qid, name):
    cs = claims(qid)
    single = []
    for p, o, lab in cs[:25]:
        single.append((count([f"?x wdt:{p} wd:{o} ."]), p, o, lab))
    single.sort()
    chosen, steps = [], []
    for n1, p, o, lab in single:
        if n1 >= CAP and len(chosen) >= 1:
            continue
        chosen.append((p, o, lab))
        n = count([f"?x wdt:{pp} wd:{oo} ." for pp, oo, _ in chosen])
        steps.append({"added": f"{p}={lab}", "alone": n1, "answers": n})
        if n == 1 or len(chosen) == 3:
            break
    # nested: replace the most selective chosen value with two of its own conditions
    nested = None
    if chosen:
        p, o, lab = chosen[0]
        vcs = [c for c in claims(o) if c[0] not in SKIP_P][:12]
        vsingle = sorted((count([f"?v wdt:{pp} wd:{oo} ."]), pp, oo, ll) for pp, oo, ll in vcs)[:2]
        pats = [f"?x wdt:{pp} wd:{oo} ." for pp, oo, _ in chosen[1:]]
        pats.append(f"?x wdt:{p} ?v .")
        pats += [f"?v wdt:{pp} wd:{oo} ." for _, pp, oo, _ in vsingle]
        n = count(pats)
        r = q(f"SELECT DISTINCT ?x WHERE {{ {' '.join(pats)} }} LIMIT 3")
        hit = [b["x"]["value"].rsplit("/", 1)[1] for b in r]
        nested = {"replaced": f"{p}={lab}", "with": [f"{pp}={ll}" for _, pp, _, ll in vsingle],
                  "conditions": len(pats), "answers": n, "target_in_answers": qid in hit, "sample": hit}
    return {"target": qid, "name": name, "item_claims": len(cs), "steps": steps, "nested": nested}


if __name__ == "__main__":
    results = []
    t0 = time.time()
    for qid, name in TARGETS.items():
        try:
            res = run(qid, name)
        except Exception as e:
            res = {"target": qid, "name": name, "error": repr(e)[:200]}
        results.append(res)
        print(json.dumps(res), flush=True)
    summary = {"targets": len(results), "sparql_calls": calls, "seconds": round(time.time() - t0, 1),
               "unique_within_3": sum(1 for r in results if r.get("steps") and r["steps"][-1]["answers"] == 1),
               "nested_unique": sum(1 for r in results if r.get("nested") and r["nested"]["answers"] == 1 and r["nested"]["target_in_answers"])}
    print(json.dumps(summary))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "results.json"), "w") as f:
        json.dump({"summary": summary, "results": results}, f, indent=1)
