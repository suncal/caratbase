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
    {name:'Blue Nile',       url:'https://www.bluenile.com',      aff:'',
     note:'The largest online inventory. 5% commission, 45-day cookie, capped at $7,500 orders.'},
    {name:'James Allen',     url:'https://www.jamesallen.com',    aff:'',
     note:'360-degree video on every stone, which is the closest thing to seeing it in person. 5%, 60-day cookie.'},
    {name:'Brilliant Earth', url:'https://www.brilliantearth.com',aff:'',
     note:'Traceable sourcing. 5% on bridal, 7% on fine jewellery, 30-day cookie.'}
  ],

  /* People who OWN it — valuation, vault. The highest-converting money event we have,
     and the only one that renews every year. */
  insurance: [
    {name:'BriteCo',         url:'https://brite.co',              aff:'',
     note:'Jewellery-specific cover, $0 deductible. Gives its appraisal software to jewellers free, funded by referrals — which tells you what a referral is worth.'},
    {name:'Jewelers Mutual', url:'https://www.jewelersmutual.com',aff:'',
     note:'The oldest specialist jewellery insurer in the US. $0 deductible.'}
  ],

  /* People SELLING. Never one buyer — the spread between them is the whole point. */
  buyers: [
    {name:'Worthy',          url:'https://www.worthy.com',        aff:'',
     note:'Auctions your piece to a network of dealers, so buyers compete. 18% commission, 2–4 weeks.'},
    {name:'myGemma',         url:'https://www.mygemma.com',       aff:'',
     note:'Formerly WP Diamonds. Direct offer rather than auction — faster, usually lower.'},
    {name:'Diamond Banc',    url:'https://diamondbanc.com',       aff:'',
     note:'Buys outright and also lends against jewellery if you want it back.'}
  ],

  /* Scrap gold and silver. */
  metalBuyers: [
    {name:'CashforGoldUSA',  url:'https://cashforgoldusa.com',    aff:'',
     note:'Insured shipping, pays on approval. Compare its offer against the figure above before accepting.'}
  ],

  /* Coloured stones — a report is often worth more than it costs. Not affiliate; these
     are simply the right places to send someone. */
  labs: [
    {name:'GIA',             url:'https://www.gia.edu/gem-lab-service/identification-report', aff:'',
     note:'Identification and treatment reports. The most widely recognised name in the trade.'},
    {name:'AGL',             url:'https://www.aglgemlab.com',     aff:'',
     note:'American Gemological Laboratories — the specialist most respected for coloured stone origin.'}
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

/* Display advertising. Left off until there is enough traffic to be accepted, and until
   ads would not be the most valuable thing in the space they occupy. */
const ADS = {
  adsense:  {client:'', enabled:false},
  provider: 'none'          /* 'adsense' | 'raptive' | 'mediavine' | 'none' */
};

/* ---------- helpers ---------- */
const Partners = {
  link(p){ return p.aff || p.url; },
  isAffiliate(p){ return !!p.aff; },
  anyAffiliate(){
    return Object.values(PARTNERS).flat().some(p => p && p.aff);
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

  /* Ad slot. Renders nothing at all until a provider is configured — an empty grey box
     labelled "advertisement" is worse than no box. */
  adSlot(){
    if(!ADS.adsense.enabled || !ADS.adsense.client) return '';
    return `<ins class="adsbygoogle" style="display:block"
      data-ad-client="${ADS.adsense.client}" data-ad-format="auto"
      data-full-width-responsive="true"></ins>`;
  }
};
