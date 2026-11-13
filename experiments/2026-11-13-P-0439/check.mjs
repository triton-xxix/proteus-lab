// P-0439: does dist/wusuo.html make any request? Run its inline shim with a recording fetch, then replay
// each asset load the toy game makes, by the route three.js / the DOM actually uses for it.
import fs from 'node:fs'; import path from 'node:path';
const G = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');
const html = fs.readFileSync(path.join(G, 'dist/wusuo.html'), 'utf8');
const shim = html.match(/<script>(window\.__A=[\s\S]*?)<\/script>/)[1];
const net = []; const realFetch = (u) => { net.push(String(u).slice(0, 60)); return Promise.resolve({ ok: true }); };
globalThis.window = { fetch: realFetch }; globalThis.Response = class { constructor(b, o) { this.status = o.status; } };
new Function(shim)();
const A = window.__A; const keys = Object.keys(A);
const out = { html_bytes: Buffer.byteLength(html), asset_keys: keys.length, keys };
// routes: three's FileLoader (GLTFLoader) calls fetch; TextureLoader uses an <img>; new Audio() uses <audio>
const loads = [
  ['assets/props/grid.glb', 'fetch'], ['assets/sfx/hit.mp3', 'fetch'], ['assets/chars.json', 'fetch'],
  ['assets/tex/ground.jpg', 'img'], ['assets/music/theme.mp3', 'audio'],
];
out.loads = [];
for (const [u, route] of loads) {
  net.length = 0;
  if (route === 'fetch') { await window.fetch(u); out.loads.push({ u, route, in_bundle: !!A[u], network: net.filter((x) => !x.startsWith('data:')).length }); }
  else out.loads.push({ u, route, in_bundle: !!A[u], network: 1, why: 'the shim wraps fetch only; an element src is requested as written' });
}
// src= / url( references left in the HTML outside data: URLs and the shim's own map
const body = html.replace(/window\.__A=\{[\s\S]*?\};/, '');
out.stray_src = [...body.matchAll(/(?:src|href)=["'](?!data:)([^"']+)["']/g)].map((m) => m[1]);
out.js_asset_strings = [...new Set([...body.matchAll(/["'`](assets\/[\w\/.-]+)["'`]/g)].map((m) => m[1]))];
// does three's TextureLoader in the bundle go through fetch? look for ImageLoader's createElementNS('img')
out.bundle_imageloader_uses_img = /createElementNS\([^)]*"img"\)/.test(body) || /createElementNS\("http:\/\/www\.w3\.org\/1999\/xhtml","img"\)/.test(body);
console.log(JSON.stringify(out, null, 1));
fs.writeFileSync('/Users/triton/PROTEUS/experiments/2026-11-13-P-0439/results.json', JSON.stringify(out, null, 1));
