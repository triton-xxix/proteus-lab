// P-0439 toy game: make the folder layout build_single_html.mjs expects, with one of each asset kind.
import fs from 'node:fs'; import path from 'node:path'; import { execFileSync } from 'node:child_process';
import sharp from 'sharp'; import { Document, NodeIO } from '@gltf-transform/core';
const G = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..'); process.chdir(G);
for (const d of ['assets/props', 'assets/tex', 'assets/fx', 'assets/ui', 'assets/sfx', 'assets/music', 'src', 'vendor/three/build']) fs.mkdirSync(d, { recursive: true });
// textures and ui
const noise = (w, h) => { const b = Buffer.alloc(w * h * 3); for (let i = 0; i < b.length; i++) b[i] = (i * 2654435761 >>> 24) & 255; return sharp(b, { raw: { width: w, height: h, channels: 3 } }); };
await noise(2048, 2048).jpeg({ quality: 90 }).toFile('assets/tex/ground.jpg');
await noise(256, 256).jpeg().toFile('assets/fx/ink.jpg');
await noise(512, 128).png().toFile('assets/ui/title.png');
await noise(64, 64).png().toFile('assets/ui/btn.png');
// one prop: a box mesh with 2,400 triangles' worth of a subdivided grid
const doc = new Document(); const buf = doc.createBuffer(); const N = 40; const pos = [], idx = [];
for (let y = 0; y <= N; y++) for (let x = 0; x <= N; x++) pos.push(x / N, Math.sin(x / 3) * Math.cos(y / 3) * 0.1, y / N);
for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const a = y * (N + 1) + x; idx.push(a, a + N + 1, a + 1, a + 1, a + N + 1, a + N + 2); }
const p = doc.createAccessor().setType('VEC3').setArray(new Float32Array(pos)).setBuffer(buf);
const i = doc.createAccessor().setType('SCALAR').setArray(new Uint32Array(idx)).setBuffer(buf);
const mesh = doc.createMesh('grid').addPrimitive(doc.createPrimitive().setAttribute('POSITION', p).setIndices(i));
doc.createScene().addChild(doc.createNode('grid').setMesh(mesh));
await new NodeIO().write('assets/props/grid.glb', doc);
fs.writeFileSync('assets/chars.json', '{}'); fs.writeFileSync('assets/props.json', JSON.stringify({ grid: 'props/grid.glb' }));
// audio
execFileSync('ffmpeg', ['-y', '-v', 'error', '-f', 'lavfi', '-i', 'sine=frequency=440:duration=1', 'assets/sfx/hit.mp3']);
execFileSync('ffmpeg', ['-y', '-v', 'error', '-f', 'lavfi', '-i', 'sine=frequency=220:duration=20', '-b:a', '192k', 'assets/music/theme.mp3']);
// three, vendored the way the build expects
fs.copyFileSync('node_modules/three/build/three.module.js', 'vendor/three/build/three.module.js');
fs.cpSync('node_modules/three/examples/jsm', 'vendor/three/jsm', { recursive: true });
// the game: every asset reached the ways a three.js game usually reaches them
fs.writeFileSync('src/game.js', `import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { MeshoptDecoder } from 'three/addons/libs/meshopt_decoder.module.js';
const r = new THREE.WebGLRenderer(); document.body.appendChild(r.domElement);
const scene = new THREE.Scene(), cam = new THREE.PerspectiveCamera(50, 1, 0.1, 100);
const gl = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
gl.load('assets/props/grid.glb', (g) => scene.add(g.scene));                      // via fetch (FileLoader)
new THREE.TextureLoader().load('assets/tex/ground.jpg', (t) => { scene.background = t; });  // via <img>
fetch('assets/sfx/hit.mp3').then((x) => x.arrayBuffer());                          // via fetch
const music = new Audio('assets/music/theme.mp3');                                 // via <audio>
fetch('assets/chars.json').then((x) => x.json());
r.setAnimationLoop(() => r.render(scene, cam));
`);
fs.writeFileSync('index.html', `<!doctype html><html><head><meta charset="utf-8"><title>toy</title>
<script type="importmap">{"imports":{"three":"./vendor/three/build/three.module.js","three/addons/":"./vendor/three/jsm/"}}</script>
</head><body><img id="logo" src="assets/ui/title.png">
<script type="module">import './src/game.js';</script></body></html>`);
console.log('prep done');
