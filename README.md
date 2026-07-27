# Power Quality & Resilience Lab — website

Static site (plain HTML/CSS/JS, no build step) for the PQR Lab at the University
of Oklahoma. Hosted on GitHub Pages.

## Structure

- `index.html` — landing page: hero banner + the News feed.
- `about.html`, `faculty.html`, `members.html`, `research.html`,
  `publications.html`, `videos.html` — content pages.
- `assets/styles.css` — all styling.
- `assets/app.js` — navigation, banner lightning effect, member photos.
- `assets/img/` — images (`people/`, `logos/`).

`styles.css` and `app.js` are linked with a `?v=N` query. After editing either
file, increment `N` in the `<link>` / `<script>` tags across the HTML pages so
browsers load the new version instead of a cached copy.

## Adding a news item

News items live in `index.html` inside `<div class="news-list">`. Each item is a
single block that links out to the full article on the WordPress site — no new
page is created. It works like filling in a template: copy a block, change the
text between the tags, and leave the structure as-is.

1. Copy one existing block:

   ```html
   <a class="news-item" href="WORDPRESS-ARTICLE-URL" target="_blank" rel="noopener">
     <div class="news-date">Mon D<br>YYYY</div>
     <p>Headline text</p>
     <span class="news-arrow" aria-hidden="true">→</span>
   </a>
   ```

2. Paste it at the top of the list (newest first).
3. Change three things:
   - `href` → the article's URL on WordPress
   - the date (keep the `<br>` between the day and the year)
   - the headline between `<p>` and `</p>`
4. Save.

The list shows about five items and scrolls for the rest, so it stays compact as
it grows.

## Local preview

Relative paths need an HTTP server (not `file://`). From the project folder:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000/.

## Hosting

GitHub Pages, serving these files directly. Keep the repository under 1 GB.
