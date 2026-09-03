/* CaratBase — Guess the Carat + home page behaviour */

/* ---------- seeded RNG so everyone gets the same stone on the same day ---------- */
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);
  t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
function dayKey(d){d=d||new Date();return d.toISOString().slice(0,10)}
function dayNumber(d){return Math.floor(Date.parse(dayKey(d))/86400000)}

/* ---------- draw a round brilliant at true face-up scale ---------- */
function diamondSVG(mm){
  const VB=60, cx=30, bandTop=30.5, r=mm/2, cy=bandTop-r+0.6;
  const ring=(n,rad,off)=>Array.from({length:n},(_,i)=>{
    const a=off+i*2*Math.PI/n;return[cx+rad*Math.cos(a),cy+rad*Math.sin(a)];});
  const P=p=>p.map(([x,y])=>x.toFixed(2)+','+y.toFixed(2)).join(' ');

  const table  = ring(8,r*0.52,Math.PI/8);
  const girdle = ring(8,r,Math.PI/8);
  const girdle2= ring(8,r,0);

  let facets='';
  table.forEach((t,i)=>{ const g=girdle[i];
    facets+=`<line x1="${t[0].toFixed(2)}" y1="${t[1].toFixed(2)}" x2="${g[0].toFixed(2)}" y2="${g[1].toFixed(2)}"/>`; });
  table.forEach((t,i)=>{ const n=table[(i+1)%8], mx=(t[0]+n[0])/2, my=(t[1]+n[1])/2, g=girdle2[i];
    facets+=`<line x1="${mx.toFixed(2)}" y1="${my.toFixed(2)}" x2="${g[0].toFixed(2)}" y2="${g[1].toFixed(2)}"/>`; });

  return `<svg viewBox="0 0 ${VB} ${VB}" xmlns="http://www.w3.org/2000/svg" role="img"
    aria-label="A diamond drawn to true scale on a ring finger">
  <defs>
    <linearGradient id="fing" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#2A2A34"/><stop offset=".42" stop-color="#3A3A46"/>
      <stop offset="1" stop-color="#22222B"/>
    </linearGradient>
    <linearGradient id="band" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#8A7238"/><stop offset=".38" stop-color="#E3C88A"/>
      <stop offset=".62" stop-color="#C9A961"/><stop offset="1" stop-color="#7E6730"/>
    </linearGradient>
    <radialGradient id="stone" cx=".38" cy=".32" r=".82">
      <stop offset="0" stop-color="#FFFFFF"/><stop offset=".38" stop-color="#DCF2FA"/>
      <stop offset=".78" stop-color="#9FD3E6"/><stop offset="1" stop-color="#6FA8C0"/>
    </radialGradient>
    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="1.1" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect x="21.5" y="11" width="17" height="49" rx="8.5" fill="url(#fing)"/>
  <rect x="21.5" y="11" width="17" height="49" rx="8.5" fill="none" stroke="#454553" stroke-width=".3"/>
  <rect x="20.6" y="${bandTop}" width="18.8" height="5.4" rx="1.1" fill="url(#band)"/>

  <g filter="url(#glow)">
    <circle cx="${cx}" cy="${cy.toFixed(2)}" r="${r.toFixed(2)}" fill="url(#stone)"/>
    <circle cx="${cx}" cy="${cy.toFixed(2)}" r="${r.toFixed(2)}" fill="none" stroke="#FFFFFF" stroke-width=".16" opacity=".85"/>
    <polygon points="${P(table)}" fill="#F2FBFF" opacity=".55"/>
    <g stroke="#5E93AC" stroke-width=".13" opacity=".8">${facets}</g>
    <polygon points="${P(table)}" fill="none" stroke="#FFFFFF" stroke-width=".16" opacity=".9"/>
  </g>

  <g fill="#6E6E7D" font-family="Inter,sans-serif" font-size="2.4" text-anchor="middle">
    <text x="30" y="8">average ring finger — 17 mm across</text>
  </g>
</svg>`;
}

/* ---------- build today's stone ---------- */
function todaysStone(){
  const rnd = mulberry32(dayNumber() * 2654435761 % 2147483647);
  const pool = CARAT_MM.filter(r => r.ct >= 0.3 && r.ct <= 3.5);
  const ct   = pool[Math.floor(rnd() * pool.length)].ct;
  const colors   = ['D','E','F','G','G','H','H','I','J'];
  const clarities= ['VVS2','VS1','VS1','VS2','VS2','SI1','SI1','SI2'];
  const cuts     = ['Excellent','Very Good','Very Good','Good'];
  const origin   = rnd() < 0.25 ? 'Lab-grown' : 'Natural';
  return {
    carat: ct, mm: mmForCarat(ct),
    color:   colors[Math.floor(rnd()*colors.length)],
    clarity: clarities[Math.floor(rnd()*clarities.length)],
    cut:     cuts[Math.floor(rnd()*cuts.length)],
    shape:'Round', origin, cert: origin === 'Lab-grown' ? 'IGI' : 'GIA'
  };
}

/* ---------- game ---------- */
(function(){
  const stage=document.getElementById('stage'); if(!stage) return;
  const stone=todaysStone(), val=valueDiamond(stone);
  const rng=document.getElementById('guessRange'), num=document.getElementById('guessNum');
  const lock=document.getElementById('lockBtn'), reveal=document.getElementById('reveal');
  const guessBox=document.getElementById('guessBox'), key='cb_game_'+dayKey();

  stage.innerHTML=diamondSVG(stone.mm);
  document.getElementById('dayLabel').textContent=
    new Date().toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric'});

  const streak=parseInt(localStorage.getItem('cb_streak')||'0',10);
  document.getElementById('streakPill').textContent='Streak '+streak;

  rng.addEventListener('input',()=>{num.textContent=(rng.value/100).toFixed(2)});

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
    if(window.cbTrack) cbTrack('tool_use',{tool:'guess_the_carat',off:+off.toFixed(3),
      carat:actual,origin:stone.origin});
  }

  lock.addEventListener('click',()=>{
    const guess=rng.value/100;
    const off=Math.abs(guess-stone.carat)/stone.carat;
    localStorage.setItem('cb_streak',String(off<=0.20?streak+1:0));
    localStorage.setItem(key,JSON.stringify({guess}));
    show(guess);
  });

  const prev=localStorage.getItem(key);
  if(prev){ try{ show(JSON.parse(prev).guess); }catch{} }

  document.getElementById('shareBtn').addEventListener('click',e=>{
    const g=JSON.parse(localStorage.getItem(key)||'{}').guess||0;
    const txt=`CaratBase — Guess the Carat, ${dayKey()}\nGuessed ${g.toFixed(2)} ct · actual ${stone.carat.toFixed(2)} ct\nRetail ${fmt(val.retailLow)} · resells for ${fmt(val.resaleLow)}\ncaratbase.com`;
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
