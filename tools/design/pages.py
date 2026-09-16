"""Static tool/reference pages that don't come from the long-tail generator.
Each page is a shell (header, nav, footer, scripts) around a body and an inline script that
uses the site's real engines. Run: python3 tools/design/pages.py"""
import pathlib, json, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import icons
ROOT = pathlib.Path(__file__).resolve().parents[2]
ICON = "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 28 28'><polygon points='19.32,18.72 14,20.32 8.68,18.72 6.32,13.84 8.68,8.96 14,7.36 19.32,8.96 21.68,13.84' fill='%23C9A961' fill-opacity='.2' stroke='%23C9A961' stroke-width='1.4'/><polygon points='16.42,15.06 14,15.79 11.58,15.06 10.5,12.84 11.58,10.62 14,9.89 16.42,10.62 17.5,12.84' fill='%23C9A961' stroke='%238A6420'/></svg>"

def shell(name, title, desc, eyebrow, h1, lede, body, script='', scripts=(), schema=None, extra_head=''):
    sc = ''.join(f'<script src="assets/{s}"></script>\n' for s in ('data.js','analytics.js','spot.js','ticker.js','logo.js','nav.js','partners.js') + tuple(scripts))
    schema_tag = f'<script type="application/ld+json">{json.dumps(schema)}</script>' if schema else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://caratbase.com/{name}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="https://caratbase.com/{name}">
<meta property="og:image" content="https://caratbase.com/assets/img/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="{ICON}">
{schema_tag}{extra_head}
</head>
<body>
<header class="site-head"><div class="wrap head-in">
  <a href="index.html" class="logo"></a><nav class="nav"></nav>
</div></header>
<main class="wrap">
  <div class="tool-hero narrow">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
  </div>
{body}
</main>
<footer class="site-foot"><div class="wrap foot-in">
  <div>&copy; <span id="yr"></span> CaratBase &mdash; independent jewelry valuation reference.</div>
  <div style="display:flex;gap:20px;flex-wrap:wrap">
    <a href="methodology.html">How we value</a><a href="widgets.html">Widgets</a><a href="disclaimer.html">Disclaimer</a>
    <a href="privacy.html">Privacy</a><a href="terms.html">Terms</a></div>
</div><div class="wrap"><p class="disclaimer">CaratBase is not a licensed appraiser and does not buy or sell jewelry. Figures are estimates for information only, not an appraisal, an offer or financial advice.</p></div></footer>
{sc}<script>
document.getElementById('yr').textContent=new Date().getFullYear();
{script}
</script>
</body></html>
'''

def faq(qa):
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in qa]}

PAGES = {}

# ---------------------------------------------------------------- COMPARE
PAGES['compare.html'] = dict(
  title='Compare Two Diamonds Side by Side — Size, Price, Resale & Value | CaratBase',
  desc='Put two diamond specifications side by side: true face-up size, retail price, resale value, price per carat and which is the better buy. Natural or lab-grown.',
  eyebrow='Compare', h1='Compare two diamonds', lede='Two specifications, side by side, with everything that actually differs: how big each looks, what each costs, what each fetches back, and which one is the better buy for the money.',
  scripts=('shapes.js',),
  schema=faq([('Is a 0.9 carat diamond much smaller than a 1 carat?','No. Linear size scales with the cube root of weight, so a 0.90 ct round is about 6.27 mm across against 6.5 mm for a 1.00 ct — 3.5% shorter — while costing roughly 25% less because it sits below the 1 carat price step.'),
              ('Which is better value, a higher color or a higher clarity?','Below about G color and VS2 clarity the differences are invisible without a loupe. For the same money, weight and cut quality are what you can actually see.')]),
  body='''

  <section class="console">
    <div class="console-head"><span class="name"><span class="dot"></span> Compare</span><span class="status">size · price · resale · verdict</span></div>
    <div class="console-body">
      <div class="console-in"><h3>Diamond A</h3><div id="fA"></div><h3 style="margin-top:20px">Diamond B</h3><div id="fB"></div></div>
      <div class="console-out" id="cOut"><div class="lab">Waiting for input</div></div>
    </div>
  </section>
  <div class="chips" style="margin:14px 0 0"><span class="small" style="align-self:center">Quick comparisons:</span>
    <button class="chip" data-p="1|Round|G|VS2|Natural;0.9|Round|G|VS2|Natural">1.00 ct vs 0.90 ct</button>
    <button class="chip" data-p="1|Round|G|VS2|Natural;1|Round|G|VS2|Lab-grown">Natural vs lab-grown</button>
    <button class="chip" data-p="1|Round|G|VS2|Natural;1.3|Round|J|SI1|Natural">G/VS2 vs bigger J/SI1</button>
    <button class="chip" data-p="1.5|Round|G|VS2|Natural;1.5|Oval|G|VS2|Natural">Round vs oval, same weight</button>
  </div>
  <div class="grid g2" style="margin-top:22px" id="out"></div>
  <div id="shop"></div>
  <section class="narrow legal" style="margin-top:40px">
    <h2>How to read this</h2>
    <p>Carat is weight, and weight rises with the cube of length — so a stone that is 26% heavier is only about 8% longer. Face-up area is what a finger shows. Price per carat is the number the trade uses; it jumps at 0.50, 1.00, 1.50 and 2.00 carats because those are the weights people ask for, which is why a stone just under a round number is the classic value buy.</p>
    <p>Resale uses our standard bands: 25–40% of retail for natural stones, 5–12% for lab-grown. Every figure is from our own model — see the <a href="methodology.html">methodology</a>.</p>
  </section>''',
  script=r'''
(function(){
  const $=id=>document.getElementById(id);
  const money=n=>'$'+Math.round(n).toLocaleString('en-US');
  const SH=['Round','Oval','Princess','Cushion','Emerald','Pear','Marquise','Radiant','Asscher','Heart'];
  function form(id, d){
    return `<div class="grid g3" style="gap:10px">
      <div class="field"><label>Carat</label><input type="number" id="${id}ct" value="${d.ct}" step="0.05" min="0.1" max="10"></div>
      <div class="field"><label>Shape</label><select id="${id}sh">${SH.map(s=>`<option${s===d.sh?' selected':''}>${s}</option>`).join('')}</select></div>
      <div class="field"><label>Color</label><select id="${id}co">${Object.keys(COLOR_MULT).map(c=>`<option${c===d.co?' selected':''}>${c}</option>`).join('')}</select></div>
      <div class="field"><label>Clarity</label><select id="${id}cl">${Object.keys(CLARITY_MULT).map(c=>`<option${c===d.cl?' selected':''}>${c}</option>`).join('')}</select></div>
      <div class="field"><label>Cut</label><select id="${id}cu">${Object.keys(CUT_MULT).map(c=>`<option${c==='Very Good'?' selected':''}>${c}</option>`).join('')}</select></div>
      <div class="field"><label>Origin</label><select id="${id}or"><option${d.or==='Natural'?' selected':''}>Natural</option><option${d.or==='Lab-grown'?' selected':''}>Lab-grown</option></select></div>
    </div>`;
  }
  $('fA').innerHTML=form('a',{ct:1,sh:'Round',co:'G',cl:'VS2',or:'Natural'});
  $('fB').innerHTML=form('b',{ct:0.9,sh:'Round',co:'G',cl:'VS2',or:'Natural'});
  function read(id){ return {carat:parseFloat($(id+'ct').value)||1, shape:$(id+'sh').value, color:$(id+'co').value, clarity:$(id+'cl').value, cut:$(id+'cu').value, origin:$(id+'or').value, cert:$(id+'or').value==='Lab-grown'?'IGI':'GIA'}; }
  function calc(){
    const A=read('a'), B=read('b'); const va=valueDiamond(A), vb=valueDiamond(B); const da=shapeDims(A.shape,A.carat), db=shapeDims(B.shape,B.carat);
    const mid=v=>(v.retailLow+v.retailHigh)/2, rmid=v=>(v.resaleLow+v.resaleHigh)/2;
    const rows=[['Face-up size',`${da.l} × ${da.w} mm`,`${db.l} × ${db.w} mm`],['Face-up area',`${(da.l*da.w).toFixed(0)} mm²`,`${(db.l*db.w).toFixed(0)} mm²`],
      ['Retail',`${money(va.retailLow)}–${money(va.retailHigh)}`,`${money(vb.retailLow)}–${money(vb.retailHigh)}`],
      ['Price per carat',money(mid(va)/A.carat),money(mid(vb)/B.carat)],['Price per mm² of face-up',money(mid(va)/(da.l*da.w)),money(mid(vb)/(db.l*db.w))],
      ['Resells for',`${money(va.resaleLow)}–${money(va.resaleHigh)}`,`${money(vb.resaleLow)}–${money(vb.resaleHigh)}`],
      ['You keep',`${Math.round(rmid(va)/mid(va)*100)}%`,`${Math.round(rmid(vb)/mid(vb)*100)}%`]];
    const card=(o,v,d,lbl)=>`<div class="panel"><div class="stage" style="min-height:220px;padding:10px">${shapeOnFinger(o.shape,o.carat)}</div>
      <h3 style="margin-top:12px">${lbl}: ${o.carat.toFixed(2)} ct ${o.shape.toLowerCase()}${o.origin==='Lab-grown'?' <span class="pill pill-ice">lab-grown</span>':''}</h3>
      <div class="small">${o.color} · ${o.clarity} · ${o.cut} cut</div>
      <div style="font-family:var(--serif);font-size:30px;font-weight:700;color:var(--gold-2);margin-top:8px">${money(v.retailLow)}–${money(v.retailHigh)}</div>
      <div class="small" style="color:var(--bad);font-weight:600">Resells for ${money(v.resaleLow)}–${money(v.resaleHigh)}</div></div>`;
    $('out').innerHTML=card(A,va,da,'A')+card(B,vb,db,'B')+`<div class="panel" style="grid-column:1/-1"><div class="table-scroll"><table><thead><tr><th></th><th class="num">A</th><th class="num">B</th></tr></thead><tbody>${rows.map(r=>`<tr><td>${r[0]}</td><td class="num">${r[1]}</td><td class="num">${r[2]}</td></tr>`).join('')}</tbody></table></div></div>`;
    const dl=(da.l/db.l-1)*100, dp=(mid(va)/mid(vb)-1)*100, area=(da.l*da.w)/(db.l*db.w);
    let verdict=`<h3>Verdict</h3><p style="margin-top:8px">A is <strong>${Math.abs(dl).toFixed(1)}% ${dl>=0?'longer':'shorter'}</strong> across than B and costs <strong>${Math.abs(dp).toFixed(0)}% ${dp>=0?'more':'less'}</strong>. `;
    if(Math.abs(dl)<5 && Math.abs(dp)>12) verdict+=`On a finger these two are indistinguishable in size; the price difference is almost entirely the grade or the round-number premium. <strong>${dp>0?'B':'A'} is the better buy.</strong>`;
    else if(area>1.15 && dp<15) verdict+=`A shows ${((area-1)*100).toFixed(0)}% more face-up area for ${dp<0?'less':'little more'} money. <strong>A is the better buy for visible size.</strong>`;
    else if(area<0.87 && dp>-15) verdict+=`B shows ${((1/area-1)*100).toFixed(0)}% more face-up area for ${dp>0?'less':'little more'} money. <strong>B is the better buy for visible size.</strong>`;
    else verdict+=`The price tracks the visible size fairly closely here; choose on shape and cut quality rather than on the numbers.`;
    if(A.origin!==B.origin) verdict+=` Note the resale row: the lab-grown stone keeps ${Math.round(rmid(A.origin==='Lab-grown'?va:vb)/mid(A.origin==='Lab-grown'?va:vb)*100)}% against ${Math.round(rmid(A.origin==='Lab-grown'?vb:va)/mid(A.origin==='Lab-grown'?vb:va)*100)}% for natural. Buy lab-grown to wear, not to hold.`;
    $('cOut').innerHTML=`<div class="lab">Diamond A</div><div class="big" style="font-size:clamp(26px,4vw,36px)">${money(va.retailLow)}–${money(va.retailHigh)}</div><div class="sub">${A.carat.toFixed(2)} ct ${A.shape.toLowerCase()} · ${A.color}/${A.clarity} · resells ${money(va.resaleLow)}–${money(va.resaleHigh)}</div>
      <div class="lab" style="margin-top:18px">Diamond B</div><div class="big" style="font-size:clamp(26px,4vw,36px)">${money(vb.retailLow)}–${money(vb.retailHigh)}</div><div class="sub">${B.carat.toFixed(2)} ct ${B.shape.toLowerCase()} · ${B.color}/${B.clarity} · resells ${money(vb.resaleLow)}–${money(vb.resaleHigh)}</div>
      <div class="note" style="margin-top:18px;color:#F6F1E6;font-size:14px;line-height:1.55">${verdict.replace('<h3>Verdict</h3><p style="margin-top:8px">','')}</div>`;
    $('shop').innerHTML=(typeof BLUE_NILE!=='undefined')?BLUE_NILE.card({shape:A.shape,carat:A.carat,color:A.color,clarity:A.clarity,lab:A.origin==='Lab-grown'},{title:'Real stones matching A and B',
      sub:`A: ${A.carat.toFixed(2)} ct ${A.shape.toLowerCase()}, ${A.color}/${A.clarity} and up · B: ${B.carat.toFixed(2)} ct ${B.shape.toLowerCase()}, ${B.color}/${B.clarity} and up. Filtered to each spec at Blue Nile.`,
      natLabel:`Like A — ${A.carat.toFixed(2)} ct ${A.shape.toLowerCase()}${A.origin==='Lab-grown'?' (lab)':''} →`, labLabel:`Like A — lab-grown →`,
      extra:[{label:`Like B — ${B.carat.toFixed(2)} ct ${B.shape.toLowerCase()}${B.origin==='Lab-grown'?' (lab)':''} →`, gold:true, spec:{shape:B.shape,carat:B.carat,color:B.color,clarity:B.clarity,lab:B.origin==='Lab-grown'}}]}):'';
    if(window.cbTrack) cbTrack('tool_use',{tool:'compare',a:`${A.carat}${A.shape}${A.color}${A.clarity}`,b:`${B.carat}${B.shape}${B.color}${B.clarity}`});
  }
  document.querySelectorAll('#fA input,#fA select,#fB input,#fB select').forEach(el=>el.addEventListener('input',calc));
  document.querySelectorAll('.chip[data-p]').forEach(b=>b.addEventListener('click',()=>{
    const [a,bb]=b.dataset.p.split(';'); [['a',a],['b',bb]].forEach(([id,str])=>{const [ct,sh,co,cl,or]=str.split('|'); $(id+'ct').value=ct; $(id+'sh').value=sh; $(id+'co').value=co; $(id+'cl').value=cl; $(id+'or').value=or;}); calc();
  }));
  calc();
})();''')

# ---------------------------------------------------------------- LAB VS NATURAL
PAGES['lab-vs-natural.html'] = dict(
  title='Lab-Grown vs Natural Diamond — Price Today and Value in Five Years | CaratBase',
  desc='The same diamond both ways: what a lab-grown and a natural stone of identical size and grade cost today, what each resells for, and how far the same money goes in each.',
  eyebrow='Lab-grown vs natural', h1='Lab-grown or natural? The same stone, both ways', lede='Identical shape, weight and grade. One is grown in a reactor in weeks, the other in the mantle over a billion years — and they are chemically the same. The difference is entirely in what they cost and what they are worth later.',
  scripts=('shapes.js',),
  schema=faq([('How much cheaper is a lab-grown diamond?','A lab-grown diamond of the same size and grade costs roughly 85% less than a natural one at retail. A 1 carat G VS2 round is about $5,250 natural and about $740 lab-grown.'),
              ('Do lab-grown diamonds hold their value?','No. Lab-grown resale is typically 5–12% of retail, against 25–40% for natural, and lab-grown prices have fallen every year since 2022 as production has scaled.'),
              ('Can anyone tell a lab-grown diamond from a natural one?','Not by eye or loupe. Laboratories use spectroscopy, and graded stones are laser-inscribed with their origin on the girdle.')]),
  body='''

  <section class="console">
    <div class="console-head"><span class="name"><span class="dot"></span> Lab-grown vs natural</span><span class="status">same stone, both ways</span></div>
    <div class="console-body">
      <div class="console-in"><h3>The stone</h3><div class="grid g2" style="gap:12px">
    <div class="field"><label>Carat</label><input type="number" id="ct" value="1" step="0.05" min="0.1" max="10"></div>
    <div class="field"><label>Shape</label><select id="sh"></select></div>
    <div class="field"><label>Color</label><select id="co"></select></div>
    <div class="field"><label>Clarity</label><select id="cl"></select></div>
  </div><p class="small" style="margin-top:8px">Very Good cut; natural graded GIA, lab-grown IGI.</p></div>
      <div class="console-out" id="cOut"><div class="lab">Waiting for input</div></div>
    </div>
  </section>
  <div class="grid g2" style="margin-top:22px" id="out"></div>
  <div class="panel" style="margin-top:18px" id="same"></div>
  <div id="shop"></div>
  <section class="narrow legal" style="margin-top:40px">
    <h2>What the numbers mean</h2>
    <p>Retail is what you would pay today. Resale is what a buyer would offer the day after — for lab-grown stones that is already close to nothing, because a stone that can be manufactured to order has no scarcity for a secondary market to price. Natural resale is weak too, but it is a market.</p>
    <p><strong>The honest way to decide:</strong> if you want the largest, cleanest stone you can wear for the money and do not care what it is worth later, lab-grown wins and it is not close. If the stone is also meant to be an heirloom, a store of value, or something you might one day need to sell, that is what the natural premium buys — nothing else.</p>
    <h2>Five years on</h2>
    <p>Lab-grown wholesale prices fell by roughly 85% between 2022 and 2025 and have not stopped falling. We model resale at 5–12% of today's retail, and expect today's retail itself to be lower in five years. A natural stone's resale band has been stable for decades. The chart above prices both today; the direction of travel is the part to weigh.</p>
  </section>''',
  script=r'''
(function(){
  const $=id=>document.getElementById(id); const money=n=>'$'+Math.round(n).toLocaleString('en-US');
  const SH=['Round','Oval','Princess','Cushion','Emerald','Pear','Marquise','Radiant','Asscher','Heart'];
  $('sh').innerHTML=SH.map(s=>`<option>${s}</option>`).join(''); $('co').innerHTML=Object.keys(COLOR_MULT).map(c=>`<option${c==='G'?' selected':''}>${c}</option>`).join(''); $('cl').innerHTML=Object.keys(CLARITY_MULT).map(c=>`<option${c==='VS2'?' selected':''}>${c}</option>`).join('');
  function calc(){
    const ct=parseFloat($('ct').value)||1, sh=$('sh').value, co=$('co').value, cl=$('cl').value;
    const N=valueDiamond({carat:ct,shape:sh,color:co,clarity:cl,cut:'Very Good',origin:'Natural',cert:'GIA'}), L=valueDiamond({carat:ct,shape:sh,color:co,clarity:cl,cut:'Very Good',origin:'Lab-grown',cert:'IGI'});
    const mid=v=>(v.retailLow+v.retailHigh)/2; const d=shapeDims(sh,ct);
    const card=(lbl,v,ice)=>`<div class="panel" style="${ice?'border-color:rgba(43,113,137,.35)':''}"><div class="stage" style="min-height:200px;padding:10px">${shapeOnFinger(sh,ct)}</div>
      <h3 style="margin-top:12px">${lbl} <span class="pill${ice?' pill-ice':''}">${ice?'lab-grown':'natural'}</span></h3>
      <div class="small">${ct.toFixed(2)} ct ${sh.toLowerCase()} · ${co} · ${cl} · ${d.l} × ${d.w} mm</div>
      <div style="font-family:var(--serif);font-size:32px;font-weight:700;color:var(--gold-2);margin-top:8px">${money(v.retailLow)}–${money(v.retailHigh)}</div>
      <div class="small" style="color:var(--bad);font-weight:600">Resells for ${money(v.resaleLow)}–${money(v.resaleHigh)} · you keep ${Math.round((v.resaleLow+v.resaleHigh)/2/mid(v)*100)}%</div></div>`;
    $('out').innerHTML=card('Natural',N,false)+card('Lab-grown',L,true);
    $('cOut').innerHTML=`<div class="lab">Natural — retail</div><div class="big">${money(N.retailLow)}–${money(N.retailHigh)}</div><div class="sub">resells for ${money(N.resaleLow)}–${money(N.resaleHigh)}</div>
      <div class="lab" style="margin-top:18px">Lab-grown — retail</div><div class="big" style="color:#9CCFE0">${money(L.retailLow)}–${money(L.retailHigh)}</div><div class="sub">resells for ${money(L.resaleLow)}–${money(L.resaleHigh)}</div>
      <div class="split"><div><div class="lab">The difference</div><div class="v">${money(mid(N)-mid(L))}</div></div><div><div class="lab">Lab-grown is</div><div class="v">${Math.round((1-mid(L)/mid(N))*100)}% cheaper</div></div></div>`;
    const big=caratForBudget(mid(N),{shape:sh,color:co,clarity:cl,cut:'Very Good',origin:'Lab-grown',cert:'IGI'});
    const saving=mid(N)-mid(L);
    $('same').innerHTML=`<h3>The same money, the other way</h3><p style="margin-top:8px">The natural stone costs about <strong>${money(saving)} more</strong> — ${Math.round(saving/mid(N)*100)}% of its price. Spent on lab-grown instead, ${money(mid(N))} buys roughly a <strong>${big?big.carat.toFixed(2):'—'} ct</strong> stone of the same grade, about ${big?shapeDims(sh,big.carat).l:'—'} mm across against ${d.l} mm. Five years on, the natural stone would typically fetch ${money(N.resaleLow)}–${money(N.resaleHigh)}; the lab-grown one ${money(L.resaleLow)}–${money(L.resaleHigh)}, and likely less.</p>`;
    $('shop').innerHTML=(typeof BLUE_NILE!=='undefined')?BLUE_NILE.card({shape:sh,carat:ct,color:co,clarity:cl},{title:`See both at Blue Nile — ${ct.toFixed(2)} ct ${sh.toLowerCase()}, ${co}/${cl} and up`}):'';
    if(window.cbTrack) cbTrack('tool_use',{tool:'lab_vs_natural',ct,sh,co,cl});
  }
  ['ct','sh','co','cl'].forEach(id=>$(id).addEventListener('input',calc)); calc();
})();''')

# ---------------------------------------------------------------- ENGAGEMENT RING BUDGET
PAGES['engagement-ring-budget.html'] = dict(
  title='How Much Should You Spend on an Engagement Ring? A Calculator With No Rule | CaratBase',
  desc='The "two months\' salary" rule was a 1930s advertisement. This calculator shows what your income and savings actually support, and exactly what each budget buys — natural or lab-grown.',
  eyebrow='Engagement ring budget', h1='How much should you spend on an engagement ring?', lede='There is no rule. "Two months\' salary" was written by an advertising agency for De Beers in the 1930s, and "three months" was the 1980s update. What follows is arithmetic instead: what your money can carry without debt, and what that buys.',
  scripts=('shapes.js',),
  schema=faq([('Is the two months salary rule real?','No. It was a De Beers advertising slogan from the 1930s (raised to three months in the 1980s). There is no financial basis for it. The median US engagement ring spend is around $5,000–6,000 and has been falling as lab-grown diamonds became mainstream.'),
              ('What is a reasonable amount to spend on an engagement ring?','A common-sense range is what you can pay in full from savings without touching an emergency fund — often between two and six weeks of take-home pay. Anything financed at interest costs more than the ring will ever be worth.')]),
  body='''

  <section class="console">
    <div class="console-head"><span class="name"><span class="dot"></span> Ring budget</span><span class="status">no rule · your numbers</span></div>
    <div class="console-body">
      <div class="console-in"><h3>Your numbers</h3>
    <div class="field"><label>Annual take-home pay (after tax)</label><input type="number" id="inc" value="60000" step="1000" min="0"></div>
    <div class="field"><label>Savings you could use without borrowing</label><input type="number" id="sav" value="6000" step="500" min="0"></div>
    <div class="field"><label>Currency</label><select id="cur"><option value="$">$ US dollar</option><option value="£">£ Pound</option><option value="€">€ Euro</option><option value="₹">₹ Rupee</option><option value="A$">A$</option><option value="C$">C$</option></select></div>
    <p class="small">Nothing is stored or sent anywhere. The arithmetic runs on your device.</p></div>
      <div class="console-out" id="cOut"><div class="lab">Waiting for input</div></div>
    </div>
  </section>
  <h2 style="margin-top:36px">What the sensible figure buys</h2>
  <p class="small" style="margin-bottom:12px">Priced with our model at today's rates. Natural stones resell for 25–40% of retail; lab-grown for 5–12%.</p>
  <div class="grid g3" id="buys"></div>
  <div id="shop"></div>
  <section class="narrow legal" style="margin-top:40px">
    <h2>The honest version</h2>
    <p>A ring is a purchase, not an investment: whatever you pay, a buyer will offer you a third of it back at best. That is the strongest argument for two things — never financing it at interest, and spending on what is visible (carat and cut) rather than on grades that need a loupe. It is also the argument for lab-grown if the stone is meant to be worn rather than kept: the same money buys a stone two to three times the weight.</p>
    <p>The figures above are general arithmetic, not advice about your finances. If the sensible band looks impossibly low, the answer is usually a smaller stone in a beautiful setting, not a loan.</p>
  </section>''',
  script=r'''
(function(){
  const $=id=>document.getElementById(id); let C='$';
  const money=n=>C+Math.round(n).toLocaleString('en-US');
  function calc(){
    C=$('cur').value; const inc=parseFloat($('inc').value)||0, sav=parseFloat($('sav').value)||0; const wk=inc/52;
    const modest=Math.max(300, Math.min(wk*2, sav)), sensible=Math.max(300, Math.min(wk*4, sav)), stretch=Math.max(300, Math.min(wk*6, sav)); const ad=inc/12*2;
    $('cOut').innerHTML=`<div class="lab">A sensible budget</div><div class="big">${money(sensible)}</div><div class="sub">about a month of take-home, paid in full from savings</div>
      <div class="split"><div><div class="lab">Modest</div><div class="v">${money(modest)}</div></div><div><div class="lab">Stretch</div><div class="v">${money(stretch)}</div></div></div>
      <div class="note">"Two months' salary" would be ${money(ad)} — an advertising slogan from the 1930s, ${(ad/sensible).toFixed(1)}× this figure.</div>`;
    const b=sensible; const spec=[['Biggest natural',{shape:'Round',color:'J',clarity:'SI1',cut:'Very Good',origin:'Natural',cert:'GIA'}],['Balanced natural',{shape:'Round',color:'G',clarity:'VS2',cut:'Very Good',origin:'Natural',cert:'GIA'}],['Lab-grown, top grade',{shape:'Round',color:'F',clarity:'VS1',cut:'Excellent',origin:'Lab-grown',cert:'IGI'}]];
    const usd=b*({'$':1,'£':1.27,'€':1.08,'₹':0.012,'A$':0.66,'C$':0.73}[C]||1);
    $('buys').innerHTML=spec.map(([t,s])=>{ const r=caratForBudget(usd,s); if(!r) return `<div class="panel"><h3>${t}</h3><p class="small">Below what the market offers at this grade.</p></div>`; const d=shapeDims(s.shape,r.carat);
      return `<div class="panel"><div class="stage" style="min-height:180px;padding:8px">${shapeOnFinger(s.shape,r.carat)}</div><h3 style="margin-top:10px">${t}</h3><div style="font-family:var(--serif);font-size:30px;font-weight:700;color:var(--gold-2)">${r.carat.toFixed(2)} ct</div><div class="small">${s.color} · ${s.clarity} · ${d.l} mm across · resells ${money(r.resaleLow/usd*b)}–${money(r.resaleHigh/usd*b)}</div></div>`; }).join('');
    const bal=caratForBudget(usd,spec[1][1]);
    $('shop').innerHTML=(bal&&typeof BLUE_NILE!=='undefined')?BLUE_NILE.card({shape:'Round',carat:bal.carat,color:'G',clarity:'VS2'},{title:`Stones at the sensible budget — about ${bal.carat.toFixed(2)} ct round, G/VS2 and up`}):'';
    if(window.cbTrack) cbTrack('tool_use',{tool:'ring_budget',inc,sav,cur:C});
  }
  ['inc','sav','cur'].forEach(id=>$(id).addEventListener('input',calc)); calc();
})();''')

# ---------------------------------------------------------------- PRICE PER CARAT
PAGES['diamond-price-per-carat.html'] = dict(
  title='Diamond Price Per Carat Chart 2026 — Why 1 Carat Costs More Than Two Halves | CaratBase',
  desc='Diamond price per carat from 0.25 to 5 carats, natural and lab-grown, with the price steps at 0.5, 1, 1.5 and 2 carats that make a stone just under a round number the classic value buy.',
  eyebrow='Price per carat', h1='Diamond price per carat', lede='Price per carat is not flat — it climbs with weight, in steps. A 1.00 carat stone costs about 30% more per carat than a 0.95 carat one, and a 2 carat stone costs far more than two 1 carat stones. The chart is the whole argument.',
  schema=faq([('How much is a diamond per carat?','For a G color, VS2 clarity, well-cut natural round: about $1,900 per carat at 0.3 ct, $5,200 at 1 ct, $8,500 at 2 ct and $14,000 at 4 ct and above. Lab-grown is about 15% of these figures.'),
              ('Why does a 1 carat diamond cost more than two half-carat diamonds?','Large clean rough is much rarer than small, and 1.00 carat is a weight buyers ask for by name, so it sits in a higher per-carat bracket. Two 0.5 ct stones cost roughly half of one 1 ct stone.')]),
  body='''
  <div class="panel" style="margin-top:8px">
    <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:8px">
      <h2 style="font-size:22px">Price per carat by weight — G color, VS2, Very Good cut, round</h2>
      <label class="small" style="display:flex;gap:8px;align-items:center"><input type="checkbox" id="lab"> Show lab-grown</label>
    </div>
    <div id="chart"></div>
    <p class="small" style="margin-top:8px">Vertical steps are the price brackets. Each begins at a weight buyers ask for — 0.50, 0.70, 0.90, 1.00, 1.50, 2.00, 3.00, 4.00 ct. The stone just below each step is the value buy.</p>
  </div>
  <h2 style="margin-top:36px">The table</h2>
  <div class="table-scroll" style="margin-top:10px"><table id="tbl"><thead><tr><th>Weight</th><th class="num">Per carat</th><th class="num">Natural retail</th><th class="num">Lab-grown retail</th><th class="num">vs. two stones of half the weight</th></tr></thead><tbody></tbody></table></div>
  <div id="shop"></div>
  <section class="narrow legal" style="margin-top:40px">
    <h2>How to use this</h2>
    <p>Decide the visible size you want in millimeters — the <a href="size.html">size chart</a> shows every weight to scale — then buy the weight just under the nearest step. A 0.90 ct round is 6.27 mm across; a 1.00 ct is 6.50 mm. Nobody can see 0.23 mm on a hand, and the price difference is about a quarter of the stone.</p>
    <p>Per-carat figures move with color and clarity in the same proportions at every weight, so the shape of the curve is the same whatever grade you buy. See the <a href="diamond-color-chart.html">color chart</a> and <a href="diamond-clarity-chart.html">clarity chart</a> for those multipliers.</p>
  </section>''',
  script=r'''
(function(){
  const $=id=>document.getElementById(id); const money=n=>'$'+Math.round(n).toLocaleString('en-US');
  const spec={shape:'Round',color:'G',clarity:'VS2',cut:'Very Good',cert:'GIA'};
  const mid=v=>(v.retailLow+v.retailHigh)/2;
  const pts=[]; for(let c=0.2;c<=5.001;c+=0.01){ const v=valueDiamond({...spec,carat:+c.toFixed(2),origin:'Natural'}); pts.push([+c.toFixed(2), mid(v)/c, mid(v)]); }
  function chart(showLab){
    const W=860,H=340,L=64,R=16,T=16,B=40; const maxY=Math.max(...pts.map(p=>p[1]))*1.05, maxX=5;
    const x=c=>L+(c/maxX)*(W-L-R), y=v=>T+(1-v/maxY)*(H-T-B);
    const path=pts.map((p,i)=>(i?'L':'M')+x(p[0]).toFixed(1)+' '+y(p[1]).toFixed(1)).join(' ');
    const lab=showLab?'<path d="'+pts.map((p,i)=>(i?'L':'M')+x(p[0]).toFixed(1)+' '+y(p[1]*LAB_FACTOR).toFixed(1)).join(' ')+'" fill="none" stroke="#2B7189" stroke-width="2.2"/>':'';
    const steps=[0.5,0.7,0.9,1,1.5,2,3,4].map(c=>`<line x1="${x(c)}" x2="${x(c)}" y1="${T}" y2="${H-B}" stroke="#E7E2D8" stroke-dasharray="3 4"/><text x="${x(c)}" y="${H-B+16}" font-size="11" text-anchor="middle" fill="#8C857A">${c}</text>`).join('');
    const ys=[0,4000,8000,12000,16000].filter(v=>v<maxY).map(v=>`<line x1="${L}" x2="${W-R}" y1="${y(v)}" y2="${y(v)}" stroke="#F0ECE3"/><text x="${L-8}" y="${y(v)+4}" font-size="11" text-anchor="end" fill="#8C857A">$${v/1000}k</text>`).join('');
    $('chart').innerHTML=`<svg viewBox="0 0 ${W} ${H}" style="width:100%;height:auto" role="img" aria-label="Diamond price per carat by weight">${ys}${steps}
      <path d="${path}" fill="none" stroke="#A97C2C" stroke-width="2.6"/>${lab}
      <text x="${W-R}" y="${H-4}" font-size="11" text-anchor="end" fill="#8C857A">carat</text>
      <text x="${L+10}" y="${T+14}" font-size="12" fill="#A97C2C" font-weight="600">Natural</text>${showLab?`<text x="${L+10}" y="${T+32}" font-size="12" fill="#2B7189" font-weight="600">Lab-grown</text>`:''}</svg>`;
  }
  chart(false); $('lab').addEventListener('change',e=>chart(e.target.checked));
  const cts=[0.25,0.3,0.4,0.5,0.7,0.75,0.9,1,1.25,1.5,2,2.5,3,4,5];
  $('tbl').querySelector('tbody').innerHTML=cts.map(c=>{ const v=valueDiamond({...spec,carat:c,origin:'Natural'}), l=valueDiamond({...spec,carat:c,origin:'Lab-grown',cert:'IGI'}); const half=valueDiamond({...spec,carat:c/2,origin:'Natural'}); const ratio=mid(v)/(2*mid(half));
    return `<tr${[0.5,1,1.5,2].includes(c)?' style="background:var(--gold-dim)"':''}><td><a href="diamond/${String(c).replace('.','-')}-carat-round/">${c} ct</a></td><td class="num">${money(mid(v)/c)}</td><td class="num">${money(v.retailLow)}–${money(v.retailHigh)}</td><td class="num">${l.retailLow===l.retailHigh?money(l.retailLow):money(l.retailLow)+'–'+money(l.retailHigh)}</td><td class="num">${ratio.toFixed(2)}× the price of two ${(c/2).toFixed(2)} ct</td></tr>`; }).join('');
  $('shop').innerHTML=(typeof BLUE_NILE!=='undefined')?BLUE_NILE.card({shape:'Round',carat:0.9,color:'G',clarity:'VS2'},{title:'The value buy — 0.90 ct rounds, G/VS2 and up',sub:'Just under the 1 carat step: 6.27 mm across against 6.50 mm, at about three quarters of the price.'}):'';
})();''')

# ---------------------------------------------------------------- COLOR CHART
PAGES['diamond-color-chart.html'] = dict(
  title='Diamond Color Chart — D to K Explained With Prices | CaratBase',
  desc='Every diamond color grade from D to K on the same 1 carat stone: what the tint looks like, when it is visible, which metal hides it, and what each step up costs in dollars.',
  eyebrow='Color', h1='Diamond color chart, with prices', lede='Color grades run from D (no tint) to Z (obviously yellow). The scale below shows the grades people actually buy, D to K, priced on the same 1 carat round VS2 stone — so the cost of each letter is visible next to the letter itself.',
  schema=faq([('What is the best diamond color to buy?','G or H. Both look white to the eye in any setting, and the price difference from D is 25–35%. In yellow or rose gold, I or J also read white because the metal warms every stone.'),
              ('Can you see the difference between D and G color?','Not face-up in a setting. D, E and F are graded colorless and G to J near-colorless; a G stone next to a D looks identical unless both are loose, upside down, on white paper under a lamp.')]),
  body='''
  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:10px;margin-top:8px" id="sw"></div>
  <p class="small" style="margin-top:10px">Tints exaggerated so the progression is visible on a screen; in a ring, D to H look the same color.</p>
  <h2 style="margin-top:36px">What each grade costs — 1 carat round, VS2, Very Good cut</h2>
  <div class="table-scroll" style="margin-top:10px"><table id="tbl"><thead><tr><th>Grade</th><th>Group</th><th>What you see</th><th class="num">Retail</th><th class="num">vs. G</th></tr></thead><tbody></tbody></table></div>
  <div id="shop"></div>
  <section class="narrow legal" style="margin-top:40px">
    <h2>Which color to buy</h2>
    <p><strong>White gold or platinum:</strong> G or H. The metal is cold and white, so a warmer stone shows against it — but G and H do not. <strong>Yellow or rose gold:</strong> I or J. The metal warms every stone, so a colorless one gains nothing and a near-colorless one loses nothing. Spending on D–F in yellow gold is paying for a difference the setting erases.</p>
    <p><strong>Larger stones show more color</strong> because there is more material for light to travel through. Above 2 carats, go one grade higher than you would at 1 carat. <strong>Elongated shapes</strong> (oval, pear, marquise) concentrate color at the tips; step cuts (emerald, Asscher) hide less than brilliants. Fluorescence, listed on the certificate, can make an I–K stone look a grade whiter in daylight; it is a discount on the certificate and an upgrade on the hand.</p>
  </section>''',
  script=r'''
(function(){
  const $=id=>document.getElementById(id); const money=n=>'$'+Math.round(n).toLocaleString('en-US');
  const G=[['D','Colorless','Icy white. The top grade; a premium for rarity you cannot see.','#FFFFFF'],['E','Colorless','Identical to D face-up.','#FEFEFC'],['F','Colorless','The last colorless grade; still no visible tint.','#FDFCF8'],
    ['G','Near-colorless','The value grade. Looks white in any metal.','#FBF9F1'],['H','Near-colorless','White face-up; faint warmth only loose, on white.','#F9F5E9'],['I','Near-colorless','Slight warmth in white gold; white in yellow.','#F6F0DD'],
    ['J','Near-colorless','Warm in white metal; excellent in yellow or rose gold.','#F3EBD0'],['K','Faint','Visible warmth. Best in yellow gold, small sizes.','#EFE4BF']];
  const spec={shape:'Round',carat:1,clarity:'VS2',cut:'Very Good',origin:'Natural',cert:'GIA'}; const mid=v=>(v.retailLow+v.retailHigh)/2; const g=mid(valueDiamond({...spec,color:'G'}));
  $('sw').innerHTML=G.map(([l,grp,_,c])=>`<div class="panel" style="text-align:center;padding:14px 8px"><div style="width:64px;height:64px;margin:0 auto;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff 0%,${c} 55%,${c} 100%);border:1px solid var(--line-2);box-shadow:inset 0 -6px 12px rgba(0,0,0,.05)"></div><div style="font-family:var(--serif);font-size:28px;font-weight:700;margin-top:8px">${l}</div><div class="small">${grp}</div></div>`).join('');
  $('tbl').querySelector('tbody').innerHTML=G.map(([l,grp,txt])=>{ const v=valueDiamond({...spec,color:l}); const d=(mid(v)/g-1)*100;
    return `<tr${l==='G'?' style="background:var(--gold-dim)"':''}><td><strong>${l}</strong></td><td>${grp}</td><td>${txt}</td><td class="num">${money(v.retailLow)}–${money(v.retailHigh)}</td><td class="num" style="color:${d>0?'var(--bad)':d<0?'var(--good)':'inherit'}">${d>0?'+':''}${d.toFixed(0)}%</td></tr>`; }).join('');
  $('shop').innerHTML=(typeof BLUE_NILE!=='undefined')?BLUE_NILE.card({shape:'Round',carat:1,color:'H',clarity:'VS2'},{title:'The value grades — 1 ct rounds, H color and up, VS2 and up',sub:'G and H look white in any setting. This filter starts there.'}):'';
})();''')

# ---------------------------------------------------------------- CLARITY CHART
PAGES['diamond-clarity-chart.html'] = dict(
  title='Diamond Clarity Chart — FL to I1 Explained With Prices | CaratBase',
  desc='Every diamond clarity grade from Flawless to I1: what is visible to the naked eye, what needs a loupe, and what each grade costs on the same 1 carat stone.',
  eyebrow='Clarity', h1='Diamond clarity chart, with prices', lede='Clarity grades describe inclusions under 10× magnification. Most of the scale is invisible to a person looking at a ring — which is exactly why it is the grade where money is most often wasted. Priced below on the same 1 carat G color round.',
  schema=faq([('What clarity is eye-clean?','VS2 and above are eye-clean in virtually every stone; SI1 is usually eye-clean in rounds under 1.5 carats; SI2 sometimes. Below SI2, inclusions are generally visible without magnification.'),
              ('Is VVS clarity worth the money?','Not for appearance. VVS1 and VS2 look identical to the eye; the difference is only under a loupe. VVS commands a premium for rarity, which matters for resale of large stones but not for how the ring looks.')]),
  body='''
  <div class="table-scroll" style="margin-top:8px"><table id="tbl"><thead><tr><th>Grade</th><th>Means</th><th>To the eye</th><th class="num">Retail, 1 ct G</th><th class="num">vs. VS2</th></tr></thead><tbody></tbody></table></div>
  <div id="shop"></div>
  <section class="narrow legal" style="margin-top:40px">
    <h2>Which clarity to buy</h2>
    <p><strong>VS2 is the value grade</strong> — eye-clean in every shape and size, at a third less than VVS1. <strong>SI1 is the expert's grade:</strong> usually eye-clean, priced 14% under VS2, but it needs the stone itself to be checked (or a 360° photo), because SI1 covers everything from a tiny crystal at the edge to a cloud under the table.</p>
    <p><strong>Step cuts show more.</strong> Emerald and Asscher cuts have large open facets that act like windows, so buy one clarity grade higher than you would for a brilliant. <strong>Bigger stones show more too</strong> — an inclusion that hides at 0.5 ct can be found at 2 ct. Where an inclusion sits matters as much as its size: under the table is worst, near the girdle is hidden by prongs.</p>
  </section>''',
  script=r'''
(function(){
  const $=id=>document.getElementById(id); const money=n=>'$'+Math.round(n).toLocaleString('en-US');
  const C=[['FL','Flawless','Nothing inside or on the surface at 10×.','Identical to VS2. Rarity premium only.'],['IF','Internally flawless','Nothing inside; minor surface blemishes.','Identical to VS2.'],['VVS1','Very, very slightly included','Inclusions hard for a grader to find at 10×.','Identical to VS2.'],['VVS2','Very, very slightly included','Inclusions difficult to see at 10×.','Identical to VS2.'],
    ['VS1','Very slightly included','Minor inclusions, seen with effort at 10×.','Eye-clean.'],['VS2','Very slightly included','Minor inclusions, easier to find at 10×.','Eye-clean. The value grade.'],['SI1','Slightly included','Noticeable at 10×.','Usually eye-clean under 1.5 ct. Check the stone.'],['SI2','Slightly included','Easy to see at 10×.','Sometimes eye-clean, often not. Check the stone.'],['I1','Included','Obvious at 10×.','Visible to the eye. Affects brilliance.']];
  const spec={shape:'Round',carat:1,color:'G',cut:'Very Good',origin:'Natural',cert:'GIA'}; const mid=v=>(v.retailLow+v.retailHigh)/2; const base=mid(valueDiamond({...spec,clarity:'VS2'}));
  $('tbl').querySelector('tbody').innerHTML=C.map(([l,n,m,e])=>{ const v=valueDiamond({...spec,clarity:l}); const d=(mid(v)/base-1)*100;
    return `<tr${l==='VS2'?' style="background:var(--gold-dim)"':''}><td><strong>${l}</strong><div class="small">${n}</div></td><td>${m}</td><td>${e}</td><td class="num">${money(v.retailLow)}–${money(v.retailHigh)}</td><td class="num" style="color:${d>0?'var(--bad)':d<0?'var(--good)':'inherit'}">${d>0?'+':''}${d.toFixed(0)}%</td></tr>`; }).join('');
  $('shop').innerHTML=(typeof BLUE_NILE!=='undefined')?BLUE_NILE.card({shape:'Round',carat:1,color:'G',clarity:'VS2'},{title:'Eye-clean by definition — 1 ct rounds, VS2 and up, G and up'}):'';
})();''')

# ---------------------------------------------------------------- BIRTHSTONES + ANNIVERSARIES
PAGES['birthstones.html'] = dict(
  title='Birthstones by Month — Every Stone, What It Costs, and the Honest Alternative | CaratBase',
  desc='All twelve birthstones with color, hardness, what a fine 1 carat stone is worth today, and the affordable alternative when the classic is out of reach. Plus anniversary gemstones by year.',
  eyebrow='Reference', h1='Birthstones by month', lede='The modern list was fixed by the American jewelers\' association in 1912 and has gained a few alternates since. Each month below gives the traditional stone, how hard it wears, what a fine 1 carat example costs at today\'s rates, and the sensible substitute when the classic is priced out of reach.',
  schema=faq([('What are the birthstones for each month?','January garnet, February amethyst, March aquamarine, April diamond, May emerald, June pearl or alexandrite, July ruby, August peridot, September sapphire, October opal or tourmaline, November topaz or citrine, December tanzanite, turquoise or blue zircon.'),
              ('Which birthstone is the most expensive?','April (diamond), May (emerald), July (ruby) and September (sapphire) are the costly months; a fine 1 carat ruby or emerald runs into the thousands. Amethyst, citrine, peridot and garnet are the affordable months — fine stones for well under $100 a carat.')]),
  scripts=('gems.js','shapes.js'),
  body='''
  <div class="grid g3" style="margin-top:8px" id="months"></div>
  <h2 style="margin-top:44px">Anniversary gemstones by year</h2>
  <p class="small" style="margin:6px 0 12px">The traditional list, with the classic stone priced where we model it.</p>
  <div class="table-scroll"><table id="anni"><thead><tr><th>Year</th><th>Traditional</th><th class="num">A fine 1 ct today</th></tr></thead><tbody></tbody></table></div>
  <section class="narrow legal" style="margin-top:40px">
    <h2>On hardness</h2>
    <p>The Mohs number is how well a stone resists scratching, and it decides whether it survives a ring. Diamond (10), sapphire and ruby (9) and alexandrite (8.5) are everyday-ring stones. Emerald (7.5–8) is hard but brittle, and is usually oiled to hide fractures. Below 7 — opal, pearl, turquoise — the stone belongs in earrings or a pendant, not on a hand.</p>
  </section>''',
  script=r'''
(function(){
  const $=id=>document.getElementById(id); const money=n=>'$'+Math.round(n).toLocaleString('en-US');
  const price=(t)=>{ if(t==='Diamond'){ const v=valueDiamond({carat:1,shape:'Round',color:'G',clarity:'VS2',cut:'Very Good',origin:'Natural',cert:'GIA'}); return [v.retailLow,v.retailHigh]; }
    if(!GEMS[t]) return null; const o=Object.keys(GEMS[t].origins).slice(-1)[0]; const v=valueGem({type:t,carat:1,tier:'Fine',treatment:t==='Emerald'?'Oiled — minor (emerald)':'Heated (standard)',origin:o}); return [v.retailLow,v.retailHigh]; };
  const M=[['January','Garnet','#B22222',7,'Garnet','Deep red; the affordable classic.','—'],['February','Amethyst','#9966CC',7,'Amethyst','Purple quartz. Fine color is cheap because supply is huge.','—'],
    ['March','Aquamarine','#7FDBD4',7.5,'Aquamarine','Pale sea-blue beryl. Also bloodstone.','Blue topaz'],['April','Diamond','#F5F5F5',10,'Diamond','The priciest month by far.','White sapphire, or lab-grown diamond'],
    ['May','Emerald','#50C878',7.5,'Emerald','Nearly always oiled; treatment drives the price.','Tsavorite garnet, green tourmaline'],['June','Pearl · Alexandrite','#F0E4D0',8.5,'Alexandrite','Alexandrite (priced here) is rare and color-changing, hardness 8.5. Pearl is soft — 2.5 to 4.5 — and priced by size and lustre, not carat.','Moonstone; cultured pearl'],
    ['July','Ruby','#E0115F',9,'Ruby','Red corundum. Burmese unheated is the world\'s dearest stone per carat.','Red spinel, rhodolite garnet'],['August','Peridot','#9ACD32',6.5,'Peridot','Olive green; inexpensive and bright.','Spinel'],
    ['September','Sapphire','#0F52BA',9,'Blue sapphire','Blue corundum; Kashmir and Ceylon carry premiums.','Blue spinel, tanzanite'],['October','Opal · Tourmaline','#FF7F50',6,'Tourmaline','Opal is fragile; tourmaline comes in every color.','Pink tourmaline'],
    ['November','Topaz · Citrine','#FFC87C',8,'Citrine','Imperial topaz is the fine stone; citrine the everyday one.','Citrine'],['December','Tanzanite · Turquoise · Zircon','#40E0D0',6.5,'Tanzanite','Tanzanite from one hill in Tanzania; turquoise is soft.','Blue zircon, blue topaz']];
  $('months').innerHTML=M.map(([m,stone,c,h,pt,note,alt])=>{ const p=price(pt); return `<div class="panel"><div style="display:flex;justify-content:space-between;align-items:center"><div class="eyebrow">${m}</div><div style="width:26px;height:26px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,${c} 60%);border:1px solid var(--line-2)"></div></div>
    <h3 style="margin-top:6px">${stone}</h3><p class="small" style="margin-top:4px">${note}</p>
    <div class="grid g2" style="gap:8px;margin-top:10px"><div class="stat"><div class="k">Hardness</div><div class="v">${h} / 10</div></div><div class="stat"><div class="k">Fine 1 ct</div><div class="v" style="font-size:15px">${p?money(p[0])+'–'+money(p[1]):'—'}</div></div></div>
    <p class="small" style="margin-top:10px"><strong>Alternative:</strong> ${alt}</p>${GEMS[pt]?`<a class="small" href="gemstone/${pt.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'')}/" style="font-weight:600;color:var(--gold-2)">${pt} values in detail →</a>`:pt==='Diamond'?`<a class="small" href="diamond/1-carat-round/" style="font-weight:600;color:var(--gold-2)">1 carat diamond prices →</a>`:''}</div>`; }).join('');
  const A=[[1,'Gold'],[5,'Sapphire','Blue sapphire'],[10,'Diamond','Diamond'],[15,'Ruby','Ruby'],[20,'Emerald','Emerald'],[25,'Silver'],[30,'Pearl'],[35,'Emerald / jade','Emerald'],[40,'Ruby','Ruby'],[45,'Sapphire','Blue sapphire'],[50,'Gold'],[55,'Alexandrite','Alexandrite'],[60,'Diamond','Diamond']];
  $('anni').querySelector('tbody').innerHTML=A.map(([y,n,pt])=>{ const p=pt?price(pt):null; return `<tr><td>${y}${y===1?'st':y===2?'nd':y===3?'rd':'th'}</td><td>${n}</td><td class="num">${p?money(p[0])+'–'+money(p[1]):(n.includes('Gold')?'<a href="gold-price/24k/">see gold price</a>':'—')}</td></tr>`; }).join('');
})();''')

# ---------------------------------------------------------------- INSURANCE COST
PAGES['insurance-cost.html'] = dict(
  title='Jewelry Insurance Cost Calculator — What Cover Should Cost, and When to Skip It | CaratBase',
  desc='Estimate what insuring a ring or piece of jewelry should cost per year, compare a specialist policy with a homeowner\'s rider, and see when self-insuring is the better answer.',
  eyebrow='Insurance', h1='What should jewelry insurance cost?', lede='Specialist jewelry cover typically runs 1–2% of the insured value per year, with no deductible. A rider on a home policy is cheaper but narrower. Enter the value and see both — and the point below which insuring is not worth the paperwork.',
  schema=faq([('How much does it cost to insure an engagement ring?','Typically 1–2% of the ring\'s value per year with a specialist jewelry insurer — $50–100 a year for a $5,000 ring — usually with no deductible and cover for loss, theft and mysterious disappearance. A homeowner\'s rider is often 0.5–1.5% but with a deductible and narrower cover.'),
              ('Is it worth insuring jewelry worth less than $1,000?','Usually not. At 1.5% a year the premium over a decade approaches a fifth of the value, and most people would rather absorb a loss of that size than administer a policy. Photograph it, keep the receipt, and self-insure.')]),
  body='''

  <section class="console">
    <div class="console-head"><span class="name"><span class="dot"></span> Insurance cost</span><span class="status">specialist · rider · self-insure</span></div>
    <div class="console-body">
      <div class="console-in"><h3>The piece</h3>
    <div class="field"><label>Replacement value</label><input type="number" id="val" value="6000" step="100" min="0"></div>
    <div class="grid g2" style="gap:12px"><div class="field"><label>Where you live</label><select id="reg"><option value="1">United States</option><option value="1.1">United Kingdom</option><option value="1.05">Europe</option><option value="1.15">Australia / Canada</option></select></div>
    <div class="field"><label>Currency</label><select id="cur"><option>$</option><option>£</option><option>€</option><option>A$</option><option>C$</option></select></div></div>
    <p class="small">Not sure of the value? <a href="value.html">Value the piece first</a> — the replacement figure is the retail number.</p></div>
      <div class="console-out" id="cOut"><div class="lab">Waiting for input</div></div>
    </div>
  </section>
  <div class="grid g3" style="margin-top:22px" id="out"></div>
  <div class="panel" style="margin-top:18px" id="verdict"></div>
  <div id="partners" style="margin-top:22px"></div>
  <section class="narrow legal" style="margin-top:40px">
    <h2>What the policy has to say</h2>
    <p><strong>Agreed value, not actual cash value.</strong> Agreed value pays the figure on the schedule; actual cash value pays what the insurer thinks a used ring is worth, which — as this site keeps pointing out — is a third of what you paid. <strong>Mysterious disappearance</strong> covers "it was on my hand and now it isn't", the most common loss. <strong>Worldwide cover</strong> matters if you travel. <strong>Replacement with like kind</strong>, not a cheque for a lower amount.</p>
    <p>You will need an appraisal or a detailed receipt. Our <a href="value.html">valuation report</a> is a starting point for that conversation, not a substitute for an appraiser's document.</p>
  </section>''',
  script=r'''
(function(){
  const $=id=>document.getElementById(id); let C='$'; const money=n=>C+Math.round(n).toLocaleString('en-US');
  function calc(){
    C=$('cur').value; const v=parseFloat($('val').value)||0, r=parseFloat($('reg').value);
    const spec=[v*0.01*r, v*0.02*r], rider=[v*0.005*r, v*0.015*r];
    $('out').innerHTML=[['Specialist jewelry policy',spec,'No deductible. Loss, theft, damage, mysterious disappearance, worldwide. Agreed value.'],
      ['Homeowner\'s or renter\'s rider',rider,'Cheaper, but a deductible applies, cover is often narrower, and a claim can raise your home premium.'],
      ['Self-insure',[0,0],'Photograph it, keep the receipt and the certificate, put the premium aside instead.']].map(([t,p,s])=>
      `<div class="panel"><div class="eyebrow">${t}</div><div style="font-family:var(--serif);font-size:32px;font-weight:700;color:var(--gold-2);margin:8px 0 4px">${p[1]?money(p[0])+'–'+money(p[1]):'—'}<small style="font-size:14px;color:var(--ink-3);font-weight:500"> /year</small></div><p class="small">${s}</p></div>`).join('');
    let msg;
    if(v<1000) msg=`<h3>Probably not worth insuring</h3><p style="margin-top:8px">At ${money(spec[1])} a year the premiums over a decade come to ${Math.round(spec[1]*10/v*100)}% of the value. Keep the receipt and a photograph, and treat a loss as a bad week rather than a claim.</p>`;
    else if(v<3000) msg=`<h3>Borderline — a rider if you already have a home policy</h3><p style="margin-top:8px">A specialist policy costs ${money(spec[0])}–${money(spec[1])} a year against a replacement cost of ${money(v)}. Reasonable if losing it would hurt; a rider at ${money(rider[0])}–${money(rider[1])} is the cheaper route if your home insurer offers one.</p>`;
    else msg=`<h3>Worth insuring, and worth a specialist policy</h3><p style="margin-top:8px">${money(spec[0])}–${money(spec[1])} a year for a ${money(v)} piece is ${(spec[1]/v*100).toFixed(1)}% at most, with no deductible and agreed-value replacement. Above about ${money(3000)} the gap between a specialist policy and a home rider — deductible, mysterious disappearance, worldwide cover — is worth the difference in premium.</p>`;
    $('verdict').innerHTML=msg;
    $('cOut').innerHTML=`<div class="lab">Specialist policy, per year</div><div class="big">${money(spec[0])}–${money(spec[1])}</div><div class="sub">${(spec[0]/v*100).toFixed(1)}–${(spec[1]/v*100).toFixed(1)}% of ${money(v)} · no deductible · agreed value</div>
      <div class="split"><div><div class="lab">Home policy rider</div><div class="v">${money(rider[0])}–${money(rider[1])}</div></div><div><div class="lab">Over ten years</div><div class="v">${money(spec[1]*10)}</div></div></div>
      <div class="note">${v<1000?'At this value, self-insuring is usually the better answer.':v<3000?'Borderline — a rider is the cheaper route if your home insurer offers one.':'Worth a specialist policy: the extra cover is worth the premium at this value.'}</div>`;
    if(window.cbTrack) cbTrack('tool_use',{tool:'insurance_cost',v});
  }
  ['val','reg','cur'].forEach(id=>$(id).addEventListener('input',calc)); calc();
  if(window.Partners) Partners.mount('partners','insurance',{title:'Specialist jewelry insurers',intro:'Both quote online in minutes and cover the things a home policy usually excludes.'});
})();''')

# ---------------------------------------------------------------- TOOLS INDEX
PAGES['tools.html'] = dict(
  title='All Tools & Reference — CaratBase',
  desc='Every calculator and reference page on CaratBase in one place: value, buy, measure, and look up.',
  eyebrow='Everything', h1='All the tools, in one place', lede='Twenty-two calculators and reference tools, plus 240 pages of worked answers. Type to search, or browse by what you are trying to do.',
  body='''
  <label class="searchbar" for="homeSearch" style="margin:0 0 30px">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <input id="homeSearch" type="search" placeholder="Search — ring size 7, 925, 1.5 carat oval, 18k…" autocomplete="off"><span class="kbd">⌘K</span></label>
''' + icons.families_html(),
  script='')

PAGES['404.html'] = dict(
  title='Page not found — CaratBase', desc='That page is not here. Search the tools and reference pages instead.',
  eyebrow='404', h1='That page isn\'t here', lede='The address may have changed, or it never existed. Everything on the site is one search away.',
  body='''
  <label class="searchbar" for="homeSearch" style="margin:0 0 30px">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
    <input id="homeSearch" type="search" placeholder="Search — ring size 7, 925, 1.5 carat oval, 18k…" autocomplete="off"><span class="kbd">⌘K</span></label>
  <div class="grid g3">
    <a class="panel" href="value.html" style="text-decoration:none;color:inherit"><h3>Value my jewelry</h3><p class="small" style="margin-top:6px">Retail, and what it really resells for.</p></a>
    <a class="panel" href="ring-size.html" style="text-decoration:none;color:inherit"><h3>Find my ring size</h3><p class="small" style="margin-top:6px">Four ways, five systems.</p></a>
    <a class="panel" href="tools.html" style="text-decoration:none;color:inherit"><h3>All tools</h3><p class="small" style="margin-top:6px">Everything, in one place.</p></a>
  </div>''',
  script='', extra_head='<meta name="robots" content="noindex">')

PAGES['about.html'] = dict(
  title='About CaratBase — The Independent Jewelry Reference',
  desc='Who runs CaratBase, why it exists, how it is paid for, and what it will never do. Independent, private, and every number shown working.',
  eyebrow='About', h1='The independent jewelry reference', lede='CaratBase exists because the one number a jewelry owner most needs — what a piece actually fetches when sold — is the one number the trade does not publish. We publish it, with the working shown.',
  body='''
  <section class="narrow legal">
    <h2>What it is</h2>
    <p>A set of free calculators and around 250 reference pages covering diamonds, colored stones, gold and metals, ring sizes and hallmarks. Every figure comes from our own price model, which is <a href="methodology.html">published in full</a>, and metal prices come from the live market. Nothing here is copied from a retailer.</p>
    <h2>Who</h2>
    <p>CaratBase is built and run by Priyankar Chakraborty, trading as CaratBase, from Georgia in the United States. It is not owned by, funded by, or affiliated with any jeweler, retailer, laboratory or insurer.</p>
    <h2>How it is paid for</h2>
    <p>Some links to retailers and insurers earn a commission if you buy. Every such link says so beside it, and it never changes a figure on the page — the valuation model does not know the links exist. We do not run display advertising, sell your data, or take payment to recommend anyone. If a partner stopped being the honest answer, the link would come out regardless of what it paid.</p>
    <h2>What it will never do</h2>
    <p>Buy or sell jewelry. Issue an appraisal — a document for insurance or probate needs a qualified appraiser who has handled the piece. Track you: there is no account, no cookie banner because there are no tracking cookies, and your vault lives on your own device.</p>
    <h2>For jewelers and publishers</h2>
    <p>The ring sizer, diamond size chart and gold calculator are available as <a href="widgets.html">free widgets</a> for any website. Retailers and laboratories interested in a data partnership can write to us.</p>
    <h2>Contact</h2>
    <p><a href="mailto:hello@caratbase.com">hello@caratbase.com</a> for anything general; <a href="mailto:privacy@caratbase.com">privacy@caratbase.com</a> for anything about your data. We read everything and reply to most.</p>
  </section>''', script='')

def main():
    for name, cfg in PAGES.items():
        html = shell(name, cfg['title'], cfg['desc'], cfg['eyebrow'], cfg['h1'], cfg['lede'], cfg['body'],
                     script=cfg.get('script',''), scripts=cfg.get('scripts',()), schema=cfg.get('schema'), extra_head=cfg.get('extra_head',''))
        (ROOT / name).write_text(html)
        print('wrote', name)

if __name__ == '__main__':
    main()
