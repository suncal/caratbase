/* CaratBase — diamond shapes at true scale.
   Carat is WEIGHT, not size. Because weight scales with the cube of the linear
   dimensions, a stone's face-up size grows only with the cube root of its carat —
   and shapes with the same weight spread very differently. An elongated cut carries
   less of its weight in the pavilion, so it looks bigger for the same money. */

/* Face-up length x width in mm for a well-cut 1.00 ct stone. */
const SHAPE_MM = {
  Round:    {l:6.5,  w:6.5,  note:'The benchmark. Most weight sits in the pavilion, so it looks smaller than its carat suggests.'},
  Oval:     {l:7.7,  w:5.7,  note:'Reads noticeably larger than a round of the same weight and elongates the finger.'},
  Pear:     {l:8.0,  w:5.5,  note:'The longest spread of the common shapes after the marquise.'},
  Marquise: {l:10.5, w:5.0,  note:'The biggest apparent size per carat of any shape — over 10 mm long at 1 ct.'},
  Emerald:  {l:7.0,  w:5.0,  note:'Step cut, so it flashes rather than sparkles. Inclusions show more readily.'},
  Asscher:  {l:5.6,  w:5.6,  note:'A square emerald cut. Compact face-up for its weight.'},
  Princess: {l:5.5,  w:5.5,  note:'Deep, so a lot of the weight is hidden below. Small face-up for its carat.'},
  Cushion:  {l:5.6,  w:5.6,  note:'Also deep. Soft corners and a warmer, chunkier sparkle.'},
  Radiant:  {l:6.2,  w:5.4,  note:'Brilliant faceting in a rectangular outline.'},
  Heart:    {l:6.4,  w:6.4,  note:'Essentially a pear with a cleft. Needs size to read clearly — rare under 0.75 ct.'}
};

/* Linear dimensions scale with the cube root of weight. */
function shapeDims(shape, ct){
  const base = SHAPE_MM[shape] || SHAPE_MM.Round;
  const k = Math.cbrt(Math.max(0.01, parseFloat(ct) || 1));
  return { l:+(base.l*k).toFixed(2), w:+(base.w*k).toFixed(2), note:base.note };
}

/* Outline for one shape, centred on (cx,cy), in mm units. */
function shapeOutline(shape, cx, cy, L, W){
  const hl=L/2, hw=W/2, n=(x)=>x.toFixed(2);
  switch(shape){
    case 'Round': case 'Oval':
      return `<ellipse cx="${n(cx)}" cy="${n(cy)}" rx="${n(hw)}" ry="${n(hl)}"/>`;
    case 'Princess':
      return `<rect x="${n(cx-hw)}" y="${n(cy-hl)}" width="${n(W)}" height="${n(L)}" rx="${n(W*0.04)}"/>`;
    case 'Cushion':
      return `<rect x="${n(cx-hw)}" y="${n(cy-hl)}" width="${n(W)}" height="${n(L)}" rx="${n(W*0.26)}"/>`;
    case 'Emerald': case 'Asscher': case 'Radiant': {
      const c=Math.min(W,L)*0.19;   // cut corners
      return `<polygon points="${[
        [cx-hw+c,cy-hl],[cx+hw-c,cy-hl],[cx+hw,cy-hl+c],[cx+hw,cy+hl-c],
        [cx+hw-c,cy+hl],[cx-hw+c,cy+hl],[cx-hw,cy+hl-c],[cx-hw,cy-hl+c]
      ].map(p=>n(p[0])+','+n(p[1])).join(' ')}"/>`;
    }
    case 'Marquise':
      return `<path d="M ${n(cx)} ${n(cy-hl)} Q ${n(cx+hw)} ${n(cy)} ${n(cx)} ${n(cy+hl)}
                       Q ${n(cx-hw)} ${n(cy)} ${n(cx)} ${n(cy-hl)} Z"/>`;
    case 'Pear':
      return `<path d="M ${n(cx)} ${n(cy-hl)}
                       C ${n(cx+hw*0.55)} ${n(cy-hl*0.45)} ${n(cx+hw)} ${n(cy+hl*0.12)} ${n(cx+hw)} ${n(cy+hl*0.42)}
                       A ${n(hw)} ${n(hw)} 0 0 1 ${n(cx-hw)} ${n(cy+hl*0.42)}
                       C ${n(cx-hw)} ${n(cy+hl*0.12)} ${n(cx-hw*0.55)} ${n(cy-hl*0.45)} ${n(cx)} ${n(cy-hl)} Z"/>`;
    case 'Heart':
      return `<path d="M ${n(cx)} ${n(cy+hl)}
                       C ${n(cx-hw*1.05)} ${n(cy+hl*0.15)} ${n(cx-hw)} ${n(cy-hl*0.85)} ${n(cx-hw*0.42)} ${n(cy-hl*0.85)}
                       C ${n(cx-hw*0.14)} ${n(cy-hl*0.85)} ${n(cx)} ${n(cy-hl*0.5)} ${n(cx)} ${n(cy-hl*0.32)}
                       C ${n(cx)} ${n(cy-hl*0.5)} ${n(cx+hw*0.14)} ${n(cy-hl*0.85)} ${n(cx+hw*0.42)} ${n(cy-hl*0.85)}
                       C ${n(cx+hw)} ${n(cy-hl*0.85)} ${n(cx+hw*1.05)} ${n(cy+hl*0.15)} ${n(cx)} ${n(cy+hl)} Z"/>`;
    default:
      return `<ellipse cx="${n(cx)}" cy="${n(cy)}" rx="${n(hw)}" ry="${n(hl)}"/>`;
  }
}

/* A stone of any shape drawn to true scale on a 17 mm finger. */
function shapeOnFinger(shape, ct){
  const d=shapeDims(shape,ct);
  const VB=60, cx=30, bandTop=31, cy=bandTop-d.l/2-0.4;
  const uid=(shape+String(ct)).replace(/[^A-Za-z0-9]/g,'');
  const body=shapeOutline(shape,cx,cy,d.l,d.w);
  const fill=body.replace('<','<').replace('/>',` fill="url(#st${uid})" stroke="#3E7C95" stroke-width=".2"/>`);
  return `<svg viewBox="0 0 ${VB} ${VB}" xmlns="http://www.w3.org/2000/svg" role="img"
    aria-label="A ${ct} carat ${shape.toLowerCase()} diamond at true scale, ${d.l} by ${d.w} millimetres">
    <defs>
      <linearGradient id="fg${uid}" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#E7DBCF"/><stop offset=".42" stop-color="#F6EDE4"/>
        <stop offset="1" stop-color="#E0D2C4"/></linearGradient>
      <linearGradient id="bd${uid}" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#8A7238"/><stop offset=".38" stop-color="#E3C88A"/>
        <stop offset=".62" stop-color="#C9A961"/><stop offset="1" stop-color="#7E6730"/></linearGradient>
      <radialGradient id="st${uid}" cx=".38" cy=".30" r=".85">
        <stop offset="0" stop-color="#FFFFFF"/><stop offset=".36" stop-color="#D3EEF9"/>
        <stop offset=".76" stop-color="#8CC6DD"/><stop offset="1" stop-color="#4E8FA8"/></radialGradient>
    </defs>
    <rect x="21.5" y="11" width="17" height="49" rx="8.5" fill="url(#fg${uid})"/>
    <rect x="21.5" y="11" width="17" height="49" rx="8.5" fill="none" stroke="#D5C6B7" stroke-width=".3"/>
    <rect x="20.6" y="${bandTop}" width="18.8" height="5.4" rx="1.1" fill="url(#bd${uid})"/>
    <g>${fill}</g>
    <g fill="#8C857A" font-family="Inter,sans-serif" font-size="2.4" text-anchor="middle">
      <text x="30" y="8">${d.l} × ${d.w} mm</text></g>
  </svg>`;
}
