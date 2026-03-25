#!/usr/bin/env python3
"""
SEO Compliance Validator for Zovo Tools
Comprehensive audit and fix for canonical URLs, schema markup, OG tags, meta descriptions, H1 tags
"""

import os
import re
import json
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict
import html

class SEOAuditor:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.issues = defaultdict(list)
        self.fixes_applied = 0
        self.total_files = 0

    def audit_file(self, file_path):
        """Audit a single HTML file for SEO compliance"""
        self.total_files += 1

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')
            issues = []

            # Get relative path from base dir for reporting
            rel_path = str(file_path.relative_to(self.base_dir))

            # Check canonical URL
            canonical = soup.find('link', rel='canonical')
            if not canonical:
                issues.append('Missing canonical URL')
            elif canonical.get('href'):
                href = canonical.get('href')
                if 'tools.zovo.one' in href or 'theluckystrike.github.io' in href:
                    issues.append(f'Stale canonical URL: {href}')
                elif not href.startswith('https://zovo.one/free-tools/'):
                    issues.append(f'Wrong canonical format: {href}')

            # Check schema markup
            schema_scripts = soup.find_all('script', type='application/ld+json')
            if not schema_scripts:
                issues.append('Missing schema markup')
            else:
                for script in schema_scripts:
                    try:
                        schema_data = json.loads(script.string)
                        schema_type = schema_data.get('@type', '')
                        if schema_type not in ['WebApplication', 'Article', 'FAQPage']:
                            issues.append(f'Invalid schema type: {schema_type}')
                    except json.JSONDecodeError:
                        issues.append('Invalid schema JSON')

            # Check OG tags
            og_title = soup.find('meta', property='og:title')
            og_url = soup.find('meta', property='og:url')
            og_type = soup.find('meta', property='og:type')
            og_site_name = soup.find('meta', property='og:site_name')

            if not og_title:
                issues.append('Missing og:title')
            if not og_url:
                issues.append('Missing og:url')
            elif og_url.get('content'):
                og_url_content = og_url.get('content')
                if 'tools.zovo.one' in og_url_content or 'theluckystrike.github.io' in og_url_content:
                    issues.append(f'Stale OG URL: {og_url_content}')
            if not og_type:
                issues.append('Missing og:type')
            if not og_site_name:
                issues.append('Missing og:site_name')

            # Check meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if not meta_desc:
                issues.append('Missing meta description')
            elif meta_desc.get('content'):
                desc_content = meta_desc.get('content')
                if len(desc_content) > 160:
                    issues.append(f'Meta description too long: {len(desc_content)} chars')
                elif len(desc_content) < 120:
                    issues.append(f'Meta description too short: {len(desc_content)} chars')

            # Check H1 tag
            h1_tags = soup.find_all('h1')
            if not h1_tags:
                issues.append('Missing H1 tag')
            elif len(h1_tags) > 1:
                issues.append(f'Multiple H1 tags: {len(h1_tags)}')

            # Check for stale URLs in content
            if 'tools.zovo.one' in content or 'theluckystrike.github.io' in content:
                stale_matches = []
                if 'tools.zovo.one' in content:
                    stale_matches.append('tools.zovo.one')
                if 'theluckystrike.github.io' in content:
                    stale_matches.append('theluckystrike.github.io')
                issues.append(f'Stale URLs in content: {", ".join(stale_matches)}')

            if issues:
                self.issues[rel_path] = issues

            return issues

        except Exception as e:
            self.issues[rel_path] = [f'File read error: {str(e)}']
            return [f'File read error: {str(e)}']

    def fix_canonical_url(self, file_path):
        """Fix canonical URL in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')
            canonical = soup.find('link', rel='canonical')

            # Determine correct canonical URL based on file path
            rel_path = str(file_path.relative_to(self.base_dir))

            if rel_path.startswith('articles/'):
                correct_url = f"https://zovo.one/free-tools/{rel_path.replace('/index.html', '/')}"
            else:
                # Tool directory
                tool_name = rel_path.replace('/index.html', '')
                correct_url = f"https://zovo.one/free-tools/{tool_name}/"

            if canonical:
                # Update existing canonical
                if canonical.get('href') != correct_url:
                    canonical['href'] = correct_url
                    self.fixes_applied += 1
            else:
                # Add missing canonical
                head = soup.find('head')
                if head:
                    new_canonical = soup.new_tag('link', rel='canonical', href=correct_url)
                    head.append(new_canonical)
                    self.fixes_applied += 1

            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

        except Exception as e:
            print(f"Error fixing canonical in {file_path}: {e}")

    def fix_og_tags(self, file_path):
        """Fix missing OG tags"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')
            head = soup.find('head')

            if not head:
                return

            # Get page title and description
            title_tag = soup.find('title')
            meta_desc = soup.find('meta', attrs={'name': 'description'})

            title_content = title_tag.get_text() if title_tag else 'Zovo Tools'
            desc_content = meta_desc.get('content') if meta_desc else 'Free online tools for productivity'

            # Determine correct URL
            rel_path = str(file_path.relative_to(self.base_dir))
            if rel_path.startswith('articles/'):
                correct_url = f"https://zovo.one/free-tools/{rel_path.replace('/index.html', '/')}"
            else:
                tool_name = rel_path.replace('/index.html', '')
                correct_url = f"https://zovo.one/free-tools/{tool_name}/"

            # Add/fix OG tags
            og_tags = [
                ('og:title', title_content),
                ('og:description', desc_content),
                ('og:type', 'website'),
                ('og:url', correct_url),
                ('og:site_name', 'Zovo')
            ]

            fixes_made = 0
            for prop, content_val in og_tags:
                existing = soup.find('meta', property=prop)
                if not existing:
                    new_tag = soup.new_tag('meta', property=prop, content=content_val)
                    head.append(new_tag)
                    fixes_made += 1
                elif existing.get('content') != content_val and prop == 'og:url':
                    # Fix stale URLs
                    if 'tools.zovo.one' in existing.get('content', '') or 'theluckystrike.github.io' in existing.get('content', ''):
                        existing['content'] = content_val
                        fixes_made += 1

            if fixes_made > 0:
                self.fixes_applied += fixes_made
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))

        except Exception as e:
            print(f"Error fixing OG tags in {file_path}: {e}")

    def fix_schema_markup(self, file_path):
        """Add schema markup if missing"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            soup = BeautifulSoup(content, 'html.parser')
            head = soup.find('head')

            if not head:
                return

            # Check if schema already exists
            schema_scripts = soup.find_all('script', type='application/ld+json')
            if schema_scripts:
                return  # Already has schema

            # Get page info
            title_tag = soup.find('title')
            meta_desc = soup.find('meta', attrs={'name': 'description'})

            title_content = title_tag.get_text() if title_tag else 'Zovo Tool'
            desc_content = meta_desc.get('content') if meta_desc else 'Free online tool'

            # Determine URL and schema type
            rel_path = str(file_path.relative_to(self.base_dir))
            if rel_path.startswith('articles/'):
                correct_url = f"https://zovo.one/free-tools/{rel_path.replace('/index.html', '/')}"
                schema_type = 'Article'
            else:
                tool_name = rel_path.replace('/index.html', '')
                correct_url = f"https://zovo.one/free-tools/{tool_name}/"
                schema_type = 'WebApplication'

            # Create schema markup
            if schema_type == 'Article':
                schema_data = {
                    "@context": "https://schema.org",
                    "@type": "Article",
                    "headline": title_content,
                    "author": {
                        "@type": "Person",
                        "name": "Michael Lip"
                    },
                    "publisher": {
                        "@type": "Organization",
                        "name": "Zovo Tools",
                        "url": "https://zovo.one/free-tools/"
                    },
                    "datePublished": "2026-03-25",
                    "dateModified": "2026-03-25",
                    "mainEntityOfPage": {
                        "@type": "WebPage",
                        "@id": correct_url
                    },
                    "description": desc_content
                }
            else:
                schema_data = {
                    "@context": "https://schema.org",
                    "@type": "WebApplication",
                    "name": title_content,
                    "description": desc_content,
                    "url": correct_url,
                    "applicationCategory": "Utility",
                    "operatingSystem": "Any",
                    "offers": {
                        "@type": "Offer",
                        "price": "0",
                        "priceCurrency": "USD"
                    }
                }

            # Add schema script
            schema_script = soup.new_tag('script', type='application/ld+json')
            schema_script.string = json.dumps(schema_data, indent=2)
            head.append(schema_script)

            self.fixes_applied += 1

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

        except Exception as e:
            print(f"Error adding schema to {file_path}: {e}")

    def fix_stale_urls(self, file_path):
        """Fix stale URLs throughout the file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Replace stale URLs
            content = content.replace('tools.zovo.one', 'zovo.one/free-tools')
            content = content.replace('theluckystrike.github.io/zovo-tools', 'zovo.one/free-tools')

            if content != original_content:
                self.fixes_applied += 1
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

        except Exception as e:
            print(f"Error fixing stale URLs in {file_path}: {e}")

    def run_audit(self):
        """Run complete SEO audit"""
        print("🔍 Starting comprehensive SEO audit...")

        # Find all HTML files
        html_files = list(self.base_dir.glob('**/*.html'))
        print(f"Found {len(html_files)} HTML files to audit")

        # Audit each file
        for i, file_path in enumerate(html_files):
            if i % 50 == 0:
                print(f"  Auditing file {i+1}/{len(html_files)}: {file_path.name}")

            self.audit_file(file_path)

        return self.issues

    def run_fixes(self):
        """Apply systematic fixes to all files"""
        print("🛠️  Starting SEO fixes...")

        html_files = list(self.base_dir.glob('**/*.html'))

        for i, file_path in enumerate(html_files):
            if i % 50 == 0:
                print(f"  Fixing file {i+1}/{len(html_files)}: {file_path.name}")

            # Apply all fixes
            self.fix_canonical_url(file_path)
            self.fix_og_tags(file_path)
            self.fix_schema_markup(file_path)
            self.fix_stale_urls(file_path)

    def generate_report(self):
        """Generate comprehensive audit report"""
        print("\n" + "="*80)
        print("SEO COMPLIANCE AUDIT REPORT")
        print("="*80)

        total_issues = sum(len(issues) for issues in self.issues.values())
        compliance_rate = ((self.total_files - len(self.issues)) / self.total_files) * 100

        print(f"📊 SUMMARY:")
        print(f"   Total files audited: {self.total_files}")
        print(f"   Files with issues: {len(self.issues)}")
        print(f"   Total issues found: {total_issues}")
        print(f"   Compliance rate: {compliance_rate:.1f}%")
        print(f"   Fixes applied: {self.fixes_applied}")

        # Issue breakdown
        issue_counts = defaultdict(int)
        for issues in self.issues.values():
            for issue in issues:
                issue_type = issue.split(':')[0] if ':' in issue else issue
                issue_counts[issue_type] += 1

        print(f"\n🔍 ISSUE BREAKDOWN:")
        for issue_type, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {issue_type}: {count} files")

        # Sample issues
        print(f"\n📝 SAMPLE ISSUES (first 20 files):")
        for i, (file_path, issues) in enumerate(self.issues.items()):
            if i >= 20:
                break
            print(f"   {file_path}:")
            for issue in issues[:3]:  # Show first 3 issues per file
                print(f"     - {issue}")
            if len(issues) > 3:
                print(f"     - ... and {len(issues)-3} more issues")

        print("="*80)

def main():
    base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")
    auditor = SEOAuditor(base_dir)

    print("🚀 SEO COMPLIANCE VALIDATOR - Agent 3")
    print("Target: 100% SEO compliance across 600+ tools and 50+ articles\n")

    # Run initial audit
    print("Phase 1: Initial SEO Audit")
    issues = auditor.run_audit()
    auditor.generate_report()

    print("\nPhase 2: Applying Systematic Fixes")
    auditor.run_fixes()

    # Run post-fix audit
    print("\nPhase 3: Post-Fix Validation")
    auditor_post = SEOAuditor(base_dir)
    issues_post = auditor_post.run_audit()
    auditor_post.generate_report()

    # Final summary
    initial_compliance = ((auditor.total_files - len(issues)) / auditor.total_files) * 100
    final_compliance = ((auditor_post.total_files - len(issues_post)) / auditor_post.total_files) * 100

    print(f"\n🎯 MISSION COMPLETE:")
    print(f"   Initial compliance: {initial_compliance:.1f}%")
    print(f"   Final compliance: {final_compliance:.1f}%")
    print(f"   Improvement: +{final_compliance - initial_compliance:.1f}%")
    print(f"   Total fixes applied: {auditor.fixes_applied}")

if __name__ == "__main__":
    main()