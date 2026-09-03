/* CaratBase — coloured stone and pearl calculator UI */
(function(){
  const $=id=>document.getElementById(id);
  if(!$('gType')) return;

  const opts=(el,list,def)=>el.innerHTML=list.map(v=>
    `<option${v===def?' selected':''}>${v}</option>`).join('');

  opts($('gType'), Object.keys(GEMS), 'Ruby');
  opts($('gTier'), GEM_TIERS, 'Fine');
  opts($('gTreat'), Object.keys(GEM_TREATMENTS), 'Heated (standard)');

  function fillOrigins(){
    const g=GEMS[$('gType').value];
    opts($('gOrigin'), Object.keys(g.origins), Object.keys(g.origins).slice(-1)[0]);
  }

  function calc(){
    const o={type:$('gType').value, carat:$('gCarat').value, tier:$('gTier').value,
             treatment:$('gTreat').value, origin:$('gOrigin').value};
    const v=valueGem(o);
    $('gTierHelp').textContent = GEM_TIER_HELP[o.tier] || '';
    if(!v){ $('gRetail').textContent='—'; return; }

    const keep=v.retailHigh?Math.round(v.resaleHigh/v.retailHigh*100):0;
    $('gRetail').textContent=fmt(v.retailLow)+' – '+fmt(v.retailHigh);
    $('gResale').textContent=fmt(v.resaleLow)+' – '+fmt(v.resaleHigh);
    $('gPpc').textContent=fmt(v.ppc);
    $('gKeep').textContent=keep+'%';
    $('gNote').textContent=v.treatmentNote;

    /* Two things are worth interrupting someone about. */
    const warn=$('gWarn');
    if(v.speculative){
      warn.style.display='block';
      warn.innerHTML=`<div class="pill pill-bad">Read this before believing the number</div>
        <p class="small" style="margin-top:10px">You have selected <strong>Exceptional</strong>,
        which is auction-house material — top colour, untreated, certified origin. Genuinely
        exceptional stones are rare enough that estimates for them are the least reliable
        figures on this site, and they need a specialist rather than a calculator. If you are
        not certain your stone is in this class, try <strong>Fine</strong> instead.</p>`;
    } else if(v.retailHigh>=2000 && /Unknown/.test(o.treatment)){
      warn.style.display='block';
      warn.innerHTML=`<div class="pill">A report would likely pay for itself</div>
        <p class="small" style="margin-top:10px">With treatment unknown, a buyer has to assume
        the least favourable case and prices for that risk — which is why the figure above is
        held down. On a stone in this value range a laboratory report usually returns several
        times its cost.</p>`;
    } else if(/glass|Dyed|Diffusion/.test(o.treatment)){
      warn.style.display='block';
      warn.innerHTML=`<div class="pill pill-bad">Handle with care</div>
        <p class="small" style="margin-top:10px">Fracture-filled, dyed and diffusion-treated
        stones can be damaged by ordinary jewellery repair — a jeweller's torch will destroy a
        glass-filled ruby. Tell anyone who works on the piece.</p>`;
    } else warn.style.display='none';

    if(window.cbTrack) cbTrack('tool_use',{tool:'gemstone',type:o.type,tier:o.tier,
      treatment:o.treatment,carat:o.carat});
  }

  $('gType').addEventListener('change',()=>{fillOrigins();calc()});
  ['gCarat','gTier','gTreat','gOrigin'].forEach(id=>{
    $(id).addEventListener('input',calc); $(id).addEventListener('change',calc);
  });
  fillOrigins(); calc();

  /* ---------- pearls ---------- */
  opts($('pType'), Object.keys(PEARL_TYPES), 'Akoya');
  opts($('pQual'), Object.keys(PEARL_QUALITY), 'Good');

  function pearls(){
    const o={type:$('pType').value, mm:$('pMm').value, quality:$('pQual').value};
    const v=valuePearlStrand(o);
    if(!v){ $('pStrand').textContent='—'; return; }
    $('pStrand').textContent=fmt(v.strandLow)+' – '+fmt(v.strandHigh);
    $('pSingle').textContent=fmt(v.singleLow)+' – '+fmt(v.singleHigh);
    $('pTypeOut').textContent=o.type;
    $('pNote').textContent=v.note;
    if(window.cbTrack) cbTrack('tool_use',{tool:'pearls',type:o.type,mm:o.mm});
  }
  ['pType','pQual','pMm'].forEach(id=>{
    $(id).addEventListener('input',pearls); $(id).addEventListener('change',pearls);
  });
  pearls();
})();
document.getElementById('yr').textContent=new Date().getFullYear();
