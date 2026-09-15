/* CaratBase — homepage showcase: a real stone, to scale, with its two numbers.
   Cycles through shapes so the first thing a visitor sees is the site's whole argument:
   this is what it looks like, this is what it costs, this is what it fetches back. */
(function(){
  const stage=document.getElementById('scStage'), cap=document.getElementById('scCap'),
        dots=document.getElementById('scDots');
  if(!stage || typeof shapeOnFinger!=='function') return;
  const SET=[
    {shape:'Round',   ct:1.0,  color:'G', clarity:'VS2'},
    {shape:'Oval',    ct:1.5,  color:'H', clarity:'VS1'},
    {shape:'Cushion', ct:2.0,  color:'G', clarity:'VS2'},
    {shape:'Pear',    ct:1.25, color:'F', clarity:'VVS2'},
    {shape:'Emerald', ct:2.5,  color:'G', clarity:'VS1'},
    {shape:'Round',   ct:1.0,  color:'G', clarity:'VS2', lab:true},
  ];
  const money=n=>'$'+Math.round(n).toLocaleString('en-US');
  let i=0, timer;
  dots.innerHTML=SET.map((_,k)=>`<i${k===0?' class="on"':''}></i>`).join('');
  function show(k, instant){
    const o=SET[k]; const v=valueDiamond({carat:o.ct,shape:o.shape,color:o.color,clarity:o.clarity,cut:'Very Good',origin:o.lab?'Lab-grown':'Natural',cert:o.lab?'IGI':'GIA'});
    const d=shapeDims(o.shape,o.ct);
    const paint=()=>{
      stage.innerHTML=shapeOnFinger(o.shape,o.ct);
      cap.innerHTML=`<div class="spec">${o.ct.toFixed(2)} ct ${o.shape.toLowerCase()}${o.lab?' · lab-grown':''}
          <small>${o.color} colour · ${o.clarity} · ${d.l} × ${d.w} mm face-up</small></div>
        <div class="nums"><div class="r">Retail <b>${money(v.retailLow)}–${money(v.retailHigh)}</b></div>
          <div class="s">Resells for ${money(v.resaleLow)}–${money(v.resaleHigh)}</div></div>`;
      dots.querySelectorAll('i').forEach((el,j)=>el.classList.toggle('on',j===k));
      stage.classList.remove('out'); cap.classList.remove('out');
    };
    if(instant){ paint(); return; }
    stage.classList.add('out'); cap.classList.add('out');
    setTimeout(paint, 360);
  }
  function next(){ i=(i+1)%SET.length; show(i); }
  show(0,true);
  timer=setInterval(next, 4200);
  dots.addEventListener('click',e=>{ const j=[...dots.children].indexOf(e.target); if(j>=0){ clearInterval(timer); i=j; show(i); timer=setInterval(next,6000);} });
  document.getElementById('showcase').addEventListener('click',e=>{ if(!e.target.closest('.dots')) location.href='value.html'; });
  document.getElementById('showcase').style.cursor='pointer';
})();
