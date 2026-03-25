#!/usr/bin/env python3
"""
Deep Violation Scanner - Agent 2 Support
Scans for advanced violations and SEO gaps in G-N tools
"""

import os
import re
import json
from pathlib import Path
from urllib.parse import urljoin, urlparse

class DeepViolationScanner:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.findings = []

    def check_internal_links(self, html_content, tool_name):
        """Check for broken internal links"""
        link_pattern = re.compile(r'href=["\']([^"\']*)["\']', re.IGNORECASE)
        links = link_pattern.findall(html_content)

        broken_links = []
        for link in links:
            if link.startswith('/free-tools/') and not link.startswith('http'):
                # Check if target tool exists
                tool_path = link.replace('/free-tools/', '').strip('/')
                if tool_path and not (self.base_dir / tool_path).exists():
                    broken_links.append(link)

        if broken_links:
            self.findings.append({
                'tool': tool_name,
                'type': 'broken_internal_links',
                'details': broken_links
            })

    def check_duplicate_meta(self, html_content, tool_name):
        """Check for duplicate meta descriptions"""
        meta_pattern = re.compile(r'<meta name="description" content="([^"]*)"', re.IGNORECASE)
        matches = meta_pattern.findall(html_content)

        if len(matches) > 1:
            self.findings.append({
                'tool': tool_name,
                'type': 'duplicate_meta_description',
                'details': matches
            })

    def check_stale_urls(self, html_content, tool_name):
        """Check for potentially stale external URLs"""
        url_pattern = re.compile(r'https?://[^\s<>"]+', re.IGNORECASE)
        urls = url_pattern.findall(html_content)

        stale_indicators = ['2023', '2022', '2021', 'beta', 'staging', 'test']
        stale_urls = []

        for url in urls:
            for indicator in stale_indicators:
                if indicator in url.lower():
                    stale_urls.append(url)
                    break

        if stale_urls:
            self.findings.append({
                'tool': tool_name,
                'type': 'potentially_stale_urls',
                'details': stale_urls
            })

    def check_missing_analytics(self, html_content, tool_name):
        """Check for missing analytics tracking"""
        has_gtag = 'gtag(' in html_content
        has_ga = 'GoogleAnalytics' in html_content or 'google-analytics' in html_content

        if not (has_gtag or has_ga):
            self.findings.append({
                'tool': tool_name,
                'type': 'missing_analytics',
                'details': 'No Google Analytics found'
            })

    def check_accessibility_issues(self, html_content, tool_name):
        """Check for accessibility violations"""
        issues = []

        # Check for images without alt text
        img_pattern = re.compile(r'<img[^>]*>', re.IGNORECASE)
        images = img_pattern.findall(html_content)

        for img in images:
            if 'alt=' not in img.lower():
                issues.append('Image without alt text')
                break

        # Check for buttons without proper labels
        if '<button>' in html_content.lower() and 'aria-label' not in html_content.lower():
            issues.append('Button without aria-label')

        if issues:
            self.findings.append({
                'tool': tool_name,
                'type': 'accessibility_issues',
                'details': issues
            })

    def scan_tool_deep(self, tool_name):
        """Deep scan of a single tool"""
        tool_dir = self.base_dir / tool_name
        index_path = tool_dir / 'index.html'

        if not index_path.exists():
            self.findings.append({
                'tool': tool_name,
                'type': 'missing_index',
                'details': 'No index.html found'
            })
            return

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Run all deep checks
            self.check_internal_links(content, tool_name)
            self.check_duplicate_meta(content, tool_name)
            self.check_stale_urls(content, tool_name)
            self.check_missing_analytics(content, tool_name)
            self.check_accessibility_issues(content, tool_name)

        except Exception as e:
            self.findings.append({
                'tool': tool_name,
                'type': 'scan_error',
                'details': str(e)
            })

    def get_gn_tools(self):
        """Get all tool directories G-N"""
        all_dirs = [d for d in os.listdir(self.base_dir) if os.path.isdir(os.path.join(self.base_dir, d))]
        gn_tools = [d for d in all_dirs if d[0].lower() in 'ghijklmn']
        return sorted(gn_tools)

    def run_deep_scan(self):
        """Run complete deep scan"""
        print("🔍 Deep Violation Scanner - Tools G-N")
        print("-" * 50)

        gn_tools = self.get_gn_tools()
        print(f"Scanning {len(gn_tools)} tools for deep violations...")

        for tool in gn_tools:
            self.scan_tool_deep(tool)

        # Report findings
        if not self.findings:
            print("✅ No deep violations found!")
            return

        print(f"\n⚠️ Found {len(self.findings)} deep violations:")

        violation_types = {}
        for finding in self.findings:
            vtype = finding['type']
            if vtype not in violation_types:
                violation_types[vtype] = []
            violation_types[vtype].append(finding)

        for vtype, findings in violation_types.items():
            print(f"\n📋 {vtype.replace('_', ' ').title()}: {len(findings)} issues")
            for finding in findings[:3]:  # Show first 3 examples
                print(f"  • {finding['tool']}: {finding['details']}")
            if len(findings) > 3:
                print(f"  ... and {len(findings) - 3} more")

        # Save detailed report
        report_path = self.base_dir / 'deep_violations_report.json'
        with open(report_path, 'w') as f:
            json.dump(self.findings, f, indent=2)
        print(f"\n📄 Detailed report saved to: {report_path}")

if __name__ == "__main__":
    scanner = DeepViolationScanner("/Users/mike/zovo-workspaces/zovo-tools")
    scanner.run_deep_scan()