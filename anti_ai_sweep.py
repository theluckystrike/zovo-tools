#!/usr/bin/env python3
"""
Deep Anti-AI Editorial Sweep - ZERO AI Signals
Scans all HTML files in zovo-tools for AI-generated language patterns and fixes them.
Author: Michael Lip
"""

import os
import re
import json
import sys
from collections import defaultdict

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

# ============================================================
# CYCLE 1: AI Word Replacements
# ============================================================

# Tier 1 - MUST FIX (case-insensitive replacements)
# Each entry: (pattern_regex, replacement_function_or_string)
# We use word-boundary matching to avoid partial word matches

TIER1_REPLACEMENTS = [
    # "comprehensive" -> "complete" or "full" or "thorough"
    (r'\bcomprehensive\b', 'complete'),
    (r'\bComprehensive\b', 'Complete'),

    # "delve" / "delving" -> "explore" / "examining"
    (r'\bdelving\b', 'examining'),
    (r'\bDelving\b', 'Examining'),
    (r'\bdelve\b', 'explore'),
    (r'\bDelve\b', 'Explore'),
    (r'\bdelves\b', 'explores'),
    (r'\bDelves\b', 'Explores'),
    (r'\bdelved\b', 'explored'),

    # "leverage" / "leveraging" -> "use" / "using"
    (r'\bleveraging\b', 'using'),
    (r'\bLeveraging\b', 'Using'),
    (r'\bleveraged\b', 'used'),
    (r'\bLeveraged\b', 'Used'),
    (r'\bleverages\b', 'uses'),
    (r'\bleverage\b', 'use'),
    (r'\bLeverage\b', 'Use'),

    # "utilize" / "utilizing" -> "use" / "using"
    (r'\butilizing\b', 'using'),
    (r'\bUtilizing\b', 'Using'),
    (r'\butilized\b', 'used'),
    (r'\bUtilized\b', 'Used'),
    (r'\butilizes\b', 'uses'),
    (r'\bUtilizes\b', 'Uses'),
    (r'\butilize\b', 'use'),
    (r'\bUtilize\b', 'Use'),
    (r'\butilization\b', 'use'),
    (r'\bUtilization\b', 'Use'),

    # "streamline" / "streamlined" -> "simplify" / "simplified"
    (r'\bstreamlining\b', 'simplifying'),
    (r'\bStreamlining\b', 'Simplifying'),
    (r'\bstreamlined\b', 'simplified'),
    (r'\bStreamlined\b', 'Simplified'),
    (r'\bstreamlines\b', 'simplifies'),
    (r'\bStreamlines\b', 'Simplifies'),
    (r'\bstreamline\b', 'simplify'),
    (r'\bStreamline\b', 'Simplify'),

    # "robust" -> "strong" / "solid" / "reliable"
    (r'\brobust\b', 'solid'),
    (r'\bRobust\b', 'Solid'),

    # "landscape" (metaphorical) -> "field" / "space"
    # Be careful: only replace when used metaphorically (e.g., "the X landscape")
    (r'\bthe\s+(\w+)\s+landscape\b', r'the \1 space'),
    (r'\bThe\s+(\w+)\s+landscape\b', r'The \1 space'),
    (r'\bdigital landscape\b', 'digital space'),
    (r'\bDigital landscape\b', 'Digital space'),
    (r'\bfinancial landscape\b', 'financial space'),
    (r'\btechnological landscape\b', 'technology space'),
    (r'\btechnology landscape\b', 'technology space'),
    (r'\blandscape of\b', 'field of'),
    (r'\bLandscape of\b', 'Field of'),

    # "cutting-edge" -> "modern" / "latest"
    (r'\bcutting-edge\b', 'modern'),
    (r'\bCutting-edge\b', 'Modern'),
    (r'\bcutting edge\b', 'modern'),
    (r'\bCutting edge\b', 'Modern'),

    # "game-changer" / "game changing" -> remove or rephrase
    (r'\ba?\s*game-changer\b', 'a major improvement'),
    (r'\ba?\s*Game-changer\b', 'A major improvement'),
    (r'\bgame-changing\b', 'significant'),
    (r'\bGame-changing\b', 'Significant'),
    (r'\bgame changer\b', 'major improvement'),
    (r'\bGame changer\b', 'Major improvement'),
    (r'\bgame changing\b', 'significant'),
    (r'\bGame changing\b', 'Significant'),

    # "empower" / "empowering" -> "help" / "enable"
    (r'\bempowering\b', 'helping'),
    (r'\bEmpowering\b', 'Helping'),
    (r'\bempowered\b', 'enabled'),
    (r'\bEmpowered\b', 'Enabled'),
    (r'\bempowers\b', 'helps'),
    (r'\bEmpowers\b', 'Helps'),
    (r'\bempower\b', 'help'),
    (r'\bEmpower\b', 'Help'),

    # "unlock" (metaphorical) -> "access" / "enable"
    # Be careful with literal unlock (e.g., unlock a phone)
    (r'\bunlock the\b', 'access the'),
    (r'\bUnlock the\b', 'Access the'),
    (r'\bunlock your\b', 'access your'),
    (r'\bUnlock your\b', 'Access your'),
    (r'\bunlocking\b', 'accessing'),
    (r'\bUnlocking\b', 'Accessing'),
    (r'\bunlocks\b', 'enables'),
    (r'\bUnlocks\b', 'Enables'),

    # "harness" -> "use" / "apply"
    (r'\bharnessing\b', 'using'),
    (r'\bHarnessing\b', 'Using'),
    (r'\bharnessed\b', 'used'),
    (r'\bharnesses\b', 'uses'),
    (r'\bharness the\b', 'use the'),
    (r'\bHarness the\b', 'Use the'),
    (r'\bharness your\b', 'use your'),
    (r'\bHarness your\b', 'Use your'),
    (r'\bharness\b', 'use'),
    (r'\bHarness\b', 'Use'),

    # "elevate" -> "improve" / "raise"
    (r'\belevating\b', 'improving'),
    (r'\bElevating\b', 'Improving'),
    (r'\belevated\b', 'improved'),
    (r'\bElevated\b', 'Improved'),
    (r'\belevates\b', 'improves'),
    (r'\bElevates\b', 'Improves'),
    (r'\belevate\b', 'improve'),
    (r'\bElevate\b', 'Improve'),

    # "seamless" / "seamlessly" -> "smooth" / "smoothly" or remove
    (r'\bseamlessly\b', 'smoothly'),
    (r'\bSeamlessly\b', 'Smoothly'),
    (r'\bseamless\b', 'smooth'),
    (r'\bSeamless\b', 'Smooth'),

    # "revolutionize" -> "change" / "improve"
    (r'\brevolutionizing\b', 'changing'),
    (r'\bRevolutionizing\b', 'Changing'),
    (r'\brevolutionized\b', 'changed'),
    (r'\bRevolutionized\b', 'Changed'),
    (r'\brevolutionizes\b', 'changes'),
    (r'\bRevolutionizes\b', 'Changes'),
    (r'\brevolutionize\b', 'change'),
    (r'\bRevolutionize\b', 'Change'),

    # "pivotal" -> "key" / "important"
    (r'\bpivotal\b', 'key'),
    (r'\bPivotal\b', 'Key'),

    # "innovative" -> "new" / "modern"
    (r'\binnovative\b', 'modern'),
    (r'\bInnovative\b', 'Modern'),
    (r'\binnovation\b', 'advancement'),
    (r'\bInnovation\b', 'Advancement'),

    # "transformative" -> "significant" / "important"
    (r'\btransformative\b', 'significant'),
    (r'\bTransformative\b', 'Significant'),

    # "holistic" -> "complete" / "full"
    (r'\bholistic\b', 'complete'),
    (r'\bHolistic\b', 'Complete'),
    (r'\bholistically\b', 'completely'),
    (r'\bHolistically\b', 'Completely'),

    # "synergy" -> remove or rephrase
    (r'\bsynergies\b', 'combined benefits'),
    (r'\bSynergies\b', 'Combined benefits'),
    (r'\bsynergy\b', 'combined benefit'),
    (r'\bSynergy\b', 'Combined benefit'),

    # "paradigm" -> remove or rephrase
    (r'\bparadigm shift\b', 'major change'),
    (r'\bParadigm shift\b', 'Major change'),
    (r'\bparadigm\b', 'approach'),
    (r'\bParadigm\b', 'Approach'),

    # "ecosystem" (non-literal) -> "system" / "platform"
    # Skip actual ecosystem references (biology/ecology tools)
    (r'\bthe\s+(\w+)\s+ecosystem\b', r'the \1 system'),
    (r'\bThe\s+(\w+)\s+ecosystem\b', r'The \1 system'),
]

# Tier 2 - Check context, fix if AI-sounding
TIER2_REPLACEMENTS = [
    # "In conclusion" -> remove or rephrase
    (r'\bIn conclusion,?\s*', ''),
    (r'\bin conclusion,?\s*', ''),

    # "It's worth noting" -> remove, just state the fact
    (r"It's worth noting that\s*", ''),
    (r"It is worth noting that\s*", ''),
    (r"it's worth noting that\s*", ''),
    (r"it is worth noting that\s*", ''),

    # "It's important to note" -> same
    (r"It's important to note that\s*", ''),
    (r"It is important to note that\s*", ''),
    (r"it's important to note that\s*", ''),
    (r"it is important to note that\s*", ''),

    # "At the end of the day" -> remove
    (r'\bAt the end of the day,?\s*', ''),
    (r'\bat the end of the day,?\s*', ''),

    # "In today's" / "In the modern" -> specific or remove
    (r"\bIn today's digital age,?\s*", ''),
    (r"\bIn today's world,?\s*", ''),
    (r"\bIn today's fast-paced,?\s*", 'In a fast-paced '),
    (r"\bIn the modern era,?\s*", ''),
    (r"\bIn the modern world,?\s*", ''),
    (r"\bIn today's ever-evolving,?\s*", ''),
    (r"\bIn today's increasingly,?\s*", ''),

    # "Whether you're a ... or a ..." - flag but harder to auto-fix
    # We'll just scan for these
]

# Excessive transition words
TRANSITION_REPLACEMENTS = [
    (r'\bFurthermore,?\s*', 'Also, '),
    (r'\bMoreover,?\s*', 'Also, '),
    (r'\bAdditionally,?\s*', 'Also, '),
    (r'\bConsequently,?\s*', 'As a result, '),
    (r'\bNevertheless,?\s*', 'Still, '),
    (r'\bNonetheless,?\s*', 'Still, '),
]


def get_all_html_files(base_dir):
    """Get all index.html files from tool directories and article directories."""
    html_files = []
    for entry in os.listdir(base_dir):
        full_path = os.path.join(base_dir, entry)
        if os.path.isdir(full_path):
            index_path = os.path.join(full_path, "index.html")
            if os.path.isfile(index_path):
                html_files.append(index_path)
            # Check for articles subdirectories
            if entry == "articles":
                for article_dir in os.listdir(full_path):
                    article_path = os.path.join(full_path, article_dir, "index.html")
                    if os.path.isfile(article_path):
                        html_files.append(article_path)
    # Also include root index.html
    root_index = os.path.join(base_dir, "index.html")
    if os.path.isfile(root_index):
        html_files.append(root_index)
    return sorted(html_files)


def is_in_script_or_style(content, match_start):
    """Check if a match position is inside a <script> or <style> tag."""
    # Find the last opening script/style tag before this position
    last_script_open = content.rfind('<script', 0, match_start)
    last_script_close = content.rfind('</script>', 0, match_start)
    if last_script_open > last_script_close:
        return True

    last_style_open = content.rfind('<style', 0, match_start)
    last_style_close = content.rfind('</style>', 0, match_start)
    if last_style_open > last_style_close:
        return True

    return False


def is_in_html_attribute(content, match_start):
    """Check if a match position is inside an HTML attribute value."""
    # Check if we're inside a tag by looking for < and > boundaries
    last_open = content.rfind('<', 0, match_start)
    last_close = content.rfind('>', 0, match_start)
    if last_open > last_close:
        # We're inside a tag - could be an attribute
        # Check if it's in alt, title, content, name attribute
        tag_content = content[last_open:match_start]
        if 'alt=' in tag_content or 'title=' in tag_content or 'name=' in tag_content:
            return True
        # Don't skip content= for meta descriptions - we want to fix those too
    return False


def is_in_url_or_href(content, match_start):
    """Check if match is inside a URL or href attribute."""
    last_open = content.rfind('<', 0, match_start)
    last_close = content.rfind('>', 0, match_start)
    if last_open > last_close:
        tag_content = content[last_open:match_start]
        if 'href=' in tag_content or 'src=' in tag_content or 'url(' in tag_content:
            return True
    return False


def safe_replace(content, pattern, replacement):
    """Replace pattern in content but skip script/style blocks and URLs."""
    result = content
    changes = 0

    # Find all matches first
    matches = list(re.finditer(pattern, result))

    # Process in reverse order to maintain positions
    for match in reversed(matches):
        start = match.start()

        # Skip if inside script, style, URL, or href
        if is_in_script_or_style(result, start):
            continue
        if is_in_url_or_href(result, start):
            continue

        # Perform replacement
        if callable(replacement):
            new_text = replacement(match)
        else:
            new_text = match.expand(replacement)

        result = result[:start] + new_text + result[match.end():]
        changes += 1

    return result, changes


def cycle1_scan_and_fix(html_files, dry_run=False):
    """Cycle 1: Scan for AI words and replace them."""
    print("=" * 70)
    print("CYCLE 1: AI Word Scan and Replace")
    print("=" * 70)

    total_changes = defaultdict(int)
    files_changed = set()
    file_change_details = defaultdict(lambda: defaultdict(int))

    all_replacements = TIER1_REPLACEMENTS + TIER2_REPLACEMENTS + TRANSITION_REPLACEMENTS

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original = f.read()
        except Exception as e:
            print(f"  ERROR reading {filepath}: {e}")
            continue

        content = original
        file_changes = 0

        for pattern, replacement in all_replacements:
            new_content, changes = safe_replace(content, pattern, replacement)
            if changes > 0:
                # Get a clean label for the pattern
                label = pattern.replace(r'\b', '').replace(r'\s+', ' ').replace('\\', '')
                total_changes[label] += changes
                file_change_details[filepath][label] = changes
                file_changes += changes
                content = new_content

        if file_changes > 0:
            files_changed.add(filepath)
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            rel_path = os.path.relpath(filepath, BASE_DIR)
            print(f"  Fixed {file_changes} AI words in: {rel_path}")

    print(f"\n--- Cycle 1 Summary ---")
    print(f"Files scanned: {len(html_files)}")
    print(f"Files modified: {len(files_changed)}")

    total_all = sum(total_changes.values())
    print(f"Total replacements: {total_all}")
    print(f"\nBreakdown by pattern:")
    for pattern, count in sorted(total_changes.items(), key=lambda x: -x[1]):
        print(f"  {pattern}: {count}")

    return total_changes, files_changed, file_change_details


# ============================================================
# CYCLE 2: Structural AI Patterns
# ============================================================

def cycle2_scan_and_fix(html_files, dry_run=False):
    """Cycle 2: Fix structural AI patterns."""
    print("\n" + "=" * 70)
    print("CYCLE 2: Structural AI Pattern Fix")
    print("=" * 70)

    stats = {
        'strong_tags_in_articles': 0,
        'bold_colon_patterns': 0,
        'em_dashes': 0,
        'files_changed': set(),
    }

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                original = f.read()
        except Exception as e:
            continue

        content = original
        is_article = '/articles/' in filepath
        file_changes = 0

        # --- Fix em-dashes (replace with hyphen or rephrase) ---
        # Match em-dash characters: Unicode \u2014 and HTML entity &mdash;
        em_dash_count = content.count('\u2014') + content.count('&mdash;')
        if em_dash_count > 0:
            # Replace em-dashes with " - " (spaced en-dash style)
            # But skip if inside script/style
            new_content = ""
            i = 0
            in_script = False
            in_style = False
            while i < len(content):
                if content[i:i+7].lower() == '<script':
                    in_script = True
                elif content[i:i+9].lower() == '</script>':
                    in_script = False
                elif content[i:i+6].lower() == '<style':
                    in_style = True
                elif content[i:i+8].lower() == '</style>':
                    in_style = False

                if not in_script and not in_style:
                    if content[i] == '\u2014':
                        new_content += ' - '
                        stats['em_dashes'] += 1
                        file_changes += 1
                        i += 1
                        continue
                    elif content[i:i+7] == '&mdash;':
                        new_content += ' - '
                        stats['em_dashes'] += 1
                        file_changes += 1
                        i += 7
                        continue

                new_content += content[i]
                i += 1
            content = new_content

        # --- Fix <strong> and <b> tags in article content ---
        # For articles, remove ALL strong/b tags in body content (not in navigation/head)
        if is_article:
            # Remove <strong>...</strong> but keep the inner text
            strong_count = len(re.findall(r'<strong>', content, re.IGNORECASE))
            if strong_count > 0:
                content = re.sub(r'<strong>(.*?)</strong>', r'\1', content, flags=re.DOTALL|re.IGNORECASE)
                stats['strong_tags_in_articles'] += strong_count
                file_changes += strong_count

            b_count = len(re.findall(r'<b>', content, re.IGNORECASE))
            if b_count > 0:
                content = re.sub(r'<b>(.*?)</b>', r'\1', content, flags=re.DOTALL|re.IGNORECASE)
                stats['strong_tags_in_articles'] += b_count
                file_changes += b_count

        # --- Fix bold-colon AI pattern: "**Keyword:** explanation" in HTML ---
        # Pattern: <strong>Word:</strong> or <b>Word:</b>
        bold_colon_matches = re.findall(r'<(?:strong|b)>([^<]+?):</(?:strong|b)>\s*', content, re.IGNORECASE)
        if bold_colon_matches:
            # Remove the bold formatting around keyword:
            content = re.sub(r'<(?:strong|b)>([^<]+?):</(?:strong|b)>\s*', r'\1: ', content, flags=re.IGNORECASE)
            stats['bold_colon_patterns'] += len(bold_colon_matches)
            file_changes += len(bold_colon_matches)

        if file_changes > 0:
            stats['files_changed'].add(filepath)
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            rel_path = os.path.relpath(filepath, BASE_DIR)
            print(f"  Fixed {file_changes} structural issues in: {rel_path}")

    print(f"\n--- Cycle 2 Summary ---")
    print(f"Strong/b tags removed (articles): {stats['strong_tags_in_articles']}")
    print(f"Bold-colon patterns fixed: {stats['bold_colon_patterns']}")
    print(f"Em-dashes replaced: {stats['em_dashes']}")
    print(f"Files modified: {len(stats['files_changed'])}")

    return stats


# ============================================================
# CYCLE 3: Article-Specific Deep Edit
# ============================================================

def cycle3_article_edit(html_files, dry_run=False):
    """Cycle 3: Article-specific deep edit checks."""
    print("\n" + "=" * 70)
    print("CYCLE 3: Article-Specific Deep Edit")
    print("=" * 70)

    article_files = [f for f in html_files if '/articles/' in f]

    stats = {
        'generic_openings_fixed': 0,
        'formulaic_conclusions_fixed': 0,
        'we_our_fixed': 0,
        'hashtags_fixed': 0,
        'markdown_bold_fixed': 0,
        'remaining_em_dashes': 0,
        'remaining_strong': 0,
        'files_changed': set(),
        'issues_remaining': defaultdict(list),
    }

    for filepath in article_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            continue

        original = content
        rel_path = os.path.relpath(filepath, BASE_DIR)

        # --- Fix "we" and "our team" references ---
        # Replace "we offer" / "our team" / "we provide" with "I" voice
        replacements_we = [
            (r'\bour team\b', 'I'),
            (r'\bOur team\b', 'I'),
            (r'\bwe offer\b', 'I offer'),
            (r'\bWe offer\b', 'I offer'),
            (r'\bwe provide\b', 'I provide'),
            (r'\bWe provide\b', 'I provide'),
            (r'\bwe have\b', 'I have'),
            (r'\bWe have\b', 'I have'),
            (r'\bwe believe\b', 'I believe'),
            (r'\bWe believe\b', 'I believe'),
            (r'\bour goal\b', 'my goal'),
            (r'\bOur goal\b', 'My goal'),
            (r'\bwe recommend\b', 'I recommend'),
            (r'\bWe recommend\b', 'I recommend'),
            (r'\bwe created\b', 'I created'),
            (r'\bWe created\b', 'I created'),
            (r'\bwe built\b', 'I built'),
            (r'\bWe built\b', 'I built'),
            (r'\bwe designed\b', 'I designed'),
            (r'\bWe designed\b', 'I designed'),
            (r'\bour approach\b', 'my approach'),
            (r'\bOur approach\b', 'My approach'),
        ]

        for pattern, replacement in replacements_we:
            new_content, changes = safe_replace(content, pattern, replacement)
            if changes > 0:
                stats['we_our_fixed'] += changes
                content = new_content

        # --- Fix markdown bold **text** ---
        md_bold = re.findall(r'\*\*[^*]+\*\*', content)
        if md_bold:
            for match in md_bold:
                inner = match[2:-2]
                content = content.replace(match, inner, 1)
                stats['markdown_bold_fixed'] += 1

        # --- Fix hashtags (#topic) at end of content ---
        hashtag_matches = re.findall(r'#[A-Za-z]\w+', content)
        # Filter out CSS selectors and hex colors
        real_hashtags = [h for h in hashtag_matches if not re.match(r'#[0-9a-fA-F]{3,8}$', h)]
        # Filter out anchor links
        real_hashtags = [h for h in real_hashtags if not h.startswith('#id-')]

        # --- Check for remaining issues ---
        if '\u2014' in content or '&mdash;' in content:
            stats['remaining_em_dashes'] += content.count('\u2014') + content.count('&mdash;')
            stats['issues_remaining'][rel_path].append(f"em-dashes: {content.count(chr(0x2014)) + content.count('&mdash;')}")

        remaining_strong = len(re.findall(r'<strong>', content, re.IGNORECASE))
        if remaining_strong > 0:
            stats['remaining_strong'] += remaining_strong
            stats['issues_remaining'][rel_path].append(f"strong tags: {remaining_strong}")

        if content != original:
            stats['files_changed'].add(filepath)
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            print(f"  Fixed article: {rel_path}")

    print(f"\n--- Cycle 3 Summary ---")
    print(f"Articles scanned: {len(article_files)}")
    print(f"Articles modified: {len(stats['files_changed'])}")
    print(f"We/our references fixed: {stats['we_our_fixed']}")
    print(f"Markdown bold fixed: {stats['markdown_bold_fixed']}")
    print(f"Remaining em-dashes: {stats['remaining_em_dashes']}")
    print(f"Remaining strong tags: {stats['remaining_strong']}")

    if stats['issues_remaining']:
        print(f"\nFiles with remaining issues:")
        for f, issues in stats['issues_remaining'].items():
            print(f"  {f}: {', '.join(issues)}")

    return stats


# ============================================================
# CYCLE 4: Tool Page Content Sections
# ============================================================

def cycle4_tool_pages(html_files, dry_run=False):
    """Cycle 4: Scan tool page educational content."""
    print("\n" + "=" * 70)
    print("CYCLE 4: Tool Page Content Sections")
    print("=" * 70)

    tool_files = [f for f in html_files if '/articles/' not in f]

    stats = {
        'total_fixes': 0,
        'files_changed': set(),
        'strong_tags_fixed': 0,
        'bold_colon_fixed': 0,
    }

    # Additional tool-specific AI patterns to scan
    tool_patterns = [
        # More AI filler phrases
        (r'\bwhether you\'re a beginner or\b', 'at any skill level'),
        (r'\bWhether you\'re a beginner or\b', 'At any skill level'),
        (r'\bwhether you are a beginner or\b', 'at any skill level'),
        (r'\bWhether you are a beginner or\b', 'At any skill level'),
        (r'\bpowerful tool\b', 'useful tool'),
        (r'\bPowerful tool\b', 'Useful tool'),
        (r'\bpowerful and\b', 'capable and'),
        (r'\bpowerful way\b', 'effective way'),
        (r'\bPowerful way\b', 'Effective way'),
        (r'\bplethora of\b', 'range of'),
        (r'\bPlethora of\b', 'Range of'),
        (r'\bmyriad of\b', 'range of'),
        (r'\bMyriad of\b', 'Range of'),
        (r'\ba myriad\b', 'many'),
        (r'\bA myriad\b', 'Many'),
        (r'\bplay a crucial role\b', 'matter'),
        (r'\bplays a crucial role\b', 'matters'),
        (r'\bplay a vital role\b', 'matter'),
        (r'\bplays a vital role\b', 'matters'),
        (r'\bplays an important role\b', 'matters'),
        (r'\bin the realm of\b', 'in'),
        (r'\bIn the realm of\b', 'In'),
        (r'\bin the world of\b', 'in'),
        (r'\bIn the world of\b', 'In'),
        (r'\bwith that being said\b', ''),
        (r'\bWith that being said,?\s*', ''),
        (r'\bThat being said,?\s*', ''),
        (r'\bthat being said,?\s*', ''),
        (r'\bIt goes without saying\b', ''),
        (r'\bit goes without saying\b', ''),
        (r'\bneedless to say,?\s*', ''),
        (r'\bNeedless to say,?\s*', ''),
    ]

    for filepath in tool_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            continue

        original = content
        file_changes = 0

        for pattern, replacement in tool_patterns:
            new_content, changes = safe_replace(content, pattern, replacement)
            if changes > 0:
                file_changes += changes
                content = new_content

        # Fix bold-colon pattern in tool pages too
        bold_colon_matches = re.findall(r'<(?:strong|b)>([^<]+?):</(?:strong|b)>\s*', content, re.IGNORECASE)
        if bold_colon_matches:
            content = re.sub(r'<(?:strong|b)>([^<]+?):</(?:strong|b)>\s*', r'\1: ', content, flags=re.IGNORECASE)
            stats['bold_colon_fixed'] += len(bold_colon_matches)
            file_changes += len(bold_colon_matches)

        if file_changes > 0:
            stats['files_changed'].add(filepath)
            stats['total_fixes'] += file_changes
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
            rel_path = os.path.relpath(filepath, BASE_DIR)
            print(f"  Fixed {file_changes} issues in: {rel_path}")

    print(f"\n--- Cycle 4 Summary ---")
    print(f"Tool pages scanned: {len(tool_files)}")
    print(f"Tool pages modified: {len(stats['files_changed'])}")
    print(f"Total fixes: {stats['total_fixes']}")
    print(f"Bold-colon patterns fixed: {stats['bold_colon_fixed']}")

    return stats


# ============================================================
# CYCLE 5: Final Verification Count
# ============================================================

def cycle5_final_count(html_files):
    """Cycle 5: Final verification - count any remaining AI signals."""
    print("\n" + "=" * 70)
    print("CYCLE 5: Final Verification Count")
    print("=" * 70)

    # All AI words to check for
    ai_words = [
        'comprehensive', 'delve', 'delving', 'delves',
        'leverage', 'leveraging', 'leveraged', 'leverages',
        'utilize', 'utilizing', 'utilized', 'utilizes', 'utilization',
        'streamline', 'streamlined', 'streamlining', 'streamlines',
        'robust',
        'cutting-edge', 'cutting edge',
        'game-changer', 'game changer', 'game-changing', 'game changing',
        'empower', 'empowering', 'empowered', 'empowers',
        'harness', 'harnessing', 'harnessed', 'harnesses',
        'elevate', 'elevating', 'elevated', 'elevates',
        'seamless', 'seamlessly',
        'revolutionize', 'revolutionizing', 'revolutionized', 'revolutionizes',
        'pivotal',
        'innovative', 'innovation',
        'transformative',
        'holistic', 'holistically',
        'synergy', 'synergies',
        'paradigm',
        'plethora', 'myriad',
    ]

    # Structural patterns
    structural_patterns = {
        'em_dashes': r'[\u2014]|&mdash;',
        'strong_in_articles': None,  # handled specially
        'In conclusion': r'\bIn conclusion\b',
        "It's worth noting": r"It's worth noting|It is worth noting",
        "It's important to note": r"It's important to note|It is important to note",
        'Furthermore': r'\bFurthermore\b',
        'Moreover': r'\bMoreover\b',
        'Additionally': r'\bAdditionally\b',
        'markdown_bold': r'\*\*[^*]+\*\*',
    }

    remaining = defaultdict(lambda: defaultdict(int))
    files_clean = 0
    files_with_issues = []
    total_remaining = 0
    word_totals = defaultdict(int)

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue

        # Extract text content (skip script/style)
        text_content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL|re.IGNORECASE)
        text_content = re.sub(r'<style[^>]*>.*?</style>', '', text_content, flags=re.DOTALL|re.IGNORECASE)
        # Keep content in href/src attributes out of text matching
        # Actually, we should also skip URLs

        rel_path = os.path.relpath(filepath, BASE_DIR)
        file_issues = 0

        # Check AI words
        for word in ai_words:
            pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
            matches = pattern.findall(text_content)
            if matches:
                count = len(matches)
                remaining[rel_path][word] = count
                file_issues += count
                word_totals[word] += count

        # Check structural patterns
        for name, pattern in structural_patterns.items():
            if pattern is None:
                continue
            matches = re.findall(pattern, text_content)
            if matches:
                count = len(matches)
                remaining[rel_path][name] = count
                file_issues += count
                word_totals[name] += count

        # Check strong tags in articles specifically
        if '/articles/' in filepath:
            strong_count = len(re.findall(r'<strong>', text_content, re.IGNORECASE))
            b_count = len(re.findall(r'<b>', text_content, re.IGNORECASE))
            if strong_count + b_count > 0:
                remaining[rel_path]['strong/b_tags'] = strong_count + b_count
                file_issues += strong_count + b_count
                word_totals['strong/b_in_articles'] += strong_count + b_count

        if file_issues > 0:
            files_with_issues.append((rel_path, file_issues))
            total_remaining += file_issues
        else:
            files_clean += 1

    # Print report
    print(f"\nFiles scanned: {len(html_files)}")
    print(f"Files with ZERO issues: {files_clean}")
    print(f"Files with remaining issues: {len(files_with_issues)}")
    print(f"Total remaining AI signals: {total_remaining}")

    if word_totals:
        print(f"\nRemaining signals by type:")
        for word, count in sorted(word_totals.items(), key=lambda x: -x[1]):
            print(f"  {word}: {count}")

    if files_with_issues:
        print(f"\nFiles with remaining issues (sorted by severity):")
        for fpath, count in sorted(files_with_issues, key=lambda x: -x[1])[:50]:
            details = remaining[fpath]
            detail_str = ", ".join(f"{k}:{v}" for k, v in sorted(details.items(), key=lambda x: -x[1]))
            print(f"  [{count}] {fpath}: {detail_str}")
        if len(files_with_issues) > 50:
            print(f"  ... and {len(files_with_issues) - 50} more files")

    return remaining, files_clean, files_with_issues, word_totals


# ============================================================
# MAIN
# ============================================================

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("*** DRY RUN MODE - No files will be modified ***\n")

    print(f"Scanning directory: {BASE_DIR}")
    html_files = get_all_html_files(BASE_DIR)
    print(f"Found {len(html_files)} HTML files to scan\n")

    if mode in ("all", "cycle1"):
        cycle1_scan_and_fix(html_files, dry_run)

    if mode in ("all", "cycle2"):
        cycle2_scan_and_fix(html_files, dry_run)

    if mode in ("all", "cycle3"):
        cycle3_article_edit(html_files, dry_run)

    if mode in ("all", "cycle4"):
        cycle4_tool_pages(html_files, dry_run)

    if mode in ("all", "cycle5", "verify"):
        cycle5_final_count(html_files)


if __name__ == "__main__":
    main()
