#!/usr/bin/env python3
"""
Continuous Quality Gate Scanner for Tools U-Z
Agent 9 - Detects and fixes violations before Google indexes them
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
        self.bold_pattern = re.compile(r'\*\*[^*]+\*\*|<b>.*?</b>|<strong>.*?</strong>', re.IGNORECASE)
        self.em_dash_pattern = re.compile(r'—')
        self.hashtag_pattern = re.compile(r'(?<![&=:;"\'/])#[A-Za-z]\w*(?![A-Fa-f0-9])')
        self.ai_phrases = [
            'AI-powered', 'AI powered', 'artificial intelligence',
            'machine learning', 'ML-based', 'powered by AI',
            'AI-driven', 'AI driven', 'smart algorithm', 'Claude', 'Anthropic'
        ]
        self.wrong_author_pattern = re.compile(r'(?!Michael Lip)\b[A-Z][a-z]+ [A-Z][a-z]+\b(?=.*(?:author|written by|created by))', re.IGNORECASE)

    def get_uz_tools(self):
        """Get all tool directories U-Z"""
        all_dirs = [d for d in os.listdir(self.base_dir) if os.path.isdir(os.path.join(self.base_dir, d))]
        uz_tools = [d for d in all_dirs if d[0].lower() in 'uvwxyz']
        return sorted(uz_tools)

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

            # Check for wrong author attribution
            if self.wrong_author_pattern.search(content):
                violations.append('wrong_author')

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

            # Fix bold text (both markdown and HTML)
            if 'bold_text' in violations:
                # Remove markdown bold
                content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
                # Remove HTML bold tags
                content = re.sub(r'<b>(.*?)</b>', r'\1', content, flags=re.IGNORECASE)
                content = re.sub(r'<strong>(.*?)</strong>', r'\1', content, flags=re.IGNORECASE)

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
                        'smart algorithm': 'intelligent system',
                        'Claude': '',
                        'Anthropic': ''
                    }
                    if phrase in replacements:
                        content = content.replace(phrase, replacements[phrase])

            # Fix wrong author attribution
            if 'wrong_author' in violations:
                content = self.wrong_author_pattern.sub('Michael Lip', content)

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
        """Run complete quality scan on U-Z tools"""
        print(f"🔍 Quality Gate - Scanning Tools U-Z at {time.strftime('%H:%M:%S')}")

        uz_tools = self.get_uz_tools()
        print(f"Found {len(uz_tools)} tools to scan")

        total_violations_fixed = 0

        for tool in uz_tools:
            if self.scan_tool(tool):
                total_violations_fixed += 1
                self.violations_found = True

        print(f"✅ Quality scan complete. Fixed violations in {total_violations_fixed} tools")
        return total_violations_fixed > 0

if __name__ == "__main__":
    scanner = QualityGate("/Users/mike/zovo-workspaces/zovo-tools")
    scanner.run_quality_scan()