<div align="center">

# `root@you:~#` Terminal Portfolio Theme

A Linux terminal-inspired portfolio theme for developers, DevOps engineers, and open-source enthusiasts. Dark mode. Matrix rain. CRT scanlines. Built to make your work look as cool as you are.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-blue.svg)](https://pages.github.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/nomadicmehul)

[Live Demo](https://nomadicmehul.github.io) · [Report Bug](https://github.com/nomadicmehul/nomadicmehul.github.io/issues) · [Request Feature](https://github.com/nomadicmehul/nomadicmehul.github.io/issues)

</div>

---

## Updating Content (no code needed)

Add speaking events, projects and testimonials by filling in a GitHub issue form. A workflow validates the entry, commits it to `data/*.json`, redeploys the site and closes the issue.

| What | Open the form |
|------|---------------|
| 🎤 Speaking event | [Add speaking event](https://github.com/nomadicmehul/nomadicmehul.github.io/issues/new?template=add-speaking-event.yml) |
| 🚀 Project | [Add project](https://github.com/nomadicmehul/nomadicmehul.github.io/issues/new?template=add-project.yml) |
| 💬 Testimonial | [Add testimonial](https://github.com/nomadicmehul/nomadicmehul.github.io/issues/new?template=add-testimonial.yml) |
| 📝 Blog posts | Nothing to do: synced from Medium daily. To sync now: **Actions → Sync Medium posts → Run workflow** |

All forms: [Issues → New issue](https://github.com/nomadicmehul/nomadicmehul.github.io/issues/new/choose)

**How it works**

1. Open a form, fill it in, click **Submit new issue**
2. Within about a minute, the **Issue form → site data** workflow runs ([Actions tab](https://github.com/nomadicmehul/nomadicmehul.github.io/actions/workflows/issue-to-data.yml))
3. On success, it comments the added JSON on the issue, closes it, and the site redeploys (another minute or two)
4. If something is invalid (bad date, broken URL, duplicate), it comments the errors instead: **edit the issue** to fix them and it re-runs

**Tips**

- Only issues opened by the repo owner are processed; anyone else's submissions are ignored.
- **Slides:** paste a full URL, drag a PDF into the field (GitHub uploads it and inserts a link), or use the filename of a deck already in `assets/slides/`.
- **Topics / Tech:** comma-separated, e.g. `Kubernetes, GKE, AI Agents`.
- **Date:** `YYYY-MM-DD`. Events are placed in date order automatically.
- To edit or remove an existing entry, change the JSON in `data/` directly (on github.com: open the file → ✏️ edit → commit).

**One-time setup** (required before the forms work)

1. Create the labels `data:speaking`, `data:project` and `data:testimonial` (**Issues → Labels → New label**). The forms apply them, and the workflow only runs on labelled issues.
2. **Settings → Pages → Source:** GitHub Actions.
3. If `main` has branch protection, allow GitHub Actions to push to it.

## What You Get

- **Terminal prompt navigation** — `root@you:~#` with colored segments and blinking cursor
- **Matrix rain background** — animated canvas with falling code characters
- **CRT scanline overlay** — subtle retro terminal aesthetic
- **4 complete pages** — Home (portfolio), Speaking (timeline), Projects (grid), Blog (Medium)
- **Fully responsive** — works on desktop, tablet, and mobile
- **Dark mode only** — because terminals don't do light mode
- **Data-driven** — speaking, projects, testimonials and blog posts live in `data/*.json`
- **SEO ready** — Open Graph, Twitter Cards, sitemap, robots.txt
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
| `data/blog.json` | Auto-synced from Medium by `.github/workflows/sync-medium.yml` (set your feed URL in `.github/scripts/sync_medium.py`) |
| `assets/img/profile.jpg` | Your profile photo |
| `assets/slides/` | Slide decks (PDF/PPTX) for speaking events |
| `assets/favicon.svg` | Your favicon (edit the SVG) |
| `index.html` | Name, hero, about, skills, recognition, social links |
| `speaking.html` | Page title and description |
| `projects.html` | Page title and description |

## Speaking Events Data

All speaking events are managed in `data/speaking.json`. Each event entry renders as a card on both the home page (first 6) and the speaking page (all events).

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
  ]
}
```

### Resource Types

Resources render as colored action buttons on each event card. Add only what you have — `"resources": []` is valid.

| Type | Color | Icon | URL Format | Use For |
|------|-------|------|------------|---------|
| `event` | Green | External link | Full URL (`https://...`) | Event page or registration link |
| `slides` | Purple | PowerPoint | Filename (`talk.pdf`) or full URL | Slide decks — local files go in `assets/slides/` |
| `code` | Blue | GitHub | Full URL (`https://github.com/...`) | Source code, repos, demo code |
| `demo` | Cyan | Play | Full URL (`https://...`) | Live demo links, deployed apps |
| `video` | Red | Video | Full URL (`https://youtube.com/...`) | Talk recordings |
| `blog` | Amber | Blog | Full URL (`https://...`) | Blog posts, write-ups |

> **Local files:** If a URL does NOT start with `http://` or `https://`, it resolves to `assets/slides/<filename>`. Drop your file in that folder and just use the filename in the JSON.

### Role Types

The `role` field shows colored badges indicating your role at the event. Supports a single string or array for multiple roles.

| Role | Color |
|------|-------|
| `Speaker` | Green |
| `Event Organizer` | Amber |
| `Mentor` | Purple |
| `Panelist` | Cyan |
| `Workshop Lead` | Blue |
| `Workshop Facilitator` | Blue |

### Adding a New Event

1. (Optional) Drop slide deck into `assets/slides/`
2. Add entry at the **top** of `data/speaking.json`
3. Push — both home page and speaking page update automatically

## Project Structure

```
├── index.html              # Main portfolio page
├── speaking.html           # Speaking engagements timeline
├── projects.html           # Open-source projects grid
├── blog.html               # Medium articles
├── 404.html                # Custom 404 error page
├── robots.txt              # SEO crawling rules
├── sitemap.xml             # SEO sitemap
├── assets/
│   ├── img/
│   │   └── profile.jpg     # Profile photo
│   ├── slides/             # Slide decks for speaking events (PDF/PPTX)
│   └── favicon.svg         # Terminal prompt favicon
└── data/
    ├── projects.json       # Projects data
    ├── speaking.json       # Speaking events data
    ├── testimonials.json   # Testimonials data
    └── blog.json           # Medium posts (auto-synced)
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
The homepage features an animated canvas background with falling characters (`01{}[]<>/\|;:=+-*`). It automatically pauses for users who prefer reduced motion.

### Data-Driven Pages
Speaking events, projects, testimonials and blog posts load from JSON files in `data/` via `fetch()`, so serve the site over HTTP (see Local Development) rather than opening the files directly. On this repo, entries can also be added through GitHub issue forms (`.github/ISSUE_TEMPLATE/`), which commit to `data/` and redeploy.

### Accessibility
- Skip-to-content link on every page
- ARIA labels on navigation and landmarks
- `role="navigation"` and `role="contentinfo"` semantic roles
- Visible focus states (green outline) for keyboard navigation
- `prefers-reduced-motion` support — disables all animations
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
| BG Secondary | `#0f1623` | Cards, sections |
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
- Additional page templates (blog, resume, contact form)
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
