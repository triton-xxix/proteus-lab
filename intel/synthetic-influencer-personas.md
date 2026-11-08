# Synthetic influencer personas sold as "undetectable", and how they are caught

Date: 2026-11-07. Status: researched, public sources only, nothing generated, posted or run. Seed: EasyInfluencers.ai (SEEN.md, 26 Sep 2026).

## What it is
A class of vendor that sells an AI-generated person rather than a tool: one face, one voice, one
posting persona, kept consistent across stills, reels and captions so it reads as an ordinary human
creator. EasyInfluencers.ai is the example I saw. Its headline was that none of these people exist,
and its answer to detection was consistency of appearance. The product is the fake person. The
neighbours are Eromify (companion images, `intel/eromify-ai-companion-funnels.md`) and Butter (the
antidetect cloud phones that post them, `intel/butter-antidetect-cloud-phones.md`).

## What it costs
EasyInfluencers.ai published no price, company, founder or country when I looked on 26 Sep 2026.
The category sells by subscription or done-for-you packages, pushed through affiliate reels. I paid
nothing; no SPEND.md line.

## How it works
At the level a defender needs: a reference set of images fixes one identity; image and video models
are conditioned on it so every post shows the same face; a scripted caption voice and a posting
calendar make the account look lived in. The value claimed is that the persona passes as a person.
Distribution, which is where most detection happens, is either the buyer's own phone or an
automation layer of the Butter kind.

## How it is detected
- **Provenance metadata.** Meta labels content "AI info" when it finds C2PA or IPTC "AI generated"
  signals or the poster discloses (renamed from "Made with AI" in July 2024). Weak on its own:
  metadata strips on re-encode and screenshot, and tools outside C2PA write none.
- **Self-disclosure and profile labels.** Platforms ask for an AI label on realistic synthetic
  media; one secondary source reports an Instagram label for AI-run profiles with reduced reach for
  unlabelled ones. I could not find Meta's own announcement, so that is unverified.
- **Account-level behaviour.** Over a 30-day window (Instagram since 30 Apr 2026, per the Butter
  write-up): posting cadence too regular, engagement that arrives in bursts, follower graphs that
  overlap other personas from the same vendor, device and network fingerprints shared across
  accounts. These catch the farm better than the face.
- **The face itself.** Consistency is the tell the vendor sells as a strength: identical bone
  structure and skin under every light, no ageing, no bad days, backgrounds that never repeat a
  real place twice. Reverse image search on backgrounds and props finds stock and generated sets.
- **Regulation, the strongest lever in the UK.** No AI-specific labelling rule exists in the CAP
  Code (ASA spokesperson, June 2026), but the existing rules bite in full: an ad must be obviously
  an ad, must not mislead, and a trader posing as a consumer is banned outright under DMCC Act 2024
  Schedule 20 practice 25, with the CMA fining directly since April 2025. The ASA's June 2026
  guidance on AI content and deepfakes says the tool used changes nothing. The ASA has treated an
  AI video of a real footballer as it would the real one despite a parody label (Sept 2025), and
  banned a gambling ad whose AI character looked under 25 (published 16 Sep 2026, verify on
  asa.org.uk). New CAP and CMA influencer guidance in October 2026 adds that some platforms require
  AI use to be disclosed.

What does not work: watermark-only detection, since most of the output never carried one, and
judging by image artefacts alone, since current models rarely leave the old hand and text faults.

## What I ran
Two public web searches on 7 Nov 2026 and a re-read of my own 26 Sep SEEN.md entry. No vendor
page fetched tonight, nothing generated.

## What I did not run, and why
No account, no trial, no generation of a persona, no posting. Signing up would mean an account and
a card, both off limits, and building a test persona to see if it passes would be exactly the
evasion the write-up is meant to catch. The Instagram AI-profile label and the Midnite ruling are
secondary-source claims I have not confirmed at the primary source.

## Sources
Read 7 Nov 2026 unless stated.
- SEEN.md entry, EasyInfluencers.ai, 26 Sep 2026.
- Lewis Silkin, "ASA warns on AI-generated content and deepfakes", 18 Jun 2026: https://lewissilkin.com/en/insights/2026/06/18/asa-warns-on-ai-generated-content-and-deepfakes-102n4o1
- Lewis Silkin, new influencer guidance from the ASA, CAP and CMA, 23 Oct 2026: https://www.lewissilkin.com/insights/2026/10/23/new-influencer-guidance-from-the-asa-cap-and-cma-what-has-changed-and-what-to-d-102o6ar
- Taipei Times (Guardian reporting), 22 Jun 2026: https://www.taipeitimes.com/News/world/archives/2026/06/22/2003859535
- Foot Anstey, Marketing Matters, September 2025: https://www.footanstey.com/our-insights/articles-news/marketing-matters-review-of-september-2025/
- Gaming.net on the Midnite ruling (secondary, unverified): https://www.gaming.net/uk-ad-watchdog-bans-midnite-tiktok-ad-over-under-25-ai-character/
- Pasquale Pillitteri on Instagram AI-profile labels (secondary, unverified): https://pasqualepillitteri.it/en/news/13823/instagram-label-ai-generated-profiles-fake-influencers
- Lilach Bullock on the AI info label: https://www.lilachbullock.com/why-instagram-ai-info-label/
