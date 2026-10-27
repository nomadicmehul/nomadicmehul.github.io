#!/usr/bin/env python3
"""Check every link in data/*.json and write a markdown report.

Used by .github/workflows/check-links.yml. Writes:
  - $REPORT_FILE: markdown report (broken links + ones that couldn't be verified)
  - $GITHUB_OUTPUT: broken=<count>

Only clear failures (404/410, DNS errors, missing local slide files) count as
broken. Sites that block bots (403/429/999, timeouts, 5xx) are listed
separately as "couldn't verify" so they don't cause false alarms.
"""
import json
import os
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
UA = "Mozilla/5.0 (link-check; +https://nomadicmehul.dev)"
BROKEN_STATUSES = {404, 410}


def collect():
    """(where, url) pairs; local slide filenames are returned as-is."""
    links = []
    for e in json.loads((ROOT / "data/speaking.json").read_text()):
        for r in e.get("resources", []):
            links.append((f"🎤 {e['title']} ({e.get('date', e['year'])}) · {r['type']}", r["url"]))
    for p in json.loads((ROOT / "data/projects.json").read_text()):
        links.append((f"🚀 {p['title']} · repo", p["repo"]))
    for t in json.loads((ROOT / "data/testimonials.json").read_text()):
        if t.get("link"):
            links.append((f"💬 {t['name']} · link", t["link"]))
    return links


def check(url):
    """Return (status, detail): status is 'ok', 'broken' or 'unsure'."""
    if not url.startswith("http"):
        ok = (ROOT / "assets" / "slides" / url).exists()
        return ("ok", "") if ok else ("broken", "file missing from assets/slides/")
    last = ""
    # HEAD is cheap but some servers answer it wrongly (e.g. cloud.google.com 404s HEAD), so only a GET can mark a link broken
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=20):
                return "ok", ""
        except urllib.error.HTTPError as e:
            if method == "HEAD":
                continue
            if e.code in BROKEN_STATUSES:
                return "broken", f"HTTP {e.code}"
            if 300 <= e.code < 400:  # redirect urllib didn't follow (e.g. 308 on older Pythons) — page exists
                return "ok", ""
            last = f"HTTP {e.code}"
        except urllib.error.URLError as e:
            reason = str(e.reason)
            if "Name or service not known" in reason or "nodename nor servname" in reason:
                return "broken", "domain doesn't resolve"
            last = reason
        except Exception as e:  # timeouts, connection resets
            last = type(e).__name__
    return "unsure", last


def main():
    links = collect()
    unique = sorted({url for _, url in links})
    with ThreadPoolExecutor(max_workers=16) as pool:
        results = dict(zip(unique, pool.map(check, unique)))

    broken = [(w, u, results[u][1]) for w, u in links if results[u][0] == "broken"]
    unsure = [(w, u, results[u][1]) for w, u in links if results[u][0] == "unsure"]

    lines = [f"Checked **{len(unique)}** links from `data/*.json`.", ""]
    if broken:
        lines += ["## ❌ Broken", "", "| Where | Link | Why |", "|---|---|---|"]
        lines += [f"| {w} | {u} | {d} |" for w, u, d in broken]
        lines += ["", "Fix with the **✏️ Update or remove entry** issue form, or edit the JSON directly.", ""]
    else:
        lines += ["✅ No broken links.", ""]
    if unsure:
        lines += ["<details><summary>Couldn't verify " + str(len(unsure)) + " links (site blocks bots or timed out) — usually fine</summary>", "",
                  "| Where | Link | Response |", "|---|---|---|"]
        lines += [f"| {w} | {u} | {d} |" for w, u, d in unsure]
        lines += ["", "</details>"]

    Path(os.environ.get("REPORT_FILE", "/dev/stdout")).write_text("\n".join(lines) + "\n")
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as out:
        out.write(f"broken={len(broken)}\n")
    print(f"{len(unique)} links: {len(broken)} broken, {len(unsure)} unverified")


if __name__ == "__main__":
    main()
