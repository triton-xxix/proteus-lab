// The Tenet timeline page: both reading orders from the same data.
//   renderTenet('watch', base)  the film as cut, eight acts, the scroll-craft engine driving it
//   renderTenet('world', base)  the same events in the order they happen, a two-column dossier
// `base` is the relative path from the page to the tenet/ folder ('' for tenet/index.html, '../' for tenet/world/).
'use strict';
const fs = require('fs');
const path = require('path');
const { ROOT, esc, readJSON, jpegSize } = require('./render.cjs');

const film = readJSON('tenet/film.json');
const events = readJSON('tenet/events.json').events;
const threads = readJSON('tenet/threads.json').threads;
const byId = Object.fromEntries(events.map(e => [e.id, e]));
const IMG = path.join(ROOT, 'tenet', 'img');

const FWD = film.colour_code.forward.hex;
const INV = film.colour_code.inverted.hex;

// ---- the acts, in watch order -------------------------------------------------------------
const ACTS = [
  { n: 1, id: 'rule', name: 'The rule', kind: 'hero', span: 1.3, events: [] },
  { n: 2, id: 'entry', name: 'The entry', kind: 'flow', events: ['opera', 'the-test', 'briefing'] },
  { n: 3, id: 'clues', name: 'The clues', kind: 'pin', span: 1.8, events: ['mumbai', 'london', 'vietnam-original', 'oslo-freeport', 'mumbai-turnstile', 'amalfi'] },
  { n: 4, id: 'turn', name: 'The turn', kind: 'flow', events: ['tallinn-highway', 'tallinn-freeport', 'tallinn-turnstile'] },
  { n: 5, id: 'reverse', name: 'The reverse', kind: 'pin', span: 2.0, events: ['tallinn-reversed', 'the-week-back', 'oslo-second-pass'] },
  { n: 6, id: 'plan', name: 'The plan', kind: 'flow', events: ['oslo-priya', 'the-plan', 'ship'] },
  { n: 7, id: 'pincer', name: 'The pincer', kind: 'pin', span: 3.6, events: ['vietnam-return', 'stalsk-pincer', 'hypocentre', 'detonation'] },
  { n: 8, id: 'resolve', name: 'The resolve', kind: 'flow', events: ['the-hill', 'london-coda'] },
];

function actOf(id) {
  return ACTS.find(a => a.events.includes(id));
}

function dayLabel(e) {
  const wt = e.world_time;
  if (wt.status === 'stated' && wt.day === 0) return 'the 14th';
  if (wt.status === 'stated' && wt.day != null) return 'day ' + wt.day;
  return 'day unstated';
}

function figure(e, base, lazy) {
  if (!e.image) return '';
  const big = path.join(IMG, e.image + '.jpg');
  const small = path.join(IMG, e.image + '-800.jpg');
  if (!fs.existsSync(big)) return '';
  const sz = jpegSize(small) || { w: 800, h: 450 };
  const alt = e.image_alt || ('A still from Tenet: ' + e.title.toLowerCase());
  return `<figure class="step__fig"><img src="${base}img/${e.image}-800.jpg" srcset="${base}img/${e.image}-800.jpg 800w, ${base}img/${e.image}.jpg 1600w" sizes="(max-width: 860px) 100vw, 42vw" width="${sz.w}" height="${sz.h}" alt="${esc(alt)}"${lazy ? ' loading="lazy" decoding="async"' : ''}></figure>`;
}

function who(e, dir) {
  const names = { protagonist: 'the Protagonist', neil: 'Neil', kat: 'Kat', sator: 'Sator', priya: 'Priya', ives: 'Ives' };
  const seen = new Set();
  return e.threads.filter(t => t.direction === dir).map(t => names[t.who]).filter(n => !seen.has(n) && seen.add(n)).join(', ');
}

// A forward (red) step. `cue` is a data-sc-cue window for pinned acts, or null for flow.
function stepFwd(e, base, opts) {
  const o = Object.assign({ cue: null, lazy: true, k: 0, actName: null, actN: null }, opts || {});
  const act = actOf(e.id);
  const actName = o.actName || (act ? act.name : '');
  const actN = o.actN || (act ? act.n : '');
  const cueAttr = o.cue ? ` data-sc-cue="${o.cue}"` : '';
  const inAttr = o.cue ? '' : ' data-sc-in data-sc-stagger="70"';
  return `<article class="step step--fwd" id="ev-${e.id}" data-ev="${e.id}" data-watch="${e.watch_order}" data-world="${e.world_order}" data-day="${esc(dayLabel(e))}" data-act="${esc(actName)}" data-actn="${actN}" style="--k:${o.k}">
  <div class="step__cue"${cueAttr}><div class="step__in sc-stack"${inAttr}>
    ${figure(e, base, o.lazy)}
    <p class="step__meta"><span class="step__n" aria-label="Watch order">${e.watch_order}</span><span class="step__loc">${esc(e.location)}</span><span class="step__day">${esc(dayLabel(e))}</span></p>
    <h3 class="step__title">${esc(e.title)}</h3>
    <p class="step__body">${esc(e.what_happens)}</p>
    <p class="step__why">${esc(e.why_it_matters)}</p>
    ${who(e, 'forward') ? `<p class="step__who"><span>Forward:</span> ${esc(who(e, 'forward'))}</p>` : ''}
  </div></div>
</article>`;
}

// The inverted (blue) side of the same event, where it has one.
function stepInv(e, base, opts) {
  if (!e.inverted_side) return '';
  const o = Object.assign({ cue: null, k: 0 }, opts || {});
  const cueAttr = o.cue ? ` data-sc-cue="${o.cue}" data-sc-rise="0"` : '';
  const inAttr = o.cue ? '' : ' data-sc-in data-sc-stagger="70"';
  const w = who(e, 'inverted') || who(e, 'contested');
  return `<article class="step step--inv" data-ev="${e.id}" data-watch="${e.watch_order}" data-world="${e.world_order}" style="--k:${o.k}" aria-label="The inverted side of ${esc(e.title)}">
  <div class="step__cue"${cueAttr}><div class="step__in sc-stack"${inAttr}>
    <p class="step__meta"><span class="step__n">${e.watch_order}</span><span class="step__loc">${esc(e.location)}</span><span class="step__day">${esc(dayLabel(e))}</span></p>
    <p class="step__body step__body--inv">${esc(e.inverted_side)}</p>
    ${w ? `<p class="step__who"><span>Inverted:</span> ${esc(w)}</p>` : ''}
  </div></div>
</article>`;
}

// Cue windows for a pinned act: n steps abutting, with short ramps so two full blocks never sit on top of
// each other for long. The first greets (on screen as the act begins); the last closes at 1 (only the
// page's last act may hold).
function cues(n) {
  const out = [];
  const w = 1 / n;
  const ramp = Math.min(0.05, w * 0.18);
  for (let i = 0; i < n; i++) {
    const a = Math.max(0, i * w - ramp);
    const b = Math.min(1, (i + 1) * w + ramp);
    if (i === 0) out.push(`0 ${b.toFixed(3)} 0 ${ramp.toFixed(3)}`);
    else out.push(`${a.toFixed(3)} ${b.toFixed(3)} ${ramp.toFixed(3)} ${ramp.toFixed(3)}`);
  }
  return out;
}

// ---- act renderers ---------------------------------------------------------------------------
function hero(base) {
  const plate = fs.existsSync(path.join(IMG, 'bullet-glass.jpg'));
  const cutout = fs.existsSync(path.join(IMG, 'mask-cutout.png'));
  const half = (side, rate) => `
    <div class="hero__half hero__half--${side}" aria-hidden="true">
      ${plate ? `<div class="plane plane--plate" data-sc-parallax="${(-1.2 * rate).toFixed(2)}"><img src="${base}img/bullet-glass.jpg" alt="" width="1600" height="900" decoding="async"></div>` : ''}
      ${cutout ? `<div class="plane plane--subject" data-sc-parallax="${(-0.5 * rate).toFixed(2)}"><img src="${base}img/mask-cutout.png" alt="" width="1280" height="720" decoding="async"></div>` : ''}
      <svg class="plane plane--trace" viewBox="0 0 1000 560" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
        <path class="trace" d="M -40 300 C 180 292, 420 288, 640 282 S 900 276, 1040 268" pathLength="1"/>
        <circle class="trace__hole" cx="640" cy="282" r="9"/>
      </svg>
      <div class="plane plane--sill" data-sc-parallax="${(0.6 * rate).toFixed(2)}"></div>
    </div>`;
  return `
<section class="act act--hero" id="act-1" data-sc-act="pin" data-sc-span="1.3" data-act-name="The rule">
  <div data-sc-stage class="stage stage--hero">
    ${half('fwd', 1)}
    ${half('inv', -1)}
    <p class="hero__title" aria-hidden="true"><span>TE</span><span class="hero__pivot">N</span><span>ET</span></p>
    <div class="hero__scrim" aria-hidden="true"></div>
    <div class="hero__copy" data-sc-cue="0 0.86 0">
      <h1 class="hero__h1">A bullet both ways.</h1>
      <p class="hero__lede">Tenet runs forward for an hour and then runs back through itself. This page lets you scroll it in both directions. ${esc(film.anchor.label)} is the only day it names.</p>
      <p class="hero__hint"><a href="#act-2">Start at the opera</a> or <a href="${base}world/">read it in the order it happened</a>.</p>
    </div>
  </div>
</section>`;
}

function columns(fwd, inv, extra) {
  return `<div class="cols">
    <div class="col col--fwd">${fwd}</div>
    <div class="col col--inv">${inv}</div>
    ${extra || ''}
  </div>`;
}

function flowAct(act, base, extra) {
  const evs = act.events.map(id => byId[id]);
  const fwd = evs.map((e, i) => stepFwd(e, base, { k: i })).join('\n');
  const inv = evs.map((e, i) => stepInv(e, base, { k: i })).join('\n');
  return `
<section class="act act--flow act--${act.id} sc-section" id="act-${act.n}" data-sc-act="flow" data-act-name="${esc(act.name)}">
  <div class="sc-wrap wrap">
    <h2 class="act__name"><span class="act__n">${act.n}</span> ${esc(act.name)}</h2>
    ${columns(fwd, inv, extra ? extra(evs) : '')}
  </div>
</section>`;
}

function pinAct(act, base, extra) {
  const evs = act.events.map(id => byId[id]);
  const cw = cues(evs.length);
  const fwd = evs.map((e, i) => stepFwd(e, base, { cue: cw[i], lazy: false, k: i })).join('\n');
  // The blue column reads upwards: later steps sit higher. Cues keep their windows; position does the reading.
  const inv = evs.map((e, i) => stepInv(e, base, { cue: cw[i], k: i })).join('\n');
  return `
<section class="act act--pin act--${act.id}" id="act-${act.n}" data-sc-act="pin" data-sc-span="${act.span}" data-act-name="${esc(act.name)}">
  <div data-sc-stage class="stage stage--${act.id}">
    <h2 class="act__name act__name--pin"><span class="act__n">${act.n}</span> ${esc(act.name)}</h2>
    ${columns(fwd, inv, extra ? extra(evs) : '')}
  </div>
</section>`;
}

// The Sator square, drawn letter by letter from the act's --sc-p.
function square() {
  const rows = film.sator_square.rows;
  let i = 0;
  const cells = rows.map(r => r.split('').map(ch => `<span class="sq__c" style="--i:${i++}">${ch}</span>`).join('')).join('');
  const map = film.sator_square.map.map(m => `<li><b>${esc(m.word)}</b> ${esc(m.is)}</li>`).join('');
  return `<aside class="square" aria-label="The Sator square">
    <div class="sq" role="img" aria-label="${esc(rows.join(' / '))}">${cells}</div>
    <p class="square__note">${esc(film.sator_square.note)}</p>
    <ul class="square__map">${map}</ul>
  </aside>`;
}

// The pincer diagram: scroll is ten minutes. Red descends the world axis, blue climbs it, they cross at five.
function pincerDiagram() {
  const ticks = [];
  for (let m = 0; m <= 10; m++) {
    const y = 40 + m * 48;
    ticks.push(`<line class="pz__tick" x1="150" x2="170" y1="${y}" y2="${y}"/><text class="pz__min" x="178" y="${y + 4}">${m === 0 ? 'minute 0' : m === 10 ? 'minute 10' : m}</text>`);
  }
  return `<div class="pincer" aria-label="The temporal pincer, as a diagram">
    <svg class="pz" viewBox="0 0 320 560" aria-hidden="true">
      <line class="pz__axis" x1="160" x2="160" y1="40" y2="520"/>
      ${ticks.join('')}
      <rect class="pz__building" x="118" y="256" width="84" height="48" rx="3"/>
      <text class="pz__label" x="160" y="286">the building</text>
      <g class="pz__red"><circle r="11" cx="132" cy="40"/><text class="pz__clock pz__clock--red" x="104" y="44" text-anchor="end">10:00</text></g>
      <g class="pz__blue"><circle r="11" cx="188" cy="520"/><text class="pz__clock pz__clock--blue" x="216" y="524">10:00</text></g>
    </svg>
    <p class="pincer__legend"><span class="pincer__red">Red team</span> goes in forward from minute zero. <span class="pincer__blue">Blue team</span> goes in inverted from minute ten. They meet at the building.</p>
    <p class="pincer__clock" aria-live="off">World clock <b class="pincer__world">0:00</b></p>
  </div>`;
}

function colophon(base) {
  const unstated = events.filter(e => e.world_time.status !== 'stated').map(e => `<li><span>${e.watch_order}</span> ${esc(e.title)}${e.world_time.note ? `: <em>${esc(e.world_time.note)}</em>` : ''}</li>`).join('');
  const rules = film.rules.map(r => `<li>${esc(r.rule)}</li>`).join('');
  const sources = [
    ['A1', 'Tenet (film), Wikipedia', 'https://en.wikipedia.org/wiki/Tenet_(film)'],
    ['B1', 'The most confusing moments in Tenet, explained, /Film', 'https://www.slashfilm.com/1563140/most-confusing-moments-in-tenet-explained/'],
    ['B2', 'The entire Tenet timeline explained, Looper', 'https://www.looper.com/769196/the-entire-tenet-timeline-explained/'],
    ['B3', 'The Tenet movie explained, No Film School', 'https://nofilmschool.com/tenet-explained'],
    ['B4', 'Neil’s timeline explained, Den of Geek', 'https://www.denofgeek.com/movies/tenet-robert-pattinson-neil-timeline/'],
  ].map(s => `<li><span>${s[0]}</span> <a href="${s[2]}" rel="noopener">${esc(s[1])}</a></li>`).join('');
  return `<footer class="colophon" id="colophon">
    <div class="colophon__grid">
      <section class="colophon__block">
        <h2 class="colophon__h">The rules the film plays by</h2>
        <ul class="colophon__list">${rules}</ul>
      </section>
      <section class="colophon__block">
        <h2 class="colophon__h">Days the film does not name</h2>
        <p class="colophon__p">One day is named: ${esc(film.anchor.label)}. Two durations are spoken: ${esc(film.durations_stated[0].what.toLowerCase())}, and ${esc(film.durations_stated[1].what.toLowerCase())}. Everything else is an order, not a date.</p>
        <ul class="colophon__list colophon__list--days">${unstated}</ul>
      </section>
      <section class="colophon__block">
        <h2 class="colophon__h">Sources</h2>
        <ul class="colophon__list">${sources}</ul>
        <p class="colophon__p">Every claim on this page is checked against these in <a href="https://github.com/triton-xxix/proteus-lab/tree/main/sites/nolan/tenet/research" rel="noopener">the research notes</a>. Where the film does not state a day, the page says so.</p>
      </section>
      <section class="colophon__block">
        <h2 class="colophon__h">Next</h2>
        <p class="colophon__p">Memento, Inception, Dunkirk and the rest are being researched one film a night. <a href="${base}../">The films</a>.</p>
        <p class="colophon__p colophon__p--small">${esc(film.credit)}</p>
        <p class="colophon__p colophon__p--small">${esc(film.disclaimer)} Built by <a href="https://triton-xxix.github.io/proteus-lab/" rel="noopener">Proteus</a>.</p>
      </section>
    </div>
  </footer>`;
}

function divider(mode, base) {
  const toWorld = mode === 'watch';
  // The watch page's divider is a bespoke fixed stage, so it reports its state to the harness. The world page is a
  // plain document: its scrolling is the change, and it publishes nothing.
  return `<aside class="divider" id="divider"${mode === 'watch' ? ` data-sc-verify-state="watch|rule|50|-"` : ''} aria-label="Forward and inverted">
    <span class="divider__line" aria-hidden="true"><svg class="divider__string" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path d="M 0 50 C 25 40, 75 60, 100 50" pathLength="1"/></svg></span>
    <span class="divider__side divider__side--fwd">Forward</span>
    <span class="divider__side divider__side--inv">Inverted</span>
    <div class="divider__folio" aria-live="polite">
      <span class="folio__act">The rule</span>
      <span class="folio__n"><b class="folio__num">1</b> of ${events.length}, ${mode === 'watch' ? 'watch order' : 'world clock'}</span>
      <span class="folio__day">${esc(film.anchor.label)}</span>
    </div>
    <nav class="divider__modes" aria-label="Reading order">
      <a class="mode${toWorld ? ' mode--on' : ''}" href="${toWorld ? '#top' : base}"${toWorld ? ' aria-current="page"' : ' data-mode-link="watch"'}>Watch order</a>
      <a class="mode${toWorld ? '' : ' mode--on'}" href="${toWorld ? base + 'world/' : '#top'}"${toWorld ? ' data-mode-link="world"' : ' aria-current="page"'}>World clock</a>
    </nav>
    <a class="divider__films" href="${base}../">Films</a>
  </aside>`;
}

function head(title, desc, base, mode) {
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta name="theme-color" content="#0B0D11">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%230B0D11'/><rect x='4' y='4' width='12' height='24' fill='%23C8463A'/><rect x='16' y='4' width='12' height='24' fill='%233C9AB4'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="${base}../shared/scrollcraft.css">
<link rel="stylesheet" href="${base}page.css">
</head>
<body class="mode-${mode}">
<a class="skip" href="#act-2">Skip to the timeline</a>
<span data-sc-progress></span>
<div class="sc-grain" aria-hidden="true"></div>`;
}

function foot(base) {
  return `
<script src="${base}../shared/scrollcraft.js"></script>
<script>ScrollCraft.mount(document.body);</script>
<script src="${base}page.js"></script>
</body>
</html>`;
}

function renderWatch(base) {
  const acts = ACTS.map(a => {
    if (a.kind === 'hero') return hero(base);
    if (a.id === 'plan') return flowAct(a, base, () => square());
    if (a.id === 'pincer') return pinAct(a, base, () => pincerDiagram());
    if (a.id === 'resolve') return flowAct(a, base) .replace('</section>', colophon(base) + '\n</section>');
    return a.kind === 'pin' ? pinAct(a, base) : flowAct(a, base);
  }).join('\n');
  return head('Tenet, both ways: a timeline', 'Every event in Tenet in the order you watch it and the order it happened, forward in red and inverted in blue, with the one day the film names.', base, 'watch')
    + divider('watch', base)
    + `\n<main id="top" class="main">\n${acts}\n</main>` + foot(base);
}

// World clock: the same steps, in world order, grouped by the day they fall on. A flow dossier.
function renderWorld(base) {
  const sorted = events.slice().sort((a, b) => a.world_order - b.world_order);
  const groups = [
    { title: 'The 14th', note: 'The only day the film names. The opera, the yacht in Vietnam and Stalsk-12 all fall on it, and the ship is already at sea, sailing backwards towards it.', test: e => ['opera', 'vietnam-original', 'vietnam-return', 'stalsk-pincer', 'hypocentre', 'detonation', 'the-hill', 'ship'].includes(e.id) },
    { title: 'After the 14th, days unstated', note: 'The Protagonist’s recruitment and first leads. The film gives no dates for any of them.', test: e => ['the-test', 'briefing', 'mumbai', 'london'].includes(e.id) },
    { title: 'Oslo day, about a week before Tallinn', note: 'The freeport job happens once in the world and three times for the Protagonist. The week in the container begins here and runs back towards Tallinn.', test: e => ['oslo-freeport', 'oslo-second-pass', 'oslo-priya', 'the-plan', 'the-week-back'].includes(e.id) },
    { title: 'Between Oslo and Tallinn', note: '', test: e => ['mumbai-turnstile', 'amalfi'].includes(e.id) },
    { title: 'Tallinn day', note: 'The heist, from both directions, and the turnstile at its centre.', test: e => ['tallinn-highway', 'tallinn-reversed', 'tallinn-freeport', 'tallinn-turnstile'].includes(e.id) },
    { title: 'Later, day unstated', note: 'After the 14th, and after Priya’s meeting in Oslo, because she is alive for it.', test: e => ['london-coda'].includes(e.id) },
  ];
  const body = groups.map((g, gi) => {
    const evs = sorted.filter(g.test);
    const fwd = evs.map((e, i) => stepFwd(e, base, { k: i, actName: g.title, actN: gi + 1 })).join('\n');
    const inv = evs.map((e, i) => stepInv(e, base, { k: i })).join('\n');
    return `
<section class="act act--flow act--world sc-section" id="world-${gi + 1}" data-sc-act="flow" data-act-name="${esc(g.title)}">
  <div class="sc-wrap wrap">
    <h2 class="act__name"><span class="act__n">${gi + 1}</span> ${esc(g.title)}</h2>
    ${g.note ? `<p class="act__note">${esc(g.note)}</p>` : ''}
    ${columns(fwd, inv)}
  </div>
</section>`;
  }).join('\n');
  const intro = `
<section class="act act--flow act--worldintro sc-section" id="act-2" data-sc-act="flow" data-act-name="World clock">
  <div class="sc-wrap wrap">
    <div class="sc-stack" data-sc-in data-sc-stagger="70">
      <h1 class="world__h1">Tenet, in the order it happened.</h1>
      <p class="world__lede">The same ${events.length} events as the <a href="${base}">watch order</a>, re-sorted by the world’s clock. The film names one day, the 14th, so the groups below are an order, not a calendar. Red is anyone moving forward through time; blue is anyone inverted.</p>
    </div>
  </div>
</section>`;
  return head('Tenet, in the order it happened', 'Every event in Tenet re-sorted into world order, with the one day the film names first.', base, 'world')
    + divider('world', base)
    + `\n<main id="top" class="main main--world">\n${intro}\n${body}\n<section class="act act--flow act--resolve sc-section" data-sc-act="flow" data-act-name="Sources"><div class="sc-wrap wrap">${colophon(base)}</div></section>\n</main>` + foot(base);
}

function renderTenet(mode, base) {
  return mode === 'world' ? renderWorld(base) : renderWatch(base);
}

module.exports = { renderTenet, ACTS, events, film, threads };
