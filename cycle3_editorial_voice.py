#!/usr/bin/env python3
"""
Cycle 3: Editorial voice check on ALL articles.
Checks for:
- "we" or "our team" language (should use "I" / Michael Lip perspective)
- "users" (should say "you" instead)
- Hashtags (#)
- Markdown-style bold (**text**)
- Colons as separators in headings (use middle dots if needed)
- Inconsistent date formats (03/2026 instead of March 2026)
"""

import os
import re
from collections import defaultdict

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools/articles"

def extract_visible_text(html):
    """Extract only visible text from HTML."""
    text = re.sub(r'<script[\s\S]*?</script>', ' ', html, flags=re.IGNORECASE)
    text = re.sub(r'<style[\s\S]*?</style>', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'<!--[\s\S]*?-->', ' ', text)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    return text

def extract_headings(html):
    """Extract all heading text from HTML."""
    headings = []
    for m in re.finditer(r'<h[1-6][^>]*>(.*?)</h[1-6]>', html, re.IGNORECASE | re.DOTALL):
        heading_html = m.group(1)
        heading_text = re.sub(r'<[^>]+>', '', heading_html).strip()
        headings.append(heading_text)
    return headings

def check_we_our(text):
    """Check for 'we', 'our team', etc. but not in legitimate contexts."""
    issues = []

    # "we" patterns that indicate non-first-person writing
    we_patterns = [
        (r'\bwe\s+(?:have|will|can|provide|offer|recommend|believe|think|suggest|created|built|designed|developed)\b', 'we + verb'),
        (r'\bour\s+(?:team|tool|tools|platform|service|calculator|app|product)\b', 'our + noun'),
        (r'\bwe\'ve\b', "we've"),
        (r'\bwe\'re\b', "we're"),
        (r'\bwe\'ll\b', "we'll"),
    ]

    for pattern, label in we_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            # Get context for each match
            for m in re.finditer(pattern, text, re.IGNORECASE):
                start = max(0, m.start() - 30)
                end = min(len(text), m.end() + 30)
                context = text[start:end].strip().replace('\n', ' ')
                issues.append(f'{label}: "...{context}..."')

    return issues

def check_users_word(text):
    """Check for 'users' (should be 'you')."""
    issues = []
    # "users" as a standalone word (not "user's" possessive in technical context)
    for m in re.finditer(r'\busers\b', text, re.IGNORECASE):
        start = max(0, m.start() - 30)
        end = min(len(text), m.end() + 30)
        context = text[start:end].strip().replace('\n', ' ')
        issues.append(f'"...{context}..."')
    return issues

def check_hashtags(text):
    """Check for hashtags (# followed by word, not heading markers)."""
    issues = []
    # Match hashtags like #coding, #webdev, etc.
    for m in re.finditer(r'#[a-zA-Z]\w{2,}', text):
        if not re.search(r'color:\s*$|background:\s*$|border:\s*$', text[max(0,m.start()-20):m.start()]):
            context = text[max(0,m.start()-20):min(len(text),m.end()+20)].strip()
            issues.append(f'"...{context}..."')
    return issues

def check_markdown_bold(html):
    """Check for **text** markdown bold in visible content."""
    issues = []
    text = extract_visible_text(html)
    for m in re.finditer(r'\*\*[^*]+\*\*', text):
        context = m.group()[:60]
        issues.append(f'"...{context}..."')
    return issues

def check_colon_headings(headings):
    """Check for colons as separators in headings."""
    issues = []
    for heading in headings:
        # Colon followed by space and text (e.g., "Section: Details")
        # But allow times like "10:00" and ratios
        if re.search(r'[a-zA-Z]:\s+[A-Z]', heading):
            issues.append(heading)
    return issues

def check_date_formats(text):
    """Check for inconsistent date formats."""
    issues = []
    # Check for numeric date formats like 03/2026, 2026-03, etc.
    for m in re.finditer(r'\b(?:0[1-9]|1[0-2])/20\d{2}\b', text):
        issues.append(f'Numeric date: "{m.group()}"')
    for m in re.finditer(r'\b20\d{2}-(?:0[1-9]|1[0-2])\b', text):
        # Allow ISO dates in schema/meta
        if m.group() not in text[:100]:  # Skip if in meta section
            issues.append(f'ISO date: "{m.group()}"')
    return issues

def fix_we_our_in_html(html):
    """Fix 'we/our' language in HTML text content."""
    changes = 0

    def replace_in_text(text):
        nonlocal changes
        original = text

        # Replace common "we" patterns
        replacements = [
            (r'\bWe have\b', 'I have'),
            (r'\bwe have\b', 'I have'),
            (r'\bWe provide\b', 'I provide'),
            (r'\bwe provide\b', 'I provide'),
            (r'\bWe offer\b', 'I offer'),
            (r'\bwe offer\b', 'I offer'),
            (r'\bWe recommend\b', 'I recommend'),
            (r'\bwe recommend\b', 'I recommend'),
            (r'\bWe believe\b', 'I believe'),
            (r'\bwe believe\b', 'I believe'),
            (r'\bWe created\b', 'I created'),
            (r'\bwe created\b', 'I created'),
            (r'\bWe built\b', 'I built'),
            (r'\bwe built\b', 'I built'),
            (r'\bWe designed\b', 'I designed'),
            (r'\bwe designed\b', 'I designed'),
            (r'\bWe developed\b', 'I developed'),
            (r'\bwe developed\b', 'I developed'),
            (r"\bWe've\b", "I've"),
            (r"\bwe've\b", "I've"),
            (r"\bWe're\b", "I'm"),
            (r"\bwe're\b", "I'm"),
            (r"\bWe'll\b", "I'll"),
            (r"\bwe'll\b", "I'll"),
            (r'\bWe can\b', 'You can'),
            (r'\bwe can\b', 'you can'),
            (r'\bWe will\b', 'I will'),
            (r'\bwe will\b', 'I will'),
            (r'\bWe suggest\b', 'I suggest'),
            (r'\bwe suggest\b', 'I suggest'),
            (r'\bWe think\b', 'I think'),
            (r'\bwe think\b', 'I think'),
            (r'\bour team\b', 'I'),
            (r'\bOur team\b', 'I'),
            (r'\bour tool\b', 'this tool'),
            (r'\bOur tool\b', 'This tool'),
            (r'\bour tools\b', 'these tools'),
            (r'\bOur tools\b', 'These tools'),
            (r'\bour platform\b', 'this platform'),
            (r'\bOur platform\b', 'This platform'),
            (r'\bour calculator\b', 'this calculator'),
            (r'\bOur calculator\b', 'This calculator'),
        ]

        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text)

        if text != original:
            changes += 1
        return text

    # Process only text content (not scripts/styles/tags)
    parts = re.split(r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)', html, flags=re.IGNORECASE)
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            result.append(part)
        else:
            tag_parts = re.split(r'(<[^>]+>)', part)
            for j, tp in enumerate(tag_parts):
                if j % 2 == 1:
                    result.append(tp)
                else:
                    result.append(replace_in_text(tp))

    return ''.join(result), changes

def fix_users_in_html(html):
    """Replace 'users' with 'you' in context."""
    changes = 0

    def replace_in_text(text):
        nonlocal changes
        original = text
        # "users can" -> "you can", "users will" -> "you will", etc.
        text = re.sub(r'\bUsers can\b', 'You can', text)
        text = re.sub(r'\busers can\b', 'you can', text)
        text = re.sub(r'\bUsers will\b', 'You will', text)
        text = re.sub(r'\busers will\b', 'you will', text)
        text = re.sub(r'\bUsers should\b', 'You should', text)
        text = re.sub(r'\busers should\b', 'you should', text)
        text = re.sub(r'\bUsers need\b', 'You need', text)
        text = re.sub(r'\busers need\b', 'you need', text)
        text = re.sub(r'\bfor users\b', 'for you', text)
        text = re.sub(r'\bFor users\b', 'For you', text)
        text = re.sub(r'\ballow users\b', 'let you', text)
        text = re.sub(r'\bAllow users\b', 'Let you', text)
        text = re.sub(r'\benable users\b', 'let you', text)
        text = re.sub(r'\bEnable users\b', 'Let you', text)
        text = re.sub(r'\bhelp users\b', 'help you', text)
        text = re.sub(r'\bHelp users\b', 'Help you', text)
        if text != original:
            changes += 1
        return text

    parts = re.split(r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)', html, flags=re.IGNORECASE)
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            result.append(part)
        else:
            tag_parts = re.split(r'(<[^>]+>)', part)
            for j, tp in enumerate(tag_parts):
                if j % 2 == 1:
                    result.append(tp)
                else:
                    result.append(replace_in_text(tp))

    return ''.join(result), changes

def main():
    print("=" * 70)
    print("CYCLE 3: Editorial Voice Check on Articles")
    print("=" * 70)

    totals = {
        "we_our": 0,
        "users": 0,
        "hashtags": 0,
        "markdown_bold": 0,
        "colon_headings": 0,
        "date_format": 0,
        "articles_scanned": 0,
        "articles_fixed": 0,
    }

    article_dirs = sorted([d for d in os.listdir(BASE_DIR)
                          if os.path.isdir(os.path.join(BASE_DIR, d))])

    for article_dir in article_dirs:
        index_path = os.path.join(BASE_DIR, article_dir, "index.html")
        if not os.path.isfile(index_path):
            continue

        totals["articles_scanned"] += 1

        with open(index_path, 'r', encoding='utf-8', errors='replace') as f:
            html = f.read()

        visible_text = extract_visible_text(html)
        headings = extract_headings(html)

        issues = []

        # Check we/our
        we_issues = check_we_our(visible_text)
        if we_issues:
            totals["we_our"] += len(we_issues)
            issues.append(f'{len(we_issues)} we/our issues')

        # Check users
        users_issues = check_users_word(visible_text)
        if users_issues:
            totals["users"] += len(users_issues)
            issues.append(f'{len(users_issues)} "users" instances')

        # Check hashtags
        hashtag_issues = check_hashtags(visible_text)
        if hashtag_issues:
            totals["hashtags"] += len(hashtag_issues)
            issues.append(f'{len(hashtag_issues)} hashtags')

        # Check markdown bold
        bold_issues = check_markdown_bold(html)
        if bold_issues:
            totals["markdown_bold"] += len(bold_issues)
            issues.append(f'{len(bold_issues)} markdown bold')

        # Check colon headings
        colon_issues = check_colon_headings(headings)
        if colon_issues:
            totals["colon_headings"] += len(colon_issues)
            issues.append(f'{len(colon_issues)} colon headings')

        # Check date formats
        date_issues = check_date_formats(visible_text)
        if date_issues:
            totals["date_format"] += len(date_issues)
            issues.append(f'{len(date_issues)} date format issues')

        # Apply fixes
        modified = False
        if we_issues:
            html, changes = fix_we_our_in_html(html)
            if changes > 0:
                modified = True

        if users_issues:
            html, changes = fix_users_in_html(html)
            if changes > 0:
                modified = True

        if modified:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html)
            totals["articles_fixed"] += 1

        if issues:
            print(f"  {article_dir}: {'; '.join(issues)}")

    print(f"\n--- Summary ({totals['articles_scanned']} articles scanned) ---")
    print(f"  'we/our' issues: {totals['we_our']}")
    print(f"  'users' instances: {totals['users']}")
    print(f"  Hashtags: {totals['hashtags']}")
    print(f"  Markdown bold: {totals['markdown_bold']}")
    print(f"  Colon headings: {totals['colon_headings']}")
    print(f"  Date format issues: {totals['date_format']}")
    print(f"  Articles fixed: {totals['articles_fixed']}")
    print(f"\n{'=' * 70}")
    print("Cycle 3 complete.")
    print(f"{'=' * 70}")

if __name__ == "__main__":
    main()
