# Photos by Alexandra Lynn (photosbyalexandralynn.com)

Static site on Netlify, deployed from `main` on GitHub (alexandrasommfit/photosbyalexandralynn). No build step on Netlify: generated files are committed.

## Editing
- Page content: `src/pages/*.html`. Shared head, nav, footer, cookie banner: `src/partials/`. Styles: `assets/site.css`. Behavior: `assets/site.js`.
- Page titles, descriptions and the nav highlight live in the `PAGES` table in `build.py`.
- After any edit run `python3 build.py`, which regenerates `index.html`, `<page>/index.html` and `sitemap.xml`. Never hand-edit the generated HTML; it is overwritten.
- Preview: `python3 -m http.server 8000`, then open http://localhost:8000.
- Always ask before pushing: a push to `main` goes live.

## Brand rules
- Colors (brand guide only): Navy #15232B, Dusty Blue #8FB2C4, Pale Blue #DDE8EC, Cream #F7F5F1, Ink #2B3540 (plus white). Do not introduce other colors.
- Dusty Blue fails contrast as text on light backgrounds. Use Navy or Ink for text; Dusty Blue for fills, borders and decoration, with Navy text on top.
- Voice: first person ("I"), warm, never salesy. Business name is "Photos by Alexandra Lynn" (Lynn).
- Never invent testimonials, photo counts, prices or policies. Policies come from the signed contract templates in Drive.

## Policies that must stay consistent (site, contracts, invoice, emails)
- 25% retainer, non-refundable once paid (exceptions per contract). Balance due 2 weeks before the session. Payments through Pixieset. Sales tax added to invoices.
- Travel within 50 miles of Tri-Cities included.
- Analytics (Google Analytics G-2ZHEXMDG0L) loads through Google Tag Manager (GTM-M4LD8TTQ) and stays off until the visitor accepts the cookie banner (consent defaults are set in `src/partials/head.html`). Keep the Privacy Policy in sync with any tracking change.
- Wedding coverage hours are Elopement 4, Classic 6, Full Day 8. Edited-image counts per package are approximate and must be re-checked if hours change.

## Photos
- Portfolio photos are listed in `src/photos.json` (id, category wedding/portrait/family, alt text). Web-sized copies live in `assets/photos/`.
- To add photos: add entries to `src/photos.json`, put each original's path in `tools/sources.local.json` (git-ignored, never published), run `python3 tools/photos.py`, then `python3 build.py`. Use neutral ids (like `autumn-01`) and never put client names in filenames, alt text, or any committed file: this repo is public.
- Alt text describes what is in the photo (people, setting, moment). No client names, no guessed locations.
- Only publish photos of clients whose contract does not have the "do not use publicly" box checked. Confirm with Alexandra before publishing a new client's photos.
- Placements: the hero uses `{{hero:desktop-id|mobile-id}}`; other spots use `{{photo:id|sizes}}` in `src/pages/*.html` and `src/partials/footer.html`; `{{gallery}}` builds the Galleries grid and shows the category filter once more than one category has photos. Remaining gray placeholder boxes mark spots still waiting for photos.

## Accessibility
- Keep one h1 per page, real links and buttons (no clickable divs or spans), visible focus, and alt text on every photo once real photos replace the gray placeholders.
