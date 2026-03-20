#!/usr/bin/env python3
"""
Batch enrichment script for Zovo tools (t-z).
Adds MISSING enrichment layers to each tool's index.html:
1. About This Tool section
2. Quick Facts cards
3. Visible FAQ from JSON-LD
4. Twitter meta tags
5. Fix og:site_name from "Zovo Tools" to "Zovo"
"""

import os
import re
import json
import html

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

# Tool-specific fourth fact for QuickFacts cards
TOOL_FACTS = {
    "table-generator": "6 Export Formats",
    "take-home-pay-calculator": "2026 Tax Brackets",
    "tax-bracket-calculator": "Federal + State",
    "tax-calculator": "All 50 States",
    "tax-refund-calculator": "Instant Estimate",
    "tdee-calculator": "5 Activity Levels",
    "temperature-converter": "3 Scales",
    "text-case-converter": "10+ Cases",
    "text-diff-checker": "Side-by-Side View",
    "text-generator": "Multiple Styles",
    "text-repeater": "Instant Output",
    "text-summarizer": "Adjustable Length",
    "text-to-handwriting": "Multiple Fonts",
    "text-to-speech": "Multiple Voices",
    "thesis-statement-generator": "Multiple Types",
    "time-calculator": "Add & Subtract",
    "time-to-decimal-calculator": "Multiple Formats",
    "time-zone-meeting-planner": "All Time Zones",
    "timecard-calculator": "Weekly Totals",
    "timestamp-converter": "Unix & ISO",
    "timezone-converter": "400+ Zones",
    "tip-calculator": "Split Support",
    "tip-split-calculator": "Per-Person Split",
    "trademark-search": "USPTO Database",
    "tuner": "Chromatic Tuner",
    "typing-speed-test": "WPM Tracking",
    "typing-test": "Live Accuracy",
    "unit-converter": "100+ Units",
    "unit-price-calculator": "Compare Prices",
    "upc-code-generator": "Multiple Formats",
    "url-encoder": "Encode & Decode",
    "url-encoder-decoder": "Encode & Decode",
    "url-shortener": "Instant Links",
    "usd-to-inr-converter": "Live Rates",
    "utc-to-pst-converter": "DST Aware",
    "uuid-generator": "v1 & v4 Support",
    "vcard-generator": "vCard 3.0",
    "video-compressor": "Multiple Formats",
    "video-to-gif": "Custom Frames",
    "video-to-gif-converter": "Custom Frames",
    "voltage-divider-calculator": "Schematic View",
    "volume-calculator": "10+ Shapes",
    "water-intake-calculator": "Body-Based",
    "watermark-maker": "Text & Image",
    "web-scraper": "CSS Selectors",
    "webhook-tester": "Live Requests",
    "webp-converter": "Batch Convert",
    "website-mockup-generator": "Live Preview",
    "whiteboard": "Infinite Canvas",
    "whiteboard-tool": "Infinite Canvas",
    "whois-lookup": "Domain Details",
    "wifi-speed-test": "Ping & Jitter",
    "wire-gauge-calculator": "AWG & Metric",
    "wireframe-tool": "Drag & Drop",
    "word-cloud-generator": "Custom Colors",
    "word-counter": "Real-Time Count",
    "word-problem-solver": "Step-by-Step",
    "word-scramble-solver": "Instant Results",
    "word-to-pdf-converter": "Preserves Format",
    "xml-formatter": "Syntax Highlight",
    "yaml-to-json-converter": "Bidirectional",
    "yaml-validator": "Error Details",
    "youtube-converter": "Multiple Formats",
    "youtube-thumbnail": "HD Downloads",
}

# Tool-specific "what it does" descriptions for About This Tool
TOOL_DESCRIPTIONS = {
    "table-generator": "create and format tables in HTML, Markdown, CSV, JSON, LaTeX, and ASCII formats with a visual editor",
    "take-home-pay-calculator": "calculate your net take-home pay after federal taxes, state taxes, Social Security, Medicare, and other deductions",
    "tax-bracket-calculator": "determine your federal and state income tax brackets and see exactly how your income is taxed at each marginal rate",
    "tax-calculator": "estimate your total income tax liability including federal, state, and FICA taxes with current year tax brackets",
    "tax-refund-calculator": "estimate your federal and state tax refund based on your income, withholdings, deductions, and credits",
    "tdee-calculator": "calculate your Total Daily Energy Expenditure based on your age, weight, height, and activity level using multiple proven formulas",
    "temperature-converter": "convert temperatures between Fahrenheit, Celsius, and Kelvin scales instantly with the conversion formula shown",
    "text-case-converter": "transform text between uppercase, lowercase, title case, sentence case, camelCase, snake_case, and more",
    "text-diff-checker": "compare two blocks of text side-by-side and highlight the exact differences between them at the character and line level",
    "text-generator": "generate placeholder and random text including Lorem Ipsum, paragraphs, sentences, and custom patterns for design and development",
    "text-repeater": "repeat any text string a specified number of times with custom separators, prefixes, and suffixes",
    "text-summarizer": "condense long text into a shorter summary while preserving the key points and main ideas",
    "text-to-handwriting": "convert typed text into realistic handwriting-style output using multiple handwriting fonts and customizable styles",
    "text-to-speech": "convert written text to spoken audio using your browser's built-in speech synthesis with multiple voice and language options",
    "thesis-statement-generator": "create well-structured thesis statements for essays and research papers based on your topic, position, and supporting reasons",
    "time-calculator": "add and subtract hours, minutes, and seconds to calculate time durations, differences, and elapsed time",
    "time-to-decimal-calculator": "convert time values in hours and minutes to decimal format and back, useful for timesheets and billing",
    "time-zone-meeting-planner": "find the best meeting time across multiple time zones and see availability overlaps for global teams",
    "timecard-calculator": "calculate work hours, overtime, and pay from your timecard entries with weekly and bi-weekly totals",
    "timestamp-converter": "convert between Unix timestamps, ISO 8601 dates, and human-readable date formats in any timezone",
    "timezone-converter": "convert times between any two time zones worldwide with daylight saving time adjustments",
    "tip-calculator": "calculate the tip amount and total bill based on your bill amount, tip percentage, and number of people splitting",
    "tip-split-calculator": "split a restaurant bill and tip evenly among multiple people with customizable tip percentages",
    "trademark-search": "search the USPTO trademark database to check if a name, logo, or slogan is already registered or pending",
    "tuner": "tune musical instruments using your device's microphone with real-time pitch detection and visual feedback",
    "typing-speed-test": "measure your typing speed in words per minute with accuracy tracking and performance statistics",
    "typing-test": "test and improve your typing speed and accuracy with timed exercises and detailed performance metrics",
    "unit-converter": "convert between hundreds of units across length, weight, volume, temperature, speed, area, and more categories",
    "unit-price-calculator": "compare prices per unit across different package sizes and quantities to find the best value",
    "upc-code-generator": "generate valid UPC-A and EAN-13 barcodes with automatic check digit calculation and downloadable images",
    "url-encoder": "encode and decode URLs and URI components to safely include special characters in web addresses",
    "url-encoder-decoder": "encode and decode URLs and URI components to safely include special characters in web addresses",
    "url-shortener": "create shortened URLs that redirect to your long links, making them easier to share and track",
    "usd-to-inr-converter": "convert US Dollars to Indian Rupees and vice versa with current exchange rate information",
    "utc-to-pst-converter": "convert between UTC and Pacific Standard Time with automatic daylight saving time detection",
    "uuid-generator": "generate universally unique identifiers in v1 and v4 formats for use in databases, APIs, and software development",
    "vcard-generator": "create vCard contact files with name, phone, email, address, and other details that can be imported into any contacts app",
    "video-compressor": "reduce video file size while maintaining quality by adjusting resolution, bitrate, and codec settings in your browser",
    "video-to-gif": "convert video clips to animated GIF images with customizable frame rate, size, and quality settings",
    "video-to-gif-converter": "convert video clips to animated GIF images with customizable frame rate, resolution, and quality settings",
    "voltage-divider-calculator": "calculate output voltage, resistor values, and current for voltage divider circuits with a visual schematic",
    "volume-calculator": "calculate the volume of 3D shapes including spheres, cylinders, cones, cubes, pyramids, and more",
    "water-intake-calculator": "determine your recommended daily water intake based on your body weight, activity level, and climate conditions",
    "watermark-maker": "add text or image watermarks to your photos with customizable position, opacity, size, and rotation",
    "web-scraper": "extract data from web pages using CSS selectors and XPath queries with structured output in JSON and CSV formats",
    "webhook-tester": "test and debug webhooks by generating unique endpoint URLs, inspecting incoming requests, and viewing headers and payloads",
    "webp-converter": "convert images between WebP, PNG, JPEG, and other formats with quality and size controls",
    "website-mockup-generator": "create realistic website mockup previews by placing screenshots into device frames for presentations and portfolios",
    "whiteboard": "draw, sketch, and collaborate on an infinite canvas with shapes, text, freehand drawing, and export options",
    "whiteboard-tool": "draw, sketch, and diagram on an infinite canvas with shapes, text, freehand tools, and export capabilities",
    "whois-lookup": "look up domain registration details including owner, registrar, creation date, expiration, and nameserver information",
    "wifi-speed-test": "measure your internet connection speed including download, upload, ping, and jitter right from your browser",
    "wire-gauge-calculator": "calculate wire gauge requirements based on current, voltage drop, distance, and material for electrical installations",
    "wireframe-tool": "create website and app wireframes with drag-and-drop UI components, grids, and export to PNG or SVG",
    "word-cloud-generator": "create visual word clouds from any text with customizable colors, fonts, shapes, and word weighting",
    "word-counter": "count words, characters, sentences, and paragraphs in your text with real-time statistics and reading time estimates",
    "word-problem-solver": "solve math word problems step by step with explanations for arithmetic, algebra, percentages, and more",
    "word-scramble-solver": "unscramble letters to find all valid English words, useful for word games like Scrabble and Words With Friends",
    "word-to-pdf-converter": "convert Word documents to PDF format while preserving formatting, fonts, images, and layout",
    "xml-formatter": "format, validate, and beautify XML documents with syntax highlighting, indentation, and error detection",
    "yaml-to-json-converter": "convert between YAML and JSON formats with validation, formatting, and error highlighting",
    "yaml-validator": "validate YAML syntax, detect errors, and format YAML documents with detailed error messages and line numbers",
    "youtube-converter": "download and convert YouTube videos to MP3, MP4, and other formats with quality selection",
    "youtube-thumbnail": "download YouTube video thumbnails in all available resolutions including HD and maxres quality",
}


def get_tool_name(slug):
    """Derive tool name from slug."""
    return slug.replace("-", " ").title()


def has_about_section(content):
    return bool(re.search(r'about.this.tool|about-this-tool', content, re.IGNORECASE))


def has_quick_facts(content):
    return bool(re.search(r'quick.facts|quick-facts|quickfacts', content, re.IGNORECASE))


def has_visible_faq(content):
    return bool(re.search(r'Common Questions|Frequently Asked', content, re.IGNORECASE))


def has_faqpage_jsonld(content):
    return bool(re.search(r'FAQPage', content))


def has_twitter_card(content):
    return bool(re.search(r'twitter:card', content, re.IGNORECASE))


def has_og_sitename_zovo_tools(content):
    return bool(re.search(r'og:site_name.*content\s*=\s*"Zovo Tools"', content, re.IGNORECASE))


def extract_faq_from_jsonld(content):
    """Extract FAQ Q&A pairs from FAQPage JSON-LD."""
    faqs = []
    # Find all JSON-LD script blocks
    jsonld_blocks = re.findall(
        r'<script\s+type="application/ld\+json">\s*(\{.*?\})\s*</script>',
        content, re.DOTALL
    )
    for block in jsonld_blocks:
        try:
            data = json.loads(block)
            if data.get("@type") == "FAQPage" and "mainEntity" in data:
                for entity in data["mainEntity"]:
                    if entity.get("@type") == "Question":
                        q = entity.get("name", "")
                        a = entity.get("acceptedAnswer", {}).get("text", "")
                        if q and a:
                            faqs.append((q, a))
        except json.JSONDecodeError:
            continue
    return faqs


def extract_meta_description(content):
    """Extract the meta description from HTML."""
    match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content, re.IGNORECASE)
    if match:
        return match.group(1)
    return ""


def extract_title(content):
    """Extract the page title."""
    match = re.search(r'<title>([^<]*)</title>', content)
    if match:
        return match.group(1)
    return ""


def extract_og_description(content):
    """Extract og:description."""
    match = re.search(r'og:description.*?content="([^"]*)"', content, re.IGNORECASE)
    if match:
        return match.group(1)
    return ""


def build_about_section(slug, tool_name):
    """Build the About This Tool HTML section."""
    desc = TOOL_DESCRIPTIONS.get(slug, f"use the {tool_name} quickly and easily")
    return f'''
<!-- About This Tool -->
<section id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;font-family:Inter,sans-serif;">
  <h2 style="color:#00ff88;font-size:1.3rem;margin-top:0;">About This Tool</h2>
  <p style="color:#b0b0c0;line-height:1.7;margin-bottom:1rem;">The {tool_name} lets you {desc}. Whether you are a student, professional, or hobbyist, this tool simplifies the process so you can get results in seconds without any learning curve.</p>
  <p style="color:#b0b0c0;line-height:1.7;margin-bottom:0;">Built by Michael Lip, this tool runs 100% client-side in your browser. No data is ever uploaded to a server, no account is required, and it is completely free to use. Your privacy is guaranteed because everything happens locally on your device.</p>
</section>
'''


def build_quick_facts(slug, tool_name):
    """Build the Quick Facts HTML section."""
    fourth_fact = TOOL_FACTS.get(slug, "Works Offline")
    return f'''
<!-- Quick Facts -->
<div style="max-width:800px;margin:2rem auto;padding:0 1rem;">
  <p style="color:#00ff88;font-size:0.8rem;font-weight:600;margin:0 0 10px;">Quick Facts</p>
  <div style="display:flex;gap:1rem;flex-wrap:wrap;">
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:120px;">
      <div style="color:#00ff88;font-size:1.1rem;font-weight:700;">100%</div>
      <div style="color:#8888a0;font-size:0.75rem;">Client-Side</div>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:120px;">
      <div style="color:#00ff88;font-size:1.1rem;font-weight:700;">Zero</div>
      <div style="color:#8888a0;font-size:0.75rem;">Data Uploaded</div>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:120px;">
      <div style="color:#00ff88;font-size:1.1rem;font-weight:700;">Free</div>
      <div style="color:#8888a0;font-size:0.75rem;">Forever</div>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:120px;">
      <div style="color:#00ff88;font-size:1.1rem;font-weight:700;">{fourth_fact.split(" ")[0] if " " in fourth_fact else fourth_fact}</div>
      <div style="color:#8888a0;font-size:0.75rem;">{" ".join(fourth_fact.split(" ")[1:]) if " " in fourth_fact else ""}</div>
    </div>
  </div>
</div>
'''


def build_visible_faq(faqs):
    """Build visible FAQ accordion section from JSON-LD FAQ data."""
    if not faqs:
        return ""
    items = ""
    for i, (q, a) in enumerate(faqs):
        q_escaped = html.escape(q)
        a_escaped = html.escape(a)
        items += f'''  <div style="background:#12121a;border:1px solid #1e1e2a;border-radius:12px;padding:24px;margin-bottom:16px;">
    <h3 style="color:#e0e0e8;font-size:1.1rem;margin:0 0 8px 0;">Q: {q_escaped}</h3>
    <p style="color:#b0b0c0;margin:0;line-height:1.6;">{a_escaped}</p>
  </div>
'''
    return f'''
<!-- Visible FAQ Section -->
<section id="faq" style="max-width:800px;margin:48px auto;padding:0 20px;">
  <h2 style="color:#00ff88;font-size:1.5rem;margin-bottom:24px;">Frequently Asked Questions</h2>
{items}</section>
'''


def build_twitter_meta(content, slug, tool_name):
    """Build twitter meta tags from existing OG tags or defaults."""
    og_title = ""
    og_desc = ""
    match_t = re.search(r'og:title.*?content="([^"]*)"', content, re.IGNORECASE)
    if match_t:
        og_title = match_t.group(1)
    else:
        og_title = f"{tool_name} | Free Online Tool"

    match_d = re.search(r'og:description.*?content="([^"]*)"', content, re.IGNORECASE)
    if match_d:
        og_desc = match_d.group(1)
    else:
        meta_desc = extract_meta_description(content)
        og_desc = meta_desc if meta_desc else f"Free online {tool_name.lower()} tool. No signup required."

    return f'''<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(og_title)}">
<meta name="twitter:description" content="{html.escape(og_desc)}">
'''


def process_tool(slug):
    """Process a single tool's index.html and add missing enrichments."""
    filepath = os.path.join(BASE_DIR, slug, "index.html")
    if not os.path.isfile(filepath):
        return None

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    tool_name = get_tool_name(slug)
    changes = []

    # 1. Fix og:site_name "Zovo Tools" -> "Zovo" (check first since it's a replacement)
    if has_og_sitename_zovo_tools(content):
        content = re.sub(
            r'(og:site_name.*?content\s*=\s*")Zovo Tools(")',
            r'\1Zovo\2',
            content,
            flags=re.IGNORECASE
        )
        changes.append("fix og:site_name")

    # 2. Add missing twitter meta tags
    if not has_twitter_card(content):
        twitter_html = build_twitter_meta(content, slug, tool_name)
        # Insert after the last og: meta tag or before </head>
        og_match = list(re.finditer(r'<meta\s+property="og:[^"]*"[^>]*>', content, re.IGNORECASE))
        if og_match:
            insert_pos = og_match[-1].end()
            content = content[:insert_pos] + "\n\n" + twitter_html + "\n" + content[insert_pos:]
        else:
            content = content.replace("</head>", twitter_html + "\n</head>")
        changes.append("add twitter meta")

    # 3. Add missing About This Tool section
    if not has_about_section(content):
        about_html = build_about_section(slug, tool_name)
        # Insert before </body>
        content = content.replace("</body>", about_html + "\n</body>")
        changes.append("add About This Tool")

    # 4. Add missing Quick Facts
    if not has_quick_facts(content):
        qf_html = build_quick_facts(slug, tool_name)
        # Insert before </body>
        content = content.replace("</body>", qf_html + "\n</body>")
        changes.append("add Quick Facts")

    # 5. Add missing visible FAQ (only if FAQPage JSON-LD exists but no visible FAQ)
    if has_faqpage_jsonld(content) and not has_visible_faq(content):
        faqs = extract_faq_from_jsonld(content)
        if faqs:
            faq_html = build_visible_faq(faqs)
            content = content.replace("</body>", faq_html + "\n</body>")
            changes.append(f"add visible FAQ ({len(faqs)} items)")

    # Write changes
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    return changes


def main():
    print("=" * 65)
    print("  ZOVO TOOLS ENRICHMENT SCRIPT (t-z)")
    print("=" * 65)
    print()

    # Gather all t-z tool directories
    all_dirs = sorted([
        d for d in os.listdir(BASE_DIR)
        if os.path.isdir(os.path.join(BASE_DIR, d))
        and d[0].lower() in "tuvwxyz"
        and os.path.isfile(os.path.join(BASE_DIR, d, "index.html"))
    ])

    print(f"Found {len(all_dirs)} tools (t-z) with index.html")
    print()

    stats = {
        "total": len(all_dirs),
        "modified": 0,
        "skipped": 0,
        "about_added": 0,
        "quickfacts_added": 0,
        "faq_added": 0,
        "twitter_added": 0,
        "sitename_fixed": 0,
    }

    for slug in all_dirs:
        changes = process_tool(slug)
        if changes is None:
            print(f"  SKIP  {slug} (no index.html)")
            stats["skipped"] += 1
            continue

        if changes:
            stats["modified"] += 1
            change_str = ", ".join(changes)
            print(f"  [MOD] {slug}: {change_str}")
            for c in changes:
                if "About" in c:
                    stats["about_added"] += 1
                if "Quick Facts" in c:
                    stats["quickfacts_added"] += 1
                if "visible FAQ" in c:
                    stats["faq_added"] += 1
                if "twitter" in c:
                    stats["twitter_added"] += 1
                if "og:site_name" in c:
                    stats["sitename_fixed"] += 1
        else:
            print(f"  [ OK ] {slug}: no changes needed")

    print()
    print("=" * 65)
    print("  SUMMARY")
    print("=" * 65)
    print(f"  Tools scanned:          {stats['total']}")
    print(f"  Tools modified:         {stats['modified']}")
    print(f"  Tools unchanged:        {stats['total'] - stats['modified'] - stats['skipped']}")
    print(f"  Tools skipped:          {stats['skipped']}")
    print()
    print(f"  About This Tool added:  {stats['about_added']}")
    print(f"  Quick Facts added:      {stats['quickfacts_added']}")
    print(f"  Visible FAQ added:      {stats['faq_added']}")
    print(f"  Twitter meta added:     {stats['twitter_added']}")
    print(f"  og:site_name fixed:     {stats['sitename_fixed']}")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
