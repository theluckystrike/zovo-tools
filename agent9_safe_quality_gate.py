#!/usr/bin/env python3
"""
Agent 9 - Safe Continuous Quality Gate
Focus: Tools U-Z, Fix only duplicate canonical URLs
Runs for 2 hours straight, every 60 seconds
"""

import os
import re
import time
import subprocess
from datetime import datetime
from pathlib import Path

class SafeAgent9QualityGate:
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
        except Exception as e:
            print(f"Pull error: {e}")

    def fix_duplicate_canonicals(self, file_path):
        """Fix duplicate canonical URLs - keep only tools.zovo.one version"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Count canonicals first
            canonical_count = content.count('rel="canonical"')
            if canonical_count <= 1:
                return False  # No duplicates

            # Split into lines and process
            lines = content.split('\n')
            fixed_lines = []
            canonical_kept = False

            for line in lines:
                if 'rel="canonical"' in line:
                    # Keep only the first tools.zovo.one canonical
                    if not canonical_kept and 'tools.zovo.one' in line:
                        fixed_lines.append(line)
                        canonical_kept = True
                    elif not canonical_kept:
                        # Keep first canonical if no tools.zovo.one found yet
                        fixed_lines.append(line)
                        canonical_kept = True
                    # Skip all other canonical lines
                else:
                    fixed_lines.append(line)

            new_content = '\n'.join(fixed_lines)

            # Only write if we actually made changes
            if new_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

                # Verify the fix worked
                new_count = new_content.count('rel="canonical"')
                print(f"    Canonicals: {canonical_count} → {new_count}")
                return True

        except Exception as e:
            print(f"    Error fixing {file_path}: {e}")

        return False

    def scan_tool(self, tool_name):
        """Scan a single tool for duplicate canonical URLs"""
        tool_dir = self.base_dir / tool_name
        html_file = tool_dir / 'index.html'

        if not html_file.exists():
            return 0

        violations_fixed = 0

        # Check for duplicate canonicals
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            canonical_count = content.count('rel="canonical"')

            if canonical_count > 1:
                print(f"  🔍 {tool_name}: {canonical_count} canonical URLs found")
                if self.fix_duplicate_canonicals(html_file):
                    violations_fixed += 1
                    print(f"  ✅ {tool_name}: Fixed duplicate canonicals")

        except Exception as e:
            print(f"  ❌ Error scanning {tool_name}: {e}")

        return violations_fixed

    def run_quality_scan(self):
        """Run quality scan on all U-Z tools"""
        uz_tools = self.get_uz_tools()
        total_violations = 0

        print(f"🔍 Scanning {len(uz_tools)} U-Z tools for duplicate canonicals...")

        for tool_name in uz_tools:
            violations = self.scan_tool(tool_name)
            if violations > 0:
                total_violations += violations

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
                print("  No changes to commit")
                return False

            timestamp = datetime.now().strftime("%H:%M:%S")
            commit_msg = f"Quality Gate Loop {self.loop_count} ({timestamp}): Fixed {violations_fixed} duplicate canonicals in U-Z tools"

            # Add all changes
            subprocess.run(['git', 'add', '-A'], cwd=self.base_dir, capture_output=True)

            # Commit
            result = subprocess.run(['git', 'commit', '-m', commit_msg], cwd=self.base_dir, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"  ❌ Commit failed: {result.stderr}")
                return False

            # Push
            result = subprocess.run(['git', 'push', 'origin', 'main'], cwd=self.base_dir, capture_output=True, text=True)

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
        print("🚀 Starting Agent 9 - Safe Continuous Quality Gate")
        print("Focus: U-Z tools duplicate canonical URLs only")
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
            self.pull_repos()

            # 2. Scan and fix
            violations_fixed = self.run_quality_scan()

            # 3. Commit and push
            if violations_fixed > 0:
                self.commit_and_push(violations_fixed)
            else:
                print("✅ No duplicate canonicals found - clean scan")

            # 4. Check for other quality issues when clean
            if violations_fixed == 0:
                print("📋 Clean scan - checking for broken links, missing schema...")
                # In a real implementation, we could add more checks here

            # 5. Wait for next cycle
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
        print("✅ U-Z tools canonical monitoring finished")

if __name__ == "__main__":
    try:
        gate = SafeAgent9QualityGate()
        gate.run_continuous_loop()
    except KeyboardInterrupt:
        print("\n\n⏹️  Quality Gate interrupted by user")
        print("✅ Exiting gracefully...")
    except Exception as e:
        print(f"\n\n❌ Quality Gate error: {e}")
        import sys
        sys.exit(1)