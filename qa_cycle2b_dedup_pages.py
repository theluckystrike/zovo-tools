#!/usr/bin/env python3
"""
Cycle 2b: Fix files with entire-page duplication.
These files have the complete HTML document concatenated multiple times.
Keep only the FIRST complete <!DOCTYPE html>...</html> document.
"""

import os
import re

BASE_DIR = '/Users/mike/zovo-workspaces/zovo-tools'


def find_all_html_files():
    files = []
    for entry in sorted(os.listdir(BASE_DIR)):
        path = os.path.join(BASE_DIR, entry)
        if os.path.isdir(path):
            idx = os.path.join(path, 'index.html')
            if os.path.isfile(idx):
                files.append(idx)
            if entry == 'articles':
                for art in sorted(os.listdir(path)):
                    art_idx = os.path.join(path, art, 'index.html')
                    if os.path.isfile(art_idx):
                        files.append(art_idx)
    return files


def fix_duplicate_pages(filepath):
    """Keep only the first complete HTML document."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    html_close_count = content.count('</html>')
    if html_close_count <= 1:
        return None

    original_size = len(content)

    # Strategy: Find the FIRST </html> and keep everything up to and including it
    first_close = content.find('</html>')
    if first_close < 0:
        return None

    # Keep everything up to and including the first </html> plus a newline
    new_content = content[:first_close + len('</html>')] + '\n'

    # Verify the trimmed content still has basic structure
    if '<head' not in new_content or '<body' not in new_content:
        print(f"  WARNING: Trimmed content missing <head> or <body> - skipping {filepath}")
        return None

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    new_size = len(new_content)
    saved = original_size - new_size
    rel_path = os.path.relpath(filepath, BASE_DIR)

    return {
        'file': rel_path,
        'html_closes': html_close_count,
        'original_size': original_size,
        'new_size': new_size,
        'saved': saved
    }


def main():
    print("=" * 70)
    print("CYCLE 2b: Fix Entire-Page Duplication")
    print("=" * 70)

    files = find_all_html_files()
    print(f"\nScanning {len(files)} HTML files...\n")

    fixed = 0
    total_saved = 0

    for filepath in files:
        result = fix_duplicate_pages(filepath)
        if result:
            fixed += 1
            total_saved += result['saved']
            print(f"  FIXED: {result['file']}")
            print(f"    {result['html_closes']} copies -> 1 copy")
            print(f"    {result['original_size']:,} -> {result['new_size']:,} bytes (saved {result['saved']:,})")

    print("\n" + "=" * 70)
    print("CYCLE 2b SUMMARY")
    print("=" * 70)
    print(f"Files scanned:  {len(files)}")
    print(f"Files fixed:    {fixed}")
    print(f"Bytes saved:    {total_saved:,}")


if __name__ == '__main__':
    main()
