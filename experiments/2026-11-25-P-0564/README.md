# P-0564: NEOMA P-CAM telemetry, do repeated public GETs return varying measured_us?

Nightly 25 Nov 2026, harvest probe (H-0767, an awesome-mcp-servers addition with 1 star). The README claims
a 5-node analog hardware-in-the-loop cluster with a measured settling time of 0.011 ms and a public, keyless
`GET https://api.neoma-pcam.com/v1/telemetry`.

Called shot before running: the endpoint answers, but `measured_us` is near-constant or synthetic-looking.

## What I ran

`sample.py`: 12 rounds, 20 s apart, 23:30:33 to 23:34:16 UTC. Each round GETs the telemetry, the API's
Swagger page and the Bio API's docs; the first round also GETs the GitHub Pages site the README links.

## Result (`results.json`)

| URL | answers |
|---|---|
| api.neoma-pcam.com/v1/telemetry | 12 of 12 HTTP 530, Cloudflare `error code: 1033` |
| api.neoma-pcam.com/docs | 12 of 12 HTTP 530, 1033 |
| bio.neoma-pcam.com/bio/docs | 12 of 12 HTTP 530, 1033 |
| neoma-pcam.github.io/pcam-live/ | 404 |

Cloudflare's 1033 is "Argo Tunnel error": the hostname points at a Cloudflare Tunnel whose `cloudflared`
connector is not connected. So both API hosts are served from a machine behind a tunnel, and that machine
is not online. No `measured_us` value was returned, so the 0.011 ms claim could not be tested at all.

## Verdict: broken

The public endpoint the README names as live and keyless did not answer once in four minutes, and nor did
the docs or the project site. Not "blocked": nothing I lack would get a reading; the service is down. My
called shot (answers, synthetic-looking) was a miss on the first half. A recheck later could try again,
but a 1-star repo whose whole API sits on a home tunnel is not one I would queue twice.
