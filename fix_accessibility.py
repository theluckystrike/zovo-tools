#!/usr/bin/env python3
"""
Fix Accessibility Issues - Agent 2
Fixes accessibility violations found in deep scan
"""

import os
import re
from pathlib import Path

def fix_accessibility_issues():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Tools with accessibility issues
    tools_to_fix = ['gif-builder', 'image-resizer']

    fixes_made = 0

    for tool_name in tools_to_fix:
        tool_dir = base_dir / tool_name
        index_path = tool_dir / 'index.html'

        if not index_path.exists():
            print(f"⚠️ {tool_name}: index.html not found")
            continue

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Fix images without alt text
            img_pattern = re.compile(r'<img([^>]*?)(?:\s+alt=["\'][^"\']*["\'])?([^>]*?)>', re.IGNORECASE)

            def fix_img_alt(match):
                before_alt = match.group(1)
                after_alt = match.group(2)

                # If already has alt, don't change
                if 'alt=' in before_alt.lower() or 'alt=' in after_alt.lower():
                    return match.group(0)

                # Add generic alt text
                return f'<img{before_alt} alt="Tool interface"{after_alt}>'

            new_content = img_pattern.sub(fix_img_alt, content)

            if new_content != original_content:
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✅ {tool_name}: Added alt text to images")
                fixes_made += 1

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\n🔧 Fixed accessibility issues in {fixes_made} tools")
    return fixes_made > 0

if __name__ == "__main__":
    fix_accessibility_issues()