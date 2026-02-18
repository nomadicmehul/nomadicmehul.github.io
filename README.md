<div align="center">

# `root@you:~#` Terminal Portfolio Theme

A Linux terminal-inspired portfolio theme for developers, DevOps engineers, and open-source enthusiasts. Dark mode. Matrix rain. CRT scanlines. Built to make your work look as cool as you are.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-blue.svg)](https://pages.github.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/nomadicmehul)

[Live Demo](https://nomadicmehul.github.io) · [Report Bug](https://github.com/nomadicmehul/nomadicmehul.github.io/issues) · [Request Feature](https://github.com/nomadicmehul/nomadicmehul.github.io/issues)

</div>

---

## What You Get

- **Terminal prompt navigation** — `root@you:~#` with colored segments and blinking cursor
- **Matrix rain background** — animated canvas with falling code characters
- **CRT scanline overlay** — subtle retro terminal aesthetic
- **3 complete pages** — Home (portfolio), Speaking (timeline), Projects (grid)
- **Fully responsive** — works on desktop, tablet, and mobile
- **Dark mode only** — because terminals don't do light mode
- **Configurable** — single `config.json` to personalize everything
- **SEO ready** — Open Graph, Twitter Cards, sitemap, robots.txt
- **Accessible** — skip-to-content, ARIA labels, focus states, reduced motion support
- **Zero dependencies** — pure HTML, CSS, and vanilla JS (no build tools needed)
- **Custom 404 page** — `bash: page_not_found: command not found`

## Quick Start

### Option 1: Use This Template

1. Click **"Use this template"** on GitHub (or fork the repo)
2. Rename to `yourusername.github.io`
3. Edit `config.json` with your info
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

Everything personal lives in `config.json`. Edit this one file to make it yours:

```json
{
  "site": {
    "title": "Your Name",
    "tagline": "Your Title",
    "email": "you@example.com",
    "url": "https://yourusername.github.io"
  },
  "terminal": {
    "user": "root",
    "host": "yourname",
    "promptPath": "~",
    "footerCommand": "chmod +x life.sh"
  },
  "social": {
    "github": "https://github.com/yourusername",
    "linkedin": "https://linkedin.com/in/yourusername",
    "twitter": "https://twitter.com/yourusername"
  }
}
```

### What to Customize

| File | What to Change |
|------|----------------|
| `config.json` | Name, bio, social links, terminal prompt, stats |
| `data/speaking.json` | Your speaking engagements |
| `data/projects.json` | Your open-source projects |
| `data/testimonials.json` | Testimonials from colleagues/mentees |
| `assets/img/profile.jpg` | Your profile photo |
| `assets/favicon.svg` | Your favicon (edit the SVG) |
| `index.html` | Hero section, about section, skills |
| `speaking.html` | Page title and description |
| `projects.html` | Page title and description |

## Project Structure

```
├── index.html              # Main portfolio page
├── speaking.html           # Speaking engagements timeline
├── projects.html           # Open-source projects grid
├── 404.html                # Custom 404 error page
├── config.json             # Theme configuration
├── robots.txt              # SEO crawling rules
├── sitemap.xml             # SEO sitemap
├── assets/
│   ├── css/
│   │   └── styles.css      # Shared base styles
│   ├── js/
│   │   └── main.js         # Shared utilities (matrix rain, nav, scroll)
│   ├── img/
│   │   └── profile.jpg     # Profile photo
│   └── favicon.svg         # Terminal prompt favicon
└── data/
    ├── projects.json       # Projects data
    ├── speaking.json       # Speaking events data
    └── testimonials.json   # Testimonials data
```

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
Speaking events and projects load from JSON data files (`data/` folder), with inline fallback data embedded in each HTML file. This means the site works both as a static site and when served locally.

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
3. Select **Deploy from branch** → `main`
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
