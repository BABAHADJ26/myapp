import { chromium } from '/opt/node22/lib/node_modules/playwright/index.mjs';
const S = '/tmp/claude-0/-home-user-myapp/37c566c8-b0f1-513b-86a2-4eb4f860f820/scratchpad';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', headless: false, args: ['--headless=new'] });
for (const [tag, vp] of [['d', { width: 1280, height: 800 }], ['m', { width: 400, height: 860 }]]) {
  const pg = await b.newPage({ viewport: vp });
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('file:///home/user/myapp/prototype/world.html'); await pg.waitForTimeout(900);
  await pg.screenshot({ path: `${S}/${tag}1.png` });
  // letter: trace from top to bottom
  await pg.click('.isle[data-i="0"]'); await pg.waitForTimeout(400);
  const r = await pg.locator('#trace').boundingBox();
  const X = r.x + r.width / 2, Y = y => r.y + y * r.height / 240;
  await pg.mouse.move(X, Y(60)); await pg.mouse.down();
  for (let y = 60; y <= 216; y += 6) await pg.mouse.move(X, Y(y));
  await pg.mouse.up(); await pg.waitForTimeout(500);
  await pg.screenshot({ path: `${S}/${tag}2.png` });
  // maths: one wrong then right, 4 rounds
  await pg.click('[data-to="home"]'); await pg.click('.isle[data-i="1"]'); await pg.waitForTimeout(500);
  for (let k = 0; k < 4; k++) {
    const sum = await pg.evaluate(() => document.querySelectorAll('#eq .grp')[0].children.length + document.querySelectorAll('#eq .grp')[1].children.length);
    if (k === 0) { await (await pg.$$(`.num:not([data-v="${sum}"])`))[0].click(); await pg.waitForTimeout(300); await pg.screenshot({ path: `${S}/${tag}3.png` }); }
    await pg.click(`.num[data-v="${sum}"]`, { force: true }); await pg.waitForTimeout(1900);
  }
  await pg.waitForTimeout(700); await pg.screenshot({ path: `${S}/${tag}4.png` });
  console.log(tag, 'errors', errs, await pg.evaluate(() => document.querySelector('.scene.on').id), await pg.evaluate(() => document.documentElement.scrollWidth));
}
await b.close();
