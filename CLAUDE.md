# CLAUDE.md - Project Guide

## Project Overview

Personal portfolio website for Mehul Patel — a static HTML/CSS/JS site deployed on GitHub Pages with a terminal/hacker aesthetic theme.

**URL:** https://nomadicmehul.github.io
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
├── 404.html                # Custom 404 page
├── config.json             # Site-wide configuration (metadata, social links, hero, skills)
├── robots.txt              # SEO
├── sitemap.xml             # SEO
├── .nojekyll               # Disables Jekyll on GitHub Pages
│
├── data/
│   ├── speaking.json       # All speaking events (source of truth)
│   ├── projects.json       # Featured projects
│   └── testimonials.json   # Testimonials
│
├── assets/
│   ├── css/styles.css      # Shared base styles
│   ├── js/main.js          # Core utilities (matrix rain, nav, config loader)
│   ├── img/profile.jpg     # Profile photo
│   ├── favicon.svg         # SVG favicon (terminal prompt)
│   ├── slides/             # Slide decks for speaking events (PDF/PPTX)
│   └── Mehul_Patel_Resume.pdf
│
├── _pages/                 # Markdown content pages (about, blog, etc.)
└── .github/                # GitHub workflows
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

The `role` field accepts a single string or an array of strings.

| Role | Badge Color | Icon |
|------|-------------|------|
| `Speaker` | Green | Microphone |
| `Event Organizer` | Amber | Users-cog |
| `Mentor` | Purple | Chalkboard |
| `Panelist` | Cyan | Comments |
| `Workshop Lead` | Blue | Laptop |
| `Workshop Facilitator` | Blue | Laptop |

### projects.json Structure

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

## Adding a New Speaking Event

1. (Optional) Drop any slide deck into `assets/slides/` (e.g. `my-talk.pdf`)
2. Add a new entry at the **top** of `data/speaking.json`:
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
- **Single source of truth** — content lives only in the `data/*.json` files; edit those and the pages pick it up via `fetch()`. There is no inline duplicate to update. (The `blog.html` `__inlineBlog` array is a genuine fallback for the external Medium RSS feed, which can fail — that one stays.)
- **config.json** — Controls site metadata, social links, hero content, skills section, recognition badges
- **`.nojekyll`** — Must remain in repo root so GitHub Pages serves raw HTML
- **Local dev** — Run `python3 -m http.server 8080` from project root and open `http://localhost:8080`

## Commit Messages

- Do **not** add `Co-Authored-By` or any Claude/AI attribution lines to commit messages.

## Branches

- `main` — Production (deployed to GitHub Pages)
- `feature/speaking-redesign` — Speaking page overhaul with dates, roles, resource links, slides folder
