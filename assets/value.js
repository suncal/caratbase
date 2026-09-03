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

  /* ---------- offer capture ----------
     Gives the user something immediately useful (how their offer compares) in exchange
     for the one number nobody publishes. Every submission makes the resale estimate
     better, which is the only data moat available here without capital. */
  $('ofSubmit').addEventListener('click',()=>{
    const amt=parseFloat($('ofAmount').value);
    if(!isFinite(amt)||amt<=0||!last) return;
    const mid=(last.est_low+last.est_high)/2;
    const pct=Math.round(amt/mid*100);
    let verdict,cls;
    if(pct>=110){verdict='That is above what we would expect for this piece. Worth taking seriously.';cls='pill-good'}
    else if(pct>=85){verdict='That is in the normal range for a genuine offer on this piece.';cls='pill-good'}
    else if(pct>=60){verdict='That is on the low side. Getting two more quotes would be worth the effort.';cls=''}
    else {verdict='That is well below what this piece should fetch. Do not accept it without other quotes.';cls='pill-bad'}

    $('ofResult').classList.remove('hide');
    $('ofResult').innerHTML=
      `<div class="stat"><div class="k">Their offer versus our resale estimate</div>
         <div class="v ${pct>=85?'good':'bad'}">${pct}%</div></div>
       <p class="small" style="margin-top:10px"><span class="pill ${cls}">${pct}% of estimate</span>
         ${verdict}</p>
       <p class="small" style="margin-top:8px;color:var(--good)">Thank you — that figure goes
         into the resale data behind every valuation on this site.</p>`;

    if(window.cbTrack) cbTrack('offer_report',{
      amount:amt, offeredBy:$('ofWho').value, pctOfEstimate:pct,
      carat:last.carat, shape:last.shape, color:last.color, clarity:last.clarity,
      cut:last.cut, origin:last.origin, cert:last.cert,
      est_low:last.est_low, est_high:last.est_high});
    $('ofSubmit').disabled=true;
  });

  /* ---------- intent = the lead ---------- */
  const COPY={
    insure:'Insurers need a documented value, and getting one normally means paying $50–300 for an appraisal. The report below gives you the specifications and both value ranges in a form you can send to an insurer — though for a high-value piece most insurers will still want a certified appraisal on top.',
    sell:'Never accept the first offer. The spread between buyers on the same stone is routinely thousands of dollars, so get at least three written quotes. Take the report below with you — a buyer who knows you have the numbers will not lowball as easily.',
    appraise:'A certified appraisal usually runs $50–300 per item and is required for scheduled insurance coverage. The report below tells you what to expect before you book one, so you can tell whether an appraisal comes back sensible.',
    curious:'Fair enough. The report below has the numbers on file whenever you want them.'
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

  /* ---------- the valuation report ----------
     Printing is the one PDF route that needs no library and no server: every desktop and
     mobile browser offers "Save as PDF" from the print dialog. */
  function buildReport(){
    if(!last) return;
    const o=last, v=valueDiamond(o), metal=valueMetal(o.karat,o.grams),
          side=valueMelee(o.sideCount,o.sideMm,o.origin);
    const sRL=side?side.retailLow:0, sRH=side?side.retailHigh:0;
    const sSL=side?side.resaleLow:0, sSH=side?side.resaleHigh:0;
    const rLo=v.retailLow+sRL+metal, rHi=v.retailHigh+sRH+metal;
    const kLo=v.resaleLow+sSL+metal, kHi=v.resaleHigh+sSH+metal;
    const now=new Date();
    const ref='CB-'+now.toISOString().slice(0,10).replace(/-/g,'')+'-'+
      Math.abs(Math.round(parseFloat(o.carat)*1000)).toString(36).toUpperCase();

    const kv=(k,val)=>`<div><div class="k">${k}</div><div class="v">${val}</div></div>`;
    const rows=[[`Centre stone — ${o.carat} ct ${o.shape.toLowerCase()}`,v.retailLow,v.retailHigh,v.resaleLow,v.resaleHigh]];
    if(side) rows.push([`Side stones — ${side.count} × ${o.sideMm} mm (${side.totalCt} ct)`,sRL,sRH,sSL,sSH]);
    if(metal) rows.push([`Setting — ${o.grams} g ${o.karat}`,metal,metal,metal,metal]);

    document.getElementById('reportArea').innerHTML=`
      <div class="rep-head">
        <div><h1 class="rep-title">Valuation Report</h1>
          <div class="rep-sub">CaratBase · caratbase.com</div></div>
        <div style="text-align:right" class="rep-sub">
          <div><strong>${ref}</strong></div>
          <div>${now.toLocaleDateString('en-GB',{day:'numeric',month:'long',year:'numeric'})}</div></div>
      </div>

      <div class="rep-sec"><h3>The piece</h3><div class="rep-kv">
        ${kv('Carat weight',o.carat+' ct')}${kv('Shape',o.shape)}${kv('Colour',o.color)}
        ${kv('Clarity',o.clarity)}${kv('Cut',o.cut)}${kv('Origin',o.origin)}
        ${kv('Certificate',o.cert)}${o.certNo?kv('Report number',o.certNo):''}
        ${o.karat&&o.karat!=='None / not sure'?kv('Setting metal',o.karat):''}
        ${o.grams?kv('Metal weight',o.grams+' g'):''}
        ${side?kv('Side stones',side.count+' × '+o.sideMm+' mm'):''}
      </div></div>

      <div class="rep-sec"><h3>Estimated value</h3>
        <div class="rep-big">
          <div><div class="k">Retail replacement</div><div class="v">${fmt(rLo)} – ${fmt(rHi)}</div></div>
          <div><div class="k">Realistic resale</div><div class="v">${fmt(kLo)} – ${fmt(kHi)}</div></div>
        </div>
        <table><thead><tr><th>Component</th><th class="num">Retail</th><th class="num">Resale</th></tr></thead>
        <tbody>${rows.map(([l,a,b,c,d])=>
          `<tr><td>${l}</td><td class="num">${fmt(a)}–${fmt(b)}</td>
           <td class="num">${fmt(c)}–${fmt(d)}</td></tr>`).join('')}
          <tr><td><strong>Whole piece</strong></td>
            <td class="num"><strong>${fmt(rLo)}–${fmt(rHi)}</strong></td>
            <td class="num"><strong>${fmt(kLo)}–${fmt(kHi)}</strong></td></tr>
        </tbody></table>
      </div>

      <div class="rep-sec"><h3>How these figures were reached</h3>
        <p class="rep-note">
          Retail is modelled from published market prices for the stated specification, using
          per-carat rates that step at each recognised size threshold, adjusted for colour,
          clarity, cut and shape. Side stones are priced individually at melee rates rather
          than as a combined weight, which is why they contribute far less than their total
          carat suggests. Metal is valued at the spot price on the date above
          (gold ${fmt(METAL_SPOT.gold)}/g), less an allowance for refining.
          Resale reflects the secondary market, where a natural diamond typically recovers
          25–40% of retail and a lab-grown stone considerably less.
        </p></div>

      <div class="rep-sec"><h3>Important</h3>
        <p class="rep-note">
          This is an estimate produced from a price model, not a physical inspection.
          CaratBase is not a licensed appraiser, does not buy or sell jewellery, and this
          document is not a formal appraisal, an offer, a guarantee of value, or financial
          advice. Insurers and courts will normally require a certified appraisal from a
          qualified professional. Figures are in US dollars.
        </p></div>

      <p class="rep-note" style="margin-top:10mm;border-top:1px solid #ddd;padding-top:3mm">
        Produced free at caratbase.com — ${ref}</p>`;
  }

  $('dlReport').addEventListener('click',()=>{
    buildReport();
    document.body.classList.add('printing-report');
    const restore=()=>document.body.classList.remove('printing-report');
    window.addEventListener('afterprint',restore,{once:true});
    setTimeout(restore,60000);           // belt and braces if afterprint never fires
    window.print();
    if(window.cbTrack) cbTrack('tool_use',{tool:'report_download',intent,carat:last.carat});
  });

  $('leadForm').addEventListener('submit',e=>{
    e.preventDefault();
    const email=$('leadEmail').value.trim();
    if(!email||!intent||!last) return;
    if(window.cbTrack) cbTrack('lead',{email,intent,carat:last.carat,shape:last.shape,
      color:last.color,clarity:last.clarity,origin:last.origin,
      cert:last.cert,cert_no:last.certNo||'',
      est_low:last.est_low,est_high:last.est_high});
    $('leadMsg').innerHTML='<span style="color:var(--good)">Saved. We will only write to '+
      email+' if this piece changes meaningfully in value.</span>';
    $('leadForm').reset();
    $('leadBtn').disabled=true;
  });
})();
document.getElementById('yr').textContent=new Date().getFullYear();
