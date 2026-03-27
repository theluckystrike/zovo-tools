#!/usr/bin/env python3
"""
Wikipedia Reference Audit for Zovo Tools
Cycle 1: Extract, validate, and categorize all Wikipedia links
"""

import os
import re
import json
from collections import Counter, defaultdict
from pathlib import Path

TOOLS_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")
REPORT_FILE = TOOLS_DIR / "wiki-audit-report.json"

# Pattern to match Wikipedia URLs
WIKI_URL_PATTERN = re.compile(r'https?://[a-z]*\.?wikipedia\.org/wiki/([^\s"<>\']+)')

# Pattern to match wiki-definition sections (grab definition text)
WIKI_DEF_PATTERN = re.compile(
    r'class="wiki-definition"[^>]*>'
    r'.*?<p[^>]*>Wikipedia</p>'
    r'<p[^>]*>(.*?)</p>'
    r'.*?<a\s+href="(https?://[a-z]*\.?wikipedia\.org/wiki/[^\s"<>\']+)"',
    re.DOTALL
)

def scan_all_tools():
    """Scan all tool directories for Wikipedia references."""
    results = {}
    all_slugs = []
    all_definitions = []
    tools_with_wiki = 0
    tools_without_wiki = 0

    tool_dirs = sorted([
        d for d in TOOLS_DIR.iterdir()
        if d.is_dir() and not d.name.startswith('.') and not d.name.startswith('_')
        and not d.name.startswith('AGENT') and not d.name.startswith('node_modules')
        and (d / "index.html").exists()
    ])

    print(f"Scanning {len(tool_dirs)} tool directories...")

    for tool_dir in tool_dirs:
        index_file = tool_dir / "index.html"
        try:
            content = index_file.read_text(encoding='utf-8', errors='replace')
        except Exception as e:
            print(f"  ERROR reading {tool_dir.name}: {e}")
            continue

        # Extract all Wikipedia URLs
        wiki_urls = WIKI_URL_PATTERN.findall(content)

        # Extract wiki-definition text
        def_matches = WIKI_DEF_PATTERN.findall(content)

        if wiki_urls:
            tools_with_wiki += 1
            # Clean slugs (remove trailing punctuation, anchors)
            cleaned_slugs = []
            for slug in wiki_urls:
                slug = slug.rstrip('.,;:)')
                if '#' in slug:
                    slug = slug.split('#')[0]
                cleaned_slugs.append(slug)

            results[tool_dir.name] = {
                "slugs": cleaned_slugs,
                "definitions": [m[0] for m in def_matches] if def_matches else [],
                "def_urls": [m[1] for m in def_matches] if def_matches else [],
            }
            all_slugs.extend(cleaned_slugs)

            if def_matches:
                for defn in def_matches:
                    all_definitions.append({
                        "tool": tool_dir.name,
                        "definition": defn[0],
                        "url": defn[1]
                    })
        else:
            tools_without_wiki += 1

    return results, all_slugs, all_definitions, tools_with_wiki, tools_without_wiki, len(tool_dirs)


def classify_slugs(all_slugs, results):
    """Classify Wikipedia slugs as likely real or fabricated."""
    slug_counts = Counter(all_slugs)

    fabricated = []
    suspicious = []
    likely_real = []

    for slug, count in slug_counts.most_common():
        reasons = []

        # Check for repeated words: "Calculator_Calculator"
        words = slug.replace('-', '_').split('_')
        word_lower = [w.lower() for w in words]
        if len(word_lower) != len(set(word_lower)):
            reasons.append("repeated_words")

        # Check for tool-name-like slugs (Title_Case compound words that look like tool names)
        # Real Wikipedia articles: "Body_mass_index", "Hash_function"
        # Fake: "Json_Formatter", "Password_Generator", "Bmi_Calculator"
        tool_name_patterns = [
            r'^[A-Z][a-z]*_(?:Calculator|Converter|Generator|Checker|Tester|Formatter|Encoder|Decoder|Validator|Analyzer|Builder|Maker|Solver|Finder|Counter|Timer|Tracker|Planner|Picker|Selector|Scanner|Extractor|Compressor|Decompressor|Minifier|Beautifier|Optimizer|Simulator|Estimator|Ranker|Sorter|Comparator|Inspector|Debugger|Profiler|Monitor|Logger|Viewer|Editor|Manager|Helper|Utility|Tool|App)s?$',
        ]

        for pat in tool_name_patterns:
            if re.match(pat, slug, re.IGNORECASE):
                reasons.append("tool_name_pattern")
                break

        # Check for currency conversion slugs like "Usd_To_Cad", "Pounds_To_Kg"
        if re.match(r'^[A-Z][a-z]*_[Tt]o_[A-Z][a-z]*$', slug):
            reasons.append("conversion_pattern")

        # Check for abbreviation-only slugs (too short to be real)
        if len(slug) <= 3 and slug.isupper():
            reasons.append("abbreviation_only")

        # Check if the slug is a single common word that IS a real Wikipedia article
        # (these are likely OK but we should still verify)

        # Check for underscores in non-standard places
        if slug.endswith('_') or slug.startswith('_'):
            reasons.append("malformed_underscores")

        if reasons:
            fabricated.append({"slug": slug, "count": count, "reasons": reasons})
        else:
            # Additional heuristics for suspicious
            # Very short slugs might be real ("Age", "BMI") or might be too vague
            if len(slug) <= 3:
                suspicious.append({"slug": slug, "count": count, "reason": "very_short"})
            else:
                likely_real.append({"slug": slug, "count": count})

    return fabricated, suspicious, likely_real


def find_tool_slug_mapping(results):
    """For each tool, determine what the Wikipedia slug should be based on the tool concept."""

    # Manual mapping for common tool types to their correct Wikipedia articles
    CONCEPT_MAPPINGS = {
        # Format/encoding tools
        "json": "JSON",
        "xml": "XML",
        "yaml": "YAML",
        "csv": "Comma-separated_values",
        "html": "HTML",
        "css": "CSS",
        "markdown": "Markdown",
        "base64": "Base64",
        "base32": "Base32",
        "hex": "Hexadecimal",
        "binary": "Binary_number",
        "octal": "Octal",
        "ascii": "ASCII",
        "unicode": "Unicode",
        "utf-8": "UTF-8",
        "url": "URL",
        "uri": "Uniform_Resource_Identifier",
        "regex": "Regular_expression",
        "jwt": "JSON_Web_Token",
        "uuid": "Universally_unique_identifier",
        "sql": "SQL",
        "toml": "TOML",
        "svg": "SVG",
        "png": "PNG",
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "gif": "GIF",
        "webp": "WebP",
        "pdf": "PDF",
        "qr": "QR_code",
        "barcode": "Barcode",

        # Crypto/hash
        "md5": "MD5",
        "sha": "SHA-2",
        "sha1": "SHA-1",
        "sha256": "SHA-2",
        "sha512": "SHA-2",
        "hash": "Hash_function",
        "hmac": "HMAC",
        "aes": "Advanced_Encryption_Standard",
        "rsa": "RSA_(cryptosystem)",
        "encryption": "Encryption",
        "password": "Password_strength",
        "bcrypt": "Bcrypt",

        # Math/calculators
        "bmi": "Body_mass_index",
        "mortgage": "Mortgage_loan",
        "compound-interest": "Compound_interest",
        "simple-interest": "Interest",
        "percentage": "Percentage",
        "fraction": "Fraction",
        "prime": "Prime_number",
        "fibonacci": "Fibonacci_sequence",
        "factorial": "Factorial",
        "matrix": "Matrix_(mathematics)",
        "quadratic": "Quadratic_equation",
        "standard-deviation": "Standard_deviation",
        "mean": "Mean",
        "median": "Median",
        "probability": "Probability",
        "permutation": "Permutation",
        "combination": "Combination",
        "gcd": "Greatest_common_divisor",
        "lcm": "Least_common_multiple",
        "logarithm": "Logarithm",
        "exponent": "Exponentiation",
        "trigonometry": "Trigonometry",
        "algebra": "Algebra",
        "calculus": "Calculus",
        "geometry": "Geometry",
        "pythagorean": "Pythagorean_theorem",
        "area": "Area",
        "volume": "Volume",
        "circumference": "Circumference",
        "perimeter": "Perimeter",
        "pi": "Pi",
        "ohm": "Ohm%27s_law",
        "acceleration": "Acceleration",
        "velocity": "Velocity",
        "density": "Density",
        "force": "Force",
        "pressure": "Pressure",
        "energy": "Energy",
        "power": "Power_(physics)",
        "frequency": "Frequency",
        "wavelength": "Wavelength",

        # Health
        "calorie": "Calorie",
        "protein": "Protein_(nutrient)",
        "carbohydrate": "Carbohydrate",
        "fat": "Fat",
        "heart-rate": "Heart_rate",
        "blood-pressure": "Blood_pressure",
        "cholesterol": "Cholesterol",
        "pregnancy": "Pregnancy",
        "ovulation": "Ovulation",
        "due-date": "Estimated_date_of_delivery",
        "sleep": "Sleep",
        "water-intake": "Drinking_water",
        "tdee": "Basal_metabolic_rate",
        "bmr": "Basal_metabolic_rate",
        "body-fat": "Body_fat_percentage",
        "lean-body-mass": "Lean_body_mass",
        "waist-to-hip": "Waist%E2%80%93hip_ratio",
        "blood-alcohol": "Blood_alcohol_content",
        "macro": "Macronutrient",

        # Finance
        "401k": "401(k)",
        "529": "529_plan",
        "ira": "Individual_retirement_account",
        "roth": "Roth_IRA",
        "tax": "Tax",
        "salary": "Salary",
        "hourly": "Wage",
        "inflation": "Inflation",
        "roi": "Return_on_investment",
        "debt": "Debt",
        "loan": "Loan",
        "apr": "Annual_percentage_rate",
        "amortization": "Amortization_(business)",
        "annuity": "Annuity",
        "depreciation": "Depreciation",
        "tip": "Gratuity",
        "discount": "Discounting",
        "margin": "Profit_margin",
        "markup": "Markup_(business)",
        "break-even": "Break-even_(economics)",
        "net-worth": "Net_worth",
        "paycheck": "Paycheck",
        "payroll": "Payroll",
        "stock": "Stock",
        "dividend": "Dividend",
        "bond": "Bond_(finance)",
        "cagr": "Compound_annual_growth_rate",
        "npv": "Net_present_value",
        "irr": "Internal_rate_of_return",

        # Time/date
        "age": "Chronological_age",
        "date": "Calendar_date",
        "time": "Time",
        "timezone": "Time_zone",
        "epoch": "Unix_time",
        "unix": "Unix_time",
        "timestamp": "Unix_time",
        "countdown": "Countdown",
        "stopwatch": "Stopwatch",
        "pomodoro": "Pomodoro_Technique",

        # Text/string
        "word-count": "Word_count",
        "character-count": "Character_(computing)",
        "lorem-ipsum": "Lorem_ipsum",
        "palindrome": "Palindrome",
        "anagram": "Anagram",
        "acronym": "Acronym",
        "cipher": "Cipher",
        "morse": "Morse_code",
        "braille": "Braille",
        "roman-numeral": "Roman_numerals",

        # Color
        "color": "Color_model",
        "rgb": "RGB_color_model",
        "hex-color": "Web_colors",
        "hsl": "HSL_and_HSV",
        "hsv": "HSL_and_HSV",
        "cmyk": "CMYK_color_model",
        "gradient": "Color_gradient",
        "contrast": "Color_contrast",

        # Unit conversions
        "temperature": "Temperature",
        "celsius": "Celsius",
        "fahrenheit": "Fahrenheit",
        "kelvin": "Kelvin",
        "length": "Length",
        "meter": "Metre",
        "mile": "Mile",
        "kilometer": "Kilometre",
        "inch": "Inch",
        "foot": "Foot_(unit)",
        "yard": "Yard",
        "centimeter": "Centimetre",
        "millimeter": "Millimetre",
        "weight": "Mass",
        "kilogram": "Kilogram",
        "pound": "Pound_(mass)",
        "ounce": "Ounce",
        "gram": "Gram",
        "ton": "Ton",
        "liter": "Litre",
        "gallon": "Gallon",
        "cup": "Cup_(unit)",
        "tablespoon": "Tablespoon",
        "teaspoon": "Teaspoon",
        "acre": "Acre",
        "hectare": "Hectare",
        "square-foot": "Square_foot",
        "square-meter": "Square_metre",
        "speed": "Speed",
        "mph": "Miles_per_hour",
        "kmh": "Kilometres_per_hour",
        "knot": "Knot_(unit)",

        # Currency
        "usd": "United_States_dollar",
        "eur": "Euro",
        "gbp": "Pound_sterling",
        "jpy": "Japanese_yen",
        "cad": "Canadian_dollar",
        "aud": "Australian_dollar",
        "chf": "Swiss_franc",
        "cny": "Renminbi",
        "inr": "Indian_rupee",
        "currency": "Currency",
        "exchange-rate": "Exchange_rate",

        # Programming
        "javascript": "JavaScript",
        "python": "Python_(programming_language)",
        "java": "Java_(programming_language)",
        "csharp": "C_Sharp_(programming_language)",
        "cpp": "C%2B%2B",
        "typescript": "TypeScript",
        "php": "PHP",
        "ruby": "Ruby_(programming_language)",
        "go": "Go_(programming_language)",
        "rust": "Rust_(programming_language)",
        "swift": "Swift_(programming_language)",
        "kotlin": "Kotlin_(programming_language)",
        "ip": "IP_address",
        "dns": "Domain_Name_System",
        "http": "HTTP",
        "https": "HTTPS",
        "api": "API",
        "rest": "REST",
        "graphql": "GraphQL",
        "websocket": "WebSocket",
        "cron": "Cron",

        # Citation
        "apa": "APA_style",
        "mla": "MLA_Handbook",
        "chicago": "The_Chicago_Manual_of_Style",
        "harvard": "Harvard_referencing",
        "ieee": "IEEE_style",
        "ama": "AMA_Manual_of_Style",
        "vancouver": "Vancouver_system",
        "turabian": "A_Manual_for_Writers_of_Research_Papers,_Theses,_and_Dissertations",

        # Misc
        "electricity": "Electricity",
        "solar": "Solar_energy",
        "concrete": "Concrete",
        "gravel": "Gravel",
        "mulch": "Mulch",
        "soil": "Soil",
        "paint": "Paint",
        "tile": "Tile",
        "carpet": "Carpet",
        "flooring": "Flooring",
        "roofing": "Roof",
        "fence": "Fence",
        "deck": "Deck_(building)",
        "drywall": "Drywall",
        "insulation": "Building_insulation",
    }

    return CONCEPT_MAPPINGS


def detect_fabricated_slugs(results):
    """More aggressive detection of fabricated Wikipedia slugs."""
    fabricated_entries = []

    for tool_name, data in results.items():
        for slug in data["slugs"]:
            is_fabricated = False
            reason = ""

            # 1. Repeated words: "Calculator_Calculator", "Converter_Converter"
            words = slug.split('_')
            word_lower = [w.lower() for w in words]
            if len(word_lower) > 1 and len(word_lower) != len(set(word_lower)):
                is_fabricated = True
                reason = "repeated_words"

            # 2. Tool-name patterns ending in tool-type words
            tool_type_words = [
                'Calculator', 'Converter', 'Generator', 'Checker', 'Tester',
                'Formatter', 'Encoder', 'Decoder', 'Validator', 'Analyzer',
                'Builder', 'Maker', 'Solver', 'Finder', 'Counter', 'Timer',
                'Tracker', 'Planner', 'Picker', 'Selector', 'Scanner',
                'Extractor', 'Compressor', 'Decompressor', 'Minifier',
                'Beautifier', 'Optimizer', 'Simulator', 'Estimator',
                'Ranker', 'Sorter', 'Comparator', 'Inspector', 'Debugger',
                'Profiler', 'Monitor', 'Logger', 'Viewer', 'Editor',
                'Manager', 'Helper', 'Utility', 'Tool', 'App',
            ]

            if not is_fabricated and len(words) >= 2:
                last_word = words[-1]
                if last_word in tool_type_words:
                    # But some real articles end in these: "Calculator" is a real article
                    # "Converter" alone is real. Multi-word + tool type = fabricated
                    if len(words) > 1 and words[0] not in ['The', 'A', 'An']:
                        is_fabricated = True
                        reason = f"tool_name_pattern (ends in {last_word})"

            # 3. X_To_Y conversion patterns
            if not is_fabricated and re.match(r'^[A-Z][a-z]*_[Tt]o_[A-Z][a-z]*$', slug):
                is_fabricated = True
                reason = "conversion_pattern"

            # 4. Slug is just the tool name with underscores
            tool_slug_from_name = tool_name.replace('-', '_').title().replace(' ', '_')
            if not is_fabricated and slug.replace('_', '').lower() == tool_name.replace('-', '').lower():
                is_fabricated = True
                reason = "slug_matches_tool_name"

            if is_fabricated:
                fabricated_entries.append({
                    "tool": tool_name,
                    "current_slug": slug,
                    "reason": reason,
                })

    return fabricated_entries


def check_definitions(all_definitions):
    """Check definition quality - flag tool-describing definitions."""
    bad_definitions = []

    bad_patterns = [
        r'(?i)this tool',
        r'(?i)this calculator',
        r'(?i)this converter',
        r'(?i)this generator',
        r'(?i)our (tool|calculator|converter)',
        r'(?i)helps you (calculate|convert|generate|check)',
        r'(?i)use this',
        r'(?i)try our',
        r'(?i)free online',
        r'(?i)learn more from wikipedia',
        r'(?i)^according to wikipedia,?\s*$',
        r'(?i)click here',
    ]

    for defn in all_definitions:
        text = defn["definition"]
        for pat in bad_patterns:
            if re.search(pat, text):
                bad_definitions.append({
                    "tool": defn["tool"],
                    "definition": text[:200],
                    "issue": f"Matches bad pattern: {pat}",
                })
                break

        # Also flag very short/empty definitions
        clean_text = re.sub(r'<[^>]+>', '', text).strip()
        if len(clean_text) < 20:
            bad_definitions.append({
                "tool": defn["tool"],
                "definition": text[:200],
                "issue": "Too short (less than 20 chars)",
            })

    return bad_definitions


def main():
    print("=" * 70)
    print("WIKIPEDIA REFERENCE AUDIT - Zovo Tools")
    print("=" * 70)

    # Scan all tools
    results, all_slugs, all_definitions, with_wiki, without_wiki, total = scan_all_tools()

    print(f"\nTotal tool directories scanned: {total}")
    print(f"Tools with Wikipedia links: {with_wiki}")
    print(f"Tools without Wikipedia links: {without_wiki}")
    print(f"Coverage: {with_wiki/total*100:.1f}%")
    print(f"Total Wikipedia URLs found: {len(all_slugs)}")
    print(f"Unique slugs: {len(set(all_slugs))}")

    # Show most common slugs
    slug_counts = Counter(all_slugs)
    print(f"\n{'='*70}")
    print("TOP 50 MOST USED WIKIPEDIA SLUGS")
    print(f"{'='*70}")
    for slug, count in slug_counts.most_common(50):
        print(f"  {count:>4}x  {slug}")

    # Detect fabricated slugs
    fabricated = detect_fabricated_slugs(results)

    print(f"\n{'='*70}")
    print(f"FABRICATED SLUGS DETECTED: {len(fabricated)}")
    print(f"{'='*70}")
    for entry in sorted(fabricated, key=lambda x: x["reason"]):
        print(f"  [{entry['reason']}] {entry['tool']}: {entry['current_slug']}")

    # Check definitions
    bad_defs = check_definitions(all_definitions)

    print(f"\n{'='*70}")
    print(f"BAD DEFINITIONS: {len(bad_defs)}")
    print(f"{'='*70}")
    for bd in bad_defs[:30]:
        defn_preview = re.sub(r'<[^>]+>', '', bd['definition'])[:80]
        print(f"  {bd['tool']}: \"{defn_preview}...\"")
        print(f"    Issue: {bd['issue']}")

    # Save full report
    report = {
        "summary": {
            "total_tools": total,
            "tools_with_wiki": with_wiki,
            "tools_without_wiki": without_wiki,
            "coverage_pct": round(with_wiki/total*100, 1),
            "total_wiki_urls": len(all_slugs),
            "unique_slugs": len(set(all_slugs)),
            "fabricated_count": len(fabricated),
            "bad_definitions_count": len(bad_defs),
        },
        "fabricated_slugs": fabricated,
        "bad_definitions": bad_defs,
        "all_results": {k: v for k, v in sorted(results.items())},
        "slug_frequency": dict(slug_counts.most_common()),
    }

    with open(REPORT_FILE, 'w') as f:
        json.dump(report, f, indent=2)

    print(f"\nFull report saved to: {REPORT_FILE}")

    return report


if __name__ == "__main__":
    main()
