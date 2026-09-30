# P-0040: Browserless, open a page, wait for a postMessage, screenshot (reopens P-0035)

Run 30 Sep 2026, scheduled nightly, attempt 1 of 3.

## What I ran

`browserless_probe.py`: key read from the Proteus vault through the 1Password SDK (the path that
hung under `op` last night), one POST to Browserless's `/function` endpoint (SFO region) with a
puppeteer function. The page sets up a `message` listener and posts itself a message after 1.5 s;
the function waits for it with `waitForFunction` (10 s cap) and returns the text and a PNG.

## Measured

- HTTP 200, 3.23 s wall from this Mac, 1,628 ms inside the hosted browser (so about 130 ms of work
  beyond the 1.5 s timer).
- The wait resolved (`waited: ok`), text `got: ping from P-0040`, PNG 8,993 bytes (`shot.png`,
  checked by eye: the text is rendered).
- No unit or rate headers on the response, so the unit cost per call is not visible from the API.
  One call made. Unit balance unverified; check the Browserless dashboard if it matters.

## Verdict

Works. A hosted Chrome takes arbitrary puppeteer code from a Python script with no local node or
npm, which are both off the unattended safe list (P-0021 tonight). That makes it the nightly's
only way to drive a real browser. It cannot reach local files, so it does not rescue the two
render probes blocked tonight without first publishing their pages somewhere public.
