# CLAUDE.md - Project Guide

## Project Overview

Personal portfolio website for Mehul Patel — a static HTML/CSS/JS site deployed on GitHub Pages with a terminal/hacker aesthetic theme.

**URL:** https://nomadicmehul.dev (custom domain via `CNAME`; nomadicmehul.github.io redirects here)
**Hosting:** GitHub Pages (no build step)
**Framework:** None — pure vanilla HTML, CSS, JavaScript

## Tech Stack

- **HTML5** — Static pages, no templating engine
- **CSS3** — Custom properties (variables), Grid, Flexbox, animations
- **Vanilla JS** — Fetch API, IntersectionObserver, Canvas (matrix rain)
- **Fonts:** Inter (sans-serif), JetBrains Mono (mono) via Google Fonts
- **Icons:** FontAwesome 6.5.1 via CDN
- **No npm/node/build tools** — everything is client-side

## Project Structure

```
/
├── index.html              # Main portfolio page (~2300 lines, self-contained)
├── speaking.html           # Speaking engagements timeline page
├── projects.html           # Open-source projects grid page
├── blog.html               # Medium articles page
├── 404.html                # Custom 404 page
├── MANAGE.md               # Generated admin index: all entries by year/month + update/remove links
├── robots.txt              # SEO
├── sitemap.xml             # SEO
│
├── data/
│   ├── speaking.json       # All speaking events (source of truth)
│   ├── projects.json       # Featured projects
│   ├── testimonials.json   # Testimonials
│   ├── roles.json          # Speaking role list (name, icon, color) — single source for pages + forms
│   └── blog.json           # Medium posts — auto-synced, don't hand-edit
│
├── assets/
│   ├── img/profile.jpg     # Profile photo
│   ├── favicon.svg         # SVG favicon (terminal prompt)
│   ├── slides/             # Slide decks for speaking events (PDF/PPTX)
│   └── Mehul_Patel_Resume.pdf
│
└── .github/
    ├── ISSUE_TEMPLATE/     # Issue forms: add + update/remove (generated) for speaking events, projects, testimonials
    ├── scripts/            # issue_to_data.py, build_manage.py, stamp_dates.py, sync_medium.py, check_links.py
    └── workflows/          # deploy.yml, issue-to-data.yml, sync-medium.yml, check-links.yml, edit-forms.yml, labels.yml, auto-assign.yml (assigns new PRs to the repo owner)
```

## Data-Driven Architecture

All dynamic content loads from JSON files via `fetch()` at runtime. The JSON files under `data/` are the **single source of truth** — there is no duplicated inline copy to keep in sync. Because the pages use `fetch()`, they must be served over HTTP (use the local dev server below); opening the raw HTML via `file://` will not load the dynamic content.

### speaking.json Structure

```json
{
  "year": 2026,
  "date": "2026-03-17",
  "title": "Event Name",
  "location": "City, Country",
  "role": ["Speaker", "Workshop Facilitator"],
  "topics": ["Topic1", "Topic2"],
  "resources": [
    { "type": "event", "label": "Event Page", "url": "https://event-page.com" },
    { "type": "slides", "label": "Slide Deck", "url": "my-talk.pdf" },
    { "type": "code", "label": "GitHub Repo", "url": "https://github.com/..." }
  ]
}
```

**Fields:**

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `year` | Yes | Number | Event year (used for grouping and year filter) |
| `date` | Yes | String | `YYYY-MM-DD` format (displayed on card) |
| `title` | Yes | String | Event name |
| `location` | Yes | String | City, Country |
| `role` | No | String or Array | Your role(s) at the event — renders as badge(s) |
| `topics` | Yes | Array | Topic tags displayed on the card |
| `resources` | Yes | Array | Links and files — renders as colored action buttons |
| `added` / `updated` | Auto | String | `YYYY-MM-DD`, stamped by `stamp_dates.py` — don't set by hand |

### Resource Types

Each resource is an object with `type`, `label`, and `url`.

| Type | Badge Color | Icon | URL Format | Use For |
|------|-------------|------|------------|---------|
| `event` | Green | External link | Full URL (`https://...`) | Link to the event page or registration |
| `slides` | Purple | PowerPoint | Filename (`talk.pdf`) or full URL | Slide decks — local files go in `assets/slides/` |
| `code` | Blue | GitHub | Full URL (`https://github.com/...`) | Source code, GitHub repos, demos |
| `demo` | Cyan | Play circle | Full URL (`https://...`) | Live demo links, deployed apps |
| `video` | Red | Video | Full URL (`https://youtube.com/...`) | Talk recordings, YouTube links |
| `blog` | Amber | Blog | Full URL (`https://...`) | Blog posts, write-ups, Medium articles |

**URL resolution:** If a URL does NOT start with `http://` or `https://`, it is treated as a local file in `assets/slides/` (e.g. `"url": "my-talk.pdf"` resolves to `assets/slides/my-talk.pdf`). Full URLs are used as-is.

**Example with all resource types:**
```json
{
  "resources": [
    { "type": "event", "label": "Event Page", "url": "https://conf.example.com" },
    { "type": "slides", "label": "Slide Deck", "url": "my-talk-2026.pdf" },
    { "type": "code", "label": "GitHub Repo", "url": "https://github.com/user/repo" },
    { "type": "demo", "label": "Live Demo", "url": "https://demo.example.com" },
    { "type": "video", "label": "Recording", "url": "https://youtube.com/watch?v=..." },
    { "type": "blog", "label": "Blog Post", "url": "https://medium.com/@user/post" }
  ]
}
```

### Role Types

The `role` field accepts a single string or an array of strings. The list of roles lives in **`data/roles.json`**, the one place to add, rename or recolor a role:

```json
{ "name": "Keynote Speaker", "icon": "fas fa-star", "color": "red" }
```

- `icon`: any FontAwesome 6 class
- `color`: `green`, `amber`, `purple`, `cyan`, `blue`, `red` or `default` (grey)

Both pages render badges from it, and the role checkboxes in the **Add speaking event** and **Update or remove speaking event** issue forms are regenerated from it automatically. Deploy fails if an event uses a role that isn't in `roles.json`.

Current roles: Speaker (green), Event Organizer (amber), Mentor (purple), Panelist (cyan), Workshop Lead and Workshop Facilitator (blue).

### projects.json Structure

`featured: true` projects show on the home page. On the Projects page the Featured badge/count only appear when some projects are *not* featured. 2 or 4 cards lay out as a 2×2 grid instead of leaving one card alone on a row.

```json
{
  "title": "Project Name",
  "description": "Description",
  "icon": "fas fa-cloud",
  "iconColor": "#0078d4",
  "repo": "https://github.com/...",
  "tech": ["Azure", "Python"],
  "featured": true
}
```

## Updating Content via GitHub Issues (recommended)

Open a new issue and pick an **Add …** or **Update or remove …** form for speaking events, projects or testimonials (labels `data:speaking`, `data:project`, `data:testimonial`, `data:edit` are created by `labels.yml`). On submit, `.github/workflows/issue-to-data.yml`:

1. Parses the form with `.github/scripts/issue_to_data.py` and validates it (dates, URLs, duplicates)
2. Commits the change to the matching `data/*.json` file on `main` (speaking events are kept sorted newest-first by `date`)
3. Triggers `deploy.yml`, comments the added JSON on the issue, and closes it

If validation fails, the errors are posted on the issue — edit the issue and it re-runs. Only issues opened by the repo **owner** are processed. Slides referenced by filename must already exist in `assets/slides/` (or paste a full URL / drag the file into the field to get a GitHub attachment URL).

**`MANAGE.md`** (repo root, linked from the issue-template chooser) is the admin index: all entries, with speaking events grouped by year → month, recent activity by month, and per-entry **Update / Remove** links. Those links open `update-*.yml` with the `entry` text field pre-filled via URL query params (`?template=…&entry=<label>`); labels come from `entry_labels()` in `issue_to_data.py` (speaking: `Title (YYYY-MM-DD)`). Typed values also match: exact title, or a unique substring.

`MANAGE.md`, the `update-*.yml` forms (each type's own fields from `TYPES[...]["edit_inputs"]`; blank = keep) and the role checkboxes in `add-speaking-event.yml` are **generated** by `.github/scripts/build_manage.py`. Don't hand-edit them.

**Entry dates:** every speaking event, project and testimonial has `added` and `updated` (`YYYY-MM-DD`), maintained by `.github/scripts/stamp_dates.py` (it compares with the previous commit; `--backfill` rebuilds them from git history). Entries are identified by speaking: title + year, project: repo, testimonial: quote.

Both are run in the same commit by `issue-to-data.yml`, and by `edit-forms.yml` when `data/*.json` is pushed directly (which also redeploys).

## Link Checking

`.github/workflows/check-links.yml` runs `.github/scripts/check_links.py` every Monday (or manually). It checks every URL in `data/*.json` plus local slide files, and keeps one open **Broken links report** issue updated, closing it once all links work. Only 404/410, unresolvable domains and missing slide files count as broken; bot-blocking responses (403/429/timeouts) are listed as "couldn't verify".

## Blog (Medium)

Browsers can't read Medium's RSS directly (no CORS) and the `rss2json` proxy is behind a Cloudflare challenge, so `.github/workflows/sync-medium.yml` fetches the feed daily (06:00 UTC, or run it manually) and merges it into `data/blog.json`, which `blog.html` and the home page read. Medium's feed only holds the latest ~10 posts; older ones are kept because the sync merges by link.

Commits made by workflows with `GITHUB_TOKEN` don't trigger other workflows, so both data workflows start `deploy.yml` explicitly via `gh workflow run`.

## Adding a New Speaking Event (manually)

1. (Optional) Drop any slide deck into `assets/slides/` (e.g. `my-talk.pdf`)
2. Add the entry to `data/speaking.json`, newest first (don't add `added`/`updated`; they're stamped on push):
   ```json
   {
     "year": 2026,
     "date": "2026-06-15",
     "title": "My New Talk",
     "location": "City, Country",
     "role": ["Speaker"],
     "topics": ["Topic1", "Topic2"],
     "resources": [
       { "type": "event", "label": "Event Page", "url": "https://event-link.com" },
       { "type": "slides", "label": "Slide Deck", "url": "my-talk.pdf" },
       { "type": "code", "label": "GitHub Repo", "url": "https://github.com/user/repo" }
     ]
   }
   ```
3. The home page shows the first 6 events; the speaking page shows all.
   Events dated today or later get an amber **Upcoming** badge automatically (no field needed).
4. Only add the resources you have — empty `"resources": []` is fine too.

## Color Palette (Terminal Theme)

| Token | Color | Usage |
|-------|-------|-------|
| `--term-green` | `#4ade80` | Primary accent, links, Speaker badge |
| `--term-amber` | `#fbbf24` | Dates, Organizer badge, blog links |
| `--term-cyan` | `#22d3ee` | Panelist badge, demo links |
| `--term-red` | `#f87171` | Video links |
| `--term-purple` | `#c084fc` | Mentor badge, slides links |
| `--term-blue` | `#60a5fa` | Workshop badge, code links |
| `--bg-primary` | `#0a0e17` | Page background |
| `--bg-card` | `#111827` | Card background |

## Important Notes

- **No build step** — edit HTML/CSS/JS directly, push, and GitHub Pages serves it
- **Single source of truth** — content lives only in the `data/*.json` files; edit those and the pages pick it up via `fetch()`. There is no inline duplicate to update.
- **Self-contained pages** — each HTML file carries its own inline CSS and JS (matrix rain, nav, etc.); there is no shared stylesheet/script. Personal content (hero, about, skills, Awards & Community Roles, ticker, social links) is hardcoded in `index.html`.
- **Deploys via GitHub Actions** (Pages source = GitHub Actions), so no Jekyll runs and `.nojekyll` isn't needed. `upload-pages-artifact` v4+ skips dotfiles, so don't rely on any dotfile being served.
- **Local dev** — Run `python3 -m http.server 8080` from project root and open `http://localhost:8080`

## Commit Messages

- Do **not** add `Co-Authored-By` or any Claude/AI attribution lines to commit messages.

## Branches

- `main` — Production (deployed to GitHub Pages on every push)
- Work on a feature branch and open a PR; PRs are auto-assigned to the repo owner
