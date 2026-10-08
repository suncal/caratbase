/* CaratBase — partner and monetisation configuration.
 *
 * ONE file holds every commercial link on the site. Two rules it enforces:
 *
 *  1. Recommendations are useful before they are profitable. Links point at the real
 *     companies today with no tracking code, so a visitor gets the answer now. Turning on
 *     revenue later means pasting an id below — not rebuilding a page.
 *  2. Nothing is recommended that we would not recommend unpaid. If a partner's `aff` is
 *     empty the link still shows, just untracked; if a partner stops being the honest
 *     answer, it comes out of this file regardless of what it pays.
 *
 * TO ACTIVATE: fill in `aff` with your tracking URL or append your parameter, set
 * ADS.adsense.client, then reload. Disclosure text appears automatically once any
 * affiliate link is live, because that is a legal requirement, not a choice.
 */

const PARTNERS = {

  /* People about to BUY — budget calculator, ring sizer, size charts. */
  retail: [
    {name:'Blue Nile',       url:'https://www.bluenile.com',      aff:'https://www.bluenile.com/?a_aid=o3pbbkxavl0np&utm_source=pap&utm_medium=affiliates',
     note:'The largest online inventory. Program terms as approved 2026-09-15: 3.5% on all sales (James Allen stones included).'},
    {name:'James Allen',     url:'https://www.jamesallen.com',    aff:'',
     note:'360-degree video on every stone, which is the closest thing to seeing it in person. 5%, 60-day cookie.'},
    {name:'Brilliant Earth', url:'https://www.brilliantearth.com',aff:'',
     note:'Traceable sourcing. 5% on bridal, 7% on fine jewelry, 30-day cookie.'}
  ],

  /* People who OWN it — valuation, vault. The highest-converting money event we have,
     and the only one that renews every year. */
  insurance: [
    {name:'BriteCo',         url:'https://brite.co',              aff:'',
     note:'Jewelry-specific cover, $0 deductible. Gives its appraisal software to jewelers free, funded by referrals — which tells you what a referral is worth.'},
    {name:'Jewelers Mutual', url:'https://www.jewelersmutual.com',aff:'',
     note:'The oldest specialist jewelry insurer in the US. $0 deductible.'}
  ],

  /* People SELLING. Never one buyer — the spread between them is the whole point. */
  /* Sell-side. This is where the site's differentiator points: every page that prints an
     honest resale figure manufactures a seller, and a seller converts harder than a
     browser. Published rates when these were checked (2026-09-27):
       Diamond Banc  10% of the funded amount, capped at $250 per completed referral
       myGemma       5%, 30-day cookie
       Worthy        via FlexOffers, 7-day cookie, rate not published
     To switch one on, paste its tracking URL into `aff` — nothing else needs changing,
     and the disclosure appears automatically. */
  buyers: [
    {name:'Worthy',          url:'https://www.worthy.com',        aff:'',
     note:'Auctions your piece to a network of dealers, so buyers compete. 18% commission, 2–4 weeks.'},
    {name:'myGemma',         url:'https://www.mygemma.com',       aff:'',
     note:'Formerly WP Diamonds. Direct offer rather than auction — faster, usually lower.'},
    {name:'Diamond Banc',    url:'https://diamondbanc.com',       aff:'',
     note:'Buys outright and also lends against jewelry if you want it back.'}
  ],

  /* Scrap gold and silver. Mounted anywhere we print a melt figure. */
  metalBuyers: [
    {name:'CashforGoldUSA',  url:'https://cashforgoldusa.com',    aff:'',
     note:'Insured shipping, pays on approval. Compare its offer against the figure above before accepting.'}
  ],

  /* Colored stones — a report is often worth more than it costs. Not affiliate; these
     are simply the right places to send someone. */
  labs: [
    {name:'GIA',             url:'https://www.gia.edu/gem-lab-service/identification-report', aff:'',
     note:'Identification and treatment reports. The most widely recognized name in the trade.'},
    {name:'AGL',             url:'https://www.aglgemlab.com',     aff:'',
     note:'American Gemological Laboratories — the specialist most respected for colored stone origin.'}
  ],

  /* Appraisers. Deliberately a professional body rather than a company: the honest answer
     is "find a qualified independent appraiser near you", and that pays nothing. */
  appraisers: [
    {name:'NAJA',            url:'https://www.najaappraisers.com', aff:'',
     note:'National Association of Jewelry Appraisers — searchable directory of accredited independents.'},
    {name:'ASA',             url:'https://www.appraisers.org',     aff:'',
     note:'American Society of Appraisers. Look for a Gems & Jewelry designation.'}
  ]
};

/* Blue Nile deep links. Parameter scheme verified against the live site 2026-09-15:
 *   /diamonds?Shape=oval-cut&CaratFrom=1.4&CaratTo=1.6&Color=G,F,E,D&Clarity=VS2,VS1,VVS2,VVS1,IF,FL
 *   /diamonds/lab-grown-diamonds?…same parameters…
 * A visitor who has just priced a 1.5 ct oval G/VS2 lands on exactly those stones.
 *
 * TO ACTIVATE (R2Net affiliate program, Post Affiliate Pro): after approval, copy the
 * tracking-link template from the affiliate dashboard into `template`, keeping {url} where
 * the destination goes. Typical shape:
 *   https://affiliates.r2net.com/scripts/XXXX?a_aid=YOUR_ID&a_bid=YOUR_BANNER&desturl={url}
 * Until then every link is the plain Blue Nile URL — useful, untracked, undisclosed. */
const BLUE_NILE = {
  template: 'a_aid=o3pbbkxavl0np&utm_source=pap&utm_medium=affiliates',   /* approved 2026-09-15; parameter form, appended to any bluenile.com URL */
  /* Blue Nile's October 2026 redesign renamed two shape values and silently DROPS an
     unrecognised one from the query string — the link still returns 200, it just lands
     on an unfiltered search. Pear and Heart are '-shaped'; the other eight stay '-cut'.
     Verified by clicking each shape in their own filter panel and reading the URL. */
  shape:   {Round:'round-cut', Oval:'oval-cut', Princess:'princess-cut', Cushion:'cushion-cut',
            Emerald:'emerald-cut', Pear:'pear-shaped', Marquise:'marquise-cut', Radiant:'radiant-cut',
            Asscher:'asscher-cut', Heart:'heart-shaped'},
  colors:  ['K','J','I','H','G','F','E','D'],
  clarity: ['SI2','SI1','VS2','VS1','VVS2','VVS1','IF','FL'],

  /* Stones matching a page's spec: this color and better, this clarity and better,
     a carat window from 5% under (the value stones just below a round number) to 10% over. */
  search(o){
    const q = new URLSearchParams();
    q.set('Shape', this.shape[o.shape] || 'round-cut');
    const ct = parseFloat(o.carat) || 1;
    q.set('CaratFrom', (ct * 0.95).toFixed(2)); q.set('CaratTo', (ct * 1.10).toFixed(2));
    const ci = this.colors.indexOf(o.color || 'G');   if(ci >= 0) q.set('Color',   this.colors.slice(ci).join(','));
    const li = this.clarity.indexOf(o.clarity || 'VS2'); if(li >= 0) q.set('Clarity', this.clarity.slice(li).join(','));
    const path = o.lab ? '/diamonds/lab-grown-diamonds' : '/diamonds';
    return this.wrap('https://www.bluenile.com' + path + '?' + q.toString());
  },
  /* The designed partner module: one card, same everywhere a buying decision is being made.
     Natural and lab-grown side by side, the spec spelled out, the disclosure on the card. */
  card(o, opts){
    const x = opts || {};
    const spec = `${(+o.carat).toFixed(2)} ct ${String(o.shape||'Round').toLowerCase()}${o.color?' · '+o.color:''}${o.clarity?' · '+o.clarity+' and up':''}`;
    const nat = this.search(Object.assign({}, o, {lab:false})), lab = this.search(Object.assign({}, o, {lab:true}));
    return `<div class="bn-card">
      <div class="bn-head">
        <div><div class="bn-eyebrow">Shop this specification</div>
          <div class="bn-title">${x.title || 'Real stones matching ' + spec}</div>
          <div class="bn-sub">${x.sub || 'Blue Nile — the largest online inventory, every stone graded and photographed. Filtered to this spec so you land on the right stones.'}</div></div>
        <div class="bn-logo" aria-hidden="true">Blue&nbsp;Nile</div>
      </div>
      <div class="bn-actions">
        <a href="${nat}" data-bn-item="1" target="_blank" rel="sponsored noopener noreferrer" class="btn btn-gold">${x.natLabel || 'Natural '+(+o.carat).toFixed(2)+' ct '+String(o.shape||'round').toLowerCase()+' →'}</a>
        <a href="${lab}" data-bn-item="1" target="_blank" rel="sponsored noopener noreferrer" class="btn btn-ghost">${x.labLabel || 'Lab-grown, same spec →'}</a>
        ${(x.extra||[]).map(e=>`<a href="${this.search(e.spec)}" data-bn-item="1" target="_blank" rel="sponsored noopener noreferrer" class="btn ${e.gold?'btn-gold':'btn-ghost'}">${e.label}</a>`).join('')}
      </div>
      <p class="bn-disc">Links to Blue Nile earn CaratBase a commission if you buy. It costs you nothing and does not change the figures on this page.</p>
    </div>`;
  },

  /* The compact co-branded row — used wherever a single spec has a single destination:
     the value, budget and size tools and the generated diamond pages. */
  button(o, label, opts){
    const x = opts || {};
    const url = this.search(o);
    const grade = [o.color ? o.color + ' color and up' : null, o.clarity ? o.clarity + ' and up' : null].filter(Boolean).join(', ');
    const sub = x.sub || `${o.lab ? 'Lab-grown' : 'Natural'}${grade ? ' · ' + grade : ''} · filtered at Blue Nile`;
    return `<a href="${url}" target="_blank" rel="sponsored noopener noreferrer" data-bn-item="1" class="bn-cta${x.small ? ' sm' : ''}">
      <span class="bn-mark">Blue Nile</span><span class="bn-txt"><b>${label}</b><small>${sub}</small></span><span class="bn-arrow">→</span></a>`;
  },
  note(){ return '<p class="bn-note bn-disc">Links to Blue Nile earn CaratBase a commission if you buy. It costs you nothing and does not change the figures on this page.</p>'; },
  wrap(url){
    if(!this.template) return url;
    if(this.template.includes('{url}')) return this.template.replace('{url}', encodeURIComponent(url));
    if(url.includes('a_aid=')) return url;
    return url + (url.includes('?') ? '&' : '?') + this.template;
  },
  active(){ return !!this.template; }
};

/* Display advertising. Left off until there is enough traffic to be accepted, and until
   ads would not be the most valuable thing in the space they occupy. */
const ADS = {
  adsense:  {client:'', enabled:false},
  provider: 'none'          /* 'adsense' | 'raptive' | 'mediavine' | 'none' */
};


/* ---------- Promotions ----------
   Heath's note was: no banners, but find a way to mention a sale in the text. So these
   render as one line of prose where a buying decision is already being made, and nowhere
   else — same rule as the rest of the Blue Nile placement.

   Every entry carries an end date and simply stops rendering after it. That is the whole
   point: a promo line is only an asset while it is true, and a site that still advertises
   a sale that ended three weeks ago looks worse than one that never mentioned it. Nothing
   has to be remembered or cleaned up.

   `where` is the page context, passed by whoever mounts it. */
const PROMOS = [
  {
    id: 'fall-edit', priority: 2, from: '2026-10-05', to: '2026-10-19',
    where: ['diamond', 'budget'],
    text: 'Blue Nile has <strong>30% off selected diamonds</strong> until 19 October.',
    cta: 'See what is included',
    url: 'https://www.bluenile.com/jewelry/todays-jewelry-deals'
  },
  {
    id: 'engagement-gwp', priority: 1, from: '2026-10-05', to: '2026-10-19',
    where: ['budget', 'engagement'],
    text: 'Until 19 October, Blue Nile add a <strong>diamond pendant free</strong> on engagement rings over $1,500, '
        + 'and <strong>diamond studs</strong> as well over $10,000.',
    cta: 'See the terms',
    url: 'https://www.bluenile.com/engagement-rings'
  },
  {
    id: 'james-allen', priority: 3, from: '2026-10-05', to: '2026-10-19',
    where: ['diamond', 'budget'],
    text: 'The James Allen collection is <strong>up to 50% off</strong> at Blue Nile until 19 October.',
    cta: 'See the collection',
    url: 'https://www.bluenile.com/jewelry/by-james-allen?isOnSale=yes'
  },
  {
    id: 'royal-asscher', priority: 1, from: '2026-10-05', to: '2026-12-31',
    where: ['shape-asscher'],
    text: 'Blue Nile now carry <strong>Royal Asscher</strong>, cut by the family that patented the shape in 1902.',
    cta: 'See the collection',
    url: 'https://www.bluenile.com/jewelry/collections/royal-asscher'
  }
];

/* ---------- helpers ---------- */
const Partners = {
  link(p){ return p.aff || p.url; },
  isAffiliate(p){ return !!p.aff; },
  anyAffiliate(){
    return Object.values(PARTNERS).flat().some(p => p && p.aff) || BLUE_NILE.active();
  },

  /* Generated diamond pages carry plain Blue Nile links as <a data-bn='{"shape":…}'>. When
     the program is switched on, rewrite them to tracked links, mark them sponsored, and
     add the disclosure — all from this one file, no page rebuild. */
  upgradeDeepLinks(){
    const links = document.querySelectorAll('a[data-bn], a[data-bn-item]');
    if(!links.length) return;
    links.forEach(a => {
      a.addEventListener('click', () => { if(window.cbTrack) cbTrack('partner_click',
        {partner:'Blue Nile', group:'deeplink', page:location.pathname}); });
      if(!BLUE_NILE.active()) return;
      if(a.dataset.bn){ try { a.href = BLUE_NILE.search(JSON.parse(a.dataset.bn)); } catch {} }
      else if(!a.href.includes('affiliates.r2net.com')) a.href = BLUE_NILE.wrap(a.href);
      a.rel = 'sponsored noopener noreferrer';
    });
    if(BLUE_NILE.active() && !document.querySelector('.bn-disclosure, .bn-disc')){
      const last = links[links.length - 1];
      last.insertAdjacentHTML('afterend', this.note());
    }
  },

  /* A block of options, never a single "best" one. The spread between buyers is the
     advice; sending everyone to one partner would be the opposite of the site's point. */
  render(group, opts){
    const list = PARTNERS[group] || [];
    if(!list.length) return '';
    const o = opts || {};
    const rows = list.map(p => `
      <a class="partner" href="${this.link(p)}" target="_blank"
         rel="${this.isAffiliate(p) ? 'sponsored noopener noreferrer' : 'noopener noreferrer'}"
         data-partner="${p.name}" data-group="${group}">
        <div class="partner-body">
          <div class="partner-name">${p.name}</div>
          <div class="partner-note">${p.note}</div>
        </div>
        <span class="partner-go">Visit →</span>
      </a>`).join('');

    return `<div class="partner-block">
      ${o.title ? `<h3 style="font-size:19px;margin-bottom:6px">${o.title}</h3>` : ''}
      ${o.intro ? `<p class="small" style="margin-bottom:14px">${o.intro}</p>` : ''}
      ${rows}
      ${o.footer ? `<p class="small" style="margin-top:12px">${o.footer}</p>` : ''}
      ${this.disclosure(group)}
    </div>`;
  },

  /* Shown only when a link in that group actually earns. Disclosure is a legal
     requirement where it applies, and silence would be dishonest where it does. */
  disclosure(group){
    const list = PARTNERS[group] || [];
    if(!list.some(p => p.aff)) return '';
    return `<p class="small" style="margin-top:12px;padding-top:10px;
      border-top:1px solid var(--line)">Some links above earn CaratBase a commission if you
      buy. It costs you nothing and does not change what we recommend — every option here
      would be listed either way.</p>`;
  },

  /* Live promotions for one page context, as a line of prose. Returns '' when there is
     nothing running, so a page that mounts it simply shows nothing out of season. */
  promos(where){
    const today = new Date().toISOString().slice(0, 10);
    return PROMOS
      .filter(p => p.where.indexOf(where) !== -1 && p.from <= today && today <= p.to)
      .sort((a, b) => (a.priority || 9) - (b.priority || 9));
  },

  mountPromo(el, where){
    const node = typeof el === 'string' ? document.getElementById(el) : el;
    if(!node) return;
    const live = this.promos(where).slice(0, 1);
    if(!live.length){ node.innerHTML = ''; return; }
    node.innerHTML = live.map(p => {
      const href = BLUE_NILE.active() ? BLUE_NILE.wrap(p.url) : p.url;
      return `<p class="bn-promo"><span class="bn-promo-tag">Offer</span> ${p.text}
        <a href="${href}" data-bn-item="1" target="_blank"
           rel="sponsored noopener noreferrer" data-promo="${p.id}">${p.cta} &rarr;</a></p>`;
    }).join('');
    node.querySelectorAll('[data-promo]').forEach(a =>
      a.addEventListener('click', () => {
        if(window.cbTrack) cbTrack('promo_click',
          {promo: a.dataset.promo, page: location.pathname});
      }));
  },

  /* Mount into a container and record clicks, so we learn which routes actually pay. */
  mount(el, group, opts){
    const node = typeof el === 'string' ? document.getElementById(el) : el;
    if(!node) return;
    node.innerHTML = this.render(group, opts);
    node.querySelectorAll('[data-partner]').forEach(a =>
      a.addEventListener('click', () => {
        if(window.cbTrack) cbTrack('partner_click',
          {partner:a.dataset.partner, group:a.dataset.group, page:location.pathname});
      }));
  },

  /* Ad slot. Renders nothing at all until a provider is configured — an empty gray box
     labeled "advertisement" is worse than no box. */
  adSlot(){
    if(!ADS.adsense.enabled || !ADS.adsense.client) return '';
    return `<ins class="adsbygoogle" style="display:block"
      data-ad-client="${ADS.adsense.client}" data-ad-format="auto"
      data-full-width-responsive="true"></ins>`;
  }
};

if(typeof document !== 'undefined') document.addEventListener('DOMContentLoaded', () => Partners.upgradeDeepLinks());

/* `const` at the top level of a classic script creates a script-scope binding, not a
   window property, so `if (window.Partners)` guards were always false and the partner
   blocks they protected never mounted. Export both explicitly. */
window.BLUE_NILE = BLUE_NILE;
window.Partners  = Partners;
