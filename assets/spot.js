/* CaratBase — live metal prices.
   Primary source is the Worker's /api/spot, which fetches on demand and caches at the
   edge for 60 seconds. The daily committed metals.json is the fallback, so the site still
   prices correctly if the Worker or the upstream feed is down. */
const Spot = (function(){
  const EP = window.CB_ANALYTICS_ENDPOINT || '';
  let latest = null, timer = null;

  function apply(d){
    const g = d && d.perGram;
    if(!g || !g.gold) return false;
    if(g.gold)     METAL_SPOT.gold     = g.gold;
    if(g.silver)   METAL_SPOT.silver   = g.silver;
    if(g.platinum) METAL_SPOT.platinum = g.platinum;
    latest = d;
    document.dispatchEvent(new CustomEvent('cb:spot',{detail:d}));
    return true;
  }

  async function fromWorker(){
    if(!EP) return false;
    const r = await fetch(EP + '/api/spot', {cache:'no-store'});
    if(!r.ok) return false;
    const d = await r.json();
    return apply({...d, live:true});
  }

  async function fromSnapshot(){
    const r = await fetch('assets/metals.json?t='+Math.floor(Date.now()/3600000));
    if(!r.ok) return false;
    const d = await r.json();
    return apply({...d, live:false});
  }

  async function refresh(){
    try { if(await fromWorker()) return; } catch {}
    try { await fromSnapshot(); } catch {}
  }

  /* Poll only while the tab is actually being looked at. A background tab refreshing
     forever is wasted requests and, on a phone, wasted battery. */
  function start(seconds){
    stop();
    const ms=(seconds||60)*1000;
    timer=setInterval(()=>{ if(!document.hidden) refresh(); }, ms);
    document.addEventListener('visibilitychange',()=>{ if(!document.hidden) refresh(); });
  }
  function stop(){ if(timer) clearInterval(timer); timer=null; }

  refresh();
  return { refresh, start, stop, get latest(){ return latest; } };
})();
