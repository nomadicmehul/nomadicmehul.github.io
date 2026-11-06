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
├── studio.html             # Content Studio: add/edit speaking events (calendar, live preview) → opens a pre-filled GitHub issue
├── demo-studio.html        # Demo Studio: create/update a separate repo per workshop/talk demo (see "Demo repos")
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
│   ├── events/             # Event files, one folder per event: <year>/<date>-<title-slug>/ (managed by event_files.py)
│   ├── og-image.png        # Link-preview image (generated — see below)
│   └── Mehul_Patel_Resume.pdf
│
└── .github/
    ├── ISSUE_TEMPLATE/     # Issue forms: add + update/remove (generated) for speaking events, projects, testimonials
    ├── scripts/            # issue_to_data.py, event_files.py, build_manage.py, stamp_dates.py, sync_medium.py, check_links.py
    └── workflows/          # deploy.yml, issue-to-data.yml, sync-medium.yml, check-links.yml, edit-forms.yml, labels.yml, auto-assign.yml (assigns new PRs to the repo owner)
```

## Data-Driven Architecture

All dynamic content loads from JSON files via `fetch()` at runtime. The JSON files under `data/` are the **single source of truth** — there is no duplicated inline copy to keep in sync. Because the pages use `fetch()`, they must be served over HTTP (use the local dev server below); opening the raw HTML via `file://` will not load the dynamic content. GitHub Pages sends `Cache-Control: max-age=600`, so every data fetch uses `fetch('data/…', { cache: 'no-cache' })`: the browser revalidates (cheap `304` when unchanged) and a refresh shows new entries right after a deploy instead of up to 10 minutes later.

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
    { "type": "slides", "label": "Slide Deck", "url": "assets/events/2026/2026-03-17-event-name/my-talk.pdf" },
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
| `slides` | Purple | PowerPoint | `assets/events/...` path or full URL | Slide decks — stored per event in `assets/events/` |
| `code` | Blue | GitHub | Full URL (`https://github.com/...`) | Source code, GitHub repos, demos |
| `demo` | Cyan | Play circle | Full URL (`https://...`) | Live demo links, deployed apps |
| `video` | Red | Video | Full URL (`https://youtube.com/...`) | Talk recordings, YouTube links |
| `blog` | Amber | Blog | Full URL (`https://...`) | Blog posts, write-ups, Medium articles |

**URL resolution** (`resolveUrl()` in `speaking.html` and `index.html`): full URLs are used as-is; a URL starting with `assets/` is a path from the site root; a bare filename resolves to `assets/slides/<name>` (legacy). `.pptx`/`.ppt` links open in Office's online viewer, since browsers can only download them.

**Event files** (`.github/scripts/event_files.py`): every local file belongs in `assets/events/<year>/<date>-<title-slug>/` (slug ≤ 60 chars). `organize()` downloads GitHub issue attachments (`github.com/user-attachments/...`, which GitHub serves with `Content-Disposition: attachment`, i.e. they download instead of opening) and copies local files whose folder no longer matches (title/date changed); `prune()` deletes files no event links to any more. `issue-to-data.yml` runs it per submission and `edit-forms.yml` runs it over all events after a direct push. Deploy fails if a linked local file is missing. The Studio's `slug()` mirrors the Python one to show the folder.

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

**Content Studio** (`studio.html`, noindex, not in the nav) is the friendliest path for speaking events: calendar, role chips, topic suggestions, location autocomplete (past locations, then cities from the free no-key Open-Meteo geocoding API, with country names mapped to the spelling already in speaking.json via `COUNTRY_NAMES`), live card preview, edit-with-diff and remove. It opens `/issues/new?labels=…&title=…&body=…` with a body in the same `### Label` format the issue forms produce (issue-form URL pre-fill only covers text fields, so roles couldn't be pre-filled). Resources go in an `Add resources` section as `type | label | url` lines (also accepted by the add form); a file upload is a `slides | ` line, listed last, that the owner drops the file onto. `parse_form()` strips `<!-- -->` hint comments, and a bare link on a line after an empty `type |` line attaches to it.

With **Connect GitHub** (classic `public_repo` token in `localStorage` key `studio-github-token`, shared with Demo Studio) the Studio skips the issue: `publish()` reads `data/speaking.json` from `main` via the contents API, applies the add/update/remove the way `issue_to_data.py` would (newest-first sort, `role` defaults to Speaker, files to `assets/events/<year>/<date>-<slug>/`, unreferenced event files deleted), and writes everything in one Git Data API commit to `main`. That push triggers `edit-forms.yml` (dates, MANAGE.md, moving files after a title/date change) and `deploy.yml`, whose run for the commit the page waits on. `JSON.stringify(data, null, 2) + "\n"` matches Python's `json.dumps(indent=2, ensure_ascii=False)` byte for byte.

Or open a new issue and pick an **Add …** or **Update or remove …** form for speaking events, projects or testimonials (labels `data:speaking`, `data:project`, `data:testimonial`, `data:edit` are created by `labels.yml`). On submit, `.github/workflows/issue-to-data.yml`:

1. Parses the form with `.github/scripts/issue_to_data.py` and validates it (dates, URLs, duplicates)
2. Commits the change to the matching `data/*.json` file on `main` (speaking events are kept sorted newest-first by `date`)
3. Triggers `deploy.yml`, comments the added JSON on the issue, and closes it

If validation fails, the errors are posted on the issue — edit the issue and it re-runs. Only issues opened by the repo **owner** are processed. Files dragged into the issue are saved to the event's folder (see Event files above). Dates accept `YYYY-MM-DD` or written-out forms (`9 Jun 2026`, `Jun 9th, 2026`, `09.06.2026`; see `parse_date()`).

**`MANAGE.md`** (repo root, linked from the issue-template chooser) is the admin index: all entries, with speaking events grouped by year → month, recent activity by month, and per-entry **Update / Remove** links. Those links open `update-*.yml` with the `entry` text field pre-filled via URL query params (`?template=…&entry=<label>`); labels come from `entry_labels()` in `issue_to_data.py` (speaking: `Title (YYYY-MM-DD)`). Typed values also match: exact title, or a unique substring.

`MANAGE.md`, the `update-*.yml` forms (each type's own fields from `TYPES[...]["edit_inputs"]`; blank = keep) and the role checkboxes in `add-speaking-event.yml` are **generated** by `.github/scripts/build_manage.py`. Don't hand-edit them.

**Entry dates:** every speaking event, project and testimonial has `added` and `updated` (`YYYY-MM-DD`), maintained by `.github/scripts/stamp_dates.py` (it compares with the previous commit; `--backfill` rebuilds them from git history). Entries are identified by speaking: title + year, project: repo, testimonial: quote.

Both are run in the same commit by `issue-to-data.yml`, and by `edit-forms.yml` when `data/*.json` is pushed directly (which also redeploys).

## Demo repos (Demo Studio)

`demo-studio.html` makes one public repo per workshop/talk demo, from the template repo **`nomadicmehul/event-demo-template`**, whose files live here in `.github/event-repo-template/` (not deployed: Pages skips dotfiles). Changing the template means pushing that folder to the template repo again (see README → Demo Studio → One-time setup); existing demo repos keep their copy.

- **Create:** `github.com/new?template_owner=…&template_name=event-demo-template&name=…&description=…&visibility=…` (documented URL params). The description starts with `🎤 `; that's how "Update a repo" tells demo repos apart (`/users/nomadicmehul/repos`, unauthenticated, 60 req/h). The page polls `/repos/…` until the repo exists, then step 2 opens `/<repo>/issues/new?title=[event] …&body=…`.
- **In each demo repo:** `.github/workflows/event-info.yml` runs `.github/scripts/event_info.py` on owner-opened issues titled `[event]…` (labels can't be used: the repo has none yet), on pushes to `event.json` (re-render only), and never in the template itself (`repository.is_template`). It writes `event.json`, downloads dropped files to `event/` (poster as `event/poster.*`), rewrites only the README between `<!-- event:start` and `<!-- event:end -->`, comments and closes. Blank field = keep, `-` = clear; `Files` lists `event/` paths to keep plus new drops, and unlisted files are deleted.
- **Update:** loads `event.json` via the contents API (`Accept: application/vnd.github.raw+json`) and sends only changed fields.
- **Connect GitHub (optional, recommended):** a classic token with `public_repo` (checked via `/user` and `X-OAuth-Scopes`), kept in `localStorage`/`sessionStorage` under `demo-studio-token`. Then files are picked on the page and nothing goes through an issue: `POST /repos/…/event-demo-template/generate`, wait for `git/ref/heads/main`, then one Git Data API commit (`plan()` builds event.json the same way `event_info.py` does, plus blobs for new files and `sha: null` entries for deleted ones). That push changes `event.json`, so the repo's workflow renders the README; the page waits for the run with `actions/runs?head_sha=`. `cleanName()` mirrors `clean_name()` in `event_info.py`.
- **Step 3** links to `studio.html?new=1&title=&date=&location=&topics=&event=&code=`, which `prefill()` in studio.html turns into a new speaking event.
- `LINK_TYPES` (Python) and `LINKS` (page), and the location autocomplete code in both studios, are kept in sync by hand.

## Link Checking

`.github/workflows/check-links.yml` runs `.github/scripts/check_links.py` every Monday (or manually). It checks every URL in `data/*.json` plus local event files, and keeps one open **Broken links report** issue updated, closing it once all links work. Only 404/410, unresolvable domains and missing event files count as broken; bot-blocking responses (403/429/timeouts) are listed as "couldn't verify".

## Blog (Medium)

Browsers can't read Medium's RSS directly (no CORS) and the `rss2json` proxy is behind a Cloudflare challenge, so `.github/workflows/sync-medium.yml` fetches the feed daily (06:00 UTC, or run it manually) and merges it into `data/blog.json`, which `blog.html` and the home page read. Medium's feed only holds the latest ~10 posts; older ones are kept because the sync merges by link.

Commits made by workflows with `GITHUB_TOKEN` don't trigger other workflows, so both data workflows start `deploy.yml` explicitly via `gh workflow run`.

## Adding a New Speaking Event (manually)

1. (Optional) Drop any slide deck into `assets/slides/` and use its bare filename; on push, `edit-forms.yml` moves it into `assets/events/<year>/<date>-<title>/` and rewrites the URL
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
- **Link-preview image** — `assets/og-image.png` (1200×630) is rendered from `.github/og-card/card.html` by `.github/og-card/render.sh` (headless Chrome). All pages' `og:image`/`twitter:image` point at it. When titles, recognitions or headline stats change, update `card.html` and re-run the script; LinkedIn caches previews, so refresh with its Post Inspector.
- **Self-contained pages** — each HTML file carries its own inline CSS and JS (matrix rain, nav, etc.); there is no shared stylesheet/script. Personal content (hero, about, skills, Awards & Community Roles, ticker, social links) is hardcoded in `index.html`.
- **Deploys via GitHub Actions** (Pages source = GitHub Actions), so no Jekyll runs and `.nojekyll` isn't needed. `upload-pages-artifact` v4+ skips dotfiles, so don't rely on any dotfile being served.
- **Local dev** — Run `python3 -m http.server 8080` from project root and open `http://localhost:8080`

## Security notes

- **Escape everything rendered from `data/*.json`.** Pages build HTML with template strings + `innerHTML`, so every data field goes through `esc()` and every data URL through `safeUrl()` (only `http(s)://` or `assets/…`). `blog.json` is generated from Medium's RSS: an article that quotes HTML code would otherwise become live HTML on the site, i.e. script running on the same origin as the studios' GitHub token.
- **Studio token** (`localStorage` `studio-github-token`, shared by both studios): never committed or sent anywhere but api.github.com; ignored when the page is framed; the banner warns if it has scopes beyond `public_repo` and links to github.com/settings/tokens to revoke. *Disconnect* only removes it from the browser.
- Pages load no third-party JavaScript (only Google Fonts / FontAwesome CSS); keep it that way, since any script on the origin can read the token.
- Issue workflows only act on issues whose author is the repo **owner**; issue bodies reach scripts through env vars, never `${{ }}` inside `run:`.

## Commit Messages

- Do **not** add `Co-Authored-By` or any Claude/AI attribution lines to commit messages.

## Branches

- `main` — Production (deployed to GitHub Pages on every push)
- Work on a feature branch and open a PR; PRs are auto-assigned to the repo owner
