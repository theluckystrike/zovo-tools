#!/usr/bin/env python3
"""Fix table-generator and text-generator broken schema blocks (empty key names)."""
import re

pages = [
    '/Users/mike/zovo-workspaces/zovo-tools/table-generator/index.html',
    '/Users/mike/zovo-workspaces/zovo-tools/text-generator/index.html',
]

for path in pages:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all ld+json blocks
    pattern = r'<script\s+type=["\']application/ld\+json["\']>\s*(.*?)\s*</script>'
    matches = list(re.finditer(pattern, content, re.DOTALL | re.IGNORECASE))

    # The first block has empty string keys - remove it
    if matches:
        first_match = matches[0]
        json_content = first_match.group(1)
        # Verify it's the broken one (has empty string keys)
        if '"": "https://schema.org"' in json_content or '"": "WebApplication"' in json_content:
            content = content.replace(first_match.group(0), '', 1)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {path} (removed broken schema block with empty keys)")
        else:
            print(f"Skipped: {path} (first block doesn't match expected pattern)")
    else:
        print(f"Skipped: {path} (no ld+json blocks found)")
