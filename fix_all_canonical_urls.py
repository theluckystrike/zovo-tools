#!/usr/bin/env python3
"""
Comprehensive Canonical URL Fix
Add or fix canonical URLs for all pages in the ecosystem
"""

import os
import re
from pathlib import Path

def fix_canonical_url(file_path, expected_path):
    """Fix canonical URL for a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        canonical_url = f"https://tools.zovo.one/{expected_path}/"

        # Check if canonical URL already exists
        existing_canonical = re.search(r'<link\s+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', content)

        if existing_canonical:
            current_url = existing_canonical.group(1)
            if current_url != canonical_url:
                # Replace incorrect canonical URL
                content = re.sub(
                    r'<link\s+rel=["\']canonical["\'][^>]*href=["\'][^"\']+["\'][^>]*>',
                    f'<link rel="canonical" href="{canonical_url}">',
                    content
                )
                return content, 'fixed'
            else:
                return content, 'correct'
        else:
            # Add missing canonical URL
            canonical_tag = f'<link rel="canonical" href="{canonical_url}">'

            # Try to add after other link/meta tags
            if '</head>' in content:
                # Find the best position to insert
                head_content = content[content.find('<head>'):content.find('</head>')]
                if '<meta' in head_content or '<link' in head_content:
                    # Add after last meta or link tag
                    last_meta_pos = max(
                        head_content.rfind('</meta>') if '</meta>' in head_content else -1,
                        head_content.rfind('<meta') if '<meta' in head_content else -1,
                        head_content.rfind('<link') if '<link' in head_content else -1
                    )

                    if last_meta_pos != -1:
                        # Find end of that tag
                        insertion_point = content.find('>', content.find('<head>') + last_meta_pos) + 1
                        content = content[:insertion_point] + f'\n    {canonical_tag}' + content[insertion_point:]
                    else:
                        # Just add before </head>
                        content = content.replace('</head>', f'    {canonical_tag}\n</head>')
                else:
                    # Add before </head>
                    content = content.replace('</head>', f'    {canonical_tag}\n</head>')

                return content, 'added'

        return content, 'no_change'

    except Exception as e:
        return None, f'error: {e}'

def main():
    print("COMPREHENSIVE CANONICAL URL FIX")
    print("="*40)

    base_path = Path("/Users/mike/zovo-workspaces/zovo-tools")

    stats = {
        'added': 0,
        'fixed': 0,
        'correct': 0,
        'errors': 0,
        'no_change': 0
    }

    # Fix tools
    print("Processing tools...")
    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name != 'articles':
            index_file = item / 'index.html'
            if index_file.exists():
                new_content, status = fix_canonical_url(index_file, item.name)

                if new_content and status != 'correct' and status != 'no_change':
                    try:
                        with open(index_file, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                    except Exception as e:
                        status = f'error: {e}'

                if status.startswith('error'):
                    stats['errors'] += 1
                else:
                    stats[status] += 1

    # Fix articles
    print("Processing articles...")
    articles_dir = base_path / 'articles'
    if articles_dir.exists():
        for item in articles_dir.iterdir():
            if item.is_dir():
                index_file = item / 'index.html'
                if index_file.exists():
                    expected_path = f"articles/{item.name}"
                    new_content, status = fix_canonical_url(index_file, expected_path)

                    if new_content and status != 'correct' and status != 'no_change':
                        try:
                            with open(index_file, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                        except Exception as e:
                            status = f'error: {e}'

                    if status.startswith('error'):
                        stats['errors'] += 1
                    else:
                        stats[status] += 1

    print("\nCanonical URL Fix Results:")
    print(f"  Added: {stats['added']}")
    print(f"  Fixed: {stats['fixed']}")
    print(f"  Already correct: {stats['correct']}")
    print(f"  No change: {stats['no_change']}")
    print(f"  Errors: {stats['errors']}")

    total_processed = sum(stats.values())
    print(f"\nTotal pages processed: {total_processed}")

if __name__ == "__main__":
    main()