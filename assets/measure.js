/* CaratBase — photo measurement UI.
   Two phases: mark the card's four corners (which sets the perspective transform), then drag
   two points across whatever you want measured. Everything stays in the browser. */
(function(){
  const $=id=>document.getElementById(id);
  if(!$('mCanvas')) return;

  const cv=$('mCanvas'), ctx=cv.getContext('2d');
  let img=null, phase='card', card=[], span=[], drag=null, H=null, mode='ring';

  const MODES={
    ring:   {label:'Ring inner diameter', help:'Drag the two points across the <strong>inside</strong> of the band, through the centre.'},
    stone:  {label:'Diamond / stone width', help:'Drag the two points across the widest part of the stone, edge to edge.'},
    band:   {label:'Band width',           help:'Drag the two points across the width of the band, from edge to edge.'}
  };
  $('mMode').innerHTML=Object.entries(MODES).map(([k,m])=>
    `<button data-m="${k}"${k===mode?' class="on"':''}>${m.label}</button>`).join('');
  $('mMode').addEventListener('click',e=>{
    const m=e.target.dataset.m; if(!m) return;
    mode=m;
    $('mMode').querySelectorAll('button').forEach(b=>b.classList.toggle('on',b.dataset.m===m));
    if(phase==='span'){ $('markHelp').innerHTML=MODES[mode].help; }
    compute();
  });

  /* ---------- photo in ---------- */
  $('mPick').onclick=()=>$('mFile').click();
  $('mFile').addEventListener('change',e=>{
    const f=e.target.files&&e.target.files[0]; if(!f) return;
    const url=URL.createObjectURL(f);
    const im=new Image();
    im.onload=()=>{ URL.revokeObjectURL(url); img=im; startCard(); };
    im.onerror=()=>{ $('outSub').textContent='That file could not be read as an image.'; };
    im.src=url;
    if(window.cbTrack) cbTrack('tool_use',{tool:'photo_measure',step:'photo'});
  });

  function fit(){
    const maxW=Math.min(cv.parentElement.clientWidth, 900);
    const scale=maxW/img.width;
    cv.width=Math.round(img.width*scale);
    cv.height=Math.round(img.height*scale);
    cv.style.height='auto';
  }

  function startCard(){
    $('stepPhoto').classList.add('hide');
    $('stepMark').classList.remove('hide');
    fit();
    const w=cv.width, h=cv.height;
    // sensible starting quad, roughly card-shaped, for the user to drag into place
    card=[[w*0.18,h*0.30],[w*0.68,h*0.30],[w*0.68,h*0.62],[w*0.18,h*0.62]];
    phase='card';
    $('markTitle').textContent='2. Mark the card';
    $('markHelp').innerHTML='Drag the four markers onto the <strong>corners of the card</strong>, '+
      'in any order as long as they stay in sequence around it. Pinch-zoom the page if you need to be precise.';
    $('mNext').textContent='Card corners are set';
    $('mStatus').textContent='step 2 of 3 — mark the card';
    draw();
  }

  function startSpan(){
    H=cardHomography(card);
    if(!H){ $('mTilt').innerHTML='<span style="color:var(--bad)">Those corners do not form a '+
      'quadrilateral. Please reposition them.</span>'; return; }
    const t=tiltEstimate(card);
    $('mTilt').innerHTML = t.degrees>28
      ? `<span style="color:var(--bad)">That shot is about ${t.degrees}° off square — quite oblique. `+
        `The correction still applies, but a flatter photo will measure better.</span>`
      : `<span style="color:var(--good)">Shot is about ${t.degrees}° off square — well within range.</span>`;
    phase='span';
    const w=cv.width, h=cv.height;
    span=[[w*0.35,h*0.72],[w*0.55,h*0.72]];
    $('markTitle').textContent='3. Measure it';
    $('markHelp').innerHTML=MODES[mode].help;
    $('mNext').textContent='Re-mark the card';
    $('mStatus').textContent='step 3 of 3 — drag the two points';
    $('whatSection').scrollIntoView({behavior:'smooth',block:'nearest'});
    draw(); compute();
  }

  $('mNext').onclick=()=>{ phase==='card' ? startSpan() : startCard(); };
  $('mRestart').onclick=()=>{
    img=null; H=null; $('stepMark').classList.add('hide'); $('stepPhoto').classList.remove('hide');
    $('mFile').value=''; $('outMm').textContent='—'; $('outSub').textContent='Add a photo to begin.';
    $('outReads').textContent='—'; $('outWorth').textContent='—'; $('outNote').textContent='';
    $('mTilt').textContent=''; $('mStatus').textContent='step 1 of 3 — add a photo';
  };

  /* ---------- drawing ---------- */
  function draw(){
    if(!img) return;
    ctx.drawImage(img,0,0,cv.width,cv.height);
    const pts = phase==='card' ? card : span;

    if(phase==='card'){
      ctx.beginPath();
      card.forEach((p,i)=> i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));
      ctx.closePath();
      ctx.fillStyle='rgba(255,31,143,.14)'; ctx.fill();
      ctx.strokeStyle='#FF1F8F'; ctx.lineWidth=2.5; ctx.stroke();
    } else {
      // keep the card outline visible so it is obvious the scale is still anchored
      ctx.beginPath();
      card.forEach((p,i)=> i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));
      ctx.closePath(); ctx.strokeStyle='rgba(255,31,143,.5)'; ctx.lineWidth=1.5; ctx.stroke();
      ctx.beginPath(); ctx.moveTo(span[0][0],span[0][1]); ctx.lineTo(span[1][0],span[1][1]);
      ctx.strokeStyle='#00C853'; ctx.lineWidth=3; ctx.stroke();
    }
    pts.forEach((p,i)=>{
      ctx.beginPath(); ctx.arc(p[0],p[1],11,0,7);
      ctx.fillStyle = phase==='card' ? '#FF1F8F' : '#00C853';
      ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=2.5; ctx.stroke();
      ctx.fillStyle='#fff'; ctx.font='bold 11px Inter,sans-serif'; ctx.textAlign='center';
      ctx.fillText(String(i+1), p[0], p[1]+4);
    });
  }

  /* ---------- dragging (mouse and touch) ---------- */
  function at(e){
    const r=cv.getBoundingClientRect();
    const t=e.touches?e.touches[0]:e;
    return [(t.clientX-r.left)*(cv.width/r.width), (t.clientY-r.top)*(cv.height/r.height)];
  }
  function down(e){
    const p=at(e), pts = phase==='card'?card:span;
    let best=-1, bd=1e9;
    pts.forEach((q,i)=>{ const d=Math.hypot(q[0]-p[0],q[1]-p[1]); if(d<bd){bd=d;best=i;} });
    if(bd<40){ drag=best; e.preventDefault(); }
  }
  function move(e){
    if(drag===null) return;
    const p=at(e), pts = phase==='card'?card:span;
    pts[drag]=[Math.max(0,Math.min(cv.width,p[0])), Math.max(0,Math.min(cv.height,p[1]))];
    e.preventDefault(); draw(); if(phase==='span') compute();
  }
  function up(){ drag=null; }
  cv.addEventListener('mousedown',down); cv.addEventListener('touchstart',down,{passive:false});
  addEventListener('mousemove',move);    cv.addEventListener('touchmove',move,{passive:false});
  addEventListener('mouseup',up);        cv.addEventListener('touchend',up);

  /* ---------- result ---------- */
  function compute(){
    if(!H || phase!=='span') return;
    const mm=measureMm(H,span[0],span[1]);
    $('outMm').textContent=mm.toFixed(2)+' mm';
    $('outLab').textContent=MODES[mode].label;

    if(mode==='ring'){
      const row=nearestRing(mm,'dia');
      $('outSub').textContent='inside diameter of the band';
      $('outReads').textContent=row?('US '+row.us+' · UK '+row.uk):'—';
      $('outWorth').textContent=row?(row.eu+' EU'):'—';
      $('outNote').innerHTML=row
        ? `That is a US ${row.us}, UK ${row.uk}, EU ${row.eu}. `+
          `<a href="ring-size.html">Check it against true-scale circles</a> before ordering.`
        : 'Outside the normal adult range — re-check the two points.';
    } else if(mode==='stone'){
      const ct=+Math.pow(mm/6.5,3).toFixed(2);
      const v=valueDiamond({carat:ct,color:'G',clarity:'VS2',cut:'Very Good',shape:'Round',
        origin:'Natural',cert:'GIA'});
      $('outSub').textContent='width across the stone';
      $('outReads').textContent=ct.toFixed(2)+' ct';
      $('outWorth').textContent=v?fmt(v.retailLow)+'–'+fmt(v.retailHigh):'—';
      $('outNote').innerHTML='Carat estimated from diameter for a round brilliant, and weight '+
        'rises with the <em>cube</em> of the width — so measure carefully. '+
        '<a href="value.html">Value it properly</a> with colour and clarity.';
    } else {
      $('outSub').textContent='width of the band';
      $('outReads').textContent=mm.toFixed(1)+' mm wide';
      $('outWorth').textContent='—';
      $('outNote').innerHTML='Add the thickness and metal in the '+
        '<a href="metals.html">gold calculator</a> to turn this into a weight and a value.';
    }
    if(window.cbTrack) cbTrack('tool_use',{tool:'photo_measure',mode,mm:+mm.toFixed(2)});
  }

  addEventListener('resize',()=>{ if(img && phase!=='photo'){ } });
})();
document.getElementById('yr').textContent=new Date().getFullYear();
