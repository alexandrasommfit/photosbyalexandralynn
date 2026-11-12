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
- 25% retainer, non-refundable once paid (exceptions per contract). Balance due 2 weeks before the session. Payments through Found (Pixieset is only the gallery platform). Sales tax added to invoices.
- Travel within 50 miles of Tri-Cities included.
- Analytics (Google Analytics G-2ZHEXMDG0L) loads through Google Tag Manager (GTM-M4LD8TTQ) on every page, including the hand-written `404.html`. Consent defaults in `src/partials/head.html` (copied on `404.html`) keep analytics cookies off until the visitor accepts the cookie banner. With Consent Mode v2, the Google tag still sends cookieless pings while consent is denied. Do not change that consent behavior. Keep the Privacy Policy in sync with any tracking change.
- Wedding coverage hours are Elopement 4, Classic 6, Full Day 8. Edited-image counts per package are approximate and must be re-checked if hours change.

## Service categories and site decisions (from Alexandra)
- Categories: Weddings & Engagements, Portraits (seniors, couples, individuals), Family & Maternity, Business & Commercial, and "Minis, Events & More" (seasonal minis, brand & lifestyle, events, boudoir; no public prices). Do NOT offer professional headshots (no studio or lighting setup). Commercial has no public prices: projects are quoted individually (there is no commercial pricing in Notion). New categories need a card on the home and services pages, a page in `src/pages/`, an entry in `PAGES` in `build.py`, the contact form dropdown, the Investment page, and the footer.
- The FAQ lives only on `/faq/`. Do not add a "Is the retainer refundable?" question: Alexandra does not want it. The Terms page keeps the retainer policy.
- The website says the gallery stays online 90 days. Do not mention the 12-month image backup on the site (it stays in the contracts).
- Rescheduling: portrait, family and commercial requests more than 2 weeks out are accommodated based on availability; weddings are harder to move because dates book far ahead.

## Photos
- Portfolio photos are listed in `src/photos.json` (id, category wedding/portrait/family, alt text). Web-sized copies live in `assets/photos/`.
- To add photos: add entries to `src/photos.json`, put each original's path in `tools/sources.local.json` (git-ignored, never published), run `python3 tools/photos.py`, then `python3 build.py`. Use neutral ids (like `autumn-01`) and never put client names in filenames, alt text, or any committed file: this repo is public.
- Faces must never be cut off on any screen. `python3 tools/photos.py` detects faces (Apple Vision, macOS) and stores a `focus` box per photo in `src/photos.json` (set `focus_manual` to override a miss). Every `{{photo:...}}` tag needs a slot type, `ctx=square|work|card|block`, and `build.py` uses it with the focus box to set `object-position`. Hero: `{{hero:desktop|mobile}}` switches photos by screen orientation. After adding photos or changing photo layouts, run `tools/face-check.js` (see the file header) on a local server: it must report no fails across phone, tablet, laptop and ultrawide sizes.
- Alt text describes what is in the photo (people, setting, moment). No client names, no guessed locations.
- Only publish photos of clients whose contract does not have the "do not use publicly" box checked. Confirm with Alexandra before publishing a new client's photos.
- Placements: the hero uses `{{hero:desktop-id|mobile-id}}`; other spots use `{{photo:id|sizes}}` in `src/pages/*.html` and `src/partials/footer.html`; `{{gallery}}` builds the Galleries grid and shows the category filter once more than one category has photos. Remaining gray placeholder boxes mark spots still waiting for photos.

## Accessibility
- Keep one h1 per page, real links and buttons (no clickable divs or spans), visible focus, and alt text on every photo once real photos replace the gray placeholders.
