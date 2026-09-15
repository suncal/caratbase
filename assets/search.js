/* CaratBase — site search. Loads the index on first use, matches on title, description and
   keywords, and ranks tools above reference pages. No server, no tracking of the query. */
(function(){
  let index=null, box=null, input=null, res=null, sel=0, loading=null;
  const ROOT=(function(){ const s=document.currentScript&&document.currentScript.src||''; const m=s.match(/^(.*?)assets\/search\.js/); return m?m[1]:'/'; })();

  function load(){
    if(index) return Promise.resolve(index);
    if(loading) return loading;
    loading=fetch(ROOT+'assets/search-index.json',{cache:'force-cache'}).then(r=>r.json()).then(d=>{index=d; return d;});
    return loading;
  }
  const norm=s=>s.toLowerCase().replace(/[^a-z0-9.½ ]+/g,' ').replace(/\s+/g,' ').trim();
  const words=s=>norm(s).split(' ').filter(Boolean);
  /* a query token matches a word exactly, or as a prefix when it is a word of 3+ letters;
     numbers must match exactly so "7" never matches "0.75" or "17" */
  function hit(tok, ws){
    const num=/^[\d.½]+$/.test(tok);
    for(const w of ws){ if(w===tok) return 2; if(!num && tok.length>=3 && w.startsWith(tok)) return 1; }
    return 0;
  }
  function score(q, it){
    const toks=words(q); if(!toks.length) return 0;
    const T=words(it.t), K=words(it.k||''), D=words(it.d||'');
    let s=0;
    if(norm(it.t)===norm(q)) s+=100;
    for(const tk of toks){
      const a=hit(tk,T), b=hit(tk,K), c=hit(tk,D);
      if(a) s+=14*a; else if(b) s+=9*b; else if(c) s+=3*c; else return 0;
    }
    if(it.g==='tool') s+=6;
    if(it.g==='ring size' && toks.some(t=>/^[\d.½]+$/.test(t))) s+=4;   /* a bare number is usually a ring size */
    return s - Math.min(6, T.length/4);  /* shorter, more specific titles first */
  }
  function render(q){
    if(!index) return;
    const hits=index.map(it=>[score(q,it),it]).filter(x=>x[0]>0).sort((a,b)=>b[0]-a[0]).slice(0,10);
    sel=0;
    if(!q.trim()){ res.innerHTML='<div class="empty">Try “ring size 7”, “925”, “1.5 carat oval”, “22k gold”, “ruby”…</div>'; return; }
    if(!hits.length){ res.innerHTML='<div class="empty">Nothing for that. Try a size, a stamp, a carat weight or a stone.</div>'; return; }
    res.innerHTML=hits.map(([_,it],i)=>`<a class="r${i===0?' on':''}" href="${ROOT}${it.u}"><span class="k">${it.g}</span><span><div class="t">${it.t}</div><div class="d">${it.d||''}</div></span></a>`).join('');
  }
  function open(prefill){
    if(!box){
      box=document.createElement('div'); box.className='search-overlay';
      box.innerHTML=`<div class="search-box" role="dialog" aria-label="Search CaratBase"><div class="in">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <input type="search" placeholder="Search tools and reference pages" autocomplete="off" aria-label="Search">
        <span class="kbd" style="font-size:11px;color:var(--ink-3);border:1px solid var(--line-2);border-radius:6px;padding:3px 7px">esc</span></div><div class="res"></div></div>`;
      document.body.appendChild(box);
      input=box.querySelector('input'); res=box.querySelector('.res');
      box.addEventListener('click',e=>{ if(e.target===box) close(); });
      input.addEventListener('input',()=>render(input.value));
      input.addEventListener('keydown',e=>{
        const rows=[...res.querySelectorAll('.r')];
        if(e.key==='ArrowDown'){ e.preventDefault(); sel=Math.min(sel+1,rows.length-1); }
        else if(e.key==='ArrowUp'){ e.preventDefault(); sel=Math.max(sel-1,0); }
        else if(e.key==='Enter'){ if(rows[sel]){ if(window.cbTrack) cbTrack('search',{q:input.value.slice(0,60),to:rows[sel].getAttribute('href')}); location.href=rows[sel].href; } return; }
        else if(e.key==='Escape'){ close(); return; }
        else return;
        rows.forEach((r,i)=>r.classList.toggle('on',i===sel));
      });
    }
    box.classList.add('open'); input.value=prefill||''; input.focus();
    load().then(()=>render(input.value));
  }
  function close(){ if(box) box.classList.remove('open'); }
  document.addEventListener('keydown',e=>{ if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){ e.preventDefault(); open(); } if(e.key==='/'&&!/input|textarea|select/i.test(document.activeElement.tagName)){ e.preventDefault(); open(); } });
  const q0=new URLSearchParams(location.search).get('q'); if(q0) setTimeout(()=>open(q0), 300);
  const home=document.getElementById('homeSearch');
  if(home){ home.addEventListener('focus',()=>{ open(home.value); home.blur(); }); }
  window.cbSearch={open,close};
})();
