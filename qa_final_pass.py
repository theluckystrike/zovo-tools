#!/usr/bin/env python3
"""
Final comprehensive pass: Verify all previous fixes stuck and catch anything missed.
"""

import os
import re
import json
import sys

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


def check_file(filepath):
    """Run all checks on a single file."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    rel_path = os.path.relpath(filepath, BASE_DIR)
    issues = []

    # 1. Duplicate sections (class-based)
    section_classes = ['badge-row', 'so-questions-section', 'wiki-definition-box',
                       'compat-table-section', 'npm-dashboard', 'original-research',
                       'live-stats', 'benchmark-chart', 'video-embed']
    for cls in section_classes:
        count = len(re.findall(r'class="' + re.escape(cls) + r'[\s"]', content))
        if count > 1:
            # Check if it's a false positive (like npm-dashboard used as link class)
            issues.append(f"Duplicate class='{cls}' x{count}")

    # 2. Duplicate ld+json with same @type (same content)
    ld_matches = list(re.finditer(r'<script\s+type="application/ld\+json"[^>]*>(.*?)</script>', content, re.DOTALL))
    if len(ld_matches) > 1:
        seen = {}
        for m in ld_matches:
            raw = m.group(1).strip()
            if raw in seen:
                issues.append(f"Duplicate identical ld+json block")
                break
            seen[raw] = True

    # 3. Content after </html> (real, not in JS strings)
    html_closes = list(re.finditer(r'</html>', content))
    real_closes = [m for m in html_closes
                   if not content[m.end():m.end()+3].lstrip().startswith("'")
                   and not content[m.end():m.end()+3].lstrip().startswith(';')
                   and '`' not in content[m.end()-1:m.end()+2]]
    if len(real_closes) > 1:
        issues.append(f"Multiple real </html> tags: {len(real_closes)}")

    # 4. Empty or tiny files
    if len(content) == 0:
        issues.append("EMPTY FILE")
    elif len(content) < 500:
        issues.append(f"TINY FILE ({len(content)} bytes)")

    # 5. Mismatched section tags
    section_opens = len(re.findall(r'<section[\s>]', content))
    section_closes = len(re.findall(r'</section>', content))
    if section_opens != section_closes:
        diff = abs(section_opens - section_closes)
        if diff > 0:
            issues.append(f"Mismatched sections: {section_opens} open, {section_closes} close (diff={diff})")

    # 6. Placeholder YouTube IDs
    for m in re.finditer(r'youtube\.com/embed/(VIDEO_ID|xxxxx|abc)', content):
        # Check if inside script
        last_script = content.rfind('<script', 0, m.start())
        last_close = content.rfind('</script>', 0, m.start())
        if last_script <= last_close:  # NOT in script (in HTML)
            issues.append(f"Placeholder YouTube embed: {m.group(1)}")

    # 7. Shields.io with spaces
    for m in re.finditer(r'img\.shields\.io/badge/[^"\'<>]*\s[^"\'<>]*', content):
        issues.append(f"Shields.io URL with space")

    return issues


def main():
    print("=" * 70)
    print("FINAL COMPREHENSIVE PASS")
    print("=" * 70)

    files = find_all_html_files()
    print(f"\nScanning {len(files)} HTML files...\n")

    total_issues = 0
    files_with_issues = 0

    for filepath in files:
        issues = check_file(filepath)
        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            rel_path = os.path.relpath(filepath, BASE_DIR)
            print(f"  {rel_path}:")
            for issue in issues:
                print(f"    - {issue}")

    print("\n" + "=" * 70)
    print("FINAL PASS SUMMARY")
    print("=" * 70)
    print(f"Files scanned:       {len(files)}")
    print(f"Files with issues:   {files_with_issues}")
    print(f"Total issues found:  {total_issues}")

    if total_issues == 0:
        print("\nALL CLEAR - No issues found!")
    else:
        print(f"\n{total_issues} issues remain. Review above for details.")

    return total_issues


if __name__ == '__main__':
    issues = main()
    sys.exit(0)
