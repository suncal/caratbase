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
   value:'solid', note:'The lowest purity that can legally be sold as "gold" in the United States. Very common in American mass-market jewellery.',
   worth:'Solid gold. Durable and cheap — often used for class rings and chain.'},
  {code:'585',  alias:['14k','14kt','583','.585'], metal:'Gold', purity:'14K · 58.5% gold',
   value:'solid', note:'The single most common gold standard in the US — the default for engagement rings and fine jewellery. A stamp of 583 rather than 585 usually indicates older Soviet or Eastern European origin.',
   worth:'Solid gold, and the sweet spot of durability and value. Just over half the weight is pure gold.'},
  {code:'750',  alias:['18k','18kt','.750'], metal:'Gold', purity:'18K · 75% gold',
   value:'solid', note:'The European fine-jewellery standard and the mark of most luxury houses — Cartier, Tiffany, Van Cleef. Richer yellow than 14K.',
   worth:'Solid gold, high value. Three quarters of the metal weight is pure gold.'},
  {code:'875',  alias:['21k','21kt'], metal:'Gold', purity:'21K · 87.5% gold',
   value:'solid', note:'Common in the Gulf states and parts of the Middle East. Rare in Western jewellery.',
   worth:'Solid gold, very high value. Soft — bends more easily than 14K or 18K.'},
  {code:'916',  alias:['22k','22kt','917','.916'], metal:'Gold', purity:'22K · 91.6% gold',
   value:'solid', note:'The Indian and South Asian gold standard, and the basis of BIS hallmarking in India. Also common across the Middle East.',
   worth:'Solid gold, very high value — often bought as a store of wealth rather than as fashion.'},
  {code:'999',  alias:['24k','24kt','990','.999','9999'], metal:'Gold or fine silver', purity:'24K · 99.9% pure',
   value:'solid', note:'Pure metal. On gold this is bullion-grade — too soft for most jewellery, so it usually indicates a bar, coin, or an investment piece. On silver, 999 means fine silver rather than sterling.',
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
   value:'solid', note:'The US platinum standard for fine jewellery. "IRID PLAT" or "10% IRID" indicates an older piece alloyed with iridium — typical of Art Deco and mid-century settings.',
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
   value:'none', note:'Electroplated nickel silver, German silver, alpaca and nickel silver all contain NO silver whatsoever. The word "silver" in these names refers to the colour, not the metal. "A1" indicates a plating grade.',
   worth:'No precious metal value at all. This is the single most common source of disappointment in inherited jewellery.', warn:true},

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
   value:'none', note:'Stainless steel, titanium and tungsten are durable modern jewellery metals with no precious content.',
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
   Baseline: natural, round brilliant, GIA, G colour, VS2 clarity,
   Very Good cut. All figures are estimates in USD.
   --------------------------------------------------------------- */

/* Price per carat rises sharply at each "magic size" threshold */
const PPC_BRACKETS = [
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
const GOLD_SPOT_PER_G = 78.0;
const KARAT_PURITY = {'24K':0.999,'22K':0.916,'18K':0.750,'14K':0.585,'10K':0.417,'9K':0.375,'Platinum':0.95,'Silver 925':0.925,'None / not sure':0};
const METAL_SPOT = {gold:78.0, platinum:33.0, silver:0.95}; /* USD per gram */

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
