#!/usr/bin/env python3
"""
Quality fixes for all index.html files in directories j-o:
1. Add id attributes to H2 tags missing them
2. Add og:image meta tag where missing
3. Add E-E-A-T footer where missing
4. Add author meta where missing
5. Fix AI language (figurative uses only)
"""

import os
import re
import glob

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

def get_files():
    """Get all index.html files in directories j-o."""
    files = []
    for entry in sorted(os.listdir(BASE_DIR)):
        first_char = entry[0].lower() if entry else ''
        if first_char >= 'j' and first_char <= 'o':
            path = os.path.join(BASE_DIR, entry, "index.html")
            if os.path.isfile(path):
                files.append(path)
    return files

def slugify(text):
    """Convert heading text to a URL-friendly slug."""
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode common HTML entities
    text = text.replace('&amp;', 'and').replace('&lt;', '').replace('&gt;', '')
    text = text.replace('&#8211;', '-').replace('&#8212;', '-')
    text = text.replace('&mdash;', '-').replace('&ndash;', '-')
    text = text.replace('&nbsp;', ' ')
    # Remove remaining entities
    text = re.sub(r'&[a-zA-Z0-9#]+;', '', text)
    # Lowercase
    text = text.lower().strip()
    # Replace spaces and special chars with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Strip leading/trailing hyphens
    text = text.strip('-')
    return text

def fix_h2_ids(content, filepath):
    """FIX 1: Add id attributes to all H2 tags missing them."""
    # First, collect all existing IDs to avoid duplicates
    existing_ids = set(re.findall(r'id=["\']([^"\']+)["\']', content))
    used_slugs = {}  # track slug -> count for deduplication

    # Initialize used_slugs with existing IDs
    for eid in existing_ids:
        used_slugs[eid] = 1

    changes = 0

    def replace_h2(match):
        nonlocal changes
        full_tag = match.group(0)

        # Skip if already has an id attribute
        if re.search(r'\bid=', full_tag):
            return full_tag

        # Extract the text content after the h2 opening tag
        # We need to find the closing </h2> to get the content
        # But since we're matching just the opening tag, we need to look ahead
        # Instead, let's use a different approach
        return full_tag  # placeholder, we'll use a different method

    # Better approach: match full <h2...>content</h2> patterns
    def replace_full_h2(match):
        nonlocal changes
        opening_tag = match.group(1)  # <h2 ...> part
        content_text = match.group(2)  # inner text
        closing = match.group(3)  # </h2>

        # Skip if already has id
        if re.search(r'\bid=', opening_tag):
            return match.group(0)

        slug = slugify(content_text)
        if not slug:
            return match.group(0)

        # Handle duplicates
        if slug in used_slugs:
            used_slugs[slug] += 1
            slug = f"{slug}-{used_slugs[slug]}"
        else:
            used_slugs[slug] = 1

        # Add id to the opening tag
        # Insert id right after <h2
        new_opening = opening_tag.replace('<h2', f'<h2 id="{slug}"', 1)
        changes += 1
        return f"{new_opening}{content_text}{closing}"

    # Match <h2 with optional attributes>content</h2> (content can span lines)
    content = re.sub(
        r'(<h2[^>]*>)(.*?)(</h2>)',
        replace_full_h2,
        content,
        flags=re.DOTALL
    )

    if changes > 0:
        print(f"  FIX 1: Added {changes} H2 IDs in {os.path.basename(os.path.dirname(filepath))}")

    return content

def fix_og_image(content, filepath):
    """FIX 2: Add og:image meta tag where missing."""
    if 'og:image' in content:
        return content

    # Find the last og: meta tag and insert after it
    # Look for the last occurrence of <meta property="og: ...">
    og_pattern = r'(<meta\s+property="og:[^"]*"[^>]*>)'
    matches = list(re.finditer(og_pattern, content))

    if matches:
        last_og = matches[-1]
        insert_pos = last_og.end()
        og_image_tag = '\n<meta property="og:image" content="https://zovo.one/og-image.png">'
        content = content[:insert_pos] + og_image_tag + content[insert_pos:]
        print(f"  FIX 2: Added og:image in {os.path.basename(os.path.dirname(filepath))}")
    else:
        # No og: tags at all - insert before </head>
        og_image_tag = '<meta property="og:image" content="https://zovo.one/og-image.png">\n'
        content = content.replace('</head>', og_image_tag + '</head>', 1)
        print(f"  FIX 2: Added og:image (before </head>) in {os.path.basename(os.path.dirname(filepath))}")

    return content

def fix_eeat_footer(content, filepath):
    """FIX 3: Add E-E-A-T footer where 'Michael Lip' is NOT in the bottom 30%."""
    lines = content.split('\n')
    total_lines = len(lines)
    bottom_start = int(total_lines * 0.7)
    bottom_section = '\n'.join(lines[bottom_start:])

    if 'Michael Lip' in bottom_section:
        return content

    footer_html = '<footer style="text-align:center;padding:24px;color:#b0b0c0;font-size:0.85rem;border-top:1px solid #1e1e2a;margin-top:40px;">Built by Michael Lip \u00b7 More free tools at <a href="https://zovo.one/free-tools/" style="color:#00ff88;text-decoration:none;">zovo.one</a></footer>'

    # Insert before </body>
    content = content.replace('</body>', footer_html + '\n</body>', 1)
    print(f"  FIX 3: Added E-E-A-T footer in {os.path.basename(os.path.dirname(filepath))}")

    return content

def fix_author_meta(content, filepath):
    """FIX 4: Add author meta tag where missing."""
    if 'name="author"' in content:
        return content

    author_tag = '<meta name="author" content="Michael Lip">\n'

    # Insert after <meta name="description" ...> if it exists
    desc_match = re.search(r'(<meta\s+name="description"[^>]*>)', content)
    if desc_match:
        insert_pos = desc_match.end()
        content = content[:insert_pos] + '\n' + author_tag + content[insert_pos:]
    else:
        # Insert before </head>
        content = content.replace('</head>', author_tag + '</head>', 1)

    print(f"  FIX 4: Added author meta in {os.path.basename(os.path.dirname(filepath))}")
    return content

def fix_ai_language(content, filepath):
    """FIX 5: Replace figurative AI language. Skip literal/technical uses."""
    changes = []

    # Define replacements: (pattern, replacement, skip_contexts)
    # We'll do word-boundary matching and check surrounding context
    replacements = [
        # "landscape" -> "space"/"field" (skip literal geographic uses)
        (r'\blandscape\b', 'space', [
            'landscape mode', 'landscape orientation', 'landscape design',
            'landscape architecture', 'landscape painting', 'landscape photo',
            'landscape image', 'landscape format', 'landscape view',
        ]),
        (r'\blandscapes\b', 'spaces', [
            'landscape mode', 'landscape orientation', 'landscape design',
        ]),
        # "elevate" -> "improve" (skip literal physical uses)
        (r'\belevate\b', 'improve', [
            'elevated cortisol', 'elevated levels', 'elevated blood',
            'elevated heart', 'elevated temperature', 'elevated risk',
            'boiling point elevation', 'elevation', 'elevated compared',
            'elevated accident', 'feet elevation', 'elevation gain',
        ]),
        (r'\belevated\b', 'improved', [
            'elevated cortisol', 'elevated levels', 'elevated blood',
            'elevated heart', 'elevated temperature', 'elevated risk',
            'boiling point elevation', 'elevated compared',
            'elevated accident', 'feet elevation',
        ]),
        # "streamline" -> "simplify" (skip if in code/variable names)
        (r'\bstreamline\b', 'simplify', ['streamline\'', '\'streamline']),
        (r'\bstreamlines\b', 'simplifies', []),
        (r'\bstreamlined\b', 'simplified', []),
        (r'\bstreamlining\b', 'simplifying', []),
        # "empower" -> "enable"
        (r'\bempower\b', 'enable', []),
        (r'\bempowers\b', 'enables', []),
        (r'\bempowered\b', 'enabled', []),
        (r'\bempowering\b', 'enabling', []),
        # "unleash" -> "unlock"
        (r'\bunleash\b', 'unlock', []),
        (r'\bunleashes\b', 'unlocks', []),
        (r'\bunleashed\b', 'unlocked', []),
        (r'\bunleashing\b', 'unlocking', []),
        # "harness" -> "use" (skip literal uses about horse harness etc)
        (r'\bharness\b', 'use', ['harness racing', 'horse harness', 'body harness', 'safety harness', 'wiring harness']),
        (r'\bharnessing\b', 'using', []),
        (r'\bharnessed\b', 'used', []),
        # "revolutionize" -> "transform"
        (r'\brevolutionize\b', 'transform', []),
        (r'\brevolutionizes\b', 'transforms', []),
        (r'\brevolutionized\b', 'transformed', []),
        (r'\brevolutionizing\b', 'transforming', []),
    ]

    for pattern, replacement, skip_contexts in replacements:
        def do_replace(match, repl=replacement, skips=skip_contexts):
            # Get surrounding context (100 chars each side)
            start = max(0, match.start() - 100)
            end = min(len(content), match.end() + 100)
            context = content[start:end].lower()

            # Check if inside a <script> block or JS code (array/object literal)
            # Look for enclosing script tags
            before_text = content[:match.start()]
            last_script_open = before_text.rfind('<script')
            last_script_close = before_text.rfind('</script')
            if last_script_open > last_script_close:
                # We're inside a <script> block - skip
                return match.group(0)

            # Check if inside an HTML attribute value that's code-like
            # (e.g., inside a JSON-LD block or similar)
            # Also skip if in a style block
            last_style_open = before_text.rfind('<style')
            last_style_close = before_text.rfind('</style')
            if last_style_open > last_style_close:
                return match.group(0)

            # Check skip contexts
            for skip in skips:
                if skip.lower() in context:
                    return match.group(0)

            return repl

        new_content = re.sub(pattern, do_replace, content, flags=re.IGNORECASE)
        if new_content != content:
            # Count actual changes
            old_matches = len(re.findall(pattern, content, re.IGNORECASE))
            new_matches = len(re.findall(pattern, new_content, re.IGNORECASE))
            diff = old_matches - new_matches
            if diff > 0:
                changes.append(f"{pattern.strip(chr(92)).strip('b')}: {diff}")
            content = new_content

    if changes:
        dirname = os.path.basename(os.path.dirname(filepath))
        print(f"  FIX 5: AI language fixes in {dirname}: {', '.join(changes)}")

    return content

def main():
    files = get_files()
    print(f"Processing {len(files)} files in directories j-o...\n")

    total_changes = {
        'h2_ids': 0,
        'og_image': 0,
        'footer': 0,
        'author': 0,
        'ai_lang': 0,
    }

    for filepath in files:
        dirname = os.path.basename(os.path.dirname(filepath))

        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()

        content = original

        # Apply all fixes
        content = fix_h2_ids(content, filepath)
        content = fix_og_image(content, filepath)
        content = fix_eeat_footer(content, filepath)
        content = fix_author_meta(content, filepath)
        content = fix_ai_language(content, filepath)

        # Only write if changed
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  -> Written: {dirname}/index.html")
        else:
            print(f"  (no changes) {dirname}/index.html")

        print()

    print("Done! All fixes applied.")

if __name__ == '__main__':
    main()
