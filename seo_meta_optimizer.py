#!/usr/bin/env python3
"""
Meta Description and H1 Tag Optimizer for Zovo Tools
Focuses on optimizing meta descriptions and H1 tags for better SEO
"""

import os
import re
import json
from pathlib import Path

class MetaOptimizer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.fixes_applied = 0
        self.files_processed = 0
        self.issues_found = []

    def analyze_meta_description(self, content):
        """Analyze meta description for length and quality issues"""
        desc_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)

        if not desc_match:
            return "missing", None, 0

        description = desc_match.group(1)
        # Clean HTML entities
        clean_desc = description.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')
        length = len(clean_desc)

        if length > 160:
            return "too_long", clean_desc, length
        elif length < 120:
            return "too_short", clean_desc, length
        else:
            return "good", clean_desc, length

    def analyze_h1_tags(self, content):
        """Analyze H1 tags for SEO compliance"""
        h1_matches = re.findall(r'<h1[^>]*>([^<]+)</h1>', content, re.IGNORECASE)

        if not h1_matches:
            return "missing", []
        elif len(h1_matches) > 1:
            return "multiple", h1_matches
        else:
            return "good", h1_matches

    def optimize_meta_description(self, content, file_path):
        """Optimize meta description length"""
        fixes = 0
        desc_status, description, length = self.analyze_meta_description(content)

        if desc_status == "too_long" and length > 160:
            # Truncate to 157 characters and add "..."
            optimized_desc = description[:157] + "..."

            # Replace in content
            pattern = r'(<meta[^>]+name=["\']description["\'][^>]*content=["\'])([^"\']+)(["\'][^>]*/?>'

            def replace_desc(match):
                nonlocal fixes
                fixes += 1
                return match.group(1) + optimized_desc + match.group(3)

            content = re.sub(pattern, replace_desc, content, flags=re.IGNORECASE)

        return content, fixes

    def add_missing_h1(self, content, file_path):
        """Add H1 tag if missing"""
        fixes = 0
        h1_status, h1_tags = self.analyze_h1_tags(content)

        if h1_status == "missing":
            # Extract title for H1
            title_match = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
            if title_match:
                title = title_match.group(1)
                # Clean and create H1
                clean_title = title.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"')

                # Remove common suffixes to make cleaner H1
                clean_title = re.sub(r'\s*\|\s*.*$', '', clean_title)  # Remove "| Zovo" etc
                clean_title = re.sub(r'\s*-\s*.*$', '', clean_title)   # Remove "- Free Tool" etc

                # Find body opening tag and add H1 after it
                body_pattern = r'(<body[^>]*>)'
                if re.search(body_pattern, content):
                    h1_tag = f'<h1 style="position:absolute;left:-9999px;top:-9999px;">{clean_title}</h1>'
                    content = re.sub(body_pattern, r'\1' + h1_tag, content, flags=re.IGNORECASE)
                    fixes += 1

        return content, fixes

    def process_file(self, file_path):
        """Process a single file for meta optimization"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            total_fixes = 0

            # Analyze issues
            desc_status, description, length = self.analyze_meta_description(content)
            h1_status, h1_tags = self.analyze_h1_tags(content)

            rel_path = str(file_path.relative_to(self.base_dir))

            # Record issues
            if desc_status != "good":
                self.issues_found.append(f"{rel_path}: Meta description {desc_status} ({length} chars)")
            if h1_status != "good":
                self.issues_found.append(f"{rel_path}: H1 tag {h1_status} ({len(h1_tags)} found)")

            # Apply fixes
            content, desc_fixes = self.optimize_meta_description(content, file_path)
            total_fixes += desc_fixes

            content, h1_fixes = self.add_missing_h1(content, file_path)
            total_fixes += h1_fixes

            # Write back if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            self.fixes_applied += total_fixes
            return total_fixes

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return 0

    def run_meta_optimization(self):
        """Run meta description and H1 optimization"""
        print("📝 Running meta description and H1 optimization...")

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

        print(f"\n✅ Meta optimization complete:")
        print(f"   Files processed: {self.files_processed}")
        print(f"   Files with fixes: {files_with_fixes}")
        print(f"   Total fixes applied: {self.fixes_applied}")
        print(f"   Issues found: {len(self.issues_found)}")

        return files_with_fixes

    def generate_issues_report(self):
        """Generate report of issues found"""
        print(f"\n📋 META DESCRIPTION & H1 ISSUES REPORT:")
        print("="*60)

        desc_too_long = [issue for issue in self.issues_found if "too_long" in issue]
        desc_too_short = [issue for issue in self.issues_found if "too_short" in issue]
        desc_missing = [issue for issue in self.issues_found if "description missing" in issue]
        h1_missing = [issue for issue in self.issues_found if "H1 tag missing" in issue]
        h1_multiple = [issue for issue in self.issues_found if "H1 tag multiple" in issue]

        print(f"Meta descriptions too long (>160 chars): {len(desc_too_long)}")
        print(f"Meta descriptions too short (<120 chars): {len(desc_too_short)}")
        print(f"Meta descriptions missing: {len(desc_missing)}")
        print(f"H1 tags missing: {len(h1_missing)}")
        print(f"Multiple H1 tags: {len(h1_multiple)}")

        # Show samples
        if desc_too_long:
            print(f"\n📏 Sample long descriptions (first 5):")
            for issue in desc_too_long[:5]:
                print(f"   {issue}")

        if h1_missing:
            print(f"\n🏷️  Sample missing H1 tags (first 5):")
            for issue in h1_missing[:5]:
                print(f"   {issue}")

        print("="*60)

def main():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")
    optimizer = MetaOptimizer(base_dir)

    print("📝 META DESCRIPTION & H1 OPTIMIZER - Agent 3")
    print("Focus: Optimize meta descriptions and H1 tags for SEO")
    print("="*70)

    files_fixed = optimizer.run_meta_optimization()
    optimizer.generate_issues_report()

    print(f"\n🎯 META OPTIMIZATION COMPLETE:")
    print(f"   Total fixes applied: {optimizer.fixes_applied}")
    print(f"   Files with fixes: {files_fixed}")
    print(f"   Files processed: {optimizer.files_processed}")

if __name__ == "__main__":
    main()