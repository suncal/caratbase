/* CaratBase — the vault: saved pieces, kept on-device */
const Vault = {
  key:'cb_vault',
  all(){ try{ return JSON.parse(localStorage.getItem(this.key)||'[]') }catch{ return [] } },
  save(list){ localStorage.setItem(this.key, JSON.stringify(list.slice(0,120))) },
  add(item){ const l=this.all(); l.unshift({...item, id:Date.now(), added:Date.now()}); this.save(l); return l.length },
  remove(id){ this.save(this.all().filter(x=>x.id!==id)) },
  count(){ return this.all().length }
};

(function(){
  const list=document.getElementById('vaultList'); if(!list) return;
  const totals=document.getElementById('vaultTotals');
  const cta=document.getElementById('vaultCta');

  function revalue(p){
    const v=valueDiamond(p);
    const metal=valueMetal(p.karat,p.grams);
    return v?{...v,metal,
      retailLow:v.retailLow+metal,retailHigh:v.retailHigh+metal,
      resaleLow:v.resaleLow+metal,resaleHigh:v.resaleHigh+metal}:null;
  }

  function render(){
    const items=Vault.all();

    if(!items.length){
      totals.innerHTML='';
      list.innerHTML=`<div class="vault-empty">
        <h3 style="margin-bottom:10px">Your vault is empty</h3>
        <p class="small" style="max-width:44ch;margin:0 auto 20px">
          Value a diamond and save it here. Add every piece you own and you will have a
          running record of what the whole collection is worth.</p>
        <a href="value.html" class="btn btn-gold">Value your first piece</a></div>`;
      cta.innerHTML='';
      return;
    }

    let rL=0,rH=0,sL=0,sH=0;
    const rows=items.map(p=>{
      const v=revalue(p); if(!v) return '';
      rL+=v.retailLow; rH+=v.retailHigh; sL+=v.resaleLow; sH+=v.resaleHigh;
      const nick=p.nickname||`${p.carat} ct ${p.shape.toLowerCase()}`;
      return `<div class="vault-item">
        <div class="thumb">${diamondSVG(mmForCarat(parseFloat(p.carat)))}</div>
        <div class="body">
          <div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:baseline">
            <h3 style="font-size:19px">${nick}</h3>
            <span class="pill${p.origin==='Lab-grown'?' pill-ice':''}">${p.origin}</span>
          </div>
          <p class="small" style="margin-top:4px">
            ${p.color} · ${p.clarity} · ${p.cut} cut${p.cert&&p.cert!=='None'?' · '+p.cert:''}${p.certNo?' #'+p.certNo:''}${p.karat&&p.karat!=='None / not sure'?' · '+p.karat+' setting':''}
          </p>
          <div style="display:flex;gap:22px;margin-top:10px;flex-wrap:wrap">
            <div><div class="small">Retail</div>
              <strong class="mono">${fmt(v.retailLow)}–${fmt(v.retailHigh)}</strong></div>
            <div><div class="small">Resale</div>
              <strong class="mono" style="color:var(--bad)">${fmt(v.resaleLow)}–${fmt(v.resaleHigh)}</strong></div>
          </div>
        </div>
        <button class="btn btn-ghost btn-sm" data-del="${p.id}">Remove</button>
      </div>`;
    }).join('');

    totals.innerHTML=`
      <div class="stat"><div class="k">Pieces in vault</div><div class="v gold">${items.length}</div></div>
      <div class="stat"><div class="k">Total retail value</div><div class="v">${fmt(rL)}–${fmt(rH)}</div></div>
      <div class="stat"><div class="k">Total if you sold today</div><div class="v bad">${fmt(sL)}–${fmt(sH)}</div></div>`;
    list.innerHTML=rows;

    cta.innerHTML=`<div class="capture center">
      <h2 style="font-size:28px">${items.length} piece${items.length>1?'s':''}, ${fmt(rL)}–${fmt(rH)} of cover</h2>
      <p class="small" style="margin:12px auto 20px;max-width:50ch">
        Most collections this size are insured for the wrong amount, or not at all — insurers
        need a documented value and appraisals cost $50–300 per item. Get a free vault report
        you can send straight to an insurer.</p>
      <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
        <a href="value.html" class="btn btn-gold">Add another piece</a>
        <a href="metals.html" class="btn btn-ghost">Today's metal prices</a></div></div>`;

    list.querySelectorAll('[data-del]').forEach(b=>b.onclick=()=>{
      Vault.remove(parseInt(b.dataset.del,10)); render();
      if(window.cbTrack) cbTrack('tool_use',{tool:'vault_remove'});
    });
  }

  render();
  document.addEventListener('cb:spot', render);  // live metal prices arrived
  if(window.cbTrack) cbTrack('tool_use',{tool:'vault_view',pieces:Vault.count()});
})();
