#!/usr/bin/env python3
"""
Targeted SEO Fixes for Zovo Tools
Handles minified HTML and focuses on critical SEO elements
"""

import os
import re
import json
from pathlib import Path

class TargetedSEOFixer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.fixes_applied = 0
        self.files_processed = 0

    def fix_canonical_urls(self, content, file_path):
        """Fix canonical URLs using regex"""
        fixes = 0

        # Get correct canonical URL
        rel_path = str(file_path.relative_to(self.base_dir))
        if rel_path.startswith('articles/'):
            correct_url = f"https://zovo.one/free-tools/{rel_path.replace('/index.html', '/')}"
        else:
            tool_name = rel_path.replace('/index.html', '')
            correct_url = f"https://zovo.one/free-tools/{tool_name}/"

        # Fix stale canonical URLs
        canonical_pattern = r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\'][^>]*/?>'

        def replace_canonical(match):
            full_match = match.group(0)
            old_url = match.group(1)

            if 'tools.zovo.one' in old_url or 'theluckystrike.github.io' in old_url:
                nonlocal fixes
                fixes += 1
                return full_match.replace(old_url, correct_url)
            return full_match

        content = re.sub(canonical_pattern, replace_canonical, content, flags=re.IGNORECASE)

        # Add canonical if missing (check if <head> exists and no canonical)
        if '<head>' in content and 'rel="canonical"' not in content and 'rel=\'canonical\'' not in content:
            head_end = content.find('</head>')
            if head_end > -1:
                canonical_tag = f'<link rel="canonical" href="{correct_url}"/>'
                content = content[:head_end] + canonical_tag + content[head_end:]
                fixes += 1

        return content, fixes

    def fix_og_urls(self, content, file_path):
        """Fix OG URLs using regex"""
        fixes = 0

        # Get correct URL
        rel_path = str(file_path.relative_to(self.base_dir))
        if rel_path.startswith('articles/'):
            correct_url = f"https://zovo.one/free-tools/{rel_path.replace('/index.html', '/')}"
        else:
            tool_name = rel_path.replace('/index.html', '')
            correct_url = f"https://zovo.one/free-tools/{tool_name}/"

        # Fix stale OG URLs
        og_url_pattern = r'<meta[^>]+property=["\']og:url["\'][^>]*content=["\']([^"\']+)["\'][^>]*/?>'

        def replace_og_url(match):
            full_match = match.group(0)
            old_url = match.group(1)

            if 'tools.zovo.one' in old_url or 'theluckystrike.github.io' in old_url:
                nonlocal fixes
                fixes += 1
                return full_match.replace(old_url, correct_url)
            return full_match

        content = re.sub(og_url_pattern, replace_og_url, content, flags=re.IGNORECASE)

        # Add basic OG tags if missing
        head_pattern = r'<head[^>]*>'
        if re.search(head_pattern, content):
            # Check for missing og:url
            if 'property="og:url"' not in content and 'property=\'og:url\'' not in content:
                head_end = content.find('</head>')
                if head_end > -1:
                    og_tag = f'<meta property="og:url" content="{correct_url}"/>'
                    content = content[:head_end] + og_tag + content[head_end:]
                    fixes += 1

            # Check for missing og:site_name
            if 'property="og:site_name"' not in content and 'property=\'og:site_name\'' not in content:
                head_end = content.find('</head>')
                if head_end > -1:
                    og_tag = f'<meta property="og:site_name" content="Zovo"/>'
                    content = content[:head_end] + og_tag + content[head_end:]
                    fixes += 1

        return content, fixes

    def fix_stale_urls_in_content(self, content):
        """Fix all stale URLs in content"""
        fixes = 0
        original = content

        # Replace stale URLs
        content = content.replace('tools.zovo.one', 'zovo.one/free-tools')
        content = content.replace('theluckystrike.github.io/zovo-tools', 'zovo.one/free-tools')

        if content != original:
            # Count the number of replacements
            fixes += original.count('tools.zovo.one')
            fixes += original.count('theluckystrike.github.io/zovo-tools')

        return content, fixes

    def add_schema_if_missing(self, content, file_path):
        """Add basic schema markup if completely missing"""
        fixes = 0

        # Check if there's already any schema
        if 'application/ld+json' in content:
            return content, fixes

        # Get page info from title and meta description
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)

        title = title_match.group(1) if title_match else 'Zovo Tool'
        description = desc_match.group(1) if desc_match else 'Free online tool'

        # Clean HTML entities
        title = title.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
        description = description.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')

        # Determine URL and schema type
        rel_path = str(file_path.relative_to(self.base_dir))
        if rel_path.startswith('articles/'):
            correct_url = f"https://zovo.one/free-tools/{rel_path.replace('/index.html', '/')}"
            schema_type = 'Article'
        else:
            tool_name = rel_path.replace('/index.html', '')
            correct_url = f"https://zovo.one/free-tools/{tool_name}/"
            schema_type = 'WebApplication'

        # Create minimal schema
        if schema_type == 'Article':
            schema_data = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": title,
                "author": {"@type": "Person", "name": "Michael Lip"},
                "publisher": {"@type": "Organization", "name": "Zovo Tools"},
                "url": correct_url,
                "description": description
            }
        else:
            schema_data = {
                "@context": "https://schema.org",
                "@type": "WebApplication",
                "name": title,
                "description": description,
                "url": correct_url,
                "applicationCategory": "Utility"
            }

        schema_json = json.dumps(schema_data, separators=(',', ':'))
        schema_tag = f'<script type="application/ld+json">{schema_json}</script>'

        # Insert before </head>
        head_end = content.find('</head>')
        if head_end > -1:
            content = content[:head_end] + schema_tag + content[head_end:]
            fixes += 1

        return content, fixes

    def process_file(self, file_path):
        """Process a single file with all SEO fixes"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            total_fixes = 0

            # Apply all fixes
            content, canonical_fixes = self.fix_canonical_urls(content, file_path)
            total_fixes += canonical_fixes

            content, og_fixes = self.fix_og_urls(content, file_path)
            total_fixes += og_fixes

            content, url_fixes = self.fix_stale_urls_in_content(content)
            total_fixes += url_fixes

            content, schema_fixes = self.add_schema_if_missing(content, file_path)
            total_fixes += schema_fixes

            # Write back if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            self.fixes_applied += total_fixes
            return total_fixes

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return 0

    def run_targeted_fixes(self):
        """Run targeted SEO fixes on all HTML files"""
        print("🎯 Running targeted SEO fixes...")

        html_files = list(self.base_dir.glob('**/*.html'))
        print(f"Found {len(html_files)} HTML files to process")

        files_with_fixes = 0

        for i, file_path in enumerate(html_files):
            if i % 50 == 0:
                print(f"  Processing file {i+1}/{len(html_files)}: {file_path.name}")

            fixes = self.process_file(file_path)
            self.files_processed += 1

            if fixes > 0:
                files_with_fixes += 1

        print(f"\n✅ Processing complete:")
        print(f"   Files processed: {self.files_processed}")
        print(f"   Files with fixes: {files_with_fixes}")
        print(f"   Total fixes applied: {self.fixes_applied}")

def main():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")
    fixer = TargetedSEOFixer(base_dir)

    print("🚀 TARGETED SEO FIXER - Agent 3")
    print("Focus: Critical SEO elements (canonical, OG, stale URLs, schema)")
    print("="*70)

    fixer.run_targeted_fixes()

    print(f"\n🎯 TARGETED FIXES COMPLETE:")
    print(f"   Total fixes applied: {fixer.fixes_applied}")
    print(f"   Files processed: {fixer.files_processed}")

if __name__ == "__main__":
    main()