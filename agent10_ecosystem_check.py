#!/usr/bin/env python3
"""
Agent 10: Advanced Ecosystem Health Checker
Comprehensive validation of the entire zovo-tools ecosystem
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
import subprocess

class EcosystemHealthChecker:
    def __init__(self):
        self.base_dir = Path('/Users/mike/zovo-workspaces/zovo-tools')
        self.issues = []
        self.stats = {}

    def log(self, message, level="INFO"):
        print(f"[ECOSYSTEM] {level}: {message}")
        if level in ["ERROR", "WARNING"]:
            self.issues.append(message)

    def check_tool_directories(self):
        """Validate all tool directories"""
        self.log("Checking tool directory structure...")

        tool_dirs = [d for d in self.base_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        self.stats['total_tools'] = len(tool_dirs)

        missing_index = []
        invalid_names = []
        empty_dirs = []

        for tool_dir in tool_dirs:
            # Check for index.html
            if not (tool_dir / "index.html").exists():
                missing_index.append(tool_dir.name)

            # Check directory naming
            if not re.match(r'^[a-z0-9-]+$', tool_dir.name):
                invalid_names.append(tool_dir.name)

            # Check if directory is empty
            if len(list(tool_dir.iterdir())) == 0:
                empty_dirs.append(tool_dir.name)

        if missing_index:
            self.log(f"Missing index.html in {len(missing_index)} tools: {missing_index[:10]}", "ERROR")

        if invalid_names:
            self.log(f"Invalid directory names: {invalid_names}", "WARNING")

        if empty_dirs:
            self.log(f"Empty directories: {empty_dirs}", "WARNING")

        self.stats['missing_index'] = len(missing_index)
        self.stats['invalid_names'] = len(invalid_names)
        self.stats['empty_dirs'] = len(empty_dirs)

        return tool_dirs

    def check_content_quality(self, tool_dirs):
        """Check content quality across all tools"""
        self.log("Checking content quality...")

        quality_issues = defaultdict(list)

        for tool_dir in tool_dirs:
            html_file = tool_dir / "index.html"
            if not html_file.exists():
                continue

            try:
                content = html_file.read_text(encoding='utf-8')
                tool_name = tool_dir.name

                # Check title format
                title_match = re.search(r'<title>([^<]+)</title>', content)
                if title_match:
                    title = title_match.group(1)
                    if not title.endswith(" | Free Online Tool"):
                        quality_issues['title_format'].append(tool_name)
                else:
                    quality_issues['missing_title'].append(tool_name)

                # Check meta description
                if 'meta name="description"' not in content:
                    quality_issues['missing_meta_desc'].append(tool_name)

                # Check dark theme
                if 'body { background: #0a0a0f;' not in content:
                    quality_issues['missing_dark_theme'].append(tool_name)

                # Check canonical URL
                if 'rel="canonical"' not in content:
                    quality_issues['missing_canonical'].append(tool_name)

                # Check schema markup
                if 'application/ld+json' not in content:
                    quality_issues['missing_schema'].append(tool_name)

            except Exception as e:
                quality_issues['read_errors'].append(f"{tool_name}: {str(e)}")

        # Report quality issues
        for issue_type, tools in quality_issues.items():
            if tools:
                self.log(f"{issue_type}: {len(tools)} tools affected", "WARNING")
                self.stats[issue_type] = len(tools)

        return quality_issues

    def check_cross_references(self, tool_dirs):
        """Check for broken cross-references between tools"""
        self.log("Checking cross-references...")

        tool_names = {tool_dir.name for tool_dir in tool_dirs}
        broken_refs = []

        for tool_dir in tool_dirs:
            html_file = tool_dir / "index.html"
            if not html_file.exists():
                continue

            try:
                content = html_file.read_text(encoding='utf-8')

                # Find internal links to other tools
                internal_links = re.findall(r'href="\.\/([^"\/]+)\/"', content)

                for link_target in internal_links:
                    if link_target not in tool_names:
                        broken_refs.append(f"{tool_dir.name} -> {link_target}")

            except Exception as e:
                self.log(f"Error checking cross-refs in {tool_dir.name}: {e}", "WARNING")

        if broken_refs:
            self.log(f"Found {len(broken_refs)} broken cross-references", "ERROR")
            for ref in broken_refs[:10]:  # Show first 10
                self.log(f"  Broken: {ref}", "ERROR")

        self.stats['broken_cross_refs'] = len(broken_refs)
        return broken_refs

    def check_orphaned_files(self):
        """Check for orphaned files in the root directory"""
        self.log("Checking for orphaned files...")

        orphaned_files = []
        allowed_root_files = {
            'README.md', 'LICENSE', '.gitignore', 'package.json',
            'sitemap.xml', 'index.html', 'robots.txt',
            # Python scripts are allowed
            'agent10_quality_master.py', 'agent10_coordinator_status.py',
            'agent10_ecosystem_check.py'
        }

        for file in self.base_dir.iterdir():
            if file.is_file():
                if file.name.startswith('.'):
                    continue  # Skip hidden files
                if file.name.endswith('.py'):
                    continue  # Python scripts are OK
                if file.name not in allowed_root_files:
                    orphaned_files.append(file.name)

        if orphaned_files:
            self.log(f"Found {len(orphaned_files)} orphaned files: {orphaned_files[:10]}", "WARNING")

        self.stats['orphaned_files'] = len(orphaned_files)
        return orphaned_files

    def verify_sitemap_consistency(self, tool_dirs):
        """Verify sitemap matches actual directories"""
        self.log("Verifying sitemap consistency...")

        sitemap_file = self.base_dir / "sitemap.xml"
        if not sitemap_file.exists():
            self.log("No sitemap.xml found", "ERROR")
            return False

        try:
            sitemap_content = sitemap_file.read_text(encoding='utf-8')

            # Extract URLs from sitemap
            sitemap_urls = re.findall(r'<loc>https://tools\.zovo\.one/([^/<]+)/</loc>', sitemap_content)
            sitemap_tools = set(sitemap_urls)

            # Get actual tool directories
            actual_tools = {tool_dir.name for tool_dir in tool_dirs if (tool_dir / "index.html").exists()}

            # Find discrepancies
            missing_from_sitemap = actual_tools - sitemap_tools
            extra_in_sitemap = sitemap_tools - actual_tools

            if missing_from_sitemap:
                self.log(f"Tools missing from sitemap: {len(missing_from_sitemap)}", "ERROR")

            if extra_in_sitemap:
                self.log(f"Extra tools in sitemap: {len(extra_in_sitemap)}", "WARNING")

            self.stats['sitemap_tools'] = len(sitemap_tools)
            self.stats['actual_tools'] = len(actual_tools)
            self.stats['missing_from_sitemap'] = len(missing_from_sitemap)
            self.stats['extra_in_sitemap'] = len(extra_in_sitemap)

            return len(missing_from_sitemap) == 0 and len(extra_in_sitemap) == 0

        except Exception as e:
            self.log(f"Error checking sitemap: {e}", "ERROR")
            return False

    def generate_health_report(self):
        """Generate comprehensive health report"""
        self.log("="*60)
        self.log("ECOSYSTEM HEALTH REPORT")
        self.log("="*60)

        # Overall stats
        self.log(f"Total tool directories: {self.stats.get('total_tools', 0)}")
        self.log(f"Tools with index.html: {self.stats.get('total_tools', 0) - self.stats.get('missing_index', 0)}")

        # Quality metrics
        quality_score = 100
        if self.stats.get('missing_index', 0) > 0:
            quality_score -= (self.stats['missing_index'] / self.stats['total_tools']) * 20

        if self.stats.get('missing_meta_desc', 0) > 0:
            quality_score -= (self.stats['missing_meta_desc'] / self.stats['total_tools']) * 15

        if self.stats.get('missing_canonical', 0) > 0:
            quality_score -= (self.stats['missing_canonical'] / self.stats['total_tools']) * 10

        self.log(f"Overall quality score: {quality_score:.1f}%")

        # Issue summary
        if self.issues:
            self.log(f"\nFound {len(self.issues)} total issues:")
            for issue in self.issues[:10]:  # Show first 10
                self.log(f"  • {issue}")
            if len(self.issues) > 10:
                self.log(f"  ... and {len(self.issues) - 10} more")
        else:
            self.log("No critical issues found!")

        self.log("="*60)

    def run_full_check(self):
        """Run comprehensive ecosystem health check"""
        self.log("Starting comprehensive ecosystem health check...")

        # 1. Check tool directories
        tool_dirs = self.check_tool_directories()

        # 2. Check content quality
        quality_issues = self.check_content_quality(tool_dirs)

        # 3. Check cross-references
        broken_refs = self.check_cross_references(tool_dirs)

        # 4. Check orphaned files
        orphaned_files = self.check_orphaned_files()

        # 5. Verify sitemap
        sitemap_ok = self.verify_sitemap_consistency(tool_dirs)

        # 6. Generate report
        self.generate_health_report()

        return len(self.issues) == 0

if __name__ == "__main__":
    checker = EcosystemHealthChecker()
    healthy = checker.run_full_check()
    exit(0 if healthy else 1)