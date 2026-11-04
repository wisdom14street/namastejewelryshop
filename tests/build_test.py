"""Offline build regressions. Synthetic products never reach the live catalog."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]


class Head(HTMLParser):
    def __init__(self, document):
        super().__init__()
        self.meta = []
        self.links = []
        self.feed(document)

    def handle_starttag(self, tag, attrs):
        if tag == 'meta':
            self.meta.append(dict(attrs))
        elif tag == 'a':
            self.links.append(dict(attrs).get('href', ''))


def fixture():
    products = []
    for i, kind in enumerate(['Ring', 'Pendant', 'Earrings', 'Bracelet', 'Necklace', 'Ring']):
        products.append({
            'id': 100 + i, 'handle': f'fixture-{i}',
            'title': f'{"Angelite" if i == 5 else "Amethyst"} .925 Sterling Silver {kind}',
            'product_type': kind, 'vendor': 'Fixture', 'body_html': '',
            'created_at': '2026-01-01T00:00:00Z',
            'images': [{'src': f'https://example.test/fixture-{i}.jpg'}],
            'variants': [{'id': 1000 + i, 'title': 'Default Title', 'price': '29.00',
                          'available': True, 'sku': f'FIX-{i}', 'compare_at_price': None}],
        })
    return products


class BuildTest(unittest.TestCase):
    def build(self, products=None, preview=False):
        tmp = tempfile.TemporaryDirectory(prefix='namaste-build-')
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        for directory in ('scripts', 'site', 'src'):
            shutil.copytree(ROOT / directory, root / directory)
        (root / 'data').mkdir()
        (root / 'data/all_products.json').write_text(json.dumps(products or fixture()))
        command = [sys.executable, str(root / 'scripts/build.py')]
        if preview:
            command.append('--preview')
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return root / 'dist'

    def test_build_links_search_metadata_and_tracking(self):
        dist = self.build()
        home = (dist / 'index.html').read_text()
        head = Head(home)
        self.assertIn('https://namastebookshop.com/', head.links)
        self.assertEqual(home.count('https://www.googletagmanager.com/gtag/js?'), 1)
        self.assertEqual(home.count('src="/assets/ga.js"'), 1)
        for key in ('og:image:width', 'og:image:height', 'og:image:type', 'og:image:alt', 'twitter:image:alt'):
            self.assertEqual(sum(m.get('property', m.get('name')) == key for m in head.meta), 1, key)
        meta = json.loads((dist / 'data/meta.json').read_text())
        self.assertIn('angelite', meta['fams'])  # Labels still cover every product.
        self.assertNotIn('angelite', meta['stone_pages'])
        self.assertIn('amethyst', meta['stone_pages'])
        for stone in meta['stone_pages']:
            self.assertTrue((dist / 'stones' / stone / 'index.html').is_file())
        catalog = json.loads((dist / 'data/catalog.json').read_text())
        self.assertEqual(len(catalog), 6)
        self.assertTrue(all(p['p'] == 29 for p in catalog))
        self.assertEqual({p['v'] for p in catalog}, set(range(1000, 1006)))
        for path in ('cart/index.html', '404.html'):
            self.assertTrue(any('noindex' in m.get('content', '') for m in Head((dist / path).read_text()).meta if m.get('name') == 'robots'))
        sitemap = (dist / 'sitemap.xml').read_text()
        self.assertNotIn('/cart/', sitemap)
        self.assertNotIn('/404.html', sitemap)

    def test_image_free_catalog_builds_with_branded_fallback(self):
        products = copy.deepcopy(fixture())
        for p in products:
            p['images'] = []
        dist = self.build(products)
        home = (dist / 'index.html').read_text()
        self.assertIn('"image": "https://namastejewelryshop.com/og.jpg"', home)
        catalog = json.loads((dist / 'data/catalog.json').read_text())
        self.assertEqual(len(catalog), 6)
        self.assertTrue(all(p['i'] == '/assets/no-photo.svg' for p in catalog))

    def test_preview_never_loads_google_analytics(self):
        dist = self.build(preview=True)
        home = (dist / 'index.html').read_text()
        self.assertNotIn('googletagmanager.com', home)
        self.assertNotIn('src="/assets/ga.js"', home)
        self.assertIn('noindex,nofollow', home)
        self.assertIn('Disallow: /', (dist / 'robots.txt').read_text())


if __name__ == '__main__':
    unittest.main()
