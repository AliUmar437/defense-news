#!/usr/bin/env python3
"""fetch_news.py — collect recent stories from configured RSS/Atom feeds.

Reads config/news_sources.json, fetches each enabled feed with feedparser,
and writes raw items to data/raw_items.json. Per-feed failures are logged
and skipped; the run never aborts because one source is down.

Usage: python automation/fetch_news.py [--config config/news_sources.json]
"""
import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

try:
    import feedparser
except ImportError:
    print("ERROR: feedparser is required. Install with: pip install -r requirements.txt",
          file=sys.stderr)
    sys.exit(2)


def load_sources(config_path):
    with open(config_path, encoding="utf-8") as f:
        data = json.load(f)
    return [s for s in data.get("sources", []) if s.get("enabled")]


def fetch_feed(source, timeout=20):
    """Fetch one feed. Returns (items, error)."""
    items = []
    try:
        feed = feedparser.parse(source["url"],
                                agent="DefenseNewsBot/1.0 (+news aggregator)",
                                request_headers={})
        # feedparser honors timeout via socket default; set a sane one
        import socket
        old = socket.getdefaulttimeout()
        socket.setdefaulttimeout(timeout)
        try:
            feed = feedparser.parse(source["url"], agent="DefenseNewsBot/1.0")
        finally:
            socket.setdefaulttimeout(old)
        status = getattr(feed, "status", None)
        if status and status >= 400:
            return [], f"HTTP {status}"
        if getattr(feed, "bozo", False) and not feed.entries:
            exc = getattr(feed, "bozo_exception", None)
            return [], f"parse error: {exc}"
        for e in feed.entries:
            items.append({
                "source_name": source["name"],
                "source_categories": source.get("categories", []),
                "title": (e.get("title") or "").strip(),
                "link": (e.get("link") or "").strip(),
                "published": e.get("published") or e.get("updated") or "",
                "summary": (e.get("summary") or e.get("description") or "").strip()[:2000],
            })
        return items, None
    except Exception as exc:  # never let one feed kill the run
        return [], f"{type(exc).__name__}: {exc}"


def main():
    ap = argparse.ArgumentParser(description="Fetch defense news feeds.")
    ap.add_argument("--config", default=str(ROOT / "config" / "news_sources.json"))
    ap.add_argument("--out", default=str(ROOT / "data" / "raw_items.json"))
    args = ap.parse_args()

    sources = load_sources(args.config)
    all_items, errors = [], {}
    for src in sources:
        items, err = fetch_feed(src)
        if err:
            errors[src["name"]] = err
            print(f"[fetch] {src['name']}: FAILED — {err}", file=sys.stderr)
        else:
            print(f"[fetch] {src['name']}: {len(items)} items")
        all_items.extend(items)
        time.sleep(1)  # be polite to sources

    payload = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "item_count": len(all_items),
        "errors": errors,
        "items": all_items,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"[fetch] wrote {len(all_items)} items to {args.out} "
          f"({len(errors)} source errors)")


if __name__ == "__main__":
    main()
