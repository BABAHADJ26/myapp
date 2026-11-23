import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const S = '/tmp/claude-0/-home-user-myapp/37c566c8-b0f1-513b-86a2-4eb4f860f820/scratchpad';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: false, args: ['--headless=new'] });
for (const [tag, vp] of [['d', { width: 1280, height: 860 }], ['m', { width: 400, height: 860 }]]) {
  const pg = await b.newPage({ viewport: vp });
  await pg.addInitScript(() => { window.__said = []; }); const errs = []; pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error' && !/404|Failed to load/.test(m.text())) errs.push(m.text()); });
  await pg.goto('http://localhost:8765/index.html'); await pg.waitForTimeout(1200);
  await pg.screenshot({ path: `${S}/h${tag}1.png` });
  // each island opens its subject
  const steps = [];
  for (let i = 0; i < 5; i++) {
    await pg.click(`[data-isle="${i}"]`); await pg.waitForTimeout(300);
    steps.push(await pg.evaluate(() => [...document.querySelectorAll('.screen')].find(s => !s.hidden).dataset.step));
    if (i === 1) await pg.screenshot({ path: `${S}/h${tag}2.png` });
    await pg.click('.screen:not([hidden]) [data-go="12"]'); await pg.waitForTimeout(200);
  }
  // a maths lesson: two wrong answers then the right one
  await pg.click('[data-isle="1"]'); await pg.waitForTimeout(300);
  await pg.click('[data-math]'); await pg.waitForTimeout(500);
  const q = await pg.evaluate(() => ({ ok: window.__q && window.__q.opts ? window.__q.opts.findIndex(o => o.ok) : -1, n: window.__q && window.__q.opts ? window.__q.opts.length : 0 }));
  let hint = 'n/a';
  if (q.ok >= 0 && q.n >= 3) {
    const btns = await pg.$$('[data-step="40"] .mq-opts .chip');
    const wrong = [...Array(q.n).keys()].filter(k => k !== q.ok);
    await btns[wrong[0]].click(); await pg.waitForTimeout(250); await btns[wrong[1]].click(); await pg.waitForTimeout(300);
    hint = await btns[q.ok].evaluate(e => e.classList.contains('whint'));
    await pg.screenshot({ path: `${S}/h${tag}3.png` });
    await btns[q.ok].click({ force: true }); await pg.waitForTimeout(400);
    await pg.screenshot({ path: `${S}/h${tag}4.png` });
  }
  // the name dialog and the parents' gate
  await pg.goto('http://localhost:8765/index.html'); await pg.waitForTimeout(800);
  await pg.click('#whMe'); await pg.fill('#wName', 'ريم'); await pg.click('#wNameOk'); await pg.waitForTimeout(200);
  const name = await pg.textContent('#whName');
  await pg.click('#toParents'); await pg.waitForTimeout(200);
  const gate = await pg.evaluate(() => { const t = document.querySelector('#wdlgBox span').textContent.match(/(\d+) \+ (\d+)/); return +t[1] + +t[2]; });
  await pg.click(`[data-pg="${gate}"]`); await pg.waitForTimeout(300);
  const parents = await pg.evaluate(() => [...document.querySelectorAll('.screen')].find(s => !s.hidden).dataset.step);
  // today's mission opens a letter lesson
  await pg.click('#homeBtn'); await pg.waitForTimeout(300); await pg.click('#whPlay', { force: true }); await pg.waitForTimeout(500);
  const mission = await pg.evaluate(() => [...document.querySelectorAll('.screen')].find(s => !s.hidden).dataset.step);
  console.log(tag, 'islands→', steps.join(','), 'hint', hint, 'name', name, 'parents', parents, 'mission', mission, 'width', await pg.evaluate(() => document.documentElement.scrollWidth), 'errors', errs);
}
await b.close();
