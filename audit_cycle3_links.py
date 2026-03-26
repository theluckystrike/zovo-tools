#!/usr/bin/env python3
"""
Cycle 3: Internal Link Audit
Checks for broken internal links across all tool and article pages.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path("/Users/mike/zovo-workspaces/zovo-tools")


def find_all_pages():
    """Find all tool and article index.html files."""
    pages = []
    for entry in sorted(os.listdir(BASE_DIR)):
        full = BASE_DIR / entry
        if full.is_dir() and (full / "index.html").exists():
            if entry in ("cleanup", "recovery_documentation", "categories"):
                continue
            if entry == "articles":
                continue
            pages.append(("tool", entry, full / "index.html"))

    articles_dir = BASE_DIR / "articles"
    if articles_dir.exists():
        for entry in sorted(os.listdir(articles_dir)):
            full = articles_dir / entry
            if full.is_dir() and (full / "index.html").exists():
                pages.append(("article", f"articles/{entry}", full / "index.html"))

    return pages


def get_existing_slugs():
    """Build a set of all existing tool and article slugs."""
    tool_slugs = set()
    article_slugs = set()

    for entry in os.listdir(BASE_DIR):
        full = BASE_DIR / entry
        if full.is_dir() and (full / "index.html").exists():
            if entry not in ("cleanup", "recovery_documentation", "categories", "articles"):
                tool_slugs.add(entry)

    articles_dir = BASE_DIR / "articles"
    if articles_dir.exists():
        for entry in os.listdir(articles_dir):
            full = articles_dir / entry
            if full.is_dir() and (full / "index.html").exists():
                article_slugs.add(entry)

    return tool_slugs, article_slugs


def extract_internal_links(content):
    """Extract all internal links from HTML content."""
    links = []

    # Match href attributes
    for m in re.finditer(r'href=["\']([^"\']*)["\']', content, re.IGNORECASE):
        url = m.group(1)

        # Internal links to free-tools
        if '/free-tools/' in url:
            slug_match = re.search(r'/free-tools/([a-z0-9-]+)/?', url)
            if slug_match:
                links.append(("tool", slug_match.group(1), url, m.start()))

        # Internal links to articles
        if '/articles/' in url:
            slug_match = re.search(r'/articles/([a-z0-9-]+)/?', url)
            if slug_match:
                links.append(("article", slug_match.group(1), url, m.start()))

    return links


def main():
    pages = find_all_pages()
    tool_slugs, article_slugs = get_existing_slugs()

    print(f"Found {len(pages)} pages to scan")
    print(f"Known tool slugs: {len(tool_slugs)}")
    print(f"Known article slugs: {len(article_slugs)}")

    stats = {
        "total_pages": len(pages),
        "total_internal_links": 0,
        "broken_tool_links": 0,
        "broken_article_links": 0,
        "pages_with_broken_links": 0,
    }

    all_broken = []
    broken_slug_counts = defaultdict(int)

    for page_type, slug, filepath in pages:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
        except Exception:
            continue

        links = extract_internal_links(content)
        stats["total_internal_links"] += len(links)

        page_broken = []
        for link_type, link_slug, full_url, pos in links:
            if link_type == "tool":
                if link_slug not in tool_slugs:
                    page_broken.append((link_type, link_slug, full_url))
                    stats["broken_tool_links"] += 1
                    broken_slug_counts[link_slug] += 1
            elif link_type == "article":
                if link_slug not in article_slugs:
                    page_broken.append((link_type, link_slug, full_url))
                    stats["broken_article_links"] += 1
                    broken_slug_counts[link_slug] += 1

        if page_broken:
            stats["pages_with_broken_links"] += 1
            all_broken.append((f"{slug}/index.html", page_broken))

    # Print report
    print("\n" + "=" * 70)
    print("CYCLE 3: INTERNAL LINK AUDIT REPORT")
    print("=" * 70)
    print(f"Total pages scanned:        {stats['total_pages']}")
    print(f"Total internal links found: {stats['total_internal_links']}")
    print(f"Broken tool links:          {stats['broken_tool_links']}")
    print(f"Broken article links:       {stats['broken_article_links']}")
    print(f"Pages with broken links:    {stats['pages_with_broken_links']}")

    if all_broken:
        # Sort broken slugs by frequency
        print(f"\n--- MOST REFERENCED BROKEN SLUGS ---")
        for slug, count in sorted(broken_slug_counts.items(), key=lambda x: -x[1])[:30]:
            print(f"  {slug}: referenced {count} times")

        print(f"\n--- BROKEN LINKS BY PAGE ({len(all_broken)} pages) ---")
        for path, broken_links in all_broken[:50]:
            print(f"\n  {path}:")
            seen = set()
            for link_type, link_slug, full_url in broken_links:
                key = f"{link_type}:{link_slug}"
                if key not in seen:
                    seen.add(key)
                    print(f"    [{link_type}] {link_slug} -> {full_url[:80]}")
        if len(all_broken) > 50:
            print(f"\n  ... and {len(all_broken) - 50} more pages")

    # Save report
    report_path = BASE_DIR / "audit_cycle3_report.json"
    with open(report_path, 'w') as f:
        json.dump({
            "stats": stats,
            "broken_slug_counts": dict(broken_slug_counts),
            "broken_links": [(p, [(t, s, u) for t, s, u in bl]) for p, bl in all_broken],
        }, f, indent=2)
    print(f"\nFull report saved to: {report_path}")


if __name__ == "__main__":
    main()
