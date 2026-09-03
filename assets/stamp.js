/* CaratBase — hallmark lookup */
(function(){
  const input=document.getElementById('stampInput');
  const out=document.getElementById('stampResults');
  const chips=document.getElementById('chips');
  if(!input) return;

  const COMMON=['925','750','585','417','375','916','PT950','GF','EPNS','GP','999','800'];
  chips.innerHTML=COMMON.map(c=>`<button class="chip" data-c="${c}">${c}</button>`).join('');
  chips.addEventListener('click',e=>{
    const c=e.target.dataset.c; if(!c) return;
    input.value=c; run(c);
  });

  const badge=v=>({
    solid:'<span class="pill pill-good">Solid precious metal</span>',
    filled:'<span class="pill">Partial — low value</span>',
    plated:'<span class="pill pill-bad">Plated — no metal value</span>',
    lab:'<span class="pill pill-ice">Real diamond, weak resale</span>',
    none:'<span class="pill pill-bad">No precious metal</span>'
  }[v]||'');

  function search(qRaw){
    const q=qRaw.toLowerCase().replace(/[\s.\-]/g,'');
    if(!q) return [];
    return STAMPS.filter(s=>{
      const hay=[s.code,...(s.alias||[])].map(x=>String(x).toLowerCase().replace(/[\s.\-]/g,''));
      return hay.some(h=>h===q) || hay.some(h=>h.includes(q)&&q.length>=2)
          || s.metal.toLowerCase().includes(q);
    }).slice(0,6);
  }

  /* The readout carries the verdict; the cards below carry the detail. */
  function paintOut(hit){
    const box=document.getElementById('stampOut');
    if(!hit){
      box.innerHTML=`<div class="lab">No match</div>
        <div class="big" style="font-size:38px">?</div>
        <div class="sub">Marks wear down and are often partly struck. Try just the digits,
          or look for a second mark elsewhere on the piece.</div>`;
      return;
    }
    const verdict={
      solid:['Solid precious metal','#7FD9A8'],
      filled:['Partial — low value','#E8D19A'],
      plated:['Plated — no metal value','#F0928E'],
      lab:['Real diamond, weak resale','#9FD8EC'],
      none:['No precious metal','#F0928E']
    }[hit.value]||['','#F6F1E6'];
    box.innerHTML=`
      <div class="lab">${hit.metal}</div>
      <div class="big">${hit.code}</div>
      <div class="sub" style="color:${verdict[1]};font-weight:600;margin-top:6px">${verdict[0]}</div>
      <div class="split" style="grid-template-columns:1fr">
        <div><div class="lab">Purity</div><div class="v" style="font-size:19px">${hit.purity}</div></div>
      </div>
      <div class="note">${hit.worth}</div>`;
  }

  function run(q){
    const hits=search(q);
    if(!q.trim()){ out.innerHTML=''; paintOut(null); 
      document.getElementById('stampOut').innerHTML=
        `<div class="lab">Waiting for a mark</div><div class="big" style="font-size:38px">—</div>
         <div class="sub">Enter a stamp and its meaning appears here.</div>`;
      return; }
    if(!hits.length){
      paintOut(null);
      out.innerHTML=`<div class="panel"><h3>No match for "${q}"</h3>
        <p class="small" style="margin-top:8px">Marks can be worn or partially struck. Try just the
        digits, or look for a second mark elsewhere on the piece — many items carry a purity mark
        and a separate maker's mark. If there is no stamp at all, that does not always mean the
        piece is fake; older and handmade jewellery is often unmarked.</p></div>`;
      return;
    }
    paintOut(hits[0]);
    out.innerHTML=hits.map(s=>`
      <div class="stamp-card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:14px;flex-wrap:wrap">
          <div><div class="stamp-code">${s.code}</div>
            <div class="small" style="margin-top:4px">${s.metal} · ${s.purity}</div></div>
          <div>${badge(s.value)}</div>
        </div>
        <p style="margin-top:14px;font-size:15px;color:var(--ink-2)">${s.note}</p>
        <p style="margin-top:10px;font-size:15px;color:var(--ink)"><strong>What it is worth:</strong> ${s.worth}</p>
      </div>`).join('');
    if(window.cbTrack) cbTrack('tool_use',{tool:'stamp_lookup',query:q,hits:hits.length});
  }

  let t; input.addEventListener('input',()=>{clearTimeout(t);t=setTimeout(()=>run(input.value),260)});
  const pre=new URLSearchParams(location.search).get('q');
  if(pre){ input.value=pre; run(pre); }
})();
document.getElementById('yr').textContent=new Date().getFullYear();
