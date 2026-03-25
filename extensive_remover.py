#!/usr/bin/env python3
"""
Ultra-focused removal of "extensive" AI filler phrase
"""

import os
import re
import glob

TOOLS_DIR = "."

def remove_extensive(content):
    """Remove the word 'extensive' from content outside script/style blocks"""
    # Split by script/style blocks to preserve them
    parts = re.split(r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)', content, flags=re.IGNORECASE)
    new_parts = []
    modified = False

    for part in parts:
        if re.match(r'<(script|style)', part, re.IGNORECASE):
            # Preserve script/style blocks exactly
            new_parts.append(part)
        else:
            # Remove "extensive" from this part
            original_part = part

            # Remove variations of extensive
            patterns = [
                r'\bextensive\b',
                r'\bExtensive\b',
                r'\bEXTENSIVE\b'
            ]

            for pattern in patterns:
                part = re.sub(pattern, '', part)

            # Clean up resulting text
            part = re.sub(r'\s+', ' ', part)  # Multiple spaces
            part = re.sub(r'\s*,\s*,', ',', part)  # Double commas
            part = re.sub(r'\s*\.\s*\.', '.', part)  # Double periods
            part = re.sub(r'^\s*[,.]', '', part, re.MULTILINE)  # Leading punctuation
            part = re.sub(r'[,.]\s*$', '', part, re.MULTILINE)  # Trailing punctuation
            part = re.sub(r'\s+([,.!?])', r'\1', part)  # Space before punctuation

            if part != original_part:
                modified = True

            new_parts.append(part)

    return ''.join(new_parts), modified

def process_file(filepath):
    """Process a single file to remove 'extensive'"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return False

    # Only process if 'extensive' is found
    if 'extensive' not in content.lower():
        return False

    original = content
    content, modified = remove_extensive(content)

    if modified and content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False

    return False

def main():
    # Find all index.html files
    pattern = os.path.join(TOOLS_DIR, '*', 'index.html')
    files = sorted(glob.glob(pattern))

    print(f"Removing 'extensive' from {len(files)} files...")
    print("=" * 60)

    modified_count = 0
    for filepath in files:
        if process_file(filepath):
            tool_name = os.path.basename(os.path.dirname(filepath))
            print(f"✓ Cleaned {tool_name}")
            modified_count += 1

    print(f"\nExtensive removal complete. {modified_count} files modified.")
    print("=" * 60)

if __name__ == '__main__':
    main()