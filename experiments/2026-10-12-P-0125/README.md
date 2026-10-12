# P-0125: exempt `_child` from the stray-image rule

**Question.** The Inception research child (10 Oct) failed `sites/nolan/check.py film` on one line only:
"image reference outside images[]", caused by a backdrop path in its own `_child.notes`. `_child` is popped by
`nolan.py ingest` before anything is built, so it can never reach a page. Does excluding `_child` from that
rule pass the committed digest with nothing else changing, while still catching a real stray image?

**Called shot.** works at 0.60; 0 fails on the parked digest once `_child` is exempt.

**Method.** `run.py` execs the live `check.py` and a copy with the blob line changed to skip `images` and
`_child`, then runs both on three digests: the HEAD copy (as the child wrote it), the working copy (note cleaned
by hand on 10 Oct), and a control (HEAD plus `poster.jpg` planted in `one_line`).

**Numbers** (`result.json`):

| digest | live | patched |
|---|---|---|
| head | 1 fail (stray image), 0 warn | 0 fail, 0 warn |
| work | 0 fail, 0 warn | 0 fail, 0 warn |
| ctrl | 1 fail (stray image) | 1 fail (stray image) |

Measured 0 against the shot's 0. The fail set otherwise is identical (empty), and the control shows the rule
still bites outside `_child`.

**Done.** The one-line patch is now in `sites/nolan/check.py`.

**Not done.** Inception is still `parked` in `films.json`; I did not unpark it or re-run ingest. That is the
nightly's step 5f job, and unparking needs a registry edit the nightly should own.
