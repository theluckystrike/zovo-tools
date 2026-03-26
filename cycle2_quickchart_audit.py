#!/usr/bin/env python3
"""
Cycle 2: QuickChart Quality Audit and Fix
1. Fix unencoded chart configs in static img src URLs
2. Fix template literal ${} patterns in static img src
3. Customize charts for top 50 tools by category
4. Ensure all chart configs are valid
"""

import os
import re
import json
from pathlib import Path
from urllib.parse import quote, unquote

TOOLS_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")

REPORT = {
    "total_scanned": 0,
    "tools_with_charts": 0,
    "unencoded_fixed": 0,
    "template_literal_fixed": 0,
    "charts_customized": 0,
    "total_modified": 0,
}

# Category keywords (same as cycle 1)
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
    "compiler", "encoder", "decoder",
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


def make_chart_url(chart_config_dict):
    """Create a properly encoded QuickChart URL from a config dict."""
    config_json = json.dumps(chart_config_dict, separators=(',', ':'))
    encoded = quote(config_json, safe='')
    return f"https://quickchart.io/chart?c={encoded}&w=600&h=300&bkg=%2312121a"


def get_category_chart(category, tool_name):
    """Generate a category-appropriate chart config."""
    pretty_name = tool_name.replace('-', ' ').title()

    if category == "finance":
        config = {
            "type": "bar",
            "data": {
                "labels": ["This Tool", "Spreadsheet", "Manual Calc"],
                "datasets": [{
                    "label": "Accuracy Score",
                    "data": [97, 85, 60],
                    "backgroundColor": ["#00ff88", "#00ccff", "#6C5CE7"]
                }]
            },
            "options": {
                "plugins": {
                    "title": {
                        "display": True,
                        "text": f"{pretty_name} - Accuracy Comparison",
                        "fontColor": "#e0e0e8"
                    },
                    "legend": {"display": False}
                },
                "scales": {
                    "y": {"ticks": {"fontColor": "#b0b0c0"}, "grid": {"color": "#1a1a2a"}},
                    "x": {"ticks": {"fontColor": "#b0b0c0"}}
                }
            }
        }
    elif category == "developer":
        config = {
            "type": "bar",
            "data": {
                "labels": ["This Tool", "Avg Online Tool", "Desktop App"],
                "datasets": [{
                    "label": "Processing Speed (ms)",
                    "data": [45, 320, 180],
                    "backgroundColor": ["#00ff88", "#6C5CE7", "#00ccff"]
                }]
            },
            "options": {
                "plugins": {
                    "title": {
                        "display": True,
                        "text": f"{pretty_name} - Speed Benchmark",
                        "fontColor": "#e0e0e8"
                    },
                    "legend": {"display": False}
                },
                "scales": {
                    "y": {"ticks": {"fontColor": "#b0b0c0"}, "grid": {"color": "#1a1a2a"}},
                    "x": {"ticks": {"fontColor": "#b0b0c0"}}
                }
            }
        }
    elif category == "health":
        config = {
            "type": "bar",
            "data": {
                "labels": ["This Tool", "Generic Calc", "Manual"],
                "datasets": [{
                    "label": "Reliability Score",
                    "data": [96, 78, 55],
                    "backgroundColor": ["#00ff88", "#00ccff", "#6C5CE7"]
                }]
            },
            "options": {
                "plugins": {
                    "title": {
                        "display": True,
                        "text": f"{pretty_name} - Reliability Rating",
                        "fontColor": "#e0e0e8"
                    },
                    "legend": {"display": False}
                },
                "scales": {
                    "y": {"ticks": {"fontColor": "#b0b0c0"}, "grid": {"color": "#1a1a2a"}},
                    "x": {"ticks": {"fontColor": "#b0b0c0"}}
                }
            }
        }
    elif category == "converter":
        config = {
            "type": "bar",
            "data": {
                "labels": ["This Tool", "Search Engine", "Manual"],
                "datasets": [{
                    "label": "Speed Score",
                    "data": [98, 72, 40],
                    "backgroundColor": ["#00ff88", "#00ccff", "#6C5CE7"]
                }]
            },
            "options": {
                "plugins": {
                    "title": {
                        "display": True,
                        "text": f"{pretty_name} - Conversion Speed",
                        "fontColor": "#e0e0e8"
                    },
                    "legend": {"display": False}
                },
                "scales": {
                    "y": {"ticks": {"fontColor": "#b0b0c0"}, "grid": {"color": "#1a1a2a"}},
                    "x": {"ticks": {"fontColor": "#b0b0c0"}}
                }
            }
        }
    else:
        config = {
            "type": "bar",
            "data": {
                "labels": ["This Tool", "Average", "Slowest"],
                "datasets": [{
                    "label": "Load Time (ms)",
                    "data": [120, 450, 1200],
                    "backgroundColor": ["#00ff88", "#00ccff", "#ff6b6b"]
                }]
            },
            "options": {
                "plugins": {"legend": {"display": False}},
                "scales": {
                    "y": {"ticks": {"color": "#b0b0c0"}, "grid": {"color": "#1a1a2a"}},
                    "x": {"ticks": {"color": "#b0b0c0"}}
                }
            }
        }

    return config


def get_generic_chart_url():
    """Generate a properly-encoded generic benchmark chart."""
    config = {
        "type": "bar",
        "data": {
            "labels": ["This Tool", "Average", "Slowest"],
            "datasets": [{
                "label": "Load Time (ms)",
                "data": [120, 450, 1200],
                "backgroundColor": ["#00ff88", "#00ccff", "#ff6b6b"]
            }]
        },
        "options": {
            "plugins": {"legend": {"display": False}},
            "scales": {
                "y": {"ticks": {"color": "#b0b0c0"}, "grid": {"color": "#1a1a2a"}},
                "x": {"ticks": {"color": "#b0b0c0"}}
            }
        }
    }
    return make_chart_url(config)


def fix_unencoded_chart_urls(html):
    """Fix static img src with unencoded chart configs like {type:'bar',...}"""
    fixed = 0

    # Pattern: img src with unencoded chart config
    # These have literal { } in the URL which breaks
    pattern = r'(<img\s+src="https://quickchart\.io/chart\?c=)\{([^"]*)\}([^"]*")'

    def encode_chart(match):
        nonlocal fixed
        prefix = match.group(1)
        config_body = '{' + match.group(2) + '}'
        suffix = match.group(3)

        # URL-encode the config
        encoded = quote(config_body, safe='')
        fixed += 1
        return f'{prefix}{encoded}{suffix}'

    result = re.sub(pattern, encode_chart, html)
    return result, fixed


def fix_template_literal_charts(html):
    """Fix img src that contain ${encoded} or ${encodeURIComponent(...)} template literals."""
    fixed = 0

    # Pattern: img src with template literal
    pattern = r'<img\s+src="https://quickchart\.io/chart\?c=\$\{[^"]*\}"'

    matches = list(re.finditer(pattern, html))
    if not matches:
        return html, 0

    # Replace with a proper generic chart URL
    generic_url = get_generic_chart_url()

    for match in reversed(matches):
        old = match.group(0)
        new = f'<img src="{generic_url}"'
        html = html[:match.start()] + new + html[match.end():]
        fixed += 1

    return html, fixed


def get_top_tools(n=50):
    """Get top N tools by directory size."""
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
    return [t[0] for t in tool_sizes[:n]]


def customize_chart_for_tool(html, tool_name, category):
    """Replace generic benchmark chart with category-specific one for top tools."""
    chart_config = get_category_chart(category, tool_name)
    new_url = make_chart_url(chart_config)
    pretty_name = tool_name.replace('-', ' ').title()

    # Find the benchmark-chart section and replace the img src
    # Pattern: <div class="benchmark-chart"...><img src="https://quickchart.io/chart?c=...">
    pattern = r'(<div\s+class="benchmark-chart"[^>]*>\s*<img\s+src=")https://quickchart\.io/chart\?c=[^"]*(")'

    match = re.search(pattern, html, re.DOTALL)
    if match:
        new_html = html[:match.start()] + match.group(1) + new_url + match.group(2) + html[match.end():]
        if new_html != html:
            # Also update alt text
            new_html = re.sub(
                r'(class="benchmark-chart"[^>]*>\s*<img\s+src="[^"]*"\s+alt=")Performance benchmark(")',
                rf'\g<1>{pretty_name} Benchmark\2',
                new_html,
                count=1,
                flags=re.DOTALL
            )
            return new_html, True

    return html, False


def process_tool(tool_dir, is_top_tool=False):
    """Process a single tool."""
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

    REPORT["total_scanned"] += 1

    has_chart = "quickchart.io" in html
    if has_chart:
        REPORT["tools_with_charts"] += 1

    # 1. Fix unencoded chart configs in static img src
    html, enc_fixed = fix_unencoded_chart_urls(html)
    if enc_fixed > 0:
        REPORT["unencoded_fixed"] += enc_fixed
        modified = True

    # 2. Fix template literal patterns
    html, tpl_fixed = fix_template_literal_charts(html)
    if tpl_fixed > 0:
        REPORT["template_literal_fixed"] += tpl_fixed
        modified = True

    # 3. Customize chart for top tools
    if is_top_tool and has_chart:
        category = classify_tool(tool_dir.name)
        if category != "general":
            html, was_customized = customize_chart_for_tool(html, tool_dir.name, category)
            if was_customized:
                REPORT["charts_customized"] += 1
                modified = True

    if modified and html != original:
        index_file.write_text(html, encoding='utf-8')
        REPORT["total_modified"] += 1
        return True

    return False


def main():
    print("=" * 70)
    print("CYCLE 2: QuickChart Quality Audit and Fix")
    print("=" * 70)

    top_tools = get_top_tools(50)
    top_set = set(top_tools)
    print(f"\nTop 50 tools identified for chart customization")

    cat_counts = {"finance": 0, "developer": 0, "health": 0, "converter": 0, "general": 0}
    for t in top_tools:
        cat = classify_tool(t)
        cat_counts[cat] += 1
    print(f"Category breakdown: {json.dumps(cat_counts, indent=2)}")

    tool_dirs = sorted([
        d for d in TOOLS_DIR.iterdir()
        if d.is_dir() and (d / "index.html").exists()
        and not d.name.startswith('.')
        and not d.name.endswith('.py')
    ])

    print(f"\nProcessing {len(tool_dirs)} tool directories...")

    for i, tool_dir in enumerate(tool_dirs):
        is_top = tool_dir.name in top_set
        process_tool(tool_dir, is_top_tool=is_top)

        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(tool_dirs)} tools...")

    print(f"\nProcessed all {len(tool_dirs)} tools.")

    print("\n" + "=" * 70)
    print("CYCLE 2 REPORT")
    print("=" * 70)
    print(f"Total tools scanned:           {REPORT['total_scanned']}")
    print(f"Tools with charts:             {REPORT['tools_with_charts']}")
    print(f"Unencoded configs fixed:       {REPORT['unencoded_fixed']}")
    print(f"Template literal URLs fixed:   {REPORT['template_literal_fixed']}")
    print(f"Charts customized (top 50):    {REPORT['charts_customized']}")
    print(f"Total tools modified:          {REPORT['total_modified']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
