#!/usr/bin/env python3
"""
File Size Audit Script for zovo-tools repo.
Scans all HTML files, flags oversized ones, reports top 50 largest.
Author: Michael Lip
"""

import os
import json

REPO = "/Users/mike/zovo-workspaces/zovo-tools"
RESULTS = []

def human_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def count_pattern(filepath, pattern):
    """Count occurrences of a pattern in file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        return content.count(pattern)
    except:
        return 0

def main():
    total_size = 0
    total_files = 0
    over_500k = []
    over_200k = []

    for root, dirs, files in os.walk(REPO):
        # Skip .git and node_modules
        dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules', '.github')]

        for fname in files:
            if not fname.endswith('.html'):
                continue

            filepath = os.path.join(root, fname)
            size = os.path.getsize(filepath)
            total_size += size
            total_files += 1

            rel_path = os.path.relpath(filepath, REPO)

            # Count duplication indicators
            doctype_count = count_pattern(filepath, '<!DOCTYPE')
            html_close_count = count_pattern(filepath, '</html>')
            body_close_count = count_pattern(filepath, '</body>')

            entry = {
                'path': rel_path,
                'size': size,
                'size_human': human_size(size),
                'doctype_count': doctype_count,
                'html_close_count': html_close_count,
                'body_close_count': body_close_count,
            }

            RESULTS.append(entry)

            if size > 500 * 1024:
                over_500k.append(entry)
            elif size > 200 * 1024:
                over_200k.append(entry)

    # Sort by size descending
    RESULTS.sort(key=lambda x: x['size'], reverse=True)
    over_500k.sort(key=lambda x: x['size'], reverse=True)
    over_200k.sort(key=lambda x: x['size'], reverse=True)

    print("=" * 80)
    print("ZOVO TOOLS - FILE SIZE AUDIT REPORT")
    print("=" * 80)
    print(f"\nTotal HTML files scanned: {total_files}")
    print(f"Total HTML size: {human_size(total_size)}")
    print(f"Files over 500KB: {len(over_500k)}")
    print(f"Files over 200KB (but under 500KB): {len(over_200k)}")

    print(f"\n{'=' * 80}")
    print("TOP 50 LARGEST FILES")
    print(f"{'=' * 80}")
    print(f"{'#':<4} {'Size':<12} {'DOCTYPE':<8} {'</html>':<8} {'</body>':<8} {'Path'}")
    print("-" * 80)

    for i, entry in enumerate(RESULTS[:50]):
        flag = ""
        if entry['doctype_count'] > 1:
            flag = " ** DUPLICATED"
        if entry['html_close_count'] > 1:
            flag += " ** MULTI-CLOSE"
        print(f"{i+1:<4} {entry['size_human']:<12} {entry['doctype_count']:<8} {entry['html_close_count']:<8} {entry['body_close_count']:<8} {entry['path']}{flag}")

    # Files with multiple DOCTYPE (clear duplication)
    duplicated = [e for e in RESULTS if e['doctype_count'] > 1]
    print(f"\n{'=' * 80}")
    print(f"FILES WITH MULTIPLE <!DOCTYPE> (duplicated content): {len(duplicated)}")
    print(f"{'=' * 80}")
    for entry in duplicated[:30]:
        print(f"  {entry['size_human']:<10} {entry['doctype_count']}x DOCTYPE  {entry['path']}")
    if len(duplicated) > 30:
        print(f"  ... and {len(duplicated) - 30} more")

    # Files with multiple </html>
    multi_close = [e for e in RESULTS if e['html_close_count'] > 1]
    print(f"\n{'=' * 80}")
    print(f"FILES WITH MULTIPLE </html> TAGS: {len(multi_close)}")
    print(f"{'=' * 80}")
    for entry in multi_close[:30]:
        print(f"  {entry['size_human']:<10} {entry['html_close_count']}x </html>  {entry['path']}")
    if len(multi_close) > 30:
        print(f"  ... and {len(multi_close) - 30} more")

    # Save full results as JSON for later use
    with open(os.path.join(REPO, 'audit_results.json'), 'w') as f:
        json.dump({
            'total_files': total_files,
            'total_size': total_size,
            'total_size_human': human_size(total_size),
            'over_500k_count': len(over_500k),
            'over_200k_count': len(over_200k),
            'duplicated_count': len(duplicated),
            'multi_close_count': len(multi_close),
            'all_files': RESULTS,
        }, f, indent=2)

    print(f"\nFull results saved to audit_results.json")

if __name__ == '__main__':
    main()
