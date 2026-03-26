#!/usr/bin/env python3
"""
Cycle 2: Anti-AI formatting scan and fix on ALL tool pages.
Scans for: <strong>/<b> tags in text content, em-dashes, AI buzzwords.
Only modifies text content - does NOT break JavaScript or tool functionality.
"""

import os
import re
from collections import defaultdict

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"
EXCLUDE_DIRS = {
    "articles", "categories", "cleanup", "recovery_documentation",
    ".git", "node_modules", "__pycache__", ".claude"
}

# AI buzzwords and their replacements
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

def get_tool_dirs():
    """Get all tool directories (not articles, not categories, not scripts)."""
    tool_dirs = []
    for item in os.listdir(BASE_DIR):
        full_path = os.path.join(BASE_DIR, item)
        if not os.path.isdir(full_path):
            continue
        if item in EXCLUDE_DIRS:
            continue
        if item.startswith('.') or item.startswith('_'):
            continue
        index_path = os.path.join(full_path, "index.html")
        if os.path.isfile(index_path):
            tool_dirs.append(item)
    return sorted(tool_dirs)

def safe_replace_in_text_content(html, ai_word, replacement):
    """
    Replace AI word only in visible text content, NOT in:
    - <script>...</script> blocks
    - <style>...</style> blocks
    - HTML tag attributes
    - JavaScript code
    - CSS code
    - URL paths
    """
    pattern = re.compile(r'\b' + re.escape(ai_word) + r'\b', re.IGNORECASE)

    count = 0

    def replace_preserving_case(match):
        nonlocal count
        count += 1
        original = match.group(0)
        if original[0].isupper():
            return replacement[0].upper() + replacement[1:]
        return replacement

    # Split by script and style blocks first (preserve them completely)
    protected_pattern = re.compile(
        r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)',
        re.IGNORECASE
    )
    parts = protected_pattern.split(html)

    result = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # Script or style block - skip entirely
            result.append(part)
        else:
            # Now split by HTML tags to only process text nodes
            tag_parts = re.split(r'(<[^>]+>)', part)
            for j, tp in enumerate(tag_parts):
                if j % 2 == 1:  # Inside a tag - skip
                    result.append(tp)
                else:  # Text content - safe to replace
                    result.append(pattern.sub(replace_preserving_case, tp))

    return ''.join(result), count

def fix_strong_b_in_text(html):
    """
    Remove <strong> and <b> tags in educational/text content only.
    Preserve them inside <script> and <style> blocks.
    """
    count = 0

    # Split by script and style blocks
    protected_pattern = re.compile(
        r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)',
        re.IGNORECASE
    )
    parts = protected_pattern.split(html)

    result = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # Script or style block - skip
            result.append(part)
        else:
            # Count strong/b tags
            count += len(re.findall(r'<strong\b[^>]*>', part, re.IGNORECASE))
            count += len(re.findall(r'<b\s[^>]*>|<b>', part, re.IGNORECASE))

            # Remove strong tags
            part = re.sub(r'<strong\b[^>]*>(.*?)</strong>', r'\1', part, flags=re.IGNORECASE | re.DOTALL)
            # Remove b tags (not br, body, button, blockquote, base, etc.)
            part = re.sub(r'<b(?:\s[^>]*)?>(?!</)(.*?)</b>', r'\1', part, flags=re.IGNORECASE | re.DOTALL)
            result.append(part)

    return ''.join(result), count

def fix_em_dashes_in_text(html):
    """Replace em-dashes and en-dashes in text content only."""
    count = 0

    protected_pattern = re.compile(
        r'(<script[\s\S]*?</script>|<style[\s\S]*?</style>)',
        re.IGNORECASE
    )
    parts = protected_pattern.split(html)

    result = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # Script or style block - skip
            result.append(part)
        else:
            count += part.count('—')
            count += part.count('–')
            count += part.count('&mdash;')
            count += part.count('&ndash;')

            part = part.replace(' — ', ', ')
            part = part.replace(' – ', ', ')
            part = part.replace('— ', ', ')
            part = part.replace('– ', ', ')
            part = part.replace(' —', ', ')
            part = part.replace(' –', ', ')
            part = part.replace('—', ', ')
            part = part.replace('–', ', ')
            part = part.replace('&mdash;', ', ')
            part = part.replace('&ndash;', ', ')
            result.append(part)

    return ''.join(result), count

def scan_and_fix_tools():
    """Scan all tool index.html files and fix issues."""
    results = {
        "total_tools": 0,
        "total_strong_b_tags": 0,
        "total_em_dashes": 0,
        "total_ai_words": 0,
        "ai_word_details": defaultdict(int),
        "tools_modified": 0,
        "tools_with_issues": [],
    }

    tool_dirs = get_tool_dirs()
    print(f"Found {len(tool_dirs)} tool directories to scan...")

    for idx, tool_dir in enumerate(tool_dirs):
        if (idx + 1) % 100 == 0:
            print(f"  Scanning {idx + 1}/{len(tool_dirs)}...")

        index_path = os.path.join(BASE_DIR, tool_dir, "index.html")
        if not os.path.isfile(index_path):
            continue

        results["total_tools"] += 1

        try:
            with open(index_path, 'r', encoding='utf-8', errors='replace') as f:
                original_html = f.read()
        except Exception as e:
            print(f"  ERROR reading {tool_dir}: {e}")
            continue

        html = original_html
        tool_stats = {"dir": tool_dir}

        # Fix strong/b tags in text content
        html, strong_count = fix_strong_b_in_text(html)
        tool_stats["strong_b_tags"] = strong_count
        results["total_strong_b_tags"] += strong_count

        # Fix em-dashes in text content
        html, dash_count = fix_em_dashes_in_text(html)
        tool_stats["em_dashes"] = dash_count
        results["total_em_dashes"] += dash_count

        # Fix AI words in text content
        ai_count = 0
        ai_details = {}
        for ai_word, replacement in AI_WORD_REPLACEMENTS.items():
            html, word_count = safe_replace_in_text_content(html, ai_word, replacement)
            if word_count > 0:
                ai_count += word_count
                ai_details[ai_word] = word_count
                results["ai_word_details"][ai_word] += word_count

        tool_stats["ai_words"] = ai_count
        tool_stats["ai_word_details"] = ai_details
        results["total_ai_words"] += ai_count

        if html != original_html:
            try:
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                results["tools_modified"] += 1
                tool_stats["modified"] = True
            except Exception as e:
                print(f"  ERROR writing {tool_dir}: {e}")
                continue
        else:
            tool_stats["modified"] = False

        if strong_count > 0 or dash_count > 0 or ai_count > 0:
            results["tools_with_issues"].append(tool_stats)

    return results

if __name__ == "__main__":
    print("=" * 70)
    print("CYCLE 2: Anti-AI Scan on Tool Pages")
    print("=" * 70)

    results = scan_and_fix_tools()

    print(f"\nTools scanned: {results['total_tools']}")
    print(f"Tools modified: {results['tools_modified']}")
    print(f"\n--- Violations Found & Fixed ---")
    print(f"<strong>/<b> tags removed: {results['total_strong_b_tags']}")
    print(f"Em-dashes/en-dashes replaced: {results['total_em_dashes']}")
    print(f"AI buzzwords replaced: {results['total_ai_words']}")

    if results['ai_word_details']:
        print(f"\n--- AI Word Breakdown ---")
        for word, count in sorted(results['ai_word_details'].items(), key=lambda x: -x[1]):
            print(f"  {word}: {count}")

    if results['tools_with_issues']:
        print(f"\n--- Tools With Issues (showing first 50) ---")
        for stats in results['tools_with_issues'][:50]:
            issues = []
            if stats.get('strong_b_tags', 0) > 0:
                issues.append(f"{stats['strong_b_tags']} strong/b")
            if stats.get('em_dashes', 0) > 0:
                issues.append(f"{stats['em_dashes']} dashes")
            if stats.get('ai_words', 0) > 0:
                ai_words_str = ', '.join(f"{k}={v}" for k, v in stats['ai_word_details'].items())
                issues.append(f"{stats['ai_words']} AI words ({ai_words_str})")
            print(f"  {stats['dir']}: {'; '.join(issues)}")

        if len(results['tools_with_issues']) > 50:
            print(f"  ... and {len(results['tools_with_issues']) - 50} more tools with issues")

    print(f"\nTotal tools with any issues: {len(results['tools_with_issues'])}")
    print(f"\n{'=' * 70}")
    print("Cycle 2 complete.")
    print(f"{'=' * 70}")
