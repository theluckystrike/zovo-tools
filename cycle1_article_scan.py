#!/usr/bin/env python3
"""
Cycle 1: Anti-AI formatting scan and fix on ALL article pages.
Scans for: <strong>/<b> tags, em-dashes, AI buzzwords.
Fixes all instances in-place.
"""

import os
import re
import json
from collections import defaultdict

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools/articles"

# AI buzzwords and their replacements (case-insensitive matching)
AI_WORD_REPLACEMENTS = {
    "comprehensive": "complete",
    "delve": "explore",
    "delves": "explores",
    "delving": "exploring",
    "leverage": "use",
    "leverages": "uses",
    "leveraging": "using",
    "leveraged": "used",
    "landscape": "field",
    "landscapes": "fields",
    "utilize": "use",
    "utilizes": "uses",
    "utilizing": "using",
    "utilized": "used",
    "utilization": "use",
    "streamline": "simplify",
    "streamlines": "simplifies",
    "streamlining": "simplifying",
    "streamlined": "simplified",
    "robust": "strong",
    "cutting-edge": "modern",
    "cutting edge": "modern",
    "game-changer": "major improvement",
    "game changer": "major improvement",
    "game-changing": "significant",
    "synergy": "combination",
    "synergies": "combinations",
    "paradigm": "model",
    "paradigms": "models",
    "paradigm shift": "major change",
    "holistic": "complete",
    "empower": "enable",
    "empowers": "enables",
    "empowering": "enabling",
    "empowered": "enabled",
    "unlock": "access",
    "unlocks": "opens",
    "unlocking": "opening",
    "harness": "use",
    "harnessing": "using",
    "harnessed": "used",
    "elevate": "improve",
    "elevates": "improves",
    "elevating": "improving",
    "elevated": "improved",
    "pivotal": "key",
    "transformative": "significant",
    "innovative": "new",
    "revolutionary": "major",
    "revolutionize": "change",
    "revolutionizes": "changes",
    "revolutionizing": "changing",
}

def fix_strong_b_tags(html):
    """Remove <strong> and <b> tags, keeping inner text."""
    count = 0
    # Count occurrences
    count += len(re.findall(r'<strong\b[^>]*>', html, re.IGNORECASE))
    count += len(re.findall(r'<b\b[^>]*>(?!</)', html, re.IGNORECASE))
    # But don't count <br>, <body>, <button>, <blockquote>, <base>, etc.
    # More precise: only match <b> and <b ...> not followed by other letters

    # Remove <strong>...</strong>
    html = re.sub(r'<strong\b[^>]*>(.*?)</strong>', r'\1', html, flags=re.IGNORECASE | re.DOTALL)
    # Remove <b>...</b> but NOT <br>, <body>, <button>, <blockquote>, etc.
    html = re.sub(r'<b\b(?:\s[^>]*)?>(?!</)(.*?)</b>', r'\1', html, flags=re.IGNORECASE | re.DOTALL)

    return html, count

def fix_em_dashes(html):
    """Replace em-dashes and en-dashes with appropriate punctuation."""
    count = 0

    # Count em-dashes (—) and en-dashes (–)
    count += html.count('—')
    count += html.count('–')
    count += html.count('&mdash;')
    count += html.count('&ndash;')

    # Replace em-dashes: " — " with ", " or ". " or " and "
    # Context-dependent: use comma for most cases
    html = html.replace(' — ', ', ')
    html = html.replace(' – ', ', ')
    html = html.replace('— ', ', ')
    html = html.replace('– ', ', ')
    html = html.replace(' —', ', ')
    html = html.replace(' –', ', ')
    # Remaining standalone dashes
    html = html.replace('—', ', ')
    html = html.replace('–', ', ')
    html = html.replace('&mdash;', ', ')
    html = html.replace('&ndash;', ', ')

    return html, count

def fix_ai_words(html):
    """Replace AI buzzwords with natural alternatives."""
    total_count = 0
    details = {}

    for ai_word, replacement in AI_WORD_REPLACEMENTS.items():
        # Word boundary matching, case-insensitive
        pattern = re.compile(r'\b' + re.escape(ai_word) + r'\b', re.IGNORECASE)

        # Don't replace inside HTML tags, scripts, or attribute values
        # We'll use a smarter approach: only replace in text content
        matches = pattern.findall(html)
        if matches:
            count = len(matches)
            total_count += count
            details[ai_word] = count

            # Replace preserving case
            def replace_preserving_case(match):
                original = match.group(0)
                if original[0].isupper():
                    return replacement[0].upper() + replacement[1:]
                return replacement

            # Only replace in text content (not inside tags or attributes)
            # Split by tags and only process text parts
            def replace_in_text_only(html_str, pat, replacer):
                # Split by script/style sections first (preserve them)
                parts = re.split(r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)', html_str, flags=re.IGNORECASE)
                result = []
                for i, part in enumerate(parts):
                    if i % 2 == 1:  # Script/style block, skip
                        result.append(part)
                    else:
                        # Now split by HTML tags
                        tag_parts = re.split(r'(<[^>]+>)', part)
                        for j, tp in enumerate(tag_parts):
                            if j % 2 == 1:  # Inside a tag, skip
                                result.append(tp)
                            else:
                                result.append(pat.sub(replacer, tp))
                return ''.join(result)

            html = replace_in_text_only(html, pattern, replace_preserving_case)

    return html, total_count, details

def scan_and_fix_articles():
    """Scan all article index.html files and fix issues."""
    results = {
        "total_articles": 0,
        "total_strong_b_tags": 0,
        "total_em_dashes": 0,
        "total_ai_words": 0,
        "ai_word_details": defaultdict(int),
        "per_article": {},
        "articles_modified": 0,
    }

    if not os.path.isdir(BASE_DIR):
        print(f"ERROR: {BASE_DIR} not found")
        return results

    article_dirs = sorted([d for d in os.listdir(BASE_DIR)
                          if os.path.isdir(os.path.join(BASE_DIR, d))])

    for article_dir in article_dirs:
        index_path = os.path.join(BASE_DIR, article_dir, "index.html")
        if not os.path.isfile(index_path):
            continue

        results["total_articles"] += 1

        with open(index_path, 'r', encoding='utf-8') as f:
            original_html = f.read()

        html = original_html
        article_stats = {}

        # Fix strong/b tags
        html, strong_count = fix_strong_b_tags(html)
        article_stats["strong_b_tags"] = strong_count
        results["total_strong_b_tags"] += strong_count

        # Fix em-dashes
        html, dash_count = fix_em_dashes(html)
        article_stats["em_dashes"] = dash_count
        results["total_em_dashes"] += dash_count

        # Fix AI words
        html, ai_count, ai_details = fix_ai_words(html)
        article_stats["ai_words"] = ai_count
        article_stats["ai_word_details"] = ai_details
        results["total_ai_words"] += ai_count
        for word, count in ai_details.items():
            results["ai_word_details"][word] += count

        if html != original_html:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(html)
            results["articles_modified"] += 1
            article_stats["modified"] = True
        else:
            article_stats["modified"] = False

        if strong_count > 0 or dash_count > 0 or ai_count > 0:
            results["per_article"][article_dir] = article_stats

    return results

if __name__ == "__main__":
    print("=" * 70)
    print("CYCLE 1: Anti-AI Scan on Articles")
    print("=" * 70)

    results = scan_and_fix_articles()

    print(f"\nArticles scanned: {results['total_articles']}")
    print(f"Articles modified: {results['articles_modified']}")
    print(f"\n--- Violations Found & Fixed ---")
    print(f"<strong>/<b> tags removed: {results['total_strong_b_tags']}")
    print(f"Em-dashes/en-dashes replaced: {results['total_em_dashes']}")
    print(f"AI buzzwords replaced: {results['total_ai_words']}")

    if results['ai_word_details']:
        print(f"\n--- AI Word Breakdown ---")
        for word, count in sorted(results['ai_word_details'].items(), key=lambda x: -x[1]):
            print(f"  {word}: {count}")

    if results['per_article']:
        print(f"\n--- Per-Article Details ---")
        for article, stats in sorted(results['per_article'].items()):
            issues = []
            if stats.get('strong_b_tags', 0) > 0:
                issues.append(f"{stats['strong_b_tags']} strong/b")
            if stats.get('em_dashes', 0) > 0:
                issues.append(f"{stats['em_dashes']} dashes")
            if stats.get('ai_words', 0) > 0:
                issues.append(f"{stats['ai_words']} AI words")
            print(f"  {article}: {', '.join(issues)}")

    print(f"\n{'=' * 70}")
    print("Cycle 1 complete.")
    print(f"{'=' * 70}")
