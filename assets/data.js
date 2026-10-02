/* CaratBase — shared data + valuation engine
   All estimates. Market anchors reflect US retail, natural round-brilliant GIA baseline. */

/* ---------------------------------------------------------------
   1. HALLMARK / STAMP DATABASE
   --------------------------------------------------------------- */
const STAMPS = [
  /* ---- GOLD (solid) ---- */
  {code:'375',  alias:['9k','9kt','9ct','.375'], metal:'Gold', purity:'9K · 37.5% gold',
   value:'solid', note:'The UK and Commonwealth entry-level gold standard. Legal to call gold in the UK, but NOT in the US, where 10K is the legal minimum.',
   worth:'Solid gold. Scrap value is real but modest — a little over a third of the piece weight is actual gold.'},
  {code:'417',  alias:['10k','10kt','.417'], metal:'Gold', purity:'10K · 41.7% gold',
   value:'solid', note:'The lowest purity that can legally be sold as "gold" in the United States. Very common in American mass-market jewelry.',
   worth:'Solid gold. Durable and cheap — often used for class rings and chain.'},
  {code:'585',  alias:['14k','14kt','583','.585'], metal:'Gold', purity:'14K · 58.5% gold',
   value:'solid', note:'The single most common gold standard in the US — the default for engagement rings and fine jewelry. A stamp of 583 rather than 585 usually indicates older Soviet or Eastern European origin.',
   worth:'Solid gold, and the sweet spot of durability and value. Just over half the weight is pure gold.'},
  {code:'750',  alias:['18k','18kt','.750'], metal:'Gold', purity:'18K · 75% gold',
   value:'solid', note:'The European fine-jewelry standard and the mark of most luxury houses — Cartier, Tiffany, Van Cleef. Richer yellow than 14K.',
   worth:'Solid gold, high value. Three quarters of the metal weight is pure gold.'},
  {code:'875',  alias:['21k','21kt'], metal:'Gold', purity:'21K · 87.5% gold',
   value:'solid', note:'Common in the Gulf states and parts of the Middle East. Rare in Western jewelry.',
   worth:'Solid gold, very high value. Soft — bends more easily than 14K or 18K.'},
  {code:'916',  alias:['22k','22kt','917','.916'], metal:'Gold', purity:'22K · 91.6% gold',
   value:'solid', note:'The Indian and South Asian gold standard, and the basis of BIS hallmarking in India. Also common across the Middle East.',
   worth:'Solid gold, very high value — often bought as a store of wealth rather than as fashion.'},
  {code:'999',  alias:['24k','24kt','990','.999','9999'], metal:'Gold or fine silver', purity:'24K · 99.9% pure',
   value:'solid', note:'Pure metal. On gold this is bullion-grade — too soft for most jewelry, so it usually indicates a bar, coin, or an investment piece. On silver, 999 means fine silver rather than sterling.',
   worth:'Maximum metal value. Check whether the piece is gold or silver before assuming — the same number is used for both.'},

  /* ---- SILVER ---- */
  {code:'925',  alias:['sterling','ster','.925','s925'], metal:'Silver', purity:'Sterling · 92.5% silver',
   value:'solid', note:'Sterling silver — by far the most common silver stamp in the world. The remaining 7.5% is usually copper, added for hardness.',
   worth:'Real solid silver, but silver is inexpensive by weight. Value usually sits in the craftsmanship, the maker, or the stones — not the metal.'},
  {code:'958',  alias:['britannia','.958'], metal:'Silver', purity:'Britannia · 95.8% silver',
   value:'solid', note:'A higher British silver standard, used 1697–1720 by law and voluntarily since. Softer and rarer than sterling.',
   worth:'Solid silver at above-sterling purity. The rarity of the standard can add collector interest.'},
  {code:'900',  alias:['coin','coin silver','.900'], metal:'Silver', purity:'Coin · 90% silver',
   value:'solid', note:'"Coin silver" — historically made from melted currency. Common in 19th-century American flatware.',
   worth:'Solid silver. Antique American coin silver often carries collector value well above scrap.'},
  {code:'800',  alias:['.800'], metal:'Silver', purity:'800 · 80% silver',
   value:'solid', note:'A Continental European standard, especially German and Italian. Below the sterling threshold, so it cannot legally be called sterling in the US or UK.',
   worth:'Solid silver, lower purity. Still worth melting, but priced below sterling.'},
  {code:'835',  alias:['830','.835','.830'], metal:'Silver', purity:'830–835 · 83–83.5% silver',
   value:'solid', note:'Scandinavian and Northern European standards, common in Danish, Dutch and German pieces of the early 20th century.',
   worth:'Solid silver below sterling purity. Mid-century Scandinavian design often carries strong collector value.'},

  /* ---- PLATINUM & PALLADIUM ---- */
  {code:'PT950', alias:['950','plat','platinum','pt','950pt','irid plat','10% irid'], metal:'Platinum', purity:'95% platinum',
   value:'solid', note:'The US platinum standard for fine jewelry. "IRID PLAT" or "10% IRID" indicates an older piece alloyed with iridium — typical of Art Deco and mid-century settings.',
   worth:'High metal value and dense, so pieces weigh more than they look. Older iridium-alloy settings can carry significant antique premium.'},
  {code:'PT900', alias:['900pt','850','pt850'], metal:'Platinum', purity:'85–90% platinum',
   value:'solid', note:'Lower platinum standards, more common in Japanese and older European work.',
   worth:'Solid platinum, still high value by weight.'},
  {code:'PD950', alias:['pd','pall','palladium','950pall','pd500'], metal:'Palladium', purity:'50–95% palladium',
   value:'solid', note:'A lighter, cheaper platinum-group metal that saw a surge of use in the 2000s. Hypoallergenic and naturally white.',
   worth:'Real precious metal, though palladium pricing is far more volatile than gold or platinum.'},

  /* ---- PLATED / FILLED — the disappointing ones ---- */
  {code:'GP',   alias:['gold plated','18kgp','14kgp','gpl','g.p.'], metal:'Base metal', purity:'Plated — microns of gold',
   value:'plated', note:'Gold plated. A base metal core with an extremely thin electroplated gold layer, often under one micron thick.',
   worth:'Effectively no precious metal value. Scrap buyers will not pay for this. Any value is in the design or brand.', warn:true},
  {code:'GEP',  alias:['hge','gold electroplate','heavy gold electroplate','18khge'], metal:'Base metal', purity:'Electroplated',
   value:'plated', note:'Gold electroplate, or heavy gold electroplate. Still plating — "heavy" is a marketing word, not a standard.',
   worth:'No meaningful precious metal value.', warn:true},
  {code:'GF',   alias:['gold filled','1/20 12k gf','12kgf','14kgf','1/10 10k','rgp','rolled gold'], metal:'Base metal + bonded gold', purity:'Gold filled — typically 5% gold by weight',
   value:'filled', note:'Gold filled is a genuine mechanical layer of gold bonded to brass, roughly 100 times thicker than plating. The fraction stamp tells you the ratio — 1/20 12K GF means 1/20th of the total weight is 12K gold.',
   worth:'Low but not zero. Some refiners buy gold-filled scrap in bulk. Wears far better than plating and vintage gold-filled has collector demand.', warn:true},
  {code:'VERMEIL', alias:['verm','gold vermeil'], metal:'Sterling silver + gold', purity:'Sterling base, gold layer',
   value:'filled', note:'Vermeil is sterling silver with a gold layer of at least 2.5 microns. Legally it must have a real silver base — that is what separates it from plating.',
   worth:'Worth the silver underneath. The gold layer adds little to scrap value but a lot to appearance.', warn:true},
  {code:'EPNS', alias:['epns','nickel silver','german silver','alpaca','ns','a1','silver plated','sp'], metal:'Base metal', purity:'No silver content',
   value:'none', note:'Electroplated nickel silver, German silver, alpaca and nickel silver all contain NO silver whatsoever. The word "silver" in these names refers to the color, not the metal. "A1" indicates a plating grade.',
   worth:'No precious metal value at all. This is the single most common source of disappointment in inherited jewelry.', warn:true},

  /* ---- OTHER MARKS ---- */
  {code:'KP',   alias:['plumb','14kp','18kp','10kp'], metal:'Gold', purity:'Karat plumb — exact',
   value:'solid', note:'"Plumb" means the gold is exactly the stated karat, with no downward tolerance. A 14KP piece is a full 14K, not 13.6K.',
   worth:'Solid gold, and a mark of an honest manufacturer.'},
  {code:'CZ',   alias:['cubic zirconia','czs','diamonique','dq'], metal:'—', purity:'Simulant stone',
   value:'none', note:'Cubic zirconia — a synthetic diamond simulant. Not a diamond and not a lab-grown diamond; a completely different material with different optics.',
   worth:'The stone has essentially no resale value. Any worth is in the metal it is set in.', warn:true},
  {code:'MOISSANITE', alias:['moiss','moissanite','charles colvard'], metal:'—', purity:'Simulant stone',
   value:'none', note:'Silicon carbide. Extremely durable and more brilliant than diamond, but an entirely different stone.',
   worth:'Little secondary market. Retails far below diamond and resells at a fraction of that.', warn:true},
  {code:'LG',   alias:['lab grown','lab-grown','lgd','laboratory grown','created'], metal:'—', purity:'Lab-grown diamond',
   value:'lab', note:'A real diamond, chemically identical to mined, but grown in a laboratory. Since 2023 the required disclosure has usually been stamped on the girdle of the stone or on the ring shank.',
   worth:'Physically a real diamond — but lab-grown prices have collapsed as production scaled, and resale is currently very weak. See our valuation tool for the current spread.', warn:true},
  {code:'STAINLESS', alias:['stainless','stnls','316l','ti','titanium','tungsten'], metal:'Base metal', purity:'Non-precious',
   value:'none', note:'Stainless steel, titanium and tungsten are durable modern jewelry metals with no precious content.',
   worth:'No scrap value. Common in men’s wedding bands.', warn:true},
  {code:'BIS',  alias:['bis','huid','hallmark india','bis916'], metal:'Gold (India)', purity:'BIS certified',
   value:'solid', note:'The Indian Bureau of Indian Standards hallmark. Since 2021 it comprises three marks: the BIS triangle logo, the purity grade (such as 22K916), and a six-character alphanumeric HUID unique to that piece.',
   worth:'Government-certified purity, which makes Indian gold unusually easy to resell at close to full metal value.'},
  {code:'LION', alias:['lion passant','leopard','anchor','rose','castle','uk hallmark','assay'], metal:'UK assay marks', purity:'British hallmarking system',
   value:'solid', note:'British hallmarks are a set, not a single stamp: a sponsor mark, a fineness mark, and an assay office mark. A walking lion means sterling silver. A leopard’s head is London, an anchor Birmingham, a castle Edinburgh, a rose Sheffield. A date letter gives the exact year.',
   worth:'A full UK hallmark set is the strongest provenance you can have — it dates the piece to a single year and can add substantial value.'}
];

/* ---------------------------------------------------------------
   2. DIAMOND VALUATION ENGINE
   Baseline: natural, round brilliant, GIA, G color, VS2 clarity,
   Very Good cut. All figures are estimates in USD.
   --------------------------------------------------------------- */

/* Price per carat rises sharply at each "magic size" threshold.
   The bottom of this curve matters more than it looks: melee is priced per carat far
   below whole stones, so a 40-stone halo must be valued at melee rates on each
   individual stone, never as one 0.4 ct lump. Getting that wrong inflates a halo
   by roughly an order of magnitude. */
const PPC_BRACKETS = [
  {max:0.008,ppc:800},{max:0.015,ppc:950},{max:0.03, ppc:1100},
  {max:0.05, ppc:1200},{max:0.10, ppc:1300},{max:0.18, ppc:1350},
  {max:0.29, ppc:1400},{max:0.49, ppc:1900},{max:0.69, ppc:2700},
  {max:0.89, ppc:3400},{max:0.99, ppc:4000},{max:1.49, ppc:5200},
  {max:1.99, ppc:6500},{max:2.99, ppc:8500},{max:3.99, ppc:11500},
  {max:99,   ppc:14000}
];
const COLOR_MULT   = {D:1.35,E:1.25,F:1.15,G:1.00,H:0.90,I:0.78,J:0.66,K:0.55};
const CLARITY_MULT = {FL:1.60,IF:1.45,VVS1:1.30,VVS2:1.22,VS1:1.10,VS2:1.00,SI1:0.86,SI2:0.72,I1:0.45};
const CUT_MULT     = {Excellent:1.08,'Very Good':1.00,Good:0.90,Fair:0.78};
const SHAPE_MULT   = {Round:1.00,Oval:0.85,Pear:0.80,Emerald:0.78,Asscher:0.78,
                      Cushion:0.75,Princess:0.75,Radiant:0.75,Marquise:0.75,Heart:0.78};
const LAB_FACTOR   = 0.15;   /* lab-grown vs natural retail, post-collapse */

/* Resale is the number nobody publishes. This is the honest part. */
const RESALE_NATURAL = [0.25,0.40];
const RESALE_LAB     = [0.05,0.12];

/* Gold spot placeholder — refreshed by the daily metals job */
const GOLD_SPOT_PER_G = 134.39;
const KARAT_PURITY = {'24K':0.999,'22K':0.916,'18K':0.750,'14K':0.585,'10K':0.417,'9K':0.375,'Platinum':0.95,'Silver 925':0.925,'None / not sure':0};
/* Seed values. assets/spot.js overwrites these from metals.json on load. */
const METAL_SPOT = {gold:134.39, platinum:55.33, silver:1.97}; /* USD per gram */

function ppcFor(ct){ for(const b of PPC_BRACKETS){ if(ct<=b.max) return b.ppc; } return 14000; }

function valueDiamond(o){
  const ct = Math.max(0.01, parseFloat(o.carat)||0);
  if(!ct) return null;
  let retail = ppcFor(ct) * ct;
  retail *= (COLOR_MULT[o.color]   ?? 1);
  retail *= (CLARITY_MULT[o.clarity] ?? 1);
  retail *= (CUT_MULT[o.cut]       ?? 1);
  retail *= (SHAPE_MULT[o.shape]   ?? 1);
  if(o.origin === 'Lab-grown') retail *= LAB_FACTOR;
  if(o.cert === 'None') retail *= 0.82;          /* uncertified stones trade at a discount */
  else if(o.cert === 'IGI' || o.cert === 'Other') retail *= 0.93;

  const band = o.origin === 'Lab-grown' ? RESALE_LAB : RESALE_NATURAL;
  return {
    retailLow:  Math.round(retail*0.88/25)*25,
    retailHigh: Math.round(retail*1.14/25)*25,
    resaleLow:  Math.round(retail*band[0]/25)*25,
    resaleHigh: Math.round(retail*band[1]/25)*25,
    isLab: o.origin === 'Lab-grown'
  };
}

function valueMetal(karat, grams){
  const g = parseFloat(grams)||0;
  if(!g || !karat || karat === 'None / not sure') return 0;
  if(karat === 'Platinum')   return Math.round(g * METAL_SPOT.platinum * 0.95);
  if(karat === 'Silver 925') return Math.round(g * METAL_SPOT.silver  * 0.925);
  return Math.round(g * METAL_SPOT.gold * (KARAT_PURITY[karat]||0));
}

/* ---------------------------------------------------------------
   2b. SIDE STONES / MELEE
   Weight scales with the cube of the diameter, and a 1 ct round is 6.5 mm, so
   ct = (mm/6.5)^3. Checked against the size table: 5.1 mm -> 0.483 ct (0.50 actual),
   4.1 mm -> 0.251 ct (0.25 actual).
   --------------------------------------------------------------- */
function caratForMm(mm){
  const d = parseFloat(mm) || 0;
  return d > 0 ? +Math.pow(d / 6.5, 3).toFixed(4) : 0;
}

/* Typical settings, so nobody has to count 38 stones with a loupe to get a number. */
const SETTINGS = [
  {key:'solitaire',  label:'Solitaire — no side stones', count:0,  mm:0},
  {key:'halo',       label:'Halo',                        count:18, mm:1.2},
  {key:'halo_pave',  label:'Halo with pavé band',         count:38, mm:1.3},
  {key:'pave',       label:'Pavé band',                   count:20, mm:1.5},
  {key:'three',      label:'Three-stone',                 count:2,  mm:4.5},
  {key:'cluster',    label:'Cluster',                     count:12, mm:2.0},
  {key:'eternity',   label:'Eternity band',               count:30, mm:2.0},
  {key:'custom',     label:'Something else — I will count',count:0, mm:1.5}
];

/* Each stone is priced at its OWN per-carat rate, then multiplied by the count. */
function valueMelee(count, mm, origin){
  const n = parseInt(count) || 0;
  const ctEach = caratForMm(mm);
  if(!n || !ctEach) return null;
  let each = ctEach * ppcFor(ctEach);
  if(origin === 'Lab-grown') each *= 0.10;      /* lab melee is cheaper still than lab solitaires */
  const retail = each * n;
  return {
    count:n, ctEach, totalCt:+(ctEach*n).toFixed(3),
    retailLow:  Math.round(retail*0.85/5)*5,
    retailHigh: Math.round(retail*1.15/5)*5,
    /* Nobody buys used melee on its own — it rides along with the setting. */
    resaleLow:  Math.round(retail*0.05/5)*5,
    resaleHigh: Math.round(retail*0.15/5)*5
  };
}

/* ---------------------------------------------------------------
   3. TRUE-SCALE MM TABLE (round brilliant, face-up diameter)
   --------------------------------------------------------------- */
const CARAT_MM = [
  {ct:0.25,mm:4.1},{ct:0.33,mm:4.4},{ct:0.40,mm:4.8},{ct:0.50,mm:5.1},
  {ct:0.60,mm:5.4},{ct:0.70,mm:5.7},{ct:0.75,mm:5.8},{ct:0.90,mm:6.2},
  {ct:1.00,mm:6.5},{ct:1.25,mm:6.9},{ct:1.50,mm:7.4},{ct:1.75,mm:7.8},
  {ct:2.00,mm:8.1},{ct:2.50,mm:8.8},{ct:3.00,mm:9.4},{ct:3.50,mm:9.9},
  {ct:4.00,mm:10.4},{ct:5.00,mm:11.0}
];
function mmForCarat(ct){
  let best = CARAT_MM[0];
  for(const r of CARAT_MM) if(Math.abs(r.ct-ct) < Math.abs(best.ct-ct)) best = r;
  return best.mm;
}

const fmt = n => '$' + Math.round(n).toLocaleString('en-US');


/* ---------------------------------------------------------------
   4. REVERSE SOLVE — biggest stone a budget will buy
   Price per carat steps at each size threshold, so the relationship between budget and
   carat is not smooth and cannot be solved algebraically. Walking the curve is exact and
   costs nothing at this resolution.
   --------------------------------------------------------------- */
function caratForBudget(budget, spec){
  const b = parseFloat(budget) || 0;
  if(b <= 0) return null;
  let best = null;
  for(let ct = 0.20; ct <= 15.001; ct += 0.01){   /* well past any realistic budget */
    const v = valueDiamond({carat:+ct.toFixed(2), ...spec});
    if(!v) continue;
    if(v.retailLow <= b) best = {carat:+ct.toFixed(2), ...v};
    else break;                       /* price rises monotonically with weight */
  }
  return best;
}

/* Four honest ways to spend the same money. */
const BUDGET_STRATEGIES = [
  {key:'size',   label:'Go for size',
   spec:{color:'J', clarity:'SI2', cut:'Very Good', shape:'Oval',  origin:'Natural', cert:'GIA'},
   note:'Lower color and clarity, and an elongated shape that spreads wider. Faces up much larger; a warm tint is visible against white metal.'},
  {key:'balance',label:'The balanced pick',
   spec:{color:'G', clarity:'VS2', cut:'Excellent', shape:'Round', origin:'Natural', cert:'GIA'},
   note:'Eye-clean, no visible tint, excellent cut. The specification most jewelers steer people toward, and the easiest to resell.'},
  {key:'quality',label:'Go for quality',
   spec:{color:'D', clarity:'VVS1', cut:'Excellent', shape:'Round', origin:'Natural', cert:'GIA'},
   note:'Top color and near-flawless. Almost none of this is visible without a loupe, which is why it buys so much less stone.'},
  {key:'lab',    label:'Lab-grown',
   spec:{color:'F', clarity:'VS1', cut:'Excellent', shape:'Round', origin:'Lab-grown', cert:'IGI'},
   note:'A real diamond, chemically identical, for a fraction of the money. Resale is currently very weak, so buy it to wear rather than to hold value.'}
];

/* ---------------------------------------------------------------
   5. WEIGHT FROM DIMENSIONS
   A plain band is an annulus: volume = pi x mean diameter x width x thickness.
   Mean diameter is the inside diameter plus one thickness, since the band wraps outside it.
   --------------------------------------------------------------- */
const METAL_DENSITY = {   /* g/cm3 */
  '24K':19.3, '22K':17.7, '18K':15.5, '14K':13.1, '10K':11.6, '9K':11.2,
  'Platinum':20.1, 'Silver 925':10.36
};
function bandWeight(insideDiaMm, widthMm, thicknessMm, karat){
  const d=parseFloat(insideDiaMm)||0, w=parseFloat(widthMm)||0, t=parseFloat(thicknessMm)||0;
  const rho=METAL_DENSITY[karat];
  if(!d||!w||!t||!rho) return null;
  const meanD = d + t;
  const mm3 = Math.PI * meanD * w * t;
  const grams = (mm3/1000) * rho;
  return { grams:+grams.toFixed(2), cm3:+(mm3/1000).toFixed(3), density:rho };
}

/* ---------------------------------------------------------------
   3. GIA REPORT INTELLIGENCE
   A GIA report states what a diamond IS. By policy it never states what it is
   worth, and it carries three fields consumers routinely misread. This section
   turns a report into a valuation plus the specific things worth knowing.

   Fluorescence is the big one, and its effect flips sign with color grade.
   Blue fluorescence is the complement of yellow, so in an already-colorless
   stone it reads as a defect and is discounted, while in a tinted stone it
   masks the tint and can make the diamond face up a grade whiter.
   Trade discounts on D-F with strong blue commonly run 5-40%; ~12% is typical.
   I-M with medium-to-very-strong fluorescence trades flat to a slight premium.
   --------------------------------------------------------------- */
const FLUO_GRADES = ['None', 'Faint', 'Medium', 'Strong', 'Very Strong'];

const FLUO_MULT = {
  /* colorless D-F: fluorescence is a discount */
  high:  {None:1.00, Faint:0.99, Medium:0.95, Strong:0.88, 'Very Strong':0.82},
  /* near-colorless G-H: largely neutral */
  mid:   {None:1.00, Faint:1.00, Medium:0.99, Strong:0.97, 'Very Strong':0.94},
  /* faint tint I-K: blue masks yellow, so flat to slightly positive */
  tinted:{None:1.00, Faint:1.00, Medium:1.01, Strong:1.02, 'Very Strong':1.01},
};

function fluoBand(color){
  if (['D','E','F'].includes(color)) return 'high';
  if (['G','H'].includes(color))     return 'mid';
  return 'tinted';
}

function fluoMultiplier(color, fluo){
  return FLUO_MULT[fluoBand(color)][fluo] ?? 1;
}

/* GIA grades cut for round brilliants only. Fancy shapes carry polish and
   symmetry but no overall cut grade, which is why "Excellent / Excellent" on a
   fancy is a finish grade, not a verdict on how well the stone was cut.
   GIA has said cut grades for marquise, oval and pear arrive in 2027. */
const GIA_CUT_GRADED_SHAPES = ['Round'];
const GIA_CUT_COMING_2027   = ['Oval', 'Pear', 'Marquise'];

/* Weight sits just under a magic number: the same stone one hundredth heavier
   crosses into a much higher price bracket. Works in the buyer's favor. */
function caratCliff(ct){
  for (const edge of [0.50, 0.70, 0.90, 1.00, 1.50, 2.00, 3.00]) {
    if (ct >= edge - 0.06 && ct < edge) {
      return {edge, below: +(edge - ct).toFixed(2)};
    }
  }
  return null;
}

/* Value a stone described by a GIA report, and say what the report does not.
   o: {shape, carat, color, clarity, cut, polish, symmetry, fluorescence, origin}
   Returns the usual valuation plus `notes`, each {kind, head, body, effect}. */
function valueGiaReport(o){
  const ct = Math.max(0.01, parseFloat(o.carat) || 0);
  if (!ct) return null;

  const base = valueDiamond({
    carat: ct, color: o.color, clarity: o.clarity,
    cut: o.cut || 'Very Good', shape: o.shape,
    origin: o.origin, cert: 'GIA',
  });
  if (!base) return null;

  const fm = fluoMultiplier(o.color, o.fluorescence || 'None');
  const v = {
    retailLow:  Math.round(base.retailLow  * fm / 25) * 25,
    retailHigh: Math.round(base.retailHigh * fm / 25) * 25,
    resaleLow:  Math.round(base.resaleLow  * fm / 25) * 25,
    resaleHigh: Math.round(base.resaleHigh * fm / 25) * 25,
    isLab: base.isLab,
    fluoMultiplier: fm,
    notes: [],
  };
  const add = (kind, head, body, effect) => v.notes.push({kind, head, body, effect});

  /* --- fluorescence --- */
  const fl = o.fluorescence || 'None';
  const band = fluoBand(o.color);
  if (fl !== 'None' && fl !== 'Faint') {
    const pct = Math.round(Math.abs(1 - fm) * 100);
    if (band === 'high') {
      add('cost', `${fl} fluorescence is costing you about ${pct}%`,
        `In a ${o.color} color stone the trade treats blue fluorescence as a fault and discounts it — 5% to 40% depending on severity and how milky the stone faces up. It is the one grade on your report that moves the price without changing how most people see the diamond. A ${o.color} with strong fluorescence can price like a non-fluorescent stone several grades lower.`,
        -pct);
    } else if (band === 'tinted') {
      add('good', `${fl} fluorescence is working in your favor`,
        `Blue is the complement of yellow, so in a ${o.color} color stone the fluorescence masks the tint and the diamond can face up close to a grade whiter. Stones like yours trade flat to a slight premium, and you likely paid less than a non-fluorescent equivalent that looks the same.`,
        +pct);
    } else {
      add('neutral', `${fl} fluorescence barely matters here`,
        `At ${o.color} color the discount for fluorescence is small — the trade prices it at a few percent at most. Do not let anyone value your stone as if it were a serious fault.`,
        -pct);
    }
  }

  /* --- cut grade on fancy shapes --- */
  if (!GIA_CUT_GRADED_SHAPES.includes(o.shape)) {
    const coming = GIA_CUT_COMING_2027.includes(o.shape);
    add('watch', `Your report has no cut grade — and that is normal`,
      `GIA grades cut for round brilliants only. A ${o.shape.toLowerCase()} carries Polish and Symmetry but no overall cut grade, so "Excellent Polish, Excellent Symmetry" describes the finish, not how well the stone was cut for light. Two ${o.shape.toLowerCase()}s with identical reports can look very different. Judge it with your eyes and the proportions, not the grades.${coming ? ` GIA has said it will start grading cut on ${o.shape.toLowerCase()}s in 2027.` : ''}`,
      0);
  }

  /* --- polish / symmetry drag --- */
  const weak = ['Fair', 'Poor'];
  if (weak.includes(o.polish) || weak.includes(o.symmetry)) {
    add('cost', 'Weak finish grades hold the price down',
      `Polish ${o.polish || '—'} and Symmetry ${o.symmetry || '—'}. Below Good, finish starts to show as softness and misaligned facets, and the stone is harder to resell whatever the color and clarity say.`,
      -5);
  }

  /* --- the carat cliff --- */
  const cliff = caratCliff(ct);
  if (cliff) {
    add('good', `You bought below the ${cliff.edge} carat cliff`,
      `At ${ct} ct your stone sits ${cliff.below} ct under ${cliff.edge}, where price per carat steps up sharply. The difference is invisible on a hand — roughly a tenth of a millimeter — but it is the single biggest saving available in a diamond. Whoever bought this chose well.`,
      0);
  }

  /* --- eye-clean clarity --- */
  if (['VVS1', 'VVS2', 'IF', 'FL'].includes(o.clarity)) {
    add('watch', 'You are paying for clarity nobody can see',
      `${o.clarity} is well past the point where inclusions are visible without magnification. It holds value on paper, but a VS1 or VS2 looks identical in the hand for meaningfully less money. Worth knowing if you ever upgrade.`,
      0);
  }

  /* --- lab-grown reality --- */
  if (v.isLab) {
    add('cost', 'A GIA report does not protect a lab-grown resale',
      `The grades are real and independently verified, but lab-grown prices have fallen steadily as production scaled, and resale runs at a small fraction of retail regardless of who graded it. Value it for wearing, not for holding.`,
      0);
  }

  return v;
}
