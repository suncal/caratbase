/* CaratBase — ring sizer */
(function(){
  const $=id=>document.getElementById(id);
  if(!$('cvSystem')) return;

  let current = RING_SIZES.find(r=>r.us===6);

  /* ---------- shared result panel ---------- */
  function paint(row, note){
    current = row;
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

  function drawGauges(){
    const v=pxPerMm();
    const picks=RING_SIZES.filter(r=>Number.isInteger(r.us)&&r.us>=4&&r.us<=13);
    $('gaugeWrap').innerHTML=picks.map(r=>{
      const px=r.dia*v;
      return `<div class="gauge" data-us="${r.us}">
        <div class="ring" style="width:${px}px;height:${px}px"></div>
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

  /* ---------- init ---------- */
  buildChart();
  fillValues();
  applyCal(pxPerMm());
  $('calRange').value = pxPerMm();
  setCalCollapsed(localStorage.getItem(CAL_DONE)==='1');
})();
document.getElementById('yr').textContent=new Date().getFullYear();
