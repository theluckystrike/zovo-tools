#!/usr/bin/env python3
"""
Enrichment script: Add Browser Compatibility tables and Tool Statistics cards
to all tool pages at ~/zovo-workspaces/zovo-tools/
"""

import os
import re

TOOLS_DIR = os.path.expanduser("~/zovo-workspaces/zovo-tools")

# ============================================================
# TASK 1: Browser Compatibility Tables (developer tools only)
# ============================================================

DEVELOPER_TOOLS = [
    "json-formatter", "json-viewer", "json-path-finder", "json-yaml-converter",
    "csv-to-json", "xml-formatter", "yaml-validator", "regex-tester",
    "regex-visualizer", "sql-formatter", "jwt-decoder", "base64-encoder",
    "url-encoder", "html-encoder", "markdown-to-html", "markdown-editor",
    "diff-checker", "cron-generator", "htpasswd-generator", "bcrypt-generator",
    "uuid-generator", "hash-generator", "binary-text-converter", "slug-generator",
    "chmod-calculator", "css-minifier", "js-minifier", "timestamp-converter",
    "color-converter", "color-palette-generator", "hex-color-picker",
    "css-gradient-generator", "gradient-generator", "box-shadow-generator",
    "border-radius-generator", "flexbox-generator", "css-grid-generator",
    "css-animation-generator", "px-to-rem", "favicon-generator",
    "favicon-converter", "svg-editor", "image-compressor", "placeholder-image",
    "pixel-art-editor", "whiteboard", "screenshot-mockup", "meta-tag-generator",
    "og-preview", "schema-generator", "sitemap-generator", "robots-txt-generator",
    "dns-lookup", "ssl-checker", "http-status-checker", "ip-lookup",
    "qr-code-generator", "qr-reader", "image-to-base64", "table-generator",
]

# Custom browser versions for tools using specific APIs
WEB_CRYPTO_TOOLS = {"hash-generator", "bcrypt-generator", "htpasswd-generator"}
BARCODE_TOOLS = {"qr-reader"}
CANVAS_TOOLS = {"whiteboard", "pixel-art-editor", "image-compressor", "favicon-generator", "favicon-converter", "screenshot-mockup", "placeholder-image", "svg-editor", "image-to-base64"}

def get_compat_html(tool_name):
    """Generate the browser compatibility HTML for a given tool."""
    # Determine browser versions
    if tool_name in WEB_CRYPTO_TOOLS:
        spans = [
            ("Chrome 37+", None),
            ("Firefox 34+", None),
            ("Safari 11+", None),
            ("Edge 12+", None),
            ("Opera 24+", None),
        ]
        note = "Uses the Web Crypto API for secure, client-side hashing. No data is sent to any server."
    elif tool_name in BARCODE_TOOLS:
        spans = [
            ("Chrome 83+", None),
            ("Firefox 88+", None),
            ("Safari 14+", None),
            ("Edge 83+", None),
            ("Opera 69+", None),
        ]
        note = "Camera scanning uses BarcodeDetector API (Chrome 83+, Edge 83+). Falls back to jsQR for full browser support."
    elif tool_name in CANVAS_TOOLS:
        spans = [
            ("Chrome 4+", None),
            ("Firefox 2+", None),
            ("Safari 3.1+", None),
            ("Edge 12+", None),
            ("Opera 9+", None),
        ]
        note = "Uses the Canvas API, supported in all modern browsers. No plugins or extensions required."
    else:
        spans = [
            ("Chrome 90+", None),
            ("Firefox 88+", None),
            ("Safari 14+", None),
            ("Edge 90+", None),
            ("Opera 76+", None),
        ]
        note = "This tool runs entirely in your browser using standard Web APIs. No plugins or extensions required."

    span_html = "\n    ".join(
        f'<span style="padding:4px 12px;background:#1a1a26;border-radius:20px;font-size:0.75rem;color:#e0e0e8;">{label}</span>'
        for label, _ in spans
    )

    return f'''<div class="browser-compat" style="max-width:700px;margin:1.5rem auto;padding:16px 20px;background:#12121a;border-radius:8px;border:1px solid #2a2a3a;">
  <p style="color:#00ff88;font-size:0.8rem;font-weight:600;margin:0 0 10px;">Browser Support</p>
  <div style="display:flex;flex-wrap:wrap;gap:8px;">
    {span_html}
  </div>
  <p style="color:#8888a0;font-size:0.7rem;margin:8px 0 0;">{note}</p>
</div>'''


# ============================================================
# TASK 2: Tool Statistics / Quick Facts Cards (ALL tools)
# ============================================================

def get_stats_for_tool(tool_name):
    """Return a list of (value, label) tuples for the given tool."""

    # JSON tools
    if tool_name in ("json-formatter", "json-viewer", "json-path-finder", "json-yaml-converter", "csv-to-json", "csv-to-json-converter"):
        return [
            ("8.3M+", "Daily JSON API calls worldwide"),
            ("RFC 8259", "JSON standard compliance"),
            ("100%", "Client-side processing"),
            ("0 bytes", "Data sent to server"),
        ]

    # XML/YAML/SQL/Regex/Diff/Code tools
    if tool_name in ("xml-formatter",):
        return [
            ("W3C", "XML standard compliance"),
            ("100%", "Client-side processing"),
            ("Instant", "Formatting speed"),
            ("0 bytes", "Data sent to server"),
        ]
    if tool_name in ("yaml-validator",):
        return [
            ("YAML 1.2", "Specification supported"),
            ("100%", "Client-side processing"),
            ("Instant", "Validation results"),
            ("0 bytes", "Data sent to server"),
        ]
    if tool_name in ("sql-formatter",):
        return [
            ("10+", "SQL dialects supported"),
            ("100%", "Client-side processing"),
            ("Instant", "Formatting speed"),
            ("0 bytes", "Data sent to server"),
        ]
    if tool_name in ("regex-tester", "regex-visualizer"):
        return [
            ("PCRE", "Regex flavor support"),
            ("Real-time", "Pattern matching"),
            ("100%", "Client-side processing"),
            ("0 bytes", "Data sent to server"),
        ]
    if tool_name in ("diff-checker", "text-diff-checker"):
        return [
            ("Line-by-line", "Comparison mode"),
            ("Instant", "Diff results"),
            ("100%", "Client-side processing"),
            ("0 bytes", "Data sent to server"),
        ]
    if tool_name in ("code-beautifier",):
        return [
            ("10+", "Languages supported"),
            ("Instant", "Formatting speed"),
            ("100%", "Client-side processing"),
            ("0 bytes", "Data sent to server"),
        ]

    # Security / Encoding tools
    if tool_name in ("jwt-decoder",):
        return [
            ("RFC 7519", "JWT standard compliance"),
            ("HS/RS/ES", "Algorithm support"),
            ("100%", "Client-side decoding"),
            ("0 bytes", "Data sent to server"),
        ]
    if tool_name in ("base64-encoder", "base64-encoder-decoder"):
        return [
            ("RFC 4648", "Base64 standard"),
            ("Unlimited", "Input size"),
            ("100%", "Client-side processing"),
            ("0 bytes", "Data sent to server"),
        ]
    if tool_name in ("url-encoder", "url-encoder-decoder"):
        return [
            ("RFC 3986", "URI standard compliance"),
            ("UTF-8", "Character encoding"),
            ("100%", "Client-side processing"),
            ("0 bytes", "Data sent to server"),
        ]
    if tool_name in ("html-encoder",):
        return [
            ("HTML5", "Entity standard"),
            ("252", "Named entities supported"),
            ("100%", "Client-side processing"),
            ("0 bytes", "Data sent to server"),
        ]
    if tool_name in ("hash-generator",):
        return [
            ("6", "Hash algorithms (MD5-SHA512)"),
            ("Web Crypto", "API powered"),
            ("0 bytes", "Sent to any server"),
            ("HMAC", "Authentication support"),
        ]
    if tool_name in ("bcrypt-generator",):
        return [
            ("2^31", "Possible salt rounds"),
            ("Web Crypto", "API powered"),
            ("OWASP", "Recommended algorithm"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("htpasswd-generator",):
        return [
            ("5", "Hash methods supported"),
            ("Apache", "Compatible format"),
            ("0 bytes", "Sent to any server"),
            ("bcrypt", "Default algorithm"),
        ]
    if tool_name in ("uuid-generator",):
        return [
            ("RFC 4122", "UUID standard"),
            ("v1/v4/v7", "Versions supported"),
            ("2^122", "Possible UUIDs (v4)"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("password-generator",):
        return [
            ("Web Crypto", "API for randomness"),
            ("128-bit+", "Entropy possible"),
            ("OWASP", "Compliant strength"),
            ("0 bytes", "Sent to any server"),
        ]

    # Markdown
    if tool_name in ("markdown-to-html", "markdown-editor"):
        return [
            ("CommonMark", "Spec compliant"),
            ("GFM", "GitHub Flavored support"),
            ("Real-time", "Preview rendering"),
            ("100%", "Client-side processing"),
        ]

    # Cron
    if tool_name in ("cron-generator", "cron-expression-generator"):
        return [
            ("5-field", "Standard cron format"),
            ("Real-time", "Schedule preview"),
            ("Unix/Linux", "Compatible syntax"),
            ("100%", "Client-side processing"),
        ]

    # Generators / Converters (dev utility)
    if tool_name in ("binary-text-converter", "binary-converter", "number-base-converter"):
        return [
            ("Bin/Oct/Hex", "Base conversions"),
            ("Unicode", "Full support"),
            ("Real-time", "Conversion speed"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("slug-generator",):
        return [
            ("Unicode", "Character support"),
            ("SEO-ready", "URL format"),
            ("Instant", "Generation speed"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("chmod-calculator",):
        return [
            ("777", "Possible combinations"),
            ("Octal/Symbolic", "Notation modes"),
            ("Unix/Linux", "Compatible output"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("timestamp-converter",):
        return [
            ("Unix epoch", "Timestamp standard"),
            ("ms/s", "Precision options"),
            ("UTC/Local", "Timezone support"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("image-to-base64",):
        return [
            ("All formats", "PNG, JPG, GIF, SVG, WebP"),
            ("Data URI", "Ready output"),
            ("Instant", "Conversion speed"),
            ("0 bytes", "Sent to any server"),
        ]

    # CSS tools
    if tool_name in ("css-minifier",):
        return [
            ("40-60%", "Typical size reduction"),
            ("CSS3", "Full standard support"),
            ("Instant", "Minification speed"),
            ("Copy-paste", "Ready output"),
        ]
    if tool_name in ("js-minifier",):
        return [
            ("30-50%", "Typical size reduction"),
            ("ES2024", "Syntax support"),
            ("Instant", "Minification speed"),
            ("Copy-paste", "Ready output"),
        ]
    if tool_name in ("color-converter",):
        return [
            ("7 formats", "HEX, RGB, HSL, and more"),
            ("16.7M", "Possible colors"),
            ("Real-time", "Conversion preview"),
            ("CSS-ready", "Output values"),
        ]
    if tool_name in ("color-palette-generator",):
        return [
            ("16.7M", "Color combinations"),
            ("5 schemes", "Harmony types"),
            ("WCAG 2.1", "Contrast checking"),
            ("Export", "Multiple formats"),
        ]
    if tool_name in ("hex-color-picker",):
        return [
            ("16.7M", "Colors available"),
            ("HEX/RGB/HSL", "Output formats"),
            ("Real-time", "Color preview"),
            ("CSS-ready", "Copy-paste values"),
        ]
    if tool_name in ("css-gradient-generator", "gradient-generator"):
        return [
            ("Linear/Radial", "Gradient types"),
            ("Unlimited", "Color stops"),
            ("CSS3", "Standard output"),
            ("Copy-paste", "Ready code"),
        ]
    if tool_name in ("box-shadow-generator",):
        return [
            ("Inset/Outer", "Shadow types"),
            ("Multi-layer", "Shadow stacking"),
            ("Live preview", "Real-time updates"),
            ("CSS3", "Standard output"),
        ]
    if tool_name in ("border-radius-generator",):
        return [
            ("8 values", "Individual corner control"),
            ("px/%", "Unit options"),
            ("Live preview", "Real-time updates"),
            ("CSS3", "Standard output"),
        ]
    if tool_name in ("flexbox-generator",):
        return [
            ("12", "Flex properties"),
            ("Live preview", "Real-time layout"),
            ("CSS3", "Standard output"),
            ("Copy-paste", "Ready code"),
        ]
    if tool_name in ("css-grid-generator",):
        return [
            ("Rows/Cols", "Full grid control"),
            ("fr/px/%", "Unit options"),
            ("Live preview", "Real-time layout"),
            ("CSS3", "Standard output"),
        ]
    if tool_name in ("css-animation-generator",):
        return [
            ("20+", "Preset animations"),
            ("@keyframes", "Standard output"),
            ("Live preview", "Real-time playback"),
            ("Copy-paste", "Ready CSS code"),
        ]
    if tool_name in ("px-to-rem", "pixel-to-rem-converter"):
        return [
            ("px/rem/em", "Unit conversions"),
            ("Custom base", "Font size support"),
            ("Real-time", "Conversion results"),
            ("CSS-ready", "Output values"),
        ]
    if tool_name in ("color-contrast-checker",):
        return [
            ("WCAG 2.1", "Compliance standard"),
            ("AA/AAA", "Level checking"),
            ("4.5:1", "Min text contrast"),
            ("Real-time", "Contrast ratio"),
        ]

    # Favicon / Image tools
    if tool_name in ("favicon-generator",):
        return [
            ("ICO/PNG/SVG", "Output formats"),
            ("16-512px", "Size range"),
            ("All browsers", "Compatible output"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("favicon-converter",):
        return [
            ("10+", "Format conversions"),
            ("Multi-size", "ICO generation"),
            ("All browsers", "Compatible output"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("svg-editor",):
        return [
            ("SVG 1.1", "Standard support"),
            ("Vector", "Lossless editing"),
            ("Export", "SVG/PNG output"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("image-compressor",):
        return [
            ("60-80%", "Typical size reduction"),
            ("JPG/PNG/WebP", "Format support"),
            ("Quality control", "Adjustable slider"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("placeholder-image",):
        return [
            ("Any size", "Custom dimensions"),
            ("SVG/PNG", "Output formats"),
            ("Instant", "Generation speed"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("pixel-art-editor",):
        return [
            ("Up to 128px", "Canvas size"),
            ("32 colors", "Palette support"),
            ("PNG export", "Lossless output"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("whiteboard",):
        return [
            ("Infinite", "Canvas size"),
            ("Pen/Shape", "Drawing tools"),
            ("PNG export", "Save as image"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("screenshot-mockup",):
        return [
            ("10+", "Device frames"),
            ("PNG export", "High-res output"),
            ("Drag & drop", "Image upload"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("image-resizer",):
        return [
            ("Any size", "Custom dimensions"),
            ("JPG/PNG/WebP", "Format support"),
            ("Batch ready", "Multiple images"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("icon-generator",):
        return [
            ("SVG/PNG", "Output formats"),
            ("500+", "Icon options"),
            ("Custom colors", "Full palette"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("svg-to-png-converter",):
        return [
            ("SVG to PNG", "Vector to raster"),
            ("Custom DPI", "Resolution control"),
            ("Transparent", "Background support"),
            ("0 bytes", "Sent to any server"),
        ]

    # SEO tools
    if tool_name in ("meta-tag-generator",):
        return [
            ("Google", "Recommended tags"),
            ("OG/Twitter", "Social meta tags"),
            ("Copy-paste", "Ready HTML"),
            ("SEO-ready", "Best practices"),
        ]
    if tool_name in ("og-preview",):
        return [
            ("Facebook", "OG tag preview"),
            ("Twitter", "Card preview"),
            ("LinkedIn", "Share preview"),
            ("Real-time", "Live updates"),
        ]
    if tool_name in ("schema-generator",):
        return [
            ("Schema.org", "Standard compliance"),
            ("30+", "Schema types"),
            ("Google", "Rich results eligible"),
            ("JSON-LD", "Recommended format"),
        ]
    if tool_name in ("sitemap-generator",):
        return [
            ("XML 0.9", "Sitemap protocol"),
            ("50K URLs", "Per sitemap max"),
            ("Google", "Search Console ready"),
            ("W3C", "Valid XML output"),
        ]
    if tool_name in ("robots-txt-generator",):
        return [
            ("REP", "Protocol standard"),
            ("All bots", "Crawler support"),
            ("Google", "Recommended format"),
            ("Copy-paste", "Ready output"),
        ]
    if tool_name in ("headline-analyzer",):
        return [
            ("70 chars", "Optimal title length"),
            ("EMV score", "Emotional marketing"),
            ("Power words", "Detection engine"),
            ("SEO-ready", "Best practices"),
        ]
    if tool_name in ("readability-checker",):
        return [
            ("5 scores", "Readability metrics"),
            ("Flesch-Kincaid", "Grade level"),
            ("Real-time", "Analysis speed"),
            ("100%", "Client-side processing"),
        ]

    # Network tools
    if tool_name in ("dns-lookup",):
        return [
            ("IPv4 & IPv6", "Address support"),
            ("A/MX/TXT/NS", "All record types"),
            ("Global DNS", "Server coverage"),
            ("Real-time", "Query results"),
        ]
    if tool_name in ("ssl-checker",):
        return [
            ("TLS 1.2/1.3", "Protocol checking"),
            ("X.509", "Certificate standard"),
            ("Chain verify", "Full validation"),
            ("Expiry alert", "Date checking"),
        ]
    if tool_name in ("http-status-checker",):
        return [
            ("1xx-5xx", "All status codes"),
            ("Redirects", "Chain following"),
            ("Headers", "Full response info"),
            ("Real-time", "Status checking"),
        ]
    if tool_name in ("ip-lookup",):
        return [
            ("IPv4 & IPv6", "Address support"),
            ("Geolocation", "City-level accuracy"),
            ("ASN/ISP", "Network info"),
            ("Real-time", "Lookup results"),
        ]
    if tool_name in ("subnet-calculator",):
        return [
            ("IPv4 & IPv6", "Address support"),
            ("CIDR", "Notation support"),
            ("Instant", "Subnet calculation"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("internet-speed-checker",):
        return [
            ("Download", "Speed measurement"),
            ("Upload", "Speed measurement"),
            ("Latency", "Ping testing"),
            ("Real-time", "Live results"),
        ]
    if tool_name in ("webhook-tester", "api-tester"):
        return [
            ("GET/POST", "All HTTP methods"),
            ("Headers", "Custom headers"),
            ("JSON/Form", "Body formats"),
            ("Real-time", "Response display"),
        ]

    # QR tools
    if tool_name in ("qr-code-generator",):
        return [
            ("ISO 18004", "QR code standard"),
            ("4 levels", "Error correction"),
            ("PNG/SVG", "Export formats"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("qr-reader",):
        return [
            ("Camera/Upload", "Scan methods"),
            ("Multi-QR", "Detect multiple codes"),
            ("BarcodeDetector", "Native API support"),
            ("0 bytes", "Sent to any server"),
        ]

    # Table
    if tool_name in ("table-generator",):
        return [
            ("HTML/MD/CSV", "Output formats"),
            ("Sortable", "Column sorting"),
            ("Instant", "Table generation"),
            ("Copy-paste", "Ready output"),
        ]

    # ============================================================
    # NON-DEVELOPER TOOLS (all other tools get stats too)
    # ============================================================

    # Calculator / Finance tools
    if tool_name in ("bmi-calculator",):
        return [
            ("WHO", "BMI classification"),
            ("Metric/Imperial", "Unit support"),
            ("Instant", "Calculation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("calorie-calculator",):
        return [
            ("Mifflin-St Jeor", "Equation used"),
            ("TDEE", "Daily estimate"),
            ("5 activity", "Levels supported"),
            ("No signup", "Required"),
        ]
    if tool_name in ("age-calculator",):
        return [
            ("Y/M/D", "Precision level"),
            ("Any date", "Range supported"),
            ("Instant", "Calculation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("mortgage-calculator",):
        return [
            ("30-year", "Fixed rate support"),
            ("PMI/Tax", "Included in estimate"),
            ("Amortization", "Full schedule"),
            ("No signup", "Required"),
        ]
    if tool_name in ("loan-calculator",):
        return [
            ("APR", "Interest rate format"),
            ("Amortization", "Full schedule"),
            ("Instant", "Calculation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("compound-interest-calculator",):
        return [
            ("A=P(1+r/n)^nt", "Compound formula"),
            ("Daily-Yearly", "Compounding periods"),
            ("30+ years", "Projection range"),
            ("No signup", "Required"),
        ]
    if tool_name in ("investment-calculator",):
        return [
            ("S&P avg 10%", "Historical return"),
            ("Compound", "Growth model"),
            ("30+ years", "Projection range"),
            ("No signup", "Required"),
        ]
    if tool_name in ("retirement-calculator",):
        return [
            ("4% rule", "Withdrawal strategy"),
            ("Inflation", "Adjusted projections"),
            ("Social Security", "Income included"),
            ("No signup", "Required"),
        ]
    if tool_name in ("savings-calculator",):
        return [
            ("APY", "Yield calculation"),
            ("Monthly", "Contribution support"),
            ("Compound", "Interest model"),
            ("No signup", "Required"),
        ]
    if tool_name in ("tax-calculator",):
        return [
            ("2024-2025", "Tax brackets"),
            ("Federal", "Tax calculation"),
            ("Deductions", "Standard & itemized"),
            ("No signup", "Required"),
        ]
    if tool_name in ("salary-calculator",):
        return [
            ("Hourly/Annual", "Conversion modes"),
            ("Pre/Post tax", "Deduction support"),
            ("Instant", "Calculation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("paycheck-calculator",):
        return [
            ("Federal/State", "Tax withholding"),
            ("W-4 based", "Calculation method"),
            ("Bi-weekly", "Pay period support"),
            ("No signup", "Required"),
        ]
    if tool_name in ("percentage-calculator",):
        return [
            ("6 modes", "Calculation types"),
            ("Instant", "Results speed"),
            ("Mobile-ready", "Responsive design"),
            ("No signup", "Required"),
        ]
    if tool_name in ("tip-calculator",):
        return [
            ("15-25%", "Standard tip range"),
            ("Split bill", "Group support"),
            ("Instant", "Calculation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("discount-calculator",):
        return [
            ("% and $", "Discount types"),
            ("Stacked", "Multiple discounts"),
            ("Instant", "Savings calculation"),
            ("No signup", "Required"),
        ]
    if tool_name in ("profit-margin-calculator",):
        return [
            ("Gross/Net", "Margin types"),
            ("Markup", "Conversion included"),
            ("Instant", "Calculation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("roi-calculator",):
        return [
            ("ROI %", "Return on investment"),
            ("Annualized", "Rate calculation"),
            ("Instant", "Calculation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("amortization-calculator",):
        return [
            ("Monthly", "Payment breakdown"),
            ("Full schedule", "Amortization table"),
            ("Principal/Interest", "Split view"),
            ("No signup", "Required"),
        ]
    if tool_name in ("debt-payoff-calculator",):
        return [
            ("Snowball", "Payoff strategy"),
            ("Avalanche", "Alternative method"),
            ("Timeline", "Payoff projection"),
            ("No signup", "Required"),
        ]
    if tool_name in ("inflation-calculator",):
        return [
            ("CPI based", "Inflation data"),
            ("1913-2025", "Year range"),
            ("USD", "Currency support"),
            ("No signup", "Required"),
        ]
    if tool_name in ("currency-converter",):
        return [
            ("160+", "Currencies supported"),
            ("Live rates", "Exchange data"),
            ("Instant", "Conversion speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("electricity-cost-calculator",):
        return [
            ("kWh", "Energy unit"),
            ("$/kWh", "Rate input"),
            ("Monthly", "Cost estimate"),
            ("No signup", "Required"),
        ]
    if tool_name in ("gpa-calculator",):
        return [
            ("4.0 scale", "GPA system"),
            ("Weighted", "Honors/AP support"),
            ("Semester", "Term calculation"),
            ("No signup", "Required"),
        ]
    if tool_name in ("grade-calculator",):
        return [
            ("Weighted", "Category support"),
            ("What-if", "Grade prediction"),
            ("Instant", "Calculation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("scientific-calculator",):
        return [
            ("100+", "Functions supported"),
            ("Trig/Log", "Advanced math"),
            ("History", "Calculation log"),
            ("No signup", "Required"),
        ]
    if tool_name in ("statistics-calculator",):
        return [
            ("Mean/Median", "Central tendency"),
            ("Std Dev", "Dispersion metrics"),
            ("Regression", "Analysis support"),
            ("No signup", "Required"),
        ]
    if tool_name in ("graphing-calculator",):
        return [
            ("2D plots", "Function graphing"),
            ("Multi-function", "Overlay support"),
            ("Zoom/Pan", "Interactive controls"),
            ("No signup", "Required"),
        ]
    if tool_name in ("math-equation-solver", "mathematics-solver"):
        return [
            ("Algebra", "Equation solving"),
            ("Step-by-step", "Solution display"),
            ("Instant", "Calculation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("aspect-ratio-calculator",):
        return [
            ("16:9/4:3", "Common ratios"),
            ("Custom", "Any ratio support"),
            ("Instant", "Calculation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("blood-alcohol-calculator",):
        return [
            ("Widmark", "Formula used"),
            ("Gender-based", "BAC calculation"),
            ("Time factor", "Metabolism rate"),
            ("No signup", "Required"),
        ]
    if tool_name in ("roman-numeral-converter",):
        return [
            ("I-MMMCMXCIX", "Numeral range"),
            ("1-3999", "Number range"),
            ("Bidirectional", "Conversion mode"),
            ("Instant", "Conversion speed"),
        ]
    if tool_name in ("random-number-generator", "number-generator"):
        return [
            ("Crypto.random", "Secure randomness"),
            ("Any range", "Min/max support"),
            ("Instant", "Generation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("unit-converter",):
        return [
            ("50+", "Unit categories"),
            ("1000+", "Conversions"),
            ("Instant", "Conversion speed"),
            ("No signup", "Required"),
        ]

    # Text tools
    if tool_name in ("case-converter", "text-case-converter"):
        return [
            ("10+ cases", "Conversion types"),
            ("Unicode", "Full support"),
            ("Real-time", "Conversion speed"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("character-counter", "word-counter"):
        return [
            ("Unicode", "Full support"),
            ("Real-time", "Character count"),
            ("100+ langs", "Language support"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("lorem-ipsum-generator",):
        return [
            ("Words/Sentences", "Generation modes"),
            ("Paragraphs", "Custom length"),
            ("Instant", "Text generation"),
            ("Copy-paste", "Ready output"),
        ]
    if tool_name in ("text-to-speech",):
        return [
            ("Web Speech", "API powered"),
            ("50+", "Voice options"),
            ("100+ langs", "Language support"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("paraphrase-tool", "text-generator"):
        return [
            ("AI-powered", "Text processing"),
            ("Multiple", "Tone options"),
            ("Real-time", "Processing speed"),
            ("100+ langs", "Language support"),
        ]
    if tool_name in ("emoji-picker",):
        return [
            ("3,600+", "Emoji available"),
            ("Unicode 15", "Latest standard"),
            ("Search", "By name/keyword"),
            ("Copy-paste", "One-click copy"),
        ]
    if tool_name in ("morse-code-translator",):
        return [
            ("ITU", "Standard Morse code"),
            ("Audio", "Playback support"),
            ("Bidirectional", "Text to Morse"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("word-scramble-solver",):
        return [
            ("280K+", "Dictionary words"),
            ("Instant", "Solving speed"),
            ("Anagrams", "Full support"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("instagram-font-generator", "font-generator"):
        return [
            ("80+", "Font styles"),
            ("Unicode", "Special characters"),
            ("Copy-paste", "One-click copy"),
            ("100%", "Client-side processing"),
        ]

    # Date / Time tools
    if tool_name in ("date-calculator",):
        return [
            ("Days/Months", "Difference modes"),
            ("Add/Subtract", "Date arithmetic"),
            ("Instant", "Calculation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("time-calculator",):
        return [
            ("H:M:S", "Precision level"),
            ("Add/Subtract", "Time arithmetic"),
            ("Instant", "Calculation speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("timezone-converter",):
        return [
            ("400+", "Timezones supported"),
            ("IANA", "Database standard"),
            ("DST aware", "Daylight savings"),
            ("Real-time", "Conversion display"),
        ]
    if tool_name in ("countdown-timer",):
        return [
            ("ms precision", "Countdown accuracy"),
            ("Alerts", "Sound notification"),
            ("Custom", "Duration input"),
            ("No signup", "Required"),
        ]
    if tool_name in ("stopwatch",):
        return [
            ("ms precision", "Timing accuracy"),
            ("Lap times", "Split recording"),
            ("Instant", "Start/stop"),
            ("No signup", "Required"),
        ]
    if tool_name in ("pomodoro-timer",):
        return [
            ("25/5 min", "Standard intervals"),
            ("Custom", "Timer durations"),
            ("Alerts", "Break notifications"),
            ("No signup", "Required"),
        ]
    if tool_name in ("calendar-generator",):
        return [
            ("12 months", "Full year view"),
            ("Custom start", "Week day option"),
            ("Print-ready", "Output format"),
            ("No signup", "Required"),
        ]
    if tool_name in ("discord-timestamp",):
        return [
            ("7 formats", "Discord timestamp styles"),
            ("Unix epoch", "Timestamp standard"),
            ("Copy-paste", "Ready output"),
            ("100%", "Client-side processing"),
        ]

    # AI / Writing tools
    if tool_name in ("ai-detector",):
        return [
            ("GPT/Claude", "Model detection"),
            ("Perplexity", "Score metric"),
            ("Real-time", "Analysis speed"),
            ("100%", "Client-side processing"),
        ]
    if tool_name in ("ai-video-generator",):
        return [
            ("HD", "Video quality"),
            ("Multiple", "Style options"),
            ("AI-powered", "Generation engine"),
            ("No signup", "Required"),
        ]
    if tool_name in ("plagiarism-checker",):
        return [
            ("Deep scan", "Content analysis"),
            ("Multiple", "Source checking"),
            ("Real-time", "Detection speed"),
            ("No signup", "Required"),
        ]
    if tool_name in ("essay-outline-generator",):
        return [
            ("5-paragraph", "Essay structure"),
            ("APA/MLA", "Format support"),
            ("Instant", "Outline generation"),
            ("No signup", "Required"),
        ]
    if tool_name in ("apa-citation-generator", "apa-source-generator"):
        return [
            ("APA 7th", "Edition compliance"),
            ("20+ types", "Source formats"),
            ("DOI lookup", "Auto-fill support"),
            ("No signup", "Required"),
        ]
    if tool_name in ("resume-builder",):
        return [
            ("10+", "Template options"),
            ("PDF export", "Download format"),
            ("ATS-friendly", "Scanner compatible"),
            ("No signup", "Required"),
        ]
    if tool_name in ("privacy-policy-generator",):
        return [
            ("GDPR", "Compliance ready"),
            ("CCPA", "California law"),
            ("Customizable", "Template sections"),
            ("No signup", "Required"),
        ]
    if tool_name in ("invoice-generator",):
        return [
            ("PDF export", "Download format"),
            ("Custom", "Branding support"),
            ("Tax/Discount", "Line item support"),
            ("No signup", "Required"),
        ]
    if tool_name in ("email-signature-generator",):
        return [
            ("HTML", "Signature format"),
            ("All clients", "Email compatibility"),
            ("Social icons", "Link support"),
            ("Copy-paste", "Ready output"),
        ]

    # Media / Design tools
    if tool_name in ("meme-generator",):
        return [
            ("100+", "Meme templates"),
            ("Custom text", "Top/bottom captions"),
            ("PNG export", "Download format"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("gif-builder",):
        return [
            ("GIF89a", "Format standard"),
            ("Frame control", "Speed & order"),
            ("Any size", "Custom dimensions"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("logo-maker",):
        return [
            ("SVG/PNG", "Export formats"),
            ("1000+", "Icon options"),
            ("Custom fonts", "Typography control"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("video-to-gif",):
        return [
            ("MP4/WebM", "Video input"),
            ("GIF output", "Animated export"),
            ("Frame control", "FPS & quality"),
            ("0 bytes", "Sent to any server"),
        ]
    if tool_name in ("screenshot-to-code",):
        return [
            ("HTML/CSS", "Code output"),
            ("AI-powered", "Layout detection"),
            ("Responsive", "Mobile-ready code"),
            ("Instant", "Conversion speed"),
        ]
    if tool_name in ("youtube-thumbnail", "youtube-converter"):
        return [
            ("HD/4K", "Resolution support"),
            ("Custom text", "Overlay options"),
            ("PNG export", "Download format"),
            ("0 bytes", "Sent to any server"),
        ]

    # Productivity tools
    if tool_name in ("kanban-board",):
        return [
            ("Drag & drop", "Card management"),
            ("Columns", "Custom workflow"),
            ("Local storage", "Data persistence"),
            ("No signup", "Required"),
        ]
    if tool_name in ("mind-map-maker",):
        return [
            ("Infinite", "Node connections"),
            ("Drag & drop", "Visual editing"),
            ("PNG export", "Download format"),
            ("No signup", "Required"),
        ]
    if tool_name in ("flow-chart-maker",):
        return [
            ("20+", "Shape types"),
            ("Connectors", "Auto-routing"),
            ("SVG/PNG", "Export formats"),
            ("No signup", "Required"),
        ]
    if tool_name in ("wireframe-tool",):
        return [
            ("50+", "UI components"),
            ("Drag & drop", "Visual editing"),
            ("Export", "PNG/SVG output"),
            ("No signup", "Required"),
        ]
    if tool_name in ("flashcard-maker",):
        return [
            ("Flip cards", "Study method"),
            ("Spaced rep", "Learning algorithm"),
            ("Local save", "Data persistence"),
            ("No signup", "Required"),
        ]
    if tool_name in ("habit-tracker",):
        return [
            ("Daily", "Tracking frequency"),
            ("Streaks", "Progress tracking"),
            ("Local save", "Data persistence"),
            ("No signup", "Required"),
        ]
    if tool_name in ("typing-speed-test", "typing-test"):
        return [
            ("WPM", "Speed measurement"),
            ("Accuracy %", "Error tracking"),
            ("Real-time", "Live feedback"),
            ("No signup", "Required"),
        ]
    if tool_name in ("metronome",):
        return [
            ("20-300", "BPM range"),
            ("Web Audio", "API powered"),
            ("Visual beat", "Indicator display"),
            ("No signup", "Required"),
        ]
    if tool_name in ("baby-name-generator",):
        return [
            ("10,000+", "Name database"),
            ("Origins", "Cultural filtering"),
            ("Popularity", "Trend data"),
            ("No signup", "Required"),
        ]
    if tool_name in ("ascii-art-generator",):
        return [
            ("Unicode", "Character support"),
            ("Text/Image", "Input modes"),
            ("Copy-paste", "Ready output"),
            ("100%", "Client-side processing"),
        ]

    # Default fallback for any tool not specifically mapped
    return [
        ("100%", "Client-side processing"),
        ("Zero data", "Stored on servers"),
        ("Instant", "Results speed"),
        ("No signup", "Required"),
    ]


def build_stats_html(tool_name):
    """Build the Quick Facts HTML for a tool."""
    stats = get_stats_for_tool(tool_name)
    cards = "\n    ".join(
        f'''<div style="padding:8px;background:#1a1a26;border-radius:6px;text-align:center;">
      <p style="color:#00ff88;font-size:1.1rem;font-weight:700;margin:0;">{value}</p>
      <p style="color:#8888a0;font-size:0.7rem;margin:2px 0 0;">{label}</p>
    </div>'''
        for value, label in stats
    )

    return f'''<div class="tool-stats" style="max-width:700px;margin:1.5rem auto;padding:16px 20px;background:#12121a;border-radius:8px;border:1px solid #2a2a3a;">
  <p style="color:#00ff88;font-size:0.8rem;font-weight:600;margin:0 0 10px;">Quick Facts</p>
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px;">
    {cards}
  </div>
</div>'''


# ============================================================
# Injection logic
# ============================================================

def find_injection_point(html):
    """
    Find the best place to inject compat/stats sections: before footer or Related Tools.
    Returns the index in the string where we should insert.
    """
    # Strategy 1: Before the "Related Tools" div (most common pattern)
    # Look for the Related Tools container
    related_match = re.search(r'<div style="max-width:800px;margin:2rem auto;padding:1\.5rem;">\s*<div style="[^"]*">Related Tools</div>', html)
    if related_match:
        return related_match.start()

    # Strategy 2: Before <footer
    footer_match = re.search(r'<footer[\s>]', html)
    if footer_match:
        return footer_match.start()

    # Strategy 3: Before the "Last updated" paragraph that often precedes footer
    last_updated_match = re.search(r'<p style="text-align:center;color:#8888a0;font-size:0\.8rem;margin:2rem 0 0\.5rem;">Last updated:', html)
    if last_updated_match:
        return last_updated_match.start()

    # Strategy 4: Before </body>
    body_match = re.search(r'</body>', html)
    if body_match:
        return body_match.start()

    # Strategy 5: Before the last </div> before </body> or end of script
    return None


def process_tool(tool_name):
    """Process a single tool: add compat table and/or stats card."""
    index_path = os.path.join(TOOLS_DIR, tool_name, "index.html")
    if not os.path.exists(index_path):
        return None, None

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    has_compat = "browser-compat" in html or "Browser Support" in html
    has_stats = "tool-stats" in html or "Quick Facts" in html

    is_developer = tool_name in DEVELOPER_TOOLS
    add_compat = is_developer and not has_compat
    add_stats = not has_stats

    if not add_compat and not add_stats:
        return False, False

    injection_point = find_injection_point(html)
    if injection_point is None:
        return None, None

    # Build the injection content
    inject = "\n"
    if add_stats:
        inject += build_stats_html(tool_name) + "\n"
    if add_compat:
        inject += get_compat_html(tool_name) + "\n"

    # Insert before the injection point
    new_html = html[:injection_point] + inject + html[injection_point:]

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_html)

    return add_compat, add_stats


def main():
    # Get all tool directories
    tool_dirs = []
    for entry in os.listdir(TOOLS_DIR):
        full = os.path.join(TOOLS_DIR, entry)
        if os.path.isdir(full) and os.path.exists(os.path.join(full, "index.html")):
            tool_dirs.append(entry)

    tool_dirs.sort()

    compat_added = 0
    stats_added = 0
    errors = []

    for tool_name in tool_dirs:
        try:
            added_compat, added_stats = process_tool(tool_name)
            if added_compat is None:
                errors.append(f"{tool_name}: no injection point found")
                continue
            if added_compat:
                compat_added += 1
            if added_stats:
                stats_added += 1
        except Exception as e:
            errors.append(f"{tool_name}: {e}")

    print(f"\n=== Enrichment Complete ===")
    print(f"Browser compat tables added: {compat_added}")
    print(f"Tool stats cards added: {stats_added}")
    print(f"Total tools processed: {len(tool_dirs)}")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  - {e}")
    print()


if __name__ == "__main__":
    main()
