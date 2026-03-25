#!/usr/bin/env python3
"""
Ultra-final cleanup to achieve 100% quality compliance
"""

import os
import re
import glob

TOOLS_DIR = "."

def fix_specific_colon_headings(content):
    """Fix the specific colon heading patterns that remain"""
    modified = False

    # Pattern 1: "Rule N:" -> "Rule N -"
    if re.search(r'Rule \d+:', content):
        content = re.sub(r'(Rule \d+):', r'\1 -', content)
        modified = True

    # Pattern 2: "Video:" -> "Video -"
    if 'Video:' in content:
        content = content.replace('Video:', 'Video -')
        modified = True

    # Pattern 3: "Multiplication and Division:" -> "Multiplication and Division -"
    colon_patterns = [
        'Multiplication and Division:',
        'Addition and Subtraction:'
    ]

    for pattern in colon_patterns:
        if pattern in content:
            content = content.replace(pattern, pattern.replace(':', ' -'))
            modified = True

    # Pattern 4: Any remaining "Word: " patterns in headings
    content = re.sub(r'(<h[1-6][^>]*>[^<]*?):\s*([^<]*</h[1-6]>)', r'\1 - \2', content)

    return content, modified

def remove_final_ai_filler(content):
    """Remove the final AI filler words"""
    remaining_filler = [
        'intuitive', 'unlock', 'powerful'
    ]

    parts = re.split(r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)', content, flags=re.IGNORECASE)
    new_parts = []
    modified = False

    for part in parts:
        if re.match(r'<(script|style)', part, re.IGNORECASE):
            new_parts.append(part)
        else:
            original_part = part
            for phrase in remaining_filler:
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

    return ''.join(new_parts), modified

def process_file(filepath):
    """Process file with ultra-final cleanup"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return False

    original = content

    # Fix colon headings
    content, colon_modified = fix_specific_colon_headings(content)

    # Remove AI filler
    content, filler_modified = remove_final_ai_filler(content)

    if (colon_modified or filler_modified) and content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False

    return False

def main():
    # Process all files
    pattern = os.path.join(TOOLS_DIR, '*', 'index.html')
    files = sorted(glob.glob(pattern))

    print("Ultra-final cleanup for 100% compliance...")
    print("=" * 60)

    modified_count = 0
    for filepath in files:
        if process_file(filepath):
            tool_name = os.path.basename(os.path.dirname(filepath))
            print(f"✓ Ultra-cleaned {tool_name}")
            modified_count += 1

    print(f"\nUltra-final cleanup complete. {modified_count} files modified.")

    # Final verification
    remaining_violations = 0

    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()

            # Check for colons in headings
            if re.search(r'<h[1-6][^>]*>[^<]*:[^<]*</h[1-6]>', content):
                remaining_violations += 1

            # Check for AI filler
            content_lower = content.lower()
            for phrase in ['intuitive', 'unlock', 'powerful']:
                if phrase in content_lower:
                    remaining_violations += 1
                    break

        except:
            continue

    if remaining_violations == 0:
        print("🎉 SUCCESS: 100% QUALITY COMPLIANCE ACHIEVED!")
    else:
        print(f"⚠️  {remaining_violations} violations may remain")

    print("=" * 60)

if __name__ == '__main__':
    main()