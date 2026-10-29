#!/usr/bin/env python3
"""Record Shopify Local Pickup availability for the products this site carries.

Reads the store's public pickup-availability section (the same text shoppers see on namastebookshop.com) for the first
available variant of each in-stock product whose kind is listed in site/config.json "kinds" (and under "max_price" when set),
and writes data/pickup.json: {"<variant_id>": {"available": true, "location": "...", "ready": "Usually ready in 2 hours"}}.
Products that cannot be checked are left out; the site then shows call-ahead wording instead of a pickup promise.
"""
import json, os, re, sys, time, urllib.request, concurrent.futures as cf
sys.path.insert(0, os.path.dirname(__file__))
from catmap import category
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CFG = json.load(open(os.path.join(ROOT, 'site', 'config.json')))
KINDS = set(CFG.get('kinds') or []); MAXP = CFG.get('max_price')
raw = json.load(open(os.path.join(ROOT, 'data', 'all_products.json')))
vids = []
for p in raw:
    k = category(p)
    if not k or (KINDS and k not in KINDS): continue
    av = [v for v in p['variants'] if v['available'] and float(v['price']) > 0]
    if not av or (MAXP and min(float(v['price']) for v in av) >= MAXP): continue
    vids.append(av[0]['id'])

def check(vid):
    url = f"https://namastebookshop.com/variants/{vid}/?section_id=pickup-availability"
    for attempt in range(3):
        try:
            t = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'NamasteJewelrySites-build/1.0'}), timeout=30).read().decode('utf-8', 'replace')
            t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t))
            m = re.search(r'Pickup available at (.+?) (Usually ready in [^.<]+?|Ready in [^.<]+?) (?:View|Check|$)', t)
            if m:
                return vid, {'available': True, 'location': m.group(1).strip(), 'ready': m.group(2).strip()}
            if re.search(r'Pickup currently unavailable', t):
                return vid, {'available': False}
            return vid, None
        except Exception:
            time.sleep(3 * (attempt + 1))
    return vid, None

out = {}
with cf.ThreadPoolExecutor(4) as ex:
    for vid, r in ex.map(check, vids):
        if r is not None:
            out[str(vid)] = r
json.dump(out, open(os.path.join(ROOT, 'data', 'pickup.json'), 'w'))
ok = sum(1 for r in out.values() if r['available'])
print(f"pickup checked {len(out)}/{len(vids)} variants, available for {ok}")
