#!/usr/bin/env python3
"""
Cycle 2: Validate HTML structure across all tool and article pages.
Checks for:
1. Unclosed section tags (mismatched <section> and </section>)
2. Content after </html>
3. Empty files or files under 500 bytes
4. Broken <img tags (missing closing > or />)
5. Sections inserted in <head> that belong in <body>
"""

import os
import re
import sys
from html.parser import HTMLParser

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


def check_content_after_html(content):
    """Check for content after </html> tag."""
    match = re.search(r'</html>\s*(.+)', content, re.DOTALL)
    if match:
        trailing = match.group(1).strip()
        if trailing:
            return trailing[:200]
    return None


def fix_content_after_html(content):
    """Move content from after </html> to before </body>."""
    match = re.search(r'(</html>)\s*(.+)', content, re.DOTALL)
    if not match:
        return content, False

    trailing = match.group(2).strip()
    if not trailing:
        return content, False

    # Remove trailing content after </html>
    content_before_html_close = content[:match.start()]

    # Find </body> and insert before it
    body_close = content_before_html_close.rfind('</body>')
    if body_close >= 0:
        new_content = (
            content_before_html_close[:body_close] +
            trailing + '\n' +
            content_before_html_close[body_close:] +
            '</html>\n'
        )
        return new_content, True
    else:
        # No </body>, just put content before </html>
        new_content = content_before_html_close + trailing + '\n</html>\n'
        return new_content, True


def check_mismatched_sections(content):
    """Count opening and closing section tags."""
    opens = len(re.findall(r'<section[\s>]', content))
    closes = len(re.findall(r'</section>', content))
    return opens, closes


def fix_mismatched_sections(content):
    """Add missing </section> tags if there are unclosed sections."""
    opens = len(re.findall(r'<section[\s>]', content))
    closes = len(re.findall(r'</section>', content))

    if opens > closes:
        missing = opens - closes
        # Insert missing </section> tags before </body>
        body_close = content.rfind('</body>')
        if body_close >= 0:
            insert = '</section>' * missing
            content = content[:body_close] + insert + content[body_close:]
            return content, missing
    elif closes > opens:
        # Extra close tags - remove the extras from the end
        extra = closes - opens
        # Remove last N </section> occurrences
        for _ in range(extra):
            last_pos = content.rfind('</section>')
            if last_pos >= 0:
                content = content[:last_pos] + content[last_pos + len('</section>'):]
        return content, extra

    return content, 0


def check_broken_img_tags(content):
    """Find <img tags that are missing their closing > or />."""
    broken = []
    # Find all <img that aren't properly closed
    # Pattern: <img followed by content that doesn't end with > before the next <
    for m in re.finditer(r'<img\s', content):
        start = m.start()
        # Look for closing > or /> within reasonable distance
        chunk = content[start:start + 2000]
        # Find first > after <img
        close = re.search(r'(?:/>|>)', chunk)
        if not close:
            broken.append(start)
        elif close.start() > 500:
            # Closing > is too far away, likely broken
            broken.append(start)
    return broken


def fix_broken_img_tags(content):
    """Fix <img tags that are missing closing >."""
    fixed = 0
    # Find img tags that don't close before next tag
    pattern = r'(<img\s[^>]*?)(<(?!/))'
    while True:
        match = re.search(pattern, content)
        if not match:
            break
        # Add closing /> before the next tag
        content = content[:match.end(1)] + '/>' + content[match.start(2):]
        fixed += 1
        if fixed > 100:  # Safety limit
            break
    return content, fixed


def check_sections_in_head(content):
    """Check if body-content sections are inside <head>."""
    head_match = re.search(r'<head[^>]*>(.*?)</head>', content, re.DOTALL)
    if not head_match:
        return []

    head_content = head_match.group(1)
    body_elements = ['<section', '<div class="tool-', '<div class="badge-row"',
                     '<div class="live-stats"', '<div class="benchmark-chart"',
                     '<main', '<article', '<footer']

    found = []
    for elem in body_elements:
        if elem in head_content:
            found.append(elem)
    return found


def fix_sections_in_head(content):
    """Move body-content sections from <head> to <body>."""
    head_match = re.search(r'(<head[^>]*>)(.*?)(</head>)', content, re.DOTALL)
    if not head_match:
        return content, 0

    head_content = head_match.group(2)
    body_elements_pattern = r'(<(?:section|div class="tool-|div class="badge-row"|div class="live-stats"|div class="benchmark-chart"|main|article|footer)[^>]*>.*?)(?=</head>)'

    # Find body content in head
    moved_parts = []
    clean_head = head_content

    # Extract sections from head
    for tag in ['<section', '<main', '<article', '<footer']:
        while tag in clean_head:
            idx = clean_head.find(tag)
            # Find matching close tag
            close_tag = '</' + tag.lstrip('<').split()[0] + '>'
            close_idx = clean_head.find(close_tag, idx)
            if close_idx >= 0:
                end = close_idx + len(close_tag)
                moved_parts.append(clean_head[idx:end])
                clean_head = clean_head[:idx] + clean_head[end:]
            else:
                break

    if not moved_parts:
        return content, 0

    # Reconstruct
    new_head = head_match.group(1) + clean_head + head_match.group(3)
    content = content[:head_match.start()] + new_head + content[head_match.end():]

    # Insert moved parts at start of <body>
    body_match = re.search(r'(<body[^>]*>)', content)
    if body_match:
        insert_point = body_match.end()
        moved_html = '\n'.join(moved_parts)
        content = content[:insert_point] + moved_html + content[insert_point:]

    return content, len(moved_parts)


def process_file(filepath):
    """Run all structural checks on a file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return {'file': filepath, 'error': str(e), 'issues': [], 'fixes': []}

    original = content
    issues = []
    fixes = []
    rel_path = os.path.relpath(filepath, BASE_DIR)
    file_size = len(content)

    # Check 1: File size
    if file_size == 0:
        issues.append(f"EMPTY FILE (0 bytes)")
    elif file_size < 500:
        issues.append(f"TINY FILE ({file_size} bytes)")

    # Check 2: Content after </html>
    trailing = check_content_after_html(content)
    if trailing:
        issues.append(f"Content after </html>: {trailing[:80]}...")
        content, fixed = fix_content_after_html(content)
        if fixed:
            fixes.append("Moved trailing content before </body>")

    # Check 3: Mismatched sections
    opens, closes = check_mismatched_sections(content)
    if opens != closes:
        issues.append(f"Mismatched sections: {opens} opens, {closes} closes")
        content, fixed_count = fix_mismatched_sections(content)
        if fixed_count > 0:
            fixes.append(f"Fixed {fixed_count} mismatched section tags")

    # Check 4: Broken img tags
    broken_imgs = check_broken_img_tags(content)
    if broken_imgs:
        issues.append(f"{len(broken_imgs)} broken <img> tag(s)")
        content, fixed_count = fix_broken_img_tags(content)
        if fixed_count > 0:
            fixes.append(f"Fixed {fixed_count} broken <img> tags")

    # Check 5: Sections in <head>
    head_sections = check_sections_in_head(content)
    if head_sections:
        issues.append(f"Body content in <head>: {head_sections}")
        content, fixed_count = fix_sections_in_head(content)
        if fixed_count > 0:
            fixes.append(f"Moved {fixed_count} sections from <head> to <body>")

    # Write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return {
        'file': rel_path,
        'issues': issues,
        'fixes': fixes,
        'size': file_size
    }


def main():
    print("=" * 70)
    print("CYCLE 2: HTML Structure Validation")
    print("=" * 70)

    files = find_all_html_files()
    print(f"\nScanning {len(files)} HTML files...\n")

    total_issues = 0
    total_fixes = 0
    files_with_issues = 0
    files_fixed = 0
    issue_types = {}
    empty_files = []
    tiny_files = []

    for i, filepath in enumerate(files):
        result = process_file(filepath)

        if result.get('error'):
            print(f"  ERROR: {result['file']}: {result['error']}")
            continue

        if result['issues']:
            files_with_issues += 1
            total_issues += len(result['issues'])
            for issue in result['issues']:
                category = issue.split(':')[0].split('(')[0].strip()
                issue_types[category] = issue_types.get(category, 0) + 1

            if result['fixes']:
                files_fixed += 1
                total_fixes += len(result['fixes'])
                print(f"  FIXED: {result['file']}")
                for fix in result['fixes']:
                    print(f"    -> {fix}")
            else:
                if 'EMPTY' in str(result['issues']) or 'TINY' in str(result['issues']):
                    if result['size'] == 0:
                        empty_files.append(result['file'])
                    else:
                        tiny_files.append((result['file'], result['size']))
                    print(f"  ISSUE: {result['file']} - {result['issues']}")

        if (i + 1) % 200 == 0:
            print(f"  ... processed {i+1}/{len(files)} files ...")

    print("\n" + "=" * 70)
    print("CYCLE 2 SUMMARY")
    print("=" * 70)
    print(f"Files scanned:       {len(files)}")
    print(f"Files with issues:   {files_with_issues}")
    print(f"Files fixed:         {files_fixed}")
    print(f"Total issues found:  {total_issues}")
    print(f"Total fixes applied: {total_fixes}")

    print(f"\nIssue breakdown:")
    for issue_type, count in sorted(issue_types.items(), key=lambda x: -x[1]):
        print(f"  {issue_type}: {count}")

    if empty_files:
        print(f"\nEmpty files ({len(empty_files)}):")
        for f in empty_files:
            print(f"  {f}")

    if tiny_files:
        print(f"\nTiny files < 500 bytes ({len(tiny_files)}):")
        for f, s in tiny_files:
            print(f"  {f} ({s} bytes)")

    return files_fixed


if __name__ == '__main__':
    fixed = main()
    sys.exit(0)
