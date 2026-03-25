#!/usr/bin/env python3
"""
Continuous Quality Gate Coordinator - Agent 15
Master quality gate for ALL tools. Runs for 2 hours straight.
Coordinates with PM1/PM2 and other agents. Advanced violation detection.
"""

import os
import time
import subprocess
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from quality_gate import QualityGate
import glob
import re

class QualityMaster:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir)
        self.scanner = QualityGate(base_dir)
        self.total_violations_fixed = 0
        self.total_new_content = 0
        self.loop_stats = []

    def run_git_command(self, command):
        """Run git command in repo"""
        try:
            result = subprocess.run(
                f"cd {self.base_dir} && {command}",
                shell=True,
                capture_output=True,
                text=True
            )
            return result.returncode == 0, result.stdout.strip()
        except Exception as e:
            print(f"Git command failed: {e}")
            return False, ""

    def pull_latest(self):
        """Pull latest changes"""
        success, output = self.run_git_command("git pull origin main")
        if success:
            if "Already up to date" in output:
                return False, "Up to date"
            else:
                return True, f"Pulled: {output.count('files changed') + output.count('create mode')}"
        return False, "Pull failed"

    def commit_and_push(self, message):
        """Commit and push changes"""
        # Check for changes
        success, output = self.run_git_command("git status --porcelain")
        if not success or not output.strip():
            return False

        print(f"📝 Committing fixes...")

        # Stage all changes
        self.run_git_command("git add -A")

        # Commit
        full_message = f"{message}\n\nAuthor: Michael Lip"
        success, _ = self.run_git_command(f'git commit -m "{full_message}"')

        if success:
            # Push
            push_success, _ = self.run_git_command("git push origin main")
            if push_success:
                print("  ✅ Committed and pushed")
                return True
            else:
                print("  ⚠️ Committed but push failed")
                return True

        return False

    def get_all_tool_dirs(self):
        """Get ALL tool directories (not just U-Z)"""
        all_dirs = []
        for item in os.listdir(self.base_dir):
            item_path = self.base_dir / item
            if item_path.is_dir() and not item.startswith('.') and not item.endswith('.py'):
                all_dirs.append(item)
        return sorted(all_dirs)

    def advanced_quality_scan(self):
        """Advanced quality scan covering ALL tools"""
        print(f"🔍 Master Quality Scan - ALL TOOLS at {time.strftime('%H:%M:%S')}")

        all_tools = self.get_all_tool_dirs()
        print(f"Scanning {len(all_tools)} total tool directories")

        violations_fixed = 0
        new_content_detected = 0

        # Track recent modifications (likely from PM1/PM2)
        recent_threshold = datetime.now() - timedelta(minutes=5)

        for tool in all_tools:
            tool_path = self.base_dir / tool

            # Check if tool was recently modified (new content from PMs)
            try:
                mod_time = datetime.fromtimestamp(os.path.getmtime(tool_path))
                if mod_time > recent_threshold:
                    new_content_detected += 1
                    print(f"  🆕 New content detected: {tool}")
            except:
                pass

            # Scan for violations
            if self.scanner.scan_tool(tool):
                violations_fixed += 1

        self.total_violations_fixed += violations_fixed
        self.total_new_content += new_content_detected

        return violations_fixed, new_content_detected

    def verify_sitemap_consistency(self):
        """Verify sitemap matches actual files"""
        print("🗺️ Verifying sitemap consistency...")

        sitemap_path = self.base_dir / "sitemap.xml"
        if not sitemap_path.exists():
            print("  ❌ No sitemap.xml found")
            return []

        issues = []
        try:
            with open(sitemap_path, 'r') as f:
                sitemap_content = f.read()

            # Extract URLs from sitemap
            url_pattern = re.compile(r'<loc>(https://tools\.zovo\.one/[^<]+)</loc>')
            sitemap_urls = url_pattern.findall(sitemap_content)

            # Check if corresponding directories exist
            for url in sitemap_urls:
                tool_slug = url.split('/')[-2] if url.endswith('/') else url.split('/')[-1]
                tool_path = self.base_dir / tool_slug
                if not tool_path.exists():
                    issues.append(f"Sitemap references non-existent tool: {tool_slug}")

            print(f"  ✅ Checked {len(sitemap_urls)} sitemap URLs")

        except Exception as e:
            print(f"  ❌ Error checking sitemap: {e}")

        return issues

    def check_orphaned_files(self):
        """Look for orphaned files or incomplete tools"""
        print("🔍 Checking for orphaned files...")

        issues = []
        all_tools = self.get_all_tool_dirs()

        for tool in all_tools:
            tool_path = self.base_dir / tool
            index_path = tool_path / "index.html"

            if not index_path.exists():
                issues.append(f"Missing index.html: {tool}")
                continue

            # Check for minimal content requirements
            try:
                with open(index_path, 'r') as f:
                    content = f.read()

                if len(content) < 1000:  # Very small files might be incomplete
                    issues.append(f"Suspiciously small index.html: {tool} ({len(content)} chars)")

                if "<title>" not in content:
                    issues.append(f"Missing title tag: {tool}")

            except Exception as e:
                issues.append(f"Error reading {tool}/index.html: {e}")

        return issues

    def deep_quality_checks(self):
        """Run deep quality checks when no basic violations found"""
        print("🔎 Running deep quality analysis...")

        issues_found = []

        # Sitemap consistency
        sitemap_issues = self.verify_sitemap_consistency()
        issues_found.extend(sitemap_issues)

        # Orphaned files
        orphan_issues = self.check_orphaned_files()
        issues_found.extend(orphan_issues)

        # Check articles index if it exists
        articles_index = self.base_dir / "articles" / "index.html"
        if articles_index.exists():
            print("  📰 Articles index found - checking freshness...")
            # Could add article index validation here

        if issues_found:
            print(f"  ⚠️ Found {len(issues_found)} deep issues:")
            for issue in issues_found[:5]:  # Show first 5
                print(f"    - {issue}")

        return len(issues_found)

    def generate_progress_report(self, loop_count):
        """Generate progress report every 10 loops"""
        if loop_count % 10 == 0:
            print("\n" + "="*60)
            print(f"📊 PROGRESS REPORT - Loop {loop_count}")
            print("="*60)
            print(f"Total violations fixed: {self.total_violations_fixed}")
            print(f"New content detected: {self.total_new_content}")

            if len(self.loop_stats) >= 10:
                recent_stats = self.loop_stats[-10:]
                avg_violations = sum(s['violations'] for s in recent_stats) / 10
                avg_new_content = sum(s['new_content'] for s in recent_stats) / 10
                print(f"Avg violations/loop (last 10): {avg_violations:.1f}")
                print(f"Avg new content/loop (last 10): {avg_new_content:.1f}")

            print("="*60)
            print()

def main():
    print("🚀 Starting Master Quality Gate Coordinator - Agent 15")
    print("Mission: Master quality gate covering ALL tools")
    print("Coordinates with PM1/PM2 and catches all violations")
    print("Duration: 2 hours continuous monitoring")
    print("Interval: 60 seconds between scans")
    print("-" * 70)

    # Initialize master quality coordinator
    master = QualityMaster("/Users/mike/zovo-workspaces/zovo-tools")

    # Run for 2 hours
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=2)
    loop_count = 0

    print(f"🕐 Started at: {start_time.strftime('%H:%M:%S')}")
    print(f"🕐 Will end at: {end_time.strftime('%H:%M:%S')}")
    print()

    while datetime.now() < end_time:
        loop_count += 1
        current_time = datetime.now()
        remaining = end_time - current_time

        print(f"🔄 Master Loop {loop_count} - {current_time.strftime('%H:%M:%S')} - {remaining.total_seconds()//60:.0f}min remaining")

        # Pull latest changes first
        pull_success, pull_msg = master.pull_latest()
        if pull_success:
            print(f"📡 {pull_msg}")

        # Run comprehensive quality scan
        violations_fixed, new_content = master.advanced_quality_scan()

        # Record stats
        master.loop_stats.append({
            'loop': loop_count,
            'time': current_time,
            'violations': violations_fixed,
            'new_content': new_content
        })

        if violations_fixed > 0:
            # Commit and push fixes
            commit_msg = f"Quality Gate Master Loop {loop_count}: Fixed {violations_fixed} violations across ALL tools"
            if master.commit_and_push(commit_msg):
                print(f"✅ Committed {violations_fixed} violation fixes")
        else:
            # Run deep quality checks
            deep_issues = master.deep_quality_checks()
            if deep_issues > 0:
                print(f"🔎 Found {deep_issues} deep quality issues")

        # Generate progress reports
        master.generate_progress_report(loop_count)

        print(f"✅ Master Loop {loop_count} complete")
        print()

        # Sleep for 60 seconds
        if datetime.now() + timedelta(seconds=60) < end_time:
            print("😴 Sleeping 60 seconds...")
            time.sleep(60)
        else:
            break

    final_time = datetime.now()
    total_duration = final_time - start_time

    print("\n🎯 Master Quality Gate Complete!")
    print("="*60)
    print(f"📊 Total loops: {loop_count}")
    print(f"⏱️ Total duration: {total_duration.total_seconds()//60:.0f} minutes")
    print(f"🔧 Total violations fixed: {master.total_violations_fixed}")
    print(f"🆕 New content detected: {master.total_new_content}")
    print(f"🎯 Mission: Master quality coordination across ALL tools")
    print("✅ Quality monitoring complete - ecosystem secured")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Master Quality Gate interrupted by user")
        print("✅ Exiting gracefully...")
    except Exception as e:
        print(f"\n\n❌ Master Quality Gate error: {e}")
        sys.exit(1)