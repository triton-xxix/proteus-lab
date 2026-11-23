# P-0551, open-artifact local daemon and PDF export (23 Nov 2026, nightly)

Question (harvest H-0752): does the local daemon serve a hand-written deck folder and export it to PDF without an account?

Not run. Checked keyless:
- `package.json` on main: a private npm workspace (`packages/*`, `plugins/dsh`), Node >= 22.18 (this Mac has 25.6.0). The daemon is not a published package here; it has to be built with `npm run build` (`scripts/build.mjs`, esbuild), and esbuild is in `allowScripts`, so it expects its install script to run.
- Repo created 17 Nov 2026, six days old, 435 stars.

Why blocked in a scheduled run: the unattended hook allows `npm ci|install --ignore-scripts` only, so esbuild's binary never lands and `npm run build` is not on the safe list; I would also be running a six-day-old codebase's build and daemon unreviewed, which is the same untrusted-code line P-0550 stopped at tonight. PDF export from HTML slides very likely needs a headless browser, which this run cannot drive (no browser pane in the nightly).

Needs: an interactive session that reads the build script, runs the build with scripts on, and opens the page.

Verdict: blocked.
