#!/usr/bin/env python3
"""
Fix Critical Quality Issues
Target the most impactful fixes for immediate quality improvements
"""

import os
import re
from pathlib import Path

def fix_canonical_urls():
    """Add missing canonical URLs"""
    base_path = Path("/Users/mike/zovo-workspaces/zovo-tools")
    fixed_count = 0

    print("Fixing missing canonical URLs...")

    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name != 'articles':
            index_file = item / 'index.html'
            if index_file.exists():
                try:
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Check if canonical URL exists
                    if 'rel="canonical"' not in content and 'rel=\'canonical\'' not in content:
                        # Add canonical URL after existing meta tags
                        canonical_url = f"https://tools.zovo.one/{item.name}/"
                        canonical_tag = f'<link rel="canonical" href="{canonical_url}">'

                        # Find position to insert (after last meta tag or in head)
                        if '</head>' in content:
                            content = content.replace('</head>', f'    {canonical_tag}\n</head>')
                            fixed_count += 1

                            with open(index_file, 'w', encoding='utf-8') as f:
                                f.write(content)

                except Exception as e:
                    print(f"Error fixing {item.name}: {e}")
                    continue

    print(f"Fixed canonical URLs for {fixed_count} pages")
    return fixed_count

def fix_em_dashes():
    """Replace em-dashes with proper alternatives"""
    base_path = Path("/Users/mike/zovo-workspaces/zovo-tools")
    fixed_count = 0

    print("Fixing em-dashes...")

    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name != 'articles':
            index_file = item / 'index.html'
            if index_file.exists():
                try:
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if '—' in content:
                        # Replace em-dashes with appropriate alternatives
                        original_content = content
                        content = content.replace(' — ', ' - ')  # Simple dash
                        content = content.replace('—', '-')      # All remaining em-dashes

                        if content != original_content:
                            fixed_count += 1
                            with open(index_file, 'w', encoding='utf-8') as f:
                                f.write(content)

                except Exception as e:
                    print(f"Error fixing em-dashes in {item.name}: {e}")
                    continue

    print(f"Fixed em-dashes in {fixed_count} pages")
    return fixed_count

def remove_ai_mentions():
    """Remove or replace problematic AI mentions"""
    base_path = Path("/Users/mike/zovo-workspaces/zovo-tools")
    fixed_count = 0

    print("Fixing AI mentions...")

    ai_replacements = {
        r'\bAI\b': 'intelligent',
        r'\bartificial intelligence\b': 'smart technology',
        r'\bmachine learning\b': 'advanced algorithms',
        r'\bClaude\b': 'advanced system',
        r'\bGPT\b': 'language model',
        r'\bChatGPT\b': 'chat system'
    }

    for item in base_path.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name != 'articles':
            index_file = item / 'index.html'
            if index_file.exists():
                try:
                    with open(index_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    original_content = content

                    # Apply replacements
                    for pattern, replacement in ai_replacements.items():
                        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)

                    if content != original_content:
                        fixed_count += 1
                        with open(index_file, 'w', encoding='utf-8') as f:
                            f.write(content)

                except Exception as e:
                    print(f"Error fixing AI mentions in {item.name}: {e}")
                    continue

    print(f"Fixed AI mentions in {fixed_count} pages")
    return fixed_count

def main():
    print("ZOVO ECOSYSTEM CRITICAL FIXES")
    print("="*40)

    total_fixes = 0

    # Fix canonical URLs
    total_fixes += fix_canonical_urls()

    # Fix em-dashes
    total_fixes += fix_em_dashes()

    # Fix AI mentions (selective fixes)
    total_fixes += remove_ai_mentions()

    print(f"\nTotal fixes applied: {total_fixes}")
    print("Critical quality issues addressed!")

if __name__ == "__main__":
    main()