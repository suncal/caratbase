/* CaratBase — daily metal prices */
(function(){
  const spot=document.getElementById('spotList'); if(!spot) return;
  const $=id=>document.getElementById(id);

  const NAMES={gold:'Gold',silver:'Silver',platinum:'Platinum',palladium:'Palladium'};
  const KARATS=[['24K',.999],['22K',.916],['18K',.750],['14K',.585],['10K',.417],['9K',.375]];

  fetch('assets/metals.json?t='+Date.now()).then(r=>r.json()).then(d=>{
    const g=d.perGram, p=d.prevPerGram||{};
    METAL_SPOT.gold=g.gold; METAL_SPOT.silver=g.silver; METAL_SPOT.platinum=g.platinum;

    $('updated').textContent='Last updated '+new Date(d.updated)
      .toLocaleString('en-US',{dateStyle:'medium',timeStyle:'short'});

    spot.innerHTML=Object.keys(NAMES).filter(k=>g[k]).map(k=>{
      const now=g[k], was=p[k]||now, dp=was?((now-was)/was*100):0;
      return `<div class="metal-row">
        <div><strong style="font-size:16px">${NAMES[k]}</strong>
          <div class="small">per gram</div></div>
        <div style="text-align:right">
          <div class="mono" style="font-family:var(--serif);font-size:24px;font-weight:600">$${now.toFixed(2)}</div>
          <div class="small ${dp>=0?'delta-up':'delta-dn'}">${dp>=0?'▲':'▼'} ${Math.abs(dp).toFixed(2)}%</div>
        </div></div>`;
    }).join('');

    document.querySelector('#karatTable tbody').innerHTML=KARATS.map(([k,pur])=>
      `<tr><td><strong>${k}</strong></td><td class="num">${(pur*100).toFixed(1)}%</td>
       <td class="num">$${(g.gold*pur).toFixed(2)}</td>
       <td class="num"><strong>$${(g.gold*pur*10).toFixed(0)}</strong></td></tr>`).join('');

    calc();
    vaultBox(g);
  }).catch(()=>{ spot.innerHTML='<p class="small">Prices unavailable right now.</p>' });

  /* weigh-your-piece calculator */
  $('mKarat').innerHTML=Object.keys(KARAT_PURITY).filter(k=>k!=='None / not sure')
    .map(k=>`<option${k==='14K'?' selected':''}>${k}</option>`).join('');
  function calc(){
    const v=valueMetal($('mKarat').value,$('mGrams').value);
    $('mOut').textContent=v?fmt(v):'—';
  }
  ['mKarat','mGrams'].forEach(id=>{
    $(id).addEventListener('input',calc); $(id).addEventListener('change',calc);
  });
  calc();

  /* what today's move did to the user's vault */
  function vaultBox(g){
    const items=(typeof Vault!=='undefined')?Vault.all():[];
    const box=$('vaultBox'); if(!items.length){ box.innerHTML=''; return; }
    let lo=0,hi=0;
    items.forEach(p=>{
      const v=valueDiamond(p); const m=valueMetal(p.karat,p.grams);
      if(v){ lo+=v.resaleLow+m; hi+=v.resaleHigh+m; }
    });
    box.innerHTML=`<div class="capture">
      <div style="display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center">
        <div><h3 style="font-size:22px">Your vault at today's prices</h3>
          <p class="small" style="margin-top:4px">${items.length} piece${items.length>1?'s':''} ·
            resale value now <strong class="mono" style="color:var(--ink)">${fmt(lo)}–${fmt(hi)}</strong></p></div>
        <a href="vault.html" class="btn btn-gold">Open my vault</a></div></div>`;
  }
  if(window.cbTrack) cbTrack('tool_use',{tool:'metals'});
})();
