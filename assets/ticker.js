/* CaratBase — price ticker.
   Metals are quoted from a live market, so they get real prices and a daily change.
   Diamonds are NOT: there is no exchange, no public tape and no live quote — which is
   precisely why resale is so opaque. They are shown as modelled benchmarks and labelled
   as such, because presenting a modelled figure as a market quote would be a lie. */
(function(){
  const host=document.querySelector('.site-head');
  if(!host || typeof METAL_SPOT==='undefined') return;
  const hasStones = typeof valueDiamond==='function';
  if(document.querySelector('.ticker')) return;

  const bar=document.createElement('div');
  bar.className='ticker';
  bar.innerHTML='<div class="ticker-track"></div>';
  host.insertAdjacentElement('afterend', bar);
  const track=bar.querySelector('.ticker-track');

  const money=n=>'$'+Math.round(n).toLocaleString('en-US');

  function items(spot){
    const g=(spot&&spot.perGram)||METAL_SPOT_FALLBACK();
    const prev=(spot&&spot.prevPerGram)||null;
    const out=[];

    [['Gold','gold','/g'],['Silver','silver','/g'],
     ['Platinum','platinum','/g'],['Palladium','palladium','/g']].forEach(([label,key,unit])=>{
      const v=g[key]; if(!v) return;
      const was=prev&&prev[key];
      const dp=was?((v-was)/was*100):null;
      out.push(`<span class="tick"><span class="sym">${label}</span>
        <span class="px">$${v.toFixed(2)}</span><span>${unit}</span>
        ${dp===null?'<span class="tag">live</span>'
          :`<span class="dl ${dp>=0?'up':'dn'}">${dp>=0?'▲':'▼'}${Math.abs(dp).toFixed(2)}%</span>`}</span>`);
    });

    /* Diamond benchmarks — modelled, clearly badged, never dressed up as a quote. */
    if(!hasStones) return out;
    const bench=[
      ['1ct natural', {carat:1,   origin:'Natural'}],
      ['2ct natural', {carat:2,   origin:'Natural'}],
      ['1ct lab',     {carat:1,   origin:'Lab-grown'}],
      ['0.5ct natural',{carat:0.5,origin:'Natural'}]
    ];
    bench.forEach(([label,o])=>{
      const v=valueDiamond({color:'G',clarity:'VS2',cut:'Very Good',shape:'Round',
        cert:o.origin==='Lab-grown'?'IGI':'GIA', ...o});
      if(!v) return;
      out.push(`<span class="tick"><span class="sym">${label}</span>
        <span class="px">${money(v.retailLow)}–${money(v.retailHigh)}</span>
        <span class="tag">benchmark</span></span>`);
    });

    /* The number that is the whole point of the site. */
    const nat=valueDiamond({carat:1,color:'G',clarity:'VS2',cut:'Very Good',shape:'Round',
      origin:'Natural',cert:'GIA'});
    out.push(`<span class="tick"><span class="sym">1ct resale</span>
      <span class="px">${money(nat.resaleLow)}–${money(nat.resaleHigh)}</span>
      <span class="tag">what you'd be offered</span></span>`);
    return out;
  }

  function METAL_SPOT_FALLBACK(){
    return {gold:METAL_SPOT.gold, silver:METAL_SPOT.silver, platinum:METAL_SPOT.platinum};
  }

  function render(spot){
    const row=items(spot).join('');
    track.innerHTML=row+row;          // duplicated so the loop has no visible seam
  }

  render(null);
  document.addEventListener('cb:spot', e=>render(e.detail));
})();
