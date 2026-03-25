#!/usr/bin/env python3
"""
Continuous Quality Gate Scanner for Tools G-N
Agent 2 - Detects and fixes violations before Google indexes them
"""

import os
import re
import glob
import subprocess
import time
from pathlib import Path

class QualityGate:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.violations_found = False

        # Violation patterns
        self.bold_pattern = re.compile(r'\*\*[^*]+\*\*')
        self.em_dash_pattern = re.compile(r'—')
        self.hashtag_pattern = re.compile(r'#[A-Za-z]\w*')
        self.ai_phrases = [
            'AI-powered', 'AI powered', 'artificial intelligence',
            'machine learning', 'ML-based', 'powered by AI',
            'AI-driven', 'AI driven', 'smart algorithm'
        ]

    def get_gn_tools(self):
        """Get all tool directories G-N"""
        all_dirs = [d for d in os.listdir(self.base_dir) if os.path.isdir(os.path.join(self.base_dir, d))]
        gn_tools = [d for d in all_dirs if d[0].lower() in 'ghijklmn']
        return sorted(gn_tools)

    def scan_file_violations(self, filepath):
        """Scan a file for content violations"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            violations = []

            # Check for bold text
            if self.bold_pattern.search(content):
                violations.append('bold_text')

            # Check for em-dashes
            if self.em_dash_pattern.search(content):
                violations.append('em_dash')

            # Check for hashtags
            if self.hashtag_pattern.search(content):
                violations.append('hashtags')

            # Check for AI phrases
            content_lower = content.lower()
            for phrase in self.ai_phrases:
                if phrase.lower() in content_lower:
                    violations.append(f'ai_phrase: {phrase}')

            return violations

        except Exception as e:
            print(f"Error scanning {filepath}: {e}")
            return []

    def check_seo_gaps(self, tool_dir):
        """Check for SEO gaps in tool HTML"""
        index_path = tool_dir / 'index.html'
        if not index_path.exists():
            return ['missing_index_html']

        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()

            gaps = []

            if '<link rel="canonical"' not in content:
                gaps.append('missing_canonical')

            if 'property="og:' not in content:
                gaps.append('missing_og_tags')

            if '"application/ld+json"' not in content:
                gaps.append('missing_schema')

            if '<meta name="description"' not in content:
                gaps.append('missing_meta_description')

            if '<nav' not in content:
                gaps.append('missing_navbar')

            return gaps

        except Exception as e:
            print(f"Error checking SEO for {tool_dir}: {e}")
            return []

    def fix_content_violations(self, filepath, violations):
        """Fix content violations in file"""
        if not violations:
            return False

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Fix bold text
            if 'bold_text' in violations:
                content = self.bold_pattern.sub(lambda m: m.group(0)[2:-2], content)

            # Fix em-dashes
            if 'em_dash' in violations:
                content = self.em_dash_pattern.sub('–', content)

            # Fix hashtags (remove them)
            if 'hashtags' in violations:
                content = self.hashtag_pattern.sub('', content)

            # Fix AI phrases
            for violation in violations:
                if violation.startswith('ai_phrase:'):
                    phrase = violation.split(': ')[1]
                    # Replace with neutral alternatives
                    replacements = {
                        'AI-powered': 'Advanced',
                        'AI powered': 'Advanced',
                        'artificial intelligence': 'smart technology',
                        'machine learning': 'data analysis',
                        'ML-based': 'data-driven',
                        'powered by AI': 'powered by advanced algorithms',
                        'AI-driven': 'algorithm-driven',
                        'AI driven': 'algorithm driven',
                        'smart algorithm': 'intelligent system'
                    }
                    if phrase in replacements:
                        content = content.replace(phrase, replacements[phrase])

            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True

        except Exception as e:
            print(f"Error fixing {filepath}: {e}")

        return False

    def scan_tool(self, tool_name):
        """Comprehensive scan of a single tool"""
        tool_dir = self.base_dir / tool_name
        if not tool_dir.exists():
            return

        print(f"Scanning {tool_name}...")

        # Scan all files in tool directory
        violations_found = False
        for file_path in tool_dir.rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.html', '.md', '.txt', '.json']:
                violations = self.scan_file_violations(file_path)
                if violations:
                    print(f"  Violations in {file_path.relative_to(self.base_dir)}: {violations}")
                    if self.fix_content_violations(file_path, violations):
                        print(f"  Fixed violations in {file_path.name}")
                        violations_found = True

        # Check SEO gaps
        seo_gaps = self.check_seo_gaps(tool_dir)
        if seo_gaps:
            print(f"  SEO gaps in {tool_name}: {seo_gaps}")
            # Note: SEO fixes would require more complex HTML manipulation

        return violations_found

    def run_quality_scan(self):
        """Run complete quality scan on G-N tools"""
        print(f"🔍 Quality Gate - Scanning Tools G-N at {time.strftime('%H:%M:%S')}")

        gn_tools = self.get_gn_tools()
        print(f"Found {len(gn_tools)} tools to scan")

        total_violations_fixed = 0

        for tool in gn_tools:
            if self.scan_tool(tool):
                total_violations_fixed += 1
                self.violations_found = True

        print(f"✅ Quality scan complete. Fixed violations in {total_violations_fixed} tools")
        return total_violations_fixed > 0

if __name__ == "__main__":
    scanner = QualityGate("/Users/mike/zovo-workspaces/zovo-tools")
    scanner.run_quality_scan()