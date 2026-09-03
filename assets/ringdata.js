/* CaratBase — ring size reference
   Source of truth is the inside DIAMETER in mm. Circumference is computed (π·d) so the
   table can never drift out of internal agreement, and EU/ISO size IS the circumference
   in mm by definition. UK/AU letters and Japan/India numbers are the published mappings. */

const RING_SIZES = [
  {us:3,    dia:14.05, uk:'F',    jp:4},
  {us:3.25, dia:14.25, uk:'F½',   jp:null},
  {us:3.5,  dia:14.45, uk:'G',    jp:5},
  {us:3.75, dia:14.65, uk:'G½',   jp:null},
  {us:4,    dia:14.86, uk:'H',    jp:6},
  {us:4.25, dia:15.06, uk:'H½',   jp:null},
  {us:4.5,  dia:15.27, uk:'I',    jp:7},
  {us:4.75, dia:15.47, uk:'J',    jp:8},
  {us:5,    dia:15.70, uk:'J½',   jp:9},
  {us:5.25, dia:15.90, uk:'K',    jp:null},
  {us:5.5,  dia:16.10, uk:'K½',   jp:10},
  {us:5.75, dia:16.30, uk:'L',    jp:null},
  {us:6,    dia:16.51, uk:'L½',   jp:11},
  {us:6.25, dia:16.71, uk:'M',    jp:null},
  {us:6.5,  dia:16.92, uk:'M½',   jp:12},
  {us:6.75, dia:17.13, uk:'N',    jp:13},
  {us:7,    dia:17.35, uk:'N½',   jp:14},
  {us:7.25, dia:17.55, uk:'O',    jp:null},
  {us:7.5,  dia:17.75, uk:'O½',   jp:15},
  {us:7.75, dia:17.97, uk:'P',    jp:null},
  {us:8,    dia:18.19, uk:'P½',   jp:16},
  {us:8.25, dia:18.39, uk:'Q',    jp:null},
  {us:8.5,  dia:18.53, uk:'Q½',   jp:17},
  {us:8.75, dia:18.80, uk:'R',    jp:null},
  {us:9,    dia:18.95, uk:'R½',   jp:18},
  {us:9.25, dia:19.22, uk:'S',    jp:null},
  {us:9.5,  dia:19.41, uk:'S½',   jp:19},
  {us:9.75, dia:19.62, uk:'T',    jp:null},
  {us:10,   dia:19.84, uk:'T½',   jp:20},
  {us:10.25,dia:20.02, uk:'U',    jp:null},
  {us:10.5, dia:20.20, uk:'U½',   jp:22},
  {us:10.75,dia:20.44, uk:'V',    jp:null},
  {us:11,   dia:20.68, uk:'V½',   jp:23},
  {us:11.5, dia:21.08, uk:'W½',   jp:24},
  {us:12,   dia:21.49, uk:'X½',   jp:25},
  {us:12.5, dia:21.89, uk:'Y½',   jp:26},
  {us:13,   dia:22.33, uk:'Z½',   jp:27}
];

RING_SIZES.forEach(r => {
  r.circ = +(r.dia * Math.PI).toFixed(2);   // inside circumference, mm
  r.eu   = +(r.dia * Math.PI).toFixed(1);   // EU / ISO 8653 size IS the circumference
});

/* Nearest row to a measurement. `field` is 'dia' | 'circ' | 'us'. */
function nearestRing(value, field){
  const v = parseFloat(value);
  if(!isFinite(v)) return null;
  let best = RING_SIZES[0];
  for(const r of RING_SIZES) if(Math.abs(r[field]-v) < Math.abs(best[field]-v)) best = r;
  return best;
}

/* How far off the exact match is, so we can be honest about between-sizes. */
function ringFit(value, field, row){
  const d = parseFloat(value) - row[field];
  return { delta:d, exact: Math.abs(d) < (field==='dia' ? 0.06 : 0.2) };
}

/* An ISO/IEC 7810 ID-1 card — every credit and debit card on earth — is exactly
   85.60 x 53.98 mm. That makes it a free, universal ruler for screen calibration. */
const CARD_MM = { w: 85.60, h: 53.98 };
