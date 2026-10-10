/* Defense News — frontend app: renders homepage from data/articles.json */
(function () {
  'use strict';

  var CATEGORIES = [
    'Breaking News', 'Global Military News', 'United States Defense',
    'China Military', 'Russia Military', 'Pakistan Defense',
    'European Defense', 'Middle East Security', 'Indo-Pacific Security',
    'Military Aviation', 'Naval Warfare and Maritime Security',
    'Ground Forces and Armored Vehicles', 'Missiles and Air Defense',
    'Military Drones and Robotics', 'Defense Technology',
    'Defense Industry and Procurement', 'Military Exercises',
    'Defense Analysis', 'Military History and Explainers'
  ];

  var REGIONS = ['United States', 'China', 'Russia', 'Pakistan', 'Europe',
    'Middle East', 'Indo-Pacific', 'Global'];

  var FALLBACK_IMG = 'assets/img/fallback.svg';
  var PAGE_SIZE = 9;

  var state = { articles: [], query: '', category: '', region: '', shown: PAGE_SIZE };

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function fmtDate(iso) {
    try {
      var d = new Date(iso);
      if (isNaN(d)) return '';
      return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) +
        ' ' + d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false }) + ' UTC';
    } catch (e) { return ''; }
  }

  function readingTime(text) {
    var words = String(text || '').split(/\s+/).length;
    return Math.max(1, Math.round(words / 200));
  }

  function articleUrl(a) { return 'articles/' + a.slug + '.html'; }
  function imgFor(a) { return a.image ? esc(a.image) : FALLBACK_IMG; }

  function metaLine(a) {
    return '<div class="meta">' + esc(fmtDate(a.publishedAt)) +
      ' &middot; ' + esc(a.sourceName || '') +
      ' &middot; ' + readingTime(a.content) + ' min read</div>';
  }

  function cardHtml(a) {
    return '<article class="card">' +
      '<a href="' + articleUrl(a) + '"><img src="' + imgFor(a) + '" alt="' + esc(a.imageAlt || a.title) + '" loading="lazy"></a>' +
      '<div class="card-body"><div class="cat">' + esc(a.category) + '</div>' +
      '<h3><a href="' + articleUrl(a) + '">' + esc(a.title) + '</a></h3>' +
      '<p>' + esc(a.summary) + '</p>' + metaLine(a) + '</div></article>';
  }

  function publishedOnly(list) {
    return list.filter(function (a) { return a.status === 'published'; })
      .sort(function (x, y) { return new Date(y.publishedAt) - new Date(x.publishedAt); });
  }

  function renderTicker(items) {
    var el = document.getElementById('ticker-track');
    if (!el) return;
    var breaking = items.filter(function (a) { return a.breaking; }).slice(0, 8);
    if (!breaking.length) {
      el.innerHTML = '<span>No breaking news at this time.</span>';
      return;
    }
    var html = breaking.map(function (a) {
      return '<a href="' + articleUrl(a) + '">' + esc(a.title) + '</a>';
    }).join('<span>///</span>');
    el.innerHTML = html + '<span>///</span>' + html; // duplicate for seamless loop
  }

  function renderFeatured(items) {
    var wrap = document.getElementById('featured');
    if (!wrap) return;
    var feats = items.filter(function (a) { return a.featured; });
    var pool = feats.length ? feats : items.slice(0, 4);
    var main = pool[0];
    var side = pool.slice(1, 4);
    if (!main) {
      wrap.innerHTML = '<div class="empty">No featured story yet. New articles will appear here automatically.</div>';
      return;
    }
    var html = '<div class="featured-main"><img src="' + imgFor(main) + '" alt="' + esc(main.imageAlt || main.title) + '">' +
      '<div class="featured-text"><span class="kicker">' + esc(main.category) + '</span>' +
      '<h1><a href="' + articleUrl(main) + '">' + esc(main.title) + '</a></h1>' +
      '<div class="meta">' + esc(fmtDate(main.publishedAt)) + ' &middot; ' + esc(main.sourceName || '') + '</div></div></div>';
    html += '<div class="featured-side"><h3>Featured Stories</h3>' + side.map(function (a) {
      return '<div class="side-item"><a href="' + articleUrl(a) + '"><img src="' + imgFor(a) + '" alt="" loading="lazy"></a>' +
        '<div><h4><a href="' + articleUrl(a) + '">' + esc(a.title) + '</a></h4><div class="meta">' + esc(fmtDate(a.publishedAt)) + '</div></div></div>';
    }).join('') + '</div>';
    wrap.innerHTML = html;
  }

  function renderLatest(items) {
    var grid = document.getElementById('latest-grid');
    if (!grid) return;
    var q = state.query.toLowerCase();
    var list = items.filter(function (a) {
      if (state.category && a.category !== state.category) return false;
      if (state.region && a.region !== state.region) return false;
      if (q && (a.title + ' ' + a.summary).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
    var shown = list.slice(0, state.shown);
    grid.innerHTML = shown.length ? shown.map(cardHtml).join('')
      : '<div class="empty">No articles match your search. Try different keywords or filters.</div>';
    var more = document.getElementById('load-more');
    if (more) more.style.display = list.length > state.shown ? '' : 'none';
    var count = document.getElementById('result-count');
    if (count) count.textContent = list.length + ' article' + (list.length === 1 ? '' : 's');
  }

  function renderCategorySections(items) {
    var wrap = document.getElementById('category-sections');
    if (!wrap) return;
    var picks = ['Military Aviation', 'Naval Warfare and Maritime Security',
      'Ground Forces and Armored Vehicles', 'Missiles and Air Defense',
      'Military Drones and Robotics', 'Defense Technology',
      'Defense Industry and Procurement', 'Defense Analysis'];
    var html = '';
    picks.forEach(function (cat) {
      var list = items.filter(function (a) { return a.category === cat; }).slice(0, 3);
      if (!list.length) return; // never show invented/empty category blocks
      html += '<section class="section"><div class="section-head">' + esc(cat) + '</div>' +
        '<div class="cards">' + list.map(cardHtml).join('') + '</div></section>';
    });
    wrap.innerHTML = html;
  }

  function fillFilters() {
    var c = document.getElementById('filter-category');
    var r = document.getElementById('filter-region');
    if (c) CATEGORIES.forEach(function (x) {
      var o = document.createElement('option'); o.value = x; o.textContent = x; c.appendChild(o);
    });
    if (r) REGIONS.forEach(function (x) {
      var o = document.createElement('option'); o.value = x; o.textContent = x; r.appendChild(o);
    });
  }

  function bindEvents(items) {
    var s = document.getElementById('search');
    var c = document.getElementById('filter-category');
    var r = document.getElementById('filter-region');
    var more = document.getElementById('load-more');
    if (s) s.addEventListener('input', function () { state.query = s.value; state.shown = PAGE_SIZE; renderLatest(items); });
    if (c) c.addEventListener('change', function () { state.category = c.value; state.shown = PAGE_SIZE; renderLatest(items); });
    if (r) r.addEventListener('change', function () { state.region = r.value; state.shown = PAGE_SIZE; renderLatest(items); });
    if (more) more.addEventListener('click', function () { state.shown += PAGE_SIZE; renderLatest(items); });
    var nl = document.getElementById('newsletter-form');
    if (nl) nl.addEventListener('submit', function (e) {
      e.preventDefault();
      document.getElementById('newsletter-msg').textContent =
        'Newsletter integration is not configured yet. See README for setup instructions.';
    });
    var t = document.querySelector('.nav-toggle');
    var nav = document.querySelector('.main-nav');
    if (t && nav) {
      t.addEventListener('click', function () { nav.classList.toggle('open'); });
      nav.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () { nav.classList.remove('open'); });
      });
    }
  }

  function boot() {
    fillFilters();
    fetch('data/articles.json', { cache: 'no-store' })
      .then(function (res) {
        if (!res.ok) throw new Error('articles.json not found');
        return res.json();
      })
      .then(function (data) {
        var items = publishedOnly(Array.isArray(data) ? data : []);
        renderTicker(items);
        renderFeatured(items);
        renderLatest(items);
        renderCategorySections(items);
        bindEvents(items);
      })
      .catch(function () {
        ['ticker-track', 'featured', 'latest-grid', 'category-sections'].forEach(function (id) {
          var el = document.getElementById(id);
          if (el) el.innerHTML = '<div class="empty">News feed is temporarily unavailable. Please try again later.</div>';
        });
        bindEvents([]);
      });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
