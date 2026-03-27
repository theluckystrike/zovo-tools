#!/usr/bin/env python3
"""
Verification: Count remaining AI formatting issues in VISIBLE TEXT ONLY.
Ignores script blocks, style blocks, HTML attributes, URL-encoded strings.
"""

import os
import re
from collections import defaultdict

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

AI_WORDS = [
    "comprehensive", "delve", "delves", "delving",
    "leverage", "leverages", "leveraging", "leveraged",
    "landscape", "landscapes",
    "utilize", "utilizes", "utilizing", "utilized", "utilization",
    "streamline", "streamlines", "streamlining", "streamlined",
    "robust",
    "cutting-edge", "cutting edge",
    "game-changer", "game changer", "game-changing",
    "synergy", "synergies",
    "paradigm", "paradigms", "paradigm shift",
    "holistic",
    "empower", "empowers", "empowering", "empowered",
    "unlock", "unlocks", "unlocking",
    "harness", "harnessing", "harnessed",
    "elevate", "elevates", "elevating", "elevated",
    "pivotal",
    "transformative",
    "innovative",
    "revolutionary", "revolutionize", "revolutionizes", "revolutionizing",
]

def extract_visible_text(html):
    """Extract only visible text from HTML, removing scripts, styles, and tags."""
    # Remove script blocks
    text = re.sub(r'<script[\s\S]*?</script>', ' ', html, flags=re.IGNORECASE)
    # Remove style blocks
    text = re.sub(r'<style[\s\S]*?</style>', ' ', text, flags=re.IGNORECASE)
    # Remove HTML comments
    text = re.sub(r'<!--[\s\S]*?-->', ' ', text)
    # Remove all HTML tags (but keep their text content)
    text = re.sub(r'<[^>]+>', ' ', text)
    # Decode common entities
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', "'")
    return text

def scan_visible_text(html):
    """Scan visible text for AI words, strong/b tags, em-dashes."""
    text = extract_visible_text(html)

    results = {
        "ai_words": defaultdict(int),
        "ai_total": 0,
        "em_dashes": text.count('\u2014') + text.count('\u2013'),  # — and –
        "strong_b_in_html": 0,
    }

    # Check for strong/b tags in the non-script/style HTML
    html_no_script = re.sub(r'<script[\s\S]*?</script>', '', html, flags=re.IGNORECASE)
    html_no_script = re.sub(r'<style[\s\S]*?</style>', '', html_no_script, flags=re.IGNORECASE)
    results["strong_b_in_html"] = len(re.findall(r'<strong\b[^>]*>', html_no_script, re.IGNORECASE))
    results["strong_b_in_html"] += len(re.findall(r'<b\s[^>]*>|<b>', html_no_script, re.IGNORECASE))

    for word in AI_WORDS:
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        matches = pattern.findall(text)
        if matches:
            results["ai_words"][word] += len(matches)
            results["ai_total"] += len(matches)

    return results

def main():
    # Scan articles
    print("=" * 70)
    print("VERIFICATION: Visible Text Only")
    print("=" * 70)

    article_dir = os.path.join(BASE_DIR, "articles")
    article_totals = {"ai": 0, "dashes": 0, "strong": 0, "ai_details": defaultdict(int)}
    article_count = 0

    for d in sorted(os.listdir(article_dir)):
        index_path = os.path.join(article_dir, d, "index.html")
        if not os.path.isfile(index_path):
            continue
        article_count += 1
        with open(index_path, 'r', encoding='utf-8', errors='replace') as f:
            html = f.read()
        r = scan_visible_text(html)
        article_totals["ai"] += r["ai_total"]
        article_totals["dashes"] += r["em_dashes"]
        article_totals["strong"] += r["strong_b_in_html"]
        for w, c in r["ai_words"].items():
            article_totals["ai_details"][w] += c
        if r["ai_total"] > 0 or r["em_dashes"] > 0 or r["strong_b_in_html"] > 0:
            issues = []
            if r["strong_b_in_html"] > 0: issues.append(f"{r['strong_b_in_html']} strong/b")
            if r["em_dashes"] > 0: issues.append(f"{r['em_dashes']} dashes")
            if r["ai_total"] > 0: issues.append(f"{r['ai_total']} AI words: {dict(r['ai_words'])}")
            print(f"  ARTICLE {d}: {'; '.join(issues)}")

    print(f"\n--- Article Summary ({article_count} articles) ---")
    print(f"  Strong/B tags in visible HTML: {article_totals['strong']}")
    print(f"  Em-dashes in visible text: {article_totals['dashes']}")
    print(f"  AI words in visible text: {article_totals['ai']}")
    if article_totals["ai_details"]:
        for w, c in sorted(article_totals["ai_details"].items(), key=lambda x: -x[1]):
            print(f"    {w}: {c}")

    # Scan tools
    tool_totals = {"ai": 0, "dashes": 0, "strong": 0, "ai_details": defaultdict(int)}
    tool_count = 0
    exclude = {"articles", "categories", "cleanup", "recovery_documentation", ".git", "node_modules", "__pycache__", ".claude"}

    tool_dirs = sorted([d for d in os.listdir(BASE_DIR)
                       if os.path.isdir(os.path.join(BASE_DIR, d))
                       and d not in exclude
                       and not d.startswith('.')
                       and not d.startswith('_')
                       and os.path.isfile(os.path.join(BASE_DIR, d, "index.html"))])

    for idx, d in enumerate(tool_dirs):
        if (idx + 1) % 200 == 0:
            print(f"  Scanning tool {idx + 1}/{len(tool_dirs)}...")
        index_path = os.path.join(BASE_DIR, d, "index.html")
        tool_count += 1
        with open(index_path, 'r', encoding='utf-8', errors='replace') as f:
            html = f.read()
        r = scan_visible_text(html)
        tool_totals["ai"] += r["ai_total"]
        tool_totals["dashes"] += r["em_dashes"]
        tool_totals["strong"] += r["strong_b_in_html"]
        for w, c in r["ai_words"].items():
            tool_totals["ai_details"][w] += c
        if r["ai_total"] > 0 or r["em_dashes"] > 0 or r["strong_b_in_html"] > 0:
            issues = []
            if r["strong_b_in_html"] > 0: issues.append(f"{r['strong_b_in_html']} strong/b")
            if r["em_dashes"] > 0: issues.append(f"{r['em_dashes']} dashes")
            if r["ai_total"] > 0: issues.append(f"{r['ai_total']} AI words: {dict(r['ai_words'])}")
            print(f"  TOOL {d}: {'; '.join(issues)}")

    print(f"\n--- Tool Summary ({tool_count} tools) ---")
    print(f"  Strong/B tags in visible HTML: {tool_totals['strong']}")
    print(f"  Em-dashes in visible text: {tool_totals['dashes']}")
    print(f"  AI words in visible text: {tool_totals['ai']}")
    if tool_totals["ai_details"]:
        for w, c in sorted(tool_totals["ai_details"].items(), key=lambda x: -x[1]):
            print(f"    {w}: {c}")

    print(f"\n{'=' * 70}")
    print("GRAND TOTAL")
    print(f"  Strong/B tags: {article_totals['strong'] + tool_totals['strong']}")
    print(f"  Em-dashes: {article_totals['dashes'] + tool_totals['dashes']}")
    print(f"  AI words: {article_totals['ai'] + tool_totals['ai']}")
    print(f"{'=' * 70}")

if __name__ == "__main__":
    main()
