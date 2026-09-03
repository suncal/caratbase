/* CaratBase — one nav, injected everywhere */
(function(){
  const LINKS=[
    ['index.html',   'Daily'],
    ['value.html',   'Value my diamond'],
    ['vault.html',   'My vault'],
    ['gemstone.html','Gemstones'],
    ['budget.html',  'Budget'],
    ['ring-size.html','Ring size'],
    ['stamp.html',   'Hallmarks'],
    ['metals.html',  'Metal prices'],
    ['size.html',    'Size chart']
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
  nav.innerHTML=LINKS.map(([href,label])=>{
    const on=(href==='index.html'&&(here==='index.html'||here===''))||href===here;
    const b=(href==='vault.html'&&badge)?` <span class="pill" style="padding:1px 8px;font-size:11px">${badge}</span>`:'';
    return `<a href="${href}"${on?' class="on"':''}>${label}${b}</a>`;
  }).join('');
})();
