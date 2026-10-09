#!/usr/bin/env python3
"""generate_articles.py — turn new items into article drafts.

For each item in data/new_items.json:
  * classify into category / region / tags via keyword rules,
  * filter out irrelevant or low-quality items,
  * if an AI provider is configured (AI_API_KEY env, OpenAI-compatible),
    generate an original 400-800 word draft; otherwise queue the item
    with its source summary for later processing (never invent content).

Writes data/drafts.json. Never publishes directly — validation and the
publication policy in publish_site.py decide what goes live.

Usage: python automation/generate_articles.py
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CATEGORY_RULES = [
    ("Military Aviation", ["fighter", "aircraft", "jet", "air force", "bomber",
                           "helicopter", "airbase", "dogfight"]),
    ("Naval Warfare and Maritime Security", ["navy", "naval", "ship", "submarine",
        "carrier", "frigate", "destroyer", "maritime", "fleet"]),
    ("Ground Forces and Armored Vehicles", ["army", "tank", "armored", "artillery",
        "infantry", "howitzer", "ground forces"]),
    ("Missiles and Air Defense", ["missile", "air defense", "patriot", "thaad",
        "interceptor", "ballistic", "hypersonic", "s-400", "iron dome"]),
    ("Military Drones and Robotics", ["drone", "uav", "unmanned", "robotic",
        "loitering munition", "quadcopter"]),
    ("Defense Industry and Procurement", ["contract", "procurement", "deal worth",
        "billion", "million deal", "lockheed", "raytheon", "boeing", "acquisition"]),
    ("Military Exercises", ["exercise", "drill", "war game", "wargame", "joint training"]),
    ("Defense Technology", ["radar", "satellite", "cyber", "laser weapon", "ai ",
        "artificial intelligence", "sensor", "stealth"]),
]
REGION_RULES = [
    ("United States", ["u.s.", "us ", "pentagon", "american", "washington"]),
    ("China", ["china", "chinese", "pla ", "beijing"]),
    ("Russia", ["russia", "russian", "moscow", "kremlin"]),
    ("Pakistan", ["pakistan", "pakistani", "ispr", "rawalpindi"]),
    ("Europe", ["europe", "nato", "eu ", "german", "french", "british", "uk "]),
    ("Middle East", ["israel", "iran", "saudi", "gulf", "middle east", "turkey", "turkish"]),
    ("Indo-Pacific", ["taiwan", "japan", "south korea", "australia", "indo-pacific", "philippines"]),
]
SENSITIVE_HINTS = ["casualt", "killed", "death toll", "airstrike killed",
                   "disputed", "allegedly", "unverified", "breaking:"]


def classify(text):
    t = " " + text.lower() + " "
    category = "Global Military News"
    for cat, kws in CATEGORY_RULES:
        if any(k in t for k in kws):
            category = cat
            break
    region = "Global"
    for reg, kws in REGION_RULES:
        if any(k in t for k in kws):
            region = reg
            break
    tags = [w for w in re.findall(r"[a-z]{4,}", t)
            if w not in {"with", "from", "that", "this", "will", "have"}][:6]
    return category, region, sorted(set(tags))


def is_relevant(text):
    t = text.lower()
    if len(t) < 40:
        return False
    military = ["military", "defense", "defence", "army", "navy", "air force",
                "weapon", "missile", "drone", "pentagon", "troop", "warship",
                "fighter", "submarine", "radar", "nato"]
    return any(k in t for k in military)


def ai_configured():
    key = os.environ.get("AI_API_KEY", "").strip()
    if not key:
        return None
    with open(ROOT / "config" / "pipeline.json", encoding="utf-8") as f:
        cfg = json.load(f)["ai"]
    return {"key": key, "url": os.environ.get("AI_API_URL", cfg["api_url"]),
            "model": os.environ.get("AI_MODEL", cfg["model"])}


def ai_draft(cfg, item, category, region):
    """Call an OpenAI-compatible chat API. Returns dict or None on failure."""
    system = ("You are a veteran defense news wire journalist (AP/Reuters style). Write an ORIGINAL news article "
              "based only on the provided source material. Never invent quotes, "
              "casualty figures, troop movements, specifications, or statements. "
              "Keep confirmed facts separate from uncertainty. HUMAN STYLE RULES (mandatory): the article must read as human-written, never AI-generated. Use active voice and concrete details. Vary sentence and paragraph length naturally; never open two articles the same way. FORBIDDEN AI tics: delve, tapestry, landscape as metaphor, in today\u2019s fast-paced world, furthermore, moreover, it is important to note, in conclusion, game-changer, cutting-edge, revolutionize, seamless, testament to. No hype adjectives, no moralizing closings. Write short declarative sentences like a wire reporter. Respond ONLY with "
              "valid JSON: {\"headline\": str, \"summary\": str (1-2 sentences), "
              "\"body\": str (markdown, 400-800 words: opening paragraph, main "
              "developments, background, key facts), \"tags\": [str]}")
    user_msg = (f"SOURCE: {item['source_name']}\nHEADLINE: {item['title']}\n"
                f"SUMMARY: {item['summary']}\nURL: {item['url']}\n"
                f"CATEGORY: {category}\nREGION: {region}")
    payload = json.dumps({
        "model": cfg["model"],
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user_msg}],
        "temperature": 0.3, "response_format": {"type": "json_object"},
    }).encode()
    req = urllib.request.Request(
        cfg["url"], data=payload,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {cfg['key']}"})
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            data = json.loads(resp.read().decode())
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception as exc:
        print(f"[generate] AI call failed for '{item['title'][:50]}': {exc}",
              file=sys.stderr)
        return None


def slugify(title):
    s = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return s[:70] or "untitled"


def main():
    ap = argparse.ArgumentParser(description="Generate article drafts.")
    ap.add_argument("--inp", default=str(ROOT / "data" / "new_items.json"))
    ap.add_argument("--out", default=str(ROOT / "data" / "drafts.json"))
    args = ap.parse_args()

    try:
        with open(args.inp, encoding="utf-8") as f:
            items = json.load(f).get("items", [])
    except FileNotFoundError:
        items = []

    ai = ai_configured()
    print(f"[generate] {len(items)} new items; AI provider: "
          f"{'configured' if ai else 'NOT configured — queueing only'}")

    drafts = []
    now = datetime.now(timezone.utc).isoformat()
    for it in items:
        text = f"{it['title']} {it['summary']}"
        if not is_relevant(text):
            continue
        category, region, tags = classify(text)
        sensitive = any(h in text.lower() for h in SENSITIVE_HINTS)
        base = {
            "id": it["dedup_id"][:16],
            "sourceName": it["source_name"],
            "sourceUrl": it["url"],
            "additionalSources": [],
            "category": category, "region": region,
            "publishedAt": it.get("published_at") or now,
            "collectedAt": it.get("collected_at") or now,
            "slug": slugify(it["title"]),
            "image": "", "imageAlt": "", "imageCredit": "",
            "author": "Defense News Desk",
            "featured": False, "breaking": "breaking" in text.lower(),
            "status": "draft",
            "verificationStatus": "unverified",
            "contentType": "news",
            "generatedByAI": False,
            "needsReview": sensitive,
        }
        draft = None
        if ai and not sensitive:
            draft = ai_draft(ai, it, category, region)
            time.sleep(1)
        if draft:
            base.update({
                "title": draft.get("headline", it["title"])[:180],
                "summary": draft.get("summary", it["summary"][:300]),
                "content": draft.get("body", ""),
                "tags": draft.get("tags", tags),
                "generatedByAI": True,
                "verificationStatus": "ai-draft",
            })
        else:
            # No AI or sensitive topic: queue faithfully, never invent.
            base.update({
                "title": it["title"][:180],
                "summary": it["summary"][:300],
                "content": "",
                "tags": tags,
                "verificationStatus": "queued-no-ai" if not ai else "queued-sensitive",
                "needsReview": True,
            })
        drafts.append(base)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"generated_at": now, "count": len(drafts), "drafts": drafts},
                  f, ensure_ascii=False, indent=2)
    print(f"[generate] {len(drafts)} drafts -> {args.out}")


if __name__ == "__main__":
    main()
