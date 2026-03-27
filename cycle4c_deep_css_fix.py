#!/usr/bin/env python3
"""
Cycle 4c: Deep CSS Fix - Fix all empty CSS values and remaining radius inconsistencies.
Uses regex for precise pattern matching across all inline styles.
"""

import re
from pathlib import Path

TOOLS_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")

REPORT = {
    "empty_color_fixed": 0,
    "empty_bg_fixed": 0,
    "empty_border_fixed": 0,
    "empty_border_left_fixed": 0,
    "video_radius_fixed": 0,
    "about_radius_fixed": 0,
    "total_modified": 0,
}


def fix_css_issues(html):
    """Fix all CSS issues in a single pass using regex."""
    original = html

    # 1. Fix color:; -> color:#e0e0e8; (in inline styles)
    # Be careful: only fix within style="" attributes
    html = re.sub(r'(style="[^"]*?)color:;', r'\1color:#e0e0e8;', html)

    # 2. Fix background:; -> background:#12121a;
    html = re.sub(r'(style="[^"]*?)background:;', r'\1background:#12121a;', html)

    # 3. Fix border:1px solid ; -> border:1px solid #2a2a3a;
    html = re.sub(r'border:1px solid ;', r'border:1px solid #2a2a3a;', html)

    # 4. Fix border-left:4px solid ; -> border-left:4px solid #00ff88;
    html = re.sub(r'border-left:4px solid ;', r'border-left:4px solid #00ff88;', html)

    # 5. Fix border-left:3px solid ; -> border-left:3px solid #00ff88;
    html = re.sub(r'border-left:3px solid ;', r'border-left:3px solid #00ff88;', html)

    # 6. Fix video wrapper border-radius: 8px/10px/.75rem -> 12px
    # Only within position:relative;padding-bottom:56.25% context
    html = re.sub(
        r'(position:relative;padding-bottom:56\.25%;height:0;overflow:hidden;border-radius:)(8px|10px|\.75rem)',
        r'\g<1>12px',
        html
    )

    # 7. Fix about-this-tool border-radius:8px -> 12px
    # Match about-this-tool divs specifically
    html = re.sub(
        r'(id="about-this-tool" style="[^"]*?)border-radius:8px',
        r'\1border-radius:12px',
        html
    )

    modified = html != original
    return html, modified


def main():
    print("=" * 70)
    print("CYCLE 4c: Deep CSS Fix")
    print("=" * 70)

    tool_dirs = sorted([
        d for d in TOOLS_DIR.iterdir()
        if d.is_dir() and (d / "index.html").exists()
        and not d.name.startswith('.')
        and not d.name.endswith('.py')
    ])

    print(f"\nProcessing {len(tool_dirs)} tool directories...")

    for i, tool_dir in enumerate(tool_dirs):
        index_file = tool_dir / "index.html"
        html = index_file.read_text(encoding='utf-8')
        html_new, modified = fix_css_issues(html)
        if modified:
            index_file.write_text(html_new, encoding='utf-8')
            REPORT["total_modified"] += 1
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(tool_dirs)} tools...")

    # Post-verification
    print("\n--- Post-verification ---")
    issues = {
        "any_color_semicolon": 0,
        "any_background_semicolon": 0,
        "any_border_solid_semicolon": 0,
        "video_non12px_radius": 0,
        "about_8px_radius": 0,
        "quickfacts_empty_gradient": 0,
    }

    for d in sorted(TOOLS_DIR.iterdir()):
        if d.is_dir() and (d / 'index.html').exists() and not d.name.startswith('.') and not d.name.endswith('.py'):
            html = (d / 'index.html').read_text()
            if re.search(r'style="[^"]*color:;', html):
                issues["any_color_semicolon"] += 1
            if re.search(r'style="[^"]*background:;', html):
                issues["any_background_semicolon"] += 1
            if 'border:1px solid ;' in html or 'border-left:4px solid ;' in html:
                issues["any_border_solid_semicolon"] += 1
            if re.search(r'padding-bottom:56\.25%.*?border-radius:(8px|10px|\.75rem)', html):
                issues["video_non12px_radius"] += 1
            if re.search(r'id="about-this-tool"[^>]*border-radius:8px', html):
                issues["about_8px_radius"] += 1
            if 'background:linear-gradient(135deg,);' in html:
                issues["quickfacts_empty_gradient"] += 1

    for key, count in issues.items():
        status = "CLEAN" if count == 0 else f"REMAINING: {count}"
        print(f"  {key}: {status}")

    print(f"\nTotal tools modified: {REPORT['total_modified']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
