#!/usr/bin/env python3
"""
Cycle 4: Final Comprehensive Verification
Checks all tools for:
1. Wikipedia links use proper _ separator (not spaces or %20)
2. SO links have proper search queries
3. No duplicate wiki-definition-box or so-questions-section per page
4. All external links use rel="noopener" and target="_blank"
"""

import re
import os
import urllib.parse

BASE = '/Users/mike/zovo-workspaces/zovo-tools'


def scan_all_tools():
    """Return list of all tool directories with index.html."""
    tools = []
    for d in sorted(os.listdir(BASE)):
        path = os.path.join(BASE, d, 'index.html')
        if os.path.isfile(path):
            tools.append(d)
    return tools


def check_wikipedia_separators(tools):
    """Check that Wikipedia links use _ not spaces or %20."""
    issues = []
    for d in tools:
        path = os.path.join(BASE, d, 'index.html')
        with open(path, 'r') as f:
            content = f.read()
        wiki_urls = re.findall(r'href="(https?://en\.wikipedia\.org/wiki/[^"]+)"', content)
        for url in wiki_urls:
            slug = url.split('/wiki/')[1]
            if '%20' in slug:
                issues.append((d, url, 'contains %20'))
            if ' ' in slug:
                issues.append((d, url, 'contains space'))
    return issues


def check_so_queries(tools):
    """Check SO link query quality."""
    issues = []
    strip_words = {'calculator', 'converter', 'generator', 'tool', 'checker', 'maker',
                   'online', 'free', 'best', 'simple', 'easy', 'quick'}

    for d in tools:
        path = os.path.join(BASE, d, 'index.html')
        with open(path, 'r') as f:
            content = f.read()
        so_urls = re.findall(r'href="https?://stackoverflow\.com/search\?q=([^"]+)"', content)
        for query in so_urls:
            decoded = urllib.parse.unquote_plus(query)
            words = decoded.lower().split()
            tool_terms = [w for w in words if w in strip_words]
            if tool_terms:
                issues.append((d, decoded, f'contains tool terms: {tool_terms}'))
            if len(words) > 7:
                issues.append((d, decoded, f'too long: {len(words)} words'))
    return issues


def check_duplicate_sections(tools):
    """Check for duplicate wiki-definition-box or so-questions-section."""
    issues = []
    for d in tools:
        path = os.path.join(BASE, d, 'index.html')
        with open(path, 'r') as f:
            content = f.read()

        # Count wiki-definition-box occurrences
        wiki_class = len(re.findall(r'class="wiki-definition-box"', content))
        wiki_comment = len(re.findall(r'<!-- wiki-definition-box -->', content))
        wiki_total = wiki_class + wiki_comment
        if wiki_total > 1:
            issues.append((d, f'wiki-definition-box appears {wiki_total} times'))

        # Count so-questions-section occurrences
        so_class = len(re.findall(r'class="so-questions-section"', content))
        so_comment = len(re.findall(r'<!-- so-questions-section -->', content))
        so_total = so_class + so_comment
        if so_total > 1:
            issues.append((d, f'so-questions-section appears {so_total} times'))

    return issues


def check_link_attributes(tools):
    """Check that Wikipedia and SO links have rel="noopener" and target="_blank"."""
    issues = []
    missing_noopener = 0
    missing_target = 0

    for d in tools:
        path = os.path.join(BASE, d, 'index.html')
        with open(path, 'r') as f:
            content = f.read()

        # Find all Wikipedia links
        wiki_links = re.finditer(r'<a\s[^>]*href="https?://en\.wikipedia\.org/wiki/[^"]*"[^>]*>', content)
        for match in wiki_links:
            tag = match.group(0)
            if 'rel="noopener"' not in tag and "rel='noopener'" not in tag:
                missing_noopener += 1
                if missing_noopener <= 5:
                    issues.append((d, 'Wikipedia link missing rel="noopener"', tag[:120]))
            if 'target="_blank"' not in tag and "target='_blank'" not in tag:
                missing_target += 1
                if missing_target <= 5:
                    issues.append((d, 'Wikipedia link missing target="_blank"', tag[:120]))

        # Find all SO links
        so_links = re.finditer(r'<a\s[^>]*href="https?://stackoverflow\.com/[^"]*"[^>]*>', content)
        for match in so_links:
            tag = match.group(0)
            if 'rel="noopener"' not in tag and "rel='noopener'" not in tag:
                missing_noopener += 1
                if missing_noopener <= 10:
                    issues.append((d, 'SO link missing rel="noopener"', tag[:120]))
            if 'target="_blank"' not in tag and "target='_blank'" not in tag:
                missing_target += 1
                if missing_target <= 10:
                    issues.append((d, 'SO link missing target="_blank"', tag[:120]))

    return issues, missing_noopener, missing_target


def fix_missing_attributes(tools):
    """Add missing rel="noopener" and target="_blank" to Wikipedia and SO links."""
    fixed_count = 0

    for d in tools:
        path = os.path.join(BASE, d, 'index.html')
        with open(path, 'r') as f:
            content = f.read()

        original = content

        # Fix Wikipedia links missing rel="noopener"
        def fix_wiki_link(match):
            tag = match.group(0)
            modified = tag
            if 'rel="noopener"' not in tag and "rel='noopener'" not in tag:
                # Add rel="noopener" before the closing >
                modified = modified[:-1] + ' rel="noopener">'
            if 'target="_blank"' not in tag and "target='_blank'" not in tag:
                modified = modified[:-1] + ' target="_blank">'
            return modified

        content = re.sub(
            r'<a\s[^>]*href="https?://en\.wikipedia\.org/wiki/[^"]*"[^>]*>',
            fix_wiki_link,
            content
        )

        # Fix SO links missing rel="noopener"
        def fix_so_link(match):
            tag = match.group(0)
            modified = tag
            if 'rel="noopener"' not in tag and "rel='noopener'" not in tag:
                modified = modified[:-1] + ' rel="noopener">'
            if 'target="_blank"' not in tag and "target='_blank'" not in tag:
                modified = modified[:-1] + ' target="_blank">'
            return modified

        content = re.sub(
            r'<a\s[^>]*href="https?://stackoverflow\.com/[^"]*"[^>]*>',
            fix_so_link,
            content
        )

        if content != original:
            with open(path, 'w') as f:
                f.write(content)
            fixed_count += 1

    return fixed_count


def main():
    print("=" * 70)
    print("CYCLE 4: Final Comprehensive Verification")
    print("=" * 70)
    print()

    tools = scan_all_tools()
    print(f"Scanning {len(tools)} tool pages...")
    print()

    # Check 1: Wikipedia separator format
    print("--- Check 1: Wikipedia URL Separators ---")
    sep_issues = check_wikipedia_separators(tools)
    if sep_issues:
        for tool, url, issue in sep_issues:
            print(f"  ISSUE: {tool}: {issue} in {url}")
    else:
        print("  PASS: All Wikipedia links use proper _ separator")

    # Check 2: SO query quality
    print("\n--- Check 2: StackOverflow Query Quality ---")
    so_issues = check_so_queries(tools)
    if so_issues:
        for tool, query, issue in so_issues:
            print(f"  ISSUE: {tool}: {issue} - \"{query}\"")
    else:
        print("  PASS: All SO queries are clean and concept-focused")

    # Check 3: Duplicate sections
    print("\n--- Check 3: Duplicate Sections ---")
    dup_issues = check_duplicate_sections(tools)
    if dup_issues:
        for tool, issue in dup_issues:
            print(f"  ISSUE: {tool}: {issue}")
    else:
        print("  PASS: No duplicate wiki-definition-box or so-questions-section")

    # Check 4: Link attributes (rel="noopener", target="_blank")
    print("\n--- Check 4: Link Attributes ---")
    attr_issues, missing_noopener, missing_target = check_link_attributes(tools)
    if attr_issues:
        for tool, issue, tag in attr_issues:
            print(f"  ISSUE: {tool}: {issue}")
        if missing_noopener > 0 or missing_target > 0:
            print(f"\n  Total missing rel='noopener': {missing_noopener}")
            print(f"  Total missing target='_blank': {missing_target}")
            print("\n  Applying fixes...")
            fixed = fix_missing_attributes(tools)
            print(f"  Fixed {fixed} files")
    else:
        print("  PASS: All Wikipedia and SO links have proper attributes")

    # Post-fix verification
    print("\n--- Post-Fix Verification ---")
    sep_issues_post = check_wikipedia_separators(tools)
    so_issues_post = check_so_queries(tools)
    dup_issues_post = check_duplicate_sections(tools)
    attr_issues_post, mn_post, mt_post = check_link_attributes(tools)

    print(f"  Wikipedia separator issues: {len(sep_issues)} -> {len(sep_issues_post)}")
    print(f"  SO query issues: {len(so_issues)} -> {len(so_issues_post)}")
    print(f"  Duplicate section issues: {len(dup_issues)} -> {len(dup_issues_post)}")
    print(f"  Missing noopener: {missing_noopener} -> {mn_post}")
    print(f"  Missing target: {missing_target} -> {mt_post}")

    total_issues = len(sep_issues_post) + len(so_issues_post) + len(dup_issues_post) + mn_post + mt_post
    print(f"\n{'=' * 70}")
    if total_issues == 0:
        print("CYCLE 4 COMPLETE: ALL CHECKS PASS - Zero issues remaining")
    else:
        print(f"CYCLE 4 COMPLETE: {total_issues} issues remaining")
    print(f"{'=' * 70}")


if __name__ == '__main__':
    main()
