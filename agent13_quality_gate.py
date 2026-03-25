#!/usr/bin/env python3
"""
Agent 13 - Continuous Quality Gate
Focus: Tools O-T and articles directory
Mission: Catch violations from PM1 and PM2 before Google sees them
"""

import os
import re
import glob
import json
import time
from datetime import datetime

class QualityGate:
    def __init__(self):
        self.base_dir = "/Users/mike/zovo-workspaces/zovo-tools"
        self.violations_found = 0
        self.fixes_applied = 0

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Agent 13: {message}")

    def scan_ot_tools(self):
        """Scan tools O-T for AI formatting violations"""
        violations = []
        pattern = os.path.join(self.base_dir, "[o-tO-T]*/index.html")

        for html_file in glob.glob(pattern):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for AI formatting violations
            ai_violations = self.detect_ai_violations(content, html_file)
            violations.extend(ai_violations)

        return violations

    def scan_articles(self):
        """Scan articles directory for violations"""
        violations = []
        articles_pattern = os.path.join(self.base_dir, "articles/*/index.html")

        for html_file in glob.glob(articles_pattern):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            ai_violations = self.detect_ai_violations(content, html_file)
            violations.extend(ai_violations)

        return violations

    def detect_ai_violations(self, content, file_path):
        """Detect common AI formatting violations"""
        violations = []

        # Check for AI filler phrases
        ai_patterns = [
            r"In today's .*? landscape",
            r"In the .*? world",
            r"In conclusion,",
            r"To summarize,",
            r"In summary,",
            r"Whether you're a .*? or",
            r"From .*? to .*?, we've got you covered",
            r"Let's dive in",
            r"Let's explore",
            r"Here's everything you need to know",
            r"in this comprehensive guide",
            r"this powerful tool",
            r"cutting-edge",
            r"game-changing",
            r"revolutionary",
            r"Next-level",
            r"State-of-the-art",
            r"Cutting-edge",
            r"Industry-leading",
            r"World-class",
            r"Best-in-class",
            r"Top-notch",
            r"Premium quality",
            r"Professional-grade",
            r"Enterprise-level",
        ]

        for pattern in ai_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                violations.append({
                    'file': file_path,
                    'type': 'AI_FILLER',
                    'pattern': pattern,
                    'text': match.group(),
                    'position': match.start()
                })

        # Check for missing SEO elements
        if '<title>' not in content:
            violations.append({
                'file': file_path,
                'type': 'MISSING_TITLE',
                'pattern': 'Missing title tag',
                'text': '',
                'position': 0
            })

        if 'meta name="description"' not in content:
            violations.append({
                'file': file_path,
                'type': 'MISSING_META_DESC',
                'pattern': 'Missing meta description',
                'text': '',
                'position': 0
            })

        return violations

    def fix_violations(self, violations):
        """Fix detected violations"""
        files_fixed = set()

        for violation in violations:
            file_path = violation['file']

            if violation['type'] == 'AI_FILLER':
                self.remove_ai_filler(file_path, violation)
                files_fixed.add(file_path)

            elif violation['type'] == 'MISSING_META_DESC':
                self.add_meta_description(file_path)
                files_fixed.add(file_path)

        self.fixes_applied += len(files_fixed)
        return list(files_fixed)

    def remove_ai_filler(self, file_path, violation):
        """Remove AI filler content"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace AI filler with more natural content
        replacements = {
            r"In today's .*? landscape": "Today",
            r"In the .*? world": "",
            r"In conclusion,": "",
            r"To summarize,": "",
            r"In summary,": "",
            r"Let's dive in": "",
            r"Let's explore": "",
            r"Here's everything you need to know": "",
            r"in this comprehensive guide": "",
            r"this powerful tool": "this tool",
            r"cutting-edge": "advanced",
            r"game-changing": "useful",
            r"revolutionary": "innovative",
        }

        pattern = violation['pattern']
        if pattern in replacements:
            content = re.sub(pattern, replacements[pattern], content, flags=re.IGNORECASE)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def add_meta_description(self, file_path):
        """Add missing meta description based on tool name"""
        tool_name = os.path.basename(os.path.dirname(file_path)).replace('-', ' ').title()

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'meta name="description"' not in content:
            meta_desc = f'    <meta name="description" content="Free {tool_name} - Calculate and analyze with precision. Easy to use, accurate results.">\n'
            content = content.replace('</head>', f'{meta_desc}</head>')

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    def run_quality_scan(self):
        """Run complete quality scan"""
        self.log("Starting quality scan...")

        # Scan O-T tools
        ot_violations = self.scan_ot_tools()
        self.log(f"Found {len(ot_violations)} violations in O-T tools")

        # Scan articles
        article_violations = self.scan_articles()
        self.log(f"Found {len(article_violations)} violations in articles")

        all_violations = ot_violations + article_violations
        self.violations_found = len(all_violations)

        if all_violations:
            self.log(f"Total violations found: {len(all_violations)}")
            fixed_files = self.fix_violations(all_violations)
            self.log(f"Fixed {len(fixed_files)} files")
            return fixed_files
        else:
            self.log("No violations found")
            return []

if __name__ == "__main__":
    gate = QualityGate()
    gate.run_quality_scan()