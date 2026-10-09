#!/usr/bin/env python3
"""normalize_sources.py — normalize raw feed items to a common schema.

Reads data/raw_items.json, cleans HTML from summaries, canonicalizes URLs,
parses publication dates to ISO 8601, and writes data/normalized_items.json.

Usage: python automation/normalize_sources.py
"""
import argparse
import html
import json
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

ROOT = Path(__file__).resolve().parent.parent
TRACKING_PARAMS = {"utm_source", "utm_medium", "utm_campaign", "utm_term",
                   "utm_content", "fbclid", "gclid", "mc_cid", "mc_eid"}


def strip_html(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def canonical_url(url):
    """Lowercase host, strip tracking params and fragments."""
    try:
        parts = urlsplit(url.strip())
        if not parts.scheme.startswith("http"):
            return url.strip()
        q = [(k, v) for k, v in parse_qsl(parts.query) if k not in TRACKING_PARAMS]
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(),
                           parts.path.rstrip("/") or "/", urlencode(q), ""))
    except Exception:
        return (url or "").strip()


def parse_date(raw):
    if not raw:
        return ""
    for fn in (parsedate_to_datetime,
               lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))):
        try:
            dt = fn(raw)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc).isoformat()
        except Exception:
            continue
    return ""


def main():
    ap = argparse.ArgumentParser(description="Normalize raw feed items.")
    ap.add_argument("--inp", default=str(ROOT / "data" / "raw_items.json"))
    ap.add_argument("--out", default=str(ROOT / "data" / "normalized_items.json"))
    args = ap.parse_args()

    with open(args.inp, encoding="utf-8") as f:
        raw = json.load(f)

    items = []
    for e in raw.get("items", []):
        title = strip_html(e.get("title", ""))
        url = canonical_url(e.get("link", ""))
        if not title or not url:
            continue
        items.append({
            "source_name": e.get("source_name", ""),
            "source_categories": e.get("source_categories", []),
            "title": title,
            "url": url,
            "published_at": parse_date(e.get("published", "")),
            "summary": strip_html(e.get("summary", ""))[:1500],
            "collected_at": raw.get("fetched_at", ""),
        })

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"count": len(items), "items": items}, f,
                  ensure_ascii=False, indent=2)
    print(f"[normalize] {len(items)} items -> {args.out}")


if __name__ == "__main__":
    main()
