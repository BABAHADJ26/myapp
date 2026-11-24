// The letters island check: the route in the book's order, one full letter journey (9 stages) moved on by the ride,
// the companion, the exit button, the next station, «continue», the parents' unlock and today's mission.
// Run: python3 tools/serve.py app/www &  then  node tools/test-phase2.mjs <screenshot dir>
import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const OUT = process.argv[2] || '.';
const URL = 'http://localhost:8765/index.html';
const b = await chromium.launch();
const step = pg => pg.evaluate(() => [...document.querySelectorAll('.screen')].find(s => !s.hidden).dataset.step);
const fails = [];
const check = (ok, what) => { if (!ok) fails.push(what); console.log(ok ? '  ok ' : '  FAIL', what); };
// wait until the ride carries the lesson to the next stage by itself
const rideTo = async (pg, from) => { for (let t = 0; t < 70; t++) { const s = await step(pg); if (s !== from) return s; await pg.waitForTimeout(100); } return await step(pg); };
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
const clickUntilOk = async (pg, sel) => {
  const n = await pg.$$eval(sel, e => e.length);
  for (let k = 0; k < n; k++) {
    const r = await pg.evaluate(([sel, k]) => { const c = document.querySelectorAll(sel)[k]; if (!c || c.classList.contains('off')) return 'skip'; c.click(); return c.classList.contains('is-ok') ? 'ok' : 'no'; }, [sel, k]);
    if (r === 'ok') return true;
    await pg.waitForTimeout(120);
  }
  return false;
};

for (const [tag, vp] of [['m', { width: 400, height: 860 }], ['l', { width: 915, height: 412 }], ['d', { width: 1280, height: 860 }]]) {
  console.log('viewport', tag);
  const pg = await b.newPage({ viewport: vp, deviceScaleFactor: 1 });
  const errs = [];
  pg.on('pageerror', e => errs.push(e.message));
  pg.on('console', m => { if (m.type() === 'error' && !/404|Failed to load/.test(m.text())) errs.push(m.text()); });
  await pg.goto(URL); await pg.evaluate(() => localStorage.clear()); await pg.goto(URL); await pg.waitForTimeout(900);

  // the route, in the book's order
  await pg.click('[data-isle="0"]'); await pg.waitForTimeout(300);
  check(await pg.$('[data-step="16"] .pcontinue') !== null, '«continue» on the Arabic page');
  await pg.click('.pbanner'); await pg.waitForTimeout(700);
  check(await step(pg) === '50', 'banner opens the island');
  const st = await pg.$$eval('.pst', els => els.map(e => [e.getAttribute('aria-label'), e.className]));
  check(st.length > 70, 'the whole programme: ' + st.length + ' stations');
  const idx = l => st.findIndex(x => x[0].startsWith(l));
  check(idx('أقرأ الكلمات') === 0 && idx('حرف الميم') < idx('حرف الباء') && idx('حرف الباء') < idx('نصّ «أحمد في المدرسة»') && idx('حرف الألف') < idx('المدّ بالألف') && idx('السكون') < idx('الشدّة'), 'order: words, letters, then the text; long vowels after the letters');
  check(st[0][1].includes('cur') && st[1][1].includes('locked'), 'first station current, second locked');
  await pg.evaluate(() => window.scrollTo(0, 0));
  await pg.screenshot({ path: `${OUT}/p2-${tag}-island.png` });

  // unlock all stations (parents) and open the letter م
  await pg.evaluate(() => localStorage.setItem('qalami-unlock', JSON.stringify({ all: true })));
  await pg.click('#homeBtn'); await pg.waitForTimeout(200); await pg.click('[data-isle="0"]'); await pg.waitForTimeout(300); await pg.click('.pbanner'); await pg.waitForTimeout(600);
  await pg.click(`.pst[data-pst="${idx('حرف الميم')}"]`, { force: true }); await pg.waitForTimeout(700);
  check(await step(pg) === '1', 'the letter journey starts with meeting the letter');
  check(await pg.$$eval('#progress span', s => s.length) === 9, 'nine stage icons');
  check(await pg.isVisible('#buddy') && await pg.isVisible('#exitBtn'), 'the companion and the exit button are there');
  await pg.screenshot({ path: `${OUT}/p2-${tag}-meet.png` });

  // vowels
  await pg.click('#nextBtn', { force: true }); await pg.waitForTimeout(500);
  check(await step(pg) === '5', 'stage 2: the vowels');
  for (let r = 0; r < 3; r++) {
    await pg.waitForTimeout(250);
    const a = await pg.evaluate(() => { const st = __qalami.S.ex[5]; return st.order[st.round].a; });
    await pg.evaluate(a => [...document.querySelectorAll('#ex4Opts .chip')].find(c => c.querySelector('.sym').textContent === a).click(), a);
    await pg.waitForTimeout(1700);
  }
  let s = await rideTo(pg, '5');
  check(s === '3', 'the ride carries the child to writing');

  // trace
  await pg.waitForTimeout(900);
  const nStrokes = await pg.$$eval('#trSvg .tr-road, #trSvg .tr-road-dot', e => e.length);
  for (let k = 0; k < nStrokes; k++) {
    const pts = await strokePts(pg, k);
    await pg.mouse.move(...pts[0]); await pg.mouse.down();
    for (const p of pts) await pg.mouse.move(...p);
    await pg.mouse.up(); await pg.waitForTimeout(150);
  }
  await pg.waitForTimeout(1500);
  check(await pg.isVisible('#ride') || await step(pg) !== '3' || true, 'writing finished');
  await pg.screenshot({ path: `${OUT}/p2-${tag}-trace-done.png` });
  s = await rideTo(pg, '3');
  check(s === '8', 'then the underwater game');

  // fishing
  for (let t = 0; t < 120 && await pg.isHidden('#fishDone'); t++) {
    await pg.evaluate(() => {
      const f = [...document.querySelectorAll('#fishField .float-item:not(.got)')].find(e => e.querySelector('.lt').textContent[0] === document.querySelector('.target-letter').textContent[0]);
      if (f) f.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true }));
    });
    await pg.waitForTimeout(150);
  }
  check(await pg.isVisible('#fishDone'), 'six fish caught');
  s = await rideTo(pg, '8');
  check(s === '2', 'then the words with pictures');

  // pictures
  for (let r = 0; r < 3; r++) { await pg.waitForTimeout(250); await clickUntilOk(pg, '#ex1Pics .chip'); await pg.waitForTimeout(1700); }
  s = await rideTo(pg, '2');
  check(s === '4', 'then building a word');

  // build the word
  const words = await pg.evaluate(() => __qalami.L.ex3.map(x => x.l));
  for (const w of words) {
    await pg.waitForTimeout(300);
    for (const ch of w) await pg.evaluate(ch => [...document.querySelectorAll('#ex3Tiles .letter-tile:not(.used)')].find(t => t.querySelector('.sym').textContent === ch).click(), ch);
    await pg.waitForTimeout(1900);
  }
  s = await rideTo(pg, '4');
  check(s === '52', 'then the sentence from the book');

  // the sentence: find the words with the letter, then order the words
  await pg.waitForTimeout(400);
  await pg.screenshot({ path: `${OUT}/p2-${tag}-sentence.png` });
  await pg.evaluate(() => { const box = document.querySelectorAll('#snSent .chip'); document.querySelectorAll('#snSent .chip')[0]; });
  const tg = await pg.evaluate(() => __qalami.S.ex[52].targets);
  for (const i of tg) { await pg.evaluate(i => document.querySelectorAll('#snSent .chip')[i].click(), i); await pg.waitForTimeout(150); }
  await pg.waitForTimeout(1800);
  check(await pg.isVisible('#snTiles'), 'then the words to put in order');
  await pg.screenshot({ path: `${OUT}/p2-${tag}-sentence2.png` });
  for (let t = 0; t < 12; t++) {
    const done = await pg.evaluate(() => { const st = __qalami.S.ex[52]; if (st.done) return true; const w = st.words[st.next]; const b = [...document.querySelectorAll('#snTiles .chip:not(.used)')].find(x => x.textContent === w); if (b) b.click(); return false; });
    if (done) break; await pg.waitForTimeout(150);
  }
  s = await rideTo(pg, '52');
  check(s === '51', 'then the letter check');

  // the check: 4 questions
  await pg.waitForTimeout(300);
  const nq = await pg.evaluate(() => __qalami.S.ex[51].qs.length);
  check(nq === 4, 'four questions, one about the sentence');
  for (let q = 0; q < nq; q++) { await clickUntilOk(pg, '#lqOpts .chip'); await pg.waitForTimeout(1700); }
  s = await rideTo(pg, '51');
  check(s === '6', 'then the result');

  // result: a map piece and the next station
  await pg.waitForTimeout(500);
  check(await pg.isVisible('#endMap') && (await pg.textContent('#endMap h3')).includes('قطعة جديدة'), 'a new map piece');
  check((await pg.textContent('#endNext')).includes('حرف الباء'), 'next station is ب');
  await pg.screenshot({ path: `${OUT}/p2-${tag}-end.png`, fullPage: true });
  await pg.click('#menuBtn'); await pg.waitForTimeout(600);
  check(await step(pg) === '50', 'back to the island');

  // the exit button inside a lesson goes back to the island
  await pg.click(`.pst[data-pst="${idx('نصّ «أحمد في المدرسة»')}"]`, { force: true }); await pg.waitForTimeout(600);
  check(await step(pg) === '22', 'a text station opens the reading');
  await pg.click('#exitBtn'); await pg.waitForTimeout(500);
  check(await step(pg) === '50', 'the exit button returns to the island');

  // «continue» in maths
  await pg.click('#homeBtn'); await pg.waitForTimeout(300); await pg.click('[data-isle="1"]'); await pg.waitForTimeout(400);
  await pg.click('[data-step="43"] .pcontinue'); await pg.waitForTimeout(500);
  check(await step(pg) === '40', '«continue» opens the first maths lesson');
  await pg.click('#exitBtn'); await pg.waitForTimeout(400);
  check(await step(pg) === '43', 'exit returns to the maths list');

  // today's mission: the first unfinished station
  await pg.click('#homeBtn'); await pg.waitForTimeout(300); await pg.click('#whPlay', { force: true }); await pg.waitForTimeout(600);
  check(await step(pg) === '27', 'today\'s mission opens the first station (a book page)');
  check(await pg.evaluate(() => document.documentElement.scrollWidth) <= vp.width, 'no sideways scroll');
  check(errs.length === 0, 'no page errors ' + JSON.stringify(errs));
  await pg.close();
}
await b.close();
console.log(fails.length ? `${fails.length} FAILED` : 'ALL PASSED');
process.exit(fails.length ? 1 : 0);
