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
- Analytics (Google Analytics G-2ZHEXMDG0L) stays off until the visitor accepts the cookie banner. Keep the Privacy Policy in sync with any tracking change.

## Accessibility
- Keep one h1 per page, real links and buttons (no clickable divs or spans), visible focus, and alt text on every photo once real photos replace the gray placeholders.
