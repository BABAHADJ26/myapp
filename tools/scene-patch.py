# "Open scene" presentation for the letter journey, and the tracer restyled to match:
# full-screen scene with Lumi and Biko at the sides (our own characters), no cards or text,
# the letter slides in as a dark road with white dots and an end arrow, an animated hand shows the start,
# red wavy ink with sparkles, the finished letter turns glossy and spins, then a gift box opens on a sticker.
# Run once:  python3 tools/scene-patch.py app/www/index.html
import sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/www/index.html'
s = open(P, encoding='utf-8').read()
assert 'scene-cast' not in s, 'already patched'


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f'expected {count} match(es), found {n}: {old[:90]!r}'
    s = s.replace(old, new)


CSS = r'''
/* ---------- open scene (letter journey) ---------- */
.scene-cast,.scene-rainbow{display:none}
.app.scene .scene-cast,.app.scene .scene-rainbow{display:block}
.scene-rainbow{position:fixed;left:50%;top:6vh;width:min(110vw,1100px);transform:translateX(-50%);z-index:-1;pointer-events:none;opacity:.75}
.scene-cast .cast{position:fixed;bottom:6px;z-index:5;pointer-events:none;width:clamp(70px,15vw,200px);animation:castbob 3s ease-in-out infinite}
.scene-cast .cast svg{width:100%;height:auto;display:block;filter:drop-shadow(0 8px 4px rgba(0,60,0,.25))}
.scene-cast .cast.l{left:max(4px,env(safe-area-inset-left,0px))}
.scene-cast .cast.r{right:max(4px,env(safe-area-inset-right,0px));animation-delay:-1.5s;width:clamp(56px,11vw,150px)}
@keyframes castbob{50%{transform:translateY(-6px)}}
.app.scene{max-width:min(820px,100vw - 2 * clamp(70px,15vw,200px));padding-bottom:110px}
.app.scene .lesson-tag{display:none}
.app.scene .screen{background:none;border:0;box-shadow:none;padding:4px 0;overflow:visible;gap:12px}
.app.scene .coach .bubble,.app.scene .coach .mascot,.app.scene .kicker,.app.scene .round{display:none}
.app.scene .coach{position:absolute;top:0;left:0;z-index:4}
.app.scene .top{flex-wrap:nowrap}.app.scene .progress{width:auto;flex:1}.app.scene .brand{font-size:1.2rem}
body{background:transparent!important}
html,body{overflow-x:clip}
.app.scene .speak{width:58px;height:58px;border:4px solid #fff;background:radial-gradient(circle at 35% 30%,#FFE07A,#F2A900 75%);box-shadow:0 5px 0 rgba(0,0,0,.22)}
.app.scene .feedback{display:none}
.app.scene .game-top{position:absolute;top:0;right:0;z-index:4}
@media (min-aspect-ratio:1/1){.app.scene .field{height:max(200px,100vh - 215px)}.app.scene .target .sym{font-size:1.8rem;line-height:1.5}.app.scene .screen{gap:8px}}
.app.scene .feedback .stars{justify-content:center}
.app.scene .nav{position:fixed;bottom:12px;left:50%;transform:translateX(-50%);z-index:6;gap:14px;width:auto}
.app.scene #nextBtn,.app.scene #prevBtn{font-size:0;padding:0;display:grid;place-items:center;border:4px solid #fff;color:#fff}
.app.scene #nextBtn{width:78px;height:78px;border-radius:24px;background:linear-gradient(#FF8A7A,#E8453C 55%,#B92D25);box-shadow:0 6px 0 rgba(0,0,0,.25),inset 0 -6px 0 rgba(0,0,0,.15)}
.app.scene #nextBtn::after{content:"";width:34px;height:34px;background:#fff;clip-path:polygon(0 50%,55% 0,55% 30%,100% 30%,100% 70%,55% 70%,55% 100%)}
.app.scene #nextBtn:not(:disabled){animation:nextpulse 1.2s ease-in-out infinite}
.app.scene #nextBtn:disabled{filter:grayscale(1);opacity:.35}
@keyframes nextpulse{50%{transform:scale(1.1)}}
.app.scene #prevBtn{width:54px;height:54px;border-radius:18px;background:linear-gradient(#7CC4FF,#2E8BEA);box-shadow:0 5px 0 rgba(0,0,0,.22)}
.app.scene #prevBtn::after{content:"";width:22px;height:22px;background:#fff;clip-path:polygon(100% 50%,45% 0,45% 30%,0 30%,0 70%,45% 70%,45% 100%)}
.app.scene #prevBtn:disabled{opacity:.3}
.app.scene .star-count{background:#fff;border-radius:999px;padding:2px 14px;box-shadow:0 4px 0 rgba(0,0,0,.18)}
.app.scene .progress{background:rgba(255,255,255,.55);border-radius:999px;padding:4px}
.app.scene .trace-wrap{border:0;background:none;width:min(100%,100vh - 240px,540px);overflow:visible}
@media (min-aspect-ratio:1/1){.app.scene .trace-wrap{width:min(100%,100vh - 150px,540px)}.app.scene [data-step="3"] .btns{position:absolute;top:0;right:0;flex-direction:column;gap:8px;z-index:4}.app.scene [data-step="3"] .btns .btn{font-size:.9rem;padding:4px 12px}}
.app.scene .btns .btn{border:4px solid #fff;box-shadow:0 5px 0 rgba(0,0,0,.2)}
.app.scene .field{border:5px solid #fff;box-shadow:0 8px 0 rgba(0,0,0,.18)}
.app.scene .target{background:rgba(255,255,255,.85);border-radius:20px;padding:4px 14px;align-self:center}
.app.scene .game-top .counter{background:#fff;border-radius:999px;padding:2px 14px}
.app.scene .board{border:6px solid #fff}
.app.scene [data-step="1"] .board{background:none;border:0;padding:0}
.app.scene .big-letter{font-size:clamp(7rem,min(34vw,42vh),15rem);line-height:1.3;padding:0 .25em .45em;margin-bottom:-.3em;color:#E8453C;background:linear-gradient(#FF9384,#E8453C 50%,#A92620);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(4px 0 0 #fff) drop-shadow(-4px 0 0 #fff) drop-shadow(0 4px 0 #fff) drop-shadow(0 -4px 0 #fff) drop-shadow(0 8px 0 rgba(0,0,0,.18));animation:bigin 1s cubic-bezier(.2,1.4,.4,1)}
@keyframes bigin{from{transform:translateX(-120%) rotate(-40deg) scale(.5);opacity:0}}
.app.scene #boardNote{background:rgba(255,255,255,.9);border-radius:999px;padding:2px 16px;font-weight:700;color:var(--ink);margin:0}
@media (max-aspect-ratio:1/1){.scene-cast .cast{width:64px}.scene-cast .cast.r{width:48px}.app.scene{max-width:760px}}
/* the tracer, road style */
.tr-edge{fill:none;stroke:#fff;stroke-linecap:round;stroke-linejoin:round}
.tr-road{stroke:#1F5C63}
.tr-road-dot{fill:#1F5C63;stroke:#fff}
.tr-center{stroke:#fff}
.tr-chev{fill:none;stroke:#fff;stroke-linecap:round;stroke-linejoin:round}
.tr-ink{stroke-linecap:round}
.tr-ink-dot{fill:#E8453C}
.tr-hand{font-size:1px}
.drawing .tr-hand{display:none}
.tr-spark{transform-box:fill-box;transform-origin:center;animation:trspark .6s ease-out forwards;fill:#FFE07A}
@keyframes trspark{from{opacity:1;transform:scale(.4)}to{opacity:0;transform:scale(1.6) rotate(90deg)}}
#trSvg.tr-enter{animation:trenter .9s cubic-bezier(.2,1.4,.4,1)}
@keyframes trenter{from{transform:translateX(-110%) rotate(-30deg) scale(.6)}}
#trSvg.tr-win{animation:trwin 1.1s ease-in-out}
@keyframes trwin{40%{transform:perspective(600px) rotateY(180deg) scale(1.08)}100%{transform:perspective(600px) rotateY(360deg)}}
.tr-win .tr-edge,.tr-win .tr-road,.tr-win .tr-center,.tr-win .tr-chev,.tr-win .tr-road-dot{opacity:0;transition:opacity .4s}
/* the gift */
.gift{position:absolute;left:50%;top:50%;width:min(64%,250px);aspect-ratio:1;transform:translate(-50%,-50%);border:0;background:none;padding:0;cursor:pointer;z-index:8;animation:giftin .7s cubic-bezier(.2,1.5,.4,1)}
@keyframes giftin{from{transform:translate(-50%,-160%) scale(.3);opacity:0}}
.gift .box{position:absolute;left:10%;bottom:4%;width:80%;animation:giftshake 1.2s ease-in-out infinite;transform-origin:bottom}
@keyframes giftshake{10%,30%{transform:rotate(-4deg)}20%,40%{transform:rotate(4deg)}50%{transform:none}}
.gift .lid{position:absolute;left:4%;bottom:52%;width:92%;transition:transform .6s cubic-bezier(.3,1.4,.5,1),opacity .6s}
.gift .rays{position:absolute;inset:-30%;border-radius:50%;background:repeating-conic-gradient(rgba(255,240,170,.9) 0 10deg,transparent 10deg 24deg);mask:radial-gradient(circle,#000 30%,transparent 68%);-webkit-mask:radial-gradient(circle,#000 30%,transparent 68%);opacity:0;transition:opacity .4s}
.gift .prize{position:absolute;left:50%;top:50%;width:62%;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#FFF4DC);border:6px solid #FFC83D;box-shadow:0 6px 0 rgba(0,0,0,.2);display:grid;place-items:center;font-size:clamp(3rem,12vw,5.5rem);line-height:1;font-family:var(--f-emoji);transform:translate(-50%,10%) scale(0);transition:transform .7s cubic-bezier(.2,1.6,.4,1) .2s}
.gift.open .box{animation:none}
.gift.open .lid{transform:translate(30%,-160%) rotate(35deg);opacity:0}
.gift.open .rays{opacity:1;animation:raysspin 6s linear infinite}
@keyframes raysspin{to{transform:rotate(360deg)}}
.gift.open .prize{transform:translate(-50%,-62%) scale(1)}
.gift.open .box{opacity:0;transition:opacity .5s .5s}
.gift.gone{transition:opacity .5s,transform .5s;opacity:0;transform:translate(-50%,-50%) scale(.3)}
@media(prefers-reduced-motion:reduce){.scene-cast .cast,#trSvg.tr-enter,#trSvg.tr-win,.app.scene #nextBtn,.gift,.gift .box,.gift.open .rays{animation:none!important}}
</style>'''
rep('</style>\n\n<div class="wbg"', CSS + '\n\n<div class="wbg"')

rep('<div class="app" dir="rtl" lang="ar">', '''<div class="app" dir="rtl" lang="ar">
  <svg class="scene-rainbow" viewBox="0 0 1000 500" aria-hidden="true"><g fill="none" stroke-width="34" opacity=".85"><circle cx="500" cy="520" r="470" stroke="#FF6B6B"/><circle cx="500" cy="520" r="436" stroke="#FFA94D"/><circle cx="500" cy="520" r="402" stroke="#FFE066"/><circle cx="500" cy="520" r="368" stroke="#69DB7C"/><circle cx="500" cy="520" r="334" stroke="#4DABF7"/><circle cx="500" cy="520" r="300" stroke="#9775FA"/></g></svg>
  <div class="scene-cast" aria-hidden="true"><div class="cast l"><svg viewBox="0 0 200 220" id="castL"><use href="#w-lion"/></svg></div><div class="cast r"><svg viewBox="0 0 160 220" id="castR"><use href="#w-pencil"/></svg></div></div>''')

rep("    $('.app').classList.toggle('in-lesson', inLesson);",
    "    $('.app').classList.toggle('in-lesson', inLesson);\n"
    "    const wasScene = $('.app').classList.contains('scene'), scene = inLesson && FLOW === JOURNEY_FLOW && i !== 6;\n"
    "    $('.app').classList.toggle('scene', scene);\n"
    "    if (scene && !wasScene) setTimeout(() => castReact('whappy'), 300);")

rep("    const sc = curScreen(); if (sc) wreact(sc.querySelector('.coach .mascot, .gch'), 'whappy');",
    "    const sc = curScreen(); if (sc) wreact(sc.querySelector('.coach .mascot, .gch'), 'whappy');\n    castReact('whappy');")
rep("      const sc = curScreen(); if (sc) wreact(sc.querySelector('.coach .mascot, .gch'), 'wthink');",
    "      const sc = curScreen(); if (sc) wreact(sc.querySelector('.coach .mascot, .gch'), 'wthink');\n      castReact('wthink');")

# ---- the tracer
rep("    svg.innerHTML = '';\n    const roads = svgEl('g', {}, svg), inks = svgEl('g', {}, svg);",
    "    svg.innerHTML = '';\n    const defs = svgEl('defs', {}, svg);\n    const roads = svgEl('g', {}, svg), inks = svgEl('g', {}, svg);")
rep("      const road = svgEl('path', { class: 'tr-road', d: st }, roads);",
    "      const edge = svgEl('path', { class: 'tr-edge', d: st }, roads);\n      const road = svgEl('path', { class: 'tr-road', d: st }, roads);")
rep("      return { d: st, len, pts, i: 0, road, center, ink };",
    "      return { d: st, len, pts, i: 0, edge, road, center, ink };")
rep('''    ptr.strokes.forEach(st => {
      if (st.dot) { st.road.setAttribute('r', size * 0.06); return; }
      st.road.style.strokeWidth = size * 0.13; st.center.style.strokeWidth = size * 0.012; st.center.style.strokeDasharray = `${size * 0.02} ${size * 0.025}`;
      st.ink.style.strokeWidth = size * 0.09;
    });''', '''    // red ink with a wavy texture, and a glossy red for the finished letter
    const w = size * 0.06;
    defs.innerHTML = `<pattern id="trWave" patternUnits="userSpaceOnUse" width="${w}" height="${w}"><rect width="${w}" height="${w}" fill="#E8453C"/><path d="M0 ${w * 0.5} Q${w * 0.25} ${w * 0.2} ${w * 0.5} ${w * 0.5} T${w} ${w * 0.5}" fill="none" stroke="#C42E26" stroke-width="${w * 0.14}"/></pattern>`
      + `<linearGradient id="trGloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF8A7A"/><stop offset=".45" stop-color="#E8453C"/><stop offset="1" stop-color="#A92620"/></linearGradient>`;
    ptr.strokes.forEach(st => {
      if (st.dot) { st.road.setAttribute('r', size * 0.065); st.road.setAttribute('stroke-width', size * 0.018); return; }
      st.edge.style.strokeWidth = size * 0.175;
      st.road.style.strokeWidth = size * 0.14;
      st.center.style.strokeWidth = size * 0.028; st.center.style.strokeDasharray = `0.01 ${size * 0.055}`;
      st.ink.style.strokeWidth = size * 0.142; st.ink.style.stroke = 'url(#trWave)';
      // a white chevron at the end of the stroke shows where it finishes
      const n = st.pts.length, e = st.pts[n - 1], q = st.pts[Math.max(0, n - 8)], a = size * 0.035;
      svgEl('path', { class: 'tr-chev', d: `M${-a} ${-a} L0 0 L${-a} ${a}`, 'stroke-width': size * 0.022, transform: `translate(${e[0]} ${e[1]}) rotate(${Math.atan2(e[1] - q[1], e[0] - q[0]) * 180 / Math.PI})` }, roads);
    });
    svg.classList.remove('tr-win', 'tr-enter'); void svg.getBoundingClientRect(); svg.classList.add('tr-enter');
    $$('#trWrap .gift').forEach(g => g.remove());''')
rep('''    ptr.demoPath.style.strokeWidth = size * 0.07;''', '''    ptr.demoPath.style.strokeWidth = size * 0.09;''')

# start marks: a ring and an animated hand instead of the green dot, red end and arrow
rep('''    const num = (x, y) => { svgEl('text', { class: 'tr-num', x, y: y + z * 0.025, 'text-anchor': 'middle', 'font-size': z * 0.07 }, g).textContent = ptr.k + 1; };
    if (st.dot) { svgEl('circle', { class: 'tr-start', cx: st.dot[0], cy: st.dot[1], r: z * 0.055, 'stroke-width': z * 0.012 }, g); num(st.dot[0], st.dot[1]); return; }
    const end = st.pts[st.pts.length - 1], a = st.pts[st.i], b = st.pts[Math.min(st.i + Math.round(z * 0.14 / 0.6), st.pts.length - 1)];
    svgEl('circle', { class: 'tr-end', cx: end[0], cy: end[1], r: z * 0.03, 'stroke-width': z * 0.008 }, g);
    if (b !== a) {
      const ang = Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI, s = z * 0.035;
      svgEl('path', { class: 'tr-arrow', d: `M${s} 0 L${-s * 0.7} ${s * 0.75} L${-s * 0.7} ${-s * 0.75} Z`, transform: `translate(${b[0]} ${b[1]}) rotate(${ang})` }, g);
    }
    svgEl('circle', { class: 'tr-start', cx: a[0], cy: a[1], r: z * 0.055, 'stroke-width': z * 0.012 }, g);
    num(a[0], a[1]);''', '''    const hand = (motion) => {
      const h = svgEl('g', { class: 'tr-hand' }, g);
      svgEl('text', { x: -z * 0.035, y: z * 0.12, 'font-size': z * 0.13, style: 'font-family:var(--f-emoji)' }, h).textContent = '☝️';
      if (motion) svgEl('animateMotion', { path: motion, dur: '1.8s', repeatCount: 'indefinite', calcMode: 'linear' }, h);
    };
    if (st.dot) {
      svgEl('circle', { class: 'tr-start', cx: st.dot[0], cy: st.dot[1], r: z * 0.075, style: 'fill:none;stroke:#3DDC5A', 'stroke-width': z * 0.016 }, g);
      hand(`M${st.dot[0]} ${st.dot[1] + z * 0.06} L${st.dot[0]} ${st.dot[1]} L${st.dot[0]} ${st.dot[1] + z * 0.06}`);
      return;
    }
    const a = st.pts[st.i], ahead = st.pts.slice(st.i, Math.min(st.pts.length, st.i + Math.round(z * 0.6 / 0.6)));
    svgEl('circle', { class: 'tr-start', cx: a[0], cy: a[1], r: z * 0.075, style: 'fill:none;stroke:#3DDC5A', 'stroke-width': z * 0.016 }, g);
    hand('M' + ahead.filter((_, j) => j % 3 === 0 || j === ahead.length - 1).map(q => q[0].toFixed(2) + ' ' + q[1].toFixed(2)).join(' L'));''')

rep("    if (dist(p, st.pts[st.i]) < ptr.tol * 1.5) { ptr.down = true; $('#trSvg').setPointerCapture(e.pointerId); fb('#ex2Fb', ''); }",
    "    if (dist(p, st.pts[st.i]) < ptr.tol * 1.5) { ptr.down = true; ptr.marks.classList.add('drawing'); $('#trSvg').setPointerCapture(e.pointerId); fb('#ex2Fb', ''); }")
rep("    if (hit > st.i) { st.i = hit; trInk(st); trMarks(); }",
    "    if (hit > st.i) { st.i = hit; trInk(st); trMarks(); ptr.marks.classList.add('drawing'); if ((ptr.sp = (ptr.sp || 0) + 1) % 3 === 0) trSpark(st.pts[hit]); }")
rep("  ['pointerup', 'pointercancel'].forEach(t => $('#trSvg').addEventListener(t, () => { ptr.down = false; }));",
    "  ['pointerup', 'pointercancel'].forEach(t => $('#trSvg').addEventListener(t, () => { ptr.down = false; if (ptr.marks) ptr.marks.classList.remove('drawing'); }));")
rep("  function trSlip() {\n    ptr.down = false;", "  function trSlip() {\n    ptr.down = false; ptr.marks.classList.remove('drawing');")
rep('''    trMarks();
    say(L.trace.doneSay);
    finish(3, '#ex2Fb');''', '''    trMarks();
    trWin();''')

JS = r'''
  /* ---------- open scene: the cast reacts, the tracer celebrates, a gift opens on a sticker ---------- */
  function castReact(cls) { if ($('.app').classList.contains('scene')) { wreact($('#castL'), cls); setTimeout(() => wreact($('#castR'), cls), 150); } }
  function trSpark(q) {
    const z = ptr.size, r = z * 0.03, star = [0, 1, 2, 3, 4].map(k => { const a = -Math.PI / 2 + k * Math.PI * 2 / 5, b = a + Math.PI / 5; return `${q[0] + Math.cos(a) * r},${q[1] + Math.sin(a) * r} ${q[0] + Math.cos(b) * r * 0.45},${q[1] + Math.sin(b) * r * 0.45}`; }).join(' ');
    const el = svgEl('polygon', { class: 'tr-spark', points: star, transform: `translate(${(Math.random() - 0.5) * z * 0.08} ${(Math.random() - 0.5) * z * 0.08})` }, $('#trSvg'));
    setTimeout(() => el.remove(), 650);
  }
  function trWin() {
    const svg = $('#trSvg');
    ptr.strokes.forEach(st => { if (!st.dot) st.ink.style.stroke = 'url(#trGloss)'; });
    svg.classList.remove('tr-enter'); void svg.getBoundingClientRect(); svg.classList.add('tr-win');
    celebrate(PRAISE[Math.floor(Math.random() * PRAISE.length)]);
    fanfare();
    say(L.trace.doneSay);
    finish(3, '#ex2Fb');
    setTimeout(() => { if (S.step === 3) showGift($('#trWrap')); }, 1500);
  }
  // stickers: our own picks, to be collected in the sticker album (phase 5)
  const STICKERS = ['🦁', '🐪', '🌴', '🕌', '🚀', '🎈', '🍉', '🦋', '🐬', '🌈', '⭐', '🎨', '🚂', '🐢', '🍊', '🌻', '🦜', '🧸', '🍪', '🏰'];
  function showGift(host) {
    const pick = STICKERS[Math.floor(Math.random() * STICKERS.length)];
    const g = document.createElement('button');
    g.type = 'button'; g.className = 'gift'; g.setAttribute('aria-label', 'افتح الهدية');
    g.innerHTML = `<span class="rays"></span>`
      + `<svg class="box" viewBox="0 0 120 92" aria-hidden="true"><rect x="6" y="6" width="108" height="82" rx="8" fill="#E8453C" stroke="#8E1F1A" stroke-width="4"/><rect x="50" y="6" width="20" height="82" fill="#FFC83D" stroke="#B07A00" stroke-width="3"/><circle cx="26" cy="34" r="4" fill="#fff" opacity=".5"/><circle cx="92" cy="60" r="4" fill="#fff" opacity=".5"/><circle cx="30" cy="70" r="3" fill="#fff" opacity=".5"/></svg>`
      + `<svg class="lid" viewBox="0 0 130 56" aria-hidden="true"><path d="M65 26C50 4 30 6 36 20C40 28 58 28 65 26ZM65 26C80 4 100 6 94 20C90 28 72 28 65 26Z" fill="#FFC83D" stroke="#B07A00" stroke-width="3"/><rect x="4" y="24" width="122" height="28" rx="8" fill="#F25A50" stroke="#8E1F1A" stroke-width="4"/><rect x="54" y="24" width="22" height="28" fill="#FFC83D" stroke="#B07A00" stroke-width="3"/></svg>`
      + `<span class="prize" aria-hidden="true">${pick}</span>`;
    host.appendChild(g);
    let opened = false;
    const open = () => {
      if (opened) return; opened = true;
      g.classList.add('open'); fanfare(); castReact('whappy');
      const sk = load('qalami-stickers'); sk.list = (sk.list || []).concat(pick); store('qalami-stickers', sk);
      setTimeout(() => g.classList.add('gone'), 2800);
      setTimeout(() => g.remove(), 3400);
    };
    g.onclick = open;
    setTimeout(open, 2000);
  }
'''
rep('\n  const INIT = {', JS + '\n  const INIT = {')

open(P, 'w', encoding='utf-8').write(s)
print('patched', P)
