#!/usr/bin/env python3
"""
Agent 10: Real-time Quality Dashboard
Live monitoring and coordination dashboard
"""

import time
import subprocess
import re
from datetime import datetime
from pathlib import Path

class QualityDashboard:
    def __init__(self):
        self.base_dir = Path('/Users/mike/zovo-workspaces/zovo-tools')
        self.start_time = time.time()
        self.loop_count = 0

    def get_git_stats(self):
        """Get git repository statistics"""
        try:
            # Get recent commit count
            recent_commits = subprocess.run(
                ['git', 'log', '--since="1 hour ago"', '--oneline'],
                capture_output=True, text=True, cwd=self.base_dir
            ).stdout.count('\n')

            # Get changed files
            changed_files = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True, text=True, cwd=self.base_dir
            ).stdout.count('\n')

            return recent_commits, changed_files
        except:
            return 0, 0

    def get_quality_loop_stats(self):
        """Extract stats from quality loop output"""
        try:
            with open('/private/tmp/claude-501/-Users-mike/tasks/bpst798dp.output', 'r') as f:
                content = f.read()

            # Count total fixes
            total_fixes = content.count('Fixed')

            # Count loops
            loop_matches = re.findall(r'Starting quality loop #(\d+)', content)
            current_loop = int(loop_matches[-1]) if loop_matches else 0

            # Get recent activity (last 500 chars)
            recent_activity = content[-500:] if len(content) > 500 else content
            last_activity_time = re.findall(r'\[(\d{2}:\d{2}:\d{2})\]', recent_activity)
            last_time = last_activity_time[-1] if last_activity_time else "Unknown"

            return total_fixes, current_loop, last_time

        except Exception as e:
            return 0, 0, f"Error: {e}"

    def count_html_files(self):
        """Count HTML files in tool directories"""
        return len(list(self.base_dir.glob('*/index.html')))

    def display_dashboard(self):
        """Display real-time dashboard"""
        elapsed_mins = (time.time() - self.start_time) / 60
        recent_commits, changed_files = self.get_git_stats()
        total_fixes, current_loop, last_activity = self.get_quality_loop_stats()
        html_files = self.count_html_files()

        # Clear screen and display dashboard
        print("\033[2J\033[H")  # Clear screen and move cursor to top
        print("=" * 80)
        print("🎯 AGENT 10: CONTINUOUS QUALITY GATE COORDINATOR")
        print("=" * 80)
        print(f"⏰ Runtime: {elapsed_mins:.1f} minutes | Target: 120 minutes")
        print(f"📊 Dashboard Updates: {self.loop_count}")
        print(f"🕒 Current Time: {datetime.now().strftime('%H:%M:%S')}")
        print()

        print("📈 QUALITY LOOP METRICS")
        print("-" * 40)
        print(f"🔧 Total Fixes Applied: {total_fixes:,}")
        print(f"🔄 Current Loop: #{current_loop}")
        print(f"⚡ Last Activity: {last_activity}")
        print(f"📁 HTML Files Monitored: {html_files:,}")
        print()

        print("🔄 GIT COORDINATION")
        print("-" * 40)
        print(f"📝 Recent Commits (1hr): {recent_commits}")
        print(f"📄 Files Currently Changed: {changed_files}")
        print(f"🤝 Multi-Agent Status: {'🟢 Coordinated' if recent_commits > 0 else '🟡 Waiting'}")
        print()

        print("🎯 MISSION STATUS")
        print("-" * 40)
        completion_pct = min(100, (elapsed_mins / 120) * 100)
        status = "🟢 ACTIVE" if elapsed_mins < 120 else "🔴 OVERTIME"
        print(f"📋 Mission Status: {status}")
        print(f"📊 Progress: {completion_pct:.1f}% ({elapsed_mins:.1f}/120 min)")

        # Progress bar
        bar_width = 50
        filled = int(bar_width * completion_pct / 100)
        bar = "█" * filled + "░" * (bar_width - filled)
        print(f"🔲 Progress: [{bar}]")
        print()

        print("🚀 PERFORMANCE INDICATORS")
        print("-" * 40)
        fixes_per_min = total_fixes / max(elapsed_mins, 1)
        print(f"⚡ Fixes Per Minute: {fixes_per_min:.1f}")
        print(f"🎯 Quality Coverage: {(html_files/659)*100:.1f}% of ecosystem")

        if current_loop > 0:
            avg_fixes_per_loop = total_fixes / current_loop
            print(f"🔄 Avg Fixes Per Loop: {avg_fixes_per_loop:.1f}")

        print()

        # Status indicators
        indicators = []
        if total_fixes > 100:
            indicators.append("🔧 High Fix Rate")
        if recent_commits > 5:
            indicators.append("🤝 Multi-Agent Active")
        if changed_files == 0:
            indicators.append("✅ Clean Working Tree")
        if current_loop >= 2:
            indicators.append("🔄 Loop Stability")

        if indicators:
            print("🏆 SUCCESS INDICATORS")
            print("-" * 40)
            for indicator in indicators:
                print(f"  {indicator}")
            print()

        print("=" * 80)
        print(f"🔄 Next update in 30 seconds... | Loop #{self.loop_count + 1}")
        print("=" * 80)

    def run_dashboard(self):
        """Run real-time dashboard"""
        try:
            while True:
                self.loop_count += 1
                self.display_dashboard()

                # Check if main loop is still running
                elapsed = time.time() - self.start_time
                if elapsed > 7200:  # 2 hours
                    print("\n🏁 2-hour mission complete!")
                    break

                time.sleep(30)  # Update every 30 seconds

        except KeyboardInterrupt:
            print("\n\n🛑 Dashboard interrupted by user")
        except Exception as e:
            print(f"\n❌ Dashboard error: {e}")

if __name__ == "__main__":
    dashboard = QualityDashboard()
    dashboard.run_dashboard()