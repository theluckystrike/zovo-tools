#!/usr/bin/env python3
"""
Fix duplicated script blocks in tool pages.
Handles the pattern where concurrent agents appended duplicate <script> blocks.
Author: Michael Lip
"""

import re
import os
import hashlib
import json
from collections import Counter

REPO = "/Users/mike/zovo-workspaces/zovo-tools"

def deduplicate_scripts(filepath):
    """Remove duplicate <script> blocks from a file, keeping only the first occurrence of each."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original_size = len(content)

    # Find all script blocks with their content
    script_pattern = re.compile(r'(<script[^>]*>)(.*?)(</script>)', re.DOTALL)

    seen_hashes = {}
    removals = []  # (start, end) tuples to remove

    for m in script_pattern.finditer(content):
        script_body = m.group(2).strip()
        if len(script_body) < 50:
            continue  # Skip tiny scripts (inline event handlers, etc.)

        h = hashlib.md5(script_body.encode()).hexdigest()

        if h in seen_hashes:
            # This is a duplicate - mark for removal
            removals.append((m.start(), m.end()))
        else:
            seen_hashes[h] = m.start()

    if not removals:
        return 0

    # Remove duplicates from end to start to preserve positions
    removals.sort(reverse=True)
    for start, end in removals:
        # Also remove any whitespace/newlines after the removed script
        while end < len(content) and content[end] in '\n\r\t ':
            end += 1
        content = content[:start] + content[end:]

    new_size = len(content)
    saved = original_size - new_size

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return saved


def fix_html_duplication(filepath):
    """Fix files where entire HTML pages were concatenated."""
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original_size = len(content)

    # Strategy: Find the first complete HTML page (DOCTYPE...to...</html>)
    # and discard everything after

    # First, check if file starts with DOCTYPE
    stripped = content.lstrip()
    if not stripped.startswith('<!DOCTYPE'):
        # File is broken at the start - skip this one for manual review
        return 0, "SKIP: File doesn't start with DOCTYPE"

    # Find the first </html> that's NOT inside a <script> tag
    # We need to track whether we're inside a script block
    pos = 0
    in_script = False
    first_real_html_close = -1

    while pos < len(content):
        if not in_script:
            script_open = content.find('<script', pos)
            html_close = content.find('</html>', pos)

            if html_close == -1:
                break

            if script_open == -1 or html_close < script_open:
                # This </html> is NOT inside a script
                first_real_html_close = html_close
                break
            else:
                # We found a <script> before </html>, skip past it
                script_end = content.find('</script>', script_open)
                if script_end == -1:
                    break
                pos = script_end + 9
        else:
            pos += 1

    if first_real_html_close == -1:
        return 0, "SKIP: No </html> found outside script tags"

    # Keep everything up to and including the first real </html>
    new_content = content[:first_real_html_close + 7].rstrip() + '\n'

    if len(new_content) >= original_size - 10:
        return 0, "No change needed"

    saved = original_size - len(new_content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return saved, f"Trimmed {saved} bytes"


def main():
    # Load audit results
    with open(os.path.join(REPO, 'audit_results.json')) as f:
        data = json.load(f)

    duplicated_files = [e for e in data['all_files'] if e['doctype_count'] > 1]

    print("=" * 70)
    print("FIXING DUPLICATED FILES")
    print("=" * 70)

    total_saved = 0
    fixed_count = 0
    skipped = []

    for entry in duplicated_files:
        filepath = os.path.join(REPO, entry['path'])
        name = entry['path']

        print(f"\nProcessing: {name} ({entry['size_human']}, {entry['doctype_count']}x DOCTYPE)")

        # Step 1: Deduplicate script blocks
        script_saved = deduplicate_scripts(filepath)
        if script_saved > 0:
            print(f"  Removed duplicate scripts: saved {script_saved/1024:.0f}KB")
            total_saved += script_saved
            fixed_count += 1

        # Re-read to check current state
        with open(filepath, 'r', errors='replace') as f:
            content = f.read()

        current_doctype_count = content.count('<!DOCTYPE')
        # Count DOCTYPEs that are NOT in script tags (real HTML DOCTYPEs)
        real_doctypes = 0
        for m in re.finditer('<!DOCTYPE', content):
            pos = m.start()
            # Check if inside a script
            before = content[:pos]
            last_script_open = before.rfind('<script')
            last_script_close = before.rfind('</script>')
            if last_script_open <= last_script_close:
                real_doctypes += 1

        if real_doctypes > 1:
            print(f"  Still has {real_doctypes} real DOCTYPEs - attempting HTML dedup")
            saved, msg = fix_html_duplication(filepath)
            if saved > 0:
                total_saved += saved
                fixed_count += 1
                print(f"  {msg}")
            else:
                print(f"  {msg}")
                if "SKIP" in str(msg):
                    skipped.append((name, msg))

        # Report final state
        with open(filepath, 'r', errors='replace') as f:
            final_content = f.read()
        print(f"  Final size: {len(final_content)/1024:.0f}KB")

    print(f"\n{'=' * 70}")
    print(f"SUMMARY")
    print(f"{'=' * 70}")
    print(f"Files processed: {len(duplicated_files)}")
    print(f"Files fixed: {fixed_count}")
    print(f"Total bytes saved: {total_saved/1024:.0f}KB ({total_saved/1024/1024:.1f}MB)")

    if skipped:
        print(f"\nSkipped files (need manual review):")
        for name, reason in skipped:
            print(f"  {name}: {reason}")


if __name__ == '__main__':
    main()
