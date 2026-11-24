# The cannon game (after the user's video), in every lesson that has a letter, a number or words to shoot at.
# Run once:  python3 tools/cannon-patch.py app/www/index.html
import sys

P = sys.argv[1] if len(sys.argv) > 1 else 'app/www/index.html'
s = open(P, encoding='utf-8').read()
assert 'cnInit' not in s, 'already patched'


def rep(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, f'expected {count} match(es), found {n}: {old[:90]!r}'
    s = s.replace(old, new)


rep('''    <!-- 52: the book's sentence''', '''    <!-- 53: the cannon -->
    <section class="screen" data-step="53" hidden>
      <div class="game-top">
        <button type="button" class="btn" data-hub>الألعاب</button>
        <span class="counter">أصبت <span id="cnCount">0 / 6</span></span>
      </div>
      <div class="coach">
        <span class="mascot" data-mascot></span>
        <p class="bubble">المس ما يحمل الحرف المطلوب، فيطلق المدفع!</p>
      </div>
      <div class="field cn-field" id="cnField"></div>
      <div class="done-panel" id="cnDone" hidden></div>
    </section>

    <!-- 52: the book's sentence''')

CSS = r'''
/* ---------- the cannon ---------- */
.cn-field{background:linear-gradient(#36B8F5,#9BDDFF 70%,#CDEFFF);touch-action:manipulation}
.cn-dusk{position:absolute;inset:0;background:linear-gradient(#2B2F7A,#7A4FB0 55%,#FF9A6B);opacity:calc(var(--dusk,0) * .5);transition:opacity 1.2s;pointer-events:none}
.cn-hill{position:absolute;left:-10%;right:-10%;bottom:-40px;height:110px;border-radius:50% 50% 0 0;background:linear-gradient(#8FDB6A,#4FAE3E);pointer-events:none}
.cn-banner{position:absolute;top:8px;left:50%;transform:translateX(-50%);z-index:4;background:linear-gradient(#FF8A6B,#E8453C);color:#fff;border:3px solid #fff;border-radius:14px;padding:2px 16px;font-weight:800;font-size:1rem;white-space:nowrap;box-shadow:0 4px 0 rgba(0,0,0,.2);pointer-events:none}
.cn-banner b{font-family:var(--f-school);font-size:1.4rem;color:#FFE07A;margin-inline-start:6px}
.cn-cliff{position:absolute;right:0;bottom:0;width:min(240px,44%);height:50%;z-index:3;pointer-events:none}
.cn-cliff::before{content:"";position:absolute;inset:auto 0 0 0;height:42%;background:linear-gradient(#5CC85A 0 16%,#C98A4B 16%,#9A6233);border-radius:22px 0 0 0;border-top:4px solid #3E9A3A}
.cn-boy{position:absolute;right:6%;bottom:34%;width:52%;z-index:1;animation:buddysway 2.6s ease-in-out infinite;transform-origin:50% 100%}
.cn-gun{position:absolute;left:-6%;bottom:30%;width:86%;z-index:2;overflow:visible}
#cnBarrel{transition:transform .16s ease-out}
#cnBarrel.kick{animation:cnkick .25s ease-out}
@keyframes cnkick{40%{translate:6px 2px}}
#cnRing{transition:stroke-dasharray .4s}
.cn-badge-on{animation:cnbadge .5s ease}
@keyframes cnbadge{50%{transform:scale(1.5);transform-box:fill-box;transform-origin:center}}
.cn-big{position:absolute;left:50%;top:48%;transform:translate(-50%,-50%);z-index:5;font-family:var(--f-school);font-weight:700;font-size:clamp(4rem,16vw,8rem);line-height:1.2;color:#2E8BEA;filter:drop-shadow(4px 0 0 #fff) drop-shadow(-4px 0 0 #fff) drop-shadow(0 4px 0 #fff) drop-shadow(0 -4px 0 #fff) drop-shadow(0 8px 0 rgba(0,0,0,.15));animation:cnbig .6s cubic-bezier(.2,1.5,.4,1);pointer-events:none;white-space:nowrap}
@keyframes cnbig{from{transform:translate(-50%,-50%) scale(.2);opacity:0}}
.cn-item{position:absolute;left:0;top:0;width:82px;border:0;background:none;padding:0;cursor:pointer;z-index:2;touch-action:manipulation;will-change:transform}
.cn-item.word{width:104px}
.cn-item svg{display:block;width:100%;height:auto;pointer-events:none}
.cn-item.k-cloud{width:110px}.cn-item.k-cloud.word{width:130px}
.cn-item .lt{position:absolute;left:0;right:0;top:34%;transform:translateY(-50%);display:flex;flex-direction:column;align-items:center;font-family:var(--f-school);font-weight:700;font-size:1.9rem;line-height:1.2;color:#18324A;text-shadow:0 0 6px #fff,0 0 3px #fff;pointer-events:none}
.cn-item.k-cloud .lt{top:58%}.cn-item.k-bubble .lt{top:50%}
.cn-item.word .lt{font-size:1.2rem}
.cn-item .lt i{font-style:normal;font-family:var(--f-emoji);font-size:1.6rem;line-height:1}
.cn-item.miss .lt{color:var(--no);animation:shake .4s}
.cn-item.pop{animation:cnpop .38s ease-out forwards}
.cn-item.away{transition:opacity .6s;opacity:0}
@keyframes cnpop{40%{scale:1.3}100%{scale:1.6;opacity:0}}
.cn-ball{position:absolute;left:-9px;top:-9px;width:18px;height:18px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#fff,#FF7A45 40%,#B92D25);z-index:4;pointer-events:none;box-shadow:0 0 10px #FFC83D}
.cn-spark{position:absolute;width:7px;height:7px;border-radius:2px;z-index:3;pointer-events:none;animation:cnspark .6s ease-out forwards}
@keyframes cnspark{to{opacity:0;transform:translate(0,14px) rotate(160deg) scale(.4)}}
.cn-star{position:absolute;z-index:4;font-style:normal;font-size:1.4rem;line-height:1;pointer-events:none;transform:translate(-50%,-50%);animation:cnstar .8s ease-out forwards}
@keyframes cnstar{to{transform:translate(calc(-50% + var(--dx)),calc(-50% + var(--dy))) scale(.6) rotate(120deg);opacity:0}}
.cn-reward{position:absolute;left:0;right:min(240px,44%);top:14%;bottom:20%;z-index:5;display:flex;align-items:center;justify-content:center;gap:4%;pointer-events:none}
.cn-rl{font-family:var(--f-school);font-weight:700;font-size:clamp(3.4rem,13vw,7rem);line-height:1.2;color:#2E8BEA;filter:drop-shadow(4px 0 0 #fff) drop-shadow(-4px 0 0 #fff) drop-shadow(0 4px 0 #fff) drop-shadow(0 -4px 0 #fff);animation:cnbig .7s cubic-bezier(.2,1.5,.4,1)}
.cn-reward img{width:min(30%,150px);height:auto;animation:cnbig .7s cubic-bezier(.2,1.5,.4,1) .25s backwards,castbob 2.4s ease-in-out 1s infinite}
@media (min-aspect-ratio:1/1){.app.scene .cn-field{height:max(220px,100vh - 215px)}}
@media (min-aspect-ratio:1/1) and (max-height:520px){.app:not(.scene) .cn-field{height:max(220px,100vh - 40px)}}
.app.scene [data-step="53"] .cn-field{margin-top:38px}
@media(prefers-reduced-motion:reduce){.cn-boy,.cn-big,.cn-rl,.cn-reward img{animation:none!important}}
</style>'''
rep('</style>\n\n<div class="wbg"', CSS + '\n\n<div class="wbg"')

# the cannon joins the games of every lesson that has something to shoot at
rep("  const LETTER_FLOW = [1, 2, 8, 3, 9, 4, 10, 5, 11, 6];", "  const LETTER_FLOW = [1, 2, 8, 3, 9, 53, 4, 10, 5, 11, 6];")
rep("  const JOURNEY_FLOW = Object.assign([1, 5, 3, 8, 2, 4, 52, 51, 6], { journey: true });", "  const JOURNEY_FLOW = Object.assign([1, 5, 3, 8, 2, 4, 53, 52, 51, 6], { journey: true });")
rep("  const JOURNEY_ICONS = { 1: '👀', 5: '🔤', 3: '✍️', 8: '🎣', 2: '🖼️', 4: '🧩', 52: '📖', 51: '⭐', 6: '🗺️', 10: '🃏' };",
    "  const JOURNEY_ICONS = { 1: '👀', 5: '🔤', 3: '✍️', 8: '🎣', 2: '🖼️', 4: '🧩', 53: '🎯', 52: '📖', 51: '⭐', 6: '🗺️', 10: '🃏' };")
rep("  const SYL_FLOW = [17, 18, 9, 19, 20, 6];", "  const SYL_FLOW = [17, 18, 9, 53, 19, 20, 6];")
rep("  const READ_FLOW = [22, 23, 10, 24, 25, 6];", "  const READ_FLOW = [22, 23, 10, 53, 24, 25, 6];")
rep("  const DICT_FLOW = [28, 29, 10, 30, 6];", "  const DICT_FLOW = [28, 29, 10, 53, 30, 6];")
rep("    FLOW = l.ball ? [40, 41, 9, 42, 6] : l.memory ? [40, 41, 10, 42, 6] : [40, 41, 42, 6];",
    "    FLOW = l.ball ? [40, 41, 9, 53, 42, 6] : l.memory ? [40, 41, 10, 53, 42, 6] : [40, 41, 42, 6];")
rep("    const r = Math.max(j / 21, b / MAX_STARS);", "    const r = Math.max(j / 24, b / MAX_STARS);")
rep("jbest[l.id] ? jbest[l.id] + ' / 21' : 'لم يبدأ'", "jbest[l.id] ? jbest[l.id] + ' / 24' : 'لم يبدأ'")

rep("  function stopEngine() { if (eng.raf) cancelAnimationFrame(eng.raf); eng.raf = 0; }",
    "  function stopEngine() { if (eng.raf) cancelAnimationFrame(eng.raf); eng.raf = 0; cnStop(); }")
rep("    7: renderHub,", "    7: renderHub, 53: () => cnInit(),")
rep("  [8, 9, 10, 11].forEach(k => {", "  [8, 9, 10, 11, 53].forEach(k => {")
# the boy is in the game, so the companion steps aside
rep("    const show = inLesson && FLOW.includes(i);", "    const show = inLesson && FLOW.includes(i) && i !== 53;")

JS = open(__file__.replace('cannon-patch.py', 'cannon.js'), encoding='utf-8').read()
rep('\n  const INIT = {', '\n' + JS + '\n  const INIT = {')

open(P, 'w', encoding='utf-8').write(s)
print('patched', P)
