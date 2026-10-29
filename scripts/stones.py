"""Stones, metals, styles and intentions read from product titles.

Intentions are the meanings crystal traditions commonly give a stone. Sites present them as tradition and belief,
never as proven effects, and every intention page carries that note.
"""
import re
STONES = [  # key, display name, title regex (checked by earliest position in the title)
 ('rose-quartz', 'Rose Quartz', r'rose quartz'), ('smoky-quartz', 'Smoky Quartz', r'smok[e]?y quartz'), ('rutilated-quartz', 'Rutilated Quartz', r'rutilated|tourmalinated quartz'),
 ('aura-quartz', 'Aura Quartz', r'\baura\b'), ('herkimer', 'Herkimer Diamond', r'herkimer'), ('strawberry-quartz', 'Strawberry Quartz', r'strawberry quartz'),
 ('black-tourmaline', 'Black Tourmaline', r'black tourmaline|schorl'), ('tourmaline', 'Tourmaline', r'tourmalin?e?|watermelon|tourmal\b'),
 ('amethyst', 'Amethyst', r'amethyst'), ('citrine', 'Citrine', r'citrine'), ('tiger-eye', "Tiger's Eye", r"tiger.?s? ?eye|hawk.?s? ?eye"),
 ('labradorite', 'Labradorite', r'labradorite|spectrolite'), ('moonstone', 'Moonstone', r'moon ?stone'), ('lapis', 'Lapis Lazuli', r'lapis'),
 ('malachite', 'Malachite', r'malachite'), ('turquoise', 'Turquoise', r'turquoise'), ('aventurine', 'Aventurine', r'aventurine'), ('jade', 'Jade', r'\bjade\b|nephrite'),
 ('obsidian', 'Obsidian', r'obsidian|apache tear'), ('onyx', 'Onyx', r'\bonyx\b|sardonyx'), ('hematite', 'Hematite', r'hematite'), ('carnelian', 'Carnelian', r'carnelian'),
 ('selenite', 'Selenite', r'selenite'), ('fluorite', 'Fluorite', r'fluorite'), ('sodalite', 'Sodalite', r'sodalite'), ('amazonite', 'Amazonite', r'amazonite'),
 ('opal', 'Opal', r'\bopal\b|opals\b'), ('opalite', 'Opalite', r'opalite'), ('garnet', 'Garnet', r'garnet'), ('peridot', 'Peridot', r'peridot'), ('aquamarine', 'Aquamarine', r'aquamarine'),
 ('moldavite', 'Moldavite', r'moldavite'), ('larimar', 'Larimar', r'larimar'), ('rhodochrosite', 'Rhodochrosite', r'rhodochrosite'), ('rhodonite', 'Rhodonite', r'rhodonite'),
 ('chrysocolla', 'Chrysocolla', r'chrysocolla|gem silica'), ('unakite', 'Unakite', r'unakite'), ('jasper', 'Jasper', r'jasper|mookaite'), ('agate', 'Agate', r'agate|druzy|druze'),
 ('lepidolite', 'Lepidolite', r'lepidolite'), ('kyanite', 'Kyanite', r'kyanite'), ('pyrite', 'Pyrite', r'pyrite'), ('shungite', 'Shungite', r'shungite'),
 ('amber', 'Amber', r'\bamber\b'), ('chrysoprase', 'Chrysoprase', r'chrysoprase'), ('topaz', 'Topaz', r'topaz'), ('iolite', 'Iolite', r'iolite'), ('kunzite', 'Kunzite', r'kunzite'),
 ('sunstone', 'Sunstone', r'sun ?stone'), ('howlite', 'Howlite', r'howlite'), ('lava', 'Lava Stone', r'\blava\b'), ('goldstone', 'Goldstone', r'goldstone|gold stone'),
 ('bloodstone', 'Bloodstone', r'bloodstone|blood stone'), ('charoite', 'Charoite', r'charoite'), ('prehnite', 'Prehnite', r'prehnite'), ('apatite', 'Apatite', r'apatite'),
 ('ammonite', 'Ammonite', r'ammonite'), ('pearl', 'Pearl', r'\bpearls?\b'), ('abalone', 'Abalone & Shell', r'abalone|mother of pearl|\bshell\b|conch'),
 ('ruby', 'Ruby', r'\bruby\b'), ('sapphire', 'Sapphire', r'sapphire'), ('emerald', 'Emerald', r'emerald'), ('tanzanite', 'Tanzanite', r'tanzanite'),
 ('morganite', 'Morganite', r'morganite'), ('azurite', 'Azurite', r'azurite'), ('dumortierite', 'Dumortierite', r'dumortierite'), ('epidote', 'Epidote', r'epidote'),
 ('seraphinite', 'Seraphinite', r'seraphinite'), ('angelite', 'Angelite', r'angelite'), ('celestite', 'Celestite', r'celestite'), ('sugilite', 'Sugilite', r'sugilite'),
 ('libyan-glass', 'Libyan Desert Glass', r'libyan'), ('tektite', 'Tektite', r'tektite'), ('coral', 'Coral', r'\bcoral\b'),
 ('rudraksha', 'Rudraksha', r'rudraksh'), ('sandalwood', 'Sandalwood', r'sandalwood'), ('wood', 'Wood & Seed', r'\bwood(en)?\b|rosewood|tulsi|bodhi|lotus seed|raktu|palo santo|bone'),
 ('clear-quartz', 'Clear Quartz', r'clear quartz|crystal quartz|rock crystal|lemurian|\bquartz\b'),
]
STONE_NAME = {k: n for k, n, _ in STONES}
_SRX = [(k, re.compile(rx, re.I)) for k, _, rx in STONES]
NON_STONE = {'rudraksha', 'sandalwood', 'wood', 'pearl', 'abalone', 'amber', 'coral'}

def stones_of(t):
    """All stones named in a title, earliest first."""
    hits = []
    for k, rx in _SRX:
        m = rx.search(t)
        if m: hits.append((m.start(), -len(m.group(0)), k))
    hits.sort(); out = []
    for _, _, k in hits:
        if k == 'clear-quartz' and any(h in out for h in ('rose-quartz', 'smoky-quartz', 'rutilated-quartz', 'aura-quartz', 'strawberry-quartz')) and not re.search(r'clear quartz', t, re.I): continue
        if k == 'tourmaline' and 'black-tourmaline' in out and len(re.findall(r'tourmal', t, re.I)) < 2: continue
        if k == 'opal' and 'opalite' in out: continue
        if k not in out: out.append(k)
    return out

# Intentions: the stones crystal traditions most often link to each intention.
INTENTS = [
 ('protection', 'Protection', ['black-tourmaline', 'obsidian', 'onyx', 'hematite', 'smoky-quartz', 'tiger-eye', 'shungite', 'pyrite', 'labradorite'], r'protect|evil eye|hamsa|nazar|eye of horus'),
 ('love', 'Love & Self-Love', ['rose-quartz', 'rhodonite', 'rhodochrosite', 'garnet', 'kunzite', 'morganite', 'strawberry-quartz'], r'\blove\b|heart'),
 ('calm', 'Calm & Peace', ['amethyst', 'lepidolite', 'howlite', 'aquamarine', 'larimar', 'sodalite', 'angelite', 'celestite', 'amazonite'], r'calm|peace|serenity|anxiety|relax'),
 ('abundance', 'Abundance & Luck', ['citrine', 'pyrite', 'aventurine', 'jade', 'goldstone', 'tiger-eye', 'sunstone'], r'luck|lucky|abundance|prosper|wealth|money'),
 ('intuition', 'Intuition & Spirit', ['labradorite', 'moonstone', 'lapis', 'amethyst', 'iolite', 'azurite', 'moldavite', 'charoite', 'sugilite'], r'intuition|third eye|psychic|spirit|goddess'),
 ('grounding', 'Grounding & Balance', ['hematite', 'smoky-quartz', 'jasper', 'onyx', 'obsidian', 'unakite', 'lava', 'bloodstone'], r'ground|balance|root chakra'),
 ('clarity', 'Clarity & Focus', ['clear-quartz', 'fluorite', 'sodalite', 'herkimer', 'apatite', 'kyanite', 'selenite'], r'clarity|focus|study|wisdom'),
 ('confidence', 'Energy & Confidence', ['carnelian', 'sunstone', 'tiger-eye', 'garnet', 'citrine', 'red-jasper'], r'courage|confidence|strength|energy|power'),
 ('chakra', 'Chakra Balance', [], r'chakra|7 stone|seven stone'),
 ('meditation', 'Meditation & Prayer', ['rudraksha', 'sandalwood', 'wood'], r'\bmala\b|prayer|meditat|japa|buddha|\bom\b|karma'),
]
INTENT_NAME = {k: n for k, n, _, _ in INTENTS}
def intents_of(t, stones):
    out = []
    for k, _, st, rx in INTENTS:
        if (stones and stones[0] in st) or re.search(rx, t, re.I): out.append(k)
    return out

METALS = ['Sterling silver', 'Silver-plated', 'Gold-tone & gold-plated', 'Copper', 'Brass', 'Stainless steel', 'Pewter', 'Base metal', 'Cord, elastic & leather']
def metal_of(t, ty, kind):
    l = (t + ' ' + ty).lower()
    if re.search(r'gold (tone|plated|dipped|filled)|gold-plated|gold-tone|18k|14k gold|vermeil', l): return 'Gold-tone & gold-plated'
    if re.search(r'silver.?plated|silver tone|silver-tone|plated', l) and not re.search(r'sterling', l): return 'Silver-plated'
    if re.search(r'sterling|\.925|\b925\b|\bss\b', l): return 'Sterling silver'
    if 'stainless' in l: return 'Stainless steel'
    if 'copper' in l: return 'Copper'
    if 'brass' in l or 'bronze' in l: return 'Brass'
    if 'pewter' in l: return 'Pewter'
    if 'base metal' in l or 'alloy' in l or re.search(r'adjustable (metal )?ring', l): return 'Base metal'
    if kind in ('beaded', 'mala') or re.search(r'cord|string|leather|hemp|elastic|stretch|knotted', l): return 'Cord, elastic & leather'
    return ''

STYLES = [
 ('Wire wrapped', r'wire.?wrap|coil wrap|wrapped'), ('Raw & natural', r'\braw\b|rough|natural (crystal|stone)|druzy|geode|cluster|uncut|chips?\b'),
 ('Crystal point', r'\bpoint\b|d/?t\b|double terminated|prism|bullet'), ('Faceted & gemstone', r'facet|cz\b|cubic|gemstone (ring|pendant)|solitaire|oval|cushion|marquise'),
 ('Evil eye & hamsa', r'evil eye|hamsa|nazar|eye of horus'), ('Moon & celestial', r'moon|star|celestial|sun\b|planet|zodiac|constellation|saturn|crescent'),
 ('Tree of life & nature', r'tree of life|leaf|flower|lotus|butterfly|dragonfly|feather|mushroom|bee\b'), ('Hearts', r'heart'),
 ('Spiritual symbols', r'\bom\b|buddha|ganesh|pentacle|pentagram|triple goddess|ankh|cross|angel|hamsa|yin|mandala|flower of life|metatron|merkaba|chakra|vajra|dorje|triquetra|celtic'),
 ('Animals', r'dragon|owl|elephant|turtle|wolf|cat\b|snake|serpent|octopus|dolphin|whale|fish|bird|horse|fox|bear|frog|mermaid|seahorse'),
 ('Bands & stacking', r'\bband\b|domed|stack|spinner|midi|ring set'), ('Beaded', r'\bbead|\d+ ?mm'),
]
def style_of(t):
    for n, rx in STYLES:
        if re.search(rx, t, re.I): return n
    return ''
def bead_mm(t):
    m = re.search(r'(\d{1,2}(?:\.\d)?)\s?(?:-\s?\d{1,2}\s?)?mm', t, re.I)
    return float(m.group(1)) if m else None
def ring_size(t):
    m = re.search(r'size\s?\(?\s?(\d{1,2}(?:\.\d)?)', t, re.I)
    return m.group(1) if m else ''
