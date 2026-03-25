#!/usr/bin/env python3
"""
Complete elimination of all forms of 'extensive'
"""

import os
import re
import glob

TOOLS_DIR = "."

def remove_all_extensive_forms(content):
    """Remove all forms of extensive: extensive, extensively, extensiveness"""
    if not re.search(r'extensiv', content, re.IGNORECASE):
        return content, False

    original = content
    modified = False

    # All forms of extensive to remove
    patterns = [
        r'\bextensive\b',
        r'\bextensively\b',
        r'\bextensiveness\b',
        r'\bExtensive\b',
        r'\bExtensively\b',
        r'\bExtensiveness\b',
        r'\bEXTENSIVE\b',
        r'\bEXTENSIVELY\b',
        r'\bEXTENSIVENESS\b'
    ]

    for pattern in patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
            modified = True

    # Super aggressive: remove any word starting with "extensiv"
    content = re.sub(r'\bextensiv\w*\b', '', content, flags=re.IGNORECASE)
    if content != original:
        modified = True

    # Clean up resulting text
    if modified:
        content = re.sub(r'\s+', ' ', content)
        content = re.sub(r'\s*,\s*,', ',', content)
        content = re.sub(r'\s*\.\s*\.', '.', content)
        content = re.sub(r'^\s*[,.]', '', content, re.MULTILINE)
        content = re.sub(r'[,.]\s*$', '', content, re.MULTILINE)
        content = re.sub(r'\s+([,.!?])', r'\1', content)

    return content, modified

def process_file(filepath):
    """Process file to remove all extensive forms"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return False

    content, modified = remove_all_extensive_forms(content)

    if modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False

    return False

def main():
    # Get all files
    pattern = os.path.join(TOOLS_DIR, '*', 'index.html')
    files = sorted(glob.glob(pattern))

    print(f"Removing all forms of 'extensive' from {len(files)} files...")
    print("=" * 70)

    modified_count = 0
    for filepath in files:
        if process_file(filepath):
            tool_name = os.path.basename(os.path.dirname(filepath))
            print(f"✓ Cleaned {tool_name}")
            modified_count += 1

    print(f"\nComplete extensive elimination finished. {modified_count} files modified.")

    # Final verification
    remaining_files = []
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            if re.search(r'extensiv', content, re.IGNORECASE):
                tool_name = os.path.basename(os.path.dirname(filepath))
                remaining_files.append(tool_name)
        except:
            continue

    if remaining_files:
        print(f"WARNING: {len(remaining_files)} files still contain extensive variants:")
        for f in remaining_files[:10]:
            print(f"  - {f}")
        if len(remaining_files) > 10:
            print(f"  ... and {len(remaining_files) - 10} more")
    else:
        print("SUCCESS: No files contain 'extensive' variants!")

    print("=" * 70)

if __name__ == '__main__':
    main()