#!/usr/bin/env python3
"""
Wikipedia Reference Fix - Cycle 2
Fix broken Wikipedia hrefs (raw API JSON dumps) and non-Wikipedia sources.
"""

import os
import re
import json

TOOLS_DIR = "/Users/mike/zovo-workspaces/zovo-tools"

def fix_raw_api_dump_hrefs(file_path):
    """Fix hrefs that contain raw Wikipedia API JSON dump instead of URL."""
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original = content

    # Pattern: href="{'desktop': {'page': 'https://en.wikipedia.org/wiki/SLUG', ...}}"
    # Replace with: href="https://en.wikipedia.org/wiki/SLUG"
    pattern = re.compile(
        r'''href="(\{'desktop':\s*\{'page':\s*'(https?://en\.wikipedia\.org/wiki/[^']+)'[^}]*\}[^"]*\})"'''
    )

    def replace_with_page_url(match):
        page_url = match.group(2)
        return f'href="{page_url}"'

    content = pattern.sub(replace_with_page_url, content)

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def fix_non_wikipedia_sources(file_path, tool_name):
    """Fix wiki-definition sections that link to non-Wikipedia sources."""

    # Mapping of tools to correct Wikipedia articles + definitions
    FIXES = {
        "closing-costs-calculator": {
            "url": "https://en.wikipedia.org/wiki/Closing_costs",
            "definition": "Closing costs are fees and expenses, beyond the property price, that buyers and sellers incur to finalize a real estate transaction. They typically range from 2% to 5% of the loan amount."
        },
        "cors-tester": {
            "url": "https://en.wikipedia.org/wiki/Cross-origin_resource_sharing",
            "definition": "Cross-origin resource sharing (CORS) is a mechanism that allows web pages to request resources from a different domain than the one that served the page, using additional HTTP headers."
        },
        "epub-to-pdf-converter": {
            "url": "https://en.wikipedia.org/wiki/EPUB",
            "definition": "EPUB (electronic publication) is an e-book file format that uses the .epub file extension. The format is designed for reflowable content, meaning the text display can be optimized for a particular display device."
        },
        "ssh-key-generator": {
            "url": "https://en.wikipedia.org/wiki/Secure_Shell",
            "definition": "Secure Shell (SSH) is a cryptographic network protocol for operating network services securely over an unsecured network. SSH keys provide a more secure method of authentication than passwords."
        },
        "take-home-pay-calculator": {
            "url": "https://en.wikipedia.org/wiki/Net_income",
            "definition": "Take-home pay, or net income, is the amount of money an employee receives after all deductions, including federal and state taxes, Social Security, Medicare, and other withholdings."
        },
        "timecard-calculator": {
            "url": "https://en.wikipedia.org/wiki/Time_and_attendance",
            "definition": "Time and attendance systems track employee work hours, including clock-in, clock-out, breaks, and overtime, for payroll processing and labor compliance."
        },
    }

    if tool_name not in FIXES:
        return False

    fix = FIXES[tool_name]

    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original = content

    # Replace the source URL
    # Find the wiki-definition section and replace the href
    wiki_def_pattern = re.compile(
        r'(class="wiki-definition"[^>]*>.*?<p[^>]*>Wikipedia</p><p[^>]*>)(.*?)(</p>.*?Source:.*?href=")(https?://[^"]+)(")',
        re.DOTALL
    )

    match = wiki_def_pattern.search(content)
    if match:
        # Replace both definition text and URL
        new_content = (
            content[:match.start()] +
            match.group(1) +
            fix["definition"] +
            match.group(3) +
            fix["url"] +
            match.group(5) +
            content[match.end():]
        )
        content = new_content
    else:
        # Try simpler replacement - just the href
        old_urls = {
            "closing-costs-calculator": "https://caniuse.com",
            "cors-tester": "https://caniuse.com",
            "epub-to-pdf-converter": "https://caniuse.com",
            "ssh-key-generator": "https://caniuse.com",
            "take-home-pay-calculator": "https://stackoverflow.com/questions/tagged/tax-calculation",
            "timecard-calculator": "https://caniuse.com",
        }
        old_url = old_urls.get(tool_name, "")
        if old_url and old_url in content:
            # Replace just the URL in the Source link
            content = content.replace(
                f'href="{old_url}"',
                f'href="{fix["url"]}"',
                1  # Only first occurrence
            )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def fix_generic_slug(file_path, tool_name):
    """Fix overly generic Wikipedia slugs."""
    GENERIC_FIXES = {
        "age-calculator": {
            "old_url": "https://en.wikipedia.org/wiki/Age",
            "new_url": "https://en.wikipedia.org/wiki/Chronological_age",
            "definition": "Chronological age refers to the amount of time that has passed from birth to a given date. It is typically expressed in years, months, and days, and is used in medicine, law, and everyday life."
        },
    }

    if tool_name not in GENERIC_FIXES:
        return False

    fix = GENERIC_FIXES[tool_name]

    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    original = content

    # Replace the old URL with new URL
    content = content.replace(fix["old_url"], fix["new_url"])

    # Also fix the definition text if it's the generic Wikipedia one
    # Find the wiki-definition and replace its text
    wiki_def_pattern = re.compile(
        r'(class="wiki-definition"[^>]*>.*?<p[^>]*>Wikipedia</p><p[^>]*>)(.*?)(</p>)',
        re.DOTALL
    )

    match = wiki_def_pattern.search(content)
    if match:
        old_def = match.group(2)
        # Only replace if the definition is generic/bad
        if 'may refer to' in old_def.lower() or len(old_def.strip()) < 30:
            content = (
                content[:match.start(1)] +
                match.group(1) +
                fix["definition"] +
                match.group(3) +
                content[match.end():]
            )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    print("=" * 70)
    print("CYCLE 2: FIX BROKEN WIKIPEDIA REFERENCES")
    print("=" * 70)

    # Known affected tools for raw API dump
    api_dump_tools = [
        "base64-encoder", "base64-encoder-decoder", "cron-generator",
        "csv-to-json", "csv-to-json-converter", "diff-checker",
        "image-to-base64", "json-formatter", "json-path-finder",
        "json-viewer", "json-yaml-converter", "lorem-ipsum-generator",
        "markdown-editor", "markdown-to-html", "password-generator",
        "regex-tester", "regex-visualizer", "text-diff-checker",
        "text-generator", "timestamp-converter", "url-encoder",
        "url-encoder-decoder", "uuid-generator",
    ]

    non_wiki_tools = [
        "closing-costs-calculator", "cors-tester", "epub-to-pdf-converter",
        "ssh-key-generator", "take-home-pay-calculator", "timecard-calculator",
    ]

    generic_slug_tools = ["age-calculator"]

    fixed_count = 0

    # Fix 1: Raw API dump hrefs
    print("\n[1] Fixing raw Wikipedia API JSON dump in hrefs...")
    for tool_name in api_dump_tools:
        file_path = os.path.join(TOOLS_DIR, tool_name, "index.html")
        if os.path.isfile(file_path):
            if fix_raw_api_dump_hrefs(file_path):
                print(f"  FIXED: {tool_name}")
                fixed_count += 1
            else:
                print(f"  SKIP (no change needed): {tool_name}")
        else:
            print(f"  MISSING: {tool_name}")

    # Fix 2: Non-Wikipedia sources
    print("\n[2] Fixing non-Wikipedia sources in wiki-definitions...")
    for tool_name in non_wiki_tools:
        file_path = os.path.join(TOOLS_DIR, tool_name, "index.html")
        if os.path.isfile(file_path):
            if fix_non_wikipedia_sources(file_path, tool_name):
                print(f"  FIXED: {tool_name}")
                fixed_count += 1
            else:
                print(f"  SKIP (no change needed): {tool_name}")
        else:
            print(f"  MISSING: {tool_name}")

    # Fix 3: Generic slugs
    print("\n[3] Fixing overly generic Wikipedia slugs...")
    for tool_name in generic_slug_tools:
        file_path = os.path.join(TOOLS_DIR, tool_name, "index.html")
        if os.path.isfile(file_path):
            if fix_generic_slug(file_path, tool_name):
                print(f"  FIXED: {tool_name}")
                fixed_count += 1
            else:
                print(f"  SKIP (no change needed): {tool_name}")
        else:
            print(f"  MISSING: {tool_name}")

    print(f"\nTotal files fixed: {fixed_count}")
    return fixed_count


if __name__ == "__main__":
    main()
