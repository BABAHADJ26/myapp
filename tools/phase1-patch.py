# Phase 1 of "Smart Kids World" on the real app: island home, subject guides, encouragement, hints.
import re, sys
P = sys.argv[1]
S = '/tmp/claude-0/-home-user-myapp/37c566c8-b0f1-513b-86a2-4eb4f860f820/scratchpad/'
s = open(P, encoding='utf-8').read()

def rep(a, b, cnt=1):
    global s
    n = s.count(a)
    assert n == cnt, (a[:80], n)
    s = s.replace(a, b)

def prefix_ids(t):
    for i in ['sky', 'hill1', 'hill2', 'tree', 'cloud', 'flower', 'star', 'apple', 'appleB', 'pencil', 'lion', 'rabbit', 'owl', 'panda', 'island']:
        t = re.sub(r'id="%s"' % i, 'id="w-%s"' % i, t)
        t = re.sub(r'href="#%s"' % i, 'href="#w-%s"' % i, t)
        t = t.replace('url(#%s)' % i, 'url(#w-%s)' % i)
    return t

bg = prefix_ids(open(S + 'bg.html').read()).replace('class="world"', 'class="wbg"')
defs = prefix_ids(open(S + 'defs.html').read())
butterfly = '''<symbol id="w-butterfly" viewBox="0 0 200 200">
    <ellipse cx="100" cy="192" rx="44" ry="6" fill="rgba(0,0,0,.18)"/>
    <path d="M96 96C70 40 14 34 18 78c4 36 44 44 78 30z" fill="#B57CFF" stroke="#2B1A0E" stroke-width="4"/><path d="M104 96c26-56 82-62 78-18-4 36-44 44-78 30z" fill="#B57CFF" stroke="#2B1A0E" stroke-width="4"/>
    <path d="M96 112c-30 0-62 14-52 46 10 26 44 12 56-22zM104 112c30 0 62 14 52 46-10 26-44 12-56-22z" fill="#4FC3F7" stroke="#2B1A0E" stroke-width="4"/>
    <circle cx="48" cy="70" r="10" fill="#FFC83D"/><circle cx="152" cy="70" r="10" fill="#FFC83D"/><circle cx="64" cy="146" r="8" fill="#FF8DB5"/><circle cx="136" cy="146" r="8" fill="#FF8DB5"/>
    <path d="M90 50q-10-26-24-32M110 50q10-26 24-32" fill="none" stroke="#2B1A0E" stroke-width="4" stroke-linecap="round"/><circle cx="66" cy="18" r="8" fill="#FF9F1C" stroke="#2B1A0E" stroke-width="3"/><circle cx="134" cy="18" r="8" fill="#FF9F1C" stroke="#2B1A0E" stroke-width="3"/>
    <ellipse cx="100" cy="128" rx="13" ry="40" fill="#FFB347" stroke="#2B1A0E" stroke-width="4"/>
    <circle cx="100" cy="76" r="28" fill="#FFC24A" stroke="#2B1A0E" stroke-width="4"/>
    <ellipse cx="90" cy="74" rx="7" ry="9" fill="#fff" stroke="#2B1A0E" stroke-width="2.5"/><ellipse cx="110" cy="74" rx="7" ry="9" fill="#fff" stroke="#2B1A0E" stroke-width="2.5"/>
    <circle cx="91" cy="76" r="4" fill="#1B4E9B"/><circle cx="111" cy="76" r="4" fill="#1B4E9B"/>
    <path d="M92 88q8 8 16 0" fill="none" stroke="#2B1A0E" stroke-width="3" stroke-linecap="round"/><circle cx="82" cy="86" r="4" fill="#FF8DB5" opacity=".7"/><circle cx="118" cy="86" r="4" fill="#FF8DB5" opacity=".7"/>
    <path d="M86 52l14-10 14 10" fill="#FF5BA7" stroke="#2B1A0E" stroke-width="2.5" stroke-linejoin="round"/>
  </symbol>'''
defs = defs.replace('</defs></svg>', butterfly + '</defs></svg>')

# ---------- styles ----------
css = '''
/* Smart Kids World: meadow world behind every screen, wooden signs, island home, guides, celebration */
.wbg{position:fixed;inset:0;z-index:-1;pointer-events:none}.wbg svg{width:100%;height:100%}
html,body{background:#8FD3FF}body{background-image:none}
.top-bar h2{background:linear-gradient(#D9954F,#B9783A 55%,#8A5424);border:3px solid #6B3D17;border-radius:14px;color:#FFF4DC;text-shadow:0 2px 0 #6B3D17;padding:2px 16px 4px;flex:0 1 auto;box-shadow:0 4px 0 rgba(0,0,0,.2)}
.world-home{display:flex;flex-direction:column;gap:12px;align-items:center;background:none;border:0;box-shadow:none;padding-inline:0}
.wh-bar{width:100%;display:flex;align-items:center;justify-content:space-between;gap:8px}
.wh-me{display:flex;align-items:center;gap:8px;background:linear-gradient(#3FA2FF,#1F6FD1);color:#fff;border:4px solid #fff;border-radius:999px;padding:3px 16px 3px 4px;box-shadow:0 5px 0 rgba(0,0,0,.2);font-weight:800;cursor:pointer}
.wh-me .av{width:44px;height:44px;border-radius:50%;background:#FFE3B8;border:3px solid #fff;display:grid;place-items:center;overflow:hidden}
.wh-me small{display:flex;align-items:center;gap:3px;font-size:.95rem}
.wh-tools{display:flex;gap:8px}
.wround{width:54px;height:54px;border-radius:50%;display:grid;place-items:center;border:4px solid #fff;box-shadow:0 5px 0 rgba(0,0,0,.22),inset 0 -6px 0 rgba(0,0,0,.15);background:linear-gradient(#5BB8FF,#1F6FD1);font-size:1.5rem;cursor:pointer}
.wround.gold{background:linear-gradient(#FFE07A,#F2A900)}
.wsign{position:relative;padding:6px 26px 8px;background:linear-gradient(#D9954F,#B9783A 55%,#8A5424);border:4px solid #6B3D17;border-radius:18px;color:#FFF4DC;font-weight:800;font-size:clamp(1.3rem,4.6vw,2rem);line-height:1.15;text-align:center;text-shadow:0 3px 0 #6B3D17;box-shadow:0 6px 0 rgba(0,0,0,.25)}
.wsign small{display:block;font-size:.5em;color:#FFE07A}
.wh-main{display:grid;grid-template-columns:minmax(0,.8fr) minmax(0,1.7fr);gap:8px;align-items:end;width:100%}
.wh-hero{display:flex;flex-direction:column;align-items:center;gap:4px}
.wh-hero svg{width:min(100%,250px);height:auto}
.wbubble{background:#fff;border-radius:20px;padding:8px 14px;font-weight:700;box-shadow:0 5px 0 rgba(0,0,0,.15);position:relative;text-align:center;font-size:1.05rem}
.wbubble:after{content:"";position:absolute;bottom:-11px;right:46%;border:11px solid transparent;border-top-color:#fff;border-bottom:0}
.wisles{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:4px 12px}
.wisle{display:flex;flex-direction:column;align-items:center;position:relative;transition:transform .15s;cursor:pointer}
.wisle svg{width:100%;height:auto;filter:drop-shadow(0 10px 6px rgba(0,60,0,.25))}
.wisle:hover{transform:translateY(-4px)}.wisle:active{transform:translateY(3px)}
.wisle .lbl{position:absolute;bottom:12%;color:#FFF4DC;font-weight:800;font-size:clamp(.78rem,2.2vw,1.05rem);line-height:1.1;text-shadow:0 2px 0 #4A2A0E;text-align:center;width:82%}
.wisle .badge{position:absolute;top:3%;left:4%;background:#fff;border-radius:999px;padding:0 8px;font-weight:800;font-size:.78rem;box-shadow:0 3px 0 rgba(0,0,0,.18)}
.wisle .prog{position:absolute;top:3%;right:4%;background:#FFC83D;border-radius:999px;padding:0 8px;font-weight:800;font-size:.78rem;box-shadow:0 3px 0 rgba(0,0,0,.18)}
.wfloat{animation:wfloat 4s ease-in-out infinite}.wisle:nth-child(2n) .wfloat{animation-delay:-1.3s}.wisle:nth-child(3n) .wfloat{animation-delay:-2.6s}
@keyframes wfloat{50%{transform:translateY(-7px)}}
.wplay{display:flex;align-items:center;gap:10px;background:radial-gradient(circle at 40% 30%,#9BF09B,#21A33A 70%);color:#fff;border:5px solid #fff;border-radius:999px;padding:8px 26px 8px 12px;font-weight:800;font-size:1.3rem;text-shadow:0 2px 0 rgba(0,0,0,.25);box-shadow:0 7px 0 rgba(0,0,0,.25);animation:wpulse 1.8s ease-in-out infinite;cursor:pointer}
.wplay i{width:46px;height:46px;border-radius:50%;background:#fff;display:grid;place-items:center;font-style:normal;color:#21A33A;font-size:1.4rem}
@keyframes wpulse{50%{transform:scale(1.05)}}
.wyears{display:flex;flex-wrap:wrap;gap:6px;justify-content:center}
.wyears span{background:rgba(255,255,255,.85);border-radius:999px;padding:2px 12px;font-weight:700;font-size:.85rem}
.wyears span.on{background:#FFC83D}
.wnote{color:#fff;font-size:.8rem;text-align:center;text-shadow:0 1px 2px rgba(0,0,0,.5);margin:0}
.guide{display:flex;align-items:flex-end;gap:10px}
.guide svg.gch{width:90px;height:auto;flex:none}
.guide .wbubble{flex:1;text-align:start}.guide .wbubble:after{right:auto;left:-10px;bottom:18px;border:10px solid transparent;border-right-color:#fff;border-left:0}
.wdlg{position:fixed;inset:0;background:rgba(10,30,60,.55);display:grid;place-items:center;z-index:30;padding:16px}
.wdlg[hidden]{display:none}
.wdlg>div{background:#fff;border-radius:24px;padding:18px;max-width:420px;width:100%;display:flex;flex-direction:column;gap:12px;align-items:center;text-align:center;box-shadow:0 10px 0 rgba(0,0,0,.25)}
.wdlg input{font:inherit;font-size:1.3rem;padding:8px 12px;border:3px solid #C7DCE8;border-radius:14px;width:100%;text-align:center}
.wdlg .opts{display:flex;gap:10px}
.wconf{position:fixed;inset:0;pointer-events:none;overflow:hidden;z-index:25}
.wconf i{position:absolute;top:-20px;width:10px;height:16px;border-radius:3px;animation:wfall linear forwards}
@keyframes wfall{to{transform:translateY(110vh) rotate(720deg)}}
.wpraise{position:fixed;left:50%;top:38%;transform:translate(-50%,-50%);background:linear-gradient(#FFE07A,#F2A900);color:#5A3300;border:5px solid #fff;border-radius:24px;padding:10px 26px;font-weight:800;font-size:clamp(1.6rem,6vw,2.4rem);box-shadow:0 8px 0 rgba(0,0,0,.25);z-index:26;pointer-events:none;animation:wpop 1.3s ease forwards}
@keyframes wpop{0%{transform:translate(-50%,-50%) scale(.3);opacity:0}20%{transform:translate(-50%,-50%) scale(1.12);opacity:1}80%{opacity:1}100%{transform:translate(-50%,-70%) scale(1);opacity:0}}
.mascot.whappy,.gch.whappy{animation:whappy .9s ease}
@keyframes whappy{25%{transform:translateY(-26px) rotate(-10deg)}50%{transform:none}70%{transform:translateY(-10px) rotate(8deg)}}
.mascot.wthink,.gch.wthink{animation:wthink 1.2s ease}
@keyframes wthink{30%,70%{transform:rotate(-9deg)}}
.chip.whint{animation:whint 1s ease-in-out infinite}
@keyframes whint{50%{transform:scale(1.07);box-shadow:0 0 0 8px rgba(255,200,61,.85),0 4px 0 var(--ink)}}
@media(max-width:700px){.wh-main{grid-template-columns:1fr}.wh-hero svg{width:140px}.wisles{grid-template-columns:repeat(2,minmax(0,1fr))}.guide svg.gch{width:64px}.wround{width:46px;height:46px}.wh-me .av{width:36px;height:36px}}
@media(prefers-reduced-motion:reduce){.wfloat,.wplay,.wconf i,.wpraise{animation:none!important}}
'''
i = s.index('</style>')
s = s[:i] + css + s[i:]

# ---------- home: the island world ----------
a = s.index('    <section class="screen" data-step="12">')
b = s.index('    <!-- 13: a year: its subjects -->')
home = '''    <section class="screen world-home" data-step="12">
      <div class="wh-bar">
        <button type="button" class="wh-me" id="whMe" aria-label="اسم الطفل"><span class="av"><svg viewBox="0 0 160 220" width="40" height="40"><use href="#w-pencil"/></svg></span><span><span id="whName">بطلنا</span><small><svg width="18" height="18"><use href="#w-star"/></svg><span id="whStars">0</span></small></span></button>
        <div class="wsign">عالم الأذكياء الصغار<small>قلمي · السنة الأولى ابتدائي</small></div>
        <div class="wh-tools"><button type="button" class="wround gold" id="toQuiz" aria-label="الفروض والاختبارات">🏆</button><button type="button" class="wround" id="toParents" aria-label="فضاء الأولياء">⚙️</button></div>
      </div>
      <div class="wh-main">
        <div class="wh-hero">
          <div class="wbubble" id="whHello">مرحبًا يا صديقي! أنا لومي. اختر جزيرة، وهيا نتعلّم ونلعب!</div>
          <svg viewBox="0 0 200 220" class="gch" id="whLion"><use href="#w-lion"/></svg>
        </div>
        <div class="wisles" id="wisles"></div>
      </div>
      <button type="button" class="wplay" id="whPlay"><i>▶</i><span>مهمّة اليوم</span></button>
      <div class="wyears" id="wyears"></div>
      <p class="wnote">وفق منهاج وزارة التربية الوطنية وكتب السنة الأولى. الشخصيات رسوم مؤقتة.</p>
    </section>

'''
s = s[:a] + home + s[b:]
rep('<div class="app" dir="rtl" lang="ar">', bg + '\n' + defs + '\n<div class="wconf" id="wconf" aria-hidden="true"></div>\n<div class="wdlg" id="wdlg" hidden><div id="wdlgBox"></div></div>\n<div class="app" dir="rtl" lang="ar">')

# every "subjects" back button now goes to the world map
s = s.replace('<button type="button" class="btn" data-go="13">المواد</button>', '<button type="button" class="btn" data-go="12">الخريطة</button>')

# ---------- a guide on each island's screen ----------
GUIDES = {16: ('pencil', '160 220', 'أنا بيكو! هنا الحروف والقراءة والإملاء، كما في كتابك.'),
          43: ('rabbit', '180 230', 'أهلًا يا بطل! أنا بوني. هيا نعدّ ونحسب معًا!'),
          45: ('owl', '180 220', 'أنا أولي! هيا نكتشف العالم من حولنا.'),
          46: ('lion', '200 220', 'أنا لومي! هنا دروس «أحبّ ديني».'),
          47: ('lion', '200 220', 'أنا لومي! هنا دروس «أحبّ وطني».'),
          48: ('butterfly', '200 200', 'أنا لولو! هيا نرسم ونلوّن ونغنّي!')}
for step, (ch, vb, line) in GUIDES.items():
    m = re.search(r'(<section class="screen" data-step="%d" hidden>\s*<div class="top-bar">.*?</div>)' % step, s, re.S)
    assert m, step
    g = '\n      <div class="guide"><svg viewBox="0 0 %s" class="gch"><use href="#w-%s"/></svg><p class="wbubble">%s</p></div>' % (vb, ch, line)
    s = s[:m.end()] + g + s[m.end():]
# the Islamic island also leads to the civic lessons
rep('<div class="units" id="islList"></div>', '<div class="units" id="islList"></div>\n      <button type="button" class="chip unit" data-go="47"><span class="pic" aria-hidden="true">🇩🇿</span><div><b>التربية المدنية: أحبّ وطني</b><small>8 دروس من كتابي</small></div></button>')

# ---------- script ----------
js = r'''
  /* ---------- Smart Kids World: island home, encouragement, celebration ---------- */
  const ISLANDS = [
    { s: 'ar', n: 'الحروف والقراءة', ic: 'أ ب ت', col: '#E8453C', go: 16, count: () => [LESSONS.length, LESSONS.filter(l => best[l.id]).length] },
    { s: 'math', n: 'الأرقام', ic: '1 2 3', col: '#2E8BEA', go: 43, count: () => [MATH.length, MATH.filter(l => best[l.id]).length] },
    { s: 'sci', n: 'الاكتشاف', ic: '🔬', col: '#3DBE4F', go: 45, count: () => [SCI.length, SCI.filter(l => best[l.id]).length] },
    { s: 'art', n: 'الألوان والفنون', ic: '🎨', col: '#8E5CE6', go: 48, count: () => [ART.length, ART.filter(l => best[l.id]).length] },
    { s: 'isl', n: 'ديني ووطني', ic: '🕌', col: '#16A085', go: 46, count: () => [ISL_LESSONS.length, ISL_LESSONS.filter(l => best[l.id]).length] },
    { s: 'brain', n: 'الذكاء والألعاب', ic: '🧩', col: '#FF9F1C' }
  ];
  const allStars = () => Object.values(best).reduce((a, n) => a + (+n || 0), 0) + Object.values(gbest).reduce((a, n) => a + (+n || 0), 0);
  const childName = () => { try { return localStorage.getItem('qalami-name') || 'بطلنا'; } catch (e) { return 'بطلنا'; } };
  function renderWorld() {
    curYear = 1;
    $('#whName').textContent = childName(); $('#whStars').textContent = allStars();
    $('#wisles').innerHTML = ISLANDS.map((it, i) => {
      const c = it.count && it.count(), digits = /^[0-9 ]+$/.test(it.ic);
      return `<button type="button" class="wisle" data-isle="${i}" aria-label="${it.n}"><svg viewBox="0 0 220 200" class="wfloat"><use href="#w-island"/><text x="110" y="84" text-anchor="middle" font-size="${it.ic.length > 2 ? 44 : 58}" font-weight="800" fill="${it.col}" stroke="#fff" stroke-width="5" paint-order="stroke" ${digits ? 'direction="ltr" unicode-bidi="bidi-override"' : ''}>${it.ic}</text></svg><span class="lbl">${it.n}</span>${c ? `<span class="prog">${c[1]} / ${c[0]}</span>` : '<span class="badge">قريبًا</span>'}</button>`;
    }).join('');
    $('#wyears').innerHTML = YEAR_NAMES.slice(1).map((y, i) => `<span class="${i ? '' : 'on'}">${y}${i ? ' · قريبًا' : ''}</span>`).join('');
  }
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-isle]'); if (!b) return;
    const it = ISLANDS[b.dataset.isle];
    if (!it.go) { wreact(b.querySelector('svg'), 'wthink'); say('قَرِيبًا!'); return; }
    curSubject = it.s; go(it.go);
  });
  // today's mission: the next letter the child has not finished yet
  $('#whPlay').onclick = () => { const l = LESSONS.find(x => !best[x.id]) || LESSONS[Math.floor(Math.random() * LESSONS.length)]; curSubject = 'ar'; startLesson(l); };
  const wdlg = html => { $('#wdlgBox').innerHTML = html; $('#wdlg').hidden = false; };
  $('#wdlg').addEventListener('click', e => { if (e.target.id === 'wdlg' || e.target.closest('[data-close]')) $('#wdlg').hidden = true; });
  $('#whMe').onclick = () => {
    wdlg(`<b>ما اسم البطل؟</b><input id="wName" maxlength="20" value="${childName().replace(/"/g, '')}" aria-label="اسم الطفل"><div class="opts"><button type="button" class="btn primary" id="wNameOk">حفظ</button><button type="button" class="btn" data-close>إلغاء</button></div>`);
    $('#wNameOk').onclick = () => { try { localStorage.setItem('qalami-name', $('#wName').value.trim() || 'بطلنا'); } catch (e) {} $('#wdlg').hidden = true; renderWorld(); };
  };
  // a small adults-only gate in front of the parents' corner
  function parentGate(then) {
    const a = 6 + Math.floor(Math.random() * 4), b = 5 + Math.floor(Math.random() * 4), ok = a + b;
    const opts = shuffle([ok, ok + 1, ok - 2]);
    wdlg(`<b>ركن الأولياء</b><span>للكبار فقط: كم ناتج ${a} + ${b}؟</span><div class="opts">${opts.map(v => `<button type="button" class="btn" data-pg="${v}">${v}</button>`).join('')}</div><button type="button" class="btn" data-close>رجوع</button>`);
    $$('[data-pg]').forEach(x => x.onclick = () => { $('#wdlg').hidden = true; if (+x.dataset.pg === ok) then(); });
  }
  // encouragement: many phrases instead of one; a phrase is spoken only once its recording exists
  const PRAISE = ['أَحْسَنْتَ!', 'رَائِعٌ!', 'مُمْتَازٌ!', 'بَرَافُو عَلَيْكَ!', 'يَا سَلَامُ!', 'أَنْتَ نَجْمٌ!', 'أَنْتَ بَطَلٌ!', 'مَا شَاءَ اللَّهُ عَلَيْكَ!', 'جَوَابٌ صَحِيحٌ!', 'هَكَذَا تَمَامًا!', 'عَمَلٌ جَمِيلٌ!', 'رَائِعٌ جِدًّا، أَنَا فَخُورٌ بِكَ!', 'عَرَفْتَهَا بِنَفْسِكَ!', 'أَصَبْتَ الْهَدَفَ!', 'أَحْسَنْتَ، وَاصِلْ هَكَذَا!', 'تَرْكِيزُكَ رَائِعٌ!', 'أَنْتَ تَتَعَلَّمُ بِسُرْعَةٍ!'];
  const TRY = ['تَقْرِيبًا! حَاوِلْ مَرَّةً أُخْرَى.', 'لَا بَأْسَ، كُلُّنَا نَتَعَلَّمُ.', 'فَكِّرْ قَلِيلًا، أَنْتَ قَادِرٌ!', 'أَثِقُ فِي قُدُرَاتِكَ، جَرِّبْ مِنْ جَدِيدٍ.', 'الْخَطَأُ يُعَلِّمُنَا، هَيَّا مَرَّةً أُخْرَى!', 'قَرِيبٌ جِدًّا! انْظُرْ جَيِّدًا.', 'لَا تَسْتَسْلِمْ، أَنْتَ تَسْتَطِيعُ!'];
  const AFTER_TRY = ['رَائِعٌ! لَمْ تَسْتَسْلِمْ وَنَجَحْتَ!', 'أَرَأَيْتَ؟ بِالْمُحَاوَلَةِ تَنْجَحُ!', 'أَحْسَنْتَ، تَعَلَّمْتَ مِنْ خَطَئِكَ!'];
  const plainAr = t => t.replace(/[ً-ْ]/g, '');
  const voiced = list => list.filter(t => CLIP_FILE[clipKey(t)]);
  let wrongStreak = 0;
  const wreact = (el, cls) => { if (!el) return; el.classList.remove('whappy', 'wthink'); void el.getBoundingClientRect(); el.classList.add(cls); setTimeout(() => el.classList.remove(cls), 1300); };
  const curScreen = () => screens.find(x => !x.hidden);
  const COLORS_W = ['#E8453C', '#2E8BEA', '#3DBE4F', '#8E5CE6', '#FF9F1C', '#FF5BA7', '#FFC83D'];
  function celebrate(text) {
    const box = $('#wconf');
    box.innerHTML = Array.from({ length: 46 }, () => `<i style="left:${Math.random() * 100}%;background:${COLORS_W[Math.floor(Math.random() * 7)]};animation-duration:${1.4 + Math.random() * 1.6}s;animation-delay:${Math.random() * .3}s"></i>`).join('') + `<div class="wpraise">${plainAr(text)}</div>`;
    clearTimeout(celebrate.t); celebrate.t = setTimeout(() => box.innerHTML = '', 3200);
    const sc = curScreen(); if (sc) wreact(sc.querySelector('.coach .mascot, .gch'), 'whappy');
  }
  const sayRaw = say;
  say = function (text, queued, done) {
    if (text === 'أحسنت') {
      const pool = wrongStreak ? AFTER_TRY : PRAISE, t = pool[Math.floor(Math.random() * pool.length)];
      celebrate(t); wrongStreak = 0;
      const v = voiced([t]); return sayRaw(v.length ? t : 'أحسنت', queued, done);
    }
    if (text === 'حاول مرة أخرى') {
      wrongStreak++;
      const sc = curScreen(); if (sc) wreact(sc.querySelector('.coach .mascot, .gch'), 'wthink');
      const v = voiced(TRY); return sayRaw(v.length ? v[Math.floor(Math.random() * v.length)] : text, queued, done);
    }
    return sayRaw(text, queued, done);
  };
'''
rep('  const INIT = {', js + '\n  const INIT = {')
rep('    12: renderYears, 13: renderSubjects,', '    12: renderWorld, 13: renderSubjects,')
rep("  $('#toParents').onclick = () => go(14);", "  $('#toParents').onclick = () => parentGate(() => go(14));")
rep('  renderYears();\n})();', '  renderWorld();\n})();')

# say() is a function declaration; make it reassignable by the wrapper above
rep('  function say(text, queued, done) {', '  let say = function (text, queued, done) {')
i = s.index('  let say = function (text, queued, done) {'); j = s.index('\n  }\n', i)
s = s[:j] + '\n  };\n' + s[j + 5:]

# hint after two mistakes in the maths/science/art questions and the reading questions
rep("    st.q = q; st.lock = false; st.picked = [];", "    st.q = q; st.lock = false; st.picked = []; st.wr = 0;")
rep("const no = b => { if (b) { b.classList.remove('is-no'); void b.offsetWidth; b.classList.add('is-no'); } bad(); st.m++;",
    "const no = b => { if (b) { b.classList.remove('is-no'); void b.offsetWidth; b.classList.add('is-no'); } bad(); st.m++; if (++st.wr === 2 && q.opts) { const k = q.opts.findIndex(o => o.ok); const hb = box.children[k]; if (hb) { hb.classList.add('whint'); say('انْظُرْ هُنَا!', true); } }")
rep("st.m++; fb('#qaFb', 'ليس هذا. ارجع إلى النص', 'no'); say('حاول مرة أخرى', true);",
    "st.m++; fb('#qaFb', 'ليس هذا. ارجع إلى النص', 'no'); say('حاول مرة أخرى', true); if (++st.wr === 2) { [...box.children].forEach(x => { if (x.dataset.ok === '1') x.classList.add('whint'); }); }")
rep("    st.lock = false;\n    $('#qaCount')", "    st.lock = false; st.wr = 0;\n    $('#qaCount')")
rep("      b.type = 'button'; b.className = 'chip';\n      b.innerHTML = `<span class=\"pic\" aria-hidden=\"true\">${p}</span><span class=\"word\">${w}</span>`;",
    "      b.type = 'button'; b.className = 'chip'; b.dataset.ok = ok ? '1' : '0';\n      b.innerHTML = `<span class=\"pic\" aria-hidden=\"true\">${p}</span><span class=\"word\">${w}</span>`;")
open(P, 'w', encoding='utf-8').write(s)
print('ok', len(s))
