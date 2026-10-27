#!/usr/bin/env python3
"""Keep `added` / `updated` dates (YYYY-MM-DD) on every entry in data/*.json.

  stamp_dates.py --base <git ref>   compare the working tree with <ref>; new entries get
                                    added + updated = today, changed entries get updated = today
  stamp_dates.py --backfill         fill in missing dates from git history

Used by issue-to-data.yml (--base HEAD, before committing a form submission) and
edit-forms.yml (--base <previous commit>, after a direct push). An entry is
identified by speaking: title + year, project: repo, testimonial: quote; a renamed
entry keeps its `added` date and gets a new `updated` one.
"""
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = {
    "data/speaking.json": lambda e: f"{e.get('title')}|{e.get('year')}",
    "data/projects.json": lambda e: e.get("repo"),
    "data/testimonials.json": lambda e: e.get("quote"),
}
META = ("added", "updated")


def content(e):
    return {k: v for k, v in e.items() if k not in META}


def load_at(ref, path):
    """JSON list of a file at a git ref ([] if missing or unparseable)."""
    try:
        out = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
        return json.loads(out)
    except (subprocess.CalledProcessError, json.JSONDecodeError):
        return []


def write(path, data):
    (ROOT / path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def stamp(base, today):
    for path, key in FILES.items():
        old = {key(e): content(e) for e in load_at(base, path)}
        data = json.loads((ROOT / path).read_text())
        stamped = 0
        for e in data:
            k = key(e)
            if k in old and content(e) == old[k]:
                continue
            if k not in old:
                e.setdefault("added", today)
            e["updated"] = today
            stamped += 1
        if stamped:
            write(path, data)
        print(f"{path}: {stamped} entr{'y' if stamped == 1 else 'ies'} stamped {today}")


def backfill(today):
    for path, key in FILES.items():
        history = subprocess.run(["git", "log", "--reverse", "--format=%H %cs", "--", path],
                                 cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
        seen = {}  # key -> {"added", "updated", "content"}
        for line in filter(None, history):
            sha, day = line.split()
            for e in load_at(sha, path):
                k, c = key(e), content(e)
                if k not in seen:
                    seen[k] = {"added": day, "updated": day, "content": c}
                elif seen[k]["content"] != c:
                    seen[k].update(updated=day, content=c)
        data = json.loads((ROOT / path).read_text())
        filled = 0
        for e in data:
            h = seen.get(key(e))
            # uncommitted entries (not in history yet) count as today
            if h and content(e) != h["content"]:
                h = {"added": h["added"], "updated": today}
            h = h or {"added": today, "updated": today}
            for field in META:
                if field not in e:
                    e[field] = h[field]
                    filled += 1
        write(path, data)
        print(f"{path}: filled {filled} date fields for {len(data)} entries")


def main():
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--base", help="git ref to compare the working tree against")
    group.add_argument("--backfill", action="store_true")
    args = ap.parse_args()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    if args.backfill:
        backfill(today)
    else:
        stamp(args.base, today)


if __name__ == "__main__":
    main()
