#!/usr/bin/env python3
"""
Cycle 1: Badge URL Validation and Fixes
- Fix URL encoding issues (raw spaces -> %20)
- Remove duplicate badge-row divs (keep only the first)
- Customize badge text for top 100 tools by category
"""

import os
import re
import json
from pathlib import Path
from urllib.parse import quote, unquote

TOOLS_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")
REPORT = {
    "total_tools_scanned": 0,
    "tools_with_badges": 0,
    "encoding_issues_fixed": 0,
    "duplicate_badge_rows_removed": 0,
    "tools_with_duplicates": 0,
    "badges_customized": 0,
    "tools_customized": 0,
}

# Category classification for top tools
FINANCE_KEYWORDS = [
    "401k", "529", "mortgage", "loan", "interest", "annuity", "payroll",
    "paycheck", "salary", "tax", "investment", "retirement", "compound",
    "amortization", "apr", "budget", "capital-gain", "cd-", "cost-of-living",
    "credit-card", "crypto", "currency", "debt", "dividend", "down-payment",
    "emi", "equity", "expense", "fica", "finance", "forex", "gold",
    "hourly-to-salary", "income", "inflation", "ira", "lease", "margin",
    "net-worth", "pension", "profit", "real-estate", "rent", "roi",
    "savings", "stock", "tip-calculator", "wage", "pay-raise", "bonus",
    "bank", "heloc", "home-equity", "property-tax", "stamp-duty",
    "social-security", "commission", "car-loan", "auto-loan", "boat-loan",
    "va-loan", "fha-", "year-is-how-much",
]

DEVELOPER_KEYWORDS = [
    "json", "html", "css", "javascript", "regex", "base64", "hash",
    "uuid", "url-encode", "url-decode", "markdown", "yaml", "xml",
    "sql", "code", "api", "binary", "hex", "ascii", "unicode",
    "jwt", "cron", "chmod", "diff", "minif", "beautif", "format",
    "compiler", "converter-online", "encoder", "decoder", "generator",
    "color-picker", "gradient", "boolean", "bitwise", "ip-",
    "subnet", "dns", "http", "qr-code", "barcode", "lorem-ipsum",
    "password-generator", "timestamp", "epoch",
]

HEALTH_KEYWORDS = [
    "bmi", "bmr", "calorie", "body-fat", "heart-rate", "blood",
    "pregnancy", "due-date", "ovulation", "a1c", "macro", "protein",
    "water-intake", "sleep", "tdee", "vo2", "body-mass", "ideal-weight",
    "waist", "hip", "biological-age", "baby-percentile", "lean-body",
    "alcohol", "bac", "cholesterol", "diabetes", "dosage", "drug",
    "fasting", "health", "medical", "metabolism", "nutrition",
    "fitness", "exercise", "keto", "weight-loss", "1-rep-max",
    "pace-calculator", "running",
]

CONVERTER_KEYWORDS = [
    "converter", "conversion", "to-usd", "to-eur", "to-gbp",
    "celsius", "fahrenheit", "kelvin", "meter", "feet", "inch",
    "mile", "kilometer", "pound", "kilogram", "ounce", "gram",
    "liter", "gallon", "acre", "hectare", "square", "cubic",
    "speed", "pressure", "volume", "length", "weight", "mass",
    "temperature", "area", "energy", "power", "force", "torque",
    "frequency", "angle", "density", "flow-rate", "time-zone",
    "roman-numeral", "number-to-words", "fraction", "percentage",
    "decimal-to-binary", "binary-to-decimal", "hex-to-", "octal",
    "unit-", "metric", "imperial",
]


def classify_tool(tool_name):
    """Classify a tool into a category based on its directory name."""
    name = tool_name.lower()
    for kw in FINANCE_KEYWORDS:
        if kw in name:
            return "finance"
    for kw in DEVELOPER_KEYWORDS:
        if kw in name:
            return "developer"
    for kw in HEALTH_KEYWORDS:
        if kw in name:
            return "health"
    for kw in CONVERTER_KEYWORDS:
        if kw in name:
            return "converter"
    return "general"


def get_category_badges(category, tool_name):
    """Get custom badge HTML for a given category."""
    badge_style = 'style="flat-square"'

    if category == "finance":
        return (
            '<div class="badge-row" style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:1rem 0;">\n'
            '<img src="https://img.shields.io/badge/Finance-Tool-00ff88?style=flat-square" alt="Finance Tool" loading="lazy">\n'
            '<img src="https://img.shields.io/badge/Updated-March%202026-00ccff?style=flat-square" alt="Updated March 2026" loading="lazy">\n'
            '<img src="https://img.shields.io/badge/Accuracy-Verified-6C5CE7?style=flat-square" alt="Accuracy Verified" loading="lazy">\n'
            '</div>'
        )
    elif category == "developer":
        return (
            '<div class="badge-row" style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:1rem 0;">\n'
            '<img src="https://img.shields.io/badge/Dev-Tool-00ff88?style=flat-square" alt="Dev Tool" loading="lazy">\n'
            '<img src="https://img.shields.io/badge/Open%20Source-Free-00ccff?style=flat-square" alt="Open Source Free" loading="lazy">\n'
            '<img src="https://img.shields.io/badge/No-Dependencies-6C5CE7?style=flat-square" alt="No Dependencies" loading="lazy">\n'
            '</div>'
        )
    elif category == "health":
        return (
            '<div class="badge-row" style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:1rem 0;">\n'
            '<img src="https://img.shields.io/badge/Health-Tool-00ff88?style=flat-square" alt="Health Tool" loading="lazy">\n'
            '<img src="https://img.shields.io/badge/Evidence%20Based-Formulas-00ccff?style=flat-square" alt="Evidence Based" loading="lazy">\n'
            '<img src="https://img.shields.io/badge/Privacy-Safe-6C5CE7?style=flat-square" alt="Privacy Safe" loading="lazy">\n'
            '</div>'
        )
    elif category == "converter":
        return (
            '<div class="badge-row" style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:1rem 0;">\n'
            '<img src="https://img.shields.io/badge/Converter-Tool-00ff88?style=flat-square" alt="Converter Tool" loading="lazy">\n'
            '<img src="https://img.shields.io/badge/Instant-Results-00ccff?style=flat-square" alt="Instant Results" loading="lazy">\n'
            '<img src="https://img.shields.io/badge/No%20Signup-Required-6C5CE7?style=flat-square" alt="No Signup Required" loading="lazy">\n'
            '</div>'
        )
    else:
        return (
            '<div class="badge-row" style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:1rem 0;">\n'
            '<img src="https://img.shields.io/badge/Free-Tool-00ff88?style=flat-square" alt="Free Tool" loading="lazy">\n'
            '<img src="https://img.shields.io/badge/Updated-March%202026-00ccff?style=flat-square" alt="Updated March 2026" loading="lazy">\n'
            '<img src="https://img.shields.io/badge/No%20Signup-Required-6C5CE7?style=flat-square" alt="No Signup Required" loading="lazy">\n'
            '</div>'
        )


def fix_badge_url_encoding(html):
    """Fix any shields.io badge URLs that have raw spaces instead of %20."""
    fixed_count = 0

    def fix_shield_url(match):
        nonlocal fixed_count
        url = match.group(0)
        # Check for raw spaces in the URL path (between src=" and next ")
        if ' ' in url and 'img.shields.io' in url:
            # Only fix spaces in the badge path portion
            parts = url.split('?')
            path = parts[0]
            if ' ' in path:
                new_path = path.replace(' ', '%20')
                fixed_count += 1
                return new_path + ('?' + parts[1] if len(parts) > 1 else '')
        return url

    # Find all shields.io URLs
    pattern = r'https://img\.shields\.io/badge/[^"\'>\s]*(?:\s[^"\'>\s]*)*'
    result = re.sub(pattern, fix_shield_url, html)
    return result, fixed_count


def remove_duplicate_badge_rows(html):
    """Keep only the first badge-row div, remove subsequent ones."""
    # Find all badge-row div blocks
    # Pattern: <div class="badge-row" ...>...</div>
    pattern = r'<div\s+class="badge-row"[^>]*>.*?</div>'
    matches = list(re.finditer(pattern, html, re.DOTALL))

    if len(matches) <= 1:
        return html, 0

    removed = 0
    # Remove from last to first to preserve indices
    for match in reversed(matches[1:]):
        # Also remove any trailing newline
        end = match.end()
        if end < len(html) and html[end] == '\n':
            end += 1
        html = html[:match.start()] + html[end:]
        removed += 1

    return html, removed


def get_top_tools():
    """Get top 100 tools by directory size."""
    tool_sizes = []
    for d in TOOLS_DIR.iterdir():
        if d.is_dir() and (d / "index.html").exists() and not d.name.startswith('.'):
            # Skip non-tool directories
            if d.name.endswith('.py') or d.name.endswith('.md') or d.name.endswith('.json'):
                continue
            try:
                size = (d / "index.html").stat().st_size
                tool_sizes.append((d.name, size))
            except Exception:
                pass

    tool_sizes.sort(key=lambda x: x[1], reverse=True)
    return [t[0] for t in tool_sizes[:100]]


def process_tool(tool_dir, is_top_tool=False):
    """Process a single tool's index.html."""
    index_file = tool_dir / "index.html"
    if not index_file.exists():
        return False

    try:
        html = index_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  Error reading {tool_dir.name}: {e}")
        return False

    original = html
    modified = False

    REPORT["total_tools_scanned"] += 1

    # Check if has badges
    if "badge-row" in html or "img.shields.io" in html:
        REPORT["tools_with_badges"] += 1

    # 1. Fix URL encoding
    html, enc_fixes = fix_badge_url_encoding(html)
    if enc_fixes > 0:
        REPORT["encoding_issues_fixed"] += enc_fixes
        modified = True

    # 2. Remove duplicate badge-row divs
    html, dups_removed = remove_duplicate_badge_rows(html)
    if dups_removed > 0:
        REPORT["duplicate_badge_rows_removed"] += dups_removed
        REPORT["tools_with_duplicates"] += 1
        modified = True

    # 3. Customize badges for top tools
    if is_top_tool:
        category = classify_tool(tool_dir.name)
        new_badges = get_category_badges(category, tool_dir.name)

        # Find and replace the first badge-row div
        badge_pattern = r'<div\s+class="badge-row"[^>]*>.*?</div>'
        match = re.search(badge_pattern, html, re.DOTALL)
        if match:
            old_badges = match.group(0)
            if old_badges != new_badges:
                html = html[:match.start()] + new_badges + html[match.end():]
                REPORT["badges_customized"] += 1
                REPORT["tools_customized"] += 1
                modified = True

    if modified and html != original:
        index_file.write_text(html, encoding='utf-8')
        return True

    return False


def main():
    print("=" * 70)
    print("CYCLE 1: Badge URL Validation and Fixes")
    print("=" * 70)

    # Get top 100 tools
    top_tools = get_top_tools()
    top_set = set(top_tools)
    print(f"\nIdentified {len(top_tools)} top tools for customization")

    # Show category breakdown for top tools
    cat_counts = {"finance": 0, "developer": 0, "health": 0, "converter": 0, "general": 0}
    for t in top_tools:
        cat = classify_tool(t)
        cat_counts[cat] += 1
    print(f"Category breakdown: {json.dumps(cat_counts, indent=2)}")

    # Process all tools
    tools_modified = 0
    tool_dirs = sorted([
        d for d in TOOLS_DIR.iterdir()
        if d.is_dir() and (d / "index.html").exists()
        and not d.name.startswith('.')
        and not d.name.endswith('.py')
    ])

    print(f"\nProcessing {len(tool_dirs)} tool directories...")

    for i, tool_dir in enumerate(tool_dirs):
        is_top = tool_dir.name in top_set
        if process_tool(tool_dir, is_top_tool=is_top):
            tools_modified += 1

        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(tool_dirs)} tools...")

    print(f"\nProcessed all {len(tool_dirs)} tools.")

    # Final report
    print("\n" + "=" * 70)
    print("CYCLE 1 REPORT")
    print("=" * 70)
    print(f"Total tools scanned:         {REPORT['total_tools_scanned']}")
    print(f"Tools with badges:           {REPORT['tools_with_badges']}")
    print(f"Encoding issues fixed:       {REPORT['encoding_issues_fixed']}")
    print(f"Tools with duplicate rows:   {REPORT['tools_with_duplicates']}")
    print(f"Duplicate rows removed:      {REPORT['duplicate_badge_rows_removed']}")
    print(f"Tools customized (top 100):  {REPORT['tools_customized']}")
    print(f"Total badges customized:     {REPORT['badges_customized']}")
    print(f"Total tools modified:        {tools_modified}")
    print("=" * 70)


if __name__ == "__main__":
    main()
