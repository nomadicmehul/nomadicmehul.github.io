#!/usr/bin/env python3
"""Turn a GitHub Issue Form submission into an entry in data/*.json.

Used by .github/workflows/issue-to-data.yml. Reads the issue from env vars
(never shell-interpolated) and writes:
  - the updated data file
  - $RESULT_FILE: a markdown message to post back on the issue

Exit code 0 = entry added, 1 = validation failed (message explains why).

Local test:
  ISSUE_LABELS='["data:speaking"]' ISSUE_BODY="$(cat body.md)" RESULT_FILE=/dev/stdout \
    python3 .github/scripts/issue_to_data.py
"""
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLES = ["Speaker", "Event Organizer", "Mentor", "Panelist", "Workshop Lead", "Workshop Facilitator"]
# (form label, resource type, button label) — order matches the speaking card buttons
RESOURCE_FIELDS = [
    ("Event page URL", "event", "Event Page"),
    ("Slides", "slides", "Slide Deck"),
    ("Code repo URL", "code", "GitHub Repo"),
    ("Live demo URL", "demo", "Live Demo"),
    ("Recording URL", "video", "Recording"),
    ("Blog post URL", "blog", "Blog Post"),
]


def parse_form(body):
    """Split an issue-form body ('### Label\\n\\nvalue' blocks) into {label: value}."""
    fields = {}
    for block in re.split(r"^### ", body or "", flags=re.M)[1:]:
        label, _, value = block.partition("\n")
        value = value.strip()
        fields[label.strip()] = "" if value == "_No response_" else value
    return fields


def checked(value):
    return re.findall(r"^- \[[xX]\] (.+)$", value, flags=re.M)


def csv(value):
    return [v.strip() for v in value.split(",") if v.strip()]


def is_url(value):
    return re.match(r"^https?://\S+$", value) is not None


def build_speaking(f, errors):
    title, location, topics = f.get("Event title", ""), f.get("Location", ""), csv(f.get("Topics", ""))
    raw_date = f.get("Date", "")
    try:
        d = date.fromisoformat(raw_date)
    except ValueError:
        errors.append(f"**Date** must be `YYYY-MM-DD` (got `{raw_date}`)")
        d = None
    if not title:
        errors.append("**Event title** is required")
    if not location:
        errors.append("**Location** is required")
    if not topics:
        errors.append("**Topics** needs at least one topic")

    resources = []
    for label, rtype, button in RESOURCE_FIELDS:
        url = f.get(label, "")
        if not url:
            continue
        # slides may be a bare filename in assets/slides/; everything else must be a URL
        if rtype == "slides" and not url.startswith("http"):
            if not (ROOT / "assets" / "slides" / url).exists():
                errors.append(f"**Slides**: `assets/slides/{url}` doesn't exist — upload it first or use a full URL")
        elif not is_url(url):
            errors.append(f"**{label}** must start with `http://` or `https://`")
        resources.append({"type": rtype, "label": button, "url": url})

    entry = {
        "year": d.year if d else None,
        "date": raw_date,
        "title": title,
        "location": location,
        "role": [r for r in checked(f.get("Role", "")) if r in ROLES] or ["Speaker"],
        "topics": topics,
        "resources": resources,
    }
    return entry, title


def insert_speaking(data, entry):
    # newest first: place before the first event that is older than this one
    idx = next((i for i, e in enumerate(data) if e.get("date", "") < entry["date"]), len(data))
    data.insert(idx, entry)


def build_project(f, errors):
    title, desc, repo = f.get("Project title", ""), f.get("Description", ""), f.get("GitHub repo URL", "")
    tech, color = csv(f.get("Tech", "")), f.get("Icon color", "") or "#4ade80"
    if not title:
        errors.append("**Project title** is required")
    if not desc:
        errors.append("**Description** is required")
    if not repo.startswith("https://github.com/"):
        errors.append("**GitHub repo URL** must start with `https://github.com/`")
    if not tech:
        errors.append("**Tech** needs at least one entry")
    if not re.match(r"^#[0-9a-fA-F]{3,8}$", color):
        errors.append(f"**Icon color** must be a hex color like `#4ade80` (got `{color}`)")
    entry = {
        "title": title,
        "description": desc,
        "icon": f.get("Icon", "") or "fas fa-code",
        "iconColor": color,
        "repo": repo,
        "tech": tech,
        "featured": bool(checked(f.get("Featured", ""))),
    }
    return entry, title


def build_testimonial(f, errors):
    quote, name, role, link = f.get("Quote", ""), f.get("Name", ""), f.get("Role", ""), f.get("Link", "")
    if not quote:
        errors.append("**Quote** is required")
    if not name:
        errors.append("**Name** is required")
    if not role:
        errors.append("**Role** is required")
    if link and not is_url(link):
        errors.append("**Link** must start with `http://` or `https://`")
    stars = int(f.get("Stars") or 5)
    return {"quote": quote, "name": name, "role": role, "stars": stars, "link": link}, name


KINDS = {
    "data:speaking": ("data/speaking.json", "speaking event", build_speaking, insert_speaking),
    "data:project": ("data/projects.json", "project", build_project, lambda d, e: d.insert(0, e)),
    "data:testimonial": ("data/testimonials.json", "testimonial", build_testimonial, lambda d, e: d.insert(0, e)),
}


def main():
    labels = json.loads(os.environ.get("ISSUE_LABELS", "[]"))
    kind = next((l for l in labels if l in KINDS), None)
    result = Path(os.environ["RESULT_FILE"])
    if not kind:
        result.write_text("No `data:*` label found on this issue — nothing to do.")
        return 1

    rel_path, noun, build, insert = KINDS[kind]
    errors = []
    entry, name = build(parse_form(os.environ.get("ISSUE_BODY", "")), errors)

    path = ROOT / rel_path
    data = json.loads(path.read_text())
    if kind == "data:speaking" and any(e.get("title") == entry["title"] and e.get("date") == entry["date"] for e in data):
        errors.append("An event with this title and date already exists")
    if kind == "data:project" and any(p.get("repo") == entry["repo"] for p in data):
        errors.append("A project with this repo already exists")

    if errors:
        result.write_text(
            "❌ Couldn't add this " + noun + ":\n\n" + "\n".join(f"- {e}" for e in errors)
            + "\n\nEdit the issue to fix it — the workflow re-runs automatically."
        )
        return 1

    insert(data, entry)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as out:
        out.write(f"file={rel_path}\nnoun={noun}\nname={name}\n")
    result.write_text(
        f"✅ Added {noun} **{name}** to `{rel_path}`. The site will redeploy in a minute or two.\n\n"
        f"```json\n{json.dumps(entry, indent=2, ensure_ascii=False)}\n```"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
