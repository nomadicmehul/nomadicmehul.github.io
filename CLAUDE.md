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

All dynamic content loads from JSON files via `fetch()` at runtime. Each HTML page also embeds **inline fallback data** (e.g. `__inlineSpeaking`) for offline/`file://` protocol support.

### speaking.json Structure

```json
{
  "year": 2026,
  "date": "2026-03-17",
  "title": "Event Name",
  "location": "City, Country",
  "link": "https://event-url.com",
  "role": ["Speaker", "Workshop Facilitator"],
  "topics": ["Topic1", "Topic2"],
  "resources": [
    { "type": "slides", "label": "Slide Deck", "url": "filename.pdf" },
    { "type": "code", "label": "GitHub Repo", "url": "https://github.com/..." }
  ]
}
```

**Key fields:**
- `role` — String or array. Supported values: `Speaker`, `Event Organizer`, `Mentor`, `Panelist`, `Workshop Lead`, `Workshop Facilitator`
- `resources[].type` — `slides`, `code`, `demo`, `video`, `blog` (each gets a distinct color badge)
- `resources[].url` — Full URL for external links, or just a filename for slides in `assets/slides/` (auto-resolved by JS)

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

1. Drop any slide deck into `assets/slides/` (e.g. `my-talk.pdf`)
2. Add a new entry at the **top** of `data/speaking.json`:
   ```json
   {
     "year": 2026,
     "date": "2026-06-15",
     "title": "My New Talk",
     "location": "City, Country",
     "link": "https://event-link.com",
     "role": ["Speaker"],
     "topics": ["Topic1", "Topic2"],
     "resources": [
       { "type": "slides", "label": "Slide Deck", "url": "my-talk.pdf" }
     ]
   }
   ```
3. The home page shows the first 6 events; the speaking page shows all.

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
- **Inline fallback data** — `index.html` has `__inlineSpeaking`, `__inlineProjects`, `__inlineTestimonials` arrays that should be kept roughly in sync with the JSON files (used when `fetch()` fails)
- **config.json** — Controls site metadata, social links, hero content, skills section, recognition badges
- **`.nojekyll`** — Must remain in repo root so GitHub Pages serves raw HTML
- **Local dev** — Run `python3 -m http.server 8080` from project root and open `http://localhost:8080`

## Branches

- `main` — Production (deployed to GitHub Pages)
- `feature/speaking-redesign` — Speaking page overhaul with dates, roles, resource links, slides folder
