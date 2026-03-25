#!/usr/bin/env python3
"""
Add Google Analytics - Agent 2
Adds Google Analytics GA4 tracking to high-priority G-N tools
"""

import os
import re
from pathlib import Path

def add_google_analytics():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # High-priority G-N tools for analytics
    priority_tools = [
        'gpa-calculator', 'grade-calculator', 'gradient-generator',
        'hash-generator', 'html-formatter', 'image-resizer', 'image-converter',
        'json-formatter', 'json-viewer', 'loan-calculator', 'mortgage-calculator',
        'markdown-editor', 'meme-generator', 'net-worth-calculator'
    ]

    # Google Analytics GA4 tracking code
    ga_code = '''
<!-- Google Analytics GA4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXX');
</script>'''

    fixes_made = 0

    for tool_name in priority_tools[:10]:  # Process 10 high-priority tools
        tool_dir = base_dir / tool_name
        index_path = tool_dir / 'index.html'

        if not index_path.exists():
            continue

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if GA already exists
            if 'gtag(' in content or 'google-analytics' in content or 'googletagmanager' in content:
                continue

            # Insert GA code before closing head tag
            head_close_pattern = re.compile(r'(</head>)', re.IGNORECASE)
            if head_close_pattern.search(content):
                content = head_close_pattern.sub(ga_code + r'\\n\\1', content)

                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ {tool_name}: Added Google Analytics tracking")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\\n🔧 Added Google Analytics to {fixes_made} high-priority tools")
    return fixes_made > 0

if __name__ == "__main__":
    add_google_analytics()