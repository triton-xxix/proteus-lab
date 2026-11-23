# P-0550, safe-anything offline scan of PROTEUS (23 Nov 2026, nightly)

Question (harvest H-0747): how many real findings does an offline scan of PROTEUS and its agent settings produce?

Not run. What I checked, keyless, from the GitHub API:
- Repo created 22 Nov 2026, 481 stars a day later, release v1.0.2 published 22 Nov 21:56Z by GitHub Actions.
- Assets: prebuilt binaries (aarch64 and x86_64 macOS, Linux, Windows), about 1.9 to 2.1 MB each, with a SHA256SUMS file. Download counts 11 to 95.

Why blocked: the only quick path is executing a prebuilt binary from a one-day-old repository, and a checksum from the same release only proves the file is the one they uploaded, not that it is safe. Running files from untrusted sources is outside what I do (charter, Claude Code's own rule), and this Mac carries the whole project, the hook and keys in 1Password. Building from source needs a Rust toolchain I have not got, and would run the same unreviewed code.

Needs: an interactive session to decide whether to build it from reviewed source, or a throwaway VM.

Verdict: blocked.
