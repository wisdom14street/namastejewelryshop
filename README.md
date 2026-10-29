# namastejewelryshop.com

Namaste Jewelry Shop: static storefront built daily from the public namastebookshop.com catalog and deployed to GitHub Pages.
Namaste Jewelry Shop is a brand of Wealth Edge Ventures Inc.

- `site/config.json`: site settings. Set `REVIEW_URL` (Google review link) to show the "Review us on Google" button and QR code; set `GOOGLE_SITE_VERIFICATION` to the Search Console HTML-tag value. Both stay hidden while empty. `kinds`, `max_price` and `best_collections` limit what the daily pickup and best-seller checks fetch.
- `site/sitecopy.py`: aisles, product mix rules and all copy for this site.
- `site/theme.css`, `site/favicon.svg`: this site's design.
- `scripts/`: shared jewelry/bead engine (fetch with pagination and 429 backoff, Shopify pickup check, best sellers, build).
- Checkout: Buy buttons open `namastebookshop.com/cart/<variant>:1?attributes[Storefront]=Namaste Jewelry Shop`, so each order is tagged with this storefront.
