#!/usr/bin/env python3
"""
Add Open Graph and Twitter Card meta tags to tool pages that are missing them.

Scans all */index.html files under the zovo-tools directory. For each file
that does NOT already contain 'og:title', it:
  1. Extracts the page title from the <title> tag (or <h1> as fallback)
  2. Extracts the description from <meta name="description"> (or generates one)
  3. Derives the tool slug from the directory name
  4. Inserts OG + Twitter meta tags into the <head> section
"""

import os
import re
import glob
import html

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://zovo.one/free-tools"


def extract_title(content):
    """Extract page title from <title> tag, falling back to <h1>."""
    m = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    if m:
        return html.unescape(m.group(1).strip())
    m = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
    if m:
        # Strip any inner HTML tags
        return html.unescape(re.sub(r'<[^>]+>', '', m.group(1)).strip())
    return None


def extract_meta_description(content):
    """Extract content from <meta name="description" content="...">."""
    m = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        content,
        re.IGNORECASE | re.DOTALL,
    )
    if m:
        return html.unescape(m.group(1).strip())
    return None


def generate_description(title):
    """Generate a fallback description from the tool title."""
    # Clean up the title: strip " | Zovo Tools", "| Zovo", "| Free Tool", etc.
    clean = re.sub(r'\s*[\|–-]\s*(Zovo\s*Tools?|Free\s*Tool).*$', '', title, flags=re.IGNORECASE).strip()
    # Remove leading "Free " for the sentence construction
    tool_name = re.sub(r'^Free\s+', '', clean, flags=re.IGNORECASE).strip()
    return f"Free online {tool_name.lower()}. Fast, accurate, and easy to use. No sign-up required."


def has_tag(content, property_or_name, value):
    """Check if a specific meta tag already exists."""
    # Check property="..." (OG tags)
    pattern1 = rf'<meta\s+property=["\']og:{re.escape(value)}["\']'
    # Check name="..." (twitter tags)
    pattern2 = rf'<meta\s+name=["\']twitter:{re.escape(value)}["\']'
    if re.search(pattern1, content, re.IGNORECASE):
        return True
    if re.search(pattern2, content, re.IGNORECASE):
        return True
    return False


def build_og_tags(title, description, slug):
    """Build the OG and Twitter meta tag block."""
    url = f"{SITE_URL}/{slug}/"
    # Escape for HTML attributes
    t = html.escape(title, quote=True)
    d = html.escape(description, quote=True)
    u = html.escape(url, quote=True)

    tags = []
    tags.append(f'<meta property="og:title" content="{t}">')
    tags.append(f'<meta property="og:description" content="{d}">')
    tags.append(f'<meta property="og:type" content="website">')
    tags.append(f'<meta property="og:url" content="{u}">')
    tags.append(f'<meta property="og:site_name" content="Zovo Tools">')
    tags.append(f'<meta name="twitter:card" content="summary_large_image">')
    tags.append(f'<meta name="twitter:title" content="{t}">')
    tags.append(f'<meta name="twitter:description" content="{d}">')

    return "\n".join(tags)


def find_insertion_point(content):
    """
    Find the best place to insert OG tags in the <head> section.

    Strategy: insert just before the first <script>, <style>, or <link rel="preconnect">
    tag that follows the last <meta> tag. If none found, insert before </head>.
    """
    # Find all meta tags and their positions
    meta_positions = [m.end() for m in re.finditer(r'<meta\s[^>]*>', content, re.IGNORECASE)]
    # Find all link canonical positions
    canonical_positions = [m.end() for m in re.finditer(r'<link\s+rel=["\']canonical["\'][^>]*>', content, re.IGNORECASE)]

    # Use the latest position among meta and canonical tags
    all_positions = meta_positions + canonical_positions
    if all_positions:
        last_meta_end = max(all_positions)
        # Find the end of the line (next newline)
        next_newline = content.find('\n', last_meta_end)
        if next_newline != -1:
            return next_newline + 1
        return last_meta_end

    # Fallback: insert before </head>
    head_close = re.search(r'</head>', content, re.IGNORECASE)
    if head_close:
        return head_close.start()

    return None


def process_file(filepath):
    """Process a single index.html file. Returns True if modified."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has OG tags
    if 'og:title' in content:
        return False, "already has OG tags"

    # Extract the tool slug from the directory name
    slug = os.path.basename(os.path.dirname(filepath))

    # Extract title
    title = extract_title(content)
    if not title:
        return False, "no title found"

    # Extract or generate description
    description = extract_meta_description(content)
    if not description:
        description = generate_description(title)

    # Build the OG tag block
    og_block = build_og_tags(title, description, slug)

    # Find insertion point
    insert_pos = find_insertion_point(content)
    if insert_pos is None:
        return False, "could not find insertion point"

    # Insert the OG tags
    new_content = content[:insert_pos] + "\n" + og_block + "\n" + content[insert_pos:]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, f"added OG tags (title: {title[:60]}...)" if len(title) > 60 else (True, f"added OG tags (title: {title})")


def main():
    files = sorted(glob.glob(os.path.join(BASE_DIR, '*/index.html')))

    total = 0
    enhanced = 0
    skipped = 0
    errors = 0

    print(f"Scanning {len(files)} tool pages for missing Open Graph tags...\n")

    for filepath in files:
        total += 1
        slug = os.path.basename(os.path.dirname(filepath))

        try:
            modified, reason = process_file(filepath)
            # Handle tuple return from the else branch
            if isinstance(modified, tuple):
                modified, reason = modified
            if modified:
                enhanced += 1
                print(f"  [ADDED]   {slug}: {reason}")
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"  [ERROR]   {slug}: {e}")

    print(f"\n{'='*60}")
    print(f"SUMMARY")
    print(f"{'='*60}")
    print(f"  Total tools scanned:  {total}")
    print(f"  Already had OG tags:  {skipped}")
    print(f"  Enhanced with OG:     {enhanced}")
    print(f"  Errors:               {errors}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
