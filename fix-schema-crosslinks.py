#!/usr/bin/env python3
"""
Fix JSON-LD WebApplication schema and FAQPage schema for all tools.
Task 3 (Related Tools) already complete - all tools have them.
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
    for cat, tools in CATEGORIES.items():
        if tool_name in tools:
            return cat
    return None

def extract_description(content):
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', content)
    if m:
        return m.group(1)
    return ""

def get_tool_title(content):
    m = re.search(r'<title>([^<]+)</title>', content)
    if m:
        return html_module.unescape(m.group(1).split("|")[0].strip())
    return ""

def get_canonical_url(content):
    m = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"', content)
    if m:
        return m.group(1)
    return ""

def tool_display_name(slug):
    words = slug.replace("-", " ").split()
    acronyms = {"json", "xml", "yaml", "csv", "jwt", "uuid", "url", "html", "css", "js", "sql", "bmi", "gpa", "qr", "svg", "ip", "dns", "ssl", "http", "og", "api", "ai", "roi", "px", "rem", "apa"}
    return " ".join(w.upper() if w.lower() in acronyms else w.capitalize() for w in words)


def extract_faq_items(content):
    """Extract FAQ Q&A pairs from the HTML, supporting multiple patterns."""
    faqs = []

    # Pattern 1: <div class="faq-q" ...>Q</div><div class="faq-a"...>A</div>
    p1 = re.findall(
        r'<div\s+class="faq-q"[^>]*>(.*?)</div>\s*<div\s+class="faq-a"[^>]*>(.*?)</div>',
        content, re.DOTALL
    )
    if p1:
        for q, a in p1:
            q_clean = re.sub(r'<[^>]+>', '', q).strip()
            a_clean = re.sub(r'<[^>]+>', '', a).strip()
            if q_clean and a_clean:
                faqs.append((q_clean, a_clean))
        if faqs:
            return faqs

    # Pattern 2: <button class="faq-q">Q</button><div class="faq-a"><p>A</p></div>
    p2 = re.findall(
        r'<button\s+class="faq-q"[^>]*>(.*?)</button>\s*<div\s+class="faq-a"[^>]*>(.*?)</div>',
        content, re.DOTALL
    )
    if p2:
        for q, a in p2:
            q_clean = re.sub(r'<[^>]+>', '', q).strip()
            a_clean = re.sub(r'<[^>]+>', '', a).strip()
            if q_clean and a_clean:
                faqs.append((q_clean, a_clean))
        if faqs:
            return faqs

    # Pattern 3: <div class="faq-question" ...>Q</div><div class="faq-answer">A</div>
    p3 = re.findall(
        r'<div\s+class="faq-question"[^>]*>(.*?)</div>\s*<div\s+class="faq-answer"[^>]*>(.*?)</div>',
        content, re.DOTALL
    )
    if p3:
        for q, a in p3:
            q_clean = re.sub(r'<[^>]+>', '', q).strip()
            a_clean = re.sub(r'<[^>]+>', '', a).strip()
            if q_clean and a_clean:
                faqs.append((q_clean, a_clean))
        if faqs:
            return faqs

    # Pattern 4: <div class="faq-item"><h3>Q</h3><p>A</p></div>
    p4 = re.findall(
        r'<div\s+class="faq-item"[^>]*>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>',
        content, re.DOTALL
    )
    if p4:
        for q, a in p4:
            q_clean = re.sub(r'<[^>]+>', '', q).strip()
            # Remove leading numbering like "1. "
            q_clean = re.sub(r'^\d+\.\s*', '', q_clean)
            a_clean = re.sub(r'<[^>]+>', '', a).strip()
            if q_clean and a_clean:
                faqs.append((q_clean, a_clean))
        if faqs:
            return faqs

    return faqs


def build_webapp_schema(tool_name, content):
    """Build WebApplication JSON-LD schema."""
    title = get_tool_title(content)
    desc = extract_description(content)
    url = get_canonical_url(content)
    if not url:
        url = f"https://tools.zovo.one/{tool_name}"

    cat = get_tool_category(tool_name)
    cat_map = {
        "Developer": "DeveloperApplication",
        "CSS/Design": "DesignApplication",
        "Media": "MultimediaApplication",
        "Calculators": "UtilitiesApplication",
        "SEO/Marketing": "BusinessApplication",
        "Text": "UtilitiesApplication",
        "Generators": "UtilitiesApplication",
        "Productivity": "UtilitiesApplication",
    }
    app_cat = cat_map.get(cat, "WebApplication")

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
    for q, a in faqs[:8]:
        entities.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": entities
    }
    return json.dumps(schema, indent=2, ensure_ascii=False)


def process_tool(tool_name):
    """Process a single tool."""
    index_path = os.path.join(TOOLS_DIR, tool_name, "index.html")
    if not os.path.isfile(index_path):
        return []

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    changes = []

    # TASK 1: Add WebApplication JSON-LD if missing
    if '"WebApplication"' not in content:
        schema_json = build_webapp_schema(tool_name, content)
        schema_block = f'<script type="application/ld+json">\n{schema_json}\n</script>'

        # Find insertion point: after existing ld+json blocks, or before </head>, or before <style>
        if 'application/ld+json' in content:
            # Insert before the first existing ld+json block
            idx = content.find('<script type="application/ld+json">')
            if idx != -1:
                content = content[:idx] + schema_block + '\n' + content[idx:]
            else:
                content = content.replace('</head>', schema_block + '\n</head>', 1)
        elif '</head>' in content:
            content = content.replace('</head>', schema_block + '\n</head>', 1)
        elif '<style>' in content:
            content = content.replace('<style>', schema_block + '\n<style>', 1)
        changes.append("Added WebApplication JSON-LD")

    # TASK 2: Add FAQPage schema if missing but FAQ content exists
    if 'FAQPage' not in content:
        faqs = extract_faq_items(content)
        if faqs:
            faq_json = build_faqpage_schema(faqs)
            faq_block = f'<script type="application/ld+json">\n{faq_json}\n</script>'

            if 'application/ld+json' in content:
                # Find the last ld+json closing </script> before </head>
                head_end = content.find('</head>')
                if head_end == -1:
                    head_end = len(content)
                # Find all ld+json script blocks before </head>
                last_end = -1
                search_pos = 0
                while True:
                    idx = content.find('<script type="application/ld+json">', search_pos, head_end)
                    if idx == -1:
                        break
                    end_idx = content.find('</script>', idx)
                    if end_idx != -1:
                        last_end = end_idx + len('</script>')
                    search_pos = idx + 1

                if last_end != -1:
                    content = content[:last_end] + '\n' + faq_block + content[last_end:]
                else:
                    content = content.replace('</head>', faq_block + '\n</head>', 1)
            elif '</head>' in content:
                content = content.replace('</head>', faq_block + '\n</head>', 1)
            changes.append(f"Added FAQPage schema ({len(faqs)} questions)")

    if content != original:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)
    return changes


if __name__ == "__main__":
    all_tools = sorted([
        d for d in os.listdir(TOOLS_DIR)
        if os.path.isdir(os.path.join(TOOLS_DIR, d))
        and os.path.isfile(os.path.join(TOOLS_DIR, d, "index.html"))
        and d not in (".", "..", ".git", "node_modules")
    ])

    print(f"Found {len(all_tools)} tools with index.html")
    print("=" * 60)

    stats = {"json_ld_added": 0, "faqpage_added": 0, "total_modified": 0}

    for tool in all_tools:
        changes = process_tool(tool)
        if changes:
            stats["total_modified"] += 1
            for c in changes:
                if "WebApplication" in c:
                    stats["json_ld_added"] += 1
                elif "FAQPage" in c:
                    stats["faqpage_added"] += 1
            print(f"  {tool}: {', '.join(changes)}")

    print("=" * 60)
    print(f"SUMMARY:")
    print(f"  WebApplication schemas added: {stats['json_ld_added']}")
    print(f"  FAQPage schemas added: {stats['faqpage_added']}")
    print(f"  Total files modified: {stats['total_modified']}")
