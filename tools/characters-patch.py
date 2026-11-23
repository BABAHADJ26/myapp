# Replace the placeholder SVG characters with the user's own character art (app/www/img/*.webp,
# cut out of the user's "Smart Kids World" design board), everywhere in the app:
# Lumi (lion), Biko (pencil), Boni (rabbit), Oli (owl), the child avatar; expressions change when the child succeeds.
# Run once:  python3 tools/characters-patch.py app/www/index.html
import sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/www/index.html'
s = open(P, encoding='utf-8').read()
assert 'img/lumi.webp' not in s, 'already patched'


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f'expected {count} match(es), found {n}: {old[:90]!r}'
    s = s.replace(old, new)


IMG = lambda name, extra='': f'<img src="img/{name}.webp" alt="" draggable="false"{extra}>'

rep('<div class="cast l"><svg viewBox="0 0 200 220" id="castL"><use href="#w-lion"/></svg></div><div class="cast r"><svg viewBox="0 0 160 220" id="castR"><use href="#w-pencil"/></svg></div>',
    '<div class="cast l">' + IMG('lumi', ' id="castL"') + '</div><div class="cast r">' + IMG('biko', ' id="castR"') + '</div>')
rep('<span class="av"><svg viewBox="0 0 160 220" width="40" height="40"><use href="#w-pencil"/></svg></span>',
    '<span class="av">' + IMG('girl-face') + '</span>')
rep('<svg viewBox="0 0 200 220" class="gch" id="whLion"><use href="#w-lion"/></svg>', IMG('lumi', ' class="gch" id="whLion"'))
rep('<svg viewBox="0 0 160 220" class="gch"><use href="#w-pencil"/></svg>', IMG('biko', ' class="gch"'), 2)
rep('<svg viewBox="0 0 200 220" class="gch"><use href="#w-lion"/></svg>', IMG('lumi', ' class="gch"'), 2)
rep('<svg viewBox="0 0 180 230" class="gch"><use href="#w-rabbit"/></svg>', IMG('boni', ' class="gch"'))
rep('<svg viewBox="0 0 180 220" class="gch"><use href="#w-owl"/></svg>', IMG('oli', ' class="gch"'))
rep('''<svg class="pbiko" viewBox="0 0 160 220" style="left:${pct(pts[cur].x + (pts[cur].x > W / 2 ? -62 : 62), W)};top:${pct(pts[cur].y + 34, H)}" aria-hidden="true"><use href="#w-pencil"/></svg>''',
    '''<img class="pbiko" src="img/biko.webp" alt="" style="left:${pct(pts[cur].x + (pts[cur].x > W / 2 ? -62 : 62), W)};top:${pct(pts[cur].y + 34, H)}">''')
rep("    svgEl('use', { href: '#w-pencil' }, ptr.pen);",
    "    svgEl('image', { href: 'img/biko.webp', width: 160, height: 220, preserveAspectRatio: 'xMidYMax meet' }, ptr.pen);")

# the small coach mascot: the subject's guide (Biko by default)
i = s.index('  const MASCOT = `<svg viewBox="0 0 80 130"')
j = s.index('</svg>`;', i) + len('</svg>`;')
s = s[:i] + '  const MASCOT = `<img src="img/biko.webp" alt="" draggable="false" class="mimg">`;' + s[j:]

# the result screen: Lumi laughing
rep('<span class="mascot" data-mascot style="width:84px"></span>', IMG('lumi-happy', ' class="end-hero"'))

CSS = r'''
/* ---------- the characters (the user's art) ---------- */
img.gch,.scene-cast .cast img,.mascot img,.pbiko,.end-hero{user-select:none;-webkit-user-select:none;-webkit-user-drag:none}
.wh-hero img.gch{width:min(100%,250px);height:auto;filter:drop-shadow(0 10px 6px rgba(0,60,0,.25))}
.guide img.gch{width:100px;height:auto;flex:none;filter:drop-shadow(0 6px 4px rgba(0,0,0,.18))}
.wh-hero img.gch,.guide img.gch{animation:castbob 3s ease-in-out infinite}
.scene-cast .cast img{width:100%;height:auto;display:block;filter:drop-shadow(0 8px 4px rgba(0,60,0,.25))}
.mascot img{width:100%;height:auto;display:block}
.wh-me .av img{width:100%;height:100%;object-fit:cover}
.pbiko{height:auto}
.end-hero{width:min(46vw,190px);height:auto;align-self:center;animation:endhero 1s cubic-bezier(.2,1.5,.4,1),castbob 3s ease-in-out 1s infinite}
@keyframes endhero{from{transform:scale(.2) rotate(-20deg);opacity:0}}
.wpop-char{position:fixed;bottom:-10px;width:min(34vw,170px);z-index:26;pointer-events:none;animation:wpopchar 2.6s ease-in-out forwards}
.wpop-char.l{left:2vw}.wpop-char.r{right:2vw}
@keyframes wpopchar{0%{transform:translateY(110%)}18%,78%{transform:translateY(0)}30%{transform:translateY(-14px) rotate(-4deg)}42%{transform:translateY(0) rotate(3deg)}100%{transform:translateY(110%)}}
@media(max-width:700px){.wh-hero img.gch{width:150px}.guide img.gch{width:80px}}
@media(prefers-reduced-motion:reduce){.wh-hero img.gch,.guide img.gch,.end-hero,.wpop-char{animation:none!important}}
</style>'''
rep('</style>\n\n<div class="wbg"', CSS + '\n\n<div class="wbg"')

# expressions: Lumi laughs and Biko winks when the child succeeds; a character pops up to cheer outside the scene too
rep("  function castReact(cls) { if ($('.app').classList.contains('scene')) { wreact($('#castL'), cls); setTimeout(() => wreact($('#castR'), cls), 150); } }",
    '''  const FACES = { castL: ['img/lumi.webp', 'img/lumi-happy.webp'], castR: ['img/biko.webp', 'img/biko-wink.webp'] };
  function castReact(cls) {
    if (!$('.app').classList.contains('scene')) return;
    ['castL', 'castR'].forEach((id, k) => setTimeout(() => {
      const el = $('#' + id);
      if (cls === 'whappy') { el.src = FACES[id][1]; clearTimeout(el.t); el.t = setTimeout(() => { el.src = FACES[id][0]; }, 1800); }
      wreact(el, cls);
    }, k * 150));
  }
  // the guide of each subject coaches its lessons
  const GUIDE_IMG = { math: 'boni', sci: 'oli', isl: 'lumi', civ: 'lumi' };
  function setCoach() { const src = 'img/' + (GUIDE_IMG[curSubject] || 'biko') + '.webp'; $$('.coach .mascot img').forEach(im => { if (!im.src.endsWith(src)) im.src = src; }); }
  function popChar() {
    if ($('.app').classList.contains('scene') || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const pick = [['lumi-happy', 'l'], ['biko-wink', 'r'], ['girl', 'r'], ['boni', 'l'], ['oli', 'r']][Math.floor(Math.random() * 5)];
    const im = document.createElement('img'); im.src = `img/${pick[0]}.webp`; im.alt = ''; im.className = 'wpop-char ' + pick[1];
    document.body.appendChild(im); setTimeout(() => im.remove(), 2700);
  }''')
rep("    const sc = curScreen(); if (sc) wreact(sc.querySelector('.coach .mascot, .gch'), 'whappy');\n    castReact('whappy');",
    "    const sc = curScreen(); if (sc) wreact(sc.querySelector('.coach .mascot, .gch'), 'whappy');\n    castReact('whappy'); popChar();")
rep("    if (scene && !wasScene) setTimeout(() => castReact('whappy'), 300);",
    "    if (scene && !wasScene) setTimeout(() => castReact('whappy'), 300);\n    setCoach();")

open(P, 'w', encoding='utf-8').write(s)
print('patched', P)
