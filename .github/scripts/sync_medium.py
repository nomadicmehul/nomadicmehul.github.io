#!/usr/bin/env python3
"""Fetch the Medium RSS feed and merge it into data/blog.json.

Medium's feed only returns the latest ~10 posts, so new posts are merged into
the existing file (keyed by link) rather than replacing it — older articles
stay in the archive.

Exits 0 without touching the file if the feed can't be fetched, so a flaky
Medium/Cloudflare response never wipes the blog.
"""
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED_URL = "https://medium.com/feed/@nomadicmehul"
OUT = Path(__file__).resolve().parents[2] / "data" / "blog.json"
NS = {"content": "http://purl.org/rss/1.0/modules/content/"}


def strip_html(s):
    text = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def first_image(s):
    m = re.search(r'<img[^>]+src="([^"]+)"', s or "")
    return m.group(1) if m else ""


def parse_feed(xml_bytes):
    root = ET.fromstring(xml_bytes)
    posts = []
    for item in root.iter("item"):
        content = item.findtext("content:encoded", default="", namespaces=NS)
        text = strip_html(content)
        # Medium content usually opens with the cover image, then the lede
        excerpt = text[:160].rsplit(" ", 1)[0] + "..." if len(text) > 160 else text
        words = len(text.split())
        posts.append({
            "title": html.unescape(item.findtext("title", "").strip()),
            "link": item.findtext("link", "").split("?")[0],
            "pubDate": parsedate_to_datetime(item.findtext("pubDate")).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "thumbnail": first_image(content),
            "excerpt": excerpt,
            "readTime": f"{max(1, round(words / 200))} min read",
            "categories": [c.text for c in item.findall("category") if c.text],
        })
    return posts


def main():
    req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0 (blog-sync; +https://nomadicmehul.dev)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            fresh = parse_feed(resp.read())
    except Exception as e:  # network error, Cloudflare challenge page, bad XML
        print(f"::warning::Could not fetch Medium feed, keeping existing blog.json: {e}")
        return 0

    if not fresh:
        print("::warning::Medium feed had no items, keeping existing blog.json")
        return 0

    existing = json.loads(OUT.read_text()) if OUT.exists() else []
    by_link = {p["link"]: p for p in existing}
    by_link.update({p["link"]: p for p in fresh})
    posts = sorted(by_link.values(), key=lambda p: p["pubDate"], reverse=True)

    OUT.write_text(json.dumps(posts, indent=2, ensure_ascii=False) + "\n")
    print(f"blog.json: {len(posts)} posts ({len(fresh)} in feed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
