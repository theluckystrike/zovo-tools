#!/usr/bin/env python3
"""
Batch enrichment script for Zovo Tools (letters O through S).
Adds missing enrichment layers to each tool's index.html:
1. About This Tool section
2. Quick Facts cards
3. Visible FAQ section (from JSON-LD)
4. Twitter meta tags
5. Fix og:site_name from "Zovo Tools" to "Zovo"
"""

import os
import re
import json
import html

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

# Skip non-tool directories
SKIP_DIRS = {"output", "seo-gists-v3", "articles"}

# Tool-specific fourth fact for Quick Facts
TOOL_FACTS = {
    "calculator": "Instant Results",
    "converter": "Multiple Formats",
    "generator": "One-Click Export",
    "editor": "Real-Time Preview",
    "checker": "Instant Analysis",
    "solver": "Step-by-Step",
    "finder": "Smart Search",
    "builder": "Drag & Drop",
    "maker": "Easy Export",
    "tester": "Live Testing",
    "validator": "Instant Validation",
    "designer": "Visual Editor",
    "tracker": "Track Progress",
    "visualizer": "Interactive Display",
    "simulator": "Real-Time Simulation",
    "formatter": "One-Click Format",
    "viewer": "Instant Preview",
    "recorder": "Browser-Based",
    "timer": "No Install Needed",
    "guide": "Expert Reference",
    "chart": "Visual Reference",
    "table": "Interactive Table",
    "keyboard": "Play Online",
    "playground": "Live Sandbox",
    "picker": "Visual Selection",
}


def get_tool_specific_fact(slug):
    """Get a relevant fourth fact based on the tool type."""
    for keyword, fact in TOOL_FACTS.items():
        if keyword in slug:
            return fact
    return "Works Offline"


def get_tool_description(slug, tool_name):
    """Generate a brief description of what the tool does."""
    descriptions = {
        "og-preview": "preview how your links appear on social media platforms like Facebook, Twitter, LinkedIn, and Discord",
        "online-calculator": "perform quick mathematical calculations including basic arithmetic, percentages, and scientific functions",
        "online-translator": "translate text between multiple languages quickly and privately",
        "ovulation-calculator": "estimate your most fertile days and ovulation window based on your menstrual cycle",
        "pace-calculator": "calculate your running or walking pace, speed, distance, and finish time",
        "paint-calculator": "estimate how much paint you need for your project based on room dimensions",
        "paper-size-guide": "look up and compare standard paper sizes including A-series, letter, legal, and more",
        "paraphrase-tool": "rewrite and rephrase text while preserving the original meaning",
        "password-generator": "create strong, secure, and random passwords with customizable length and character options",
        "pay-stub-calculator": "calculate your pay stub details including gross pay, deductions, and net pay",
        "pay-stub-creator": "create professional pay stubs with detailed earnings and deduction breakdowns",
        "pay-stub-generator": "generate detailed pay stubs with tax calculations and deduction summaries",
        "paycheck-calculator": "calculate your take-home pay after federal and state tax deductions",
        "paycheck-estimator": "estimate your net paycheck amount after all taxes and withholdings",
        "paycheck-tax-calculator": "calculate how much tax is withheld from your paycheck",
        "payroll-calculator": "calculate payroll including gross pay, taxes, deductions, and net pay for employees",
        "payroll-tax-calculator": "calculate employer and employee payroll tax obligations",
        "paystub-generator": "generate professional pay stubs with accurate tax and deduction calculations",
        "pdf-compressor": "reduce PDF file sizes while maintaining quality, entirely in your browser",
        "pdf-editor": "edit PDF documents including adding text, annotations, and highlights",
        "pdf-merger": "combine multiple PDF files into a single document",
        "pdf-to-word-converter": "convert PDF documents to editable Word format",
        "percentage-calculator": "calculate percentages, percentage changes, and percentage differences",
        "percentage-change-calculator": "calculate the percentage increase or decrease between two values",
        "percentage-finder": "find percentages of numbers and solve percentage problems",
        "periodic-table": "explore the periodic table of elements with detailed information about each element",
        "photo-editor": "edit photos with filters, cropping, resizing, and adjustments",
        "photo-filter": "apply professional photo filters and effects to your images",
        "physics-formula-calculator": "solve physics problems using common formulas for mechanics, electricity, and more",
        "piano-keyboard": "play a virtual piano keyboard with realistic sounds",
        "ping-test": "test network connectivity and measure response times to any host",
        "pixel-art-editor": "create pixel art with a grid-based drawing tool and export your creations",
        "pixel-to-rem-converter": "convert pixel values to rem units and vice versa for responsive web design",
        "placeholder-image": "generate placeholder images with custom dimensions, colors, and text",
        "plagiarism-checker": "check text for potential plagiarism and duplicate content",
        "poem-generator": "generate creative poems in various styles and formats",
        "pomodoro-timer": "boost productivity with the Pomodoro technique timer for focused work sessions",
        "pregnancy-weight-tracker": "track and monitor healthy weight gain during pregnancy",
        "privacy-policy-generator": "generate a customized privacy policy for your website or app",
        "profit-margin-calculator": "calculate gross profit margin, net profit margin, and markup percentages",
        "property-tax-calculator": "estimate annual property tax based on home value and local tax rates",
        "protein-calculator": "calculate your daily protein intake needs based on your goals and activity level",
        "px-to-rem": "convert CSS pixel values to rem units for responsive and accessible designs",
        "qr-code-designer": "design custom QR codes with colors, logos, and styling options",
        "qr-code-generator": "generate QR codes for URLs, text, WiFi, contacts, and more",
        "qr-code-maker": "create QR codes quickly for any type of content",
        "qr-reader": "scan and decode QR codes from images or your device camera",
        "qr-wifi-generator": "generate QR codes that let people connect to your WiFi network instantly",
        "quadratic-solver": "solve quadratic equations and see step-by-step solutions with graphing",
        "random-number-generator": "generate random numbers within any range with various distribution options",
        "random-picker": "randomly pick items from a list for decisions, raffles, or selections",
        "readability-checker": "analyze text readability using Flesch-Kincaid, Gunning Fog, and other scoring methods",
        "readme-generator": "create professional README files for your GitHub repositories",
        "receipt-generator": "create professional receipts for transactions and purchases",
        "recipe-scaler": "scale recipe ingredients up or down for any number of servings",
        "recycling-guide": "look up recycling guidelines and learn how to properly recycle common materials",
        "regex-generator": "build and generate regular expressions with a visual interface",
        "regex-tester": "test and debug regular expressions with real-time matching and syntax highlighting",
        "regex-visualizer": "visualize regular expressions as railroad diagrams to understand pattern matching",
        "rental-yield-calculator": "calculate rental property yield, cash flow, and return on investment",
        "resistor-color-code-calculator": "decode resistor color bands to find resistance values and tolerances",
        "resume-builder": "build a professional resume with customizable templates and sections",
        "resume-generator": "generate a polished resume from your information with professional formatting",
        "retirement-calculator": "plan your retirement by estimating savings growth, income needs, and withdrawal rates",
        "rhyme-finder": "find rhyming words for poetry, songwriting, and creative writing",
        "ring-size-chart": "find your ring size using international size charts and conversion tables",
        "robots-txt-generator": "generate robots.txt files to control how search engines crawl your website",
        "roi-calculator": "calculate return on investment to evaluate the profitability of investments",
        "roman-numeral-converter": "convert between Roman numerals and standard numbers",
        "running-pace-calculator": "calculate your running pace, split times, and race finish estimates",
        "salary-calculator": "calculate your salary conversions between hourly, weekly, monthly, and annual pay",
        "salary-to-hourly-calculator": "convert annual salary to hourly wage and vice versa",
        "sales-tax-calculator": "calculate sales tax amounts and total prices for purchases",
        "savings-calculator": "calculate how your savings will grow over time with compound interest",
        "savings-goal-calculator": "plan how to reach your savings goals with monthly contribution estimates",
        "schema-generator": "generate structured data markup (JSON-LD) for better search engine visibility",
        "scientific-calculator": "perform advanced mathematical calculations including trigonometry, logarithms, and more",
        "scientific-calculator-online": "perform scientific calculations with a full-featured online calculator",
        "scientific-notation-converter": "convert numbers between standard and scientific notation",
        "screen-recorder": "record your screen directly in the browser without any software installation",
        "screenshot-mockup": "place screenshots into device mockup frames for presentations and portfolios",
        "screenshot-to-code": "convert website screenshots into HTML and CSS code",
        "shoe-size-converter": "convert shoe sizes between US, UK, EU, and other international sizing systems",
        "sip-calculator": "calculate returns on Systematic Investment Plan contributions over time",
        "sitemap-generator": "generate XML sitemaps to help search engines index your website",
        "sitemap-validator": "validate your XML sitemap for errors and compliance with search engine standards",
        "sleep-calculator": "calculate optimal bedtimes and wake times based on sleep cycles",
        "sleep-quality-calculator": "assess and track your sleep quality with science-based metrics",
        "slug-generator": "generate URL-friendly slugs from any text for SEO-optimized URLs",
        "sorting-visualizer": "visualize sorting algorithms like bubble sort, quicksort, and merge sort in action",
        "speech-to-text": "convert spoken words to text using your browser's speech recognition",
        "speed-converter": "convert between speed units like mph, km/h, knots, and m/s",
        "speed-test": "test your internet connection speed including download, upload, and latency",
        "sql-formatter": "format and beautify SQL queries for better readability",
        "sql-playground": "write and execute SQL queries in a browser-based sandbox environment",
        "ssh-key-generator": "generate SSH key pairs for secure server authentication",
        "ssl-checker": "check SSL/TLS certificate status, expiration, and security details for any domain",
        "statistics-calculator": "calculate statistical measures including mean, median, standard deviation, and more",
        "statistics-probability-calculator": "calculate probability distributions, combinations, and permutations",
        "stock-profit-calculator": "calculate stock trading profits, losses, and return percentages",
        "stock-return-calculator": "calculate investment returns including dividends and capital gains",
        "stopwatch": "use a precise online stopwatch with lap timing and split tracking",
        "story-title-generator": "generate creative and engaging titles for stories, articles, and blog posts",
        "student-loan-calculator": "calculate student loan payments, interest, and repayment timelines",
        "student-loan-repayment-calculator": "plan your student loan repayment strategy with payment schedules",
        "subnet-calculator": "calculate subnet masks, network addresses, and IP address ranges",
        "sudoku-solver": "solve Sudoku puzzles instantly with step-by-step solution explanations",
        "svg-animator": "create SVG animations with keyframes and timing controls",
        "svg-editor": "edit and create SVG vector graphics with a visual editor",
        "svg-optimizer": "optimize and minify SVG files to reduce file size",
        "svg-path-editor": "edit SVG path data visually with control points and curves",
        "svg-to-png-converter": "convert SVG vector files to PNG raster images at any resolution",
    }
    if slug in descriptions:
        return descriptions[slug]
    # Fallback: derive from tool name
    return f"use the {tool_name} for quick, accurate results right in your browser"


def get_og_title(content):
    """Extract og:title from HTML content."""
    m = re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', content)
    if m:
        return m.group(1)
    # Fallback to <title>
    m = re.search(r'<title>([^<]*)</title>', content)
    if m:
        return m.group(1)
    return ""


def get_og_description(content):
    """Extract og:description from HTML content."""
    m = re.search(r'<meta\s+property="og:description"\s+content="([^"]*)"', content)
    if m:
        return m.group(1)
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
    if m:
        return m.group(1)
    return ""


def extract_faq_from_jsonld(content):
    """Extract FAQ Q&A pairs from FAQPage JSON-LD."""
    faqs = []
    # Find all JSON-LD blocks
    jsonld_blocks = re.findall(
        r'<script\s+type="application/ld\+json">\s*(\{[\s\S]*?\})\s*</script>',
        content
    )
    for block in jsonld_blocks:
        try:
            data = json.loads(block)
            if data.get("@type") == "FAQPage" and "mainEntity" in data:
                for item in data["mainEntity"]:
                    q = item.get("name", "")
                    a_obj = item.get("acceptedAnswer", {})
                    a = a_obj.get("text", "") if isinstance(a_obj, dict) else ""
                    if q and a:
                        faqs.append((q, a))
        except (json.JSONDecodeError, KeyError):
            continue
    return faqs


def build_about_section(slug, tool_name):
    """Build the About This Tool HTML section."""
    desc = get_tool_description(slug, tool_name)
    return f'''
<!-- About This Tool -->
<section id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;font-family:'Inter',sans-serif;">
  <h2 style="color:#fff;font-size:1.4rem;margin:0 0 1rem 0;">About This Tool</h2>
  <p style="color:#c0c0cc;line-height:1.7;margin:0 0 1rem 0;">The {tool_name} lets you {desc}. Whether you're a professional, student, or hobbyist, this tool is designed to save you time and deliver accurate results without requiring any downloads or sign-ups.</p>
  <p style="color:#c0c0cc;line-height:1.7;margin:0;">Built by Michael Lip, this tool runs 100% client-side in your browser. No data is ever uploaded or sent to any server, ensuring complete privacy and security for all your inputs.</p>
</section>
'''


def build_quick_facts(slug, tool_name):
    """Build the Quick Facts HTML section."""
    fourth_fact = get_tool_specific_fact(slug)
    return f'''
<!-- Quick Facts -->
<section style="max-width:800px;margin:2rem auto;font-family:'Inter',sans-serif;">
  <p style="color:#00ff88;font-size:0.8rem;font-weight:600;margin:0 0 10px;">Quick Facts</p>
  <div style="display:flex;gap:1rem;flex-wrap:wrap;">
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:140px;">
      <div style="color:#00ff88;font-size:1.2rem;font-weight:700;">100%</div>
      <div style="color:#b0b0c0;font-size:0.8rem;">Client-Side</div>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:140px;">
      <div style="color:#00ff88;font-size:1.2rem;font-weight:700;">Zero</div>
      <div style="color:#b0b0c0;font-size:0.8rem;">Data Uploaded</div>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:140px;">
      <div style="color:#00ff88;font-size:1.2rem;font-weight:700;">Free</div>
      <div style="color:#b0b0c0;font-size:0.8rem;">Forever</div>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:140px;">
      <div style="color:#00ff88;font-size:1.2rem;font-weight:700;">{fourth_fact.split()[0] if " " in fourth_fact else fourth_fact}</div>
      <div style="color:#b0b0c0;font-size:0.8rem;">{" ".join(fourth_fact.split()[1:]) if " " in fourth_fact else ""}</div>
    </div>
  </div>
</section>
'''


def build_visible_faq(faqs):
    """Build visible FAQ accordion section from extracted Q&A pairs."""
    if not faqs:
        return ""
    items_html = ""
    for q, a in faqs:
        escaped_q = html.escape(q)
        escaped_a = html.escape(a)
        items_html += f'''
    <div style="background:#12121a;border:1px solid #1e1e2a;border-radius:12px;padding:24px;margin-bottom:16px;">
      <h3 style="color:#e0e0e8;font-size:1.1rem;margin:0 0 8px 0;">Q: {escaped_q}</h3>
      <p style="color:#b0b0c0;margin:0;line-height:1.6;">{escaped_a}</p>
    </div>'''

    return f'''
<!-- Frequently Asked Questions -->
<section style="max-width:800px;margin:3rem auto;font-family:'Inter',sans-serif;">
  <h2 style="color:#00ff88;font-size:1.5rem;margin-bottom:24px;" id="frequently-asked-questions">Frequently Asked Questions</h2>
  {items_html}
</section>
'''


def build_twitter_meta(content, slug, tool_name):
    """Build Twitter meta tags from existing OG data."""
    og_title = get_og_title(content) or f"{tool_name} | Zovo"
    og_desc = get_og_description(content) or f"Free {tool_name} - runs entirely in your browser."
    return f'''<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(og_title)}">
<meta name="twitter:description" content="{html.escape(og_desc)}">
'''


def process_tool(tool_dir):
    """Process a single tool's index.html and add missing enrichment layers."""
    index_path = os.path.join(tool_dir, "index.html")
    if not os.path.isfile(index_path):
        return None

    slug = os.path.basename(tool_dir)
    tool_name = slug.replace("-", " ").title()

    with open(index_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    original_content = content
    changes = []

    # 1. Fix og:site_name "Zovo Tools" -> "Zovo"
    if re.search(r'<meta\s+property="og:site_name"\s+content="Zovo Tools"', content):
        content = re.sub(
            r'(<meta\s+property="og:site_name"\s+content=")Zovo Tools(")',
            r'\1Zovo\2',
            content
        )
        changes.append("fix og:site_name")

    # 2. Missing Twitter meta
    if not re.search(r'twitter:card', content, re.IGNORECASE):
        twitter_tags = build_twitter_meta(content, slug, tool_name)
        # Insert after last og: meta tag or after <head>
        og_match = list(re.finditer(r'<meta\s+property="og:[^"]*"\s+content="[^"]*"\s*/?>', content))
        if og_match:
            insert_pos = og_match[-1].end()
            content = content[:insert_pos] + "\n" + twitter_tags + content[insert_pos:]
        else:
            # Insert after <head> tag
            head_match = re.search(r'<head[^>]*>', content)
            if head_match:
                insert_pos = head_match.end()
                content = content[:insert_pos] + "\n" + twitter_tags + content[insert_pos:]
        changes.append("add twitter meta")

    # 3. Missing visible FAQ (has FAQPage JSON-LD but no visible FAQ section)
    has_faq_jsonld = '"FAQPage"' in content or "'FAQPage'" in content
    has_visible_faq = bool(re.search(r'Common Questions|Frequently Asked|frequently-asked-questions', content, re.IGNORECASE))

    if has_faq_jsonld and not has_visible_faq:
        faqs = extract_faq_from_jsonld(content)
        if faqs:
            faq_html = build_visible_faq(faqs)
            # Insert before </body>
            body_close = content.rfind("</body>")
            if body_close != -1:
                content = content[:body_close] + faq_html + "\n" + content[body_close:]
                changes.append(f"add visible FAQ ({len(faqs)} items)")

    # 4. Missing Quick Facts
    if not re.search(r'Quick Facts|quick-facts|quick_facts', content, re.IGNORECASE):
        quick_facts_html = build_quick_facts(slug, tool_name)
        body_close = content.rfind("</body>")
        if body_close != -1:
            content = content[:body_close] + quick_facts_html + "\n" + content[body_close:]
            changes.append("add Quick Facts")

    # 5. Missing About This Tool
    if not re.search(r'About This Tool|about-this-tool|about_this_tool', content, re.IGNORECASE):
        about_html = build_about_section(slug, tool_name)
        body_close = content.rfind("</body>")
        if body_close != -1:
            content = content[:body_close] + about_html + "\n" + content[body_close:]
            changes.append("add About This Tool")

    if content != original_content:
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)
        return changes
    return []


def main():
    # Collect all tool directories starting with o through s
    tool_dirs = []
    for entry in sorted(os.listdir(BASE_DIR)):
        if entry in SKIP_DIRS:
            continue
        first_char = entry[0].lower()
        if first_char < 'o' or first_char > 's':
            continue
        full_path = os.path.join(BASE_DIR, entry)
        if os.path.isdir(full_path) and os.path.isfile(os.path.join(full_path, "index.html")):
            tool_dirs.append(full_path)

    print(f"Found {len(tool_dirs)} tools (o-s) to process\n")

    stats = {
        "processed": 0,
        "modified": 0,
        "skipped_no_changes": 0,
        "about_added": 0,
        "quick_facts_added": 0,
        "faq_added": 0,
        "twitter_added": 0,
        "og_fixed": 0,
        "errors": 0,
    }

    for tool_dir in tool_dirs:
        slug = os.path.basename(tool_dir)
        try:
            changes = process_tool(tool_dir)
            stats["processed"] += 1

            if changes is None:
                print(f"  SKIP  {slug} (no index.html)")
                continue

            if changes:
                stats["modified"] += 1
                for c in changes:
                    if "About" in c:
                        stats["about_added"] += 1
                    if "Quick Facts" in c:
                        stats["quick_facts_added"] += 1
                    if "FAQ" in c:
                        stats["faq_added"] += 1
                    if "twitter" in c:
                        stats["twitter_added"] += 1
                    if "og:site_name" in c:
                        stats["og_fixed"] += 1
                print(f"  OK    {slug}: {', '.join(changes)}")
            else:
                stats["skipped_no_changes"] += 1
                print(f"  ---   {slug}: already enriched")
        except Exception as e:
            stats["errors"] += 1
            print(f"  ERR   {slug}: {e}")

    print(f"\n{'='*60}")
    print(f"ENRICHMENT COMPLETE")
    print(f"{'='*60}")
    print(f"  Tools scanned:         {stats['processed']}")
    print(f"  Tools modified:        {stats['modified']}")
    print(f"  Already enriched:      {stats['skipped_no_changes']}")
    print(f"  About sections added:  {stats['about_added']}")
    print(f"  Quick Facts added:     {stats['quick_facts_added']}")
    print(f"  Visible FAQs added:    {stats['faq_added']}")
    print(f"  Twitter meta added:    {stats['twitter_added']}")
    print(f"  og:site_name fixed:    {stats['og_fixed']}")
    print(f"  Errors:                {stats['errors']}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
