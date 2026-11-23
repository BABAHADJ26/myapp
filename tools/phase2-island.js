  /* ---------- phase 2: the letters island (path, map pieces, journey, tracer, letter check) ---------- */
  // how each letter is written: strokes in order, in a 100-unit box (drawn over Noto Naskh Arabic); {dot:[x,y]} is a dot to tap
  const TRACE = {
    'أ': ['M51 22 L50 59', 'M53 7 C48 4 45 10 50 11 L54 11 L46 15'],
    'ب': ['M67 36 C70 44 70 52 62 55 C54 58 42 59 37 56 C32 53 32 47 33 42', { dot: [48, 68] }],
    'ت': ['M67 36 C70 44 70 52 62 55 C54 58 42 59 37 56 C32 53 32 47 33 42', { dot: [52, 36] }, { dot: [43, 37] }],
    'ث': ['M67 36 C70 44 70 52 62 55 C54 58 42 59 37 56 C32 53 32 47 33 42', { dot: [53, 36] }, { dot: [44, 37] }, { dot: [48, 31] }],
    'ج': ['M36 41 C40 36 48 37 54 39 L66 40 L60 45 C50 46 42 52 40 60 C38 70 42 77 52 77 C58 77 62 74 66 72', { dot: [53, 61] }],
    'ح': ['M36 41 C40 36 48 37 54 39 L66 40 L60 45 C50 46 42 52 40 60 C38 70 42 77 52 77 C58 77 62 74 66 72'],
    'خ': ['M36 41 C40 36 48 37 54 39 L66 40 L60 45 C50 46 42 52 40 60 C38 70 42 77 52 77 C58 77 62 74 66 72', { dot: [50, 28] }],
    'د': ['M54 35 C57 42 61 49 59 53 C56 58 46 58 40 56'],
    'ذ': ['M53 36 C56 44 61 50 58 55 C54 59 44 59 41 54', { dot: [50, 26] }],
    'ر': ['M53 39 C57 48 59 58 54 66 C50 72 42 70 38 66'],
    'ز': ['M54 39 C58 48 60 58 54 66 C50 72 42 70 37 65', { dot: [50, 30] }],
    'س': ['M75 39 C77 48 77 56 71 58 C66 59 62 57 63 46 C62 56 58 60 52 58 C50 56 48 50 48 45 C52 56 50 70 38 73 C28 75 24 66 26 55'],
    'ش': ['M75 39 C77 48 77 56 71 58 C66 59 62 57 63 46 C62 56 58 60 52 58 C50 56 48 50 48 45 C52 56 50 70 38 73 C28 75 24 66 26 55', { dot: [64, 34] }, { dot: [55, 34] }, { dot: [61, 29] }],
    'ص': ['M49 55 C55 44 63 37 70 38 C78 40 80 47 72 51 C66 54 56 56 49 56 C48 68 40 73 32 73 C25 73 22 66 24 57'],
    'ض': ['M49 55 C55 44 63 37 70 38 C78 40 80 47 72 51 C66 54 56 56 49 56 C48 68 40 73 32 73 C25 73 22 66 24 57', { dot: [60, 28] }],
    'ط': ['M38 58 C46 48 56 37 64 38 C72 39 74 47 68 52 C62 56 50 58 38 58 L29 53', 'M41 22 L39 57'],
    'ظ': ['M38 58 C46 48 56 37 64 38 C72 39 74 47 68 52 C62 56 50 58 38 58 L29 53', 'M41 22 L41 52', { dot: [57, 28] }],
    'ع': ['M55 38 C52 33 44 33 42 40 C41 47 48 51 56 48 L61 45 C50 50 40 56 40 65 C40 74 48 78 56 76 L67 70'],
    'غ': ['M55 38 C52 33 44 33 42 40 C41 47 48 51 56 48 L61 45 C50 50 40 56 40 65 C40 74 48 78 56 76 L67 70', { dot: [46, 24] }],
    'ف': ['M66 47 C60 44 60 36 67 34 C73 33 76 42 75 50 C74 56 64 58 56 59 C44 60 36 58 34 54 C32 50 33 45 33 42', { dot: [61, 21] }],
    'ق': ['M53 53 C47 50 48 39 55 39 C62 39 65 48 64 56 C63 68 56 74 48 74 C40 74 34 68 36 56', { dot: [59, 29] }, { dot: [51, 29] }],
    'ك': ['M62 21 C60 24 61 30 62 38 L63 52 C63 57 60 59 54 59 L35 59', 'M50 38 C46 36 43 41 47 42 L50 42 L43 45'],
    'ل': ['M57 22 L58 54 C58 66 54 72 46 73 C38 73 34 66 35 56'],
    'م': ['M40 52 C44 44 48 38 53 38 C57 40 60 46 61 50 C61 55 50 57 40 57 C38 64 38 71 39 78'],
    'ن': ['M61 45 C64 54 64 64 58 69 C52 74 42 74 38 70 C35 66 36 60 38 55', { dot: [49, 41] }],
    'ه': ['M49 33 C60 37 68 48 65 59 C58 58 52 56 47 52 C43 48 45 42 50 44 C55 47 51 56 44 58 C38 60 34 57 33 54'],
    'و': ['M58 54 C50 55 44 52 45 46 C46 39 56 37 59 44 C62 52 60 64 52 69 C48 71 42 69 38 66'],
    'ي': ['M66 44 C64 37 56 38 54 44 C52 50 58 54 64 57 C68 62 62 70 52 72 C42 74 36 68 37 55', { dot: [52, 79] }, { dot: [44, 80] }]
  };
  EX_NAMES[51] = 'اختبار الحرف';

  // the path: the letters in the order the book teaches them, with their page and مقطع
  const PATH = [];
  BOOK_UNITS.forEach(u => u.pages.forEach(pg => {
    const les = pg.lesson && LESSONS.find(l => l.id === pg.lesson);
    if (les && TRACE[les.letter] && !PATH.some(p => p.les === les)) PATH.push({ les, page: pg.page, maqta: u.maqta });
  }));
  LESSONS.forEach(les => { if (TRACE[les.letter] && !PATH.some(p => p.les === les)) PATH.push({ les, page: 0, maqta: 9 }); });
  const jbest = load('qalami-path');
  const unlockAll = () => !!load('qalami-unlock').all;
  const pathDone = les => (jbest[les.id] || 0) > 0 || (best[les.id] || 0) > 0;
  const pathStars = les => {
    const j = jbest[les.id] || 0, b = best[les.id] || 0;
    if (!j && !b) return 0;
    const r = Math.max(j / 15, b / MAX_STARS);
    return r >= 0.85 ? 3 : r >= 0.6 ? 2 : 1;
  };
  const pathOpen = i => i === 0 || unlockAll() || pathDone(PATH[i].les) || pathDone(PATH[i - 1].les);
  function startJourney(les) { startLesson(les, JOURNEY_FLOW); }
  $('#pUnlock').onchange = e => store('qalami-unlock', { all: e.target.checked });

  // the treasure map of the island: one piece per letter, uncovered when the letter is done
  function mapSvg(fresh) {
    const cols = 7, rows = Math.ceil(PATH.length / cols), W = 280, H = 160, pw = W / cols, ph = H / rows;
    let cover = '';
    PATH.forEach((p, k) => {
      const x = W - (k % cols + 1) * pw, y = Math.floor(k / cols) * ph;
      if (!pathDone(p.les)) cover += `<rect x="${x}" y="${y}" width="${pw}" height="${ph}" fill="#EBD3A0" stroke="#B98B4E" stroke-width="1.2"/><text x="${x + pw / 2}" y="${y + ph / 2 + 7}" text-anchor="middle" font-size="19" font-weight="700" font-family="Noto Naskh Arabic, serif" fill="#B98B4E">${p.les.letter}</text>`;
      else if (k === fresh) cover += `<rect class="pnew" x="${x + 2}" y="${y + 2}" width="${pw - 4}" height="${ph - 4}" rx="4" fill="none" stroke="#FFC83D" stroke-width="3.5"/>`;
    });
    return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="خريطة جزيرة الحروف">
      <rect width="${W}" height="${H}" fill="#4FB3F5"/>
      <path d="M10 30q10-6 20 0t20 0M220 140q10-6 20 0t20 0M14 130q10-6 20 0t20 0M226 22q10-6 20 0t20 0" fill="none" stroke="#BFE8FF" stroke-width="2.5" stroke-linecap="round"/>
      <path d="M36 108C26 70 66 28 130 32C196 24 258 50 250 94C244 134 190 148 130 144C78 150 44 138 36 108Z" fill="#F2D9A0"/>
      <path d="M52 104C46 74 80 42 132 44C188 38 238 60 234 92C230 122 186 132 132 130C86 134 58 124 52 104Z" fill="#5CC85A"/>
      <path d="M150 74L170 44L190 74Z" fill="#9A7653"/><path d="M164 53L170 44L176 53L170 50Z" fill="#fff"/>
      <path d="M176 76L192 54L208 76Z" fill="#86664A"/>
      <g transform="translate(92 60)"><rect x="0" y="10" width="34" height="24" fill="#F4E9FF" stroke="#8E5CE6" stroke-width="2"/><rect x="-4" y="0" width="12" height="34" fill="#E3D4FF" stroke="#8E5CE6" stroke-width="2"/><rect x="26" y="0" width="12" height="34" fill="#E3D4FF" stroke="#8E5CE6" stroke-width="2"/><path d="M-6 0L2-12L10 0ZM24 0L32-12L40 0Z" fill="#8E5CE6"/><rect x="12" y="20" width="10" height="14" rx="5" fill="#8A5424"/></g>
      <use href="#w-tree" transform="translate(70 100) scale(.18)"/><use href="#w-tree" transform="translate(214 104) scale(.16)"/><use href="#w-tree" transform="translate(150 112) scale(.14)"/>
      <path d="M64 116C90 96 120 118 150 100S196 84 214 98" fill="none" stroke="#8A5424" stroke-width="2.5" stroke-dasharray="5 4"/>
      <path d="M208 90l12 12M220 90l-12 12" stroke="#E8453C" stroke-width="4" stroke-linecap="round"/>
      <g transform="translate(30 132)"><circle r="13" fill="#fff" stroke="#8A5424" stroke-width="2"/><path d="M0-10L4 0L0 10L-4 0Z" fill="#E8453C"/></g>
      ${cover}</svg>`;
  }
  const mapNote = () => {
    const n = PATH.filter(p => pathDone(p.les)).length;
    return n === PATH.length ? '🎉 اكتملت الخريطة! وجدت كنز جزيرة الحروف!' : `قطع الخريطة: ${n} من ${PATH.length}`;
  };

  // the winding path: one station per letter, a wooden sign at each new مقطع
  function renderPath() {
    const W = 360, pts = [], signs = [];
    let y = 46, prevM = 0;
    PATH.forEach((p, i) => {
      if (p.maqta !== prevM) { signs.push({ y: y - 4, m: p.maqta, i }); y += 70; prevM = p.maqta; }
      pts.push({ x: W / 2 + Math.sin(i * 1.15 + 0.6) * 108, y });
      y += 96;
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
    const cur = PATH.findIndex((p, i) => pathOpen(i) && !pathDone(p.les));
    const pct = (v, t) => (v / t * 100).toFixed(2) + '%';
    let h = `<svg viewBox="0 0 ${W} ${H}" aria-hidden="true">${deco}<path d="${d}" fill="none" stroke="#D2AE62" stroke-width="40" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#F2D9A0" stroke-width="32" stroke-linecap="round"/><path d="${d}" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="2 12" stroke-linecap="round"/></svg>`;
    signs.forEach(sg => {
      const m = MAQATI.find(x => x.n === sg.m), p = pts[sg.i];
      h += `<div class="psign" style="left:${pct(p.x > W / 2 ? W / 2 - 60 : W / 2 + 60, W)};top:${pct(sg.y, H)}">${m ? 'المقطع ' + m.n + `<small>${m.pic} ${m.title}</small>` : 'حروف أخرى'}</div>`;
    });
    PATH.forEach((p, i) => {
      const open = pathOpen(i), done = pathDone(p.les), n = pathStars(p.les), q = pts[i];
      const cls = done ? 'done' : open ? 'open' : 'locked';
      h += `<button type="button" class="pst ${cls}${i === cur ? ' cur' : ''}" data-pst="${i}" style="left:${pct(q.x, W)};top:${pct(q.y, H)}" aria-label="حرف ${p.les.name}${p.page ? '، كتابي صفحة ' + p.page : ''}${open ? '' : '، مقفل'}">`
        + (p.page ? `<span class="pg">ص ${p.page}</span>` : '')
        + `<span class="l">${p.les.letter}</span>`
        + (done ? `<span class="ps">${[0, 1, 2].map(k => STAR(k < n)).join('')}</span>` : open ? '' : '<span class="lock" aria-hidden="true">🔒</span>')
        + '</button>';
    });
    if (cur >= 0) h += `<svg class="pbiko" viewBox="0 0 160 220" style="left:${pct(pts[cur].x + (pts[cur].x > W / 2 ? -62 : 62), W)};top:${pct(pts[cur].y + 34, H)}" aria-hidden="true"><use href="#w-pencil"/></svg>`;
    const trail = $('#pathTrail');
    trail.style.aspectRatio = W + ' / ' + H;
    trail.innerHTML = h;
    $('#pathMap').innerHTML = mapSvg(-1);
    $('#pathMapNote').textContent = mapNote();
    $('#pathHello').textContent = cur >= 0
      ? `أنا بيكو! محطّتك التالية: حرف ${PATH[cur].les.name}${PATH[cur].page ? '، كما في صفحة ' + PATH[cur].page + ' من كتابك' : ''}. كل حرف تكمله يكشف قطعة من الخريطة!`
      : 'أنا بيكو! أكملت كل محطّات الجزيرة. يمكنك أن تعيد أيّ حرف لتجمع نجومًا أكثر.';
    if (cur >= 0) setTimeout(() => { const b = trail.querySelector('.pst.cur'); if (b && S.step === 50) b.scrollIntoView({ block: 'center', behavior: 'smooth' }); }, 450);
  }
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-pst]'); if (!b) return;
    const i = +b.dataset.pst;
    if (!pathOpen(i)) { wreact(b, 'wthink'); say('أَكْمِلِ الْمَحَطَّةَ السَّابِقَةَ أَوَّلًا.'); return; }
    curSubject = 'ar';
    startJourney(PATH[i].les);
  });

  // the end of a journey: keep the best stars, show the new map piece, offer the next station
  function journeyEnd() {
    const jr = FLOW === JOURNEY_FLOW && !L.kind;
    $('#endMap').hidden = !jr; $('#endNext').hidden = true;
    if (!jr) return;
    const total = totalStars(), k = PATH.findIndex(p => p.les === L), fresh = !pathDone(L);
    if (total > (jbest[L.id] || 0)) { jbest[L.id] = total; store('qalami-path', jbest); }
    $('#endMap').innerHTML = `<h3>${fresh ? '🗺️ ربحت قطعة جديدة من خريطة الجزيرة!' : '🗺️ خريطة جزيرة الحروف'}</h3><div class="pmap">${mapSvg(fresh ? k : -1)}</div><p>${mapNote()}</p>`;
    if (fresh) say('رَبِحْتَ قِطْعَةً جَدِيدَةً مِنَ الْخَرِيطَةِ!', true);
    const nx = PATH[k + 1];
    if (nx) {
      const b = $('#endNext');
      b.hidden = false; b.textContent = 'المحطّة التالية: حرف ' + nx.les.name + ' ←';
      b.onclick = () => startJourney(nx.les);
    }
  }

  /* the tracer: follow the road stroke by stroke, from the green dot to the red one; dots are tapped */
  const ptr = { strokes: [], k: 0, down: false, slips: 0, demo: false, size: 60, tol: 6 };
  const NS = 'http://www.w3.org/2000/svg';
  const svgEl = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); Object.entries(attrs).forEach(([a, v]) => e.setAttribute(a, v)); if (parent) parent.appendChild(e); return e; };
  function setupPathTrace() {
    const data = TRACE[L.letter], svg = $('#trSvg');
    $('#trWrap').classList.add('pathmode'); $('#trCheck').hidden = true; $('#trShow').hidden = false;
    cancelAnimationFrame(ptr.raf);
    Object.assign(ptr, { k: 0, down: false, slips: 0, demo: false });
    svg.setAttribute('viewBox', '0 0 100 100');
    svg.innerHTML = '';
    const roads = svgEl('g', {}, svg), inks = svgEl('g', {}, svg);
    ptr.marks = svgEl('g', {}, svg);
    ptr.demoPath = svgEl('path', { class: 'tr-demo', d: '' }, svg);
    ptr.pen = svgEl('svg', { viewBox: '0 0 160 220', style: 'display:none;overflow:visible' }, svg);
    svgEl('use', { href: '#w-pencil' }, ptr.pen);
    ptr.strokes = data.map(st => {
      if (typeof st !== 'string') return { dot: st.dot, road: svgEl('circle', { class: 'tr-road-dot', cx: st.dot[0], cy: st.dot[1], r: 3.4 }, roads), ink: svgEl('circle', { class: 'tr-ink-dot', cx: st.dot[0], cy: st.dot[1], r: 0 }, inks) };
      const road = svgEl('path', { class: 'tr-road', d: st }, roads);
      const len = road.getTotalLength(), pts = [];
      for (let t = 0; t < len; t += 0.6) { const q = road.getPointAtLength(t); pts.push([q.x, q.y]); }
      const e = road.getPointAtLength(len); pts.push([e.x, e.y]);
      const center = svgEl('path', { class: 'tr-center', d: st }, roads);
      const ink = svgEl('path', { class: 'tr-ink', d: st }, inks);
      ink.style.strokeDasharray = len; ink.style.strokeDashoffset = len;
      return { d: st, len, pts, i: 0, road, center, ink };
    });
    // fit the letter to the board
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    ptr.strokes.forEach(st => {
      const bb = st.dot ? { x: st.dot[0] - 3, y: st.dot[1] - 3, width: 6, height: 6 } : st.road.getBBox();
      x0 = Math.min(x0, bb.x); y0 = Math.min(y0, bb.y); x1 = Math.max(x1, bb.x + bb.width); y1 = Math.max(y1, bb.y + bb.height);
    });
    const size = Math.max(42, x1 - x0, y1 - y0) * 1.32, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
    svg.setAttribute('viewBox', `${(cx - size / 2).toFixed(2)} ${(cy - size / 2).toFixed(2)} ${size.toFixed(2)} ${size.toFixed(2)}`);
    Object.assign(ptr, { size, tol: size * 0.085 });
    ptr.strokes.forEach(st => {
      if (st.dot) { st.road.setAttribute('r', size * 0.06); return; }
      st.road.style.strokeWidth = size * 0.13; st.center.style.strokeWidth = size * 0.012; st.center.style.strokeDasharray = `${size * 0.02} ${size * 0.025}`;
      st.ink.style.strokeWidth = size * 0.09;
    });
    ptr.demoPath.style.strokeWidth = size * 0.07;
    ptr.pen.setAttribute('width', size * 0.16); ptr.pen.setAttribute('height', size * 0.22);
    trMarks();
  }
  function trMarks() {
    const g = ptr.marks, st = ptr.strokes[ptr.k], z = ptr.size;
    g.innerHTML = '';
    if (!st) return;
    const num = (x, y) => { svgEl('text', { class: 'tr-num', x, y: y + z * 0.025, 'text-anchor': 'middle', 'font-size': z * 0.07 }, g).textContent = ptr.k + 1; };
    if (st.dot) { svgEl('circle', { class: 'tr-start', cx: st.dot[0], cy: st.dot[1], r: z * 0.055, 'stroke-width': z * 0.012 }, g); num(st.dot[0], st.dot[1]); return; }
    const end = st.pts[st.pts.length - 1], a = st.pts[st.i], b = st.pts[Math.min(st.i + Math.round(z * 0.14 / 0.6), st.pts.length - 1)];
    svgEl('circle', { class: 'tr-end', cx: end[0], cy: end[1], r: z * 0.03, 'stroke-width': z * 0.008 }, g);
    if (b !== a) {
      const ang = Math.atan2(b[1] - a[1], b[0] - a[0]) * 180 / Math.PI, s = z * 0.035;
      svgEl('path', { class: 'tr-arrow', d: `M${s} 0 L${-s * 0.7} ${s * 0.75} L${-s * 0.7} ${-s * 0.75} Z`, transform: `translate(${b[0]} ${b[1]}) rotate(${ang})` }, g);
    }
    svgEl('circle', { class: 'tr-start', cx: a[0], cy: a[1], r: z * 0.055, 'stroke-width': z * 0.012 }, g);
    num(a[0], a[1]);
  }
  const trPos = e => { const svg = $('#trSvg'), p = svg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY; return p.matrixTransform(svg.getScreenCTM().inverse()); };
  const dist = (p, q) => Math.hypot(p.x - q[0], p.y - q[1]);
  function trInk(st) { st.ink.style.strokeDashoffset = st.len * (1 - st.i / (st.pts.length - 1)); }
  function trStrokeDone() {
    const st = ptr.strokes[ptr.k];
    if (st.dot) st.ink.setAttribute('r', ptr.size * 0.05); else { st.i = st.pts.length - 1; trInk(st); }
    ptr.down = false; ptr.slips = 0; ptr.k++;
    good();
    if (ptr.k < ptr.strokes.length) { trMarks(); fb('#ex2Fb', ''); return; }
    trMarks();
    say(L.trace.doneSay);
    finish(3, '#ex2Fb');
  }
  function trSlip() {
    ptr.down = false;
    S.ex[3].m++; ptr.slips++;
    bad();
    const w = $('#trWrap'); w.classList.remove('slip'); void w.offsetWidth; w.classList.add('slip');
    if (ptr.slips >= 2) { ptr.slips = 0; fb('#ex2Fb', 'انظر كيف يرسمه بيكو، ثم جرّب أنت', 'no'); say('اُنْظُرْ كَيْفَ يَرْسُمُهُ بِيكُو، ثُمَّ جَرِّبْ أَنْتَ.'); setTimeout(() => trDemo(ptr.k), 600); }
    else { fb('#ex2Fb', 'اتبع الطريق بإصبعك، وابدأ من النقطة الخضراء', 'no'); say('حاول مرة أخرى'); }
  }
  function trDemo(k) {
    const st = ptr.strokes[k];
    if (!st || ptr.demo || S.step !== 3) return;
    ptr.demo = true;
    const pen = ptr.pen, at = (x, y) => { pen.setAttribute('x', x - ptr.size * 0.05); pen.setAttribute('y', y - ptr.size * 0.22); };
    pen.style.display = '';
    const stop = () => { pen.style.display = 'none'; ptr.demoPath.setAttribute('d', ''); ptr.demo = false; };
    if (st.dot) { at(st.dot[0], st.dot[1]); st.ink.setAttribute('r', ptr.size * 0.05); setTimeout(() => { st.ink.setAttribute('r', 0); stop(); }, 1100); return; }
    ptr.demoPath.setAttribute('d', st.d); ptr.demoPath.style.strokeDasharray = st.len; ptr.demoPath.style.strokeDashoffset = st.len;
    const t0 = performance.now(), dur = Math.min(3600, Math.max(1500, st.len * 28));
    const step = now => {
      const f = Math.min(1, (now - t0) / dur), q = st.pts[Math.round(f * (st.pts.length - 1))];
      at(q[0], q[1]); ptr.demoPath.style.strokeDashoffset = st.len * (1 - f);
      if (f < 1) ptr.raf = requestAnimationFrame(step); else setTimeout(stop, 600);
    };
    ptr.raf = requestAnimationFrame(step);
  }
  $('#trShow').onclick = () => trDemo(ptr.k);
  $('#trSvg').addEventListener('pointerdown', e => {
    const st = ptr.strokes[ptr.k];
    if (!st || ptr.demo || S.ex[3].done) return;
    e.preventDefault();
    const p = trPos(e);
    if (st.dot) { if (dist(p, st.dot) < ptr.tol * 1.6) trStrokeDone(); else { fb('#ex2Fb', 'المس النقطة الخضراء'); } return; }
    if (dist(p, st.pts[st.i]) < ptr.tol * 1.5) { ptr.down = true; $('#trSvg').setPointerCapture(e.pointerId); fb('#ex2Fb', ''); }
    else { fb('#ex2Fb', 'ابدأ من النقطة الخضراء ✋'); say('اِبْدَأْ مِنَ النُّقْطَةِ الْخَضْرَاءِ.'); }
  });
  $('#trSvg').addEventListener('pointermove', e => {
    if (!ptr.down) return;
    const st = ptr.strokes[ptr.k], p = trPos(e), n = st.pts.length, ahead = Math.round(ptr.size * 0.3 / 0.6);
    let hit = -1, near = 1e9;
    for (let j = st.i; j < Math.min(n, st.i + ahead); j++) { const dd = dist(p, st.pts[j]); near = Math.min(near, dd); if (dd < ptr.tol) hit = j; }
    if (hit > st.i) { st.i = hit; trInk(st); trMarks(); }
    if (st.i >= n - 3) trStrokeDone();
    else if (near > ptr.tol * 2.3) trSlip();
  });
  ['pointerup', 'pointercancel'].forEach(t => $('#trSvg').addEventListener(t, () => { ptr.down = false; }));

  /* the underwater fishing: bubbles, sea grass, a submarine with the letter, and a net for each catch */
  function seaDeco() {
    const bubbles = Array.from({ length: 9 }, (_, k) => `<i style="left:${4 + k * 11}%;animation-delay:-${(k * 0.73) % 5}s;animation-duration:${4 + k % 3}s"></i>`).join('');
    return `<div class="sea-deco" aria-hidden="true">${bubbles}<span class="weed w1"></span><span class="weed w2"></span><span class="weed w3"></span>`
      + `<svg class="sub" viewBox="0 0 124 72"><path d="M112 42l10-10v20z" fill="#E8453C" stroke="#18324A" stroke-width="2.5" stroke-linejoin="round"/><ellipse cx="60" cy="44" rx="52" ry="23" fill="#FFC83D" stroke="#18324A" stroke-width="3"/><rect x="46" y="10" width="28" height="18" rx="6" fill="#FFC83D" stroke="#18324A" stroke-width="3"/><path d="M60 10V2h10" fill="none" stroke="#18324A" stroke-width="3" stroke-linecap="round"/><circle cx="40" cy="44" r="13" fill="#E6F7FF" stroke="#18324A" stroke-width="3"/><text x="40" y="51" font-size="19" text-anchor="middle" font-weight="700" font-family="Noto Naskh Arabic, serif" fill="#18324A">${L.letter}</text><circle cx="74" cy="44" r="8" fill="#BFE8FF" stroke="#18324A" stroke-width="3"/><circle cx="96" cy="44" r="5" fill="#BFE8FF" stroke="#18324A" stroke-width="2.5"/></svg></div>`;
  }
  function netAt(it) {
    const n = document.createElement('span');
    n.className = 'net';
    n.style.transform = `translate(${it.x + 16}px, ${it.y - 6}px)`;
    eng.field.appendChild(n);
    setTimeout(() => n.remove(), 750);
  }

  /* the letter check: 3 questions, all with recorded sounds; a wrong answer only greys the option, a hint after two */
  const NOT_IN = { 'أ': 'اأإآءئؤى', 'ت': 'ة', 'ه': 'ة' };
  function lqMake() {
    const mine = L.chars || [L.letter], avoid = mine.join('') + (NOT_IN[L.letter] || '');
    const look = (LOOKALIKE[L.letter] || '').split('').filter(c => PATH.some(p => p.les.letter === c));
    const others = shuffle(PATH.map(p => p.les.letter).filter(c => c !== L.letter && !look.includes(c)));
    const letters = () => shuffle([L.letter, ...[...shuffle(look), ...others].slice(0, 2)]).map(c => ({ t: c, ok: c === L.letter }));
    const qs = [{ prompt: 'استمع واختر الحرف الصحيح.', voice: 'استمع واختر الحرف الصحيح.', say: NAMES[L.letter] || L.letter, opts: letters() }];
    // pictures: one whose name has the letter, two from other letters' lessons that do not
    const yes = shuffle([...L.memory, ...L.forms].filter(x => hasClip(x.w)))[0];
    const seen = new Set([yes && yes.p]), no = [];
    shuffle(LESSONS.filter(l => l !== L).flatMap(l => l.memory || [])).forEach(x => {
      if (no.length < 2 && !seen.has(x.p) && hasClip(x.w) && ![...bare(x.w)].some(c => avoid.includes(c))) { seen.add(x.p); no.push(x); }
    });
    if (yes && no.length === 2) qs.push({ prompt: L.ex1.bubble, say: L.ex1.say, pics: 1, opts: shuffle([{ ...yes, ok: true }, ...no]).map(x => ({ t: x.w, p: x.p, ok: !!x.ok })) });
    // the first letter of a word from the lesson
    const starts = shuffle([...(L.ex4 || []), ...L.forms.filter(f => /أوّل/.test(f.pos))].filter(x => mine.includes(bare(x.w)[0]) && hasClip(x.w)));
    if (starts[0]) qs.push({ prompt: 'بأيّ حرف تبدأ هذه الكلمة؟', voice: 'بأيّ حرف تبدأ هذه الكلمة؟', say: starts[0].w, pic: starts[0].p, opts: letters() });
    while (qs.length < 3) qs.push({ ...qs[0], opts: letters() });
    return qs.slice(0, 3);
  }
  function lqInit() {
    const st = S.ex[51];
    if (st.built) { if (st.done) return; } else { st.built = true; st.qs = lqMake(); st.i = 0; }
    st.qs.forEach(q => { loadClipFor(clipKey(q.say)); q.opts.forEach(o => loadClipFor(clipKey(o.t))); });
    lqQ();
  }
  function lqQ() {
    const st = S.ex[51], q = st.qs[st.i], box = $('#lqOpts');
    st.lock = false; st.wrong = 0;
    $('#lqCount').textContent = (st.i + 1) + ' / ' + st.qs.length;
    $('#lqPrompt').textContent = q.prompt;
    $('#lqPic').textContent = q.pic || '';
    $('#lqSay').dataset.say = q.say;
    fb('#lqFb', '');
    box.innerHTML = '';
    q.opts.forEach(o => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'chip' + (q.pics ? ' pic-btn' : '');
      b.setAttribute('aria-label', o.t);
      b.innerHTML = q.pics ? `<span class="pic" aria-hidden="true">${o.p}</span><span class="word">${o.t}</span>` : `<span class="sym">${o.t}</span>`;
      b.onclick = () => {
        if (st.lock) return;
        if (q.pics) say(o.t);
        if (o.ok) {
          st.lock = true; b.classList.remove('whint'); b.classList.add('is-ok'); good();
          say('أحسنت', true);
          setTimeout(() => { st.i++; st.i < st.qs.length ? lqQ() : finish(51, '#lqFb'); }, 1500);
        } else {
          st.m++; st.wrong++; bad();
          b.classList.add('is-no', 'off');
          say('حاول مرة أخرى', true);
          if (st.wrong >= 2) [...box.children].find((x, k) => q.opts[k].ok).classList.add('whint');
        }
      };
      box.appendChild(b);
    });
    if (q.voice) say(q.voice);
    say(q.say, !!q.voice);
  }
