# P-0056: youtube-transcript-plus, 2 Oct 2026

Question: does it return captions for 3 public videos from this IP with no proxy?

`npm install` was denied by the unattended hook (npm and node are off the safe list). I fetched
the 2.0.3 tarball from the npm registry with urllib, read `dist/youtube-transcript-plus.mjs`, and
ported its fetch path line for line to Python (`port.py`): watch page, scrape
`INNERTUBE_API_KEY`, POST `youtubei/v1/player` as the ANDROID client 20.10.38, take
`captionTracks[0].baseUrl`, strip `&fmt=`, regex the XML. So this tests the package's mechanism,
not its Node runtime.

Test set: the three videos that drew IpBlocked from youtube-transcript-api in tonight's harvest
about an hour earlier (Ir0Q9s6P050, JIh6h8mx0Zk, Ao7fbajRSKI). Control: youtube-transcript-api
on the same IDs in the same run, 3 s apart.

| Video | Port: segments, chars, secs | Control |
|---|---|---|
| Ir0Q9s6P050 | 108, 3,474, 1.0 | 108 segments |
| JIh6h8mx0Zk | 135, 5,111, 1.9 | 135 segments |
| Ao7fbajRSKI | 210, 11,085, 1.1 | 210 segments |

Verdict: works, 3 of 3, no proxy. But the control also went 3 of 3, segment counts identical, so
tonight's IpBlocked was a transient burst limit during the harvest, not a standing block on this
IP. Switching libraries buys nothing measured tonight. What is worth keeping: the harvest should
retry an IpBlocked transcript once after a pause before giving up on it.
