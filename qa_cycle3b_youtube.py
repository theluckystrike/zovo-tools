#!/usr/bin/env python3
"""
Cycle 3b: Fix placeholder YouTube video IDs.
Remove video embed sections with placeholder IDs like VIDEO_ID, xxxxx, xxx, abc.
Also fix malformed YouTube IDs (extra characters appended).
"""

import os
import re

BASE_DIR = '/Users/mike/zovo-workspaces/zovo-tools'

# Placeholder IDs that should be removed
PLACEHOLDER_IDS = {'VIDEO_ID', 'xxxxx', 'xxx', 'abc', ',', '.'}


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


def fix_placeholder_youtube(content):
    """Remove video-embed sections containing placeholder YouTube IDs."""
    fixes = 0

    for placeholder in PLACEHOLDER_IDS:
        # Pattern: section with video-embed class containing the placeholder
        # Match the section containing an iframe/embed with the placeholder ID
        patterns = [
            # iframe with youtube embed
            rf'<section\s+class="video-embed"[^>]*>.*?youtube\.com/embed/{re.escape(placeholder)}.*?</section>',
            # Direct youtube URL with placeholder
            rf'<iframe[^>]*src="[^"]*youtube\.com/embed/{re.escape(placeholder)}[^"]*"[^>]*>.*?</iframe>',
        ]

        for pattern in patterns:
            matches = list(re.finditer(pattern, content, re.DOTALL))
            for m in reversed(matches):
                content = content[:m.start()] + content[m.end():]
                fixes += 1

    # Fix YouTube IDs with extra characters (e.g., dQw4w9WgXcQ. or dQw4w9WgXcQ))
    def fix_extra_chars(match):
        nonlocal fixes
        prefix = match.group(1)
        vid_id = match.group(2)
        suffix = match.group(3)

        # If ID is 12+ chars and the last char is punctuation, remove it
        if len(vid_id) > 11 and vid_id[-1] in '.),;:!':
            fixes += 1
            return prefix + vid_id[:11] + suffix
        return match.group(0)

    content = re.sub(
        r'(youtube\.com/embed/)([^"\'?<>\s]+)(["\'])',
        fix_extra_chars,
        content
    )

    return content, fixes


def main():
    print("=" * 70)
    print("CYCLE 3b: Fix Placeholder YouTube Embeds")
    print("=" * 70)

    files = find_all_html_files()
    print(f"\nScanning {len(files)} HTML files...\n")

    total_fixes = 0
    files_fixed = 0

    for filepath in files:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        new_content, fixes = fix_placeholder_youtube(content)

        if fixes > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_fixed += 1
            total_fixes += fixes
            rel_path = os.path.relpath(filepath, BASE_DIR)
            print(f"  FIXED: {rel_path} ({fixes} fixes)")

    print("\n" + "=" * 70)
    print("CYCLE 3b SUMMARY")
    print("=" * 70)
    print(f"Files scanned:  {len(files)}")
    print(f"Files fixed:    {files_fixed}")
    print(f"Total fixes:    {total_fixes}")


if __name__ == '__main__':
    main()
