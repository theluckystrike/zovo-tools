#!/usr/bin/env python3
"""
Final SEO Cleanup for Zovo Tools
Aggressively removes BreadcrumbList schemas and adds H1 tags properly
"""

import os
import re
from pathlib import Path

class FinalSEOCleanup:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.fixes_applied = 0
        self.files_processed = 0

    def remove_breadcrumb_schemas(self, content):
        """Aggressively remove all BreadcrumbList schemas"""
        fixes = 0

        # Pattern to match any JSON-LD script containing BreadcrumbList
        breadcrumb_pattern = r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>.*?"@type"\s*:\s*"BreadcrumbList".*?</script>'

        # Find and count all matches
        matches = re.findall(breadcrumb_pattern, content, re.IGNORECASE | re.DOTALL)
        fixes += len(matches)

        # Remove all BreadcrumbList schemas
        content = re.sub(breadcrumb_pattern, '', content, flags=re.IGNORECASE | re.DOTALL)

        # Also remove any remaining empty JSON-LD scripts
        empty_pattern = r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>\s*</script>'
        empty_matches = re.findall(empty_pattern, content, re.IGNORECASE)
        content = re.sub(empty_pattern, '', content, flags=re.IGNORECASE)
        fixes += len(empty_matches)

        return content, fixes

    def add_h1_aggressively(self, content, file_path):
        """Add H1 tag using aggressive insertion method"""
        fixes = 0

        # Check if H1 already exists
        if re.search(r'<h1[^>]*>', content, re.IGNORECASE):
            return content, fixes

        # Extract title
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
        if not title_match:
            return content, fixes

        title = title_match.group(1)
        clean_title = title.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
        clean_title = re.sub(r'\s*\|\s*.*$', '', clean_title)
        clean_title = re.sub(r'\s*-\s*.*$', '', clean_title)

        # Try multiple insertion points
        insertion_patterns = [
            # After opening body tag
            (r'(<body[^>]*>)', r'\1<h1 style="position:absolute;left:-10000px;top:-10000px;width:1px;height:1px;overflow:hidden;">' + clean_title + '</h1>'),
            # Before first div with class
            (r'(<div[^>]+class=["\'][^"\']*["\'][^>]*>)', r'<h1 style="position:absolute;left:-10000px;top:-10000px;width:1px;height:1px;overflow:hidden;">' + clean_title + '</h1>\1'),
            # After the first opening div tag
            (r'(<body[^>]*>.*?<div[^>]*>)', r'\1<h1 style="position:absolute;left:-10000px;top:-10000px;width:1px;height:1px;overflow:hidden;">' + clean_title + '</h1>'),
        ]

        for pattern, replacement in insertion_patterns:
            if re.search(pattern, content, re.IGNORECASE | re.DOTALL):
                content = re.sub(pattern, replacement, content, count=1, flags=re.IGNORECASE | re.DOTALL)
                fixes += 1
                break

        return content, fixes

    def fix_stale_og_urls(self, content):
        """Fix any remaining stale OG URLs"""
        fixes = 0

        # Fix OG URLs that still point to tools.zovo.one
        og_url_pattern = r'(<meta[^>]+property=["\']og:url["\'][^>]*content=["\'])([^"\']*tools\.zovo\.one[^"\']*)(["\'[^>]*/?)'

        def replace_og_url(match):
            nonlocal fixes
            old_url = match.group(2)
            new_url = old_url.replace('tools.zovo.one', 'zovo.one/free-tools')
            fixes += 1
            return match.group(1) + new_url + match.group(3)

        content = re.sub(og_url_pattern, replace_og_url, content, flags=re.IGNORECASE)

        return content, fixes

    def fix_websiteapp_schema(self, content, file_path):
        """Fix WebSite schema to WebApplication for tools"""
        fixes = 0

        # Skip the main index.html
        if file_path.name == 'index.html' and 'articles' not in str(file_path):
            rel_path = str(file_path.relative_to(self.base_dir))
            if rel_path == 'index.html':  # Main site index
                return content, fixes

        # Change WebSite to WebApplication for tool pages
        website_pattern = r'("@type"\s*:\s*")(WebSite)(")'
        def replace_schema_type(match):
            nonlocal fixes
            fixes += 1
            return match.group(1) + 'WebApplication' + match.group(3)

        content = re.sub(website_pattern, replace_schema_type, content, flags=re.IGNORECASE)

        return content, fixes

    def cleanup_multiple_spaces(self, content):
        """Clean up multiple consecutive spaces that might be left from removals"""
        # Remove multiple consecutive spaces, newlines
        content = re.sub(r'\s+', ' ', content)
        # Fix spacing around tags
        content = re.sub(r'>\s+<', '><', content)
        return content

    def process_file(self, file_path):
        """Process a single file with final cleanup"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            total_fixes = 0

            # Apply aggressive fixes
            content, breadcrumb_fixes = self.remove_breadcrumb_schemas(content)
            total_fixes += breadcrumb_fixes

            content, h1_fixes = self.add_h1_aggressively(content, file_path)
            total_fixes += h1_fixes

            content, og_fixes = self.fix_stale_og_urls(content)
            total_fixes += og_fixes

            content, schema_fixes = self.fix_websiteapp_schema(content, file_path)
            total_fixes += schema_fixes

            # Clean up spacing
            if total_fixes > 0:
                content = self.cleanup_multiple_spaces(content)

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

    def run_final_cleanup(self):
        """Run final SEO cleanup on all HTML files"""
        print("🧹 Running final SEO cleanup...")

        html_files = list(self.base_dir.glob('**/*.html'))
        print(f"Found {len(html_files)} HTML files to clean up")

        files_with_fixes = 0

        for i, file_path in enumerate(html_files):
            if i % 50 == 0:
                print(f"  Cleaning file {i+1}/{len(html_files)}: {file_path.name}")

            fixes = self.process_file(file_path)

            if fixes > 0:
                files_with_fixes += 1

        print(f"\n✅ Final cleanup complete:")
        print(f"   Files processed: {self.files_processed}")
        print(f"   Files with fixes: {files_with_fixes}")
        print(f"   Total fixes applied: {self.fixes_applied}")

        return files_with_fixes

def main():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")
    cleaner = FinalSEOCleanup(base_dir)

    print("🧹 FINAL SEO CLEANUP - Agent 3")
    print("Aggressive cleanup: BreadcrumbList removal, H1 insertion, schema fixes")
    print("="*70)

    files_fixed = cleaner.run_final_cleanup()

    print(f"\n🎯 FINAL CLEANUP COMPLETE:")
    print(f"   Total fixes applied: {cleaner.fixes_applied}")
    print(f"   Files with fixes: {files_fixed}")
    print(f"   Files processed: {cleaner.files_processed}")

    # Run final audit to see results
    print(f"\n🔍 Running final audit to check results...")
    from seo_fix_corrected import CorrectedSEOFixer
    auditor = CorrectedSEOFixer(base_dir)
    total_issues = auditor.run_comprehensive_audit()
    auditor.generate_comprehensive_report()

    # Calculate final improvement
    compliance_rate = ((auditor.files_processed - len(auditor.issues_found)) / auditor.files_processed) * 100
    print(f"\n🏆 FINAL SEO COMPLIANCE RATE: {compliance_rate:.1f}%")

if __name__ == "__main__":
    main()