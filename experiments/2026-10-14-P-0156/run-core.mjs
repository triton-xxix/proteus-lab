// npm test is off the unattended safe list; this does what it does: chdir into the repo and run its
// own scripts/test-core.mjs (which spawns node --test over the core suites).
const repo = process.argv[2];
process.chdir(repo);
await import(`${repo}/scripts/test-core.mjs`);
