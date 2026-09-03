/* CaratBase — valuation tool + intent capture */
(function(){
  const $=id=>document.getElementById(id);
  if(!$('fCarat')) return;

  const fill=(el,arr,def)=>{el.innerHTML=arr.map(v=>`<option${v===def?' selected':''}>${v}</option>`).join('')};
  fill($('fShape'),  Object.keys(SHAPE_MULT),   'Round');
  fill($('fColor'),  Object.keys(COLOR_MULT),   'G');
  fill($('fClarity'),Object.keys(CLARITY_MULT), 'VS2');
  fill($('fCut'),    Object.keys(CUT_MULT),     'Very Good');
  fill($('fKarat'),  Object.keys(KARAT_PURITY), 'None / not sure');

  let last=null, counted=false;

  function read(){
    return {carat:$('fCarat').value, shape:$('fShape').value, color:$('fColor').value,
      clarity:$('fClarity').value, cut:$('fCut').value, origin:$('fOrigin').value,
      cert:$('fCert').value, karat:$('fKarat').value, grams:$('fGrams').value};
  }

  function calc(){
    const o=read(), v=valueDiamond(o);
    if(!v){ $('oRetail').textContent='—'; return; }
    const metal=valueMetal(o.karat,o.grams);
    const retailHi=v.retailHigh+metal, resaleHi=v.resaleHigh+metal;
    const keep=retailHi?Math.round(resaleHi/retailHi*100):0;

    $('oRetail').textContent=fmt(v.retailLow+metal)+' – '+fmt(retailHi);
    $('oResale').textContent=fmt(v.resaleLow+metal)+' – '+fmt(resaleHi);
    $('oMetal').textContent =metal?fmt(metal):'—';
    $('oKeep').textContent  =keep+'%';

    $('oNote').innerHTML = v.isLab
      ? 'Lab-grown stones have very little secondary market at present. The metal in the setting may be worth more than the diamond.'
      : `Based on a ${o.carat} ct ${o.shape.toLowerCase()} ${o.origin.toLowerCase()} diamond, ${o.color} colour, ${o.clarity}, ${o.cut} cut${o.cert==='None'?', uncertified (discounted for grading risk)':', '+o.cert+' certified'}.`;

    last={...o, est_low:v.resaleLow+metal, est_high:v.resaleHigh+metal};
    if(!counted && window.cbTrack){counted=true;cbTrack('valuation',{carat:o.carat,origin:o.origin,shape:o.shape});}
  }

  ['fCarat','fShape','fColor','fClarity','fCut','fOrigin','fCert','fKarat','fGrams']
    .forEach(id=>{$(id).addEventListener('input',calc);$(id).addEventListener('change',calc)});
  calc();

  /* ---------- intent = the lead ---------- */
  const COPY={
    insure:'Most jewellery is under-insured or not insured at all, because insurers need a documented value and getting one usually means paying for an appraisal. We will email your valuation report as a PDF you can send straight to an insurer.',
    sell:'Never accept the first offer — the spread between buyers on the same stone is often thousands of dollars. We will email your report plus a breakdown of what each type of buyer typically pays.',
    appraise:'A certified appraisal usually runs $50–300 per item and is required for scheduled insurance coverage. We will email your estimate so you know what to expect before you book one.',
    curious:'No problem. We will email the report so you have the numbers on file.'
  };
  let intent=null;

  document.querySelectorAll('[data-intent]').forEach(b=>{
    b.addEventListener('click',()=>{
      intent=b.dataset.intent;
      document.querySelectorAll('[data-intent]').forEach(x=>{
        x.classList.remove('btn-gold');x.classList.add('btn-ghost')});
      b.classList.add('btn-gold');b.classList.remove('btn-ghost');
      $('intentCopy').textContent=COPY[intent];
      $('intentFollow').classList.remove('hide');
      if(window.cbTrack) cbTrack('tool_use',{tool:'intent_select',intent});
    });
  });

  $('leadForm').addEventListener('submit',e=>{
    e.preventDefault();
    const email=$('leadEmail').value.trim();
    if(!email||!intent||!last) return;
    if(window.cbTrack) cbTrack('lead',{email,intent,carat:last.carat,shape:last.shape,
      color:last.color,clarity:last.clarity,origin:last.origin,
      est_low:last.est_low,est_high:last.est_high});
    $('leadMsg').innerHTML='<span style="color:var(--good)">Report on its way to '+email+'.</span>';
    $('leadForm').reset();
    $('leadBtn').disabled=true;
  });
})();
document.getElementById('yr').textContent=new Date().getFullYear();
