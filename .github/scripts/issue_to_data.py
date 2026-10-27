#!/usr/bin/env python3
"""Turn a GitHub Issue Form submission into a change in data/*.json.

Used by .github/workflows/issue-to-data.yml. Handles the "add" forms
(data:speaking, data:project, data:testimonial) and the "update or remove"
form (data:edit). Reads the issue from env vars (never shell-interpolated)
and writes:
  - the updated data file
  - $RESULT_FILE: a markdown message to post back on the issue
  - $GITHUB_OUTPUT: file=<data file>, message=<commit message>

Exit code 0 = change applied, 1 = validation failed (message explains why).

Local test:
  ISSUE_LABELS='["data:speaking"]' ISSUE_BODY="$(cat body.md)" RESULT_FILE=/dev/stdout \
    python3 .github/scripts/issue_to_data.py
"""
import difflib
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLES = ["Speaker", "Event Organizer", "Mentor", "Panelist", "Workshop Lead", "Workshop Facilitator"]
# (add-form label, resource type, button label) — order matches the speaking card buttons
RESOURCE_FIELDS = [
    ("Event page URL", "event", "Event Page"),
    ("Slides", "slides", "Slide Deck"),
    ("Code repo URL", "code", "GitHub Repo"),
    ("Live demo URL", "demo", "Live Demo"),
    ("Recording URL", "video", "Recording"),
    ("Blog post URL", "blog", "Blog Post"),
]
RESOURCE_LABELS = {rtype: button for _, rtype, button in RESOURCE_FIELDS}


# ---------- form parsing ----------

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


def form_url(value):
    """A URL from a form field; files dragged into a textarea arrive as [name](url)."""
    link = re.search(r"\]\((https?://[^)\s]+)\)", value)
    return link.group(1) if link else value.strip()


# ---------- validation (shared by add and edit) ----------

def validate_speaking(e, errors):
    try:
        e["year"] = date.fromisoformat(e.get("date", "")).year
    except ValueError:
        errors.append(f"**date** must be `YYYY-MM-DD` (got `{e.get('date', '')}`)")
    for key in ("title", "location"):
        if not e.get(key):
            errors.append(f"**{key}** is required")
    if not e.get("topics"):
        errors.append("**topics** needs at least one topic")
    roles = e.get("role", [])
    unknown = [r for r in ([roles] if isinstance(roles, str) else roles) if r not in ROLES]
    if unknown:
        errors.append(f"Unknown role {unknown} — use: {', '.join(ROLES)}")
    for r in e.get("resources", []):
        if r["type"] not in RESOURCE_LABELS:
            errors.append(f"Unknown resource type `{r['type']}` — use: {', '.join(RESOURCE_LABELS)}")
        elif r["type"] == "slides" and not r["url"].startswith("http"):
            # slides may be a bare filename in assets/slides/; everything else must be a URL
            if not (ROOT / "assets" / "slides" / r["url"]).exists():
                errors.append(f"**slides**: `assets/slides/{r['url']}` doesn't exist — upload it first or use a full URL")
        elif not is_url(r["url"]):
            errors.append(f"**{r['type']}** link must start with `http://` or `https://` (got `{r['url']}`)")


def validate_project(e, errors):
    for key in ("title", "description"):
        if not e.get(key):
            errors.append(f"**{key}** is required")
    if not e.get("repo", "").startswith("https://github.com/"):
        errors.append("**repo** must start with `https://github.com/`")
    if not e.get("tech"):
        errors.append("**tech** needs at least one entry")
    if not re.match(r"^#[0-9a-fA-F]{3,8}$", e.get("iconColor", "")):
        errors.append(f"**iconColor** must be a hex color like `#4ade80` (got `{e.get('iconColor', '')}`)")


def validate_testimonial(e, errors):
    for key in ("quote", "name", "role"):
        if not e.get(key):
            errors.append(f"**{key}** is required")
    if not 1 <= e.get("stars", 0) <= 5:
        errors.append("**stars** must be 1–5")
    if e.get("link") and not is_url(e["link"]):
        errors.append("**link** must start with `http://` or `https://`")


# ---------- add forms ----------

def build_speaking(f):
    resources = [
        {"type": rtype, "label": button, "url": form_url(f[label])}
        for label, rtype, button in RESOURCE_FIELDS if f.get(label)
    ]
    return {
        "year": None,  # filled in from date by validate_speaking
        "date": f.get("Date", ""),
        "title": f.get("Event title", ""),
        "location": f.get("Location", ""),
        "role": checked(f.get("Role", "")) or ["Speaker"],
        "topics": csv(f.get("Topics", "")),
        "resources": resources,
    }


def build_project(f):
    return {
        "title": f.get("Project title", ""),
        "description": f.get("Description", ""),
        "icon": f.get("Icon", "") or "fas fa-code",
        "iconColor": f.get("Icon color", "") or "#4ade80",
        "repo": f.get("GitHub repo URL", ""),
        "tech": csv(f.get("Tech", "")),
        "featured": bool(checked(f.get("Featured", ""))),
    }


def build_testimonial(f):
    return {
        "quote": f.get("Quote", ""),
        "name": f.get("Name", ""),
        "role": f.get("Role", ""),
        "stars": int(f.get("Stars") or 5),
        "link": f.get("Link", ""),
    }


# key = field that identifies an entry in the edit form; fields = editable fields and their value kind
TYPES = {
    "speaking": {
        "path": "data/speaking.json", "noun": "speaking event", "key": "title",
        "build": build_speaking, "validate": validate_speaking,
        "fields": {"title": str, "date": str, "location": str, "role": list, "topics": list},
    },
    "project": {
        "path": "data/projects.json", "noun": "project", "key": "title",
        "build": build_project, "validate": validate_project,
        "fields": {"title": str, "description": str, "icon": str, "iconColor": str, "repo": str, "tech": list, "featured": bool},
    },
    "testimonial": {
        "path": "data/testimonials.json", "noun": "testimonial", "key": "name",
        "build": build_testimonial, "validate": validate_testimonial,
        "fields": {"quote": str, "name": str, "role": str, "stars": int, "link": str},
    },
}
ADD_LABELS = {"data:speaking": "speaking", "data:project": "project", "data:testimonial": "testimonial"}
EDIT_TYPES = {"Speaking event": "speaking", "Project": "project", "Testimonial": "testimonial"}


def add(kind, f, data, errors):
    t = TYPES[kind]
    entry = t["build"](f)
    t["validate"](entry, errors)
    if kind == "speaking" and any(e.get("title") == entry["title"] and e.get("date") == entry["date"] for e in data):
        errors.append("An event with this title and date already exists")
    if kind == "project" and any(p.get("repo") == entry["repo"] for p in data):
        errors.append("A project with this repo already exists")
    if not errors:
        data.insert(0, entry)
    return "add", entry


# ---------- edit form ----------

def find_entry(data, key, query, errors):
    """Exact (case-insensitive) match, else a unique substring match. 'Title (YYYY-MM-DD)' narrows by date."""
    m = re.match(r"^(.*?)\s*\((\d{4}-\d{2}-\d{2})\)$", query)
    name, on = (m.group(1), m.group(2)) if m else (query, None)
    pool = [e for e in data if on is None or e.get("date") == on]
    q = name.strip().lower()
    hits = [e for e in pool if e.get(key, "").lower() == q] or [e for e in pool if q and q in e.get(key, "").lower()]
    if len(hits) == 1:
        return hits[0]
    if hits:
        options = ", ".join(f"`{e[key]} ({e['date']})`" if "date" in e else f"`{e[key]}`" for e in hits[:5])
        errors.append(f"**Entry** matches {len(hits)} entries — be more specific, e.g. {options}")
    else:
        close = difflib.get_close_matches(name, [e.get(key, "") for e in data], n=3, cutoff=0.5)
        errors.append(f"**Entry** `{query}` not found" + (f" — did you mean {', '.join(f'`{c}`' for c in close)}?" if close else ""))
    return None


def apply_fields(entry, text, fields, errors):
    by_lower = {k.lower(): k for k in fields}
    for line in text.splitlines():
        if not line.strip():
            continue
        raw_key, sep, value = line.partition(":")
        key = by_lower.get(raw_key.strip().lower())
        if not sep or not key:
            errors.append(f"Can't use `{line.strip()}` — write `field: value` with one of: {', '.join(fields)}")
            continue
        value, kind = value.strip(), fields[key]
        if kind is list:
            entry[key] = csv(value)
        elif kind is bool:
            entry[key] = value.lower() in ("true", "yes", "1", "y")
        elif kind is int:
            try:
                entry[key] = int(value)
            except ValueError:
                errors.append(f"**{key}** must be a number")
        else:
            entry[key] = value


def apply_resources(entry, add_text, remove_text, errors):
    resources = entry.setdefault("resources", [])
    for rtype in csv(remove_text.lower()):
        if not any(r["type"] == rtype for r in resources):
            errors.append(f"No `{rtype}` resource to remove")
        resources[:] = [r for r in resources if r["type"] != rtype]
    for line in add_text.splitlines():
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) not in (2, 3):
            errors.append(f"Can't read resource `{line.strip()}` — use `type | url` or `type | label | url`")
            continue
        rtype = parts[0].lower()
        label = parts[1] if len(parts) == 3 else RESOURCE_LABELS.get(rtype, rtype.title())
        resources.append({"type": rtype, "label": label, "url": form_url(parts[-1])})


def edit(kind, f, data, errors):
    t = TYPES[kind]
    entry = find_entry(data, t["key"], f.get("Entry", ""), errors)
    if entry is None:
        return None, None
    if f.get("Action") == "Remove":
        data.remove(entry)
        return "remove", entry

    changes, add_res, remove_res = f.get("Change fields", ""), f.get("Add resources", ""), f.get("Remove resources", "")
    if (add_res or remove_res) and kind != "speaking":
        errors.append("**Add/Remove resources** only apply to speaking events")
    if not (changes or add_res or remove_res):
        errors.append("Nothing to update — fill in **Change fields** or **Add/Remove resources**")
    apply_fields(entry, changes, t["fields"], errors)
    if kind == "speaking":
        apply_resources(entry, add_res, remove_res, errors)
    t["validate"](entry, errors)
    return "update", entry


# ---------- main ----------

def main():
    labels = json.loads(os.environ.get("ISSUE_LABELS", "[]"))
    result = Path(os.environ["RESULT_FILE"])
    f = parse_form(os.environ.get("ISSUE_BODY", ""))

    if "data:edit" in labels:
        kind = EDIT_TYPES.get(f.get("Data type", ""))
        handler = edit
    else:
        kind = next((ADD_LABELS[l] for l in labels if l in ADD_LABELS), None)
        handler = add
    if not kind:
        result.write_text("Couldn't tell which data file this issue is for — nothing to do.")
        return 1

    t = TYPES[kind]
    path = ROOT / t["path"]
    data = json.loads(path.read_text())
    errors = []
    action, entry = handler(kind, f, data, errors)

    if errors:
        result.write_text(
            f"❌ Couldn't {action or 'change'} this {t['noun']}:\n\n" + "\n".join(f"- {e}" for e in errors)
            + "\n\nEdit the issue to fix it — the workflow re-runs automatically."
        )
        return 1

    if kind == "speaking":
        data.sort(key=lambda e: e.get("date", ""), reverse=True)  # newest first; stable for same-day events
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    verb, prep = {"add": ("Added", "to"), "update": ("Updated", "in"), "remove": ("Removed", "from")}[action]
    name = entry[t["key"]]
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as out:
        out.write(f"file={t['path']}\nmessage=data: {action} {t['noun']} \"{name}\"\n")
    result.write_text(
        f"✅ {verb} {t['noun']} **{name}** {prep} `{t['path']}`. The site will redeploy in a minute or two.\n\n"
        f"```json\n{json.dumps(entry, indent=2, ensure_ascii=False)}\n```"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
