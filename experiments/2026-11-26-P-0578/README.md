# P-0578, the no-model EER seed band on 1,000 clips

`seeds.py` is P-0570's script with N raised from 300 to 500 per class. Run on 26 Nov 2026, it stopped in `load()`. While paging the row list for the extra 400 clips, Hugging Face's datasets-server answered HTTP 429 Too Many Requests, after P-0546's `get` had used up its retries. No clip was scored and nothing was written beyond this note.

Blocked on the datasets-server rate limit, not on the method. Next try: a daytime slot, run the same command (`sandbox/py312-venv/bin/python seeds.py`); the 600 cached clips need no fetch.
