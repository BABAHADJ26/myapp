# The Arabic programme in the ministry's order, a richer letter journey, the companion and the ride between stages,
# and smooth navigation between stages, lessons and units.
# 1) The island path becomes the whole Arabic programme of the book, in order: per مقطع, per unit: its letters
#    (each a journey: letter, vowels, writing, game, words, building a word, the book's sentence, check), the unit's
#    book pages, then the unit's text with its comprehension exercises; after the last letter the long vowels and
#    sukun; at the end of each مقطع its dictation.
# 2) A child companion (the user's boy) watches, thinks, cheers and, while waiting, says «أنا أثق بقدراتك».
#    When a stage is done he flies in with a propeller cap, or the girl rides in on a skateboard, and carries
#    the lesson to the next stage by itself (no «اضغط التالي»).
# 3) An exit button in every lesson, «the next lesson / next unit» on every result screen, «continue» on every list.
# Run once:  python3 tools/program-patch.py app/www/index.html
import sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/www/index.html'
s = open(P, encoding='utf-8').read()
assert 'const ROUTE = []' not in s, 'already patched'


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f'expected {count} match(es), found {n}: {old[:90]!r}'
    s = s.replace(old, new)


# ---------------------------------------------------------------- journey flow becomes per lesson
s = s.replace('FLOW === JOURNEY_FLOW', '!!FLOW.journey').replace('FLOW !== JOURNEY_FLOW', '!FLOW.journey')
rep("  const JOURNEY_FLOW = [1, 3, 8, 2, 10, 51, 6];\n  const JOURNEY_ICONS = ['👀', '✍️', '🎣', '🖼️', '🃏', '⭐', '🗺️'];",
    "  // letter → vowels → writing → game → words → building a word → the book's sentence → check\n"
    "  const JOURNEY_FLOW = Object.assign([1, 5, 3, 8, 2, 4, 52, 51, 6], { journey: true });\n"
    "  const JOURNEY_ICONS = { 1: '👀', 5: '🔤', 3: '✍️', 8: '🎣', 2: '🖼️', 4: '🧩', 52: '📖', 51: '⭐', 6: '🗺️', 10: '🃏' };")
rep("    FLOW = flow || LETTER_FLOW;", "    FLOW = flow && flow.journey ? journeyFlow(les) : flow || LETTER_FLOW;")
rep("    const pk = !!FLOW.journey ? 'j' : 'n' + FLOW.length;", "    const pk = FLOW.journey ? 'j' + FLOW.join() : 'n' + FLOW.length;")
rep("JOURNEY_ICONS.map(x => `<span aria-hidden=\"true\">${x}</span>`).join('')",
    "FLOW.map(k => `<span aria-hidden=\"true\">${JOURNEY_ICONS[k] || '•'}</span>`).join('')")

# ---------------------------------------------------------------- stage done: the ride, not «press next»
rep("    say('رائع! انتهى النشاط. اضغط التالي.', true);\n    if (S.step === i) nextBtn.disabled = false;",
    "    if (S.step === i) { nextBtn.disabled = false; autoNext(i); }")
rep("      if (S.step === step) nextBtn.disabled = false;\n      updateStarsNow();\n      say('رائع! انتهى النشاط. اضغط التالي.', true);",
    "      if (S.step === step) { nextBtn.disabled = false; autoNext(step); }\n      updateStarsNow();")

# go(): companion, exit button, entering animation, leaving the route
rep("    $('.app').classList.toggle('in-lesson', inLesson);",
    "    clearTimeout(autoNext.t);\n"
    "    if ([0, 12, 13, 14, 15, 16, 21, 26, 31, 43, 45, 46, 47, 48, 49].includes(i)) fromRoute = false;\n"
    "    $('.app').classList.toggle('in-lesson', inLesson);\n"
    "    $('#exitBtn').hidden = !inLesson;")
rep("    if (INIT[i]) INIT[i]();\n    window.scrollTo({ top: 0, behavior: 'smooth' });",
    "    if (INIT[i]) INIT[i]();\n    buddyOn(i);\n    const sc0 = screens.find(sc => +sc.dataset.step === i); sc0.classList.remove('enter'); void sc0.offsetWidth; sc0.classList.add('enter');\n    window.scrollTo({ top: 0, behavior: 'smooth' });")

# result screen: back to the island when the lesson came from it
rep("  $('#menuBtn').onclick = () => go(", "  $('#menuBtn').onclick = () => fromRoute ? go(50) : go(")
rep("  $('#hubMenu').onclick = () => go(!!FLOW.journey ? 50 : 0);", "  $('#hubMenu').onclick = () => go(FLOW.journey || fromRoute ? 50 : 0);")

# ---------------------------------------------------------------- HTML
rep('<button type="button" class="brand" id="homeBtn" aria-label="الرئيسية">',
    '<button type="button" class="wround exitb" id="exitBtn" hidden aria-label="الخروج إلى قائمة الدروس">✕</button>\n    <button type="button" class="brand" id="homeBtn" aria-label="الرئيسية">')
rep('<div class="wcheer" id="wcheer" hidden aria-live="polite"></div>',
    '<div class="wcheer" id="wcheer" hidden aria-live="polite"></div>\n'
    '<div class="buddy" id="buddy" hidden aria-hidden="true"><img id="buddyImg" src="img/boy-think.webp" alt=""></div>\n'
    '<div class="ride" id="ride" hidden aria-hidden="true"></div>')
rep('''    <!-- 51: the letter check: 3 questions -->''', '''    <!-- 52: the book's sentence: find the letter in its words, then put the words in order -->
    <section class="screen" data-step="52" hidden>
      <span class="kicker">الجملة من كتابي</span>
      <div class="coach">
        <span class="mascot" data-mascot></span>
        <p class="bubble" id="snBubble"></p>
      </div>
      <div class="lq-q"><span class="sn-ref" id="snRef"></span><button type="button" class="speak" id="snSay" aria-label="استمع إلى الجملة"></button></div>
      <div class="sn-sent" id="snSent"></div>
      <div class="sn-tiles" id="snTiles" hidden></div>
      <p class="feedback" id="snFb" aria-live="polite"></p>
    </section>

    <!-- 51: the letter check: 3 questions -->''')

CSS = r'''
/* ---------- the companion, the ride, the exit button, the sentence stage ---------- */
.exitb{width:44px;height:44px;font-size:1.2rem;color:#fff;background:linear-gradient(#FF8A7A,#E8453C);border-width:3px}
.top{position:relative}
.buddy{position:fixed;left:max(4px,env(safe-area-inset-left,0px));bottom:6px;z-index:6;width:clamp(78px,13vw,150px);pointer-events:none;transform-origin:50% 100%;animation:buddysway 2.6s ease-in-out infinite}
.buddy img{width:100%;height:auto;display:block;filter:drop-shadow(0 6px 4px rgba(0,0,0,.25))}
.buddy.hop{animation:buddyhop .8s ease}
@keyframes buddysway{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(4deg) translateY(-4px)}}
@keyframes buddyhop{30%{transform:translateY(-34px) rotate(-6deg)}60%{transform:translateY(0)}80%{transform:translateY(-10px)}}
.app.in-lesson:not(.scene) .nav{margin-left:clamp(84px,13vw,150px)}
.app.scene .scene-cast .cast.l{display:none}
.app.in-lesson{padding-bottom:110px}
.ride{position:fixed;inset:0;z-index:28;pointer-events:none;overflow:hidden}
.ride .rider{position:absolute;right:-40vw;display:flex;flex-direction:column;align-items:center}
.ride.heli .rider{top:22vh;width:clamp(120px,22vw,220px);animation:heli 2.5s cubic-bezier(.45,.05,.55,.95) forwards}
.ride.skate .rider{bottom:2vh;width:clamp(120px,22vw,230px);animation:skate 2.5s cubic-bezier(.45,.05,.55,.95) forwards}
.ride .rider img{width:100%;height:auto;display:block;filter:drop-shadow(0 10px 8px rgba(0,0,0,.25))}
.ride .cap{width:78%;margin-bottom:-14%;position:relative;z-index:1}
.ride .prop{transform-box:fill-box;transform-origin:center;animation:propspin .12s linear infinite}
.ride .skb{width:100%;margin-top:-10%}
.ride .trail{position:absolute;top:40%;left:100%;width:60vw;height:6px;border-radius:6px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.9) 0 26px,transparent 26px 44px)}
@keyframes propspin{50%{transform:scaleX(.08)}}
@keyframes heli{0%{transform:translate(0,30px) rotate(6deg)}45%{transform:translate(calc(-50vw - 50%),-10px) rotate(-4deg)}55%{transform:translate(calc(-60vw - 50%),-14px) rotate(-6deg)}100%{transform:translate(calc(-140vw - 100%),20px) rotate(-10deg)}}
@keyframes skate{0%{transform:translate(0,0)}45%{transform:translate(calc(-50vw - 50%),0) rotate(-3deg)}50%{transform:translate(calc(-56vw - 50%),-30px) rotate(-8deg)}58%{transform:translate(calc(-62vw - 50%),0)}100%{transform:translate(calc(-140vw - 100%),0)}}
.screen.enter{animation:screenin .45s ease-out}
@keyframes screenin{from{opacity:0;transform:translateX(-40px)}}
.sn-sent{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;direction:rtl}
.sn-sent .chip{flex-direction:row;padding:6px 16px;font-family:var(--f-school);font-weight:700;font-size:clamp(1.5rem,5vw,2.1rem);line-height:1.7}
.sn-sent .chip.slot-e{min-width:70px;border-style:dashed;background:rgba(255,255,255,.6);color:transparent}
.sn-tiles{display:flex;flex-wrap:wrap;justify-content:center;gap:10px}
.sn-tiles .chip{flex-direction:row;padding:6px 16px;font-family:var(--f-school);font-weight:700;font-size:clamp(1.4rem,4.6vw,1.9rem);line-height:1.7;background:#FFF4DC}
.sn-tiles .chip.used{visibility:hidden}
.sn-ref{font-weight:800;color:var(--ink-soft);font-size:.9rem}
.pst .ic{font-size:2rem;line-height:1}
.pst .ic.ar{font-family:var(--f-school);font-weight:700;font-size:1.9rem}
.pst .nm{position:absolute;top:100%;margin-top:16px;background:rgba(255,255,255,.92);color:var(--ink);border-radius:10px;padding:1px 8px;font-size:.72rem;font-weight:800;line-height:1.35;white-space:nowrap;max-width:150px;overflow:hidden;text-overflow:ellipsis;text-shadow:none}
.pst.t-text{background:radial-gradient(circle at 35% 30%,#9FD8FF,#2E8BEA 75%)}
.pst.t-dict{background:radial-gradient(circle at 35% 30%,#E3D0FF,#8E5CE6 75%)}
.pst.t-page,.pst.t-syl{width:64px;height:64px}
.pcontinue{display:flex;align-items:center;gap:10px;width:100%;padding:8px 14px;border:4px solid #fff;border-radius:20px;background:radial-gradient(circle at 40% 30%,#9BF09B,#21A33A 75%);color:#fff;font:inherit;font-weight:800;font-size:1.15rem;text-shadow:0 2px 0 rgba(0,0,0,.25);box-shadow:0 6px 0 rgba(0,0,0,.2);cursor:pointer;text-align:start}
.pcontinue i{width:42px;height:42px;flex:none;border-radius:50%;background:#fff;color:#21A33A;display:grid;place-items:center;font-style:normal;text-shadow:none}
.pcontinue small{display:block;font-size:.8rem;color:#EFFFF0}
@media(prefers-reduced-motion:reduce){.buddy,.screen.enter,.ride .prop{animation:none!important}}
</style>'''
rep('</style>\n\n<div class="wbg"', CSS + '\n\n<div class="wbg"')

# ---------------------------------------------------------------- the island: the whole programme
a = s.index('  // the winding path: one station per letter, a wooden sign at each new مقطع')
b = s.index('  /* the tracer: follow the road stroke by stroke')
JS_ROUTE = open(__file__.replace('program-patch.py', 'program-route.js'), encoding='utf-8').read()
s = s[:a] + JS_ROUTE + '\n' + s[b:]

rep("  function startJourney(les) { startLesson(les, JOURNEY_FLOW); }",
    "  function startJourney(les) { startLesson(les, JOURNEY_FLOW); }\n"
    "  // the book's sentence for a letter (its page in «كتابي»), and the journey without that stage when there is none\n"
    "  const bookSent = les => { const x = (BOOK_BY_LESSON[les.id] || []).find(x => x.pg.sents && x.pg.sents.length); return x ? { u: x.u, pg: x.pg, s: plain(x.pg.sents[0]).replace(/[.،!؟]+$/, '') } : null; };\n"
    "  function journeyFlow(les) { return Object.assign(JOURNEY_FLOW.filter(k => k !== 52 || bookSent(les)), { journey: true }); }")
rep("    const r = Math.max(j / 15, b / MAX_STARS);", "    const r = Math.max(j / 21, b / MAX_STARS);")
rep("jbest[l.id] ? jbest[l.id] + ' / 15' : 'لم يبدأ'", "jbest[l.id] ? jbest[l.id] + ' / 21' : 'لم يبدأ'")

# home and the Arabic page: the route
rep("    { s: 'ar', n: 'الحروف والقراءة', ic: 'أ ب ت', col: '#E8453C', go: 16, count: () => [PATH.length, PATH.filter(p => pathDone(p.les)).length] },",
    "    { s: 'ar', n: 'الحروف والقراءة', ic: 'أ ب ت', col: '#E8453C', go: 16, count: () => [ROUTE.length, ROUTE.filter(stDone).length] },")
rep("  $('#whPlay').onclick = () => { const p = PATH.find(x => !pathDone(x.les)) || PATH[Math.floor(Math.random() * PATH.length)]; curSubject = 'ar'; startJourney(p.les); };",
    "  $('#whPlay').onclick = () => { let i = ROUTE.findIndex((st, k) => stOpen(k) && !stDone(st)); if (i < 0) i = Math.floor(Math.random() * ROUTE.length); startStation(i); };")
rep("    const pd = PATH.filter(p => pathDone(p.les)).length;\n    $('#units').innerHTML = `<button type=\"button\" class=\"pbanner\" data-go=\"50\"><span class=\"pic\" aria-hidden=\"true\">🏝️</span><span>جزيرة الحروف<small>${PATH.length} محطّة بترتيب كتابك · ${pd} مكتملة · قطعة من الخريطة لكل حرف</small></span></button>`",
    "    const pd = ROUTE.filter(stDone).length;\n    $('#units').innerHTML = `<button type=\"button\" class=\"pbanner\" data-go=\"50\"><span class=\"pic\" aria-hidden=\"true\">🏝️</span><span>جزيرة الحروف: برنامج السنة الأولى<small>${ROUTE.length} محطّة بترتيب كتابك: الحروف، ثم الكلمات، ثم الجمل والنصوص · ${pd} مكتملة</small></span></button>`")

# the letter check gets a fourth question on the sentence
rep("    while (qs.length < 3) qs.push({ ...qs[0], opts: letters() });\n    return qs.slice(0, 3);",
    '''    while (qs.length < 3) qs.push({ ...qs[0], opts: letters() });
    // understanding the book's sentence: which of these words was in it?
    const bs = bookSent(L);
    if (bs) {
      const inS = shuffle(bs.s.split(/\\s+/).filter(w => [...bare(w)].some(c => mine.includes(c))))[0];
      const outS = [];
      shuffle(LESSONS.filter(l => l !== L).flatMap(l => l.memory || [])).forEach(x => { if (outS.length < 2 && ![...bare(x.w)].some(c => avoid.includes(c)) && !outS.includes(x.w)) outS.push(x.w); });
      if (inS && outS.length === 2) qs.splice(3, 0, { prompt: 'أيّ كلمة سمعتها في الجملة؟', voice: 'أَيُّ كَلِمَةٍ سَمِعْتَهَا فِي الْجُمْلَةِ؟', say: bs.s, opts: shuffle([inS, ...outS]).map(w => ({ t: w, ok: w === inS })) });
    }
    return qs.slice(0, 4);''')
rep("        if (q.pics) say(o.t);", "        if (q.pics || hasClip(o.t)) say(o.t);")

# the waiting line and the INIT entries
rep("  const PRAISE = ENC.praise, TRY = ENC.oops, AFTER_TRY = ENC.afterTry;",
    "  ENC.trust = ['أَنَا أَثِقُ بِقُدُرَاتِكَ!'];\n  const PRAISE = ENC.praise, TRY = ENC.oops, AFTER_TRY = ENC.afterTry;")
rep("  INIT[51] = lqInit;", "  INIT[51] = lqInit;\n  INIT[52] = snInit;\n  [43, 45, 46, 47, 48, 16].forEach(k => { const f = INIT[k]; INIT[k] = () => { f(); renderContinue(k); }; });")
rep("  EX_NAMES[51] = 'اختبار الحرف';", "  EX_NAMES[51] = 'اختبار الحرف';\n  EX_NAMES[52] = 'الجملة من كتابي';")

# praise and mistakes move the companion
rep("      celebrate(t); wrongStreak = 0;\n      return sayRaw(isRec(t) ? t : 'أحسنت', queued, done);",
    "      celebrate(t); wrongStreak = 0; buddyFace('cheer', 1800);\n      return sayRaw(isRec(t) ? t : 'أحسنت', queued, done);")
rep("      cheer(t, 'biko');\n      return sayRaw(isRec(t) ? t : text, queued, done);",
    "      cheer(t, 'biko'); buddyFace('think', 0, true);\n      return sayRaw(isRec(t) ? t : text, queued, done);")

rep("  $('#homeBtn').onclick = ", "  $('#exitBtn').onclick = () => { tone([0], 0.01); $('#menuBtn').onclick(); };\n  window.__qalami = { get L() { return L; }, get S() { return S; }, get FLOW() { return FLOW; } };\n  $('#homeBtn').onclick = ")

open(P, 'w', encoding='utf-8').write(s)
print('patched', P)
