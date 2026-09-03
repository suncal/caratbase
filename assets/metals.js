/* CaratBase — gold calculator and daily metal prices */
(function(){
  const $=id=>document.getElementById(id);
  if(!$('mOut')) return;

  const NAMES={gold:'Gold',silver:'Silver',platinum:'Platinum',palladium:'Palladium'};
  const KARATS=[['24K',.999],['22K',.916],['18K',.750],['14K',.585],['10K',.417],['9K',.375]];

  /* Weight is entered in whatever unit the trade near you uses. A troy ounce is not an
     ounce, and a tola is the standard unit across much of South Asia and the Gulf. */
  const UNITS={
    g:   {label:'grams',       toG:1},
    ozt: {label:'troy oz',     toG:31.1034768},
    dwt: {label:'pennyweight', toG:1.55517384},
    tola:{label:'tola',        toG:11.6638038}
  };
  let unit='g';

  $('mUnits').innerHTML=Object.entries(UNITS).map(([k,u])=>
    `<button data-u="${k}"${k===unit?' class="on"':''}>${u.label}</button>`).join('');
  $('mUnits').addEventListener('click',e=>{
    const u=e.target.dataset.u; if(!u) return;
    unit=u;
    $('mUnits').querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.u===u));
    calc();
  });

  $('mKarat').innerHTML=Object.keys(KARAT_PURITY).filter(k=>k!=='None / not sure')
    .map(k=>`<option${k==='14K'?' selected':''}>${k}</option>`).join('');

  function calc(){
    const grams=(parseFloat($('mWeight').value)||0)*UNITS[unit].toG;
    const karat=$('mKarat').value;
    const val=valueMetal(karat,grams);
    if(!val){ $('mOut').textContent='—'; $('mOutSub').textContent=''; return; }

    const purity=KARAT_PURITY[karat]||0;
    const pureG=grams*purity;
    const metalName = karat==='Platinum'?'platinum' : karat==='Silver 925'?'silver' : 'gold';

    $('mOut').textContent=fmt(val);
    $('mOutSub').textContent=
      `${(grams).toFixed(2)} g of ${karat}${unit!=='g'?` (${$('mWeight').value} ${UNITS[unit].label})`:''}`;
    $('mOffer').textContent=fmt(val*0.70)+' – '+fmt(val*0.90);
    $('mPure').textContent=pureG.toFixed(2)+' g '+metalName;
    $('mNote').innerHTML=
      `Buyers refine the metal and take a margin, so 70–90% of the figure above is a normal
       offer. Below about 60%, walk away. This counts metal only — any stones are valued
       <a href="value.html">separately</a>.`;
    if(window.cbTrack) cbTrack('tool_use',{tool:'gold_calculator',karat,grams:+grams.toFixed(2)});
  }
  ['mWeight','mKarat'].forEach(id=>{
    $(id).addEventListener('input',calc); $(id).addEventListener('change',calc);
  });

  /* ---------- live prices ---------- */
  fetch('assets/metals.json?t='+Math.floor(Date.now()/3600000)).then(r=>r.json()).then(d=>{
    const g=d.perGram, p=d.prevPerGram||{};
    METAL_SPOT.gold=g.gold; METAL_SPOT.silver=g.silver; METAL_SPOT.platinum=g.platinum;

    const when=new Date(d.updated);
    $('calcStatus').textContent='gold $'+g.gold.toFixed(2)+'/g · '+
      when.toLocaleDateString('en-US',{month:'short',day:'numeric'});
    $('updated').textContent='Last updated '+when.toLocaleString('en-US',
      {dateStyle:'medium',timeStyle:'short'});

    $('spotList').innerHTML=Object.keys(NAMES).filter(k=>g[k]).map(k=>{
      const now=g[k], was=p[k]||now, dp=was?((now-was)/was*100):0;
      return `<div class="metal-row">
        <div><strong style="font-size:16px">${NAMES[k]}</strong><div class="small">per gram</div></div>
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
    vaultBox();
  }).catch(()=>{
    $('calcStatus').textContent='using last known prices';
    $('spotList').innerHTML='<p class="small">Prices unavailable right now.</p>';
    calc();
  });

  function vaultBox(){
    const items=(typeof Vault!=='undefined')?Vault.all():[];
    const box=$('vaultBox'); if(!items.length){ box.innerHTML=''; return; }
    let lo=0,hi=0;
    items.forEach(p=>{
      const v=valueDiamond(p), m=valueMetal(p.karat,p.grams);
      if(v){ lo+=v.resaleLow+m; hi+=v.resaleHigh+m; }
    });
    box.innerHTML=`<div class="capture">
      <div style="display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:center">
        <div><h3 style="font-size:22px">Your vault at today's prices</h3>
          <p class="small" style="margin-top:4px">${items.length} piece${items.length>1?'s':''} ·
            resale value now <strong class="mono" style="color:var(--ink)">${fmt(lo)}–${fmt(hi)}</strong></p></div>
        <a href="vault.html" class="btn btn-gold">Open my vault</a></div></div>`;
  }

  calc();
})();
document.getElementById('yr').textContent=new Date().getFullYear();
