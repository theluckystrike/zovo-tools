#!/usr/bin/env python3
"""
Fix Canonical Domain URLs
Replace zovo.one/free-tools/ with tools.zovo.one/
"""

import os
import re
from pathlib import Path

def fix_canonical_domain(file_path):
    """Fix canonical domain for a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Replace incorrect canonical domains
        content = re.sub(
            r'https://zovo\.one/free-tools/([^"\']*)',
            r'https://tools.zovo.one/\1',
            content
        )

        # Also fix OpenGraph URLs
        content = re.sub(
            r'property="og:url"[^>]*content="https://zovo\.one/free-tools/([^"\']*)"',
            r'property="og:url" content="https://tools.zovo.one/\1"',
            content
        )

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"Error fixing {file_path}: {e}")
        return False

def main():
    print("FIXING CANONICAL DOMAIN URLS")
    print("="*40)

    base_path = Path("/Users/mike/zovo-workspaces/zovo-tools")
    fixed_count = 0

    # Fix tools
    print("Processing tools...")
    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name != 'articles':
            index_file = item / 'index.html'
            if index_file.exists():
                if fix_canonical_domain(index_file):
                    fixed_count += 1

    # Fix articles
    print("Processing articles...")
    articles_dir = base_path / 'articles'
    if articles_dir.exists():
        for item in articles_dir.iterdir():
            if item.is_dir():
                index_file = item / 'index.html'
                if index_file.exists():
                    if fix_canonical_domain(index_file):
                        fixed_count += 1

    print(f"\nFixed canonical domains in {fixed_count} files")
    print("Domain fix complete!")

if __name__ == "__main__":
    main()