#!/usr/bin/env python3
"""
Final targeted cleanup for the last remaining violations
"""

import os
import re
import glob

TOOLS_DIR = "."

# Remaining AI filler to remove
REMAINING_FILLER = [
    'intuitive', 'comprehensive', 'unlock', 'extensive'
]

def clean_file_violations(filepath, content):
    """Clean specific violations in specific files"""
    modified = False
    tool_name = os.path.basename(os.path.dirname(filepath))

    # Fix dot-product-calculator bold tags
    if tool_name == 'dot-product-calculator':
        if '<strong>' in content or '<b>' in content:
            content = re.sub(r'</?strong>', '', content)
            content = re.sub(r'</?b>', '', content)
            modified = True

    # Fix Q: patterns in headings (convert colon to dash)
    if re.search(r'<h[1-6][^>]*>Q:', content):
        content = re.sub(r'(<h[1-6][^>]*>)Q:', r'\1Q -', content)
        modified = True

    # Fix "All equivalents:" pattern
    if 'All equivalents:' in content:
        content = content.replace('All equivalents:', 'All equivalents -')
        modified = True

    # Remove remaining AI filler phrases (outside script/style blocks)
    parts = re.split(r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)', content, flags=re.IGNORECASE)
    new_parts = []

    for part in parts:
        if re.match(r'<(script|style)', part, re.IGNORECASE):
            new_parts.append(part)
        else:
            original_part = part
            for phrase in REMAINING_FILLER:
                # Remove the phrase
                pattern = r'\b' + re.escape(phrase) + r'\b'
                part = re.sub(pattern, '', part, flags=re.IGNORECASE)

            # Clean up text
            part = re.sub(r'\s+', ' ', part)
            part = re.sub(r'\s*,\s*,', ',', part)
            part = re.sub(r'\s*\.\s*\.', '.', part)
            part = re.sub(r'^\s*[,.]', '', part, re.MULTILINE)
            part = re.sub(r'[,.]\s*$', '', part, re.MULTILINE)
            part = re.sub(r'\s+([,.!?])', r'\1', part)

            if part != original_part:
                modified = True

            new_parts.append(part)

    content = ''.join(new_parts)
    return content, modified

def process_file(filepath):
    """Process a single file with targeted fixes"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return False

    original = content
    content, modified = clean_file_violations(filepath, content)

    if modified and content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False

    return False

def main():
    # Target files with remaining violations
    problem_files = [
        'dot-product-calculator',
        'cooking-conversion-calculator'
    ]

    # First, fix specific problem files
    print("Targeted fixes for remaining violations...")
    print("=" * 60)

    modified_count = 0
    for tool_name in problem_files:
        filepath = os.path.join(TOOLS_DIR, tool_name, 'index.html')
        if os.path.exists(filepath):
            if process_file(filepath):
                print(f"✓ Fixed {tool_name}")
                modified_count += 1

    # Then sweep all files for AI filler
    pattern = os.path.join(TOOLS_DIR, '*', 'index.html')
    files = sorted(glob.glob(pattern))

    for filepath in files:
        if process_file(filepath):
            tool_name = os.path.basename(os.path.dirname(filepath))
            if tool_name not in problem_files:  # Don't double-count
                modified_count += 1

    print(f"\nFinal cleanup pass complete. {modified_count} files modified.")
    print("=" * 60)

if __name__ == '__main__':
    main()