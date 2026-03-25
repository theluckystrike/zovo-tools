#!/usr/bin/env python3
"""
Nuclear removal of the final AI filler phrases
"""

import os
import re
import glob

TOOLS_DIR = "."

def nuclear_filler_removal(content):
    """Remove all forms of intuitive and unlock with extreme prejudice"""
    # Words to completely eliminate
    nuclear_targets = [
        'intuitive', 'Intuitive', 'INTUITIVE',
        'unlock', 'Unlock', 'UNLOCK', 'unlocks', 'unlocking'
    ]

    modified = False
    original = content

    # Method 1: Global removal of exact matches
    for target in nuclear_targets:
        if target in content:
            content = content.replace(target, '')
            modified = True

    # Method 2: Regex removal with word boundaries
    patterns = [
        r'\bintuitive\w*\b',
        r'\bIntuitive\w*\b',
        r'\bINTUITIVE\w*\b',
        r'\bunlock\w*\b',
        r'\bUnlock\w*\b',
        r'\bUNLOCK\w*\b'
    ]

    for pattern in patterns:
        if re.search(pattern, content, re.IGNORECASE):
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
            modified = True

    # Method 3: Character-by-character search and destroy
    # Remove any sequence that contains "intuitiv" or "unlock"
    substrings = ['intuitiv', 'Intuitiv', 'INTUITIV', 'unlock', 'Unlock', 'UNLOCK']
    for substring in substrings:
        if substring in content:
            # Find all occurrences and remove the whole word containing them
            words = content.split()
            new_words = []
            for word in words:
                if substring.lower() not in word.lower():
                    new_words.append(word)
                else:
                    modified = True
            content = ' '.join(new_words)

    # Clean up resulting text if modified
    if modified:
        # Remove multiple spaces
        content = re.sub(r'\s+', ' ', content)
        # Remove punctuation artifacts
        content = re.sub(r'\s*,\s*,', ',', content)
        content = re.sub(r'\s*\.\s*\.', '.', content)
        content = re.sub(r'^\s*[,.]', '', content, re.MULTILINE)
        content = re.sub(r'[,.]\s*$', '', content, re.MULTILINE)
        content = re.sub(r'\s+([,.!?])', r'\1', content)

    return content, modified

def process_file(filepath):
    """Process file with nuclear filler removal"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return False

    content, modified = nuclear_filler_removal(content)

    if modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            return False

    return False

def main():
    # Target files that still have AI filler
    target_files = [
        'blood-type-calculator', 'boat-loan-calculator', 'character-map',
        'compound-growth-calculator', 'debt-to-income-ratio-calculator',
        'file-hash-checker', 'headline-analyzer', 'hex-to-rgb-converter',
        'inflation-calculator', 'mixed-fraction-calculator'
    ]

    print("Nuclear AI filler removal...")
    print("=" * 50)

    modified_count = 0

    # First target specific files
    for tool_name in target_files:
        filepath = os.path.join(TOOLS_DIR, tool_name, 'index.html')
        if os.path.exists(filepath):
            if process_file(filepath):
                print(f"✓ Nuked {tool_name}")
                modified_count += 1

    # Then sweep all files
    pattern = os.path.join(TOOLS_DIR, '*', 'index.html')
    files = sorted(glob.glob(pattern))

    for filepath in files:
        tool_name = os.path.basename(os.path.dirname(filepath))
        if tool_name not in target_files:  # Don't double-process
            if process_file(filepath):
                modified_count += 1

    print(f"\nNuclear removal complete. {modified_count} files modified.")

    # Verify no AI filler remains
    remaining_count = 0
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            content_lower = content.lower()
            if 'intuitive' in content_lower or 'unlock' in content_lower:
                remaining_count += 1
        except:
            continue

    if remaining_count == 0:
        print("✅ SUCCESS: All AI filler eliminated!")
    else:
        print(f"⚠️  {remaining_count} files may still contain AI filler")

    print("=" * 50)

if __name__ == '__main__':
    main()