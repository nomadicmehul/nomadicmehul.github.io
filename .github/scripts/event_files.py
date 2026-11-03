#!/usr/bin/env python3
"""Keep each speaking event's files in its own folder: assets/events/<year>/<date>-<title-slug>/.

A resource url can be a web URL or a file on the site. organize() puts the files where they belong:
  - files dragged into a GitHub issue (github.com/user-attachments/...) are downloaded,
    because GitHub serves those as downloads, while files served by Pages open in the browser
  - local files (a bare name in assets/slides/, or an assets/... path) are copied into the
    event's folder, e.g. after its title or date changed
and points the resource at the file's path from the site root. prune() then deletes old
copies that no event links to any more.

Run directly to tidy every event in data/speaking.json (edit-forms.yml does this after a direct push).
"""
import json
import mimetypes
import re
import shutil
import sys
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
EVENTS_DIR = "assets/events"
LEGACY_DIR = "assets/slides"  # bare filenames resolve here (older entries)
ATTACHMENT = re.compile(r"^https://(github\.com/(user-attachments/|[^/]+/[^/]+/files/)|(private-)?user-images\.githubusercontent\.com/)")
MAX_BYTES = 95 * 1024 * 1024  # GitHub rejects files over 100 MB
UA = "Mozilla/5.0 (event-files; +https://nomadicmehul.dev)"


def slug(text, limit=60):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if len(s) > limit:
        s = s[:limit].rsplit("-", 1)[0]
    return s or "event"


def folder(entry):
    """Site-root folder for an event's files, e.g. assets/events/2026/2026-10-22-berlin-claude-workshop."""
    return f"{EVENTS_DIR}/{entry['date'][:4]}/{entry['date']}-{slug(entry['title'])}"


def local_path(url):
    """Site-root path of a local file resource; '' for a web URL."""
    if re.match(r"^https?://", url):
        return ""
    return url if url.startswith("assets/") else f"{LEGACY_DIR}/{url}"


def local_paths(entry):
    return [p for r in entry.get("resources", []) if (p := local_path(r["url"]))]


def clean_name(name):
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", unquote(name))
    return re.sub(r"-{2,}", "-", name).strip("-.") or "file"


def place(data, name, dest):
    """Write bytes to dest/name (adding -2, -3… if a different file has that name); returns the site-root path."""
    stem, suffix = Path(name).stem, "".join(Path(name).suffixes[-1:])
    target, n = ROOT / dest / name, 1
    while target.exists() and target.read_bytes() != data:
        n += 1
        target = ROOT / dest / f"{stem}-{n}{suffix}"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    return target.relative_to(ROOT).as_posix()


def download(url, dest, rtype):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read(MAX_BYTES + 1)
        name = resp.headers.get_filename() or Path(urlparse(url).path).name
        ctype = resp.headers.get_content_type()
    if len(data) > MAX_BYTES:
        raise ValueError("file is over 95 MB — host it elsewhere and paste the URL")
    if not Path(name).suffix:  # pasted images arrive as .../assets/<uuid>
        name = rtype + (mimetypes.guess_extension(ctype) or "")
    return place(data, clean_name(name), dest)


def organize(entry, errors):
    """Download or copy the entry's files into its folder; returns the site-root paths it wrote."""
    dest, saved = folder(entry), []
    for r in entry.get("resources", []):
        url, src = r["url"], local_path(r["url"])
        try:
            if ATTACHMENT.match(url):
                r["url"] = download(url, dest, r["type"])
            elif src and Path(src).parent.as_posix() != dest and (ROOT / src).is_file():
                r["url"] = place((ROOT / src).read_bytes(), clean_name(Path(src).name), dest)
            else:
                continue
        except (OSError, ValueError) as e:
            errors.append(f"**{r['type']}**: couldn't save `{url}` to the site ({e})")
            continue
        saved.append(r["url"])
    return saved


def prune(paths, events):
    """Delete files in `paths` that no event links to any more, then any folders left empty."""
    used = {p for e in events for p in local_paths(e)}
    for p in set(paths) - used:
        if not p.startswith((EVENTS_DIR + "/", LEGACY_DIR + "/")) or ".." in p:
            continue
        f = ROOT / p
        if f.is_file():
            f.unlink()
        d = f.parent
        while d != ROOT / "assets" and d.is_dir() and not any(d.iterdir()):
            d.rmdir()
            d = d.parent


def main():
    path = ROOT / "data" / "speaking.json"
    events = json.loads(path.read_text())
    before = [p for e in events for p in local_paths(e)]
    errors, saved = [], []
    for e in events:
        saved += organize(e, errors)
    prune(before, events)
    path.write_text(json.dumps(events, indent=2, ensure_ascii=False) + "\n")
    for p in saved:
        print(f"saved {p}")
    for err in errors:
        print(f"error: {err}", file=sys.stderr)
    print(f"{len(saved)} file(s) organized, {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
