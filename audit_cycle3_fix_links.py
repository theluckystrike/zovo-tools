#!/usr/bin/env python3
"""
Cycle 3: Fix broken internal links.
Maps broken slugs to correct existing slugs where possible.
Removes links to truly non-existent pages only when necessary.
"""

import os
import re
import json
from pathlib import Path

BASE_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")

# Mapping of broken slug -> correct slug
SLUG_CORRECTIONS = {
    # "intelligent-" prefix -> "ai-" prefix
    "intelligent-detector": "ai-detector",
    "intelligent-image-generator": "ai-image-generator",
    "intelligent-headshot-generator": "ai-headshot-generator",
    "intelligent-logo-generator": "ai-logo-generator",
    # Missing suffix
    "contrast-checker": "color-contrast-checker",
    "salary-to-hourly": "salary-to-hourly-calculator",
    "text-compare": "text-diff-checker",
    "binary-to-decimal": "binary-to-decimal-converter",
    "hex-to-decimal": "hex-converter",
    "hex-to-rgb": "hex-to-rgb-converter",
    "hex-calculator": "hex-converter",
    "json-to-csv": "json-to-csv-converter",
    "epoch-converter": "epoch-time-converter",
    "unix-timestamp-converter": "timestamp-converter",
    "auto-loan-calculator": "car-loan-calculator",
    "ip-address-lookup": "ip-lookup",
    "-body-weight-calculator": "ideal-body-weight-calculator",
    "-weight-calculator": "ideal-body-weight-calculator",
    "usps-shipping-calculator": "usps-postage-calculator",
    "texas-salary-calculator": "texas-payroll-calculator",
    "maryland-salary-calculator": "maryland-payroll-calculator",
    "georgia-paycheck-calculator": "georgia-salary-calculator",
    "texas-paycheck-calculator": "texas-payroll-calculator",
    "svg-improver": "svg-optimizer",
    "postage-calculator": "usps-postage-calculator",
    "html-minifier": "html-formatter",
    # "articles" as a tool slug -> this is a navigation issue, /free-tools/articles/ should be removed or pointed elsewhere
}

# These broken links should be REMOVED (link text kept, href removed) because no equivalent exists
# We won't remove these -- just leave them as-is for now since they point to pages that might be created later
# We ONLY fix the ones we have clear mappings for.


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


def fix_links_in_page(filepath):
    """Fix broken internal links in a single page."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original = content
    fixes = []

    for broken_slug, correct_slug in SLUG_CORRECTIONS.items():
        # Fix both relative and absolute URL patterns
        patterns = [
            (f'/free-tools/{broken_slug}/', f'/free-tools/{correct_slug}/'),
            (f'/free-tools/{broken_slug}"', f'/free-tools/{correct_slug}/"'),
        ]

        for old, new in patterns:
            if old in content:
                count = content.count(old)
                content = content.replace(old, new)
                fixes.append(f"Fixed {count}x: {broken_slug} -> {correct_slug}")

    # Special fix: /free-tools/articles/ -> /articles/ (wrong path prefix)
    if '/free-tools/articles/' in content:
        count = content.count('/free-tools/articles/')
        # Replace with correct articles path
        content = content.replace('/free-tools/articles/', '/articles/')
        fixes.append(f"Fixed {count}x: /free-tools/articles/ -> /articles/")

    modified = content != original
    return fixes, content if modified else None


def main():
    pages = find_all_pages()
    print(f"Scanning {len(pages)} pages for broken links to fix")

    total_fixes = 0
    files_modified = 0

    for page_type, slug, filepath in pages:
        fixes, new_content = fix_links_in_page(filepath)

        if new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_modified += 1
            total_fixes += len(fixes)
            for fix in fixes:
                print(f"  {slug}: {fix}")

    print(f"\n{'=' * 70}")
    print(f"CYCLE 3: LINK FIX SUMMARY")
    print(f"{'=' * 70}")
    print(f"Files modified:  {files_modified}")
    print(f"Total fixes:     {total_fixes}")


if __name__ == "__main__":
    main()
