/* CaratBase — valuation tool, certificate lookup, vault save, intent capture */
(function(){
  const $=id=>document.getElementById(id);
  if(!$('fCarat')) return;

  const fill=(el,arr,def)=>{el.innerHTML=arr.map(v=>`<option${v===def?' selected':''}>${v}</option>`).join('')};
  fill($('fShape'),  Object.keys(SHAPE_MULT),   'Round');
  fill($('fColor'),  Object.keys(COLOR_MULT),   'G');
  fill($('fClarity'),Object.keys(CLARITY_MULT), 'VS2');
  fill($('fCut'),    Object.keys(CUT_MULT),     'Very Good');
  fill($('fKarat'),  Object.keys(KARAT_PURITY), 'None / not sure');
  $('fSetting').innerHTML = SETTINGS.map(x=>
    `<option value="${x.key}">${x.label}</option>`).join('');

  /* Picking a style fills in a typical count and size; the fields stay editable. */
  $('fSetting').addEventListener('change',()=>{
    const cfg = SETTINGS.find(x=>x.key===$('fSetting').value);
    if(!cfg || cfg.key==='custom') return;
    $('fSideCount').value = cfg.count;
    if(cfg.mm) $('fSideMm').value = cfg.mm;
    calc();
  });

  /* ---------- certificate number ----------
     Neither GIA nor IGI publishes a free lookup API, so we do the two useful things
     that need no API: sanity-check the format, and send the user to the official
     verification page. The number itself is what makes a lead worth anything. */
  const LABS={
    GIA:{name:'GIA', url:'https://www.gia.edu/report-check',
         test:n=>/^\d{7,10}$/.test(n)},
    IGI:{name:'IGI', url:'https://www.igi.org/verify-your-report',
         test:n=>/^(LG)?\d{8,12}$/i.test(n)}
  };

  function certCheck(){
    const raw=$('fCertNo').value.trim();
    const n=raw.replace(/[^A-Za-z0-9]/g,'');
    const lab=$('fCert').value;
    const hint=$('certHint');
    $('certNoWrap').classList.toggle('hide', lab==='None');
    if(!n){
      hint.innerHTML='Laser-inscribed on the girdle of most modern stones, and printed on the report. '+
        'A certified stone can be graded and priced without anyone handling it, which is why it is '+
        'worth far more to a buyer than an unpapered one.';
      return null;
    }
    // An LG prefix is an IGI convention for lab-grown stones — follow it.
    if(/^LG/i.test(n)){
      if($('fOrigin').value!=='Lab-grown'){
        $('fOrigin').value='Lab-grown'; $('fOrigin').dispatchEvent(new Event('change'));
      }
      if($('fCert').value!=='IGI'){ $('fCert').value='IGI'; }
    }
    const L=LABS[$('fCert').value]||LABS.GIA;
    const ok=L.test(n);
    hint.innerHTML = ok
      ? `<span style="color:var(--good);font-weight:600">Format looks like a valid ${L.name} number.</span>
         Confirm the grades against the official record at
         <a href="${L.url}" target="_blank" rel="noopener noreferrer">${L.name} report check</a>
         and enter them above — a verified stone is what buyers actually bid on.`
      : `<span style="color:var(--warn);font-weight:600">That does not match the usual ${L.name} format.</span>
         Check the number on the report itself. ${L.name} numbers are typically
         ${lab==='IGI'?'8 to 12 digits, sometimes with an LG prefix on lab-grown stones':'7 to 10 digits'}.`;
    return n;
  }

  let last=null, counted=false;

  function read(){
    return {carat:$('fCarat').value, shape:$('fShape').value, color:$('fColor').value,
      clarity:$('fClarity').value, cut:$('fCut').value, origin:$('fOrigin').value,
      cert:$('fCert').value, certNo:$('fCertNo').value.trim().replace(/[^A-Za-z0-9]/g,''),
      karat:$('fKarat').value, grams:$('fGrams').value,
      sideCount:$('fSideCount').value, sideMm:$('fSideMm').value};
  }

  function calc(){
    const o=read(), v=valueDiamond(o);
    if(!v){ $('oRetail').textContent='—'; return; }
    const metal = valueMetal(o.karat,o.grams);
    const side  = valueMelee(o.sideCount,o.sideMm,o.origin);

    const sideRL = side?side.retailLow:0,  sideRH = side?side.retailHigh:0;
    const sideSL = side?side.resaleLow:0,  sideSH = side?side.resaleHigh:0;

    const retailLo = v.retailLow  + sideRL + metal;
    const retailHi = v.retailHigh + sideRH + metal;
    const resaleLo = v.resaleLow  + sideSL + metal;
    const resaleHi = v.resaleHigh + sideSH + metal;
    const keep = retailHi ? Math.round(resaleHi/retailHi*100) : 0;

    $('oRetail').textContent = fmt(retailLo)+' – '+fmt(retailHi);
    $('oResale').textContent = fmt(resaleLo)+' – '+fmt(resaleHi);
    $('oMetal').textContent  = metal?fmt(metal):'—';
    $('oKeep').textContent   = keep+'%';

    /* Where the money actually is. Almost nobody guesses this correctly. */
    const rows = [[`Centre stone — ${o.carat} ct ${o.origin.toLowerCase()}`,
                   v.retailLow, v.retailHigh, v.resaleLow, v.resaleHigh]];
    if(side) rows.push([`Side stones — ${side.count} × ${o.sideMm} mm (${side.totalCt} ct total)`,
                        sideRL, sideRH, sideSL, sideSH]);
    if(metal) rows.push([`Setting metal — ${o.grams} g ${o.karat}`, metal, metal, metal, metal]);
    document.querySelector('#breakdown tbody').innerHTML = rows.map(([lab,rl,rh,sl,sh])=>
      `<tr><td>${lab}</td><td class="num">${fmt(rl)}–${fmt(rh)}</td>
       <td class="num" style="color:var(--bad)">${fmt(sl)}–${fmt(sh)}</td></tr>`).join('')
      + `<tr style="background:var(--gold-dim)"><td><strong>Whole piece</strong></td>
         <td class="num"><strong>${fmt(retailLo)}–${fmt(retailHi)}</strong></td>
         <td class="num"><strong style="color:var(--bad)">${fmt(resaleLo)}–${fmt(resaleHi)}</strong></td></tr>`;

    $('sideVerdict').innerHTML = side
      ? `Those ${side.count} side stones come to ${side.totalCt} ct all together, but each one is
         priced at its own tiny per-carat rate rather than as one big stone — so they add about
         <strong style="color:var(--ink)">${fmt(sideRH)}</strong>, roughly
         <strong style="color:var(--ink)">${Math.round(sideRH/retailHi*100)}%</strong> of the ring.
         Most of what a halo or pavé costs is the setting and the labour of fitting them, not the
         diamonds.`
      : '';

    $('oNote').innerHTML = v.isLab
      ? 'Lab-grown stones have very little secondary market at present. The metal in the setting may be worth more than the diamond.'
      : `Based on a ${o.carat} ct ${o.shape.toLowerCase()} ${o.origin.toLowerCase()} diamond, ${o.color} colour, ${o.clarity}, ${o.cut} cut${o.cert==='None'?', uncertified (discounted for grading risk)':', '+o.cert+' certified'}${o.certNo?' #'+o.certNo:''}. Materials only — it excludes the jeweller's making and setting charges.`;

    $('sideHint').textContent = side
      ? `Each stone is about ${side.ctEach} ct. Typical pavé is 1.0–1.5 mm, a halo 1.2–1.8 mm.`
      : 'Typical pavé stones are 1.0–1.5 mm across, halo stones 1.2–1.8 mm.';

    last={...o, est_low:resaleLo, est_high:resaleHi};
    if(!counted && window.cbTrack){counted=true;cbTrack('valuation',
      {carat:o.carat,origin:o.origin,shape:o.shape,sideStones:side?side.count:0});}
  }

  ['fCarat','fShape','fColor','fClarity','fCut','fOrigin','fCert','fKarat','fGrams',
   'fSideCount','fSideMm']
    .forEach(id=>{$(id).addEventListener('input',calc);$(id).addEventListener('change',calc)});
  $('fCertNo').addEventListener('input',()=>{certCheck();calc()});
  $('fCert').addEventListener('change',certCheck);
  certCheck(); calc();
  document.addEventListener('cb:spot', calc);   // live metal prices arrived

  /* ---------- save to vault ---------- */
  $('saveVaultBtn').addEventListener('click',()=>{
    if(!last) return;
    const n=Vault.add(last);
    $('vaultMsg').innerHTML=`<span style="color:var(--good)">Saved. Your vault now holds
      ${n} piece${n>1?'s':''}. <a href="vault.html">See what it is all worth.</a></span>`;
    $('saveVaultBtn').textContent='Saved to vault';
    setTimeout(()=>{$('saveVaultBtn').textContent='Save another'},2200);
    if(window.cbTrack) cbTrack('tool_use',{tool:'vault_add',pieces:n,certified:!!last.certNo});
  });

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
      cert:last.cert,cert_no:last.certNo||'',
      est_low:last.est_low,est_high:last.est_high});
    $('leadMsg').innerHTML='<span style="color:var(--good)">Report on its way to '+email+'.</span>';
    $('leadForm').reset();
    $('leadBtn').disabled=true;
  });
})();
document.getElementById('yr').textContent=new Date().getFullYear();
