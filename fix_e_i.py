#!/usr/bin/env python3
"""
Surgical quality fixes for all tool index.html files in directories e-i.
FIX 1: Add id attributes to H2 tags missing them
FIX 2: Add og:image meta tag where missing
FIX 3: Add E-E-A-T footer where missing
FIX 4: Add author meta where missing
FIX 5: Fix AI language (figurative uses only)
"""

import os
import re
import glob

BASE = '/Users/mike/zovo-workspaces/zovo-tools/'

def get_files():
    """Get all index.html files in e-i directories."""
    files = sorted(glob.glob(BASE + '[e-i]*/index.html'))
    return [f for f in files if os.path.isfile(f)]

def slugify(text):
    """Convert heading text to a slug id."""
    # Strip HTML tags first
    text = re.sub(r'<[^>]+>', '', text)
    # Decode HTML entities
    text = text.replace('&amp;', 'and').replace('&', 'and')
    text = re.sub(r'&[a-zA-Z]+;', '', text)
    text = re.sub(r'&#\d+;', '', text)
    # Lowercase
    text = text.lower().strip()
    # Replace spaces and non-alphanum with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Strip leading/trailing hyphens
    text = text.strip('-')
    return text

def fix_h2_ids(content):
    """FIX 1: Add id attributes to all H2 tags missing them."""
    used_ids = set()

    # First, collect all existing H2 ids
    for m in re.finditer(r'<h2[^>]*\bid=["\']([^"\']+)["\']', content):
        used_ids.add(m.group(1))

    def replace_h2(match):
        tag = match.group(0)
        # Check if this h2 already has an id
        if re.search(r'\bid=', tag):
            return tag

        # Extract text content between <h2...> and </h2>
        # We need to find the closing tag after this match
        start = match.end()
        close_idx = content.find('</h2>', start)
        if close_idx == -1:
            # Inline content: try to get text from within the tag if self-closing-ish
            return tag

        inner = content[start:close_idx]
        slug = slugify(inner)

        if not slug:
            return tag

        # Handle duplicates
        final_slug = slug
        counter = 2
        while final_slug in used_ids:
            final_slug = f"{slug}-{counter}"
            counter += 1
        used_ids.add(final_slug)

        # Insert id after <h2
        new_tag = tag[:3] + f' id="{final_slug}"' + tag[3:]
        return new_tag

    # Match <h2 with any attributes but NOT already containing id=
    # We process each <h2 tag
    result = re.sub(r'<h2(?=[^>]*>)', replace_h2, content)
    return result

def fix_og_image(content):
    """FIX 2: Add og:image meta tag where missing."""
    if 'og:image' in content:
        return content

    og_image_tag = '<meta property="og:image" content="https://zovo.one/og-image.png">'

    # Find the last og: meta tag and insert after it
    og_matches = list(re.finditer(r'<meta\s+property="og:[^"]*"[^>]*>', content))
    if og_matches:
        last_og = og_matches[-1]
        insert_pos = last_og.end()
        content = content[:insert_pos] + '\n' + og_image_tag + content[insert_pos:]
    else:
        # No og tags at all - insert before </head>
        content = content.replace('</head>', og_image_tag + '\n</head>', 1)

    return content

def fix_eeat_footer(content, filepath):
    """FIX 3: Add E-E-A-T footer where missing (check bottom 30%)."""
    lines = content.split('\n')
    total = len(lines)
    bottom_start = int(total * 0.7)
    bottom = '\n'.join(lines[bottom_start:])

    if 'Michael Lip' in bottom:
        return content

    footer = '<footer style="text-align:center;padding:24px;color:#b0b0c0;font-size:0.85rem;border-top:1px solid #1e1e2a;margin-top:40px;">Built by Michael Lip \u00b7 More free tools at <a href="https://zovo.one/free-tools/" style="color:#00ff88;text-decoration:none;">zovo.one</a></footer>'

    # Insert before </body>
    content = content.replace('</body>', footer + '\n</body>', 1)
    return content

def fix_author_meta(content):
    """FIX 4: Add author meta where missing."""
    if 'name="author"' in content:
        return content

    author_tag = '<meta name="author" content="Michael Lip">'

    # Insert after <meta name="description"...> or after <meta name="viewport"...>
    desc_match = re.search(r'<meta\s+name="description"[^>]*>', content)
    if desc_match:
        insert_pos = desc_match.end()
        content = content[:insert_pos] + '\n' + author_tag + content[insert_pos:]
    else:
        viewport_match = re.search(r'<meta\s+name="viewport"[^>]*>', content)
        if viewport_match:
            insert_pos = viewport_match.end()
            content = content[:insert_pos] + '\n' + author_tag + content[insert_pos:]
        else:
            content = content.replace('</head>', author_tag + '\n</head>', 1)

    return content

def fix_ai_language(content, filepath):
    """FIX 5: Fix AI language - only figurative uses."""
    dirname = os.path.basename(os.path.dirname(filepath))
    changes = []

    # === LANDSCAPE ===
    # Skip files where "landscape" is used literally (orientation, photos, etc.)
    # We need context-aware replacement
    def replace_landscape(match):
        full = match.group(0)
        # Get surrounding context (100 chars before and after)
        start = max(0, match.start() - 120)
        end = min(len(content), match.end() + 120)
        ctx = content[start:end].lower()

        # Skip literal uses
        literal_patterns = [
            'landscape orientation', 'landscape mode', 'portrait and landscape',
            'landscape and portrait', 'portrait or landscape', 'landscape or portrait',
            'value="landscape"', 'landscape"', "'landscape'", 'landscape photo',
            'landscape image', 'landscape option', 'option value', 'orient',
            'landscape</option', 'landscape</strong', '<option', 'jspdf',
            'imgw > imgh', 'pagesize', 'pagew', 'pageh',
            # image metadata viewer - scene types
            'scene_types', 'scene type', 'capture type', 'standard',
            # gravel calculator - literal landscaping
            'landscaper', 'landscape supply', 'landscape fabric',
            'landscape edging', 'landscape mulch', 'landscape cover',
            'landscape yard', 'professional landscaper',
            # flow chart maker - tablet landscape mode
            'tablet', 'responsive', 'phone',
            # heic-to-pdf - page orientation
            'page', 'orient', 'pdf',
        ]

        for pat in literal_patterns:
            if pat in ctx:
                return full

        # Figurative uses: "the landscape of...", "... landscape", "market landscape",
        # "current landscape", "digital landscape", "... landscape ..."
        word = match.group(1)
        # Determine replacement
        if 'digital' in ctx or 'reading' in ctx:
            replacement = 'space'
        elif 'market' in ctx or 'loan' in ctx or 'mortgage' in ctx or 'equity' in ctx:
            replacement = 'market'
        elif 'opinion' in ctx or 'complex' in ctx:
            replacement = 'field'
        else:
            replacement = 'space'

        # Preserve case
        if word[0].isupper():
            replacement = replacement.capitalize()

        changes.append(f"  landscape -> {replacement}")
        return full.replace(word, replacement)

    content = re.sub(r'\b(L|l)(andscape)\b(?!["\'])',
                     lambda m: replace_landscape_smart(m, content, changes), content)

    # === ELEVATE ===
    def replace_elevate(match):
        word = match.group(0)
        start = max(0, match.start() - 100)
        end = min(len(content), match.end() + 100)
        ctx = content[start:end].lower()

        # Skip literal uses (elevate body temperature, elevated off floor, etc.)
        literal = ['temperature', 'off the floor', 'off floor', 'elevated off',
                   'router', 'placement', 'position', 'centrally', 'wall']
        for pat in literal:
            if pat in ctx:
                return word

        # Figurative
        if 'elevated' in word.lower():
            rep = 'higher' if 'rate' in ctx or 'interest' in ctx else 'improved'
        elif 'elevate' in word.lower():
            rep = 'improve'
        else:
            rep = 'improve'

        if word[0].isupper():
            rep = rep.capitalize()

        # Match form: elevate/elevates/elevated/elevating
        if word.lower() == 'elevated':
            rep = 'high' if 'rate' in ctx or 'interest' in ctx else 'improved'
        elif word.lower() == 'elevates':
            rep = 'improves'
        elif word.lower() == 'elevating':
            rep = 'improving'

        if word[0].isupper():
            rep = rep.capitalize()

        changes.append(f"  {word} -> {rep}")
        return rep

    content = re.sub(r'\b[Ee]levat(?:e|es|ed|ing)\b', replace_elevate, content)

    # === STREAMLINE ===
    def replace_streamline(match):
        word = match.group(0)
        start = max(0, match.start() - 100)
        end = min(len(content), match.end() + 100)
        ctx = content[start:end].lower()

        # Skip proper nouns like "Streamlined NTRU Prime" or when in quotes for headline analyzer word lists
        if 'ntru' in ctx:
            return word
        # Skip when it's inside a JS string array (headline analyzer word lists)
        local_ctx = content[max(0, match.start()-5):match.end()+5]
        if "'" in local_ctx[:5] or '"' in local_ctx[:5]:
            # Could be in a JS array - check more carefully
            line_start = content.rfind('\n', 0, match.start())
            line = content[line_start:match.end()+50]
            if ("'" in line and "," in line) or ('"' in line and "," in line):
                # Likely in a JS array, keep as is
                if 'signal' not in ctx[:80]:
                    return word

        # Also skip the headline-analyzer article text that describes the word itself
        if 'signal specificity' in ctx or 'signal' in ctx:
            return word

        rep = word.lower()
        if rep == 'streamline':
            rep = 'simplify'
        elif rep == 'streamlines':
            rep = 'simplifies'
        elif rep == 'streamlined':
            rep = 'simplified'
        elif rep == 'streamlining':
            rep = 'simplifying'
        else:
            rep = 'simplify'

        if word[0].isupper():
            rep = rep.capitalize()

        changes.append(f"  {word} -> {rep}")
        return rep

    content = re.sub(r'\b[Ss]treamlin(?:e|es|ed|ing)\b', replace_streamline, content)

    # === EMPOWER ===
    def replace_empower(match):
        word = match.group(0)
        start = max(0, match.start() - 60)
        end = min(len(content), match.end() + 60)
        ctx = content[start:end].lower()

        # Skip when in JS arrays (headline analyzer)
        local_ctx = content[max(0, match.start()-5):match.end()+5]
        if "'" in local_ctx[:5] or '"' in local_ctx[:5]:
            line_start = content.rfind('\n', 0, match.start())
            line = content[line_start:match.end()+50]
            if ("'" in line and "," in line):
                return word

        rep = word.lower()
        if rep == 'empower':
            rep = 'enable'
        elif rep == 'empowers':
            rep = 'enables'
        elif rep == 'empowered':
            rep = 'enabled'
        elif rep == 'empowering':
            rep = 'enabling'
        else:
            rep = 'enable'

        if word[0].isupper():
            rep = rep.capitalize()

        changes.append(f"  {word} -> {rep}")
        return rep

    content = re.sub(r'\b[Ee]mpower(?:s|ed|ing|ment)?\b', replace_empower, content)

    # === UNLEASH ===
    def replace_unleash(match):
        word = match.group(0)
        rep = word.lower()
        if rep in ('unleash', 'unleashes'):
            rep = 'unlock' if rep == 'unleash' else 'unlocks'
        elif rep == 'unleashed':
            rep = 'unlocked'
        elif rep == 'unleashing':
            rep = 'unlocking'
        else:
            rep = 'unlock'
        if word[0].isupper():
            rep = rep.capitalize()
        changes.append(f"  {word} -> {rep}")
        return rep

    content = re.sub(r'\b[Uu]nleash(?:es|ed|ing)?\b', replace_unleash, content)

    # === HARNESS ===
    def replace_harness(match):
        word = match.group(0)
        rep = word.lower()
        if rep == 'harness':
            rep = 'use'
        elif rep == 'harnesses':
            rep = 'uses'
        elif rep == 'harnessed':
            rep = 'used'
        elif rep == 'harnessing':
            rep = 'using'
        else:
            rep = 'use'
        if word[0].isupper():
            rep = rep.capitalize()
        changes.append(f"  {word} -> {rep}")
        return rep

    content = re.sub(r'\b[Hh]arness(?:es|ed|ing)?\b', replace_harness, content)

    # === REVOLUTIONIZE ===
    def replace_revolutionize(match):
        word = match.group(0)
        rep = word.lower()
        if rep == 'revolutionize':
            rep = 'transform'
        elif rep == 'revolutionizes':
            rep = 'transforms'
        elif rep == 'revolutionized':
            rep = 'transformed'
        elif rep == 'revolutionizing':
            rep = 'transforming'
        else:
            rep = 'transform'
        if word[0].isupper():
            rep = rep.capitalize()
        changes.append(f"  {word} -> {rep}")
        return rep

    content = re.sub(r'\b[Rr]evolutioniz(?:e|es|ed|ing)\b', replace_revolutionize, content)

    if changes:
        print(f"  AI language fixes in {dirname}:")
        for c in changes:
            print(f"    {c}")

    return content


def replace_landscape_smart(match, full_content, changes):
    """Context-aware landscape replacement."""
    word = match.group(0)
    pos = match.start()

    start = max(0, pos - 150)
    end = min(len(full_content), pos + len(word) + 150)
    ctx = full_content[start:end].lower()

    # Skip literal uses
    literal_indicators = [
        'orientation', 'portrait', 'mode', 'value="', "value='",
        'option', 'orient', 'jspdf', 'imgw', 'imgh', 'pagew', 'pageh',
        'pagesize', 'scene_type', 'capture type', 'tablet', 'responsive',
        'phone', 'screen size', 'pdf', 'page size',
        # gravel/landscaping literal
        'landscaper', 'landscape supply', 'landscape fabric',
        'landscape edging', 'landscape mulch', 'landscape cover',
        'landscape yard', 'quarr', 'decorative',
        'weed', 'gravel', 'garden', 'soil', 'foundation',
        'drainage', 'depth', 'river rock', 'pea gravel',
        'steel', 'edging', 'linear foot', 'cubic',
        # image types
        'image', 'photo', 'batch', 'resize',
        # metadata
        'scene', 'metering', 'capture',
    ]

    for pat in literal_indicators:
        if pat in ctx:
            return word

    # If we get here, it's likely figurative
    if 'digital' in ctx or 'reading' in ctx:
        rep = 'space'
    elif 'market' in ctx or 'loan' in ctx or 'mortgage' in ctx:
        rep = 'market'
    elif 'opinion' in ctx or 'evidence' in ctx:
        rep = 'mix'
    elif 'equity' in ctx:
        rep = 'market'
    elif '2025' in ctx or 'current' in ctx:
        rep = 'market'
    else:
        rep = 'space'

    if word[0].isupper():
        rep = rep.capitalize()

    changes.append(f"  {word} -> {rep}")
    return rep


def main():
    files = get_files()
    print(f"Processing {len(files)} files in e-i directories...\n")

    stats = {
        'h2_ids_added': 0,
        'og_image_added': 0,
        'footer_added': 0,
        'author_added': 0,
        'ai_lang_fixed': 0,
        'files_modified': 0,
    }

    for filepath in files:
        dirname = os.path.basename(os.path.dirname(filepath))
        original = open(filepath, 'r', encoding='utf-8').read()
        content = original

        # FIX 1: H2 IDs
        before_h2 = len(re.findall(r'<h2(?![^>]*\bid=)[^>]*>', content))
        content = fix_h2_ids(content)
        after_h2 = len(re.findall(r'<h2(?![^>]*\bid=)[^>]*>', content))
        h2_fixed = before_h2 - after_h2
        if h2_fixed > 0:
            stats['h2_ids_added'] += h2_fixed
            print(f"  [{dirname}] Added {h2_fixed} H2 id(s)")

        # FIX 2: og:image
        had_og = 'og:image' in content
        content = fix_og_image(content)
        if not had_og and 'og:image' in content:
            stats['og_image_added'] += 1
            print(f"  [{dirname}] Added og:image")

        # FIX 3: E-E-A-T footer
        before_footer = content
        content = fix_eeat_footer(content, filepath)
        if content != before_footer:
            stats['footer_added'] += 1
            print(f"  [{dirname}] Added E-E-A-T footer")

        # FIX 4: Author meta
        had_author = 'name="author"' in content
        content = fix_author_meta(content)
        if not had_author and 'name="author"' in content:
            stats['author_added'] += 1
            print(f"  [{dirname}] Added author meta")

        # FIX 5: AI language
        before_ai = content
        content = fix_ai_language(content, filepath)
        if content != before_ai:
            stats['ai_lang_fixed'] += 1

        # Write back if changed
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_modified'] += 1

    print(f"\n{'='*50}")
    print(f"SUMMARY:")
    print(f"  Files processed: {len(files)}")
    print(f"  Files modified:  {stats['files_modified']}")
    print(f"  H2 IDs added:    {stats['h2_ids_added']}")
    print(f"  og:image added:  {stats['og_image_added']}")
    print(f"  Footers added:   {stats['footer_added']}")
    print(f"  Author meta:     {stats['author_added']}")
    print(f"  AI lang files:   {stats['ai_lang_fixed']}")

if __name__ == '__main__':
    main()
