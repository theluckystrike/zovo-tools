#!/usr/bin/env python3
"""
Advanced SEO QA Agent Delta - T-Z Tools Optimization
Comprehensive SEO audit and optimization for tools starting with T-Z
"""

import os
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

class SEOAuditor:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.issues = []
        self.optimizations = []

    def check_title_tag(self, html_content, tool_name):
        """Check title tag optimization"""
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html_content, re.IGNORECASE)
        if not title_match:
            self.issues.append(f"{tool_name}: Missing title tag")
            return False

        title = title_match.group(1)
        title_length = len(title)

        # Check title length (ideal: 50-60 characters)
        if title_length > 60:
            self.issues.append(f"{tool_name}: Title too long ({title_length} chars): {title[:50]}...")
        elif title_length < 30:
            self.issues.append(f"{tool_name}: Title too short ({title_length} chars): {title}")

        # Check for keyword optimization
        if tool_name.replace('-', ' ').lower() not in title.lower():
            self.issues.append(f"{tool_name}: Title doesn't contain primary keyword")

        return True

    def check_meta_description(self, html_content, tool_name):
        """Check meta description optimization"""
        desc_pattern = r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']'
        desc_match = re.search(desc_pattern, html_content, re.IGNORECASE)

        if not desc_match:
            self.issues.append(f"{tool_name}: Missing meta description")
            return False

        description = desc_match.group(1)
        desc_length = len(description)

        # Check description length (ideal: 150-160 characters)
        if desc_length > 160:
            self.issues.append(f"{tool_name}: Meta description too long ({desc_length} chars)")
        elif desc_length < 120:
            self.issues.append(f"{tool_name}: Meta description too short ({desc_length} chars)")

        # Check for compelling language
        if not any(word in description.lower() for word in ['free', 'instant', 'online', 'calculator', 'tool']):
            self.issues.append(f"{tool_name}: Meta description lacks compelling keywords")

        return True

    def check_header_structure(self, html_content, tool_name):
        """Check H1-H6 header hierarchy"""
        headers = re.findall(r'<h([1-6])[^>]*>([^<]+)</h[1-6]>', html_content, re.IGNORECASE)

        if not headers:
            self.issues.append(f"{tool_name}: No headers found")
            return False

        h1_count = len([h for h in headers if h[0] == '1'])
        if h1_count == 0:
            self.issues.append(f"{tool_name}: No H1 tag found")
        elif h1_count > 1:
            self.issues.append(f"{tool_name}: Multiple H1 tags ({h1_count} found)")

        return True

    def check_canonical_tag(self, html_content, tool_name):
        """Check canonical URL implementation"""
        canonical_pattern = r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']'
        canonical_match = re.search(canonical_pattern, html_content, re.IGNORECASE)

        if not canonical_match:
            self.issues.append(f"{tool_name}: Missing canonical tag")
            return False

        canonical_url = canonical_match.group(1)
        if not canonical_url.startswith('https://'):
            self.issues.append(f"{tool_name}: Canonical URL not HTTPS")

        return True

    def check_open_graph(self, html_content, tool_name):
        """Check Open Graph meta tags"""
        og_tags = ['og:title', 'og:description', 'og:url', 'og:type', 'og:image']
        missing_og = []

        for tag in og_tags:
            pattern = f'<meta[^>]*property=["\'][^"\']*{tag}[^"\']*["\'][^>]*>'
            if not re.search(pattern, html_content, re.IGNORECASE):
                missing_og.append(tag)

        if missing_og:
            self.issues.append(f"{tool_name}: Missing OG tags: {', '.join(missing_og)}")

        return len(missing_og) == 0

    def check_schema_markup(self, html_content, tool_name):
        """Check structured data/schema markup"""
        schema_patterns = [
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>',
            r'itemscope',
            r'itemtype'
        ]

        has_schema = any(re.search(pattern, html_content, re.IGNORECASE) for pattern in schema_patterns)

        if not has_schema:
            self.issues.append(f"{tool_name}: No schema markup found")
            return False

        return True

    def check_mobile_optimization(self, html_content, tool_name):
        """Check mobile viewport and responsive design"""
        viewport_pattern = r'<meta[^>]*name=["\']viewport["\'][^>]*>'
        if not re.search(viewport_pattern, html_content, re.IGNORECASE):
            self.issues.append(f"{tool_name}: Missing viewport meta tag")
            return False

        return True

    def audit_tool(self, tool_path):
        """Comprehensive SEO audit for a single tool"""
        tool_name = tool_path.name
        index_file = tool_path / 'index.html'

        if not index_file.exists():
            self.issues.append(f"{tool_name}: No index.html found")
            return False

        try:
            with open(index_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
        except Exception as e:
            self.issues.append(f"{tool_name}: Error reading index.html: {e}")
            return False

        # Run all SEO checks
        self.check_title_tag(html_content, tool_name)
        self.check_meta_description(html_content, tool_name)
        self.check_header_structure(html_content, tool_name)
        self.check_canonical_tag(html_content, tool_name)
        self.check_open_graph(html_content, tool_name)
        self.check_schema_markup(html_content, tool_name)
        self.check_mobile_optimization(html_content, tool_name)

        return True

    def get_tz_tools(self):
        """Get all tool directories starting with T-Z"""
        all_tools = [d for d in self.base_path.iterdir()
                    if d.is_dir() and not d.name.startswith('.')]

        tz_tools = [tool for tool in all_tools
                   if tool.name[0].lower() >= 't' and tool.name[0].lower() <= 'z']

        return sorted(tz_tools)

    def run_comprehensive_audit(self):
        """Run complete SEO audit on T-Z tools"""
        tz_tools = self.get_tz_tools()
        total_tools = len(tz_tools)

        print(f"🔍 Starting SEO audit of {total_tools} T-Z tools...")

        for i, tool_path in enumerate(tz_tools, 1):
            print(f"[{i}/{total_tools}] Auditing {tool_path.name}...")
            self.audit_tool(tool_path)

        return self.generate_report()

    def generate_report(self):
        """Generate comprehensive SEO audit report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_issues': len(self.issues),
            'issues_by_category': self.categorize_issues(),
            'all_issues': self.issues,
            'optimizations_applied': self.optimizations
        }

        # Save report
        report_file = self.base_path / 'seo_audit_report_tz.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        return report

    def categorize_issues(self):
        """Categorize issues by type"""
        categories = {
            'title_issues': [],
            'meta_description_issues': [],
            'header_issues': [],
            'canonical_issues': [],
            'og_issues': [],
            'schema_issues': [],
            'mobile_issues': []
        }

        for issue in self.issues:
            if 'title' in issue.lower():
                categories['title_issues'].append(issue)
            elif 'meta description' in issue.lower():
                categories['meta_description_issues'].append(issue)
            elif 'header' in issue.lower() or 'h1' in issue.lower():
                categories['header_issues'].append(issue)
            elif 'canonical' in issue.lower():
                categories['canonical_issues'].append(issue)
            elif 'og' in issue.lower() or 'open graph' in issue.lower():
                categories['og_issues'].append(issue)
            elif 'schema' in issue.lower():
                categories['schema_issues'].append(issue)
            elif 'viewport' in issue.lower() or 'mobile' in issue.lower():
                categories['mobile_issues'].append(issue)

        return categories

if __name__ == "__main__":
    base_path = "/Users/mike/zovo-workspaces/zovo-tools"
    auditor = SEOAuditor(base_path)

    print("🚀 SEO Agent Delta - Advanced T-Z Tools Audit Starting...")
    report = auditor.run_comprehensive_audit()

    print(f"\n📊 SEO Audit Complete!")
    print(f"Total Issues Found: {report['total_issues']}")
    print(f"Report saved to: seo_audit_report_tz.json")

    # Print summary by category
    for category, issues in report['issues_by_category'].items():
        if issues:
            print(f"\n{category.replace('_', ' ').title()}: {len(issues)}")
            for issue in issues[:3]:  # Show first 3 issues per category
                print(f"  - {issue}")