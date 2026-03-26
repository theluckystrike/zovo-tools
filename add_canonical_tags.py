#!/usr/bin/env python3
"""
Fix Canonical URLs for all zovo-tools pages.
- Removes all existing canonical tags (including malformed double-href ones)
- Removes orphaned href="https://tools.zovo.one/..." fragments
- Adds a single correct canonical: https://zovo.one/free-tools/{tool-slug}/
"""

import os
import re
from pathlib import Path


def fix_canonical_tags():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Directories/files to skip (not tool directories)
    skip = {
        '.git', '.github', 'node_modules', '__pycache__', '.DS_Store',
        'cleanup', 'sitemap.xml', 'robots.txt', 'CNAME', '404.html',
        'index.html',  # root index
    }

    # Also skip any Python scripts and non-directory files at root level
    skip_extensions = {'.py', '.json', '.md', '.txt', '.xml', '.yml', '.yaml', '.sh', '.js'}

    fixed = 0
    added = 0
    already_correct = 0
    errors = 0

    for entry in sorted(base_dir.iterdir()):
        # Skip non-directories and known non-tool entries
        if not entry.is_dir():
            continue
        if entry.name in skip or entry.name.startswith('.'):
            continue

        index_path = entry / 'index.html'
        if not index_path.exists():
            continue

        tool_name = entry.name
        correct_canonical = f'https://zovo.one/free-tools/{tool_name}/'
        correct_tag = f'<link rel="canonical" href="{correct_canonical}">'

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Step 1: Remove ALL existing canonical link tags (any format, any domain)
            # This handles: <link rel="canonical" href="..."> and <link rel="canonical" href="..."/>
            content = re.sub(
                r'<link\s+rel="canonical"\s+href="[^"]*"\s*/?\s*>',
                '',
                content,
                flags=re.IGNORECASE
            )

            # Step 2: Remove orphaned href="https://tools.zovo.one/..." fragments
            # These appear as: > href="https://tools.zovo.one/some-tool/">
            # or just: href="https://tools.zovo.one/some-tool/">
            # They are remnants from malformed double-href canonical tags
            content = re.sub(
                r'\s*href="https://tools\.zovo\.one/[^"]*">\s*',
                '',
                content
            )

            # Step 3: Also remove any bare href fragments pointing to tools.zovo.one
            # that might appear as standalone attributes without a tag
            content = re.sub(
                r'\s*href="https://tools\.zovo\.one/[^"]*"\s*',
                ' ',
                content
            )

            # Step 4: Insert the correct canonical tag after <title>...</title>
            title_match = re.search(r'(</title>)', content, re.IGNORECASE)
            if title_match:
                insert_pos = title_match.end()
                content = content[:insert_pos] + '\n    ' + correct_tag + content[insert_pos:]
            else:
                # If no title tag, insert after <head> or <head ...>
                head_match = re.search(r'(<head[^>]*>)', content, re.IGNORECASE)
                if head_match:
                    insert_pos = head_match.end()
                    content = content[:insert_pos] + '\n    ' + correct_tag + content[insert_pos:]
                else:
                    print(f"  SKIP {tool_name}: No <title> or <head> found")
                    errors += 1
                    continue

            # Step 5: Clean up any double spaces or empty lines created by removal
            content = re.sub(r'  +', ' ', content)
            # But don't collapse spaces inside <pre> or <script> tags -
            # actually the above is too aggressive. Let's be more targeted:
            # Only clean up the specific artifacts
            # Revert the aggressive space cleanup
            content = original_content  # Reset and redo more carefully

            # Redo with more careful approach
            # Step 1: Remove ALL existing canonical link tags
            content = re.sub(
                r'\s*<link\s+rel="canonical"\s+href="[^"]*"\s*/?\s*>\s*',
                ' ',
                content,
                flags=re.IGNORECASE
            )

            # Step 2: Remove orphaned href="https://tools.zovo.one/..." fragments
            # Pattern: optional whitespace, href="https://tools.zovo.one/...", optional >
            content = re.sub(
                r'\s*href="https://tools\.zovo\.one/[^"]*">\s*',
                ' ',
                content
            )

            # Step 3: Insert correct canonical after </title>
            title_match = re.search(r'(</title>)', content, re.IGNORECASE)
            if title_match:
                insert_pos = title_match.end()
                content = content[:insert_pos] + ' ' + correct_tag + content[insert_pos:]
            else:
                head_match = re.search(r'(<head[^>]*>)', content, re.IGNORECASE)
                if head_match:
                    insert_pos = head_match.end()
                    content = content[:insert_pos] + '\n    ' + correct_tag + content[insert_pos:]
                else:
                    print(f"  SKIP {tool_name}: No <title> or <head> found")
                    errors += 1
                    continue

            if content != original_content:
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # Determine what changed
                had_canonical = 'rel="canonical"' in original_content
                had_tools_domain = 'tools.zovo.one' in original_content
                had_correct = f'href="{correct_canonical}"' in original_content

                if had_correct and not had_tools_domain:
                    already_correct += 1
                elif had_canonical:
                    fixed += 1
                else:
                    added += 1
            else:
                already_correct += 1

        except Exception as e:
            print(f"  ERROR {tool_name}: {e}")
            errors += 1

    print(f"\nCanonical Tag Fix Summary:")
    print(f"  Fixed (wrong domain/malformed): {fixed}")
    print(f"  Added (was missing):            {added}")
    print(f"  Already correct (refreshed):    {already_correct}")
    print(f"  Errors/skipped:                 {errors}")
    print(f"  Total processed:                {fixed + added + already_correct + errors}")


if __name__ == "__main__":
    fix_canonical_tags()
