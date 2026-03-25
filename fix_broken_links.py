#!/usr/bin/env python3
"""
Fix Broken Internal Links - Agent 2
Fixes broken internal links found in deep scan
"""

import os
import re
from pathlib import Path

def fix_broken_links():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")

    # Known broken links and their fixes
    broken_link_fixes = {
        '/free-tools/intelligent-image-generator/': '/free-tools/ai-image-generator/',
        '/free-tools/study-timer/': '/free-tools/pomodoro-timer/',
        '/free-tools/college-cost-calculator/': '/free-tools/college-calculator/',
        '/free-tools/scholarship-gpa-checker/': '/free-tools/gpa-calculator/',
        '/free-tools/ai-text-humanizer/': '/free-tools/text-humanizer/',
        '/free-tools/intelligent-logo-generator/': '/free-tools/ai-logo-generator/',
        '/free-tools/finance-tracker/': '/free-tools/budget-tracker/',
        '/free-tools/workout-timer/': '/free-tools/interval-timer/',
        '/free-tools/meal-planner/': '/free-tools/menu-planner/',
        '/free-tools/habit-builder/': '/free-tools/habit-tracker/',
        '/free-tools/study-guide-generator/': '/free-tools/study-planner/',
    }

    tools_to_fix = [
        'glassmorphism-generator',
        'gpa-calculator-pro',
        'gradient-text-generator',
        'hash-generator',
        'headline-analyzer',
        'heart-rate-zone-calculator',
        'heloc-calculator',
        'home-equity-calculator',
        'home-loan-calculator',
        'hour-calculator',
        'hourly-pay-calculator',
        'image-generator',
        'image-resizer',
        'invoice-generator'
    ]

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

            # Fix each broken link
            for broken_link, fixed_link in broken_link_fixes.items():
                if broken_link in content:
                    content = content.replace(broken_link, fixed_link)
                    print(f"✅ {tool_name}: Fixed {broken_link} → {fixed_link}")
                    fixes_made += 1

            # Write back if changed
            if content != original_content:
                with open(index_path, 'w', encoding='utf-8') as f:
                    f.write(content)

        except Exception as e:
            print(f"❌ Error fixing {tool_name}: {e}")

    print(f"\n🔧 Fixed {fixes_made} broken links")
    return fixes_made > 0

if __name__ == "__main__":
    fix_broken_links()