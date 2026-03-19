#!/usr/bin/env python3
"""
Fix JSON-LD schema, FAQPage schema, and add cross-linking sections to all tools.
"""
import os
import re
import json
import html as html_module

TOOLS_DIR = os.path.expanduser("~/zovo-workspaces/zovo-tools")

# ============================
# CATEGORY DEFINITIONS
# ============================
CATEGORIES = {
    "Developer": [
        "json-formatter", "json-viewer", "json-path-finder", "json-yaml-converter",
        "csv-to-json", "xml-formatter", "yaml-validator", "regex-tester",
        "regex-visualizer", "sql-formatter", "jwt-decoder", "base64-encoder",
        "url-encoder", "html-encoder", "markdown-to-html", "markdown-editor",
        "diff-checker", "cron-generator", "htpasswd-generator", "bcrypt-generator",
        "uuid-generator", "hash-generator", "binary-text-converter", "slug-generator",
        "chmod-calculator", "css-minifier", "js-minifier", "timestamp-converter",
        "api-tester", "http-status-checker", "dns-lookup", "ssl-checker",
        "image-to-base64", "csv-to-json-converter", "base64-encoder-decoder",
        "url-encoder-decoder", "text-diff-checker", "cron-expression-generator"
    ],
    "CSS/Design": [
        "color-converter", "color-palette-generator", "hex-color-picker",
        "css-gradient-generator", "gradient-generator", "box-shadow-generator",
        "border-radius-generator", "flexbox-generator", "css-grid-generator",
        "css-animation-generator", "px-to-rem", "favicon-generator",
        "favicon-converter", "svg-editor", "image-compressor", "placeholder-image",
        "pixel-art-editor", "whiteboard", "screenshot-mockup", "image-resizer",
        "svg-to-png-converter", "pixel-to-rem-converter", "color-contrast-checker",
        "logo-maker", "wireframe-tool", "screenshot-to-code"
    ],
    "SEO/Marketing": [
        "meta-tag-generator", "og-preview", "schema-generator", "sitemap-generator",
        "robots-txt-generator", "headline-analyzer", "readability-checker",
        "ai-detector", "slug-generator", "email-signature-generator",
        "privacy-policy-generator"
    ],
    "Calculators": [
        "bmi-calculator", "age-calculator", "percentage-calculator", "gpa-calculator",
        "grade-calculator", "loan-calculator", "mortgage-calculator", "tip-calculator",
        "discount-calculator", "compound-interest-calculator", "calorie-calculator",
        "subnet-calculator", "aspect-ratio-calculator", "tax-calculator",
        "salary-calculator", "paycheck-calculator", "roi-calculator",
        "profit-margin-calculator", "investment-calculator", "retirement-calculator",
        "savings-calculator", "debt-payoff-calculator", "amortization-calculator",
        "blood-alcohol-calculator", "electricity-cost-calculator",
        "time-calculator", "date-calculator", "scientific-calculator",
        "graphing-calculator", "math-equation-solver", "mathematics-solver"
    ],
    "Text": [
        "text-case-converter", "character-counter", "word-counter", "text-generator",
        "paraphrase-tool", "morse-code-translator", "text-to-speech",
        "ascii-art-generator", "lorem-ipsum-generator", "case-converter",
        "plagiarism-checker", "typing-test", "typing-speed-test",
        "essay-outline-generator", "apa-citation-generator", "apa-source-generator"
    ],
    "Generators": [
        "password-generator", "qr-code-generator", "qr-reader", "meme-generator",
        "invoice-generator", "resume-builder", "baby-name-generator",
        "table-generator", "calendar-generator", "number-generator",
        "random-number-generator", "roman-numeral-converter", "number-base-converter",
        "binary-converter", "currency-converter", "unit-converter",
        "timezone-converter", "instagram-font-generator"
    ],
    "Media": [
        "ai-video-generator", "youtube-converter", "youtube-thumbnail",
        "emoji-picker", "ip-lookup"
    ],
    "Productivity": [
        "pomodoro-timer", "countdown-timer", "stopwatch", "kanban-board",
        "discord-timestamp"
    ]
}

def get_tool_category(tool_name):
    """Find which category a tool belongs to."""
    for cat, tools in CATEGORIES.items():
        if tool_name in tools:
            return cat
    return None

def get_related_tools(tool_name, count=5):
    """Get related tools from the same category."""
    cat = get_tool_category(tool_name)
    if not cat:
        # Try to find by keyword matching
        for c, tools in CATEGORIES.items():
            for t in tools:
                if any(kw in tool_name for kw in t.split("-")) and t != tool_name:
                    cat = c
                    break
            if cat:
                break
    if not cat:
        # Fallback: pick from Developer tools
        cat = "Developer"

    same_cat = [t for t in CATEGORIES[cat] if t != tool_name]
    # Verify they exist
    same_cat = [t for t in same_cat if os.path.isdir(os.path.join(TOOLS_DIR, t))]
    return same_cat[:count]

def tool_display_name(slug):
    """Convert tool slug to display name."""
    words = slug.replace("-", " ").split()
    # Special casing for acronyms
    acronyms = {"json", "xml", "yaml", "csv", "jwt", "uuid", "url", "html", "css", "js", "sql", "bmi", "gpa", "qr", "svg", "ip", "dns", "ssl", "http", "og", "api", "ai", "roi", "px", "rem", "apa"}
    result = []
    for w in words:
        if w.lower() in acronyms:
            result.append(w.upper())
        else:
            result.append(w.capitalize())
    return " ".join(result)

def extract_title(content):
    """Extract title from HTML."""
    m = re.search(r'<title>([^<]+)</title>', content)
    if m:
        title = m.group(1).split("|")[0].split("-")[0].strip()
        return html_module.unescape(title)
    return ""

def extract_description(content):
    """Extract meta description."""
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
    if m:
        return m.group(1)
    return ""

def get_tool_title(content):
    """Get the full tool title."""
    m = re.search(r'<title>([^<]+)</title>', content)
    if m:
        return html_module.unescape(m.group(1).split("|")[0].strip())
    return ""

def get_canonical_url(content):
    """Get canonical URL."""
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', content)
    if m:
        return m.group(1)
    return ""

def extract_faq_items(content):
    """Extract FAQ Q&A pairs from the HTML."""
    faqs = []
    # Pattern: <div class="faq-q" ...>Question</div> followed by <div class="faq-a">Answer</div>
    pattern = r'<div\s+class="faq-q"[^>]*>(.*?)</div>\s*<div\s+class="faq-a"[^>]*>(.*?)</div>'
    matches = re.findall(pattern, content, re.DOTALL)
    for q, a in matches:
        q_clean = re.sub(r'<[^>]+>', '', q).strip()
        a_clean = re.sub(r'<[^>]+>', '', a).strip()
        if q_clean and a_clean:
            faqs.append((q_clean, a_clean))
    return faqs

def build_webapp_schema(tool_name, content):
    """Build WebApplication JSON-LD schema."""
    title = get_tool_title(content)
    desc = extract_description(content)
    url = get_canonical_url(content)

    if not url:
        url = f"https://tools.zovo.one/{tool_name}"

    # Determine application category
    cat = get_tool_category(tool_name)
    if cat == "Developer":
        app_cat = "DeveloperApplication"
    elif cat in ("CSS/Design", "Media"):
        app_cat = "DesignApplication"
    elif cat in ("Calculators",):
        app_cat = "UtilitiesApplication"
    elif cat == "SEO/Marketing":
        app_cat = "BusinessApplication"
    else:
        app_cat = "WebApplication"

    schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title or tool_display_name(tool_name),
        "description": desc or f"Free online {tool_display_name(tool_name).lower()}.",
        "url": url,
        "applicationCategory": app_cat,
        "operatingSystem": "Any",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        "author": {"@type": "Person", "name": "Michael Lip"},
        "isAccessibleForFree": True,
        "browserRequirements": "Requires a modern web browser"
    }

    return json.dumps(schema, indent=2)

def build_faqpage_schema(faqs):
    """Build FAQPage JSON-LD schema."""
    entities = []
    for q, a in faqs[:8]:  # Limit to 8 FAQs for schema
        # Escape for JSON
        q_esc = q.replace('"', '\\"').replace('\n', ' ').strip()
        a_esc = a.replace('"', '\\"').replace('\n', ' ').strip()
        entities.append({
            "@type": "Question",
            "name": q_esc,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a_esc
            }
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }

    return json.dumps(schema, indent=2, ensure_ascii=False)

def build_related_tools_section(tool_name):
    """Build a styled Related Tools section."""
    related = get_related_tools(tool_name, 5)
    if not related:
        return ""

    links = ""
    for t in related:
        display = tool_display_name(t)
        links += f'<a href="/{t}/" style="display:inline-block;padding:6px 14px;background:#1a1a2e;border:1px solid #2a2a4a;border-radius:6px;color:#e0e0e0;text-decoration:none;font-size:0.85rem;transition:border-color 0.2s;">{display}</a>\n'

    section = f'''<div style="max-width:800px;margin:2rem auto;padding:1.5rem;">
<div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.1em;color:#6C5CE7;margin-bottom:0.75rem;font-weight:500;">Related Tools</div>
<div style="display:flex;flex-wrap:wrap;gap:8px;">
{links.strip()}
</div>
</div>'''

    return section

def has_related_tools(content):
    """Check if the tool already has a Related Tools section."""
    return bool(re.search(r'[Rr]elated\s*[Tt]ools', content))

def process_tool(tool_name):
    """Process a single tool: add JSON-LD, FAQPage, and related tools."""
    index_path = os.path.join(TOOLS_DIR, tool_name, "index.html")
    if not os.path.isfile(index_path):
        return None

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = []

    # TASK 1: Add WebApplication JSON-LD if missing
    if 'application/ld+json' not in content:
        schema_json = build_webapp_schema(tool_name, content)
        schema_block = f'''<script type="application/ld+json">
{schema_json}
</script>'''
        # Insert before </head> or before first <style>
        if '</head>' in content:
            content = content.replace('</head>', schema_block + '\n</head>', 1)
        elif '<style>' in content:
            content = content.replace('<style>', schema_block + '\n<style>', 1)
        changes.append("Added WebApplication JSON-LD")

    # TASK 2: Add FAQPage schema if missing but FAQ content exists
    if 'FAQPage' not in content:
        faqs = extract_faq_items(content)
        if faqs:
            faq_json = build_faqpage_schema(faqs)
            faq_block = f'''<script type="application/ld+json">
{faq_json}
</script>'''
            # Insert after existing ld+json block, or before </head>
            if 'application/ld+json' in content:
                # Find the last </script> for ld+json and insert after it
                last_ldjson = content.rfind('</script>', 0, content.find('</head>'))
                if last_ldjson != -1:
                    insert_pos = last_ldjson + len('</script>')
                    content = content[:insert_pos] + '\n' + faq_block + content[insert_pos:]
                else:
                    content = content.replace('</head>', faq_block + '\n</head>', 1)
            elif '</head>' in content:
                content = content.replace('</head>', faq_block + '\n</head>', 1)
            changes.append(f"Added FAQPage schema ({len(faqs)} questions)")

    # TASK 3: Add Related Tools section if missing
    if not has_related_tools(content):
        related_section = build_related_tools_section(tool_name)
        if related_section:
            # Insert before </body>
            if '</body>' in content:
                content = content.replace('</body>', related_section + '\n</body>', 1)
            changes.append("Added Related Tools section")

    if content != original:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)
        return changes
    return []

# ============================
# MAIN EXECUTION
# ============================
if __name__ == "__main__":
    # Get all tool directories
    all_tools = sorted([
        d for d in os.listdir(TOOLS_DIR)
        if os.path.isdir(os.path.join(TOOLS_DIR, d))
        and os.path.isfile(os.path.join(TOOLS_DIR, d, "index.html"))
        and d not in (".", "..", ".git", "node_modules")
    ])

    print(f"Found {len(all_tools)} tools with index.html")
    print("=" * 60)

    stats = {
        "json_ld_added": 0,
        "faqpage_added": 0,
        "related_added": 0,
        "total_modified": 0
    }

    for tool in all_tools:
        changes = process_tool(tool)
        if changes:
            stats["total_modified"] += 1
            for c in changes:
                if "WebApplication" in c:
                    stats["json_ld_added"] += 1
                elif "FAQPage" in c:
                    stats["faqpage_added"] += 1
                elif "Related Tools" in c:
                    stats["related_added"] += 1
            print(f"  {tool}: {', '.join(changes)}")
        else:
            print(f"  {tool}: no changes needed")

    print("=" * 60)
    print(f"SUMMARY:")
    print(f"  JSON-LD schemas added: {stats['json_ld_added']}")
    print(f"  FAQPage schemas added: {stats['faqpage_added']}")
    print(f"  Related Tools sections added: {stats['related_added']}")
    print(f"  Total files modified: {stats['total_modified']}")
