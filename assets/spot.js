/* CaratBase — pull today's metal prices into the shared valuation engine.
   metals.json is refreshed daily by .github/workflows/metals.yml. */
(function(){
  fetch('assets/metals.json?t='+Math.floor(Date.now()/3600000)).then(r=>r.json()).then(d=>{
    const g=d.perGram||{};
    if(g.gold)     METAL_SPOT.gold=g.gold;
    if(g.silver)   METAL_SPOT.silver=g.silver;
    if(g.platinum) METAL_SPOT.platinum=g.platinum;
    document.dispatchEvent(new CustomEvent('cb:spot',{detail:d}));
  }).catch(()=>{ /* seed values in data.js stand in */ });
})();
