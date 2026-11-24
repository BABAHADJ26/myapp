  // the route: the whole Arabic programme of «كتابي في اللغة العربية», in its order (letters → words → sentences → texts)
  const ROUTE = [];
  {
    const seen = new Set(), lastLetter = PATH.length ? PATH[PATH.length - 1].les.id : '';
    MAQATI.forEach(m => {
      BOOK_UNITS.filter(u => u.maqta === m.n).forEach(u => {
        u.pages.forEach((pg, k) => {
          const les = pg.lesson && LESSONS.find(l => l.id === pg.lesson);
          if (les && TRACE[les.letter]) {
            if (seen.has(les.id)) return;
            seen.add(les.id);
            ROUTE.push({ t: 'letter', ref: les, page: pg.page, maqta: m.n });
            // the long vowels and sukun come once every letter is known
            if (les.id === lastLetter) SYLLABLES.forEach(sy => ROUTE.push({ t: 'syl', ref: sy, maqta: m.n }));
          } else if (!pg.lesson) ROUTE.push({ t: 'page', ref: u, k, id: 'pg-' + u.id + '-' + k, page: pg.page, maqta: m.n, name: pageName(pg) });
        });
        ROUTE.push({ t: 'text', ref: u, page: u.page, maqta: m.n });
      });
      const d = DICTS.find(x => x.maqta === m.n);
      if (d) ROUTE.push({ t: 'dict', ref: d, maqta: m.n });
    });
  }
  const pagesSeen = load('qalami-pages');
  const flowMax = f => f.filter(k => EX_NAMES[k]).length * 3;
  const stDone = st => st.t === 'letter' ? pathDone(st.ref) : st.t === 'page' ? !!pagesSeen[st.id] : (best[st.ref.id] || 0) > 0;
  const stStars = st => {
    if (st.t === 'letter') return pathStars(st.ref);
    if (st.t === 'page') return stDone(st) ? 3 : 0;
    const b = best[st.ref.id] || 0; if (!b) return 0;
    const r = b / flowMax(st.t === 'text' ? READ_FLOW : st.t === 'dict' ? DICT_FLOW : SYL_FLOW);
    return r >= 0.85 ? 3 : r >= 0.6 ? 2 : 1;
  };
  const stOpen = i => i === 0 || unlockAll() || stDone(ROUTE[i]) || stDone(ROUTE[i - 1]);
  const stName = st => st.t === 'letter' ? 'حرف ' + st.ref.name : st.t === 'text' ? 'نصّ «' + st.ref.title + '»' : st.t === 'dict' ? 'إملاء المقطع ' + st.ref.maqta : st.t === 'syl' ? st.ref.title : st.name;
  let fromRoute = false;
  function startStation(i) {
    const st = ROUTE[i];
    curSubject = 'ar';
    if (st.t === 'letter') startJourney(st.ref);
    else if (st.t === 'text') startRead(st.ref);
    else if (st.t === 'dict') startDict(st.ref);
    else if (st.t === 'syl') startSyl(st.ref);
    else { pagesSeen[st.id] = 1; store('qalami-pages', pagesSeen); openBookPage(st.ref, st.k); }
    fromRoute = true;
  }

  // the winding path: one station per lesson, a wooden sign at each new مقطع
  function renderPath() {
    const W = 360, pts = [], signs = [];
    let y = 46, prevM = 0;
    ROUTE.forEach((p, i) => {
      if (p.maqta !== prevM) { signs.push({ y: y - 4, m: p.maqta, i }); y += 70; prevM = p.maqta; }
      pts.push({ x: W / 2 + Math.sin(i * 1.15 + 0.6) * 108, y });
      y += p.t === 'letter' ? 96 : 104;
    });
    const H = y - 20;
    let d = `M${pts[0].x.toFixed(1)} ${(pts[0].y - 60).toFixed(1)} L${pts[0].x.toFixed(1)} ${pts[0].y.toFixed(1)}`;
    for (let i = 0; i < pts.length - 1; i++) {
      const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
      d += ` C${(p1.x + (p2.x - p0.x) / 6).toFixed(1)} ${(p1.y + (p2.y - p0.y) / 6).toFixed(1)} ${(p2.x - (p3.x - p1.x) / 6).toFixed(1)} ${(p2.y - (p3.y - p1.y) / 6).toFixed(1)} ${p2.x.toFixed(1)} ${p2.y.toFixed(1)}`;
    }
    let deco = '';
    pts.forEach((p, i) => {
      const side = p.x > W / 2 ? -1 : 1, x = W / 2 + side * (70 + (i % 3) * 22);
      if (Math.abs(p.x - W / 2) < 50) return;
      deco += i % 2 ? `<use href="#w-tree" transform="translate(${x.toFixed(0)} ${p.y - 6}) scale(.32)"/>` : `<use href="#w-flower" transform="translate(${x.toFixed(0)} ${p.y + 18}) scale(1.3)"/><use href="#w-flower" transform="translate(${(x + 22).toFixed(0)} ${p.y + 6})"/>`;
    });
    const cur = ROUTE.findIndex((p, i) => stOpen(i) && !stDone(p));
    const pct = (v, t) => (v / t * 100).toFixed(2) + '%';
    let h = `<svg viewBox="0 0 ${W} ${H}" aria-hidden="true">${deco}<path d="${d}" fill="none" stroke="#D2AE62" stroke-width="40" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#F2D9A0" stroke-width="32" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round"/></svg>`;
    signs.forEach(sg => {
      const m = MAQATI.find(x => x.n === sg.m), p = pts[sg.i];
      h += `<div class="psign" style="left:${pct(p.x > W / 2 ? W / 2 - 60 : W / 2 + 60, W)};top:${pct(sg.y, H)}">${m ? 'المقطع ' + m.n + `<small>${m.pic} ${m.title}</small>` : ''}</div>`;
    });
    ROUTE.forEach((p, i) => {
      const open = stOpen(i), done = stDone(p), n = stStars(p), q = pts[i];
      const cls = (done ? 'done' : open ? 'open' : 'locked') + ' t-' + p.t;
      const face = p.t === 'letter' ? `<span class="l">${p.ref.letter}</span>`
        : p.t === 'syl' ? `<span class="ic ar">${p.ref.mark || p.ref.letter}</span>`
        : `<span class="ic" aria-hidden="true">${p.t === 'text' ? p.ref.letter : p.t === 'dict' ? '✍️' : '📗'}</span>`;
      h += `<button type="button" class="pst ${cls}${i === cur ? ' cur' : ''}" data-pst="${i}" style="left:${pct(q.x, W)};top:${pct(q.y, H)}" aria-label="${stName(p)}${p.page ? '، كتابي صفحة ' + p.page : ''}${open ? '' : '، مقفل'}">`
        + (p.page ? `<span class="pg">ص ${p.page}</span>` : '')
        + face
        + (done ? `<span class="ps">${[0, 1, 2].map(k => STAR(k < n)).join('')}</span>` : open ? '' : '<span class="lock" aria-hidden="true">🔒</span>')
        + (p.t !== 'letter' ? `<span class="nm">${p.t === 'text' ? p.ref.title : stName(p)}</span>` : '')
        + '</button>';
    });
    if (cur >= 0) h += `<img class="pbiko" src="img/biko.webp" alt="" style="left:${pct(pts[cur].x + (pts[cur].x > W / 2 ? -62 : 62), W)};top:${pct(pts[cur].y + 34, H)}">`;
    const trail = $('#pathTrail');
    trail.style.aspectRatio = W + ' / ' + H;
    trail.innerHTML = h;
    $('#pathMap').innerHTML = mapSvg(-1);
    $('#pathMapNote').textContent = mapNote();
    $('#pathHello').textContent = cur >= 0
      ? `أنا بيكو! محطّتك التالية: ${stName(ROUTE[cur])}${ROUTE[cur].page ? '، كما في صفحة ' + ROUTE[cur].page + ' من كتابك' : ''}. نتعلّم الحروف، ثم الكلمات، ثم الجمل والنصوص. وكل حرف تكمله يكشف قطعة من الخريطة!`
      : 'أنا بيكو! أكملت برنامج السنة الأولى كلّه. يمكنك أن تعيد أيّ محطّة لتجمع نجومًا أكثر.';
    if (cur >= 0) setTimeout(() => { const b = trail.querySelector('.pst.cur'); if (b && S.step === 50) b.scrollIntoView({ block: 'center', behavior: 'smooth' }); }, 450);
  }
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-pst]'); if (!b) return;
    const i = +b.dataset.pst;
    if (!stOpen(i)) { wreact(b, 'wthink'); say('أَكْمِلِ الْمَحَطَّةَ السَّابِقَةَ أَوَّلًا.'); return; }
    startStation(i);
  });

  // the next lesson in its own list (book order), for lessons opened from the lists
  function nextInList(l) {
    const after = (list, f, start, label) => { const k = list.indexOf(l); const n = k >= 0 ? list[k + 1] : null; return n ? { go: () => start(n), label: (f && f(l) !== f(n) ? 'الوحدة التالية · ' : 'الدرس التالي: ') + label(n) } : null; };
    if (!l.kind) return after(LESSONS.filter(x => TRACE[x.letter]), null, n => startLesson(n), n => 'حرف ' + n.name);
    if (l.kind === 'syl') return after(SYLLABLES, null, startSyl, n => n.title);
    if (l.kind === 'dict') return after(DICTS, null, startDict, n => n.title);
    if (l.kind === 'math') return after(MATH, x => x.sit, startMath, n => n.title);
    if (l.kind === 'sci') return after(SCI, x => x.sit, startMath, n => n.title);
    if (l.kind === 'art') return after(ART, x => x.sit, startMath, n => n.title);
    if (l.kind === 'read' && l.subj) return after(ISL_LESSONS.filter(x => x.subj === l.subj), x => x.maqta, startRead, n => n.title);
    if (l.kind === 'read' && BOOK_UNITS.includes(l)) return after(BOOK_UNITS, x => x.maqta, startRead, n => n.title);
    if (l.kind === 'read') return after(READINGS, null, startRead, n => n.title);
    return null;
  }

  // the end of a lesson: a letter's map piece, then the next station (or the next lesson / unit of its list)
  function journeyEnd() {
    const jr = !!FLOW.journey && !L.kind;
    $('#endMap').hidden = !jr; $('#endNext').hidden = true;
    if (jr) {
      const total = totalStars(), k = PATH.findIndex(p => p.les === L), fresh = !pathDone(L);
      if (total > (jbest[L.id] || 0)) { jbest[L.id] = total; store('qalami-path', jbest); }
      $('#endMap').innerHTML = `<h3>${fresh ? '🗺️ ربحت قطعة جديدة من خريطة الجزيرة!' : '🗺️ خريطة جزيرة الحروف'}</h3><div class="pmap">${mapSvg(fresh ? k : -1)}</div><p>${mapNote()}</p>`;
      if (fresh) say('رَبِحْتَ قِطْعَةً جَدِيدَةً مِنَ الْخَرِيطَةِ!', true);
      if (fresh && k >= 0 && PATH.filter(p => p.maqta === PATH[k].maqta).every(p => pathDone(p.les))) enc('maqta', { queued: true });
    }
    const ri = ROUTE.findIndex(st => st.ref === L && st.t !== 'page');
    let nx = null;
    if (ri >= 0 && (fromRoute || jr)) {
      const st = ROUTE[ri + 1];
      if (st) nx = { go: () => startStation(ri + 1), label: (st.maqta !== ROUTE[ri].maqta ? 'المقطع التالي · ' : 'المحطّة التالية: ') + stName(st) };
    } else nx = nextInList(L);
    if (nx) {
      const b = $('#endNext');
      b.hidden = false; b.textContent = nx.label + ' ←';
      b.onclick = nx.go;
    }
  }

  // «continue»: the first unfinished lesson of a list, at the top of the list
  function renderContinue(step) {
    const sc = screens.find(x => +x.dataset.step === step);
    const lists = { 43: [MATH, startMath], 45: [SCI, startMath], 46: [ISL_LESSONS.filter(x => x.subj === 'isl'), startRead], 47: [ISL_LESSONS.filter(x => x.subj === 'civ'), startRead], 48: [ART, startMath] };
    let label, run;
    if (step === 16) {
      const i = ROUTE.findIndex((st, k) => stOpen(k) && !stDone(st));
      if (i < 0) return;
      label = stName(ROUTE[i]); run = () => startStation(i);
    } else {
      const [list, start] = lists[step], n = list.find(x => !best[x.id]);
      if (!n) return;
      label = n.title; run = () => start(n);
    }
    let b = sc.querySelector('.pcontinue');
    if (!b) { b = document.createElement('button'); b.type = 'button'; b.className = 'pcontinue'; (sc.querySelector('.guide') || sc.querySelector('.top-bar')).after(b); }
    b.innerHTML = `<i>▶</i><span>تابع من حيث توقّفت<small>${label}</small></span>`;
    b.onclick = run;
  }

  /* the book's sentence: find the words with the letter (analysis), then put the words back in order (synthesis) */
  function snInit() {
    const st = S.ex[52];
    if (st.built) return;
    st.built = true;
    const bs = bookSent(L);
    st.words = bs.s.split(/\s+/); st.sent = bs.s;
    loadClips(bs.u.id);
    $('#snRef').textContent = '📗 كتابي ص ' + bs.pg.page;
    $('#snSay').dataset.say = bs.pg.sents[0].replace(/[\[\]]/g, '');
    st.mine = L.chars || [L.letter];
    st.targets = st.words.map((w, i) => [...bare(w)].some(c => st.mine.includes(c)) ? i : -1).filter(i => i >= 0);
    st.found = new Set();
    if (st.targets.length) snFind(); else snOrder();
  }
  function snFind() {
    const st = S.ex[52];
    st.round = 1; st.wrong = 0;
    $('#snBubble').textContent = 'اضغط على كل كلمة فيها حرف ' + L.name + '.';
    $('#snTiles').hidden = true; fb('#snFb', '');
    const box = $('#snSent'); box.innerHTML = '';
    st.words.forEach((w, i) => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'chip'; b.textContent = w;
      b.onclick = () => {
        if (st.round !== 1 || st.found.has(i)) return;
        if (st.targets.includes(i)) {
          st.found.add(i); b.innerHTML = hlWord(w, { chars: st.mine.join('') }); b.classList.add('is-ok'); good();
          if (hasClip(w)) say(w);
          if (st.found.size === st.targets.length) { st.round = 0; say('أحسنت', true); setTimeout(snOrder, 1500); }
        } else {
          st.m++; st.wrong++; b.classList.remove('is-no'); void b.offsetWidth; b.classList.add('is-no'); bad(); say('حاول مرة أخرى');
          if (st.wrong >= 2) st.targets.filter(t => !st.found.has(t)).forEach(t => box.children[t].classList.add('whint'));
        }
      };
      box.appendChild(b);
    });
    say('اِضْغَطْ عَلَى كُلِّ كَلِمَةٍ فِيهَا هَذَا الْحَرْفُ.'); say(NAMES[L.letter] || L.letter, true); say($('#snSay').dataset.say, true);
  }
  function snOrder() {
    const st = S.ex[52];
    if (S.step !== 52) return;
    st.round = 2; st.wrong = 0;
    // long sentences: the first words stay in place, the child orders the last four
    st.next = Math.max(0, st.words.length - 4);
    $('#snBubble').textContent = 'استمع إلى الجملة، ثم رتّب كلماتها.';
    fb('#snFb', '');
    const box = $('#snSent'), tiles = $('#snTiles');
    const draw = () => {
      box.innerHTML = st.words.map((w, i) => i < st.next ? `<span class="chip${i >= Math.max(0, st.words.length - 4) ? ' is-ok' : ''}">${hlWord(w, { chars: st.mine.join('') })}</span>` : '<span class="chip slot-e">؟</span>').join('');
    };
    draw();
    tiles.hidden = false; tiles.innerHTML = '';
    shuffle(st.words.map((w, i) => ({ w, i })).slice(st.next)).forEach(t => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'chip'; b.textContent = t.w;
      b.onclick = () => {
        if (st.round !== 2 || b.classList.contains('used')) return;
        if (st.words[st.next] === t.w) {
          b.classList.add('used'); st.next++; draw(); good(); [...tiles.children].forEach(x => x.classList.remove('whint'));
          if (st.next === st.words.length) { st.round = 0; say($('#snSay').dataset.say); finish(52, '#snFb'); }
        } else {
          st.m++; st.wrong++; b.classList.remove('is-no'); void b.offsetWidth; b.classList.add('is-no'); bad(); say('حاول مرة أخرى');
          if (st.wrong >= 2) { const ok = [...tiles.children].find(x => !x.classList.contains('used') && x.textContent === st.words[st.next]); if (ok) ok.classList.add('whint'); }
        }
      };
      tiles.appendChild(b);
    });
    say('اِسْتَمِعْ إِلَى الْجُمْلَةِ ثُمَّ رَتِّبْ كَلِمَاتِهَا'); say($('#snSay').dataset.say, true);
  }

  /* the companion: the user's boy watches each lesson, thinks while waiting, cheers on success */
  const BUDDY = { think: 'boy-think', cheer: 'boy-cheer', wink: 'boy-wink', love: 'boy-love' };
  const idle = { last: Date.now(), nudges: 0, at: 0, step: -1 };
  function buddyFace(face, ms, hop) {
    const el = $('#buddy');
    $('#buddyImg').src = `img/${BUDDY[face]}.webp`;
    clearTimeout(buddyFace.t);
    if (ms) buddyFace.t = setTimeout(() => { $('#buddyImg').src = `img/${BUDDY[S.step === 6 ? 'love' : 'think']}.webp`; }, ms);
    if (hop || face === 'cheer') { el.classList.remove('hop'); void el.offsetWidth; el.classList.add('hop'); setTimeout(() => el.classList.remove('hop'), 820); }
  }
  function buddyOn(i) {
    const show = inLesson && FLOW.includes(i);
    $('#buddy').hidden = !show;
    if (!show) return;
    idle.last = Date.now(); idle.nudges = 0; idle.step = i;
    if (i === 6) buddyFace('love', 0, true); else { buddyFace('wink', 1500); }
  }
  document.addEventListener('pointerdown', () => { idle.last = Date.now(); }, true);
  // while the child thinks: now and then, «أنا أثق بقدراتك»
  setInterval(() => {
    if ($('#buddy').hidden || S.step === 6 || document.hidden) return;
    const st = S.ex[S.step];
    if ((st && st.done) || $('#ride').classList.contains('on')) return;
    const now = Date.now();
    if (now - idle.last > 16000 && now - idle.at > 24000 && idle.nudges < 3) {
      idle.at = now; idle.nudges++;
      buddyFace('love', 2600, true);
      enc('trust', { face: 'boy-love' });
    }
  }, 1000);

  /* the ride: when a stage is done, the boy flies in with a propeller cap (or the girl rides a skateboard)
     and takes the child to the next stage */
  const CAP = `<svg class="cap" viewBox="0 0 120 64" aria-hidden="true"><rect x="57" y="8" width="6" height="22" rx="2" fill="#555"/><g class="prop"><ellipse cx="34" cy="9" rx="26" ry="6" fill="#E8453C" stroke="#8E1F1A" stroke-width="2"/><ellipse cx="86" cy="9" rx="26" ry="6" fill="#2E8BEA" stroke="#1A4F8C" stroke-width="2"/></g><circle cx="60" cy="9" r="5" fill="#FFC83D" stroke="#B07A00" stroke-width="2"/><path d="M14 62C14 34 34 24 60 24S106 34 106 62Z" fill="#FFC83D" stroke="#B07A00" stroke-width="3"/><path d="M38 28C30 38 28 50 28 62M82 28C90 38 92 50 92 62" stroke="#E8453C" stroke-width="7" fill="none"/><path d="M60 24V62" stroke="#3DBE4F" stroke-width="7"/></svg>`;
  const BOARD = `<svg class="skb" viewBox="0 0 200 50" aria-hidden="true"><path d="M8 14H192C198 14 198 26 192 26H8C2 26 2 14 8 14Z" fill="#8E5CE6" stroke="#4B2A8C" stroke-width="3"/><path d="M30 18H170" stroke="#FFC83D" stroke-width="3" stroke-dasharray="10 8"/><circle cx="42" cy="38" r="10" fill="#FFC83D" stroke="#18324A" stroke-width="3"/><circle cx="158" cy="38" r="10" fill="#FFC83D" stroke="#18324A" stroke-width="3"/></svg>`;
  let rideN = 0;
  function ride(then) {
    const r = $('#ride'), heli = rideN++ % 2 === 0;
    r.className = 'ride on ' + (heli ? 'heli' : 'skate');
    r.innerHTML = `<div class="rider"><span class="trail"></span>${heli ? CAP + '<img src="img/boy-cheer.webp" alt="">' : '<img src="img/girl.webp" alt="">' + BOARD}</div>`;
    r.hidden = false;
    tone([392, 523, 659, 784], 0.07);
    setTimeout(then, 1150);
    setTimeout(() => { r.hidden = true; r.className = 'ride'; r.innerHTML = ''; }, 2550);
  }
  function autoNext(step) {
    clearTimeout(autoNext.t);
    autoNext.t = setTimeout(() => {
      if (S.step !== step || !inLesson) return;
      const nx = FLOW[FLOW.indexOf(step) + 1];
      if (nx === undefined) return;
      ride(() => { if (S.step === step) go(nx); });
    }, 1900);
  }
