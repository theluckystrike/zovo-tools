#!/usr/bin/env python3
"""
Comprehensive cleanup for final quality violations:
- Remove hashtag headers (# ## ###)
- Remove colons in headings ("Feature: Description")
- Remove AI filler phrases
- Final em-dash and bold cleanup
"""

import os
import re
import glob

TOOLS_DIR = "."

# Banned AI filler phrases - comprehensive list
BANNED_PHRASES = [
    'comprehensive', 'extensive', 'robust', 'powerful', 'cutting-edge',
    'state-of-the-art', 'revolutionary', 'game-changing', 'innovative',
    'seamlessly', 'effortlessly', 'intuitive', 'user-friendly', 'streamlined',
    'leverage', 'harness', 'unlock', 'empower', 'supercharge',
    'whether you\'re', 'looking to', 'need to', 'want to', 'ready to',
    'dive into', 'take your', 'elevate your', 'transform your',
    'next level', 'ultimate guide', 'complete guide', 'perfect for',
    'ideal for', 'designed to', 'built to', 'engineered to',
    'optimization', 'optimize', 'maximizing', 'maximize',
    'furthermore', 'moreover', 'additionally', 'in addition',
    'it\'s worth noting', 'it should be noted', 'importantly'
]

# Counters
stats = {
    'files_processed': 0,
    'hashtag_headers_fixed': 0,
    'colon_headings_fixed': 0,
    'ai_filler_removed': 0,
    'em_dashes_fixed': 0,
    'bold_formatting_fixed': 0,
    'files_modified': 0
}

def fix_hashtag_headers(content):
    """Convert hashtag headers to proper HTML headers"""
    changes_made = False
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        original_line = line
        # Match hashtag headers but not inside script/style blocks
        if re.match(r'^#+\s', line.strip()):
            # Count hashtags
            hashtag_count = len(re.match(r'^#+', line.strip()).group(0))
            # Extract text after hashtags
            text = re.sub(r'^#+\s*', '', line.strip())
            # Convert to HTML header (limit to h6)
            header_level = min(hashtag_count, 6)
            line = f'<h{header_level}>{text}</h{header_level}>'
            changes_made = True
            stats['hashtag_headers_fixed'] += 1

        new_lines.append(line)

    return '\n'.join(new_lines), changes_made

def fix_colon_headings(content):
    """Remove colons from headings like 'Feature: Description' -> 'Feature Description'"""
    changes_made = False

    # Pattern to match headings with colons
    pattern = r'(<h[1-6][^>]*>)([^<]*?):\s*([^<]*?)(</h[1-6]>)'

    def replace_colon(match):
        nonlocal changes_made
        changes_made = True
        stats['colon_headings_fixed'] += 1
        return f"{match.group(1)}{match.group(2)} {match.group(3)}{match.group(4)}"

    content = re.sub(pattern, replace_colon, content)
    return content, changes_made

def remove_ai_filler(content):
    """Remove AI filler phrases"""
    changes_made = False
    original_content = content

    # Skip script and style blocks
    def clean_outside_code_blocks(text):
        parts = re.split(r'(<script[\s>].*?</script>|<style[\s>].*?</style>)', text, flags=re.DOTALL | re.IGNORECASE)
        result = []

        for part in parts:
            if re.match(r'<(script|style)', part, re.IGNORECASE):
                result.append(part)
            else:
                # Remove AI filler phrases (case insensitive)
                for phrase in BANNED_PHRASES:
                    # Simple word boundary replacement
                    pattern = r'\b' + re.escape(phrase) + r'\b'
                    part = re.sub(pattern, '', part, flags=re.IGNORECASE)

                # Clean up multiple spaces and punctuation
                part = re.sub(r'\s+', ' ', part)
                part = re.sub(r'\s*,\s*,', ',', part)
                part = re.sub(r'\s*\.\s*\.', '.', part)
                part = re.sub(r'^\s*,\s*', '', part)
                part = re.sub(r'\s*,\s*$', '', part)

                result.append(part)

        return ''.join(result)

    content = clean_outside_code_blocks(content)

    if content != original_content:
        changes_made = True
        stats['ai_filler_removed'] += 1

    return content, changes_made

def final_cleanup(content):
    """Final cleanup for em dashes and bold formatting"""
    changes_made = False
    original_content = content

    # Skip script and style blocks for text cleanup
    def clean_outside_code_blocks(text):
        parts = re.split(r'(<script[\s>].*?</script>|<style[\s>].*?</style>)', text, flags=re.DOTALL | re.IGNORECASE)
        result = []

        for part in parts:
            if re.match(r'<(script|style)', part, re.IGNORECASE):
                result.append(part)
            else:
                # Replace em dashes
                if '—' in part or '\u2014' in part:
                    part = part.replace('—', ' - ')
                    part = part.replace('\u2014', ' - ')
                    stats['em_dashes_fixed'] += 1

                # Remove bold formatting
                if '<strong>' in part or '</strong>' in part:
                    part = re.sub(r'</?strong>', '', part)
                    stats['bold_formatting_fixed'] += 1

                if '<b>' in part or '</b>' in part:
                    part = re.sub(r'</?b>', '', part)
                    stats['bold_formatting_fixed'] += 1

                # Remove markdown bold
                if '**' in part:
                    part = re.sub(r'\*\*(.+?)\*\*', r'\1', part)
                    stats['bold_formatting_fixed'] += 1

                result.append(part)

        return ''.join(result)

    content = clean_outside_code_blocks(content)

    if content != original_content:
        changes_made = True

    return content, changes_made

def process_file(filepath):
    """Process a single file for all violations"""
    stats['files_processed'] += 1

    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    original_content = content
    file_changed = False

    # Apply all fixes
    content, changed = fix_hashtag_headers(content)
    file_changed |= changed

    content, changed = fix_colon_headings(content)
    file_changed |= changed

    content, changed = remove_ai_filler(content)
    file_changed |= changed

    content, changed = final_cleanup(content)
    file_changed |= changed

    # Write back if changed
    if file_changed and content != original_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_modified'] += 1
            tool_name = os.path.basename(os.path.dirname(filepath))
            print(f"✓ Fixed {tool_name}")
        except Exception as e:
            print(f"Error writing {filepath}: {e}")

def main():
    # Find all index.html files
    pattern = os.path.join(TOOLS_DIR, '*', 'index.html')
    files = sorted(glob.glob(pattern))

    print(f"Starting comprehensive cleanup of {len(files)} files...")
    print("=" * 60)

    for filepath in files:
        process_file(filepath)

    print("\n" + "=" * 60)
    print("COMPREHENSIVE CLEANUP COMPLETE")
    print("=" * 60)
    print(f"Files processed: {stats['files_processed']}")
    print(f"Files modified: {stats['files_modified']}")
    print(f"Hashtag headers fixed: {stats['hashtag_headers_fixed']}")
    print(f"Colon headings fixed: {stats['colon_headings_fixed']}")
    print(f"AI filler phrases removed: {stats['ai_filler_removed']}")
    print(f"Em dashes fixed: {stats['em_dashes_fixed']}")
    print(f"Bold formatting removed: {stats['bold_formatting_fixed']}")
    print("=" * 60)

if __name__ == '__main__':
    main()