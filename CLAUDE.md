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
`index.html`'s `.news-list`, each linking to a full article page under `news/`
(e.g. `news/lab-update.html`) — no longer to WordPress. The list is a
fixed-height scroll area showing about five items. See README.md for how to
add a new one, including the article page.

Article pages in `news/` share the site header/footer with the rest of the
site (paths are one level up, e.g. `../assets/styles.css`) and use a `.prose`
div for the body. `assets/styles.css` has a "News article pages" section with
the extra rules that style them (image spacing, galleries, media-text,
blockquotes, etc.).

## Publications

`publications.html` renders `assets/publications.json` client-side. That JSON is
**generated** by `scripts/fetch_publications.py` (ORCID + Semantic Scholar +
`scripts/manual_publications.json`, merged/de-duped) and refreshed weekly by
`.github/workflows/update-publications.yml`. **Never hand-edit
`assets/publications.json`** — it is overwritten each run. Durable manual
additions go in `scripts/manual_publications.json` (or the ORCID record). No API
keys are used; everything is public/keyless.
