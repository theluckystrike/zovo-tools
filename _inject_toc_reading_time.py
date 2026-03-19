#!/usr/bin/env python3
"""
Inject Table of Contents and Reading Time into all tool index.html files.
Processes 162 tool directories under ~/zovo-workspaces/zovo-tools/.
"""

import os
import re
import glob
from html.parser import HTMLParser


# --- Config ---
TOOLS_DIR = os.path.expanduser("~/zovo-workspaces/zovo-tools")
WPM = 238
MIN_H2_FOR_TOC = 3

# H2 headings to exclude from TOC
EXCLUDED_H2_TEXTS = {
    "frequently asked questions",
    "faq",
    "faqs",
    "related tools",
    "navigation",
    "main content area",
}


def slugify(text):
    """Convert heading text to a URL-friendly slug."""
    slug = text.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug


class TextExtractor(HTMLParser):
    """Extract visible text from HTML, ignoring scripts and styles."""
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self._skip = False
        self._skip_tags = {'script', 'style', 'noscript'}

    def handle_starttag(self, tag, attrs):
        if tag in self._skip_tags:
            self._skip = True

    def handle_endtag(self, tag):
        if tag in self._skip_tags:
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self.text_parts.append(data)

    def get_text(self):
        return ' '.join(self.text_parts)


def extract_text(html):
    """Get visible text content from HTML."""
    parser = TextExtractor()
    parser.feed(html)
    return parser.get_text()


def count_words(text):
    """Count words in text."""
    return len(text.split())


def extract_h2_headings(html):
    """Extract all H2 headings with their text content (stripped of HTML tags).
    Returns list of (full_match, tag_with_attrs, inner_html, plain_text, has_id, existing_id)."""
    # Match <h2 ...>...</h2> including multiline
    pattern = re.compile(r'(<h2([^>]*)>)(.*?)</h2>', re.IGNORECASE | re.DOTALL)
    headings = []
    for m in pattern.finditer(html):
        full_match = m.group(0)
        open_tag = m.group(1)       # e.g. <h2 style="...">
        attrs_str = m.group(2)      # e.g.  style="..."
        inner_html = m.group(3)     # e.g. Understanding <span>BMI</span>
        # Strip HTML tags from inner to get plain text
        plain_text = re.sub(r'<[^>]+>', '', inner_html).strip()

        # Check if it already has an id
        id_match = re.search(r'id=["\']([^"\']+)["\']', attrs_str)
        has_id = id_match is not None
        existing_id = id_match.group(1) if id_match else None

        headings.append({
            'full_match': full_match,
            'open_tag': open_tag,
            'attrs_str': attrs_str,
            'inner_html': inner_html,
            'plain_text': plain_text,
            'has_id': has_id,
            'existing_id': existing_id,
        })
    return headings


def should_include_in_toc(heading_text):
    """Check if this heading should be included in the TOC."""
    return heading_text.lower().strip() not in EXCLUDED_H2_TEXTS


def build_toc_html(headings_for_toc):
    """Build the TOC nav HTML from a list of (slug, text) tuples."""
    items = []
    for slug, text in headings_for_toc:
        items.append(
            f'    <li style="margin:0.4rem 0;">'
            f'<a href="#{slug}" style="color:#00ccff;text-decoration:none;font-size:0.9rem;">{text}</a>'
            f'</li>'
        )
    items_html = '\n'.join(items)
    return (
        f'<nav class="toc" aria-label="Table of Contents" style="background:#12121a;border:1px solid #2a2a3a;border-radius:8px;padding:1.25rem;margin:1.5rem 0;">\n'
        f'  <div style="font-family:monospace;font-size:0.75rem;letter-spacing:0.1em;text-transform:uppercase;color:#8888a0;margin-bottom:0.75rem;">Contents</div>\n'
        f'  <ol style="list-style:none;padding:0;margin:0;">\n'
        f'{items_html}\n'
        f'  </ol>\n'
        f'</nav>'
    )


def build_reading_time_html(word_count):
    """Build the reading time div HTML."""
    minutes = max(1, round(word_count / WPM))
    return (
        f'<div class="reading-time" style="font-family:monospace;font-size:0.75rem;color:#8888a0;letter-spacing:0.05em;margin:0.5rem 0 1.5rem;">\n'
        f'  {minutes} min read &middot; {word_count} words\n'
        f'</div>'
    )


def find_h1_insertion_point(html):
    """Find the position right after the closing </h1> tag (first occurrence).
    Returns the end position of the first </h1>, or None."""
    # Find the first <h1...>...</h1> in the <body> section
    body_match = re.search(r'<body', html, re.IGNORECASE)
    start_search = body_match.start() if body_match else 0

    # Find first h1 closing tag after body
    h1_pattern = re.compile(r'</h1>', re.IGNORECASE)
    m = h1_pattern.search(html, start_search)
    if m:
        return m.end()
    return None


def find_insertion_after_h1_line(html, h1_end_pos):
    """Find the right place to insert after the H1 line.
    We want to insert after the H1's closing tag, but we need to handle
    cases where there's a subtitle <p> right after.
    Returns the insertion position."""
    # Look at what comes after the </h1>
    # Skip whitespace
    rest = html[h1_end_pos:]

    # Check if there's a subtitle paragraph or descriptive <p> right after
    # We'll insert after that paragraph if it looks like a subtitle
    subtitle_match = re.match(r'\s*<p\s+class=["\']subtitle["\'][^>]*>.*?</p>', rest, re.IGNORECASE | re.DOTALL)
    if subtitle_match:
        return h1_end_pos + subtitle_match.end()

    # Also check for a plain <p> with style that looks like a subtitle (short, styled)
    # Common pattern: <p style="color:#aaa;...">description text</p>
    styled_p_match = re.match(r'\s*<p\s+style="[^"]*color:#[a-f0-9]{3,6}[^"]*"[^>]*>.*?</p>', rest, re.IGNORECASE | re.DOTALL)
    if styled_p_match:
        # Only treat it as subtitle if it's relatively short (< 500 chars)
        if len(styled_p_match.group(0)) < 500:
            return h1_end_pos + styled_p_match.end()

    return h1_end_pos


def process_file(filepath):
    """Process a single index.html file. Returns a status string."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Check if already processed
    if 'class="toc"' in html and 'class="reading-time"' in html:
        return 'already_done'
    has_toc = 'class="toc"' in html
    has_reading_time = 'class="reading-time"' in html

    if has_toc and has_reading_time:
        return 'already_done'

    # Extract text and count words
    visible_text = extract_text(html)
    word_count = count_words(visible_text)

    # Extract H2 headings
    all_h2s = extract_h2_headings(html)

    # Filter headings for TOC (exclude FAQ, Related Tools, etc.)
    toc_h2s = [h for h in all_h2s if should_include_in_toc(h['plain_text'])]

    # Determine slugs and add id attributes to H2s that don't have them
    slug_counts = {}
    headings_for_toc = []
    modified_html = html

    for h in all_h2s:
        if h['has_id']:
            slug = h['existing_id']
        else:
            slug = slugify(h['plain_text'])

        # Deduplicate slugs
        if slug in slug_counts:
            slug_counts[slug] += 1
            unique_slug = f"{slug}-{slug_counts[slug]}"
        else:
            slug_counts[slug] = 0
            unique_slug = slug

        # Add id to H2 if it doesn't have one
        if not h['has_id']:
            new_open_tag = h['open_tag'].replace('<h2', f'<h2 id="{unique_slug}"', 1)
            new_full = h['full_match'].replace(h['open_tag'], new_open_tag, 1)
            modified_html = modified_html.replace(h['full_match'], new_full, 1)
            # Update the full_match reference so further replacements work
            h['full_match'] = new_full
            h['open_tag'] = new_open_tag
            h['assigned_slug'] = unique_slug
        else:
            h['assigned_slug'] = slug if slug_counts[slug] == 0 else unique_slug

        # Add to TOC list if it should be included
        if should_include_in_toc(h['plain_text']):
            headings_for_toc.append((h['assigned_slug'], h['plain_text']))

    # Find insertion point (after first H1)
    h1_end = find_h1_insertion_point(modified_html)
    if h1_end is None:
        return 'no_h1'

    insert_pos = find_insertion_after_h1_line(modified_html, h1_end)

    # Build what to insert
    inserts = []

    if not has_reading_time:
        inserts.append(build_reading_time_html(word_count))

    if not has_toc and len(headings_for_toc) >= MIN_H2_FOR_TOC:
        inserts.append(build_toc_html(headings_for_toc))

    if not inserts:
        # Nothing to insert (e.g. already has reading time and not enough H2s for TOC)
        if modified_html != html:
            # But we did add id attributes to H2s
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(modified_html)
            return 'ids_only'
        return 'skipped'

    injection = '\n' + '\n'.join(inserts) + '\n'

    final_html = modified_html[:insert_pos] + injection + modified_html[insert_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(final_html)

    has_new_toc = not has_toc and len(headings_for_toc) >= MIN_H2_FOR_TOC
    has_new_reading = not has_reading_time
    if has_new_toc and has_new_reading:
        return 'toc_and_reading'
    elif has_new_toc:
        return 'toc_only'
    elif has_new_reading:
        return 'reading_only'
    return 'modified'


def main():
    # Find all tool directories with index.html
    pattern = os.path.join(TOOLS_DIR, "*/index.html")
    files = sorted(glob.glob(pattern))

    # Filter out non-tool directories (like CNAME, scripts, etc.)
    tool_files = []
    for f in files:
        dirname = os.path.basename(os.path.dirname(f))
        # Skip hidden dirs, CNAME, files starting with _ or .
        if dirname.startswith('.') or dirname.startswith('_') or dirname == 'CNAME':
            continue
        tool_files.append(f)

    print(f"Found {len(tool_files)} tool pages to process\n")

    stats = {
        'toc_and_reading': 0,
        'toc_only': 0,
        'reading_only': 0,
        'ids_only': 0,
        'already_done': 0,
        'no_h1': 0,
        'skipped': 0,
        'errors': 0,
    }
    errors = []

    for filepath in tool_files:
        tool_name = os.path.basename(os.path.dirname(filepath))
        try:
            result = process_file(filepath)
            stats[result] = stats.get(result, 0) + 1
            if result == 'toc_and_reading':
                print(f"  [TOC+READ] {tool_name}")
            elif result == 'reading_only':
                print(f"  [READ]     {tool_name}")
            elif result == 'toc_only':
                print(f"  [TOC]      {tool_name}")
            elif result == 'ids_only':
                print(f"  [IDS]      {tool_name}")
            elif result == 'no_h1':
                print(f"  [NO-H1]    {tool_name}")
            elif result == 'already_done':
                print(f"  [SKIP]     {tool_name}")
            elif result == 'skipped':
                print(f"  [SKIP]     {tool_name}")
        except Exception as e:
            stats['errors'] += 1
            errors.append((tool_name, str(e)))
            print(f"  [ERROR]    {tool_name}: {e}")

    print(f"\n{'='*55}")
    print(f"SUMMARY")
    print(f"{'='*55}")
    print(f"  Total tool pages found:        {len(tool_files)}")
    print(f"  TOC + Reading time added:      {stats['toc_and_reading']}")
    print(f"  Reading time only added:       {stats['reading_only']}")
    print(f"  TOC only added:                {stats['toc_only']}")
    print(f"  IDs only added (no injection): {stats['ids_only']}")
    print(f"  Already had both:              {stats['already_done']}")
    print(f"  Skipped (no changes needed):   {stats['skipped']}")
    print(f"  No H1 found:                   {stats['no_h1']}")
    print(f"  Errors:                        {stats['errors']}")
    total_enhanced = stats['toc_and_reading'] + stats['reading_only'] + stats['toc_only'] + stats['ids_only']
    print(f"  ---")
    print(f"  Total files enhanced:          {total_enhanced}")

    if errors:
        print(f"\nErrors detail:")
        for name, err in errors:
            print(f"  {name}: {err}")


if __name__ == '__main__':
    main()
