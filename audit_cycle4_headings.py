#!/usr/bin/env python3
"""
Cycle 4: Heading Hierarchy Audit
Checks every tool page for proper heading structure:
- Exactly one <h1> tag
- No skipped heading levels (h1 -> h3 without h2)
- No empty headings
"""

import os
import re
import json
from pathlib import Path
from collections import Counter

BASE_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")


def find_all_pages():
    pages = []
    for entry in sorted(os.listdir(BASE_DIR)):
        full = BASE_DIR / entry
        if full.is_dir() and (full / "index.html").exists():
            if entry in ("cleanup", "recovery_documentation", "categories", "articles"):
                continue
            pages.append(("tool", entry, full / "index.html"))

    articles_dir = BASE_DIR / "articles"
    if articles_dir.exists():
        for entry in sorted(os.listdir(articles_dir)):
            full = articles_dir / entry
            if full.is_dir() and (full / "index.html").exists():
                pages.append(("article", f"articles/{entry}", full / "index.html"))

    return pages


def extract_headings(content):
    """Extract all heading tags with their level and text content."""
    headings = []

    # Match h1-h6 tags with their content
    pattern = r'<(h[1-6])([^>]*)>(.*?)</\1>'
    for m in re.finditer(pattern, content, re.DOTALL | re.IGNORECASE):
        tag = m.group(1).lower()
        attrs = m.group(2)
        text = re.sub(r'<[^>]+>', '', m.group(3)).strip()  # Strip inner HTML tags
        level = int(tag[1])
        headings.append({
            "tag": tag,
            "level": level,
            "text": text,
            "position": m.start(),
        })

    return headings


def audit_page(filepath, page_type, slug):
    """Audit heading hierarchy for a single page."""
    issues = []
    fixes = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        issues.append(f"Could not read: {e}")
        return issues, fixes, None

    original = content
    headings = extract_headings(content)

    if not headings:
        issues.append("NO HEADINGS: Page has no heading tags at all")
        return issues, fixes, None

    # Check for exactly one h1
    h1s = [h for h in headings if h["level"] == 1]
    if len(h1s) == 0:
        issues.append("MISSING H1: No <h1> tag found")
    elif len(h1s) > 1:
        issues.append(f"MULTIPLE H1: Found {len(h1s)} <h1> tags")
        # Show the duplicates
        for h in h1s:
            text_preview = h["text"][:60] + "..." if len(h["text"]) > 60 else h["text"]
            issues.append(f"  H1 at pos {h['position']}: \"{text_preview}\"")

        # Fix: Convert all but the first h1 to h2
        # We need to be careful - only change extra h1s to h2
        first_h1_seen = False
        for h in headings:
            if h["level"] == 1:
                if first_h1_seen:
                    # This is a duplicate h1, convert to h2
                    old_open = f'<h1'
                    old_close = '</h1>'
                    # Find this specific h1 by position
                    pos = h["position"]
                    # Find the opening and closing tags
                    open_end = content.find('>', pos) + 1
                    close_start = content.find('</h1>', open_end)
                    if close_start > 0:
                        # Replace opening h1 with h2
                        content = content[:pos] + content[pos:open_end].replace('<h1', '<h2', 1) + content[open_end:close_start] + '</h2>' + content[close_start + 5:]
                        fixes.append(f"converted_duplicate_h1_to_h2")
                else:
                    first_h1_seen = True

    # Check for empty headings
    empty_headings = [h for h in headings if h["text"].strip() == ""]
    if empty_headings:
        issues.append(f"EMPTY HEADINGS: {len(empty_headings)} heading(s) with no text")
        # Remove empty headings
        for h in reversed(empty_headings):  # reversed to preserve positions
            pos = h["position"]
            tag = h["tag"]
            close_tag = f'</{tag}>'
            close_pos = content.find(close_tag, pos)
            if close_pos > 0:
                full_tag = content[pos:close_pos + len(close_tag)]
                content = content.replace(full_tag, '', 1)
                fixes.append(f"removed_empty_{tag}")

    # Check for skipped heading levels
    # Re-extract headings after any modifications
    headings_final = extract_headings(content)
    prev_level = 0
    skips = []
    for h in headings_final:
        if h["text"].strip() == "":
            continue
        level = h["level"]
        if prev_level > 0 and level > prev_level + 1:
            skips.append(f"h{prev_level} -> h{level} (skipped h{prev_level + 1})")
        prev_level = level

    if skips:
        issues.append(f"SKIPPED LEVELS: {len(skips)} heading level skip(s)")
        for skip in skips[:5]:
            issues.append(f"  {skip}")
        if len(skips) > 5:
            issues.append(f"  ... and {len(skips) - 5} more")

    # Check h2 presence
    h2s = [h for h in headings_final if h["level"] == 2]
    if len(h2s) == 0 and len(headings_final) > 1:
        issues.append("NO H2: Page has headings but no <h2> sections")

    modified = content != original
    return issues, fixes, content if modified else None


def main():
    pages = find_all_pages()
    print(f"Found {len(pages)} pages to audit")

    stats = {
        "total": len(pages),
        "no_headings": 0,
        "missing_h1": 0,
        "multiple_h1": 0,
        "empty_headings": 0,
        "skipped_levels": 0,
        "no_h2": 0,
        "files_modified": 0,
        "total_fixes": 0,
    }

    all_issues = []

    for page_type, slug, filepath in pages:
        issues, fixes, new_content = audit_page(filepath, page_type, slug)

        if issues:
            all_issues.append((f"{slug}/index.html", issues))
            for issue in issues:
                if "NO HEADINGS" in issue:
                    stats["no_headings"] += 1
                elif "MISSING H1" in issue:
                    stats["missing_h1"] += 1
                elif "MULTIPLE H1" in issue:
                    stats["multiple_h1"] += 1
                elif "EMPTY HEADINGS" in issue:
                    stats["empty_headings"] += 1
                elif "SKIPPED LEVELS" in issue:
                    stats["skipped_levels"] += 1
                elif "NO H2" in issue:
                    stats["no_h2"] += 1

        if new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            stats["files_modified"] += 1
            stats["total_fixes"] += len(fixes)

    # Print report
    print("\n" + "=" * 70)
    print("CYCLE 4: HEADING HIERARCHY AUDIT REPORT")
    print("=" * 70)
    print(f"Total pages audited:        {stats['total']}")
    print(f"No headings at all:         {stats['no_headings']}")
    print(f"Missing H1:                 {stats['missing_h1']}")
    print(f"Multiple H1:                {stats['multiple_h1']}")
    print(f"Empty headings:             {stats['empty_headings']}")
    print(f"Skipped heading levels:     {stats['skipped_levels']}")
    print(f"No H2 sections:             {stats['no_h2']}")
    print(f"Files modified (fixes):     {stats['files_modified']}")
    print(f"Total fixes applied:        {stats['total_fixes']}")

    if all_issues:
        print(f"\n--- ISSUES ({len(all_issues)} pages) ---")

        # Group by issue type
        multiple_h1 = [(p, i) for p, i in all_issues if any("MULTIPLE H1" in x for x in i)]
        empty = [(p, i) for p, i in all_issues if any("EMPTY HEADING" in x for x in i)]
        skipped = [(p, i) for p, i in all_issues if any("SKIPPED LEVELS" in x for x in i)]
        missing_h1 = [(p, i) for p, i in all_issues if any("MISSING H1" in x for x in i)]

        if multiple_h1:
            print(f"\n  Multiple H1 ({len(multiple_h1)} pages):")
            for p, issues in multiple_h1[:10]:
                h1_count = [i for i in issues if "MULTIPLE H1" in i][0]
                print(f"    {p}: {h1_count}")
            if len(multiple_h1) > 10:
                print(f"    ... and {len(multiple_h1) - 10} more")

        if empty:
            print(f"\n  Empty Headings ({len(empty)} pages):")
            for p, issues in empty[:10]:
                print(f"    {p}")

        if skipped:
            print(f"\n  Skipped Levels ({len(skipped)} pages):")
            for p, issues in skipped[:10]:
                skip_detail = [i for i in issues if "SKIPPED LEVELS" in i][0]
                print(f"    {p}: {skip_detail}")
            if len(skipped) > 10:
                print(f"    ... and {len(skipped) - 10} more")

        if missing_h1:
            print(f"\n  Missing H1 ({len(missing_h1)} pages):")
            for p, issues in missing_h1[:10]:
                print(f"    {p}")

    # Save report
    report_path = BASE_DIR / "audit_cycle4_report.json"
    with open(report_path, 'w') as f:
        json.dump({
            "stats": stats,
            "issues": [(p, i) for p, i in all_issues],
        }, f, indent=2)
    print(f"\nFull report saved to: {report_path}")


if __name__ == "__main__":
    main()
