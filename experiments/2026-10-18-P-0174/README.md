# P-0174: GenAI for Beginners lesson 08, does the shipped index cluster by video?

Refill source 6 (Microsoft Generative AI for Beginners). The suggested build, a lesson against Ollama, is
blocked here: no Ollama on this Mac (P-0075, P-0124). Lesson 08 ships its embedding index of Microsoft AI
Show transcripts, so the keyless question is whether those vectors carry what the lesson's search relies
on: chunks of the same talk sit nearer each other than chunks of other talks.

Shot (blind, before the file was opened): works at 0.80, same-video nearest neighbour 70 to 90%, chance
under 5%, 1536 dims.

## Method

`nn.py` (run with `sandbox/py312-venv`, numpy 2.3.5): download `embedding_index_3m.json` (49,448,137 bytes,
3.8 s) to `sandbox/p0174/`, normalise the `ada_v2` vectors, take each chunk's nearest other chunk by
cosine, and count same `videoId`. Chance is the same-video share if the neighbour were picked at random.
Second pass drops same-video chunks within 360 s of the chunk (its own and the next window), because
3-minute windows next to each other share words.

## Numbers

- 1409 chunks, 1536 dims, 279 videos, median 5 chunks a video.
- Same-video nearest neighbour: **69.6%**. Chance: **0.4%**. About 170 times chance.
- With adjacent windows excluded: **41.7%**, still about 100 times chance.
- Mean nearest-neighbour cosine 0.908 (the results.json key says median; it is the mean). ada-002's
  cosines bunch high, so a raw threshold of 0.8 would match nearly everything.

## Not done

No query embedding (that needs a key: Azure OpenAI or OpenAI), so the lesson's actual search is not run.
No look at which videos fail to cluster. No comparison against a local embedding model.
