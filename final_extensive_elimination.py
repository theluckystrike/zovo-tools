#!/usr/bin/env python3
"""
Final elimination of 'extensive' - handle even minified and edge cases
"""

import os
import re
import glob

TOOLS_DIR = "."

def nuclear_extensive_removal(content):
    """Remove 'extensive' with nuclear approach - handle all edge cases"""
    if 'extensive' not in content.lower():
        return content, False

    original = content
    modified = False

    # Method 1: Global case-insensitive replacement with word boundaries
    patterns = [
        r'\bextensive\b',
        r'\bExtensive\b',
        r'\bEXTENSIVE\b',
        r'\bEXTENSive\b'  # Mixed case
    ]

    for pattern in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
            modified = True

    # Method 2: Even more aggressive - remove "extensive" anywhere it appears
    # as long as it's not part of another word
    if 'extensive' in content.lower():
        # Find all positions of "extensive" (case insensitive)
        positions = []
        search_text = content.lower()
        start = 0
        while True:
            pos = search_text.find('extensive', start)
            if pos == -1:
                break
            positions.append(pos)
            start = pos + 1

        # Remove from end to beginning to maintain positions
        for pos in reversed(positions):
            # Check if it's a standalone word (not part of another word)
            before_char = content[pos-1] if pos > 0 else ' '
            after_char = content[pos+9] if pos+9 < len(content) else ' '

            if not (before_char.isalnum() or after_char.isalnum()):
                # It's a standalone word, remove it
                content = content[:pos] + content[pos+9:]
                modified = True

    # Method 3: Clean up resulting text artifacts
    if modified:
        # Clean up multiple spaces
        content = re.sub(r'\s+', ' ', content)
        # Clean up punctuation issues
        content = re.sub(r'\s*,\s*,', ',', content)
        content = re.sub(r'\s*\.\s*\.', '.', content)
        content = re.sub(r'^\s*[,.]', '', content, re.MULTILINE)
        content = re.sub(r'[,.]\s*$', '', content, re.MULTILINE)
        content = re.sub(r'\s+([,.!?])', r'\1', content)

    return content, modified

def process_file(filepath):
    """Process file with nuclear extensive removal"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return False

    content, modified = nuclear_extensive_removal(content)

    if modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False

    return False

def main():
    # Get all files that still contain "extensive"
    pattern = os.path.join(TOOLS_DIR, '*', 'index.html')
    files = sorted(glob.glob(pattern))

    files_with_extensive = []
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            if 'extensive' in content.lower():
                files_with_extensive.append(filepath)
        except:
            continue

    print(f"Found {len(files_with_extensive)} files still containing 'extensive'")
    print("=" * 70)

    modified_count = 0
    for filepath in files_with_extensive:
        if process_file(filepath):
            tool_name = os.path.basename(os.path.dirname(filepath))
            print(f"✓ Nuclear removal from {tool_name}")
            modified_count += 1

    print(f"\nNuclear extensive elimination complete. {modified_count} files modified.")

    # Verify results
    remaining_count = 0
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            if 'extensive' in content.lower():
                remaining_count += 1
        except:
            continue

    print(f"Files with 'extensive' remaining: {remaining_count}")
    print("=" * 70)

if __name__ == '__main__':
    main()