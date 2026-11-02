// Build the published bootgpt teardown machine (P-0296 plus the Workshop's portrait layout) with the kit.
//   node /Users/triton/PROTEUS/sites/bootgpt/build.mjs
process.env.TEARDOWN_OUT = '/Users/triton/PROTEUS/sites/bootgpt/out';
process.argv = [process.argv[0], 'build.mjs', '/Users/triton/PROTEUS/sites/bootgpt'];
await import('/Users/triton/PROTEUS/sandbox/teardown/src/teardown-HEAD/sims/build.mjs');
