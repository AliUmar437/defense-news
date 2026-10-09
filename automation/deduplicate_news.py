#!/usr/bin/env python3
"""deduplicate_news.py — drop already-processed stories.

Reads data/normalized_items.json plus the persistent store
data/processed_items.json, keeps only unseen items, records their
identifiers, and writes data/new_items.json.

Identity = sha256(canonical URL); falls back to sha256(source + title)
when the URL is missing. Also guards against near-duplicate headlines
from different sources via normalized-title comparison.

Usage: python automation/deduplicate_news.py
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def norm_title(t):
    t = t.lower()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def item_id(item):
    if item.get("url"):
        return hashlib.sha256(item["url"].encode()).hexdigest()
    key = (item.get("source_name", "") + "|" + item.get("title", "")).encode()
    return hashlib.sha256(key).hexdigest()


def load_store(path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"processed_ids": []}


def main():
    ap = argparse.ArgumentParser(description="Deduplicate normalized items.")
    ap.add_argument("--inp", default=str(ROOT / "data" / "normalized_items.json"))
    ap.add_argument("--store", default=str(ROOT / "data" / "processed_items.json"))
    ap.add_argument("--out", default=str(ROOT / "data" / "new_items.json"))
    args = ap.parse_args()

    with open(args.inp, encoding="utf-8") as f:
        items = json.load(f).get("items", [])
    store = load_store(args.store)
    seen = set(store.get("processed_ids", []))
    seen_titles = set(store.get("processed_titles", []))

    fresh = []
    for it in items:
        iid = item_id(it)
        nt = norm_title(it.get("title", ""))
        if iid in seen or (nt and nt in seen_titles):
            continue
        it["dedup_id"] = iid
        fresh.append(it)
        seen.add(iid)
        if nt:
            seen_titles.add(nt)

    # Persist state BEFORE writing output so a later crash can't republish.
    store["processed_ids"] = sorted(seen)
    store["processed_titles"] = sorted(seen_titles)
    Path(args.store).parent.mkdir(parents=True, exist_ok=True)
    with open(args.store, "w", encoding="utf-8") as f:
        json.dump(store, f, ensure_ascii=False, indent=2)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"count": len(fresh), "items": fresh}, f,
                  ensure_ascii=False, indent=2)
    print(f"[dedupe] {len(items)} in, {len(fresh)} new -> {args.out}")


if __name__ == "__main__":
    main()
