#!/usr/bin/env python3
"""build_site.py — generate static article pages, sitemap.xml, and rss.xml.

Reads data/articles.json (published only) + config/site.json and writes:
  articles/<slug>.html   one static page per article (with JSON-LD NewsArticle)
  sitemap.xml            all real published pages
  rss.xml                latest 30 published articles

Idempotent: regenerating never duplicates or deletes published articles.
Only published articles appear in listings, sitemap, and RSS.

Usage: python scripts/build_site.py
"""
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parent.parent


def esc(s):
    return html.escape(str(s or ""), quote=True)


def load_config():
    with open(ROOT / "config" / "site.json", encoding="utf-8") as f:
        return json.load(f)


def load_articles():
    with open(ROOT / "data" / "articles.json", encoding="utf-8") as f:
        data = json.load(f)
    arts = [a for a in (data if isinstance(data, list) else data.get("articles", []))
            if a.get("status") == "published"]
    arts.sort(key=lambda a: a.get("publishedAt", ""), reverse=True)
    return arts


def reading_time(content):
    return max(1, round(len(str(content or "").split()) / 200))


def related_for(article, all_articles, n=3):
    scored = []
    for other in all_articles:
        if other["slug"] == article["slug"]:
            continue
        score = 0
        if other.get("category") == article.get("category"):
            score += 3
        if other.get("region") == article.get("region"):
            score += 2
        score += len(set(other.get("tags", [])) & set(article.get("tags", [])))
        if score:
            scored.append((score, other))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [o for _, o in scored[:n]]


ARTICLE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {site}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{meta_desc}">
<meta property="og:type" content="article">
<meta property="og:url" content="{url}">
{og_image}
<meta property="article:published_time" content="{published}">
<meta property="article:section" content="{category}">
<link rel="stylesheet" href="../assets/css/style.css">
<script type="application/ld+json">{jsonld}</script>
</head>
<body>
<header class="site-header"><div class="wrap header-top">
<a class="logo" href="../index.html">{site_upper}</a></div>
<nav class="main-nav"><div class="wrap"><ul>
<li><a href="../index.html">Home</a></li>
<li><a href="../index.html#latest">Latest</a></li>
<li><a href="../pages/about.html">About</a></li>
</ul></div></nav></header>
<main class="wrap">
<div class="breadcrumb"><a href="../index.html">Home</a> / {category} / {short_title}</div>
<article>
<div class="article-hero">{hero_img}</div>
<div class="article-body">
<span class="kicker">{category}</span>
<h1>{title}</h1>
<div class="byline"><span>By {author}</span><span>{published_fmt}</span>
<span>{read_time} min read</span><span>Region: {region}</span></div>
<div class="prose">{body}</div>
<div class="source-box"><strong>Source:</strong> {source_name}<br>
<a href="{source_url}" rel="noopener" target="_blank">{source_url}</a></div>
<div class="tags">{tags}</div>
</div>
</article>
<section class="section"><div class="section-head">Related Articles</div>
<div class="cards">{related}</div></section>
</main>
<footer class="site-footer"><div class="wrap footer-bottom">
<span>&copy; {year} {site}. All rights reserved.</span>
<span><a href="../pages/editorial-policy.html">Editorial Policy</a></span>
</div></footer>
</body>
</html>
"""


def md_to_html(md):
    """Minimal markdown -> HTML (paragraphs + ## headings). Escapes raw HTML."""
    out = []
    for block in str(md or "").split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if block.startswith("## "):
            out.append(f"<h2>{esc(block[3:])}</h2>")
        elif block.startswith("# "):
            out.append(f"<h2>{esc(block[2:])}</h2>")
        else:
            out.append(f"<p>{esc(block)}</p>")
    return "\n".join(out) or "<p></p>"


def build_article(article, all_articles, cfg):
    base = cfg["production_url"].rstrip("/")
    url = f"{base}/articles/{article['slug']}.html"
    img = article.get("image") or "assets/img/fallback.svg"
    img_url = img if img.startswith("http") else f"{base}/{img}"
    hero = (f'<img src="../{esc(img)}" alt="{esc(article.get("imageAlt") or article["title"])}">'
            + (f'<div class="meta">Image: {esc(article["imageCredit"])}</div>'
               if article.get("imageCredit") else ""))
    related = "".join(
        f'<article class="card"><div class="card-body"><div class="cat">{esc(r["category"])}</div>'
        f'<h3><a href="{esc(r["slug"])}.html">{esc(r["title"])}</a></h3>'
        f'<p>{esc(r["summary"])}</p></div></article>'
        for r in related_for(article, all_articles))
    if not related:
        related = '<div class="empty">More related coverage coming soon.</div>'
    try:
        pub = datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
        pub_fmt = pub.strftime("%b %d, %Y %H:%M UTC")
    except Exception:
        pub_fmt = article.get("publishedAt", "")
    jsonld = json.dumps({
        "@context": "https://schema.org", "@type": "NewsArticle",
        "headline": article["title"], "description": article["summary"],
        "datePublished": article.get("publishedAt"),
        "dateModified": article.get("updatedAt") or article.get("publishedAt"),
        "author": {"@type": "Organization", "name": article.get("author", cfg["site_name"])},
        "publisher": {"@type": "Organization", "name": cfg["site_name"]},
        "mainEntityOfPage": url, "image": [img_url],
        "articleSection": article.get("category", ""),
    }, ensure_ascii=False)
    return ARTICLE_TEMPLATE.format(
        title=esc(article["title"]), site=esc(cfg["site_name"]),
        site_upper=esc(cfg["site_name"]).upper(),
        meta_desc=esc(article["summary"][:160]), url=url,
        og_image=f'<meta property="og:image" content="{esc(img_url)}">',
        published=esc(article.get("publishedAt", "")),
        category=esc(article.get("category", "")),
        short_title=esc(article["title"][:60]),
        hero_img=hero, author=esc(article.get("author", "")),
        published_fmt=esc(pub_fmt),
        read_time=reading_time(article.get("content")),
        region=esc(article.get("region", "")),
body=md_to_html(article.get("content")),
        source_name=esc(article.get("sourceName", "")),
        source_url=esc(article.get("sourceUrl", "")),
        tags="".join(f'<span class="tag">{esc(t)}</span>' for t in article.get("tags", [])),
        related=related, year=datetime.now(timezone.utc).year,
        jsonld=jsonld.replace("</", "<\\/"),
    )


def build_sitemap(articles, cfg):
    base = cfg["production_url"].rstrip("/")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = [f"  <url><loc>{base}/</loc><lastmod>{now}</lastmod></url>"]
    for p in ["pages/about.html", "pages/contact.html", "pages/editorial-policy.html",
              "pages/corrections.html", "pages/privacy.html", "pages/terms.html",
              "pages/sources.html"]:
        urls.append(f"  <url><loc>{base}/{p}</loc><lastmod>{now}</lastmod></url>")
    for a in articles:
        lm = (a.get("updatedAt") or a.get("publishedAt") or "")[:10] or now
        urls.append(f"  <url><loc>{base}/articles/{a['slug']}.html</loc>"
                    f"<lastmod>{xml_escape(lm)}</lastmod></url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(urls) + "\n</urlset>\n")


def build_rss(articles, cfg):
    base = cfg["production_url"].rstrip("/")
    items = []
    for a in articles[:30]:
        try:
            pub = datetime.fromisoformat(a["publishedAt"].replace("Z", "+00:00"))
            pub_str = pub.strftime("%a, %d %b %Y %H:%M:%S +0000")
        except Exception:
            pub_str = ""
        items.append(
            "  <item>\n"
            f"    <title>{xml_escape(a['title'])}</title>\n"
            f"    <link>{base}/articles/{xml_escape(a['slug'])}.html</link>\n"
            f"    <guid>{base}/articles/{xml_escape(a['slug'])}.html</guid>\n"
            f"    <description>{xml_escape(a.get('summary', ''))}</description>\n"
            f"    <pubDate>{pub_str}</pubDate>\n"
            f"    <category>{xml_escape(a.get('category', ''))}</category>\n"
            "  </item>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n<channel>\n'
            f"  <title>{xml_escape(cfg['site_name'])}</title>\n"
            f"  <link>{base}/</link>\n"
            f"  <description>{xml_escape(cfg['description'])}</description>\n"
            f"  <language>{xml_escape(cfg.get('language', 'en'))}</language>\n"
            + "\n".join(items) + "\n</channel>\n</rss>\n")


def main():
    cfg = load_config()
    articles = load_articles()
    adir = ROOT / "articles"
    adir.mkdir(exist_ok=True)

    for a in articles:
        (adir / f"{a['slug']}.html").write_text(
            build_article(a, articles, cfg), encoding="utf-8")

    (ROOT / "sitemap.xml").write_text(build_sitemap(articles, cfg), encoding="utf-8")
    (ROOT / "rss.xml").write_text(build_rss(articles, cfg), encoding="utf-8")
    print(f"[build] {len(articles)} article pages, sitemap.xml, rss.xml written")


if __name__ == "__main__":
    main()
