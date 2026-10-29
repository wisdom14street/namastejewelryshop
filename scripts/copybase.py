"""Shared building blocks for the jewelry/bead sitecopy files: colors, plural names and HTML helpers.
No marketing copy lives here; every site writes its own words in site/sitecopy.py."""
import re, html
from hoods import HOODS
E = html.escape
STONE_COLOR = {'amethyst': '#8e5bb5', 'rose-quartz': '#e7a2b4', 'clear-quartz': '#9fb7c9', 'citrine': '#e0a526', 'black-tourmaline': '#2d2d2d', 'tiger-eye': '#a8702a',
 'labradorite': '#4f7894', 'moonstone': '#b9c3d6', 'lapis': '#2b4c9b', 'malachite': '#227a52', 'turquoise': '#2fb3aa', 'aventurine': '#4c9a5c', 'jade': '#4f8f67',
 'obsidian': '#3a3a40', 'onyx': '#1f1f1f', 'hematite': '#5b5f66', 'carnelian': '#d0612e', 'selenite': '#d9d4c7', 'fluorite': '#7c7fc4', 'sodalite': '#3b55a0',
 'amazonite': '#5fb8a8', 'opal': '#a6cbd6', 'opalite': '#b8d0e6', 'garnet': '#8b1e2d', 'peridot': '#8fae2e', 'aquamarine': '#79c0d2', 'moldavite': '#567a2c',
 'larimar': '#6cb8d8', 'rhodochrosite': '#d8768a', 'rhodonite': '#c5677a', 'jasper': '#a5482f', 'agate': '#9c7a5b', 'amber': '#d18a1d', 'aura-quartz': '#7aa7d8',
 'smoky-quartz': '#6b5844', 'tourmaline': '#3f8a5a', 'topaz': '#4aa3d6', 'ruby': '#b3122f', 'sunstone': '#e07a3c', 'goldstone': '#a5652a', 'rudraksha': '#7a4a2b',
 'sandalwood': '#b08455', 'wood': '#8a6a4f', 'howlite': '#cfcfcf', 'emerald': '#1f8a5a', 'sapphire': '#22408f', 'tanzanite': '#4b4fb0', 'pyrite': '#b39b4c', 'shungite': '#2b2b2b'}
INTENT_COLOR = {'protection': '#2d2d2d', 'love': '#d9708a', 'calm': '#8e5bb5', 'abundance': '#d6a12a', 'intuition': '#4f7894', 'grounding': '#7a5a3a',
 'clarity': '#7fa6c4', 'confidence': '#d0612e', 'chakra': '#c25ab5', 'meditation': '#8a6a4f'}
def stone_color(k): return STONE_COLOR.get(k, '#9c8a73')
def intent_color(k): return INTENT_COLOR.get(k, '#9c8a73')
KIND = {'beaded': ('beaded bracelet', 'beaded bracelets'), 'mala': ('mala', 'malas'), 'bracelet': ('bracelet', 'bracelets and cuffs'), 'pendant': ('pendant', 'pendants'),
        'necklace': ('necklace', 'necklaces'), 'chain': ('chain', 'chains'), 'ring': ('ring', 'rings'), 'earrings': ('pair of earrings', 'earrings'), 'anklet': ('anklet', 'anklets'),
        'charm': ('charm', 'charms'), 'beads': ('bead strand', 'bead strands'), 'meditation': ('meditation tool', 'meditation tools')}
def kind_one(k): return KIND[k][0]
def kinds_phrase(cnt, n=3):
    parts = [f'{c} {KIND[k][1] if c != 1 else KIND[k][0]}' for k, c in cnt.most_common(n)]
    return parts[0] if len(parts) == 1 else ', '.join(parts[:-1]) + ' and ' + parts[-1]
def plist(xs):
    xs = list(xs)
    return '' if not xs else xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]
def tradition(S, k):
    return [n.split(' & ')[0].lower() for n in S.stone_intents(k)]
def hood_list(S, prefix, current=''):
    return '<ul class="hoodlist">' + ''.join(f'<li><a href="{prefix}{k}/"><b>{E(n)}</b><span>Directions to 2 West 14th Street</span></a></li>' for k, n, _ in HOODS if k != current) + '</ul>'
