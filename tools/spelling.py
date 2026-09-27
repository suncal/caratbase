"""US spelling across the site's source files. Whole words, case preserved. Run, then
regenerate pages. Reports counts; --check only reports."""
import pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
MAP = {
 'jewellery':'jewelry','jeweller':'jeweler','jewellers':'jewelers',"jeweller's":"jeweler's","jewellers'":"jewelers'",
 'colour':'color','colours':'colors','colourless':'colorless','coloured':'colored','colouring':'coloring','discolour':'discolor',
 'centre':'center','centres':'centers','centred':'centered','grey':'gray','greys':'grays','catalogue':'catalog','favourite':'favorite',
 'honour':'honor','millimetre':'millimeter','millimetres':'millimeters','metre':'meter','metres':'meters','licence':'license',
 'organisation':'organization','recognise':'recognize','recognised':'recognized','recognises':'recognizes','standardised':'standardized',
 'prioritise':'prioritize','specialise':'specialize','realise':'realize','minimise':'minimize','maximise':'maximize',
 'analyse':'analyze','travelled':'traveled','jewelled':'jeweled','modelled':'modeled','cancelled':'canceled','labelled':'labeled',
 'programme':'program','defence':'defense','offence':'offense','whilst':'while','learnt':'learned','authorised':'authorized',
 'customise':'customize','enquire':'inquire','enquiries':'inquiries','fibre':'fiber','litre':'liter','neighbour':'neighbor','neighbours':'neighbors',
 'behaviour':'behavior','flavour':'flavor','humour':'humor','labour':'labor','savour':'savor','theatre':'theater','sombre':'somber','calibre':'caliber',
 'apologise':'apologize','summarise':'summarize','capitalise':'capitalize','optimise':'optimize','optimised':'optimized','normalise':'normalize','normalised':'normalized',
 'practise':'practice','aluminium':'aluminum','mould':'mold','tonne':'ton','kerb':'curb','pyjamas':'pajamas','cosy':'cozy','plough':'plow','draught':'draft',
 'favour':'favor','favours':'favors','favoured':'favored','favouring':'favoring','favourable':'favorable','favourably':'favorably','favourites':'favorites',
 'behaviours':'behaviors','flavours':'flavors','honours':'honors','labours':'labors','licences':'licenses','defences':'defenses',
 'organise':'organize','organised':'organized','organises':'organizes','organisations':'organizations','authorise':'authorize','authorises':'authorizes',
 'specialised':'specialized','specialises':'specializes','realised':'realized','realises':'realizes','minimised':'minimized','maximised':'maximized',
 'analysed':'analyzed','analysing':'analyzing','paralyse':'paralyze','summarised':'summarized','prioritised':'prioritized','customised':'customized',
 'dialogue':'dialog','travelling':'traveling','labelling':'labeling','modelling':'modeling','cancelling':'canceling','fuelled':'fueled',
 'amongst':'among','spelt':'spelled','fulfil':'fulfill','instalment':'installment','skilful':'skillful','marvellous':'marvelous',
 'speciality':'specialty','specialities':'specialties','cheque':'check','cheques':'checks','storey':'story','practising':'practicing',
 'vapour':'vapor','odour':'odor','armour':'armor','rumour':'rumor','valour':'valor','vigour':'vigor','harbour':'harbor','parlour':'parlor',
 'splendour':'splendor','endeavour':'endeavor','tumour':'tumor','pretence':'pretense','sceptical':'skeptical','manoeuvre':'maneuver',
}
FILES = [p for p in ROOT.glob('*.html') if p.name != 'dashboard.html'] + list(ROOT.glob('assets/*.js')) + list(ROOT.glob('*.js')) + list(ROOT.glob('worker/*.js')) + \
        [ROOT/'tools/genpages.py'] + list((ROOT/'tools/design').glob('*.py')) + list((ROOT/'tools/outreach').glob('*.md')) + list((ROOT/'tools/outreach').glob('*.py')) + \
        [ROOT/'tools/feed/build_picks.py', ROOT/'README.md'] + list(ROOT.glob('embed/*/index.html'))
PAT = re.compile(r"\b(" + "|".join(re.escape(k) for k in sorted(MAP, key=len, reverse=True)) + r")\b", re.I)
def fix(m):
    w = m.group(0); r = MAP[w.lower()]
    if w.isupper(): return r.upper()
    if w[0].isupper(): return r[0].upper() + r[1:]
    return r
check = '--check' in sys.argv
tot = 0
for f in FILES:
    s = f.read_text(); n = len(PAT.findall(s))
    if not n: continue
    tot += n
    if check: print(f'{n:4d}  {f.relative_to(ROOT)}')
    else: f.write_text(PAT.sub(fix, s)); print(f'{n:4d}  {f.relative_to(ROOT)}')
print('total', tot, 'occurrences', '(check only)' if check else 'converted')
