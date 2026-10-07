#!/usr/bin/env node
// Build the Nolan site into the deploy root.
//   node sites/nolan/build.cjs [--out /Users/triton/PROTEUS/sites/builds/nolan]
// Renders the index (career timeline, film grid) from films.json, the Tenet deep page in both orders,
// and a standard page for every films/<slug>.json present. Copies the engine, page assets and images. No deps.
'use strict';
const fs = require('fs');
const path = require('path');
const { ROOT, esc, readJSON, write, copy, copyDir } = require('./lib/render.cjs');
const { renderTenet } = require('./lib/tenet.cjs');
const { renderFilm } = require('./lib/film.cjs');
const { timeline } = require('./lib/timeline.cjs');
const { glyph } = require('./lib/structure.cjs');

const args = process.argv.slice(2);
const outIdx = args.indexOf('--out');
const OUT = outIdx >= 0 ? path.resolve(args[outIdx + 1]) : path.resolve(ROOT, '..', 'builds', 'nolan');

const films = readJSON('films.json');
const themes = readJSON('themes.json');

function filmData() {
  const d = {};
  for (const f of films.films) {
    const p = path.join(ROOT, 'films', f.slug + '.json');
    if (fs.existsSync(p)) d[f.slug] = JSON.parse(fs.readFileSync(p, 'utf8'));
  }
  return d;
}

function indexPage(data) {
  const sorted = films.films.slice().sort((a, b) => a.year - b.year);
  const rows = sorted.map(f => {
    const deep = f.deep_page && fs.existsSync(path.join(OUT, f.deep_page, 'index.html'));
    const std = !!data[f.slug];
    const link = deep ? `<a class="film__link" href="${f.deep_page}">Walk the timeline</a>${std ? ` · <a class="film__link" href="films/${f.slug}/">Read</a>` : ''}` : (std ? `<a class="film__link" href="films/${f.slug}/">Read</a>` : `<span class="film__soon">coming</span>`);
    const sketch = std && data[f.slug].time_structure && data[f.slug].time_structure.sketch;
    return `<li class="film${deep || std ? ' film--live' : ''}">
      <span class="film__year">${f.year}</span>
      <h2 class="film__title">${esc(f.title)}</h2>
      ${sketch ? glyph(sketch) : ''}
      <p class="film__note">${esc(std ? (data[f.slug].one_line || f.note || '') : (f.note || ''))}</p>
      ${link}
    </li>`;
  }).join('\n');
  const liveCount = films.films.filter(f => (f.deep_page && fs.existsSync(path.join(OUT, f.deep_page, 'index.html'))) || data[f.slug]).length;
  const themeRows = themes.themes.map(t => {
    const dots = sorted.map(f => {
      const has = data[f.slug] && (data[f.slug].themes || []).some(x => x.id === t.id);
      return has ? `<a class="tm__dot tm__dot--on" href="films/${f.slug}/#theme-${t.id}" title="${esc(t.name)} in ${esc(f.title)}"></a>` : `<span class="tm__dot" title="${esc(f.title)}"></span>`;
    }).join('');
    const count = sorted.filter(f => data[f.slug] && (data[f.slug].themes || []).some(x => x.id === t.id)).length;
    return { count, html: `<div class="tm__row"><span class="tm__name">${esc(t.name)}</span><span class="tm__dots">${dots}</span></div>` };
  }).filter(r => r.count > 0).sort((a, b) => b.count - a.count).map(r => r.html).join('');
  return `<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Christopher Nolan, film by film</title>
<meta name="description" content="An unofficial fan site: each of Christopher Nolan's films and how it plays with time, researched from sources by Proteus, an AI explorer.">
<meta name="theme-color" content="#0B0D11">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='6' fill='%230B0D11'/><rect x='4' y='4' width='12' height='24' fill='%23C8463A'/><rect x='16' y='4' width='12' height='24' fill='%233C9AB4'/></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,300..800&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="shared/site.css">
<link rel="stylesheet" href="shared/film.css">
</head>
<body>
<main class="site">
  <header class="site__head">
    <p class="site__kicker">An unofficial fan site</p>
    <h1 class="site__h1">Christopher Nolan, film by film.</h1>
    <p class="site__lede">Thirteen features, each one a different trick with time. Every page is built from sourced research by <a href="https://triton-xxix.github.io/proteus-lab/">Proteus</a>, an AI explorer, one film a night. ${liveCount} of ${films.films.length} live.</p>
  </header>
  <div class="career-wrap">${timeline(films.films, data)}</div>
  <ol class="films">
${rows}
  </ol>
  ${themeRows ? `<section class="tm" aria-label="Themes across the films"><h2 class="site__kicker">Themes, film by film</h2><div class="tm__head"><span></span><span class="tm__dots">${sorted.map(f => `<span class="tm__col" title="${esc(f.title)}">${String(f.year).slice(2)}</span>`).join('')}</span></div>${themeRows}</section>` : ''}
  <footer class="site__foot">
    <p>Not affiliated with Christopher Nolan, Syncopy or Warner Bros. Stills are © their studios and are used for commentary and criticism. Where a film does not state a day, the page says so.</p>
    <p>Data for every page is published as JSON beside it. Research notes and sources live in <a href="https://github.com/triton-xxix/proteus-lab/tree/main/sites/nolan">the repository</a>.</p>
  </footer>
</main>
</body>
</html>`;
}

function build() {
  fs.mkdirSync(OUT, { recursive: true });
  const data = filmData();
  // engine and shared styles
  copy(path.join(ROOT, '..', 'engine', 'scrollcraft.js'), path.join(OUT, 'shared', 'scrollcraft.js'));
  copy(path.join(ROOT, '..', 'engine', 'scrollcraft.css'), path.join(OUT, 'shared', 'scrollcraft.css'));
  copy(path.join(ROOT, 'src', 'site.css'), path.join(OUT, 'shared', 'site.css'));
  copy(path.join(ROOT, 'src', 'film.css'), path.join(OUT, 'shared', 'film.css'));
  // tenet deep page, both orders
  copy(path.join(ROOT, 'tenet', 'page.css'), path.join(OUT, 'tenet', 'page.css'));
  copy(path.join(ROOT, 'tenet', 'page.js'), path.join(OUT, 'tenet', 'page.js'));
  copyDir(path.join(ROOT, 'tenet', 'img'), path.join(OUT, 'tenet', 'img'), (name, isDir) => !(isDir && name === 'raw'));
  write(OUT, 'tenet/index.html', renderTenet('watch', ''));
  write(OUT, 'tenet/world/index.html', renderTenet('world', '../'));
  fs.mkdirSync(path.join(OUT, 'data'), { recursive: true });
  for (const f of ['film.json', 'events.json', 'threads.json']) copy(path.join(ROOT, 'tenet', f), path.join(OUT, 'data', 'tenet-' + f));
  copy(path.join(ROOT, 'films.json'), path.join(OUT, 'data', 'films.json'));
  // standard film pages
  const sorted = films.films.slice().sort((a, b) => a.year - b.year);
  let n = 0;
  for (const f of sorted) {
    const d = data[f.slug];
    if (!d) continue;
    const i = sorted.indexOf(f);
    const prev = sorted.slice(0, i).reverse().find(x => data[x.slug]) || null;
    const next = sorted.slice(i + 1).find(x => data[x.slug]) || null;
    write(OUT, `films/${f.slug}/index.html`, renderFilm(d, f, '../', { prev, next }));
    copy(path.join(ROOT, 'films', f.slug + '.json'), path.join(OUT, 'data', f.slug + '.json'));
    const imgDir = path.join(ROOT, f.slug, 'img');
    if (fs.existsSync(imgDir)) copyDir(imgDir, path.join(OUT, f.slug, 'img'), (name, isDir) => !(isDir && name === 'raw'));
    n++;
  }
  write(OUT, 'index.html', indexPage(data));
  fs.writeFileSync(path.join(OUT, '.nojekyll'), '');
  const live = films.films.filter(f => (f.deep_page && fs.existsSync(path.join(OUT, f.deep_page, 'index.html'))) || data[f.slug]).length;
  fs.writeFileSync(path.join(ROOT, 'site.json'), JSON.stringify({ name: 'Christopher Nolan, film by film', url: films.site_url, live, total: films.films.length, updated: new Date().toISOString().slice(0, 10) }, null, 2) + '\n');
  console.log('built', OUT, 'films', n, 'live', live, 'of', films.films.length);
}

build();
