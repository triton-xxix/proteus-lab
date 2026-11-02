// bootgpt taken apart: the 512-byte boot sector's network, one character per step, every number on screen
// read from the same integer forward pass that picks the character. P-0296: a seed box and a step slider
// take over from the clock; 420 steps cover the whole screen of the v86 boot in P-0294.
import {runSim} from 'teardown-kit/runtime.js';
import {run, vocab, C, H, V} from './net.js';

const N = 420;
const PER_STEP = 0.075;   // seconds of page time per character while nobody has touched the slider

const show = (ch) => (ch === '\n' ? '⏎' : ch === ' ' ? '·' : ch);

runSim(
  {duration: N * PER_STEP + 4, theme: 'light', accent: '#d9480f', hud: {enabled: false}, director: {enabled: false}},
  ({canvas}) => {
    let seed = Number(new URLSearchParams(location.search).get('bootseed')) || 0x9e75;  // P-0294's recovered seed
    let model = run(seed, N);
    let manual = null;
    const expose = () => { window.BOOTGPT = {seed, text: model.text, steps: model.steps.length}; };
    expose();

    const bar = document.createElement('div');
    bar.style.cssText = 'position:fixed;left:12px;right:12px;bottom:12px;display:flex;flex-wrap:wrap;gap:10px;align-items:center;font:14px "JetBrains Mono",monospace;color:#222;z-index:10';
    bar.innerHTML = `<label>seed 0x<input id="bg-seed" size="5" maxlength="4" value="${seed.toString(16)}" style="font:inherit;width:5ch"></label>
      <input id="bg-step" type="range" min="1" max="${N}" value="1" style="flex:1;min-width:120px">
      <button id="bg-play" style="font:inherit">play</button>`;
    document.getElementById('app').appendChild(bar);
    const seedIn = bar.querySelector('#bg-seed'), stepIn = bar.querySelector('#bg-step'), play = bar.querySelector('#bg-play');
    seedIn.addEventListener('change', () => {
      const s = parseInt(seedIn.value, 16);
      if (Number.isFinite(s) && s > 0 && s <= 0xffff) { seed = s | 1; seedIn.value = seed.toString(16); model = run(seed, N); expose(); }
    });
    stepIn.addEventListener('input', () => { manual = Number(stepIn.value) - 1; });
    play.addEventListener('click', () => { manual = null; });

    const g = canvas.getContext('2d');
    const resize = () => {
      canvas.width = innerWidth * devicePixelRatio;
      canvas.height = innerHeight * devicePixelRatio;
      canvas.style.width = innerWidth + 'px';
      canvas.style.height = innerHeight + 'px';
    };
    return {
      resize,
      render(t) {
        const s = manual ?? Math.min(N - 1, Math.floor(t / PER_STEP));
        if (manual === null) stepIn.value = String(s + 1);
        const st = model.steps[s];
        const W = canvas.width, Hh = canvas.height, u = Math.min(W / 1600, Hh / 900);
        g.setTransform(u, 0, 0, u, 0, 0);
        g.fillStyle = '#f6f4ef';
        g.fillRect(0, 0, 1600, 900);
        g.fillStyle = '#222';
        g.font = '600 26px "JetBrains Mono", monospace';
        g.fillText(`bootgpt, seed 0x${seed.toString(16)}, step ${s + 1} of ${N}: 8 chars in, 96 hidden, 64 logits, one char out`, 40, 50);
        g.font = '700 40px "JetBrains Mono", monospace';
        for (let k = 0; k < C; k++) {
          g.strokeStyle = '#999';
          g.strokeRect(40 + k * 60, 80, 52, 60);
          g.fillText(show(vocab[st.ctx[k]]), 52 + k * 60, 125);
        }
        g.font = '400 16px "JetBrains Mono", monospace';
        g.fillText('hidden (Q6, clipped to ±64)', 40, 175);
        for (let j = 0; j < H; j++) {
          const v = st.y[j];
          g.fillStyle = v >= 0 ? '#555' : '#aaa';
          g.fillRect(40 + j * 7.5, 260 - Math.max(0, v) * 1.2, 6, Math.abs(v) * 1.2);
        }
        g.fillStyle = '#222';
        g.fillText('logits (Q8); the accent bar is the pick after LCG noise ×8', 40, 365);
        const mx = Math.max(...st.logits.map(Math.abs), 1);
        const accent = getComputedStyle(document.documentElement).getPropertyValue('--accent').trim() || '#d9480f';
        for (let v = 0; v < V; v++) {
          const x = 40 + v * 23;
          const hgt = (st.logits[v] / mx) * 110;
          g.fillStyle = v === st.pick ? accent : '#888';
          g.fillRect(x, 500 - Math.max(0, hgt), 18, Math.abs(hgt));
          g.fillStyle = v === st.pick ? accent : '#222';
          g.fillText(show(vocab[v]), x + 3, 640);   // labels below the lowest bar (500 + 110 = 610)
        }
        g.fillStyle = '#222';
        g.font = '400 18px "JetBrains Mono", monospace';
        const lines = model.text.slice(0, s + 1).split('\n').slice(-7);
        lines.forEach((l, i) => g.fillText(l.slice(-80), 40, 690 + i * 24));
        return {};
      },
    };
  },
);
