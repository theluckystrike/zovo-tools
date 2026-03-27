#!/usr/bin/env python3
"""
Deep Anti-AI Editorial Sweep v2 - ZERO AI Signals
Context-aware scanning with domain-specific exceptions.
Scans all HTML files in zovo-tools for AI-generated language patterns and fixes them.
Author: Michael Lip
"""

import os
import re
import json
import sys
from collections import defaultdict

BASE_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

# Domain-specific exceptions: words that look like AI buzzwords but are legitimate
# in specific tool contexts
DOMAIN_EXCEPTIONS = {
    # "seamless" in gutter-size-calculator refers to "seamless gutters" (a real product)
    'gutter-size-calculator': ['seamless', 'Seamless'],
    # "utilization" in credit-score-simulator means "credit utilization" (financial term)
    'credit-score-simulator': ['utilization', 'Utilization'],
    # "elevated" in a1c-calculator means medically elevated blood sugar levels
    'a1c-calculator': ['elevated', 'Elevated'],
    # "harnesses" in random-counter means "test harnesses" (programming term)
    'random-counter': ['harnesses'],
    # "harnesses" in roof-pitch-calculator may refer to physical safety harnesses
    'roof-pitch-calculator': ['harnesses'],
    # "innovation" in h1b context is about immigration policy discussion
    'h1b-wage-level-calculator': ['innovation'],
}


def get_all_html_files(base_dir):
    """Get all index.html files from tool directories and article directories."""
    html_files = []
    for entry in os.listdir(base_dir):
        full_path = os.path.join(base_dir, entry)
        if os.path.isdir(full_path):
            index_path = os.path.join(full_path, "index.html")
            if os.path.isfile(index_path):
                html_files.append(index_path)
            if entry == "articles":
                for article_dir in os.listdir(full_path):
                    article_path = os.path.join(full_path, article_dir, "index.html")
                    if os.path.isfile(article_path):
                        html_files.append(article_path)
    root_index = os.path.join(base_dir, "index.html")
    if os.path.isfile(root_index):
        html_files.append(root_index)
    return sorted(html_files)


def get_tool_name(filepath):
    """Extract tool directory name from filepath."""
    rel = os.path.relpath(filepath, BASE_DIR)
    parts = rel.split(os.sep)
    return parts[0] if parts else ''


def is_in_script_or_style(content, match_start):
    """Check if a match position is inside a <script> or <style> tag."""
    last_script_open = content.rfind('<script', 0, match_start)
    last_script_close = content.rfind('</script>', 0, match_start)
    if last_script_open > last_script_close:
        return True
    last_style_open = content.rfind('<style', 0, match_start)
    last_style_close = content.rfind('</style>', 0, match_start)
    if last_style_open > last_style_close:
        return True
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


def is_in_json_ld(content, match_start):
    """Check if match is inside a JSON-LD script block."""
    last_jsonld = content.rfind('application/ld+json', 0, match_start)
    if last_jsonld == -1:
        return False
    last_script_close = content.rfind('</script>', last_jsonld, match_start)
    if last_script_close == -1:
        return True  # inside JSON-LD
    return False


def is_domain_exception(filepath, matched_text):
    """Check if the matched word is a domain-specific exception for this tool."""
    tool_name = get_tool_name(filepath)
    exceptions = DOMAIN_EXCEPTIONS.get(tool_name, [])
    for exc in exceptions:
        if exc.lower() in matched_text.lower():
            return True
    return False


def get_surrounding_context(content, start, end, chars=60):
    """Get surrounding text for context-aware decisions."""
    ctx_start = max(0, start - chars)
    ctx_end = min(len(content), end + chars)
    return content[ctx_start:ctx_end]


def context_aware_skip(filepath, content, match_start, match_end, matched_text):
    """Advanced context checks for words that might be legitimate."""
    context = get_surrounding_context(content, match_start, match_end, 80).lower()
    word = matched_text.lower().strip()

    # "seamless" - skip if about seamless gutters
    if word in ('seamless', 'seamlessly'):
        if any(term in context for term in ['gutter', 'aluminum', 'copper', 'installation']):
            return True

    # "elevated" - skip if medical context
    if word == 'elevated':
        if any(term in context for term in ['blood', 'glucose', 'a1c', 'risk', 'sugar',
                                             'pressure', 'heart', 'level', 'cholesterol',
                                             'triglyceride', 'bilirubin', 'creatinine',
                                             'temperature', 'deck', 'surface', 'floor',
                                             'platform', 'highway', 'train', 'railroad']):
            return True

    # "utilization" - skip if "credit utilization" (financial term)
    if word == 'utilization':
        if 'credit' in context:
            return True

    # "innovation" - skip if about policy, economy, or Swiss context
    if word == 'innovation':
        if any(term in context for term in ['swiss', 'switzerland', 'patent', 'research',
                                             'policy', 'contribute', 'economy', 'h1b',
                                             'visa', 'immigration', 'workforce']):
            return True

    # "harnesses" - skip if "test harnesses" or safety harnesses
    if word == 'harnesses':
        if any(term in context for term in ['test', 'safety', 'fall protection', 'climbing',
                                             'roof', 'roofing', 'construction']):
            return True

    # "comprehensive" - skip if part of "comprehensive coverage" (insurance),
    # "comprehensive exam" (medical), or "comprehensive chart/table"
    if word == 'comprehensive':
        if any(term in context for term in ['coverage', 'insurance', 'exam', 'examination',
                                             'chart', 'table', 'reference']):
            return True

    # "revolutionized" - skip if talking about historical events
    if word == 'revolutionized':
        if any(term in context for term in ['history', 'century', 'industry', 'swimming',
                                             'fiberglass', 'concrete', 'manufacturing']):
            return True

    return False


def safe_replace(content, pattern, replacement, filepath=None):
    """Replace pattern in content but skip script/style blocks, URLs, and domain exceptions."""
    result = content
    changes = 0

    matches = list(re.finditer(pattern, result))

    for match in reversed(matches):
        start = match.start()
        end = match.end()
        matched_text = match.group()

        # Skip if inside script, style, URL, or href
        if is_in_script_or_style(result, start):
            continue
        if is_in_url_or_href(result, start):
            continue
        if is_in_json_ld(result, start):
            continue

        # Skip domain-specific exceptions
        if filepath and is_domain_exception(filepath, matched_text):
            continue

        # Context-aware skip
        if filepath and context_aware_skip(filepath, result, start, end, matched_text):
            continue

        # Perform replacement
        if callable(replacement):
            new_text = replacement(match)
        else:
            new_text = match.expand(replacement)

        result = result[:start] + new_text + result[end:]
        changes += 1

    return result, changes


# ============================================================
# ALL REPLACEMENT RULES
# ============================================================

TIER1_REPLACEMENTS = [
    # "comprehensive" -> "complete" or "full"
    (r'\bcomprehensive\b', 'complete'),
    (r'\bComprehensive\b', 'Complete'),

    # "delve" / "delving"
    (r'\bdelving\b', 'examining'),
    (r'\bDelving\b', 'Examining'),
    (r'\bdelve\b', 'explore'),
    (r'\bDelve\b', 'Explore'),
    (r'\bdelves\b', 'explores'),
    (r'\bDelves\b', 'Explores'),
    (r'\bdelved\b', 'explored'),

    # "leverage" / "leveraging"
    (r'\bleveraging\b', 'using'),
    (r'\bLeveraging\b', 'Using'),
    (r'\bleveraged\b', 'used'),
    (r'\bLeveraged\b', 'Used'),
    (r'\bleverages\b', 'uses'),
    (r'\bleverage\b', 'use'),
    (r'\bLeverage\b', 'Use'),

    # "utilize" / "utilizing"
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

    # "streamline" / "streamlined"
    (r'\bstreamlining\b', 'simplifying'),
    (r'\bStreamlining\b', 'Simplifying'),
    (r'\bstreamlined\b', 'simplified'),
    (r'\bStreamlined\b', 'Simplified'),
    (r'\bstreamlines\b', 'simplifies'),
    (r'\bStreamlines\b', 'Simplifies'),
    (r'\bstreamline\b', 'simplify'),
    (r'\bStreamline\b', 'Simplify'),

    # "robust" -> "solid"
    (r'\brobust\b', 'solid'),
    (r'\bRobust\b', 'Solid'),

    # "landscape" (metaphorical)
    (r'\bthe\s+(\w+)\s+landscape\b', r'the \1 space'),
    (r'\bThe\s+(\w+)\s+landscape\b', r'The \1 space'),
    (r'\bdigital landscape\b', 'digital space'),
    (r'\bDigital landscape\b', 'Digital space'),
    (r'\bfinancial landscape\b', 'financial space'),
    (r'\btechnological landscape\b', 'technology space'),
    (r'\btechnology landscape\b', 'technology space'),
    (r'\blandscape of\b', 'field of'),
    (r'\bLandscape of\b', 'Field of'),

    # "cutting-edge"
    (r'\bcutting-edge\b', 'modern'),
    (r'\bCutting-edge\b', 'Modern'),
    (r'\bcutting edge\b', 'modern'),
    (r'\bCutting edge\b', 'Modern'),

    # "game-changer" / "game changing"
    (r'\ba?\s*game-changer\b', 'a major improvement'),
    (r'\ba?\s*Game-changer\b', 'A major improvement'),
    (r'\bgame-changing\b', 'significant'),
    (r'\bGame-changing\b', 'Significant'),
    (r'\bgame changer\b', 'major improvement'),
    (r'\bGame changer\b', 'Major improvement'),
    (r'\bgame changing\b', 'significant'),
    (r'\bGame changing\b', 'Significant'),

    # "empower" / "empowering"
    (r'\bempowering\b', 'helping'),
    (r'\bEmpowering\b', 'Helping'),
    (r'\bempowered\b', 'enabled'),
    (r'\bEmpowered\b', 'Enabled'),
    (r'\bempowers\b', 'helps'),
    (r'\bEmpowers\b', 'Helps'),
    (r'\bempower\b', 'help'),
    (r'\bEmpower\b', 'Help'),

    # "unlock" (metaphorical)
    (r'\bunlock the\b', 'access the'),
    (r'\bUnlock the\b', 'Access the'),
    (r'\bunlock your\b', 'access your'),
    (r'\bUnlock your\b', 'Access your'),
    (r'\bunlocking\b', 'accessing'),
    (r'\bUnlocking\b', 'Accessing'),
    (r'\bunlocks\b', 'enables'),
    (r'\bUnlocks\b', 'Enables'),

    # "harness" -> "use"
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

    # "elevate" -> "improve"
    (r'\belevating\b', 'improving'),
    (r'\bElevating\b', 'Improving'),
    (r'\belevated\b', 'improved'),
    (r'\bElevated\b', 'Improved'),
    (r'\belevates\b', 'improves'),
    (r'\bElevates\b', 'Improves'),
    (r'\belevate\b', 'improve'),
    (r'\bElevate\b', 'Improve'),

    # "seamless" / "seamlessly"
    (r'\bseamlessly\b', 'smoothly'),
    (r'\bSeamlessly\b', 'Smoothly'),
    (r'\bseamless\b', 'smooth'),
    (r'\bSeamless\b', 'Smooth'),

    # "revolutionize"
    (r'\brevolutionizing\b', 'changing'),
    (r'\bRevolutionizing\b', 'Changing'),
    (r'\brevolutionized\b', 'changed'),
    (r'\bRevolutionized\b', 'Changed'),
    (r'\brevolutionizes\b', 'changes'),
    (r'\bRevolutionizes\b', 'Changes'),
    (r'\brevolutionize\b', 'change'),
    (r'\bRevolutionize\b', 'Change'),

    # "pivotal"
    (r'\bpivotal\b', 'key'),
    (r'\bPivotal\b', 'Key'),

    # "innovative" / "innovation"
    (r'\binnovative\b', 'modern'),
    (r'\bInnovative\b', 'Modern'),
    (r'\binnovation\b', 'advancement'),
    (r'\bInnovation\b', 'Advancement'),
    (r'\binnovations\b', 'advancements'),
    (r'\bInnovations\b', 'Advancements'),

    # "transformative"
    (r'\btransformative\b', 'significant'),
    (r'\bTransformative\b', 'Significant'),

    # "holistic"
    (r'\bholistic\b', 'complete'),
    (r'\bHolistic\b', 'Complete'),
    (r'\bholistically\b', 'completely'),
    (r'\bHolistically\b', 'Completely'),

    # "synergy"
    (r'\bsynergies\b', 'combined benefits'),
    (r'\bSynergies\b', 'Combined benefits'),
    (r'\bsynergy\b', 'combined benefit'),
    (r'\bSynergy\b', 'Combined benefit'),

    # "paradigm"
    (r'\bparadigm shift\b', 'major change'),
    (r'\bParadigm shift\b', 'Major change'),
    (r'\bparadigm\b', 'approach'),
    (r'\bParadigm\b', 'Approach'),

    # "ecosystem" (non-literal)
    (r'\bthe\s+(\w+)\s+ecosystem\b', r'the \1 system'),
    (r'\bThe\s+(\w+)\s+ecosystem\b', r'The \1 system'),
]

TIER2_REPLACEMENTS = [
    # "In conclusion"
    (r'\bIn conclusion,?\s*', ''),
    (r'\bin conclusion,?\s*', ''),

    # "It's worth noting"
    (r"It's worth noting that\s*", ''),
    (r"It is worth noting that\s*", ''),
    (r"it's worth noting that\s*", ''),
    (r"it is worth noting that\s*", ''),
    # Also match without "that"
    (r"It's worth noting,?\s*", ''),
    (r"It is worth noting,?\s*", ''),

    # "It's important to note"
    (r"It's important to note that\s*", ''),
    (r"It is important to note that\s*", ''),
    (r"it's important to note that\s*", ''),
    (r"it is important to note that\s*", ''),
    # Without "that"
    (r"It's important to note,?\s*", ''),
    (r"It is important to note,?\s*", ''),

    # "At the end of the day"
    (r'\bAt the end of the day,?\s*', ''),
    (r'\bat the end of the day,?\s*', ''),

    # "In today's" / "In the modern"
    (r"\bIn today's digital age,?\s*", ''),
    (r"\bIn today's world,?\s*", ''),
    (r"\bIn today's fast-paced,?\s*", 'In a fast-paced '),
    (r"\bIn the modern era,?\s*", ''),
    (r"\bIn the modern world,?\s*", ''),
    (r"\bIn today's ever-evolving,?\s*", ''),
    (r"\bIn today's increasingly,?\s*", ''),
]

TRANSITION_REPLACEMENTS = [
    (r'\bFurthermore,?\s*', 'Also, '),
    (r'\bMoreover,?\s*', 'Also, '),
    (r'\bAdditionally,?\s*', 'Also, '),
    (r'\bConsequently,?\s*', 'As a result, '),
    (r'\bNevertheless,?\s*', 'Still, '),
    (r'\bNonetheless,?\s*', 'Still, '),
]

TOOL_EXTRA_PATTERNS = [
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


# ============================================================
# CYCLE 1: AI Word Scan and Fix
# ============================================================

def cycle1_scan_and_fix(html_files, dry_run=False):
    print("=" * 70)
    print("CYCLE 1: AI Word Scan and Replace")
    print("=" * 70)

    total_changes = defaultdict(int)
    files_changed = set()

    all_replacements = TIER1_REPLACEMENTS + TIER2_REPLACEMENTS + TRANSITION_REPLACEMENTS + TOOL_EXTRA_PATTERNS

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
            new_content, changes = safe_replace(content, pattern, replacement, filepath)
            if changes > 0:
                label = pattern.replace(r'\b', '').replace(r'\s+', ' ').replace('\\', '')
                total_changes[label] += changes
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

    return total_changes, files_changed


# ============================================================
# CYCLE 2: Structural AI Patterns
# ============================================================

def cycle2_scan_and_fix(html_files, dry_run=False):
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
        except:
            continue

        content = original
        is_article = '/articles/' in filepath
        file_changes = 0

        # --- Fix em-dashes ---
        em_dash_count = content.count('\u2014') + content.count('&mdash;')
        if em_dash_count > 0:
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
        if is_article:
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

        # --- Fix bold-colon AI pattern everywhere ---
        bold_colon_matches = re.findall(r'<(?:strong|b)>([^<]+?):</(?:strong|b)>\s*', content, re.IGNORECASE)
        if bold_colon_matches:
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
    print("\n" + "=" * 70)
    print("CYCLE 3: Article-Specific Deep Edit")
    print("=" * 70)

    article_files = [f for f in html_files if '/articles/' in f]

    stats = {
        'we_our_fixed': 0,
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
        except:
            continue

        original = content
        rel_path = os.path.relpath(filepath, BASE_DIR)

        # --- Fix "we" and "our team" references ---
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
            new_content, changes = safe_replace(content, pattern, replacement, filepath)
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

        # --- Check for remaining issues ---
        if '\u2014' in content or '&mdash;' in content:
            em_count = content.count('\u2014') + content.count('&mdash;')
            stats['remaining_em_dashes'] += em_count
            stats['issues_remaining'][rel_path].append(f"em-dashes: {em_count}")

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
    print("\n" + "=" * 70)
    print("CYCLE 4: Tool Page Content Sections")
    print("=" * 70)

    tool_files = [f for f in html_files if '/articles/' not in f]

    stats = {
        'total_fixes': 0,
        'files_changed': set(),
        'bold_colon_fixed': 0,
    }

    for filepath in tool_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue

        original = content
        file_changes = 0

        for pattern, replacement in TOOL_EXTRA_PATTERNS:
            new_content, changes = safe_replace(content, pattern, replacement, filepath)
            if changes > 0:
                file_changes += changes
                content = new_content

        # Fix bold-colon pattern in tool pages
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
# CYCLE 5: Final Verification Count (context-aware)
# ============================================================

def cycle5_final_count(html_files):
    print("\n" + "=" * 70)
    print("CYCLE 5: Final Verification Count")
    print("=" * 70)

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
        'innovative', 'innovation', 'innovations',
        'transformative',
        'holistic', 'holistically',
        'synergy', 'synergies',
        'paradigm',
        'plethora', 'myriad',
    ]

    structural_patterns = {
        'em_dashes': r'[\u2014]|&mdash;',
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
    domain_skipped = defaultdict(int)

    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue

        # Strip scripts and styles for scanning
        text_content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL|re.IGNORECASE)
        text_content = re.sub(r'<style[^>]*>.*?</style>', '', text_content, flags=re.DOTALL|re.IGNORECASE)

        rel_path = os.path.relpath(filepath, BASE_DIR)
        file_issues = 0

        # Check AI words with context awareness
        for word in ai_words:
            pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
            for m in pattern.finditer(text_content):
                # Check if domain exception
                if is_domain_exception(filepath, m.group()):
                    domain_skipped[word] += 1
                    continue
                # Check context-aware skip
                if context_aware_skip(filepath, text_content, m.start(), m.end(), m.group()):
                    domain_skipped[word] += 1
                    continue
                # Real AI signal
                remaining[rel_path][word] += 1
                file_issues += 1
                word_totals[word] += 1

        # Check structural patterns
        for name, pattern in structural_patterns.items():
            matches = re.findall(pattern, text_content)
            if matches:
                count = len(matches)
                remaining[rel_path][name] = count
                file_issues += count
                word_totals[name] += count

        # Check strong tags in articles
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

    print(f"\nFiles scanned: {len(html_files)}")
    print(f"Files with ZERO issues: {files_clean}")
    print(f"Files with remaining issues: {len(files_with_issues)}")
    print(f"Total remaining AI signals: {total_remaining}")
    print(f"Domain-specific terms skipped (legitimate): {sum(domain_skipped.values())}")

    if domain_skipped:
        print(f"\nLegitimate domain terms skipped:")
        for word, count in sorted(domain_skipped.items(), key=lambda x: -x[1]):
            print(f"  {word}: {count} (legitimate)")

    if word_totals:
        print(f"\nRemaining AI signals by type:")
        for word, count in sorted(word_totals.items(), key=lambda x: -x[1]):
            print(f"  {word}: {count}")

    if files_with_issues:
        print(f"\nFiles with remaining issues (sorted by severity):")
        for fpath, count in sorted(files_with_issues, key=lambda x: -x[1])[:100]:
            details = remaining[fpath]
            detail_str = ", ".join(f"{k}:{v}" for k, v in sorted(details.items(), key=lambda x: -x[1]))
            print(f"  [{count}] {fpath}: {detail_str}")

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
