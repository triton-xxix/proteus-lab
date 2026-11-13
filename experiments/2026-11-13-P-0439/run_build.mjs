// chdir into the toy game, then run the skill's packager unchanged (copied to tools/build.mjs so node_modules resolve)
import path from 'node:path';
const G = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..'); process.chdir(G);
const t0 = Date.now(); await import('./build.mjs'); console.log('build seconds', ((Date.now() - t0) / 1000).toFixed(1));
