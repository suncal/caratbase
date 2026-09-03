/* CaratBase — brand mark.
   A round brilliant seen from above: girdle, table, and the eight bezel and star facets.
   It is the same geometry the size tools draw at true scale, so the mark is literally a
   picture of what the site does. Kept to two rings and eight lines so it stays legible
   at favicon size. */
function caratMark(size, gold, ink){
  const S=size||28, g=gold||'#C9A961', k=ink||'#8A6420';
  const c=S/2, R=S*0.44, T=S*0.20;
  const pts=(n,r,off)=>Array.from({length:n},(_,i)=>{
    const a=off+i*2*Math.PI/n; return [c+r*Math.cos(a), c+r*Math.sin(a)];});
  const P=p=>p.map(([x,y])=>x.toFixed(2)+','+y.toFixed(2)).join(' ');
  const girdle=pts(8,R,Math.PI/8), table=pts(8,T,Math.PI/8);
  const spokes=table.map((t,i)=>{const q=girdle[i];
    return `<line x1="${t[0].toFixed(2)}" y1="${t[1].toFixed(2)}" x2="${q[0].toFixed(2)}" y2="${q[1].toFixed(2)}"/>`;}).join('');
  return `<svg width="${S}" height="${S}" viewBox="0 0 ${S} ${S}" fill="none"
    xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">
    <polygon points="${P(girdle)}" fill="${g}" fill-opacity=".13" stroke="${g}" stroke-width="1.35"
      stroke-linejoin="round"/>
    <polygon points="${P(table)}" fill="${g}" fill-opacity=".55" stroke="${k}" stroke-width="1"
      stroke-linejoin="round"/>
    <g stroke="${k}" stroke-width=".85" stroke-opacity=".75">${spokes}</g>
  </svg>`;
}

/* Paint the mark into every .logo on the page. */
(function(){
  document.querySelectorAll('.logo').forEach(a=>{
    if(a.querySelector('svg')) return;
    a.innerHTML = `<span class="mark">${caratMark(26)}</span><span class="word">CaratBase</span>`;
  });
})();
