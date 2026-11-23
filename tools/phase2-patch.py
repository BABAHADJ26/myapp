# Phase 2 of "Smart Kids World": the letters island.
# A winding path of the book's letters (stars, locks, a map piece per letter), a 6-stage journey per letter
# (meet, trace along the road, underwater fishing, pictures and words, memory, a 3-question check),
# a new stroke-by-stroke tracer, and the underwater theme of the fishing game.
# Run once on app/www/index.html:  python3 tools/phase2-patch.py app/www/index.html
import sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/www/index.html'
s = open(P, encoding='utf-8').read()
assert 'PATH_ORDER' not in s and 'JOURNEY_FLOW' not in s, 'already patched'


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f'expected {count} match(es), found {n}: {old[:80]!r}'
    s = s.replace(old, new)


# ---------------------------------------------------------------- CSS
CSS = r'''
/* ---------- phase 2: the letters island ---------- */
.pbanner{display:flex;align-items:center;gap:12px;width:100%;padding:10px 16px;border:4px solid #fff;border-radius:22px;background:linear-gradient(#7FD36B,#2FA84A);color:#fff;font:inherit;font-weight:800;font-size:1.35rem;text-shadow:0 2px 0 rgba(0,0,0,.25);box-shadow:0 6px 0 rgba(0,0,0,.2);cursor:pointer;text-align:start;margin-bottom:12px}
.pbanner .pic{font-size:2.4rem}
.pbanner small{display:block;font-size:.85rem;color:#FFF4DC}
.pmap-card,.end-map{background:linear-gradient(#F7E7C1,#EBD3A0);border:4px solid #B98B4E;border-radius:20px;padding:10px;box-shadow:0 6px 0 rgba(0,0,0,.15);text-align:center;width:100%;max-width:460px;margin:0 auto}
.pmap-card h3,.end-map h3{margin:0 0 6px;color:#6B3D17;font-size:1.1rem}
.pmap svg{width:100%;height:auto;display:block;border-radius:12px}
.pmap-card p,.end-map p{margin:6px 0 0;font-weight:800;color:#6B3D17}
.pnew{animation:pnew 1s ease-in-out infinite}
@keyframes pnew{50%{stroke-width:7}}
.ptrail{position:relative;width:100%;max-width:440px;margin:0 auto;border-radius:30px;background:radial-gradient(ellipse at 50% 20%,#9BE27A,#4FAE3E 85%);border:7px solid #F2D9A0;box-shadow:0 0 0 5px #4FB3F5,0 12px 0 rgba(0,0,0,.15);overflow:hidden}
.ptrail>svg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}
.pst{position:absolute;transform:translate(-50%,-50%);width:76px;height:76px;border-radius:50%;border:5px solid #fff;background:radial-gradient(circle at 35% 30%,#FFE07A,#F2A900 75%);box-shadow:0 6px 0 rgba(0,0,0,.25),inset 0 -6px 0 rgba(0,0,0,.12);display:grid;place-items:center;padding:0;cursor:pointer;font:inherit;color:#5A3300;z-index:2}
.pst .l{font-family:var(--f-school);font-weight:700;font-size:2.1rem;line-height:1;margin-top:-4px}
.pst .ps{position:absolute;bottom:-14px;display:flex;background:#fff;border-radius:999px;padding:1px 5px;box-shadow:0 2px 0 rgba(0,0,0,.2)}
.pst .ps .star{width:15px;height:15px}
.pst .pg{position:absolute;top:-13px;background:#B9783A;color:#FFF4DC;border:2px solid #6B3D17;border-radius:999px;font-size:.68rem;font-weight:800;padding:0 6px;line-height:1.5;white-space:nowrap}
.pst.done{background:radial-gradient(circle at 35% 30%,#9BF09B,#21A33A 75%);color:#fff;text-shadow:0 2px 0 rgba(0,0,0,.25)}
.pst.locked{background:radial-gradient(circle at 35% 30%,#EEF3F6,#A9BAC6 75%);color:#61798A;cursor:pointer}
.pst .lock{position:absolute;bottom:-12px;font-size:1.15rem}
.pst.cur{animation:pcur 1.4s ease-in-out infinite;box-shadow:0 0 0 8px rgba(255,255,255,.65),0 6px 0 rgba(0,0,0,.25)}
@keyframes pcur{50%{transform:translate(-50%,-50%) scale(1.09)}}
.pbiko{position:absolute;width:58px;height:80px;transform:translate(-50%,-100%);z-index:3;pointer-events:none;animation:pbiko 1.2s ease-in-out infinite}
@keyframes pbiko{50%{margin-top:-8px}}
.psign{position:absolute;transform:translate(-50%,-50%);z-index:1;background:linear-gradient(#D9954F,#B9783A 55%,#8A5424);border:3px solid #6B3D17;border-radius:12px;color:#FFF4DC;font-weight:800;font-size:.82rem;line-height:1.25;padding:3px 10px 4px;text-align:center;box-shadow:0 4px 0 rgba(0,0,0,.2);white-space:nowrap}
.psign small{display:block;color:#FFE07A;font-size:.72rem}
.pmore{text-align:center;margin:14px 0 0}
.like{flex-direction:row;gap:10px;margin:8px auto 0;font-weight:800;font-size:1.3rem;padding:6px 18px}
.like .sym{font-size:2.4rem}.like .pic{font-size:2.2rem}
.trace-wrap #trSvg{position:absolute;inset:0;width:100%;height:100%;touch-action:none;display:none;user-select:none;-webkit-user-select:none}
.trace-wrap.pathmode #trSvg{display:block}
.trace-wrap.pathmode canvas{display:none}
.tr-road{fill:none;stroke:rgba(243,246,238,.2);stroke-linecap:round;stroke-linejoin:round}
.tr-road-dot{fill:rgba(243,246,238,.22)}
.tr-center{fill:none;stroke:rgba(243,246,238,.8);stroke-linecap:round}
.tr-ink{fill:none;stroke:#FFC83D;stroke-linecap:round;stroke-linejoin:round}
.tr-ink-dot{fill:#FFC83D}
.tr-demo{fill:none;stroke:#7FD3FF;stroke-linecap:round;stroke-linejoin:round}
.tr-start{fill:#3DDC5A;stroke:#fff;transform-box:fill-box;transform-origin:center;animation:trpulse 1s ease-in-out infinite}
@keyframes trpulse{50%{transform:scale(1.3)}}
.tr-end{fill:#E8453C;stroke:#fff}
.tr-arrow{fill:#fff}
.tr-num{fill:#18324A;font-weight:800;font-family:var(--f-display)}
.trace-wrap.slip{animation:shake .4s}
.lq-q{display:flex;align-items:center;justify-content:center;gap:14px;min-height:96px}
.lq-q .pic{font-size:4.6rem;line-height:1}
.lq-opts .chip .sym{font-size:3rem}
.lq-opts .chip .pic{font-size:3rem}
.lq-opts .chip.off{opacity:.4;pointer-events:none}
.field.sea.deep{background:linear-gradient(#63CBF2,#1F6FA6 55%,#0E3F6B)}
.sea-deco{position:absolute;inset:0;pointer-events:none;z-index:0;overflow:hidden}
.sea-deco i{position:absolute;bottom:24px;width:11px;height:11px;border-radius:50%;border:2px solid rgba(255,255,255,.75);animation:bubble 5s linear infinite}
@keyframes bubble{from{transform:translateY(0);opacity:0}10%{opacity:1}to{transform:translateY(-400px);opacity:0}}
.sea-deco .weed{position:absolute;bottom:20px;width:16px;border-radius:14px 14px 0 0;background:linear-gradient(#5FD07A,#1F8F45);transform-origin:bottom;animation:weed 3s ease-in-out infinite}
.weed.w1{left:4%;height:74px}.weed.w2{left:9%;height:48px;animation-delay:-1s}.weed.w3{left:58%;height:60px;animation-delay:-2s}
@keyframes weed{50%{transform:rotate(9deg)}}
.sea-deco .sub{position:absolute;bottom:24px;right:8px;width:124px;animation:wfloat 3s ease-in-out infinite}
.net{position:absolute;left:0;top:0;width:72px;height:72px;border-radius:50%;border:4px solid #8A5424;background:repeating-linear-gradient(45deg,transparent 0 7px,rgba(255,255,255,.9) 7px 9px),repeating-linear-gradient(-45deg,transparent 0 7px,rgba(255,255,255,.9) 7px 9px);z-index:3;pointer-events:none;animation:netdrop .7s ease-out forwards}
@keyframes netdrop{from{opacity:0;margin-top:-60px;scale:.5}40%{opacity:1;margin-top:0;scale:1}to{opacity:0;scale:.7}}
.progress.jr{gap:4px}
.progress.jr span{height:auto;display:grid;place-items:center;font-size:1.05rem;line-height:1.5;background:rgba(255,255,255,.7);border-color:var(--line)}
.progress.jr span.done{background:var(--ok-bg);border-color:var(--ok)}
.progress.jr span.current{background:var(--sun);border-color:var(--ink)}
.punlock{display:flex;gap:10px;align-items:center;background:var(--sky);border-radius:14px;padding:8px 12px;font-weight:700;cursor:pointer}
.punlock input{width:24px;height:24px;flex:none}
@media(prefers-reduced-motion:reduce){.pst.cur,.pbiko,.pnew,.tr-start,.sea-deco i,.sea-deco .weed,.sea-deco .sub,.net{animation:none!important}}
</style>'''
rep('</style>\n\n<div class="wbg"', CSS + '\n\n<div class="wbg"')

# ---------------------------------------------------------------- HTML
rep('''      <div class="units" id="units"></div>
    </section>
''', '''      <div class="units" id="units"></div>
    </section>

    <!-- 50: the letters island: a winding path of the book's letters -->
    <section class="screen" data-step="50" hidden>
      <div class="top-bar"><button type="button" class="btn" data-go="16">الحروف والقراءة</button><h2>جزيرة الحروف</h2></div>
      <div class="guide"><svg viewBox="0 0 160 220" class="gch"><use href="#w-pencil"/></svg><p class="wbubble" id="pathHello"></p></div>
      <div class="pmap-card"><h3>🗺️ خريطة جزيرة الحروف</h3><div class="pmap" id="pathMap"></div><p id="pathMapNote"></p></div>
      <div class="ptrail" id="pathTrail"></div>
      <p class="pmore"><button type="button" class="btn" data-go="0">كل تمارين الحروف (9 أنشطة لكل حرف)</button></p>
    </section>

    <!-- 51: the letter check: 3 questions -->
    <section class="screen" data-step="51" hidden>
      <span class="kicker">اختبار الحرف</span>
      <div class="coach">
        <span class="mascot" data-mascot></span>
        <p class="bubble" id="lqPrompt"></p>
      </div>
      <div class="round"><span>السؤال <span id="lqCount">1 / 3</span></span></div>
      <div class="lq-q"><span class="pic" id="lqPic" aria-hidden="true"></span><button type="button" class="speak" id="lqSay" aria-label="استمع"></button></div>
      <div class="row3 lq-opts" id="lqOpts"></div>
      <p class="feedback" id="lqFb" aria-live="polite"></p>
    </section>
''')

rep('''        <p id="boardNote"></p>
      </div>''', '''        <p id="boardNote"></p>
      </div>
      <button type="button" class="chip like" id="learnLike"></button>''')

rep('''        <canvas id="trInk" aria-label="لوحة الكتابة"></canvas>
      </div>
      <div class="btns">
        <button type="button" class="btn" id="trClear">امسح</button>''', '''        <canvas id="trInk" aria-label="لوحة الكتابة"></canvas>
        <svg id="trSvg" aria-label="لوحة الكتابة"></svg>
      </div>
      <div class="btns">
        <button type="button" class="btn" id="trShow" hidden>✏️ شاهد بيكو</button>
        <button type="button" class="btn" id="trClear">امسح</button>''')

rep('''      <p class="hint" id="endSub"></p>''', '''      <p class="hint" id="endSub"></p>
      <div class="end-map" id="endMap" hidden></div>
      <div class="btns"><button type="button" class="btn primary big" id="endNext" hidden></button></div>''')

rep('''      <div class="tiles4" id="pStats"></div>''', '''      <div class="tiles4" id="pStats"></div>
      <label class="punlock"><input type="checkbox" id="pUnlock">افتح كل محطّات جزيرة الحروف (إن كان طفلك قد درس هذه الحروف في القسم)</label>''')

# ---------------------------------------------------------------- JS: hooks into the existing code
rep("  const LETTER_FLOW = [1, 2, 8, 3, 9, 4, 10, 5, 11, 6];",
    "  const LETTER_FLOW = [1, 2, 8, 3, 9, 4, 10, 5, 11, 6];\n"
    "  // the letters island: meet, trace, fish, pictures and words, memory, check, then the result and a map piece\n"
    "  const JOURNEY_FLOW = [1, 3, 8, 2, 10, 51, 6];\n"
    "  const JOURNEY_ICONS = ['👀', '✍️', '🎣', '🖼️', '🃏', '⭐', '🗺️'];")

rep('''  function startLesson(les) {
    loadClips(les.id);
    (BOOK_BY_LESSON[les.id] || []).forEach(x => loadClips(x.u.id));
    FLOW = LETTER_FLOW;''', '''  function startLesson(les, flow) {
    loadClips(les.id);
    (BOOK_BY_LESSON[les.id] || []).forEach(x => loadClips(x.u.id));
    FLOW = flow || LETTER_FLOW;''')

rep('''    $('#bigLetter').textContent = L.letter;''', '''    $('#bigLetter').textContent = L.letter;
    const lf = L.forms[0];
    $('#learnLike').innerHTML = `<span class="sym">${L.letter}</span><span>مثل</span><span class="pic" aria-hidden="true">${lf.p}</span><span class="word">${lf.w}</span>`;
    $('#learnLike').dataset.say = lf.w;''')

rep("    if ([0, 7, 12, 13, 14, 15, 16, 21, 26, 27, 31, 43, 45, 46, 47, 48, 49].includes(i)) inLesson = false;\n"
    "    if (progress.children.length !== FLOW.length) progress.innerHTML = '<span></span>'.repeat(FLOW.length);",
    "    if ([0, 7, 12, 13, 14, 15, 16, 21, 26, 27, 31, 43, 45, 46, 47, 48, 49, 50].includes(i)) inLesson = false;\n"
    "    const pk = FLOW === JOURNEY_FLOW ? 'j' : 'n' + FLOW.length;\n"
    "    if (progress.dataset.k !== pk) {\n"
    "      progress.dataset.k = pk;\n"
    "      progress.classList.toggle('jr', FLOW === JOURNEY_FLOW);\n"
    "      progress.innerHTML = FLOW === JOURNEY_FLOW ? JOURNEY_ICONS.map(x => `<span aria-hidden=\"true\">${x}</span>`).join('') : '<span></span>'.repeat(FLOW.length);\n"
    "    }")

rep('''    try { await document.fonts.load(FONT(100), L.letter); } catch (e) {}
    setupTrace();''', '''    if (TRACE[L.letter]) { setupPathTrace(); return; }
    $('#trWrap').classList.remove('pathmode'); $('#trCheck').hidden = false; $('#trShow').hidden = true;
    try { await document.fonts.load(FONT(100), L.letter); } catch (e) {}
    setupTrace();''')

rep('''  $('#trClear').onclick = () => { if (!S.ex[3].done) { clearInk(); fb('#ex2Fb', ''); } };''',
    '''  $('#trClear').onclick = () => { if (S.ex[3].done) return; fb('#ex2Fb', ''); if ($('#trWrap').classList.contains('pathmode')) setupPathTrace(); else clearInk(); };''')

rep('''    if (total > (best[L.id] || 0)) {
      best[L.id] = total;''', '''    if (FLOW !== JOURNEY_FLOW && total > (best[L.id] || 0)) {
      best[L.id] = total;''')

rep('''    field.hidden = false; field.innerHTML = '';''', '''    field.hidden = false; field.innerHTML = mode === 'fish' ? seaDeco() : '';
    field.classList.toggle('deep', mode === 'fish');''')

rep('''      it.el.classList.add('got');
      good();''', '''      it.el.classList.add('got');
      if (eng.mode === 'fish') netAt(it);
      good();''')

rep("      return `<tr><td><b style=\"font-family:var(--f-school);font-size:1.4rem\">${l.letter}</b></td><td class=\"n\">${best[l.id] ? best[l.id] + ' / ' + MAX_STARS : 'لم يبدأ'}</td>",
    "      return `<tr><td><b style=\"font-family:var(--f-school);font-size:1.4rem\">${l.letter}</b></td><td class=\"n\">${best[l.id] ? best[l.id] + ' / ' + MAX_STARS : jbest[l.id] ? jbest[l.id] + ' / 15' : 'لم يبدأ'}</td>")

rep("  const lessonsDone = () => LESSONS.filter(l => (best[l.id] || 0) > 0).length;",
    "  const lessonsDone = () => LESSONS.filter(l => (best[l.id] || 0) > 0 || (jbest[l.id] || 0) > 0).length;")

rep("    $('#units').innerHTML = renderBook() +",
    "    const pd = PATH.filter(p => pathDone(p.les)).length;\n"
    "    $('#units').innerHTML = `<button type=\"button\" class=\"pbanner\" data-go=\"50\"><span class=\"pic\" aria-hidden=\"true\">🏝️</span><span>جزيرة الحروف<small>${PATH.length} محطّة بترتيب كتابك · ${pd} مكتملة · قطعة من الخريطة لكل حرف</small></span></button>` + renderBook() +")

rep("      unit('🔤', `الحروف الهجائية (${LESSONS.length} حرفًا)`, `${done} من ${LESSONS.length} دروس مكتملة · لكل حرف شرح و4 أنشطة و4 ألعاب`, 0,",
    "      unit('🔤', `الحروف الهجائية (${LESSONS.length} حرفًا)`, `${done} من ${LESSONS.length} دروس مكتملة · طريق الحروف بترتيب الكتاب`, 50,")

rep("    else if (b) startLesson(LESSONS.find(l => l.id === b.dataset.blesson));",
    "    else if (b) startJourney(LESSONS.find(l => l.id === b.dataset.blesson));")

rep("    { s: 'ar', n: 'الحروف والقراءة', ic: 'أ ب ت', col: '#E8453C', go: 16, count: () => [LESSONS.length, LESSONS.filter(l => best[l.id]).length] },",
    "    { s: 'ar', n: 'الحروف والقراءة', ic: 'أ ب ت', col: '#E8453C', go: 16, count: () => [PATH.length, PATH.filter(p => pathDone(p.les)).length] },")

rep("  const allStars = () => Object.values(best).reduce((a, n) => a + (+n || 0), 0) + Object.values(gbest).reduce((a, n) => a + (+n || 0), 0);",
    "  const allStars = () => [best, gbest, jbest].reduce((t, o) => t + Object.values(o).reduce((a, n) => a + (+n || 0), 0), 0);")

rep("  $('#whPlay').onclick = () => { const l = LESSONS.find(x => !best[x.id]) || LESSONS[Math.floor(Math.random() * LESSONS.length)]; curSubject = 'ar'; startLesson(l); };",
    "  $('#whPlay').onclick = () => { const p = PATH.find(x => !pathDone(x.les)) || PATH[Math.floor(Math.random() * PATH.length)]; curSubject = 'ar'; startJourney(p.les); };")

rep(": L.kind === 'math' || L.kind === 'sci' || L.kind === 'art' ? startMath(L) : startLesson(L);",
    ": L.kind === 'math' || L.kind === 'sci' || L.kind === 'art' ? startMath(L) : startLesson(L, FLOW === JOURNEY_FLOW ? JOURNEY_FLOW : undefined);")
rep(": L.kind === 'art' ? 48 : 0);", ": L.kind === 'art' ? 48 : FLOW === JOURNEY_FLOW ? 50 : 0);")
rep("  $('#hubMenu').onclick = () => go(0);\n  $('#hubLesson').onclick = () => startLesson(L);",
    "  $('#hubMenu').onclick = () => go(FLOW === JOURNEY_FLOW ? 50 : 0);\n  $('#hubLesson').onclick = () => startLesson(L, FLOW === JOURNEY_FLOW ? JOURNEY_FLOW : undefined);")

rep('''    INIT['replay' + k] = run;
  });
''', '''    INIT['replay' + k] = run;
  });
  INIT[50] = renderPath;
  INIT[51] = lqInit;
  INIT[6] = (f => () => { f(); journeyEnd(); })(INIT[6]);
  INIT[14] = (f => () => { f(); $('#pUnlock').checked = unlockAll(); })(INIT[14]);
''')

# ---------------------------------------------------------------- JS: the island itself
JS = open(__file__.replace('phase2-patch.py', 'phase2-island.js'), encoding='utf-8').read()
rep('\n  const INIT = {', '\n' + JS + '\n  const INIT = {')

open(P, 'w', encoding='utf-8').write(s)
print('patched', P)
