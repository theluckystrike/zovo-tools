#!/usr/bin/env python3
"""
Agent 10: Master Quality Gate Coordinator
Continuous quality monitoring with advanced checks and cross-agent coordination
"""

import os
import re
import json
import subprocess
import time
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

class QualityGateCoordinator:
    def __init__(self):
        self.base_dir = Path('/Users/mike/zovo-workspaces/zovo-tools')
        self.violations_fixed = 0
        self.loops_completed = 0
        self.start_time = time.time()
        self.last_progress_report = time.time()

    def log(self, message):
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] AGENT 10: {message}")

    def run_git_command(self, cmd):
        """Execute git command safely"""
        try:
            result = subprocess.run(cmd, shell=True, cwd=self.base_dir,
                                  capture_output=True, text=True, timeout=30)
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            self.log(f"Git command timed out: {cmd}")
            return False, "", "Timeout"

    def pull_latest_changes(self):
        """Pull latest changes from other agents"""
        success, stdout, stderr = self.run_git_command("git pull origin main")
        if not success:
            self.log(f"Failed to pull: {stderr}")
        return success

    def push_fixes(self, message="Agent 10: Quality fixes"):
        """Push quality fixes"""
        self.run_git_command("git add .")
        success, _, _ = self.run_git_command(f'git commit -m "{message}"')
        if success:
            self.run_git_command("git push origin main")
            return True
        return False

    def scan_html_files(self):
        """Comprehensive HTML quality scan"""
        violations = []
        html_files = list(self.base_dir.glob("*/index.html"))

        for html_file in html_files:
            try:
                content = html_file.read_text(encoding='utf-8')
                tool_name = html_file.parent.name

                # Core quality checks
                issues = []

                # 1. Meta description check
                if 'meta name="description"' not in content:
                    issues.append("Missing meta description")
                elif len(re.findall(r'content="([^"]*)"', content)[0] if re.findall(r'content="([^"]*)"', content) else "") < 120:
                    issues.append("Meta description too short")

                # 2. Title check
                title_match = re.search(r'<title>([^<]+)</title>', content)
                if not title_match:
                    issues.append("Missing title tag")
                else:
                    title = title_match.group(1)
                    if not title.endswith(" | Free Online Tool"):
                        issues.append("Title doesn't end with '| Free Online Tool'")

                # 3. H1 check
                h1_matches = re.findall(r'<h1[^>]*>([^<]+)</h1>', content)
                if len(h1_matches) != 1:
                    issues.append(f"Should have exactly 1 H1, found {len(h1_matches)}")

                # 4. Schema markup check
                if 'application/ld+json' not in content:
                    issues.append("Missing schema markup")

                # 5. Canonical URL check
                if 'rel="canonical"' not in content:
                    issues.append("Missing canonical URL")

                # 6. Dark theme CSS check
                if 'body { background: #0a0a0f;' not in content:
                    issues.append("Missing dark theme CSS")

                # 7. Google Analytics check
                if 'G-XXXXXXXXXX' not in content:
                    issues.append("Missing Google Analytics")

                if issues:
                    violations.append({
                        'file': str(html_file),
                        'tool': tool_name,
                        'issues': issues
                    })

            except Exception as e:
                self.log(f"Error scanning {html_file}: {e}")

        return violations

    def advanced_ecosystem_checks(self):
        """Advanced checks for ecosystem health"""
        issues = []

        # 1. Count total directories
        tool_dirs = [d for d in self.base_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        self.log(f"Found {len(tool_dirs)} tool directories")

        # 2. Check for orphaned files
        orphaned_files = []
        for file in self.base_dir.glob("*.html"):
            if file.name not in ['index.html', 'sitemap.html']:
                orphaned_files.append(file)

        if orphaned_files:
            issues.append(f"Found {len(orphaned_files)} orphaned HTML files")

        # 3. Check for missing index.html files
        missing_index = []
        for tool_dir in tool_dirs:
            if not (tool_dir / "index.html").exists():
                missing_index.append(tool_dir.name)

        if missing_index:
            issues.append(f"Missing index.html in {len(missing_index)} tools: {missing_index[:5]}")

        # 4. Check for tools without proper naming
        invalid_names = []
        for tool_dir in tool_dirs:
            if not re.match(r'^[a-z0-9-]+$', tool_dir.name):
                invalid_names.append(tool_dir.name)

        if invalid_names:
            issues.append(f"Invalid directory names: {invalid_names}")

        return issues

    def fix_common_violations(self, violations):
        """Fix common quality violations automatically"""
        fixes_made = 0

        for violation in violations:
            try:
                html_file = Path(violation['file'])
                content = html_file.read_text(encoding='utf-8')
                original_content = content

                for issue in violation['issues']:
                    if "Missing meta description" in issue:
                        # Add basic meta description
                        tool_name = violation['tool'].replace('-', ' ').title()
                        meta_desc = f'<meta name="description" content="Free online {tool_name.lower()} tool. Calculate, convert, and analyze instantly with our user-friendly interface. No registration required - start using now.">'
                        content = re.sub(r'(<meta charset[^>]*>)', r'\1\n    ' + meta_desc, content)
                        fixes_made += 1

                    elif "Title doesn't end with" in issue:
                        # Fix title format
                        content = re.sub(r'<title>([^<]+)</title>',
                                       r'<title>\1 | Free Online Tool</title>', content)
                        fixes_made += 1

                    elif "Missing canonical URL" in issue:
                        # Add canonical URL
                        tool_name = violation['tool']
                        canonical = f'<link rel="canonical" href="https://tools.zovo.one/{tool_name}/">'
                        content = re.sub(r'(<meta name="description"[^>]*>)',
                                       r'\1\n    ' + canonical, content)
                        fixes_made += 1

                    elif "Missing Google Analytics" in issue:
                        # Add Google Analytics (placeholder)
                        ga_script = '''
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-XXXXXXXXXX');
    </script>'''
                        content = re.sub(r'</head>', ga_script + '\n</head>', content)
                        fixes_made += 1

                if content != original_content:
                    html_file.write_text(content, encoding='utf-8')
                    self.log(f"Fixed {violation['tool']}: {len(violation['issues'])} issues")

            except Exception as e:
                self.log(f"Error fixing {violation['file']}: {e}")

        return fixes_made

    def generate_progress_report(self):
        """Generate detailed progress report"""
        elapsed = time.time() - self.start_time
        elapsed_mins = elapsed / 60

        self.log("="*60)
        self.log(f"QUALITY COORDINATOR PROGRESS REPORT")
        self.log(f"Runtime: {elapsed_mins:.1f} minutes")
        self.log(f"Loops completed: {self.loops_completed}")
        self.log(f"Total violations fixed: {self.violations_fixed}")
        self.log(f"Average violations per loop: {self.violations_fixed/max(1,self.loops_completed):.1f}")
        self.log("="*60)

    def continuous_monitoring_loop(self, duration_hours=2):
        """Main continuous monitoring loop"""
        end_time = time.time() + (duration_hours * 3600)

        while time.time() < end_time:
            loop_start = time.time()
            self.loops_completed += 1

            self.log(f"Starting quality loop #{self.loops_completed}")

            # 1. Pull latest changes
            self.pull_latest_changes()

            # 2. Comprehensive scan
            violations = self.scan_html_files()

            # 3. Advanced ecosystem checks
            ecosystem_issues = self.advanced_ecosystem_checks()

            if violations:
                self.log(f"Found {len(violations)} files with quality violations")
                fixes = self.fix_common_violations(violations)
                self.violations_fixed += fixes

                if fixes > 0:
                    self.push_fixes(f"Agent 10: Fixed {fixes} quality violations in loop #{self.loops_completed}")
            else:
                self.log("No violations found - running advanced checks")
                if ecosystem_issues:
                    for issue in ecosystem_issues:
                        self.log(f"ECOSYSTEM ISSUE: {issue}")

            # 4. Progress report every 10 loops
            if self.loops_completed % 10 == 0:
                self.generate_progress_report()

            # 5. Wait for next cycle (60 seconds)
            loop_duration = time.time() - loop_start
            sleep_time = max(0, 60 - loop_duration)

            if sleep_time > 0:
                self.log(f"Loop completed in {loop_duration:.1f}s, sleeping {sleep_time:.1f}s until next cycle")
                time.sleep(sleep_time)
            else:
                self.log(f"Loop took {loop_duration:.1f}s (over 60s budget)")

if __name__ == "__main__":
    coordinator = QualityGateCoordinator()
    coordinator.continuous_monitoring_loop(2)