// Build this folder (a teardown machine) with the kit, output under ./out of this folder.
//   node experiments/2026-11-02-P-0296/build.mjs
process.env.TEARDOWN_OUT = '/Users/triton/PROTEUS/experiments/2026-11-02-P-0296/out';
process.argv = [process.argv[0], 'build.mjs', '/Users/triton/PROTEUS/experiments/2026-11-02-P-0296'];
await import('/Users/triton/PROTEUS/sandbox/teardown/src/teardown-HEAD/sims/build.mjs');
