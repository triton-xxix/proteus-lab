// Build bootgpt-teardown with the teardown kit without writing into the working directory:
// set TEARDOWN_OUT before the kit's build script reads it.
//   node experiments/2026-11-02-P-0295/build.mjs
process.env.TEARDOWN_OUT = '/Users/triton/PROTEUS/experiments/2026-11-02-P-0295/out';
process.argv = [process.argv[0], 'build.mjs', '/Users/triton/PROTEUS/experiments/2026-11-02-P-0295/bootgpt-teardown'];
await import('/Users/triton/PROTEUS/sandbox/teardown/src/teardown-HEAD/sims/build.mjs');
