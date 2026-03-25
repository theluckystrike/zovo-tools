#!/usr/bin/env python3
"""
Quick Zovo Ecosystem Validation
Fast metrics collection for immediate analysis
"""

import os
import re
import json
from pathlib import Path

def count_directories():
    """Count tool and article directories"""
    base_path = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Count tool directories
    tools = 0
    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name != 'articles':
            if (item / 'index.html').exists():
                tools += 1

    # Count article directories
    articles = 0
    articles_dir = base_path / 'articles'
    if articles_dir.exists():
        for item in articles_dir.iterdir():
            if item.is_dir() and (item / 'index.html').exists():
                articles += 1

    return tools, articles

def quick_content_scan(max_files=50):
    """Quick scan of sample files for immediate metrics"""
    base_path = Path("/Users/mike/zovo-workspaces/zovo-tools")

    violations = {
        'bold_tags': 0,
        'em_dashes': 0,
        'ai_mentions': 0
    }

    word_counts = []
    canonical_issues = []

    files_checked = 0

    # Sample tools
    for item in base_path.iterdir():
        if files_checked >= max_files:
            break

        if item.is_dir() and not item.name.startswith('.') and item.name != 'articles':
            index_file = item / 'index.html'
            if index_file.exists():
                try:
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check for violations
                    bold_count = len(re.findall(r'<b\b[^>]*>|</b>', content))
                    violations['bold_tags'] += bold_count

                    em_dash_count = len(re.findall(r'—', content))
                    violations['em_dashes'] += em_dash_count

                    ai_count = len(re.findall(r'\b(?:AI|artificial intelligence|machine learning|Claude|GPT|ChatGPT)\b',
                                            content, re.IGNORECASE))
                    violations['ai_mentions'] += ai_count

                    # Count words (rough estimate)
                    text_content = re.sub(r'<[^>]+>', '', content)
                    words = len(re.findall(r'\b\w+\b', text_content))
                    word_counts.append(words)

                    # Check canonical URL
                    canonical_match = re.search(r'<link\s+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)', content)
                    expected_canonical = f"https://tools.zovo.one/{item.name}/"

                    if not canonical_match:
                        canonical_issues.append(f"{item.name}: No canonical URL")
                    elif canonical_match.group(1) != expected_canonical:
                        canonical_issues.append(f"{item.name}: Wrong canonical URL")

                    files_checked += 1

                except Exception as e:
                    continue

    return violations, word_counts, canonical_issues, files_checked

def main():
    print("QUICK ZOVO ECOSYSTEM VALIDATION")
    print("="*50)

    # Count directories
    tools, articles = count_directories()
    total_pages = tools + articles

    print(f"Directory Counts:")
    print(f"  Tools: {tools}")
    print(f"  Articles: {articles}")
    print(f"  Total Pages: {total_pages}")

    # Quick content scan
    violations, word_counts, canonical_issues, files_checked = quick_content_scan()

    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0

    print(f"\nQuick Quality Scan ({files_checked} files sampled):")
    print(f"  Average words per page: {avg_words:,.0f}")
    print(f"  Bold tag violations: {violations['bold_tags']}")
    print(f"  Em-dash violations: {violations['em_dashes']}")
    print(f"  AI mention violations: {violations['ai_mentions']}")
    print(f"  Canonical URL issues: {len(canonical_issues)}")

    if canonical_issues[:5]:
        print(f"\nSample canonical issues:")
        for issue in canonical_issues[:5]:
            print(f"    {issue}")

    # Estimate full ecosystem
    if files_checked > 0:
        scale_factor = total_pages / files_checked
        print(f"\nEstimated Full Ecosystem Metrics:")
        print(f"  Total words: ~{sum(word_counts) * scale_factor:,.0f}")
        print(f"  Bold violations: ~{violations['bold_tags'] * scale_factor:.0f}")
        print(f"  Em-dash violations: ~{violations['em_dashes'] * scale_factor:.0f}")
        print(f"  AI violations: ~{violations['ai_mentions'] * scale_factor:.0f}")

if __name__ == "__main__":
    main()