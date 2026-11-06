<div align="center">

# `root@you:~#` Terminal Portfolio Theme

A Linux terminal-inspired portfolio theme for developers, DevOps engineers, and open-source enthusiasts. Dark mode. Matrix rain. CRT scanlines. Built to make your work look as cool as you are.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-blue.svg)](https://pages.github.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/nomadicmehul)

[Live Demo](https://nomadicmehul.dev) · [Report Bug](https://github.com/nomadicmehul/nomadicmehul.github.io/issues) · [Request Feature](https://github.com/nomadicmehul/nomadicmehul.github.io/issues)

</div>

---

## Updating Content (no code needed)

Add, update or remove speaking events, projects and testimonials by filling in a GitHub issue form. A workflow validates the change, commits it to `data/*.json`, redeploys the site and closes the issue.

### 📅 Speaking events: [Content Studio](https://nomadicmehul.dev/studio.html)

**Connect GitHub** (button at the top, same token as Demo Studio) to choose slide files right on the page: **Publish to site** uploads them to the event's folder, updates `data/speaking.json` in one commit and waits for the deploy. Without a token you finish on GitHub as below.

A page on the site for adding or editing speaking events: **calendar date picker**, role chips, topic suggestions from past events, **location autocomplete** (your past places first, then cities worldwide as you type), a **live preview** of the card, duplicate checks, and drafts that survive a reload. When it's ready, **Add event on GitHub** opens the issue already filled in. If you're attaching slides, drag the file in there, then submit. **Edit event** lets you search any event, change it, and sends only what changed (or removes it).

### 🧪 Workshop & talk demo repos: [Demo Studio](https://nomadicmehul.dev/demo-studio.html)

Creates a separate GitHub repo for a workshop or talk demo, e.g. `github.com/nomadicmehul/2027-kubecon-europe-claude-agents`. Fill in the title, event, type, date (calendar), location, speakers, topics, an About text, links, the event or speaker **poster** and any **files**.

**Recommended: Connect GitHub** (button at the top). Paste a [classic token with only `public_repo`](https://github.com/settings/tokens/new?scopes=public_repo&description=Demo+Studio+%28nomadicmehul.dev%29) once; it stays in that browser and is only sent to api.github.com. Then you pick the poster and files right on the page, and **Create repo & publish** creates the repo from the template, uploads everything in one commit and waits until the README is built. **Update a repo** works the same way (and can see private repos). *Disconnect* removes the token.

**Without a token** you finish on GitHub:

1. **Create on GitHub**: opens GitHub's new-repo page with the name and description filled in, from the `event-demo-template` repo. Click *Create repository*; the page notices when it exists.
2. **Add details on GitHub**: opens a filled-in issue in the new repo. Drag in the poster and files, submit. The repo's own workflow writes `event.json`, saves files to `event/`, and generates the top of the README (poster, date, location, links, about, files, gallery). Everything under **## Demo** in the README is yours and never overwritten.
3. *(optional)* **Open in Content Studio**: adds the event to the speaking page with the repo as its code link.

**Update a repo** lists your demo repos (descriptions starting with 🎤), loads the current `event.json`, and sends only what changed. Inside each repo there's also an **Event info** issue form, and editing `event.json` by hand re-renders the README.

<details><summary>One-time setup: the template repo</summary>

The template's files live in this repo at [`.github/event-repo-template/`](.github/event-repo-template). To publish them:

1. Create an empty public repo named `event-demo-template` (Demo Studio shows a link when it's missing).
2. Push the folder's contents to it, e.g.
   ```bash
   tmp=$(mktemp -d) && cp -R .github/event-repo-template/. "$tmp" && cd "$tmp" \
     && git init -b main && git add -A && git commit -m "Event demo template" \
     && git remote add origin https://github.com/nomadicmehul/event-demo-template.git && git push -u origin main
   ```
3. In that repo: **Settings → General → ✓ Template repository**.

After changing the template, push it again the same way (`git push --force`); repos already created keep their own copy.
</details>

### 👉 Everything else: [MANAGE.md](https://github.com/nomadicmehul/nomadicmehul.github.io/blob/main/MANAGE.md)

One page listing everything on the site: speaking events grouped by **year → month**, projects, testimonials, and **recent activity by month**. Every row has **✏️ Update** and **🗑️ Remove** links that open the right form with the entry already filled in. It's also linked at the top of **Issues → New issue**.

Or open a form directly:

| What | Add new | Update or remove existing |
|------|---------|---------------------------|
| 🎤 Speaking event | [Add speaking event](https://github.com/nomadicmehul/nomadicmehul.github.io/issues/new?template=add-speaking-event.yml) | [Update or remove speaking event](https://github.com/nomadicmehul/nomadicmehul.github.io/issues/new?template=update-speaking-event.yml) |
| 🚀 Project | [Add project](https://github.com/nomadicmehul/nomadicmehul.github.io/issues/new?template=add-project.yml) | [Update or remove project](https://github.com/nomadicmehul/nomadicmehul.github.io/issues/new?template=update-project.yml) |
| 💬 Testimonial | [Add testimonial](https://github.com/nomadicmehul/nomadicmehul.github.io/issues/new?template=add-testimonial.yml) | [Update or remove testimonial](https://github.com/nomadicmehul/nomadicmehul.github.io/issues/new?template=update-testimonial.yml) |
| 📝 Blog posts | Nothing to do: synced from Medium daily. To sync now: **Actions → Sync Medium posts → Run workflow** |

All forms: [Issues → New issue](https://github.com/nomadicmehul/nomadicmehul.github.io/issues/new/choose)

**How it works**

1. Open a form (or use the Content Studio), fill it in, click **Submit new issue**
2. Within about a minute, the **Issue form → site data** workflow runs ([Actions tab](https://github.com/nomadicmehul/nomadicmehul.github.io/actions/workflows/issue-to-data.yml))
3. On success, it comments on the issue (links to any saved files, plus the JSON), closes it, and the site redeploys (another minute or two)
4. If something is invalid (bad date, broken URL, duplicate), it comments the errors instead: **edit the issue** to fix them and it re-runs

**Tips**

- Only issues opened by the repo owner are processed; anyone else's submissions are ignored.
- **Files (slides etc.):** drag a PDF or PPTX into the issue. The workflow downloads it into the event's own folder, `assets/events/<year>/<date>-<event-name>/`, so it's served by the site and **opens in a new tab** (GitHub's own attachment links force a download). PowerPoint files open in Office's online viewer. If the event's title or date changes, its files move to the new folder; removing a resource or event deletes its files. Pasting a full URL works too.
- **Topics / Tech:** comma-separated, e.g. `Kubernetes, GKE, AI Agents`.
- **Date:** `YYYY-MM-DD`, or written out (`9 Jun 2026`, `Jun 9th, 2026`, `09.06.2026`). The Content Studio has a calendar. Events are placed in date order automatically.
- **Tracking:** every entry has `added` and `updated` dates (YYYY-MM-DD), set automatically on add, update and direct JSON edits. Don't type them yourself.
- **Update or remove:** click the entry's link in [MANAGE.md](https://github.com/nomadicmehul/nomadicmehul.github.io/blob/main/MANAGE.md), then fill in **only the fields that should change**; blank fields keep their current value. Opening the form directly works too: type the title, or a unique part of it. Each type has its own fields, e.g. *New location* and *New topics* for events, *Featured* for projects, *Stars* for testimonials.
- **Add a recording after a talk:** MANAGE.md → find the event → ✏️ Update → Add resources = `video | https://youtube.com/...`
- **Broken links:** every Monday a workflow checks all links in `data/*.json` and keeps a **Broken links report** issue up to date (closed automatically once everything is fixed). Run it any time from **Actions → Check links**.

**Setup** (already done for this repo; needed once on a fork)

1. **Settings → Pages → Source:** GitHub Actions.
2. Labels `data:speaking`, `data:project`, `data:testimonial` and `data:edit` are created automatically by **Sync labels** on the first push to `main`. If one ever goes missing, run **Actions → Sync labels**.
3. If `main` has branch protection, allow GitHub Actions to push to it.

## Automation

Everything runs on GitHub Actions; nothing to install.

| Workflow | When | What it does |
|---|---|---|
| **Deploy to GitHub Pages** | Push to `main` (site files or `data/`) | Validates all `data/*.json`, then publishes the site |
| **Issue form → site data** | Owner opens or edits a form issue | Validates the entry, stamps `added`/`updated`, commits, regenerates `MANAGE.md`, redeploys, closes the issue |
| **Refresh MANAGE.md, forms & entry dates** | Direct push to `data/*.json` | Stamps dates on changed entries, regenerates `MANAGE.md` and the forms |
| **Sync Medium posts** | Daily 06:00 UTC, or manually | Adds new Medium posts to `data/blog.json` and redeploys |
| **Check links** | Mondays 07:00 UTC, or manually | Checks every link in `data/`; keeps one **Broken links report** issue up to date |
| **Sync labels** | Push to `main` touching the forms | Creates the labels the forms need |
| **Auto-assign PRs** | PR opened | Assigns the PR to the repo owner |

## What You Get

- **Terminal prompt navigation** — `root@you:~#` with colored segments and blinking cursor
- **Matrix rain background** — animated canvas with falling code characters
- **CRT scanline overlay** — subtle retro terminal aesthetic
- **4 complete pages** — Home (portfolio), Speaking (timeline), Projects (grid), Blog (Medium)
- **Fully responsive** — works on desktop, tablet, and mobile
- **Dark mode only** — because terminals don't do light mode
- **Data-driven** — speaking, projects, testimonials and blog posts live in `data/*.json`
- **SEO ready** — Open Graph and Twitter Cards with a designed link-preview image, schema.org ProfilePage data, sitemap, robots.txt
- **Upcoming talks** — events dated today or later get an **Upcoming** badge automatically
- **Accessible** — skip-to-content, ARIA labels, focus states, reduced motion support
- **Zero dependencies** — pure HTML, CSS, and vanilla JS (no build tools needed)
- **Custom 404 page** — `bash: page_not_found: command not found`

## Quick Start

### Option 1: Use This Template

1. Click **"Use this template"** on GitHub (or fork the repo)
2. Rename to `yourusername.github.io`
3. Replace the personal content in the HTML pages (name, bio, social links, hero, recognition)
4. Update the data in `data/` folder
5. Push — your site is live at `https://yourusername.github.io`

### Option 2: Local Development

```bash
git clone https://github.com/nomadicmehul/nomadicmehul.github.io.git
cd nomadicmehul.github.io

# Serve locally (pick any method)
python3 -m http.server 8000
# or
npx serve .
# or
php -S localhost:8000
```

Open `http://localhost:8000` and start customizing.

## Configuration

### What to Customize

| File | What to Change |
|------|----------------|
| `data/speaking.json` | Your speaking engagements |
| `data/projects.json` | Your open-source projects |
| `data/testimonials.json` | Testimonials from colleagues/mentees |
| `data/roles.json` | Speaking roles and their badge icon/color |
| `data/blog.json` | Auto-synced from Medium by `.github/workflows/sync-medium.yml` (set your feed URL in `.github/scripts/sync_medium.py`) |
| `assets/img/profile.jpg` | Your profile photo |
| `assets/events/` | Files for speaking events, one folder per event: `<year>/<date>-<event-name>/` |
| `assets/favicon.svg` | Your favicon (edit the SVG) |
| `.github/og-card/card.html` | Link-preview image shown on LinkedIn, X, Slack, WhatsApp. Edit, then run `.github/og-card/render.sh` to regenerate `assets/og-image.png` (needs Chrome) |
| `index.html` | Name, hero, about, skills, recognition, social links |
| `speaking.html` | Page title and description |
| `projects.html` | Page title and description |
| `CNAME` | Your custom domain (delete it to use `yourusername.github.io`) |
| `.github/ISSUE_TEMPLATE/config.yml`, this README | Links that point at `nomadicmehul/nomadicmehul.github.io`; replace with your repo |

## Speaking Events Data

All speaking events are managed in `data/speaking.json`. Each event entry renders as a card on both the home page (first 6) and the speaking page (all events). Events dated today or later get an amber **Upcoming** badge automatically; no extra field needed.

### Event Structure

```json
{
  "year": 2026,
  "date": "2026-03-17",
  "title": "Google Cloud Builders Day in Berlin",
  "location": "Berlin, Germany",
  "role": ["Speaker", "Workshop Facilitator"],
  "topics": ["Google Cloud", "Cloud", "Builders Day"],
  "resources": [
    { "type": "event", "label": "Event Page", "url": "https://cloud.google.com/..." },
    { "type": "slides", "label": "Slide Deck", "url": "my-talk.pdf" },
    { "type": "code", "label": "GitHub Repo", "url": "https://github.com/user/repo" }
  ],
  "added": "2026-03-28",
  "updated": "2026-03-30"
}
```

`added` / `updated` are stamped automatically (see [Automation](#automation)); don't edit them by hand. Projects and testimonials have them too.

### Resource Types

Resources render as colored action buttons on each event card. Add only what you have — `"resources": []` is valid.

| Type | Color | Icon | URL Format | Use For |
|------|-------|------|------------|---------|
| `event` | Green | External link | Full URL (`https://...`) | Event page or registration link |
| `slides` | Purple | PowerPoint | `assets/events/...` path or full URL | Slide decks — uploads are saved per event in `assets/events/` |
| `code` | Blue | GitHub | Full URL (`https://github.com/...`) | Source code, repos, demo code |
| `demo` | Cyan | Play | Full URL (`https://...`) | Live demo links, deployed apps |
| `video` | Red | Video | Full URL (`https://youtube.com/...`) | Talk recordings |
| `blog` | Amber | Blog | Full URL (`https://...`) | Blog posts, write-ups |

> **Local files:** a URL starting with `assets/` is a path from the site root (e.g. `assets/events/2026/2026-06-09-my-talk/deck.pdf`). A bare filename resolves to `assets/slides/<filename>` and gets moved into the event's folder on the next push. `.pptx` files open in Office's online viewer.

### Role Types

The `role` field accepts a single string or an array of strings. The list of roles lives in **`data/roles.json`**, the one place to add, rename or recolor a role:

```json
{ "name": "Keynote Speaker", "icon": "fas fa-star", "color": "red" }
```

- `icon`: any FontAwesome 6 class
- `color`: `green`, `amber`, `purple`, `cyan`, `blue`, `red` or `default` (grey)

Both pages render badges from it, and the role checkboxes in the **Add speaking event** and **Update or remove speaking event** issue forms are regenerated from it automatically. Deploy fails if an event uses a role that isn't in `roles.json`.

Current roles: Speaker (green), Event Organizer (amber), Mentor (purple), Panelist (cyan), Workshop Lead and Workshop Facilitator (blue).

### Adding a New Event

The easy way is the [Add speaking event](https://github.com/nomadicmehul/nomadicmehul.github.io/issues/new?template=add-speaking-event.yml) form (see [Updating Content](#updating-content-no-code-needed)). To edit the JSON directly instead:

1. Add the entry to `data/speaking.json`, newest first. For a file, use a GitHub attachment URL, or drop it in `assets/slides/` and use the bare filename
2. Push. The file is moved into `assets/events/<year>/<date>-<event-name>/` (and the URL updated), dates are stamped, `MANAGE.md` is refreshed and the site redeploys automatically

## Projects Data

`data/projects.json` holds the open-source projects:

```json
{
  "title": "Dispatch",
  "description": "AI-powered CLI tool that solves GitHub issues in batch...",
  "icon": "fas fa-bolt",
  "iconColor": "#f59e0b",
  "repo": "https://github.com/nomadicmehul/dispatch",
  "tech": ["Node.js", "AI", "Claude"],
  "featured": true
}
```

- `featured: true` projects appear on the home page; the Projects page shows all of them.
- The **Featured** badge and count only appear when some projects aren't featured (if all are, they'd say nothing).
- With 2 or 4 cards the grid becomes 2×2, so no card sits alone on a row.
- `repo` must be a `https://github.com/...` URL (deploy checks it).

## Project Structure

```
├── index.html              # Main portfolio page
├── speaking.html           # Speaking engagements timeline
├── studio.html             # Content Studio: add/edit speaking events (calendar, live preview → GitHub issue)
├── demo-studio.html        # Demo Studio: create/update a separate GitHub repo per workshop or talk demo
├── projects.html           # Open-source projects grid
├── blog.html               # Medium articles
├── 404.html                # Custom 404 error page
├── MANAGE.md               # Generated: every entry by year/month with update/remove links
├── CNAME                   # Custom domain (nomadicmehul.dev)
├── robots.txt              # SEO crawling rules
├── sitemap.xml             # SEO sitemap
├── assets/
│   ├── img/
│   │   └── profile.jpg     # Profile photo
│   ├── events/             # Event files: <year>/<date>-<event-name>/slides.pdf (managed by the workflows)
│   ├── og-image.png        # 1200×630 link-preview image (generated from .github/og-card/)
│   └── favicon.svg         # Terminal prompt favicon
└── data/
    ├── projects.json       # Projects data
    ├── speaking.json       # Speaking events data
    ├── testimonials.json   # Testimonials data
    ├── roles.json          # Speaking roles (badge icon + color)
    └── blog.json           # Medium posts (auto-synced)
.github/
├── ISSUE_TEMPLATE/         # Add / update-or-remove forms (update forms are generated)
├── og-card/                # Source + render script for assets/og-image.png
├── scripts/                # Python behind the workflows (no dependencies)
└── workflows/              # See Automation
```

Each HTML page is self-contained: its CSS and JS are inline, so there is no shared stylesheet or script to keep in sync.

## Features Deep Dive

### Terminal Prompt Logo
The nav displays a colorized Linux root prompt:
- `root` — green (superuser)
- `@` — amber (separator)
- `mehul` — cyan (hostname)
- `:` — grey
- `~` — blue (path)
- `#` — red, blinking (root indicator)
- `█` — green, blinking cursor

### Matrix Rain
The homepage features an animated canvas background with falling characters (`01{}[]<>/\|;:=+-*`). It's off for users who prefer reduced motion, and pauses while the tab is in the background.

### Link Preview & Search
- **Link-preview image:** `assets/og-image.png` (1200×630) is what LinkedIn, X, Slack and WhatsApp show when the site is shared. It's rendered from `.github/og-card/card.html`; after editing it, run `.github/og-card/render.sh`. LinkedIn caches previews, so refresh with its [Post Inspector](https://www.linkedin.com/post-inspector/).
- **Structured data:** the home page has schema.org `ProfilePage` data (name, title, location, skills, recognitions, social profiles) for search engines. Check it with Google's [Rich Results Test](https://search.google.com/test/rich-results).

### Data-Driven Pages
Speaking events, projects, testimonials and blog posts load from JSON files in `data/` via `fetch()`, so serve the site over HTTP (see Local Development) rather than opening the files directly. Entries are usually managed through GitHub issue forms and [MANAGE.md](MANAGE.md); see [Updating Content](#updating-content-no-code-needed).

### Accessibility
- Skip-to-content link on every page
- ARIA labels on navigation and landmarks
- `role="navigation"` and `role="contentinfo"` semantic roles
- Visible focus states (green outline) for keyboard navigation
- `prefers-reduced-motion` support on every page: animations and transitions are switched off
- Semantic `<main>`, `<nav>`, `<footer>` structure

## Deployment

### GitHub Pages (Recommended)
1. Push to your `yourusername.github.io` repo
2. Go to **Settings → Pages**
3. Set **Source** to **GitHub Actions** (used by `.github/workflows/deploy.yml`)
4. Your site is live!

### Netlify
[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start)

Just drag and drop the folder, or connect your GitHub repo.

### Vercel
```bash
npx vercel
```

### Any Static Host
This is pure HTML/CSS/JS — it works everywhere. Just upload the files.

## Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Terminal Green | `#4ade80` | Primary accent, links, prompts |
| Green Bright | `#86efac` | Hover states |
| Amber | `#fbbf24` | Secondary accent, @ symbol |
| Cyan | `#22d3ee` | Tertiary accent, hostname |
| Red | `#f87171` | Hash symbol, errors |
| Purple | `#c084fc` | Decorative accents |
| Blue | `#60a5fa` | Path, info elements |
| BG Primary | `#0a0e17` | Main background |
| BG Secondary | `#0f1623` | Alternate sections |
| BG Card | `#111827` | Cards |
| Text Primary | `#e2e8f0` | Headings, body text |
| Text Secondary | `#94a3b8` | Descriptions, labels |

## Contributing

Contributions are welcome! Whether it's a bug fix, new feature, or improvement:

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Ideas for Contributions
- Additional page templates (resume, contact form)
- Color scheme variants (amber/gold theme, blue/cyan theme)
- Animation options (typing effect variants, glitch effects)
- Integration with headless CMS
- Internationalization (i18n) support
- Performance optimizations

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details. Use it, fork it, make it yours.

## Support This Project

This theme is free and open source — and it always will be. If it saved you time, helped you land a gig, or you just dig the terminal vibes, consider buying me a coffee. Every cup fuels late-night commits and new features for the community.

<a href="https://buymeacoffee.com/nomadicmehul" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" width="200"></a>

Other ways to support: give this repo a star, share it with a friend, or open a PR with your improvements. Open source runs on community energy.

## Credits

Built by [Mehul Patel](https://github.com/nomadicmehul) with mass-caffeine, vim, and a love for terminals.

Fonts: [Inter](https://rsms.me/inter/) & [JetBrains Mono](https://www.jetbrains.com/lp/mono/)

---

<div align="center">

**If this theme helped you, give it a ⭐ on GitHub!**

`chmod +x life.sh && ./life.sh`

[☕ Buy Me a Coffee](https://buymeacoffee.com/nomadicmehul)

</div>
