# Defense News

AI-powered military news website with an automated news publishing pipeline.
Static site (GitHub Pages) + scheduled automation (GitHub Actions). No server required.

## Quick start (local preview)

```bash
cd global-defense-brief
python3 -m http.server 8080
# open http://localhost:8080
```

The homepage renders from `data/articles.json`. With an empty dataset it shows
proper empty states — no invented articles are ever displayed.

## Deploy to GitHub Pages

1. Create a new GitHub repository (e.g. `defense-news-site`) and push this folder:
   ```bash
   git init && git add . && git commit -m "Initial Defense News site"
   git branch -M main && git remote add origin git@github.com:YOUR-USERNAME/defense-news-site.git
   git push -u origin main
   ```
2. In the repo: **Settings → Pages → Source: GitHub Actions**.
3. Update `config/site.json` → `production_url` to your real URL
   (`https://YOUR-USERNAME.github.io/defense-news-site`) and the same URL in
   `robots.txt` and the `<link rel="canonical">` / `og:url` tags in `index.html`.
4. Push again — the `deploy-pages.yml` workflow publishes the site.

## Enable the automated news pipeline

1. In the repo: **Settings → Secrets and variables → Actions** → add:
   - `AI_API_KEY` — your AI provider key (OpenAI-compatible). **Optional.**
   - `AI_API_URL` — override for other providers (optional).
   - `AI_MODEL` — override model name (optional).
2. The `scheduled-news.yml` workflow runs every 3 hours (UTC) automatically.
   Trigger it manually anytime via **Actions → Scheduled defense news collection → Run workflow**.
3. Change the schedule in one place: the `cron:` line in
   `.github/workflows/scheduled-news.yml`. (GitHub may delay scheduled runs.)

### How the pipeline works

```
fetch_news.py        → collect RSS/Atom from config/news_sources.json
normalize_sources.py → clean HTML, canonicalize URLs, ISO dates
deduplicate_news.py  → persistent seen-store in data/processed_items.json
generate_articles.py → classify + (if AI_API_KEY set) draft articles;
                       otherwise queue source summaries — never invents content
validate_articles.py → fact-check gates → approved vs review queue
publish_site.py      → orchestrates all steps, merges per publication policy,
                       runs scripts/build_site.py
scripts/build_site.py→ generates articles/*.html, sitemap.xml, rss.xml
```

### Publication policy

`config/pipeline.json` → `publication_policy.mode`:

- `"review"` (default): all AI-generated drafts are held in
  `data/review_queue.json` for human approval. Approve by moving an entry to
  `data/articles.json` with `"status": "published"`, then run
  `python scripts/build_site.py` and commit.
- `"auto"`: validated articles publish automatically.

Sensitive topics (casualties, disputed battlefield claims, unverified breaking
allegations) are **always** held for review, regardless of mode.

### Without an AI key

The pipeline still runs: it collects, deduplicates, classifies, and queues
source items with their summaries in the review queue. Nothing is fabricated
to fill the gap.

## Manual pipeline run

```bash
pip install -r requirements.txt
python automation/publish_site.py --max 10
```

## Project structure

```
index.html                 homepage shell (renders data/articles.json)
assets/css/style.css       editorial design (navy/charcoal/white/red)
assets/js/app.js           rendering, search, filters, ticker, load-more
assets/img/fallback.svg    neutral fallback image
articles/                  generated article pages (do not hand-edit)
pages/                     About, Contact, Editorial/Corrections/Privacy/Terms, Sources
data/articles.json         published articles (empty until pipeline runs)
data/processed_items.json  persistent dedup store (committed)
config/news_sources.json   RSS sources (verified working, 2026-10-09)
config/pipeline.json       AI config, limits, publication policy
automation/                6 pipeline scripts
scripts/build_site.py      static generator (articles, sitemap, RSS)
.github/workflows/         scheduled-news.yml, deploy-pages.yml
```

## Costs

- GitHub Pages hosting: free. GitHub Actions: within free tier for this workload.
- AI article generation: requires a paid API key (or free-tier key from a
  compatible provider). RSS collection, filtering, and queuing work without it.

## Google Search Console

1. Go to https://search.google.com/search-console → Add property →
   URL prefix: your production URL.
2. Verify via the HTML file method (upload the file to the repo root, push,
   deploy, then verify).
3. Submit `sitemap.xml`. No automatic Google News approval is promised.

## Limitations

- Scheduled GitHub workflows can be delayed or skipped by GitHub; the site
  always serves the last successful build.
- Article images: the pipeline stores source-provided image URLs when feeds
  include them; otherwise the neutral fallback is used. Never hotlink images
  without usage rights — review `imageCredit` before publishing.
- Newsletter form is a placeholder until a provider is configured.
