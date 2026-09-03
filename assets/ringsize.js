/* CaratBase — ring sizer */
(function(){
  const $=id=>document.getElementById(id);
  if(!$('cvSystem')) return;

  let current = RING_SIZES.find(r=>r.us===6);
  // Read this now: the default paint during init overwrites cb_ring_last before
  // the restore step would otherwise get to look at it.
  const LAST_US = parseFloat(localStorage.getItem('cb_ring_last'));

  /* ---------- shared result panel ---------- */
  function paint(row, note){
    current = row;
    try{ localStorage.setItem('cb_ring_last', String(row.us)); }catch{}
    $('outUS').textContent = row.us;
    $('outFit').innerHTML = note || '';
    $('outGrid').innerHTML = [
      ['UK / AU',              row.uk],
      ['Europe (ISO)',         row.eu],
      ['India / Japan',        row.jp ?? '—'],
      ['Diameter',             row.dia.toFixed(2)+' mm'],
      ['Circumference',        row.circ.toFixed(1)+' mm']
    ].map(([k,v])=>`<div class="stat"><div class="k">${k}</div>
        <div class="v" style="font-size:23px">${v}</div></div>`).join('');
    highlightChart(row);
  }

  /* ---------- tabs ---------- */
  document.querySelectorAll('.tab').forEach(t=>t.addEventListener('click',()=>{
    document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));
    document.querySelectorAll('.tabpane').forEach(x=>x.classList.remove('on'));
    t.classList.add('on'); $(t.dataset.pane).classList.add('on');
    if(t.dataset.pane==='p-screen') drawGauges();
    if(window.cbTrack) cbTrack('tool_use',{tool:'ring_size',mode:t.dataset.pane});
  }));

  /* ---------- 1. convert a known size ---------- */
  const SYS_FIELD={us:'us',uk:'uk',eu:'eu',jp:'jp'};
  function fillValues(){
    const sys=$('cvSystem').value, f=SYS_FIELD[sys];
    const rows=RING_SIZES.filter(r=>r[f]!=null);
    $('cvValue').innerHTML=rows.map(r=>
      `<option value="${r.us}"${r.us===6?' selected':''}>${r[f]}</option>`).join('');
    convert();
  }
  function convert(){
    const row=RING_SIZES.find(r=>r.us===parseFloat($('cvValue').value));
    if(row) paint(row,'');
  }
  $('cvSystem').addEventListener('change',fillValues);
  $('cvValue').addEventListener('change',convert);

  /* ---------- 2. measure a ring you own ---------- */
  function fromDia(){
    const v=parseFloat($('rgDia').value);
    const row=nearestRing(v,'dia'); if(!row) return;
    const fit=ringFit(v,'dia',row);
    paint(row, fit.exact
      ? `${v} mm is a clean US ${row.us}.`
      : `${v} mm sits between sizes — closest is US ${row.us}, about
         ${Math.abs(fit.delta).toFixed(2)} mm ${fit.delta>0?'over':'under'}.
         <strong style="color:var(--ink-2)">When you are between sizes, go up.</strong>`);
  }
  $('rgDia').addEventListener('input',fromDia);

  /* ---------- 3. measure your finger ---------- */
  function fromCirc(){
    const v=parseFloat($('fgCirc').value);
    const row=nearestRing(v,'circ'); if(!row) return;
    const fit=ringFit(v,'circ',row);
    paint(row, fit.exact
      ? `${v} mm around is a clean US ${row.us}.`
      : `${v} mm sits between sizes — closest is US ${row.us}.
         <strong style="color:var(--ink-2)">When you are between sizes, go up.</strong>`);
  }
  $('fgCirc').addEventListener('input',fromCirc);

  /* ---------- 4. true-scale on-screen sizer ----------
     Calibrated against an ISO/IEC 7810 ID-1 card (85.60 mm wide), which every bank
     card on earth conforms to. Once we know px-per-mm we can draw real sizes. */
  const CAL_KEY='cb_pxpermm', CAL_DONE='cb_pxpermm_done';
  function pxPerMm(){ return parseFloat(localStorage.getItem(CAL_KEY)) || 3.78; }

  function applyCal(v){
    try{ localStorage.setItem(CAL_KEY,String(v)); }catch{}
    const el=$('cardCal');
    el.style.width  = (CARD_MM.w*v)+'px';
    el.style.height = (CARD_MM.h*v)+'px';
    const note='screen: '+v.toFixed(2)+' px per mm';
    $('calNote').textContent=note;
    $('calMiniNote').textContent=note;
    drawGauges();
  }
  $('calRange').addEventListener('input',e=>applyCal(parseFloat(e.target.value)));

  /* Collapse the calibration once it is done so the circles are the first thing you see. */
  function setCalCollapsed(on){
    $('calFull').classList.toggle('hide',on);
    $('calMini').classList.toggle('hide',!on);
    $('calBox').classList.toggle('done',on);
    try{ localStorage.setItem(CAL_DONE,on?'1':'0'); }catch{}
  }
  $('calDone').addEventListener('click',()=>{
    setCalCollapsed(true);
    $('gaugeWrap').scrollIntoView({behavior:'smooth',block:'center'});
    if(window.cbTrack) cbTrack('tool_use',{tool:'ring_size',mode:'calibrated'});
  });
  $('calRedo').addEventListener('click',()=>{
    setCalCollapsed(false);
    $('cardCal').scrollIntoView({behavior:'smooth',block:'center'});
  });

  // 1.2mm, not more: this must be fully covered by even a narrow 2mm band, or a
  // correctly sized ring would wrongly read as too small.
  const COLLAR_MM = 1.2;   // fluorescent band just outside true diameter
  const SEAT_MM    = 9;    // dashed placement guide, comfortably past a wide band

  function drawGauges(){
    const v=pxPerMm();
    const picks=RING_SIZES.filter(r=>Number.isInteger(r.us)&&r.us>=4&&r.us<=13);
    $('gaugeWrap').innerHTML=picks.map(r=>{
      const core   = r.dia*v;
      const collar = (r.dia+COLLAR_MM*2)*v;
      const seat   = (r.dia+SEAT_MM*2)*v;
      return `<div class="gauge" data-us="${r.us}">
        <div class="target" style="width:${seat}px;height:${seat}px">
          <div class="seat"></div>
          <div class="collar" style="width:${collar}px;height:${collar}px">
            <div class="core" style="width:${core}px;height:${core}px"></div>
          </div>
        </div>
        <div class="lbl">US ${r.us}</div>
        <div class="sub">${r.dia.toFixed(1)} mm</div></div>`;
    }).join('');
    $('gaugeWrap').querySelectorAll('.gauge').forEach(g=>g.addEventListener('click',()=>{
      $('gaugeWrap').querySelectorAll('.gauge').forEach(x=>x.classList.remove('picked'));
      g.classList.add('picked');
      const row=RING_SIZES.find(r=>r.us===parseFloat(g.dataset.us));
      if(row) paint(row,'Measured on screen — worth confirming with a jeweller before you buy.');
    }));
  }

  /* ---------- chart ---------- */
  function buildChart(){
    document.querySelector('#chart tbody').innerHTML=RING_SIZES.map(r=>
      `<tr data-us="${r.us}"><td><strong>${r.us}</strong></td><td>${r.uk}</td><td>${r.eu}</td>
       <td>${r.jp ?? '—'}</td><td class="num">${r.dia.toFixed(2)} mm</td>
       <td class="num">${r.circ.toFixed(1)} mm</td></tr>`).join('');
  }
  function highlightChart(row){
    document.querySelectorAll('#chart tbody tr').forEach(tr=>{
      const on = parseFloat(tr.dataset.us)===row.us;
      tr.style.background = on ? 'var(--gold-dim)' : '';
      tr.style.fontWeight = on ? '600' : '';
    });
  }

  /* ---------- printable paper sizer ---------- */
  $('printBtn').addEventListener('click',()=>{
    const picks=RING_SIZES.filter(r=>r.us%0.5===0 && r.us>=4 && r.us<=13);
    $('printArea').innerHTML=`
      <h2 style="font-family:Georgia,serif;margin-bottom:4mm">CaratBase paper ring sizer</h2>
      <p style="font-size:10pt;max-width:150mm;margin-bottom:3mm">
        Print at <strong>100% scale</strong> — no "fit to page", no shrinking. Check the bar below
        measures exactly 50 mm with a ruler before you trust the circles. Then slide a ring over
        each circle until one matches the <em>inside</em> of the band.</p>
      <div class="print-cal"></div>
      <p style="font-size:9pt;margin:2mm 0 6mm">↑ this bar must measure exactly 50 mm</p>
      <div>${picks.map(r=>`
        <span class="print-ring" style="width:${r.dia}mm;height:${r.dia}mm">
          <span style="position:absolute;bottom:-5mm;left:0;width:100%;text-align:center;
            font-size:8pt;font-family:Arial,sans-serif">US ${r.us}</span></span>`).join('')}</div>
      <p style="font-size:9pt;margin-top:14mm">caratbase.com</p>`;
    if(window.cbTrack) cbTrack('tool_use',{tool:'ring_size',mode:'print'});
    window.print();
  });

  /* ---------- saved sizes ---------- */
  const SAVED_KEY='cb_ring_sizes';
  const saved = {
    all(){ try{ return JSON.parse(localStorage.getItem(SAVED_KEY)||'[]') }catch{ return [] } },
    put(list){ try{ localStorage.setItem(SAVED_KEY,JSON.stringify(list.slice(0,20))) }catch{} },
    add(name,us){ const l=this.all().filter(x=>x.name!==name);
      l.unshift({name,us,at:Date.now()}); this.put(l); },
    remove(name){ this.put(this.all().filter(x=>x.name!==name)); }
  };

  function renderSaved(){
    const l=saved.all(), box=$('savedList');
    box.innerHTML = l.length ? l.map(x=>{
      const row=RING_SIZES.find(r=>r.us===x.us)||{};
      return `<div class="saved-row">
        <span class="who">${escapeHtml(x.name)}</span>
        <span class="small">${row.uk||''} · ${row.dia?row.dia.toFixed(2)+' mm':''}</span>
        <span class="sz">US ${x.us}</span>
        <button class="btn btn-ghost btn-sm" data-load="${escapeAttr(x.name)}">Open</button>
        <button class="btn btn-ghost btn-sm" data-drop="${escapeAttr(x.name)}">×</button>
      </div>`;
    }).join('') : '';
    box.querySelectorAll('[data-load]').forEach(b=>b.onclick=()=>{
      const rec=saved.all().find(x=>x.name===b.dataset.load); if(!rec) return;
      const row=RING_SIZES.find(r=>r.us===rec.us);
      if(row){ $('saveName').value=rec.name; paint(row,`Saved size for ${escapeHtml(rec.name)}.`); }
    });
    box.querySelectorAll('[data-drop]').forEach(b=>b.onclick=()=>{
      saved.remove(b.dataset.drop); renderSaved();
    });
  }
  const escapeHtml=t=>String(t).replace(/[&<>"']/g,c=>
    ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const escapeAttr=t=>escapeHtml(t);

  $('saveSizeBtn').addEventListener('click',()=>{
    const name=($('saveName').value.trim())||'My ring size';
    saved.add(name,current.us); renderSaved();
    $('shareMsg').innerHTML='<span style="color:var(--good)">Saved. It will be here next time '+
      'you open this page on this device.</span>';
    if(window.cbTrack) cbTrack('tool_use',{tool:'ring_size',mode:'save',us:current.us});
  });

  /* ---------- sharing ----------
     Everything a jeweller needs travels in the message itself, so the recipient never
     has to trust a conversion or even open the link. */
  function shareUrl(){
    const name=$('saveName').value.trim();
    const u=new URL(location.href.split('?')[0]);
    u.searchParams.set('size',current.us);
    if(name) u.searchParams.set('name',name);
    return u.toString();
  }
  function shareText(){
    const r=current, name=$('saveName').value.trim();
    return `${name?name+"'s ring size":'Ring size'}\n\n`+
      `US / Canada:      ${r.us}\n`+
      `UK / Australia:   ${r.uk}\n`+
      `Europe (ISO):     ${r.eu}\n`+
      `India / Japan:    ${r.jp ?? '—'}\n`+
      `Inside diameter:  ${r.dia.toFixed(2)} mm\n`+
      `Circumference:    ${r.circ.toFixed(1)} mm\n\n`+
      `Measured at ${shareUrl()}`;
  }
  function refreshShareLinks(){
    const t=shareText();
    $('shWhats').href='https://wa.me/?text='+encodeURIComponent(t);
    $('shMail').href='mailto:?subject='+encodeURIComponent(
      ($('saveName').value.trim()||'Ring')+' size')+'&body='+encodeURIComponent(t);
  }
  $('saveName').addEventListener('input',refreshShareLinks);

  $('shShare').addEventListener('click',async()=>{
    refreshShareLinks();
    const data={title:'Ring size',text:shareText(),url:shareUrl()};
    if(navigator.share){ try{ await navigator.share(data); }catch{} }
    else { copy(shareText()); }
    if(window.cbTrack) cbTrack('tool_use',{tool:'ring_size',mode:'share',us:current.us});
  });
  $('shCopy').addEventListener('click',()=>copy(shareUrl()));
  function copy(text){
    navigator.clipboard?.writeText(text).then(()=>{
      $('shareMsg').innerHTML='<span style="color:var(--good)">Copied to your clipboard.</span>';
    }).catch(()=>{ $('shareMsg').textContent=text; });
  }

  /* ---------- arriving on a shared link ---------- */
  function readSharedLink(){
    const q=new URLSearchParams(location.search);
    const sz=parseFloat(q.get('size')); if(!isFinite(sz)) return false;
    const row=RING_SIZES.find(r=>r.us===sz); if(!row) return false;
    const name=(q.get('name')||'').slice(0,60);
    $('sharedCard').classList.remove('hide');
    $('sharedCard').innerHTML=`
      <div class="eyebrow" style="margin-bottom:8px">Shared with you</div>
      <h2 style="font-size:30px">${name?escapeHtml(name)+"'s ring size is":'The ring size is'}
        <span style="color:var(--gold-2)">US ${row.us}</span></h2>
      <div class="grid" style="grid-template-columns:repeat(5,1fr);gap:10px;margin-top:20px">
        ${[['US / Canada',row.us],['UK / AU',row.uk],['Europe (ISO)',row.eu],
           ['India / Japan',row.jp ?? '—'],['Diameter',row.dia.toFixed(2)+' mm']]
          .map(([k,v])=>`<div class="stat"><div class="k">${k}</div>
            <div class="v" style="font-size:22px">${v}</div></div>`).join('')}
      </div>
      <p class="small" style="margin-top:16px">Every system is shown so any jeweller,
        anywhere, can use it. Measure your own below.</p>`;
    paint(row,'');
    if(name) $('saveName').value=name;
    if(window.cbTrack) cbTrack('tool_use',{tool:'ring_size',mode:'shared_link_opened'});
    return true;
  }

  /* ---------- init ---------- */
  buildChart();
  fillValues();
  applyCal(pxPerMm());
  $('calRange').value = pxPerMm();
  setCalCollapsed(localStorage.getItem(CAL_DONE)==='1');
  renderSaved();
  if(!readSharedLink()){
    const lastRow=RING_SIZES.find(r=>r.us===LAST_US);
    if(lastRow && lastRow.us!==6) paint(lastRow,'Picking up where you left off.');
  }
  refreshShareLinks();
})();
document.getElementById('yr').textContent=new Date().getFullYear();
