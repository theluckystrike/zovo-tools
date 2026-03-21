#!/usr/bin/env python3
"""
Rebuild the zovo-tools index.html to include ALL tool directories.
"""

import os
import re
from html import escape

TOOLS_DIR = "/Users/mike/zovo-workspaces/zovo-tools"
OUTPUT_FILE = os.path.join(TOOLS_DIR, "index.html")

CATEGORY_KEYWORDS = {
    "Developer": [
        "json", "xml", "css-grid", "css-flex", "css-clip", "css-filter",
        "js-", "javascript", "html-", "api-", "regex", "code-", "sql",
        "git-", "docker", "curl", "yaml", "base64", "jwt", "uuid",
        "url-encoder", "url-decode", "bcrypt", "hash-gen", "cors",
        "csp-header", "sitemap", "robots", "schema-", "dns-",
        "ip-lookup", "http-", "ascii-", "chmod", "cron-",
        "diff-check", "favicon", "webhook", "minif", "formatter",
        "beautif", "svg-", "dom-", "markdown-", "csv-to-json",
        "json-to", "xml-to", "json-path", "graphql", "npm",
        "typescript", "python-", "upc-code", "barcode-gen",
        "open-graph", "htaccess", "toml", "responsive-test",
        "user-agent", "syntax", "html-entity", "html-table",
        "html-form", "html-email", "css-animation", "css-transform",
        "text-diff", "code-", "pixel-ruler", "screen-resolution",
        "url-shortener", "url-encoder-decoder", "web-scraper",
        "qr-code", "binary-translator", "hex-to", "hex-color",
        "color-code-converter",
    ],
    "Finance": [
        "loan", "mortgage", "tax-", "interest-", "savings", "investment",
        "budget", "debt", "payroll", "salary", "401k", "529-",
        "apy", "cagr", "amortization", "bond-", "break-even",
        "payment-", "refinance", "equity", "emi-", "roi-",
        "compound-interest", "simple-interest", "inflation",
        "retirement", "annuity", "depreciation", "margin-calc",
        "markup-calc", "discount-calc", "tip-calc", "tip-split",
        "percentage", "profit", "currency", "exchange-rate",
        "paycheck", "take-home", "hourly-to", "overtime",
        "net-worth", "income-tax", "expense", "cost-of-living",
        "rent-", "lease-", "car-", "auto-loan", "fuel-",
        "gas-mileage", "mpg", "down-payment", "closing-cost",
        "home-afford", "stamp-duty", "capital-gains",
        "estate-tax", "inheritance", "unit-price", "price-",
        "wage-", "pay-raise", "timecard", "time-to-decimal",
        "time-card", "finance", "financial", "billing",
        "adp-pay", "pay-stub", "stock-", "dividend",
        "credit-card", "apr-", "sales-tax", "vat-",
        "gst-", "tax-bracket", "tax-refund",
        "age-calculator", "date-calculator", "days-between",
        "voltage-divider", "wire-gauge", "ohms-law", "resistor",
        "concrete-calc", "fence-calc", "gravel-calc",
        "square-footage", "mulch", "soil-calc",
        "btu-calc", "board-foot", "deck-", "drywall",
        "paint-calc", "roofing", "tile-calc", "wallpaper",
        "pool-volume", "volume-calc", "area-calc",
        "usd-to", "eur-to", "gbp-to", "inr-to", "btc-to",
    ],
    "Design": [
        "color-p", "color-wheel", "color-mixer", "color-blind",
        "gradient", "shadow-gen", "box-shadow", "border-radius",
        "grid-gen", "flexbox-gen", "animation-gen", "font-pair",
        "svg-edit", "image-resize", "photo-", "pixel-art",
        "palette", "contrast-check", "glassmorphism", "clip-path",
        "mockup", "wireframe", "whiteboard", "webp-conv", "image-crop",
        "image-filter", "collage", "watermark", "video-to-gif", "ico-conv",
        "ai-logo", "logo-gen", "icon-gen", "pattern-gen",
        "neomorphism", "neumorphism", "blob-gen", "wave-gen",
        "mesh-gradient", "duotone", "noise-gen", "texture",
        "color-convert", "pantone", "tailwind-color", "material-color",
        "figma", "sketch", "css-gradient",
    ],
    "Writing": [
        "grammar", "readability", "word-counter", "paraphrase",
        "headline", "citation", "apa-", "bibliography", "essay",
        "resume", "cover-letter", "text-case", "text-repeat",
        "text-summar", "text-to-speech", "text-to-hand", "text-gen",
        "word-cloud", "acrostic", "ai-detector", "ai-humanizer",
        "article-", "blog-", "poem", "story-gen", "haiku",
        "rhyme", "synonym", "antonym", "thesaurus", "proofread",
        "plagiarism", "rewrite", "tone-", "sentiment",
        "passive-voice", "letter-gen", "email-writer",
        "bio-gen", "slogan", "character-count", "name-generator",
    ],
    "Education": [
        "gpa", "grade-calc", "typing-speed", "typing-test",
        "chemistry", "periodic-table", "fibonacci", "binary-search",
        "graphing", "equation", "fraction", "algebra",
        "geometry", "statistics-", "probability", "matrix-calc",
        "quadratic", "scientific-calc", "math-", "flash-card",
        "flashcard", "study-", "quiz", "trivia",
        "word-problem", "word-scramble", "anagram",
        "number-base", "roman-numeral", "multiplication",
        "division-calc", "prime-number", "standard-deviation",
        "mean-median", "significant-fig", "sig-fig",
    ],
    "Media": [
        "audio-", "video-comp", "video-trim", "video-to-mp",
        "gif-maker", "mp3-", "mp4-", "pdf-", "epub",
        "image-compressor", "speech-to-text", "screen-recorder",
        "ebook", "podcast", "youtube", "spotify", "music-",
        "sound-", "tuner", "metronome", "bpm-", "drum-",
        "ringtone", "wav-to", "flac-", "ogg-", "subtitle",
        "srt-", "vtt-", "karaoke", "slideshow", "presentation",
    ],
    "Productivity": [
        "pomodoro", "timer", "calendar-", "countdown",
        "password-gen", "password-str", "email-temp",
        "business-card", "invoice-gen", "note-",
        "todo", "task-", "kanban", "project-",
        "meeting-", "agenda", "planner", "schedule",
        "habit", "goal-", "checklist", "template-",
        "timezone", "utc-to", "world-clock", "stopwatch",
        "alarm-", "reminder", "bookmark", "clipboard",
        "vcard", "ics-calendar", "unit-converter",
        "decision", "random-picker", "wheel-spin",
        "coin-flip", "dice-roll",
    ],
    "Business": [
        "invoice", "business-name", "seo-", "meta-tag-anal",
        "keyword-", "domain-", "ai-seo", "email-signature",
        "company-", "startup-", "brand-", "trademark",
    ],
    "Health": [
        "bmi", "calorie", "sleep-", "blood-", "body-fat",
        "pregnancy", "due-date", "bmr", "macro-calc",
        "period-", "alcohol", "heart-rate", "tdee",
        "water-intake", "fitness", "workout", "exercise",
        "protein-", "keto", "fasting", "meditation",
        "vision-", "hearing-", "running-pace", "pace-calc",
        "vo2-", "pushup",
    ],
    "Utility": [],
}

CATEGORY_COLORS = {
    "Developer": "#6C5CE7",
    "Finance": "#00d68f",
    "Design": "#fd79a8",
    "Writing": "#fdcb6e",
    "Education": "#74b9ff",
    "Media": "#e17055",
    "Productivity": "#00cec9",
    "Business": "#a29bfe",
    "Health": "#55efc4",
    "Utility": "#81ecec",
}

POPULAR_SLUGS = [
    "json-formatter", "password-generator", "base64-encoder", "regex-tester",
    "qr-code-generator", "mortgage-calculator", "color-palette-generator", "uuid-generator",
]

EXCLUDE_DIRS = {
    "articles", ".git", ".github", "node_modules", "__pycache__",
    "scripts", "assets", "images", "css", "js", ".claude"
}


def extract_title_and_desc(filepath):
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(20000)
    except Exception:
        return None, None

    title_match = re.search(r"<title[^>]*>(.*?)</title>", content, re.IGNORECASE | re.DOTALL)
    title = title_match.group(1).strip() if title_match else None

    desc_match = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        content, re.IGNORECASE | re.DOTALL
    )
    if not desc_match:
        desc_match = re.search(
            r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']',
            content, re.IGNORECASE | re.DOTALL
        )
    desc = desc_match.group(1).strip() if desc_match else None

    return title, desc


def categorize_tool(slug, title, desc):
    text = (slug + " " + (title or "").lower() + " " + (desc or "").lower())

    priority_order = [
        "Health", "Education", "Media", "Business",
        "Design", "Writing", "Productivity",
        "Developer", "Finance",
    ]

    for cat in priority_order:
        keywords = CATEGORY_KEYWORDS.get(cat, [])
        for kw in keywords:
            if kw is None:
                continue
            if kw in slug or kw in text:
                return cat

    if "calculator" in slug or "calculator" in text:
        return "Finance"

    if "converter" in slug:
        return "Utility"

    return "Utility"


def truncate_desc(desc, max_len=130):
    if not desc:
        return ""
    if len(desc) <= max_len:
        return desc
    return desc[:max_len].rstrip()


def scan_tools():
    tools = []
    for entry in sorted(os.listdir(TOOLS_DIR)):
        dirpath = os.path.join(TOOLS_DIR, entry)
        if not os.path.isdir(dirpath):
            continue
        if entry in EXCLUDE_DIRS or entry.startswith("."):
            continue

        index_file = os.path.join(dirpath, "index.html")
        if not os.path.isfile(index_file):
            continue

        title, desc = extract_title_and_desc(index_file)
        if not title:
            title = entry.replace("-", " ").title()

        title = re.sub(r"\s*[\|·\-]\s*(Zovo|zovo\.one)\s*$", "", title)
        title = title.strip()

        cat = categorize_tool(entry, title, desc)
        mtime = os.path.getmtime(index_file)

        tools.append({
            "slug": entry,
            "title": title,
            "desc": desc or "",
            "category": cat,
            "mtime": mtime,
        })

    return tools


def make_card_html(tool):
    slug = tool["slug"]
    title = escape(tool["title"])
    desc = escape(truncate_desc(tool["desc"]))
    cat = tool["category"]
    color = CATEGORY_COLORS.get(cat, "#81ecec")

    display_title = title
    if len(display_title) > 60:
        display_title = display_title[:57] + "..."

    return (
        '<a href="/free-tools/' + slug + '/" class="card" data-cat="' + cat + '">'
        '<div class="category" style="color:' + color + '">' + cat + '</div>'
        '<h2>' + display_title + '</h2>'
        '<p>' + desc + '</p>'
        '<span class="tag">Free</span></a>'
    )


def build_html(tools):
    total = len(tools)

    cat_counts = {}
    for t in tools:
        cat_counts[t["category"]] = cat_counts.get(t["category"], 0) + 1

    tools_sorted = sorted(tools, key=lambda t: t["slug"])

    popular = [t for t in tools_sorted if t["slug"] in POPULAR_SLUGS]
    popular_order = {s: i for i, s in enumerate(POPULAR_SLUGS)}
    popular.sort(key=lambda t: popular_order.get(t["slug"], 999))

    tools_by_mtime = sorted(tools, key=lambda t: t["mtime"], reverse=True)
    new_tools = tools_by_mtime[:8]

    num_categories = len([c for c in cat_counts if cat_counts[c] > 0])

    popular_cards = "\n".join(make_card_html(t) for t in popular)
    new_cards = "\n".join(make_card_html(t) for t in new_tools)
    all_cards = "\n".join(make_card_html(t) for t in tools_sorted)

    cat_order = ["Developer", "Finance", "Design", "Writing", "Education", "Media", "Productivity", "Business", "Health", "Utility"]
    filter_buttons = '<button class="filter-btn active" data-filter="all">All (' + str(total) + ')</button>\n'
    for cat in cat_order:
        count = cat_counts.get(cat, 0)
        if count > 0:
            filter_buttons += '<button class="filter-btn" data-filter="' + cat + '">' + cat + ' (' + str(count) + ')</button>\n'

    html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>''' + str(total) + '''+ Free Online Tools - Calculators, Generators & Converters | Zovo</title>
<meta name="description" content="''' + str(total) + '''+ free online tools by Zovo. Calculators, generators, converters and developer tools. No sign-up, no ads, no tracking.">
<meta name="author" content="Michael Lip">
<link rel="canonical" href="https://zovo.one/free-tools/">
<link rel="icon" href="https://zovo.one/favicon.ico">
<meta property="og:title" content="''' + str(total) + '''+ Free Online Tools | Zovo">
<meta property="og:description" content="Free online tools. Calculators, generators, and productivity tools. No sign-up, no ads.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://zovo.one/free-tools/">
<meta property="og:site_name" content="Zovo">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="''' + str(total) + '''+ Free Online Tools | Zovo">
<meta name="twitter:description" content="Free calculators, generators, converters and developer tools. No sign-up required.">
<meta name="human-authored" content="true">
<meta name="date" content="2026-03-21">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Zovo",
  "url": "https://zovo.one/free-tools/",
  "description": "''' + str(total) + '''+ free online tools. Calculators, generators, converters and developer tools.",
  "author": { "@type": "Person", "name": "Michael Lip", "url": "https://zovo.one" },
  "potentialAction": { "@type": "SearchAction", "target": "https://zovo.one/free-tools/?q={search_term_string}", "query-input": "required name=search_term_string" }
}
</script>

<style>

*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',system-ui,sans-serif;background:#0a0a0f;color:#e0e0e0;line-height:1.7}
a{color:#6C5CE7;text-decoration:none}

/* Nav */
.nav{position:sticky;top:0;z-index:1000;background:rgba(10,10,15,0.95);backdrop-filter:blur(12px);border-bottom:1px solid #1a1a2a;padding:0 1.5rem}
.nav-inner{max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;height:56px}
.nav-logo{display:flex;align-items:center;gap:2px;text-decoration:none}
.nav-logo .brand{font-size:1.3rem;font-weight:700;color:#00ff88;letter-spacing:-0.5px}
.nav-logo .dot{color:#00ff88;font-size:1.3rem}
.nav-links{display:flex;align-items:center;gap:1.8rem}
.nav-links a{color:#8888a0;font-size:0.85rem;text-decoration:none;transition:color 0.2s}
.nav-links a:hover{color:#fff}
.nav-links a.active{color:#00ff88}

/* Hero */
.hero{text-align:center;padding:4rem 1rem 2.5rem;background:radial-gradient(ellipse at 50% 0%,rgba(108,92,231,0.08) 0%,transparent 60%)}
.hero-count{font-size:4rem;font-weight:700;color:#fff;line-height:1;margin-bottom:0.3rem}
.hero-count span{background:linear-gradient(135deg,#00ff88,#00ccff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-sub{font-size:1.15rem;color:#8888a0;margin-bottom:0.8rem}
.hero-tagline{font-size:0.9rem;color:#555570;margin-bottom:2rem}
.hero-stats{display:flex;justify-content:center;gap:2.5rem;margin-top:1.5rem;flex-wrap:wrap}
.hero-stat{text-align:center}
.hero-stat .num{font-size:1.4rem;font-weight:600;color:#fff}
.hero-stat .label{font-size:0.75rem;color:#666680;margin-top:2px}

/* Search */
.search-wrap{max-width:560px;margin:0 auto 2rem;position:relative}
.search{display:block;width:100%;padding:14px 20px 14px 44px;background:#12121e;border:1px solid #2a2a4a;border-radius:12px;color:#e0e0e0;font-size:1rem;font-family:inherit;outline:none;transition:border-color 0.2s,box-shadow 0.2s}
.search:focus{border-color:#6C5CE7;box-shadow:0 0 0 3px rgba(108,92,231,0.15)}
.search::placeholder{color:#555}
.search-icon{position:absolute;left:16px;top:50%;transform:translateY(-50%);color:#555;font-size:1rem}

/* Container */
.container{max-width:1200px;margin:0 auto;padding:0 1rem}

/* Section headers */
.section-header{display:flex;align-items:center;gap:0.8rem;margin:2.5rem 0 1.2rem}
.section-header h2{font-size:1.2rem;font-weight:600;color:#fff}
.section-header .badge{font-size:0.65rem;padding:3px 8px;border-radius:10px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px}
.badge-popular{background:rgba(0,255,136,0.12);color:#00ff88}
.badge-new{background:rgba(0,204,255,0.12);color:#00ccff}
.badge-trending{background:rgba(253,203,110,0.12);color:#fdcb6e}

/* Filters */
.filters{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:2rem;padding:0 1rem}
.filter-btn{padding:7px 14px;background:#12121e;border:1px solid #2a2a4a;border-radius:20px;color:#888;font-size:0.78rem;cursor:pointer;transition:all 0.2s;font-family:inherit}
.filter-btn:hover,.filter-btn.active{background:rgba(108,92,231,0.1);border-color:#6C5CE7;color:#6C5CE7}

/* Grid */
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px;margin-bottom:1rem}
.grid-featured{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:14px;margin-bottom:2rem}

/* Cards */
.card{background:#12121e;border:1px solid #1e1e32;border-radius:12px;padding:20px;transition:all 0.25s;text-decoration:none;position:relative;overflow:hidden;display:block}
.card:hover{border-color:#6C5CE7;transform:translateY(-3px);box-shadow:0 8px 24px rgba(108,92,231,0.1)}
.card h2{font-size:0.95rem;font-weight:500;color:#fff;margin-bottom:6px;display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.card p{color:#777790;font-size:0.82rem;margin-bottom:10px;line-height:1.5}
.category{font-size:0.68rem;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;margin-bottom:6px}
.tag{display:inline-block;background:rgba(0,255,136,0.08);color:#00ff88;font-size:0.68rem;padding:2px 8px;border-radius:4px;font-weight:500}

/* Email capture */
.email-section{background:#12121e;border:1px solid #1e1e32;border-radius:16px;padding:2.5rem;text-align:center;margin:3rem 0}
.email-section h3{font-size:1.2rem;color:#fff;margin-bottom:0.5rem}
.email-section p{color:#777790;font-size:0.9rem;margin-bottom:1.2rem}
.email-form{display:flex;gap:8px;max-width:440px;margin:0 auto}
.email-form input{flex:1;padding:12px 16px;background:#0a0a0f;border:1px solid #2a2a4a;border-radius:8px;color:#e0e0e0;font-size:0.9rem;font-family:inherit;outline:none}
.email-form input:focus{border-color:#00ff88}
.email-form button{padding:12px 24px;background:linear-gradient(135deg,#00ff88,#00cc6a);color:#0a0a0f;border:none;border-radius:8px;font-weight:600;font-size:0.85rem;cursor:pointer;transition:transform 0.2s;font-family:inherit;white-space:nowrap}
.email-form button:hover{transform:scale(1.02)}

/* Footer */
.site-footer{border-top:1px solid #1a1a2a;padding:3rem 1rem;margin-top:3rem}
.footer-inner{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:2rem}
.footer-brand .brand-name{font-size:1.2rem;font-weight:700;color:#00ff88;margin-bottom:0.5rem}
.footer-brand p{color:#555570;font-size:0.82rem;line-height:1.6}
.footer-col h4{color:#fff;font-size:0.8rem;font-weight:600;margin-bottom:0.8rem;text-transform:uppercase;letter-spacing:0.5px}
.footer-col a{display:block;color:#666680;font-size:0.82rem;margin-bottom:0.5rem;text-decoration:none;transition:color 0.2s}
.footer-col a:hover{color:#00ff88}
.footer-bottom{max-width:1200px;margin:2rem auto 0;padding-top:1.5rem;border-top:1px solid #1a1a2a;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem}
.footer-bottom p{color:#444460;font-size:0.75rem}
.footer-bottom a{color:#555570;text-decoration:none}
.footer-bottom a:hover{color:#00ff88}

.hidden{display:none}

@media(max-width:768px){
  .hero-count{font-size:2.8rem}
  .hero-stats{gap:1.5rem}
  .nav-links a.mobile-hide{display:none}
  .footer-inner{grid-template-columns:1fr 1fr}
  .email-form{flex-direction:column}
  .grid,.grid-featured{grid-template-columns:1fr 1fr}
}
@media(max-width:480px){
  .footer-inner{grid-template-columns:1fr}
  .grid,.grid-featured{grid-template-columns:1fr}
  .hero-count{font-size:2.2rem}
}

</style>
</head>
<body>

<nav class="nav">
<div class="nav-inner">
<a href="/free-tools/" class="nav-logo"><span class="brand">Zovo</span><span class="dot">.</span></a>
<div class="nav-links">
<a href="/free-tools/" class="active">Tools</a>
<a href="/free-tools/articles/">Articles</a>
<a href="https://zovo.one">zovo.one</a>
</div>
</div>
</nav>

<div class="hero">
<div class="hero-count"><span>''' + str(total) + '''+</span></div>
<div class="hero-sub">Free Online Tools</div>
<div class="hero-tagline">No sign-up · No ads · No tracking · 100% client-side</div>
<div class="search-wrap">
<span class="search-icon">&#x1F50D;</span>
<input type="text" class="search" id="search" placeholder="Search ''' + str(total) + '''+ tools..." autocomplete="off">
</div>
<div class="hero-stats">
<div class="hero-stat"><div class="num">''' + str(total) + '''+</div><div class="label">Tools</div></div>
<div class="hero-stat"><div class="num">''' + str(num_categories) + '''</div><div class="label">Categories</div></div>
<div class="hero-stat"><div class="num">0</div><div class="label">Tracking Scripts</div></div>
<div class="hero-stat"><div class="num">$0</div><div class="label">Cost</div></div>
</div>
</div>

<div class="container">

<div class="section-header" id="popular-section">
<h2>Most Popular</h2>
<span class="badge badge-popular">Top Picks</span>
</div>
<div class="grid-featured" id="popular-grid">
''' + popular_cards + '''
</div>

<div class="section-header" id="new-section">
<h2>New This Week</h2>
<span class="badge badge-new">Just Added</span>
</div>
<div class="grid-featured" id="new-grid">
''' + new_cards + '''
</div>

<div class="section-header" id="all-section">
<h2>All Tools</h2>
<span class="badge" style="background:rgba(255,255,255,0.06);color:#888">''' + str(total) + ''' tools</span>
</div>

<div class="filters">
''' + filter_buttons + '''
</div>

<div class="grid" id="tools-grid">
''' + all_cards + '''
</div>

</div>

<footer style="text-align:center;padding:3rem 1rem;color:#555;font-size:0.8rem;border-top:1px solid #1a1a2a;margin-top:3rem">
<p>Built by Michael Lip · <a href="https://zovo.one" style="color:#6C5CE7">zovo.one</a></p>
<p style="margin-top:0.3rem">All tools run 100% client-side. No data is sent to any server.</p>
</footer>

<script>
// Search — filters all sections
const search = document.getElementById('search');
const allGrid = document.getElementById('tools-grid');
const allCards = allGrid.querySelectorAll('.card');
const popularGrid = document.getElementById('popular-grid');
const newGrid = document.getElementById('new-grid');
const popularSection = document.getElementById('popular-section');
const newSection = document.getElementById('new-section');

search.addEventListener('input', function() {
  const q = this.value.toLowerCase().trim();
  if (q.length > 0) {
    popularSection.style.display = 'none';
    popularGrid.style.display = 'none';
    newSection.style.display = 'none';
    newGrid.style.display = 'none';
  } else {
    popularSection.style.display = '';
    popularGrid.style.display = '';
    newSection.style.display = '';
    newGrid.style.display = '';
  }
  allCards.forEach(card => {
    const text = card.textContent.toLowerCase();
    card.style.display = text.includes(q) ? '' : 'none';
  });
});

// Category filters
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    const filter = this.dataset.filter;
    allCards.forEach(card => {
      if (filter === 'all' || card.dataset.cat === filter) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  });
});
</script>
</body>
</html>'''

    return html


def main():
    print("Scanning tool directories...")
    tools = scan_tools()
    print("Found " + str(len(tools)) + " tools")

    cat_counts = {}
    for t in tools:
        cat_counts[t["category"]] = cat_counts.get(t["category"], 0) + 1
    for cat in sorted(cat_counts.keys()):
        print("  " + cat + ": " + str(cat_counts[cat]))

    print("\nBuilding index.html...")
    html = build_html(tools)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print("Written " + OUTPUT_FILE)
    print("Total tools: " + str(len(tools)))


if __name__ == "__main__":
    main()
