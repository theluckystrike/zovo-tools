#!/usr/bin/env python3
"""
Corrected SEO Fixer for Zovo Tools
Handles the actual HTML format used in the files
"""

import os
import re
from pathlib import Path

class CorrectedSEOFixer:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.fixes_applied = 0
        self.files_processed = 0
        self.issues_found = []

    def analyze_meta_description(self, content):
        """Analyze meta description using correct format"""
        # Pattern for: <meta content="..." name="description"/>
        desc_match = re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]*name=["\']description["\'][^>]*/?>', content, re.IGNORECASE)

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

    def optimize_meta_description(self, content, file_path):
        """Optimize meta description length"""
        fixes = 0
        desc_status, description, length = self.analyze_meta_description(content)

        if desc_status == "too_long" and length > 160:
            # Truncate to 157 characters and add "..."
            optimized_desc = description[:157] + "..."

            # Replace in content using correct pattern
            pattern = r'(<meta[^>]+content=["\'])([^"\']+)(["\'][^>]*name=["\']description["\'][^>]*/?)'

            def replace_desc(match):
                nonlocal fixes
                fixes += 1
                return match.group(1) + optimized_desc + match.group(3)

            content = re.sub(pattern, replace_desc, content, flags=re.IGNORECASE)

        return content, fixes

    def analyze_h1_tags(self, content):
        """Analyze H1 tags for SEO compliance"""
        h1_matches = re.findall(r'<h1[^>]*>([^<]+)</h1>', content, re.IGNORECASE | re.DOTALL)

        if not h1_matches:
            return "missing", []
        elif len(h1_matches) > 1:
            return "multiple", h1_matches
        else:
            return "good", h1_matches

    def check_canonical_url(self, content, file_path):
        """Check canonical URL compliance"""
        rel_path = str(file_path.relative_to(self.base_dir))
        if rel_path.startswith('articles/'):
            expected_url = f"https://zovo.one/free-tools/{rel_path.replace('/index.html', '/')}"
        else:
            tool_name = rel_path.replace('/index.html', '')
            expected_url = f"https://zovo.one/free-tools/{tool_name}/"

        canonical_match = re.search(r'<link[^>]+href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\'][^>]*/?>', content, re.IGNORECASE)

        if not canonical_match:
            return "missing", None, expected_url

        actual_url = canonical_match.group(1)
        if actual_url != expected_url:
            if 'tools.zovo.one' in actual_url or 'theluckystrike.github.io' in actual_url:
                return "stale", actual_url, expected_url
            else:
                return "wrong_format", actual_url, expected_url

        return "good", actual_url, expected_url

    def check_schema_markup(self, content):
        """Check schema markup compliance"""
        schema_matches = re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>([^<]+)</script>', content, re.IGNORECASE | re.DOTALL)

        if not schema_matches:
            return "missing", []

        # Check for valid schema types
        valid_types = ['WebApplication', 'Article', 'FAQPage']
        schema_types = []

        for schema in schema_matches:
            if '"@type"' in schema:
                type_match = re.search(r'"@type"\s*:\s*"([^"]+)"', schema)
                if type_match:
                    schema_types.append(type_match.group(1))

        invalid_types = [t for t in schema_types if t not in valid_types]
        if invalid_types:
            return "invalid_type", invalid_types

        return "good", schema_types

    def process_file(self, file_path):
        """Process a single file and record all SEO issues"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            rel_path = str(file_path.relative_to(self.base_dir))
            issues = []
            total_fixes = 0

            # Check meta description
            desc_status, description, length = self.analyze_meta_description(content)
            if desc_status != "good":
                if desc_status == "too_long":
                    issues.append(f"Meta description too long: {length} chars")
                    # Apply fix
                    content, fixes = self.optimize_meta_description(content, file_path)
                    total_fixes += fixes
                elif desc_status == "too_short":
                    issues.append(f"Meta description too short: {length} chars")
                else:
                    issues.append("Meta description missing")

            # Check H1 tags
            h1_status, h1_tags = self.analyze_h1_tags(content)
            if h1_status != "good":
                if h1_status == "missing":
                    issues.append("H1 tag missing")
                elif h1_status == "multiple":
                    issues.append(f"Multiple H1 tags: {len(h1_tags)}")

            # Check canonical URL
            canonical_status, actual_url, expected_url = self.check_canonical_url(content, file_path)
            if canonical_status != "good":
                if canonical_status == "missing":
                    issues.append("Missing canonical URL")
                elif canonical_status == "stale":
                    issues.append(f"Stale canonical URL: {actual_url}")
                elif canonical_status == "wrong_format":
                    issues.append(f"Wrong canonical format: {actual_url}")

            # Check schema markup
            schema_status, schema_data = self.check_schema_markup(content)
            if schema_status != "good":
                if schema_status == "missing":
                    issues.append("Missing schema markup")
                elif schema_status == "invalid_type":
                    issues.append(f"Invalid schema types: {', '.join(schema_data)}")

            if issues:
                self.issues_found.append({
                    'file': rel_path,
                    'issues': issues
                })

            # Write back if fixes were made
            if total_fixes > 0:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

            self.fixes_applied += total_fixes
            self.files_processed += 1
            return len(issues)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return 0

    def run_comprehensive_audit(self):
        """Run comprehensive SEO audit"""
        print("🔍 Running comprehensive SEO audit...")

        html_files = list(self.base_dir.glob('**/*.html'))
        print(f"Found {len(html_files)} HTML files to audit")

        total_issues = 0

        for i, file_path in enumerate(html_files):
            if i % 50 == 0:
                print(f"  Processing file {i+1}/{len(html_files)}: {file_path.name}")

            issues_count = self.process_file(file_path)
            total_issues += issues_count

        return total_issues

    def generate_comprehensive_report(self):
        """Generate comprehensive SEO audit report"""
        print("\n" + "="*80)
        print("COMPREHENSIVE SEO AUDIT REPORT")
        print("="*80)

        # Count different types of issues
        meta_too_long = 0
        meta_too_short = 0
        meta_missing = 0
        h1_missing = 0
        h1_multiple = 0
        canonical_missing = 0
        canonical_stale = 0
        canonical_wrong = 0
        schema_missing = 0
        schema_invalid = 0

        for file_data in self.issues_found:
            for issue in file_data['issues']:
                if "too long" in issue:
                    meta_too_long += 1
                elif "too short" in issue:
                    meta_too_short += 1
                elif "Meta description missing" in issue:
                    meta_missing += 1
                elif "H1 tag missing" in issue:
                    h1_missing += 1
                elif "Multiple H1 tags" in issue:
                    h1_multiple += 1
                elif "Missing canonical" in issue:
                    canonical_missing += 1
                elif "Stale canonical" in issue:
                    canonical_stale += 1
                elif "Wrong canonical" in issue:
                    canonical_wrong += 1
                elif "Missing schema" in issue:
                    schema_missing += 1
                elif "Invalid schema" in issue:
                    schema_invalid += 1

        total_issues = len(self.issues_found)
        compliance_rate = ((self.files_processed - len(self.issues_found)) / self.files_processed) * 100

        print(f"📊 SUMMARY:")
        print(f"   Files audited: {self.files_processed}")
        print(f"   Files with issues: {len(self.issues_found)}")
        print(f"   Compliance rate: {compliance_rate:.1f}%")
        print(f"   Fixes applied: {self.fixes_applied}")

        print(f"\n📋 ISSUE BREAKDOWN:")
        print(f"   Meta descriptions too long: {meta_too_long}")
        print(f"   Meta descriptions too short: {meta_too_short}")
        print(f"   Meta descriptions missing: {meta_missing}")
        print(f"   H1 tags missing: {h1_missing}")
        print(f"   Multiple H1 tags: {h1_multiple}")
        print(f"   Canonical URLs missing: {canonical_missing}")
        print(f"   Canonical URLs stale: {canonical_stale}")
        print(f"   Canonical URLs wrong format: {canonical_wrong}")
        print(f"   Schema markup missing: {schema_missing}")
        print(f"   Schema markup invalid: {schema_invalid}")

        # Show sample issues
        print(f"\n🔍 SAMPLE ISSUES (first 10 files):")
        for i, file_data in enumerate(self.issues_found[:10]):
            print(f"   {file_data['file']}:")
            for issue in file_data['issues'][:3]:
                print(f"     - {issue}")
            if len(file_data['issues']) > 3:
                print(f"     - ... and {len(file_data['issues'])-3} more")

        print("="*80)

def main():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")
    fixer = CorrectedSEOFixer(base_dir)

    print("🔍 COMPREHENSIVE SEO AUDIT - Agent 3")
    print("Focus: Complete SEO compliance analysis and fixes")
    print("="*70)

    total_issues = fixer.run_comprehensive_audit()
    fixer.generate_comprehensive_report()

    print(f"\n🎯 SEO AUDIT COMPLETE:")
    print(f"   Total issues found: {total_issues}")
    print(f"   Fixes applied: {fixer.fixes_applied}")
    print(f"   Files processed: {fixer.files_processed}")

if __name__ == "__main__":
    main()