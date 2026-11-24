  /* ---------- the cannon game: the boy stands by his cannon; the child touches the things that carry the lesson's
     letter (or number, or word), the cannon turns, fires and bursts them; a ring around the wheel fills, the sky turns
     to evening, and at the end the letter comes back big with a friend ---------- */
  GAMES.cannon = { step: 53, name: 'المدفع', pic: '🎯' };
  EX_NAMES[53] = 'المدفع';
  ENC.cannon = ['هَيَّا نُطْلِقُ الْمِدْفَعَ!'];
  const cn = { raf: 0, items: [], over: true };
  const CN_FRIENDS = ['st-bee', 'st-fish', 'st-dolphin', 'st-turtle', 'st-dog', 'st-cat', 'st-star'];
  const CN_COLORS = ['#E8453C', '#2E8BEA', '#3DBE4F', '#8E5CE6', '#FF9F1C', '#FF5BA7'];
  function cnStop() { if (cn.raf) cancelAnimationFrame(cn.raf); cn.raf = 0; cn.over = true; }
  // what this lesson shoots at: its letter (or syllables, or number), or one of its words
  function cnMode() {
    if (L.targets && L.targets.length) return { kind: 'sym', targets: L.targets, distract: (L.distract || []).filter(x => !L.targets.includes(x)), label: L.kind === 'syl' ? L.targets[0] : L.letter };
    const mem = (L.memory || []).filter(x => x.w);
    if (mem.length >= 3) {
      const t = mem[Math.floor(Math.random() * mem.length)];
      return { kind: 'word', targets: [t.w], distract: mem.filter(x => x.w !== t.w).map(x => x.w), label: t.w, pic: !(L.kind === 'read' || L.kind === 'dict') ? Object.fromEntries(mem.map(x => [x.w, x.p])) : null };
    }
    return null;
  }
  const CANNON = label => `<svg class="cn-gun" viewBox="0 0 170 130" aria-hidden="true">
    <defs><linearGradient id="cnRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF8A6B"/><stop offset=".5" stop-color="#E8453C"/><stop offset="1" stop-color="#A92620"/></linearGradient></defs>
    <g id="cnBarrel" transform="rotate(28 108 74)">
      <path d="M30 56 L112 60 Q124 74 112 88 L30 92 Z" fill="url(#cnRed)" stroke="#6E1712" stroke-width="3" stroke-linejoin="round"/>
      <rect x="10" y="48" width="24" height="52" rx="9" fill="#FFC83D" stroke="#9A6A00" stroke-width="3"/>
      <rect x="58" y="57" width="10" height="34" rx="3" fill="#FFC83D" stroke="#9A6A00" stroke-width="2"/>
      <ellipse cx="12" cy="74" rx="5" ry="20" fill="#3A1410"/>
      <circle id="cnMuzzle" cx="10" cy="74" r="1" fill="none"/>
    </g>
    <path d="M78 112 L100 70 L138 70 L150 112 Z" fill="#B9783A" stroke="#6B3D17" stroke-width="3" stroke-linejoin="round"/>
    <circle cx="118" cy="100" r="26" fill="#8A5424" stroke="#5A3410" stroke-width="3"/>
    <circle cx="118" cy="100" r="20" fill="#fff" stroke="#E6EEF3" stroke-width="2"/>
    <circle id="cnRing" cx="118" cy="100" r="20" fill="none" stroke="#3DBE4F" stroke-width="5" stroke-linecap="round" transform="rotate(-90 118 100)" stroke-dasharray="0 126"/>
    <text id="cnBadge" x="118" y="108" text-anchor="middle" font-size="${[...label].length > 3 ? 11 : 22}" font-weight="700" font-family="Noto Naskh Arabic, serif" fill="#18324A">${label}</text>
  </svg>`;
  const CN_SHAPE = {
    bubble: c => `<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="rgba(255,255,255,.35)" stroke="rgba(255,255,255,.95)" stroke-width="4"/><path d="M28 34 Q36 22 50 20" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/><circle cx="50" cy="50" r="44" fill="none" stroke="${c}" stroke-width="2" opacity=".5"/></svg>`,
    balloon: c => `<svg viewBox="0 0 100 130"><path d="M50 100 q-8 12 0 26" fill="none" stroke="#18324A" stroke-width="2"/><path d="M44 96 L56 96 L50 104 Z" fill="${c}"/><ellipse cx="50" cy="50" rx="40" ry="48" fill="${c}" stroke="rgba(0,0,0,.25)" stroke-width="2"/><ellipse cx="34" cy="30" rx="8" ry="13" fill="#fff" opacity=".45"/></svg>`,
    hot: c => `<svg viewBox="0 0 100 130"><path d="M50 4 C10 4 4 44 26 70 L38 90 L62 90 L74 70 C96 44 90 4 50 4Z" fill="${c}" stroke="rgba(0,0,0,.25)" stroke-width="2"/><path d="M50 4 C34 4 30 44 40 70 L44 90 M50 4 C66 4 70 44 60 70 L56 90" fill="none" stroke="#FFC83D" stroke-width="7"/><path d="M40 90 L42 104 M60 90 L58 104" stroke="#6B3D17" stroke-width="2"/><rect x="38" y="102" width="24" height="18" rx="3" fill="#B9783A" stroke="#6B3D17" stroke-width="2"/></svg>`,
    cloud: () => `<svg viewBox="0 0 130 80"><path d="M24 70 C4 70 4 44 24 42 C22 20 50 12 62 28 C70 10 102 14 102 38 C124 38 126 70 104 70 Z" fill="#fff" stroke="#DCEAF5" stroke-width="3"/></svg>`
  };
  function cnInit() {
    cnStop();
    const field = $('#cnField'), mode = cnMode();
    $('#cnDone').hidden = true;
    if (!mode) { field.hidden = true; if (inLesson) { Object.assign(S.ex[53], { done: true, stars: 3, m: 0 }); nextBtn.disabled = false; autoNext(53); } return; }
    field.hidden = false;
    Object.assign(cn, { field, mode, items: [], hits: 0, m: 0, goal: 6, over: false, ready: false, last: performance.now(), next: 0 });
    field.style.setProperty('--dusk', 0);
    const lab = mode.kind === 'word' ? 'كلمة' : L.kind === 'math' ? 'العدد' : L.kind === 'syl' ? 'المقطع' : 'حرف';
    $('[data-step="53"] .coach .bubble').textContent = 'المس ما يحمل ' + (mode.kind === 'word' ? 'الكلمة المطلوبة' : L.kind === 'math' ? 'العدد المطلوب' : L.kind === 'syl' ? 'المقطع المطلوب' : 'الحرف المطلوب') + '، فيطلق المدفع!';
    field.innerHTML = `<div class="cn-dusk"></div><div class="cn-hill"></div>
      <div class="cn-banner">أطلق المدفع على ${lab} <b>${mode.label}</b></div>
      <div class="cn-cliff"><img class="cn-boy" id="cnBoy" src="img/boy-wink.webp" alt="">${CANNON(mode.label)}</div>
      <div class="cn-big" id="cnBig">${mode.label}</div>`;
    $('#cnCount').textContent = '0 / ' + cn.goal;
    if (!inLesson && field.getBoundingClientRect().bottom > innerHeight) setTimeout(() => field.scrollIntoView({ block: 'end', behavior: 'smooth' }), 350);
    // the letter shows big, then flies into the cannon's wheel
    const big = $('#cnBig'), badge = $('#cnBadge');
    setTimeout(() => {
      if (cn.field !== field || cn.over) return;
      const a = big.getBoundingClientRect(), b = badge.getBoundingClientRect();
      big.animate([{ transform: 'translate(-50%,-50%) scale(1)', opacity: 1 }, { transform: `translate(calc(-50% + ${b.x + b.width / 2 - a.x - a.width / 2}px), calc(-50% + ${b.y + b.height / 2 - a.y - a.height / 2}px)) scale(.12)`, opacity: .6 }], { duration: 700, easing: 'cubic-bezier(.5,0,.6,1)', fill: 'forwards' });
      setTimeout(() => { big.remove(); badge.classList.add('cn-badge-on'); cn.ready = true; cnFace('cheer', 900); }, 720);
    }, 1300);
    enc('cannon', { show: false, queued: false });
    if (mode.kind === 'word') say(mode.label, true);
    else if (L.kind === 'math') numSay(+L.letter).forEach(x => say(x, true));
    else if (L.kind === 'syl') say(L.balloon.say, true);
    else if (NAMES[L.letter]) say(NAMES[L.letter], true);
    cn.raf = requestAnimationFrame(cnTick);
  }
  function cnFace(face, ms) {
    const im = $('#cnBoy'); if (!im) return;
    im.src = `img/boy-${face}.webp`;
    clearTimeout(cnFace.t);
    if (ms) cnFace.t = setTimeout(() => { if ($('#cnBoy')) $('#cnBoy').src = 'img/boy-wink.webp'; }, ms);
  }
  function cnSpawn() {
    const f = cn.field, W = f.clientWidth, H = f.clientHeight, gunW = Math.min(200, W * 0.32);
    const shown = cn.items.filter(o => o.t && !o.busy).length;
    const t = shown < 2 || Math.random() < 0.42;
    const pool = t ? cn.mode.targets : cn.mode.distract.length ? cn.mode.distract : cn.mode.targets;
    const label = pool[Math.floor(Math.random() * pool.length)];
    const kinds = cn.mode.kind === 'word' ? ['bubble', 'balloon', 'cloud', 'hot'] : ['bubble', 'balloon', 'hot', 'cloud', 'bubble', 'balloon'];
    const kind = kinds[Math.floor(Math.random() * kinds.length)];
    const it = { t: cn.mode.targets.includes(label), label, kind, phase: Math.random() * 6 };
    const el = document.createElement('button');
    el.type = 'button';
    el.className = 'cn-item k-' + kind + (cn.mode.kind === 'word' ? ' word' : '');
    el.setAttribute('aria-label', label);
    const pic = cn.mode.pic && cn.mode.pic[label];
    el.innerHTML = CN_SHAPE[kind](CN_COLORS[Math.floor(Math.random() * CN_COLORS.length)]) + `<span class="lt">${pic ? `<i>${pic}</i>` : ''}${label}</span>`;
    el.addEventListener('pointerdown', e => { e.preventDefault(); cnHit(it); });
    f.appendChild(el);
    it.el = el;
    const size = cn.mode.kind === 'word' ? 104 : 82;
    if (kind === 'cloud') { it.x = -size - 10; it.y = 18 + Math.random() * H * 0.28; it.vx = 26 + Math.random() * 18; it.vy = 0; }
    else { it.x = 8 + Math.random() * Math.max(20, W - gunW - size - 20); it.y = H + 10; it.vx = 0; it.vy = -(30 + Math.random() * 22); }
    it.size = size;
    cn.items.push(it);
  }
  function cnTick(now) {
    if (cn.over && !cn.items.length) return;
    const dt = Math.min(0.05, (now - cn.last) / 1000); cn.last = now;
    const f = cn.field, W = f.clientWidth, gunW = Math.min(240, W * 0.44);
    if (cn.ready && !cn.over && now > cn.next && cn.items.filter(o => !o.busy).length < 6) { cnSpawn(); cn.next = now + 900 + Math.random() * 700; }
    cn.items = cn.items.filter(it => {
      if (it.busy) return true;
      it.phase += dt * 2;
      it.x += it.vx * dt + (it.kind === 'cloud' ? 0 : Math.sin(it.phase) * 0.4);
      it.y += it.vy * dt + (it.kind === 'cloud' ? Math.sin(it.phase) * 0.2 : 0);
      if (it.y < -it.size * 1.4 || it.x > W - gunW - 40 && it.kind === 'cloud') { it.el.remove(); return false; }
      it.el.style.transform = `translate(${it.x}px, ${it.y}px)`;
      return true;
    });
    if (!cn.over || cn.items.length) cn.raf = requestAnimationFrame(cnTick);
  }
  function cnHit(it) {
    if (it.busy || cn.over || !cn.ready) return;
    if (!it.t) {
      cn.m++; bad(); cnFace('think', 1000);
      it.el.classList.remove('miss'); void it.el.offsetWidth; it.el.classList.add('miss');
      return;
    }
    it.busy = true;
    const f = cn.field.getBoundingClientRect(), r = it.el.getBoundingClientRect();
    const tx = r.x + r.width / 2 - f.x, ty = r.y + r.height / 2 - f.y;
    // turn the barrel towards the target, then fire
    const piv = $('#cnBarrel').ownerSVGElement, pm = piv.getScreenCTM(), pt = piv.createSVGPoint(); pt.x = 108; pt.y = 74;
    const p = pt.matrixTransform(pm), ang = Math.max(-8, Math.min(80, Math.atan2(-(ty + f.y - p.y), -(tx + f.x - p.x)) * 180 / Math.PI));
    $('#cnBarrel').setAttribute('transform', `rotate(${ang.toFixed(1)} 108 74)`);
    setTimeout(() => {
      const mz = $('#cnMuzzle').getBoundingClientRect(), mx = mz.x - f.x, my = mz.y - f.y;
      const ball = document.createElement('span'); ball.className = 'cn-ball';
      ball.style.transform = `translate(${mx}px, ${my}px)`;
      cn.field.appendChild(ball);
      tone([150, 90], 0.09);
      $('#cnBarrel').classList.remove('kick'); void $('#cnBarrel').getBoundingClientRect(); $('#cnBarrel').classList.add('kick');
      ball.animate([{ transform: `translate(${mx}px, ${my}px) scale(.6)` }, { transform: `translate(${tx}px, ${ty}px) scale(1)` }], { duration: 320, easing: 'cubic-bezier(.3,.6,.5,1)', fill: 'forwards' });
      for (let k = 0; k < 6; k++) setTimeout(() => cnSpark(mx + (tx - mx) * k / 6, my + (ty - my) * k / 6), k * 45);
      setTimeout(() => { ball.remove(); cnBurst(it, tx, ty); }, 320);
    }, 160);
  }
  function cnSpark(x, y) {
    const s = document.createElement('i'); s.className = 'cn-spark';
    s.style.left = x + 'px'; s.style.top = y + 'px'; s.style.background = CN_COLORS[Math.floor(Math.random() * CN_COLORS.length)];
    cn.field.appendChild(s); setTimeout(() => s.remove(), 600);
  }
  function cnBurst(it, x, y) {
    it.el.classList.add('pop');
    setTimeout(() => { it.el.remove(); cn.items = cn.items.filter(o => o !== it); }, 380);
    for (let k = 0; k < 10; k++) {
      const s = document.createElement('i'); s.className = 'cn-star'; s.textContent = k % 3 ? '★' : '✦';
      const a = Math.PI * 2 * k / 10;
      s.style.left = x + 'px'; s.style.top = y + 'px'; s.style.color = CN_COLORS[k % CN_COLORS.length];
      s.style.setProperty('--dx', Math.cos(a) * (40 + Math.random() * 30) + 'px'); s.style.setProperty('--dy', Math.sin(a) * (40 + Math.random() * 30) + 'px');
      cn.field.appendChild(s); setTimeout(() => s.remove(), 800);
    }
    good(); cnFace('cheer', 1000);
    cn.hits++;
    $('#cnCount').textContent = cn.hits + ' / ' + cn.goal;
    $('#cnRing').setAttribute('stroke-dasharray', `${(126 * cn.hits / cn.goal).toFixed(1)} 126`);
    cn.field.style.setProperty('--dusk', (cn.hits / cn.goal).toFixed(2));
    if (cn.hits % 2 === 0 && cn.hits < cn.goal) enc('catch', { show: false });
    if (cn.hits >= cn.goal) cnEnd();
  }
  function cnEnd() {
    cn.over = true;
    cn.items.forEach(o => { o.busy = true; o.el.classList.add('away'); });
    setTimeout(() => { cn.items.forEach(o => o.el.remove()); cn.items = []; }, 700);
    const friend = CN_FRIENDS[Math.floor(Math.random() * CN_FRIENDS.length)];
    const rw = document.createElement('div'); rw.className = 'cn-reward';
    rw.innerHTML = `<span class="cn-rl">${cn.mode.label}</span><img src="img/${friend}.webp" alt="">`;
    cn.field.appendChild(rw);
    cnFace('cheer'); fanfare(); celebrate(encPick('allCaught', 'praise'));
    setTimeout(() => {
      if (S.step !== 53 && !cn.field.isConnected) return;
      cn.field.hidden = true;
      showDone('cannon', cn.m, '#cnDone', cn.m);
    }, 2600);
  }
