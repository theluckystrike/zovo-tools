#!/usr/bin/env python3
"""
Cycle 1b: Expand badge customization to cover ALL badge patterns across top 100 tools.
The first pass only matched one specific badge-row div pattern.
This handles all variant patterns found in the codebase.
"""

import os
import re
from pathlib import Path

TOOLS_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")

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
    "compiler", "converter-online", "encoder", "decoder", "generator-online",
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


# Already-customized badge text to skip
ALREADY_CUSTOM = ["Finance-Tool", "Dev-Tool", "Health-Tool", "Converter-Tool"]


def get_top_tools():
    tool_sizes = []
    for d in TOOLS_DIR.iterdir():
        if d.is_dir() and (d / "index.html").exists() and not d.name.startswith('.'):
            if d.name.endswith('.py') or d.name.endswith('.md') or d.name.endswith('.json'):
                continue
            try:
                size = (d / "index.html").stat().st_size
                tool_sizes.append((d.name, size))
            except Exception:
                pass
    tool_sizes.sort(key=lambda x: x[1], reverse=True)
    return [t[0] for t in tool_sizes[:100]]


def has_custom_badge(html):
    for tag in ALREADY_CUSTOM:
        if tag in html:
            return True
    return False


def replace_generic_shields_badges(html, category):
    """Replace generic Free-Tool / Free_Tool badges with category-specific ones."""
    modified = False

    # Map of category to badge replacements
    category_map = {
        "finance": {
            "first_badge": ("Finance-Tool", "Finance Tool"),
            "third_badge": ("Accuracy-Verified", "Accuracy Verified"),
        },
        "developer": {
            "first_badge": ("Dev-Tool", "Dev Tool"),
            "third_badge": ("No-Dependencies", "No Dependencies"),
        },
        "health": {
            "first_badge": ("Health-Tool", "Health Tool"),
            "third_badge": ("Privacy-Safe", "Privacy Safe"),
        },
        "converter": {
            "first_badge": ("Converter-Tool", "Converter Tool"),
            "third_badge": ("No%20Signup-Required", "No Signup Required"),
        },
    }

    if category not in category_map:
        return html, False

    cm = category_map[category]

    # Pattern 1: Free-Tool badge
    old_patterns_first = [
        r'(https://img\.shields\.io/badge/)Free-Tool(-00ff88)',
        r'(https://img\.shields\.io/badge/)Free_Tool-No_Login(-00ff88)',
        r'(https://img\.shields\.io/badge/)Free%20Tool-No%20Login(-00ff88)',
        r'(https://img\.shields\.io/badge/)tool-free(-00ff88)',
    ]
    for pat in old_patterns_first:
        new_text = cm["first_badge"][0]
        replacement = rf'\g<1>{new_text}\2'
        new_html = re.sub(pat, replacement, html)
        if new_html != html:
            # Also fix alt text
            html = new_html
            modified = True

    # Pattern for third badge (No Signup -> category specific)
    old_patterns_third = [
        r'(https://img\.shields\.io/badge/)No%20Signup-Required(-6C5CE7)',
    ]
    for pat in old_patterns_third:
        new_text = cm["third_badge"][0]
        replacement = rf'\g<1>{new_text}\2'
        new_html = re.sub(pat, replacement, html)
        if new_html != html:
            html = new_html
            modified = True

    # Fix alt texts to match
    if modified:
        html = html.replace('alt="Free Tool"', f'alt="{cm["first_badge"][1]}"')
        html = html.replace('alt="Free tool no login required"', f'alt="{cm["first_badge"][1]}"')
        html = html.replace('alt="Free Tool - No Login"', f'alt="{cm["first_badge"][1]}"')

    return html, modified


def main():
    print("=" * 70)
    print("CYCLE 1b: Expand Badge Customization")
    print("=" * 70)

    top_tools = get_top_tools()
    top_set = set(top_tools)

    modified_count = 0
    skipped_already_custom = 0

    for tool_name in top_tools:
        tool_dir = TOOLS_DIR / tool_name
        index_file = tool_dir / "index.html"
        if not index_file.exists():
            continue

        html = index_file.read_text(encoding='utf-8')

        if has_custom_badge(html):
            skipped_already_custom += 1
            continue

        category = classify_tool(tool_name)
        if category == "general":
            continue

        html_new, was_modified = replace_generic_shields_badges(html, category)
        if was_modified:
            index_file.write_text(html_new, encoding='utf-8')
            modified_count += 1
            print(f"  Customized: {tool_name} -> {category}")

    print(f"\nAlready customized (skipped): {skipped_already_custom}")
    print(f"Newly customized:            {modified_count}")
    print("=" * 70)


if __name__ == "__main__":
    main()
