#!/usr/bin/env python3
"""validate_articles.py — validate drafts before publication.

Reads data/drafts.json, applies the fact-checking rules, and splits drafts
into data/approved.json (safe to publish) and data/review_queue.json
(needs a human). Never approves: empty bodies, invalid source URLs,
unparseable dates, placeholder text, or drafts flagged needsReview when
the publication policy demands review.

Usage: python automation/validate_articles.py
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDERS = ["lorem ipsum", "todo", "tbd", "[insert", "xxx", "placeholder"]


def valid_url(u):
    try:
        p = urlsplit(u)
        return p.scheme in ("http", "https") and bool(p.netloc)
    except Exception:
        return False


def valid_date(s):
    try:
        datetime.fromisoformat(s.replace("Z", "+00:00"))
        return True
    except Exception:
        return False


def validate(d):
    """Return (ok, [reasons])."""
    reasons = []
    if not d.get("title") or len(d["title"]) < 15:
        reasons.append("headline too short or missing")
    if not d.get("summary") or len(d["summary"]) < 40:
        reasons.append("summary too short or missing")
    if not d.get("content") or len(d["content"].split()) < 100:
        reasons.append("body too short (<100 words) or empty")
    if not valid_url(d.get("sourceUrl", "")):
        reasons.append("source URL invalid")
    if not valid_date(d.get("publishedAt", "")):
        reasons.append("publication date unparseable")
    blob = (d.get("title", "") + d.get("summary", "") + d.get("content", "")).lower()
    if any(p in blob for p in PLACEHOLDERS):
        reasons.append("placeholder text detected")
    if d.get("needsReview"):
        reasons.append("flagged for human review (sensitive topic or no AI draft)")
    return (not reasons), reasons


def main():
    ap = argparse.ArgumentParser(description="Validate article drafts.")
    ap.add_argument("--inp", default=str(ROOT / "data" / "drafts.json"))
    ap.add_argument("--approved", default=str(ROOT / "data" / "approved.json"))
    ap.add_argument("--review", default=str(ROOT / "data" / "review_queue.json"))
    args = ap.parse_args()

    try:
        with open(args.inp, encoding="utf-8") as f:
            drafts = json.load(f).get("drafts", [])
    except FileNotFoundError:
        drafts = []

    approved, review = [], []
    for d in drafts:
        ok, reasons = validate(d)
        d["validation"] = {"passed": ok, "reasons": reasons,
                           "checked_at": datetime.now(timezone.utc).isoformat()}
        if ok:
            d["status"] = "approved"
            d["verificationStatus"] = "validated"
            approved.append(d)
        else:
            d["status"] = "needs_review"
            review.append(d)

    for path, items in ((args.approved, approved), (args.review, review)):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"count": len(items), "items": items}, f,
                      ensure_ascii=False, indent=2)
    print(f"[validate] {len(drafts)} drafts: {len(approved)} approved, "
          f"{len(review)} need review")


if __name__ == "__main__":
    main()
