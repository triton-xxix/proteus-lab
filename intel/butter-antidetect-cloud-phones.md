# Butter, and antidetect cloud phones for multi-account posting

Date: 2026-10-10. Status: researched (public sources and the vault's 24 Sep verdict line in SEEN.md; nothing run).

## What it is
Butter (hellobutter.io) sells "one video, many variants, many accounts": it renders variants of a
clip and posts each one from a separate social account. The rendering is ordinary templating. The
grey part is the posting. By the vault's 24 Sep reading of Butter's own help page, each account
sits on its own GeeLark cloud phone, a rented Android instance in a data centre with a spoofed
device identity, described by the vendor as indistinguishable from organic activity. Cloud phones
are the mobile cousin of antidetect browsers: one fake, persistent "device" per account so the
platform cannot link the accounts by hardware.

## What it costs
Butter: not checked tonight (the vault line found no founder, no legal entity and a terms page
that 404s). Cloud phones are sold per device per month or per minute by several vendors, often
bundled with antidetect browsers (Multilogin sells both). GeeLark's site did not resolve from here
tonight (DNS failure), so I have no price of my own. I paid nothing.

## How it works
At the level a defender needs: a phone app reports dozens of device signals (model, build, GPU and
renderer, sensors, battery and telemetry behaviour, network and SIM details) and the platform
hashes them into a device identity. Ordinary desktop Android emulators give themselves away on
those signals and on attestation (Google's Play Integrity classes most emulators as high risk). A
cloud phone runs Android natively on server hardware and rewrites the identity per instance, with a
residential or mobile proxy for the IP. Each account gets one instance for life, so it looks like
one person on one phone.

## How it is detected
- **Shared hardware underneath.** Many instances run on the same racks. Vendors who sell physical
  phone farms say this leaves instance profiles clustered on GPU, kernel and timing traits. That is
  a competitor's claim and unverified, but it is the right place to look: the spoof covers the
  identifiers, not the silicon.
- **Attestation.** Hardware-backed key attestation and Play Integrity's strong verdicts are hard to
  fake from a server; a platform that requires them for posting cuts the cheap end out.
- **Behaviour, not device.** Many accounts posting near-identical variants of one asset, on a
  schedule, with similar captions and no organic browsing, is visible at content level whatever the
  device says. Instagram's account-level review over 30 days (from 30 Apr 2026) and YouTube's
  inauthentic-content demonetisation (from Jul 2025) both judge this layer.
- **Proxy tells.** Residential proxy pools are resold and reused; IP reputation and ASN mix across
  a cluster of accounts give them away.
- **What does not work.** Checking one identifier at a time. The whole product is per-identifier
  plausibility; the tell is the population, not the individual.

Vendor material on detection rates (for example "most emulators fail within days") is marketing
from one side or the other. I found nothing a platform has published on how it catches cloud
phones, and say so rather than guess.

## What I ran
Nothing. One web search and one failed fetch (geelark.com, DNS not found) on 10 Oct 2026, inside
the nightly run.

## What I did not run, and why
Renting a cloud phone or signing up to Butter would mean creating an account and evading a
platform's controls on a system Luke does not own: both over the line in the charter. A useful
version I could run is a defender's one: measure, on a phone I own, which of the published device
signals an app can read, and compare with a public emulator image. Not done.

## Sources
- SEEN.md line, 2026-09-24, Butter (vault verdict, which cites Butter's help page). Read 10 Oct.
- Multilogin, "Cloud phones explained" and "Cloud phones vs mobile emulators" (vendor). Search result, 10 Oct.
  https://multiloginx.helpjuice.com/en_US/cloud-phones/cloud-phones-explained
  https://multilogin.com/blog/cloud-phones-vs-mobile-emulators/
- Scroogefrog, "Cloud phone, physical phone, or emulator? 2026" (vendor). 10 Oct.
  https://blog.scroogefrog.com/2026/07/cloud-phone-physical-phone-or-emulator-2026-device-selection-guide-for-multi-account-operations/
- Conbersa, "Real devices vs cloud phones" (vendor of physical devices). 10 Oct.
  https://www.conbersa.ai/learn/real-devices-vs-cloud-phones-distribution
- Shield Labs, "How to detect anti-detect browsers in 2026" (detection vendor). 10 Oct.
  https://shieldlabs.ai/blog/how-to-detect-anti-detect-browsers
