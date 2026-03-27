#!/usr/bin/env python3
"""
Cycle 4b: Fix remaining visual consistency issues.
1. about-this-tool: empty color:;, empty background:;, border-radius:8px
2. Video wrapper: border-radius 8px/10px/.75rem -> 12px
3. Quick-facts: empty gradient values
"""

import re
from pathlib import Path

TOOLS_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")

REPORT = {
    "about_tool_color_fixed": 0,
    "about_tool_bg_fixed": 0,
    "about_tool_radius_fixed": 0,
    "video_radius_fixed": 0,
    "quickfacts_gradient_fixed": 0,
    "total_modified": 0,
}


def fix_all(html):
    """Apply all remaining visual consistency fixes."""
    original = html

    # === ABOUT-THIS-TOOL FIXES ===

    # Fix 1: about-this-tool h2/heading with empty color:;
    # These are headings inside the about section, not the div itself
    replacements = [
        # Heading styles with empty color
        ('id="about-this-tool" style="color:;font-size:1.3rem;margin-top:0;"',
         'id="about-this-tool" style="color:#fff;font-size:1.3rem;margin-top:0;"'),
        ('id="about-this-tool" style="color:;font-size:1.3rem;margin:0 0 1rem 0;"',
         'id="about-this-tool" style="color:#fff;font-size:1.3rem;margin:0 0 1rem 0;"'),
        ('id="about-this-tool" style="color:;font-size:1.3rem;margin:0 0 1rem;"',
         'id="about-this-tool" style="color:#fff;font-size:1.3rem;margin:0 0 1rem;"'),

        # Div styles with empty background AND empty color AND empty border
        ('id="about-this-tool" style="background:;border:1px solid ;border-radius:8px;padding:1.5rem;max-width:800px;margin:2rem auto;color:;font-family:Inter,sans-serif;"',
         'id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:12px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;font-family:Inter,sans-serif;"'),

        # Div with proper bg but empty color at end
        ('id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem;max-width:800px;margin:2rem auto;color:;"',
         'id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:12px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;"'),

        # Div with different property order, empty color
        ('id="about-this-tool" style="margin:2rem auto;max-width:800px;padding:1.5rem;background:#12121a;border:1px solid #2a2a3a;border-radius:8px;color:;font-family:Inter,sans-serif;"',
         'id="about-this-tool" style="margin:2rem auto;max-width:800px;padding:1.5rem;background:#12121a;border:1px solid #2a2a3a;border-radius:12px;color:#e0e0e8;font-family:Inter,sans-serif;"'),

        # Div with 8px radius but otherwise correct
        ('id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;"',
         'id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:12px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;"'),
    ]

    for old, new in replacements:
        if old in html:
            count = html.count(old)
            html = html.replace(old, new)
            REPORT["about_tool_color_fixed"] += count

    # === VIDEO WRAPPER BORDER-RADIUS FIXES ===
    # These need regex to handle different endings

    # Fix 10px -> 12px
    video_replacements = [
        ('padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px"',
         'padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px"'),
        ('padding-bottom:56.25%;height:0;overflow:hidden;border-radius:10px;',
         'padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px;'),
        ('padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px"',
         'padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px"'),
        ('padding-bottom:56.25%;height:0;overflow:hidden;border-radius:8px;',
         'padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px;'),
        ('padding-bottom:56.25%;height:0;overflow:hidden;border-radius:.75rem"',
         'padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px"'),
        ('padding-bottom:56.25%;height:0;overflow:hidden;border-radius:.75rem;',
         'padding-bottom:56.25%;height:0;overflow:hidden;border-radius:12px;'),
    ]

    for old, new in video_replacements:
        if old in html:
            count = html.count(old)
            html = html.replace(old, new)
            REPORT["video_radius_fixed"] += count

    # === QUICK-FACTS EMPTY GRADIENT FIX ===
    # Fix: background:linear-gradient(135deg,); -> proper gradient
    old_gradient = 'background:linear-gradient(135deg,);border:1px solid ;'
    new_gradient = 'background:linear-gradient(135deg,#12121a,#1a1a2e);border:1px solid #2a2a3a;'
    if old_gradient in html:
        count = html.count(old_gradient)
        html = html.replace(old_gradient, new_gradient)
        REPORT["quickfacts_gradient_fixed"] += count

    modified = html != original
    return html, modified


def main():
    print("=" * 70)
    print("CYCLE 4b: Remaining Visual Consistency Fixes")
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
        html_new, modified = fix_all(html)
        if modified:
            index_file.write_text(html_new, encoding='utf-8')
            REPORT["total_modified"] += 1
        if (i + 1) % 100 == 0:
            print(f"  Processed {i + 1}/{len(tool_dirs)} tools...")

    # Post-verification
    print("\n--- Post-verification ---")
    remaining = {
        "about_empty_color": 0,
        "about_8px_radius": 0,
        "video_8px_radius": 0,
        "video_10px_radius": 0,
        "video_75rem_radius": 0,
        "quickfacts_empty_gradient": 0,
        "about_empty_bg": 0,
    }

    for d in sorted(TOOLS_DIR.iterdir()):
        if d.is_dir() and (d / 'index.html').exists() and not d.name.startswith('.') and not d.name.endswith('.py'):
            html = (d / 'index.html').read_text()
            if 'id="about-this-tool"' in html and 'color:;' in html:
                remaining["about_empty_color"] += 1
            if 'id="about-this-tool"' in html and 'border-radius:8px' in html:
                remaining["about_8px_radius"] += 1
            if 'padding-bottom:56.25%' in html and 'border-radius:8px' in html:
                remaining["video_8px_radius"] += 1
            if 'padding-bottom:56.25%' in html and 'border-radius:10px' in html:
                remaining["video_10px_radius"] += 1
            if 'padding-bottom:56.25%' in html and 'border-radius:.75rem' in html:
                remaining["video_75rem_radius"] += 1
            if 'background:linear-gradient(135deg,);' in html:
                remaining["quickfacts_empty_gradient"] += 1
            if 'id="about-this-tool"' in html and 'background:;' in html:
                remaining["about_empty_bg"] += 1

    for key, count in remaining.items():
        status = "CLEAN" if count == 0 else f"REMAINING: {count}"
        print(f"  {key}: {status}")

    print("\n" + "=" * 70)
    print("CYCLE 4b REPORT")
    print("=" * 70)
    print(f"About-tool color/radius fixed: {REPORT['about_tool_color_fixed']}")
    print(f"Video border-radius fixed:     {REPORT['video_radius_fixed']}")
    print(f"Quick-facts gradient fixed:    {REPORT['quickfacts_gradient_fixed']}")
    print(f"Total tools modified:          {REPORT['total_modified']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
