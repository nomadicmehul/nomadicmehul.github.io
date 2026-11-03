#!/usr/bin/env python3
"""Keep this demo repo's event details: event.json, files in event/, and the event section of README.md.

Run by .github/workflows/event-info.yml. On an "[event] …" issue (from Demo Studio on
nomadicmehul.dev, or the "Event info" issue form) it applies the issue; otherwise it only
re-renders README.md from event.json (e.g. after editing event.json by hand).

The issue body is "### Field\\n\\nvalue" blocks. A blank field keeps the current value, "-" clears it.
  Links:  one per line, "type | url" or "type | label | url" (a file dropped in as the url is saved to event/)
  Poster: an image dropped into the issue, or an image URL
  Files:  files already in event/ to keep (one path per line) plus files dropped into the issue;
          files in event/ that are no longer listed are deleted

Writes $RESULT_FILE (a markdown comment for the issue). Exit 1 = nothing saved, the comment says why.

Local test:
  EVENT_NAME=issues ISSUE_BODY="$(cat body.md)" RESULT_FILE=/dev/stdout python3 .github/scripts/event_info.py
"""
import json
import mimetypes
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "event.json"
README = ROOT / "README.md"
FILES_DIR = "event"
START, END = "<!-- event:start", "<!-- event:end -->"
STUDIO = "https://nomadicmehul.dev/demo-studio.html"
# type → (default label, emoji); order is the order links appear in the README
LINK_TYPES = {
    "event": ("Event Page", "🌐"), "slides": ("Slides", "📑"), "code": ("Code", "💻"), "demo": ("Live Demo", "▶️"),
    "video": ("Recording", "🎥"), "blog": ("Blog Post", "✍️"), "other": ("Link", "🔗"),
}
TEXT_FIELDS = {"Title": "title", "Event": "event", "Type": "type", "Location": "location", "About": "about"}
LIST_FIELDS = {"Speakers": "speakers", "Topics": "topics"}
DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%d.%m.%Y", "%d %b %Y", "%d %B %Y", "%b %d %Y", "%B %d %Y")
ATTACHMENT = re.compile(r"^https://(github\.com/(user-attachments/|[^/]+/[^/]+/files/)|(private-)?user-images\.githubusercontent\.com/)")
MD_LINK = re.compile(r"!?\[([^\]]*)\]\((https?://[^)\s]+)\)")
IMAGE = re.compile(r"\.(png|jpe?g|gif|webp|svg)$", re.I)
MAX_BYTES = 95 * 1024 * 1024  # GitHub rejects files over 100 MB
UA = "Mozilla/5.0 (event-info; +https://nomadicmehul.dev)"


# ---------- reading the issue ----------

def parse_form(body):
    """Split an issue body ('### Label\\n\\nvalue' blocks) into {label: value}."""
    body = re.sub(r"<!--.*?-->", "", body or "", flags=re.S)  # hints like "drop the file here"
    fields = {}
    for block in re.split(r"^### ", body, flags=re.M)[1:]:
        label, _, value = block.partition("\n")
        value = value.strip()
        fields[label.strip()] = "" if value == "_No response_" else value
    return fields


def csv(value):
    return [v.strip() for v in value.split(",") if v.strip()]


def parse_date(value):
    s = " ".join(re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", value.replace(",", " ")).split())
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    return None


def first_link(value):
    """(name, url) of the first markdown link or bare URL in value, else None."""
    m = MD_LINK.search(value)
    if m:
        return m.group(1), m.group(2)
    m = re.search(r"https?://\S+", value)
    return ("", m.group(0)) if m else None


# ---------- files ----------

def clean_name(name):
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", unquote(name))
    return re.sub(r"-{2,}", "-", name).strip("-.") or "file"


def fetch(url):
    """Bytes, filename and content type of url. Private-repo attachments need the token, which
    must not follow the redirect to the storage host, hence add_unredirected_header."""
    token = os.environ.get("GH_TOKEN")
    for auth in ([False, True] if token else [False]):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        if auth:
            req.add_unredirected_header("Authorization", f"token {token}")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read(MAX_BYTES + 1)
                return data, resp.headers.get_filename(), resp.headers.get_content_type()
        except urllib.error.HTTPError as e:
            if auth or e.code not in (401, 403, 404):
                raise
    raise ValueError("not found")


def save(url, hint="", name=None):
    """Download url into event/ (as `name` if given); returns the repo path."""
    data, served_name, ctype = fetch(url)
    if len(data) > MAX_BYTES:
        raise ValueError("file is over 95 MB — host it elsewhere and paste the URL")
    ext = mimetypes.guess_extension(ctype) or ""
    if name:
        name += Path(served_name or urlparse(url).path).suffix or ext
    else:
        name = next((n for n in (served_name, Path(urlparse(url).path).name, hint) if n and Path(n).suffix), None) or (hint or "file") + ext
    stem, suffix = Path(clean_name(name)).stem, Path(clean_name(name)).suffix
    target, n = ROOT / FILES_DIR / f"{stem}{suffix}", 1
    while target.exists() and target.read_bytes() != data and not name.startswith("poster"):
        n += 1
        target = ROOT / FILES_DIR / f"{stem}-{n}{suffix}"
    target.parent.mkdir(exist_ok=True)
    target.write_bytes(data)
    return target.relative_to(ROOT).as_posix()


def stored(ev):
    """Every event/ path the event links to."""
    paths = [ev.get("poster", "")] + ev.get("files", []) + [l["url"] for l in ev.get("links", [])]
    return {p for p in paths if p.startswith(FILES_DIR + "/")}


# ---------- applying the issue ----------

def apply(f, ev, errors):
    for label, key in TEXT_FIELDS.items():
        value = f.get(label, "")
        if value == "-":
            ev.pop(key, None)
        elif value:
            ev[key] = value
    for label, key in LIST_FIELDS.items():
        value = f.get(label, "")
        if value == "-":
            ev.pop(key, None)
        elif value:
            ev[key] = csv(value)
    if f.get("Date") == "-":
        ev.pop("date", None)
    elif f.get("Date"):
        day = parse_date(f["Date"])
        if day:
            ev["date"] = day.isoformat()
        else:
            errors.append(f"**Date** must be a date like `2026-06-09` or `9 Jun 2026` (got `{f['Date']}`)")

    if f.get("Links") == "-":
        ev.pop("links", None)
    elif f.get("Links"):
        ev["links"] = read_links(f["Links"], errors)

    poster = f.get("Poster", "")
    if poster == "-":
        ev.pop("poster", None)
    elif poster.startswith(FILES_DIR + "/"):
        ev["poster"] = poster.split()[0]
    elif poster:
        link = first_link(poster)
        if not link:
            errors.append("**Poster**: drag an image into the issue or paste an image URL")
        else:
            try:
                ev["poster"] = save(link[1], link[0], name="poster")
            except (OSError, ValueError) as e:
                errors.append(f"**Poster**: couldn't save `{link[1]}` ({e})")

    files = f.get("Files", "")
    if files == "-":
        ev.pop("files", None)
    elif files:
        kept = [line.strip() for line in files.splitlines() if line.strip().startswith(FILES_DIR + "/")]
        missing = [p for p in kept if not (ROOT / p).is_file()]
        errors += [f"**Files**: `{p}` isn't in the repo" for p in missing]
        new = []
        for name, url in MD_LINK.findall(files) or [("", u) for u in re.findall(r"https?://\S+", files)]:
            try:
                new.append(save(url, name))
            except (OSError, ValueError) as e:
                errors.append(f"**Files**: couldn't save `{name or url}` ({e})")
        ev["files"] = list(dict.fromkeys(kept + new))

    if not ev.get("title"):
        errors.append("**Title** is required")


def read_links(text, errors):
    links, pending = [], None  # pending: a "slides |" line whose file was dropped on the next line
    for line in text.splitlines():
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) == 1 and pending is not None and first_link(line):
            pending["url"], pending = first_link(line)[1], None
            continue
        if len(parts) > 3 and parts[2].startswith("["):  # a dropped file whose name has a "|"
            parts = parts[:2] + ["|".join(parts[2:])]
        if len(parts) not in (2, 3):
            errors.append(f"**Links**: can't read `{line.strip()}` — use `type | url` or `type | label | url`")
            continue
        rtype = parts[0].lower()
        if rtype not in LINK_TYPES:
            errors.append(f"**Links**: unknown type `{rtype}` — use: {', '.join(LINK_TYPES)}")
            continue
        url = first_link(parts[-1])[1] if first_link(parts[-1]) else parts[-1]
        links.append({"type": rtype, "label": parts[1] if len(parts) == 3 else LINK_TYPES[rtype][0], "url": url})
        pending = links[-1] if not url else None
    for link in links:
        if not link["url"]:
            errors.append(f"**Links**: `{link['type']}` has no URL or file — drag the file in after `{link['type']} |`")
        elif ATTACHMENT.match(link["url"]):
            try:
                link["url"] = save(link["url"], link["type"])
            except (OSError, ValueError) as e:
                errors.append(f"**Links**: couldn't save the `{link['type']}` file ({e})")
        elif not re.match(r"^https?://\S+$", link["url"]) and not (ROOT / link["url"]).is_file():
            errors.append(f"**Links**: `{link['type']}` must be a full URL (got `{link['url']}`)")
    return links


# ---------- README ----------

def href(path):
    return path if re.match(r"^https?://", path) else quote(path)


def render(ev):
    title = ev.get("title", "Untitled")
    out = [f"{START} — generated from event.json by .github/scripts/event_info.py; change it with an “[event]” issue -->", ""]
    if ev.get("poster"):
        out += [f'<p align="center"><img src="{href(ev["poster"])}" alt="{title} poster" width="760"></p>', ""]
    out += [f"# {title}", ""]
    meta = []
    kind, event = ev.get("type"), ev.get("event")
    if event:
        meta.append((f"**{kind}** at " if kind else "") + f"**{event}**")
    elif kind:
        meta.append(f"**{kind}**")
    if ev.get("date"):
        meta.append("📅 " + date.fromisoformat(ev["date"]).strftime("%a, %-d %b %Y"))
    if ev.get("location"):
        meta.append(f"📍 {ev['location']}")
    if meta:
        out += [" · ".join(meta), ""]
    if ev.get("speakers"):
        out += ["🎤 " + ", ".join(ev["speakers"]), ""]
    links = sorted(ev.get("links", []), key=lambda l: list(LINK_TYPES).index(l["type"]))
    if links:
        out += [" · ".join(f"**[{LINK_TYPES[l['type']][1]} {l['label']}]({href(l['url'])})**" for l in links), ""]
    if ev.get("topics"):
        out += [" ".join(f"`{t}`" for t in ev["topics"]), ""]
    if ev.get("about"):
        out += ["## About", "", ev["about"], ""]
    files = ev.get("files", [])
    docs, images = [p for p in files if not IMAGE.search(p)], [p for p in files if IMAGE.search(p)]
    if docs:
        out += ["## Files", ""] + [f"- 📎 [{Path(p).name}]({href(p)})" for p in docs] + [""]
    if images:
        out += ["## Gallery", "", "<p>" + " ".join(f'<a href="{href(p)}"><img src="{href(p)}" alt="{Path(p).name}" width="240"></a>' for p in images) + "</p>", ""]
    return "\n".join(out + [END])


def write_readme(ev):
    block = render(ev)
    text = README.read_text() if README.exists() else ""
    if START in text and END in text:
        text = text[:text.index(START)] + block + text[text.index(END) + len(END):]
    else:
        text = block + "\n\n" + text
    README.write_text(text)


# ---------- main ----------

def main():
    result = Path(os.environ.get("RESULT_FILE", os.devnull))
    ev = json.loads(DATA.read_text()) if DATA.exists() else {}
    if os.environ.get("EVENT_NAME") == "issues":
        before = stored(ev)
        errors = []
        apply(parse_form(os.environ.get("ISSUE_BODY", "")), ev, errors)
        if errors:
            result.write_text("❌ Couldn't save the event info:\n\n" + "\n".join(f"- {e}" for e in errors)
                              + "\n\nEdit the issue to fix it — the workflow re-runs automatically.")
            return 1
        for p in before - stored(ev):  # replaced poster, removed files
            (ROOT / p).unlink(missing_ok=True)
        ev["updated"] = date.today().isoformat()
        DATA.write_text(json.dumps(ev, indent=2, ensure_ascii=False) + "\n")
    elif not ev:
        print("No event.json yet — nothing to render")
        return 0
    write_readme(ev)

    repo = os.environ.get("GITHUB_REPOSITORY", "")
    files = sorted(stored(ev))
    result.write_text(
        f"✅ Saved **{ev['title']}** — [README](https://github.com/{repo}#readme) and `event.json` are updated.\n\n"
        + (f"📁 Files in `{FILES_DIR}/`:\n" + "".join(f"- [`{p}`](https://github.com/{repo}/blob/HEAD/{quote(p)})\n" for p in files) + "\n" if files else "")
        + f"To change anything later, use [Demo Studio]({STUDIO}?repo={repo.split('/')[-1]}) or open an **Event info** issue here."
    )
    print(f"Rendered README for {ev['title']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
