// Phase 2 check: the letters island, one full letter journey, the tracer, the map piece.
// Run: python3 tools/serve.py app/www &  then  node tools/test-phase2.mjs <screenshot dir>
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const OUT = process.argv[2] || '.';
const URL = 'http://localhost:8765/index.html';
const b = await chromium.launch();
const step = pg => pg.evaluate(() => [...document.querySelectorAll('.screen')].find(s => !s.hidden).dataset.step);
const next = async pg => { await pg.click('#nextBtn'); await pg.waitForTimeout(500); };
const fails = [];
const check = (ok, what) => { if (!ok) fails.push(what); console.log(ok ? '  ok ' : '  FAIL', what); };

// client coordinates of the current tracer stroke (sampled from the svg on the page)
const strokePts = (pg, k) => pg.evaluate(k => {
  const svg = document.querySelector('#trSvg'), m = svg.getScreenCTM();
  const el = svg.querySelectorAll('.tr-road, .tr-road-dot')[k];
  const toC = (x, y) => { const p = svg.createSVGPoint(); p.x = x; p.y = y; const q = p.matrixTransform(m); return [q.x, q.y]; };
  if (el.tagName === 'circle') return [toC(+el.getAttribute('cx'), +el.getAttribute('cy'))];
  const n = el.getTotalLength(), out = [];
  for (let t = 0; t <= n; t += 1) { const q = el.getPointAtLength(t); out.push(toC(q.x, q.y)); }
  const e = el.getPointAtLength(n); out.push(toC(e.x, e.y));
  return out;
}, k);

for (const [tag, vp] of [['m', { width: 400, height: 860 }], ['d', { width: 1280, height: 860 }]]) {
  console.log('viewport', tag);
  const pg = await b.newPage({ viewport: vp, deviceScaleFactor: 1 });
  const errs = [];
  pg.on('pageerror', e => errs.push(e.message));
  pg.on('console', m => { if (m.type() === 'error' && !/404|Failed to load/.test(m.text())) errs.push(m.text()); });
  await pg.goto(URL); await pg.evaluate(() => localStorage.clear()); await pg.goto(URL); await pg.waitForTimeout(900);

  // home → letters island
  await pg.click('[data-isle="0"]'); await pg.waitForTimeout(300);
  check(await step(pg) === '16', 'island 0 opens the Arabic page');
  await pg.click('.pbanner'); await pg.waitForTimeout(700);
  check(await step(pg) === '50', 'banner opens the letters island');
  const st = await pg.$$eval('.pst', els => els.map(e => [e.querySelector('.l').textContent, e.className]));
  check(st.length === 28, '28 stations: ' + st.length);
  check(st[0][0] === 'م' && st[1][0] === 'ب', 'book order starts م ب: ' + st.slice(0, 4).map(x => x[0]).join(' '));
  check(st[0][1].includes('cur') && st[1][1].includes('locked'), 'first station current, second locked');
  await pg.evaluate(() => window.scrollTo(0, 0));
  await pg.screenshot({ path: `${OUT}/p2-${tag}-island.png`, fullPage: tag === 'm' });
  await pg.click('.pst[data-pst="1"]'); await pg.waitForTimeout(300);
  check(await step(pg) === '50', 'a locked station stays closed');

  // journey: meet
  await pg.click('.pst[data-pst="0"]', { force: true }); await pg.waitForTimeout(600);
  check(await step(pg) === '1', 'station opens the meet stage');
  check((await pg.textContent('#learnLike')).includes('مثل'), 'the "letter like word" card');
  check(await pg.$$eval('#progress span', s => s.length) === 7, 'seven stage icons');
  await pg.screenshot({ path: `${OUT}/p2-${tag}-meet.png` });

  // trace: a slip, then two slips show Biko, then the right way
  await next(pg);
  check(await step(pg) === '3', 'trace stage');
  await pg.waitForTimeout(300);
  let pts = await strokePts(pg, 0);
  await pg.mouse.move(...pts[0]); await pg.mouse.down();
  await pg.mouse.move(pts[0][0] + 150, pts[0][1] + 150, { steps: 6 }); await pg.mouse.up();
  check(/no/.test(await pg.getAttribute('#ex2Fb', 'class')), 'leaving the road is a slip');
  await pg.mouse.move(...pts[0]); await pg.mouse.down();
  await pg.mouse.move(pts[0][0] - 160, pts[0][1] - 160, { steps: 6 }); await pg.mouse.up();
  await pg.waitForTimeout(900);
  check(await pg.evaluate(() => [...document.querySelectorAll('#trSvg svg')].some(s => s.style.display !== 'none')), 'after two slips Biko shows the way');
  await pg.screenshot({ path: `${OUT}/p2-${tag}-trace-demo.png` });
  await pg.waitForTimeout(4200);
  const nStrokes = await pg.$$eval('#trSvg .tr-road, #trSvg .tr-road-dot', e => e.length);
  for (let k = 0; k < nStrokes; k++) {
    pts = await strokePts(pg, k);
    await pg.mouse.move(...pts[0]); await pg.mouse.down();
    for (const p of pts) await pg.mouse.move(...p);
    await pg.mouse.up(); await pg.waitForTimeout(150);
  }
  await pg.waitForTimeout(300);
  check(!(await pg.isDisabled('#nextBtn')), 'tracing all strokes finishes the stage');
  await pg.screenshot({ path: `${OUT}/p2-${tag}-trace-done.png` });

  // underwater fishing
  await next(pg);
  check(await step(pg) === '8', 'fishing stage');
  check(await pg.$('#fishField.deep .sea-deco .sub') !== null, 'underwater scene with the submarine');
  await pg.waitForTimeout(400);
  await pg.screenshot({ path: `${OUT}/p2-${tag}-fish.png` });
  for (let t = 0; t < 120 && await pg.isHidden('#fishDone'); t++) {
    await pg.evaluate(() => {
      const f = [...document.querySelectorAll('#fishField .float-item:not(.got)')].find(e => e.querySelector('.lt').textContent[0] === document.querySelector('.target-letter').textContent[0]);
      if (f) f.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
    });
    await pg.waitForTimeout(150);
  }
  check(await pg.isVisible('#fishDone'), 'six fish caught');

  // pictures and words
  await next(pg);
  check(await step(pg) === '2', 'pictures stage');
  for (let r = 0; r < 3; r++) {
    await pg.waitForTimeout(200);
    const n = await pg.$$eval('#ex1Pics .chip', e => e.length);
    for (let k = 0; k < n; k++) {
      const ok = await pg.evaluate(k => { const c = document.querySelectorAll('#ex1Pics .chip')[k]; c.click(); return c.classList.contains('is-ok'); }, k);
      if (ok) break;
      await pg.waitForTimeout(120);
    }
    await pg.waitForTimeout(1800);
  }
  check(!(await pg.isDisabled('#nextBtn')), 'pictures stage done');

  // memory: remember what each card shows
  await next(pg);
  check(await step(pg) === '10', 'memory stage');
  const seen = {};
  for (let t = 0; t < 40 && await pg.isHidden('#memDone'); t++) {
    const cards = await pg.$$eval('#memGrid .card', e => e.map((c, i) => ({ i, done: c.classList.contains('matched') })));
    const open = cards.filter(c => !c.done).map(c => c.i);
    if (open.length < 2) { await pg.waitForTimeout(500); continue; }
    const known = Object.entries(seen).filter(([i]) => open.includes(+i));
    let pair = null;
    for (const [i, w] of known) { const j = known.find(([j2, w2]) => j2 !== i && w2 === w); if (j) { pair = [+i, +j[0]]; break; } }
    const flip = async i => { await pg.click(`#memGrid .card >> nth=${i}`); await pg.waitForTimeout(120); return pg.getAttribute(`#memGrid .card >> nth=${i}`, 'aria-label'); };
    if (pair) { await flip(pair[0]); await flip(pair[1]); delete seen[pair[0]]; delete seen[pair[1]]; await pg.waitForTimeout(500); continue; }
    const unk = open.filter(i => !(i in seen));
    const a = unk[0]; const wa = await flip(a); seen[a] = wa;
    const m = Object.entries(seen).find(([j, w]) => +j !== a && w === wa);
    if (m) { await flip(+m[0]); delete seen[a]; delete seen[m[0]]; await pg.waitForTimeout(500); continue; }
    const bb = unk[1] ?? open.find(i => i !== a); const wb = await flip(bb); seen[bb] = wb;
    if (wb === wa) { delete seen[a]; delete seen[bb]; }
    await pg.waitForTimeout(1300);
  }
  check(await pg.isVisible('#memDone'), 'memory done');

  // the letter check: a wrong answer, then the hint, then right
  await next(pg);
  check(await step(pg) === '51', 'letter check stage');
  await pg.waitForTimeout(300);
  await pg.screenshot({ path: `${OUT}/p2-${tag}-check.png` });
  let hinted = false;
  for (let q = 0; q < 3; q++) {
    for (let k = 0; k < 3; k++) {
      const r = await pg.evaluate(k => { const c = document.querySelectorAll('#lqOpts .chip')[k]; if (c.classList.contains('off')) return 'off'; c.click(); return c.classList.contains('is-ok') ? 'ok' : 'no'; }, k);
      if (r === 'ok') break;
      if (await pg.$('#lqOpts .chip.whint')) hinted = true;
      await pg.waitForTimeout(150);
    }
    await pg.waitForTimeout(1700);
  }
  check(!(await pg.isDisabled('#nextBtn')), 'letter check done');
  check(await pg.$$eval('#lqOpts .chip', e => e.length) === 3, 'three options');

  // result: a map piece and the next station
  await next(pg);
  check(await step(pg) === '6', 'result screen');
  check(await pg.isVisible('#endMap') && (await pg.textContent('#endMap h3')).includes('قطعة جديدة'), 'a new map piece');
  check((await pg.textContent('#endNext')).includes('الباء'), 'next station is ب');
  await pg.waitForTimeout(600);
  await pg.screenshot({ path: `${OUT}/p2-${tag}-end.png`, fullPage: true });
  await pg.click('#menuBtn'); await pg.waitForTimeout(600);
  const st2 = await pg.$$eval('.pst', els => els.slice(0, 3).map(e => e.className));
  check(st2[0].includes('done') && st2[1].includes('cur') && st2[2].includes('locked'), 'island updated: ' + st2.join(' | '));
  check((await pg.textContent('#pathMapNote')).includes('1 من 28'), 'map shows 1 of 28');

  // parents can open every station
  await pg.click('#homeBtn'); await pg.waitForTimeout(300); await pg.click('#toParents'); await pg.waitForTimeout(200);
  const gate = await pg.evaluate(() => { const t = document.querySelector('#wdlgBox span').textContent.match(/(\d+) \+ (\d+)/); return +t[1] + +t[2]; });
  await pg.click(`[data-pg="${gate}"]`); await pg.waitForTimeout(300);
  await pg.check('#pUnlock');
  await pg.click('#homeBtn'); await pg.waitForTimeout(200);
  await pg.click('[data-isle="0"]'); await pg.waitForTimeout(300); await pg.click('.pbanner'); await pg.waitForTimeout(500);
  check(await pg.$$eval('.pst.locked', e => e.length) === 0, 'unlock opens all stations');
  // today's mission goes to the next station of the path
  await pg.click('#homeBtn'); await pg.waitForTimeout(200); await pg.click('#whPlay', { force: true }); await pg.waitForTimeout(500);
  check((await pg.textContent('#bigLetter')) === 'ب', 'today\'s mission opens ب');
  check(await pg.evaluate(() => document.documentElement.scrollWidth) <= vp.width, 'no sideways scroll');
  check(errs.length === 0, 'no page errors ' + JSON.stringify(errs));
  if (hinted) console.log('  (hint seen in the check)');
  await pg.close();
}
await b.close();
console.log(fails.length ? `${fails.length} FAILED` : 'ALL PASSED');
process.exit(fails.length ? 1 : 0);
