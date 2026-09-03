/* CaratBase — coloured stones and pearls.
 *
 * Coloured stones do not price like diamonds and treating them the same would be badly
 * wrong. Four differences drive everything here:
 *
 *  1. There is no universal grading standard. No 4Cs, no single authority. Two labs can
 *     describe the same stone differently, so every range here is wider than a diamond's.
 *  2. TREATMENT is usually the largest single factor. An unheated Burmese ruby and a
 *     glass-filled one of identical appearance differ by a factor of hundreds.
 *  3. ORIGIN carries real money — Kashmir sapphire, Mogok ruby, Colombian emerald — but
 *     only when a recognised lab has certified it. Claimed origin is worth nothing.
 *  4. Price per carat climbs far more steeply with size than it does for diamonds,
 *     because large fine coloured stones are genuinely rare.
 */

/* Retail price per carat at 1 ct, by quality tier. */
const GEMS = {
  'Ruby':            {tiers:[400,2200,9000,60000],  origins:{'Myanmar (Mogok)':2.6,'Mozambique':1.0,'Thailand':0.85,'Unknown / not certified':0.75}},
  'Blue sapphire':   {tiers:[350,1400,5500,30000],  origins:{'Kashmir':6.0,'Myanmar':2.4,'Sri Lanka (Ceylon)':1.35,'Madagascar':1.0,'Australia':0.7,'Unknown / not certified':0.75}},
  'Pink sapphire':   {tiers:[300,1200,4000,15000],  origins:{'Sri Lanka (Ceylon)':1.3,'Madagascar':1.0,'Unknown / not certified':0.8}},
  'Yellow sapphire': {tiers:[200,700,2200,7000],    origins:{'Sri Lanka (Ceylon)':1.3,'Madagascar':1.0,'Unknown / not certified':0.8}},
  'Emerald':         {tiers:[300,1500,6000,28000],  origins:{'Colombia (Muzo)':2.2,'Zambia':1.0,'Brazil':0.85,'Unknown / not certified':0.75}},
  'Alexandrite':     {tiers:[1500,7000,22000,70000],origins:{'Russia (Ural)':2.5,'Brazil':1.2,'Sri Lanka':1.0,'Unknown / not certified':0.8}},
  'Spinel':          {tiers:[150,700,2500,9000],    origins:{'Myanmar (Mogok)':2.0,'Tanzania':1.0,'Unknown / not certified':0.85}},
  'Paraiba tourmaline':{tiers:[2000,9000,25000,60000],origins:{'Brazil':2.5,'Mozambique':1.0,'Nigeria':0.8,'Unknown / not certified':0.8}},
  'Tanzanite':       {tiers:[120,400,900,2200],     origins:{'Tanzania':1.0,'Unknown / not certified':0.95}},
  'Aquamarine':      {tiers:[60,220,600,1600],      origins:{'Brazil':1.0,'Mozambique':0.95,'Unknown / not certified':0.9}},
  'Tourmaline':      {tiers:[60,250,800,2500],      origins:{'Brazil':1.1,'Afghanistan':1.0,'Unknown / not certified':0.9}},
  'Tsavorite garnet':{tiers:[300,1200,3500,9000],   origins:{'Kenya':1.1,'Tanzania':1.0,'Unknown / not certified':0.9}},
  'Garnet':          {tiers:[25,90,300,900],        origins:{'Unknown / not certified':1.0}},
  'Peridot':         {tiers:[25,90,250,600],        origins:{'Pakistan (Kashmir)':1.4,'China':1.0,'Unknown / not certified':0.95}},
  'Amethyst':        {tiers:[8,25,60,150],          origins:{'Unknown / not certified':1.0}},
  'Citrine':         {tiers:[6,18,45,110],          origins:{'Unknown / not certified':1.0}},
  'Blue topaz':      {tiers:[6,15,35,80],           origins:{'Unknown / not certified':1.0}},
  'Imperial topaz':  {tiers:[200,800,2200,6000],    origins:{'Brazil':1.0,'Unknown / not certified':0.9}},
  'Opal (black)':    {tiers:[150,700,2500,9000],    origins:{'Australia (Lightning Ridge)':1.3,'Ethiopia':0.7,'Unknown / not certified':0.9}},
  'Opal (white)':    {tiers:[15,60,200,600],        origins:{'Australia':1.2,'Ethiopia':0.8,'Unknown / not certified':0.9}},
  'Jade (jadeite)':  {tiers:[100,900,6000,40000],   origins:{'Myanmar':1.2,'Unknown / not certified':0.8}}
};

const GEM_TIERS = ['Commercial','Good','Fine','Exceptional'];
const GEM_TIER_HELP = {
  'Commercial':  'Included, pale or over-dark, visible flaws to the naked eye. Most high-street coloured stones sit here.',
  'Good':        'Pleasant colour, minor visible inclusions, cut reasonably well. A nice everyday stone.',
  'Fine':        'Strong saturated colour, eye-clean or nearly so, well cut. What a specialist dealer would stock.',
  'Exceptional': 'Auction-house material — top colour, untreated, certified origin. Genuinely rare. If you are unsure, you are almost certainly not in this tier.'
};

/* Treatment is usually the biggest lever on value, and the one owners least often know. */
const GEM_TREATMENTS = {
  'Not treated (lab certified)':   {mult:3.2, note:'Untreated stones of good colour are genuinely scarce and carry a large premium — but only when a recognised lab says so in writing.'},
  'Heated (standard)':             {mult:1.0, note:'Heating is routine, permanent, accepted across the trade, and assumed unless a report says otherwise.'},
  'Oiled — minor (emerald)':       {mult:1.0, note:'Nearly every emerald is oiled. Minor oil is normal and does not meaningfully reduce value.'},
  'Oiled — moderate (emerald)':    {mult:0.62,note:'Moderate oil or resin indicates more fractures being masked, and buyers price accordingly.'},
  'Oiled — significant (emerald)': {mult:0.35,note:'Significant filling means substantial fractures. Value falls sharply and the stone is fragile.'},
  'Diffusion treated':             {mult:0.16,note:'Colour driven into the surface rather than grown in. A fraction of the value of a naturally coloured stone.'},
  'Fracture filled — glass':       {mult:0.04,note:'Lead-glass filled ruby is largely glass by volume. It has almost no resale value and can be destroyed by ordinary jewellery repair.'},
  'Dyed':                          {mult:0.07,note:'Dye sits in fractures and fades. Very little value.'},
  'Irradiated':                    {mult:0.55,note:'Common in blue topaz and some others. Stable, but priced below untreated equivalents.'},
  'Unknown':                       {mult:0.55,note:'Without a report a buyer must assume the least favourable case, and prices for that risk. Getting a report is often worth more than it costs.'}
};

/* Price per carat climbs much faster with size than it does for diamonds. */
const GEM_SIZE_STEPS = [
  {max:0.49,m:0.55},{max:0.99,m:0.78},{max:1.99,m:1.0},{max:2.99,m:1.5},
  {max:4.99,m:2.2},{max:9.99,m:3.2},{max:1e9,m:4.5}
];
function gemSizeMult(ct){ for(const s of GEM_SIZE_STEPS) if(ct<=s.max) return s.m; return 4.5; }

function valueGem(o){
  const g=GEMS[o.type]; if(!g) return null;
  const ct=Math.max(0.05, parseFloat(o.carat)||0); if(!ct) return null;
  const tierIx=Math.max(0, GEM_TIERS.indexOf(o.tier));
  const t=GEM_TREATMENTS[o.treatment]||GEM_TREATMENTS['Unknown'];

  /* Origin and treatment premiums overlap in reality — an "exceptional" ruby is usually
     already assumed unheated and Burmese — so multiplying them raw double counts and runs
     away at the top. Damp the combined premium above 4x rather than letting it compound. */
  let combined = (g.origins[o.origin] ?? 1) * t.mult;
  if(combined > 4) combined = 4 + (combined - 4) * 0.5;

  const ppc = g.tiers[tierIx] * gemSizeMult(ct) * combined;
  const retail = ppc * ct;

  /* Coloured stone resale is weaker than diamond resale: no universal grading means a
     buyer carries more risk, and the market for any given stone is thinner. */
  const band = tierIx >= 2 ? [0.20,0.35] : [0.10,0.22];
  return {
    retailLow:  Math.round(retail*0.72/5)*5,
    retailHigh: Math.round(retail*1.32/5)*5,
    resaleLow:  Math.round(retail*band[0]/5)*5,
    resaleHigh: Math.round(retail*band[1]/5)*5,
    ppc: Math.round(ppc),
    speculative: tierIx===3,
    treatmentNote: t.note
  };
}

/* ---------------- PEARLS ----------------
   Pearls are not priced per carat at all — by type, diameter, and quality. */
const PEARL_TYPES = {
  'Freshwater':  {base:70,   sizes:[6,12], note:'The most common and least expensive. Modern freshwater can rival Akoya in lustre.'},
  'Akoya':       {base:420,  sizes:[6,10], note:'The classic white round pearl. Sharp mirror-like lustre is what you pay for.'},
  'Tahitian':    {base:1100, sizes:[8,16], note:'Naturally dark. Green, peacock and aubergine overtones command the most.'},
  'South Sea':   {base:2800, sizes:[9,20], note:'The largest and rarest cultured pearl. White or golden; golden runs higher.'}
};
const PEARL_QUALITY = {'Commercial':0.45,'Good':1.0,'Fine':2.1,'Gem':4.5};

function valuePearlStrand(o){
  const t=PEARL_TYPES[o.type]; if(!t) return null;
  const mm=parseFloat(o.mm)||0; if(!mm) return null;
  const q=PEARL_QUALITY[o.quality] ?? 1;
  /* Value rises steeply with diameter — large round pearls are disproportionately rare. */
  const sizeFactor=Math.pow(mm/8, 3.1);
  const strand=t.base*sizeFactor*q;
  const single=strand/14;      /* a 16-18in strand is roughly 40 pearls; one pearl is worth far less pro-rata */
  return {
    strandLow:  Math.round(strand*0.7/10)*10,
    strandHigh: Math.round(strand*1.35/10)*10,
    singleLow:  Math.max(1, Math.round(single*0.7)),
    singleHigh: Math.max(2, Math.round(single*1.35)),
    note:t.note
  };
}
