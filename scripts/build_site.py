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
    scored.sort(key=lambda x: (x[0], x[1].get("publishedAt", "")), reverse=True)
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
{ga_tag}
</head>
<body>
<header class="site-header"><div class="wrap header-top">
<a class="logo" href="../index.html">{site_upper}</a></div>
<nav class="main-nav"><div class="wrap"><ul>
{nav}
</ul></div></nav></header>
<main class="wrap">
<div class="breadcrumb"><a href="../index.html">Home</a> / {category} / {short_title}</div>
<article>
<div class="article-hero">{hero_img}</div>
<div class="article-body">
<span class="kicker">{category}</span>
<h1>{title}</h1>
<div class="byline"><span>{author}</span><span>{published_fmt}</span>
<span>{read_time} min read</span><span>Region: {region}</span></div>
<div class="prose">{body}</div>
<div class="source-box"><strong>Source:</strong> <a href="{source_url}" rel="noopener" target="_blank">{source_name}</a></div>
<div class="tags">{tags}</div>
</div>
</article>
<section class="section"><div class="section-head">Related Articles</div>
<div class="cards">{related}</div></section>
</main>
<footer class="site-footer"><div class="footer-bottom"><div class="wrap footer-bottom-inner">
<span>&copy; {year} {site}. All rights reserved.</span>
<nav class="footer-legal"><a href="../pages/privacy.html">Privacy</a><a href="../pages/terms.html">Terms</a><a href="../pages/contact.html">Contact</a></nav>
</div></div></footer>
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
    credit = esc(article["imageCredit"]) if article.get("imageCredit") else ""
    if article.get("imageCreditUrl"):
        credit = f'<a href="{esc(article["imageCreditUrl"])}" rel="noopener" target="_blank">{credit}</a>'
    hero = (f'<img src="../{esc(img)}" alt="{esc(article.get("imageAlt") or article["title"])}">'
            + (f'<div class="meta">Image: {credit}</div>' if credit else ""))
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
        ga_tag=ga_tag(cfg),
        nav=nav_links("../"),
    )


def build_sitemap(articles, cfg, cats=None):
    base = cfg["production_url"].rstrip("/")
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    urls = [f"  <url><loc>{base}/</loc><lastmod>{now}</lastmod></url>"]
    for p in ["pages/about.html", "pages/contact.html", "pages/editorial-policy.html",
              "pages/corrections.html", "pages/privacy.html", "pages/terms.html",
              "pages/sources.html"]:
        urls.append(f"  <url><loc>{base}/{p}</loc><lastmod>{now}</lastmod></url>")
    for cat in (cats or {}):
        urls.append(f"  <url><loc>{base}/categories/{cat_slug(cat)}.html</loc><lastmod>{now}</lastmod></url>")
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



def ga_tag(cfg):
    gid = cfg.get("ga4_measurement_id", "")
    if not gid:
        return ""
    return ("""<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=""" + gid + """"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', '""" + gid + """');
</script>""")


def cat_slug(cat):
    import re
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", str(cat or "").lower())).strip("-")


NAV_CATEGORIES = [
    "Military Aviation",
    "Naval Warfare and Maritime Security",
    "Ground Forces and Armored Vehicles",
    "Missiles and Air Defense",
    "Military Drones and Robotics",
]


def nav_links(prefix=""):
    items = [f'<li><a href="{prefix}index.html">Home</a></li>',
             f'<li><a href="{prefix}index.html#latest">Latest</a></li>']
    for c in NAV_CATEGORIES:
        items.append(f'<li><a href="{prefix}categories/{cat_slug(c)}.html">{esc(c.split(" and ")[0].split(" Warfare")[0])}</a></li>')
    items.append(f'<li><a href="{prefix}pages/about.html">About</a></li>')
    return "\n".join(items)


CATEGORY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{category} — {site}</title>
<meta name="description" content="Latest {category} news and analysis — {site}.">
<link rel="canonical" href="{url}">
<link rel="stylesheet" href="../assets/css/style.css">
{ga_tag}
</head>
<body>
<header class="site-header"><div class="wrap header-top">
<div><a class="logo" href="../index.html">{site_upper}</a>
<div class="tagline">Military &middot; Defense &middot; Security</div></div>
<button class="nav-toggle" aria-label="Toggle navigation">MENU</button>
</div>
<nav class="main-nav"><div class="wrap"><ul>
{nav}
</ul></div></nav></header>
<main class="wrap">
<div class="breadcrumb"><a href="../index.html">Home</a> / {category}</div>
<section class="section"><div class="section-head">{category}</div>
<div class="cards">{cards}</div></section>
</main>
<footer class="site-footer"><div class="footer-bottom"><div class="wrap footer-bottom-inner">
<span>&copy; {year} {site}. All rights reserved.</span>
<nav class="footer-legal"><a href="../pages/privacy.html">Privacy</a><a href="../pages/terms.html">Terms</a><a href="../pages/contact.html">Contact</a></nav>
</div></div></footer>
<script>
document.querySelector('.nav-toggle').addEventListener('click',function(){{
document.querySelector('.main-nav').classList.toggle('open');}});
document.querySelectorAll('.main-nav a').forEach(function(a){{
a.addEventListener('click',function(){{document.querySelector('.main-nav').classList.remove('open');}});}});
</script>
</body>
</html>
"""


def build_category_page(category, articles, cfg):
    base = cfg["production_url"].rstrip("/")
    slug = cat_slug(category)
    url = f"{base}/categories/{slug}.html"
    cards = []
    for a in articles:
        img = a.get("image") or "assets/img/fallback.svg"
        img_tag = (f'<a href="../articles/{esc(a["slug"])}.html">'
                   f'<img class="card-img" src="../{esc(img)}" alt="{esc(a["title"])}"></a>')
        cards.append(
            f'<article class="card">{img_tag}<div class="card-body">'
            f'<div class="cat">{esc(a["category"])}</div>'
            f'<h3><a href="../articles/{esc(a["slug"])}.html">{esc(a["title"])}</a></h3>'
            f'<p>{esc(a["summary"])}</p></div></article>')
    return CATEGORY_TEMPLATE.format(
        category=esc(category), site=esc(cfg["site_name"]),
        site_upper=esc(cfg["site_name"]).upper(), url=url,
        nav=nav_links("../"), cards="".join(cards),
        ga_tag=ga_tag(cfg),
        year=datetime.now(timezone.utc).year,
    )


def main():
    cfg = load_config()
    articles = load_articles()
    adir = ROOT / "articles"
    adir.mkdir(exist_ok=True)

    for a in articles:
        (adir / f"{a['slug']}.html").write_text(
            build_article(a, articles, cfg), encoding="utf-8")

    cdir = ROOT / "categories"
    cdir.mkdir(exist_ok=True)
    cats = {}
    for a in articles:
        cats.setdefault(a.get("category", "Uncategorized"), []).append(a)
    for cat, items in cats.items():
        (cdir / f"{cat_slug(cat)}.html").write_text(
            build_category_page(cat, items, cfg), encoding="utf-8")

    (ROOT / "sitemap.xml").write_text(build_sitemap(articles, cfg, cats), encoding="utf-8")
    (ROOT / "rss.xml").write_text(build_rss(articles, cfg), encoding="utf-8")
    print(f"[build] {len(articles)} article pages, {len(cats)} category pages, sitemap.xml, rss.xml written")


if __name__ == "__main__":
    main()
