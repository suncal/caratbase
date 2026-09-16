/* CaratBase — motion system.
   Entry reveals, tweening numbers, cursor-aware cards, a compact header on scroll, and
   chart draw-on. Everything degrades to nothing under prefers-reduced-motion, and nothing
   here changes a single figure — it only changes how figures arrive. */
(function(){
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));

  /* 1 — reveal on scroll: sections and grid children rise into place, staggered */
  // Only things below the fold get hidden-then-revealed. Anything visible at load is
  // never touched, so there is no flash between first paint and this script running.
  const all = $$('main > section, main > .console, main .family, main .mood, main .trust2, main .ml-grid, main .grid, .tool-grid2, .foot-map');
  const below = all.filter(el => el.getBoundingClientRect().top > innerHeight * 0.92);
  if(!reduce){
    below.forEach(el => el.classList.add('rv'));
    $$('.tool-grid2, .grid, .ml-grid, .trust2, .foot-map').forEach(g => { if(!g.classList.contains('rv') && !g.closest('.rv')) return; Array.from(g.children).forEach((c, i) => { c.classList.add('rv-child'); c.style.setProperty('--i', Math.min(i, 8)); }); });
    const io = new IntersectionObserver(es => es.forEach(e => { if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    below.forEach(el => io.observe(el));
  }

  /* 2 — tweening numbers: when a result changes, count from the old figure to the new.
     Each element keeps a small state: the text we last wrote (so we can tell our own
     writes from the app's) and the running frame (so a new value cancels the old run). */
  const NUM = /(-?[\d,]+(?:\.\d+)?)/g;
  const state = new WeakMap();
  function tweenText(el, prev, cur, dur){
    const st = state.get(el) || {}; if(st.raf) cancelAnimationFrame(st.raf);
    const pn = prev.match(NUM) || [], cn = cur.match(NUM) || [];
    if(!pn.length || pn.length !== cn.length){ st.written = cur; state.set(el, st); return; }
    const parts = cur.split(NUM), pairs = [];
    for(let i = 1, k = 0; i < parts.length; i += 2, k++){
      const a = parseFloat(pn[k].replace(/,/g,'')), b = parseFloat(cn[k].replace(/,/g,''));
      const dec = (cn[k].split('.')[1] || '').length;
      if(!isNaN(a) && !isNaN(b) && a !== b) pairs.push({ i, a, b, dec, final: cn[k] });
    }
    if(!pairs.length){ st.written = cur; state.set(el, st); return; }
    const t0 = performance.now();
    const step = now => {
      const p = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      pairs.forEach(q => { parts[q.i] = p < 1 ? (q.a + (q.b - q.a) * e).toLocaleString('en-US', { minimumFractionDigits: q.dec, maximumFractionDigits: q.dec }) : q.final; });
      st.written = parts.join(''); el.textContent = st.written;
      st.raf = p < 1 ? requestAnimationFrame(step) : 0;
    };
    st.raf = requestAnimationFrame(step); state.set(el, st);
  }
  if(!reduce){
    const SEL = '.console-out .big, .console-out .split .v, .trust-bar .n, .showcase .nums b, .result-big, .stat .v';
    $$(SEL).forEach(el => state.set(el, { written: el.textContent, raf: 0 }));
    new MutationObserver(muts => {
      const seen = new Set();
      muts.forEach(m => { const n = m.target.nodeType === 3 ? m.target.parentElement : m.target; const host = n && n.closest && n.closest(SEL); if(host) seen.add(host); });
      seen.forEach(el => {
        const st = state.get(el), cur = el.textContent;
        if(!st){ state.set(el, { written: cur, raf: 0 }); return; }
        if(cur === st.written) return;                 // our own write
        const from = st.written; st.written = cur;     // external write: animate from what was showing
        if(cur.length < 60) tweenText(el, from, cur, 480);
      });
    }).observe(document.body, { subtree: true, childList: true, characterData: true });
  }

  /* 2b — the trust-bar counts up once on arrival */
  if(!reduce){
    $$('.trust-bar .n').forEach((el, i) => {
      const t = el.textContent; if(!NUM.test(t) || /[—–]/.test(t)) return; NUM.lastIndex = 0;
      const zero = t.replace(NUM, m => m.includes('.') ? '0.' + '0'.repeat(m.split('.')[1].length) : '0');
      setTimeout(() => { const st = state.get(el) || {}; st.written = zero; state.set(el, st); tweenText(el, zero, t, 900); }, 200 + i * 90);
    });
    // gold arrives later from the live feed: count from 0 when it lands
    document.addEventListener('cb:spot', () => setTimeout(() => { const el = document.getElementById('tbGold'); if(!el) return; const t = el.textContent; if(!NUM.test(t)) return; NUM.lastIndex = 0; const st = state.get(el) || {}; st.written = '$0'; state.set(el, st); tweenText(el, '$0', t, 900); }, 50), { once: true });
  }

  /* 3 — cursor-aware cards: a few degrees of tilt toward the pointer, nothing more */
  if(!reduce && matchMedia('(hover:hover)').matches){
    $$('.tool2, .showcase, .bn-cta, .stone').forEach(card => {
      card.addEventListener('pointermove', e => {
        const r = card.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        card.style.transform = `perspective(900px) rotateX(${(-y * 3).toFixed(2)}deg) rotateY(${(x * 4).toFixed(2)}deg) translateY(-3px)`;
      });
      card.addEventListener('pointerleave', () => { card.style.transform = ''; });
    });
  }

  /* 4 — compact header once the page has scrolled */
  const head = document.querySelector('.site-head');
  if(head){ let on = false; addEventListener('scroll', () => { const s = scrollY > 40; if(s !== on){ on = s; head.classList.toggle('compact', s); } }, { passive: true }); }

  /* 5 — charts draw on when they arrive */
  if(!reduce){
    const draw = new IntersectionObserver(es => es.forEach(e => { if(!e.isIntersecting) return; $$('path[stroke-width]', e.target).forEach((p, i) => { const L = p.getTotalLength ? p.getTotalLength() : 0; if(!L || L < 50) return; p.style.strokeDasharray = L; p.style.strokeDashoffset = L; p.style.transition = `stroke-dashoffset 1.4s cubic-bezier(.2,.7,.2,1) ${i*120}ms`; requestAnimationFrame(() => requestAnimationFrame(() => { p.style.strokeDashoffset = 0; })); }); draw.unobserve(e.target); }), { threshold: .3 });
    $$('#chart svg').forEach(s => draw.observe(s));
  }

  /* 6 — live dot: the eyebrow on pages that show market data pulses once data arrives */
  document.addEventListener('cb:spot', () => document.body.classList.add('live'));
})();
