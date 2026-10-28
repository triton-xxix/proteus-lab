# P-0246: is Google's Business Profile Q&A API still listed?

28 Oct 2026, nightly probe loop, keyless curl only.

| check | result |
|---|---|
| Reference page developers.google.com/my-business/reference/qanda/rest | 200, 61 KB, still lists 8 methods (questions create/delete/list/patch, answers delete/list/upsert), no deprecation word on the page |
| Sunset dates page (content/sunset-dates) | "My Business Q&A API was discontinued on November 3, 2025"; support ended 2025-09-15, replacement: None; Q&A notification types also gone |
| Discovery doc mybusinessqanda.googleapis.com/$discovery/rest?version=v1 | 404 |
| Control: Business Information API discovery doc, same form | 200, 85 KB |
| Unauthenticated GET mybusinessqanda.googleapis.com/v1/locations/1/questions | 404 (a live Google API answers 401/403 without a key) |

Verdict: works, as a check. The answer is yes, the reference still lists it, but the API is gone:
discontinued 3 Nov 2025 with no replacement, and the host returns 404 where a live API returns its
discovery doc. Anyone building GBP Q&A automation from the reference page would be building on a dead
endpoint. Files: the three HTML pages and both JSON bodies beside this note.
