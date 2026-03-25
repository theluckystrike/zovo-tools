#!/usr/bin/env python3
"""
Final comprehensive validation scan to verify all violations are resolved
"""

import os
import re
import glob

TOOLS_DIR = "."

# Violation categories to check
violations = {
    'hashtag_headers': [],
    'em_dashes': [],
    'en_dashes': [],
    'bold_tags': [],
    'markdown_bold': [],
    'colons_in_headings': [],
    'ai_filler_phrases': [],
    'missing_verified_signal': [],
    'missing_update_history': []
}

# AI filler phrases to check for
AI_FILLER = [
    'comprehensive', 'extensive', 'robust', 'powerful', 'cutting-edge',
    'state-of-the-art', 'revolutionary', 'game-changing', 'innovative',
    'seamlessly', 'effortlessly', 'intuitive', 'user-friendly', 'streamlined',
    'leverage', 'harness', 'unlock', 'empower', 'supercharge',
    'whether you\'re', 'looking to', 'need to', 'want to', 'ready to'
]

def check_violations(filepath):
    """Check a single file for all violation types"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return

    tool_name = os.path.basename(os.path.dirname(filepath))

    # Check for hashtag headers (outside of script blocks)
    lines = content.split('\n')
    in_script = False
    for i, line in enumerate(lines):
        if '<script' in line.lower():
            in_script = True
        elif '</script>' in line.lower():
            in_script = False
        elif not in_script and re.match(r'^\s*#+\s', line):
            violations['hashtag_headers'].append(f"{tool_name} (line {i+1}): {line.strip()}")

    # Check for em dashes
    if '—' in content or '\u2014' in content:
        violations['em_dashes'].append(tool_name)

    # Check for en dashes
    if '–' in content or '\u2013' in content:
        violations['en_dashes'].append(tool_name)

    # Check for bold tags
    if '<strong>' in content or '<b>' in content:
        violations['bold_tags'].append(tool_name)

    # Check for markdown bold (outside script blocks)
    if '**' in content and not re.search(r'<script[\s\S]*?\*\*[\s\S]*?</script>', content, re.IGNORECASE):
        violations['markdown_bold'].append(tool_name)

    # Check for colons in headings
    colon_headings = re.findall(r'<h[1-6][^>]*>[^<]*:[^<]*</h[1-6]>', content)
    if colon_headings:
        for heading in colon_headings:
            violations['colons_in_headings'].append(f"{tool_name}: {heading}")

    # Check for AI filler phrases (case insensitive, outside script blocks)
    content_lower = content.lower()
    script_blocks = re.findall(r'<script[\s\S]*?</script>', content, re.IGNORECASE)
    script_content_lower = ' '.join(script_blocks).lower()

    for phrase in AI_FILLER:
        if phrase in content_lower and phrase not in script_content_lower:
            violations['ai_filler_phrases'].append(f"{tool_name}: {phrase}")
            break

    # Check for missing verified signal
    if 'Last verified working:' not in content:
        violations['missing_verified_signal'].append(tool_name)

    # Check for missing update history
    if 'update-history' not in content and 'Update History' not in content:
        violations['missing_update_history'].append(tool_name)

def main():
    # Find all index.html files
    pattern = os.path.join(TOOLS_DIR, '*', 'index.html')
    files = sorted(glob.glob(pattern))

    print(f"Running final validation scan on {len(files)} files...")
    print("=" * 80)

    for filepath in files:
        check_violations(filepath)

    # Report results
    print("\nFINAL VALIDATION RESULTS")
    print("=" * 80)

    total_violations = 0
    for category, items in violations.items():
        count = len(items)
        total_violations += count
        status = "✓ PASS" if count == 0 else "✗ FAIL"
        print(f"{category.replace('_', ' ').title():<25}: {count:>3} violations {status}")

    print("=" * 80)

    if total_violations == 0:
        print("🎉 ALL VIOLATIONS RESOLVED! Quality validation PASSED!")
        print("✅ Zero hashtag headers")
        print("✅ Zero em/en dashes")
        print("✅ Zero bold formatting")
        print("✅ Zero colons in headings")
        print("✅ Zero AI filler phrases")
        print("✅ All files have verified signals")
        print("✅ All files have update histories")
    else:
        print(f"❌ {total_violations} VIOLATIONS REMAINING")
        print("\nDETAILED VIOLATIONS:")

        for category, items in violations.items():
            if items:
                print(f"\n{category.replace('_', ' ').title()}:")
                for item in items[:10]:  # Show first 10 violations
                    print(f"  • {item}")
                if len(items) > 10:
                    print(f"  ... and {len(items) - 10} more")

    print("=" * 80)

    # Generate summary report
    quality_score = ((len(files) * 7 - total_violations) / (len(files) * 7)) * 100
    print(f"OVERALL QUALITY SCORE: {quality_score:.1f}%")
    print(f"Files processed: {len(files)}")
    print(f"Total violations: {total_violations}")
    print("=" * 80)

if __name__ == '__main__':
    main()