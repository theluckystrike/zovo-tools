#!/usr/bin/env python3
"""
QA Agent Echo - Comprehensive Performance & Security Audit
Performance and Security QA across 834+ tool directories
"""

import os
import re
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Set

class QAAgentEcho:
    def __init__(self, base_dir: str = "/Users/mike/zovo-workspaces/zovo-tools"):
        self.base_dir = Path(base_dir)
        self.audit_results = {
            'performance': {},
            'security': {},
            'summary': {},
            'improvements': []
        }
        self.total_dirs = 0
        self.processed_dirs = 0

    def run_comprehensive_audit(self):
        """Run comprehensive performance and security audit"""
        print("🔍 QA Agent Echo - Starting Comprehensive Audit")
        print(f"📁 Base Directory: {self.base_dir}")

        # Get all tool directories
        tool_dirs = [d for d in self.base_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        self.total_dirs = len(tool_dirs)

        print(f"📊 Found {self.total_dirs} tool directories to audit")

        for tool_dir in tool_dirs:
            if tool_dir.name.startswith('.'):
                continue

            self.audit_tool_directory(tool_dir)
            self.processed_dirs += 1

            if self.processed_dirs % 50 == 0:
                print(f"⚡ Progress: {self.processed_dirs}/{self.total_dirs} directories processed")

        self.generate_audit_report()
        self.apply_performance_optimizations()
        self.implement_security_enhancements()

    def audit_tool_directory(self, tool_dir: Path):
        """Audit individual tool directory for performance and security"""
        try:
            html_files = list(tool_dir.glob("*.html"))
            if not html_files:
                return

            main_html = html_files[0]  # Usually index.html

            with open(main_html, 'r', encoding='utf-8') as f:
                content = f.read()

            # Performance audits
            perf_issues = self.audit_performance(content, tool_dir.name)

            # Security audits
            sec_issues = self.audit_security(content, tool_dir.name)

            self.audit_results['performance'][tool_dir.name] = perf_issues
            self.audit_results['security'][tool_dir.name] = sec_issues

        except Exception as e:
            print(f"❌ Error auditing {tool_dir.name}: {e}")

    def audit_performance(self, content: str, tool_name: str) -> Dict:
        """Audit performance issues"""
        issues = {
            'critical': [],
            'warning': [],
            'info': [],
            'score': 100
        }

        # Check for Google Fonts optimization
        if 'fonts.googleapis.com' in content:
            if 'preconnect' not in content:
                issues['critical'].append('Missing preconnect for Google Fonts')
                issues['score'] -= 15
            if 'display=swap' not in content:
                issues['warning'].append('Missing font-display: swap')
                issues['score'] -= 5

        # Check for inline CSS size
        inline_css_matches = re.findall(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
        total_css_size = sum(len(match) for match in inline_css_matches)
        if total_css_size > 50000:  # 50KB threshold
            issues['warning'].append(f'Large inline CSS: {total_css_size/1024:.1f}KB')
            issues['score'] -= 10

        # Check for inline JS size
        inline_js_matches = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
        total_js_size = sum(len(match) for match in inline_js_matches)
        if total_js_size > 100000:  # 100KB threshold
            issues['warning'].append(f'Large inline JavaScript: {total_js_size/1024:.1f}KB')
            issues['score'] -= 10

        # Check for resource hints
        if 'dns-prefetch' not in content and 'preconnect' not in content:
            issues['info'].append('Consider adding resource hints')
            issues['score'] -= 3

        # Check for defer/async on scripts
        script_tags = re.findall(r'<script[^>]*src=', content)
        non_async_scripts = [s for s in script_tags if 'async' not in s and 'defer' not in s]
        if non_async_scripts:
            issues['warning'].append(f'{len(non_async_scripts)} scripts without async/defer')
            issues['score'] -= 5

        # Check for image optimization hints
        if '<img' in content:
            if 'loading="lazy"' not in content:
                issues['info'].append('Consider adding lazy loading to images')
                issues['score'] -= 2

        return issues

    def audit_security(self, content: str, tool_name: str) -> Dict:
        """Audit security issues"""
        issues = {
            'critical': [],
            'warning': [],
            'info': [],
            'score': 100
        }

        # Check for CSP header
        if 'Content-Security-Policy' not in content:
            issues['critical'].append('Missing Content Security Policy')
            issues['score'] -= 25

        # Check for X-Frame-Options
        if 'X-Frame-Options' not in content:
            issues['warning'].append('Missing X-Frame-Options header')
            issues['score'] -= 10

        # Check for HTTPS enforcement
        if 'http://' in content and tool_name not in ['http-status-checker']:
            issues['warning'].append('HTTP links found - should use HTTPS')
            issues['score'] -= 8

        # Check for external script integrity
        external_scripts = re.findall(r'<script[^>]*src=["\']https?://[^"\']*["\'][^>]*>', content)
        scripts_without_integrity = [s for s in external_scripts if 'integrity=' not in s]
        if scripts_without_integrity:
            issues['warning'].append(f'{len(scripts_without_integrity)} external scripts without integrity check')
            issues['score'] -= 10

        # Check for inline event handlers (XSS risk)
        inline_events = re.findall(r'on\w+\s*=', content, re.IGNORECASE)
        if inline_events:
            issues['warning'].append(f'{len(inline_events)} inline event handlers found')
            issues['score'] -= 5

        # Check for eval() usage
        if 'eval(' in content:
            issues['critical'].append('eval() usage detected - XSS risk')
            issues['score'] -= 20

        # Check for innerHTML usage without sanitization
        if 'innerHTML' in content and 'DOMPurify' not in content:
            issues['warning'].append('innerHTML usage without apparent sanitization')
            issues['score'] -= 8

        return issues

    def generate_audit_report(self):
        """Generate comprehensive audit report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.base_dir / f"qa_audit_report_{timestamp}.json"

        # Calculate summary statistics
        total_tools = len(self.audit_results['performance'])

        perf_scores = [data['score'] for data in self.audit_results['performance'].values()]
        sec_scores = [data['score'] for data in self.audit_results['security'].values()]

        avg_perf_score = sum(perf_scores) / len(perf_scores) if perf_scores else 0
        avg_sec_score = sum(sec_scores) / len(sec_scores) if sec_scores else 0

        self.audit_results['summary'] = {
            'total_tools_audited': total_tools,
            'average_performance_score': round(avg_perf_score, 2),
            'average_security_score': round(avg_sec_score, 2),
            'tools_needing_performance_attention': len([s for s in perf_scores if s < 80]),
            'tools_needing_security_attention': len([s for s in sec_scores if s < 80]),
            'audit_timestamp': timestamp
        }

        with open(report_file, 'w') as f:
            json.dump(self.audit_results, f, indent=2)

        print(f"📊 Audit report generated: {report_file}")
        print(f"🎯 Performance Average: {avg_perf_score:.1f}/100")
        print(f"🔒 Security Average: {avg_sec_score:.1f}/100")

    def apply_performance_optimizations(self):
        """Apply performance optimizations across tools"""
        print("⚡ Applying Performance Optimizations...")

        optimizations_applied = 0

        for tool_name, issues in self.audit_results['performance'].items():
            if issues['score'] < 80:  # Focus on tools with low performance scores
                tool_path = self.base_dir / tool_name / "index.html"

                if tool_path.exists():
                    try:
                        with open(tool_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        original_content = content

                        # Add font-display: swap to Google Fonts
                        if 'fonts.googleapis.com' in content and 'display=swap' not in content:
                            content = re.sub(
                                r'(https://fonts\.googleapis\.com/css2\?[^"\']*)',
                                r'\1&display=swap',
                                content
                            )

                        # Add preconnect for Google Fonts
                        if 'fonts.googleapis.com' in content and 'preconnect' not in content:
                            head_pattern = r'(<head[^>]*>)'
                            preconnect = r'\1\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                            content = re.sub(head_pattern, preconnect, content, count=1)

                        # Add async to external scripts where appropriate
                        content = re.sub(
                            r'<script src="(https?://[^"]*)"([^>]*)>',
                            r'<script src="\1" async\2>',
                            content
                        )

                        if content != original_content:
                            with open(tool_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            optimizations_applied += 1
                            self.audit_results['improvements'].append(f"Performance optimizations applied to {tool_name}")

                    except Exception as e:
                        print(f"❌ Error optimizing {tool_name}: {e}")

        print(f"⚡ Performance optimizations applied to {optimizations_applied} tools")

    def implement_security_enhancements(self):
        """Implement security enhancements across tools"""
        print("🔒 Implementing Security Enhancements...")

        enhancements_applied = 0

        for tool_name, issues in self.audit_results['security'].items():
            if issues['score'] < 80:  # Focus on tools with low security scores
                tool_path = self.base_dir / tool_name / "index.html"

                if tool_path.exists():
                    try:
                        with open(tool_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        original_content = content

                        # Add basic CSP if missing
                        if 'Content-Security-Policy' not in content:
                            head_pattern = r'(<head[^>]*>)'
                            csp_meta = r'\1\n<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; style-src \'self\' \'unsafe-inline\' fonts.googleapis.com; font-src fonts.gstatic.com; script-src \'self\' \'unsafe-inline\' www.googletagmanager.com; img-src \'self\' data:;">'
                            content = re.sub(head_pattern, csp_meta, content, count=1)

                        # Add X-Frame-Options if missing
                        if 'X-Frame-Options' not in content:
                            head_pattern = r'(<head[^>]*>)'
                            frame_options = r'\1\n<meta http-equiv="X-Frame-Options" content="DENY">'
                            content = re.sub(head_pattern, frame_options, content, count=1)

                        # Convert HTTP links to HTTPS (careful with this)
                        if 'http://' in content:
                            # Only convert common resources, not arbitrary links
                            content = re.sub(r'http://(fonts\.googleapis\.com|fonts\.gstatic\.com)', r'https://\1', content)

                        if content != original_content:
                            with open(tool_path, 'w', encoding='utf-8') as f:
                                f.write(content)
                            enhancements_applied += 1
                            self.audit_results['improvements'].append(f"Security enhancements applied to {tool_name}")

                    except Exception as e:
                        print(f"❌ Error enhancing {tool_name}: {e}")

        print(f"🔒 Security enhancements applied to {enhancements_applied} tools")

def main():
    """Main execution function"""
    print("🚀 Starting QA Agent Echo - Performance & Security Audit")

    qa_agent = QAAgentEcho()
    qa_agent.run_comprehensive_audit()

    print("\n✅ QA Agent Echo audit complete!")
    print(f"📊 Summary:")
    summary = qa_agent.audit_results['summary']
    print(f"   Tools Audited: {summary.get('total_tools_audited', 0)}")
    print(f"   Avg Performance Score: {summary.get('average_performance_score', 0)}/100")
    print(f"   Avg Security Score: {summary.get('average_security_score', 0)}/100")
    print(f"   Improvements Applied: {len(qa_agent.audit_results['improvements'])}")

if __name__ == "__main__":
    main()