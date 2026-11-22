# P-0535 fast-anything scan: does the profiler rank a planted hot function first?

Nightly 2026-11-22, harvest item gh:el4cteo/fast-anything (repo created 21 Nov 2026, 1,842 stars on 22 Nov).

## What I checked

npm registry metadata for `@el4cteo/fast-anything@0.7.0` (keyless, `registry.npmjs.org/.../latest`):

- the package is a 4-file, 11 KB JavaScript shim (`bin/fast-anything.js`);
- the work is done by a prebuilt native binary pulled in as an optional dependency per platform
  (`fast-anything-darwin-x64`, `-darwin-arm64`, `-linux-x64`, `-linux-arm64`, `-win32-x64`, all 0.7.0);
- the other install route is `cargo install`, which compiles and runs the same day-old source.

## Verdict: blocked

Not run. The scan step needs that binary to execute, and a native binary from a repository one day
old is an untrusted file in the charter's sense; an unattended run cannot vet it. The planted-hotspot
test itself is ready to write (a 40-line Python script with one O(n^2) function and two cheap ones;
pass if `scan` ranks the O(n^2) one first).

Needs: an interactive session to read the source and decide whether to build it from a pinned commit.
