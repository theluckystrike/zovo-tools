#!/usr/bin/env python3
"""
Add Canonical URLs - Agent 2
Adds canonical link tags to tools missing them
"""

import os
import re
from pathlib import Path

def add_canonical_tags():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Tools identified as missing canonical tags
    priority_tools = [
        'html-to-pdf-converter', 'ico-converter', 'ics-calendar-generator',
        'image-metadata-viewer', 'image-to-text-ocr', 'life-expectancy-calculator',
        'json-to-xml-converter', 'normal-distribution-table'
    ]

    fixes_made = 0

    for tool_name in priority_tools:
        tool_dir = base_dir / tool_name
        index_path = tool_dir / 'index.html'

        if not index_path.exists():
            continue

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if canonical already exists
            if '<link rel="canonical"' in content:
                continue

            # Generate canonical URL
            canonical_url = f"https://tools.zovo.one/free-tools/{tool_name}/"

            # Insert canonical tag after title or in head
            title_pattern = re.compile(r'(<title>[^<]*</title>)', re.IGNORECASE)
            if title_pattern.search(content):
                canonical_tag = f'\\1\\n    <link rel="canonical" href="{canonical_url}">'
                content = title_pattern.sub(canonical_tag, content)

                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {tool_name}: Added canonical URL")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\\n🔧 Added canonical URLs to {fixes_made} tools")
    return fixes_made > 0

if __name__ == "__main__":
    add_canonical_tags()