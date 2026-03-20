#!/usr/bin/env python3
"""
Enrichment script for Zovo tools: letters D through H.
Adds missing layers: About This Tool, QuickFacts, Visible FAQ, Twitter meta, og:site_name fix.
Does NOT modify layers that already exist.
"""

import os
import re
import json
import html as html_mod

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

# Tool-specific fourth QuickFact based on slug keywords
TOOL_FACTS = {
    "calculator": "Instant Results",
    "converter": "Multiple Formats",
    "generator": "One-Click Export",
    "checker": "Real-Time Analysis",
    "validator": "Instant Validation",
    "editor": "Live Preview",
    "builder": "Drag & Drop",
    "maker": "Easy Export",
    "finder": "Smart Search",
    "solver": "Step-by-Step",
    "tracker": "Visual Dashboard",
    "picker": "Visual Selection",
    "machine": "Interactive Controls",
    "reader": "Instant Loading",
    "tester": "Detailed Reports",
    "simulator": "Live Preview",
    "analyzer": "Deep Insights",
    "lookup": "Instant Lookup",
    "planner": "Smart Planning",
    "playground": "Live Code Editor",
}

# Short descriptions for About This Tool, keyed by patterns in slug
TOOL_DESCRIPTIONS = {
    "date-calculator": "calculate date differences, add or subtract time, find business days, and determine ages from birthdates",
    "debt-calculator": "analyze your debts, compare payoff strategies, and create a plan to become debt-free faster",
    "debt-consolidation-calculator": "evaluate whether consolidating your debts into a single loan could save you money on interest and simplify payments",
    "debt-consolidation-loan-calculator": "compare debt consolidation loan options, estimate monthly payments, and calculate total interest savings",
    "debt-payoff-calculator": "create a debt payoff plan using snowball or avalanche methods and see exactly when you will be debt-free",
    "diff-checker": "compare two blocks of text side by side and instantly highlight the differences between them",
    "dilution-calculator": "calculate solution dilutions, determine concentrations, and convert between molarity units for chemistry lab work",
    "discord-timestamp": "generate Discord-formatted timestamps that display in every user's local timezone automatically",
    "discount-calculator": "quickly calculate sale prices, percentage discounts, savings amounts, and compare deals side by side",
    "dns-lookup": "perform DNS lookups for any domain and view A, AAAA, MX, CNAME, TXT, NS, and SOA records",
    "dns-propagation-checker": "check DNS propagation status across global nameservers and verify that your DNS changes have taken effect",
    "docker-compose-generator": "generate Docker Compose YAML configurations with a visual interface instead of writing YAML by hand",
    "dog-age-calculator": "convert your dog's age to human years using breed-specific calculations based on modern veterinary science",
    "domain-availability-checker": "instantly check if a domain name is available for registration across multiple TLD extensions",
    "domain-name-generator": "generate creative, brandable domain name suggestions based on your keywords and preferences",
    "down-payment-calculator": "calculate down payment amounts for home purchases and see how different percentages affect your monthly mortgage",
    "drum-machine": "create beats and drum patterns with an interactive drum machine featuring multiple kits and tempo controls",
    "due-date-calculator": "estimate pregnancy due dates based on last menstrual period, conception date, or ultrasound measurements",
    "dummy-data-generator": "generate realistic test data in JSON, CSV, or SQL format for development and testing purposes",
    "ebook-reader": "read EPUB ebooks directly in your browser with customizable fonts, themes, and reading progress tracking",
    "electric-bill-calculator": "estimate your monthly electric bill based on appliance usage, rates, and consumption patterns",
    "electricity-cost-calculator": "calculate the cost of running electrical devices and appliances based on wattage, usage hours, and local rates",
    "email-signature-generator": "create professional HTML email signatures with your contact details, social links, and branding",
    "email-validator": "validate email addresses for correct syntax, domain existence, and deliverability indicators",
    "emi-calculator": "calculate equated monthly installments for loans, showing payment breakdowns, amortization schedules, and total interest",
    "emoji-picker": "browse, search, and copy emojis organized by category with skin tone variants and recent usage tracking",
    "epoch-time-converter": "convert between Unix epoch timestamps and human-readable dates in multiple formats and timezones",
    "epub-to-pdf-converter": "convert EPUB ebook files to PDF format directly in your browser without uploading to any server",
    "essay-outline-generator": "create structured essay outlines with thesis statements, topic sentences, and supporting point frameworks",
    "exam-grade-calculator": "calculate exam grades, determine scores needed to pass, and convert between grading scales",
    "expense-tracker": "track daily expenses, categorize spending, and visualize your budget with interactive charts and reports",
    "fancy-text-generator": "convert plain text into stylish Unicode fonts and decorative text styles for social media and messaging",
    "favicon-converter": "convert images to ICO favicon format in multiple sizes optimized for browsers and devices",
    "favicon-emoji-generator": "create favicons from emoji characters with customizable backgrounds and sizes",
    "favicon-generator": "generate favicons from text, images, or emoji with all sizes needed for modern browsers and devices",
    "fibonacci-generator": "generate Fibonacci sequences, calculate specific terms, and explore the mathematical properties of the series",
    "file-hash-checker": "verify file integrity by computing and comparing MD5, SHA-1, SHA-256, and SHA-512 checksums",
    "flashcard-maker": "create, study, and organize digital flashcards with spaced repetition for effective learning",
    "flexbox-generator": "visually design CSS flexbox layouts with an interactive builder and copy the generated code",
    "flow-chart-maker": "create professional flowcharts and diagrams with drag-and-drop shapes, connectors, and export options",
    "font-generator": "preview and compare fonts, generate font stacks, and test typography for your web projects",
    "font-identifier": "identify fonts from images by analyzing letterforms and matching them against a database of typefaces",
    "font-pair-generator": "discover harmonious font pairings for your designs with curated combinations and live previews",
    "fraction-calculator": "add, subtract, multiply, and divide fractions with step-by-step solutions and automatic simplification",
    "freelance-rate-calculator": "calculate your ideal freelance hourly rate based on desired salary, expenses, and billable hours",
    "fuel-cost-calculator": "estimate fuel costs for trips based on distance, vehicle fuel economy, and current gas prices",
    "gif-builder": "create animated GIFs from images with customizable frame timing, looping options, and size controls",
    "gif-maker": "create and edit animated GIFs from images or video clips with frame controls and optimization",
    "gitignore-generator": "generate .gitignore files for any programming language, framework, or IDE with curated templates",
    "glassmorphism-generator": "create frosted glass CSS effects with adjustable blur, transparency, and border properties",
    "google-keyword-planner-tool": "research keyword ideas, search volumes, and competition levels to plan your SEO and content strategy",
    "gpa-calculator": "calculate your GPA from course grades and credit hours using standard 4.0, weighted, or custom scales",
    "gpa-calculator-pro": "calculate weighted and unweighted GPA with advanced features like semester tracking and what-if analysis",
    "grade-calculator": "calculate final grades, determine what scores you need on remaining assignments, and track academic progress",
    "gradient-generator": "create beautiful CSS gradients with a visual editor and copy the generated CSS code instantly",
    "gradient-text-generator": "apply gradient colors to text with CSS and copy the code for use in your web projects",
    "graph-calculator": "plot mathematical functions, visualize equations, and explore graphs with an interactive coordinate system",
    "graphing-calculator": "graph mathematical functions, plot data points, and explore equations with a full-featured calculator",
    "graphing-calculator-online": "plot and analyze mathematical functions online with a powerful graphing calculator and equation solver",
    "graphing-scientific-calculator": "combine scientific calculation with graphing capabilities to visualize mathematical functions and equations",
    "habit-tracker": "build and maintain daily habits with streak tracking, visual calendars, and progress statistics",
    "haiku-generator": "generate haiku poems following the traditional 5-7-5 syllable structure with customizable themes",
    "hash-generator": "generate MD5, SHA-1, SHA-256, SHA-384, and SHA-512 hashes from text or files with HMAC support",
    "headline-analyzer": "analyze headlines for emotional impact, word balance, length, and SEO effectiveness with actionable scores",
    "heloc-calculator": "calculate home equity line of credit payments, draw periods, and total interest costs",
    "hex-color-picker": "pick and convert hex colors with a visual color wheel, RGB sliders, and saved color palettes",
    "hex-converter": "convert between hexadecimal, decimal, binary, and octal number systems with step-by-step explanations",
    "home-equity-loan-calculator": "calculate home equity loan payments, compare rates, and determine how much equity you can borrow",
    "hourly-to-salary-converter": "convert hourly wages to annual salary and vice versa, accounting for overtime, benefits, and taxes",
    "hourly-wage-calculator": "calculate hourly earnings from salary or total pay, factor in overtime, and compare compensation packages",
    "html-css-playground": "write and preview HTML, CSS, and JavaScript code in real time with a split-pane live editor",
    "html-email-builder": "build responsive HTML emails with a drag-and-drop editor and export clean, compatible code",
    "html-encoder": "encode and decode HTML entities, escape special characters, and sanitize text for safe web display",
    "html-to-markdown": "convert HTML content to clean Markdown format while preserving structure, links, and formatting",
    "html-to-pdf-converter": "convert HTML pages and content to PDF documents directly in your browser",
    "htpasswd-generator": "generate Apache .htpasswd entries with bcrypt, MD5, or SHA-1 password hashing for HTTP authentication",
    "http-header-analyzer": "inspect HTTP response headers for any URL, check security headers, caching, and server configuration",
    "http-status-checker": "check HTTP status codes for any URL, follow redirects, and diagnose website connectivity issues",
}


def get_tool_description(slug):
    """Get description for a tool, falling back to a generic one."""
    if slug in TOOL_DESCRIPTIONS:
        return TOOL_DESCRIPTIONS[slug]
    tool_name = slug.replace("-", " ")
    return f"use the {tool_name} with an intuitive interface designed for speed and accuracy"


def get_fourth_fact(slug):
    """Get the tool-specific fourth QuickFact."""
    for keyword, fact in TOOL_FACTS.items():
        if keyword in slug:
            return fact
    return "Works Offline"


def get_tool_dirs():
    """Get all tool directories starting with d through h."""
    dirs = []
    for entry in sorted(os.listdir(BASE_DIR)):
        full_path = os.path.join(BASE_DIR, entry)
        if not os.path.isdir(full_path):
            continue
        first_char = entry[0].lower()
        if first_char < 'd' or first_char > 'h':
            continue
        index_path = os.path.join(full_path, "index.html")
        if os.path.isfile(index_path):
            dirs.append((entry, index_path))
    return dirs


def extract_faq_from_jsonld(content):
    """Extract FAQ Q&A pairs from FAQPage JSON-LD."""
    faqs = []
    # Find all JSON-LD blocks
    pattern = r'<script\s+type="application/ld\+json"\s*>(.*?)</script>'
    matches = re.findall(pattern, content, re.DOTALL)
    for match in matches:
        try:
            data = json.loads(match)
            if data.get("@type") == "FAQPage" and "mainEntity" in data:
                for entity in data["mainEntity"]:
                    q = entity.get("name", "")
                    a_obj = entity.get("acceptedAnswer", {})
                    a = a_obj.get("text", "") if isinstance(a_obj, dict) else ""
                    if q and a:
                        faqs.append((q, a))
        except (json.JSONDecodeError, KeyError, TypeError):
            continue
    return faqs


def has_about_section(content):
    return "About This Tool" in content or "about-this-tool" in content


def has_quick_facts(content):
    return "Quick Facts" in content or "quick-facts" in content


def has_visible_faq(content):
    return "Common Questions" in content or "Frequently Asked" in content


def has_twitter_card(content):
    return 'twitter:card' in content


def has_zovo_tools_site_name(content):
    return bool(re.search(r'og:site_name.*?Zovo Tools', content, re.IGNORECASE))


def get_meta_content(content, prop_name, attr="property"):
    """Extract meta tag content value."""
    pattern = rf'<meta\s+{attr}="{prop_name}"\s+content="([^"]*)"'
    match = re.search(pattern, content)
    if not match:
        pattern = rf'<meta\s+content="([^"]*)"\s+{attr}="{prop_name}"'
        match = re.search(pattern, content)
    return match.group(1) if match else ""


def get_title(content):
    """Extract <title> text."""
    match = re.search(r'<title>(.*?)</title>', content)
    return match.group(1) if match else ""


def get_description(content):
    """Extract meta description."""
    match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
    if not match:
        match = re.search(r'<meta\s+content="([^"]*)"\s+name="description"', content)
    return match.group(1) if match else ""


def build_about_section(slug):
    """Build the About This Tool HTML section."""
    tool_name = slug.replace("-", " ").title()
    desc = get_tool_description(slug)
    return f'''
<!-- About This Tool -->
<section id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;font-family:Inter,sans-serif;">
  <h2 style="color:#00ff88;font-size:1.3rem;margin:0 0 1rem 0;">About This Tool</h2>
  <p style="line-height:1.7;margin-bottom:1rem;font-size:0.95rem;color:#c0c0d0;">The {tool_name} lets you {desc}. Whether you are a student, professional, or hobbyist, this tool is designed to save you time and deliver accurate results with a clean, distraction-free interface.</p>
  <p style="line-height:1.7;margin:0;font-size:0.95rem;color:#c0c0d0;">Built by Michael Lip, this tool runs 100% client-side in your browser. No data is ever sent to a server, uploaded, or stored remotely. Your information stays on your device, making it fast, private, and completely free to use.</p>
</section>
'''


def build_quick_facts(slug):
    """Build the Quick Facts HTML section."""
    fourth = get_fourth_fact(slug)
    return f'''
<!-- Quick Facts -->
<section id="quick-facts" style="max-width:800px;margin:2rem auto;padding:0 20px;">
  <h2 style="color:#00ff88;font-size:1.3rem;margin-bottom:1rem;font-family:Inter,sans-serif;">Quick Facts</h2>
  <div style="display:flex;gap:1rem;flex-wrap:wrap;">
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:140px;">
      <div style="font-size:1.4rem;margin-bottom:0.25rem;">&#x1f512;</div>
      <div style="color:#e0e0e8;font-weight:600;font-size:0.9rem;">100% Client-Side</div>
      <div style="color:#8888a0;font-size:0.75rem;">Runs in your browser</div>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:140px;">
      <div style="font-size:1.4rem;margin-bottom:0.25rem;">&#x1f6e1;</div>
      <div style="color:#e0e0e8;font-weight:600;font-size:0.9rem;">No Data Uploaded</div>
      <div style="color:#8888a0;font-size:0.75rem;">Everything stays local</div>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:140px;">
      <div style="font-size:1.4rem;margin-bottom:0.25rem;">&#x2764;</div>
      <div style="color:#e0e0e8;font-weight:600;font-size:0.9rem;">Free Forever</div>
      <div style="color:#8888a0;font-size:0.75rem;">No signup required</div>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:140px;">
      <div style="font-size:1.4rem;margin-bottom:0.25rem;">&#x26a1;</div>
      <div style="color:#e0e0e8;font-weight:600;font-size:0.9rem;">{fourth}</div>
      <div style="color:#8888a0;font-size:0.75rem;">Built for speed</div>
    </div>
  </div>
</section>
'''


def build_visible_faq(faqs):
    """Build a visible accordion-style FAQ section from JSON-LD data."""
    if not faqs:
        return ""
    items_html = ""
    for i, (q, a) in enumerate(faqs):
        safe_q = html_mod.escape(q)
        safe_a = html_mod.escape(a)
        items_html += f'''
  <details style="background:#12121a;border:1px solid #1e1e2a;border-radius:8px;margin-bottom:8px;">
    <summary style="cursor:pointer;padding:1rem 1.25rem;color:#e0e0e8;font-weight:500;font-size:1rem;list-style:none;display:flex;justify-content:space-between;align-items:center;">
      {safe_q}
      <span style="color:#00ff88;font-size:1.2rem;margin-left:1rem;flex-shrink:0;">+</span>
    </summary>
    <div style="padding:0 1.25rem 1rem;color:#b0b0c0;line-height:1.7;font-size:0.95rem;">{safe_a}</div>
  </details>'''

    return f'''
<!-- Visible FAQ Section -->
<section id="visible-faq" style="max-width:800px;margin:48px auto;padding:0 20px;">
  <h2 style="color:#00ff88;font-size:1.5rem;margin-bottom:24px;font-family:Inter,sans-serif;">Frequently Asked Questions</h2>
{items_html}
</section>
'''


def build_twitter_meta(content):
    """Build twitter meta tags from existing OG or title/description."""
    title = get_meta_content(content, "og:title") or get_title(content)
    desc = get_meta_content(content, "og:description") or get_description(content)
    lines = []
    lines.append('<meta name="twitter:card" content="summary_large_image">')
    if title:
        lines.append(f'<meta name="twitter:title" content="{html_mod.escape(title)}">')
    if desc:
        lines.append(f'<meta name="twitter:description" content="{html_mod.escape(desc)}">')
    return "\n".join(lines)


def process_tool(slug, index_path):
    """Process a single tool's index.html. Returns dict of changes made."""
    changes = {
        "about": False,
        "quickfacts": False,
        "faq": False,
        "twitter": False,
        "og_site_name": False,
    }

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    modified = False

    # 1. About This Tool
    if not has_about_section(content):
        about_html = build_about_section(slug)
        # Insert before </body>
        if "</body>" in content:
            content = content.replace("</body>", about_html + "\n</body>", 1)
            changes["about"] = True
            modified = True

    # 2. Quick Facts
    if not has_quick_facts(content):
        qf_html = build_quick_facts(slug)
        # Insert before </body>
        if "</body>" in content:
            content = content.replace("</body>", qf_html + "\n</body>", 1)
            changes["quickfacts"] = True
            modified = True

    # 3. Visible FAQ (only if JSON-LD FAQPage exists but no visible FAQ)
    has_faq_jsonld = '"FAQPage"' in content
    if has_faq_jsonld and not has_visible_faq(content):
        faqs = extract_faq_from_jsonld(content)
        if faqs:
            faq_html = build_visible_faq(faqs)
            if "</body>" in content:
                content = content.replace("</body>", faq_html + "\n</body>", 1)
                changes["faq"] = True
                modified = True

    # 4. Twitter meta tags
    if not has_twitter_card(content):
        twitter_html = build_twitter_meta(content)
        # Insert after last og: meta or before </head>
        # Find good insertion point
        og_matches = list(re.finditer(r'<meta\s+property="og:[^"]*"[^>]*>', content))
        if og_matches:
            last_og = og_matches[-1]
            insert_pos = last_og.end()
            content = content[:insert_pos] + "\n" + twitter_html + "\n" + content[insert_pos:]
        elif "</head>" in content:
            content = content.replace("</head>", twitter_html + "\n</head>", 1)
        changes["twitter"] = True
        modified = True

    # 5. Fix og:site_name "Zovo Tools" -> "Zovo"
    if has_zovo_tools_site_name(content):
        content = re.sub(
            r'(<meta\s+property="og:site_name"\s+content=")Zovo Tools(")',
            r'\1Zovo\2',
            content
        )
        changes["og_site_name"] = True
        modified = True

    if modified:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)

    return changes


def main():
    tools = get_tool_dirs()
    print(f"Found {len(tools)} tools (d-h) to process.\n")

    totals = {"about": 0, "quickfacts": 0, "faq": 0, "twitter": 0, "og_site_name": 0}
    skipped = 0
    processed = 0

    for slug, path in tools:
        changes = process_tool(slug, path)
        any_change = any(changes.values())
        if any_change:
            processed += 1
            parts = []
            if changes["about"]:
                parts.append("About")
                totals["about"] += 1
            if changes["quickfacts"]:
                parts.append("QuickFacts")
                totals["quickfacts"] += 1
            if changes["faq"]:
                parts.append("FAQ")
                totals["faq"] += 1
            if changes["twitter"]:
                parts.append("Twitter")
                totals["twitter"] += 1
            if changes["og_site_name"]:
                parts.append("og:site_name")
                totals["og_site_name"] += 1
            print(f"  [ENRICHED] {slug:45s} +{', '.join(parts)}")
        else:
            skipped += 1
            print(f"  [SKIP]     {slug:45s} (all layers present)")

    print(f"\n{'='*65}")
    print(f"ENRICHMENT COMPLETE")
    print(f"{'='*65}")
    print(f"Total tools scanned:       {len(tools)}")
    print(f"Tools modified:            {processed}")
    print(f"Tools already complete:    {skipped}")
    print(f"")
    print(f"Layers added:")
    print(f"  About This Tool:         {totals['about']}")
    print(f"  Quick Facts:             {totals['quickfacts']}")
    print(f"  Visible FAQ:             {totals['faq']}")
    print(f"  Twitter meta:            {totals['twitter']}")
    print(f"  og:site_name fixed:      {totals['og_site_name']}")
    print(f"  TOTAL enrichments:       {sum(totals.values())}")


if __name__ == "__main__":
    main()
