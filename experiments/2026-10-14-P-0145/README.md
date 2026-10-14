# P-0145: new-term-radar night two

14 Oct 2026, Trials, about 12:40Z. Follows P-0142 (13 Oct: 54 GitHub repos under 14 days old averaging
200+ stars a day; a quarter from one org, a visible slice looking star-farmed).

**Question.** Re-run the rule, cap one repo per owner, drop forks, check the suspicious slice for star
farming, diff Hugging Face trending against 13 Oct. How many of the 54 survive?

**Called shot.** works at 0.65; 30 of the 54 survive.

## Method

`radar2.py`: same keyless GitHub search as P-0142 (`created:>=2026-09-30 stars:>=200`, sorted by stars),
then for each of the 54: still 200+ a day tonight; not a fork; one repo per owner (the best stars-per-day
repo stays). The suspicious slice is a keyword match on the name and description (pc, port, mobile, gta,
driver, nsfw, release, bloodborne, d2r, crack, free, download, apk) or no language, plus two controls from
the clean top (storytold/photocraft, openai/math).

The planned stargazer check (first 100 `starred_at` times, five sampled stargazer account ages) failed:
`GET /repos/{o}/{r}/stargazers` returns **401 Unauthorized unauthenticated**, with both the star+json and
the plain media type (tested with curl at 12:40Z; `/users/{login}` still answers keyless). The twelve
failed calls still cost core quota. `owner_age.py` is the fallback: the repo owner's account age,
followers and public repo count, flag under 60 days. A weaker signal and a different one; the note says so.

## Numbers

Of the 54 from 13 Oct:

| step | count | dropped |
|---|---|---|
| still 200+ a day tonight | 48 | 4 not in tonight's search (CopilotKit/OpenDots, shader-effects-inc/shaders, omlahore/RemoveMacAI, nykooi1/vibe-wise: aged past 14 days, renamed or gone, not checked which), 2 fell below 200 (HelixDB/helix-foundry, wesbos/photo-frame-dashboard) |
| not a fork | 48 | 0 |
| one repo per owner | 36 | 12, all storytold (photocraft stays at 4,277 a day) |
| owner account under 60 days | **34** | nullmoth/nvidia-macos-driver (owner 19 days old, 4 repos), overdriveps5/overdrive-releases (owner 2 days old, 1 repo) |

The other eight in the suspicious slice have owners 256 to 3,006 days old; the two controls are
organisations 2,110 and 4,029 days old. So the owner-age proxy clears most of the slice that looked farmed
by name. That is not evidence the stars are real; it says the owners are not throwaways.

Tonight's own set: 53 flagged, 0 forks, 41 after the owner cap, 5 new since last night (CoolkHz/gptibo,
HeyPuter/everything, deeplethe/solid-glass, outcrawlai/scout, solana-classic/solana-classic).

Hugging Face trending top 50: 48 of 50 kept from 13 Oct, 2 entered (fishaudio/drama-3,
openbmb/MiniCPM-V-4.7-35B-A3B-gguf), 2 left. The list barely moves night to night, so a daily diff is a
two-name signal at most.

Calls: 3 search pages, 12 failed stargazer calls, 12 user calls, 1 HF call; core remaining 32 of 60.

## What it says about the claim

With an owner cap and a fork filter the radar's nightly list is 41 names, not 54, and the cap alone does
most of the work. Whether the 34 survivors are "new AI names" is the repo's own 14-day Google Trends
scoring step, which nobody has run yet; the data to run it on 27 Oct is in results.json. The stargazer
farm check the first night asked for needs a GitHub token (even read-only), so it is closed keyless.

## Not done

Stargazer account age or star timing (401). Why the 4 left the search. The Trends scoring (queued, due
27 Oct).
