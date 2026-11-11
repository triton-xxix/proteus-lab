# P-0408: key discovery by value overlap v column name, Northwind and Sakila

Trials, 11 Nov 2026. Refill source 145. Follows P-0397 (Chinook only).

**Question.** P-0397 got 9% precision for "every child value exists in the parent key" and 9 of 10
declared keys found by column name on Chinook, a tidy teaching database. Do those two numbers hold on
two more public samples?

**Shot.** works at 0.70: full value overlap precision under 20 percent on both; same-column-name
recall at least 0.8 on both, with at least one false positive by name on Sakila.

**Method.** `two.py`, P-0397's rules unchanged. `two.py fetch` downloads `northwind.db`
(jpwhite3/northwind-SQLite3, 24.7 MB) and `sakila_master.db` (bradleygrant/sakila-sqlite3, 5.8 MB) as
data into their own folders under `sandbox/` (not kept in git); `two.py score` opens them read-only.
Candidates are every integer column against every other table's single-column integer key. Truth is
the declared foreign keys. One change from `overlap.py`: a key declared without a parent column, or
with the parent table in a different case, is resolved to the parent's primary key.

**Numbers** (results.json), Chinook from P-0397 beside them:

| | Chinook | Northwind | Sakila |
|---|---|---|---|
| tables | 11 | 13 | 16 |
| candidate joins | 218 | 125 | 436 |
| declared keys among them (of all declared) | 10 (11) | 8 (13) | 20 (22) |
| full value overlap, flagged | 110 | 41 | 236 |
| of those, accidents | 100 | 33 | 216 |
| **full overlap precision** | 0.09 | 0.195 | 0.085 |
| full overlap, child not its own key, precision | 0.15 | 0.308 | 0.115 |
| **same column name: recall** | 0.90 | 0.875 (7 of 8) | 0.95 (19 of 20) |
| same column name: precision | 1.00 | 1.00 | 0.826 (4 false) |
| overlap and same name together: precision, recall | 1.00, 0.90 | 1.00, 0.875 | 1.00, 0.95 |

**Reading.**

- Both numbers hold. Value overlap alone is right between 1 time in 12 and 1 in 5. The name finds
  7 of 8 and 19 of 20.
- The misses are role names again: `Orders.ShipVia` to `Shippers.ShipperID`, and
  `store.manager_staff_id` to `staff.staff_id`. Same failure as Chinook's `SupportRepId`. Three
  databases, three misses, all one kind.
- Sakila gives the first false positives by name: four `film_id` columns against `film_text.film_id`,
  a search table with the same key name and no declared link. `film_text` is empty in this copy, so
  the overlap is 0 and the two rules together throw them out. Name and overlap together were 100%
  precise on all three databases; neither alone was.

**Caveats.**

- Integer single-column keys only. Northwind has 5 of 13 declared keys outside that: text ids
  (`CustomerID`), a composite bridge table and a same-table key. So "7 of 8" is 7 of 13 of the whole
  schema. A real tool has to handle text keys before any of this matters.
- Two Sakila keys fell outside the candidates: `film.original_language_id` (all null) and
  `film_actor.actor_id`, which I have not explained (probably `actor`'s key type). Not chased.
- Still teaching databases. Truth is the declared keys only.

**Not done.** The auto-ontology-mcp tool P-0397 was about is still not run; that stays blocked on an
attended session.
