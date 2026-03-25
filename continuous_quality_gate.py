#!/usr/bin/env python3
"""
Continuous Quality Gate - Agent 18
Runs quality checks every 60 seconds for 2 hours straight
Focus: Tools O-T and articles directory
"""

import os
import subprocess
import time
import glob
import re
from datetime import datetime, timedelta

class ContinuousQualityGate:
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(hours=2)
        self.loop_count = 0
        self.violations_fixed = 0
        self.seo_gaps_fixed = 0

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")

    def run_command(self, command, description=""):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                self.log(f"✓ {description}: Success")
                return result.stdout
            else:
                self.log(f"✗ {description}: {result.stderr}")
                return None
        except Exception as e:
            self.log(f"✗ {description}: Exception {str(e)}")
            return None

    def pull_latest_changes(self):
        self.log("Pulling latest changes from repo...")
        return self.run_command("git pull", "Git pull")

    def get_ot_tools_and_articles(self):
        """Get all HTML files from tools O-T and articles directory"""
        html_files = []

        # Get tools O-T
        for letter in 'opqrst':
            pattern = f"{letter}*/*.html"
            files = glob.glob(pattern)
            html_files.extend(files)

        # Get all article HTML files
        article_files = glob.glob("articles/*/*.html")
        html_files.extend(article_files)

        self.log(f"Found {len(html_files)} HTML files to check")
        return html_files

    def scan_ai_violations(self, file_path):
        """Scan for AI formatting violations"""
        violations = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for common AI formatting violations
            patterns = [
                (r'<div class="ai-', 'AI class names'),
                (r'claude|anthropic|assistant|ai-generated', 'AI mentions', re.IGNORECASE),
                (r'Co-Authored-By: Claude', 'AI attribution'),
                (r'<h1[^>]*>.*?</h1>.*?<h1[^>]*>', 'Multiple H1 tags'),
                (r'<title></title>', 'Empty title tag'),
                (r'<meta name="description" content=""\s*/>', 'Empty meta description'),
                (r'<p>\s*</p>', 'Empty paragraph tags'),
                (r'style="[^"]*color:\s*#[0-9a-f]{6}[^"]*"', 'Inline color styles'),
            ]

            for pattern, description, *flags in patterns:
                flag = flags[0] if flags else 0
                matches = re.findall(pattern, content, flag)
                if matches:
                    violations.append((description, len(matches)))

        except Exception as e:
            self.log(f"Error scanning {file_path}: {str(e)}")

        return violations

    def fix_violations(self, file_path, violations):
        """Fix common violations"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Fix empty paragraphs
            content = re.sub(r'<p>\s*</p>', '', content)

            # Fix multiple H1 tags (keep first, convert others to H2)
            h1_matches = list(re.finditer(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL))
            if len(h1_matches) > 1:
                for i, match in enumerate(h1_matches[1:], 1):
                    old_h1 = match.group(0)
                    new_h2 = old_h1.replace('<h1', '<h2').replace('</h1>', '</h2>')
                    content = content.replace(old_h1, new_h2, 1)

            # Remove AI mentions
            ai_patterns = [
                (r'claude|anthropic|assistant|ai-generated', '', re.IGNORECASE),
                (r'Co-Authored-By: Claude[^\n]*\n?', ''),
            ]

            for pattern, replacement, *flags in ai_patterns:
                flag = flags[0] if flags else 0
                content = re.sub(pattern, replacement, content, flags=flag)

            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.violations_fixed += 1
                return True

        except Exception as e:
            self.log(f"Error fixing {file_path}: {str(e)}")

        return False

    def check_seo_elements(self, file_path):
        """Check for missing SEO elements"""
        gaps = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for required SEO elements
            checks = [
                (r'<title>[^<]+</title>', 'Missing or empty title tag'),
                (r'<meta name="description" content="[^"]{50,160}"[^>]*>', 'Missing or poor meta description'),
                (r'<meta property="og:title"', 'Missing OG title'),
                (r'<meta property="og:description"', 'Missing OG description'),
                (r'<meta name="robots"', 'Missing robots meta tag'),
                (r'<link rel="canonical"', 'Missing canonical tag'),
                (r'"@type": "WebPage"', 'Missing schema markup'),
            ]

            for pattern, description in checks:
                if not re.search(pattern, content):
                    gaps.append(description)

        except Exception as e:
            self.log(f"Error checking SEO for {file_path}: {str(e)}")

        return gaps

    def fix_seo_gaps(self, file_path, gaps):
        """Fix basic SEO gaps"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            modified = False

            # Extract filename for fallback content
            filename = os.path.basename(file_path).replace('.html', '')
            tool_name = filename.replace('-', ' ').title()

            # Add missing robots tag
            if 'Missing robots meta tag' in gaps:
                robots_tag = '<meta name="robots" content="index, follow">'
                if '<meta name="viewport"' in content:
                    content = content.replace('<meta name="viewport"', f'{robots_tag}\n    <meta name="viewport"')
                    modified = True

            # Add basic canonical tag if missing
            if 'Missing canonical tag' in gaps and 'tools.zovo.one' not in content:
                canonical_url = f"https://tools.zovo.one/{filename}/"
                canonical_tag = f'<link rel="canonical" href="{canonical_url}">'
                if '</head>' in content:
                    content = content.replace('</head>', f'    {canonical_tag}\n</head>')
                    modified = True

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.seo_gaps_fixed += 1
                return True

        except Exception as e:
            self.log(f"Error fixing SEO gaps for {file_path}: {str(e)}")

        return False

    def advanced_quality_checks(self):
        """Run advanced quality checks when no violations found"""
        self.log("Running advanced quality checks...")

        # Check articles index page currency
        index_path = "articles/index.html"
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                index_content = f.read()

            # Count articles in directory vs index
            article_dirs = [d for d in os.listdir('articles') if os.path.isdir(f'articles/{d}')]
            index_links = len(re.findall(r'<a[^>]*href="[^"]*"', index_content))

            if len(article_dirs) != index_links:
                self.log(f"⚠ Articles index mismatch: {len(article_dirs)} dirs vs {index_links} links")

        # Check for thin articles (under 1500 words)
        thin_articles = []
        for article_dir in glob.glob("articles/*/"):
            html_file = os.path.join(article_dir, "index.html")
            if os.path.exists(html_file):
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                word_count = len(re.findall(r'\b\w+\b', re.sub(r'<[^>]+>', '', content)))
                if word_count < 1500:
                    thin_articles.append((article_dir, word_count))

        if thin_articles:
            self.log(f"⚠ Found {len(thin_articles)} thin articles")

        return len(thin_articles) == 0

    def commit_and_push_changes(self):
        """Commit and push any changes"""
        status = self.run_command("git status --porcelain", "Git status check")

        if status and status.strip():
            # Add only HTML files that were modified
            self.run_command("git add *.html */*.html */*/*.html", "Add HTML files")

            commit_msg = f"Quality gate fixes: {self.violations_fixed} violations, {self.seo_gaps_fixed} SEO gaps"
            self.run_command(f'git commit -m "{commit_msg}"', "Commit changes")
            self.run_command("git push", "Push changes")

            self.log(f"✓ Committed and pushed fixes")
            return True
        else:
            self.log("No changes to commit")
            return False

    def run_quality_loop(self):
        """Run one iteration of the quality loop"""
        self.loop_count += 1
        self.log(f"=== QUALITY LOOP {self.loop_count} ===")

        # Reset counters for this loop
        loop_violations = 0
        loop_seo_gaps = 0

        # Step 1: Pull latest changes
        self.pull_latest_changes()

        # Step 2: Get files to check (O-T tools + articles)
        html_files = self.get_ot_tools_and_articles()

        # Step 3: Scan and fix violations
        for file_path in html_files:
            violations = self.scan_ai_violations(file_path)
            if violations:
                self.log(f"Found violations in {file_path}: {violations}")
                if self.fix_violations(file_path, violations):
                    loop_violations += 1

            # Step 4: Check and fix SEO gaps
            seo_gaps = self.check_seo_elements(file_path)
            if seo_gaps:
                self.log(f"Found SEO gaps in {file_path}: {seo_gaps}")
                if self.fix_seo_gaps(file_path, seo_gaps):
                    loop_seo_gaps += 1

        # Step 5: Advanced checks if no issues found
        if loop_violations == 0 and loop_seo_gaps == 0:
            self.advanced_quality_checks()

        # Step 6: Commit and push changes
        if loop_violations > 0 or loop_seo_gaps > 0:
            self.commit_and_push_changes()

        self.log(f"Loop {self.loop_count} complete: {loop_violations} files fixed, {loop_seo_gaps} SEO fixes")

    def run_continuous_monitoring(self):
        """Run the continuous monitoring loop for 2 hours"""
        self.log("Starting continuous quality gate monitoring for 2 hours...")
        self.log(f"Focus area: Tools O-T and articles directory")
        self.log(f"End time: {self.end_time.strftime('%H:%M:%S')}")

        while datetime.now() < self.end_time:
            try:
                self.run_quality_loop()

                # Calculate time remaining
                time_left = self.end_time - datetime.now()
                minutes_left = int(time_left.total_seconds() / 60)

                self.log(f"Quality check complete. {minutes_left} minutes remaining. Sleeping 60 seconds...")

                if datetime.now() < self.end_time:
                    time.sleep(60)

            except KeyboardInterrupt:
                self.log("Interrupted by user")
                break
            except Exception as e:
                self.log(f"Error in quality loop: {str(e)}")
                time.sleep(60)

        self.log("=== CONTINUOUS QUALITY GATE COMPLETE ===")
        self.log(f"Total loops: {self.loop_count}")
        self.log(f"Total violations fixed: {self.violations_fixed}")
        self.log(f"Total SEO gaps fixed: {self.seo_gaps_fixed}")

if __name__ == "__main__":
    gate = ContinuousQualityGate()
    gate.run_continuous_monitoring()
