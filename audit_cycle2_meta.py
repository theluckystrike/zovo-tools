#!/usr/bin/env python3
"""
Cycle 2: Meta Tag Audit (Safe version)
Checks every tool page for required meta tags, OG tags, canonical links, and author attribution.
Fixes duplicate meta descriptions and canonical links safely.
Key safety: Fixes malformed HTML (unclosed tags) BEFORE removing duplicates.
"""

import os
import re
import json
from pathlib import Path

BASE_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")


def find_all_pages():
    """Find all tool and article index.html files."""
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


def fix_malformed_tags(content):
    """Fix common malformed HTML tag issues like missing closing > brackets."""
    fixed = content
    fixes = []

    # Fix: <link ... rel="canonical"<meta  (missing > before <meta)
    # Pattern: a link tag ending with canonical" or canonical' followed by < instead of >
    pattern = r'(<link\s+[^>]*?rel=["\']canonical["\'])(<)'
    match = re.search(pattern, fixed, re.IGNORECASE)
    while match:
        fixed = fixed[:match.end(1)] + '>' + fixed[match.start(2):]
        fixes.append("fixed_unclosed_canonical_tag")
        match = re.search(pattern, fixed, re.IGNORECASE)

    # Fix: <link ... href="..."<meta  (missing > on link tags)
    pattern2 = r'(<link\s+[^>]*?href=["\'][^"\']*["\'])(<)'
    match2 = re.search(pattern2, fixed, re.IGNORECASE)
    while match2:
        fixed = fixed[:match2.end(1)] + '>' + fixed[match2.start(2):]
        fixes.append("fixed_unclosed_link_tag")
        match2 = re.search(pattern2, fixed, re.IGNORECASE)

    return fixed, fixes


def find_meta_descriptions(content):
    """Find all meta description tags with their content and position."""
    results = []

    # Pattern 1: name first, then content
    for m in re.finditer(
        r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\'][^>]*/?>',
        content, re.IGNORECASE
    ):
        results.append({"content": m.group(1), "full_tag": m.group(0), "start": m.start()})

    # Pattern 2: content first, then name
    for m in re.finditer(
        r'<meta\s+content=["\']([^"\']*?)["\']\s+name=["\']description["\'][^>]*/?>',
        content, re.IGNORECASE
    ):
        results.append({"content": m.group(1), "full_tag": m.group(0), "start": m.start()})

    # Sort by position
    results.sort(key=lambda x: x["start"])
    return results


def find_og_titles(content):
    """Find all og:title meta tags."""
    results = []

    for m in re.finditer(
        r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']*)["\'][^>]*/?>',
        content, re.IGNORECASE
    ):
        results.append({"content": m.group(1), "full_tag": m.group(0)})

    for m in re.finditer(
        r'<meta\s+content=["\']([^"\']*?)["\']\s+property=["\']og:title["\'][^>]*/?>',
        content, re.IGNORECASE
    ):
        results.append({"content": m.group(1), "full_tag": m.group(0)})

    return results


def find_canonicals(content):
    """Find all canonical link tags."""
    results = []

    for m in re.finditer(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\'][^>]*/?>',
        content, re.IGNORECASE
    ):
        results.append({"href": m.group(1), "full_tag": m.group(0), "start": m.start()})

    for m in re.finditer(
        r'<link\s+href=["\']([^"\']*?)["\']\s+rel=["\']canonical["\'][^>]*/?>',
        content, re.IGNORECASE
    ):
        results.append({"href": m.group(1), "full_tag": m.group(0), "start": m.start()})

    # Deduplicate by position
    seen = set()
    unique = []
    for r in results:
        if r["start"] not in seen:
            seen.add(r["start"])
            unique.append(r)

    unique.sort(key=lambda x: x["start"])
    return unique


def find_authors(content):
    """Find all author meta tags."""
    results = []

    for m in re.finditer(
        r'<meta\s+name=["\']author["\']\s+content=["\']([^"\']*)["\'][^>]*/?>',
        content, re.IGNORECASE
    ):
        results.append(m.group(1))

    for m in re.finditer(
        r'<meta\s+content=["\']([^"\']*?)["\']\s+name=["\']author["\'][^>]*/?>',
        content, re.IGNORECASE
    ):
        results.append(m.group(1))

    return results


def audit_page(filepath, page_type, slug):
    """Audit a single page for meta tag issues."""
    issues = []
    all_fixes = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        issues.append(f"Could not read: {e}")
        return issues, all_fixes, None

    original = content

    # Step 1: Fix malformed HTML first
    content, html_fixes = fix_malformed_tags(content)
    all_fixes.extend(html_fixes)

    # Step 2: Audit meta descriptions
    descs = find_meta_descriptions(content)
    if len(descs) == 0:
        issues.append("MISSING: meta description")
    elif any(d["content"].strip() == "" for d in descs):
        issues.append("EMPTY: meta description")

    if len(descs) > 1:
        issues.append(f"DUPLICATE: {len(descs)} meta description tags")
        # Keep the longest content description
        best = max(descs, key=lambda d: len(d["content"]))
        for d in descs:
            if d["full_tag"] != best["full_tag"] and d["full_tag"] in content:
                content = content.replace(d["full_tag"], '', 1)
                all_fixes.append("removed_duplicate_meta_desc")

    # Step 3: Audit og:title
    og_titles = find_og_titles(content)
    if len(og_titles) == 0:
        issues.append("MISSING: og:title")
    elif any(t["content"].strip() == "" for t in og_titles):
        issues.append("EMPTY: og:title")

    # Step 4: Audit canonical links
    cans = find_canonicals(content)
    if len(cans) == 0:
        issues.append("MISSING: canonical link")

    if len(cans) > 1:
        issues.append(f"DUPLICATE: {len(cans)} canonical links")
        # Keep the one with the best URL (prefer zovo.one/free-tools/ pattern)
        best = cans[0]
        for c in cans:
            if "zovo.one/free-tools/" in c["href"]:
                best = c
                break
        for c in cans:
            if c["full_tag"] != best["full_tag"] and c["full_tag"] in content:
                content = content.replace(c["full_tag"], '', 1)
                all_fixes.append("removed_duplicate_canonical")

    # Step 5: Audit author
    authors = find_authors(content)
    if len(authors) == 0:
        issues.append("MISSING: author meta tag")

    modified = content != original
    return issues, all_fixes, content if modified else None


def main():
    pages = find_all_pages()
    print(f"Found {len(pages)} pages to audit")

    stats = {
        "total": len(pages),
        "missing_meta_desc": 0,
        "empty_meta_desc": 0,
        "duplicate_meta_desc": 0,
        "missing_og_title": 0,
        "empty_og_title": 0,
        "missing_canonical": 0,
        "duplicate_canonical": 0,
        "missing_author": 0,
        "fixed_malformed_html": 0,
        "files_modified": 0,
        "total_fixes": 0,
    }

    all_issues = []

    for page_type, slug, filepath in pages:
        issues, fixes, new_content = audit_page(filepath, page_type, slug)

        if issues:
            all_issues.append((f"{slug}/index.html", issues))
            for issue in issues:
                if "MISSING: meta description" in issue:
                    stats["missing_meta_desc"] += 1
                elif "EMPTY: meta description" in issue:
                    stats["empty_meta_desc"] += 1
                elif "DUPLICATE:" in issue and "meta description" in issue:
                    stats["duplicate_meta_desc"] += 1
                elif "MISSING: og:title" in issue:
                    stats["missing_og_title"] += 1
                elif "EMPTY: og:title" in issue:
                    stats["empty_og_title"] += 1
                elif "MISSING: canonical" in issue:
                    stats["missing_canonical"] += 1
                elif "DUPLICATE:" in issue and "canonical" in issue:
                    stats["duplicate_canonical"] += 1
                elif "MISSING: author" in issue:
                    stats["missing_author"] += 1

        for fix in fixes:
            if "malformed" in fix or "unclosed" in fix:
                stats["fixed_malformed_html"] += 1

        if new_content is not None:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            stats["files_modified"] += 1
            stats["total_fixes"] += len(fixes)

    # Print report
    print("\n" + "=" * 70)
    print("CYCLE 2: META TAG AUDIT REPORT")
    print("=" * 70)
    print(f"Total pages audited:        {stats['total']}")
    print(f"Missing meta description:   {stats['missing_meta_desc']}")
    print(f"Empty meta description:     {stats['empty_meta_desc']}")
    print(f"Duplicate meta descriptions:{stats['duplicate_meta_desc']}")
    print(f"Missing og:title:           {stats['missing_og_title']}")
    print(f"Empty og:title:             {stats['empty_og_title']}")
    print(f"Missing canonical link:     {stats['missing_canonical']}")
    print(f"Duplicate canonical links:  {stats['duplicate_canonical']}")
    print(f"Missing author meta:        {stats['missing_author']}")
    print(f"Fixed malformed HTML tags:  {stats['fixed_malformed_html']}")
    print(f"Files modified:             {stats['files_modified']}")
    print(f"Total fixes applied:        {stats['total_fixes']}")

    if all_issues:
        print(f"\n--- REMAINING ISSUES ({len(all_issues)} pages) ---")
        # Group by issue type
        missing_desc_pages = []
        missing_og_pages = []
        missing_canonical_pages = []
        missing_author_pages = []
        dup_pages = []

        for path, issues in all_issues:
            for issue in issues:
                if "MISSING: meta description" in issue:
                    missing_desc_pages.append(path)
                elif "MISSING: og:title" in issue:
                    missing_og_pages.append(path)
                elif "MISSING: canonical" in issue:
                    missing_canonical_pages.append(path)
                elif "MISSING: author" in issue:
                    missing_author_pages.append(path)
                elif "DUPLICATE" in issue:
                    dup_pages.append((path, issue))

        if missing_desc_pages:
            print(f"\n  Missing meta description ({len(missing_desc_pages)}):")
            for p in missing_desc_pages[:15]:
                print(f"    {p}")
            if len(missing_desc_pages) > 15:
                print(f"    ... and {len(missing_desc_pages) - 15} more")

        if missing_og_pages:
            print(f"\n  Missing og:title ({len(missing_og_pages)}):")
            for p in missing_og_pages[:15]:
                print(f"    {p}")
            if len(missing_og_pages) > 15:
                print(f"    ... and {len(missing_og_pages) - 15} more")

        if missing_canonical_pages:
            print(f"\n  Missing canonical link ({len(missing_canonical_pages)}):")
            for p in missing_canonical_pages[:15]:
                print(f"    {p}")
            if len(missing_canonical_pages) > 15:
                print(f"    ... and {len(missing_canonical_pages) - 15} more")

        if missing_author_pages:
            print(f"\n  Missing author meta ({len(missing_author_pages)}):")
            for p in missing_author_pages[:15]:
                print(f"    {p}")
            if len(missing_author_pages) > 15:
                print(f"    ... and {len(missing_author_pages) - 15} more")

        if dup_pages:
            print(f"\n  Remaining duplicates ({len(dup_pages)}):")
            for p, issue in dup_pages:
                print(f"    {p}: {issue}")

    # Save report
    report_path = BASE_DIR / "audit_cycle2_report.json"
    with open(report_path, 'w') as f:
        json.dump({
            "stats": stats,
            "issues": [(p, i) for p, i in all_issues],
        }, f, indent=2)
    print(f"\nFull report saved to: {report_path}")


if __name__ == "__main__":
    main()
