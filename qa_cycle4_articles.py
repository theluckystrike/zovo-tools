#!/usr/bin/env python3
"""
Cycle 4: Content quality check on articles.
Checks:
1. No <strong> or <b> tags (anti-AI rule)
2. No em-dashes
3. No AI words: comprehensive, delve, leverage, landscape, utilize, streamline, robust
4. No emojis
5. No Claude/Anthropic/AI-generated mentions
6. All word counts > 1000
"""

import os
import re
import sys
import unicodedata

BASE_DIR = '/Users/mike/zovo-workspaces/zovo-tools'
ARTICLES_DIR = os.path.join(BASE_DIR, 'articles')

AI_WORDS = [
    'comprehensive', 'delve', 'leverage', 'landscape',
    'utilize', 'streamline', 'robust'
]

AI_MENTIONS = [
    'Claude', 'Anthropic', 'AI-generated', 'AI generated',
    'GPT', 'ChatGPT', 'language model'
]

# Emoji regex: matches most emoji ranges
EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F1E0-\U0001F1FF"  # flags
    "\U00002702-\U000027B0"
    "\U000024C2-\U0001F251"
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U0001FA00-\U0001FA6F"  # chess symbols
    "\U0001FA70-\U0001FAFF"  # symbols extended
    "\U00002600-\U000026FF"  # misc symbols
    "\U0000FE00-\U0000FE0F"  # variation selectors
    "\U0000200D"  # zero width joiner
    "\U00002B50"  # star
    "\U0000231A-\U0000231B"  # watch/hourglass
    "\U000023E9-\U000023F3"  # media controls
    "\U000023F8-\U000023FA"
    "]+",
    flags=re.UNICODE
)


def find_article_files():
    """Find all article index.html files."""
    files = []
    if not os.path.isdir(ARTICLES_DIR):
        return files
    for entry in sorted(os.listdir(ARTICLES_DIR)):
        idx = os.path.join(ARTICLES_DIR, entry, 'index.html')
        if os.path.isfile(idx):
            files.append(idx)
    return files


def extract_body_text(content):
    """Extract text content from HTML body, excluding script/style tags."""
    # Remove script and style blocks
    text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    # Remove all HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Decode HTML entities
    text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    text = text.replace('&mdash;', '--').replace('&ndash;', '-')
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def count_words(text):
    """Count words in text."""
    words = text.split()
    return len(words)


def find_strong_b_tags(content):
    """Find <strong> and <b> tags in the body content (not in nav/footer)."""
    # Extract body content
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    if not body_match:
        return []

    body = body_match.group(1)

    # Remove script tags from body
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL)

    findings = []
    for tag in ['strong', 'b']:
        pattern = rf'<{tag}[^>]*>(.*?)</{tag}>'
        for m in re.finditer(pattern, body, re.DOTALL):
            text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            if text:
                findings.append({
                    'tag': tag,
                    'text': text[:80],
                    'position': m.start()
                })

    return findings


def find_em_dashes(content):
    """Find em-dashes in text content."""
    body_text = extract_body_text(content)
    positions = []

    # Check for actual em-dash character
    for m in re.finditer('\u2014', body_text):
        ctx_start = max(0, m.start() - 30)
        ctx_end = min(len(body_text), m.end() + 30)
        positions.append(body_text[ctx_start:ctx_end])

    # Also check HTML entity
    for m in re.finditer(r'&mdash;', content):
        ctx_start = max(0, m.start() - 30)
        ctx_end = min(len(content), m.end() + 30)
        ctx = re.sub(r'<[^>]+>', '', content[ctx_start:ctx_end])
        positions.append(ctx.strip()[:60])

    return positions


def find_ai_words(content):
    """Find AI-typical words in text content."""
    body_text = extract_body_text(content).lower()
    findings = []

    for word in AI_WORDS:
        count = len(re.findall(r'\b' + word + r'\b', body_text))
        if count > 0:
            findings.append((word, count))

    return findings


def find_emojis(content):
    """Find emojis in text content."""
    body_text = extract_body_text(content)
    emojis = EMOJI_PATTERN.findall(body_text)
    return emojis


def find_ai_mentions(content):
    """Find mentions of Claude, Anthropic, AI-generated."""
    body_text = extract_body_text(content)
    findings = []

    for mention in AI_MENTIONS:
        if mention.lower() in body_text.lower():
            findings.append(mention)

    return findings


def fix_strong_b_tags(content):
    """Replace <strong> and <b> with plain text or <span>."""
    fixes = 0

    for tag in ['strong', 'b']:
        pattern = rf'<{tag}[^>]*>(.*?)</{tag}>'
        count = len(re.findall(pattern, content, re.DOTALL))
        if count > 0:
            # Replace with the inner content (remove bold wrapping)
            content = re.sub(pattern, r'\1', content, flags=re.DOTALL)
            fixes += count

    return content, fixes


def fix_em_dashes(content):
    """Replace em-dashes with double hyphens or commas."""
    fixes = 0

    # Replace em-dash character
    if '\u2014' in content:
        count = content.count('\u2014')
        content = content.replace('\u2014', ' -- ')
        fixes += count

    # Replace HTML entity
    if '&mdash;' in content:
        count = content.count('&mdash;')
        content = content.replace('&mdash;', ' -- ')
        fixes += count

    return content, fixes


def fix_ai_words(content):
    """Replace AI-typical words with better alternatives."""
    replacements = {
        'comprehensive': 'complete',
        'delve': 'explore',
        'leverage': 'use',
        'landscape': 'space',
        'utilize': 'use',
        'streamline': 'simplify',
        'robust': 'solid',
    }

    fixes = 0
    for word, replacement in replacements.items():
        # Case-insensitive replacement preserving case
        def replace_preserve_case(match):
            nonlocal fixes
            fixes += 1
            original = match.group(0)
            if original[0].isupper():
                return replacement.capitalize()
            return replacement

        content = re.sub(r'\b' + word + r'\b', replace_preserve_case, content, flags=re.IGNORECASE)

    return content, fixes


def fix_emojis(content):
    """Remove emojis from content."""
    new_content = EMOJI_PATTERN.sub('', content)
    fixes = len(content) - len(new_content)
    return new_content, fixes > 0


def fix_ai_mentions(content):
    """Remove or replace AI-related mentions."""
    fixes = 0
    for mention in AI_MENTIONS:
        if mention.lower() in content.lower():
            # This requires careful handling - report rather than auto-fix
            fixes += 1
    return content, fixes  # Don't auto-fix, just report


def process_article(filepath):
    """Run all quality checks on an article."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        return {'file': filepath, 'error': str(e)}

    original = content
    rel_path = os.path.relpath(filepath, BASE_DIR)
    issues = []
    fixes = {}

    # Word count
    body_text = extract_body_text(content)
    word_count = count_words(body_text)
    if word_count < 1000:
        issues.append(f"Word count too low: {word_count}")

    # Check 1: <strong> and <b> tags
    strong_tags = find_strong_b_tags(content)
    if strong_tags:
        issues.append(f"{len(strong_tags)} <strong>/<b> tag(s)")
        content, n = fix_strong_b_tags(content)
        if n: fixes['strong_b_removed'] = n

    # Check 2: Em-dashes
    em_dashes = find_em_dashes(content)
    if em_dashes:
        issues.append(f"{len(em_dashes)} em-dash(es)")
        content, n = fix_em_dashes(content)
        if n: fixes['em_dashes_fixed'] = n

    # Check 3: AI words
    ai_words = find_ai_words(content)
    if ai_words:
        word_list = ', '.join(f'{w} x{c}' for w, c in ai_words)
        issues.append(f"AI words: {word_list}")
        content, n = fix_ai_words(content)
        if n: fixes['ai_words_replaced'] = n

    # Check 4: Emojis
    emojis = find_emojis(content)
    if emojis:
        issues.append(f"Emojis found: {''.join(emojis[:10])}")
        content, fixed = fix_emojis(content)
        if fixed: fixes['emojis_removed'] = len(emojis)

    # Check 5: AI mentions
    ai_mentions = find_ai_mentions(content)
    if ai_mentions:
        issues.append(f"AI mentions: {', '.join(ai_mentions)}")

    # Write if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return {
        'file': rel_path,
        'word_count': word_count,
        'issues': issues,
        'fixes': fixes,
        'changed': content != original
    }


def main():
    print("=" * 70)
    print("CYCLE 4: Article Content Quality Check")
    print("=" * 70)

    files = find_article_files()
    print(f"\nScanning {len(files)} articles...\n")

    total_issues = 0
    files_with_issues = 0
    files_fixed = 0
    issue_types = {}
    low_word_count = []

    for filepath in files:
        result = process_article(filepath)

        if result.get('error'):
            print(f"  ERROR: {result['file']}: {result['error']}")
            continue

        if result['issues']:
            files_with_issues += 1
            total_issues += len(result['issues'])

            if result.get('changed'):
                files_fixed += 1

            rel_path = result['file']
            print(f"\n  {'FIXED' if result.get('changed') else 'ISSUE'}: {rel_path} ({result['word_count']} words)")
            for issue in result['issues']:
                print(f"    - {issue}")
            if result['fixes']:
                print(f"    Fixes: {result['fixes']}")

            if result['word_count'] < 1000:
                low_word_count.append((rel_path, result['word_count']))

    print("\n" + "=" * 70)
    print("CYCLE 4 SUMMARY")
    print("=" * 70)
    print(f"Articles scanned:     {len(files)}")
    print(f"Articles with issues: {files_with_issues}")
    print(f"Articles fixed:       {files_fixed}")
    print(f"Total issues found:   {total_issues}")

    if low_word_count:
        print(f"\nArticles under 1000 words ({len(low_word_count)}):")
        for path, wc in sorted(low_word_count, key=lambda x: x[1]):
            print(f"  {path}: {wc} words")

    # Also scan tool pages for the same issues (just report, no fix)
    print("\n" + "=" * 70)
    print("BONUS: Quick scan of tool pages for AI mentions")
    print("=" * 70)

    tool_ai_mentions = 0
    for entry in sorted(os.listdir(BASE_DIR)):
        if entry == 'articles':
            continue
        idx = os.path.join(BASE_DIR, entry, 'index.html')
        if os.path.isfile(idx):
            with open(idx, 'r', errors='ignore') as f:
                content = f.read()
            body_text = extract_body_text(content).lower()
            for mention in ['claude', 'anthropic', 'ai-generated', 'ai generated', 'chatgpt']:
                if mention.lower() in body_text:
                    if mention.lower() == 'claude' and 'claude shannon' in body_text:
                        continue  # Claude Shannon is a real person
                    tool_ai_mentions += 1
                    print(f"  WARNING: {entry} mentions '{mention}'")
                    break

    print(f"\nTool pages with AI mentions: {tool_ai_mentions}")


if __name__ == '__main__':
    main()
