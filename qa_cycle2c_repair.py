#!/usr/bin/env python3
"""
Cycle 2c: Repair severely corrupted files with full-page duplication.
These files have their entire HTML concatenated multiple times.
Strategy: Find the first REAL complete document by tracking tag nesting.
"""

import os
import re

BASE_DIR = '/Users/mike/zovo-workspaces/zovo-tools'

# Files known to have multiple </html> tags
TARGET_FILES = [
    'ai-seo-analyzer', 'ai-website-builder', 'cover-letter-generator',
    'gear-ratio-calculator', 'html-css-playground', 'html-encoder',
    'html-formatter', 'html-to-pdf-converter', 'image-converter',
    'investment-return-calculator', 'loan-calculator', 'markdown-editor',
    'markdown-to-html', 'meta-tag-generator', 'pay-stub-creator',
    'privacy-policy-generator', 'screenshot-to-code', 'upc-code-generator'
]


def find_real_document_end(content):
    """
    Find the real end of the FIRST complete HTML document.
    Handle JS template literals that contain </html> by tracking context.

    Strategy: Walk through the content tracking:
    - Are we inside a <script> block?
    - Are we inside a template literal (backtick)?
    - Are we inside a string ('...' or "...")?

    The real </html> is the one that's NOT inside any of these.
    """
    # First, try simple approach: find the last </html> in the file
    # and truncate there (but verify the content is valid)

    # Actually, for these severely duplicated files, the issue is that
    # batch processes appended content. The REAL document includes
    # all the script tags with template literals.

    # Better approach: find where content starts repeating.
    # If the file is N copies of the same content, we can find the period.

    # Find all <!DOCTYPE positions (these might also be in templates)
    doctypes = [m.start() for m in re.finditer(r'<!DOCTYPE\s+html', content, re.IGNORECASE)]

    if len(doctypes) <= 1:
        return len(content)  # Only one document, no duplication

    # The first DOCTYPE is always at position 0 (the real document start)
    # But subsequent DOCTYPEs might be inside JS template literals

    # Check each DOCTYPE: is it inside a script block?
    for i, pos in enumerate(doctypes[1:], 1):
        # Count open/close script tags before this position
        # If script_opens > script_closes, we're inside a script
        # But this is expensive. Let's try a simpler heuristic:

        # Check the 10 characters before the DOCTYPE
        before = content[max(0, pos-10):pos]

        # If preceded by backtick, it's inside a template literal
        if '`' in before:
            continue

        # If preceded by newline or start-of-chunk, it might be real
        # Test: is the content from 0 to pos a prefix of the content from pos?
        # i.e., is it repeating?
        chunk_before = content[:pos]
        chunk_after = content[pos:pos + min(1000, len(content) - pos)]
        first_1000 = content[:1000]

        # Check if what follows this DOCTYPE looks like the start of our document
        if chunk_after[:500].strip()[:100] == first_1000.strip()[:100]:
            # This is a repeated copy
            return pos

    # If no clear repetition found, try another approach:
    # Find the last </html> that is followed by newline+EOF or just EOF
    last_html = content.rfind('</html>')
    if last_html >= 0:
        after = content[last_html + len('</html>'):].strip()
        if not after:
            # The file ends cleanly. Now find where duplication starts
            # by comparing file chunks
            pass

    # Fallback: try to find periodicity
    # Check if content[0:L] == content[L:2L] for various L values
    for dt_pos in doctypes[1:]:
        before = content[max(0, dt_pos-5):dt_pos]
        # Skip if inside template literal
        if '`' in before or "'" in before or '"' in before:
            continue
        # This might be a real document boundary
        first_chunk = content[:500]
        repeat_chunk = content[dt_pos:dt_pos+500]
        # Compare (allow for minor differences at boundaries)
        if first_chunk[:200] == repeat_chunk[:200]:
            return dt_pos

    return len(content)


def find_document_end_v2(content):
    """
    Alternative approach: Parse the file understanding JS context.
    Track backtick depth for template literals.
    """
    i = 0
    in_script = False
    in_template = 0  # Nesting depth of template literals
    in_single_quote = False
    in_double_quote = False

    while i < len(content):
        c = content[i]

        # Handle escape sequences in strings/templates
        if c == '\\' and (in_single_quote or in_double_quote or in_template > 0):
            i += 2
            continue

        if in_single_quote:
            if c == "'":
                in_single_quote = False
            i += 1
            continue

        if in_double_quote:
            if c == '"':
                in_double_quote = False
            i += 1
            continue

        if in_template > 0:
            if c == '`':
                in_template -= 1
            elif c == '$' and i + 1 < len(content) and content[i+1] == '{':
                # Template expression - would need recursive parsing
                pass
            i += 1
            continue

        if in_script:
            if c == '`':
                in_template += 1
            elif c == "'":
                in_single_quote = True
            elif c == '"':
                in_double_quote = True
            elif content[i:i+9] == '</script>':
                in_script = False
                i += 9
                continue
            i += 1
            continue

        # Outside script - look for tags
        if content[i:i+7] == '<script':
            # Check if it's a real script tag (not inside another context)
            end_of_tag = content.find('>', i + 7)
            if end_of_tag >= 0:
                in_script = True
                i = end_of_tag + 1
                continue

        if content[i:i+7] == '</html>':
            # We found </html> outside of any script/string context
            # This is the real end of the document
            return i + 7

        i += 1

    return len(content)


def repair_file(tool_name):
    """Repair a file with full-page duplication."""
    filepath = os.path.join(BASE_DIR, tool_name, 'index.html')
    if not os.path.isfile(filepath):
        print(f"  SKIP: {tool_name}/index.html not found")
        return 0

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    html_count = content.count('</html>')
    if html_count <= 1:
        print(f"  SKIP: {tool_name} - only {html_count} </html> tag(s)")
        return 0

    original_size = len(content)

    # Use the parser approach to find real document end
    real_end = find_document_end_v2(content)

    if real_end >= original_size:
        # Parser didn't find a clear end, try the repetition approach
        real_end = find_real_document_end(content)

    if real_end >= original_size - 10:
        print(f"  WARNING: Could not find duplication boundary for {tool_name}")
        return 0

    new_content = content[:real_end].rstrip() + '\n'

    # Verify the trimmed content has basic HTML structure
    has_doctype = '<!DOCTYPE' in new_content[:100] or '<!doctype' in new_content[:100]
    has_html = '</html>' in new_content[-20:]

    if not has_doctype:
        print(f"  WARNING: Trimmed content missing <!DOCTYPE> for {tool_name}")
        return 0

    saved = original_size - len(new_content)
    new_html_count = new_content.count('</html>')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"  FIXED: {tool_name}")
    print(f"    </html> tags: {html_count} -> {new_html_count}")
    print(f"    Size: {original_size:,} -> {len(new_content):,} bytes (saved {saved:,})")

    return saved


def main():
    print("=" * 70)
    print("CYCLE 2c: Repair Severely Corrupted Files")
    print("=" * 70)

    total_saved = 0
    fixed = 0

    for tool_name in TARGET_FILES:
        saved = repair_file(tool_name)
        if saved > 0:
            total_saved += saved
            fixed += 1

    print("\n" + "=" * 70)
    print("CYCLE 2c SUMMARY")
    print("=" * 70)
    print(f"Files targeted:  {len(TARGET_FILES)}")
    print(f"Files fixed:     {fixed}")
    print(f"Bytes saved:     {total_saved:,}")

    # Verify
    print("\nVerification:")
    for tool_name in TARGET_FILES:
        filepath = os.path.join(BASE_DIR, tool_name, 'index.html')
        if os.path.isfile(filepath):
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read()
            count = content.count('</html>')
            size = len(content)
            status = "OK" if count == 1 else f"STILL HAS {count}"
            print(f"  {tool_name}: {count} </html>, {size:,} bytes - {status}")


if __name__ == '__main__':
    main()
