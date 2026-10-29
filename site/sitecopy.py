"""Namaste Jewelry Shop (namastejewelryshop.com): sterling silver and finer gemstone pieces. All copy is written for this site only."""
import re, collections
from copybase import E, stone_color, intent_color, kinds_phrase, kind_one, plist, tradition, hood_list, HOODS as HOOD_DATA

AISLES = {
 'ring':      ('Sterling Silver Rings', 'Rings', 'sterling-silver-rings', 'Solid .925 rings set with gemstones, sold size by size, plus plain bands.', '#9aa3ae'),
 'pendant':   ('Sterling Silver Pendants', 'Pendants', 'sterling-silver-pendants', 'Bezel, claw and wire-set gemstone pendants in .925 silver.', '#6d7a8a'),
 'chain':     ('Chains & Necklaces', 'Chains', 'sterling-silver-chains', 'Box, rope, snake, Franco and Cuban link chains by length, and finished sterling necklaces.', '#3d4652'),
 'earrings':  ('Sterling Silver Earrings', 'Earrings', 'sterling-silver-earrings', 'Gemstone studs, drops and hoops in sterling.', '#8c96a3'),
 'bracelet':  ('Bracelets & Anklets', 'Bracelets', 'sterling-silver-bracelets', 'Sterling link, chip and gemstone bracelets, plus anklets.', '#b0b7c0'),
 'collector': ('Collector Stones', 'Collector', 'collector-gemstone-jewelry', 'Pieces from $150: moldavite, opal, rare and larger stones in sterling.', '#b08a3e'),
}
def assign(x):
    if x['base'] in ('meditation', 'beads', 'charm'): return None
    fine = x['metal'] == 'Sterling silver' or (x['metal'] == 'Gold-tone & gold-plated' and x['price'] >= 40)
    if not fine: return None
    if x['price'] >= 150: return 'collector'
    if x['base'] in ('ring',): return 'ring'
    if x['base'] == 'pendant': return 'pendant'
    if x['base'] in ('chain', 'necklace', 'mala'): return 'chain'
    if x['base'] == 'earrings': return 'earrings'
    return 'bracelet'
LABELS = {'stone': 'Gemstone', 'metal': 'Metal'}
PRICE_BANDS = [('0-40', 'Under $40'), ('40-80', '$40 to $80'), ('80-150', '$80 to $150'), ('150-300', '$150 to $300'), ('300-99999', '$300 and up')]
BRAND_BANDS = [('Under $50', 0, 50), ('$50 to $120', 50, 120), ('$120 and up', 120, 1e9)]
STONE_MIN = 5; INTENT_MIN = 5; NAV_INTENTS = False

VISIT_EYEBROW = 'Try it on at the counter'
def STORE_DESC(S): return f'Sterling silver and gemstone jewelry shop by Union Square in Manhattan with about {S.ABOUT_N:,} .925 rings, pendants, chains, earrings and bracelets.'
REVIEW_TITLE = 'Wearing something from 14th Street?'
REVIEW_TEXT = 'If the fit, the stone or the service was right, a Google review helps others looking for sterling silver jewelry near Union Square.'
LOGO_SVG = '<svg viewBox="0 0 40 40"><circle cx="20" cy="23" r="9" fill="none" stroke="currentColor" stroke-width="2.4"/><path d="M16 12l4-6 4 6-4 3z" fill="#c7ccd4"/></svg>'
WORDMARK = 'Namaste <b>Jewelry Shop</b>'
BAR_TEXT = 'Sterling silver at 2 West 14th Street'
SEARCH_PLACEHOLDER = 'Search sterling rings, pendants, chains, stones'
QUIZ = None

def FOOTER_EXPLORE(S):
    return [('Gemstones A to Z', '/stones/'), ('How to spot real sterling', '/guide/how-to-tell-real-sterling-silver/'), ('Chain length guide', '/guide/chain-length-guide/'),
            ('Ring sizes', '/guide/ring-sizing/'), ('Silver care', '/guide/sterling-silver-care/'), ('By intention', '/intentions/'), ('Sterling silver in Manhattan', '/sterling-silver-jewelry-nyc/')]
FOOT_BLURB = 'Sterling silver set with real gemstones, sized and priced online, and waiting at the counter on 14th Street.'
HERO_BASES = ('ring', 'pendant', 'earrings')
def HERO(S):
    return {'eyebrow': '.925 Sterling silver &middot; 2 West 14th Street, New York',
            'h1': 'Sterling silver, <em>set with real stones.</em>',
            'lede': f'{S.N:,} pieces in solid sterling and finer settings: gemstone rings in your size, claw and bezel pendants, chains by the inch and studs. From {S.money(S.MIN_PRICE)} to collector stones over $150. A few minutes from Union Square.' + (f' Reserve online; pickups are {S.READY.lower()}.' if S.PICKUP_ON else ''),
            'shop_cta': 'Shop sterling'}
def _stones(S):
    keys = [k for k in S.STONE_KEYS if k not in S.NON_STONE][:16]
    chips = ''.join(f'<a class="chip" href="/stones/{k}/">{E(S.STONE_NAME[k])} <small>{S.stone_any[k]}</small></a>' for k in keys)
    return f'<section class="wrap"><div class="sechead"><h2>By gemstone</h2><a href="/stones/">Gemstones A&ndash;Z &rarr;</a></div><div class="chips">{chips}</div></section>'
def _chains(S):
    lens = [(L, sum(1 for x in S.products if x['base'] == 'chain' and re.search(rf'\b{L}"', x['title']))) for L in (16, 18, 20, 22, 24, 30)]
    lens = [(L, n) for L, n in lens if n]
    if not lens: return ''
    return '<section class="wrap"><div class="sechead"><h2>Chains by length</h2><a href="/guide/chain-length-guide/">Which length? &rarr;</a></div><div class="chips">' + ''.join(f'<a class="chip" href="/chains/{L}-inch/">{L} inch <small>{n}</small></a>' for L, n in lens) + '</div></section>'
def _near(S): return f'<section class="wrap"><div class="sechead"><h2>Directions from your neighborhood</h2></div>{hood_list(S, "/near/")}</section>'
def _whys(S):
    return [('Solid .925 silver', 'Settings are sterling unless a listing says otherwise. Look for .925 in the title.'),
            ('Sized, not guessed', 'Each ring size is its own listing, so you see exactly which sizes are in stock.'),
            (('Reserve and collect', f'Choose Pickup at checkout and try it on when you collect. Orders are {S.READY.lower()}.') if S.PICKUP_ON else ('', '')),
            ('Chains to match', 'Sterling chains in several weaves and lengths, so a pendant leaves wearing the right one.'),
            ('Collector stones', 'Moldavite, opal and larger statement stones from $150.'),
            ('Open seven days', 'From 11 AM daily, until 8 PM Monday to Thursday, 9 PM Friday and Saturday and 7 PM Sunday.')]
def _best(S): return S.by_rank(S.leaders)[:8] if S.HAS_RANK else S.by_rank(S.leaders)[:8]
def _collector(S): return S.by_rank([x for x in S.leaders if x['aisle'] == 'collector' and not x['noimg']])[:4]
def _rings(S): return S.by_rank([x for x in S.leaders if x['aisle'] == 'ring' and not x['noimg']])[:8]
HOME_SECTIONS = [
 {'type': 'grid', 'title': 'Most wanted in sterling', 'select': _best, 'href': '/shop/', 'link': 'All sterling', 'intro': 'In the order they sell on namastebookshop.com, updated every morning.'},
 {'type': 'html', 'html': _stones},
 {'type': 'grid', 'title': 'Gemstone rings', 'select': _rings, 'href': '/shop/sterling-silver-rings/', 'link': 'Every size'},
 {'type': 'visit'},
 {'type': 'collections', 'title': 'Settings & styles', 'items': [
   {'title': 'Claw & prong set', 'blurb': 'Stones held by silver claws.', 'href': '/claw-set-gemstone-jewelry/', 'filter': {'q': 'claw|prong'}},
   {'title': 'Faceted gemstones', 'blurb': 'Cut stones that catch light.', 'href': '/faceted-gemstone-jewelry/', 'filter': {'style': ['Faceted & gemstone']}},
   {'title': 'Moldavite in sterling', 'blurb': 'Natural green tektite.', 'href': '/stones/moldavite/', 'filter': {'stone': ['moldavite']}},
   {'title': 'Plain silver bands', 'blurb': 'Stacking and everyday bands.', 'href': '/sterling-silver-bands/', 'filter': {'aisle': ['ring'], 'style': ['Bands & stacking']}},
   {'title': 'Wire-wrapped sterling', 'blurb': 'Hand-wrapped in .925 wire.', 'href': '/sterling-wire-wrapped-pendants/', 'filter': {'style': ['Wire wrapped']}},
   {'title': 'Collector stones', 'blurb': 'From $150.', 'href': '/shop/collector-gemstone-jewelry/', 'filter': {'aisle': ['collector']}}]},
 {'type': 'html', 'html': _chains},
 {'type': 'whys', 'title': 'The counter at 2 West 14th', 'items': _whys},
 {'type': 'grid', 'title': 'Collector stones', 'select': _collector, 'href': '/shop/collector-gemstone-jewelry/', 'link': 'See all'},
 {'type': 'brands', 'title': 'Silversmiths & makers', 'n': 10},
 {'type': 'html', 'html': _near},
 {'type': 'review'},
 {'type': 'band', 'title': 'Reserve now, try it on at pickup', 'text': lambda S: 'Every piece is a live listing. Reserve it, then see it in person on 14th Street, or have it shipped insured by the carrier options shown at checkout.',
  'steps': lambda S: [('Choose size and stone', 'Filter by gemstone, price, style and maker.'), ('Pick Pickup at checkout', f'Secure Shopify checkout. {S.READY or "Usually ready the same day"}.'), ('Collect it', S.STORE_ADDR + '.')]},
]
def HOME_TITLE(S): return 'Namaste Jewelry Shop | Sterling Silver Gemstone Jewelry, Union Square NYC'
def HOME_DESC(S): return f'{S.N:,} sterling silver gemstone rings, pendants, chains and earrings at {S.STORE_ADDR}, by Union Square. Rings by size, chains by length, collector stones. Pickup or ship.'
def SHOP_TITLE(S): return 'Shop Sterling Silver Gemstone Jewelry | Namaste Jewelry Shop NYC'
def SHOP_DESC(S): return f'{S.N:,} .925 sterling silver pieces with real gemstones, from {S.money(S.MIN_PRICE)}. Reserve online and pick up at 2 West 14th Street, Manhattan, or ship.'
SHOP_H1 = 'All sterling & fine jewelry'
def SHOP_SUB(S): return f'{S.N:,} pieces. Narrow by gemstone, style, maker and price.'
def AISLE_TITLE(S, k): return f'{AISLES[k][0]} in NYC | Namaste Jewelry Shop, Union Square'
def AISLE_DESC(S, k): return f'{AISLES[k][3]} {S.cat_count[k]} in stock at 2 West 14th Street. Try on at pickup or ship.'

def LANDINGS(S):
    L = [
     {'path': '/claw-set-gemstone-jewelry/', 'title': 'Claw Set Gemstone Jewelry in Sterling Silver | Namaste Jewelry Shop', 'desc': 'Claw and prong set gemstone rings and pendants in .925 sterling silver near Union Square, NYC.',
      'h1': 'Claw & prong set', 'sub': 'Open settings that let light reach the stone.', 'filter': {'q': 'claw|prong'}},
     {'path': '/faceted-gemstone-jewelry/', 'title': 'Faceted Gemstone Jewelry in Sterling | Namaste Jewelry Shop NYC', 'desc': 'Faceted topaz, garnet, amethyst, peridot and more in sterling settings at 2 West 14th Street.',
      'h1': 'Faceted gemstones', 'sub': 'Cut stones in sterling settings.', 'filter': {'style': ['Faceted & gemstone']}},
     {'path': '/sterling-silver-bands/', 'title': 'Sterling Silver Bands & Stacking Rings | Namaste Jewelry Shop', 'desc': 'Plain and domed sterling silver bands and stacking rings by size near Union Square.',
      'h1': 'Sterling bands & stacking rings', 'sub': 'Everyday bands, sized one per listing.', 'filter': {'aisle': ['ring'], 'style': ['Bands & stacking']}},
     {'path': '/sterling-wire-wrapped-pendants/', 'title': 'Sterling Wire Wrapped Pendants | Namaste Jewelry Shop NYC', 'desc': 'Gemstones hand-wrapped in sterling silver wire, at 2 West 14th Street, Manhattan.',
      'h1': 'Sterling wire-wrapped pendants', 'sub': 'Stones wrapped by hand in .925 wire.', 'filter': {'style': ['Wire wrapped']}},
    ]
    for Ln in (16, 18, 20, 22, 24, 30):
        L.append({'path': f'/chains/{Ln}-inch/', 'title': f'{Ln} Inch Sterling Silver Chains | Namaste Jewelry Shop NYC', 'desc': f'{Ln}-inch .925 sterling silver chains in box, rope, snake, Franco and Cuban link at 2 West 14th Street.',
                  'h1': f'{Ln}-inch chains', 'sub': f'Sterling chains that measure {Ln} inches.', 'filter': {'aisle': ['chain'], 'q': rf'\b{Ln}"'},
                  'intro': f'<p class="intro">{ {16: "Sits at the base of the neck on most people; a choker-adjacent length.", 18: "The most common pendant length; lands at or just below the collarbone.", 20: "A little below the collarbone; good for larger pendants.", 22: "Rests above the neckline of most tops.", 24: "A longer drop that sits around the top of the chest.", 30: "A long chain for layering or for wearing over clothes."}[Ln]} See the <a href="/guide/chain-length-guide/">chain length guide</a>.</p>'})
    return L

def stone_tile(S, k):
    xs = [x for x in S.products if k in x['stones']]
    return f'{S.money(min(x["price"] for x in xs))} to {S.money(max(x["price"] for x in xs))}'
def STONE_PAGE(S, k, xs):
    n = S.STONE_NAME[k]; tr = tradition(S, k); kc = S.kinds_of(xs)
    lo, hi = min(x['price'] for x in xs), max(x['price'] for x in xs)
    sizes = sorted({x['size'] for x in xs if x['size']}, key=float)
    intro = (f'<p class="intro">{len(xs)} {E(n.lower())} pieces in sterling and fine settings: {kinds_phrase(kc)}. Prices run {S.money(lo)} to {S.money(hi)}.'
             + (f' Ring sizes in stock right now: {", ".join(sizes)}.' if sizes else '') + '</p>'
             + (f'<p class="note-belief">Folklore around {E(n.lower())} speaks of {plist(tr)}. We mention it as tradition only.</p>' if tr else ''))
    faq = [(f'Do you have {n.lower()} rings in my size?', (f'Today we have sizes {", ".join(sizes)}. Each size is listed separately.' if sizes else f'There are no {n.lower()} rings listed by size right now; call {S.PHONE} and we will check.')),
           (f'Is the {n.lower()} jewelry sterling silver?', 'Most pieces on this page are .925 sterling; the Metal line on each product page confirms it.'),
           (f'Where can I see {n.lower()} jewelry in Manhattan?', f'At {S.STORE_ADDR}, by Union Square. Reserve online to have it ready.')]
    return {'title': f'{n} Sterling Silver Jewelry in NYC | Namaste Jewelry Shop', 'desc': f'{len(xs)} {n.lower()} sterling silver rings, pendants and earrings from {S.money(lo)} at 2 West 14th Street, near Union Square.',
            'h1': f'{n} in sterling silver', 'sub': f'{len(xs)} pieces', 'intro': intro, 'faq': faq, 'faq_title': f'About our {n.lower()} pieces'}
def intent_tile(S, k):
    st = [S.STONE_NAME[s] for ik, _, sts, _ in S.INTENTS if ik == k for s in sts if s in S.STONE_NAME][:2]
    return f'In sterling: {plist(st).lower()} and more.' if st else 'Symbols set in sterling.'
def INTENT_PAGE(S, k, xs):
    n = S.INTENT_NAME[k]; st = [S.STONE_NAME[s] for ik, _, sts, _ in S.INTENTS if ik == k for s in sts if s in S.STONE_NAME]
    lo = min(x['price'] for x in xs)
    return {'title': f'Sterling Silver Jewelry for {n} | Namaste Jewelry Shop NYC', 'desc': f'{len(xs)} sterling gemstone pieces chosen for {n.lower()} from {S.money(lo)}, at 2 West 14th Street by Union Square.',
            'h1': f'Sterling pieces for {n.lower()}', 'sub': f'{len(xs)} pieces from {S.money(lo)}',
            'intro': f'<p class="intro">Silver settings with the stones and symbols people choose for {E(n.lower())}' + (f', such as {E(plist(st[:4]).lower())}' if st else '') + '.</p><p class="note-belief">These pairings come from crystal folklore. We list them as tradition, with no claim that a stone does anything.</p>',
            'faq': [(f'Which gemstones are traditionally tied to {n.lower()}?', (f'Folklore most often names {plist(st[:5]).lower()}.' if st else 'This page gathers symbols worn for this intention.') + ' It is tradition, not science.')]}
def STONES_HUB(S): return {'title': 'Gemstones A to Z in Sterling Silver | Namaste Jewelry Shop NYC', 'desc': f'{len(S.STONE_KEYS)} gemstones in sterling silver settings at 2 West 14th Street, with price ranges.', 'h1': 'Gemstones A to Z',
                           'lead': f'Every gemstone with at least {STONE_MIN} sterling or fine pieces in stock, with today\'s price range.'}
def INTENTS_HUB(S): return {'title': 'Sterling Silver Jewelry by Intention | Namaste Jewelry Shop', 'desc': 'Sterling gemstone jewelry grouped by the intentions folklore gives each stone.', 'h1': 'By intention', 'lead': 'Grouped by the meanings folklore attaches to each gemstone, offered as tradition only.'}

def brand_intro(S, k, st):
    name = S.BRAND_NAME[k]; xs = st['xs']
    stones = [S.STONE_NAME[s] for s, _ in collections.Counter(x['family'] for x in xs if x['family']).most_common(4)]
    sizes = sorted({x['size'] for x in xs if x['size']}, key=float)
    t = f'{st["n"]} sterling and fine piece{"s" if st["n"] != 1 else ""} from {E(name)} are at the counter: {kinds_phrase(S.kinds_of(xs))}.'
    if stones: t += f' Gemstones include {E(plist(stones).lower())}.'
    if sizes: t += f' Rings in sizes {", ".join(sizes[:10])}.'
    return f'<p>{t} Prices from {S.money(st["min"])}.</p>'
def brand_faq(S, k, st):
    name = S.BRAND_NAME[k]
    return [(f'Where is {name} sterling jewelry sold in NYC?', f'Namaste Jewelry Shop at {S.STORE_ADDR} carries {st["n"]} {name} pieces.'),
            (f'What is the price range for {name}?', f'{S.money(st["min"])} to {S.money(st["max"])} today.' if st['max'] > st['min'] else f'{S.money(st["min"])} today.')]
def BRAND_H1(S, k): return f'{S.BRAND_NAME[k]} sterling silver'
def BRAND_TITLE(S, k, st): return f'{S.BRAND_NAME[k]} Sterling Silver Jewelry, NYC | Namaste Jewelry Shop'
def BRAND_DESC(S, k, st): return f'{st["n"]} {S.BRAND_NAME[k]} sterling and gemstone pieces from {S.money(st["min"])} at 2 West 14th Street by Union Square.'
def BRANDS_TITLE(S): return 'Silversmiths & Jewelry Makers | Namaste Jewelry Shop NYC'
def BRANDS_DESC(S): return 'The named silversmiths and jewelry makers at Namaste Jewelry Shop, 2 West 14th Street.'
BRANDS_H1 = 'Silversmiths & makers'
def BRANDS_LEAD(S, n): return f'{n} named makers have sterling pieces at the counter. Many more pieces come from independent workshops without a public label and are found under <a href="/stones/">gemstones</a>.'

PAIR = {'pendant': ['chain'], 'ring': ['earrings'], 'earrings': ['pendant'], 'chain': ['pendant'], 'necklace': ['earrings'], 'bracelet': ['ring'], 'anklet': ['bracelet'], 'beaded': ['ring'], 'mala': ['pendant']}
REL_BRAND = 'Also by {brand}'
REL_SCENT = 'More in {scent}'
REL_PAIR = 'Complete the look'
REL_MORE = 'More {aisle}'
def describe(S, x):
    k = x['base']; stn = x['stones']; s = []
    setting = re.search(r'claw|prong|bezel|wire wrap|wrapped|filigree|celtic|domed|spinner', x['title'], re.I)
    s.append(f"A {kind_one(k)} in {x['metal'].lower()}" + (f" with {E(plist([S.STONE_NAME[t] for t in stn[:3]]).lower())}" if stn else '') + (f", {setting.group(0).lower()} setting" if setting and k in ('ring', 'pendant') else '') + '.')
    if x['size']: s.append(f'Ring size {E(x["size"])} (US). Need another size? Search the stone name; each size is listed on its own.')
    if k == 'chain': s.append('Pair it with any of our pendants; check the bail opening against the chain thickness listed in the title.')
    if x['metal'] == 'Sterling silver': s.append('Sterling is 92.5 percent pure silver. Store it in a pouch away from air and humidity and polish with a silver cloth to keep its shine.')
    if stn and stn[0] not in S.NON_STONE and tradition(S, stn[0]): s.append(f"Crystal lore links {E(S.STONE_NAME[stn[0]].lower())} with {plist(tradition(S, stn[0]))}; that is tradition, not a proven property.")
    s.append('Each natural stone is a little different from the next, and from the photo.')
    s.append('Try it on when you collect it at 2 West 14th Street, or have it shipped from New York City. Checkout runs securely on Shopify through namastebookshop.com.')
    return s
def PRODUCT_DESC(S, x, v0): return f"{x['title']} in {x['metal'].lower() or 'a fine setting'}, {S.money(v0['price'])}. " + ('Reserve for pickup at 2 West 14th Street by Union Square.' if x['pickup'] else 'At 2 West 14th Street by Union Square.')

def ABOUT_DESC(S): return 'About Namaste Jewelry Shop, the sterling silver and gemstone counter at 2 West 14th Street by Union Square. A brand of Wealth Edge Ventures Inc.'
ABOUT_H1 = 'About Namaste Jewelry Shop'
def ABOUT(S):
    return f'''<p class="lead">Namaste Jewelry Shop is the sterling silver counter at {S.STORE_ADDR}: gemstone rings by size, pendants, chains, earrings and bracelets in .925 silver and finer settings.</p>
<p>We keep {S.N:,} pieces listed online with photos, live prices and stock, and we keep them simple to shop: one ring size per listing, chains labeled by length and thickness, and collector stones in their own aisle.{" Reserve any piece and choose Pickup to try it on at the counter." if S.PICKUP_ON else ""}</p>
<h2>Visit the counter</h2><p>{S.STORE_ADDR}. Call <a href="tel:{S.TEL}">{S.PHONE}</a>.</p>{S.hours_html()}{S.visit_buttons()}
<h2>Who we are</h2><p>{S.LEGAL} Orders are checked out on Shopify through <a href="{S.SHOP}" rel="noopener">namastebookshop.com</a>, which takes payment and fulfills orders and pickups.</p>
<h2>Our aisles</h2><ul>{''.join(f'<li><a href="/shop/{AISLES[k][2]}/">{E(AISLES[k][0])}</a>: {E(AISLES[k][3])}</li>' for k in S.AISLE_KEYS)}</ul>
<h2>A note on stone lore</h2><p>Where we mention what a stone is said to mean, it is tradition and folklore, shared for interest. We make no health or metaphysical claims.</p>'''
VISIT_TITLE = 'Visit the Sterling Silver Counter by Union Square'
def VISIT_DESC(S): return f'Hours, directions and pickup for Namaste Jewelry Shop at {S.STORE_ADDR}, a few minutes from Union Square.'
def VISIT_LEAD(S): return f'The counter is at {S.STORE_ADDR}, just west of Fifth Avenue on 14th Street. Reserve online and try the piece on when you collect it.'
def FAQ_DESC(S): return 'Sterling silver questions answered: .925 stamps, ring sizes, chain lengths, tarnish, pickup and shipping at Namaste Jewelry Shop.'
FAQ_H1 = 'Sterling silver questions'
def FAQ(S):
    return [('Is everything sterling silver?', 'Almost all of it. A few higher-priced pieces are in gold-plated or gold-tone settings; the Metal line on each product page says which.'),
            ('What does .925 mean?', 'It means 92.5 percent silver, the standard for sterling. Read <a href="/guide/how-to-tell-real-sterling-silver/">how to spot real sterling</a>.'),
            ('How do I order the right ring size?', 'Each size is its own listing. Use the <a href="/guide/ring-sizing/">ring sizing page</a> or come in and try a few.'),
            ('Which chain length should I get?', 'Most people wear pendants on 18 inches. See the <a href="/guide/chain-length-guide/">chain length guide</a>.'),
            ('Can I reserve and try on before I take it home?', 'Yes. Choose Pickup at checkout and look it over when you collect it at 2 West 14th Street.' + (f' Orders are {S.READY.lower()}.' if S.READY else '')),
            ('Where are you?', f'{S.STORE_ADDR}, about a 4-minute walk from 14 St&ndash;Union Square. Open daily from 11 AM.'),
            ('Do you ship?', 'Yes, from New York City; options and costs show at checkout on Shopify before you pay.'),
            ('Why does silver tarnish?', 'Silver reacts with sulfur in the air. Store it in a closed pouch and polish with a silver cloth. See <a href="/guide/sterling-silver-care/">silver care</a>.')]
def GUIDES(S):
    return [
     {'path': '/guide/how-to-tell-real-sterling-silver/', 'title': 'How to Tell Real Sterling Silver: .925 Stamps & Simple Checks', 'desc': 'What the .925 stamp means, how sterling differs from silver-plated and silver-tone, and simple checks you can do.', 'h1': 'How to spot real sterling silver',
      'html': '''<p class="lead">Sterling silver is an alloy of 92.5 percent silver and 7.5 percent other metals, usually copper, which makes it strong enough to wear.</p>
<h2>Look for the stamp</h2><p>Sterling is usually stamped .925, 925 or STERLING, often inside a ring band or on a clasp. Small pieces may not have room for a stamp.</p>
<h2>Sterling vs. plated vs. silver-tone</h2><ul><li><b>Sterling:</b> solid silver alloy through and through.</li><li><b>Silver-plated:</b> a thin silver layer over another metal; it can wear off.</li><li><b>Silver-tone:</b> a silver color with no silver content.</li></ul>
<h2>Simple checks</h2><ul><li>Silver is not magnetic; a strong magnet that grabs a piece suggests another metal.</li><li>Tarnish on sterling wipes off with a silver cloth to bright metal beneath.</li></ul><p><a class="btn" href="/shop/">Shop sterling</a></p>'''},
     {'path': '/guide/chain-length-guide/', 'title': 'Necklace Chain Length Guide: 16 to 30 Inches', 'desc': 'Where 16, 18, 20, 22, 24 and 30 inch chains fall, plus how chain thickness affects which pendants fit.', 'h1': 'Chain length guide',
      'html': '''<p class="lead">Chain length changes how a pendant sits. Here is where each common length usually falls on an adult.</p>
<ul><li><b>16 inches:</b> at the base of the neck.</li><li><b>18 inches:</b> at the collarbone, the most popular pendant length.</li><li><b>20 inches:</b> just below the collarbone.</li><li><b>22 inches:</b> above most necklines.</li><li><b>24 inches:</b> at the top of the chest.</li><li><b>30 inches:</b> long, for layering or wearing over clothes.</li></ul>
<h2>Thickness and bails</h2><p>Chains are listed with their width in millimeters. A 1.1 to 1.5 mm chain fits most pendant bails; heavier Cuban and Franco chains suit pendants with a wide bail.</p><p><a class="btn" href="/shop/sterling-silver-chains/">Shop chains</a></p>'''},
     {'path': '/guide/ring-sizing/', 'title': 'Ring Sizing for Sterling Silver Gemstone Rings', 'desc': 'Find your US ring size at home and shop our sterling gemstone rings, each listed by size.', 'h1': 'Ring sizing',
      'html': '''<p class="lead">Every sterling ring here is listed size by size. To find yours, measure a ring you already wear.</p>
<table><caption class="sr">US ring sizes by inside diameter</caption><thead><tr><th scope="col">US size</th><th scope="col">Inside diameter</th></tr></thead><tbody><tr><td>5</td><td>15.7 mm</td></tr><tr><td>6</td><td>16.5 mm</td></tr><tr><td>7</td><td>17.3 mm</td></tr><tr><td>8</td><td>18.1 mm</td></tr><tr><td>9</td><td>19.0 mm</td></tr><tr><td>10</td><td>19.8 mm</td></tr><tr><td>11</td><td>20.6 mm</td></tr></tbody></table>
<p>Wide bands feel tighter, and fingers are larger later in the day. When in doubt, try one on at pickup.</p><p><a class="btn" href="/shop/sterling-silver-rings/">Shop rings</a></p>'''},
     {'path': '/guide/sterling-silver-care/', 'title': 'Sterling Silver Care: Cleaning, Storing & Tarnish', 'desc': 'Keep sterling silver and gemstones bright: storage, polishing and what to avoid.', 'h1': 'Sterling silver care',
      'html': '''<p class="lead">Wear it often, store it closed up and polish lightly.</p><ul><li>Store pieces separately in closed pouches or a lined box.</li><li>Polish with a silver cloth; avoid dips on pieces with porous stones such as turquoise, opal or malachite.</li><li>Take rings off for cleaning products, chlorine and the gym.</li><li>Put jewelry on after lotion and perfume.</li></ul>'''},
     {'path': '/sterling-silver-jewelry-nyc/', 'title': 'Sterling Silver Jewelry in NYC near Union Square', 'store_ld': True, 'desc': f'Sterling silver gemstone jewelry in Manhattan: {S.N:,} pieces at {S.STORE_ADDR}, by Union Square, with pickup.', 'h1': 'Sterling silver jewelry in NYC',
      'html': f'<p class="lead">{S.N:,} sterling and fine pieces, a few minutes from Union Square: {kinds_phrase(S.kind_count, 4)}.</p>{hood_list(S, "/near/")}{S.visit_block()}'},
    ]
HOOD_LINE = {'union-square': 'The closest sterling counter to the Union Square subway exits.', 'east-village': 'A straight walk west on 14th Street from Avenue A.',
             'chelsea': 'Just east of Sixth Avenue on 14th.', 'flatiron': 'Straight down Fifth Avenue.', 'greenwich-village': 'Up Fifth from Washington Square.', 'midtown': 'Two express stops from Times Square.'}
def HOODS(S):
    picks = S.by_rank([x for x in S.leaders if not x['noimg'] and x['aisle'] in ('ring', 'pendant')])[:8]
    return [{'path': f'/near/{k}/', 'title': f'Sterling Silver Jewelry near {n} | Namaste Jewelry Shop', 'h1': f'Sterling silver near {n}',
             'desc': f'Sterling silver gemstone rings, pendants and chains near {n}, NYC, at {S.STORE_ADDR}. Directions, hours and pickup.',
             'html': f'<p class="lead">{E(HOOD_LINE[k])} {S.N:,} sterling and fine pieces, rings sized one per listing.</p><h2>Getting here from {E(n)}</h2><p>{E(route)}</p><h2>At the counter now</h2>{S.grid(picks)}{S.visit_block()}<h2>More neighborhoods</h2>{hood_list(S, "/near/", k)}'}
            for k, n, route in HOOD_DATA]
NOT_FOUND = 'That piece is no longer at the counter'
