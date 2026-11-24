# All 90 encouragement lines (voice-scripts/voice-script-encouragement.txt) in their places:
# correct answers, streaks, gentle words after a mistake, the hint after two, success after trying,
# lesson start and return, between activities, end of lesson by stars, stickers, games, tracing,
# maths, reading, the daily greeting and goodbye.
# Each line shows in a bubble with Lumi; it is spoken in the user's voice once its recording exists
# (CLIP_FILE), otherwise the old recorded line (or nothing) is heard, never a device voice for these lines.
# Run once:  python3 tools/encouragement-patch.py app/www/index.html
import re, sys, json

P = sys.argv[1] if len(sys.argv) > 1 else 'app/www/index.html'
s = open(P, encoding='utf-8').read()
assert 'const ENC = ' not in s, 'already patched'


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f'expected {count} match(es), found {n}: {old[:90]!r}'
    s = s.replace(old, new)


L = {}
for line in open(P.replace('app/www/index.html', 'voice-scripts/voice-script-encouragement.txt'), encoding='utf-8'):
    m = re.match(r'(\d\d)  (.+)', line.rstrip())
    if m: L[int(m.group(1))] = m.group(2).strip()
assert len(L) == 90
groups = {
    'praise': range(1, 21), 'streak': range(21, 25), 'oops': range(25, 33), 'hint': range(33, 36), 'afterTry': range(36, 40),
    'start': range(40, 44), 'back': [44, 45], 'next': [46], 'almost': [47], 'half': [48], 'last': [49], 'game': [50],
    'done': range(51, 58), 'full': [58, 56], 'mid': [59], 'low': [60], 'sticker': range(61, 65), 'maqta': [65],
    'play': [66], 'hurry': [67], 'catch': [68, 69], 'allCaught': [70], 'timeUp': [71],
    'arrow': [72], 'green': [73], 'line': [74], 'writing': [75], 'calm': [76],
    'count': [77], 'countWell': [78], 'fast': [79], 'mathPro': [80], 'reading': [81], 'listen': [82], 'understood': [83],
    'morning': [84], 'evening': [85], 'newToday': [86], 'week': [87], 'better': [88], 'bye': [89], 'tomorrow': [90]}
ENC = {k: [L[i] for i in v] for k, v in groups.items()}
used = {i for v in groups.values() for i in v}
assert used == set(range(1, 91))

# ---------------------------------------------------------------- the bubble
rep('<div class="wconf" id="wconf" aria-hidden="true"></div>',
    '<div class="wconf" id="wconf" aria-hidden="true"></div>\n<div class="wcheer" id="wcheer" hidden aria-live="polite"></div>')
CSS = r'''
/* ---------- encouragement bubble ---------- */
.wcheer{position:fixed;top:64px;left:50%;transform:translateX(-50%);z-index:24;display:flex;align-items:center;gap:8px;max-width:min(92vw,560px);background:#fff;border:4px solid #FFC83D;border-radius:999px;padding:4px 18px 4px 6px;box-shadow:0 6px 0 rgba(0,0,0,.18);font-weight:800;font-size:clamp(1rem,3.6vw,1.3rem);line-height:1.3;color:#5A3300;pointer-events:none}
.wcheer img{width:46px;height:46px;object-fit:contain;flex:none}
.wcheer.on{animation:wcheer 2.6s ease-in-out forwards}
@keyframes wcheer{0%{opacity:0;transform:translate(-50%,-30px) scale(.8)}12%,82%{opacity:1;transform:translate(-50%,0) scale(1)}100%{opacity:0;transform:translate(-50%,-20px)}}
.wh-hero .wbubble{animation:none}
@media(prefers-reduced-motion:reduce){.wcheer.on{animation:none}}
</style>'''
rep('</style>\n\n<div class="wbg"', CSS + '\n\n<div class="wbg"')

# ---------------------------------------------------------------- the phrases and the say() wrapper
i = s.index("  const PRAISE = ['")
j = s.index("  const plainAr = t =>", i)
s = s[:i] + '  // the 90 encouragement lines, by situation (see voice-scripts/voice-script-encouragement.txt)\n  const ENC = ' + json.dumps(ENC, ensure_ascii=False) + ''';
  const PRAISE = ENC.praise, TRY = ENC.oops, AFTER_TRY = ENC.afterTry;
''' + s[j:]

rep('''  const sayRaw = say;
  say = function (text, queued, done) {
    if (text === 'أحسنت') {
      const pool = wrongStreak ? AFTER_TRY : PRAISE, t = pool[Math.floor(Math.random() * pool.length)];
      celebrate(t); wrongStreak = 0;
      const v = voiced([t]); return sayRaw(v.length ? t : 'أحسنت', queued, done);
    }
    if (text === 'حاول مرة أخرى') {
      wrongStreak++;
      const sc = curScreen(); if (sc) wreact(sc.querySelector('.coach .mascot, .gch'), 'wthink');
      castReact('wthink');
      const v = voiced(TRY); return sayRaw(v.length ? v[Math.floor(Math.random() * v.length)] : text, queued, done);
    }
    return sayRaw(text, queued, done);''', '''  const sayRaw = say;
  // pick a line (not the same as last time), show it, and speak it if its recording exists
  const encLast = {};
  const isRec = t => !!CLIP_FILE[clipKey(t)];
  function encPick(...keys) {
    const pool = keys.flatMap(k => ENC[k]), rec = pool.filter(isRec), from = rec.length ? rec : pool, k = keys.join();
    let t, n = 0;
    do { t = from[Math.floor(Math.random() * from.length)]; } while (from.length > 1 && t === encLast[k] && ++n < 9);
    encLast[k] = t; return t;
  }
  function cheer(text, face) {
    const box = $('#wcheer');
    box.innerHTML = `<img src="img/${face || 'lumi-happy'}.webp" alt=""><span>${plainAr(text)}</span>`;
    box.hidden = false; box.classList.remove('on'); void box.offsetWidth; box.classList.add('on');
    clearTimeout(cheer.t); cheer.t = setTimeout(() => { box.hidden = true; }, 2650);
  }
  // show (unless show:false) and speak if recorded, else the fallback line if any; returns true if something was spoken
  function enc(keys, o = {}) {
    const t = encPick(...[].concat(keys));
    if (o.show !== false) cheer(t, o.face);
    if (isRec(t)) { sayRaw(t, o.queued); return true; }
    if (o.fallback) { sayRaw(o.fallback, o.queued); return true; }
    return false;
  }
  let rightStreak = 0;
  const subjKind = () => inLesson && L ? (L.kind === 'math' ? 'math' : L.kind === 'read' || L.kind === 'dict' ? 'read' : '') : '';
  say = function (text, queued, done) {
    if (text === 'أحسنت') {
      rightStreak++;
      const k = subjKind();
      const keys = wrongStreak ? ['afterTry'] : rightStreak >= 3 && rightStreak % 3 === 0 ? ['streak'] : k === 'math' && Math.random() < 0.35 ? ['fast', 'mathPro'] : k === 'read' && Math.random() < 0.35 ? ['reading', 'understood'] : ['praise'];
      const t = encPick(...keys);
      celebrate(t); wrongStreak = 0;
      return sayRaw(isRec(t) ? t : 'أحسنت', queued, done);
    }
    if (text === 'حاول مرة أخرى') {
      wrongStreak++; rightStreak = 0;
      const sc = curScreen(); if (sc) wreact(sc.querySelector('.coach .mascot, .gch'), 'wthink');
      castReact('wthink');
      const k = subjKind();
      // the second mistake brings the hint (the activity makes the answer shine)
      const keys = wrongStreak === 2 ? ['hint'] : S.step === 3 ? ['oops', 'calm'] : k === 'math' ? ['oops', 'countWell'] : k === 'read' ? ['oops', 'listen'] : ['oops'];
      const t = encPick(...keys);
      cheer(t, 'biko');
      return sayRaw(isRec(t) ? t : text, queued, done);
    }
    return sayRaw(text, queued, done);''')

# ---------------------------------------------------------------- lesson start, between activities
rep("    if (coach) say(coach.dataset.say);",
    '''    let said = false;
    const fi = inLesson ? FLOW.indexOf(i) : -1;
    if (fi === 0 && !S.greeted) {
      S.greeted = true; S.lastF = 0; rightStreak = 0; wrongStreak = 0;
      said = enc((best[L.id] || (typeof jbest !== 'undefined' && jbest[L.id])) ? 'back' : L.kind === 'math' ? ['start', 'count'] : 'start');
    } else if (fi > 0 && i !== 6 && fi > (S.lastF || 0)) {
      S.lastF = fi;
      const key = [8, 9, 10, 11].includes(i) ? 'game' : fi === FLOW.length - 2 ? 'last' : fi === Math.floor((FLOW.length - 1) / 2) ? 'half' : L.kind === 'math' && Math.random() < 0.4 ? 'count' : fi % 2 ? 'next' : 'almost';
      said = enc(key);
    }
    if (coach) say(coach.dataset.say, said);''')

# ---------------------------------------------------------------- end of lesson, by stars
rep("    say(title); say(L.learned, true);",
    '''    const ek = total >= max ? 'full' : total >= max * 0.6 ? 'done' : total >= max * 0.35 ? 'mid' : 'low', et = encPick(ek);
    $('#endTitle').textContent = plainAr(et);
    say(isRec(et) ? et : title); say(L.learned, true);
    const vis = load('qalami-visit'), today = new Date().toDateString();
    if (vis.doneDay !== today) { vis.doneDay = today; vis.doneN = 0; }
    vis.doneN = (vis.doneN || 0) + 1; store('qalami-visit', vis);''')

# ---------------------------------------------------------------- games
rep("  function memInit() {", "  function memInit() {\n    if (!inLesson) enc('play', { queued: true });")
rep("  function sortInit() {", "  function sortInit() {\n    if (!inLesson) enc('play', { queued: true });")
rep("    if (L.kind === 'math') numSay(+L.letter).forEach(x => say(x, true)); else if (NAMES[L.letter]) say(NAMES[L.letter], true);",
    "    if (L.kind === 'math') numSay(+L.letter).forEach(x => say(x, true)); else if (NAMES[L.letter]) say(NAMES[L.letter], true);\n    if (!inLesson) enc('play', { queued: true });")
rep("      eng.caught++;", "      eng.caught++;\n      if (eng.caught < eng.goal && eng.caught % 2 === 0) enc('catch', { show: eng.caught % 4 === 0 });")
rep("  function showDone(key, m, sel, mistakes) {",
    "  function showDone(key, m, sel, mistakes) {\n    if (key === 'fish' || key === 'balloon') enc('allCaught', { queued: true });")

# ---------------------------------------------------------------- tracing
rep("say('اِبْدَأْ مِنَ النُّقْطَةِ الْخَضْرَاءِ.');", "enc('green', { fallback: 'اِبْدَأْ مِنَ النُّقْطَةِ الْخَضْرَاءِ.' });")
rep("    if (ptr.k < ptr.strokes.length) { trMarks(); fb('#ex2Fb', ''); return; }",
    "    if (ptr.k < ptr.strokes.length) { trMarks(); fb('#ex2Fb', ''); enc('line', { show: false }); return; }")
rep("    celebrate(PRAISE[Math.floor(Math.random() * PRAISE.length)]);", "    celebrate(encPick('writing', 'praise'));")
rep("    trMarks();\n  }\n  function trMarks() {", "    trMarks();\n    enc('arrow', { show: false, queued: true });\n  }\n  function trMarks() {")

# ---------------------------------------------------------------- stickers and the map
rep("      g.classList.add('open'); fanfare(); castReact('whappy');",
    "      g.classList.add('open'); fanfare(); castReact('whappy');\n      enc('sticker', { queued: true });")
rep("    if (fresh) say('رَبِحْتَ قِطْعَةً جَدِيدَةً مِنَ الْخَرِيطَةِ!', true);",
    "    if (fresh) say('رَبِحْتَ قِطْعَةً جَدِيدَةً مِنَ الْخَرِيطَةِ!', true);\n"
    "    if (fresh && PATH.filter(p => p.maqta === PATH[k].maqta).every(p => pathDone(p.les))) enc('maqta', { queued: true });")

# ---------------------------------------------------------------- the day: greeting on the home screen, goodbye after lessons
rep('''  function renderWorld() {
    curYear = 1;''', '''  function renderWorld() {
    curYear = 1;
    if (!renderWorld.greeted) {
      renderWorld.greeted = true;
      const vis = load('qalami-visit'), today = new Date().toDateString(), stars = allStars();
      const first = new Date().getHours() < 12 ? encPick('morning') : encPick('evening');
      const then = vis.day && vis.day !== today && stars > (vis.stars || 0) ? encPick(stars - (vis.weekStars || 0) > 40 ? 'week' : 'better') : encPick('newToday');
      if (vis.day !== today) { if (!vis.weekDay || Date.now() - vis.weekDay > 7 * 864e5) { vis.weekDay = Date.now(); vis.weekStars = stars; } vis.day = today; vis.stars = stars; store('qalami-visit', vis); }
      $('#whHello').textContent = plainAr(first + ' ' + then);
      if (isRec(first)) sayRaw(first); if (isRec(then)) sayRaw(then, true);
    }''')
rep("  $('#homeBtn').onclick = () => go(12);",
    "  $('#homeBtn').onclick = () => { if (S.step === 6) enc((load('qalami-visit').doneN || 0) >= 3 ? 'tomorrow' : 'bye'); go(12); };")

open(P, 'w', encoding='utf-8').write(s)
print('patched', P, '— lines placed:', sum(len(v) for v in ENC.values()))
