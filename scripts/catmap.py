"""Jewelry and bead kinds for the Namaste jewelry and bead storefronts.

category(p) returns the kind ('base') of a namastebookshop.com product, or None when it is not jewelry
(meditation tools are returned as 'meditation' so the bead shop can carry them). Each site's sitecopy.assign()
then decides which of these kinds, metals and prices belong on that site and in which aisle.
"""
import re
KINDS = ['beaded', 'mala', 'bracelet', 'pendant', 'necklace', 'chain', 'ring', 'earrings', 'anklet', 'charm', 'beads', 'meditation']
T = {
 'beaded': ['Crystal Bead Bracelets', 'Crystal & Beads Adjustable Bracelet'],
 'mala': ['Crystal Beads Mala', 'Crystal Mala', 'Mala'],
 'bracelet': ['Bracelet', 'Crystal Bracelet', 'Copper Bracelet /Cuff', 'Adjustable String Bracelet', 'Adjustable Sterling Silver Bracelet', 'Adjustable Chain Bracelet',
              'Steel/Leather Bracelet', 'Stainless Steel Bracelet', 'Vegan Leather Bracelet', 'Bangle', 'Cuff Crystal Bracelets', 'Link Stone Bracelet', 'Sterling Silver Bracelet'],
 'pendant': ['Pendant', 'Sterling Silver Pendant', 'Crystal Pendant', 'Plated Stone Pendant', 'Wire Wrapped Pendant', 'SS Wire Wrap Pendant', 'Plated Pendant',
             'Pendant Carded', 'Copper Pendant', 'Teardrop', 'Crystal Heart Pendant'],
 'necklace': ['Necklace', 'Crystal Necklace', 'Black Cord Stone Necklace', 'Sterling Silver Necklace', 'Plated Stone Necklace', 'Plated Black Necklace'],
 'chain': ['Sterling Silver Chains', 'Plated Chains'],
 'ring': ['Ring', 'Adjustable Base Metal Ring', 'Sterling Silver RIngs', 'Domed Band Rings', 'Plated Stone Ring', 'Stainless Steel Rings', 'Beads Ring'],
 'earrings': ['Plated Stone Earrings', 'Earrings', 'Brass Earrings', 'Crystal Earrings', 'Earings', 'Sterling Silver Earrings'],
 'anklet': ['Anklet', 'Sterling Silver Anklet'],
 'charm': ['Charm'],
 'beads': ['Beads Strand', 'Waist Beads'],
 'meditation': ['Brass Singing Bowl', 'Hand Bells', 'Tuning Fork', 'Meditation & Wellness'],
}
TYPE2KIND = {t: k for k, ts in T.items() for t in ts}
NOT_JEWELRY = re.compile(r'\bby [A-Z]|singing bowl|candle|key ?chain|holder|\bdish\b|jewelry box|\bbox\b|\bbook\b|\bcards?\b|\bdeck\b|\bbag\b|pouch|\bstand\b|display|\btray\b|soap|spray|\boil\b|statue|chime|cleaner|polish cloth|sticker|magnet|pendulum|suncatcher|wall hanging|ornament', re.I)
def _by_title(t):
    if re.search(r'\bmalas?\b', t, re.I): return 'mala'
    if re.search(r'earrings?|earings?|studs?\b', t, re.I): return 'earrings'
    if re.search(r'anklet', t, re.I): return 'anklet'
    if re.search(r'\bbracelets?\b|bangle|\bcuff\b', t, re.I):
        return 'beaded' if re.search(r'\bbead(s|ed)?\b|\d+ ?mm|chip', t, re.I) and not re.search(r'link|chain|cuff|bangle|leather|string', t, re.I) else 'bracelet'
    if re.search(r'\brings?\b', t, re.I) and not re.search(r'earring|key ?ring|ring holder|o-ring', t, re.I): return 'ring'
    if re.search(r'pendant', t, re.I): return 'pendant'
    if re.search(r'necklace|choker', t, re.I): return 'necklace'
    if re.search(r'\bchain\b', t, re.I): return 'chain'
    if re.search(r'\bcharms?\b', t, re.I): return 'charm'
    return None

def category(p):
    t, ty = p['title'].strip(), (p.get('product_type') or '').strip()
    if ty in TYPE2KIND:
        k = TYPE2KIND[ty]
        if k == 'meditation':
            if ty == 'Meditation & Wellness' and re.search(r'\bmala\b', t, re.I): return 'mala'
            return 'meditation'
        if k == 'beaded' and re.search(r'\bmala\b', t, re.I): return 'mala'
        if k == 'mala' and re.search(r'stretch bracelet', t, re.I): return 'beaded'
        if k == 'bracelet' and re.search(r'\bbead(s|ed)?\b|\d+ ?mm|chip', t, re.I) and not re.search(r'link|chain|cuff|bangle|leather|string|wire', t, re.I): return 'beaded'
        if k == 'necklace' and re.search(r'\bchain\b', t, re.I) and not re.search(r'pendant|stone|crystal|cz|with|w/|charm|evil eye|heart|moon|star', t, re.I): return 'chain'
        if k == 'necklace' and re.search(r'\bmala\b', t, re.I): return 'mala'
        return k
    if ty in ('', 'Crystal Jewelry', 'Jewelry', 'Stones', 'Crystal', 'Crystals'):
        if NOT_JEWELRY.search(t): return None
        if ty in ('Stones', 'Crystal', 'Crystals') and not re.search(r'pendant|necklace|bracelet|earring|\bring\b', t, re.I): return None
        return _by_title(t)
    return None
