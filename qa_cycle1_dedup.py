#!/usr/bin/env python3
"""
Cycle 1: Detect and remove duplicate layer sections in all tool/article HTML files.
Keeps FIRST occurrence of each section, removes subsequent duplicates.
"""

import os
import re
import json
import sys

BASE_DIR = '/Users/mike/zovo-workspaces/zovo-tools'

# Patterns to detect duplicate sections
# Each entry: (name, regex_pattern_to_find_full_section)
SECTION_PATTERNS = [
    ('badge-row', r'<div\s+class="badge-row"[^>]*>.*?</div>\s*(?=<|$)'),
    ('so-questions-section', r'<section\s+class="so-questions-section"[^>]*>.*?</section>'),
    ('wiki-definition-box', r'<section\s+class="wiki-definition-box"[^>]*>.*?</section>'),
    ('compat-table-section', r'<section\s+class="compat-table-section"[^>]*>.*?</section>'),
    ('npm-dashboard', r'<section\s+class="npm-dashboard"[^>]*>.*?</section>'),
    ('original-research', r'<section\s+class="original-research"[^>]*>.*?</section>'),
    ('live-stats', r'<div\s+class="live-stats"[^>]*>.*?</div>\s*(?=<|$)'),
    ('benchmark-chart', r'<div\s+class="benchmark-chart"[^>]*>.*?</div>\s*(?=<|$)'),
    ('video-embed', r'<section\s+class="video-embed"[^>]*>.*?</section>'),
]

def find_all_html_files():
    """Find all index.html files in tool/article directories."""
    files = []
    for entry in sorted(os.listdir(BASE_DIR)):
        path = os.path.join(BASE_DIR, entry)
        if os.path.isdir(path):
            idx = os.path.join(path, 'index.html')
            if os.path.isfile(idx):
                files.append(idx)
            # Check articles subdirectory
            if entry == 'articles':
                for art in sorted(os.listdir(path)):
                    art_idx = os.path.join(path, art, 'index.html')
                    if os.path.isfile(art_idx):
                        files.append(art_idx)
    return files


def count_class_occurrences(content, class_name):
    """Count occurrences of a class attribute in the content."""
    # Match class="class_name" or class="class_name ..."
    pattern = r'class="' + re.escape(class_name) + r'[\s"]'
    return len(re.findall(pattern, content))


def remove_duplicate_sections_simple(content, class_name, tag='section'):
    """
    Remove duplicate sections by finding class markers and keeping only the first.
    Uses a simpler approach: find all start positions, then remove content from 2nd onwards.
    """
    # Build opening tag pattern
    if tag == 'div':
        open_pattern = r'<div\s+class="' + re.escape(class_name) + r'"'
    else:
        open_pattern = r'<' + tag + r'\s+class="' + re.escape(class_name) + r'"'

    close_tag = '</' + tag + '>'

    positions = [(m.start(), m.end()) for m in re.finditer(open_pattern, content)]

    if len(positions) <= 1:
        return content, 0

    # Keep only the first occurrence, remove the rest
    removed = 0
    # Process from last to first to maintain position integrity
    for i in range(len(positions) - 1, 0, -1):
        start = positions[i][0]
        # Find the matching close tag - need to count nesting
        depth = 0
        pos = start
        end = -1

        while pos < len(content):
            # Find next opening or closing tag of same type
            next_open = content.find('<' + tag, pos + 1)
            next_close = content.find(close_tag, pos)

            if tag == 'div':
                next_open = content.find('<div', pos + 1)
                next_close = content.find('</div>', pos)

            if next_close == -1:
                break

            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 1
            else:
                if depth == 0:
                    end = next_close + len(close_tag)
                    break
                else:
                    depth -= 1
                    pos = next_close + 1

        if end > start:
            # Also remove any trailing whitespace/newline
            while end < len(content) and content[end] in '\n\r\t ':
                end += 1
            content = content[:start] + content[end:]
            removed += 1

    return content, removed


def remove_duplicate_ld_json(content):
    """Remove duplicate ld+json blocks with the same @type."""
    pattern = r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>'
    matches = list(re.finditer(pattern, content, re.DOTALL))

    if len(matches) <= 1:
        return content, 0

    # Parse each and track @type
    seen_types = {}
    to_remove = []

    for m in matches:
        try:
            data = json.loads(m.group(1))
            t = data.get('@type', 'unknown')
            # Handle list types by converting to tuple for hashing
            if isinstance(t, list):
                t = tuple(t)
            t = str(t)
            raw = m.group(1).strip()
            if t in seen_types:
                # Check if it's actually a duplicate (same content)
                if raw == seen_types[t]['raw']:
                    to_remove.append(m)
                else:
                    # Different content, same type - keep both but track
                    # Use a counter suffix to allow unique types
                    counter = 2
                    while f"{t}_{counter}" in seen_types:
                        counter += 1
                    seen_types[f"{t}_{counter}"] = {'match': m, 'raw': raw}
            else:
                seen_types[t] = {'match': m, 'raw': raw}
        except (json.JSONDecodeError, AttributeError, TypeError):
            # If we can't parse, check raw string for @type
            type_match = re.search(r'"@type"\s*:\s*"([^"]+)"', m.group(1))
            if type_match:
                t = type_match.group(1)
                raw = m.group(1).strip()
                if t in seen_types:
                    if raw == seen_types[t]['raw']:
                        to_remove.append(m)
                    else:
                        counter = 2
                        while f"{t}_{counter}" in seen_types:
                            counter += 1
                        seen_types[f"{t}_{counter}"] = {'match': m, 'raw': raw}
                else:
                    seen_types[t] = {'match': m, 'raw': raw}

    removed = len(to_remove)
    # Remove from end to start
    for m in reversed(to_remove):
        start = m.start()
        end = m.end()
        # Remove trailing whitespace
        while end < len(content) and content[end] in '\n\r\t ':
            end += 1
        content = content[:start] + content[end:]

    return content, removed


def process_file(filepath):
    """Process a single HTML file, removing duplicate sections."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            original = f.read()
    except Exception as e:
        return {'file': filepath, 'error': str(e), 'fixes': {}}

    content = original
    fixes = {}

    # Process each section pattern
    section_map = {
        'badge-row': 'div',
        'so-questions-section': 'section',
        'wiki-definition-box': 'section',
        'compat-table-section': 'section',
        'npm-dashboard': 'section',
        'original-research': 'section',
        'live-stats': 'div',
        'benchmark-chart': 'div',
        'video-embed': 'section',
    }

    for class_name, tag in section_map.items():
        count = count_class_occurrences(content, class_name)
        if count > 1:
            content, removed = remove_duplicate_sections_simple(content, class_name, tag)
            if removed > 0:
                fixes[class_name] = removed

    # Process duplicate ld+json
    ld_count = content.count('application/ld+json')
    if ld_count > 3:  # Most pages legitimately have 2-3 (WebPage, FAQPage, HowTo, etc.)
        # Check for actual duplicate @types
        content, ld_removed = remove_duplicate_ld_json(content)
        if ld_removed > 0:
            fixes['ld+json-duplicates'] = ld_removed

    # Write back if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return {'file': filepath, 'fixes': fixes, 'saved': len(original) - len(content)}

    return {'file': filepath, 'fixes': {}, 'saved': 0}


def main():
    print("=" * 70)
    print("CYCLE 1: Duplicate Section Detection and Removal")
    print("=" * 70)

    files = find_all_html_files()
    print(f"\nScanning {len(files)} HTML files...\n")

    total_fixes = 0
    total_saved = 0
    files_fixed = 0
    fix_summary = {}

    for i, filepath in enumerate(files):
        result = process_file(filepath)

        if result.get('error'):
            print(f"  ERROR: {result['file']}: {result['error']}")
            continue

        if result['fixes']:
            files_fixed += 1
            saved = result.get('saved', 0)
            total_saved += saved
            rel_path = os.path.relpath(result['file'], BASE_DIR)
            fix_count = sum(result['fixes'].values())
            total_fixes += fix_count

            print(f"  FIXED: {rel_path} - {result['fixes']} (saved {saved:,} bytes)")

            for pattern, count in result['fixes'].items():
                fix_summary[pattern] = fix_summary.get(pattern, 0) + count

        if (i + 1) % 100 == 0:
            print(f"  ... processed {i+1}/{len(files)} files ...")

    print("\n" + "=" * 70)
    print("CYCLE 1 SUMMARY")
    print("=" * 70)
    print(f"Files scanned:  {len(files)}")
    print(f"Files fixed:    {files_fixed}")
    print(f"Total fixes:    {total_fixes}")
    print(f"Bytes saved:    {total_saved:,}")
    print(f"\nFix breakdown:")
    for pattern, count in sorted(fix_summary.items(), key=lambda x: -x[1]):
        print(f"  {pattern}: {count} duplicates removed")

    return files_fixed


if __name__ == '__main__':
    fixed = main()
    sys.exit(0 if fixed >= 0 else 1)
