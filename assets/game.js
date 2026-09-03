/* CaratBase — Guess the Carat: daily stone, archive, streaks and stats */

function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);
  t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function dayKey(d){d=d||new Date();return d.toISOString().slice(0,10)}
function dayNumber(k){return Math.floor(Date.parse(k)/86400000)}

/* ---------- a round brilliant drawn at true face-up scale ---------- */
function diamondSVG(mm){
  const VB=60, cx=30, bandTop=30.5, r=mm/2, cy=bandTop-r+0.6;
  const ring=(n,rad,off)=>Array.from({length:n},(_,i)=>{
    const a=off+i*2*Math.PI/n;return[cx+rad*Math.cos(a),cy+rad*Math.sin(a)];});
  const P=p=>p.map(([x,y])=>x.toFixed(2)+','+y.toFixed(2)).join(' ');
  const table=ring(8,r*0.52,Math.PI/8), girdle=ring(8,r,Math.PI/8), girdle2=ring(8,r,0);
  const uid='d'+Math.round(mm*100);

  let facets='';
  table.forEach((t,i)=>{const g=girdle[i];
    facets+=`<line x1="${t[0].toFixed(2)}" y1="${t[1].toFixed(2)}" x2="${g[0].toFixed(2)}" y2="${g[1].toFixed(2)}"/>`;});
  table.forEach((t,i)=>{const n=table[(i+1)%8],mx=(t[0]+n[0])/2,my=(t[1]+n[1])/2,g=girdle2[i];
    facets+=`<line x1="${mx.toFixed(2)}" y1="${my.toFixed(2)}" x2="${g[0].toFixed(2)}" y2="${g[1].toFixed(2)}"/>`;});

  return `<svg viewBox="0 0 ${VB} ${VB}" xmlns="http://www.w3.org/2000/svg" role="img"
    aria-label="A ${mm} millimetre diamond drawn to true scale on a ring finger">
  <defs>
    <linearGradient id="fing${uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#E7DBCF"/><stop offset=".42" stop-color="#F6EDE4"/>
      <stop offset="1" stop-color="#E0D2C4"/></linearGradient>
    <linearGradient id="band${uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8A7238"/><stop offset=".38" stop-color="#E3C88A"/>
      <stop offset=".62" stop-color="#C9A961"/><stop offset="1" stop-color="#7E6730"/></linearGradient>
    <radialGradient id="stone${uid}" cx=".38" cy=".32" r=".82">
      <stop offset="0" stop-color="#FFFFFF"/><stop offset=".36" stop-color="#D3EEF9"/>
      <stop offset=".76" stop-color="#8CC6DD"/><stop offset="1" stop-color="#4E8FA8"/></radialGradient>
  </defs>
  <rect x="21.5" y="11" width="17" height="49" rx="8.5" fill="url(#fing${uid})"/>
  <rect x="21.5" y="11" width="17" height="49" rx="8.5" fill="none" stroke="#D5C6B7" stroke-width=".3"/>
  <rect x="20.6" y="${bandTop}" width="18.8" height="5.4" rx="1.1" fill="url(#band${uid})"/>
  <g>
    <circle cx="${cx}" cy="${cy.toFixed(2)}" r="${r.toFixed(2)}" fill="url(#stone${uid})"/>
    <circle cx="${cx}" cy="${cy.toFixed(2)}" r="${r.toFixed(2)}" fill="none" stroke="#3E7C95" stroke-width=".18" opacity=".7"/>
    <polygon points="${P(table)}" fill="#F4FCFF" opacity=".8"/>
    <g stroke="#5E93AC" stroke-width=".13" opacity=".65">${facets}</g>
    <polygon points="${P(table)}" fill="none" stroke="#3E7C95" stroke-width=".15" opacity=".55"/>
  </g>
  <g fill="#8C857A" font-family="Inter,sans-serif" font-size="2.4" text-anchor="middle">
    <text x="30" y="8">average ring finger — 17 mm across</text></g>
</svg>`;
}

/* ---------- deterministic stone for any date ---------- */
function stoneFor(key){
  const rnd=mulberry32(dayNumber(key)*2654435761%2147483647);
  const pool=CARAT_MM.filter(r=>r.ct>=0.3&&r.ct<=3.5);
  const ct=pool[Math.floor(rnd()*pool.length)].ct;
  const colors=['D','E','F','G','G','H','H','I','J'];
  const clarities=['VVS2','VS1','VS1','VS2','VS2','SI1','SI1','SI2'];
  const cuts=['Excellent','Very Good','Very Good','Good'];
  const origin=rnd()<0.25?'Lab-grown':'Natural';
  return {carat:ct, mm:mmForCarat(ct),
    color:colors[Math.floor(rnd()*colors.length)],
    clarity:clarities[Math.floor(rnd()*clarities.length)],
    cut:cuts[Math.floor(rnd()*cuts.length)],
    shape:'Round', origin, cert:origin==='Lab-grown'?'IGI':'GIA'};
}

/* ---------- history ---------- */
const Hist={
  key:'cb_history',
  all(){try{return JSON.parse(localStorage.getItem(this.key)||'{}')}catch{return{}}},
  set(k,v){const h=this.all();h[k]=v;localStorage.setItem(this.key,JSON.stringify(h))},
  get(k){return this.all()[k]}
};

/* ---------- the game ---------- */
(function(){
  const stage=document.getElementById('stage'); if(!stage) return;

  const qs=new URLSearchParams(location.search);
  const today=dayKey();
  let key=qs.get('d')||today;
  if(!/^\d{4}-\d{2}-\d{2}$/.test(key)||key>today) key=today;

  const stone=stoneFor(key), val=valueDiamond(stone);
  const rng=document.getElementById('guessRange'), num=document.getElementById('guessNum');
  const reveal=document.getElementById('reveal'), guessBox=document.getElementById('guessBox');

  stage.innerHTML=diamondSVG(stone.mm);
  const label=new Date(key+'T12:00:00Z').toLocaleDateString('en-US',
    {weekday:'long',month:'long',day:'numeric'});
  document.getElementById('dayLabel').innerHTML =
    key===today ? label : `${label} &nbsp;·&nbsp; <a href="./">back to today</a>`;

  rng.addEventListener('input',()=>{num.textContent=(rng.value/100).toFixed(2)});

  function streaks(){
    const h=Hist.all(); const keys=Object.keys(h).sort();
    let cur=0,best=0;
    // current streak counts back from today through consecutive played+close days
    for(let i=0;;i++){
      const d=new Date(); d.setUTCDate(d.getUTCDate()-i);
      const rec=h[dayKey(d)];
      if(rec&&rec.off<=0.20) cur++; else break;
    }
    let run=0,prev=null;
    keys.forEach(k=>{
      const rec=h[k];
      const consecutive = prev && dayNumber(k)-dayNumber(prev)===1;
      run = (rec.off<=0.20) ? (consecutive?run+1:1) : 0;
      best=Math.max(best,run); prev=k;
    });
    return {cur,best:Math.max(best,cur)};
  }

  function paintStats(){
    const grid=document.getElementById('statsGrid'); if(!grid) return;
    const h=Hist.all(), recs=Object.values(h);
    const s=streaks();
    const avg=recs.length?recs.reduce((a,r)=>a+r.off,0)/recs.length:0;
    grid.innerHTML=`
      <div class="stat"><div class="k">Played</div><div class="v">${recs.length}</div></div>
      <div class="stat"><div class="k">Current streak</div><div class="v gold">${s.cur}</div></div>
      <div class="stat"><div class="k">Best streak</div><div class="v">${s.best}</div></div>
      <div class="stat"><div class="k">Average miss</div>
        <div class="v ${avg<=0.2?'good':''}">${recs.length?(avg*100).toFixed(0)+'%':'—'}</div></div>`;

    const buckets=[['Within 10%',0,.10],['10–25%',.10,.25],['25–50%',.25,.50],['Over 50%',.50,99]];
    const counts=buckets.map(([,lo,hi])=>recs.filter(r=>r.off>lo&&r.off<=hi||(lo===0&&r.off<=hi)).length);
    const max=Math.max(1,...counts);
    document.getElementById('statsDist').innerHTML= recs.length? buckets.map(([lab],i)=>`
      <div style="margin-bottom:11px">
        <div style="display:flex;justify-content:space-between;font-size:13.5px">
          <span style="color:var(--ink-2)">${lab}</span><strong class="mono">${counts[i]}</strong></div>
        <div style="height:6px;background:var(--line-2);border-radius:999px;overflow:hidden;margin-top:5px">
          <span style="display:block;height:100%;width:${counts[i]/max*100}%;
            background:linear-gradient(90deg,var(--gold),#D8BA76)"></span></div>
      </div>`).join('') : '<p class="small">Play your first stone to start building a record.</p>';

    const pill=document.getElementById('streakPill');
    if(pill) pill.textContent='Streak '+s.cur;
  }

  function paintArchive(){
    const box=document.getElementById('archive'); if(!box) return;
    const h=Hist.all(); let out='';
    for(let i=0;i<14;i++){
      const d=new Date(); d.setUTCDate(d.getUTCDate()-i);
      const k=dayKey(d), st=stoneFor(k), rec=h[k];
      const done=!!rec;
      out+=`<a href="?d=${k}" style="display:flex;justify-content:space-between;align-items:center;
        gap:12px;padding:11px 0;border-bottom:1px solid var(--line);text-decoration:none;color:inherit">
        <span style="font-size:14px;color:var(--ink-2)">${i===0?'Today':
          new Date(k+'T12:00:00Z').toLocaleDateString('en-US',{month:'short',day:'numeric'})}</span>
        <span class="small">${done?st.carat.toFixed(2)+' ct':'not played'}</span>
        <span class="pill${done?(rec.off<=0.20?' pill-good':' pill-bad'):''}"
          style="min-width:64px;text-align:center">${done?(rec.off*100).toFixed(0)+'% off':'play'}</span></a>`;
    }
    box.innerHTML=out;
  }

  function show(guess){
    const actual=stone.carat, off=Math.abs(guess-actual)/actual;
    let title,cls;
    if(off<=0.10){title='Excellent eye.';cls='pill-good'}
    else if(off<=0.25){title='Close.';cls=''}
    else if(off<=0.50){title='Not quite.';cls=''}
    else {title='Way off.';cls='pill-bad'}

    document.getElementById('verdict').innerHTML=
      `<span class="pill ${cls}">${title}</span> <span class="small">You guessed ${guess.toFixed(2)} ct
       — that is ${(off*100).toFixed(0)}% ${guess>actual?'over':'under'}.</span>`;
    document.getElementById('rActual').textContent=actual.toFixed(2);
    document.getElementById('rRetail').textContent=fmt(val.retailLow)+'–'+fmt(val.retailHigh);
    document.getElementById('rResale').textContent=fmt(val.resaleLow)+'–'+fmt(val.resaleHigh);

    const keepPct=Math.round(val.resaleHigh/val.retailHigh*100);
    document.getElementById('rSpec').innerHTML=
      `${stone.origin} ${stone.shape.toLowerCase()} brilliant · ${stone.color} colour ·
       ${stone.clarity} · ${stone.cut} cut · ${stone.cert} · ${stone.mm} mm across.
       <strong style="color:var(--ink-2)">Resells for about ${keepPct}% of retail.</strong>
       ${val.isLab?' Lab-grown stones currently have very little secondary market.':''}`;

    guessBox.classList.add('hide'); reveal.classList.add('show');
    paintStats(); paintArchive();
  }

  document.getElementById('lockBtn').addEventListener('click',()=>{
    const guess=rng.value/100, off=Math.abs(guess-stone.carat)/stone.carat;
    Hist.set(key,{guess,actual:stone.carat,off:+off.toFixed(4)});
    show(guess);
    if(window.cbTrack) cbTrack('tool_use',{tool:'guess_the_carat',off:+off.toFixed(3),
      carat:stone.carat,origin:stone.origin,archive:key!==today});
  });

  const prev=Hist.get(key);
  if(prev) show(prev.guess); else { paintStats(); paintArchive(); }

  document.getElementById('shareBtn').addEventListener('click',e=>{
    const rec=Hist.get(key)||{guess:0};
    const txt=`CaratBase — Guess the Carat, ${key}\nGuessed ${rec.guess.toFixed(2)} ct · actual ${stone.carat.toFixed(2)} ct\nRetail ${fmt(val.retailLow)} · resells for ${fmt(val.resaleLow)}\ncaratbase.com`;
    navigator.clipboard?.writeText(txt);
    e.target.textContent='Copied'; setTimeout(()=>e.target.textContent='Copy result',1800);
  });
})();

/* ---------- the resale gap table ---------- */
(function(){
  const tb=document.querySelector('#gapTable tbody'); if(!tb) return;
  const rows=[
    {label:'0.50 ct natural', o:{carat:.5,  origin:'Natural'}},
    {label:'1.00 ct natural', o:{carat:1,   origin:'Natural'}},
    {label:'1.50 ct natural', o:{carat:1.5, origin:'Natural'}},
    {label:'2.00 ct natural', o:{carat:2,   origin:'Natural'}},
    {label:'3.00 ct natural', o:{carat:3,   origin:'Natural'}},
    {label:'1.00 ct lab-grown',o:{carat:1,  origin:'Lab-grown'}}
  ];
  tb.innerHTML=rows.map(r=>{
    const v=valueDiamond({color:'G',clarity:'VS2',cut:'Very Good',shape:'Round',
      cert:r.o.origin==='Lab-grown'?'IGI':'GIA',...r.o});
    const keep=Math.round(v.resaleHigh/v.retailHigh*100);
    return `<tr><td>${r.label}</td>
      <td class="num">${fmt(v.retailLow)}–${fmt(v.retailHigh)}</td>
      <td class="num">${fmt(v.resaleLow)}–${fmt(v.resaleHigh)}</td>
      <td class="num" style="color:${keep<20?'var(--bad)':'var(--warn)'};font-weight:600">${keep}%</td></tr>`;
  }).join('');
})();

/* ---------- email capture ---------- */
(function(){
  const f=document.getElementById('emailForm'); if(!f) return;
  f.addEventListener('submit',e=>{
    e.preventDefault();
    const email=document.getElementById('emailInput').value.trim();
    if(!email) return;
    if(window.cbTrack) cbTrack('email',{email,where:'home'});
    document.getElementById('emailMsg').innerHTML=
      '<span style="color:var(--good)">Saved. Value a stone and your report will be sent to '+email+'.</span>';
    f.reset();
  });
})();

document.getElementById('yr').textContent=new Date().getFullYear();
