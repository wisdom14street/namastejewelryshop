# namastejewelryshop.com

Namaste Jewelry Shop: static storefront built daily from the public namastebookshop.com catalog and deployed to GitHub Pages.
Namaste Jewelry Shop is a brand of Wealth Edge Ventures Inc.

- `site/config.json`: site settings. Set `REVIEW_URL` (Google review link) to show the "Review us on Google" button and QR code; set `GOOGLE_SITE_VERIFICATION` to the Search Console HTML-tag value. Both stay hidden while empty. `kinds`, `max_price` and `best_collections` limit what the daily pickup and best-seller checks fetch.
- `site/sitecopy.py`: aisles, product mix rules and all copy for this site.
- `site/theme.css`, `site/favicon.svg`: this site's design.
- `scripts/`: shared jewelry/bead engine (fetch with pagination and 429 backoff, Shopify pickup check, best sellers, build).
- Checkout: the on-site cart opens a multi-item Shopify cart permalink on `namastebookshop.com`. It sends `attributes[Storefront]=Namaste Jewelry Shop`, `attributes[Site]=namastejewelryshop.com`, an order note and `ref=namastejewelryshop`. These are source markers, not Shopify order tags or evidence that a purchase completed. See [Shopify's permalink documentation](https://shopify.dev/docs/apps/build/checkout/create-cart-permalinks).

## Measurement

The existing GA4 property is configured by `GA_MEASUREMENT_ID` in `site/config.json`. Production pages load one Google tag; preview builds omit it. Product views, accepted cart additions and checkout clicks use the existing event handlers. A `begin_checkout` event records a handoff, not a paid order. Do not add a storefront `purchase` event: only a verified completed order from Shopify should supply that event, with a transaction ID and deduplication.

Use GA4 reports filtered to hostname `namastejewelryshop.com` for visitors and page views. Confirm report access and actual event receipt; installing a tag alone does not prove either. Use Shopify order details to verify the `Storefront` and `Site` attributes and referral code, and distinguish paid, cancelled, refunded and test orders. A missing marker does not prove this storefront played no part in a customer's visit. Cross-domain sessions, purchase tracking and consent behavior on the checkout store require separate verification in Shopify and GA4; this static site cannot establish them.

## Verification

Run `node --test tests/*.test.cjs` and `python3 -m unittest discover -s tests -p '*_test.py'` with Node 24 and Python 3.12. The Python tests build temporary sites from synthetic fixtures, including a catalog without images; they never fetch or publish products. Both suites run before the daily production fetch and deployment.
