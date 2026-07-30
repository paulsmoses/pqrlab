# Power Quality & Resilience Lab — website

Static site (plain HTML/CSS/JS, no build step) for the PQR Lab at the University
of Oklahoma. Hosted on GitHub Pages.

## Structure

- `index.html` — landing page: hero banner + the News feed.
- `about.html`, `faculty.html`, `members.html`, `research.html`,
  `publications.html`, `videos.html` — content pages.
- `assets/styles.css` — all styling.
- `assets/app.js` — navigation, banner effect, member photos, sponsor scrollbar.
- `assets/img/` — images (`people/`, `logos/`, `research/`, `sponsor/`).
- `scripts/` + `.github/workflows/` — the automatic publications updater.

`styles.css` and `app.js` are linked with a `?v=N` query. After editing either
file, increment `N` in the `<link>` / `<script>` tags across the HTML pages so
browsers load the new version instead of a cached copy.

> **Easiest way to make edits:** open the file on GitHub, click the ✏️ pencil,
> change the text, and click **Commit changes**. The site redeploys in about a
> minute — no local setup needed.

---

## Adding a news item

News items live in `index.html` inside `<div class="news-list">`. Each item
links out to the full article on WordPress — no new page is created.

1. Copy one existing block:

   ```html
   <a class="news-item" href="WORDPRESS-ARTICLE-URL" target="_blank" rel="noopener">
     <div class="news-date">Mon D<br>YYYY</div>
     <p>Headline text</p>
     <span class="news-arrow" aria-hidden="true">→</span>
   </a>
   ```

2. Paste it at the top of the list (newest first).
3. Change three things: the `href` (article URL), the date (keep the `<br>`),
   and the headline between `<p>` and `</p>`.
4. Save.

The list shows about five items and scrolls for the rest.

---

## Adding a group member

Members live in `members.html`. Each person is one `<div class="member">` block
inside a group (e.g. **Current PhD Students**, **Current Undergraduate
Students**).

1. In `members.html`, use **Ctrl+F** (⌘F on Mac) to find the group heading,
   e.g. `Current PhD Students`.
2. Just below it is a `<div class="grid cols-3">` holding the member cards. Copy
   one existing card:

   ```html
   <div class="member">
     <div class="top">
       <div class="avatar" data-name="Full Name"></div>
       <div><h4>Full Name</h4><p class="role">PhD Student</p></div>
     </div>
     <div class="tags"><span class="chip">Since 2025</span></div>
     <p class="bio">Short biography goes here.</p>
   </div>
   ```

3. Paste it next to the other cards and edit:
   - The **name in two places** — `data-name="Full Name"` *and* `<h4>Full Name</h4>`
   - The **role** (`<p class="role">…</p>`)
   - The **tags** — each `<span class="chip">…</span>` is one small pill; add,
     remove, or edit them
   - The **bio** (`<p class="bio">…</p>`)
4. **Photo (optional):** put a JPG in `assets/img/people/` (e.g.
   `first-last.jpg`), then add `data-img` to the avatar:

   ```html
   <div class="avatar" data-name="Full Name" data-img="assets/img/people/first-last.jpg"></div>
   ```

   With no `data-img`, the person automatically gets a colored circle with their
   initials.
5. Update the count next to the group heading — find
   `<h3>Current PhD Students</h3><span class="count">3</span>` and change the
   number.
6. Save.

**To remove a member:** delete that whole `<div class="member"> … </div>` block
(see "Removing an element" below) and lower the count number.

Past-scholar cards additionally have a `<button class="readmore-btn">` and a
`<span class="more">` for the expandable text — keep those tags if you copy one.

---

## Publications

The Publications page builds its list **automatically** from Dr. Moses's **ORCID**
and **Semantic Scholar** records, refreshed every week by a GitHub Action. In
normal use there is nothing to maintain here.

**If a paper is missing**, there are two ways to add it:

1. **Add it to the ORCID record** (the lasting fix). It appears on the next
   weekly refresh — no site edit needed.
2. **Add it directly on the site** — edit `scripts/manual_publications.json`.
   This file is merged in on every refresh, so entries here are never lost. Put
   each paper between the `[ ]`, separated by commas:

   ```json
   [
     {
       "title": "Full paper title",
       "year": 2026,
       "venue": "Conference or journal name",
       "authors": "A. Author, P. Moses",
       "url": "https://doi.org/10.xxxx/xxxxx"
     }
   ]
   ```

   Keep the quotes and commas exactly as shown. `url` can be a DOI link or any
   link to the paper.

> **Do not** hand-edit `assets/publications.json` — that file is regenerated
> automatically and your change would be overwritten. Use
> `manual_publications.json` instead.

A manual addition (or a new ORCID paper) goes live on the next weekly run. To
publish it immediately, trigger the updater by hand: repo **Actions** tab →
**Update publications** → **Run workflow**.

---

## Editing text or removing anything (general)

Every page is made of **elements** wrapped in tags — for example `<p>…</p>` for a
paragraph, `<div>…</div>` for a block, `<section>…</section>` for a whole
section. Each opening tag like `<div …>` has a matching closing tag `</div>`.

### Change wording

1. Open the `.html` file for that page.
2. Press **Ctrl+F** (⌘F on Mac) and type the words you see on the site.
3. Edit the text that sits **between** the tags (between a `>` and the next `<`),
   then save. Example — to change the phone number, search for
   `(405) 325-2969` and type the new one in its place.

Leave the tags themselves (`<p>`, `<div ...>`, etc.) alone; just change the words.

### Remove an element or section

To remove something, delete it **from its opening tag through its matching
closing tag**, together. Deleting only one half breaks the page layout.

1. **Ctrl+F** for some text inside the thing you want to remove.
2. Scroll **up** to its opening tag (e.g. `<div class="...">`) and **down** to
   the matching closing tag (`</div>`).
3. Select and delete everything from the opening tag to the closing tag,
   inclusive. (Most editors highlight the matching tag when you click on one,
   which makes the pair easy to spot.)

### Safe-editing tips

- Don't change the top of each page (the `<head>` block and the header/nav menu)
  unless you mean to — those load the shared styling and the navigation.
- Save, then check it (locally with the preview server below, or after pushing).
- If a page looks broken, it's almost always a missing `</...>` closing tag or a
  deleted `<` / `>`. Undo (⌘Z / Ctrl+Z) and try again.

---

## Local preview

Relative paths need an HTTP server (not `file://`). From the project folder:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000/. Press **Ctrl+C** in that terminal to stop it.

## Hosting

GitHub Pages, serving these files directly. Keep the repository under 1 GB.
