#!/usr/bin/env python3
"""
Fix Canonical URLs for all zovo-tools pages.
- Removes all existing <link rel="canonical" ...> tags
- Removes orphaned ' href="https://tools.zovo.one/...">' fragments
  (left over from malformed double-href canonical tags)
- Adds a single correct canonical: https://zovo.one/free-tools/{tool-slug}/
  inserted after the FIRST </title> tag only
"""

import os
import re
from pathlib import Path


def fix_canonical_tags():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Skip known non-tool entries at root level
    skip_names = {
        '.git', '.github', 'node_modules', '__pycache__', '.DS_Store',
        'cleanup', 'sitemap.xml', 'robots.txt', 'CNAME', '404.html',
    }

    fixed = 0
    added = 0
    already_correct = 0
    errors = 0

    for entry in sorted(base_dir.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name in skip_names or entry.name.startswith('.'):
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

            # Check current state before changes
            had_any_canonical = bool(re.search(r'<link\s+rel="canonical"', content, re.IGNORECASE))
            had_correct_canonical = correct_tag in content
            had_tools_domain = 'tools.zovo.one' in content

            # Step 1: Remove ALL existing <link rel="canonical" ...> tags
            # Handles both self-closing (/>) and normal (>) variants
            content = re.sub(
                r'\s*<link\s+rel="canonical"\s+href="[^"]*"\s*/?\s*>',
                '',
                content,
                flags=re.IGNORECASE
            )

            # Step 2: Remove orphaned href="https://tools.zovo.one/..."
            # These are bare href attributes NOT inside any <a> or <link> tag,
            # left from malformed double-href canonical tags.
            # Pattern: ' href="https://tools.zovo.one/.../">' appearing after />
            content = re.sub(
                r'(?<=/\>)\s*href="https://tools\.zovo\.one/[^"]*/?"\s*>',
                '',
                content
            )
            # Also catch the variant without the preceding />
            content = re.sub(
                r'(?<=robots"/>)\s*href="https://tools\.zovo\.one/[^"]*/?"\s*>',
                '',
                content
            )

            # Step 3: Insert the correct canonical tag after the FIRST </title> only
            title_match = re.search(r'(</title>)', content, re.IGNORECASE)
            if title_match:
                insert_pos = title_match.end()
                if '\n' in content[:200]:
                    separator = '\n    '
                else:
                    separator = ' '
                content = content[:insert_pos] + separator + correct_tag + content[insert_pos:]
            else:
                head_match = re.search(r'(<head[^>]*>)', content, re.IGNORECASE)
                if head_match:
                    insert_pos = head_match.end()
                    content = content[:insert_pos] + '\n    ' + correct_tag + content[insert_pos:]
                else:
                    print(f"  SKIP {tool_name}: No <title> or <head> tag found")
                    errors += 1
                    continue

            # Write if changed
            if content != original_content:
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                if had_correct_canonical and not had_tools_domain:
                    already_correct += 1
                elif had_any_canonical:
                    fixed += 1
                else:
                    added += 1
            else:
                already_correct += 1

        except Exception as e:
            print(f"  ERROR {tool_name}: {e}")
            errors += 1

    total = fixed + added + already_correct + errors
    print(f"\nCanonical Tag Fix Summary:")
    print(f"  Fixed (wrong domain/malformed): {fixed}")
    print(f"  Added (was missing):            {added}")
    print(f"  Refreshed (were correct):       {already_correct}")
    print(f"  Errors/skipped:                 {errors}")
    print(f"  Total processed:                {total}")


if __name__ == "__main__":
    fix_canonical_tags()
