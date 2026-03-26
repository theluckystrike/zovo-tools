#!/usr/bin/env python3
"""
Cycle 3: Validate external URLs across all HTML files.
Checks:
1. Wikipedia links use real article slugs (no duplicated words)
2. StackOverflow search links have proper query encoding
3. Shields.io badge URLs have proper URL encoding (no spaces)
4. QuickChart URLs are properly encoded
5. YouTube video IDs are 11 characters
"""

import os
import re
import sys
from urllib.parse import unquote, quote

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


def check_wikipedia_links(content, filepath):
    """Check Wikipedia links for duplicated/broken slugs."""
    issues = []
    pattern = r'https?://en\.wikipedia\.org/wiki/([^"\'<>\s]+)'

    for m in re.finditer(pattern, content):
        slug = m.group(1)
        decoded = unquote(slug)

        # Check for duplicated words in slug (e.g., Calculator_Calculator)
        words = decoded.replace('_', ' ').split()
        if len(words) >= 2:
            for i in range(len(words) - 1):
                if words[i].lower() == words[i+1].lower() and len(words[i]) > 2:
                    issues.append({
                        'type': 'wikipedia_duplicate_word',
                        'url': m.group(0),
                        'slug': decoded,
                        'duplicate': words[i],
                        'position': m.start()
                    })
                    break

        # Check for obviously broken slugs (very long, gibberish)
        if len(decoded) > 200:
            issues.append({
                'type': 'wikipedia_long_slug',
                'url': m.group(0)[:100] + '...',
                'slug': decoded[:80] + '...',
                'position': m.start()
            })

        # Check for URL-encoded characters that shouldn't be there
        if '%' in slug and '%20' in slug:
            issues.append({
                'type': 'wikipedia_space_in_url',
                'url': m.group(0)[:100],
                'position': m.start()
            })

    return issues


def fix_wikipedia_links(content):
    """Fix broken Wikipedia links."""
    fixes = 0

    def fix_wiki_url(match):
        nonlocal fixes
        url = match.group(0)
        slug = match.group(1)
        decoded = unquote(slug)

        # Fix duplicated words
        words = decoded.replace('_', ' ').split()
        new_words = []
        for i, w in enumerate(words):
            if i > 0 and w.lower() == words[i-1].lower() and len(w) > 2:
                continue  # Skip duplicate
            new_words.append(w)

        new_slug = '_'.join(new_words)
        if new_slug != decoded.replace(' ', '_'):
            fixes += 1
            return f'https://en.wikipedia.org/wiki/{new_slug}'

        # Fix spaces
        if '%20' in slug:
            fixes += 1
            return url.replace('%20', '_')

        return url

    content = re.sub(
        r'https?://en\.wikipedia\.org/wiki/([^"\'<>\s]+)',
        fix_wiki_url,
        content
    )

    return content, fixes


def check_stackoverflow_links(content, filepath):
    """Check StackOverflow links for proper encoding."""
    issues = []
    pattern = r'https?://stackoverflow\.com/search\?q=([^"\'<>\s]+)'

    for m in re.finditer(pattern, content):
        query = m.group(1)
        decoded = unquote(query)

        # Check for unencoded spaces
        if ' ' in query:
            issues.append({
                'type': 'stackoverflow_unencoded_space',
                'url': m.group(0)[:100],
                'position': m.start()
            })

        # Check for double-encoding
        if '%25' in query:
            issues.append({
                'type': 'stackoverflow_double_encoded',
                'url': m.group(0)[:100],
                'position': m.start()
            })

    return issues


def fix_stackoverflow_links(content):
    """Fix StackOverflow search links."""
    fixes = 0

    def fix_so_url(match):
        nonlocal fixes
        query = match.group(1)

        # Fix double encoding
        if '%25' in query:
            query = unquote(query)
            # Re-encode properly
            query = quote(unquote(query), safe='')
            fixes += 1
            return f'https://stackoverflow.com/search?q={query}'

        # Fix unencoded spaces
        if ' ' in query:
            query = query.replace(' ', '+')
            fixes += 1
            return f'https://stackoverflow.com/search?q={query}'

        return match.group(0)

    content = re.sub(
        r'https?://stackoverflow\.com/search\?q=([^"\'<>\s]*(?:\s[^"\'<>\s]*)*)',
        fix_so_url,
        content
    )

    return content, fixes


def check_shields_io_links(content, filepath):
    """Check Shields.io badge URLs for proper encoding."""
    issues = []
    pattern = r'https?://img\.shields\.io/badge/([^"\'<>\s]+)'

    for m in re.finditer(pattern, content):
        badge_path = m.group(1)

        # Check for unencoded spaces
        if ' ' in badge_path:
            issues.append({
                'type': 'shields_unencoded_space',
                'url': m.group(0)[:100],
                'position': m.start()
            })

        # Check for double-encoding
        if '%2520' in badge_path:
            issues.append({
                'type': 'shields_double_encoded',
                'url': m.group(0)[:100],
                'position': m.start()
            })

    return issues


def fix_shields_io_links(content):
    """Fix Shields.io badge URLs."""
    fixes = 0

    def fix_shield_url(match):
        nonlocal fixes
        full_url = match.group(0)

        # Fix unencoded spaces
        if ' ' in full_url:
            fixes += 1
            return full_url.replace(' ', '%20')

        # Fix double encoding
        if '%2520' in full_url:
            fixes += 1
            return full_url.replace('%2520', '%20')

        return full_url

    content = re.sub(
        r'https?://img\.shields\.io/badge/[^"\'<>\s]+',
        fix_shield_url,
        content
    )

    return content, fixes


def check_quickchart_links(content, filepath):
    """Check QuickChart URLs for proper encoding."""
    issues = []
    pattern = r'https?://quickchart\.io/chart\?[^"\'<>\s]+'

    for m in re.finditer(pattern, content):
        url = m.group(0)

        # Check for unencoded spaces
        if ' ' in url:
            issues.append({
                'type': 'quickchart_unencoded_space',
                'url': url[:100] + '...' if len(url) > 100 else url,
                'position': m.start()
            })

        # Check for double-encoding
        if '%2520' in url or '%257B' in url:
            issues.append({
                'type': 'quickchart_double_encoded',
                'url': url[:100] + '...',
                'position': m.start()
            })

    return issues


def fix_quickchart_links(content):
    """Fix QuickChart URLs."""
    fixes = 0

    def fix_qc_url(match):
        nonlocal fixes
        url = match.group(0)

        # Fix double encoding
        if '%2520' in url:
            fixes += 1
            return url.replace('%2520', '%20')
        if '%257B' in url:
            fixes += 1
            return url.replace('%257B', '%7B').replace('%257D', '%7D')

        return url

    content = re.sub(
        r'https?://quickchart\.io/chart\?[^"\'<>\s]+',
        fix_qc_url,
        content
    )

    return content, fixes


def check_youtube_links(content, filepath):
    """Check YouTube video IDs are 11 characters."""
    issues = []

    # Standard YouTube URL patterns
    patterns = [
        r'youtube\.com/watch\?v=([^"\'&<>\s]+)',
        r'youtube\.com/embed/([^"\'?<>\s]+)',
        r'youtu\.be/([^"\'?<>\s]+)',
    ]

    for pattern in patterns:
        for m in re.finditer(pattern, content):
            video_id = m.group(1)
            if len(video_id) != 11:
                issues.append({
                    'type': 'youtube_invalid_id',
                    'id': video_id,
                    'id_length': len(video_id),
                    'position': m.start()
                })

    return issues


def process_file(filepath):
    """Run all URL checks on a file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return {'file': filepath, 'error': str(e)}

    original = content
    rel_path = os.path.relpath(filepath, BASE_DIR)
    all_issues = []

    # Check all URL types
    wiki_issues = check_wikipedia_links(content, filepath)
    so_issues = check_stackoverflow_links(content, filepath)
    shields_issues = check_shields_io_links(content, filepath)
    qc_issues = check_quickchart_links(content, filepath)
    yt_issues = check_youtube_links(content, filepath)

    all_issues = wiki_issues + so_issues + shields_issues + qc_issues + yt_issues

    # Apply fixes
    fixes = {}
    content, n = fix_wikipedia_links(content)
    if n: fixes['wikipedia'] = n

    content, n = fix_stackoverflow_links(content)
    if n: fixes['stackoverflow'] = n

    content, n = fix_shields_io_links(content)
    if n: fixes['shields_io'] = n

    content, n = fix_quickchart_links(content)
    if n: fixes['quickchart'] = n

    # Write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return {
        'file': rel_path,
        'issues': all_issues,
        'fixes': fixes,
        'changed': content != original
    }


def main():
    print("=" * 70)
    print("CYCLE 3: External URL Validation")
    print("=" * 70)

    files = find_all_html_files()
    print(f"\nScanning {len(files)} HTML files...\n")

    total_issues = 0
    total_fixes = 0
    files_with_issues = 0
    files_fixed = 0
    issue_types = {}

    for i, filepath in enumerate(files):
        result = process_file(filepath)

        if result.get('error'):
            print(f"  ERROR: {result['file']}: {result['error']}")
            continue

        if result['issues'] or result.get('fixes'):
            files_with_issues += 1
            total_issues += len(result['issues'])

            for issue in result['issues']:
                t = issue['type']
                issue_types[t] = issue_types.get(t, 0) + 1

            if result.get('changed'):
                files_fixed += 1
                fix_total = sum(result['fixes'].values())
                total_fixes += fix_total
                print(f"  FIXED: {result['file']} - {result['fixes']}")
            elif result['issues']:
                # Only print first few unfixed issues
                if files_with_issues <= 30:
                    for issue in result['issues'][:2]:
                        t = issue['type']
                        detail = issue.get('url', issue.get('id', ''))
                        if len(str(detail)) > 80:
                            detail = str(detail)[:80] + '...'
                        print(f"  ISSUE: {result['file']} - {t}: {detail}")

        if (i + 1) % 200 == 0:
            print(f"  ... processed {i+1}/{len(files)} files ...")

    print("\n" + "=" * 70)
    print("CYCLE 3 SUMMARY")
    print("=" * 70)
    print(f"Files scanned:       {len(files)}")
    print(f"Files with issues:   {files_with_issues}")
    print(f"Files fixed:         {files_fixed}")
    print(f"Total issues found:  {total_issues}")
    print(f"Total fixes applied: {total_fixes}")

    print(f"\nIssue breakdown:")
    for issue_type, count in sorted(issue_types.items(), key=lambda x: -x[1]):
        print(f"  {issue_type}: {count}")

    return files_fixed


if __name__ == '__main__':
    main()
