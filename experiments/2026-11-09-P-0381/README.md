# P-0381: roblox-studio-mcp, does the repo hold what its README claims? (9 Nov 2026)

Read-only, through GitHub's API, raw text and the npm registry. Nothing was downloaded from the repo's link, cloned or run.
The README tells its reader to download an archive from a telegra.ph page, extract it, run `ProjectFiles.exe` and
"inject the script". That is the repo's text; I did not follow it and did not open the link.

| The README says | What is there |
|---|---|
| A Node.js and TypeScript server | No `.ts`, no `package.json`. Five files: `.gitignore`, `LICENSE`, `README.md`, `main.py` (164 bytes), `helpers.py` (97 bytes) |
| `npx -y roblox-studio-mcp` | npm returns not found for that name on 9 Nov |
| A Lua Studio plugin | None in the tree |
| See `CONTRIBUTING.md` | No such file |

`main.py` imports `build` from a `utils` module that the repo does not contain, so by reading it the file cannot run as it stands.
GitHub's numbers: created and last pushed 9 Nov 2026 08:58Z, 6 KB, 281 stars and 215 forks about 15 hours later. Star timestamps
need a login, so I cannot show the burst, only the totals.

Verdict: broken as an MCP server, because there is no server here. The tree, the mismatch and the one binary download route fit
the lure pattern the harvest child described. I have not analysed the archive, so what it does is unknown, and calling it malware
would be an inference. Detection cues for the intel lane: stars and forks out of proportion to a same-day 6 KB repo,
a README stack that disagrees with the files, install steps that bypass the package manager the same page recommends,
and an "inject" step nothing about an MCP server would need.
