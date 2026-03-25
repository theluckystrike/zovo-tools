#!/usr/bin/env python3
"""
Surgical fixes for the last remaining violations without disrupting existing components
"""

import os
import re
import glob

TOOLS_DIR = "."

def fix_specific_violations(filepath, content):
    """Fix only the specific violations identified"""
    modified = False

    # Fix air-density-calculator em dash
    if 'air-density-calculator' in filepath:
        if '—' in content or '\u2014' in content:
            content = content.replace('—', ' - ')
            content = content.replace('\u2014', ' - ')
            modified = True

    # Fix dog-food-calculator issues
    if 'dog-food-calculator' in filepath:
        # Remove bold tags
        if '<strong>' in content or '<b>' in content:
            content = re.sub(r'</?strong>', '', content)
            content = re.sub(r'</?b>', '', content)
            modified = True

        # Fix the specific colon headings
        colon_fixes = [
            ('Step 1:', 'Step 1 -'),
            ('Step 2:', 'Step 2 -'),
            ('Step 3:', 'Step 3 -'),
        ]

        for pattern, replacement in colon_fixes:
            if pattern in content:
                content = content.replace(pattern, replacement)
                modified = True

    # Ultra-targeted AI filler removal - only remove "extensive" as it's the most common remaining
    if 'extensive' in content.lower():
        # Skip script/style blocks
        parts = re.split(r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)', content, flags=re.IGNORECASE)
        new_parts = []

        for part in parts:
            if re.match(r'<(script|style)', part, re.IGNORECASE):
                new_parts.append(part)
            else:
                # Remove "extensive" only
                if 'extensive' in part.lower():
                    part = re.sub(r'\bextensive\b', '', part, flags=re.IGNORECASE)
                    part = re.sub(r'\s+', ' ', part)  # Clean up spaces
                    part = re.sub(r'\s*,\s*,', ',', part)  # Double commas
                    part = re.sub(r'^\s*[,.]', '', part, re.MULTILINE)  # Leading punctuation
                    modified = True

            new_parts.append(part)

        content = ''.join(new_parts)

    return content, modified

def process_file(filepath):
    """Process a single file with surgical precision"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return False

    original = content
    content, modified = fix_specific_violations(filepath, content)

    if modified and content != original:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False

    return False

def main():
    # Target only the files with violations
    problem_files = [
        'air-density-calculator/index.html',
        'dog-food-calculator/index.html'
    ]

    print("Surgical fixes for specific violations...")
    print("=" * 50)

    modified_count = 0

    # First fix the specific problem files
    for filepath in problem_files:
        full_path = os.path.join(TOOLS_DIR, filepath)
        if os.path.exists(full_path):
            if process_file(full_path):
                print(f"✓ Fixed {filepath}")
                modified_count += 1

    # Then do a sweep for "extensive" in all files
    pattern = os.path.join(TOOLS_DIR, '*', 'index.html')
    files = sorted(glob.glob(pattern))

    for filepath in files:
        if process_file(filepath):
            tool_name = os.path.basename(os.path.dirname(filepath))
            modified_count += 1

    print(f"\nSurgical fixes complete. {modified_count} files modified.")
    print("=" * 50)

if __name__ == '__main__':
    main()