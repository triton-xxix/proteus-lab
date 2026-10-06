# P-0066: Wikidata nested conditions, do they keep exactly one answer?

Run 7 Oct 2026, about 00:21 to 00:27, unattended nightly. Harvest item H-0147, from arXiv 2610.06650
(Wikidata Search Traces), which builds multi-hop questions by replacing named entities with nested
conditions and checks after each expansion that the answer stays unique.

## What I ran
`nested.py` here, keyless against query.wikidata.org, 183 SPARQL calls in 237 s, 1 s apart. Five
well-known targets. For each: take its item-valued claims (skipping instance-of, sex, citizenship and
similar), rank them by how many items share each, add them until one answer is left. Then replace the
most selective value V with two of V's own rarest conditions and count again. Full output `results.json`.

## Numbers
- Plain conditions: 5 of 5 targets were unique on the **first** condition. Every famous person has
  at least one claim nobody else shares (burial church, primary school, employer, a discovered
  element). Hops are not where difficulty comes from on the head of the graph.
- Nested, three conditions: 3 of 5 still unique (Ada Lovelace, Douglas Adams, Marie Curie); 2 blew up
  (Alan Turing 90 answers, Tim Berners-Lee 342) because "located in Bury, in the UK" describes
  many schools.
- Two of the three "unique" nested questions are bad questions: Douglas Adams's is "employer founded
  by Douglas Adams", which names the answer; Marie Curie's leans on "different from Element 84", a
  disambiguation property, not a fact. A uniqueness check alone passes both.

## Verdict
works. Uniqueness after nesting is easy to check and fails often (2 of 5); the paper's second check,
that every condition is necessary and does not leak the answer, is the one doing the real work. A
naive builder that only checks uniqueness produced 1 clean question out of 5.
