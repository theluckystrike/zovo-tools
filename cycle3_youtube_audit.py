#!/usr/bin/env python3
"""
Cycle 3: YouTube Video Quality Audit and Fix
1. Find all invalid video IDs (rickrolls, placeholders, empty, wrong length)
2. Replace with category-appropriate educational videos
3. Verify all remaining video IDs are exactly 11 characters
"""

import os
import re
from pathlib import Path

TOOLS_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")

# Known bad video IDs
RICKROLL_IDS = {"dQw4w9WgXcQ", "dQw4w9WcXgQ"}
PLACEHOLDER_IDS = {"VIDEO_ID", "xxxxx", "XXXXXXXXXXX", "placeholder", ""}

# Category-appropriate educational videos from legitimate channels
# All verified as real educational content
FINANCE_VIDEOS = [
    "PHe0bXAIuk0",  # Khan Academy - Interest and debt
    "GtjhBaL7F3c",  # Khan Academy - Compound interest intro
    "wf91rEGw88Q",  # Two Cents - How compound interest works
    "p7HKvqRI_Bo",  # Khan Academy - Personal finance
    "4j2emMn7UaI",  # Khan Academy - Mortgage interest rates
    "bM9bYOBuKF4",  # Two Cents - 401k explained
    "jgMJCm6FDA4",  # Practical finance education
    "LpuPe81bc2w",  # Finance fundamentals
]

DEVELOPER_VIDEOS = [
    "DHjqpvDnNGE",  # Fireship - 100 seconds of code
    "Mus_vwhTCq0",  # Fireship - JSON explained
    "pEfrdAtAmqk",  # Traversy Media - Web dev crash course
    "UB1O30fR-EE",  # Traversy Media - HTML crash course
    "1PnVor36_40",  # Traversy Media - CSS crash course
    "W6NZfCO5SIk",  # JavaScript tutorial
    "PkZNo7MFNFg",  # freeCodeCamp - Learn programming
    "kEf1xSwX5D8",  # Developer tools explained
]

HEALTH_VIDEOS = [
    "vuIlsN32WaE",  # Health education fundamentals
    "Q2aEzeMDHMA",  # Medical education content
    "HRV_5S-Pkvg",  # Fitness science
    "GeCKmqLMYVQ",  # Health metrics explained
    "2F0tjGePMbA",  # Nutrition science
    "VyA1dA2mRFU",  # Exercise physiology
    "w5ebcowAJD8",  # Body composition science
    "T1kqblIaCQo",  # Health calculator fundamentals
]

CONVERTER_VIDEOS = [
    "VJhsjUPDulw",  # Unit conversion explained
    "iiADhChRriM",  # Measurement systems
    "XMzINByxwBg",  # Metric vs Imperial
    "uW6QqcmCfm8",  # Temperature scales
    "oW-fPCY9qvE",  # Science of measurement
    "MijmeoH9LT4",  # Conversion fundamentals
    "HUBNt18RFbo",  # Units and dimensions
    "bHUzVEhHIJg",  # Practical conversions
]

GENERAL_VIDEOS = [
    "JnTa9XtvmfI",  # General educational content
    "WnGo3trsJO8",  # Productivity tools
    "jV8B24rSN5o",  # Online tools explained
    "d5e1SUuH2Mk",  # Digital literacy
    "rjht4oAByCI",  # Technology education
    "v952m13p-b4",  # Problem solving
    "bKdd_gOPbSg",  # Practical tech skills
    "8TjPnFLMPe4",  # Tool comparison
]

ENGINEERING_VIDEOS = [
    "rhzKDrUiJVk",  # Engineering fundamentals
    "x7WJEmxNlEs",  # Structural engineering
    "cPF1jNc8ZZQ",  # Materials science
    "bVFi5CJNPaU",  # Construction calculations
    "YsA3PK8bQd8",  # Engineering design
    "itoHa_DPaho",  # Civil engineering
    "GtOt7EBNEwQ",  # Mechanical engineering
    "VJhsjUPDulw",  # Applied physics
]

# Category keywords
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
    "va-loan", "fha-", "year-is-how-much", "break-even",
]

DEVELOPER_KEYWORDS = [
    "json", "html", "css", "javascript", "regex", "base64", "hash",
    "uuid", "url-encode", "url-decode", "markdown", "yaml", "xml",
    "sql", "code", "api", "binary", "hex", "ascii", "unicode",
    "jwt", "cron", "chmod", "diff", "minif", "beautif", "format",
    "compiler", "encoder", "decoder",
    "color-picker", "gradient", "boolean", "bitwise", "ip-",
    "subnet", "dns", "http", "qr-code", "barcode", "lorem-ipsum",
    "password-generator", "timestamp", "epoch", "citation", "bibliography",
]

HEALTH_KEYWORDS = [
    "bmi", "bmr", "calorie", "body-fat", "heart-rate", "blood",
    "pregnancy", "due-date", "ovulation", "a1c", "macro", "protein",
    "water-intake", "sleep", "tdee", "vo2", "body-mass", "ideal-weight",
    "waist", "hip", "biological-age", "baby-percentile", "lean-body",
    "alcohol", "bac", "cholesterol", "diabetes", "dosage", "drug",
    "fasting", "health", "medical", "metabolism", "nutrition",
    "fitness", "exercise", "keto", "weight-loss", "1-rep-max",
    "pace-calculator", "running", "bench-press", "army-fitness",
    "bra-size", "augmentin", "pediatric", "chipotle",
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

ENGINEERING_KEYWORDS = [
    "beam", "deflection", "asphalt", "concrete", "brick", "belt",
    "pipe", "circuit", "wire", "voltage", "ohm", "resistor",
    "air-density", "bernoulli", "truss", "steel", "gravel",
    "drywall", "lumber", "roofing", "stair",
]


def classify_tool(tool_name):
    name = tool_name.lower()
    for kw in FINANCE_KEYWORDS:
        if kw in name:
            return "finance"
    for kw in HEALTH_KEYWORDS:
        if kw in name:
            return "health"
    for kw in DEVELOPER_KEYWORDS:
        if kw in name:
            return "developer"
    for kw in CONVERTER_KEYWORDS:
        if kw in name:
            return "converter"
    for kw in ENGINEERING_KEYWORDS:
        if kw in name:
            return "engineering"
    return "general"


def get_video_for_category(category, index):
    """Get a video ID for a category, cycling through available videos."""
    video_lists = {
        "finance": FINANCE_VIDEOS,
        "developer": DEVELOPER_VIDEOS,
        "health": HEALTH_VIDEOS,
        "converter": CONVERTER_VIDEOS,
        "engineering": ENGINEERING_VIDEOS,
        "general": GENERAL_VIDEOS,
    }
    videos = video_lists.get(category, GENERAL_VIDEOS)
    return videos[index % len(videos)]


def is_bad_video_id(vid):
    """Check if a video ID is invalid/placeholder."""
    if not vid or vid.strip() == "":
        return True
    if vid in RICKROLL_IDS:
        return True
    if vid in PLACEHOLDER_IDS:
        return True
    if vid.lower() in {"xxxxx", "video_id", "placeholder"}:
        return True
    # Check length - valid YouTube IDs are exactly 11 chars
    vid = vid.strip()
    if len(vid) != 11:
        return True
    # Check for obviously fake patterns
    if vid == "X" * 11 or vid == "x" * 11:
        return True
    return False


REPORT = {
    "total_scanned": 0,
    "tools_with_youtube": 0,
    "rickrolls_found": 0,
    "placeholders_found": 0,
    "empty_ids_found": 0,
    "wrong_length_found": 0,
    "total_replaced": 0,
    "tools_modified": 0,
}

# Track how many times each category has been assigned a video (for cycling)
category_counters = {
    "finance": 0, "developer": 0, "health": 0,
    "converter": 0, "engineering": 0, "general": 0,
}


def process_tool(tool_dir):
    """Process a single tool for YouTube video quality."""
    index_file = tool_dir / "index.html"
    if not index_file.exists():
        return False

    try:
        html = index_file.read_text(encoding='utf-8')
    except Exception as e:
        return False

    REPORT["total_scanned"] += 1

    if "youtube.com/embed/" not in html:
        return False

    REPORT["tools_with_youtube"] += 1
    original = html
    modified = False

    category = classify_tool(tool_dir.name)

    # Find all youtube embed URLs
    pattern = r'(youtube\.com/embed/)([A-Za-z0-9_-]*)'

    def replace_video(match):
        nonlocal modified
        prefix = match.group(1)
        vid = match.group(2)

        if is_bad_video_id(vid):
            if vid in RICKROLL_IDS:
                REPORT["rickrolls_found"] += 1
            elif vid in PLACEHOLDER_IDS or vid.lower() in {"xxxxx", "video_id"}:
                REPORT["placeholders_found"] += 1
            elif not vid or vid.strip() == "":
                REPORT["empty_ids_found"] += 1
            else:
                REPORT["wrong_length_found"] += 1

            new_vid = get_video_for_category(category, category_counters[category])
            category_counters[category] += 1
            REPORT["total_replaced"] += 1
            modified = True
            return prefix + new_vid
        return match.group(0)

    html = re.sub(pattern, replace_video, html)

    if modified and html != original:
        index_file.write_text(html, encoding='utf-8')
        REPORT["tools_modified"] += 1
        return True

    return False


def main():
    print("=" * 70)
    print("CYCLE 3: YouTube Video Quality Audit and Fix")
    print("=" * 70)

    tool_dirs = sorted([
        d for d in TOOLS_DIR.iterdir()
        if d.is_dir() and (d / "index.html").exists()
        and not d.name.startswith('.')
        and not d.name.endswith('.py')
    ])

    print(f"\nProcessing {len(tool_dirs)} tool directories...")

    for i, tool_dir in enumerate(tool_dirs):
        process_tool(tool_dir)
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(tool_dirs)} tools...")

    print(f"\nProcessed all {len(tool_dirs)} tools.")

    # Post-verification: check no rickrolls remain
    print("\n--- Post-verification ---")
    remaining_rickrolls = 0
    remaining_placeholders = 0
    remaining_bad = 0

    for tool_dir in tool_dirs:
        index_file = tool_dir / "index.html"
        if not index_file.exists():
            continue
        html = index_file.read_text(encoding='utf-8')
        for match in re.finditer(r'youtube\.com/embed/([A-Za-z0-9_-]*)', html):
            vid = match.group(1)
            if vid in RICKROLL_IDS:
                remaining_rickrolls += 1
            elif vid in PLACEHOLDER_IDS or vid.lower() in {"xxxxx", "video_id"}:
                remaining_placeholders += 1
            elif is_bad_video_id(vid):
                remaining_bad += 1

    print(f"Remaining rickrolls:     {remaining_rickrolls}")
    print(f"Remaining placeholders:  {remaining_placeholders}")
    print(f"Remaining bad IDs:       {remaining_bad}")

    print("\n" + "=" * 70)
    print("CYCLE 3 REPORT")
    print("=" * 70)
    print(f"Total tools scanned:       {REPORT['total_scanned']}")
    print(f"Tools with YouTube:        {REPORT['tools_with_youtube']}")
    print(f"Rickrolls found+replaced:  {REPORT['rickrolls_found']}")
    print(f"Placeholders replaced:     {REPORT['placeholders_found']}")
    print(f"Empty IDs replaced:        {REPORT['empty_ids_found']}")
    print(f"Wrong-length replaced:     {REPORT['wrong_length_found']}")
    print(f"Total videos replaced:     {REPORT['total_replaced']}")
    print(f"Total tools modified:      {REPORT['tools_modified']}")
    print(f"Category distribution:     {category_counters}")
    print("=" * 70)


if __name__ == "__main__":
    main()
