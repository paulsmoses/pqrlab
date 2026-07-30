# CLAUDE.md

Static HTML/CSS/JS site (no build step, no framework) for the PQR Lab, hosted on
GitHub Pages. Keep the repository under 1 GB.

## Conventions

- Shared assets: `assets/styles.css` and `assets/app.js`, linked with `?v=N`.
  Bump `N` in every HTML page after editing either asset — browsers cache them.
- The header and footer are duplicated in each HTML file. Change all pages
  together (e.g. a scripted find/replace) to keep them identical.
- Banners (`.hero` and `.page-head`) receive the lightning + grid overlay
  injected by `app.js`; the animation and grid styling live in `styles.css`.
  Do not hardcode the overlay markup in the HTML.
- Avatars: `.avatar[data-name]` renders an initials monogram; add
  `data-img="..."` for a photo, which falls back to the monogram on load error.

## News

The homepage is the News page. News items are `<a class="news-item">` blocks in
`index.html`'s `.news-list`, each linking to the article on WordPress
(`pqrlabmoses.wordpress.com`). Do **not** generate per-article HTML pages. To add
one, copy a block and set its `href`, date, and headline. The list is a
fixed-height scroll area showing about five items. See README.md.

## Publications

`publications.html` renders `assets/publications.json` client-side. That JSON is
**generated** by `scripts/fetch_publications.py` (ORCID + Semantic Scholar +
`scripts/manual_publications.json`, merged/de-duped) and refreshed weekly by
`.github/workflows/update-publications.yml`. **Never hand-edit
`assets/publications.json`** — it is overwritten each run. Durable manual
additions go in `scripts/manual_publications.json` (or the ORCID record). No API
keys are used; everything is public/keyless.
