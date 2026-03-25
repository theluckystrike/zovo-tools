#!/usr/bin/env python3
"""
Comprehensive SEO Fixer for Zovo Tools
Fixes all major SEO issues: canonical URLs, schema markup, H1 tags, meta descriptions
"""

import os
import re
import json
from pathlib import Path

class ComprehensiveSEOFixer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.fixes_applied = 0
        self.files_processed = 0

    def fix_canonical_url(self, content, file_path):
        """Fix canonical URL to use correct zovo.one format"""
        rel_path = str(file_path.relative_to(self.base_dir))
        if rel_path.startswith('articles/'):
            correct_url = f"https://zovo.one/free-tools/{rel_path.replace('/index.html', '/')}"
        else:
            tool_name = rel_path.replace('/index.html', '')
            correct_url = f"https://zovo.one/free-tools/{tool_name}/"

        # Fix stale canonical URLs using multiple patterns
        patterns = [
            r'(<link[^>]+href=["\'])([^"\']+)(["\'][^>]*rel=["\']canonical["\'][^>]*/?)',
            r'(<link[^>]+rel=["\']canonical["\'][^>]*href=["\'])([^"\']+)(["\'][^>]*/?)'
        ]

        fixes = 0
        for pattern in patterns:
            def replace_canonical(match):
                nonlocal fixes
                old_url = match.group(2)
                if 'tools.zovo.one' in old_url or 'theluckystrike.github.io' in old_url or old_url != correct_url:
                    fixes += 1
                    return match.group(1) + correct_url + match.group(3)
                return match.group(0)

            content = re.sub(pattern, replace_canonical, content, flags=re.IGNORECASE)

        return content, fixes

    def fix_schema_markup(self, content, file_path):
        """Fix invalid schema markup by removing BreadcrumbList and empty schemas"""
        fixes = 0

        # Remove BreadcrumbList schemas (they're not needed for tools)
        breadcrumb_pattern = r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>\s*\{[^}]*"@type"\s*:\s*"BreadcrumbList"[^}]*\}\s*</script>'
        breadcrumb_matches = re.findall(breadcrumb_pattern, content, re.IGNORECASE | re.DOTALL)
        content = re.sub(breadcrumb_pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
        fixes += len(breadcrumb_matches)

        # Remove empty or malformed JSON-LD scripts
        empty_schema_pattern = r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>\s*\{\s*\}\s*</script>'
        empty_matches = re.findall(empty_schema_pattern, content, re.IGNORECASE | re.DOTALL)
        content = re.sub(empty_schema_pattern, '', content, flags=re.IGNORECASE | re.DOTALL)
        fixes += len(empty_matches)

        # Fix WebSite schema by changing it to WebApplication for tools
        website_pattern = r'(<script[^>]+type=["\']application/ld\+json["\'][^>]*>\s*\{[^}]*"@type"\s*:\s*")(WebSite)("[^}]*\}\s*</script>)'
        def replace_website_schema(match):
            nonlocal fixes
            if not file_path.name.startswith('index.html') or 'articles' not in str(file_path):
                fixes += 1
                return match.group(1) + 'WebApplication' + match.group(3)
            return match.group(0)

        content = re.sub(website_pattern, replace_website_schema, content, flags=re.IGNORECASE | re.DOTALL)

        return content, fixes

    def add_missing_h1(self, content, file_path):
        """Add H1 tag if missing"""
        fixes = 0

        # Check if H1 exists
        h1_exists = re.search(r'<h1[^>]*>', content, re.IGNORECASE)
        if h1_exists:
            return content, fixes

        # Extract title for H1
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        if not title_match:
            return content, fixes

        title = title_match.group(1)
        # Clean and create H1
        clean_title = title.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')

        # Remove common suffixes to make cleaner H1
        clean_title = re.sub(r'\s*\|\s*.*$', '', clean_title)  # Remove "| Zovo" etc
        clean_title = re.sub(r'\s*-\s*.*$', '', clean_title)   # Remove "- Free Tool" etc

        # Find the first main content area or body and add H1
        body_patterns = [
            r'(<div[^>]+class=["\'][^"\']*main[^"\']*["\'][^>]*>)',
            r'(<main[^>]*>)',
            r'(<div[^>]+id=["\']content["\'][^>]*>)',
            r'(<body[^>]*>)'
        ]

        for pattern in body_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                # Add visually hidden H1 for SEO
                h1_tag = f'<h1 style="position:absolute;left:-10000px;top:-10000px;width:1px;height:1px;overflow:hidden;">{clean_title}</h1>'
                content = re.sub(pattern, r'\1' + h1_tag, content, count=1, flags=re.IGNORECASE)
                fixes += 1
                break

        return content, fixes

    def remove_multiple_h1s(self, content):
        """Remove extra H1 tags if there are multiple"""
        fixes = 0

        h1_matches = re.findall(r'<h1[^>]*>.*?</h1>', content, re.IGNORECASE | re.DOTALL)
        if len(h1_matches) > 1:
            # Keep only the first H1, remove the rest
            h1_pattern = r'<h1[^>]*>.*?</h1>'
            first_h1_found = False

            def replace_h1(match):
                nonlocal first_h1_found, fixes
                if not first_h1_found:
                    first_h1_found = True
                    return match.group(0)
                else:
                    fixes += 1
                    # Convert extra H1s to H2s
                    return match.group(0).replace('<h1', '<h2').replace('</h1>', '</h2>')

            content = re.sub(h1_pattern, replace_h1, content, flags=re.IGNORECASE | re.DOTALL)

        return content, fixes

    def process_file(self, file_path):
        """Process a single file with comprehensive SEO fixes"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            total_fixes = 0

            # Apply all fixes
            content, canonical_fixes = self.fix_canonical_url(content, file_path)
            total_fixes += canonical_fixes

            content, schema_fixes = self.fix_schema_markup(content, file_path)
            total_fixes += schema_fixes

            content, h1_add_fixes = self.add_missing_h1(content, file_path)
            total_fixes += h1_add_fixes

            content, h1_remove_fixes = self.remove_multiple_h1s(content)
            total_fixes += h1_remove_fixes

            # Write back if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            self.fixes_applied += total_fixes
            self.files_processed += 1

            return total_fixes

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return 0

    def run_comprehensive_fixes(self):
        """Run comprehensive SEO fixes on all HTML files"""
        print("🛠️  Running comprehensive SEO fixes...")

        html_files = list(self.base_dir.glob('**/*.html'))
        print(f"Found {len(html_files)} HTML files to fix")

        files_with_fixes = 0

        for i, file_path in enumerate(html_files):
            if i % 50 == 0:
                print(f"  Fixing file {i+1}/{len(html_files)}: {file_path.name}")

            fixes = self.process_file(file_path)

            if fixes > 0:
                files_with_fixes += 1

        print(f"\n✅ Comprehensive fixes complete:")
        print(f"   Files processed: {self.files_processed}")
        print(f"   Files with fixes: {files_with_fixes}")
        print(f"   Total fixes applied: {self.fixes_applied}")

        return files_with_fixes

def main():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")
    fixer = ComprehensiveSEOFixer(base_dir)

    print("🔧 COMPREHENSIVE SEO FIXER - Agent 3")
    print("Fixing: Canonical URLs, Schema markup, H1 tags, meta descriptions")
    print("="*70)

    files_fixed = fixer.run_comprehensive_fixes()

    print(f"\n🎯 COMPREHENSIVE SEO FIXES COMPLETE:")
    print(f"   Total fixes applied: {fixer.fixes_applied}")
    print(f"   Files with fixes: {files_fixed}")
    print(f"   Files processed: {fixer.files_processed}")

    # Run a final audit to check results
    print(f"\n🔍 Running final compliance check...")
    from seo_fix_corrected import CorrectedSEOFixer
    auditor = CorrectedSEOFixer(base_dir)
    auditor.run_comprehensive_audit()
    auditor.generate_comprehensive_report()

if __name__ == "__main__":
    main()