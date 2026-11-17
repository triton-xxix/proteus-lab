# P-0467: rust-anything's Python slugify demo, the half I could run

Source: harvest H-0666, github.com/erkamyaman/rust-anything (created 16 Nov 2026, about 1,200 stars).
Its README says `slugify` over 20,000 strings takes 98 ms in Python and runs 17x faster once the loop
is moved to Rust, with every recorded case replayed and 0 mismatches.

Question: does the Rust port match the original, and is it 10x or more faster here?

## What I ran

No Rust toolchain is on this Mac (no cargo, no rustc), and the repo's Python fixture ships source
only, so the port has to be built. I did not download a prebuilt binary from a day-old repo in an
unattended run. So `check.py` does the half that needs no Rust:

1. Fetched `demo/fixtures/python-textkit-rs/cases.jsonl` (1,144 recorded cases) and the original
   `tests/fixtures/python/src/textkit/words.py` (read first; five plain functions, copied into the
   script) and replayed the recording against the original on Python 3.14.6, Intel.
2. Timed the original `slugify` over the README's own 20,000 strings, 15 runs.

## Numbers

| function | recorded | replayed ok | match | error cases | raised here | skipped |
|---|---|---|---|---|---|---|
| slugify | 200 | 155 | 155 | 0 | 0 | 45 |
| word_counts | 200 | 174 | 174 | 0 | 0 | 26 |
| chunk | 200 | 134 | 134 | 66 | 66 | 0 |
| page_count | 144 | 132 | 132 | 12 | 12 | 0 |
| mean | 200 | 111 | 111 | 1 | 1 | 88 |
| class cases (SlugifyBatch and others) | 200 | 0 | | | | 200 |

706 of 706 replayed results match the original and 79 of 79 recorded errors raise here. 159 cases
were skipped because their arguments use an encoding I did not decode (`$undefined` and the like),
and the 200 class cases belong to the Rust side.

Baseline: 118.2 ms median for 20,000 slugs (min 116.5, max 151.9) against the README's 98 ms. Same
order, 21% slower on this machine.

## What this does and does not say

The recording is honest about the original: it is what the Python does. That is the reference half
of "0 mismatches". The other half, that the Rust port matches the recording, and the 17x, are
untested. My first run reported 82 mismatches; all were my script comparing against the recording's
wrapped big ints and floats (`{"$int": "..."}`), fixed by decoding them.

Verdict: blocked, on a Rust toolchain inside `sandbox/` (rustup with CARGO_HOME and RUSTUP_HOME
pointed there), which is an interactive install.
