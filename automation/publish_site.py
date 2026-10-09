#!/usr/bin/env python3
"""publish_site.py — run the full pipeline: collect -> publish.

Orchestrates: fetch_news -> normalize_sources -> deduplicate_news ->
generate_articles -> validate_articles -> merge approved articles into
data/articles.json -> scripts/build_site.py (article pages, sitemap, RSS).

Publication policy (config/pipeline.json):
  mode=auto   -> validated articles are published automatically.
  mode=review -> validated articles are ALSO held in the review queue;
                 only items explicitly approved by a human are published.

Sensitive topics are always held for review regardless of mode.

Usage: python automation/publish_site.py [--max N]
"""
import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run_step(name, script, *args):
    print(f"--- {name} ---")
    r = subprocess.run([sys.executable, str(ROOT / "automation" / script),
                        *args], cwd=ROOT)
    if r.returncode != 0:
        print(f"[{name}] FAILED (exit {r.returncode})", file=sys.stderr)
        sys.exit(r.returncode)


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def main():
    ap = argparse.ArgumentParser(description="Run the publishing pipeline.")
    ap.add_argument("--max", type=int, default=10,
                    help="max articles published per run")
    args = ap.parse_args()

    with open(ROOT / "config" / "pipeline.json", encoding="utf-8") as f:
        policy = json.load(f)["publication_policy"]["mode"]
    print(f"[pipeline] publication policy: {policy}")

    run_step("fetch", "fetch_news.py")
    run_step("normalize", "normalize_sources.py")
    run_step("dedupe", "deduplicate_news.py")
    run_step("generate", "generate_articles.py")
    run_step("validate", "validate_articles.py")

    approved = load_json(ROOT / "data" / "approved.json",
                         {"items": []})["items"]
    articles_path = ROOT / "data" / "articles.json"
    articles = load_json(articles_path, [])
    existing_slugs = {a.get("slug") for a in articles}

    published = 0
    review_held = []
    for d in approved:
        if policy != "auto":
            d["status"] = "needs_review"
            review_held.append(d)
            continue
        slug = d["slug"]
        i = 2
        while slug in existing_slugs:  # prevent duplicate slugs
            slug = f"{d['slug']}-{i}"
            i += 1
        d["slug"] = slug
        d["status"] = "published"
        articles.append(d)
        existing_slugs.add(slug)
        published += 1
        if published >= args.max:
            break

    if review_held:
        rq = load_json(ROOT / "data" / "review_queue.json", {"items": []})
        seen = {x.get("id") for x in rq["items"]}
        for d in review_held:
            if d["id"] not in seen:
                rq["items"].append(d)
        rq["count"] = len(rq["items"])
        with open(ROOT / "data" / "review_queue.json", "w", encoding="utf-8") as f:
            json.dump(rq, f, ensure_ascii=False, indent=2)

    if published:
        articles.sort(key=lambda a: a.get("publishedAt", ""), reverse=True)
        with open(articles_path, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"[pipeline] published {published} new articles")
    else:
        print("[pipeline] no new articles published "
              f"({len(review_held)} held for review)")

    # Rebuild static artifacts (article pages, sitemap, RSS) every run.
    print("--- build_site ---")
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "build_site.py")],
                       cwd=ROOT)
    if r.returncode != 0:
        print("[build_site] FAILED", file=sys.stderr)
        sys.exit(r.returncode)

    print(f"[pipeline] done at {datetime.now(timezone.utc).isoformat()} — "
          f"published={published}, held={len(review_held)}")


if __name__ == "__main__":
    main()
