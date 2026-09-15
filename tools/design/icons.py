"""Inline SVG micro-illustrations for the tool cards. One source, used by index.html and tools.html."""
import math
_ring12 = ''.join(f'<circle cx="{round(30*math.cos(i*0.5236),1)}" cy="{round(30*math.sin(i*0.5236),1)}" r="5.5" fill="{c}" stroke="#8A6420" opacity=".9"/>'
                  for i,c in enumerate(['#B22222','#9966CC','#7FFFD4','#F5F5F5','#50C878','#F0E4D0','#E0115F','#9ACD32','#0F52BA','#FF7F50','#FFC87C','#40E0D0']))
ICO = {
 'diamond': '<svg viewBox="0 0 96 96" fill="none" stroke="#8A6420" stroke-width="1.6" stroke-linejoin="round"><polygon points="66,64 48,70 30,64 22,48 30,32 48,26 66,32 74,48" fill="#F6EFDE"/><polygon points="57,53 48,56 39,53 35,48 39,43 48,40 57,43 61,48" fill="#fff"/><path d="M22 48h13M61 48h13M30 32l9 11M66 32l-9 11M30 64l9-11M66 64l-9 11M48 26v14M48 56v14"/></svg>',
 'gems': '<svg viewBox="0 0 96 96" fill="none" stroke-width="1.5"><ellipse cx="30" cy="52" rx="14" ry="18" fill="#C9484A" stroke="#7A1F22"/><ellipse cx="60" cy="40" rx="15" ry="19" fill="#2F5FA8" stroke="#1B3A6B"/><ellipse cx="66" cy="66" rx="12" ry="14" fill="#2E8B57" stroke="#1B5E3A"/><path d="M24 40l6-6M54 26l6-6" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".8"/></svg>',
 'gold': '<svg viewBox="0 0 96 96" fill="none"><path d="M14 70 30 50l14 12 16-24 22 16" stroke="#8A6420" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M26 82h44l-6-14H32z" fill="#D8BA76" stroke="#8A6420" stroke-width="1.4"/></svg>',
 'stamp': '<svg viewBox="0 0 96 96" fill="none"><circle cx="48" cy="52" r="26" stroke="#8A6420" stroke-width="7"/><circle cx="48" cy="52" r="26" stroke="#E3C88A" stroke-width="3"/><rect x="34" y="46" width="28" height="12" rx="2" fill="#fff" stroke="#8A6420" stroke-width="1"/><text x="48" y="55.5" font-family="Inter,system-ui" font-size="8.5" font-weight="700" text-anchor="middle" fill="#8A6420">925</text></svg>',
 'vault': '<svg viewBox="0 0 96 96" fill="none" stroke="#8A6420" stroke-width="1.6"><rect x="18" y="22" width="60" height="56" rx="8" fill="#F6EFDE"/><circle cx="48" cy="50" r="13" fill="#fff"/><circle cx="48" cy="50" r="4" fill="#C9A961"/><path d="M48 37v-5M48 68v-5M35 50h-5M66 50h-5"/></svg>',
 'budget': '<svg viewBox="0 0 96 96" fill="none" stroke="#8A6420" stroke-width="1.5"><circle cx="24" cy="62" r="8" fill="#F6EFDE"/><circle cx="46" cy="58" r="12" fill="#F6EFDE"/><circle cx="74" cy="52" r="17" fill="#F6EFDE"/><path d="M14 80h68" stroke-linecap="round"/><text x="48" y="26" font-family="Inter,system-ui" font-size="9" text-anchor="middle" fill="#8A6420">same money</text></svg>',
 'compare': '<svg viewBox="0 0 96 96" fill="none" stroke="#8A6420" stroke-width="1.5" stroke-linejoin="round"><polygon points="36,56 26,60 16,56 12,48 16,40 26,36 36,40 40,48" fill="#F6EFDE"/><polygon points="84,58 70,64 56,58 50,48 56,38 70,32 84,38 90,48" fill="#F6EFDE"/><path d="M12 76h28M50 76h40" stroke="#C9A961"/><text x="46" y="51" font-family="Inter" font-size="10" text-anchor="middle" fill="#8A6420">vs</text></svg>',
 'lab': '<svg viewBox="0 0 96 96" fill="none" stroke-width="1.5" stroke-linejoin="round"><polygon points="42,52 30,56 18,52 14,44 18,36 30,32 42,36 46,44" fill="#F6EFDE" stroke="#8A6420"/><polygon points="82,52 70,56 58,52 54,44 58,36 70,32 82,36 86,44" fill="#E6F2F6" stroke="#2B7189"/><text x="30" y="72" font-family="Inter,system-ui" font-size="8" text-anchor="middle" fill="#8A6420">natural</text><text x="70" y="72" font-family="Inter,system-ui" font-size="8" text-anchor="middle" fill="#2B7189">lab</text></svg>',
 'ppc': '<svg viewBox="0 0 96 96" fill="none" stroke="#8A6420" stroke-width="1.8" stroke-linecap="round"><path d="M14 74h68M14 74V20"/><path d="M18 66c14-2 22-6 26-14s8-14 16-18 12-6 18-6" stroke="#C9A961" stroke-width="2.4"/><path d="M44 52v-6M60 34v-6" stroke="#B0413B" stroke-width="2"/></svg>',
 'color': '<svg viewBox="0 0 96 96" fill="none"><rect x="12" y="34" width="12" height="28" fill="#fff" stroke="#C9C2B4"/><rect x="26" y="34" width="12" height="28" fill="#FCFBF6" stroke="#C9C2B4"/><rect x="40" y="34" width="12" height="28" fill="#F9F5E6" stroke="#C9C2B4"/><rect x="54" y="34" width="12" height="28" fill="#F5EDD2" stroke="#C9C2B4"/><rect x="68" y="34" width="12" height="28" fill="#F0E3BD" stroke="#C9C2B4"/><text x="18" y="76" font-family="Inter" font-size="8" text-anchor="middle" fill="#8A6420">D</text><text x="74" y="76" font-family="Inter" font-size="8" text-anchor="middle" fill="#8A6420">K</text></svg>',
 'clarity': '<svg viewBox="0 0 96 96" fill="none" stroke="#8A6420" stroke-width="1.5"><circle cx="48" cy="48" r="26" fill="#F6EFDE"/><circle cx="48" cy="48" r="16" fill="#fff"/><circle cx="42" cy="44" r="1.4" fill="#8A6420" stroke="none"/><circle cx="53" cy="52" r="1" fill="#8A6420" stroke="none"/><path d="M68 68l12 12" stroke-width="3" stroke-linecap="round"/></svg>',
 'ring': '<svg viewBox="0 0 96 96" fill="none" stroke="#8A6420" stroke-width="1.4"><circle cx="48" cy="50" r="30" stroke-dasharray="2 3"/><circle cx="48" cy="50" r="22"/><circle cx="48" cy="50" r="14" stroke-dasharray="2 3"/><rect x="58" y="66" width="30" height="19" rx="2.5" fill="#2E3440" stroke="none"/><rect x="62" y="71" width="8" height="6" rx="1" fill="#D8BA76"/></svg>',
 'photo': '<svg viewBox="0 0 96 96" fill="none" stroke="#8A6420" stroke-width="1.5"><rect x="14" y="26" width="68" height="48" rx="6" fill="#F6EFDE"/><path d="M36 26l4-6h16l4 6"/><rect x="22" y="52" width="26" height="16" rx="2" fill="#2E3440" stroke="none"/><circle cx="64" cy="52" r="9" stroke="#8A6420" stroke-width="3.5"/></svg>',
 'size': '<svg viewBox="0 0 96 96" fill="none" stroke="#8A6420" stroke-width="1.4"><circle cx="20" cy="60" r="6" fill="#F6EFDE"/><circle cx="38" cy="60" r="8" fill="#F6EFDE"/><circle cx="60" cy="60" r="10" fill="#F6EFDE"/><circle cx="84" cy="60" r="12" fill="#F6EFDE" stroke-width="1.6"/><text x="20" y="82" font-family="Inter" font-size="7.5" text-anchor="middle" fill="#8A6420">.5</text><text x="38" y="82" font-family="Inter" font-size="7.5" text-anchor="middle" fill="#8A6420">1</text><text x="60" y="82" font-family="Inter" font-size="7.5" text-anchor="middle" fill="#8A6420">2</text><text x="84" y="82" font-family="Inter" font-size="7.5" text-anchor="middle" fill="#8A6420">3</text></svg>',
 'engage': '<svg viewBox="0 0 96 96" fill="none" stroke="#8A6420" stroke-width="1.6"><circle cx="48" cy="58" r="20"/><polygon points="48,22 56,32 48,44 40,32" fill="#F6EFDE" stroke-linejoin="round"/><path d="M40 32h16"/><text x="48" y="90" font-family="Inter" font-size="8" text-anchor="middle" fill="#8A6420">how much?</text></svg>',
 'insure': '<svg viewBox="0 0 96 96" fill="none" stroke="#8A6420" stroke-width="1.6" stroke-linejoin="round"><path d="M48 16l26 10v22c0 16-11 26-26 32-15-6-26-16-26-32V26z" fill="#F6EFDE"/><polygon points="48,36 56,44 48,56 40,44" fill="#fff"/></svg>',
 'birth': '<svg viewBox="0 0 96 96" fill="none" stroke-width="1.2"><g transform="translate(48 48)">' + _ring12 + '</g><text x="48" y="52" font-family="Inter" font-size="8" text-anchor="middle" fill="#8A6420">12</text></svg>',
 'widget': '<svg viewBox="0 0 96 96" fill="none" stroke="#8A6420" stroke-width="1.5"><rect x="14" y="20" width="68" height="50" rx="6" fill="#F6EFDE"/><rect x="24" y="30" width="48" height="30" rx="4" fill="#fff"/><path d="M34 40h28M34 48h18" stroke="#C9A961" stroke-width="2"/><path d="M40 80h16" stroke-linecap="round"/></svg>',
}
def card(href, key, h3, p, go, hero=False):
    return (f'<a href="{href}" class="tool2{" hero-card" if hero else ""}"><div><h3>{h3}</h3><p>{p}</p>'
            f'<span class="go">{go} →</span></div><div class="vis">{ICO[key]}</div></a>')

FAMILIES = [
 ('Value what you own', 'Retail, and the honest resale figure.', [
   ('value.html','diamond','Value my diamond &amp; jewellery','Centre stone, side stones and the metal, priced as a whole piece — the retail figure a jeweller would charge and the resale range you would actually be offered.','Start a valuation', True),
   ('gemstone.html','gems','Gemstones &amp; pearls','Ruby, sapphire, emerald, tanzanite and more. Treatment matters more than size, and this shows you by how much.','Value a gemstone', False),
   ('metals.html','gold','Gold &amp; metal prices','Live spot per gram, every karat, and what a scrap buyer will really offer.',"Today's prices", False),
   ('stamp.html','stamp','Hallmark lookup','925, 750, 585, GF, EPNS — what the stamp inside the band means, and whether there is any metal value.','Decode a stamp', False),
   ('vault.html','vault','My vault','Every piece you value, saved on your own device, with a running total as prices move.','Open my vault', False)]),
 ('Buy the right stone', 'Before the counter, not after.', [
   ('budget.html','budget','What my budget buys','Enter what you want to spend and see the biggest stone it buys — four ways, side by side, with resale.','See what it buys', False),
   ('compare.html','compare','Compare two diamonds','Two specs side by side: true size, price, resale, price per carat, and which is the better buy.','Compare', False),
   ('lab-vs-natural.html','lab','Lab-grown vs natural','The same stone both ways — what each costs today, and what each is worth in five years.','See both', False),
   ('engagement-ring-budget.html','engage','How much to spend on a ring','There is no rule. What your income actually supports, and what that money buys.','Work it out', False),
   ('diamond-price-per-carat.html','ppc','Diamond price per carat','Why a 1 carat stone costs far more than two half carats — the whole curve, with the cliffs.','See the chart', False),
   ('diamond-color-chart.html','color','Diamond colour chart','D to K on the same 1 carat stone: what you can see, and what each step costs.','See the scale', False),
   ('diamond-clarity-chart.html','clarity','Diamond clarity chart','FL to I1: what is visible to the eye, what needs a loupe, and the price of each grade.','See the grades', False)]),
 ('Measure it', 'No ruler, no scales, no appointment.', [
   ('ring-size.html','ring','Ring sizer','Four ways to measure, including circles drawn true to life on your screen, calibrated against any bank card.','Find my size', False),
   ('measure.html','photo','Measure from a photo','Photograph your ring beside a bank card and get its true size in millimetres — corrected for camera angle.','Measure from a photo', False),
   ('size.html','size','Carat size chart','What a carat actually looks like: true millimetre sizes for every weight and shape, drawn on a finger.','See the sizes', False)]),
 ('Reference', 'The answers people look up most.', [
   ('birthstones.html','birth','Birthstones by month',"Every month's stone, what it is worth, and the honest alternative when the classic is out of reach.",'See all twelve', False),
   ('insurance-cost.html','insure','Jewellery insurance cost','What cover should cost for a piece of your value, and when it is not worth insuring at all.','Estimate it', False),
   ('diamond/','diamond','Diamond sizes &amp; prices','Every carat weight in every shape — 110 pages of size, price by grade, and resale.','Browse', False),
   ('ring-size/','ring','Ring size charts','Every size in US, UK, EU, India and Japan with diameter and circumference.','All sizes', False),
   ('hallmark/','stamp','Hallmarks explained','All 27 marks: metal, purity, and whether the piece is worth anything by weight.','All marks', False),
   ('widgets.html','widget','Free widgets for your site',"Ring sizer, diamond size chart and gold calculator for any jeweller's website. Two lines of code.",'Get the code', False)]),
]
def families_html():
    out = []
    for title, sub, cards in FAMILIES:
        out.append(f'<div class="family"><div class="family-head"><h2>{title}</h2><p>{sub}</p></div><div class="tool-grid2">'
                   + ''.join(card(*c) for c in cards) + '</div></div>')
    return '\n'.join(out)
