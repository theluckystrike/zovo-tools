#!/usr/bin/env python3
"""
Enrichment script for Zovo tools starting with letters i through n.
Adds missing enrichment layers to each tool's index.html:
1. About This Tool section
2. QuickFacts section
3. Visible FAQ (from JSON-LD FAQPage)
4. Twitter meta tags
5. Fix og:site_name from "Zovo Tools" to "Zovo"
"""

import os
import re
import json

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

# Tool-specific facts for QuickFacts
TOOL_SPECIFIC_FACTS = {
    "ico-converter": ("Multi-Size", "Up to 256×256"),
    "icon-generator": ("Icon Sizes", "16px to 512px"),
    "ics-calendar-generator": ("ICS Format", "Works Everywhere"),
    "image-compressor": ("Up to 80%", "Size Reduction"),
    "image-converter": ("10+ Formats", "Supported"),
    "image-cropper": ("Pixel Perfect", "Precision Crop"),
    "image-metadata-viewer": ("EXIF Data", "Full Extraction"),
    "image-resizer": ("Custom Sizes", "Any Dimension"),
    "image-to-base64": ("Instant Encode", "Copy & Paste"),
    "image-to-text-ocr": ("OCR Powered", "Text Extraction"),
    "inflation-calculator": ("CPI Data", "Historical Rates"),
    "instagram-font-generator": ("30+ Styles", "Unicode Fonts"),
    "interest-rate-calculator": ("APR & APY", "Both Supported"),
    "internet-service-comparison": ("Side by Side", "ISP Compare"),
    "internet-speed-checker": ("Real-Time", "Speed Test"),
    "investment-calculator": ("Compound Growth", "Visualized"),
    "investment-return-calculator": ("ROI Tracking", "Full Analysis"),
    "invoice-generator": ("PDF Export", "Professional Layout"),
    "ip-address-tracker": ("Geolocation", "Instant Lookup"),
    "ip-lookup": ("IP Details", "Full Geolocation"),
    "javascript-playground": ("Live Preview", "Real-Time Output"),
    "js-minifier": ("Code Shrink", "Instant Minify"),
    "json-formatter": ("Syntax Check", "Auto-Validate"),
    "json-path-finder": ("Path Query", "Click to Copy"),
    "json-to-xml-converter": ("Instant Convert", "Valid XML"),
    "json-viewer": ("Tree View", "Collapsible Nodes"),
    "json-yaml-converter": ("Bidirectional", "JSON ↔ YAML"),
    "jwt-decoder": ("Token Parse", "Header + Payload"),
    "kanban-board": ("Drag & Drop", "Visual Workflow"),
    "keto-calculator": ("Macro Split", "Personalized"),
    "keyword-density-checker": ("SEO Analysis", "Word Frequency"),
    "lease-calculator": ("Monthly Cost", "Full Breakdown"),
    "life-expectancy-calculator": ("Health Factors", "Personalized"),
    "loan-calculator": ("Payment Plan", "Amortization"),
    "loan-simulator": ("What-If", "Scenario Compare"),
    "logo-maker": ("Custom Design", "Download SVG/PNG"),
    "lorem-ipsum-generator": ("Paragraphs", "Words & Sentences"),
    "macro-calculator": ("TDEE Based", "Custom Ratios"),
    "madlib-generator": ("Fill-in Fun", "Instant Stories"),
    "markdown-editor": ("Live Preview", "Split Pane"),
    "markdown-table-generator": ("Visual Editor", "Copy Markdown"),
    "markdown-to-html": ("Instant Render", "Full Syntax"),
    "markup-calculator": ("Profit Margin", "Cost Analysis"),
    "math-equation-solver": ("Step by Step", "Full Solutions"),
    "math-solver": ("All Operations", "Step by Step"),
    "mathematics-solver": ("Advanced Math", "Detailed Steps"),
    "matrix-calculator": ("Operations", "Up to 10×10"),
    "meeting-cost-calculator": ("Time = Money", "Per-Minute Cost"),
    "meme-generator": ("Custom Text", "Popular Templates"),
    "meta-tag-generator": ("SEO Ready", "All Major Tags"),
    "metronome": ("Adjustable BPM", "Audio Precision"),
    "mind-map-maker": ("Visual Thinking", "Drag & Drop"),
    "mind-map-tool": ("Branch Layout", "Export Ready"),
    "mla-citation-generator": ("MLA 9th Ed.", "Auto-Format"),
    "molarity-calculator": ("Chemistry", "Precise Molarity"),
    "morse-code-translator": ("Encode/Decode", "Audio Playback"),
    "mortgage-calculator": ("Amortization", "Full Schedule"),
    "mortgage-comparison": ("Side by Side", "Rate Compare"),
    "mortgage-quote-calculator": ("Instant Quote", "All Costs"),
    "mp3-cutter": ("Trim Audio", "Waveform View"),
    "net-worth-calculator": ("Assets & Debts", "Full Picture"),
    "neumorphism-generator": ("Soft UI", "CSS Output"),
    "nginx-config-generator": ("Server Config", "Best Practices"),
    "noise-generator": ("White/Pink/Brown", "Audio Therapy"),
    "number-base-converter": ("Any Base", "2 to 36"),
    "number-generator": ("Random Numbers", "Custom Range"),
    "number-system-converter": ("Hex/Oct/Bin", "Instant Convert"),
}

# Tool descriptions for About This Tool
TOOL_DESCRIPTIONS = {
    "ico-converter": "Convert PNG, JPG, and WebP images into ICO favicon files with support for multiple icon sizes. Whether you need favicons for a website or icons for a Windows application, this tool handles the conversion entirely in your browser with no uploads required.",
    "icon-generator": "Create custom icons in various sizes and formats for your projects. Generate clean, scalable icons that work across websites, apps, and desktop applications without any design software.",
    "ics-calendar-generator": "Generate ICS calendar files that work with Google Calendar, Apple Calendar, Outlook, and other calendar applications. Create events with custom dates, times, locations, and recurrence rules.",
    "image-compressor": "Reduce image file sizes without visible quality loss. This tool uses browser-based compression algorithms to shrink PNG, JPG, and WebP files, making them load faster on websites while maintaining visual clarity.",
    "image-converter": "Convert images between popular formats including PNG, JPG, WebP, GIF, and BMP. Change formats instantly in your browser with options for quality and size adjustments.",
    "image-cropper": "Crop images with pixel-level precision using an intuitive visual editor. Set exact dimensions, use aspect ratio presets, and export your cropped images in multiple formats.",
    "image-metadata-viewer": "View EXIF, IPTC, and XMP metadata embedded in your photos and images. See camera settings, GPS coordinates, timestamps, and other hidden data stored in your image files.",
    "image-resizer": "Resize images to exact pixel dimensions or by percentage. Maintain aspect ratio, batch resize multiple images, and export in various formats for web, social media, or print.",
    "image-to-base64": "Convert images to Base64 encoded strings for embedding directly in HTML, CSS, or JavaScript. Eliminate extra HTTP requests by inlining small images as data URIs.",
    "image-to-text-ocr": "Extract text from images using optical character recognition. Upload screenshots, photos of documents, or scanned pages and get editable, copyable text output.",
    "inflation-calculator": "Calculate how inflation affects purchasing power over time. See how the value of money has changed historically and project future values using CPI-based inflation data.",
    "instagram-font-generator": "Generate stylish Unicode text for Instagram bios, captions, and comments. Choose from dozens of font styles that work on Instagram, Twitter, Facebook, and other platforms.",
    "interest-rate-calculator": "Calculate interest rates, payments, and total costs for loans and investments. Compare APR vs APY, see how compounding frequency affects returns, and plan your finances.",
    "internet-service-comparison": "Compare internet service providers side by side. Evaluate plans based on speed, price, data caps, and contract terms to find the best internet deal for your needs.",
    "internet-speed-checker": "Test your internet connection speed with download and upload measurements. Get real-time results to verify your ISP is delivering the speeds you are paying for.",
    "investment-calculator": "Project investment growth with compound interest over time. Visualize how regular contributions, different interest rates, and various time horizons affect your portfolio.",
    "investment-return-calculator": "Calculate total return on investment including dividends, capital gains, and fees. Compare different investment scenarios and track annualized performance.",
    "invoice-generator": "Create professional invoices with customizable templates. Add your business details, line items, tax calculations, and payment terms, then export as PDF.",
    "ip-address-tracker": "Look up any IP address to find its geographic location, ISP, organization, and network information. Useful for security analysis, network troubleshooting, and content verification.",
    "ip-lookup": "Get detailed information about any IP address including geolocation, hostname, ISP, and ASN data. Quickly identify the origin and owner of network traffic.",
    "javascript-playground": "Write, test, and debug JavaScript code in a live browser environment. See console output in real time, experiment with DOM manipulation, and prototype ideas without any setup.",
    "js-minifier": "Minify JavaScript code to reduce file size and improve page load times. Remove whitespace, comments, and unnecessary characters while preserving functionality.",
    "json-formatter": "Format, validate, and beautify JSON data with syntax highlighting and error detection. Paste messy JSON and get clean, properly indented output with tree view navigation.",
    "json-path-finder": "Navigate JSON structures and find paths to specific values. Click any element to get its JSONPath expression, making it easy to reference data in your code.",
    "json-to-xml-converter": "Convert JSON data to well-formed XML and vice versa. Handles nested objects, arrays, and attributes with configurable output formatting.",
    "json-viewer": "Visualize JSON data in an interactive tree view with collapsible nodes. Search, filter, and explore large JSON documents with syntax highlighting.",
    "json-yaml-converter": "Convert between JSON and YAML formats bidirectionally. Paste JSON to get YAML or paste YAML to get JSON with proper formatting and validation.",
    "jwt-decoder": "Decode and inspect JSON Web Tokens without sending them to any server. View the header, payload, and signature claims of JWTs used in authentication systems.",
    "kanban-board": "Organize tasks and projects with a visual drag-and-drop kanban board. Create columns, add cards, set priorities, and track workflow progress in your browser.",
    "keto-calculator": "Calculate your ideal macronutrient ratios for a ketogenic diet. Get personalized fat, protein, and carb targets based on your body metrics and activity level.",
    "keyword-density-checker": "Analyze the keyword density and word frequency in your text content. Optimize your writing for SEO by identifying overused or underused keywords.",
    "lease-calculator": "Calculate monthly lease payments, total costs, and buyout options for vehicle or equipment leases. Compare lease vs buy scenarios with detailed breakdowns.",
    "life-expectancy-calculator": "Estimate life expectancy based on health factors, lifestyle choices, and demographic data. Get personalized insights about factors that influence longevity.",
    "loan-calculator": "Calculate monthly payments, total interest, and amortization schedules for any type of loan. Compare different loan terms and interest rates side by side.",
    "loan-simulator": "Simulate different loan scenarios with adjustable parameters. See how changes in interest rate, term length, and extra payments affect your total cost.",
    "logo-maker": "Design custom logos with text, shapes, and colors. Export your logo in SVG and PNG formats for use on websites, business cards, and social media.",
    "lorem-ipsum-generator": "Generate placeholder text in paragraphs, sentences, or words. Get classic lorem ipsum or alternative placeholder text for your design mockups and prototypes.",
    "macro-calculator": "Calculate your daily macronutrient needs based on your TDEE, body composition goals, and activity level. Get personalized protein, carb, and fat targets.",
    "madlib-generator": "Create hilarious fill-in-the-blank stories. Enter nouns, verbs, adjectives, and other word types to generate unique and entertaining mad lib stories.",
    "markdown-editor": "Write and preview Markdown in a split-pane editor. See your formatted output in real time with support for tables, code blocks, images, and all standard Markdown syntax.",
    "markdown-table-generator": "Create Markdown tables visually with a spreadsheet-like interface. Add rows and columns, enter data, and copy perfectly formatted Markdown table syntax.",
    "markdown-to-html": "Convert Markdown text to clean HTML output. Supports full GitHub-flavored Markdown syntax including tables, task lists, code blocks, and footnotes.",
    "markup-calculator": "Calculate profit margins, markups, and selling prices from cost and desired profit. Essential for retail pricing, wholesale calculations, and business planning.",
    "math-equation-solver": "Solve mathematical equations step by step. Enter algebraic, quadratic, or system-of-equations problems and get detailed solutions with explanations.",
    "math-solver": "Solve arithmetic, algebra, and calculus problems with step-by-step explanations. Enter any math expression and get the solution along with the working process.",
    "mathematics-solver": "Advanced mathematics solver covering algebra, calculus, trigonometry, and more. Get detailed step-by-step solutions for complex mathematical problems.",
    "matrix-calculator": "Perform matrix operations including addition, multiplication, determinants, inverse, transpose, and eigenvalues. Supports matrices up to 10x10.",
    "meeting-cost-calculator": "Calculate the real cost of meetings based on attendee salaries and duration. See how much your organization spends on meetings and identify opportunities to save.",
    "meme-generator": "Create memes with custom text on popular templates. Add top and bottom text, choose from trending formats, and download your meme instantly.",
    "meta-tag-generator": "Generate HTML meta tags for SEO optimization. Create title tags, meta descriptions, Open Graph tags, Twitter cards, and other essential meta tags for your web pages.",
    "metronome": "A precise digital metronome with adjustable BPM, time signatures, and accent patterns. Practice music with consistent timing using audio and visual beat indicators.",
    "mind-map-maker": "Create visual mind maps to organize ideas, plan projects, and brainstorm. Add branches, colors, and notes with an intuitive drag-and-drop interface.",
    "mind-map-tool": "Build structured mind maps with automatic layout. Organize thoughts, create hierarchies, and export your mind maps for presentations and documentation.",
    "mla-citation-generator": "Generate properly formatted MLA 9th edition citations for books, articles, websites, and other sources. Create Works Cited entries and in-text citations automatically.",
    "molarity-calculator": "Calculate molarity, moles, volume, and molecular weight for chemistry solutions. Essential for lab preparation and stoichiometry calculations.",
    "morse-code-translator": "Translate text to Morse code and back with audio playback. Hear the dots and dashes as they would sound on a telegraph, and decode Morse code messages.",
    "mortgage-calculator": "Calculate monthly mortgage payments with principal, interest, taxes, and insurance breakdowns. View full amortization schedules and see how extra payments reduce your loan.",
    "mortgage-comparison": "Compare multiple mortgage offers side by side. Evaluate different rates, terms, and down payments to find the most cost-effective home loan option.",
    "mortgage-quote-calculator": "Get instant mortgage payment estimates with detailed cost breakdowns. Factor in down payment, interest rate, PMI, taxes, and insurance for a complete picture.",
    "mp3-cutter": "Trim and cut MP3 audio files with a visual waveform editor. Select precise start and end points to extract the exact audio segment you need.",
    "net-worth-calculator": "Calculate your total net worth by listing assets and liabilities. Track your financial health over time and see a clear picture of your overall financial position.",
    "neumorphism-generator": "Generate soft UI (neumorphism) CSS styles with an interactive visual editor. Adjust shadows, border radius, and colors to create modern neumorphic design elements.",
    "nginx-config-generator": "Generate Nginx server configuration files with best practices. Create configs for reverse proxy, SSL, caching, gzip compression, and common web application setups.",
    "noise-generator": "Generate white, pink, and brown noise for focus, relaxation, and sleep. Adjust volume and noise type to create the perfect ambient sound environment.",
    "number-base-converter": "Convert numbers between any bases from 2 (binary) to 36. Handles decimal, binary, octal, hexadecimal, and custom base conversions instantly.",
    "number-generator": "Generate random numbers within a custom range with options for unique numbers, specific counts, and sorting. Useful for lotteries, sampling, and testing.",
    "number-system-converter": "Convert between binary, octal, decimal, and hexadecimal number systems. See conversions update in real time as you type with step-by-step explanations.",
}


def get_tool_dirs():
    """Get all tool directories starting with letters i through n that have an index.html."""
    tools = []
    for name in sorted(os.listdir(BASE_DIR)):
        if not name[0].isalpha():
            continue
        first_letter = name[0].lower()
        if first_letter < 'i' or first_letter > 'n':
            continue
        html_path = os.path.join(BASE_DIR, name, "index.html")
        if os.path.isfile(html_path):
            tools.append(name)
    return tools


def get_tool_name(slug):
    """Derive tool name from slug."""
    return slug.replace("-", " ").title()


def extract_title_from_html(html):
    """Extract the <title> text from HTML."""
    m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip()
    return ""


def extract_description_from_html(html):
    """Extract meta description from HTML."""
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return ""


def extract_faq_from_jsonld(html):
    """Extract FAQ Q&A pairs from FAQPage JSON-LD."""
    faqs = []
    # Find all JSON-LD blocks
    blocks = re.findall(r'<script\s+type=["\']application/ld\+json["\']>(.*?)</script>', html, re.DOTALL | re.IGNORECASE)
    for block in blocks:
        try:
            data = json.loads(block)
        except json.JSONDecodeError:
            continue

        # Handle @graph structure
        if "@graph" in data:
            for item in data["@graph"]:
                if item.get("@type") == "FAQPage" and "mainEntity" in item:
                    for q in item["mainEntity"]:
                        name = q.get("name", "")
                        answer = q.get("acceptedAnswer", {}).get("text", "")
                        if name and answer:
                            faqs.append((name, answer))
        elif data.get("@type") == "FAQPage" and "mainEntity" in data:
            for q in data["mainEntity"]:
                name = q.get("name", "")
                answer = q.get("acceptedAnswer", {}).get("text", "")
                if name and answer:
                    faqs.append((name, answer))
    return faqs


def has_about_section(html):
    return "About This Tool" in html or "about-this-tool" in html


def has_quick_facts(html):
    return "Quick Facts" in html or "quick-facts" in html or "quickfacts" in html.lower()


def has_visible_faq(html):
    return "Common Questions" in html or "Frequently Asked" in html or "faq-item" in html or "faq-q" in html or "faq-question" in html


def has_twitter_card(html):
    return 'twitter:card' in html.lower()


def has_zovo_tools_site_name(html):
    return bool(re.search(r'og:site_name["\']?\s+content=["\']Zovo Tools["\']', html, re.IGNORECASE))


def build_about_section(slug, tool_name):
    desc = TOOL_DESCRIPTIONS.get(slug, f"Use {tool_name} to get quick, accurate results right in your browser. This free tool handles everything you need with a clean, intuitive interface.")
    return f'''
<!-- About This Tool -->
<div id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;font-family:Inter,sans-serif;">
  <h2 style="color:#fff;font-size:1.3rem;margin:0 0 1rem 0;">About This Tool</h2>
  <p style="color:#c0c0d0;font-size:0.92rem;line-height:1.7;margin:0 0 0.75rem 0;">{desc}</p>
  <p style="color:#c0c0d0;font-size:0.92rem;line-height:1.7;margin:0;">Built by Michael Lip, this tool runs 100% client-side in your browser. No data is uploaded or sent to any server. Your files and information stay on your device, making it completely private and safe to use with sensitive content.</p>
</div>
'''


def build_quick_facts(slug, tool_name):
    fact = TOOL_SPECIFIC_FACTS.get(slug, ("Instant Results", "No Waiting"))
    return f'''
<!-- Quick Facts -->
<div id="quick-facts" style="max-width:800px;margin:2rem auto;font-family:Inter,sans-serif;">
  <p style="color:#00ff88;font-size:0.8rem;font-weight:600;margin:0 0 10px;">Quick Facts</p>
  <div style="display:flex;gap:1rem;flex-wrap:wrap;">
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:130px;">
      <p style="color:#00ff88;font-size:1.1rem;font-weight:700;margin:0;">100%</p>
      <p style="color:#8888a0;font-size:0.7rem;margin:2px 0 0;">Client-Side</p>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:130px;">
      <p style="color:#00ff88;font-size:1.1rem;font-weight:700;margin:0;">Zero</p>
      <p style="color:#8888a0;font-size:0.7rem;margin:2px 0 0;">Data Uploaded</p>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:130px;">
      <p style="color:#00ff88;font-size:1.1rem;font-weight:700;margin:0;">Free</p>
      <p style="color:#8888a0;font-size:0.7rem;margin:2px 0 0;">Forever</p>
    </div>
    <div style="background:#1a1a2a;padding:0.75rem;border-radius:6px;text-align:center;flex:1;min-width:130px;">
      <p style="color:#00ff88;font-size:1.1rem;font-weight:700;margin:0;">{fact[0]}</p>
      <p style="color:#8888a0;font-size:0.7rem;margin:2px 0 0;">{fact[1]}</p>
    </div>
  </div>
</div>
'''


def build_visible_faq(faqs):
    if not faqs:
        return ""
    items_html = ""
    for i, (q, a) in enumerate(faqs):
        # Escape HTML entities in Q&A
        q_safe = q.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        a_safe = a.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        items_html += f'''    <div class="enrich-faq-item" style="border-bottom:1px solid #2a2a3a;">
      <button onclick="this.parentElement.classList.toggle('open')" style="width:100%;text-align:left;background:none;border:none;padding:1rem 0;color:#fff;font-size:0.95rem;font-weight:500;cursor:pointer;font-family:Inter,sans-serif;display:flex;justify-content:space-between;align-items:center;">{q_safe}<span style="color:#6C5CE7;font-size:1.3rem;transition:transform 0.3s;">+</span></button>
      <div style="max-height:0;overflow:hidden;transition:max-height 0.3s ease;"><p style="color:#b0b0b8;font-size:0.9rem;line-height:1.7;padding:0 0 1rem 0;margin:0;">{a_safe}</p></div>
    </div>
'''
    return f'''
<!-- Visible FAQ Section -->
<div id="visible-faq" style="max-width:800px;margin:2rem auto;font-family:Inter,sans-serif;">
  <h2 style="color:#fff;font-size:1.3rem;margin:0 0 1rem 0;">Common Questions</h2>
  <div style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:0 1.5rem;">
{items_html}  </div>
</div>
<style>
.enrich-faq-item.open div {{ max-height: 500px !important; }}
.enrich-faq-item.open button span {{ transform: rotate(45deg); }}
</style>
'''


def build_twitter_meta(title, description):
    title_safe = title.replace('"', '&quot;')
    desc_safe = description.replace('"', '&quot;')
    return f'''<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title_safe}">
<meta name="twitter:description" content="{desc_safe}">
'''


def process_tool(slug):
    html_path = os.path.join(BASE_DIR, slug, "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    tool_name = get_tool_name(slug)
    changes = []
    modified = False

    # 5. Fix og:site_name "Zovo Tools" -> "Zovo"
    if has_zovo_tools_site_name(html):
        html = re.sub(
            r'(og:site_name["\']?\s+content=["\'])Zovo Tools(["\'])',
            r'\1Zovo\2',
            html,
            flags=re.IGNORECASE
        )
        changes.append("Fixed og:site_name")
        modified = True

    # 4. Add Twitter meta if missing
    if not has_twitter_card(html):
        title = extract_title_from_html(html)
        desc = extract_description_from_html(html)
        twitter_meta = build_twitter_meta(title or tool_name, desc or f"Free online {tool_name.lower()}. 100% client-side, no data uploaded.")
        # Insert after last og: meta tag or after </title>
        og_matches = list(re.finditer(r'<meta\s+property=["\']og:[^"\']+["\'][^>]*>', html, re.IGNORECASE))
        if og_matches:
            insert_pos = og_matches[-1].end()
            html = html[:insert_pos] + "\n" + twitter_meta + html[insert_pos:]
        else:
            # Insert after </title> or <meta name="description"...>
            m = re.search(r'</title>', html, re.IGNORECASE)
            if m:
                insert_pos = m.end()
                html = html[:insert_pos] + "\n" + twitter_meta + html[insert_pos:]
        changes.append("Added Twitter meta tags")
        modified = True

    # Sections to insert before </body>
    sections_to_add = []

    # 1. About This Tool
    if not has_about_section(html):
        sections_to_add.append(("About This Tool", build_about_section(slug, tool_name)))

    # 2. QuickFacts
    if not has_quick_facts(html):
        sections_to_add.append(("QuickFacts", build_quick_facts(slug, tool_name)))

    # 3. Visible FAQ from JSON-LD
    if not has_visible_faq(html):
        faqs = extract_faq_from_jsonld(html)
        if faqs:
            sections_to_add.append(("Visible FAQ", build_visible_faq(faqs)))

    if sections_to_add:
        # Insert all sections before </body>
        insert_content = "\n".join(s[1] for s in sections_to_add)
        body_close = html.rfind("</body>")
        if body_close == -1:
            # Try end of file
            html += "\n" + insert_content
        else:
            html = html[:body_close] + insert_content + "\n" + html[body_close:]
        changes.extend([s[0] for s in sections_to_add])
        modified = True

    if modified:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

    return changes


def main():
    tools = get_tool_dirs()
    print(f"Found {len(tools)} tools (i-n) to process\n")

    stats = {
        "total": len(tools),
        "modified": 0,
        "about_added": 0,
        "quickfacts_added": 0,
        "faq_added": 0,
        "twitter_added": 0,
        "sitename_fixed": 0,
        "skipped": 0,
    }

    for slug in tools:
        changes = process_tool(slug)
        if changes:
            stats["modified"] += 1
            change_str = ", ".join(changes)
            print(f"  [UPDATED] {slug}: {change_str}")
            for c in changes:
                if "About" in c:
                    stats["about_added"] += 1
                if "QuickFacts" in c:
                    stats["quickfacts_added"] += 1
                if "FAQ" in c:
                    stats["faq_added"] += 1
                if "Twitter" in c:
                    stats["twitter_added"] += 1
                if "site_name" in c:
                    stats["sitename_fixed"] += 1
        else:
            stats["skipped"] += 1
            print(f"  [OK] {slug}: All layers present")

    print(f"\n{'='*60}")
    print(f"ENRICHMENT COMPLETE")
    print(f"{'='*60}")
    print(f"Total tools scanned:       {stats['total']}")
    print(f"Tools modified:            {stats['modified']}")
    print(f"Tools already complete:    {stats['skipped']}")
    print(f"About This Tool added:     {stats['about_added']}")
    print(f"QuickFacts added:          {stats['quickfacts_added']}")
    print(f"Visible FAQ added:         {stats['faq_added']}")
    print(f"Twitter meta added:        {stats['twitter_added']}")
    print(f"og:site_name fixed:        {stats['sitename_fixed']}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
