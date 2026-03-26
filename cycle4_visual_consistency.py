#!/usr/bin/env python3
"""
Cycle 4: Visual Consistency Audit and Fix
Standardize all enrichment sections to consistent dark theme:
- Background: #12121a
- Border: 1px solid #2a2a3a
- Text: #a0a0b0
- Accent: #00ff88
- Links: #00ccff
- Border radius: 12px
- Max width: 800px
- Margin: auto centering
"""

import os
import re
from pathlib import Path

TOOLS_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")

REPORT = {
    "total_scanned": 0,
    "benchmark_chart_fixed": 0,
    "quick_facts_fixed": 0,
    "about_tool_fixed": 0,
    "video_embed_fixed": 0,
    "video_border_radius_fixed": 0,
    "empty_color_fixed": 0,
    "empty_gradient_fixed": 0,
    "total_tools_modified": 0,
}


def fix_benchmark_chart_style(html):
    """Standardize benchmark-chart sections: max-width:800px, margin:2rem auto, text-align:center."""
    fixed = 0

    # Fix: benchmark-chart with margin:2rem 0 -> margin:2rem auto;max-width:800px;text-align:center
    old = 'class="benchmark-chart" style="margin:2rem 0;"'
    new = 'class="benchmark-chart" style="margin:2rem auto;max-width:800px;text-align:center;"'
    if old in html:
        count = html.count(old)
        html = html.replace(old, new)
        fixed += count

    # Fix: bare benchmark-chart with no style
    old2 = 'class="benchmark-chart">'
    new2 = 'class="benchmark-chart" style="margin:2rem auto;max-width:800px;text-align:center;">'
    # Only replace if it's the div, not a substring match
    pattern = r'<div\s+class="benchmark-chart">'
    matches = list(re.finditer(pattern, html))
    for match in reversed(matches):
        html = html[:match.start()] + '<div class="benchmark-chart" style="margin:2rem auto;max-width:800px;text-align:center;">' + html[match.end():]
        fixed += 1

    return html, fixed


def fix_quick_facts_style(html):
    """Standardize quick-facts sections."""
    fixed = 0
    target_style = 'class="quick-facts" style="margin:2rem auto;padding:1.5rem;background:linear-gradient(135deg,#12121a,#1a1a2e);border:1px solid #2a2a3a;border-radius:12px;max-width:800px;"'

    # Fix: missing max-width and auto centering
    old1 = 'class="quick-facts" style="margin:2rem 0;padding:1.5rem;background:linear-gradient(135deg,#12121a,#1a1a2e);border:1px solid #2a2a3a;border-radius:12px;"'
    if old1 in html:
        count = html.count(old1)
        html = html.replace(old1, target_style)
        fixed += count

    # Fix: empty gradient values
    old2 = 'class="quick-facts" style="margin:2rem 0;padding:1.5rem;background:linear-gradient(135deg,);border:1px solid ;border-radius:12px;"'
    if old2 in html:
        count = html.count(old2)
        html = html.replace(old2, target_style)
        fixed += count

    # Fix: bare quick-facts with no style
    pattern = r'<section\s+class="quick-facts">'
    matches = list(re.finditer(pattern, html))
    for match in reversed(matches):
        html = html[:match.start()] + f'<section {target_style}>' + html[match.end():]
        fixed += 1

    return html, fixed


def fix_about_tool_style(html):
    """Fix about-this-tool sections with empty color values and inconsistent styling."""
    fixed = 0

    # Fix: empty color:; in about-this-tool div
    old1 = 'id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem;max-width:800px;margin:2rem auto;color:;font-family:Inter,sans-serif;"'
    new1 = 'id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:12px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;font-family:Inter,sans-serif;"'
    if old1 in html:
        count = html.count(old1)
        html = html.replace(old1, new1)
        fixed += count

    # Fix: border-radius:8px -> 12px in about-this-tool
    old2 = 'id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;font-family:\'Inter\',sans-serif;"'
    new2 = 'id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:12px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;font-family:Inter,sans-serif;"'
    if old2 in html:
        count = html.count(old2)
        html = html.replace(old2, new2)
        fixed += count

    # Same but without quotes around Inter
    old3 = 'id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;font-family:Inter,sans-serif;"'
    new3 = 'id="about-this-tool" style="background:#12121a;border:1px solid #2a2a3a;border-radius:12px;padding:1.5rem;max-width:800px;margin:2rem auto;color:#e0e0e8;font-family:Inter,sans-serif;"'
    if old3 in html:
        count = html.count(old3)
        html = html.replace(old3, new3)
        fixed += count

    return html, fixed


def fix_video_embed_style(html):
    """Standardize video-embed sections: max-width:800px, margin:2rem auto, border-radius:12px."""
    fixed = 0

    # Fix video-embed container: add max-width and auto centering
    old1 = 'class="video-embed" style="margin:2rem 0;"'
    new1 = 'class="video-embed" style="margin:2rem auto;max-width:800px;"'
    if old1 in html:
        count = html.count(old1)
        html = html.replace(old1, new1)
        fixed += count

    # Fix bare video-embed
    pattern = r'<div\s+class="video-embed">'
    matches = list(re.finditer(pattern, html))
    for match in reversed(matches):
        # Don't replace if it has an id attribute
        old_text = match.group(0)
        html = html[:match.start()] + '<div class="video-embed" style="margin:2rem auto;max-width:800px;">' + html[match.end():]
        fixed += 1

    return html, fixed


def fix_video_border_radius(html):
    """Standardize video wrapper border-radius to 12px."""
    fixed = 0

    # Fix border-radius:8px in video wrappers
    old_patterns = [
        ('border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.3);', 'border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.3);'),
        ('border-radius:8px;"', 'border-radius:12px;"'),
        ('border-radius:10px"', 'border-radius:12px"'),
        ('border-radius:10px;margin-bottom:16px"', 'border-radius:12px;margin-bottom:16px"'),
    ]

    for old, new in old_patterns:
        # Only fix inside position:relative video wrapper context
        if old in html:
            # Check it's in a video wrapper context
            video_pattern = f'position:relative;padding-bottom:56.25%;height:0;overflow:hidden;{old}'
            if video_pattern in html:
                count = html.count(video_pattern)
                html = html.replace(video_pattern, f'position:relative;padding-bottom:56.25%;height:0;overflow:hidden;{new}')
                fixed += count

    return html, fixed


def process_tool(tool_dir):
    """Process a single tool for visual consistency."""
    index_file = tool_dir / "index.html"
    if not index_file.exists():
        return False

    try:
        html = index_file.read_text(encoding='utf-8')
    except Exception:
        return False

    REPORT["total_scanned"] += 1
    original = html
    modified = False

    # 1. Fix benchmark-chart styling
    html, count = fix_benchmark_chart_style(html)
    if count > 0:
        REPORT["benchmark_chart_fixed"] += count
        modified = True

    # 2. Fix quick-facts styling
    html, count = fix_quick_facts_style(html)
    if count > 0:
        REPORT["quick_facts_fixed"] += count
        modified = True

    # 3. Fix about-this-tool styling
    html, count = fix_about_tool_style(html)
    if count > 0:
        REPORT["about_tool_fixed"] += count
        modified = True

    # 4. Fix video-embed wrapper styling
    html, count = fix_video_embed_style(html)
    if count > 0:
        REPORT["video_embed_fixed"] += count
        modified = True

    # 5. Fix video border-radius
    html, count = fix_video_border_radius(html)
    if count > 0:
        REPORT["video_border_radius_fixed"] += count
        modified = True

    if modified and html != original:
        index_file.write_text(html, encoding='utf-8')
        REPORT["total_tools_modified"] += 1
        return True

    return False


def verify():
    """Post-verification of consistency."""
    print("\n--- Post-verification ---")

    issues = {
        "benchmark_no_maxwidth": 0,
        "quickfacts_no_maxwidth": 0,
        "about_empty_color": 0,
        "about_8px_radius": 0,
        "video_no_maxwidth": 0,
        "video_8px_radius": 0,
        "video_10px_radius": 0,
        "quickfacts_empty_gradient": 0,
    }

    for d in sorted(TOOLS_DIR.iterdir()):
        if d.is_dir() and (d / 'index.html').exists() and not d.name.startswith('.') and not d.name.endswith('.py'):
            html = (d / 'index.html').read_text()

            if 'class="benchmark-chart" style="margin:2rem 0;"' in html:
                issues["benchmark_no_maxwidth"] += 1
            if 'class="quick-facts" style="margin:2rem 0;' in html and 'max-width' not in html.split('class="quick-facts"')[1][:200]:
                issues["quickfacts_no_maxwidth"] += 1
            if 'id="about-this-tool"' in html and 'color:;' in html:
                issues["about_empty_color"] += 1
            if 'id="about-this-tool"' in html and 'border-radius:8px' in html:
                issues["about_8px_radius"] += 1
            if 'class="video-embed" style="margin:2rem 0;"' in html:
                issues["video_no_maxwidth"] += 1
            if 'padding-bottom:56.25%' in html and 'border-radius:8px' in html:
                issues["video_8px_radius"] += 1
            if 'padding-bottom:56.25%' in html and 'border-radius:10px' in html:
                issues["video_10px_radius"] += 1
            if 'background:linear-gradient(135deg,);' in html:
                issues["quickfacts_empty_gradient"] += 1

    for key, count in issues.items():
        status = "CLEAN" if count == 0 else f"REMAINING: {count}"
        print(f"  {key}: {status}")


def main():
    print("=" * 70)
    print("CYCLE 4: Visual Consistency Audit and Fix")
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

    verify()

    print("\n" + "=" * 70)
    print("CYCLE 4 REPORT")
    print("=" * 70)
    print(f"Total tools scanned:           {REPORT['total_scanned']}")
    print(f"Benchmark chart style fixed:   {REPORT['benchmark_chart_fixed']}")
    print(f"Quick facts style fixed:       {REPORT['quick_facts_fixed']}")
    print(f"About tool style fixed:        {REPORT['about_tool_fixed']}")
    print(f"Video embed style fixed:       {REPORT['video_embed_fixed']}")
    print(f"Video border-radius fixed:     {REPORT['video_border_radius_fixed']}")
    print(f"Total tools modified:          {REPORT['total_tools_modified']}")
    print("=" * 70)


if __name__ == "__main__":
    main()
