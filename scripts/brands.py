"""Jewelry brands and makers we can identify in the namastebookshop.com catalog.

A product belongs to a brand when its title names the brand OR its Shopify vendor field is that company.
Opaque supplier codes (yngint, vlorg, SDNIMP, kncrfin, drftpb, Crtnnpl, NAGIMPINC) and the store's own
'Namaste Bookshop' vendor are not public brand names, so they never create a brand page.
Brand pages state only what the live catalog shows (counts, stones, metals, prices); no claims about the companies.
"""
import re
BRANDS = [
 # key, display name, title regex, vendor names
 ('clea-ray', 'Clea Ray', r'clea ray', []),
 ('dare-to-dream', 'Dare to Dream (Esagono)', r'dare to dream', ['Esagono LLC']),
 ('karmalogy', 'Zorbitz Karma Beads', r'karmalogy|karma beads', ['ZORBITZ Inc']),
 ('starborn', 'Starborn', r'^$', ['STARBORN']),
 ('nirvana', 'Nirvana Inc.', r'^$', ['Nirvana Inc', 'Nirvana Inc Silver Jewelry']),
 ('crystal-earth-studio', 'Crystal Earth Studio', r'^$', ['crystal Earth Studio']),
 ('heaven-earth', 'Heaven & Earth', r'^$', ['Heaven & Earth LLC', 'HVNRTH']),
 ('indiana-gems', 'Indiana Gems International', r'^$', ['indiana Gems International']),
 ('angelstar', 'AngelStar', r'^$', ['Quanta/Angel Star/Mandala Art']),
 ('benjamin', 'Benjamin International', r'^$', ['Benjamin International', 'BNJINT']),
 ('ocealic', 'Ocealic Linkways', r'^$', ['OCNLKW', 'Ocealic Linkways']),
 ('village-original', 'Village Original', r'^$', ['Village Original Inc']),
 ('cherisse', 'Handmade by Cherisse', r'by cherisse', []),
]
NAME = {k: n for k, n, _, _ in BRANDS}
_RX = [(k, re.compile(rx, re.I)) for k, _, rx, _ in BRANDS if rx != '^$']
_V = {v: k for k, _, _, vs in BRANDS for v in vs}
def brand_of(title, vendor=''):
    for k, rx in _RX:
        if rx.search(title): return k
    return _V.get(vendor or '', '')
FACTS = {}
