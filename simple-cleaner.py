#!/usr/bin/env python3
import re
import sys
import argparse

def clean_html_file(filepath):
    """Clean AI formatting violations from HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

    original_content = content
    changes = []

    # 1. Fix bold formatting (markdown and HTML)
    # Markdown bold (**text**)
    md_bold_count = len(re.findall(r'\*\*(.+?)\*\*', content))
    if md_bold_count > 0:
        content = re.sub(r'\*\*(.+?)\*\*', r'\1', content)
        changes.append(f"Removed {md_bold_count} markdown bold patterns")

    # HTML bold tags
    strong_count = len(re.findall(r'<strong[^>]*>.*?</strong>', content, re.DOTALL))
    b_count = len(re.findall(r'<b[^>]*>.*?</b>', content, re.DOTALL))

    if strong_count > 0:
        content = re.sub(r'<strong[^>]*>(.*?)</strong>', r'\1', content, flags=re.DOTALL)
        changes.append(f"Removed {strong_count} <strong> tags")

    if b_count > 0:
        content = re.sub(r'<b[^>]*>(.*?)</b>', r'\1', content, flags=re.DOTALL)
        changes.append(f"Removed {b_count} <b> tags")

    # 2. Fix em/en dashes (Unicode characters)
    em_count = content.count('\u2014')  # em dash —
    en_count = content.count('\u2013')  # en dash –

    if em_count > 0:
        content = content.replace('\u2014', ', ')
        changes.append(f"Fixed {em_count} em dashes")

    if en_count > 0:
        content = content.replace('\u2013', ', ')
        changes.append(f"Fixed {en_count} en dashes")

    # 3. Fix colon headings (but preserve URLs, CSS, steps)
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        pattern = f'<{tag}[^>]*>([^<]*:[^<]*)</{tag}>'
        matches = re.findall(pattern, content, re.IGNORECASE)
        colon_headings_fixed = 0

        for match in matches:
            # Skip URLs, CSS, time formats, and step instructions
            if any(skip in match.lower() for skip in ['http', 'https', '://', 'am', 'pm', 'step ']):
                continue
            if match.startswith('Step '):
                continue

            # Only process if it looks like "Label: Description" pattern
            if ':' in match and len(match.split(':', 1)) == 2:
                parts = match.split(':', 1)
                if len(parts[0].strip()) < 50 and len(parts[1].strip()) > 0:  # Reasonable label length
                    new_heading = parts[1].strip()
                    content = content.replace(f'>{match}<', f'>{new_heading}<')
                    colon_headings_fixed += 1

        if colon_headings_fixed > 0:
            changes.append(f"Fixed {colon_headings_fixed} colon headings in {tag.upper()}")

    # 4. Fix common AI phrases
    ai_phrases = {
        'comprehensive': 'complete',
        'optimize': 'improve',
        'optimized': 'enhanced',
        'optimizing': 'improving',
        'leverage': 'use',
        'leveraging': 'using',
        'utilize': 'use',
        'utilizing': 'using',
        'robust': 'strong',
        'seamlessly': 'smoothly',
        'seamless': 'smooth',
        'delve into': 'look at',
        'delving into': 'looking at',
        'facilitate': 'help',
        'facilitating': 'helping'
    }

    ai_fixed = []
    for phrase, replacement in ai_phrases.items():
        # Use word boundaries for whole words only
        pattern = r'\b' + re.escape(phrase) + r'\b'
        matches = re.findall(pattern, content, re.IGNORECASE)
        count = len(matches)
        if count > 0:
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            ai_fixed.append(f"{phrase}×{count}")

    if ai_fixed:
        changes.append(f"Fixed AI phrases: {', '.join(ai_fixed[:5])}")

    # 5. Clean up artifacts from replacements
    content = re.sub(r',\s*,+', ',', content)  # Remove double commas
    content = re.sub(r'  +', ' ', content)     # Remove double spaces

    # Write back if changes were made
    if content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            for change in changes:
                print(f"  ✓ {change}")
            print(f"  Total: {len(changes)} change types applied")
            return True
        except Exception as e:
            print(f"Error writing file: {e}")
            return False
    else:
        print("  ✓ No changes needed")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clean AI formatting violations from HTML file')
    parser.add_argument('filepath', help='Path to HTML file to clean')
    args = parser.parse_args()

    success = clean_html_file(args.filepath)
    sys.exit(0 if success else 1)