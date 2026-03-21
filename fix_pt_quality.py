#!/usr/bin/env python3
"""
Quality fixes for all tool directories p-t:
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

# Collect all index.html files in directories starting with p-t
tool_dirs = sorted(glob.glob(os.path.join(BASE_DIR, "[p-t]*", "index.html")))

print(f"Found {len(tool_dirs)} index.html files in p-t directories\n")

stats = {
    "h2_ids_added": 0,
    "og_image_added": 0,
    "footer_added": 0,
    "author_added": 0,
    "ai_language_fixed": 0,
    "files_modified": set(),
}

# ============================================================
# FIX 1: Add id attributes to H2 tags missing them
# ============================================================

def slugify(text):
    """Generate a slug from heading text: lowercase, strip tags, replace spaces with hyphens, strip special chars."""
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode common HTML entities
    text = text.replace('&amp;', 'and').replace('&lt;', '').replace('&gt;', '').replace('&#39;', '').replace('&quot;', '')
    # Lowercase
    text = text.lower().strip()
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Strip everything that's not alphanumeric or hyphen
    text = re.sub(r'[^a-z0-9-]', '', text)
    # Collapse multiple hyphens
    text = re.sub(r'-+', '-', text)
    # Strip leading/trailing hyphens
    text = text.strip('-')
    return text


def fix_h2_ids(content, filepath):
    """Add id attributes to H2 tags that don't have them."""
    changes = 0
    used_ids = set()

    # First, collect all existing IDs in the document
    existing_ids = re.findall(r'\bid=["\']([^"\']+)["\']', content)
    used_ids.update(existing_ids)

    def replace_h2(match):
        nonlocal changes
        full_tag = match.group(0)
        attrs = match.group(1) or ""
        inner = match.group(2)

        # Skip if already has an id
        if re.search(r'\bid\s*=', attrs):
            return full_tag

        slug = slugify(inner)
        if not slug:
            return full_tag

        # Handle duplicates
        final_slug = slug
        counter = 2
        while final_slug in used_ids:
            final_slug = f"{slug}-{counter}"
            counter += 1
        used_ids.add(final_slug)

        changes += 1
        # Insert id right after <h2
        return f'<h2 id="{final_slug}"{" " + attrs.strip() if attrs.strip() else ""}>{ inner }</h2>'

    # Match <h2 ...>...</h2> (non-greedy, single line - h2 tags are usually on one line)
    new_content = re.sub(
        r'<h2([^>]*)>(.*?)</h2>',
        replace_h2,
        content,
        flags=re.DOTALL
    )

    if changes > 0:
        stats["h2_ids_added"] += changes
        stats["files_modified"].add(filepath)
    return new_content


# ============================================================
# FIX 2: Add og:image meta tag where missing
# ============================================================

def fix_og_image(content, filepath):
    """Add og:image meta tag after last og: meta tag if missing."""
    if 'og:image' in content:
        return content

    og_image_tag = '<meta property="og:image" content="https://zovo.one/og-image.png">'

    # Find the last og: meta tag and insert after it
    # We look for the last occurrence of <meta property="og: ...">
    og_matches = list(re.finditer(r'<meta\s+property="og:[^"]*"[^>]*>', content))
    if og_matches:
        last_og = og_matches[-1]
        insert_pos = last_og.end()
        new_content = content[:insert_pos] + "\n" + og_image_tag + content[insert_pos:]
        stats["og_image_added"] += 1
        stats["files_modified"].add(filepath)
        return new_content

    # If no og: tags exist, try inserting before </head>
    head_match = re.search(r'</head>', content, re.IGNORECASE)
    if head_match:
        insert_pos = head_match.start()
        new_content = content[:insert_pos] + og_image_tag + "\n" + content[insert_pos:]
        stats["og_image_added"] += 1
        stats["files_modified"].add(filepath)
        return new_content

    return content


# ============================================================
# FIX 3: Add E-E-A-T footer where missing
# ============================================================

EEAT_FOOTER = '<footer style="text-align:center;padding:24px;color:#b0b0c0;font-size:0.85rem;border-top:1px solid #1e1e2a;margin-top:40px;">Built by Michael Lip \u00b7 More free tools at <a href="https://zovo.one/free-tools/" style="color:#00ff88;text-decoration:none;">zovo.one</a></footer>'


def fix_eeat_footer(content, filepath):
    """Add E-E-A-T footer if Michael Lip not in bottom 30%."""
    lines = content.split('\n')
    total = len(lines)
    bottom_start = int(total * 0.7)
    bottom_section = '\n'.join(lines[bottom_start:])

    if 'Michael Lip' in bottom_section:
        return content

    # Insert before </body>
    body_match = re.search(r'</body>', content, re.IGNORECASE)
    if body_match:
        insert_pos = body_match.start()
        new_content = content[:insert_pos] + EEAT_FOOTER + "\n" + content[insert_pos:]
        stats["footer_added"] += 1
        stats["files_modified"].add(filepath)
        return new_content

    return content


# ============================================================
# FIX 4: Add author meta where missing
# ============================================================

def fix_author_meta(content, filepath):
    """Add author meta tag in <head> if missing."""
    if re.search(r'<meta\s+name=["\']author["\']', content, re.IGNORECASE):
        return content

    author_tag = '<meta name="author" content="Michael Lip">'

    # Insert after <meta name="description" ...> if exists
    desc_match = re.search(r'<meta\s+name=["\']description["\'][^>]*>', content, re.IGNORECASE)
    if desc_match:
        insert_pos = desc_match.end()
        new_content = content[:insert_pos] + "\n" + author_tag + content[insert_pos:]
        stats["author_added"] += 1
        stats["files_modified"].add(filepath)
        return new_content

    # Otherwise insert before </head>
    head_match = re.search(r'</head>', content, re.IGNORECASE)
    if head_match:
        insert_pos = head_match.start()
        new_content = content[:insert_pos] + author_tag + "\n" + content[insert_pos:]
        stats["author_added"] += 1
        stats["files_modified"].add(filepath)
        return new_content

    return content


# ============================================================
# FIX 5: Fix AI language (figurative uses only)
# ============================================================

# Each entry: (pattern, replacement, skip_contexts)
# skip_contexts are substrings that indicate literal use - skip the whole line if found
AI_REPLACEMENTS = [
    # "landscape" -> "space"/"field" (skip literal: orientation, photos, landscape mode, mulch, crypto, Landscape as proper noun)
    (r'\blandscape\b', 'space', [
        'landscape orientation', 'landscape mode', 'landscape photo',
        'landscape)', 'Landscape)', 'landscape"', 'landscapes',
        'Colored Sketch', 'hand-drawn', 'atmosphere',
        'mulch', 'Mulch', 'cinematic', '16:9',
        'DSLR', 'Landscape</strong>', '>Landscapes<',
        'rotating to landscape', 'use landscape',
    ]),
    # "elevate" -> "improve" (skip: Basho elevated, body temperature, core body)
    (r'\belevate[sd]?\b', None, [  # None means dynamic replacement
        'Basho elevated', 'core body temperature', 'body temperature',
        'cortisol',
    ]),
    # "streamline" -> "simplify" (skip: Streamlined NTRU, streamlined as a product name)
    (r'\bstreamline[sd]?\b', None, [
        'Streamlined NTRU', 'NTRU Prime',
    ]),
    # "empower" -> "enable"
    (r'\bempower[sed]*\b', None, []),
    # "unleash" -> "unlock"
    (r'\bunleash(?:es|ed)?\b', None, []),
    # "harness" -> "use"
    (r'\bharness(?:es|ed|ing)?\b', None, []),
    # "revolutionize" -> "transform"
    (r'\brevolutionize[sd]?\b', None, []),
]


def get_replacement(match_text, base_replacement):
    """Handle verb conjugation for replacements."""
    if base_replacement:
        return base_replacement

    lower = match_text.lower()

    # elevate/elevates/elevated -> improve/improves/improved
    if lower.startswith('elevat'):
        if lower == 'elevated':
            return 'improved'
        elif lower == 'elevates':
            return 'improves'
        else:
            return 'improve'

    # streamline/streamlines/streamlined -> simplify/simplifies/simplified
    if lower.startswith('streamline'):
        if lower == 'streamlined':
            return 'simplified'
        elif lower == 'streamlines':
            return 'simplifies'
        else:
            return 'simplify'

    # empower/empowers/empowered -> enable/enables/enabled
    if lower.startswith('empower'):
        if lower == 'empowered':
            return 'enabled'
        elif lower == 'empowers':
            return 'enables'
        else:
            return 'enable'

    # unleash/unleashes/unleashed -> unlock/unlocks/unlocked
    if lower.startswith('unleash'):
        if lower == 'unleashed':
            return 'unlocked'
        elif lower == 'unleashes':
            return 'unlocks'
        else:
            return 'unlock'

    # harness/harnesses/harnessed/harnessing -> use/uses/used/using
    if lower.startswith('harness'):
        if lower == 'harnessed':
            return 'used'
        elif lower == 'harnesses':
            return 'uses'
        elif lower == 'harnessing':
            return 'using'
        else:
            return 'use'

    # revolutionize/revolutionizes/revolutionized -> transform/transforms/transformed
    if lower.startswith('revolutionize'):
        if lower == 'revolutionized':
            return 'transformed'
        elif lower == 'revolutionizes':
            return 'transforms'
        else:
            return 'transform'

    return base_replacement


def fix_ai_language(content, filepath):
    """Replace figurative AI language, skipping literal uses."""
    changes = 0
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        new_line = line

        # Skip lines inside <script> JSON-LD blocks or JS code that contain synonym arrays
        # These are data/code, not editorial content
        # We detect this by checking if the line looks like JS array or JSON
        # Also skip lines inside <option> tags (form values)
        is_code_or_data = False
        stripped = line.strip()
        if (stripped.startswith('"') and ':' in stripped and ('[' in stripped or '{' in stripped)):
            is_code_or_data = True
        if '<option' in line and 'value=' in line:
            is_code_or_data = True
        # Skip script content - lines that are clearly inside JS
        if stripped.startswith('document.getElementById') or stripped.startswith('var ') or stripped.startswith('let ') or stripped.startswith('const '):
            is_code_or_data = True

        if not is_code_or_data:
            for pattern, base_repl, skip_contexts in AI_REPLACEMENTS:
                matches = list(re.finditer(pattern, new_line, re.IGNORECASE))
                if not matches:
                    continue

                # Check skip contexts - if any skip context is in the line, skip this replacement
                should_skip = False
                for ctx in skip_contexts:
                    if ctx.lower() in new_line.lower():
                        should_skip = True
                        break

                if should_skip:
                    continue

                # Apply replacements (reverse order to maintain positions)
                for m in reversed(matches):
                    original = m.group(0)
                    replacement = get_replacement(original, base_repl)
                    if replacement:
                        # Preserve original case for first letter
                        if original[0].isupper():
                            replacement = replacement[0].upper() + replacement[1:]
                        new_line = new_line[:m.start()] + replacement + new_line[m.end():]
                        changes += 1

        new_lines.append(new_line)

    if changes > 0:
        stats["ai_language_fixed"] += changes
        stats["files_modified"].add(filepath)
    return '\n'.join(new_lines)


# ============================================================
# MAIN: Process all files
# ============================================================

for filepath in tool_dirs:
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original = content

    # Apply all fixes in order
    content = fix_h2_ids(content, filepath)
    content = fix_og_image(content, filepath)
    content = fix_eeat_footer(content, filepath)
    content = fix_author_meta(content, filepath)
    content = fix_ai_language(content, filepath)

    # Only write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("=" * 60)
print("QUALITY FIX SUMMARY (p-t directories)")
print("=" * 60)
print(f"  H2 IDs added:        {stats['h2_ids_added']}")
print(f"  og:image added:      {stats['og_image_added']}")
print(f"  E-E-A-T footers:     {stats['footer_added']}")
print(f"  Author meta added:   {stats['author_added']}")
print(f"  AI language fixes:   {stats['ai_language_fixed']}")
print(f"  Files modified:      {len(stats['files_modified'])}")
print("=" * 60)
