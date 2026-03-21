#!/usr/bin/env python3
"""
Quality fixes for all tools in directories u-z:
1. Add id attributes to H2 tags missing them
2. Add og:image meta tag where missing
3. Add E-E-A-T footer where missing
4. Add author meta where missing
5. Fix AI language replacements
Plus specific known issues from audit.
"""

import os
import re
import glob

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

def get_files():
    """Get all index.html files in directories u-z."""
    files = []
    for entry in sorted(os.listdir(BASE_DIR)):
        if entry[0] in 'uvwxyz' and os.path.isdir(os.path.join(BASE_DIR, entry)):
            idx = os.path.join(BASE_DIR, entry, "index.html")
            if os.path.isfile(idx):
                files.append(idx)
    return files

def slugify(text):
    """Convert text to a URL-friendly slug."""
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = text.replace('&amp;', 'and').replace('&', 'and')
    # Lowercase
    text = text.lower().strip()
    # Replace spaces and non-alphanumeric with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Strip leading/trailing hyphens
    text = text.strip('-')
    return text

def fix_h2_ids(content):
    """FIX 1: Add id attributes to all H2 tags missing them."""
    used_ids = set()

    # First, collect all existing h2 ids
    existing = re.findall(r'<h2[^>]*\bid=["\']([^"\']+)["\']', content)
    for eid in existing:
        used_ids.add(eid)

    def replace_h2(match):
        full_tag = match.group(0)
        # Skip if already has id
        if re.search(r'\bid=', full_tag):
            return full_tag

        # Extract text content from between <h2...> and </h2>
        # We need to find the closing tag
        start = match.start()
        close_match = re.search(r'</h2>', content[start:], re.IGNORECASE)
        if not close_match:
            return full_tag

        inner_text = content[start + len(full_tag):start + close_match.start()]
        slug = slugify(inner_text)

        if not slug:
            return full_tag

        # Handle duplicates
        final_slug = slug
        counter = 2
        while final_slug in used_ids:
            final_slug = f"{slug}-{counter}"
            counter += 1
        used_ids.add(final_slug)

        # Insert id into the h2 tag
        # Insert after <h2
        new_tag = full_tag[:3] + f' id="{final_slug}"' + full_tag[3:]
        return new_tag

    # Match opening h2 tags (not self-closing, just the opening tag)
    content = re.sub(r'<h2(?:\s[^>]*)?\s*>', replace_h2, content, flags=re.IGNORECASE)
    return content

def fix_og_image(content):
    """FIX 2: Add og:image meta tag where missing."""
    if 'og:image' in content:
        return content

    # Find the last og: meta tag and insert after it
    og_pattern = r'(<meta\s+property="og:[^"]*"[^>]*>)'
    matches = list(re.finditer(og_pattern, content))

    if matches:
        last_og = matches[-1]
        insert_pos = last_og.end()
        og_image_tag = '\n<meta property="og:image" content="https://zovo.one/og-image.png">'
        content = content[:insert_pos] + og_image_tag + content[insert_pos:]
    else:
        # No og tags at all, insert before </head>
        content = content.replace('</head>', '<meta property="og:image" content="https://zovo.one/og-image.png">\n</head>')

    return content

def fix_eeat_footer(content):
    """FIX 3: Add E-E-A-T footer where Michael Lip doesn't appear in bottom 30%."""
    lines = content.split('\n')
    total = len(lines)
    bottom_start = int(total * 0.7)
    bottom_section = '\n'.join(lines[bottom_start:])

    if 'Michael Lip' in bottom_section:
        return content

    footer_html = '<footer style="text-align:center;padding:24px;color:#b0b0c0;font-size:0.85rem;border-top:1px solid #1e1e2a;margin-top:40px;">Built by Michael Lip \u00b7 More free tools at <a href="https://zovo.one/free-tools/" style="color:#00ff88;text-decoration:none;">zovo.one</a></footer>'

    # Insert before </body>
    content = content.replace('</body>', footer_html + '\n</body>')
    return content

def fix_author_meta(content):
    """FIX 4: Add author meta where missing."""
    if '<meta name="author"' in content:
        return content

    # Insert after description meta or after viewport meta
    desc_match = re.search(r'(<meta name="description"[^>]*>)', content)
    if desc_match:
        insert_pos = desc_match.end()
        content = content[:insert_pos] + '\n<meta name="author" content="Michael Lip">' + content[insert_pos:]
    else:
        viewport_match = re.search(r'(<meta name="viewport"[^>]*>)', content)
        if viewport_match:
            insert_pos = viewport_match.end()
            content = content[:insert_pos] + '\n<meta name="author" content="Michael Lip">' + content[insert_pos:]

    return content

def fix_ai_language(content, filepath):
    """FIX 5: Fix AI language - figurative uses only."""
    dirname = os.path.basename(os.path.dirname(filepath))

    # We need to be careful: only replace figurative uses, not literal ones
    # Process line by line to have context
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        original = line

        # Skip script/JSON lines
        if any(skip in line.lower() for skip in ['<script', '</script', '"@type"', '"name":', '"text":', 'application/ld+json']):
            new_lines.append(line)
            continue

        # Skip lines inside <script> blocks - we handle this more carefully below

        # "landscape" - only replace figurative uses
        # watermark-maker: "landscape images" and "landscape photos" are LITERAL - skip
        if dirname == 'watermark-maker':
            pass  # All landscape uses are literal (portrait/landscape photos)
        elif dirname == 'word-cloud-generator':
            # "data visualization landscape" is figurative
            line = line.replace('data visualization landscape', 'data visualization space')
        else:
            # Generic: replace figurative "landscape" but not literal photo/image contexts
            if 'landscape' in line.lower():
                # Check if it's a photo/image context
                photo_context = any(w in line.lower() for w in ['portrait and landscape', 'landscape photo', 'landscape image', 'landscape mode', 'landscape orientation', 'portrait/landscape', 'landscape/portrait'])
                if not photo_context:
                    line = re.sub(r'\blandscape\b', 'space', line)
                    line = re.sub(r'\bLandscape\b', 'Space', line)

        # "elevate" / "elevated" - skip literal uses (physical elevation, technical "elevated jitter")
        if 'elevat' in line.lower():
            literal_elevate = any(w in line.lower() for w in ['elevated location', 'elevated position', 'jitter is elevated', 'elevated jitter', 'elevated place'])
            if not literal_elevate:
                line = re.sub(r'\belevate\b', 'improve', line)
                line = re.sub(r'\bElevate\b', 'Improve', line)
                line = re.sub(r'\belevates\b', 'improves', line)
                line = re.sub(r'\belevating\b', 'improving', line)
                line = re.sub(r'\belevated\b', 'improved', line)

        # "streamline" → "simplify"
        if 'streamline' in line.lower():
            line = re.sub(r'\bstreamline\b', 'simplify', line)
            line = re.sub(r'\bStreamline\b', 'Simplify', line)
            line = re.sub(r'\bstreamlines\b', 'simplifies', line)
            line = re.sub(r'\bstreamlining\b', 'simplifying', line)
            line = re.sub(r'\bstreamlined\b', 'simplified', line)
            line = re.sub(r'\bStreamlined\b', 'Simplified', line)

        # "empower" → "enable"
        if 'empower' in line.lower():
            line = re.sub(r'\bempower\b', 'enable', line)
            line = re.sub(r'\bEmpower\b', 'Enable', line)
            line = re.sub(r'\bempowers\b', 'enables', line)
            line = re.sub(r'\bempowering\b', 'enabling', line)
            line = re.sub(r'\bempowered\b', 'enabled', line)

        # "unleash" → "unlock"
        if 'unleash' in line.lower():
            line = re.sub(r'\bunleash\b', 'unlock', line)
            line = re.sub(r'\bUnleash\b', 'Unlock', line)
            line = re.sub(r'\bunleashes\b', 'unlocks', line)
            line = re.sub(r'\bunleashing\b', 'unlocking', line)
            line = re.sub(r'\bunleashed\b', 'unlocked', line)

        # "harness" → "use"
        if 'harness' in line.lower():
            line = re.sub(r'\bharness\b', 'use', line)
            line = re.sub(r'\bHarness\b', 'Use', line)
            line = re.sub(r'\bharnesses\b', 'uses', line)
            line = re.sub(r'\bharnessing\b', 'using', line)
            line = re.sub(r'\bharnessed\b', 'used', line)

        # "revolutionize" → "transform"
        if 'revolutioniz' in line.lower():
            line = re.sub(r'\brevolutionize\b', 'transform', line)
            line = re.sub(r'\bRevolutionize\b', 'Transform', line)
            line = re.sub(r'\brevolutionizes\b', 'transforms', line)
            line = re.sub(r'\brevolutionizing\b', 'transforming', line)
            line = re.sub(r'\brevolutionized\b', 'transformed', line)

        new_lines.append(line)

    return '\n'.join(new_lines)

def fix_known_issues(content, filepath):
    """Fix specific known issues from audit."""
    dirname = os.path.basename(os.path.dirname(filepath))

    # vcard-generator: rename FAQ heading
    if dirname == 'vcard-generator':
        # Update the heading text
        content = content.replace(
            'Common Questions About vCard Files',
            'Frequently Asked Questions'
        )
        # Also update the id and TOC link to match
        content = content.replace(
            'id="common-questions-about-vcard-files"',
            'id="frequently-asked-questions"'
        )
        content = content.replace(
            'href="#common-questions-about-vcard-files"',
            'href="#frequently-asked-questions"'
        )

    # wacc-calculator: fix author meta from "theluckystrike" to "Michael Lip"
    if dirname == 'wacc-calculator':
        content = content.replace(
            '<meta name="author" content="theluckystrike">',
            '<meta name="author" content="Michael Lip">'
        )
        # Also fix in structured data
        content = content.replace(
            '"name": "theluckystrike"',
            '"name": "Michael Lip"'
        )

    return content

def process_file(filepath):
    """Apply all fixes to a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original

    dirname = os.path.basename(os.path.dirname(filepath))

    # Apply fixes in order
    content = fix_known_issues(content, filepath)  # Do known issues first (before h2 id gen)
    content = fix_h2_ids(content)
    content = fix_og_image(content)
    content = fix_eeat_footer(content)
    content = fix_author_meta(content)
    content = fix_ai_language(content, filepath)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    files = get_files()
    print(f"Found {len(files)} index.html files in u-z directories")

    modified = 0
    for filepath in files:
        dirname = os.path.basename(os.path.dirname(filepath))
        changed = process_file(filepath)
        if changed:
            modified += 1
            print(f"  FIXED: {dirname}/index.html")
        else:
            print(f"  OK:    {dirname}/index.html")

    print(f"\nDone. Modified {modified} of {len(files)} files.")

if __name__ == '__main__':
    main()
