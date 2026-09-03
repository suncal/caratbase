/* CaratBase — budget calculator */
(function(){
  const $=id=>document.getElementById(id);
  if(!$('bAmount')) return;

  const PRESETS=[1000,2500,5000,10000,25000];
  $('bPresets').innerHTML=PRESETS.map(v=>
    `<button data-v="${v}"${v===5000?' class="on"':''}>$${(v/1000).toFixed(v>=10000?0:1).replace('.0','')}k</button>`).join('');
  $('bPresets').addEventListener('click',e=>{
    const v=e.target.dataset.v; if(!v) return;
    $('bAmount').value=v; run();
  });

  function run(){
    const b=parseFloat($('bAmount').value)||0;
    const results=BUDGET_STRATEGIES.map(s=>({...s, r:caratForBudget(b,s.spec)}));
    const size=results.find(x=>x.key==='size'), bal=results.find(x=>x.key==='balance'),
          top=results.find(x=>x.key==='quality'), lab=results.find(x=>x.key==='lab');

    $('bPresets').querySelectorAll('button').forEach(btn=>
      btn.classList.toggle('on', parseFloat(btn.dataset.v)===b));

    if(!bal.r){
      $('bBig').textContent='—';
      $('bBigSub').textContent='Below about $300 there is very little on the market.';
      $('bBalanced').textContent='—'; $('bTop').textContent='—'; $('bNote').textContent='';
      $('bGrid').innerHTML=''; return;
    }

    $('bBig').textContent=size.r.carat.toFixed(2)+' ct';
    $('bBigSub').textContent='natural, if you prioritise size over colour and clarity';
    $('bBalanced').textContent=bal.r.carat.toFixed(2)+' ct';
    $('bTop').textContent=top.r?top.r.carat.toFixed(2)+' ct':'—';

    const mult=top.r?(size.r.carat/top.r.carat):null;
    $('bNote').innerHTML= mult
      ? `The same ${fmt(b)} buys <strong style="color:#E8D19A">${mult.toFixed(1)}× more stone</strong>
         if you spend it on carat rather than on the top colour and clarity grades — almost
         none of which is visible without a loupe. A lab-grown stone at good quality would be
         about ${lab.r?lab.r.carat.toFixed(2)+' ct':'—'}, though it resells for very little.`
      : '';

    $('bGrid').innerHTML=results.map(s=>{
      if(!s.r) return '';
      const sp=s.spec, keep=Math.round(s.r.resaleHigh/s.r.retailHigh*100);
      return `<div class="panel">
        <div style="display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap">
          <div style="flex:0 0 150px;max-width:150px">
            <div class="stage" style="min-height:180px;padding:10px">
              ${shapeOnFinger(sp.shape, s.r.carat)}</div>
          </div>
          <div style="flex:1;min-width:190px">
            <div style="display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap">
              <h3 style="font-size:20px">${s.label}</h3>
              <span class="pill${sp.origin==='Lab-grown'?' pill-ice':''}">${sp.origin}</span>
            </div>
            <div style="font-family:var(--serif);font-size:34px;font-weight:700;color:var(--gold-2);
              line-height:1;margin:10px 0 4px">${s.r.carat.toFixed(2)} ct</div>
            <div class="small">${sp.shape} · ${sp.color} · ${sp.clarity} · ${sp.cut} cut</div>
            <div style="display:flex;gap:20px;margin-top:12px;flex-wrap:wrap">
              <div><div class="small">Costs</div>
                <strong class="mono">${fmt(s.r.retailLow)}–${fmt(s.r.retailHigh)}</strong></div>
              <div><div class="small">Resells for</div>
                <strong class="mono" style="color:var(--bad)">${fmt(s.r.resaleLow)}–${fmt(s.r.resaleHigh)}</strong></div>
              <div><div class="small">You keep</div>
                <strong class="mono" style="color:${keep<20?'var(--bad)':'var(--warn)'}">${keep}%</strong></div>
            </div>
            <p class="small" style="margin-top:12px">${s.note}</p>
          </div>
        </div>
      </div>`;
    }).join('');

    if(window.cbTrack) cbTrack('tool_use',{tool:'budget_calculator',budget:b,
      biggest:size.r.carat, balanced:bal.r.carat});
  }

  $('bAmount').addEventListener('input',run);
  run();
})();
document.getElementById('yr').textContent=new Date().getFullYear();
