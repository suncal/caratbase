/* CaratBase — one nav, injected everywhere */
(function(){
  /* Grouped, not a flat list. Ten tools appended one at a time had grown into ten
     top-level links that wrapped onto a second row and collided with the ticker. Four
     groups scale as more tools arrive; the mobile sheet flattens them back out with
     headings, which reads better on a phone than nesting would. */
  const GROUPS=[
    {label:'Value',   items:[
      ['value.html',    'Diamonds & jewellery'],
      ['gemstone.html', 'Gemstones & pearls'],
      ['metals.html',   'Gold & metal prices'],
      ['budget.html',   'What my budget buys']]},
    {label:'Buy',     items:[
      ['compare.html',                'Compare two diamonds'],
      ['lab-vs-natural.html',         'Lab-grown vs natural'],
      ['engagement-ring-budget.html', 'How much to spend'],
      ['diamond-price-per-carat.html','Price per carat'],
      ['diamond-color-chart.html',    'Colour chart'],
      ['diamond-clarity-chart.html',  'Clarity chart']]},
    {label:'Measure', items:[
      ['measure.html',  'From a photo'],
      ['ring-size.html','Ring size'],
      ['size.html',     'Carat & shape sizes'],
      ['stamp.html',    'Hallmarks'],
      ['birthstones.html','Birthstones']]},
    {label:'My vault', href:'vault.html'},
    {label:'All tools', href:'tools.html'}
  ];

  const here=(location.pathname.split('/').pop()||'index.html');
  const nav=document.querySelector('nav.nav'); if(!nav) return;

  /* On a phone eight links cannot sit in a header bar — they wrap over the logo and
     collide with the ticker. A toggle plus a sheet is the only thing that fits. */
  const head=nav.parentElement;
  if(head && !head.querySelector('.navbtn')){
    const btn=document.createElement('button');
    btn.className='navbtn'; btn.type='button';
    btn.setAttribute('aria-label','Menu');
    btn.setAttribute('aria-expanded','false');
    btn.innerHTML='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" '+
      'stroke="currentColor" stroke-width="1.9" stroke-linecap="round">'+
      '<path d="M3 6h18M3 12h18M3 18h18"/></svg>';
    head.insertBefore(btn, nav);
    /* search: one button, every page */
    if(!head.querySelector('.navsearch')){
      const sb=document.createElement('button'); sb.className='navsearch'; sb.type='button';
      sb.setAttribute('aria-label','Search'); sb.title='Search (⌘K)';
      sb.innerHTML='<svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>';
      sb.addEventListener('click',()=>{ if(window.cbSearch) cbSearch.open(); });
      head.insertBefore(sb, btn);
      if(!document.querySelector('script[src*="assets/search.js"]')){
        const sc=document.createElement('script'); const me=document.querySelector('script[src*="assets/nav.js"]');
        sc.src=(me?me.src.replace(/nav\.js.*$/,'search.js'):'assets/search.js'); document.body.appendChild(sc);
      }
    }
    const isMobile=()=>matchMedia('(max-width:900px)').matches;
    const close=()=>{
      nav.classList.remove('open');
      btn.setAttribute('aria-expanded','false');
    };
    const open=()=>{
      nav.classList.add('open');
      btn.setAttribute('aria-expanded','true');
    };
    btn.addEventListener('click',e=>{
      e.stopPropagation();
      nav.classList.contains('open') ? close() : open();
    });
    // a rotation back to desktop must not leave the sheet in a half-open state
    addEventListener('resize',()=>{ if(!isMobile()) close(); });
    nav.addEventListener('click',e=>{ if(e.target.closest('a')) close(); });
    document.addEventListener('click',e=>{
      if(nav.classList.contains('open') && !nav.contains(e.target)) close();
    });
    document.addEventListener('keydown',e=>{ if(e.key==='Escape') close(); });
  }
  let badge=0;
  try{ badge=JSON.parse(localStorage.getItem('cb_vault')||'[]').length }catch{}
  const isHere=h => h===here || (h==='index.html' && (here===''||here==='index.html'));

  nav.innerHTML = GROUPS.map((g,gi)=>{
    if(g.href){
      const b=(g.href==='vault.html'&&badge)
        ? ` <span class="pill" style="padding:1px 8px;font-size:11px">${badge}</span>` : '';
      return `<a href="${g.href}"${isHere(g.href)?' class="on"':''}>${g.label}${b}</a>`;
    }
    const active=g.items.some(([h])=>isHere(h));
    return `<div class="navgroup" data-g="${gi}">
      <button type="button" class="navtop${active?' on':''}" aria-expanded="false">
        ${g.label}<svg width="10" height="10" viewBox="0 0 12 8" fill="none"
          stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M1 1.5 6 6.5 11 1.5"/></svg>
      </button>
      <div class="navmenu">${g.items.map(([h,t])=>
        `<a href="${h}"${isHere(h)?' class="on"':''}>${t}</a>`).join('')}</div>
    </div>`;
  }).join('');

  /* Open and close by setting styles directly. Hover for pointers, click for touch and
     keyboard — one code path, no cascade to argue with. */
  const groups=[...nav.querySelectorAll('.navgroup')];
  const show=g=>{
    const m=g.querySelector('.navmenu');
    m.style.opacity='1'; m.style.visibility='visible';
    m.style.transform='translateX(-50%) translateY(2px)';
    g.classList.add('open');
    g.querySelector('.navtop').setAttribute('aria-expanded','true');
  };
  const hide=g=>{
    const m=g.querySelector('.navmenu');
    // on mobile the panel is always laid out inline, so leave it alone there
    if(matchMedia('(max-width:900px)').matches) return;
    m.style.opacity=''; m.style.visibility=''; m.style.transform='';
    g.classList.remove('open');
    g.querySelector('.navtop').setAttribute('aria-expanded','false');
  };
  const hideAll=except=>groups.forEach(g=>{ if(g!==except) hide(g); });

  groups.forEach(g=>{
    const btn=g.querySelector('.navtop');
    g.addEventListener('mouseenter',()=>{ if(!matchMedia('(max-width:900px)').matches){ hideAll(g); show(g); } });
    g.addEventListener('mouseleave',()=>hide(g));
    btn.addEventListener('click',e=>{
      e.preventDefault(); e.stopPropagation();
      if(matchMedia('(max-width:900px)').matches) return;   // sheet shows everything already
      const open=g.classList.contains('open');
      hideAll(); open ? hide(g) : show(g);
    });
    btn.addEventListener('keydown',e=>{
      if(e.key==='Escape'){ hide(g); btn.blur(); }
    });
  });
  document.addEventListener('click',()=>hideAll());
  addEventListener('resize',()=>hideAll());

})();

/* ---------- footer site map: rendered once, everywhere ---------- */
(function(){
  const foot=document.querySelector('footer.site-foot'); if(!foot || foot.querySelector('.foot-map')) return;
  const me=document.querySelector('script[src*="assets/nav.js"]'); const root=me?me.src.replace(/assets\/nav\.js.*$/,''):'/';
  const L=(u,t)=>`<a href="${root}${u}">${t}</a>`;
  const cols=[
    ['Value',['value.html','Diamond & jewellery'],['gemstone.html','Gemstones & pearls'],['metals.html','Gold & metal prices'],['stamp.html','Hallmark lookup'],['vault.html','My vault']],
    ['Buy',['budget.html','What my budget buys'],['compare.html','Compare two diamonds'],['lab-vs-natural.html','Lab-grown vs natural'],['engagement-ring-budget.html','How much to spend'],['diamond-price-per-carat.html','Price per carat'],['diamond-color-chart.html','Colour chart'],['diamond-clarity-chart.html','Clarity chart']],
    ['Measure',['ring-size.html','Ring sizer'],['measure.html','From a photo'],['size.html','Carat size chart'],['ring-size/','Ring size charts'],['diamond/','Sizes by carat & shape']],
    ['Reference',['birthstones.html','Birthstones'],['insurance-cost.html','Insurance cost'],['hallmark/','Hallmarks explained'],['gold-price/','Gold price by karat'],['gemstone/','Gemstone values'],['widgets.html','Free widgets'],['methodology.html','How we value'],['about.html','About']],
  ];
  const map=document.createElement('div'); map.className='wrap';
  map.innerHTML='<div class="foot-map"><div><div class="tag">CaratBase</div><p>The independent jewellery reference. Every number shown working; no account, no tracking.</p></div>'
    + cols.map(c=>'<div><h4>'+c[0]+'</h4>'+c.slice(1).map(x=>L(x[0],x[1])).join('')+'</div>').join('') + '</div>';
  foot.insertBefore(map, foot.firstChild);
})();
