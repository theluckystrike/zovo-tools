#!/usr/bin/env python3
"""
Agent 9 - Continuous Quality Gate
Focus: Tools U-Z, Fix duplicate canonical URLs and other violations
Runs for 2 hours straight, every 60 seconds
"""

import os
import re
import time
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

class Agent9QualityGate:
    def __init__(self):
        self.base_dir = Path("/Users/mike/zovo-workspaces/zovo-tools")
        self.loop_count = 0
        self.start_time = time.time()

    def get_uz_tools(self):
        """Get all tool directories U-Z"""
        all_dirs = [d for d in os.listdir(self.base_dir) if os.path.isdir(self.base_dir / d)]
        uz_tools = [d for d in all_dirs if d[0].lower() in 'uvwxyz']
        return sorted(uz_tools)

    def pull_repos(self):
        """Pull latest from repos"""
        try:
            # Pull zovo-tools
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ Pulled zovo-tools")
            else:
                print("❌ Failed to pull zovo-tools")

            # Pull quality-pipeline if it exists
            quality_pipeline = Path("/Users/mike/zovo-workspaces/quality-pipeline")
            if quality_pipeline.exists():
                result = subprocess.run(
                    ['git', 'pull', 'origin', 'main'],
                    cwd=quality_pipeline,
                    capture_output=True,
                    text=True
                )
        except Exception as e:
            print(f"Pull error: {e}")

    def fix_duplicate_canonicals(self, file_path):
        """Fix duplicate canonical URLs in HTML files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Pattern to match duplicate canonical URLs
            # Keep the first one that contains tools.zovo.one, remove others
            lines = content.split('\n')
            canonical_found = False
            fixed_lines = []

            for line in lines:
                if 'rel="canonical"' in line:
                    if not canonical_found and 'tools.zovo.one' in line:
                        fixed_lines.append(line)
                        canonical_found = True
                    elif not canonical_found:
                        # Keep first canonical even if not tools.zovo.one
                        fixed_lines.append(line)
                        canonical_found = True
                    # Skip subsequent canonical lines
                else:
                    fixed_lines.append(line)

            content = '\n'.join(fixed_lines)

            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True

        except Exception as e:
            print(f"Error fixing canonicals in {file_path}: {e}")

        return False

    def check_and_fix_violations(self, tool_dir):
        """Check and fix violations in a tool directory"""
        violations_fixed = 0
        html_file = tool_dir / 'index.html'

        if html_file.exists():
            # Fix duplicate canonicals
            if self.fix_duplicate_canonicals(html_file):
                violations_fixed += 1
                print(f"  Fixed duplicate canonicals in {tool_dir.name}")

            # Check for other content violations
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                original_content = content

                # Fix em-dashes
                if '—' in content:
                    content = content.replace('—', '–')
                    violations_fixed += 1

                # Remove hashtags
                hashtag_pattern = re.compile(r'#[A-Za-z]\w*\s*')
                if hashtag_pattern.search(content):
                    content = hashtag_pattern.sub('', content)
                    violations_fixed += 1

                # Fix HTML bold tags
                bold_pattern = re.compile(r'<b>(.*?)</b>', re.IGNORECASE)
                if bold_pattern.search(content):
                    content = bold_pattern.sub(r'\1', content)
                    violations_fixed += 1

                strong_pattern = re.compile(r'<strong>(.*?)</strong>', re.IGNORECASE)
                if strong_pattern.search(content):
                    content = strong_pattern.sub(r'\1', content)
                    violations_fixed += 1

                # Fix AI phrases
                ai_replacements = {
                    'AI-powered': 'Advanced',
                    'AI powered': 'Advanced',
                    'artificial intelligence': 'smart technology',
                    'machine learning': 'data analysis',
                    'ML-based': 'data-driven',
                    'powered by AI': 'powered by advanced algorithms',
                    'AI-driven': 'algorithm-driven',
                    'AI driven': 'algorithm driven',
                    'Claude': '',
                    'Anthropic': ''
                }

                for ai_phrase, replacement in ai_replacements.items():
                    if ai_phrase in content:
                        content = content.replace(ai_phrase, replacement)
                        violations_fixed += 1

                # Ensure author is Michael Lip
                wrong_author_pattern = re.compile(
                    r'(?<!Michael )(?<!Michael Lip )\b[A-Z][a-z]+ [A-Z][a-z]+\b(?=.*(?:author|written by|created by))',
                    re.IGNORECASE
                )
                if wrong_author_pattern.search(content):
                    content = wrong_author_pattern.sub('Michael Lip', content)
                    violations_fixed += 1

                # Write back if changes were made
                if content != original_content:
                    with open(html_file, 'w', encoding='utf-8') as f:
                        f.write(content)

            except Exception as e:
                print(f"Error checking violations in {tool_dir}: {e}")

        return violations_fixed

    def run_quality_scan(self):
        """Run quality scan on all U-Z tools"""
        uz_tools = self.get_uz_tools()
        total_violations = 0

        print(f"🔍 Scanning {len(uz_tools)} U-Z tools...")

        for tool_name in uz_tools:
            tool_dir = self.base_dir / tool_name
            if tool_dir.exists():
                violations = self.check_and_fix_violations(tool_dir)
                if violations > 0:
                    total_violations += violations
                    print(f"  ⚠️  {tool_name}: Fixed {violations} violations")

        return total_violations

    def commit_and_push(self, violations_fixed):
        """Commit and push changes if any were made"""
        if violations_fixed == 0:
            return False

        try:
            # Check if there are changes
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )

            if not result.stdout.strip():
                return False

            timestamp = datetime.now().strftime("%H:%M:%S")
            commit_msg = f"Quality Gate Loop {self.loop_count} ({timestamp}): Fixed {violations_fixed} violations in U-Z tools"

            # Add all changes
            subprocess.run(['git', 'add', '-A'], cwd=self.base_dir, capture_output=True)

            # Commit
            subprocess.run(['git', 'commit', '-m', commit_msg], cwd=self.base_dir, capture_output=True)

            # Push
            result = subprocess.run(['git', 'push', 'origin', 'main'], cwd=self.base_dir, capture_output=True)

            if result.returncode == 0:
                print(f"✅ Committed and pushed: {commit_msg}")
                return True
            else:
                print(f"❌ Push failed: {result.stderr}")
                return False

        except Exception as e:
            print(f"Commit/push error: {e}")
            return False

    def run_continuous_loop(self):
        """Run continuous quality gate for 2 hours"""
        print("🚀 Starting Agent 9 - Continuous Quality Gate")
        print("Focus: Tools U-Z (duplicate canonicals, content violations)")
        print("Duration: 2 hours | Interval: 60 seconds")
        print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
        print("-" * 60)

        target_end_time = self.start_time + (2 * 60 * 60)  # 2 hours

        while time.time() < target_end_time:
            self.loop_count += 1
            loop_start = time.time()
            remaining_minutes = (target_end_time - time.time()) / 60

            print(f"\n🔄 LOOP {self.loop_count} - {datetime.now().strftime('%H:%M:%S')} ({remaining_minutes:.0f}min remaining)")

            # 1. Pull latest
            print("📡 Pulling latest...")
            self.pull_repos()

            # 2. Scan and fix
            violations_fixed = self.run_quality_scan()

            # 3. Commit and push
            if violations_fixed > 0:
                self.commit_and_push(violations_fixed)
            else:
                print("✅ No violations found - clean scan")

            # 4. Wait for next cycle
            elapsed = time.time() - loop_start
            remaining_time = target_end_time - time.time()

            if remaining_time > 60:
                sleep_time = max(0, 60 - elapsed)
                if sleep_time > 0:
                    print(f"😴 Sleeping {sleep_time:.1f}s until next loop...")
                    time.sleep(sleep_time)
            else:
                print("⏰ Approaching end time...")
                break

        total_runtime = (time.time() - self.start_time) / 60
        print(f"\n🏁 Quality Gate Complete!")
        print(f"Loops: {self.loop_count} | Runtime: {total_runtime:.1f} minutes")
        print("✅ U-Z tools quality monitoring finished")

if __name__ == "__main__":
    gate = Agent9QualityGate()
    gate.run_continuous_loop()